"""Temperature class with getter and setter."""

"""It lets you set and get temprature without
writing all the conversion methods between different measurements,
Kelvin (default), Celsius, Fahrenheit and Rankine
"""


class Temperature(object):
    """docstring for Temperature."""

    coefficients = {
        'c': (1.0, 0.0, -273.15),
        'f': (1.8, -273.15, 32.0),
        'r': (1.8, 0.0, 0.0)
    }

    def __init__(self, **kwargs):
        """Constructer."""
        try:
            name, value = kwargs.popitem()
        except KeyError:
            name, value = 'k', 0  # no arguments, default is Kelvin('k')

        if kwargs or name not in 'kcfr':
            kwargs[name] = value  # set it back for debugging purpose
            raise TypeError('invalid arguments %r' % kwargs)

        setattr(self, name, float(value))

    def __getattr__(self, name):
        """calculate c, f, r based on k."""
        try:
            eq = self.coefficients[name]
        except KeyError:
            raise AttributeError(name)

        return (self.k + eq[1]) * eq[0] + eq[2]

    def __setattr__(self, name, value):
        """calculate k's value based on input c, f, r."""
        if name in self.coefficients:
            # if c, f, r, calculate and set k's value based on it.
            eq = self.coefficients[name]
            self.k = (value - eq[2]) / eq[0] - eq[1]
        elif name == 'k':
            # if k, just set k's value
            object.__setattr__(self, name, value)
        else:
            raise AttributeError(name)

    def __str__(self):
        """Simply print."""
        return "%s K" % self.k

    # http://stackoverflow.com/questions/1436703/difference-between-str-and-repr-in-python
    # always implement __repr__ for printing, since __str__ uses it, too.
    def __repr__(self):
        """Detailed print."""
        return "Temperature(k=%r)" % self.k

if __name__ == "__main__":
    t = Temperature(f=70)
    print t.c

    t.c = 23
    print t.f
