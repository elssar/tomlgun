#!/usr/bin/env python
#-*- encoding: utf-8 -*-

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

def compare(dict1, dict2, parent=''):
    try:
        if isntance(dict2, dict):
            raise Exception('{0} is not a dictionary!'.format(dict2))
        for key in dict1:
            if key not in dict2:
                raise Exception('Key {0} not found in {1}!'.format(key, parent+dict2))
            if type(dict1[key])!=type(dict2[key]):
                raise Exception('Key {0} not of the same type in {1}'.format(key, parent+dict2))
            if isisntance(dict1[key], dict):
                compare(dict1[key], dict2[key], parent+key+'.')
            else:
                if isinstance(dict1[key], list):
                    if not list_compare(dict1[key], dict2[key]):
                        raise Exception('Key {0} not equal in {1}'.format(key, parent+dict2))
                else:
                    if dict1[key]!=dict2[key]:
                        raise Exception('Key {0} not equal in {1}'.format(key, parent+dict2))
        return True
    except Exception, e:
        print e
        return False

def list_compare(list1, list2):
    if len(list1)!=len(list2):
        return False
    for (i, j) in zip(list1, list2):
        if type(i)!=type(j):
            return False
        if isinstance(i, list):
            if not list_compare(i, j):
                return False
        if i!=j:
            return False
    return True

if __name__=='__main__':
    easy= compare(yaml, toml)
    print 'Easy example: {0}'.format(['Fail', 'Pass'][easy])
    hard= compare(easy_yaml, hard_yaml)
    print 'Hard example: {0}'.format(['Fail', 'Pass'][hard])