#
# (C) Copyright 2013 Enthought, Inc., Austin, TX
# All right reserved.
#
# This file is open source software distributed according to the terms in
# LICENSE.txt
#
from traits.etsconfig.api import ETSConfig

import enaml

from .trait_operators import TRAIT_OPERATORS

if ETSConfig.toolkit not in ['', 'qt4']:
    raise ValueError('traits-enaml does not support WX')

ETSConfig.toolkit = 'qt4'

def imports():
    return enaml.imports(operators=TRAIT_OPERATORS)
