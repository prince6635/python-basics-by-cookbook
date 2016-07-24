"""Flattening a Nested Sequence.

Problem: Some of the items in a sequence may in turn be sub-sequences,
and so on, to arbitrary depth of "nesting". You need to loop over a "flattened"
sequence, "expanding" each sub-sequence into a single, flat sequence of scalar
items. (A scalar, or atom, is anything that is not a sequencei.e., a leaf, if
you think of the nested sequence as a tree.)
"""


def list_or_tuple(x):
    return isinstance(x, (list, tuple))


def flatten(sequence, to_expand=list_or_tuple):
    for item in sequence:
        if to_expand(item):
            for sub_item in flatten(item, list_or_tuple):
                yield sub_item
        else:
            yield item


def non_string_iterable(obj):
    try:
        iter(obj)
    except TypeError:
        return False
    else:
        # identify whether an object is string-like
        return not isinstance(obj, basestring)


def flatten_iteratively(sequence, to_expand=non_string_iterable):
    """The main technique for recursion removal is to keep an explicit last-in,
    first-out (LIFO) stack, which, in this case, we can implement with
    a list of iterators"""
    # iter: return an iterator object
    # make the original sequence to be an iterator object and put into the list
    iterators = [iter(sequence)]
    while iterators:
        print(iterators[-1])
        for item in iterators[-1]:
            if to_expand(item):
                iterators.append(iter(item))
                break
            else:
                yield item
        else:
            # means the current iterator object is fully analyzed
            iterators.pop()


def get_flattened_sequence(x):
    result = []
    # for item in flatten(x):
    # for item in flatten(x, non_string_iterable):
    for item in flatten_iteratively(x):
        result.append(item)
    return result


if __name__ == "__main__":
    x = [1, 2, [3, [], 4, [5, 6], 7, [8, ], ], 9]
    x = [1, 2, [3, [], "abc", [5, 6], 7, [8, ], ], 9]
    x = [1]
    result = get_flattened_sequence(x)
    print result
