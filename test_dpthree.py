"""Test module for dpthree."""
from __future__ import print_function, absolute_import, unicode_literals

import sys
import warnings

import dpthree
from dpthree import *

try:
    import unittest2 as unittest
except:
    import unittest


class TestDpthree(unittest.TestCase):
    def setUp(self):
        self.catcher = warnings.catch_warnings()
        self.catcher.__enter__()
        warnings.resetwarnings()
        warnings.simplefilter('error', DeprecationWarning)

    def test_warnings(self):
        with self.assertRaises(DeprecationWarning):
            unicode('unicode')

        with self.assertRaises(DeprecationWarning):
            xrange(10)

        with self.assertRaises(DeprecationWarning):
            reduce([1, 2, 3, 4, 5])

        with self.assertRaises(DeprecationWarning):
            raw_input('-> ')

    def test_names(self):
        if dpthree.PY2:
            self.assertEqual(unicode.__name__, 'unicode')
            self.assertEqual(str.__name__, 'unicode')
            self.assertEqual(bytes.__name__, 'str')

            self.assertEqual(range.__name__, 'xrange')
            self.assertEqual(raw_input.__name__, 'raw_input')

        if dpthree.PY3:
            self.assertEqual(unicode.__name__, 'str')
            self.assertEqual(str.__name__, 'str')
            self.assertEqual(bytes.__name__, 'bytes')

            self.assertEqual(xrange.__name__, 'range')
            self.assertEqual(raw_input.__name__, 'input')

    def tearDown(self):
        self.catcher.__exit__(None, None, None)


def test(*args, **kwargs):
    print('testing!')
    print(unicode('unicode'))

if __name__ == '__main__':
    # test()
    unittest.main(verbosity=2)
