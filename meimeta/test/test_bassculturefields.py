# test_metadatadocument.py

import unittest
import os
import sys
sys.path.insert(0, '..')
from meimeta.metadatadocument import *
from utilities import *

class BasscultureFiledsTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_fieldorder(self):
        exportPath = os.path.join('test', 'docs', 'out')
        filename = os.path.join('test', 'docs', 'bassculture-fieldorders.txt')
        doc = MetadataDocument(filename = filename, exportPath = exportPath)
        self.assertIn('@bc:id', doc.rowmodel.fields)
        self.assertEqual(len(doc.rows), 2)
        meiHead = doc.headers['bc-header-00'].meiHead
        children = get_descendants(meiHead, 'source')[0].getChildren()
        status = doc.exportHeaders()

        self.assertEqual(children[0].getName(), 'identifier')
        self.assertEqual(children[1].getName(), 'titleStmt')
        self.assertEqual(children[2].getName(), 'editionStmt')

        self.assertTrue(status)

    def test_allfields(self):
        exportPath = os.path.join('test', 'docs', 'out')
        filename = os.path.join('test', 'docs', 'bassculture-fields-test.txt.bcfields')
        doc = MetadataDocument(filename = filename, exportPath = exportPath)
        self.assertIn('@bc:id', doc.rowmodel.fields)
        self.assertEqual(len(doc.rows), 70)
        status = doc.exportHeaders()
        self.assertTrue(status)

    def test_realdata(self):
        exportPath = os.path.join('test', 'docs', 'out')
        filename = os.path.join('test', 'docs', 'bassculture-realdata.txt.bcfields')
        doc = MetadataDocument(filename = filename, exportPath = exportPath)
        self.assertIn('@bc:id', doc.rowmodel.fields)
        status = doc.exportHeaders()
        self.assertTrue(status)

def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(BasscultureFiledsTest, 'test'))
    return test_suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())

