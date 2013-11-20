import unittest

from traits_enaml.testing.enaml_test_assistant import EnamlTestAssistant


class TestToolkitObject(EnamlTestAssistant, unittest.TestCase):
    """ Test the ToolkitObject interface. """

    def test_destroy(self):
        # The 'destroy' method should dispose the Qt control.

        enaml_source = """
from enaml.widgets.api import Label, MainWindow

enamldef MainView(MainWindow): win:
    Label:
        text = 'test'
"""

        view, toolkit_view = self.parse_and_create(enaml_source)
        label_control = self.find_toolkit_widget(toolkit_view, 'QtLabel')
        with self.delete_widget(label_control):
            view.destroy()
