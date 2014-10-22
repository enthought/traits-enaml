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
import enaml
from enaml.qt.qt_application import QtApplication

from traits.api import HasTraits, Str, Range
from traitsui.api import View



class Person(HasTraits):
    """ A simple class representing a person object.

    """
    last_name = Str()

    first_name = Str()

    age = Range(low=0)

    def _age_changed(self, new):
        """ Prints out a message whenever the person's age changes. """
        msg = "{first} {last} is {age} years old."
        s = msg.format(
            first=self.first_name, last=self.last_name, age=self.age,
        )
        print s

if __name__ == '__main__':
    import traits_enaml
    with traits_enaml.imports():
        from person import PersonView

    john = Person(first_name='John', last_name='Doe', age=42)

    app = QtApplication()
    view = PersonView(person=john)
    view.show()

    app.start()
