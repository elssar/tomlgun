#!/usr/bin/env python

"""
Python parser for TOML - https://github.com/mojombo/toml
TOML is like INI, only better, or so Tom Preston-Werner says.
"""

__author__= 'elssar <elssar@altrawcode.com>'
__license__= 'MIT'

import datetime

# -----------------Load section------------

def load(txt):
    """
    Will create a dict from a toml file.
    This is currently in the works
    """
    try:
        if not isinstance(txt, (str, unicode)):
            raise Exception("Can't parse non string values")
    except Exception, e:
        print e
        exit(-1)
    toml= {}
    lines= txt.splitlines()
    for line in lines:
        rule= line.strip()
        if rule=='':
            continue
        if rule[0]=='#':
            continue
        

# -----------Dump section------------------

def dump(toml, LEVEL=-1, PARENT=''):
    """
    Will convert a toml dict to toml file format.
    Caution! If using a loaded config, formatting, comments and order won't be preserved.
    If these mean anything to you, don't use!
    Usage: dump(toml-dict, [LEVEL=0,PARENT='',])
    returns: str
    """
    try:
        if not isinstance(toml, dict):
            raise Exception("Can't pass non dict value to dump")
    except Exception, e:
        print e
        exit(-1)
    txt= ''
    for key in toml:
        if isisntance(toml[key], dict):
            txt+= '{0}[{1}{2}]\n'.format('\t'*LEVEL, PARENT, key)
            txt+= dump(toml[key], LEVEL+1, key+'.')
        else:
            txt+= '{0}{1}\n'.format('\t'*LEVEL, key_val_to_str(key, toml[key]))
    return txt

def key_val_to_str(key, val):
    return '{0} = {1}'.format(key, variable_to_str(val))

def variable_to_str(var):
    if isinstance(var, list):
        s= ''
        for val in var:
            s+= '{0} ,'.format(variable_to_srt(val))
        return '[{0}]'.format(s[:-2])
    elif isinstance(var, (int, float, long, complex)):
        return '{0}'.format(var)
    elif isinstance(var, (str, unicode)):
        return '{"{0}"'.format(var.encode('unicode-escape'))
    elif isinstance(var, bool):
        return'{0}'.format(['false', 'true'][var])
    elif isinstance(var, datetime):
        return'{0}Z'.format(var.isoformat()[:19])

if __name__=='__main__':
    print "You crazy? Import in your python script, don't call from the command line!"
    print ">_<"