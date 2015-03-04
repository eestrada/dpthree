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


class Test_dpthree(unittest.TestCase):
    def setUp(self):
        self.catcher = warnings.catch_warnings()
        self.catcher.__enter__()
        try:
            warnings.resetwarnings()
            warnings.simplefilter('ignore', DeprecationWarning)
        except:
            self.catcher.__exit__(None, None, None)
            raise

    def test_warnings(self):
        warnings.simplefilter('error', DeprecationWarning)

        with self.assertRaises(Warning):
            try:
                unicode('unicode')
            except Exception as e:
                # print(e, file=sys.stderr)
                raise

        with self.assertRaises(Warning):
            try:
                xrange(10)
            except Exception as e:
                # print(e, file=sys.stderr)
                raise

        with self.assertRaises(Warning):
            try:
                reduce([1, 2, 3, 4, 5])
            except Exception as e:
                # print(e, file=sys.stderr)
                raise

        with self.assertRaises(Warning):
            raw_input('-> ')

        with self.assertRaises(Warning):
            try:
                unichr(6000)
            except Exception as e:
                # print(e, file=sys.stderr)
                raise

        with self.assertRaises(Warning):
            try:
                bytechr(128)
            except Exception as e:
                # print(e, file=sys.stderr)
                raise

    def test_bytechr(self):
        with self.assertRaises(TypeError):
            bytechr('a string')  # should only accept integers

        with self.assertRaises(ValueError):
            bytechr(256)  # should be too large a value

        self.assertIsInstance(bytechr(0), bytes)  # only return byte strings

        for i in range(256):
            self.assertEqual(len(bytechr(i)), 1)

    def test_basestring(self):
        with self.assertRaises(TypeError):
            basestring()

        with self.assertRaises(TypeError):
            basestring('arg')

        with self.assertRaises(TypeError):
            basestring(key='value')

    def test_inheritance(self):
        self.assertIsInstance(unicode('unicode'), str)
        self.assertIsInstance('unicode string', unicode)

        self.assertIsInstance(bytes(), bytes)
        self.assertIsInstance(b'byte string', bytes)

        self.assertIsInstance(str(), basestring)
        self.assertIsInstance(bytes(), basestring)
        self.assertIsInstance('unicode string', basestring)
        self.assertIsInstance(b'byte string', basestring)

        self.assertIsInstance(xrange(1), range)
        self.assertIsInstance(xrange(1), xrange)

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

            self.assertEqual(raw_input.__name__, 'input')

            self.assertEqual(bytechr.__name__, 'bytechr')
            self.assertEqual(chr.__name__, 'chr')
            self.assertEqual(unichr.__name__, 'chr')

        # asserts for all versions
        self.assertEqual(xrange.__name__, 'xrange')

    def tearDown(self):
        self.catcher.__exit__(None, None, None)

if __name__ == '__main__':
    unittest.main()
