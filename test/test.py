#!/usr/bin/env python

"""
Tests for tomlgun, a Python parser for TOML
"""

__author__= 'elssar <elssar@altrawcode.com>'

from os import path
from yaml import load
import tomlgun

base= path.dirname(path.abspath(__file__))

with open(path.join(base, 'example.yaml'), 'r') as y:
    yaml= load(y)

with open(path.join(base, 'example.toml'), 'r') as t:
    toml= tomlgun.load(t.read())

if __name__=='__main__':
    print yaml==toml           # Gotta love python!