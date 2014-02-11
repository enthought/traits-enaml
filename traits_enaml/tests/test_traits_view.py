#
# (C) Copyright 2013 Enthought, Inc., Austin, TX
# All right reserved.
#
# This file is open source software distributed according to the terms in
# LICENSE.txt
#
import unittest

from traits.api import HasTraits, Str

from traits_enaml.testing.enaml_test_assistant import EnamlTestAssistant


class Model(HasTraits):

    txt = Str('foo')


class TestTraitsView(EnamlTestAssistant, unittest.TestCase):

    def setUp(self):

        EnamlTestAssistant.setUp(self)

        enaml_source = """
from enaml.widgets.api import MainWindow
from traits_enaml.widgets.traits_view import TraitsView

enamldef MainView(MainWindow): win:
    attr model

    TraitsView:
        model = win.model
"""

        self.model = Model()

        view, toolkit_view = self.parse_and_create(enaml_source,
                                                   model=self.model)

        self.view = view
        self.traits_view = self.find_enaml_widget(view, "TraitsView")

    def tearDown(self):
        self.traits_view = None
        self.view = None
        self.model = None

        EnamlTestAssistant.tearDown(self)

    def test_disposing_traits_view(self):
        control = self.traits_view.ui.control

        self.view.destroy()
        self.assertEqual(self.traits_view.ui.control, None)

        self.assertEqual(control.parent(), None)
