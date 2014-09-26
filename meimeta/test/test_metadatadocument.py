# test_metadatadocument.py

import unittest
import os
import sys
sys.path.insert(0, '..')
from meimeta.metadatadocument import *
from utilities import *

class MetadataDocumentTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_readrowmodel(self):
        doc = MetadataDocument(os.path.join('test', 'docs', 'doc-test.txt'))
        self.assertIn('@bc:id', doc.rowmodel.fields)
        self.assertIn('path/to/an/element', doc.rowmodel.fields)
        self.assertIn('path/to/another/element/with[attr="value"]', doc.rowmodel.fields)

    def test_readrowdata(self):
        doc = MetadataDocument(os.path.join('test', 'docs', 'doc-test.txt'))
        self.assertEqual(len(doc.rows), 2)
        self.assertEqual(doc.rows[0].values['@bc:id'].value, 'header-00')
        self.assertEqual(doc.rows[0].values['path/to/an/element'].value, 'data01')
        self.assertEqual(doc.rows[0].values['path/to/another/element/with[attr="value"]'].value, 'data02')

    def test_readrowdata_emptyrow(self):
        doc = MetadataDocument()
        doc.addRow('\t\t\t\t\t\t')
        doc.addRow('')
        self.assertEqual(len(doc.rows), 0)

    def test_header(self):
        doc = MetadataDocument()
        doc.rowmodel.importFromTabbedString('@bc:id\tpath/to/elem1\tpath/to/elem2/with[attr=value]')
        doc.addRow('header-00\tdata01\t')
        doc.addRow('header-00\t\tdata02')
        doc.addRow('header-01\tdata01\t')
        doc.addRow('header-02\t\tdata02')
 
        self.assertEqual(len(doc.headers.keys()), 3)
        self.assertIn('header-00', doc.headers)
        self.assertIn('header-01', doc.headers)
        self.assertIn('header-02', doc.headers)
        self.assertEqual(len(get_descendants(doc.headers['header-00'].meiHead, 'elem1')), 1)
        self.assertEqual(len(get_descendants(doc.headers['header-00'].meiHead, 'with')), 1)
        self.assertEqual(len(get_descendants(doc.headers['header-01'].meiHead, 'elem1')), 1)
        self.assertEqual(len(get_descendants(doc.headers['header-01'].meiHead, 'elem2')), 0)
        self.assertEqual(len(get_descendants(doc.headers['header-02'].meiHead, 'elem1')), 0)
        self.assertEqual(len(get_descendants(doc.headers['header-02'].meiHead, 'elem2')), 1)

    def test_multifielddoc(self):
        doc = MetadataDocument()
        doc.rowmodel.importFromTabbedString('@bc:id\tpath/to/single\tpath/to/multi*')
        doc.addRow('header-00\tdata01\t')
        doc.addRow('header-00\t\tdata02-val1')
        doc.addRow('header-00\t\tdata02-val2')

        self.assertEqual(len(get_descendants(doc.headers['header-00'].meiHead, 'multi')), 2)
        self.assertEqual(get_descendants(doc.headers['header-00'].meiHead, 'multi')[0].value, 'data02-val1')
        self.assertEqual(get_descendants(doc.headers['header-00'].meiHead, 'multi')[1].value, 'data02-val2')

    def test_multifielddoc(self):
        doc = MetadataDocument()
        doc.rowmodel.importFromTabbedString('@bc:id\tpath/to/single\tpath/to/multi*')
        doc.addRow('header-00\tdata01\t')
        doc.addRow('header-00\t\tdata02-val1')
        doc.addRow('header-00\t\tdata02-val2')

        self.assertEqual(len(get_descendants(doc.headers['header-00'].meiHead, 'multi')), 2)
        self.assertEqual(get_descendants(doc.headers['header-00'].meiHead, 'multi')[0].value, 'data02-val1')
        self.assertEqual(get_descendants(doc.headers['header-00'].meiHead, 'multi')[1].value, 'data02-val2')

    def test_multiidfield(self):
        doc = MetadataDocument()
        doc.rowmodel.importFromTabbedString('@bc:id\tworkDesc/work*/@bc:id\tworkDesc/work/titleStmt/title*')
        doc.addRow('header-00\twork-00\t')
        self.assertEqual(len(get_descendants(doc.headers['header-00'].meiHead, 'work')), 1)
        self.assertEqual(get_descendants(doc.headers['header-00'].meiHead, 'work')[0].getAttribute('bc:id').value, 'work-00')

        doc.addRow('header-00\twork-00\ttitle 1')
        doc.addRow('header-00\twork-00\ttitle 2')

        self.assertEqual(len(get_descendants(doc.headers['header-00'].meiHead, 'work')), 1)
        self.assertEqual(len(get_descendants(doc.headers['header-00'].meiHead, 'title')), 3)
        self.assertEqual(get_descendants(doc.headers['header-00'].meiHead, 'work')[0].getAttribute('bc:id').value, 'work-00')
        self.assertEqual(get_descendants(doc.headers['header-00'].meiHead, 'title')[0].value, '') # titleStmt/title
        self.assertEqual(get_descendants(doc.headers['header-00'].meiHead, 'title')[1].value, 'title 1') # 1st work title
        self.assertEqual(get_descendants(doc.headers['header-00'].meiHead, 'title')[2].value, 'title 2') # 2nd work title

    def test_export(self):
        exportPath = os.path.join('test', 'docs', 'out')
        filename = os.path.join('test', 'docs', 'meta-test.txt')
        doc = MetadataDocument(filename = filename, exportPath = exportPath)
        status = doc.exportHeaders()
        self.assertTrue(status)

    def test_removequotes(self):
        txt = ' "workDesc/work/notesStmt/annot[type=""description""]" '
        doc = MetadataDocument()
        self.assertEqual(doc.removeQuotes(txt), ' workDesc/work/notesStmt/annot[type="description"] ')

def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(MetadataDocumentTest, 'test'))
    return test_suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())

