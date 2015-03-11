"""Module to deal with the differences between Python 2 and Python 3 builtins.

dpthree stands for "Duck Punch Three." This is because the builtins for the
current module get overwritten via Duck Punching. This is also sometimes called
Monkey Patching.

The module is meant to be imported with a star import, like this:
    from dpthree import *

When imported this way, it will override builtin callables that have different
behaviour in Python 3. It also imports some callables that have the same
functionality, but different names in Python 3. For instance, the unicode
builtin in Python 2 is the same as the str builtin in Python 3. It is defined
here to help port old code. However, any names that have been removed in
Python 3 use a DeprecationWarning (which will either be ignored, printed, or
raised based on the warning level used).

Removals to be made aware of:

xrange has been removed in Python 3. Well, sort of; xrange is replaced with
range, but with some increased functionality. For instance, in Python 3,
range objects can be larger than sys.maxsize.

unicode has been removed in Python 3. Well, again, sort of. str in Python 3 is
more or less what unicode was in Python 2.

reduce has been moved to the functools module in Python 3

basestring has been removed in Python 3 as str and bytes do not share a common
parent. Use isinstance(obj, (str, bytes)) instead.
"""
from __future__ import print_function, absolute_import

__all__ = ('ascii', 'filter', 'hex', 'map', 'oct', 'zip',
           'bytes', 'str', 'basestring', 'range', 'input', 'chr',
           'unicode', 'xrange', 'reduce', 'raw_input', 'unichr')

import sys
import abc
import warnings
import functools

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3


def _func_warn(f, name=None, msg=None, cat=DeprecationWarning):
    """Wrap callables with a deprecation warning."""
    name = name if name is not None else f.__name__
    wrnmsg = ('The builtin callable "{name}" is removed in Python 3 and '
              'should no longer be used.'.format(name=name))

    wrnmsg = wrnmsg if msg is None else msg.format(name=name)

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        warnings.warn(wrnmsg, cat, stacklevel=2)
        return f(*args, **kwargs)

    return wrapper


def _class_warn(return_type, subs=None, name=None, msg=None,
                cat=DeprecationWarning):
    subs = (return_type,) if subs is None else subs

    name = name if name is not None else return_type.__name__
    wrnmsg = ('The builtin type "{name}" is removed in Python 3 and '
              'should no longer be used.')

    wrnmsg = wrnmsg if msg is None else msg
    wrnmsg = wrnmsg.format(name=name)

    def __new__(cls, *args, **kwargs):
        """Use as factory function for real underlying type."""
        warnings.warn(wrnmsg, cat, stacklevel=2)
        return return_type(*args, **kwargs)

    def __subclasshook__(cls, C):
        """Check inheritance against real underlying type(s)."""
        warnings.warn(wrnmsg, cat, stacklevel=4)
        return issubclass(C, subs)

    __subclasshook__ = classmethod(__subclasshook__)

    attrs = dict(__new__=__new__, __subclasshook__=__subclasshook__)

    return abc.ABCMeta(name, (object,), attrs)

if PY2:
    from future_builtins import ascii, filter, hex, map, oct, zip
    bytes = str
    str = unicode
    _bs_subs = (basestring,)
    range = xrange
    input = raw_input
    bytechr = chr
    chr = unichr
else:
    from builtins import ascii, filter, hex, map, oct, zip
    bytes = bytes
    str = str
    _bs_subs = (str, bytes)
    range = range
    input = input

    def bytechr(i):
        """Return bytestring of one character with ordinal i; 0 <= i < 256."""
        if not 0 <= i < 256:
            if not isinstance(i, int):
                raise TypeError('an integer is required')
            else:
                raise ValueError('bytechr() arg not in range(256)')
        return chr(i).encode('latin1')

    chr = chr


# code for both versions of Python
# These work for both since we have already redifined the input callables to
# match Python 3.
# These types and callables exist in Python 2 but not in Python 3 (or, they
# exist, but not by these names). They shouldn't be used, but can be helpful in
# getting Python 2 code to run in Python 3 with fewer modifications. Use of
# any of these raises a DeprecationWarning.
def _bs_raise(*args, **kwargs):
    raise TypeError('The basestring type cannot be instantiated')

unicode = _class_warn(str, name='unicode')
basestring = _class_warn(_bs_raise, subs=_bs_subs, name='basestring')
xrange = _class_warn(range, name='xrange')
reduce = _func_warn(functools.reduce, 'reduce')
raw_input = _func_warn(input, 'raw_input')
unichr = _func_warn(chr, 'unichr')

# kludges for things that have no new equivalent in Python 3.
_kldgmsg = ('The function/class "{name}" exists in neither versions 2 or 3 of '
            'Python. It is merely a kludge to help cover up differences '
            'between the two versions.')

# since chr now only works with unicode, this callable gives the Python 2
# behavior of chr
bytechr = _func_warn(bytechr, name='bytechar', msg=_kldgmsg)

_name_map = {'builtins': '__builtin__',
             'winreg': '_winreg',
             'configparser': 'ConfigParser',
             'copyreg': 'copy_reg',
             'queue': 'Queue',
             'socketserver': 'SocketServer',
             '_markupbase': 'markupbase',
             'reprlib': 'repr',
             'test.support': 'test.test_support',
             'tkinter': 'Tkinter'}


def _load_tk():
    old = ('ScrolledText', 'tkColorChooser', 'tkCommonDialog', 'tkFileDialog',
           'tkFont', 'tkMessageBox', 'tkSimpleDialog', 'Tkdnd', 'ttk', 'Tix')
    new = ('scrolledtext', 'colorchooser', 'commondialog', 'filedialog',
           'font', 'messagebox', 'simpledialog', 'dnd', 'ttk', 'tix')

    mod = __import__('Tkinter', level=0)
    sys.modules.pop('Tkinter')
    for old, new in zip(old, new):
        setattr(mod, new, __import__(old, level=0))

    return mod


def _load_dbm():
    mod = __import__('anydbm', level=0)
    sys.modules.pop('anydbm')

    if sys.modules['dbm'] == mod:  # we've done this before
        return mod

    old = ('dbm', 'gdbm', 'dumbdbm', 'whichdb')
    new = ('ndbm', 'gnu', 'dumb', 'whichdb')
    attr = (None, None, None, 'whichdb')

    for old, new, attr in zip(old, new, attr):
        old = __import__(old, level=0)
        if attr is not None:
            old = getattr(old, attr)
        setattr(mod, new, old)

    return mod


def loadnewname(name):
    """Load modules by their new names."""
    if PY2 and name in _name_map:
        mods = sys.modules
        sys.modules = {}
        try:
            if name == 'dbm':
                mod = _load_dbm()
            elif name == 'tkinter':
                mod = _load_tk()
            else:
                mod = __import__(_name_map[name], level=0)
            sys.modules[name] = mod
        finally:
            mods.update(sys.modules)
            sys.modules = mods


def loadallnew():
    if PY2:
        for new, old in _name_map:
            mod = __import__(old, level=0)
            sys.modules[new] = mod
