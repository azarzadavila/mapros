class Real:
    def __init__(self, symbol=None):
        self.equals = []
        self.lower = []
        self.greater = []
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
    pass
