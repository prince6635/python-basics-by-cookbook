"""Singleton.

You want to make sure that only one instance of a class is ever created.
Just have your class inherit from Singleton, and don't override __new__.
Then, all calls to that class (normally creations of new instances) return the
same instance. (The instance is created once, on the first such call to each
given subclass of Singleton during each run of your program.)
"""


class Singleton(object):
    """A Pythonic Singleton."""
    def __new__(cls, *args, **kwargs):
        if '_instance' not in vars(cls):
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance


""" Avoiding the "Singleton" Design Pattern with the Borg Idiom.

Problem: You want to make sure that only one instance of a class is ever
created: you don't care about the id of the resulting instances, just about
their state and behavior, and you need to ensure subclassability.
Solution: Application needs (forces) related to the "Singleton" Design Pattern
can be met by allowing multiple instances to be created while ensuring that all
instances share state and behavior. This is more flexible than fiddling with
instance creation. Have your class inherit from the following Borg class.

NOTE: If you override __new__ in your class (very few classes need to do that),
just remember to use BorgSingleton.__new__, rather than object.__new__,
within your override. If you want instances of your class to share state among
themselves, but not with instances of other subclasses of BorgSingleton, make
sure that your class has, at class scope, the "state"ment:
    _shared_state = {}
With this "data override", your class doesn't inherit the _shared_state
attribute from BorgSingleton but rather gets its own. It is to enable this
"data override" that BorgSingleton's __new__ uses cls._shared_state instead of
BorgSingleton._shared_state.
"""


class BorgSingleton(object):
    _shared_state = {}

    def __new__(cls, *args, **kwargs):
        obj = object.__new__(cls, *args, **kwargs)
        obj.__dict__ = cls._shared_state
        return obj

    # since the instance's ids diff, rewrite __hash__ and __eq__
    # to make them to behave the same one when they're used as keys in dict.
    def __hash__(self):
        # any arbitrary constant integer
        return 9

    def __eq__(self, other):
        try:
            return self.__dict__ is other.__dict__
        except AttributeError:
            return False


"""Summary:
The Singleton Design Pattern is all about ensuring that just one instance of a
certain class is ever created. In my experience, Singleton is generally not the
best solution to the problems it tries to solve, producing different kinds of
issues in various object models. We typically want to let as many instances be
created as necessary, but all with shared state. Who cares about identity?
It's state (and behavior) we care about. The alternate pattern based on sharing
state, in order to solve roughly the same problems as Singleton does, has also
been called Monostate. Incidentally, I like to call Singleton "Highlander"
because there can be only one.

In Python, you can implement the Monostate Design Pattern in many ways, but the
Borg design nonpattern is often best. Simplicity is Borg's greatest strength.
Since the __dict__ of any instance can be rebound, Borg in its __new__ rebinds
the __dict__ of each of its instances to a class-attribute dictionary. Now,
any reference or binding of an instance attribute will affect all instances
equally. I thank David Ascher for suggesting the appropriate name Borg for this
nonpattern. Borg is a nonpattern because it had no known uses at the time of
its first publication (although several uses are now known): two or more known
uses are part of the prerequisites for being a design pattern.
See the detailed discussion at http://www.aleax.it/5ep.html.

Borg odds and ends:
The __getattr__ and __setattr__ special methods are not involved in Borg's
operations. Therefore, you can define them independently in your subclass, for
whatever other purposes you may require, or you may leave these special methods
undefined. Either way is not a problem because Python does not call __setattr__
in the specific case of the rebinding of the instance's __dict__ attribute.
Borg does not work well for classes that choose to keep some or all of their
per-instance state somewhere other than in the instance's __dict__. So, in
subclasses of Borg, avoid defining __slots__that's a memory-footprint
optimization that would make no sense, anyway, since it's meant for classes
that have a large number of instances, and Borg subclasses will effectively
have just one instance! Moreover, instead of inheriting from built-in types
such as list or dict, your Borg subclasses should use wrapping and automatic
delegation. (I named this latter twist "DeleBorg,"
in my paper available at http://www.aleax.it/5ep.html.)
"""


if __name__ == "__main__":
    class SingletonSpam(Singleton):
        def __init__(self, arg):
            self.arg = arg

        def spam(self):
            return self.arg

    ss1 = SingletonSpam('spam1')
    print(id(ss1), ss1.spam())
    ss2 = SingletonSpam('spam2')
    print(id(ss2), ss2.spam())

    """
    One issue with Singleton in general is subclassability.
    The way class Singleton is coded in this recipe, each descendant subclass,
    direct or indirect, will get a separate instance. Literally speaking,
    this violates the constraint of only one instance per class, depending on
    what one exactly means by it:
    """
    class Foo(Singleton):
        pass

    class Bar(Foo):
        pass
    f = Foo()
    b = Bar()
    # emits False True True
    print(f is b, isinstance(f, Foo), isinstance(b, Foo))

    # BorgSingleton
    class BorgSingletonExample(BorgSingleton):
        name = None

        def __init__(self, name=None):
            if name is not None:
                self.name = name

        def __str__(self):
            return 'name->%s' % self.name

    a = BorgSingletonExample('Zee')
    b = BorgSingletonExample()
    # instantiating b shares self.name with a
    print a, b
    c = BorgSingletonExample('Zi')
    # making c changes self.name of a & b too
    print a, b, c
    b.name = "Z"
    # setting b.name changes name of a & c too
    print a, b, c

    print id(a), id(b), id(c)
    singletons_dict = {}
    val = 0
    for i in a, b, c:
        singletons_dict[i] = val
        val += 1
    for i in a, b, c:
        print i, singletons_dict[i]
