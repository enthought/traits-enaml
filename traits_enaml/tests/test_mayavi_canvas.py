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

from mayavi.core.ui.api import MlabSceneModel

from traits_enaml.testing.enaml_test_assistant import EnamlTestAssistant


class MayaviCanvasTestCase(EnamlTestAssistant, unittest.TestCase):

    def setUp(self):

        EnamlTestAssistant.setUp(self)

        enaml_source = """
from enaml.widgets.api import MainWindow
from traits_enaml.widgets.mayavi_canvas import MayaviCanvas

enamldef MainView(MainWindow):
    attr scene

    MayaviCanvas:
        scene << parent.scene

"""
        self.scene = MlabSceneModel()
        self.view, _ = self.parse_and_create(enaml_source, scene=self.scene)
        self.canvas = self.find_enaml_widget(self.view, 'MayaviCanvas')

    def tearDown(self):
        self.canvas = None
        self.view = None
        self.scene = None
        EnamlTestAssistant.tearDown(self)

    def test_updating_the_scene(self):
        canvas = self.canvas

        with self.assertTraitChanges(canvas.model, 'scene', count=1):
            canvas.scene = MlabSceneModel()
        self.assertEqual(canvas.model.scene, canvas.scene)

    def test_toggling_the_mayavi_toolbar(self):
        canvas = self.canvas
        editor = canvas.ui.get_editors('scene')[0]
        toolbar = editor._scene._tool_bar

        # show the view
        with self.event_loop():
            self.view.show()

        # toggle the toolbar
        with self.event_loop():
            canvas.show_toolbar = False
        self.assertFalse(toolbar.isVisible())
        with self.event_loop():
            canvas.show_toolbar = True
        self.assertTrue(toolbar.isVisible())


if __name__ == "__main__":
    unittest.main()
