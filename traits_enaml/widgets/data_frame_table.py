#----------------------------------------------------------------------------
#
#  Copyright (c) 2014, Enthought, Inc.
#  All rights reserved.
#
#  This software is provided without warranty under the terms of the BSD
#  license included in /LICENSE.txt and may be redistributed only
#  under the conditions described in the aforementioned license.  The license
#  is also available online at http://www.enthought.com/licenses/BSD.txt
#
#  Thanks for using Enthought open source!
#
#----------------------------------------------------------------------------
import numpy as np
from pandas import DataFrame

from atom.api import Typed, set_default, observe
from enaml.core.declarative import d_
from enaml.widgets.api import RawWidget

from pyface.qt.QtCore import QAbstractTableModel, QModelIndex, Qt
from pyface.qt.QtGui import (
    QTableView, QHeaderView, QAbstractItemView, QFontMetrics)


class ColumnCache(object):
    """ Pull out a view for each column for quick element access.

    """

    def __init__(self, data_frame):
        self.reset(data_frame)

    def __getitem__(self, ij):
        i, j = ij
        return self.columns[j][i]

    def reset(self, new_data_frame=None):
        """ Reset the cache.

        """
        if new_data_frame is not None:
            self.data_frame = new_data_frame
        ncols = len(self.data_frame.columns)
        self.columns = [None] * ncols
        for data_block in self.data_frame._data.blocks:
            for i, ref_loc in enumerate(data_block.mgr_locs):
                self.columns[ref_loc] = data_block.values[i, :]

    def clear(self):
        """ Clear out the cache entirely.

        """
        del self.data_frame
        del self.columns


class QDataFrameModel(QAbstractTableModel):
    def __init__(self, data_frame, *args, **kwds):
        self.data_frame = data_frame
        self.cache = ColumnCache(data_frame)
        self.argsort_indices = None
        self.default_decimals = 6
        super(QDataFrameModel, self).__init__(*args, **kwds)

    def headerData(self, section, orientation, role):
        if role == Qt.TextAlignmentRole:
            if orientation == Qt.Horizontal:
                return int(Qt.AlignHCenter | Qt.AlignVCenter)
            return int(Qt.AlignRight | Qt.AlignVCenter)
        elif role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._get_unicode_string(
                    self.data_frame.columns[section])
            else:
                if self.argsort_indices is not None:
                    section = self.argsort_indices[section]
                return self._get_unicode_string(self.data_frame.index[section])
        else:
            return None

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or \
                not (0 <= index.row() < len(self.data_frame)):
            return None
        if role == Qt.DisplayRole:
            formatted = self._get_formatted_value(index.row(), index.column())
            return formatted
        elif role == Qt.TextAlignmentRole:
            return int(Qt.AlignRight | Qt.AlignVCenter)
        else:
            return None

    def columnCount(self, index=QModelIndex()):
        if not index.isValid():
            return len(self.data_frame.columns)
        else:
            return 0

    def rowCount(self, index=QModelIndex()):
        if not index.isValid():
            return len(self.data_frame.index)
        else:
            return 0

    def sort(self, column, order=Qt.AscendingOrder):
        if column == -1:
            # Return to unsorted.
            if self.argsort_indices is not None:
                self.argsort_indices = None
                self._emit_all_data_changed()
            return

        if len(self.cache.columns) == 0:
            return

        ascending = (order == Qt.AscendingOrder)
        data = self.cache.columns[column]
        # If things are currently sorted, we will try to be stable
        # relative to that order, not the original data's order.
        if self.argsort_indices is not None:
            data = data[self.argsort_indices]
        if ascending:
            indices = np.argsort(data, kind='mergesort')
        else:
            # Do the double-reversing to maintain stability.
            indices = (len(data) - 1 -
                       np.argsort(data[::-1], kind='mergesort')[::-1])
            if np.issubdtype(data.dtype, np.dtype(np.floating)):
                # The block of NaNs is now at the beginning. Move it to
                # the bottom.
                num_nans = np.isnan(data).sum()
                if num_nans > 0:
                    indices = np.roll(indices, -num_nans)
        if self.argsort_indices is not None:
            indices = self.argsort_indices[indices]
        self.argsort_indices = indices
        self._emit_all_data_changed()

    def _emit_all_data_changed(self):
        """ Emit signals to note that all data has changed, e.g. by sorting.

        """
        self.dataChanged.emit(
            self.index(0, 0),
            self.index(len(self.data_frame.index) - 1,
                       len(self.data_frame.columns) - 1),
        )
        self.headerDataChanged.emit(
            Qt.Vertical,
            0,
            len(self.data_frame.index) - 1,
        )

    def format_value(self, value):
        """ Return a nice unicode formatting of the given value.

        """
        if isinstance(value, (float, np.floating)):
            if np.isnan(value):
                return u'--'
        return self._get_unicode_string(value)

    def _get_formatted_value(self, i, j):
        if self.argsort_indices is not None:
            i = self.argsort_indices[i]
        value = self.cache[i, j]
        formatted = self.format_value(value)
        return formatted

    def _get_unicode_string(self, value):
        if isinstance(value, str):
            try:
                return unicode(value, encoding='utf-8')
            except UnicodeDecodeError:
                return unicode(value, encoding='latin-1')
        else:
            return unicode(value)


class QDataFrameTableView(QTableView):
    """ View a pandas DataFrame in a table.

    """

    def __init__(self, df_model, parent=None, **kwds):
        super(QDataFrameTableView, self).__init__(parent=parent, **kwds)
        self.df_model = df_model
        self.setModel(df_model)
        self._setup_sorting()
        self._setup_selection()
        self._setup_scrolling()
        self._setup_headers()
        self._setup_style()

    @classmethod
    def from_data_frame(cls, df, **kwds):
        """ Instantiate a DataFrameTableView directly from a DataFrame.

        """
        df_model = QDataFrameModel(df)
        self = cls(df_model, **kwds)
        return self

    def _setup_sorting(self):
        self.sortByColumn(-1, Qt.AscendingOrder)
        self.setSortingEnabled(True)

    def _setup_selection(self):
        self.selection_model = self.selectionModel()
        self.setSelectionMode(QAbstractItemView.ContiguousSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectItems)

    def _setup_scrolling(self):
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerItem)

    def _setup_headers(self):
        self.vheader = QHeaderView(Qt.Vertical)
        self.setVerticalHeader(self.vheader)
        font = self.vheader.font()
        font.setBold(True)
        fmetrics = QFontMetrics(font)
        max_width = fmetrics.width(u" {0} ".format(
            unicode(self.df_model.rowCount())))
        self.vheader.setMinimumWidth(max_width)
        self.vheader.setClickable(True)
        self.vheader.setStretchLastSection(False)
        self.vheader.setResizeMode(QHeaderView.Fixed)

        self.hheader = self.horizontalHeader()
        self.hheader.setStretchLastSection(False)
        self.hheader.setClickable(True)
        self.hheader.setMovable(True)

    def _setup_style(self):
        self.setWordWrap(False)


class DataFrameTable(RawWidget):
    """ A widget that displays a table view tied to a pandas DataFrame.

    """
    #: The data frame to display
    data_frame = d_(Typed(DataFrame))

    #: Expand the table by default
    hug_width = set_default('weak')
    hug_height = set_default('weak')

    def create_widget(self, parent):
        """ Create the DataFrameTable Qt widget.

        """
        return QDataFrameTableView.from_data_frame(
            self.data_frame, parent=parent)

    @observe('data_frame')
    def _data_frame_changed(self, change):
        """ Proxy changes in `data_frame` down to the Qt widget.

        """
        table = self.get_widget()
        if table is not None:
            df_model = QDataFrameModel(change['value'])
            table = self.get_widget()
            table.df_model = df_model
            table.setModel(df_model)
