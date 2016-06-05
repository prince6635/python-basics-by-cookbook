"""This module shows a polymorphic in OOP."""


class Repeater(object):
    """docstring for Repeater."""

    def __init__(self):
        """Constructer."""
        pass

    def repeat(self, N):
        """Repeatly print a string."""
        print N * "*-*"


class Printer(object):
    """docstring for Printer."""

    def __init__(self):
        """Constructer."""
        pass

    def repeat(self, N):
        """Repeatly print a string."""
        for i in range(N):
            print "This is Printer.repeat!"


def test_polymorphism():
    """test method for polymorphic."""
    repeater = Repeater()
    printer = Printer()

    mixed_objs = repeater, printer, Repeater(), Printer()
    for whatever in mixed_objs:
        whatever.repeat(3)

if __name__ == "__main__":
    test_polymorphism()
