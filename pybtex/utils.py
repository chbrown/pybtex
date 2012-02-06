# Copyright (c) 2007, 2008, 2009, 2010, 2011  Andrey Golovizin
# 
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
# 
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


"""Miscellaneous small utils."""


from functools import wraps


def memoize(f):
    memory = {}
    @wraps(f)
    def new_f(*args):
        if args not in memory:
            memory[args] = f(*args)
        return memory[args]
    return new_f


class CaseInsensitiveDict(dict):
    """A dict with case-insensitive lookup.

    >>> d = CaseInsensitiveDict(TesT='passed')
    >>> d
    CaseInsensitiveDict({'TesT': 'passed'})
    >>> print d['TesT']
    passed
    >>> print d['test']
    passed
    >>> print d['Test']
    passed
    >>> d['Test'] = 'passed again'
    >>> print d['test']
    passed again
    >>> 'test' in d
    True
    >>> print d.keys()
    ['Test']
    >>> for key in d:
    ...     print key
    Test
    >>> for key, value in d.iteritems():
    ...     print key, value
    Test passed again
    >>> len(d)
    1
    >>> del d['test']
    >>> len(d)
    0
    >>> 'test' in d
    False
    >>> 'Test' in d
    False

    """
    def __init__(self, *args, **kwargs):
        initial_data = dict(*args, **kwargs)
        super(CaseInsensitiveDict, self).__init__(*args, **kwargs)
        self._keys = dict((key.lower(), key) for key in self)

    def __setitem__(self, key, value):
        """To implement lowercase keys."""
        key_lower = key.lower()
        try:
            existing_key = self._keys[key_lower]
        except KeyError:
            pass
        else:
            super(CaseInsensitiveDict, self).__delitem__(existing_key)
        super(CaseInsensitiveDict, self).__setitem__(key, value)
        self._keys[key_lower] = key

    def __getitem__(self, key):
        existing_key = self._keys[key.lower()]
        return super(CaseInsensitiveDict, self).__getitem__(existing_key)

    def __delitem__(self, key):
        key_lower = key.lower()
        existing_key = self._keys[key_lower]
        super(CaseInsensitiveDict, self).__delitem__(existing_key)
        del self._keys[key_lower]

    def pop(self, key, default=None):
        raise NotImplementedError
    
    def popitem(self):
        raise NotImplementedError
    
    def has_key(self, key):
        raise NotImplementedError
        
    def __contains__(self, key):
        return key.lower() in self._keys

    def setdefault(self, key, default=None):
        raise NotImplementedError
    
    def get(self, item, default=None):
        """A case insensitive get."""
        try:
            return self[self._keys[key.lower()]]
        except KeyError:
            return default

    def update(self, *args, **kwargs):
        raise NotImplementedError

    def copy(self):
        """Create a new caselessDict object that is a copy of this one."""
        return CaseInsensitiveDict(self)

    def clear(self):
        """Clear this caselessDict."""
        super(CaseInsensitiveDict, self).clear()
        self._keydict = {}

    def __repr__(self):
        """A caselessDict version of __repr__ """
        return '{0}({1})'.format(
            type(self).__name__, super(CaseInsensitiveDict, self).__repr__()
        )
