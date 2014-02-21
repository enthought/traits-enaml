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
from traits.api import HasTraits, Disallow, TraitListObject, TraitDictObject

from enaml.core.standard_tracer import StandardTracer, SubscriptionObserver


class TraitsObserver(SubscriptionObserver):
    """ An observer object which manages a tracer subscription.

    Subclassed to allow weak-referencing.

    """
    __slots__ = ('__weakref__',)


class TraitsTracer(StandardTracer):
    """ A CodeTracer for tracing expressions which use Traits.

    This tracer maintains a running set of `traced_traits` which are the
    (obj, name) pairs of traits items discovered during tracing.

    """
    __slots__ = 'traced_traits'

    def __init__(self, owner, name):
        """ Initialize a TraitsTracer.

        """
        super(TraitsTracer, self).__init__(owner, name)
        self.traced_traits = set()

    #--------------------------------------------------------------------------
    # Private API
    #--------------------------------------------------------------------------
    def _trace_trait(self, obj, name):
        """ Add the trait object and name pair to the traced items.

        Parameters
        ----------
        obj : HasTraits
            The traits object owning the attribute.

        name : str
            The trait name to for which to bind a handler.

        """
        # Traits will happily force create a trait for things which aren't
        # actually traits. This tries to avoid most of that when possible.
        trait = obj.trait(name)
        if trait is not None and trait.trait_type is not Disallow:
            self.traced_traits.add((obj, name))
            # Check for lists
            if trait.handler.has_items:
                self.traced_traits.add((obj, '{}_items'.format(name)))

    #--------------------------------------------------------------------------
    # AbstractScopeListener Interface
    #--------------------------------------------------------------------------
    def dynamic_load(self, obj, attr, value):
        """ Called when an object attribute is dynamically loaded.

        This will trace the object if it is a HasTraits instance.
        See also: `AbstractScopeListener.dynamic_load`.

        """
        super(TraitsTracer, self).dynamic_load(obj, attr, value)
        if isinstance(obj, HasTraits):
            self._trace_trait(obj, attr)

    #--------------------------------------------------------------------------
    # CodeTracer Interface
    #--------------------------------------------------------------------------
    def load_attr(self, obj, attr):
        """ Called before the LOAD_ATTR opcode is executed.

        This will trace the object if it is a HasTraits instance.
        See also: `CodeTracer.dynamic_load`.

        """
        super(TraitsTracer, self).load_attr(obj, attr)
        if isinstance(obj, HasTraits):
            self._trace_trait(obj, attr)

    def call_function(self, func, argtuple, argspec):
        """ Called before the CALL_FUNCTION opcode is executed.

        This will trace the func is the builtin `getattr` and the object
        is a HasTraits instance. See also: `CodeTracer.call_function`

        """
        super(TraitsTracer, self).call_function(func, argtuple, argspec)
        nargs = argspec & 0xFF
        nkwargs = (argspec >> 8) & 0xFF
        if (func is getattr and (nargs == 2 or nargs == 3) and nkwargs == 0):
            obj, attr = argtuple[0], argtuple[1]
            if isinstance(obj, HasTraits) and isinstance(attr, basestring):
                self._trace_trait(obj, attr)

    def binary_subscr(self, obj, idx):
        """ Called before the BINARY_SUBSCR opcode is executed.

        This will trace the object if it is a `TraitListObject` or a
        `TraitDictObject`. See also: `CodeTracer.get_iter`.

        """
        super(TraitsTracer, self).binary_subscr(obj, idx)
        if isinstance(obj, (TraitListObject, TraitDictObject)):
            traits_obj = obj.object()
            if traits_obj is not None:
                if obj.name_items:
                    self._trace_trait(traits_obj, obj.name_items)

    def get_iter(self, obj):
        """ Called before the GET_ITER opcode is executed.

        This will trace the object if it is a `TraitListObject`
        See also: `CodeTracer.get_iter`.

        """
        super(TraitsTracer, self).get_iter(obj)
        if isinstance(obj, TraitListObject):
            traits_obj = obj.object()
            if traits_obj is not None:
                if obj.name_items:
                    self._trace_trait(traits_obj, obj.name_items)

    #--------------------------------------------------------------------------
    # StandardTracer Interface
    #--------------------------------------------------------------------------
    def finalize(self):
        """ Finalize the tracing process.

        This method will discard the old observer and attach a new
        observer to the traced dependencies.

        """
        owner = self.owner
        name = self.name
        key = '_[%s|trace]' % name
        storage = owner._d_storage

        # invalidate the old observer so that it can be collected
        old_observer = storage.get(key)
        if old_observer is not None:
            old_observer.ref = None

        # create a new observer and subscribe it to the dependencies
        if self.items or self.traced_traits:
            observer = TraitsObserver(owner, name)
            storage[key] = observer
            for obj, d_name in self.items:
                obj.observe(d_name, observer)
            for obj, d_name in self.traced_traits:
                obj.on_trait_change(observer.__call__, d_name)
