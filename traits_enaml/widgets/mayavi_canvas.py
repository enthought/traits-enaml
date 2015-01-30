#------------------------------------------------------------------------------
#  Copyright (c) 2013, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
from atom.api import Bool, Typed, observe, set_default
from enaml.core.declarative import d_

from traits.api import Instance, HasStrictTraits
from traitsui.api import View, Item
from tvtk.pyface.scene_editor import SceneEditor
from tvtk.pyface.scene_model import SceneModel

from mayavi.core.ui.mayavi_scene import MayaviScene

from .traits_view import TraitsView


class MayaviModel(HasStrictTraits):
    scene = Instance(SceneModel, args=())
    view = View(
        Item('scene', editor=SceneEditor(scene_class=MayaviScene), resizable=True, show_label=False),
        resizable=True)


class MayaviCanvas(TraitsView):
    """ A traits view widget that displays a mayavi scene.

    :Attributes:
        **scene** = *d_(Typed(SceneModel))*
            The mayavi scene model to be displayed.
        **show_toolbar** = *d_(Bool(True))*
            If True, show the Mayavi toolbar.

    """
    #: The mayavi scene model to be displayed.
    scene = d_(Typed(SceneModel))

    #: If True, show the Mayavi toolbar.
    show_toolbar = d_(Bool(True))

    #: The readonly instance of the model used for the traits_view.
    model = d_(Typed(MayaviModel), writable=False)

    #: The readonly instance of the view.
    view = d_(Typed(View), writable=False)

    #: Mayavi canvas expands freely in width and height by default.
    hug_width = set_default('ignore')
    hug_height = set_default('ignore')

    def create_widget(self, parent):
        control = super(MayaviCanvas, self).create_widget(parent)
        self.show_toolbar_changed({'value': self.show_toolbar})
        return control

    def _default_model(self):
        return MayaviModel(scene=self.scene)

    def _default_view(self):
        return self.model.trait_view()

    @observe('scene')
    def scene_changed(self, change):
        self.model.scene = change['value']

    @observe('show_toolbar')
    def show_toolbar_changed(self, change):
        ui = self.ui
        if ui is not None and ui.control is not None:
            editor = ui.get_editors('scene')[0]
            editor._scene._tool_bar.setVisible(change['value'])
