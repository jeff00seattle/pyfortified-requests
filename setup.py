#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  @namespace requests-fortified
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
    'requests_fortified',
    'requests_fortified.errors',
    'requests_fortified.exceptions',
    'requests_fortified.support',
    'requests_fortified.support.response'
]

TEST_REQUIREMENTS = ['pytest>=3.2.5', 'pytest-cov']

with open('requests_fortified/__init__.py', 'r') as fd:
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
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Natural Language :: English',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: Implementation :: PyPy'
]

with codecs.open('README.rst', 'r', 'utf-8') as f:
    readme = f.read()

setup(
    name='requests-fortified',
    version=version,
    description="Extension of Python HTTP `requests` with verbose logging using `logging-fortified`.",
    long_description=readme,
    url='https://github.com/jeff00seattle/requests-fortified',
    download_url='https://github.com/jeff00seattle/requests-fortified/archive/v{0}.tar.gz'.format(version),
    keywords="requests fortified",
    license='MIT License',
    zip_safe=False,
    include_package_data=True,
    install_requires=REQUIREMENTS,
    packages=PACKAGES,
    package_data={'': ['LICENSE']},
    package_dir={'requests-fortified': 'requests-fortified'},
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=TEST_REQUIREMENTS,
    classifiers=CLASSIFIERS
)
