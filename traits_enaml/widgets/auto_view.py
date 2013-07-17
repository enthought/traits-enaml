#
# (C) Copyright 2013 Enthought, Inc., Austin, TX
# All right reserved.
#
# This file is open source software distributed according to the terms in
# LICENSE.txt
#

from collections import namedtuple
from datetime import date, time

from traits.api import (BaseInstance, Bool, Button, Enum, Event, Float, Int,
                        Range, Str)
import traits_enaml

with traits_enaml.imports():
    from enaml.widgets.api import Label
    from traits_enaml.widgets.auto_editors import (AutoView, AutoWindow,
                                                   BoolEditor, ButtonEditor,
                                                   DateEditor, EnumEditor,
                                                   FloatEditor,
                                                   FloatRangeEditor, IntEditor,
                                                   IntRangeEditor, StrEditor,
                                                   TimeEditor, DefaultEditor)

TraitDesc = namedtuple('TraitDesc', 'name trait_type label tooltip editor')


def auto_view(model):
    """ Generate a view directly from a `HasTraits` instance.
    """
    descriptions = _model_traits(model)
    labels = [Label(text=desc.label) for desc in descriptions]
    editors = [_get_editor(model, desc) for desc in descriptions]
    objects = [widget for pair in zip(labels, editors) for widget in pair]
    return AutoView(objects=objects)


def auto_window(model):
    """ Generate a window directly from a `HasTraits` instance.
    """
    return AutoWindow(view=auto_view(model))


def _get_editor(model, trait_desc):
    kwargs = {'model': model, 'trait_desc': trait_desc}
    if trait_desc.tooltip:
        kwargs['tool_tip'] = trait_desc.tooltip

    if trait_desc.editor:
        return trait_desc.editor(**kwargs)
    elif isinstance(trait_desc.trait_type, Bool):
        return BoolEditor(**kwargs)
    elif isinstance(trait_desc.trait_type, Button):
        return ButtonEditor(**kwargs)
    elif (isinstance(trait_desc.trait_type, BaseInstance) and
            trait_desc.trait_type.klass is date):
        return DateEditor(**kwargs)
    elif isinstance(trait_desc.trait_type, Enum):
        return EnumEditor(**kwargs)
    elif isinstance(trait_desc.trait_type, Float):
        return FloatEditor(**kwargs)
    elif (isinstance(trait_desc.trait_type, Range) and
            (isinstance(trait_desc.trait_type._low, float) or
             isinstance(trait_desc.trait_type._high, float))):
        return FloatRangeEditor(**kwargs)
    elif isinstance(trait_desc.trait_type, Int):
        return IntEditor(**kwargs)
    elif (isinstance(trait_desc.trait_type, Range) and
            isinstance(trait_desc.trait_type._low, int) and
            isinstance(trait_desc.trait_type._high, int)):
        return IntRangeEditor(**kwargs)
    elif isinstance(trait_desc.trait_type, Str):
        return StrEditor(**kwargs)
    elif (isinstance(trait_desc.trait_type, BaseInstance) and
            trait_desc.trait_type.klass is time):
        return TimeEditor(**kwargs)

    return DefaultEditor(**kwargs)


def _model_traits(model):
    traits = []
    for name in model.class_trait_names():
        trait = model.trait(name)
        if type(trait.trait_type) is Event:
            continue
        label = trait.label or " ".join(name.split('_')).capitalize()
        tooltip = trait.tooltip
        editor = trait.enaml_editor
        desc = TraitDesc(name, trait.trait_type, label, tooltip, editor)
        traits.append(desc)
    return traits
