#!/usr/bin/env python
#-*- encoding: utf-8 -*-

"""
Python parser for TOML - https://github.com/mojombo/toml
TOML is like INI, only better, or so Tom Preston-Werner says.
"""

__author__= 'elssar <elssar@altrawcode.com>'
__license__= 'MIT'

from datetime import datetime
from re import match, compile as compile
from string import digits
from dateutil.parser import parse as parse_date

# -----------------Load section-------------------

def load(txt):
    """
    Will create a dict from a toml file.
    This is currently in the works
    """
    try:
        if not isinstance(txt, (str, unicode)):
            raise Exception("Can't parse non strings")
        toml= {}
        current_keygroup= toml
        lines= txt.splitlines()
        IN_ARRAY= False
        for line in lines:
            rule= line.strip()
            if rule=='':
                continue
            if rule[0]=='#':
                continue
            if rule[0]=='[' and not IN_ARRAY:  # in multiline arrays, the first element on a line could be an array
                subkey= rule[1:rule.find(']')].split('.')
                current_keygroup= toml
                for key in subkey:
                    if not key in current_keygroup:
                        current_keygroup[key]= {}
                    elif not isinstance(current_keygroup[key], dict):
                        raise Exception('Error! Multiple values assigned to the same key')
                    current_keygroup= current_keygroup[key]
            else:
                key, value= parse_line(line)
                if isinstance(value, tuple):
                    if (not IN_ARRAY) and key in current_keygroup:   # Explicit is better than implicit
                        raise Exception('Error! Multiple values assigned to the same key')
                    if key not in current_keygroup:
                        current_keygroup[key]= []
                    for values in value[0]:
                        current_keygroup[key].append(values)
                    IN_ARRAY= value[1]
                if key in current_keygroup:
                    raise Exception('Error! Multiple values assigned to the same key')
                current_keygroup[key]= value
    except Exception, e:
        print e
        exit(-1)

def parse_line(line):
    tokens= line.split('=', 1)
    if len(tokens)<2:
        raise Exception('Error! The key has no value')
    token= tokens[1].strip()
    return token[0].strip, parse_token(token)

def parse_token(token):
    if token[0]=='[':
        return parse_array(token)
    if token[0]=='"':
        return parse_string(token)
    if token[:4] in ('true', 'false'):
        if len(token)==4 or token[4:].strip()[0]=='#':
            return [False, True][token[:4]=='true']
        raise Exception('Error! Invalid markup')
    date_format= compile('^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z')
    if match(date_format, token[:20]) and (len(token==20) or token[20:].strip()[0]=='#'):
        return parse_date(token[:20])
    number_format= compile('^[-]?\d+[.]?\d+')   # This looks right, but isn't working on my interpreter
    if token[0] in ['-', '.'] or token[0] in digits:   # I don't know what I was thinking, but
        regx= number_format.match(token)               # I'm fairly certain it works, so
        if regx:                                       # 'if ain't broke, don't fix it'
            start, end= regx.span()                    # Touch only if it breaks
            if len(token)>end:
                s= token[end:].strip()
                if s[0]!='#':
                    raise Exception('Error! Invalid markup')
            num= token[:end]
            return [float(num), int(num)][int(num)==float(num)]
    raise Exception('Error! Invalid markup')

def parse_string(token):
    if len(token)==1 or token[1:].find('"')==-1:
        raise Exception('Error! Invalid markup')
    flag= False
    for i, char in enumerate(token[1:]):
        if char=='"':
            if i==0:
                flag= True
                break
            if token[i]!='\\' or token[i-1]=='\\':
                flag= True
                break
    if not flag:
        raise Exception('Error! Invalid markup')
    if len(token)>i+2 and token[i+3:].strip()[0]!='#':
        raise Exception('Error! Invalid markup')
    return token[1:i+1].decode('unicode-escape')

# I know the string parsing is a lot unwieldly, and could've been better
# done with regular expressions, but I'm a regex noob, and regex broke my
# brain this morning, so this is the best I could come up with, with a broken brain
# If anyone is interested, the regex was breaking when there are " in the line, after
# the intended end of string
# Example -
# key= "string" " <--this would break the regex
# key= "string" #comment with a " in it <--gah!
# Oh why oh why did I decide to write a parser /o\
#                                              -|-
#                                              / \
# - elssar, ~2013-02-26T16:59:31 IST
    
def parse_array(token):
    items= [x.strip() for x in token.split(',')]
    
    
# ---------------------Dump section---------------------

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
        if isinstance(toml[key], dict):
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
        return'{0}Z'.format(var.isoformat()[:19])  # h/t https://github.com/uiri/toml/blob/master/toml.py

if __name__=='__main__':
    print "You crazy? Import in your python script, don't call from the command line!"
    print ">_<"