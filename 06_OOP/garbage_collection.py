"""Keeping References to Bound Methods Without Inhibiting Garbage Collection.

You want to hold references to bound methods, while still allowing the
associated object to be garbage-collected.
"""

import weakref
import new


class Ref(object):
    """Wraps any callable, most importantly a bound method,
    in a way that allows a bound method's object to be GC'ed,
    while providing the same interface as a normal weak reference."""
    def __init__(self, fn):
        try:
            # try to get object, function, and class
            o, f, c = fn.__self__, fn.__func__, fn.__class__
        except AttributeError:
            self._obj = None
            self._func = fn
            self._cls = None
        else:
            if o is None:
                self._obj = None
            else:
                self._obj = weakref.ref(o)

            self._func = f
            self._cls = c

    def __call__(self):
        if self._obj is None:
            return self._func
        elif self._obj() is None:
            return None
        return new.instancemethod(self._func, self._obj(), self._cls)


class ProxyRef(Ref):
    """If you want semantics closer to that of a weakref.proxy.

    they're easy to implement, for example by subclassing the Ref class.
    When you call a proxy, the proxy calls the referent with
    the same arguments. If the referent's object no longer lives,
    then weakref.ReferenceError gets raised instead.
    """
    def __call__(self, *args, **kwargs):
        func = Ref.__call__(self)
        if func is None:
            raise weakref.ReferenceError('reference object is dead')
        else:
            return func(*args, **kwargs)

    def __eq__(self, other):
        if type(other) != type(self):
            return False
        return Ref.__call__(self) == Ref.__call__(other)


class TestObj(object):
    """docstring for TestObj."""
    def f(self):
        print "Hello"

    def __del__(self):
        print "TestObj's instance is dying."

if __name__ == "__main__":
    to = TestObj()
    to_func = to.f
    # c continues to wander about with glazed eyes...
    # ...until we stake its bound method, only then it goes away:
    print("deleting to...")
    del to
    print("deleting to.f...")
    del to_func

    # throw exception since weakref.ref is a real weak reference
    to = TestObj()
    to_func_weakref = weakref.ref(to.f)
    # <weakref at 0x10b0667e0; dead>
    print(to_func_weakref)
    # TypeError: 'NoneType' object is not callable
    # to_func_weakref()()

    """Calling the Ref instance, which refers to a bound method,
    has the same semantics as calling a weakref.ref instance that refers to,
    say, a function object: if the referent has died, it returns None;
    otherwise, it returns the referent. Actually, in this case,
    it returns a freshly minted new.instancemethod (holding a strong reference
    to the objectso, be sure not to hold on to that, unless you do want to keep
    the object alive for a while!).
    """
    to = TestObj()
    to_func_customized_weak_ref = Ref(to.f)
    print(to_func_weakref)
    to_func_customized_weak_ref()()
    del to
    print(to_func_customized_weak_ref())
