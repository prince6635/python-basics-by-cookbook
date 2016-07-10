"""Implementing the State Design Pattern.

Problem: An object in your program can switch among several "states",
and the object's behavior must change along with the object's state.
Solution: The key idea of the State Design Pattern is to objectify the "state"
(with its several behaviors) into a class instance (with its several methods).
In Python, you don't have to build an abstract class to represent the interface
that is common to the various states: just write the classes for the
"state"s themselves.

With the State Design Pattern, you can "factor out" a number of related
behaviors of an object (and possibly some data connected with these behaviors)
into an auxiliary state object, to which the main object delegates these
behaviors as needed, through calls to methods of the "state" object. In Python
terms, this design pattern is related to the idioms of rebinding an object's
whole __class__, as shown in ring_buffer.py, and rebinding just certain
methods. This design pattern, in a sense, lies in between those
Python idioms: you group a set of related behaviors, rather than switching
either all behavior, by changing the object's whole __class__, or each method
on its own, without grouping. With relation to the classic design pattern
terminology, this recipe presents a pattern that falls somewhere between the
classic State Design Pattern and the classic Strategy Design Pattern.
"""


class TraceNormal(object):
    """state for normal level of verbosity."""
    def start_message(self):
        self.num_of_strs = self.num_of_chars = 0

    def emit_message(self, msg):
        self.num_of_strs += 1
        self.num_of_chars += len(msg)

    def end_message(self):
        print("normal: %d characters in %d strings." %
              (self.num_of_chars, self.num_of_strs))


class TraceChatty(object):
    """state for high level of verbosity."""
    def start_message(self):
        self.msgs = []

    def emit_message(self, msg):
        self.msgs.append(repr(msg))

    def end_message(self):
        print("chatty: messages - ", ",".join(self.msgs))


class TraceQuiet(object):
    """state for zero level of verbosity."""
    def start_message(self):
        pass

    def emit_message(self, msg):
        pass

    def end_message(self):
        pass


class Tracer(object):
    def __init__(self, state):
        self.state = state

    def set_state(self, state):
        self.state = state

    def emit_strings(self, strings):
        self.state.start_message()
        for str in strings:
            self.state.emit_message(str)
        self.state.end_message()


if __name__ == "__main__":
    t = Tracer(TraceNormal())
    t.emit_strings('some example strings are here'.split())
    t.set_state(TraceQuiet())
    t.emit_strings('some example strings are here'.split())
    t.set_state(TraceChatty())
    t.emit_strings('some example strings are here'.split())
