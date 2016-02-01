dpthree
=======

This is a module to deal with the differences between Python 2 and Python 3
builtins.

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

`xrange` has been removed in Python 3. Well, sort of; `xrange` is replaced with
`range`, but with some increased functionality. For instance, in Python 3,
`range` objects can be larger than sys.maxsize.

`unicode` has been removed in Python 3. Well, again, sort of. `str` in Python 3
is more or less what `unicode` was in Python 2.

`reduce` has been moved to the functools module in Python 3

`basestring` has been removed in Python 3 as `str` and `bytes` do not share a 
common parent. Use `isinstance(obj, (str, bytes))` instead.