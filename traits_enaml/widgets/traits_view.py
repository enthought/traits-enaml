#
# (C) Copyright 2013 Enthought, Inc., Austin, TX
# All right reserved.
#
# This file is open source software distributed according to the terms in
# LICENSE.txt
#
from traits.api import HasTraits
from traitsui.api import View

from atom.api import Typed, set_default

from enaml.core.declarative import d_
from enaml.widgets.raw_widget import RawWidget


class TraitsView(RawWidget):
    """ A widget which wraps a TraitsUI View on an object.

    :Attributes:
        **model** = `d_(Typed(HasTraits))`
            The HasTraits instance that we are using.
        **view** = `d_(Typed(View))`
            The View instance that we are using.
        **ui** = `Typed(HasTraits)`
            A reference to the TraitsUI UI object.
        **hug_width** = `set_default('weak')`
            TraitsViews hug their contents' width weakly by default.

    """

    #: The HasTraits instance that we are using.
    model = d_(Typed(HasTraits))

    #: The View instance that we are using.
    view = d_(Typed(View))

    #: A reference to the TraitsUI UI object.
    ui = Typed(HasTraits)

    #: TraitsViews hug their contents' width weakly by default.
    hug_width = set_default('weak')

    def create_widget(self, parent):
        self.ui = self.model.edit_traits(
            self.view, parent=parent, kind='subpanel')
        self.ui.control.setParent(parent)
        return self.ui.control

    def destroy_widget(self):
        control = self.ui.control
        if control is not None:
            control.setParent(None)
            self.ui.dispose()

    def destroy(self):
        """ A reimplemented destructor.

        This destructor disposes the TraitsUI object before proceeding with
        the regular Enaml destruction.

        """
        self.destroy_widget()
        super(TraitsView, self).destroy()
