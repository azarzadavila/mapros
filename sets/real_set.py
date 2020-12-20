import abc
from sets.real import Real, apply_order


class RealSetInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def add(self, var):
        pass

    @abc.abstractmethod
    def add_interval(self, interval):
        pass

    @abc.abstractmethod
    def add_order(self, order, var1, var2):
        pass


class RealSet(RealSetInterface):
    def __init__(self):
        self.variables = []
        self.intervals = []

    def add(self, var):
        self.variables.append(Real(symbol=var))

    def add_interval(self, interval):
        self.intervals.append(interval)

    def get_var(self, var):
        for v in self.variables:
            if v.symbol == var:
                return v

    def add_order(self, order, var1, var2):
        v1 = self.get_var(var1)
        v2 = self.get_var(var2)
        apply_order(order, v1, v2)
