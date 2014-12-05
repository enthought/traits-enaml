import unittest

import pandas
from numpy.testing import assert_array_equal

from traits_enaml.widgets.data_frame_table import ColumnCache


class TestColumnCache(unittest.TestCase):

    def setUp(self):
        self.data_frame = pandas.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})

    def tearDown(self):
        del self.data_frame

    def test_initialize(self):
        cache = ColumnCache(self.data_frame)
        assert_array_equal(cache.columns, [[1, 2, 3], [4, 5, 6]])
        self.assertIs(cache.data_frame, self.data_frame)

    def test_getitem(self):
        cache = ColumnCache(self.data_frame)
        self.assertEqual(cache[1, 0], 2)
        self.assertEqual(cache[0, 1], 4)

    def test_reset_with_new_data_frame(self):
        new_data_frame = pandas.DataFrame({'a': [3, 2, 1], 'b': [4, 6, 5]})
        cache = ColumnCache(self.data_frame)
        cache.reset(new_data_frame)
        assert_array_equal(cache.columns, [[3, 2, 1], [4, 6, 5]])
        self.assertIs(cache.data_frame, new_data_frame)

    def test_reset_as_update(self):
        cache = ColumnCache(self.data_frame)
        assert_array_equal(cache.columns, [[1, 2, 3], [4, 5, 6]])
        self.data_frame['b'] = [7, 8, 0]
        cache.reset()
        assert_array_equal(cache.columns, [[1, 2, 3], [7, 8, 0]])
        self.assertIs(cache.data_frame, self.data_frame)


if __name__ == "__main__":
    unittest.main()
