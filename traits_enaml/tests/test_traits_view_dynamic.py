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
