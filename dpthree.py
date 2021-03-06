"""Module to deal with the differences between Python 2 and Python 3 builtins.

dpthree stands for "Duck Punch Three." This is because the builtins for the
current module get overwritten via Duck Punching. This is also sometimes called
Monkey Patching.

The module is meant to be imported with a star import, like this:
    from dpthree.builtins import *

When imported this way, it will override builtin callables that have different
behaviour in Python 3. It also imports some callables that have the same
functionality, but different names in Python 3. For instance, the unicode
builtin in Python 2 is the same as the str builtin in Python 3. It is defined
here to help port old code. However, any names that have been removed in
Python 3 raise a DeprecationWarning (which will either be ignored, printed, or
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
from __future__ import print_function, absolute_import, division

__all__ = ('builtins', 'removed', 'kludges')
# __all__ = ('builtins', 'tkinter', 'dbm', 'winreg')

import io
import sys
import abc
import types
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
    wrapper.__name__ = name

    # NOTE: this may cause issues. Consider removal.
    wrapper.__doc__ = f.__doc__.replace(f.__name__, name)

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

    @classmethod
    def __subclasshook__(cls, C):
        """Check inheritance against real underlying type(s)."""
        warnings.warn(wrnmsg, cat, stacklevel=4)
        return issubclass(C, subs)

    attrs = dict(__new__=__new__, __subclasshook__=__subclasshook__)

    return abc.ABCMeta(name, (object,), attrs)

# build PY3 style builtins module from scratch
if PY2:
    # TODO: add '__all__' attribute to homebrew builtins so that star
    # import only duck punches builtins with changed semantics

    # NOTE: fixes errors with unicode defaulting to using `ascii` codec.
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')

    # TODO: duck punch the builtin `object` type to hide compatibility
    # issues (e.g., `__bool__` versus `__nonzero__`, `__next__` versus
    # `next`, etc.). This might be dangerous, but worth a try at least.
    builtins = types.ModuleType('builtins')
    import __builtin__ as past_builtins
    import future_builtins

    builtins._past_builtins = past_builtins

    _to_remove = set(['apply', 'basestring', 'buffer', 'cmp', 'coerce',
                      'execfile', 'file', 'intern', 'long', 'raw_input',
                      'reduce', 'reload', 'unichr', 'unicode'])
    _to_add = set(n for n in dir(past_builtins) if not n.startswith('_'))
    _to_add.update(('__import__', '__doc__'))
    _to_add -= _to_remove
    for _attr in _to_add:
        setattr(builtins, _attr, getattr(past_builtins, _attr))

    # duck punch old names that mean something different in Py3
    for _set, _get in [('chr', 'unichr'), ('range', 'xrange'),
                       ('bytes', 'str'), ('str', 'unicode'),
                       ('input', 'raw_input')]:
        setattr(builtins, _set, getattr(past_builtins, _get))

    # old names with new semantics
    for _attr in ('ascii', 'filter', 'hex', 'map', 'oct', 'zip'):
        setattr(builtins, _attr, getattr(future_builtins, _attr))

    builtins.open = io.open

    # make builtins int act more like Python3 int (a la Python2 long)
    exec("""class int(_past_builtins.long):
    import abc
    __metaclass__ = abc.ABCMeta

    def __new__(cls, x=0, *args, **kwargs):
        # run super constructor first to cause other exceptions to be
        # raised first.
        self = super(int, cls).__new__(cls, x, *args, **kwargs)
        if isinstance(x, (str, bytes)) and x.endswith('L'):
            base = args[0] if args else kwargs.get('base', 10)
            raise ValueError("invalid literal for int() with base %r: '%s'" %
                             (base, x))
        return self

    def __repr__(self):
        return super(int, self).__repr__().rstrip('L')

    @classmethod
    def __subclasshook__(cls, C):
        return issubclass(C, (_past_builtins.int, _past_builtins.long))""", vars(builtins))

    exec("""class bytes(_past_builtins.bytes):
    import abc as _abc
    __metaclass__ = _abc.ABCMeta

    def __new__(cls, source=0, encoding='utf-8', errors='strict'):
        if isinstance(source, int):
            return super(bytes, cls).__new__(cls, b'\\0' * source)
        elif isinstance(source, _past_builtins.basestring):
            return super(bytes, cls).__new__(cls, source)
        else:  # assume an iterator of integers, such that: 0 <= integer < 256
            _ = b''.join(map(_past_builtins.chr, source))
            return super(bytes, cls).__new__(cls, _)

    def __getitem__(self, index):
        if isinstance(index, slice):
            return super(bytes, self).__getitem__(index)
        else:  # assume integral indexing
            return ord(super(bytes, self).__getitem__(index))

    def __repr__(self):
        return 'b' + super(bytes, self).__repr__()

    @classmethod
    def __subclasshook__(cls, C):
        return issubclass(C, _past_builtins.bytes)""", vars(builtins))

    exec("""def compile(source, filename, mode, flags=0, dont_inherit=False, optimize=-1, **kwargs):
    if isinstance(source, memoryview):
        source = source.tobytes()
    return _past_builtins.compile(source, filename, mode, flags, dont_inherit, **kwargs)""", vars(builtins))

    # TODO: duck punch `itertools.filterfalse` as an alias to `itertools.ifilterfalse`
    # TODO: wrap `itertools.imap`, `itertools.ifilter` and
    # `itertools.ifilterfalse` in a deprecation warning (after making the
    # `filterfalse` alias, so that it doesn't pick up the warning). Have the
    # warning point to the `six`, `future` and `dpthree` modules as compatibility options.

    del past_builtins, _to_add, _to_remove, future_builtins

    # This is only needed on PY2
    sys.modules['builtins'] = builtins

else:
    import builtins

# make sure importing works correctly for our builtins submodule in PY2 and PY3
sys.modules['.'.join([__name__, builtins.__name__])] = builtins

# removed builtin names
# These types and callables exist in Python 2 but not in Python 3 (or, they
# exist, but not by these names). They shouldn't be used, but can be helpful in
# getting Python 2 code to run in Python 3 with fewer modifications. Use of
# any of these raises a DeprecationWarning.
removed = types.ModuleType('removed', ('Builtins removed in Python 3.0 and '
                                       'above.\n\nNoteworthy: all callables '
                                       'in this module print/raise a '
                                       'DeprecationWarning when used.'))
sys.modules['.'.join([__name__, removed.__name__])] = removed

def _bs_raise(*args, **kwargs):
    """Pseudo constructor for basestring."""
    raise TypeError('The basestring type cannot be instantiated')

removed.basestring = _class_warn(_bs_raise,
                                 subs=(basestring,) if PY2 else (str, bytes),
                                 name='basestring')
removed.unicode = _class_warn(builtins.str, name='unicode')
removed.xrange = _class_warn(builtins.range, name='xrange')
removed.reduce = _func_warn(functools.reduce, 'reduce')
removed.raw_input = _func_warn(builtins.input, 'raw_input')
removed.unichr = _func_warn(builtins.chr, 'unichr')

del _bs_raise

# kludges for things that have no new equivalent in Python 3.
_kludge_doc = ('Kludges for Python 2 builtins that have no equivalent in '
               'Python 3. Use of these is discouraged, as this makes your '
               'software dependent on dpthree for, basically, forever. You '
               'should instead create your own solution or copy any needed '
               'solutions from the dpthree source.\n\nNoteworthy: all '
               'callables in this module print/raise a DeprecationWarning '
               'when used.')
kludges = types.ModuleType('kludges', _kludge_doc)
sys.modules['.'.join([__name__, kludges.__name__])] = kludges


def bytechr(i):
    """Return bytestring of one character with ordinal i; 0 <= i < 256."""
    if not 0 <= i < 256:
        if not isinstance(i, int):
            raise TypeError('an integer is required')
        else:
            raise ValueError('bytechr() arg not in range(256)')
    return chr(i).encode('latin1')

if PY2:
    bytechr = chr

_kldgmsg = ('The function/class "{name}" exists in neither versions 2 nor 3 '
            'of Python. It is merely a kludge to help cover up differences '
            'between the two versions.')

# since PY3 chr only works with unicode, this callable gives the Python 2
# behavior of chr
kludges.bytechr = _func_warn(bytechr, name='bytechr', msg=_kldgmsg)

# TODO: for PY3 make `bytestr` class that is like PY2 str class for use in PY3
# TODO: for PY3 make `nativestr` kludge that is PY2 `str` class in PY2 and PY3 `str` class in PY3

del _kludge_doc, _kldgmsg

# moved or renamed
modules = types.ModuleType('modules', 'Moved or renamed modules. Some of '
                           'these have extra or changed members.')
sys.modules['.'.join([__name__, modules.__name__])] = modules

_name_map = {'winreg': '_winreg',
             'configparser': 'ConfigParser',
             'copyreg': 'copy_reg',
             'queue': 'Queue',
             'socketserver': 'SocketServer',
             '_markupbase': 'markupbase',
             'reprlib': 'repr',
             'tkinter': 'Tkinter'}

if PY2:
    _names = _name_map.items()
else:
    _names = list(_name_map.keys())
    _names = zip(_names, _names)

for _new, _old in _names:
    try:
        _mod = __import__(_old, level=0)
    except ImportError:
        continue
    else:
        setattr(modules, _new, _mod)
        # duck punch relative to internal sub-module
        sys.modules['.'.join([__name__, 'modules', _new])] = _mod
        # also duck punch module module name as a top level name
        sys.modules[_new] = _mod

##################
# module renames #
##################

# TODO: change this to a sequence of pairs. Keeping them in sync as two separate
# sequences is a pain. (Why did I even do this in the first place?!)
_tk_old = ('ScrolledText', 'tkColorChooser', 'tkCommonDialog', 'tkFileDialog',
           'tkFont', 'tkMessageBox', 'tkSimpleDialog', 'Tkdnd', 'ttk', 'Tix',
           'Tkconstants')
_tk_new = ('scrolledtext', 'colorchooser', 'commondialog', 'filedialog',
           'font', 'messagebox', 'simpledialog', 'dnd', 'ttk', 'tix',
           'constants')


def _dp_tk2():
    mod = __import__('Tkinter', level=0)
    sys.modules['tkinter'] = mod
    for old, new in zip(_tk_old, _tk_new):
        try:
            smod = __import__(old, level=0)
        except ImportError as e:
            continue
        else:
            setattr(mod, new, smod)
            sys.modules['tkinter.' + new] = smod

    return mod

def _dp_tk3():
    # NOTE: although these exist in PY3, we make sure they are loaded, otherwise
    # submodule imports for dpthree.modules.tkinter will not work properly
    for _name in _tk_new:
        try:
            __import__('tkinter.' + _name, level=0)
        except ImportError as e:
            pass

if hasattr(modules, 'tkinter'):
    if PY2:
        _dp_tk2()
    else:
        _dp_tk3()

    for _name in _tk_new:
        if hasattr(modules.tkinter, _name):
            sys.modules['.'.join([__name__, 'modules.tkinter', _name])] = getattr(modules.tkinter, _name)

del _tk_old, _tk_new


def _load_dbm():
    dbm = types.ModuleType('dbm', '')
    anydbm = __import__('anydbm', level=0)
    setattr(dbm, '__doc__', getattr(anydbm, '__doc__', ''))

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


def _loadnewname(name):
    """Load modules by their new names."""
    if PY2 and name in _name_map:
        mods = sys.modules
        sys.modules = {}
        try:
            if name == 'dbm':
                mod = _load_dbm()
            elif name == 'tkinter':
                mod = _dp_tk_subs2()
            else:
                mod = __import__(_name_map[name], level=0)
            sys.modules[name] = mod
        finally:
            mods.update(sys.modules)
            sys.modules = mods


def loadnewnames():
    if PY2:
        for new in _name_map:
            _loadnewname(new)

#######################
# module duck punches #
#######################

def _PY2_module_duck_punches():
    """Duck punch old modules with new attributes they don't yet have."""
    import collections
    import UserDict

    collections.UserDict = UserDict.UserDict
    # TODO: wrap the old `UserDict.UserDict` in a deprecation warning

if PY2:
    _PY2_module_duck_punches()
