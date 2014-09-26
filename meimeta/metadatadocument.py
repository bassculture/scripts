# metadatadocument.py

import sys
import os
import re
from rowmodel import *
from rowdata import *
from header import *
from pymei import *

class MetaDocExection(Exception):
    pass

class MetaDocNoHeaderIDException(MetaDocExection):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(str(self.value.rawdata))

class MetadataDocument:
    def __init__(self, filename = None, exportPath = '', exportFilenameBase = 'meta.', exportFileExt = '.mei'):
        self.filename = filename
        self.rows = []
        self.headers = {}
        self.rowmodel = RowModel()
        if filename != None:
            self.open()

        self.exportPath = exportPath
        self.exportFilenameBase = exportFilenameBase
        self.exportFileExt = exportFileExt

    def removeQuotes(self, txt):
        txt = re.sub(r'(^|[^"])"([^"]|$)', r'\1\2', txt)
        txt = re.sub(r'"{2}', r'"', txt)
        return txt

    def open(self):
        if self.filename == None:
            return None
        self.file = open(self.filename)

        self.file.readline() # line 1
        self.file.readline() # line 2
        self.file.readline() # line 3
        rowmodeltext = self.file.readline().rstrip('\n') # line 4
        rowmodeltext = self.removeQuotes(rowmodeltext)
        self.rowmodel.importFromTabbedString(rowmodeltext)

        for line in self.file:
            self.addRow(line.rstrip('\n'))
        return self

    def addRow(self, line):
        r = Row(self.rowmodel)
        r.readFromTabbedText(line)
        # print line
        if len(r.values.keys()) > 0:
            self.rows.append(r)
            self.processRow(r)
        return self

    def processRow(self, row):
        if 'HEADER_ID' not in row.values and '@xml:id' not in row.values and '@bc:id' not in row.values:
            raise MetaDocNoHeaderIDException(row)
        if 'HEADER_ID' in row.values:
            header_id = row.values['HEADER_ID'].value
        if '@xml:id' in row.values:
            header_id = row.values['@xml:id'].value
        if '@bc:id' in row.values:
            header_id = row.values['@bc:id'].value
        if header_id in self.headers:
            header = self.headers[header_id]
        else:
            header = Header(header_id)
            self.headers[header_id] = header

        for path in row.values:
            header.setFieldFromRow(path, row)

    def exportHeader(self, header, filename):
        meidoc = MeiDocument()
        root = MeiElement('mei')
        meidoc.root = root
        root.addChild(header)
        root.addChild(MeiElement('music')) # only for making the MEI valid against mei-CMN.rng
        status = XmlExport.meiDocumentToFile(meidoc, os.path.join(self.exportPath, filename))
        return status

    def exportFilename(self, file_id):
        return self.exportFilenameBase + file_id + self.exportFileExt

    def exportHeaders(self):
        result = True
        for header_id in self.headers:
            self.headers[header_id].sortFields()
            result = result and self.exportHeader(self.headers[header_id].meiHead, self.exportFilename(header_id))
        return result

