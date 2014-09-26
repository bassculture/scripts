# rowmodel.py
import sys
from path import *

class InvalidFieldException(Exception):
    def __init__(self):
        pass

class FieldModel:
    def __init__(self, index, name = None, multi = False, idelempath = None, idattrsel = None, idfield = None):
        self.name = name
        self.index = index
        self.children = dict() # dict of FieldModel
        self.multi = multi
        self.idelempath = idelempath    # if the field is an id field, this is
                                        # set to the field's element-path
        self.idattrsel = idattrsel      # if the field is an id field this is
                                        # set to the id attribute selector
        self.idfield = None             # points to an id field. An id field
                                        # will have a path that is a prefox 
                                        # of the path of this field

    def addChild(self, child_path, child):
        if (child_path not in self.children):
            self.children[child_path] = child

    def addChild(self, child_path, name, index, multi = False, idelempath = None, idattrsel = None, idfield = None):
        if (child_path not in self.children):
            self.children[child_path] = FieldModel(index, name, multi, idelempath, idattrsel, idfield)

    def setMulti(self, value):
        self.multi = value

class RowModel:
    def __init__(self):
        self.fields = dict() # of FieldModel

    def isIdAttribute(self, attrname):
        return attrname == '@bc:id'

    def trim_slash(self, path):
        res  = path
        if len(res) > 0 and res[0] == '/':
            res = res[1:]
        if len(res) > 0 and res[len(res)-1] == '/':
            res = res[0:len(res)-1]
        return res

    def addField(self, path, index, name = None):
        path_parts = path.split('*')
        root_path = self.trim_slash(path_parts[0])
        multi = len(path_parts) > 1

        child_path = ''
        if len(path_parts) > 1:
            child_path = path_parts[1]
            child_path = self.trim_slash(child_path)
        
        if len(path_parts) > 1 and len(child_path) > 0:
            if (root_path not in self.fields):
                idelempath = None
                idattrsel = None
                if self.isIdAttribute(child_path):
                    idelempath = root_path
                    idattrsel = child_path
                fieldModel = self.fields[root_path] = FieldModel(\
                    index = None, \
                    name = 'n/a', \
                    multi = multi, \
                    idelempath = idelempath, \
                    idattrsel = idattrsel\
                )
            else:
                fieldModel = self.fields[root_path]

            fieldModel.addChild(child_path, name, index)
        elif len(path_parts) == 1 or (len(path_parts) > 1 and len(child_path) == 0):

            if (root_path not in self.fields):

                idattrsel = attribute_part(root_path)
                idelempath = None
                if (idattrsel != None):
                    idelempath = element_part(root_path)

                fieldModel = self.fields[root_path] = FieldModel(\
                    index = index, \
                    name = name, \
                    multi = multi, \
                    idelempath = idelempath, \
                    idattrsel = idattrsel \
                )

            else:
                fieldModel = self.fields[root_path]
        else:
            raise "cannot process path: " + str(path)


        for existing_path in self.fields:
            if fieldModel.idelempath != None:
                if self.fields[existing_path] != fieldModel and \
                    isprefix(fieldModel.idelempath, existing_path) and \
                    (self.fields[existing_path].idfield == None or \
                    isprefix(self.fields[existing_path].idfield.idelempath, fieldModel.idelempath)):

                    self.fields[existing_path].idfield = fieldModel

            existing_field = self.fields[existing_path]
            if existing_field.idelempath != None and \
                isprefix(existing_field.idelempath, root_path) and \
                (fieldModel.idfield == None or \
                isprefix(fieldModel.idfield.idelempath, existing_field.idelempath)) and \
                fieldModel != existing_field:

                fieldModel.idfield = existing_field

        return fieldModel

    def importFromTabbedString(self, row):
        textfields = row.split('\t')
        i = 0
        for txtfield in textfields:
            self.addField(path = txtfield, index = i)
            i += 1





