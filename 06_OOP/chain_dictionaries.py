"""Chaining Dictionary Lookups."""


class ChainedMap(object):
    """docstring for ChainedMap."""

    """it is not a "full mapping" even within the read-only design choice."""

    def __init__(self, *mappings):
        """Constructor."""
        # record the sequence of mappings into which we must look
        self._mappings = mappings

    def get(self, key, default=None):
        """return self[key] if present, otherwise `default`."""
        try:
            return self[key]
        except KeyError:
            return default

    def __getitem__(self, key):
        """try looking up into each mapping in queue."""
        for mapping in self._mappings:
            try:
                return mapping[key]
            except KeyError:
                pass

        # `key' not found in any mapping, so raise KeyError exception
        raise KeyError(key)

    def __contains__(self, key):
        """return True if `key' is present in self, otherwise False."""
        try:
            self[key]
            return True
        except KeyError:
            return False

    def __repr__(self):
        """print ChainedMap."""
        res = ""
        for mapping in self._mappings:
            line = ""
            for k, v in mapping.items():
                line += "({}:{})".format(k, v)
            res += line + "\n"
        return res


import UserDict
from sets import Set


class FullChainedMap(ChainedMap, UserDict.DictMixin):
    """docstring for FullChainedMap."""

    """You can make any partial mapping into a "full mapping" by inheriting
    from class DictMixin.
    Note:
    that the implementation in ChainedMap of methods get and _ _contains_ _
    is redundant (although innocuous) once we subclass DictMixin,
    since DictMixin also implements those two methods (as well as many others)
    in terms of lower-level methods"""

    def copy(self):
        """copy."""
        return self.__class__(self._mappings)

    def __iter__(self):
        """iterator."""
        visited = Set()
        for mapping in self._mappings:
            for key in mapping:
                if key not in visited:
                    yield key
                    visited.add(key)

    iterkeys = __iter__

    def keys(self):
        """keys."""
        return list(self)


import sys
if __name__ == "__main__":
    py_internal_lib_lookup = ChainedMap(
        locals(), globals(), vars(sys.modules["__builtin__"]))
    dict1 = {'Name': 'Zara', 'Age': 7, 'Class': 'First'}
    dict2 = {'Name': 'Zee', 'Age': 17, 'Class': 'Second'}
    dicts_lookup = ChainedMap(dict1, dict2)
    print dicts_lookup

    full_dicts_lookup = FullChainedMap(dict1, dict2)
    for key in full_dicts_lookup:
        print key
    full_dicts_lookup_copy = full_dicts_lookup.copy()
    print full_dicts_lookup_copy.__dict__
