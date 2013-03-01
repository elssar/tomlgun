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

with open(path.join(base, 'hard_example.yaml'), 'r') as hy:
    hard_yaml= load(hy)

with open(path.join(base, 'hard_example.toml'), 'r') as ht:
    hard_toml= tomlgun.load(ht.read())

if __name__=='__main__':
    print 'Easy example: ', yaml==toml           # Gotta love python!
    print 'Hard example: ', hard_yaml==hard_toml