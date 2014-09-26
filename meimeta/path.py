# path.py
'''
path -- a series of node selectors delimited by '/'.
        A node selector can either be an element selector or
        an attribute selector. Attribute selector start
        with the character '@'. Any attribute selector
        must be the last node selector in the path.
        An element selector can contain attribute constraints,
        e.g. element[attr1=value2,attr2=value2] If an attribute
        value contains '/' cahracter it must be escaped by a'\'
        character.
'''

import re
import os
from pymei import MeiElement
from utilities import *

class Path:
    def __init__(self, path):
        self.path = path

    def trim_slash(self):
        return trim_slash(self.path)

    def split(self):
        return split_path(self.path)

    def element_part(self):
        return element_part(self.path)

    def attribute_part(self):
        return attribute_part(self.path)

def trim_slash(path):
    res  = path
    if len(res) > 0 and res[0] == '/':
        res = res[1:]
    if len(res) > 0 and res[len(res)-1] == '/':
        res = res[0:len(res)-1]
    return res

def split_path(path):
    tokens = path.replace('"', '').\
        replace('\\/', '\\[fwslash]').\
        split('/')
    res = []
    for t in tokens:
        t = t.replace('\\[fwslash]', '/')
        if t != '':
            res.append(t)
    return res

def element_part(path):
    return re.sub(r'/?@.*', '', path)

def attribute_part(path):
    res = None
    search_res = re.search(r'/?(@.*)', path)
    if (search_res != None):
        res = search_res.group(1)
    return res

def isprefix(path1, path2):
    tokens1 = split_path(trim_slash(path1))
    tokens2 = split_path(trim_slash(path2))
    return isprefix_tokens(tokens1, tokens2)

def isprefix_tokens(tokens1, tokens2):
    if len(tokens2) == 0:
        return len(tokens1) == 0
    mei = MeiElement('mei')
    root = chain_elems_with_attribute_value(mei, [ tokens2[0] ])
    if len(tokens1) == 0:
        return True
    chain_elems_with_attribute_value(root, tokens2)
    descs = get_descendants(root, tokens1[-1])
    elem = chain_elems_with_attribute_value(root, tokens1)
    return (len(descs) > 0 and descs[0] == elem)

def build_from_tokens(tokens):
    res = ''
    first = True
    for t in tokens:
        if not first:
            res += '/'
        else:
            first = False
        t = t.replace('/', '\\/')
        res += t
    return res

def merge_attrtoken(token, attribute_token):
    res = token
    if re.search('\[', res):
        sre = re.match(r'\[([^\]]*)\]', attribute_token)
        if sre:
            attr_and_val = sre.group(1)
            if len(attr_and_val) > 0:
                res = re.sub(']', ',' + attr_and_val + ']', res)
    else:
        res += attribute_token
    return res


def insert_selector(path, prefix, selector):
    if len(selector) == 0:
        return path
    path_tokens = split_path(trim_slash(path))
    prefix_tokens = split_path(trim_slash(prefix))
    if isprefix_tokens(prefix_tokens, path_tokens):
        if selector[0] == '[' and selector[-1] == ']':
            if len(prefix_tokens) > 0:
                position = len(prefix_tokens) - 1
            else:
                position = 0
            token = merge_attrtoken(path_tokens[position], selector)
            path_tokens.pop(position)
            path_tokens.insert(position, token)
        else:
            if len(prefix_tokens) > 0:
                position = len(prefix_tokens)
            else:
                position = 1
            path_tokens.insert(position, selector)

    return build_from_tokens(path_tokens)


