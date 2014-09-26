# test_header.py

import unittest
import os
import sys
sys.path.insert(0, '..')
from meimeta.metadatadocument import *
from utilities import *
from meimeta.rowdata import Value, Row
from meimeta.rowmodel import RowModel


class HeaderTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_singlefield(self):
        header = Header('id')
        elem = header.setSingleField('path/to/an/elem', 'value')
        self.assertEqual(elem.value, 'value')
        self.assertEqual(len(get_descendants(header.meiHead, 'path')), 1)
        self.assertEqual(len(get_descendants(header.meiHead, 'to')), 1)
        self.assertEqual(len(get_descendants(header.meiHead, 'an')), 1)

    def test_setattrvalue(self):
        header = Header('id')
        elem = header.setSingleField('path/to/an/@attribute', 'value')
        self.assertEqual(elem.getAttribute('attribute').value, 'value')
        self.assertEqual(get_descendants(header.meiHead, 'an')[0], elem)

    def test_singlefieldwithattr(self):
        header = Header('id')
        elem = header.setSingleField('path/to/an/elem/with[attr="http:\/\/example.com\/"]', 'value')
        self.assertEqual(elem.value, 'value')
        self.assertEqual(elem.getAttribute('attr').value, 'http://example.com/')
        self.assertEqual(get_descendants(header.meiHead, 'with')[0], elem)

    def test_singlefieldoverride(self):
        header = Header('id')
        elem1 = header.setSingleField('path/to/an/elem', 'value1')
        elem2 = header.setSingleField('path/to/an/elem', 'value2')
        self.assertEqual(elem1, elem2)
        self.assertEqual(elem2.value, 'value2')
        self.assertEqual(get_descendants(header.meiHead, 'elem')[0], elem1)

    def test_multifield(self):
        header = Header('id')
        elem1 = header.addMultiField('path/to/an/elem', Value('value1'))
        elem2 = header.addMultiField('path/to/an/elem', Value('value2'))
        self.assertNotEqual(elem1, elem2)
        self.assertEqual(elem1.value, 'value1')
        self.assertEqual(elem2.value, 'value2')
        self.assertEqual(len(header.meiHead.getChildrenByName('path')), 1)
        self.assertEqual(len(get_descendants(header.meiHead, 'elem')), 2)
        self.assertEqual(get_descendants(header.meiHead, 'elem')[0], elem1)
        self.assertEqual(get_descendants(header.meiHead, 'elem')[1], elem2)

    def test_combinedmultifield(self):
        header = Header('id')

        value = Value('root value')
        value.addChild('child/path/to/childElem[attr=attrval1]', 'child value 1')
        value.addChild('child/path/to/another/childElem[attr=attrval2]', 'child value 2')

        elem = header.addMultiField('path/to/an/elem', value)

        self.assertEqual(elem.value, 'root value')
        self.assertEqual(get_descendants(header.meiHead, 'elem')[0], elem)
        self.assertEqual(get_descendants(header.meiHead, 'childElem'), get_descendants(elem, 'childElem'))
        self.assertEqual(get_descendants(header.meiHead, 'childElem[attr=attrval1]')[0].value, 'child value 1')
        self.assertEqual(get_descendants(header.meiHead, 'childElem[attr=attrval2]')[0].value, 'child value 2')

    def test_combinedmultifieldinstances(self):
        header = Header('id')
        value = Value('root value')
        value.addChild('child/path/to/childElem', 'child value 1')
        value.addChild('child/path/to/another/childElem', 'child value 2')        
        elem1 = header.addMultiField('path/to/an/elem', value)
        elem2 = header.addMultiField('path/to/an/elem', value)

        self.assertNotEqual(elem1, elem2)
        self.assertEqual(len(get_descendants(elem1, 'childElem')), 2)
        self.assertEqual(len(get_descendants(elem2, 'childElem')), 2)
        self.assertEqual(get_descendants(header.meiHead, 'elem'), [elem1, elem2])
        self.assertEqual(len(get_descendants(header.meiHead, 'childElem')), 4)

    def test_setfieldfromrow(self):
        header = Header('id')
        model = RowModel()
        model.importFromTabbedString('a*/@bc:id\ta/b\ta/c')
        row = Row(model)
        row.readFromTabbedText('id-00\tfoo\t')
        elem1 = header.setFieldFromRow('a', row)
        elem2 = header.setFieldFromRow('a/b', row)
        self.assertEqual(len(get_descendants(header.meiHead, 'a')), 1)
        self.assertEqual(get_descendants(header.meiHead, 'a')[0], elem1)
        self.assertEqual(get_descendants(header.meiHead, 'a')[0].getAttribute('bc:id').value, 'id-00')
        self.assertEqual(len(get_descendants(header.meiHead, 'b')), 1)
        self.assertEqual(get_descendants(header.meiHead, 'b')[0], elem2)
        self.assertEqual(get_descendants(header.meiHead, 'b')[0].value, 'foo')

        row.readFromTabbedText('id-01\tfoo\tbar')
        elem1 = header.setFieldFromRow('a', row)
        elem2 = header.setFieldFromRow('a/b', row)
        elem3 = header.setFieldFromRow('a/c', row)
        self.assertEqual(len(get_descendants(header.meiHead, 'a')), 2)
        self.assertEqual(get_descendants(header.meiHead, 'a')[1], elem1)
        self.assertEqual(get_descendants(header.meiHead, 'a')[1].getAttribute('bc:id').value, 'id-01')

        self.assertEqual(len(get_descendants(header.meiHead, 'b')), 2)
        self.assertEqual(get_descendants(header.meiHead, 'b')[1], elem2)
        self.assertEqual(get_descendants(header.meiHead, 'b')[1].value, 'foo')

        self.assertEqual(len(get_descendants(header.meiHead, 'c')), 1)
        self.assertEqual(get_descendants(header.meiHead, 'c')[0], elem3)
        self.assertEqual(get_descendants(header.meiHead, 'c')[0].value, 'bar')

    def test_setfieldfromrowmulti(self):
        header = Header('id')
        model = RowModel()
        model.importFromTabbedString('a*/@bc:id\ta/b\ta/c')
        row = Row(model)
        row.readFromTabbedText('id-00\t\t')
        elem1 = header.setFieldFromRow('a', row)

        row = Row(model)
        row.readFromTabbedText('id-01\t\t')
        elem2 = header.setFieldFromRow('a', row)

        self.assertNotEqual(elem1, elem2)

    def test_setfieldfromrow_update(self):
        header = Header('id')
        model = RowModel()
        model.importFromTabbedString('a*/@bc:id\ta/b\ta/c')
        row = Row(model)
        row.readFromTabbedText('id-00\tfoo\tbar')
        elem1 = header.setFieldFromRow('a', row)
        elem2 = header.setFieldFromRow('a/b', row)
        elem3 = header.setFieldFromRow('a/c', row)

        row.readFromTabbedText('id-00\tfoo-foo\tbar-bar')
        elem1 = header.setFieldFromRow('a', row)
        elem2_ = header.setFieldFromRow('a/b', row)
        elem3_ = header.setFieldFromRow('a/c', row)

        self.assertEqual(elem2, elem2_)
        self.assertEqual(elem3, elem3_)
        self.assertEqual(get_descendants(header.meiHead, 'b')[0].value, 'foo-foo')
        self.assertEqual(get_descendants(header.meiHead, 'c')[0].value, 'bar-bar')

    def test_sortfields(self):
        header = Header('id')
        pubSt = header.setSingleField('fileDesc/sourceDesc/source/pubStmt', 'pubstmt')
        ident = header.setSingleField('fileDesc/sourceDesc/source/identifier', 'id')
        ttlSt = header.setSingleField('fileDesc/sourceDesc/source/titleStmt', 'title')

        # print 'children of source before sort: \n' + str(get_descendants(header.meiHead, 'source')[0].getChildren())
        # print ""
        header.sortFields()
        # print 'children of source after sort: \n' + str(get_descendants(header.meiHead, 'source')[0].getChildren())
        self.assertEqual(len(get_descendants(header.meiHead, 'source')[0].getChildren()), 3)
        self.assertEqual(get_descendants(header.meiHead, 'source')[0].getChildren(), [ident, ttlSt, pubSt])

def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(HeaderTest, 'test'))
    return test_suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())

