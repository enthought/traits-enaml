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
from enaml.core.dynamicscope import DynamicScope
from enaml.core.expression_engine import HandlerPair, ReadHandler
from enaml.core.funchelper import call_func
from enaml.core.operators import gen_tracer, op_notify, op_simple, op_update
from enaml.core.standard_handlers import HandlerMixin

from .traits_tracer import TraitsTracer


class TraitsTracedReadHandler(ReadHandler, HandlerMixin):
    """ An expression read handler which traces code execution.

    This handler is used in conjuction with the standard '<<' operator.

    """
    def __call__(self, owner, name):
        """ Evaluate and return the expression value.

        """
        func = self.func
        f_globals = func.__globals__
        f_builtins = f_globals['__builtins__']
        f_locals = self.get_locals(owner)
        tr = TraitsTracer(owner, name)
        scope = DynamicScope(owner, f_locals, f_globals, f_builtins, None, tr)
        return call_func(func, (tr,), {}, scope)


def trait_op_subscribe(code, scope_key, f_globals):
    """ The Traits Enaml operator function for the `<<` operator.

    This operator generates a tracer function with optimized local
    access and hooks it up to a TraitsTracedReadHandler. This
    operator does not support write semantics.

    Parameters
    ----------
    code : CodeType
        The code object created by the Enaml compiler.

    scope_key : object
        The block scope key created by the Enaml compiler.

    f_globals : dict
        The global scope for the for code execution.

    Returns
    -------
    result : HandlerPair
        A pair with the reader set to a TraitsTracedReadHandler.

    """
    func = gen_tracer(code, f_globals)
    reader = TraitsTracedReadHandler(func=func, scope_key=scope_key)
    return HandlerPair(reader=reader)


def trait_op_delegate(code, scope_key, f_globals):
    """ The Traits Enaml operator function for the `:=` operator.

    This operator combines the '<<' and the '>>' operators into a
    single operator. It supports both read and write semantics.

    Parameters
    ----------
    code : CodeType
        The code object created by the Enaml compiler.

    scope_key : object
        The block scope key created by the Enaml compiler.

    f_globals : dict
        The global scope for the for code execution.

    Returns
    -------
    result : HandlerPair
        A pair with the reader set to a TraitsTracedReadHandler and
        the writer set to a StandardInvertedWriteHandler.

    """
    p1 = trait_op_subscribe(code, scope_key, f_globals)
    p2 = op_update(code, scope_key, f_globals)
    return HandlerPair(reader=p1.reader, writer=p2.writer)


TRAIT_OPERATORS = {
    '=': op_simple,
    '::': op_notify,
    '>>': op_update,
    '<<': trait_op_subscribe,
    ':=': trait_op_delegate,
}
