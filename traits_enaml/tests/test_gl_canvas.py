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
import unittest

import numpy as np

from traits_enaml.testing.enaml_test_assistant import EnamlTestAssistant


class GLCanvasTestCase(EnamlTestAssistant, unittest.TestCase):

    def setUp(self):

        EnamlTestAssistant.setUp(self)

        enaml_source = """
from OpenGL import GL

from enaml.widgets.api import MainWindow
from traits_enaml.widgets.gl_canvas import GLCanvas

enamldef MainView(MainWindow): main:
    GLCanvas: canvas:
        init_gl => ():
            GL.glClearColor(0.0, 1.0, 0.0, 1.0)
        draw_gl => ():
            GL.glClear(GL.GL_COLOR_BUFFER_BIT)
"""
        view, toolkit_view = self.parse_and_create(enaml_source)
        self.view = view
        view.show()

    def tearDown(self):
        self.view = None
        EnamlTestAssistant.tearDown(self)

    def test_gl_canvas_proxy(self):
        from enaml.qt.qt_raw_widget import QtRawWidget

        canvas = self.view.children[0]
        # Check that the proxy is strictly a QtRawWidget (not a subclass).
        self.assertEqual(type(canvas.proxy), QtRawWidget)

    def test_gl_canvas_draw(self):
        canvas = self.view.children[0]
        widget = canvas.get_widget()

        with self.event_loop():
            canvas.update()

        image = widget.grabFrameBuffer()
        width, height = image.width(), image.height()
        arr = np.array(image.constBits()).reshape(height, width, 4)

        expected = np.zeros((height, width, 4), dtype='uint8')
        expected[:, :, 1] = 255
        expected[:, :, 3] = 255

        np.testing.assert_array_equal(arr, expected)
