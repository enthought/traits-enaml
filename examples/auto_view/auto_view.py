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
import datetime

from enaml.qt.qt_application import QtApplication
from traits.api import (HasTraits, Bool, Button, Date, Enum, Float, Int, List,
                        Range, Str, Time)
import traits_enaml
from traits_enaml.widgets.auto_view import auto_window
with traits_enaml.imports():
    from traits_enaml.widgets.auto_editors import DefaultEditor


class AllTypes(HasTraits):
    """ A simple class with all kinds of traits

    """
    boolean_value = Bool(True, label="Custom Bool Label:")
    button_value = Button("I'm a button!")
    int_value = Int(42, tooltip="You can add a tooltip as well.")
    float_value = Float(3.141592)
    enum_value = Enum("foo", "bar", "baz", "qux")
    int_range_value = Range(low=0, high=10)
    float_range_value = Range(low=0.0, high=1.0)
    list_value = List([0, 1, 2])
    str_value = Str("Word")
    date_value = Date(datetime.date.today())
    time_value = Time(datetime.time())
    range_value = Range(low=0, high=100,
                        label="Traits Range Editor:",
                        enaml_editor=DefaultEditor)

    _my_float = Float

    def _button_value_fired(self):
        print "Button was pressed"

    def _anytrait_changed(self, name, old, new):
        print name, "changed from", old, "to", new

if __name__ == '__main__':
    all = AllTypes()
    app = QtApplication()
    view = auto_window(all)
    view.show()

    app.start()
