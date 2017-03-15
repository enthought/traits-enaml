#----------------------------------------------------------------------------
#
#  Copyright (c) 2013-17, Enthought, Inc.
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
import numpy

from enaml.qt.QtCore import Qt

from traits_enaml.widgets.data_frame_table import QDataFrameModel


def create_data_frame(nrows, ncols):
    """ Create a test pandas DataFrame.

    Parameters:
    -----------
    nrows : int
        The number of rows to create.

    ncols : int
        The number of columns to create.

    Returns:
    --------
    A pandas DataFrame with randomized data of size (nrows, ncols).

    """
    def random_strings(nrows):
        choices = numpy.array(
            ['foo', 'bar', 'baz', 'fake', 'random'],
            dtype=object)
        data = choices[numpy.random.randint(0, len(choices), size=nrows)]
        return data

    def random_integers(nrows):
        data = numpy.random.randint(0, 10000, size=nrows)
        return data

    def random_floats(nrows):
        digits = numpy.random.randint(1, 6)
        data = numpy.power(10, numpy.random.normal(digits, 0.2, size=nrows))
        i = numpy.random.randint(0, nrows, size=nrows // 20)
        data[i] = numpy.nan
        return data

    from itertools import cycle, islice
    series = {}
    columns = []
    random_funcs = cycle([
        ('s', random_strings),
        ('i', random_integers),
        ('f', random_floats),
        ('f', random_floats),
        ('f', random_floats),
    ])
    for i, (code, func) in enumerate(islice(random_funcs, 0, ncols), 1):
        name = '{}col{:04d}'.format(code, i)
        series[name] = func(nrows)
        columns.append(name)

    return pandas.DataFrame(data=series, columns=columns)


class TestQDataFrameModel(unittest.TestCase):

    def setUp(self):
        self.data_frame = create_data_frame(10, 7)
        self.q_model = QDataFrameModel(data_frame=self.data_frame)

    def tearDown(self):
        del self.data_frame
        del self.q_model

    def test_column_header_aligment(self):
        # given
        model = self.q_model
        role = Qt.TextAlignmentRole
        section = None  # all sections
        orientation = Qt.Horizontal

        # when/then
        self.assertEqual(
            model.headerData(section, orientation, role),
            int(Qt.AlignHCenter | Qt.AlignVCenter))

        # when
        section = 1

        # then
        self.assertEqual(
            model.headerData(section, orientation, role),
            int(Qt.AlignHCenter | Qt.AlignVCenter))

    def test_row_header_aligment(self):
        # given
        model = self.q_model
        role = Qt.TextAlignmentRole
        section = None  # all sections
        orientation = Qt.Vertical

        # when/then
        self.assertEqual(
            model.headerData(section, orientation, role),
            int(Qt.AlignRight | Qt.AlignVCenter))

        # when
        section = 1
        # then
        self.assertEqual(
            model.headerData(section, orientation, role),
            int(Qt.AlignRight | Qt.AlignVCenter))

    def test_column_header_name(self):
        # given
        model = self.q_model
        role = Qt.DisplayRole
        section = 1  # all sections

        # when
        orientation = Qt.Horizontal

        # then
        self.assertEqual(
            model.headerData(section, orientation, role), u"icol0002")

    def test_row_header_name(self):
        # given
        model = self.q_model
        role = Qt.DisplayRole
        section = 1  # all sections

        # when
        orientation = Qt.Vertical

        # then
        self.assertEqual(
            model.headerData(section, orientation, role), u"1")

    def test_column_count(self):
        # given
        model = self.q_model

        # when/then
        self.assertEqual(model.columnCount(), 7)

        # when/then
        index = model.index(1233, 0)
        self.assertEqual(model.columnCount(index), 7)

        # when/then
        index = model.index(1, 1)
        self.assertEqual(model.columnCount(index), 0)

    def test_row_count(self):
        # given
        model = self.q_model

        # when/then
        self.assertEqual(model.rowCount(), 10)

        # when/then
        index = model.index(1233, 0)
        self.assertEqual(model.rowCount(index), 10)

        # when/then
        index = model.index(1, 1)
        self.assertEqual(model.rowCount(index), 0)

    def test_sort_ascending(self):
        # given
        model = self.q_model
        data_frame = self.data_frame


if __name__ == "__main__":
    unittest.main()
