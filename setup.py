# Copyright (c) 2011-2013 by Enthought, Inc.
# All rights reserved.

from setuptools import setup, find_packages


setup(
    name='traits-enaml',
    version='0.1',
    author='Enthought, Inc',
    author_email='info@enthought.com',
    url='https://github.com/enthought/traits-enaml',
    description='Utilities for interoperation between Traits and Enaml',
    long_description=open('README.md').read(),
    packages=find_packages(exclude=('*.tests',)),
    package_data={'traits_enaml': ['*.enaml'],},
    requires=[
    ],
)
