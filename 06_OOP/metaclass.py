"""meta class."""

"""
Metaclass in python:
http://stackoverflow.com/questions/100003/what-is-a-metaclass-in-python
A metaclass is the class of a class.
Like a class defines how an instance of the class behaves,
a metaclass defines how a class behaves.
A class is an instance of a metaclass.

Metaprogramming:
A program could be designed to read, generate,
analyse or transform other programs, and even modify itself while running.

dynamically create a class in python:
http://programmers.stackexchange.com/questions/267318/does-dynamically-generating-classes-in-python-affect-readability-performance
"""


class BaseClass(object):
    """docstring for BaseClass."""

    def __init__(self, class_type=object):
        """Constructer."""
        self._type = class_type

    def get_type(self):
        """Get class's type."""
        return self._type


class SubClass(BaseClass):
    """docstring for SubClass."""

    __metaclass__ = type
    x = 23


def test_meta_class():
    """test meta class."""
    sub_obj = SubClass()
    print "SubClass: %s, %s" % (sub_obj.x, sub_obj.__metaclass__)

    # Equals: dynamically create a sub class
    AnotherSubClass = type('AnotherSubClass', (BaseClass,), {'x': 32})
    asc_obj = AnotherSubClass()
    print "AnotherSubClass: %s" % (asc_obj.x)


def ClassFactory(name, arg_names, BaseClass=BaseClass):
    """Dynamically create a derived class."""
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if key not in arg_names:
                raise TypeError(
                    "Argument %s not valid for %s" %
                    (key, self.__class__.__name__))
            setattr(self, key, value)
        print name[:-len("Class")]
        BaseClass.__init__(self, name[:-len("Class")])
    newclass = type(name, (BaseClass,), {"__init__": __init__})
    return newclass


def test_class_factory():
    """test class factory."""
    SpecialClass = ClassFactory("SpecialClass", "a b c".split())
    s = SpecialClass(a=2)
    print s.a
    print s.get_type()
    # s2 = SpecialClass(d=3)
    # print s2.a

if __name__ == "__main__":
    test_meta_class()
    test_class_factory()
