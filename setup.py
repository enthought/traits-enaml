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

import os
import re
from setuptools import find_packages, setup
from subprocess import check_output

MAJOR = 0
MINOR = 3
MICRO = 0
IS_RELEASED = False
VERSION = '%d.%d.%d' % (MAJOR, MINOR, MICRO)
VERSION_FILE_TEMPLATE = """\
# This file is generated from setup.py
version = '{version}'
full_version = '{full_version}'
git_revision = '{git_revision}'
is_released = {is_released}
if not is_released:
    version = full_version
"""
DEFAULT_VERSION_FILE = os.path.join('traits_enaml', '_version.py')


# Return the git revision as a string
def git_version():
    def _minimal_ext_cmd(cmd):
        # construct minimal environment
        env = {}

        for k in ['SYSTEMROOT', 'PATH', 'HOME']:
            v = os.environ.get(k)
            if v is not None:
                env[k] = v
        # LANGUAGE is used on win32
        env['LANGUAGE'] = 'C'
        env['LANG'] = 'C'
        env['LC_ALL'] = 'C'
        out = check_output(cmd, env=env)
        return out
    try:
        out = _minimal_ext_cmd(['git', 'rev-parse', 'HEAD'])
        git_revision = out.strip().decode('ascii')
    except OSError:
        git_revision = "Unknown"
    try:
        out = _minimal_ext_cmd(['git', 'rev-list', '--count', 'HEAD'])
        git_count = out.strip().decode('ascii')
    except OSError:
        git_count = '0'
    return git_revision, git_count


def write_version_py(filename=DEFAULT_VERSION_FILE,
                     template=VERSION_FILE_TEMPLATE):
    # Adding the git rev number needs to be done inside
    # write_version_py(), otherwise the import of traits_enaml._version messes
    # up the build under Python 3.
    fullversion = VERSION
    if os.path.exists('.git'):
        git_rev, dev_num = git_version()
    elif os.path.exists(DEFAULT_VERSION_FILE):
        # must be a source distribution, use existing version file
        try:
            from traits_enaml._version import git_revision as git_rev
            from traits_enaml._version import full_version as full_v
        except ImportError:
            raise ImportError("Unable to import git_revision. Try removing "
                              "traits_enaml/_version.py and the build directory "
                              "before building.")
        match = re.match(r'.*?\.dev(?P<dev_num>\d+)$', full_v)
        if match is None:
            dev_num = '0'
        else:
            dev_num = match.group('dev_num')
    else:
        git_rev = "Unknown"
        dev_num = '0'
    if not IS_RELEASED:
        fullversion += '.dev{0}'.format(dev_num)
    with open(filename, "wt") as fp:
        fp.write(template.format(version=VERSION,
                                 full_version=fullversion,
                                 git_revision=git_rev,
                                 is_released=IS_RELEASED))
    return fullversion


if __name__ == "__main__":
    __version__ = write_version_py()

    with open('README.rst') as file_:
        long_description = file_.read()

    setup(
        name='traits-enaml',
        version=__version__,
        author='Enthought, Inc',
        author_email='info@enthought.com',
        url='https://github.com/enthought/traits-enaml',
        description='Utilities for interoperation between Traits and Enaml',
        long_description=long_description,
        packages=find_packages(),
        package_data={'traits_enaml.testing.tests': ['*.enaml'],
                        'traits_enaml.widgets': ['*.enaml']},
        requires=[],
    )
