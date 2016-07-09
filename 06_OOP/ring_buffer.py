"""Implement a ring buffer.

define a buffer with a fixed size, so that, when it fills up,
adding another element overwrites the first (oldest) one.
This kind of data structure is particularly useful for storing
log and history information.
"""


class RingBuffer(object):
    """class that implements a not-yet-full buffer."""

    """The notable design choice in the implementation is that,
    since these objects undergo a nonreversible state transition at some point
    in their lifetimesfrom nonfull buffer to full buffer
    (and behavior changes at that point)I modeled that by
    changing self.__class__. This works just as well for classic classes
    as for new-style ones, as long as the old and new classes of the object
    have the same slots (e.g., it works fine for two new-style classes that
    have no slots at all, such as RingBuffer and _ _Full in this recipe).
    Note that, differently from other languages, the fact that class __Full is
    implemented inside class RingBuffer does not imply any special relationship
    between these classes; that's a good thing, too, because no such
    relationship is necessary.
    Changing the class of an instance may be strange in many languages,
    but it is an excellent Pythonic alternative to other ways of representing
    occasional, massive, irreversible, and discrete changes of state that
    vastly affect behavior, as in this recipe. Fortunately,
    Python supports it for all kinds of classes.
    """
    def __init__(self, max_size):
        self.max = max_size
        self.data = []

    class __Full(object):
        """class that implements a full buffer."""
        def append(self, x):
            """Append an element overwriting the oldest one."""
            self.data[self.cur] = x
            self.cur = (self.cur + 1) % self.max

        def get_data(self):
            """return list of elements in correct order."""
            return self.data[self.cur] + self.data[:self.cur]

    def append(self, x):
        """append an element at the end of the buffer."""
        self.data.append(x)
        if len(self.data) == self.max:
            self.cur = 0

            # Permanently change self's class from non-full to full
            self.__class__ = RingBuffer.__Full

    def get_data(self):
        """Return a list of elements from the oldest to the newest."""
        return self.data


class RingBufferAlternative(object):
    """docstring for RingBufferAlternative.

    Alternatively, we might switch just two methods,
    rather than the whole class, of a ring buffer instance that becomes full.
    """
    def __init__(self, max_size):
        self.max = max_size
        self.data = []

    def _full_append(self, x):
        self.data[self.cur] = x
        self.cur = (self.cur + 1) % self.max

    def _full_get_data(self):
        return self.data[self.cur:] + self.data[:self.cur]

    def append(self, x):
        self.data.append(x)
        if len(self.data) == self.max:
            self.cur = 0
            # Permanently change self's methods from non-full to full
            self.append = self._full_append
            self.get_data = self._full_get_data

    def get_data(self):
        return self.data


from collections import deque
class RingBufferByDeque(deque):
    """by double-ended queue."""
    def __init__(self, max_size):
        deque.__init__(self)
        self.max = max_size

    def append(self, x):
        deque.append(self, x)
        if len(self) > self.max:
            self.popleft()

    def get_data(self):
        return list(self)


class RingBufferDequeWithSwitch(deque):
    """docstring for RingBufferDequeWithSwitch"""
    def __init__(self, max_size):
        deque.__init__(self)
        self.max = max_size

    def _full_append(self, x):
        deque.append(self, x)
        self.popleft()

    def append(self, x):
        deque.append(self, x)
        if len(self) == self.max:
            self.append = self._full_append

    def get_data(self):
        return list(self)


if __name__ == "__main__":
    # rb = RingBuffer(5)
    # rb = RingBufferAlternative(5)
    # rb = RingBufferByDeque(5)
    rb = RingBufferDequeWithSwitch(5)
    rb.append(1)
    rb.append(2)
    rb.append(3)
    rb.append(4)
    print rb.__class__, rb.get_data()

    rb.append(5)
    print rb.__class__, rb.get_data()

    rb.append(6)
    print rb.__class__, rb.get_data()

    rb.append(7)
    rb.append(8)
    rb.append(9)
    rb.append(10)
    print rb.__class__, rb.get_data()
