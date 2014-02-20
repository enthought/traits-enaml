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

from enable.api import Component
from traits.api import HasTraits, Instance

from traits_enaml.testing.enaml_test_assistant import EnamlTestAssistant


class Model(HasTraits):

    component = Instance(Component)


class EnableCanvasTestCase(EnamlTestAssistant, unittest.TestCase):

    def setUp(self):

        EnamlTestAssistant.setUp(self)

        enaml_source = """
from enaml.widgets.api import MainWindow
from traits_enaml.widgets.enable_canvas import EnableCanvas

enamldef MainView(MainWindow):
    attr model

    EnableCanvas:
        name = 'canvas'
        component << model.component
"""
        self.component = Component()
        self.model = Model(component=self.component)

        view, toolkit_view = self.parse_and_create(
            enaml_source, model=self.model
        )

        self.view = view

    def tearDown(self):
        self.component = None
        self.view = None
        self.model = None

        EnamlTestAssistant.tearDown(self)

    def test_using_enable_canvas_widget(self):

        canvas = self.view.find('canvas')

        with self.assertAtomChanges(canvas, 'component'):
            self.model.component = Component()

        canvas = None

    def test_enable_canvas_proxy(self):

        from enaml.qt.qt_raw_widget import QtRawWidget

        canvas = self.view.find('canvas')
        # Check that the proxy is strictly a QtRawWidget (not a subclass).
        self.assertEqual(type(canvas.proxy), QtRawWidget)
