"""Test module for dpthree."""
from __future__ import print_function, absolute_import

import sys
import warnings

import dpthree

from dpthree import kludges
from dpthree import removed
from dpthree import builtins
from dpthree import modules


try:
    import unittest2 as unittest
except ImportError:
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

    def test_removed(self):
        for name in ('apply', 'basestring', 'buffer', 'long', 'cmp', 'coerce', 'reduce', 'reload', 'file',
                      'execfile', 'intern', 'unicode', 'raw_input', 'unichr'):
            with self.assertRaises(AttributeError):
                getattr(builtins, name)
                print('removed builtin %r still available' % name)

    def test_modules(self):
        from importlib import import_module
        if hasattr(modules, 'tkinter'):
            for mod in ('dpthree.modules.tkinter.', 'tkinter.'):
                for sub in ('scrolledtext', 'colorchooser', 'commondialog',
                            'filedialog', 'font', 'messagebox', 'simpledialog',
                            'dnd'):
                    import_module(mod + sub)

    def test_warnings(self):
        warnings.simplefilter('error', DeprecationWarning)

        with self.assertRaises(Warning):
            removed.unicode(u'unicode')

        with self.assertRaises(Warning):
            removed.xrange(10)

        with self.assertRaises(Warning):
            removed.reduce([1, 2, 3, 4, 5])

        with self.assertRaises(Warning):
            removed.raw_input('-> ')

        with self.assertRaises(Warning):
            removed.unichr(6000)

        with self.assertRaises(Warning):
            kludges.bytechr(128)

    def test_bytechr(self):
        with self.assertRaises(TypeError):
            kludges.bytechr(u'a string')  # should only accept integers

        with self.assertRaises(ValueError):
            kludges.bytechr(256)  # should be too large a value

        # only return byte strings
        self.assertIsInstance(kludges.bytechr(0), bytes)

        for i in range(256):
            self.assertEqual(len(kludges.bytechr(i)), 1)

    def test_basestring(self):
        with self.assertRaises(TypeError):
            removed.basestring()

        with self.assertRaises(TypeError):
            removed.basestring('arg')

        with self.assertRaises(TypeError):
            removed.basestring(key='value')

    def test_bytes(self):
        test_bytes = builtins.bytes(b'I am a bytes object.')
        self.assertIsInstance(test_bytes[0:1], builtins.bytes)
        self.assertIsInstance(test_bytes[0], builtins.int)

    @unittest.skipIf(not dpthree.PY2, "Test is only relevant in Python 2")
    def test_new_int(self):
        # duck punched int type inherits from Python 2 long type
        self.assertIsInstance(builtins.int(), long)

        self.assertEqual(builtins.int(), 0)

        self.assertEqual(builtins.int(1), 1.0)

        with self.assertRaises(ValueError):
            builtins.int('1L')

        with self.assertRaises(TypeError):
            builtins.int(1, base=10)

        with self.assertRaises(TypeError):
            builtins.int(1, 10)

        with self.assertRaises(TypeError):
            builtins.int(1, None)

    def test_inheritance(self):
        self.assertIsInstance(removed.unicode(u'unicode'), builtins.str)
        self.assertIsInstance(u'unicode string', removed.unicode)

        self.assertIsInstance(builtins.bytes(), builtins.bytes)
        self.assertIsInstance(b'byte string', builtins.bytes)

        self.assertIsInstance(builtins.str(), removed.basestring)
        self.assertIsInstance(builtins.bytes(), removed.basestring)
        self.assertIsInstance(u'unicode string', removed.basestring)
        self.assertIsInstance(b'byte string', removed.basestring)

        self.assertIsInstance(removed.xrange(1), builtins.range)
        self.assertIsInstance(removed.xrange(1), removed.xrange)

    def test_names(self):
        # name asserts for all versions
        self.assertEqual(kludges.bytechr.__name__, 'bytechr')

        self.assertEqual(removed.raw_input.__name__, 'raw_input')
        self.assertEqual(removed.unicode.__name__, 'unicode')
        self.assertEqual(removed.unichr.__name__, 'unichr')
        self.assertEqual(removed.xrange.__name__, 'xrange')

        self.assertEqual(builtins.bytes.__name__, 'bytes')

    @unittest.skipIf(not dpthree.PY2, "Test is only relevant in Python 2")
    def test_names2(self):
        self.assertEqual(builtins.str.__name__, 'unicode')
        self.assertEqual(builtins.range.__name__, 'xrange')
        self.assertEqual(builtins.chr.__name__, 'unichr')

    @unittest.skipIf(not dpthree.PY3, "Test is only relevant in Python 3")
    def test_names3(self):
        self.assertEqual(builtins.str.__name__, 'str')
        self.assertEqual(builtins.range.__name__, 'range')
        self.assertEqual(builtins.chr.__name__, 'chr')

    def tearDown(self):
        self.catcher.__exit__(None, None, None)

if __name__ == '__main__':
    unittest.main()
