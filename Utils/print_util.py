"""Print utility functions."""

from pprint import pprint


def print_obj_user_defined(obj):
    """Print only user defined properties of an object."""
    pprint(vars(obj))
    print('===================')


def print_obj_all(obj):
    """Print all current properties of an object."""
    for attr in dir(obj):
        print "obj.%s = %s" % (attr, getattr(obj, attr))
    print('===================')


class TestClass(object):
    """docstring for TestClass."""

    def __init__(self, field1, field2):
        """Constructor."""
        self.field1 = field1
        self.field2 = field2
        self.maps = {
            "Name": "Zee",
            "Age": 1
        }

    def get_age(self):
        """Return age."""
        return self.Age


if __name__ == "__main__":
    tc = TestClass("f1", "f2")
    print_obj_all(tc)
    print_obj_user_defined(tc)
