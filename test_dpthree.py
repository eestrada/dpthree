"""Test module for dpthree."""
from __future__ import print_function, absolute_import, unicode_literals

import sys
import warnings

import dpthree
from dpthree import *
from dpthree import bytechr

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
        with self.assertRaises(Warning):
            try:
                unicode('unicode')
            except Exception as e:
                print(e, file=sys.stderr)
                raise

        with self.assertRaises(Warning):
            try:
                xrange(10)
            except Exception as e:
                print(e, file=sys.stderr)
                raise

        with self.assertRaises(Warning):
            try:
                reduce([1, 2, 3, 4, 5])
            except Exception as e:
                print(e, file=sys.stderr)
                raise

        with self.assertRaises(Warning):
            raw_input('-> ')

        with self.assertRaises(Warning):
            try:
                unichr(6000)
            except Exception as e:
                print(e, file=sys.stderr)
                raise

        with self.assertRaises(Warning):
            try:
                bytechr(128)
            except Exception as e:
                print(e, file=sys.stderr)
                raise

    def test_inheritance(self):
        warnings.resetwarnings()
        # self.assertIsInstance(unicode('unicode'), str)
        # self.assertIsInstance(str, basestring)
        # self.assertIsInstance(bytes, basestring)

    def test_names(self):
        if dpthree.PY2:
            self.assertEqual(unicode.__name__, 'unicode')
            self.assertEqual(str.__name__, 'unicode')
            self.assertEqual(bytes.__name__, 'str')

            self.assertEqual(range.__name__, 'xrange')
            self.assertEqual(raw_input.__name__, 'raw_input')

            self.assertEqual(bytechr.__name__, 'chr')
            self.assertEqual(chr.__name__, 'unichr')
            self.assertEqual(unichr.__name__, 'unichr')

        if dpthree.PY3:
            self.assertEqual(unicode.__name__, 'unicode')
            self.assertEqual(str.__name__, 'str')
            self.assertEqual(bytes.__name__, 'bytes')

            self.assertEqual(xrange.__name__, 'range')
            self.assertEqual(raw_input.__name__, 'input')

            self.assertEqual(bytechr.__name__, 'bytechr')
            self.assertEqual(chr.__name__, 'chr')
            self.assertEqual(unichr.__name__, 'chr')

    def tearDown(self):
        self.catcher.__exit__(None, None, None)

if __name__ == '__main__':
    unittest.main()
