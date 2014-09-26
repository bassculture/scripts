import unittest
import os
import sys
sys.path.insert(0, '..')
from meimeta.metaimport import ImportFromTabbedText

class MeiMetaObjectTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_nothing(self):
        self.assertEqual(1,1)

class MeiMetaImportTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_importempty(self):
        headers = ImportFromTabbedText('n/a')
        self.assertEqual(len(headers), 1)
        metainfo = headers[0]
        self.assertEqual(metainfo.id, 'n/a')
        self.assertEqual(metainfo.work, None)
        self.assertEqual(len(metainfo.sources), 0)

    def test_importtest(self):
        headers = ImportFromTabbedText(os.path.join("test", "docs", "bassculture-fields-test.txt"))
        self.assertEqual(len(headers), 7)

        metainfo = headers[0]
        self.assertEqual(metainfo.id, 'header-id-00')
        self.assertEqual(metainfo.work, None)
        self.assertEqual(len(metainfo.sources), 1)
        self.assertEqual(metainfo.sources[0].id, 'src-id-00')
        
        metainfo = headers[1]
        self.assertEqual(metainfo.id, 'header-id-01')
        self.assertNotEqual(metainfo.work, None)
        self.assertEqual(len(metainfo.sources), 0)
        self.assertEqual(metainfo.work.id, 'work-id-01')

        metainfo = headers[2]
        self.assertEqual(metainfo.id, 'header-id-02')
        self.assertNotEqual(metainfo.work, None)
        self.assertNotEqual(len(metainfo.sources), 2)
        self.assertEqual(metainfo.work.id, 'work-id-02')
        self.assertEqual(metainfo.sources[0].id, 'src-id-02')
        self.assertEqual(metainfo.sources[1].id, 'src-id-03')


if __name__ == '__main__':

    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(MeiMetaObjectTest, 'test'))
    test_suite.addTest(unittest.makeSuite(MeiMetaImportTest, 'test'))

    runner = unittest.TextTestRunner()
    runner.run(test_suite)
