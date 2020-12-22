class RealInterval:
    def __init__(self, start, end, include_start=True, include_end=True, symbol=None):
        self.start = start
        self.end = end
        self.include_start = include_start
        self.include_end = include_end
        self.symbol = symbol

    def __str__(self):
        left = "[" if self.include_start else "]"
        right = "]" if self.include_end else "["
        return left + str(self.start) + "," + str(self.end) + right

    def __repr__(self):
        return "RealInterval({})".format(str(self))

    def __eq__(self, other):
        return self.symbol == other.symbol

    def __hash__(self):
        return hash(self.symbol)


def intersection(inter1, inter2):
    pass
