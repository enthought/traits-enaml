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

from setuptools import setup, find_packages


setup(
    name='traits-enaml',
    version='0.2.1dev',
    author='Enthought, Inc',
    author_email='info@enthought.com',
    url='https://github.com/enthought/traits-enaml',
    description='Utilities for interoperation between Traits and Enaml',
    long_description=open('README.rst').read(),
    packages=find_packages(),
    package_data={'traits_enaml.testing.tests': ['*.enaml'],
                  'traits_enaml.widgets': ['*.enaml']},
    requires=[
    ],
)
