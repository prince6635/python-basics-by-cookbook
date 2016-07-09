"""Making a Fast Copy of an Object.

You need to implement the special method __copy__ so that
your class can cooperate with the copy.copy function.
Because the _ _init_ _ method of your specific class happens to be slow,
you need to bypass it and get an "empty", uninitialized instance of the class.
"""


def empty_copy(obj):
    class Empty(obj.__class__):
        def __init__(self):
            pass

    new_copy = Empty()
    # .__class__ is a reference to the type of the current instance
    new_copy.__class__ = obj.__class__
    return new_copy


class MyClass(object):
    def __init__(self):
        # assume there's a lot of work here
        pass

    def my_print(self):
        print("test...")

    def __copy__(self):
        new_copy = empty_copy(self)
        # copy some relevant subset of self's attributes to newcopy
        # new_copy.__dict__.update(self.__dict__)
        # new_copy.__dict__ = dict(self.__dict__)

        return new_copy

    def __deepcopy__(self, memo):
        new_copy = empty_copy(self)
        # use copy.deepcopy(self.x, memo) to get deep copies of elements
        # in the relevant subset of self's attributes, to set in newcopy
        return new_copy

if __name__ == "__main__":
    import copy
    # does run __init__
    mc = MyClass()
    print(mc)
    # does NOT run __init__
    mc_copy = copy.copy(mc)
    mc_copy.my_print()
    print(mc_copy)
