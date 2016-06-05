"""This module shows a basic class in python.

Python's class should always inherit from object.
http://stackoverflow.com/questions/4015417/python-class-inherits-object
Python 3.x:
    class MyClass(object): = new-style class
    class MyClass: = new-style class (implicitly inherits from object)
Python 2.x:
    class MyClass(object): = new-style class
    class MyClass: = OLD-STYLE CLASS
"""


class Behave(object):
    """An example class has behaviors."""

    def __init__(self, name, num=1):
        """!!!Constructer!!!."""
        self.name = name
        self.num = num

    def once(self):
        """Print name once."""
        print "Hello, ", self.name

    def rename(self, newName):
        """Change name variable."""
        print "Hello, ", self.name
        self.name = newName

    def repeat(self, N):
        """Repeat printing names."""
        for i in range(N):
            self.once()

    def __add__(self, another_behave):
        """Override __add__ for Behave.

        so b1 + b2 will use b1.__add__(b2) first,
        if it doesn't work, will try b2.__add__(b1).
        """
        return self.num + another_behave.num


def test_behave_class():
    """Method to test Behave class."""
    bh = Behave("Queen Bee")
    bh.repeat(3)
    bh.rename("Stringer")
    bh.once()
    print bh.name
    bh.name = "See, you can rebind it here"
    bh.repeat(2)

    bh1 = Behave("B1", 10)
    bh2 = Behave("B2", 20)
    print bh1 + bh2

if __name__ == "__main__":
    test_behave_class()
