#
# (C) Copyright 2013 Enthought, Inc., Austin, TX
# All right reserved.
#
# This file is open source software distributed according to the terms in
# LICENSE.txt
#

import datetime

import enaml
from enaml.qt.qt_application import QtApplication
from traits.api import (HasTraits, Bool, Button, Date, Enum, Float, Int,
                        Range, Str, Time)


class AllTypes(HasTraits):
    """ A simple class with all kinds of traits

    """
    boolean_value = Bool(True)
    button_value = Button("I'm a button!")
    int_value = Int(42)
    float_value = Float(3.141592)
    enum_value = Enum("foo", "bar", "baz", "qux")
    int_range_value = Range(low=0, high=10)
    float_range_value = Range(low=0.0, high=1.0)
    str_value = Str("Word")
    date_value = Date(datetime.date.today())
    time_value = Time(datetime.time())

    def _button_value_fired(self):
        print "Button was pressed"

    def _anytrait_changed(self, name, old, new):
        print name, "changed from", old, "to", new

if __name__ == '__main__':
    with enaml.imports():
        from traits_enaml.widgets.auto_view import auto_window

    all = AllTypes()
    app = QtApplication()
    view = auto_window(all)
    view.show()

    app.start()
