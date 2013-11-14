import unittest

from traits.api import Event, HasTraits, Str
from traits_enaml.testing.enaml_test_assistant import EnamlTestAssistant

class TraitModel(HasTraits):
    value_delegate = Str()
    value_subscribe = Str()
    value_update = Str()
    value_simple = Str('simple_text')
    value_notify = Event()

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
"""
        self.model = TraitModel()
        view, toolkit_view = self.parse_and_create(
            enaml_source, model=self.model
        )

        self.view = view

    def tearDown(self):
        self.enaml_widget = None
        self.toolkit_widget = None
        EnamlTestAssistant.tearDown(self)


    def test_op_delegate(self):

        enaml_widget = self.view.find('test_op_delegate')

        with self.assertTraitChanges(self.model, 'value_delegate'):
            enaml_widget.text = 'new_value'

        self.assertEquals(self.model.value_delegate, 'new_value')

        with self.assertAtomChanges(enaml_widget, 'text'):
            self.model.value_delegate = 'updated_trait'

        self.assertEquals(enaml_widget.text, 'updated_trait')

    def test_op_subscribe(self):

        enaml_widget = self.view.find('test_op_subscribe')

        with self.assertTraitDoesNotChange(self.model, 'value_subscribe'):
            enaml_widget.text = 'new_value'

        with self.assertAtomChanges(enaml_widget, 'text'):
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

        with self.assertTraitChanges(self.model, 'value_notify'):
            enaml_widget.text = 'new text'

