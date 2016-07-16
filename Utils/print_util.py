"""Print utility functions."""

from pprint import pprint


def print_obj(obj):
    """Print only __dict__"""
    print(obj.__dict__)
    print('===================')


def print_obj_user_defined(obj):
    """Print only user defined properties of an object."""
    pprint(vars(obj))
    print('===================')


def print_obj_all(obj):
    """Print all current properties of an object."""
    for attr in dir(obj):
        print "obj.%s = %s" % (attr, getattr(obj, attr))
    print('===================')


def print_exception(ex):
    ex_template = "An exception of type {0} occured. Arguments:\n{1!r}"
    ex_message = ex_template.format(type(ex).__name__, ex.args)
    print ex_message
    print('===================')


def print_cur_memory():
    import psutil
    import os
    # https://pythonhosted.org/psutil/
    # in bytes
    bs = psutil.Process(os.getpid()).memory_info().rss
    from hurry.filesize import size
    mbs = size(bs)
    print mbs


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

err = IOError("io error!")


def throw_exception():
    raise err

if __name__ == "__main__":
    tc = TestClass("f1", "f2")
    # print_obj_all(tc)
    # print_obj_user_defined(tc)
    print_obj(tc)

    try:
        throw_exception()
    # except Exception as ex:
        # print_exception(ex)
    # except err:
    except IOError:
        print('done')

    print_cur_memory()
