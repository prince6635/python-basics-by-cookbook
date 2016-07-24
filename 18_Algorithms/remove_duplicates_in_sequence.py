"""Removing Duplicates from a Sequence.

Problem: You have a sequence that may include duplicates, and you want to
remove the duplicates in the fastest possible way, without knowing much about
the properties of the items in the sequence. You do not care about the order
of items in the resulting sequence.
"""

from sets import Set as set


def remove_duplicates(seq):
    """Return a list of the elements in arbitary order without duplicates.

    it tries three methods, from fastest to slowest, letting runtime exceptions
    pick the best method for the sequence at hand.
    """
    # method 1: all sequence elements must be hashable. - O(n)
    try:
        # Set(x) will sort x and remove the duplicates
        return list(set(seq))
    except TypeError:
        pass  # Move on to the next method

    # method 2: when the elements enjoy a total ordering - O(n*log(n))
    # Since you can't hash all elements (e.g., using them as dictionary keys,
    # or, as in this case, set elements), try sorting, to bring equal items
    # together and then weed them out in a single pass
    ls = list(seq)
    try:
        ls.sort()
    except TypeError:
        del ls  # Move on to the next method
    else:
        # the sort worked, so we're fine -- do the weeding
        return [x for i, x in enumerate(ls) if not i or x != ls[i-1]]

    # method 3: O(n^2)
    # If sorting also turns out to be impossible, the sequence items must
    # at least support equality testing
    res = []
    for x in seq:
        if x not in res:
            res.append(x)
    return res


def remove_duplicates_inplace(seq, hash_func=None):
    # this method only works if the items are hashable
    # if seq=[[1, 2], [2, 3]], it raises: TypeError: unhashable type: 'list'
    if hash_func is None:
        def hash_func(x):
            return x

    visited = set()
    result = []
    for item in seq:
        hash_code = hash_func(item)
        if hash_code not in visited:
            visited.add(hash_code)
            result.append(item)
    return result


def remove_duplicates_inplace_last(seq, hash_func=None):
    # always pick the last element among all duplicate ones
    # use case:
    #   somelines = remove_duplicates_inplace_last(open('my.txt'), str.lower)
    seq = list(seq)
    seq.reverse()
    result = remove_duplicates_inplace(seq, hash_func)
    result.reverse()
    return result


def remove_duplicates_inplace_non_hashable_items(seq, hash_func=None):
    """"For nonhashable items, the simplest fallback approach is to use a
    set-like container that supports the add method and membership testing
    without requiring items to be hashable. Unfortunately, performance will
    be much worse than with a real set. """
    if hash_func is None:
        def hash_func(x):
            return x

    visited = set()
    result = []
    for item in seq:
        hash_code = hash_func(item)
        try:
            is_visited = hash_code not in visited
        except TypeError:
            class FakeSet(list):
                add = list.append
            visited = FakeSet(visited)
            is_visited = hash_code not in visited

        if is_visited:
            visited.add(hash_code)
            result.append(item)

    return result


def remove_duplicates_inplace_non_hashable_items_fancy(seq,
                                                       hash_func,
                                                       pick_func):
    """Keeps "best" item of each hash_func defined equivalence class,
    with picking function p doing pairwise choice of (index, item)."""
    representative = {}
    for idx, item in enumerate(seq):
        hash_code = hash_func(item)
        if hash_code in representative:
            # It's NOT a problem to rebind index and item within the
            # for loop: the next leg of the loop does not use their binding
            idx, item = pick_func((idx, item), representative[hash_code])
        representative[hash_code] = idx, item
    # reconstruct sequence order by sorting on indices
    aux_list = representative.values()
    aux_list.sort()
    return [item for idx, item in aux_list]


def test_remove_duplicates_inplace_non_hashable_items_fancy(words):
    # work for: ["a", "1", "b", "a", "b"]
    # won't work for: ["abc", "ab", "abc", "123"]
    def first_letter(word):
        return word[0].lower()

    def prefer((idx1, word1), (idx2, word2)):
        if len(word2) > len(word1):
            return idx2, word2
        return idx1, word1

    def prefer_fancier(word1, word2=None):
        return word2 is None or len(word1) > len(word2)

    return remove_duplicates_inplace_non_hashable_items_fancy(
        words, first_letter, prefer)


if __name__ == "__main__":
    seq1 = [4, 4, 1, 2, 3, 1, 2, 3]
    print(remove_duplicates(seq1))
    print(remove_duplicates_inplace(seq1))
    print(remove_duplicates_inplace_last(seq1))
    print(remove_duplicates_inplace_non_hashable_items(seq1))
    seq2 = 'abcabc'
    print(remove_duplicates(seq2))
    print(remove_duplicates_inplace(seq2))
    print(remove_duplicates_inplace_last(seq2))
    print(remove_duplicates_inplace_non_hashable_items(seq2))
    seq3 = [[3, 4], [1, 2], [2, 3], [1, 2]]
    print(remove_duplicates(seq3))
    # print(remove_duplicates_inplace(seq3))
    # print(remove_duplicates_inplace_last(seq3))
    print(remove_duplicates_inplace_non_hashable_items(seq3))

    lol = [[1, 2], [], [1, 2], [3], [], [3, 4], [1, 2], [], [2, 1]]
    # d1==d2 and yet repr(d1)!=repr(d2), repr class __repr__
    print(remove_duplicates_inplace_non_hashable_items(lol, repr))

    words = ["a", "1", "b", "a", "b"]
    print(test_remove_duplicates_inplace_non_hashable_items_fancy(words))
