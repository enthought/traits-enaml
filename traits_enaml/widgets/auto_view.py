#
# (C) Copyright 2013 Enthought, Inc., Austin, TX
# All right reserved.
#
# This file is open source software distributed according to the terms in
# LICENSE.txt
#

from collections import namedtuple
from datetime import date, time
from string import capwords

from traits.api import (BaseInstance, Bool, Button, Enum, Event, Float, Int,
                        Range, Str)
import traits_enaml

with traits_enaml.imports():
    from enaml.widgets.api import Label
    from traits_enaml.widgets.auto_editors import (
        AutoView, AutoWindow, BoolEditor, ButtonEditor,
        DateEditor, EnumEditor, FloatEditor, FloatRangeEditor,
        IntEditor, IntRangeEditor, StrEditor, TimeEditor,
        DefaultEditor)

TraitDesc = namedtuple('TraitDesc', 'name trait_type label tooltip editor')

# Dictionary from trait_type -> enaml component factories.
TRAIT2ENAML = {
    Bool: lambda trait_type: BoolEditor,
    Button: lambda trait_type: ButtonEditor,
    Enum: lambda trait_type: EnumEditor,
    Float: lambda trait_type: FloatEditor,
    Int: lambda trait_type: IntEditor,
    Str: lambda trait_type: StrEditor,
    Range: lambda trait_type: _range_editor_factory(trait_type),
    BaseInstance: lambda trait_type: _time_editor_factory(trait_type)}


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
    else:
        trait_type = trait_desc.trait_type
        for key, factory in TRAIT2ENAML.iteritems():
            if isinstance(trait_type, key):
                break
        else:
            factory = lambda trait: DefaultEditor
        editor = factory(trait_type)
        return editor(**kwargs)


def _range_editor_factory(trait_type):
    low, high = trait_type._low, trait_type._high
    if isinstance(low, float) and isinstance(high, float):
        return FloatRangeEditor
    elif isinstance(low, int) and isinstance(high, int):
        return IntRangeEditor
    else:
        return DefaultEditor


def _time_editor_factory(trait_type):
    klass = trait_type.klass
    if klass is time:
        return TimeEditor
    elif klass is date:
        return DateEditor
    else:
        return DefaultEditor


def _model_traits(model):
    traits = []
    names = [
        name for name in model.class_trait_names()
        if not name.startswith('_')]
    for name in names:
        trait = model.trait(name)
        if type(trait.trait_type) is Event:
            continue
        label = trait.label or capwords(name.replace('_', ' '))
        tooltip = trait.tooltip
        editor = trait.enaml_editor
        desc = TraitDesc(name, trait.trait_type, label, tooltip, editor)
        traits.append(desc)
    return traits
