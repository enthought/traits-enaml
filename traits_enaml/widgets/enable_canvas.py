#------------------------------------------------------------------------------
#  Copyright (c) 2013, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
from atom.api import Typed, observe, set_default
from enable.api import Window, Component

from enaml.widgets.api import RawWidget
from enaml.core.declarative import d_


class EnableCanvas(RawWidget):
    """ A widget that displays an enable component

    """
    #: The enable component to be displayed
    component = d_(Typed(Component))

    #: Internal storage for the enable window
    _window = Typed(Window)

    #: Enable canvas' expand freely in width and height by default
    hug_width = set_default('ignore')
    hug_height = set_default('ignore')

    def create_widget(self, parent):
        if self.component is not None:
            self._window = Window(parent, component=self.component,
                                  bgcolor=self.component.bgcolor)
            enable_widget = self._window.control
        else:
            self._window = None
            enable_widget = None

        return enable_widget

    @observe('component')
    def component_changed(self, new):
        self._window.component = new['value']
