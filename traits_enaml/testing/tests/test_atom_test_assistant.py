#------------------------------------------------------------------------------
# Copyright (c) 2005-2013, Enthought, Inc.
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in /LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
#------------------------------------------------------------------------------
import threading
import time
import unittest

from atom.api import Atom, Bool, Float, Event, ContainerList, observe

from traits_enaml.testing.atom_test_assistant import AtomTestAssistant

class TestObject(Atom):

    number = Float(2.0)
    list_of_numbers = ContainerList(Float())
    flag = Bool()

    @observe('number')
    def _add_number_to_list(self, change):
        self.list_of_numbers.append(change['value'])

    def add_to_number(self, value):
        self.number += value

class TestAtomTestAssistant(unittest.TestCase, AtomTestAssistant):

    def setUp(self):
        self.maxDiff = None
        self.test_object = TestObject()

    def test_when_using_with(self):
        """ Check normal use cases as a context manager.
        """
        test_object = self.test_object

        # default values are lazy
        test_object.number

        # Change event should NOT BE detected
        with self.assertAtomDoesNotChange(test_object, 'number') as result:
            test_object.flag = True
            test_object.number = 2.0

        msg = 'The assertion result is not None: {0}'.format(result.event)
        self.assertIsNone(result.event, msg=msg)

        # Change event should BE detected
        with self.assertAtomChanges(test_object, 'number') as result:
            test_object.flag = False
            test_object.number = 5.0

        expected = (test_object, 'update', 'number', None, None, 2.0, 5.0)
        self.assertSequenceEqual(expected, result.event)

        # Change event should BE detected exactly 2 times
        with self.assertAtomChanges(test_object, 'number', count=2) as result:
            test_object.flag = False
            test_object.number = 4.0
            test_object.number = 3.0

        expected = [(test_object, 'update', 'number', None, None, 5.0, 4.0),
                    (test_object, 'update', 'number', None, None, 4.0, 3.0)]
        self.assertSequenceEqual(expected, result.events)
        self.assertSequenceEqual(expected[-1], result.event)

        # Change event should BE detected
        with self.assertAtomChanges(test_object, 'number') as result:
            test_object.flag = True
            test_object.add_to_number(10.0)

        expected = (test_object, 'update', 'number', None, None, 3.0, 13.0)
        self.assertSequenceEqual(expected, result.event)

        # Change event should BE detected exactly 3 times
        with self.assertAtomChanges(test_object, 'number', count=3) as result:
            test_object.flag = True
            test_object.add_to_number(10.0)
            test_object.add_to_number(10.0)
            test_object.add_to_number(10.0)

        expected = [
            (test_object, 'update', 'number', None, None, 13.0, 23.0),
            (test_object, 'update', 'number', None, None, 23.0, 33.0),
            (test_object, 'update', 'number', None, None, 33.0, 43.0)]
        self.assertSequenceEqual(expected, result.events)
        self.assertSequenceEqual(expected[-1], result.event)

    def test_when_using_functions(self):
        test_object = self.test_object

        # Change event should BE detected (including the initial creation)
        self.assertAtomChanges(
            test_object, 'number', 2, test_object.add_to_number, 13.0)

        # default values are lazy
        test_object.flag
        # Change event should NOT BE detected
        self.assertAtomDoesNotChange(
            test_object, 'flag', test_object.add_to_number, 13.0)

    def test_indirect_events(self):
        """ Check catching indirect change events.
        """
        test_object = self.test_object

        # Change event should BE detected
        with self.assertAtomChanges(
                test_object, 'list_of_numbers') as result:
            test_object.flag = True
            test_object.number = -3.0

        expected = (
            test_object, 'container', 'list_of_numbers',
            'append', -3.0,  None, [-3.0])
        print result.event
        self.assertSequenceEqual(expected, result.event)

    def test_exception_inside_context(self):
        """ Check that exception inside the context statement block are
        propagated.

        """
        test_object = self.test_object

        with self.assertRaises(AttributeError):
            with self.assertAtomChanges(test_object, 'number'):
                test_object.i_do_exist

        with self.assertRaises(AttributeError):
            with self.assertAtomDoesNotChange(test_object, 'number'):
                test_object.i_do_exist

    def test_non_change_on_failure(self):
        """ Check behaviour when assertion should be raised for non trait
        change.

        """
        test_object = self.test_object
        # default values are lazy
        test_object.number

        atoms = 'flag', 'number'
        with self.assertRaises(AssertionError):
            with self.assertAtomDoesNotChange(test_object, atoms) as result:
                test_object.flag = True
                test_object.number = -3.0
        expected = [
            (test_object, 'create', 'flag', None, None, None, True),
            (test_object, 'update', 'number', None, None, 2.0, -3.0)]
        self.assertEqual(result.events, expected)

    def test_change_on_failure(self):
        """ Check behaviour when assertion should be raised for trait change.
        """
        test_object = self.test_object
        with self.assertRaises(AssertionError):
            with self.assertAtomChanges(test_object, 'number') as result:
                test_object.flag = True
        self.assertEqual(result.events, [])

        # Change event will not be fired 3 times
        with self.assertRaises(AssertionError):
            with self.assertAtomChanges(
                    test_object, 'number', count=4) as result:
                test_object.flag = True
                test_object.add_to_number(10.0)
                test_object.add_to_number(10.0)

        expected = [
            (test_object, 'create', 'number', None, None, None, 2.0),
            (test_object, 'update', 'number', None, None, 2.0, 12.0),
            (test_object, 'update', 'number', None, None, 12.0, 22.0)]
        self.assertSequenceEqual(expected, result.events)

    def test_asserts_in_context_block(self):
        """ Make sure that the atoms context manager does not stop
        regular assertions inside the managed code block from happening.
        """
        test_object = TestObject(number=16.0)

        with self.assertAtomDoesNotChange(test_object, 'number'):
            self.assertEqual(test_object.number, 16.0)

        with self.assertRaisesRegexp(AssertionError, '16\.0 != 12\.0'):
            with self.assertAtomDoesNotChange(test_object, 'number'):
                self.assertEqual(test_object.number, 12.0)

    def test_special_case_for_count(self):
        """ Count equal to 0 should be valid but it is discouraged.
        """
        test_object = TestObject(number=16.0)

        with self.assertAtomChanges(test_object, 'number', count=0):
            test_object.flag = True


if __name__ == '__main__':
    unittest.main()
