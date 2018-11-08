# Copyright (c) 2013 by Enthought Inc.
import io
import sys
import unittest

import traits_enaml
from traits_enaml.testing.enaml_test_assistant import (
    EnamlTestAssistant, print_enaml_widget_tree)

ENAML_SOURCE = """\
from enaml.widgets.main_window import MainWindow
from traits_enaml.testing.tests.enaml_test_container import EnamlTestContainer

enamldef MainView(MainWindow):
    attr some_attr
    EnamlTestContainer:
        name = "test_container"
    EnamlTestContainer:
        name = "test_container 2"
    EnamlTestContainer:
        name = "test_container 3"
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
        assistant = self.test_assistant
        try:
            assistant.parse_and_create(ENAML_SOURCE)
        except ImportError:
            self.fail(msg="Failed to set up enaml class.")

    def test_parse_and_create_kwargs(self):
        # Test that parse_and_create correctly passes along kwargs.
        assistant = self.test_assistant
        attr_value = 123
        view, _ = assistant.parse_and_create(
            ENAML_SOURCE, some_attr=attr_value)

        with assistant.event_loop():
            main_view = assistant.find_enaml_widget(view, "MainView")
            self.assertEqual(attr_value, main_view.some_attr)

    def test_find_all_enaml_widgets(self):
        assistant = self.test_assistant

        with traits_enaml.imports():
            from traits_enaml.testing.tests.enaml_test_container import (
                EnamlTestContainer)

        view, _ = assistant.parse_and_create(ENAML_SOURCE)

        with assistant.event_loop():
            widgets = assistant.find_all_enaml_widgets(
                view, "EnamlTestContainer")

        self.assertEqual(len(widgets), 3)
        for widget in widgets:
            self.assertIsInstance(widget, EnamlTestContainer)


class TestEnamlTestHelperFunctions(EnamlTestAssistant, unittest.TestCase):

    def test_print_enaml_widget_tree(self):
        view, _ = self.parse_and_create(ENAML_SOURCE)
        stream = io.StringIO()
        old_stdout = sys.stdout
        try:
            sys.stdout = stream
            print_enaml_widget_tree(view)
        finally:
            sys.stdout = old_stdout
            stream.close()
        lines = ''.join(stream.buflist).splitlines()
        # basic check we should have four items in the hierarchy.
        self.assertEqual(len(lines), 4)
