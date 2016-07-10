"""Checking Whether an Object Has Necessary Attributes.

You need to check whether an object has certain necessary attributes before
performing state-altering operations. However, you want to avoid type-testing
because you know it interferes with polymorphism.
"""


def munge1(alist):
    """
    If alist is missing any of the methods you're calling
    (explicitly, such as append and extend; or implicitly, such as the calls to
    __getitem__ and __setitem__ implied by the assignment statement
    alist[4] = alist[3]), the attempt to access and call a missing method
    raises an exception. Function munge1 makes no attempt to catch the
    exception, so the execution of munge1 terminates, and the exception
    propagates to the caller of munge1. The caller may choose to catch the
    exception and deal with it, or terminate execution and let the exception
    propagate further back along the chain of calls, as appropriate.

    This approach is usually just fine, but problems may occasionally occur.
    Suppose, for example, that the alist object has an append method but not an
    extend method. In this peculiar case, the munge1 function partially alters
    alist before an exception is raised. Such partial alterations are generally
    not cleanly undoable; depending on your application, they can sometimes be
    a bother.
    """
    alist.append(23)
    alist.extend(range(5))
    alist.append(42)
    alist[4] = alist[3]
    alist.extend(range(2))


def munge2(alist):
    """
    To forestall the "partial alterations" problem, the first approach that
    comes to mind is to check the type of alist. Such a naive
    "Look Before You Leap" (LBYL) approach may look safer than doing no checks
    at all, but LBYL has a serious defect: it loses polymorphism!
    The worst approach of all is checking for equality of types:
    """
    # a very bad idea
    if type(alist) is list:
        munge1(alist)
    else:
        raise TypeError("expected list, got %s" % type(alist))


def munge3(alist):
    """
    This even fails, without any good reason, when alist is an instance of a
    subclass of list. You can at least remove that huge defect by using
    isinstance instead:
    """
    if isinstance(alist, list):
        munge1(alist)
    else:
        raise TypeError("expected list, got %s" % type(alist))


def munge4(alist):
    """
    However, munge3 still fails, needlessly, when alist is an instance of a
    type or class that mimics list but doesn't inherit from it. In other words,
    such type-checking sacrifices one of Python's great strengths:
    signature-based polymorphism. For example, you cannot pass to munge3
    an instance of Python 2.4's collections.deque, which is a real pity because
    such a deque does supply all needed functionality and indeed can be passed
    to the original munge1 and work just fine. Probably a zillion sequence
    types are out there that, like deque, are quite acceptable to munge1 but
    not to munge3. Type-checking, even with isinstance, exacts an
    enormous price.

    A far better solution is accurate LBYL, which is both safe and
    fully polymorphic:
    """
    # Extract all bound methods you need (get immediate exception,
    # without partial alteration, if any needed method is missing):
    append = alist.append
    extend = alist.extend
    # Check operations, such as indexing, to get an exception ASAP
    # if signature compatibility is missing:
    try:
        alist[0] = alist[0]
    except IndexError:
        # An empty alist is okay
        pass
    # Operate: no exceptions are expected from this point onwards append(23)
    extend(range(5))
    append(42)
    alist[4] = alist[3]
    extend(range(2))


""" Summary:
The normal Pythonic way of life can be described as the Easier to Ask
Forgiveness than Permission (EAFP) approach: just try to perform whatever
operations you need, and either handle or propagate any exceptions that may
result. It usually works great. The only real problem that occasionally arises
is "partial alteration": when you need to perform several operations on an
object, just trying to do them all in natural order could result in some of
them succeeding, and partially altering the object,
before an exception is raised.

Accurate LBYL generally offers a good trade-off in comparison to EAFP,
assuming we need safeguards against partial alterations. The extra complication
is modest, and the slowdown due to the checks is typically compensated by the
extra speed gained by using bound methods through local names rather than
explicit attribute access (at least if the operations include loops, which
is often the case). It's important to avoid overdoing the checks, and the
assert statement can help with that. For example, you can add such checks as
assert callable(append) to munge4. In this case, the compiler removes the
assert entirely when you run the program with optimization (i.e., with
flags -O or -OO passed to the python command), while performing the checks when
the program is run for testing and debugging
(i.e., without the optimization flags).
"""
