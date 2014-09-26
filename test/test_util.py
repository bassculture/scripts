import unittest
import sys
sys.path.insert(0, '..')
from pymei import MeiElement
import scripts.utilities as utilities

class UtilitiesTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_get_children_with_attribute_value(self):
        meiHead = MeiElement('meiHead')
        titleStmt = MeiElement('titleStmt')
        title = MeiElement('tite')
        respStmt = MeiElement('respStmt')
        titleStmt.addChild(title)
        titleStmt.addChild(respStmt)
        meiHead.addChild(titleStmt)

        persName = MeiElement('persName')
        persName.addAttribute('role', 'composer')
        respStmt.addChild(persName)

        self.assertEqual(len(utilities.get_children_with_attribute_value(respStmt, 'persName', 'role', 'composer')), 1)


    def test_get_children(self):
        meiHead = MeiElement('meiHead')
        titleStmt = MeiElement('titleStmt')
        title = MeiElement('tite')
        respStmt = MeiElement('respStmt')
        titleStmt.addChild(title)
        titleStmt.addChild(respStmt)
        meiHead.addChild(titleStmt)

        persName = MeiElement('persName')
        persName.addAttribute('role', 'composer')
        respStmt.addChild(persName)

        composers = utilities.get_children_by_expr(respStmt, 'persName[role=composer]')
        self.assertEqual(len(composers), 1)
        self.assertEqual(composers[0].getAttribute('role').value, 'composer')

    def test_chainelemswithattr_empty(self):
        mei = MeiElement('mei')
        elem = utilities.chain_elems_with_attribute_value(mei, [])
        self.assertEqual(elem, mei)

    def test_chainelemswithattr2(self):
        mei = MeiElement('mei')
        score1 = utilities.chain_elems_with_attribute_value(mei, ['music', 'body', 'mdiv[xml:id=id-01]', 'score'])
        score2 = utilities.chain_elems_with_attribute_value(mei, ['music', 'body', 'mdiv[xml:id=id-02]', 'score'])
        score3 = utilities.chain_elems_with_attribute_value(mei, ['music', 'body', 'mdiv[xml:id=id-02]', 'score'])
        self.assertNotEqual(score1, score2)
        self.assertEqual(score2, score3)
        self.assertEqual(utilities.get_descendants(mei, 'mdiv[xml:id=id-01]')[0].getChildren(), [score1])
        self.assertEqual(utilities.get_descendants(mei, 'mdiv[xml:id=id-02]')[0].getChildren(), [score2])

    def test_chainelemswithattr(self):
        meiHead = MeiElement('meiHead')
        composer = None
        composer = utilities.chain_elems_with_attribute_value(meiHead, ['fileDesc', 'titleStmt', 'respStmt', 'persName[role=composer]'])
        self.assertNotEqual(composer, None)
        self.assertEqual(composer.getAttribute('role').value, 'composer')
        identifier = utilities.chain_elems_with_attribute_value(meiHead, [
                'source',
                'itemList',
                'item',
                'physLoc',
                'repository',
                'identifier[authority=RISM,authURI=http://example.com/]' 
            ])
        self.assertEqual(identifier.getAttribute('authority').value, 'RISM')
        self.assertEqual(identifier.getAttribute('authURI').value, 'http://example.com/')

        ptr = utilities.chain_elems_with_attribute_value(meiHead, [
            'work',
            'notesStmt',
            'annot[type=link]',
            'ptr[target=http://example.com,title=link title]'
            ])

        self.assertEqual(ptr.getAttribute('target').value, 'http://example.com')
        self.assertEqual(ptr.getAttribute('title').value, 'link title')

        annots = utilities.get_descendants(meiHead, 'annot[type=link]')
        self.assertEqual(len(annots), 1)
        self.assertEqual(annots[0].getAttribute('type').value, 'link')

if __name__ == "__main__":
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(UtilitiesTest, 'test'))

    runner = unittest.TextTestRunner()
    runner.run(test_suite)
