import unittest
import os
import sys

import test_path
import test_rowmodel
import test_rowdata
import test_header
import test_metadatadocument

def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(test_path.suite())
    test_suite.addTest(test_rowmodel.suite())
    test_suite.addTest(test_rowdata.suite())
    test_suite.addTest(test_header.suite())
    test_suite.addTest(test_metadatadocument.suite())
    return test_suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
