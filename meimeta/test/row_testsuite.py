import unittest
import os
import sys

import test_rowmodel
import test_rowdata

def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(test_rowmodel.suite())
    test_suite.addTest(test_rowdata.suite())
    return test_suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
