"""List related."""
from __future__ import print_function


def list_get(L, i, default_value=None):
    """Returning an Element of a List If It Exists.

    Problem
    You have a list L and an index i, and you want to get L[i] when i is a
    valid index into L; otherwise, you want to get a default value v. If L were
    a dictionary, you'd use L.get(i, v), but lists don't have a get method.
    """
    # valid indices are negative ones down to -len(L) inclusive,
    # and non-negative ones up to len(L) exclusive
    if -len(L) <= i < len(L):
        return L[i]
    else:
        return default_value


def list_get_for_more_correct_cases(L, i, default_value=None):
    """ If almost all calls to list_get pass a valid index value for i,
    you might prefer an alternative approach.
    However, unless a vast majority of the calls pass a valid index,
    this alternative (as some time measurements show) can be up to four times
    slower than the list_get function shown in the solution. Therefore,
    this "easier to get forgiveness than permission" (EGFP) approach,
    although it is often preferable in Python, cannot be recommended for
    this specific case.

    EGFP: basically it's using try/catch instead of checking it's None or not.
    http://stackoverflow.com/questions/12265451/ask-forgiveness-not-permission-explain
    """
    try:
        return L[i]
    except IndexError:
        return default_value


def loop_with_indexes(L):
    """Looping over Items and Their Indices in a Sequence.

    Problem: You need to loop on a sequence, but at each step you also need to
    know which index into the sequence you have reached (e.g., because you need
    to rebind some entries in the sequence), and Python's preferred approach to
    looping doesn't use the indices.

    Looping directly is cleaner, more readable, faster, and more general
    (since you can loop on any iterable, by definition, while indexing works
    only on sequences, such as lists).
        for item in sequence:
            process(item)
    function enumerate, which takes any iterable argument and returns an
    iterator yielding all the pairs (two-item tuples) of the for (index, it
    em), one pair at a time. By writing your for loop's header clause in the
    form:
        for index, item in enumerate(sequence):
    both the index and the item are available within the loop's body. For help
    remembering the order of the items in each pair enumerate yields, think of
    the idiom d=dict(enumerate(L)). This gives a dictionary d that's
    equivalent to list L, in the sense that d[i] is L[i] for any valid
    non-negative index i.
    """
    # 1, loop over indices and accessing items by indexing
    for idx in range(len(L)):
        if L[idx] >= 6:
            L[idx] = 'new'

    # 2, use built-in function enumerate - cleaner, more readable, and faster.
    for idx, item in enumerate(L):
        if item < 3:
            L[idx] = 'new_again'


def create_list_without_sharing_reference():
    """Creating Lists of Lists Without Sharing References.

    Problem: You want to create a multidimensional list but want to avoid
    implicit reference sharing.
    Solution: To build a list and avoid implicit reference sharing, use a list
    comprehension. For example, to build a 5 x 10 array of zeros:
        multilist = [[0 for col in range(5)] for row in range(10)]
    """
    alist = [0] * 5
    print('a list:%s' % alist)
    # create with sharing References.
    multi = [[0] * 5] * 3
    # [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
    print(multi)
    # Multiplying a sequence by a number creates a new sequence with the
    # specified number of new references to the original contents.
    # [['oops!', 0, 0, 0, 0], ['oops!', 0, 0, 0, 0], ['oops!', 0, 0, 0, 0]]
    multi[0][0] = 'oops!'
    print(multi)

    # create without sharing References.
    multilist = [[0 for col in range(5)] for row in range(3)]
    print(multilist)
    multilist[0][0] = 'changed'
    # [['changed', 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
    print(multilist)


if __name__ == "__main__":
    L = [1, 2, 3, 4, 5, 6, 7, 8]
    for i in range(15):
        # print L[i]
        print("(%s, %s)" %
              (list_get(L, i), list_get_for_more_correct_cases(L, i)),
              end=" ")
    print("")

    loop_with_indexes(L)
    print(L)

    create_list_without_sharing_reference()
