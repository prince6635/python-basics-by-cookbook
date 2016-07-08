"""Delegating automatically as an Alternative to inheritance.

inherit from a class or type, but you need some tweak that inheritance
does not provide. For example, you want to selectively hide some of
the base class' methods (not special methods, see delegate_special_methods.py),
which inheritance doesn't allow.
"""


class Location(object):
    """docstring for Location"""
    def __init__(self, price):
        self.price = price

    def get_price(self):
        return self.price


class Event(object):
    """docstring for Event"""
    def __init__(self, discount):
        self.discount = discount

    def get_discount(self):
        return self.discount


class Pricing(object):
    """docstring for Princing"""
    def __init__(self, location, event):
        self.location = location
        self.event = event

    def set_location(self, location):
        self.location = location

    def get_price(self):
        return self.location.get_price()

    def get_discount(self):
        return self.event.get_discount()


class AutoDelegator(object):
    """docstring for AutoDelegator"""
    delegates = ()
    do_not_delegates = ()

    def __getattr__(self, key):
        if key not in self.do_not_delegates:
            for delegate in self.delegates:
                try:
                    return getattr(delegate, key)
                except AttributeError:
                    pass
        raise AttributeError(key)


class AutoDelegatePricing(AutoDelegator):
    """docstring for AutoDelegatePricing"""
    def __init__(self, location, event):
        self.delegates = [location, event]

    def set_location(self, location):
        self.delegates[0] = location

    def set_event(self, event):
        self.delegates[1] = event


class AutoDelegatePricingWithLimitedFunctions(AutoDelegatePricing):
    """docstring for AutoDelegatePricingWithLimitedFunctions"""

    do_not_delegates = ('get_discount',)

    def __init__(self, location, event):
        super(AutoDelegatePricingWithLimitedFunctions, self).__init__(
            location, event)


if __name__ == "__main__":
    location = Location(1.23)
    event = Event(0.75)
    price = Pricing(location, event)
    print price.get_price()
    print price.get_discount()

    auto_delegate_price = AutoDelegatePricing(location, event)
    print auto_delegate_price.get_price()
    print auto_delegate_price.get_discount()

    auto_delegate_price_with_limited = AutoDelegatePricingWithLimitedFunctions(
        location, event)
    print auto_delegate_price_with_limited.get_price()
    # raise AttributeError
    print auto_delegate_price_with_limited.get_discount()
