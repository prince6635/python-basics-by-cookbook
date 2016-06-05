"""This module shows inheritance in OOP."""


class BaseClass(object):
    """docstring for BaseClass."""

    def __init__(self, name):
        """Constructer."""
        self.name = name

    def once(self):
        """Print name once."""
        print "BaseClass, ", self.name

    def repeat(self, N):
        """Repeat printing names."""
        for i in range(N):
            self.once()


class SubClass(BaseClass):
    """docstring for SubClass."""

    def __init__(self, name):
        """!!!Call base's Constructer first!!!.

        equals: BaseClass.__init__(self, name)
        """
        super(SubClass, self).__init__(name)

    def once(self):
        """Print name once."""
        print "SubClass, (%s)" % self.name


class OneMoreThanBase(BaseClass):
    """docstring for OneMoreThanBase."""

    def __init__(self, name):
        """Constructer."""
        super(OneMoreThanBase, self).__init__(name)

    def repeat(self, N):
        """repeatly print N + 1 than BaseClass.repeat."""
        # or: BaseClass.repeat(self, N + 1)
        super(OneMoreThanBase, self).repeat(N + 1)


def test_inheritance():
    """test inheritance in OOP."""
    sub_obj = SubClass("Queen Bee's Child")
    sub_obj.repeat(3)

    one_more_obj = OneMoreThanBase("Base's one more")
    one_more_obj.repeat(3)

if __name__ == "__main__":
    test_inheritance()
