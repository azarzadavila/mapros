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
