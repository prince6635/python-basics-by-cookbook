"""1, Automatically Initializing Instance Variables from __init__ Arguments.

Problem: You want to avoid writing and maintaining __init__ methods that
consist of almost nothing but a series of
    self.something = something assignments.
Solution: You can "factor out" the attribute-assignment task to an
auxiliary function

NOTE:
One problem with self.__dict__.update(locals()) is that it includes self,
so you get self.self. It would be better to filter self out of locals()

2, You want to ensure that __init__ is called for all superclasses that define
it, and Python does not do this automatically.
use: super(CurrentClassName, self).__init__()
"""


def attributes_from_dict(dict):
    self = dict.pop('self')
    for key, val in dict.iteritems():
        setattr(self, key, val)


def attributes_from_dict_simplified(self, dict):
    self.__dict__.update(dict)
    del self.self


def attributes_from_dict_from_arguments(dict):
    self = dict.pop('self')
    code_object = self.__init__.__func__.func_code
    argument_names = code_object.co_varnames[1:code_object.co_argcount]
    # for: def __init__(self, foo, bar, baz, boom=1, bang=2)
    # print: ('foo', 'bar', 'baz', 'boom', 'bang')
    print argument_names

    for name in argument_names:
        setattr(self, name, dict[name])


class InitRelated(object):
    # instead of:
    # def __init__(self, foo, bar, baz, boom=1, bang=2):
    #     self.foo = foo
    #     self.bar = bar
    #     self.baz = baz
    #     self.boom = boom
    #     self.bang = bang

    # use:
    def __init__(self, foo, bar, baz, boom=1, bang=2):
        super(InitRelated, self).__init__()

        # attributes_from_dict(locals())
        # attributes_from_dict_simplified(self, locals())
        attributes_from_dict_from_arguments(locals())


class Base1(object):
    def met(self):
        print "met in Base1"


class Derived1(Base1):
    def met(self):
        s = super(Derived1, self)
        if hasattr(s, 'met'):
            s.met()
        print('met in Derived1')


class Base2(object):
    pass


class Derived2(Base2):
    def met(self):
        s = super(Derived2, self)
        if hasattr(s, 'met'):
            s.met()
        print('met in Derived2')


import inspect


# here is one example of how you might code a class with a method that calls
# the superclass' version of the same method only if the latter is callable
# without arguments:
class Derived(Base1, Base2):
    def met(self):
        s = super(Derived, self)
        # get the superclass's bound-method object, or else None
        met = getattr(s, 'met', None)
        try:
            args, var_args, var_kw, defaults = inspect.getargspec(met)
            print args, var_args, var_kw, defaults
        except TypeError:
            # met is not a method, just ignore it
            pass
        else:
            # met is a method, do all its arguments have default values?
            if defaults is None or args is None or len(defaults) == len(args):
                # yes! so, call it:
                met()
        print('met in Derived')

if __name__ == "__main__":
    ir = InitRelated('f', 'b1', 'b2')
    print ir.__dict__

    Derived1().met()
    Derived2().met()
    Derived().met()
