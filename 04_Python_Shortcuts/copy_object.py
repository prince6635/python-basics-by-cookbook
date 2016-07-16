"""Copying an Object.

You want to copy an object. However, when you assign an object,
pass it as an argument, or return it as a result, Python uses a reference to
the original object, without making a copy.

copy.copy(obj) needs obj to be a copiable object, internally it'll call its own
type's copy function, list->list(obj), dictionary->dict(obj), set->set(obj)

to customize the copy function, override __copy__ or __deepcopy__

difference between is and ==:
    x = 'asd'
    y = 'asd'
    z = input() #write here string 'asd'. For Python 2.x use raw_input()
    x == y # True.
    x is y # True.
    x == z # True.
    x is z # False.
is checks for identity. a is b is True iff a and b are the same object
    (they are both stored in the same memory address).
== checks for equality, which is usually defined by the magic method __eq__ -
    i.e., a == b is True if a.__eq__(b) is True.
In your case specifically, Python optimizes the two hardcoded strings into the
same object (since strings are immutable, there's no danger in that). Since
input() will create a string at runtime, it can't do that optimization,
so a new string object is created.
"""

import copy


class UserDefinedObj(object):
    """docstring for UserDefinedObj."""
    def __init__(self, arg):
        super(UserDefinedObj, self).__init__()
        self.arg = arg
        self.my_list = [1, 2, 3]


def assign():
    # When you assign an object (or pass it as an argument,
    # or return it as a result), Python (like Java) uses a reference to
    # the original object, not a copy.
    a = [1, 2, 3]
    b = a
    print "{a:%s}-{b:%s}" % (a, b)
    a.append(6)
    print "{a:%s}-{b:%s}" % (a, b)


def shallow_copy():
    # case 1:
    existing_list = [1, 2, 3]
    new_list = copy.copy(existing_list)
    # not the same object
    print existing_list is new_list
    print existing_list == new_list
    print "{existing:%s}-{new:%s}" % (existing_list, new_list)
    new_list[0] = 6
    print "{existing:%s}-{new:%s}" % (existing_list, new_list)

    # case 2:
    a = [['foo'], [1, 2], ['bar', 23]]
    b = copy.copy(a)
    print "{a:%s}-{b:%s}" % (a, b)
    # only a will be changed
    a.append(['new'])
    print "{a:%s}-{b:%s}" % (a, b)
    # both a and b will be changed
    a[1].append('boo')
    print "{a:%s}-{b:%s}" % (a, b)

    # case 3:
    udo = UserDefinedObj("test")
    new_udo = copy.copy(udo)
    print udo is new_udo

    # !!! True since it's not copied recursively
    print udo.my_list is new_udo.my_list

    # case 4: for string
    s1 = 'cat'
    s2 = copy.copy(s1)
    # The is operator checks whether two objects are not merely equal (use ==),
    # but in fact the same object
    print "string copied:%s" % (s1 is s2)


def deep_copy():
    # want every item and attribute in the object to be separately copied,
    # recursively, use deepcopy
    udo = UserDefinedObj("test")
    new_udo = copy.deepcopy(udo)
    print udo is new_udo

    # False
    print udo.my_list is new_udo.my_list


if __name__ == "__main__":
    assign()
    shallow_copy()
    deep_copy()
