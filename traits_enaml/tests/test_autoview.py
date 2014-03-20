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
import datetime

import traits_enaml
from traits.api import (
    Bool, Button, Date, Enum, Float, Int, HasTraits, List, Range, Str, Time,
    Tuple)
from traits_enaml.testing.enaml_test_assistant import EnamlTestAssistant
from traits_enaml.widgets.auto_view import auto_window, auto_view

with traits_enaml.imports():
    from traits_enaml.widgets.auto_view import DefaultEditor


class AllTypes(HasTraits):
    """ A simple class with all kinds of traits

    """
    boolean_value = Bool(True, label="Custom Bool Label:")
    button_value = Button("I'm a button!")
    int_value = Int(42, tooltip="You can add a tooltip as well.")
    float_value = Float(3.141592)
    enum_value = Enum("foo", "bar", "baz", "qux")
    int_range_value = Range(low=0, high=10)
    float_range_value = Range(low=0.0, high=1.0)
    list_value = List([0, 1, 2])
    str_value = Str("Word")
    date_value = Date(datetime.date.today())
    time_value = Time(datetime.time())
    range_value = Range(low=0, high=100,
                        label="Traits Range Editor:",
                        enaml_editor=DefaultEditor)

    _notifications = List(Tuple)


class TestAutoView(EnamlTestAssistant, unittest.TestCase):

    def test_auto_view(self):
        with traits_enaml.imports():
            from enaml.widgets.api import Window

        model = AllTypes()
        window = Window()
        window.insert_children(None, (auto_view(model=model),))
        with self.event_loop():
            window.show()
        self.check_component_counts(window)
        self.check_label_text(window)

    def test_auto_window(self):
        model = AllTypes()
        window = auto_window(model=model)
        with self.event_loop():
            window.show()
        self.check_component_counts(window)
        self.check_label_text(window)

    def check_component_counts(self, view):
        expected_counts = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 12]
        components = [
            'BoolEditor', 'ButtonEditor', 'DateEditor',
            'EnumEditor', 'FloatEditor', 'FloatRangeEditor',
            'IntEditor', 'IntRangeEditor', 'StrEditor',
            'TimeEditor', 'DefaultEditor', 'Label']
        for index, component in enumerate(components):
            items = self.find_all_enaml_widgets(view, component)
            self.assertEqual(len(items), expected_counts[index])

    def check_label_text(self, view):
        labels = [
            'Custom Bool Label:', 'Button Value', 'Date Value',
            'Enum Value', 'Float Value', 'Float Range Value',
            'Int Value', 'Int Range Value', 'Str Value',
            'Time Value', 'Traits Range Editor:', 'List Value']
        components = self.find_all_enaml_widgets(view, 'Label')
        self.assertEqual(len(components), 12)
        components_text = [component.text for component in components]
        self.assertItemsEqual(components_text, labels)
