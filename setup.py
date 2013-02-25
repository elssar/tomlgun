#!/usr/bin/env python

from setuptools import setup
from os import path

with open(path.join(path.dirname(__file__), 'README.md')) as readme:
    ld= readme.read()

setup(name= 'tomlgun',
    version= '0.1',
    author= 'elssar',
    author_email= 'elssar@altrawcode.com',
    py_modules= ['tomlgun'],
    url= 'https://github.com/elssar/tomlgun',
    license= 'MIT',
    description= 'Python parser for TOML - https://github.com/mojombo/toml',
    long_description= ld,
    keywords= 'TOML parser',
    )
