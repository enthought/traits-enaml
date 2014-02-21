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
