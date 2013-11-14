# Copyright (c) 2012-2013 by Enthought Inc.

import contextlib
import sys
from unittest.case import _ExpectedFailure, _UnexpectedSuccess

from traits.api import (
    Any, Event, HasStrictTraits, Instance, Int, List, Property, Str,
)
from traits.testing.unittest_tools import UnittestTools, reverse_assertion



@contextlib.contextmanager
def expected_failure():
    """ An expected failure context manager. The executed block will only be
    considered an expected failure of there is an assertion raised. Else of
    an exception is raised the error is re-raised. Finally if there was no
    exception the block is marked an unexpected success

    """
    try:
        yield
    except AssertionError:
        raise _ExpectedFailure(sys.exc_info())
    except Exception:
        raise
    else:
        raise _UnexpectedSuccess

class _AssertAtomChangesContext(object):
    """Context manager used to implement TestAssistant.assertAtomChanges."""
    def __init__(self, obj, xname, count, test_case):
        self.obj = obj
        self.xname = xname
        self.count = count
        self.event = None
        self.events = []
        self.failureException = test_case.failureException

    def _listener(self, change):
        """Dummy trait listener."""
        obj = change['object']
        name = change['name']
        value = change['value']
        self.event = (obj, name, value)
        self.events.append(self.event)

    def __enter__(self):
        """Bind the trait listener."""
        self.obj.observe(self.xname, self._listener)
        return self

    def __exit__(self, exc_type, exc_value, tb):
        """Remove the trait listener."""
        if exc_type is not None:
            return False

        self.obj.unobserve(self.xname)
        if self.event is None:
            msg = 'A change event was not fired for: {0}'.format(self.xname)
            raise self.failureException(msg)
        elif self.count is not None and len(self.events) != self.count:
            msg = 'Change event for {0} was fired {1} times instead of {2}'
            items = self.xname, len(self.events), self.count
            raise self.failureException(msg.format(*items))

        return False

class TestAssistant(UnittestTools):
    """Mixin class to augment the unittest.TestCase with useful methods."""

    ### Trait assertion methods ########################################

    def assertAtomChanges(self, obj, trait, count=None, callableObj=None,
                           *args, **kwargs):
        """ Same method as assertTraitChanges but for Atom based object ... """

        context = _AssertAtomChangesContext(obj, trait, count, self)
        if callableObj is None:
            return context
        with context:
            callableObj(*args, **kwargs)

    def assertAtomDoesNotChange(self, obj, atom, callableObj=None,
                                 *args, **kwargs):
        """Assert an object atom does not change.

        Assert that the class atom does not change during
        execution of the provided function.

        """
        msg = 'A change event was fired for: {0}'.format(atom)
        context = _AssertAtomChangesContext(obj, atom, None, self)
        if callableObj is None:
            return reverse_assertion(context, msg)
        with reverse_assertion(context, msg):
            callableObj(*args, **kwargs)

