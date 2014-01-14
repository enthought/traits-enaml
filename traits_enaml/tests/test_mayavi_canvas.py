import unittest

from mayavi.core.ui.api import MlabSceneModel
from traits.api import HasTraits, Instance

from traits_enaml.testing.enaml_test_assistant import EnamlTestAssistant


class Model(HasTraits):

    scene = Instance(MlabSceneModel)


class MayaviCanvasTestCase(EnamlTestAssistant, unittest.TestCase):

    def setUp(self):

        EnamlTestAssistant.setUp(self)

        enaml_source = """
from enaml.widgets.api import MainWindow
from traits_enaml.widgets.mayavi_canvas import MayaviCanvas

enamldef MainView(MainWindow):
    attr model

    MayaviCanvas:
        name = 'canvas'
        scene << model.scene
        show_toolbar = False
"""
        self.scene = MlabSceneModel()
        self.model = Model(scene=self.scene)

        view, toolkit_view = self.parse_and_create(
            enaml_source, model=self.model
        )

        self.view = view

    def tearDown(self):
        self.scene = None
        self.view = None
        self.model = None

        EnamlTestAssistant.tearDown(self)

    def test_using_mayavi_canvas_widget(self):
        canvas = self.view.find('canvas')

        with self.assertAtomChanges(canvas, 'scene'):
            self.model.scene = MlabSceneModel()

        canvas = None
