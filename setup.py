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
    version='0.3.0dev',
    author='Enthought, Inc',
    author_email='info@enthought.com',
    url='https://github.com/enthought/traits-enaml',
    description='Utilities for interoperation between Traits and Enaml',
    long_description=open('README.rst').read(),
    packages=find_packages(),
    package_data={'traits_enaml.testing.tests': ['*.enaml'],
                  'traits_enaml.widgets': ['*.enaml']},
    requires=['enaml>=0.8.9', 'traitsui>=5.0.0', 'traits>=4.5.0'],
    extras_require={
        'pyside': ['pyside'],
        'pyqt': ['pyqt<4.12'],
        'mayavi': ['mayavi'],
        'pandas': ['pandas'],
        'pyopengl': ['pyopengl']},
    classifiers=[c.strip() for c in """\
        Development Status :: 5 - Production/Stable
        Intended Audience :: Developers
        License :: OSI Approved :: BSD License
        Operating System :: MacOS
        Operating System :: Microsoft :: Windows
        Operating System :: OS Independent
        Operating System :: POSIX
        Operating System :: Unix
        Programming Language :: Python :: 2.7
        Topic :: Software Development
        Topic :: Software Development :: Libraries
        """.splitlines() if len(c.strip()) > 0],
)
