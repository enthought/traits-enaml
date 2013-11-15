# Copyright (c) 2013 by Enthought Inc.

import unittest
from traits_enaml.testing.enaml_test_assistant import EnamlTestAssistant

ENAML_SOURCE = """\
from enaml.widgets.main_window import MainWindow
from traits_enaml.testing.tests.enaml_test_container import EnamlTestContainer

enamldef MainView(MainWindow):
    attr some_attr
    EnamlTestContainer:
        name = "test_container"
"""


class TestEnamlTestAssistant(unittest.TestCase):
    def setUp(self):
        self.test_assistant = EnamlTestAssistant()
        self.test_assistant.setUp()

    def tearDown(self):
        self.test_assistant.tearDown()

    def test_parse_and_create(self):
        # Check that parse_and_create is able to create enaml objects
        # which refer to other enaml files.
        try:
            self.test_assistant.parse_and_create(ENAML_SOURCE)
        except ImportError:
            self.fail(msg="Failed to set up enaml class.")

    def test_parse_and_create_kwargs(self):
        # Test that parse_and_create correctly passes along kwargs.
        attr_value = 123
        view, _ = self.test_assistant.parse_and_create(ENAML_SOURCE,
                                                       some_attr=attr_value)

        with self.test_assistant.event_loop():
            main_view = self.test_assistant.find_enaml_widget(view, "MainView")
            self.assertEqual(attr_value, main_view.some_attr)
