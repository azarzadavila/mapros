import abc
from sets.real_interval import RealInterval


class Command(metaclass=abc.ABCMeta):
    def __init__(self, receiver):
        self._receiver = receiver

    @abc.abstractmethod
    def execute(self):
        pass


class NewVariableCommand(Command):
    def __init__(self, receiver, symbol):
        super().__init__(receiver)
        self.symbol = symbol

    def execute(self):
        self._receiver.add(self.symbol)


class NewIntervalCommand(Command):
    def __init__(self, receiver, start, end, include_start, include_end, symbol):
        super().__init__(receiver)
        self.interval = RealInterval(start, end, include_start, include_end, symbol)

    def execute(self):
        self._receiver.add_interval(self.interval)


class OrderCommand(Command):
    def __init__(self, receiver, order, var1, var2):
        super().__init__(receiver)
        self.order = order
        self.var1 = var1
        self.var2 = var2

    def execute(self):
        self._receiver.add_order(self.order, self.var1, self.var2)


class Question(metaclass=abc.ABCMeta):
    def __init__(self, receiver):
        self._receiver = receiver

    @abc.abstractmethod
    def execute(self):
        pass


class IntersectionQuestion(Question):
    def __init__(self, receiver, var1, var2):
        super().__init__(receiver)
        self.var1 = var1
        self.var2 = var2

    def execute(self):
        return self._receiver.compute_intersection(self.var1, self.var2)
