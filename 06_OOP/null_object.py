"""Implementing the Null Object Design Pattern.

You want to reduce the need for conditional statements in your code,
particularly the need to keep checking for special cases.
Solution: The usual placeholder object for "there's nothing here" is None,
but we may be able to do better than that by defining a class meant exactly
to act as such a placeholder.

You can use an instance of the Null class instead of the primitive value None.
By using such an instance as a placeholder, instead of None, you can avoid many
conditional statements in your code and can often express algorithms with
little or no checking for special values.
"""


class Null(object):
    """ Null objects always and reliably "do nothing." """
    # optional optimization: ensure only one instance per subclass
    # (essentially just to save memory, no functional difference)
    def __new__(cls, *args, **kwargs):
        # make it a singleton
        if '_instance' not in vars(cls):
            cls._instance = super(Null, cls).__new__(cls)
        return cls._instance

    def __init__(self, *args, **kwargs):
        pass

    def __call__(self, *args, **kwargs):
        return self

    def __repr__(self):
        return "Null()"

    def __nonzero__(self):
        return False

    def __getattr__(self, name):
        return self

    def __setattr__(self, name, value):
        return self

    def __delattr__(self, name):
        return self

"""
In the new object model, Python does not call __getattr__ on an instance for
any special methods needed to perform an operation on the instance
(rather, it looks up such methods in the instance class' slots). You may have
to take care and customize Null to your application's needs regarding
operations on null objects, and therefore special methods of the null objects'
class, either directly in the class' sources or by subclassing it
appropriately. For example, with this recipe's Null, you cannot index Null
instances, nor take their length, nor iterate on them. If this is a problem
for your purposes, you can add all the special methods you need (in Null itself
or in an appropriate subclass) and implement them appropriately.
"""


class SequentialNull(Null):
    def __len__(self):
        return 0

    def __iter__(self):
        return iter(())

    def __getitem__(self, i):
        return self

    def __delitem__(self, i):
        return self

    def __setitem__(self, i, v):
        return self


""" Summary:
The key goal of Null objects is to provide an intelligent replacement for the
often-used primitive value None in Python. (Other languages represent the lack
of a value using either null or a null pointer.) These nobody-lives-here
markers/placeholders are used for many purposes, including the important case
in which one member of a group of otherwise similar elements is special. This
usage usually results in conditional statements all over the place to
distinguish between ordinary elements and the primitive null (e.g., None)
value, but Null objects help you avoid that.

Among the advantages of using Null objects are the following:
- Superfluous conditional statements can be avoided by providing a first-class
object alternative for the primitive value None, thereby improving
code readability.
- Null objects can act as placeholders for objects whose behavior is not yet
implemented.
- Null objects can be used polymorphically with instances of just about any
other class (perhaps needing suitable subclassing for special methods, as
previously mentioned).
- Null objects are very predictable.

The one serious disadvantage of Null is that it can hide bugs. If a function
returns None, and the caller did not expect that return value, the caller most
likely will soon thereafter try to call a method or perform an operation that
None doesn't support, leading to a reasonably prompt exception and traceback.
If the return value that the caller didn't expect is a Null, the problem might
stay hidden for a longer time, and the exception and traceback, when they
eventually happen, may therefore be harder to reconnect to the location of the
defect in the code. Is this problem serious enough to make using Null
inadvisable? The answer is a matter of opinion. If your code has halfway decent
unit tests, this problem will not arise; while, if your code lacks decent unit
tests, then using Null is the least of your problems. But, as I said, it boils
down to a matter of opinions. I use Null very widely, and I'm extremely happy
with the effect it has had on my productivity.
"""


def compute(x, y):
    try:
        # lots of computation here to return some appropriate object
        return [x, y]
    except Exception:
        return None


def compute_with_nullobj(x, y):
    try:
        # lots of computation here to return some appropriate object
        return [x, y]
    except Exception:
        return Null()

if __name__ == "__main__":
    xs = [1, 2, 3]
    ys = [11, 22, 33]
    for x in xs:
        for y in ys:
            obj = compute(x, y)
            if obj is not None:
                obj.append(100)
            print obj
    print("============")

    # if return Null object when exception is thrown
    for x in xs:
        for y in ys:
            obj = compute_with_nullobj(x, y)
            obj.append(100)
            print obj
