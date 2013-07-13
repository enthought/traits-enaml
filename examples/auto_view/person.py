#
# (C) Copyright 2013 Enthought, Inc., Austin, TX
# All right reserved.
#
# This file is open source software distributed according to the terms in
# LICENSE.txt
#

import enaml
from enaml.qt.qt_application import QtApplication
from traits.api import HasTraits, Str, Range


class Person(HasTraits):
    """ A simple class representing a person object.

    """
    last_name = Str()

    first_name = Str()

    age = Range(low=0, high=120)

    def _anytrait_changed(self, name, old, new):
        print name, "changed from", old, "to", new

if __name__ == '__main__':
    with enaml.imports():
        from traits_enaml.widgets.auto_view import auto_view

    john = Person(first_name='John', last_name='Doe', age=42)

    app = QtApplication()
    view = auto_view(john)
    view.show()

    app.start()
