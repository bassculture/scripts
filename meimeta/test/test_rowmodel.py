import unittest
import os
import sys
sys.path.insert(0, '..')
from meimeta.rowmodel import *

class FieldModelTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_create(self):

        fieldModel = FieldModel(name = 'Work ID', index = 1)
        self.assertEqual(fieldModel.name, 'Work ID')    
        self.assertEqual(fieldModel.index, 1)    


class RowModelTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_rowmodel_simplefield(self):
        rowModel = RowModel()
        rowModel.addField(path = '/work/@bc:id/', index = 1, name = 'Work ID')
        rowModel.addField(path = '/work/titleStmt/title*', index = 2, name = 'Work Title')

        self.assertTrue('work/@bc:id' in rowModel.fields)
        self.assertEqual(rowModel.fields['work/@bc:id'].index, 1)
        self.assertEqual(rowModel.fields['work/@bc:id'].name, 'Work ID')
        
        self.assertTrue('work/titleStmt/title' in rowModel.fields)
        self.assertEqual(rowModel.fields['work/titleStmt/title'].index, 2)
        self.assertEqual(rowModel.fields['work/titleStmt/title'].name, 'Work Title')
        self.assertTrue(rowModel.fields['work/titleStmt/title'].multi)

    def test_rowmodel_idfieldsmulti(self):
        model = RowModel()
        model.addField(path = 'a/b*/@bc:id', index = 0)
        self.assertTrue(model.fields['a/b'].multi)
        self.assertEqual(model.fields['a/b'].idelempath, 'a/b')
        self.assertEqual(model.fields['a/b'].idattrsel, '@bc:id')

        # N.B.: id attribute of a lower level element 
        # does not make the top level field an ID field
        model.addField(path = 'x*/y/@bc:id', index = 1)
        self.assertTrue(model.fields['x'].multi)
        self.assertEqual(model.fields['x'].idelempath, None)

    def test_rowmodel_idfields(self):
        model = RowModel()
        model.addField(path = 'a/b/@bc:id', index = 0)
        self.assertEqual(model.fields['a/b/@bc:id'].idelempath, 'a/b')
        self.assertEqual(model.fields['a/b/@bc:id'].idattrsel, '@bc:id')
        self.assertFalse(model.fields['a/b/@bc:id'].multi)

    def test_rowmodel_idfieldpaired(self):
        model = RowModel()
        model.addField(path = 'a/b/@bc:id', index = 0)
        model.addField(path = 'a/b/c*/d', index = 1)
        self.assertEqual(model.fields['a/b/c'].idfield, model.fields['a/b/@bc:id'])

    def test_rowmodel_idfieldpairedinreverseorder(self):
        model = RowModel()
        model.addField(path = 'a/b/c*/d', index = 1)
        model.addField(path = 'a/b/@bc:id', index = 0)
        self.assertEqual(model.fields['a/b/c'].idfield, model.fields['a/b/@bc:id'])

    def test_rowmodel_idfieldtransitivity(self):
        model = RowModel()
        model.addField(path = 'a/@bc:id', index = 0)
        model.addField(path = 'a/b/@bc:id', index = 1)
        model.addField(path = 'a/b/c*', index = 2)
        self.assertEqual(model.fields['a/@bc:id'].idfield, None)
        self.assertEqual(model.fields['a/b/@bc:id'].idfield, model.fields['a/@bc:id'])
        self.assertEqual(model.fields['a/b/c'].idfield, model.fields['a/b/@bc:id'])

        
    def test_rowmodel_combinedfields(self):
        rowModel = RowModel()
        rowModel.addField(
            name = 'Name of Responsible Person',
            path = '/work/titleStmt/respStmt/persName*/',
            index = 3
        )
        rowModel.addField(
            name = 'Name of Responsible Person',
            path = 'work/titleStmt/respStmt/persName*/@role',
            index = 4
        )

        self.assertTrue('work/titleStmt/respStmt/persName' in rowModel.fields)
        self.assertEqual(rowModel.fields['work/titleStmt/respStmt/persName'].index, 3)
        children = rowModel.fields['work/titleStmt/respStmt/persName'].children
        self.assertTrue('@role' in children)
        self.assertEqual(children['@role'].index, 4)

    def test_importfromstring(self):
        headerfields = '/@id\twork/@bc:id\twork/titleStmt/title*\twork/titleStmt/respStmt/persName*\twork/titleStmt/respStmt/persName*/@role'
        rowModel = RowModel()
        rowModel.importFromTabbedString(headerfields)

        self.assertTrue('@id' in rowModel.fields)
        self.assertEqual(rowModel.fields['@id'].index, 0)

        self.assertTrue('work/@bc:id' in rowModel.fields)
        self.assertEqual(rowModel.fields['work/@bc:id'].index, 1)
        self.assertFalse(rowModel.fields['work/@bc:id'].multi)
        
        self.assertTrue('work/titleStmt/title' in rowModel.fields)
        self.assertEqual(rowModel.fields['work/titleStmt/title'].index, 2)
        self.assertTrue(rowModel.fields['work/titleStmt/title'].multi)

        self.assertTrue('work/titleStmt/respStmt/persName' in rowModel.fields)
        self.assertEqual(rowModel.fields['work/titleStmt/respStmt/persName'].index, 3)
        self.assertTrue(rowModel.fields['work/titleStmt/respStmt/persName'].multi)
        children = rowModel.fields['work/titleStmt/respStmt/persName'].children
        self.assertTrue('@role' in children)
        self.assertEqual(children['@role'].index, 4)


def suite():
    test_suite = unittest.TestSuite()
    # test_suite.addTest(unittest.makeSuite(FieldModelTest, 'test'))
    test_suite.addTest(unittest.makeSuite(RowModelTest, 'test'))
    return test_suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())

