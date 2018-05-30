#!/usr/bin/env python

import re
from os.path import abspath, dirname, join
from setuptools import setup, find_packages


CURDIR = dirname(abspath(__file__))

CLASSIFIERS = '''
Development Status :: 5 - Production/Stable
License :: OSI Approved :: Apache Software License
Operating System :: OS Independent
Programming Language :: Python
Programming Language :: Python :: 2
Programming Language :: Python :: 3
Topic :: Software Development :: Testing
Framework :: Robot Framework
Framework :: Robot Framework :: Library
'''.strip().splitlines()
with open(join(CURDIR, 'src', 'ExtendedSeleniumLibrary', '__init__.py')) as f:
    VERSION = re.search("\n__version__ = '(.*)'", f.read()).group(1)
with open(join(CURDIR, 'README.rst')) as f:
    DESCRIPTION = f.read()
with open(join(CURDIR, 'requirements.txt')) as f:
    REQUIREMENTS = f.read().splitlines()

setup(
    name             = 'extendedseleniumlibrary',
    version          = VERSION,
    description      = 'Extended Web testing library (from SeleniumLibrary) for Robot Framework',
    long_description = DESCRIPTION,
    author           = 'Lanh Dang',
    author_email     = 'danglanh.it@gmail.com',
    url              = 'https://github.com/krazytools/ExtendedSeleniumLibrary',
    license          = 'Apache License 2.0',
    keywords         = 'extended robotframework testing testautomation selenium webdriver web',
    platforms        = 'any',
    classifiers      = CLASSIFIERS,
    install_requires = REQUIREMENTS,
    package_dir      = {'': 'src'},
    packages         = find_packages('src')
)
