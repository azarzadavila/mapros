import abc


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
