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
from traits.etsconfig.api import ETSConfig

import enaml

from .trait_operators import TRAIT_OPERATORS

if ETSConfig.toolkit not in ['', 'qt4']:
    raise ValueError('traits-enaml does not support WX')

ETSConfig.toolkit = 'qt4'


def imports():
    return enaml.imports(operators=TRAIT_OPERATORS)
