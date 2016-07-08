"""Delegating Special Methods in Proxies.

In the new-style object model, Python operations perform implicit lookups for
special methods
(https://docs.python.org/3/reference/datamodel.html#special-method-names)
on the class (rather than on the instance,
as they do in the classic object model).
Nevertheless, you need to wrap new-style instances in proxies that can also
delegate a selected set of special methods to the object they're wrapping.
"""

utils_path = ("/Users/ziwang/Documents/Projects/"
              "python/githubprojects/python-basics-by-cookbook/Utils")

import sys
print(utils_path)
sys.path.append(utils_path)
from print_util import print_obj_all, print_obj_user_defined


""" In the new-style object model.

Python operations don't look up special methods at runtime:
they rely on "slots" held in class objects. Such slots are updated when a class
object is built or modified. Therefore, a proxy object that wants to delegate
some special methods to an object it's wrapping needs to belong to a specially
made and tailored class. Fortunately, as this recipe shows, making and
instantiating classes on the fly is quite an easy job in Python.
"""


class Proxy(object):
    """base class for all proxies."""
    def __init__(self, obj):
        self._obj = obj

    def __getattr__(self, attrib):
        return getattr(self._obj, attrib)


def make_binder(unbound_method):
    def f(self, *a, **k):
        return unbound_method(self._obj, *a, **k)
    return f

known_proxy_classes = {}


"""Function proxy.

uses a "cache" of classes it has previously generated, the global dictionary
known_proxy_classes, keyed by the class of the object being wrapped and
the tuple of special methods' names being delegated. To make a new class,
proxy calls the built-in type, passing as arguments the name of the new class
(made by appending 'Proxy' to the name of the class being wrapped), class Proxy
as the only base, and an "empty" class dictionary (since it's adding no class
attributes yet). Base class Proxy deals with initialization and delegation of
ordinary attribute lookups. Then, factory function proxy loops over the names
of specials to be delegated: for each of them, it gets the unbound method from
the class of the object being wrapped, and sets it as an attribute of the new
class within a make_binder closure. make_binder deals with calling the unbound
method with the appropriate first argument
(i.e., the object being wrapped, self._obj).
"""


def proxy(obj, *specials):
    """factory-function for a proxy able to delegate special methods."""
    # do we already have a suitable customized class around?
    # !!! .__class__ is a reference to the type of the current instance.
    obj_cls = obj.__class__
    key = obj_cls, specials
    # (<type 'list'>, ('len', 'iter'))
    print(key)

    tests = 1, "test"
    # (1, 'test')
    print(tests)

    cls = known_proxy_classes.get(key)
    if cls is None:
        # we don't have a suitable class around, so let's make it
        cls = type("%sProxy" % obj_cls.__name__, (Proxy,), {})
        # print(cls)

        for name in specials:
            name = '__%s__' % name
            unbound_method = getattr(obj_cls, name)
            setattr(cls, name, make_binder(unbound_method))
        # also cache it for the future
        known_proxy_classes[key] = cls
    # instantiate and return the needed proxy
    return cls(obj)


if __name__ == "__main__":
    # only deletegate __len__ and __iter__
    a = proxy([], 'len', 'iter')
    print(a)
    print(a.__class__)
    print(a._obj)

    # all non-special methods are deletegated
    print(a.append)

    # __len__ and __iter__ are delegated special methods
    print(len(a))
    a.append(23)
    print(len(a))

    for x in a:
        print x
    print(list(a))
    print(sum(a))
    print(max(a))

    # error since __getitem__ is not delegated
    print(a[0])
