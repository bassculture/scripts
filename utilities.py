'''
' 
' utilities.py 
'
'''

import logging
import argparse
import re
import sys
sys.path.insert(0, '..')

from pymei import *

def set_logging(parser):
    parser.add_argument('--logging', help="accepted values: DEBUG, INFO, WARNING, ERROR, CRITICAL. Defaults to WARNING.")
    args = parser.parse_args()
    if args.logging:
        if args.logging == "DEBUG":
            loglevel=logging.DEBUG
        if args.logging == "INFO":
            loglevel=logging.INFO
        if args.logging == "WARNING":
            loglevel=logging.WARNING
        if args.logging == "ERROR":
            loglevel=logging.ERROR
        if args.logging == "CRITICAL":
            loglevel=logging.CRITICAL
        logging.basicConfig(level=loglevel)

def get_descendants(MEI_tree, expr):    

    def parse_tokens(tokens):   
        
        def parse_token(token):
            
            def parse_attrs(token):
                
                def parse_attrs_str(attrs_str):
                    res = []
                    attr_pairs = attrs_str.split(",")
                    for attr_pair in attr_pairs:
                        if attr_pair == '':
                            continue
                        name_val = attr_pair.split("=")
                        if len(name_val)>1:
                            attr = MeiAttribute(name_val[0], name_val[1])
                            res.append(attr)
                        else:
                            logging.warning("get_descendants(): invalid attribute specifier in expression: " + expr)
                    return res
                m = re.search("\[(.*)\]", token)
                attrs_str = ""
                if m != None:
                    attrs_str = m.group(1)
                return parse_attrs_str(attrs_str)

            m = re.search("^([^\[]+)", token)
            elem = MeiElement(m.group(1))
            attrs = parse_attrs(token)
            for attr in attrs:
                elem.addAttribute(attr)
            return elem
            
        elems = []
        for t in tokens:
            elems.append(parse_token(t))
        return elems
    
    def match_elems(elems2match, el):
        tagname = el.getName()
        for e2m in elems2match:
            if e2m.getName() == tagname:
                match = True
                for atr in e2m.getAttributes():
                    if atr.getName() == "n" and atr.getValue() == "1":
                        if el.hasAttribute("n") and el.getAttribute("n").getValue() != "1":
                            match = False
                    elif not el.hasAttribute(atr.getName()) or el.getAttribute(atr.getName()).getValue() != atr.getValue():
                        match = False
                if match:
                    return True
        return False
    
    res = []
    descendants = MEI_tree.getDescendants()
    tokens = expr.split(" ")
    elems2match = parse_tokens(tokens)
    for el in descendants:
        if (match_elems(elems2match, el)):
            res.append(el)
    return res

def parse_token(token):
    
    def parse_attrs(token):
        
        def parse_attrs_str(attrs_str):
            res = []
            attr_pairs = attrs_str.split(",")
            for attr_pair in attr_pairs:
                if attr_pair == '':
                    continue
                name_val = attr_pair.split("=")
                if len(name_val)>1:
                    attr = MeiAttribute(name_val[0], name_val[1])
                    res.append(attr)
                else:
                    logging.warning("get_descendants(): invalid attribute specifier in expression: " + expr)
            return res
        m = re.search("\[(.*)\]", token)
        attrs_str = ""
        if m != None:
            attrs_str = m.group(1)
        return parse_attrs_str(attrs_str)

    m = re.search("^([^\[]+)", token)
    elem = MeiElement(m.group(1))
    attrs = parse_attrs(token)
    for attr in attrs:
        elem.addAttribute(attr)
    return elem

def parse_tokens(tokens):
    elems = []
    for t in tokens:
        elems.append(parse_token(t))
    return elems

def match_elems(elems2match, el):
    tagname = el.getName()
    for e2m in elems2match:
        if e2m.getName() == tagname:
            match = True
            for atr in e2m.getAttributes():
                if atr.getName() == "n" and atr.getValue() == "1":
                    if el.hasAttribute("n") and el.getAttribute("n").getValue() != "1":
                        match = False
                elif not el.hasAttribute(atr.getName()) or el.getAttribute(atr.getName()).getValue() != atr.getValue():
                    match = False
            if match:
                return True
    return False


def get_descendants_with_attribute_value(MEI_tree, names, attr, value):
    res = []
    descendants = MEI_tree.getDescendantsByName(names)
    for elem in descendants:
        if elem.hasAttribute(attr) and elem.getAttribute(attr).getValue() == value:
            res.append(elem)
    return res

def get_children_with_attribute_value(MEI_tree, names, attr, value):
    res = []
    children = MEI_tree.getChildrenByName(names)
    for elem in children:
        if elem.hasAttribute(attr) and elem.getAttribute(attr).getValue() == value:
            res.append(elem)
    return res
    
def chain_elems(start_elem, elems):
    def getOrAddChild(mei_elem, child_name):
        children = mei_elem.getChildrenByName(child_name)
        if len(children) > 0:
            return children
        mei_elem.addChild(MeiElement(child_name))
        return mei_elem.getChildrenByName(child_name)

    if elems == []:
        return start_elem
    children = getOrAddChild(start_elem, elems[0])
    return chain_elems(children[0], elems[1:])

def get_children_by_expr(MEI_tree, el_selector):
    res = []
    el2match = parse_token(el_selector)
    children = MEI_tree.getChildren()
    for elem in children:
        if match_elems([el2match], elem):
            res.append(elem)
    return res

def chain_elems_with_attribute_value(start_elem, selectors):
    def getOrAddChild(mei_elem, child_selector):
        children = get_children_by_expr(mei_elem, child_selector)
        if len(children) > 0:
            return children
        mei_elem.addChild(parse_token(child_selector))
        return get_children_by_expr(mei_elem, child_selector)

    if selectors == []:
        return start_elem
    children = getOrAddChild(start_elem, selectors[0])
    return chain_elems_with_attribute_value(children[0], selectors[1:])

def source_name2NCName(source_name, prefix="RISM"):
    # replace illegal characters:
    #   * '/' --> '-'
    # add prefix if the string starts with a digit
    res = re.sub("\s+", "_", source_name)
    res = re.sub("/", "-", res)
    res = re.sub("[^a-zA-Z0-9_\-.]", "_", res)
    res = re.sub("^([0-9\-.])", prefix+"\g<1>", res)
    return res

