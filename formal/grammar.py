from enum import Enum, auto


class Sentence:
    def __init__(self, data):
        self.data = data


class AtomicSentence:
    def __init__(self, data):
        self.data = data


class Term:
    def __init__(self, data):
        self.data = data


class Predicate:
    def __init__(self, arity):
        self.arity = arity


class LogicFunction:
    def __init__(self, arity):
        self.arity = arity


NEGATION = 0


class Quantifier(Enum):
    UNIVERSAL = auto()
    EXISTENTIAL = auto()


class BinaryConnector(Enum):
    CONJUCTION = auto()
    DISJUNCTION = auto()
    IMPLICATION = auto()
    BICONDITIONAL = auto()


class Constant:
    def __init__(self, cst):
        self.cst = cst


class Variable:
    def __init__(self, var):
        self.var = var


def check_binary_connector(x):
    return isinstance(x, BinaryConnector)


def check_terms(arity, args):
    if len(args) != arity:
        return False
    for x in args:
        if not check_term(x):
            return False
    return True


def check_term(x):
    if not isinstance(x, Term):
        return False
    if len(x.data) == 1:
        return isinstance(x.data[0], Constant) or isinstance(x.data[0], Variable)
    if len(x.data) == 2:
        fct = x.data[0]
        if not isinstance(fct, LogicFunction):
            return False
        args = x.data[1]
        return check_terms(fct.arity, args)
    return False


def check_atomic_sentence(x):
    if not isinstance(x, AtomicSentence):
        return False
    if len(x.data) == 1:
        return isinstance(x.data[0], bool)
    if len(x.data) == 2:
        pred = x.data[0]
        if not isinstance(pred, Predicate):
            return False
        args = x.data[1]
        return check_terms(pred.arity, args)
    return False


def check_sentence(x):
    if not isinstance(x, Sentence):
        return False
    if len(x.data) == 1:
        return check_atomic_sentence(x)
    if len(x.data) == 2:
        return x.data[0] == NEGATION and check_sentence(x.data[1])
    if len(x.data) == 3:
        if isinstance(x.data[0], Quantifier):
            return isinstance(x.data[1], Variable) and check_sentence(x.data[2])
        return (
            check_sentence(x.data[0])
            and isinstance(x.data[1], BinaryConnector)
            and check_sentence(x.data[2])
        )
    return False
