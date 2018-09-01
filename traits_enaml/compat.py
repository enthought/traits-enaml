#----------------------------------------------------------------------------
#
#  Copyright (c) 2018, Enthought, Inc.
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
""" Compatibility module to support a wider range of enaml versions.

"""
__all__ = ['QApplication']

try:
    from enaml.qt.QtGui import QApplication
except ImportError:
    from enaml.qt.QtWidgets import QApplication
