#
# (C) Copyright 2013 Enthought, Inc., Austin, TX
# All right reserved.
#
# This file is open source software distributed according to the terms in
# LICENSE.txt
#
from traits.api import HasTraits

from atom.api import Typed, set_default

from enaml.core.declarative import d_
from enaml.widgets.raw_widget import RawWidget


class TraitsView(RawWidget):
    """ A widget which wraps a TraitsUI View on an object.

    """
    # XXX should perhaps be subclassed from Control directly?
    
    #: The HasTraits instance that we are using
    model = d_(Typed(HasTraits))

    #: TraitsViews hug their contents' width weakly by default.
    hug_width = set_default('weak')

    def create_widget(self, parent):
        ui = self.model.edit_traits(kind='subpanel')
        # XXX this is dodgy, probably should have a proxy which holds the UI instance
        ui.control.setParent(parent)
        return ui.control

