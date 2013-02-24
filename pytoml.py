#!/usr/bin/env python
#

"""
Python parser for TOML - https://github.com/mojombo/toml
TOML is like INI, only better, or so Tom Preston-Werner says.
"""

__author__= 'elssar <elssar@altrawcode.com>'
__license__= 'MIT'

import datetime

def load(txt):
    """
    Will create a dict from a toml file
    """
    try:
        if not (isinstance(txt, str) or isinstance(txt, unicode)):
            raise Exception("Can't parse non string values")
    except Exception, e:
        print e
        exit()
    

def dump(toml):
    """
    Will convert a toml dict to toml file format.
    Caution! dump will not preserve formatting, comments and order.
    If these mean anything to you, don't use!
    """
    try:
        if not isinstance(toml, dict):
            raise Exception("Can't pass non dict value to dump")
        
    except Exception, e:
        print e
        exit()

