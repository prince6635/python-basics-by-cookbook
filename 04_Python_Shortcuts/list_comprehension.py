"""Constructing Lists with List Comprehensions.

Construct a new list by operating on elements of an existing sequence
(or other kind of iterable).
Elegance, clarity, and pragmatism, are Python's core values.
List comprehensions show how pragmatism can enhance both clarity and elegance.

!!! Cases not to use list comprehensions:
1, when you simply want to perform a loop
2, when another built-in does what you want even more directly and immediately.
    For example, to copy a list, use L1 = list(L), not:
        L1 = [x for x in L]
3, when the operation you want to perform on each item is to call a function on
    the item and use the function's result, use L1 = map(f, L) rather than
        L1 = [f(x) for x in L].

But in most cases, a list comprehension is just right.

In Python 2.4, you should consider using a generator expression,
rather than a list comprehension, when the sequence may be long and you only
need one item at a time.
"""


def list_comprehension():
    old_list = [1, 2, 3, 4, 5, 6, 7, 8]
    print old_list

    # create a new list by adding 23 to each item of some other list.
    new_list1 = [x + 23 for x in old_list]
    print new_list1

    # create the new list to comprise all items in the other list that are
    # larger than 5
    new_list2 = [x for x in old_list if x > 5]
    print new_list2

    # combine both ideas of new_list1 and new_list2
    new_list3 = [x + 23 for x in old_list if x > 5]
    print new_list3

    # if your task is to set all items greater than 100 to 100,
    # in an existing list object L, the best solution is:
    L = [98, 99, 100, 101, 102]
    L[:] = [min(x, 100) for x in L]
    # !!! Assigning to the "whole-list slice" L[:] alters the existing list
    # object in place, rather than just rebinding the name L, as would be the
    # case if you coded L = . . . instead.
    print L


def generator_expression():
    """
    The syntax of generator expressions is just the same as
    for list comprehensions, except that generator expressions are surrounded
    by parentheses, ( and ), not brackets, [ and ]. For example, say that we
    only need the summation of the list computed in this recipe's Solution,
    not each item of the list. In Python 2.3, we would code:
        total = sum([x + 23 for x in theoldlist if x > 5])
    In Python 2.4, we can code more naturally, omitting the brackets (no need
    to add additional parenthesesthe parentheses already needed to call the
    built-in sum suffice):
        total = sum(x + 23 for x in theoldlist if x > 5)
    Besides being a little bit cleaner, this method avoids materializing the
    list as a whole in memory and thus may be slightly faster when the list
    is extremely long.
    """
    theoldlist = [1, 2, 3, 4, 5, 6, 7, 8]
    total = sum(x + 23 for x in theoldlist if x > 5)
    print total


if __name__ == "__main__":
    list_comprehension()
    generator_expression()
