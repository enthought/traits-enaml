#
# (C) Copyright 2013 Enthought, Inc., Austin, TX
# All right reserved.
#
# This file is open source software distributed according to the terms in
# LICENSE.txt
#

from traits.api import HasTraits, Str, Range
from traitsui.api import View

import enaml
from enaml.qt.qt_application import QtApplication


class Person(HasTraits):
    """ A simple class representing a person object.

    """
    last_name = Str()

    first_name = Str()

    age = Range(low=0)

    traits_view = View('last_name', 'first_name', 'age', resizable=True)

if __name__ == '__main__':
    with enaml.imports():
        from traits_view import PersonView

    john = Person(first_name='John', last_name='Doe', age=42)

    app = QtApplication()
    view = PersonView(person=john)
    view.show()

    app.start()
