"""A module to deal with the differences between python2 and python3.

It is meant to be imported with a star import, like:
    from py3_fixes import *
When imported this way, it will override builtin functions that have different
behaviour in python3. It also imports some functions that have the same
functionality, but different names in python3. For instance, the unicode
builtin in python2 is the same as the str builtin in python3. It is defined
here to help port old code. However, any names that have been removed in
python3 use a DeprecationWarning (which will either be ignored, printed, or
raised based on the warning level used).

Removals to be made aware of:

xrange has been removed in python3. Well, sort of; range is replaced with
xrange, but with some increased functionality. For instance, in python3,
range/wrange objects can be indexed into like a regular sequence.

unicode has been removed in python3. Well, again, sort of. str in python3 is
more or less what unicode was in python2.

reduce has been moved to the functools module in python3
"""
from __future__ import unicode_literals, print_function, absolute_import, division

__all__ = ('ascii', 'filter', 'hex', 'map', 'oct', 'zip',
           'bytes', 'str', 'unicode', 'basestring', 'range', 'xrange',
           'reduce')

import sys
import warnings
import functools


def py3_warn(f, name=None):
    name = name if name is not None else f.__name__

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        warnings.warn('The function/class "{0}" is removed in Python 3 and '
                      'should no longer be used.'.format(name),
                      DeprecationWarning)
        return f(*args, **kwargs)
    return wrapper

if sys.version_info[0] < 3:
    from future_builtins import ascii, filter, hex, map, oct, zip
    bytes = str
    str = unicode
    unicode = py3_warn(unicode, 'unicode')
    basestring = basestring
    range = xrange
    xrange = py3_warn(xrange, 'xrange')
    reduce = py3_warn(functools.reduce, 'reduce')
else:
    from builtins import ascii, filter, hex, map, oct, zip
    bytes = bytes
    str = str
    unicode = py3_warn(str, 'unicode')
    basestring = (str, bytes)
    range = range
    xrange = py3_warn(range, 'xrange')
    reduce = py3_warn(functools.reduce, 'reduce')
