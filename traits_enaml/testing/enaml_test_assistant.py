# Copyright (c) 2012-2013 by Enthought Inc.
import types

from enaml.core.parser import parse
from enaml.core.enaml_compiler import EnamlCompiler

import traits_enaml

from .gui_test_assistant import GuiTestAssistant
from .atom_test_assistant import AtomTestAssistant


def print_enaml_widget_tree(widget, level=0):
    """ Debugging helper to print out the enaml widget tree starting at a
    particular `widget`.

    Parameters
    ----------
    widget: QObject
        The root widget in the tree to print.
    level: int
        The current level in the tree. Used internally for displaying the
        tree level.

    """
    level = level + 4
    if level == 0:
        print
    print ' '*level, widget
    for child in widget.children:
        print_enaml_widget_tree(child, level=level)
    if level == 0:
        print


class EnamlTestAssistant(GuiTestAssistant, AtomTestAssistant):

    def tearDown(self):
        super(EnamlTestAssistant, self).tearDown()
        self.enaml_module = None

    def find_toolkit_widget(self, root, type_name):
        """ A simple function that recursively walks a widget tree until it
        finds a widget of a particular type.

        """

        if type_name in [cls.__name__ for cls in type(root).__mro__]:
            return root.widget

        for child in root.children():
            found = self.find_toolkit_widget(child, type_name)
            if found is not None:
                return found

        return None

    def find_all_enaml_widgets(self, root, type_name):
        """ A simple function that recursively walks a widget tree and returns
        a list of all widgets of a particular type.

        """

        return [child for child in root.traverse()
                if type_name in [cls.__name__ for cls in type(child).__mro__]]

    def find_enaml_widget(self, root, type_name):
        """ A simple function that recursively walks a widget tree until it
        finds a widget of a particular type.

        """

        for child in root.traverse():
            if type_name in [cls.__name__ for cls in type(child).__mro__]:
                return child

        return None

    def parse_and_create(self, source, **kwargs):
        """ Parses and compiles the source. The source should have a
        component defined with the name 'MainView'.

        Arguments
        ---------
        source : str
            The enaml source file

        kwargs : dict
            The default attribute values to pass to the component.

        Returns
        -------
            A tuple of the server and client component trees for the
            'MainView' component.

        """

        # This replicates what enaml.runner.main does
        enaml_ast = parse(source, filename='__enaml_tests__')
        code = EnamlCompiler.compile(enaml_ast, '__enaml_tests__')

        enaml_module = types.ModuleType('__tests__')
        ns = enaml_module.__dict__

        with traits_enaml.imports():
            exec code in ns
        View = ns['MainView']

        enaml_view = View(**kwargs)
        enaml_view.initialize()
        if not enaml_view.proxy_is_active:
            enaml_view.activate_proxy()

        toolkit_view = enaml_view.proxy

        # We need to keep a reference to the enaml_module to ensure it does not
        # get collected. If no reference is kept, enaml operators will not be
        # able to resolve objects properly (eg. validator = IntValidator(...)
        # will fail)
        self.enaml_module = enaml_module

        return enaml_view, toolkit_view
