# dpthree

[![Run Status](https://api.shippable.com/projects/58afc3c8b1c2a40600ebc14f/badge?branch=master)](https://app.shippable.com/projects/58afc3c8b1c2a40600ebc14f)
[![Coverage Status](https://api.shippable.com/projects/58afc3c8b1c2a40600ebc14f/coverageBadge?branch=master)](https://app.shippable.com/projects/58afc3c8b1c2a40600ebc14f)

--------------------------------------------------------------------------------

This is a module to deal with the differences between Python 2 and
Python 3 builtins.

The question then becomes, "Why not use another existing compatibility
package?"  Here is what I see is as issues with the currently existing
packages.

### six

`six` is a great package which has made it possible for lots of
software to deal with the differences between major Python
versions. It is completely contained in one file, which makes it easy
to deploy with code that can't reach out to the outisde world to grab
packages from `pypi` or whereever. Just plop the single file in your
code base and you are good to go.

However, six isn't what I would call "idiomatic". Once you use `six`,
it is obvious that you used it; there are `six`-isms sprinkled all
through out your code. Once you choose to use `six`, you are pretty
much locked in until you decide to do a massive refactoring of your
code to be rid of it. Thus, you can't simply remove a few boilerplate
lines of code per module and be done of it when you decide to drop
support for Python 2.x

### python-future

Another option is `python-future` from PythonCharmers. This _is_
idiomatic Python. When you use this package your code still looks
largely like vanilla python code and runs more or less as expected. A
few lines of boilerplate at the top of a file are often all that is
needed. However, it has the issue that it is a multi-file install
which places files _outside_ its primary package hierarchy. So, for
instance modules like `Tkinter` which have a changed name in Python 3,
now get explicity installed as `tkinter` in the top of the global module file hierarchy. In
some ways this is good: it uses the builtin `import` mechanisms to deal
with these packages. However, it also makes it unclear where stuff
lives and it means you pretty much _must_ be installing at the system
scope or have a `virtualenv` that you are installing into.  This just
doesn't jibe well with some project structures. So the idea is good
in theory, but crippled in practice. If you code base fits this
structure, then awesome! `python-future` is for you. If not, sorry,
move along.

### dpthree

`dpthree` is meant to be a balance of the two approaches. It attempts
to be close to idiomatic Python, like `python-future` is, but it
also is contained in a single file, like `six` is. It doesn't cover
the module issues as thouroughly or as cleanly as `python-future`
does, but it does address the most common aspects of it.

`dpthree` stands for "Duck Punch Three." This is because the builtins
for the current module get overwritten via Duck Punching. This is also
sometimes called Monkey Patching.

The module is generally intended to be imported with a star import,
like this:

    from dpthree.builtins import *

When imported this way, it will override builtin callables that have
different behaviour in Python 3. It also imports some callables that
have the same functionality, but different names in Python 3. For
instance, the unicode builtin in Python 2 is the same as the str
builtin in Python 3. It is defined here to help port old
code. However, any names that have been removed in Python 3 raise a
`DeprecationWarning` (which will either be ignored, printed, or raised
based on the warning level used). This should better help you discover
edge cases in your code base that still use deprecated and/or removed
features.

Removals to be made aware of:

`xrange` has been removed in Python 3. Well, sort of; `xrange` is
replaced with `range`, but with some increased functionality. For
instance, in Python 3, `range` objects can be larger than sys.maxsize.

`unicode` has been removed in Python 3. Well, again, sort of. `str` in
Python 3 is more or less what `unicode` was in Python 2.

`reduce` has been moved to the functools module in Python 3. In
`dpthree`, it can still be made available in the global `builtins`
space, but is now wrapped in a `DeprecationWarning` to help you find
any uses of it in your codebase. If `reduce` is used as part of the
`functools` module, it has no such `DeprecationWarning` raised.

`basestring` has been removed in Python 3 because `str` and `bytes` do
not share a common parent anymore. Use `isinstance(obj, (str, bytes))`
instead.
