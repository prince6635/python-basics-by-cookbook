"""Restricting Attribute Setting."""


def no_new_attributes(wrapped_setattr):
    """function to replace the default __setattr__.

    raise an error on attempts to add a new attribute,
    while allowing existing attributes to be set to new values.
    """
    def __setattr__(self, name, value):
        if hasattr(self, name):
            # not a new attribute, allow setting
            wrapped_setattr(self, name, value)
        else:
            # a new attribute, forbid adding it
            raise AttributeError("can't add attribute %r to %s" % (name, self))
    return __setattr__


class NoNewAttrs(object):
    """docstring for NoNewAttrs.

    subclasses of NoNewAttrs inhibit addition of new attributes,
    while allowing existing attributed to be set to new values.
    """

    __setattr__ = no_new_attributes(object.__setattr__)

    class __metaclass__(type):
        """simple custom metaclass.

        To block adding new attributes to this class.
        """

        __setattr__ = no_new_attributes(type.__setattr__)


class Person(NoNewAttrs):
    """docstring for Person."""

    first_name = ''
    last_name = ''

    def __init__(self, first_name, last_name):
        """Constructor."""
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self):
        """Representation of Person."""
        return 'Person(%r, %r)' % (self.first_name, self.last_name)


if __name__ == "__main__":
    me = Person("Zee", "Wong")
    print me
    me.first_name = "Zi"
    print me

    """ The point of inheriting from NoNewAttrs is forcing yourself to
    "declare" all allowed attributes by setting them at class level
    in the body of the class itself.
    Any further attempt to set a new,
    "undeclared" attribute raises an AttributeError """
    # Person.address = ''
    me.address = ''
