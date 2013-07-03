#
# (C) Copyright 2013 Enthought, Inc., Austin, TX
# All right reserved.
#
# This file is open source software distributed according to the terms in
# LICENSE.txt
#
from enaml.core.operators import SubscriptionObserver, OperatorBase, op_simple, \
    op_notify, op_update, bind_write_operator, bind_read_operator, \
    add_operator_storage
from enaml.core.funchelper import call_func
from enaml.core.dynamic_scope import DynamicScope, Nonlocals
from enaml.core.standard_inverter import StandardInverter

from atom.datastructures.api import sortedmap

from .traits_tracer import TraitsTracer


class TraitsObserver(SubscriptionObserver):

    __slots__ = '__weakref__'

    def handler(self):
        owner = self.owner
        if owner is not None:
            name = self.name
            setattr(owner, name, owner._run_eval_operator(name))


class OpSubscribe(OperatorBase):

    __slots__ = 'observers'

    def __init__(self, binding):
        super(OpSubscribe, self).__init__(binding)
        self.observers = sortedmap()

    def release(self, owner):
        super(OpSubscribe, self).release(owner)
        obs = self.observers.pop(owner, None)
        if obs is not None:
            atom_ob, traits_ob = obs
            atom_ob.owner = None
            traits_ob.owner = None

    def eval(self, owner):
        tracer = TraitsTracer()
        overrides = {'nonlocals': Nonlocals(owner, tracer), 'self': owner}
        f_locals = self.get_locals(owner)
        func = self.binding.func
        scope = DynamicScope(
            owner, f_locals, overrides, func.func_globals, tracer
        )
        result = call_func(func, (tracer,), {}, scope)
        observers = self.observers
        old = observers.get(owner)
        if old is not None:
            atom_ob, traits_ob = old
            atom_ob.owner = None
            traits_ob.owner = None
        atom_ob = SubscriptionObserver(owner, self.binding.name)
        traits_ob = TraitsObserver(owner, self.binding.name)
        observers[owner] = (atom_ob, traits_ob)
        for obj, name in tracer.traced_items:
            obj.observe(name, atom_ob)
        for obj, name in tracer.traced_traits:
            obj.on_trait_change(traits_ob.handler, name)
        return result


class OpDelegate(OpSubscribe):
    """ An operator class which implements the `:=` operator semantics.

    """
    __slots__ = ()

    def notify(self, change):
        """ Run the notification code bound to the operator.

        This method is called by the '_run_notify_operator()' method on
        a Declarative instance.

        Parameters
        ----------
        change : dict
            The change dict for the change on the requestor.

        """
        owner = change['object']
        nonlocals = Nonlocals(owner, None)
        inverter = StandardInverter(nonlocals)
        overrides = {'nonlocals': nonlocals, 'self': owner}
        f_locals = self.get_locals(owner)
        func = self.binding.auxfunc
        scope = DynamicScope(
            owner, f_locals, overrides, func.func_globals, None
        )
        call_func(func, (inverter, change.get('value')), {}, scope)


def trait_op_subscribe(klass, binding):
    bind_write_operator(klass, binding, OpSubscribe(binding))
    add_operator_storage(klass)


def trait_op_delegate(klass, binding):
    operator = OpDelegate(binding)
    bind_read_operator(klass, binding, operator)
    bind_write_operator(klass, binding, operator)
    add_operator_storage(klass)


TRAIT_OPERATORS = {
    '=': op_simple,
    '::': op_notify,
    '>>': op_update,
    '<<': trait_op_subscribe,
    ':=': trait_op_delegate,
}
