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
from traits_enaml.widgets.traits_view import TraitsView


class Model(HasTraits):

    txt = Str('foo')


class TestTraitsViewDynamic(EnamlTestAssistant, unittest.TestCase):

    def setUp(self):

        EnamlTestAssistant.setUp(self)

        enaml_source = """
from enaml.widgets.api import MainWindow
from enaml.core.api import Include

enamldef MainView(MainWindow): win:
    attr traits_view


    Include:
        objects << [traits_view] if traits_view is not None else []
"""

        view, toolkit_view = self.parse_and_create(enaml_source)
        self.view = view

    def tearDown(self):
        self.view = None
        self.model = None

        EnamlTestAssistant.tearDown(self)

    def test_add_traits_view(self):
        traits_view = TraitsView(model=Model())
        with self.event_loop():
            self.view.show()
        with self.event_loop():
            self.view.traits_view = traits_view
        self.assertEqual(traits_view.ui.rebuild.__name__, 'ui_subpanel')


if __name__ == "__main__":
    unittest.main()
