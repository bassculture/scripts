import unittest
import os
import sys
sys.path.insert(0, '..')
from meimeta.rowdata import *
from meimeta.rowmodel import *

class RowDataTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_rowobject(self):
        model = RowModel()
        row = Row(model)
        self.assertEqual(row.model, model)
        self.assertEqual(row.values, dict())

    def test_readfromtabbedtext(self):

        headerfields = '0\twork/@bc:id\twork/titleStmt/title*\twork/titleStmt/respStmt/persName*\twork/titleStmt/respStmt/persName*/@role'
        # headerfields = '0\twork/@bc:id'
        model = RowModel()
        model.importFromTabbedString(headerfields)

        rowtext = 'header-id-00\twork-id-00\twork title\tsurename, firstname\tcomposer'
        row = Row(model)
        row.readFromTabbedText(rowtext)

        self.assertIn('0', row.values)
        self.assertEqual(row.values['0'].value, 'header-id-00')
        self.assertIn('work/@bc:id', row.values)
        self.assertEqual(row.values['work/@bc:id'].value, 'work-id-00')

    def test_partialrow(self):
        model = RowModel()
        model.importFromTabbedString('@bc:id\tpath/to/elem1\tpath/to/elem2/with[attr=value]')
        row = Row(model)

        row.readFromTabbedText('header-00\tdata0\t')
        self.assertIn('path/to/elem1', row.values)
        self.assertNotIn('path/to/elem2/with[attr=value]', row.values)

    def test_idfields(self):
        model = RowModel()
        model.importFromTabbedString('a*/@bc:id\t/a/b\tc/d')
        row = Row(model)

        row.readFromTabbedText('id-00\tdata0\t')
        self.assertIn('a', row.values)
        self.assertIn('a/b', row.values)

def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(RowDataTest, 'test'))
    return test_suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())

