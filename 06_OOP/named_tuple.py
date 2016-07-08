"""named tuples.

Python tuples are handy ways to group pieces of information,
but having to access each item by numeric index is a bother.
You'd like to build tuples whose items are also accessible as named attributes.
"""

from operator import itemgetter

"""Function super_tuple's implementation is quite straightforward.
To build the new subclass, superTuple uses a class statement,
and in that statement's body, it defines three specials: an "empty" __slots__
(just to save memory, since our supertuple instances don't need any
per-instance dictionary anyway); a __new__ method that checks the number of
arguments before delegating to tuple.__new__; and an appropriate __repr__
method. After the new class object is built, we set into it a property for each
named attribute we want. Each such property has only a "getter",
since our supertuples, just like tuples themselves, are immutableno setting of
fields. Finally, we set the new class' name and return the class object.
Each of the getters is easily built by a simple call to the built-in itemgetter
from the standard library module operator.
"""


def super_tuple(type_name, *attribute_names):
    " create and return a subclass of `tuple', with named attributes "
    # make the subclass with appropriate _ _new_ _ and _ _repr_ _ specials
    attr_len = len(attribute_names)

    class SuperTuple(tuple):
        """SuperTuple."""
        # save memory, we don't need per-instance dict
        # http://stackoverflow.com/questions/472000/usage-of-slots
        __slots__ = ()

        def __new__(cls, *args):
            if len(args) != attr_len:
                raise TypeError(
                    '%s takes exactly %d arguments (%d given)' %
                    (type_name, attr_len, len(args)))
            return tuple.__new__(cls, args)

        def __repr__(self):
            return '%s(%s)' % (type_name, ', '.join(map(repr, self)))

    # add a few key touches to our new subclass of `tuple'
    for index, attr_name in enumerate(attribute_names):
        setattr(SuperTuple, attr_name, property(itemgetter(index)))
    SuperTuple.__name__ = type_name
    return SuperTuple

if __name__ == "__main__":
    # regular tuple
    tup1 = ('physics', 'chemistry', 1997, 2000)
    tup2 = (1, 2, 3, 4, 5, 6, 7)

    print "tup1[0]: ", tup1[0]
    print "tup2[1:5]: ", tup2[1:5]

    # named tuple
    Point = super_tuple('Point', 'x', 'y')
    print(Point)
    # wrong number of fields
    # p = Point(1, 2, 3)
    p = Point(1, 2)
    print(p)
    print(p.x)
    print(p.y)
