from enum import Enum, auto


class Sentence:
    def __init__(self, *data):
        self.data = data
        if not check_sentence(self):
            raise ValueError("This is not a correct sentence.")

    def __str__(self):
        s = "("
        for i in range(len(self.data) - 1):
            s += str(self.data[i])
            s += " "
        s += str(self.data[-1])
        s += ")"
        return s


class IDSentence:
    def __init__(self, id):
        if id is None:
            raise ValueError("The id of an IDSentence may not be None.")
        self.id = id

    def __str__(self):
        return str(self.id)


def str_with_arity(arity_obj, args):
    s = str(arity_obj)
    s += "("
    for i in range(len(args) - 1):
        s += str(args[i])
        s += ", "
    s += str(args[-1])
    s += ")"
    return s


class AtomicSentence:
    def __init__(self, data):
        self.data = data
        if not check_atomic_sentence(self):
            raise ValueError("This is not a correct atomic sentence.")

    def __str__(self):
        if len(self.data) == 1:
            return str(self.data[0])
        return str_with_arity(self.data[0], self.data[1])


class Term:
    def __init__(self, *data):
        self.data = data
        if not check_term(self):
            raise ValueError("This is not a correct term.")

    def __str__(self):
        if len(self.data) == 1:
            return str(self.data[0])
        return str_with_arity(self.data[0], self.data[1])


class Predicate:
    def __init__(self, arity, name=None):
        self.arity = arity
        self.name = name
        if not isinstance(arity, int) or arity < 0:
            raise ValueError("The arity of a predicate can not be negative.")

    def __str__(self):
        return self.name


class LogicFunction:
    def __init__(self, arity, name=None):
        self.arity = arity
        self.name = name
        if not isinstance(arity, int) or arity < 0:
            raise ValueError("The arity of a function can not be negative.")

    def __str__(self):
        return self.name


NEGATION = 0


class Quantifier(Enum):
    UNIVERSAL = auto()
    EXISTENTIAL = auto()

    def __str__(self):
        smap = {self.UNIVERSAL: "for all", self.EXISTENTIAL: "exists"}
        return smap[self.value]


class BinaryConnector(Enum):
    CONJUCTION = auto()
    DISJUNCTION = auto()
    IMPLICATION = auto()
    BICONDITIONAL = auto()

    def __str__(self):
        smap = {
            self.CONJUCTION: "AND",
            self.DISJUNCTION: "OR",
            self.IMPLICATION: "=>",
            self.BICONDITIONAL: "<=>",
        }
        return smap[self.value]


class Constant:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class Variable:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


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
    if isinstance(x, IDSentence):
        return True
    if not isinstance(x, Sentence):
        return False
    if len(x.data) == 1:
        return check_atomic_sentence(x) or isinstance(x.data[0], IDSentence)
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
