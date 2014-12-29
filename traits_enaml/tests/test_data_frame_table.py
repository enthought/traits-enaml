#----------------------------------------------------------------------------
#
#  Copyright (c) 2013-14, Enthought, Inc.
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
import unittest

import pandas

from pyface.qt.QtCore import Qt

from traits_enaml.widgets.data_frame_table import ColumnCache
from traits_enaml.testing.enaml_test_assistant import EnamlTestAssistant


class DataFrameTableTestCase(EnamlTestAssistant, unittest.TestCase):

    def setUp(self):
        EnamlTestAssistant.setUp(self)

        enaml_source = """
from enaml.widgets.api import MainWindow
from traits_enaml.widgets.data_frame_table import DataFrameTable

enamldef MainView(MainWindow):
    attr df

    DataFrameTable:
        data_frame << parent.df

"""
        self.data_frame = pandas.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
        self.view, _ = self.parse_and_create(enaml_source, df=self.data_frame)
        self.table = self.find_enaml_widget(self.view, 'DataFrameTable')

    def tearDown(self):
        self.data_frame = None
        self.view = None
        self.table = None
        EnamlTestAssistant.tearDown(self)

    def test_updating_the_data_frame(self):
        table = self.table

        new_df = pandas.DataFrame()
        table.data_frame = new_df

        self.assert_(table.proxy.widget.model().data_frame is new_df)

    def test_column_cache(self):
        cache = ColumnCache(self.data_frame)

        self.assert_(cache[1, 0] == 2)

        cache.clear()
        self.assert_(not hasattr(cache, 'data_frame') and
                     not hasattr(cache, 'columns'))

    def test_sort(self):
        qtable = self.table.proxy.widget
        qtable.sortByColumn(0, Qt.DescendingOrder)
        qmodel = qtable.model()
        self.assert_(int(qmodel.data(qmodel.createIndex(0, 0))) == 3)

    def test_invalid_index(self):
        qmodel = self.table.proxy.widget.model()
        self.assert_(qmodel.data(qmodel.createIndex(-1, -1)) is None)

if __name__ == "__main__":
    unittest.main()
