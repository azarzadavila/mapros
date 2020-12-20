from enum import Enum, auto


class Order(Enum):
    LT = auto()
    LE = auto()
    EQ = auto()
    GT = auto()
    GE = auto()
