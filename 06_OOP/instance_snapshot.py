"""Checking an Instance for Any State Changes.

Problem: You need to check whether any changes to an instance's state have
occurred to selectively save instances that have been modified since the last
"save" operation.
Solution: An effective solution is a mixin classa class you can multiply
inherit from and that is able to take snapshots of an instance's state and
compare the instance's current state with the last snapshot to determine
whether or not the instance has been modified
"""
import copy


class ChangeCheckerMixin(object):
    container_items = {dict: dict.iteritems, list: enumerate}
    """ As container types, ChangeCheckerMixin, as presented,
    considers only list and dict. If you also use other types as containers,
    you just need to add them appropriately to the containerItems dictionary.
    That dictionary must map each container type to a function callable on
    an instance of that type to get an iterator on indices and values
    (with indices usable to index the container). Container type instances must
    also support being shallowly copied with standard library Python function
    copy.copy. For example, to add Python 2.4's collections.deque as a
    container to a subclass of ChangeCheckerMixin, you can code:

        import collections
        class CCM_with_deque(ChangeCheckerMixin):
            containerItems = dict(ChangeCheckerMixin.containerItems)
            containerItems[collections.deque] = enumerate

    since collections.deque can be "walked over" with enumerate,
    just like list can.
    """
    immutable = False

    def snapshot(self):
        ''' create a "snapshot" of self's state --
        like a shallow copy, but recursing over container types
        (not over general instances: instances must keep track of their
        own changes if needed). '''
        if self.immutable:
            return
        else:
            self._snapshot = self._copy_container(self.__dict__)

    def make_immutable(self):
        ''' if set .immutable to be True, the instance state can't change
        any more '''
        self.immutable = True
        try:
            del self._snapshot
        except AttributeError:
            pass

    def _copy_container(self, container):
        ''' semi-shallow copy, recursing on container types only '''
        new_container = copy.copy(container)
        # if new_container is dict or list, then iterate each item.
        for k, v in self.container_items[type(new_container)](new_container):
            if type(v) in self.container_items:
                new_container[k] = self._copy_container(v)
            elif hasattr(v, 'snapshot'):
                # if the item has snapshot method, just take a snapshot.
                v.snapshot()
        return new_container

    def is_changed(self):
        ''' True if self's state is changed since the last snapshot '''
        if self.immutable:
            return False
        # remove snapshot from self.__dict__, put it back at the end
        snap = self.__dict__.pop('_snapshot', None)
        if snap is None:
            return True

        try:
            return self._check_container(self.__dict__, snap)
        finally:
            self._snapshot = snap

    def _check_container(self, container, snapshot):
        ''' return True if the container and its snapshot differ '''
        if len(container) != len(snapshot):
            return True

        for k, v in self.container_items[type(container)](container):
            try:
                snap_v = snapshot[k]
            except LookupError:
                return True

            if self._check_item(v, snap_v):
                return True
        return False

    def _check_item(self, new_item, old_item):
        ''' compare new_item and old_item. If they are containers,
        call self._check_container recursively. If they're an instance with an
        'is_changed' method, delegate to that method. Otherwise, return True if
        the items differ. '''
        if type(new_item) != type(old_item):
            return True
        if type(new_item) in self.container_items:
            return self._check_container(new_item, old_item)
        if new_item is old_item:
            method_is_changed = getattr(new_item, "is_changed", None)
            if method_is_changed is None:
                return False
            return method_is_changed()
        return new_item != old_item


if __name__ == "__main__":
    class Example(ChangeCheckerMixin):
        # http://stackoverflow.com/questions/36901/what-does-double-star-and-star-do-for-python-parameters
        # for * and ** arguments
        def __init__(self, *args, **kwargs):
            self.L = list(*args, **kwargs)

        def __str__(self):
            return 'Example(%s)' % str(self.L)

        def __getattr__(self, a):
            return getattr(self.L, a)

    ex = Example('test')
    print 'ex=', ex, 'is_changed=', ex.is_changed()
    # now, assume ex gets saved, then...:
    ex.snapshot()
    print 'ex=', ex, 'is_changed=', ex.is_changed()
    # now we change ex...:
    ex.append('x')
    print 'ex=', ex, 'is_changed=', ex.is_changed()
