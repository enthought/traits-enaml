#
# (C) Copyright 2014 Enthought, Inc., Austin, TX
# All right reserved.
#
# This file is open source software distributed according to the terms in
# LICENSE.txt
#

""" This example fails on wx. It must be run with ETS_TOOLKIT=qt4. """

import numpy as np
import pandas

import enaml
from enaml.qt.qt_application import QtApplication


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
        choices = np.array(['foo', 'bar', 'baz', 'fake', 'random'],
                           dtype=object)
        data = choices[np.random.randint(0, len(choices), size=nrows)]
        return data

    def random_integers(nrows):
        data = np.random.randint(0, 10000, size=nrows)
        return data

    def random_floats(nrows):
        digits = np.random.randint(1, 6)
        data = np.power(10, np.random.normal(digits, 0.2, size=nrows))
        i = np.random.randint(0, nrows, size=nrows // 20)
        data[i] = np.nan
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

    return pandas.DataFrame(series, columns=columns)


if __name__ == '__main__':
    with enaml.imports():
        from data_frame_view import Main

    app = QtApplication()
    view = Main(df=create_data_frame(10000, 40))
    view.show()

    app.start()
