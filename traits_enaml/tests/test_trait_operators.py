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
import six
import unittest

from traits.api import (
    Event, Float, HasTraits, Str, List, Dict, Set, Property)
from traits_enaml.testing.enaml_test_assistant import EnamlTestAssistant


class TraitModel(HasTraits):
    value = Float
    value_delegate = Str()
    value_subscribe = Str()
    value_update = Str()
    value_simple = Str('simple_text')
    value_notify = Event()
    list_values = List(Str)
    dict_values = Dict(Str, Str)
    set_values = Set(Str)
    property_value = Property(depends_on='value')
    typed_property_value = Property(Float, depends_on='value')
    collection_property_value = Property(List, depends_on='value')

    def _get_property_value(self):
        return self.value

    def _get_typed_property_value(self):
        return self.value

    def _get_collection_property_value(self):
        value = self.value
        return [value, value * 10]


class TraitOperatorsTestCase(EnamlTestAssistant, unittest.TestCase):

    def setUp(self):

        EnamlTestAssistant.setUp(self)

        enaml_source = """
from enaml.widgets.api import MainWindow, Field

enamldef MainView(MainWindow):
    attr model
    Field:
        name = 'test_op_delegate'
        text := model.value_delegate
    Field:
        name = 'test_op_subscribe'
        text << model.value_subscribe
    Field:
        name = 'test_op_update'
        text >> model.value_update
    Field:
        name = 'test_op_simple'
        text = model.value_simple
    Field:
        name = 'test_op_notify'
        text ::
            model.value_notify = True
    Field:
        name = 'test_list_subscribe'
        text << str(model.list_values)
    Field:
        name = 'test_dict_subscribe'
        text << str(model.dict_values)
    Field:
        name = 'test_set_subscribe'
        text << str(model.set_values)
    Field:
        name = 'test_property_subscribe'
        text << str(model.property_value)
    Field:
        name = 'test_typed_property_subscribe'
        text << str(model.typed_property_value)
    Field:
        name = 'test_collection_property_subscribe'
        text << str(model.collection_property_value)
"""
        self.model = TraitModel()
        view, toolkit_view = self.parse_and_create(
            enaml_source, model=self.model
        )

        self.view = view

    def tearDown(self):
        self.view = None
        self.model = None
        EnamlTestAssistant.tearDown(self)

    def test_op_delegate(self):

        enaml_widget = self.view.find('test_op_delegate')

        with self.assertTraitChanges(self.model, 'value_delegate'):
            enaml_widget.text = 'new_value'

        self.assertEquals(self.model.value_delegate, 'new_value')

        with self.assertAtomChanges(enaml_widget, 'text', count=1):
            self.model.value_delegate = 'updated_trait'

        self.assertEquals(enaml_widget.text, 'updated_trait')

    def test_op_subscribe(self):

        enaml_widget = self.view.find('test_op_subscribe')

        with self.assertTraitDoesNotChange(self.model, 'value_subscribe'):
            enaml_widget.text = 'new_value'

        with self.assertAtomChanges(enaml_widget, 'text', count=1):
            self.model.value_subscribe = 'updated_trait'

        self.assertEquals(enaml_widget.text, 'updated_trait')

    def test_op_update(self):

        enaml_widget = self.view.find('test_op_update')

        with self.assertTraitChanges(self.model, 'value_update'):
            enaml_widget.text = 'new_value'

        self.assertEquals(self.model.value_update, 'new_value')

        with self.assertAtomDoesNotChange(enaml_widget, 'text'):
            self.model.value_subscribe = 'updated_trait'

    def test_op_simple(self):

        enaml_widget = self.view.find('test_op_simple')

        self.assertEquals(self.model.value_simple, enaml_widget.text)
        self.assertEquals('simple_text', enaml_widget.text)

        with self.assertTraitDoesNotChange(self.model, 'value_simple'):
            enaml_widget.text = 'new_value'

        with self.assertAtomDoesNotChange(enaml_widget, 'text'):
            self.model.value_simple = 'updated_trait'

    def test_op_notify(self):

        enaml_widget = self.view.find('test_op_notify')

        with self.assertTraitChanges(self.model, 'value_notify'):
            enaml_widget.text = 'changing text'

        # Updating the text with the same value does not trigger the event
        with self.assertTraitDoesNotChange(self.model, 'value_notify'):
            enaml_widget.text = 'changing text'

        with self.assertTraitChanges(self.model, 'value_notify', count=1):
            enaml_widget.text = 'new text'

    def test_list_subscribe(self):

        enaml_widget = self.view.find('test_list_subscribe')

        with self.assertTraitDoesNotChange(self.model, 'list_values'):
            enaml_widget.text = 'new_value'

        # check on replace
        with self.assertAtomChanges(enaml_widget, 'text', count=1):
            self.model.list_values = ['1']
            self.assertEquals(enaml_widget.text, "['1']")

        # check on append
        with self.assertAtomChanges(enaml_widget, 'text', count=1):
            self.model.list_values.append('2')
            self.assertEquals(enaml_widget.text, "['1', '2']")

        # check on remove
        with self.assertAtomChanges(enaml_widget, 'text', count=1):
            self.model.list_values.remove('1')
            self.assertEquals(enaml_widget.text, "['2']")

    def test_dict_subscribe(self):

        enaml_widget = self.view.find('test_dict_subscribe')

        with self.assertTraitDoesNotChange(self.model, 'dict_values'):
            enaml_widget.text = 'new_value'

        # check on replace
        with self.assertAtomChanges(enaml_widget, 'text', count=1):
            self.model.dict_values = {'one': '1'}
            self.assertEquals(enaml_widget.text, "{'one': '1'}")

        # check on append
        with self.assertAtomChanges(enaml_widget, 'text', count=1):
            self.model.dict_values['two'] = '2'
            self.assertEquals(
                enaml_widget.text, str({'one': '1', 'two': '2'}))

        # check on remove
        with self.assertAtomChanges(enaml_widget, 'text', count=1):
            del self.model.dict_values['one']
            self.assertEquals(enaml_widget.text, "{'two': '2'}")

    def test_set_subscribe(self):

        enaml_widget = self.view.find('test_set_subscribe')

        with self.assertTraitDoesNotChange(self.model, 'set_values'):
            enaml_widget.text = 'new_value'

        # check on replace
        with self.assertAtomChanges(enaml_widget, 'text', count=1):
            self.model.set_values = {'1'}
            if six.PY2:
                expected = "TraitSetObject(['1'])"
            elif six.PY3:
                expected = "TraitSetObject({'1'})"
            self.assertEquals(enaml_widget.text, expected)

        # check on append
        with self.assertAtomChanges(enaml_widget, 'text', count=1):
            self.model.set_values.add('2')
            if six.PY2:
                expected = "TraitSetObject(['1', '2'])"
            elif six.PY3:
                expected = "TraitSetObject({'1', '2'})"
            self.assertEquals(enaml_widget.text, expected)

        # check on remove
        with self.assertAtomChanges(enaml_widget, 'text', count=1):
            self.model.set_values.remove('1')
            if six.PY2:
                expected = "TraitSetObject(['2'])"
            elif six.PY3:
                expected = "TraitSetObject({'2'})"
            self.assertEquals(enaml_widget.text, expected)

    def test_property_subscribe(self):

        enaml_widget = self.view.find('test_property_subscribe')

        with self.assertTraitDoesNotChange(self.model, 'property_value'):
            enaml_widget.text = 'new_value'

        # check on replace
        with self.assertAtomChanges(enaml_widget, 'text', count=1):
            self.model.value = 3.4
            self.assertEquals(enaml_widget.text, u"3.4")

    def test_typed_property_subscribe(self):

        enaml_widget = self.view.find('test_typed_property_subscribe')

        with self.assertTraitDoesNotChange(
                self.model, 'typed_property_value'):
            enaml_widget.text = 'new_value'

        # check on replace
        with self.assertAtomChanges(enaml_widget, 'text', count=1):
            self.model.value = 4.5
            self.assertEquals(enaml_widget.text, u"4.5")

    def test_collection_property_subscribe(self):

        enaml_widget = self.view.find('test_collection_property_subscribe')

        with self.assertTraitDoesNotChange(
                self.model, 'collection_property_value'):
            enaml_widget.text = 'new_value'

        # check on replace
        with self.assertAtomChanges(enaml_widget, 'text', count=1):
            self.model.value = 4.5
            self.assertEquals(enaml_widget.text, u"[4.5, 45.0]")
