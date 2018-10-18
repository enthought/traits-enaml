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
from builtins import object
from collections import namedtuple

from traits.testing.unittest_tools import reverse_assertion


Change = namedtuple(
    'Change',
    ['object', 'type', 'name', 'operation', 'item', 'oldvalue', 'value'])


class _AssertAtomChangesContext(object):
    """ Context manager used to implement TestAssistant.assertAtomChanges.

    """
    def __init__(self, obj, xname, count, test_case):
        self.obj = obj
        self.xname = xname
        self.count = count
        self.event = None
        self.events = []
        self.failureException = test_case.failureException

    def _listener(self, change):
        """ Dummy atom listener.

        """
        obj = change['object']
        type_ = change['type']
        name = change['name']
        value = change['value']
        old_value = change.get('oldvalue', None)
        operation = change.get('operation', None)
        item = change.get('item', None)
        self.event = Change(
            obj, type_, name, operation, item, old_value, value)
        self.events.append(self.event)

    def __enter__(self):
        """ Bind the trait listener.

        """
        self.obj.observe(self.xname, self._listener)
        return self

    def __exit__(self, exc_type, exc_value, tb):
        """ Remove the trait listener.

        """
        if exc_type is not None:
            return False

        self.obj.unobserve(self.xname)
        if self.event is None and self.count != 0:
            msg = 'A change event was not fired for: {0}'.format(self.xname)
            raise self.failureException(msg)
        elif self.count is not None and len(self.events) != self.count:
            msg = 'Change event for {0} was fired {1} times instead of {2}'
            items = self.xname, len(self.events), self.count
            raise self.failureException(msg.format(*items))

        return False


class AtomTestAssistant(object):
    """ Mixin class to augment the unittest.TestCase with useful atom
    assert methods.

    """

    ### Trait assertion methods ########################################

    def assertAtomChanges(
            self, obj, trait, count=None, callableObj=None, *args, **kwargs):
        """ Same method as assertTraitChanges but for Atom based object ...

        """

        context = _AssertAtomChangesContext(obj, trait, count, self)
        if callableObj is None:
            return context
        with context:
            callableObj(*args, **kwargs)

    def assertAtomDoesNotChange(
            self, obj, atom, callableObj=None, *args, **kwargs):
        """Assert an object atom does not change.

        Assert that the class atom does not change during execution of the
        provided function.

        """
        msg = 'A change event was fired for: {0}'.format(atom)
        context = _AssertAtomChangesContext(obj, atom, None, self)
        if callableObj is None:
            return reverse_assertion(context, msg)
        with reverse_assertion(context, msg):
            callableObj(*args, **kwargs)
