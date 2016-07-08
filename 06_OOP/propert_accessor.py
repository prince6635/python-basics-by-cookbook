"""Your classes use some property instances.

where either the getter or the setter is just boilerplate code to fetch or
set an instance attribute. You would prefer to just specify the attribute name,
instead of writing boilerplate code.
"""


def xproperty(getter, setter, del_func=None, doc_func=None):
    if isinstance(getter, str):
        attr_name = getter

        def getter(obj):
            return getattr(obj, attr_name)
    elif isinstance(setter, str):
        attr_name = setter

        def setter(obj, val):
            setattr(obj, attr_name, val)
    else:
        raise TypeError('either getter or setter must by a string')

    return property(getter, setter, del_func, doc_func)


class Lower(object):
    def __init__(self, s=''):
        self.s = s

    def _getS(self):
        return self._s

    def _setS(self, s):
        self._s = s.lower()

    s = property(_getS, _setS)


class EnhancedLower(object):
    def __init__(self, s=''):
        self.s = s

    def _setS(self, s):
        self._s = s.lower()

    s = xproperty('_s', _setS)
