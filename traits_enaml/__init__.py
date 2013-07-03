#
# (C) Copyright 2013 Enthought, Inc., Austin, TX
# All right reserved.
#
# This file is open source software distributed according to the terms in
# LICENSE.txt
#
import enaml
from .trait_operators import TRAIT_OPERATORS


def imports():
    return enaml.imports(operators=TRAIT_OPERATORS)
