# header.py

from pymei import MeiElement
from utilities import *
from path import *

class NoFieldForPathException(Exception):
    def __init__(self, path):
        self.path = path
        pass

class Header:
    def __init__(self, id, ns = 'http://bassculture.info/ns/1.0', nsprefix = 'bc'):
        self.id = id
        self.meiHead = MeiElement('meiHead')
        self.meiHead.addAttribute('xmlns:' + nsprefix, ns)
        fileDesc = MeiElement('fileDesc')
        titleStmt = MeiElement('titleStmt')
        title = MeiElement('title')
        pubStmt = MeiElement('pubStmt')

        titleStmt.addChild(title)
        fileDesc.addChild(titleStmt)
        fileDesc.addChild(pubStmt)
        self.meiHead.addChild(fileDesc)

    def setFieldFromRow(self, path, row):
        '''
        
        Notes:
        If row.model.fields[path].idfield is defined
        (it means that idfield's element-path is a prefix of
        path) then an id selector should be added to the path
        which selects the element to be added or set.
        '''
        res = None
        if path not in row.model.fields:
            raise NoFieldForPathException(path)

        path_ext = path
        idfield = row.model.fields[path].idfield
        if idfield != None and len(idfield.idelempath) > 0:
            # insert id-selector to path: 
            
            #  * insert it here:            idfield.idelempath
            #  * insert this attrselelctor: idfield.idattrsel
            #  * insert this value:
            if idfield.multi:
                attrval = row.values[idfield.idelempath].children[idfield.idattrsel].value
            else:
                attrval = row.values[idfield.idelempath + '/' + idfield.idattrsel].value

            path_ext = self.insertIdSelector(path, idfield.idelempath, idfield.idattrsel, attrval)

        if path in row.values:
            if row.model.fields[path].multi:
                if row.model.fields[path].idelempath != None:
                    idattrsel = row.model.fields[path].idattrsel
                    path_ext = self.insertIdSelector(path_ext, path_ext, idattrsel, row.values[path].children[idattrsel].value)
                    res = self.setSingleField(path_ext, row.values[path].value)    
                else:
                    res = self.addMultiField(path_ext, row.values[path])
            else:
                # print path_ext
                res = self.setSingleField(path_ext, row.values[path].value)

        return res

    def insertIdSelector(self, path, elempath, attrsel, attrval):
        return insert_selector(path, elempath, '[' + attrsel[1:] +  '=' + attrval + ']')

    def setSingleField(self, path, value):
        '''
        Add a new element to the specified path relative to the meiHead
        element. 
        
        Arguments:
        path -- a string containing the path to the node. Can be an element
                or an attribute node. Relative to the meiHead element.
        value -- the string to be stored in the element's text node
        '''
        return self.setSingleFieldOf(self.meiHead, path, value)

    def setSingleFieldOf(self, elem, path, value):
        '''
        Add a new element to the specified path. 
        
        Arguments:
        elem -- the root element to which the path is relative
        path -- a string containing the path to the node. Can be an element 
                or an attribute node. 
        value -- the string to be stored in the element's text node
        '''

        tokens = split_path(path)
        attr_selector = None
        if tokens[len(tokens)-1][0] == '@':
            elem_selectors = tokens[0:len(tokens)-1]
            attr_selector = tokens[len(tokens)-1]
        else:
            elem_selectors = tokens
        el = chain_elems_with_attribute_value(elem, elem_selectors)
        if value != None:
            if (attr_selector != None):
                if (attr_selector == '@xml:id'):
                    el.setId(value)
                else:
                    el.addAttribute(attr_selector[1:], value)
            else:
                el.value = value
        return el

    def addMultiField(self, path, value_obj):
        '''
        Add a new element to the specified path relative to the meiHead
        
        Arguments:
        path -- a string containing the path to the root element. 
                (Cannot be an attribute node). Relative to the meiHead element.
                If path is 'path/to/an/element' it will add an a new 'element'
                node to the left-most path 'path/to/an'
        value_obj -- Value() obejct containing the nodes text value and its 
                 children
        '''
        tokens = split_path(path)
        '''(N.B. a multifield cannot be an attribtue)'''

        path_selectors = tokens[0:len(tokens)-1]
        elem_selector = tokens[len(tokens)-1]

        new_elem = parse_token(elem_selector)
        if value_obj.value != None:
            new_elem.value = value_obj.value
        el = chain_elems_with_attribute_value(self.meiHead, path_selectors)
        el.addChild(new_elem)

        for child_path in value_obj.children:
            self.setSingleFieldOf(new_elem, child_path, value_obj.children[child_path].value)

        return new_elem

    def sortFields(self):

        # As per http://music-encoding.org/documentation/guidelines2013/source
        source_childrenorder = [ 'identifier', 'titleStmt', 'editionStmt', 'pubStmt', 'physDesc', 'physLoc', 'notesStmt', 'itemList' ]

        # As per http://music-encoding.org/documentation/guidelines2013/titleStmt
        titleStmt_childrenorder = [ 'title', 'arranger', 'athor', 'composer', 'editor', 'funder', 'librettist', 'lyricist', 'respStmt', 'sponsor' ]

        # As per http://music-encoding.org/documentation/guidelines2013/titleStmt
        physLoc_childrenorder = [ 'repository', 'identifier', 'athor', 'composer', 'editor', 'funder', 'librettist', 'lyricist', 'respStmt', 'sponsor' ]

        # As per http://music-encoding.org/documentation/guidelines2013/work
        work_childrenorder = [ 'identifier', 'titleStmt', 'incip', 'key' 'mensuration', 'meter', 'tempo', 'otherChar', 'history', 'langUsage', 'perfMedium', 'audience', 'contents', 'context', 'biblList', 'notesStmt', 'classification', 'expressionList', 'componentGrp', 'relationList' ]

        children_orders = {\
            'source' : source_childrenorder, \
            'titleStmt' : titleStmt_childrenorder, \
            'physLoc' : physLoc_childrenorder, \
            'work' : work_childrenorder
        }

        for elemname in children_orders:
            # print 'Sorting ' + elemname + ' : ' + str(children_orders[elemname])
            self.sortElems(elemname, children_orders[elemname])


        return self     

    def sortElems(self, elemname, source_children_order):
        elems = get_descendants(self.meiHead, elemname)
        for elem in elems:
            self.sortElem(elem, source_children_order)
        return elems

    def sortElem(self, elem, children_order):
        list2sort = []
        children = elem.getChildren()
        for child in elem.getChildren():
            tagname = child.getName()
            if tagname in children_order:
                # print "{a}"
                # print 'adding elem to list2sort: ' + str(child)
                list2sort.append((child, children_order.index(tagname)))
            else:
                # print "{b}"
                list2sort.append((child, 0))

        # print 'list2sort: \n' + str(list2sort)
        # print ""
        for item in sorted(list2sort, key=lambda item: item[1]):
            elem.removeChild(item[0])
            elem.addChild(item[0])

        return elem








