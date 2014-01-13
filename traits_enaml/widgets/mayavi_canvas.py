#------------------------------------------------------------------------------
#  Copyright (c) 2013, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
from atom.api import Bool, Typed, observe, set_default

from enaml.widgets.api import RawWidget
from enaml.core.declarative import d_

from traits.api import HasTraits, Instance, Bool as BoolTrait
from traitsui.api import View, Item, Handler

from tvtk.pyface.scene_editor import SceneEditor
from tvtk.pyface.scene_model import SceneModel


class MayaviModel(HasTraits):
    scene = Instance(SceneModel, ())
    view = View(Item('scene', editor=SceneEditor(), resizable=True,
                     show_label=False),
                resizable=True)


class ToolbarVisibilityHandler(Handler):
    #: Should the toolbar be visible?
    visible = BoolTrait

    def position(self, info):
        editor = info.ui.get_editors('scene')[0]
        editor._scene._tool_bar.setVisible(self.visible)


class MayaviCanvas(RawWidget):
    """ A widget that displays a mayavi scene.

    :Attributes:
        **scene** = *d_(Typed(SceneModel))*
            The mayavi scene model to be displayed.

    """
    #: The mayavi scene model to be displayed.
    scene = d_(Typed(SceneModel))

    #: If True, show the Mayavi toolbar
    show_toolbar = d_(Bool(True))

    #: The traits model that is used to create the mayavi UI
    _model = MayaviModel()

    #: Mayavi canvas' expand freely in width and height by default
    hug_width = set_default('ignore')
    hug_height = set_default('ignore')

    def initialize(self):
        super(MayaviCanvas, self).initialize()
        if self.scene is not None:
            self._model.scene = self.scene

    def create_widget(self, parent):
        handler = ToolbarVisibilityHandler(visible=self.show_toolbar)
        ui = self._model.edit_traits(kind='subpanel', handler=handler)
        widget = ui.control
        widget.setParent(parent)

        return widget

    @observe('scene')
    def scene_changed(self, change):
        self._model.scene = change['value']
