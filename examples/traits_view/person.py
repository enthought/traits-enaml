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

    traits_view = View('last_name', 'first_name', 'age', resizable=True)

if __name__ == '__main__':
    with enaml.imports():
        from traits_view import PersonView

    john = Person(first_name='John', last_name='Doe', age=42)

    app = QtApplication()
    view = PersonView(person=john)
    view.show()

    app.start()
