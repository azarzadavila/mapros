class RealInterval:
    def __init__(self, start, end, include_start=True, include_end=True):
        self.start = start
        self.end = end
        self.include_start = include_start
        self.include_end = include_end

    def intersection(self, interval):
        if self.start in interval.start.greater and self.end in interval.end.greater:
            return RealInterval(start=self.start, end=interval.end)

    def __str__(self):
        left = "[" if self.include_start else "]"
        right = "]" if self.include_end else "["
        return left + str(self.start) + "," + str(self.end) + right

    def __repr__(self):
        return "RealInterval({})".format(str(self))
