import unittest
import os
import sys
sys.path.insert(0, '..')
from meimeta.path import *

class PathTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_elementpart(self):
        self.assertEqual(element_part('/a/b/c/@d'), '/a/b/c')
        self.assertEqual(element_part('/@a'), '')
        self.assertEqual(element_part('@a'), '')

    def test_attributepart(self):
        self.assertEqual(attribute_part('a/b/c/@d'), '@d')
        self.assertEqual(attribute_part('@a'), '@a')
        self.assertEqual(attribute_part('a/b/c'), None)

    def test_isprefix(self):
        self.assertTrue(isprefix('a/b', 'a/b/c'))
        self.assertFalse(isprefix('/a/b/c', 'a/b/'))
        self.assertTrue(isprefix('', ''))
        self.assertTrue(isprefix('/', ''))
        self.assertTrue(isprefix('', '/'))
        self.assertTrue(isprefix('a/b', 'a/b'))

    def test_isprefixtokens(self):
        self.assertTrue(isprefix_tokens([], []))
        self.assertTrue(isprefix_tokens([], ['root']))

    def test_isprefixwithattr(self):
        self.assertTrue(isprefix('a/b[c=cval]', 'a/b[c=cval]/d'))
        self.assertFalse(isprefix('a/b[c=cval1]', 'a/b[c=cval2]/d'))

        # weeker condition allows prefix
        self.assertTrue(isprefix('a/b', 'a/b[c=cval/d'))

        # stronger condition prevents prefix
        self.assertFalse(isprefix('a/b[c=cval]', 'a/b/d'))

    def test_buildfromtokens(self):
        self.assertEqual(build_from_tokens(['music', 'body', 'mdiv', 'score']), 'music/body/mdiv/score')

    def test_insertselector(self):
        path = 'a/b/d'
        prefix = '/a/b'
        selector = 'c'
        self.assertEqual(insert_selector(path, prefix, selector), 'a/b/c/d')

        path =   'music/body/mdiv[label=label]/score'
        prefix = 'music/body/mdiv[label=label]'
        selector = '[n=1]'
        self.assertEqual(insert_selector(path, prefix, selector), 'music/body/mdiv[label=label,n=1]/score')

        path =   'a/b/c'
        prefix = ''
        selector = '[foo=bar]'
        self.assertEqual(insert_selector(path, prefix, selector), 'a[foo=bar]/b/c')

        path =   'a/c'
        prefix = ''
        selector = 'b[foo=bar]'
        self.assertEqual(insert_selector(path, prefix, selector), 'a/b[foo=bar]/c')

    def test_mergeattrtoken(self):
        self.assertEqual(merge_attrtoken('mdiv', '[foo=bar]'), 'mdiv[foo=bar]')
        self.assertEqual(merge_attrtoken('mdiv[foo=bar]', '[n=1]'), 'mdiv[foo=bar,n=1]')

    def test_splitpath(self):
        path = 'path/to/an/element/with[attr="http:\/\/example.com\/"]/and/more'
        tokens = split_path(path)
        self.assertEqual(len(tokens), 7)
        self.assertEqual(tokens, [
            'path', 'to', 'an', 'element', 
            'with[attr=http://example.com/]', 'and', 'more'
        ])

def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(PathTest, 'test'))
    return test_suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())

