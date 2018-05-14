#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  @namespace pyfortified-requests
#

from __future__ import with_statement

# To install this library, open a Terminal shell,
# then run this file by typing:
#
# python setup.py install
#

import sys
import re
import codecs

from setuptools import setup

REQUIREMENTS = [
    req for req in open('requirements.txt')
    .read().split('\n')
    if req != ''
]

PACKAGES = [
    'pyfortified_requests',
    'pyfortified_requests.errors',
    'pyfortified_requests.exceptions',
    'pyfortified_requests.support',
    'pyfortified_requests.support.response'
]

with open('pyfortified_requests/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')

if len(sys.argv) < 2 or sys.argv[1] == 'version':
    print(version)
    sys.exit()

CLASSIFIERS = [
    # How mature is this project? Common values are
    #   3 - Alpha
    #   4 - Beta
    #   5 - Production/Stable
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Natural Language :: English',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Natural Language :: English',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Topic :: Software Development :: Libraries :: Python Modules'
]

with codecs.open('README.rst', 'r', 'utf-8') as f:
    readme = f.read()

setup(
    name='pyfortified-requests',
    version=version,
    description="Extension to Python `requests` functionality.",
    long_description=readme,
    url='https://github.com/jeff00seattle/pyfortified-requests',
    download_url='https://github.com/jeff00seattle/pyfortified-requests/archive/v{0}.tar.gz'.format(version),
    keywords="pyfortified requests",
    license='MIT License',
    zip_safe=False,
    include_package_data=True,
    install_requires=REQUIREMENTS,
    packages=PACKAGES,
    package_data={'': ['LICENSE']},
    package_dir={'pyfortified-requests': 'pyfortified-requests'},
    classifiers=CLASSIFIERS
)
