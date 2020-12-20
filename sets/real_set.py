import abc


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
