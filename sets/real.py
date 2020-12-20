from sets.utils import Order


class Real:
    def __init__(self, symbol=None):
        self.lt = set()
        self.le = set()
        self.eq = set()
        self.gt = set()
        self.ge = set()
        self.symbol = symbol

    def __str__(self):
        return self.symbol

    def __repr__(self):
        return "Real(symbol={})".format(self.symbol)

    def __eq__(self, other):
        return other.symbol == self.symbol

    def __hash__(self):
        return hash(self.symbol)


def apply_order(order, v1, v2):
    if order == Order.LT:
        v1.lt.add(v2)
        v2.gt.add(v1)
    elif order == Order.LE:
        v1.le.add(v2)
        v2.ge.add(v1)
    elif order == Order.EQ:
        v1.eq.add(v2)
        v2.eq.add(v1)
    elif order == Order.GT:
        v1.gt.add(v1)
        v2.lt.add(v2)
    elif order == Order.GE:
        v1.ge.add(v2)
        v2.le.add(v1)
    else:
        raise ValueError("Unknown order : {}".format(order))
