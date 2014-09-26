from pymei import MeiElement
from utilities import *


class Field:
    def __init__(self, path, value):
        self.path = path
        self.value = value


class Header:
    def __init__(self, id):
        self.id = id
        self.meiHead = MeiElement('meiHead')

    def setFileds(elem, fields):
        for field in fields:
            setField(elem, field)

    def setField(elem, field):
        path_tokens = self.split_path(field.path)

    def split_path(path):
        tokens = path.replace('"', '').
            replace('\\/', '\\[fwslash]').
            split('/')
        res = []
        for t in tokens:
            res.append(t.replace('\\[fwslash]', '/'))
        return res


class BassyHeader:
    def __init__(self, id):
        self.id = id
        self.meiHead = MeiElement('meiHead')
        titleStmt = MeiElement('titleStmt')
        title = MeiElement('tite')
        respStmt = MeiElement('respStmt')
        titleStmt.addChild(title)
        titleStmt.addChild(respStmt)
        self.meiHead.addChild(titleStmt)

        # define minimal sourceDesc

    def analyse_selector(selector):
        sel = selector.replace('"').replace('*', '')
        tokens = sel.split('/')
        for token in tokens:

    def setFileds(elem, fields):
        for field in fields:
            setField(elem, field)

    def setField(elem, field):
        path_tokens = field.path.split('/')
        # * then probably call something like chain_elems() or get_descendants()
        self.getElement()

        # * set value to resulting element
