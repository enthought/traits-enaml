#
# (C) Copyright 2013 Enthought, Inc., Austin, TX
# All right reserved.
#
# This file is open source software distributed according to the terms in
# LICENSE.txt
#

""" This example fails on wx. It must be run with ETS_TOOLKIT=qt4. """

import enaml
from enaml.qt.qt_application import QtApplication


if __name__ == '__main__':
    with enaml.imports():
        from mayavi_canvas import Main

    app = QtApplication()
    view = Main()
    view.show()

    app.start()
