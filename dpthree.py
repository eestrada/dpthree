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
"""
from __future__ import print_function, absolute_import

__all__ = ('ascii', 'filter', 'hex', 'map', 'oct', 'zip', 'input',
           'bytes', 'str', 'unicode', 'basestring', 'range', 'xrange',
           'reduce', 'input', 'raw_input')

import sys
import warnings
import functools

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3


def py3_warn(f, name=None):
    """Wrap callables with a deprecation warning."""
    name = name if name is not None else f.__name__

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        warnings.warn('The function/class "{0}" is removed in Python 3 and '
                      'should no longer be used.'.format(name),
                      DeprecationWarning, stacklevel=2)
        return f(*args, **kwargs)
    return wrapper

if PY2:
    from future_builtins import ascii, filter, hex, map, oct, zip
    bytes = str
    str = unicode
    basestring = basestring
    range = xrange
    input = raw_input
else:
    from builtins import ascii, filter, hex, map, oct, zip
    bytes = bytes
    str = str
    basestring = (str, bytes)
    range = range
    input = input

# code for both versions of Python
# These work for both since we have already redifined these callables to match
# Python 3.
unicode = py3_warn(str, 'unicode')
xrange = py3_warn(range, 'xrange')
reduce = py3_warn(functools.reduce, 'reduce')
raw_input = py3_warn(input, 'raw_input')
