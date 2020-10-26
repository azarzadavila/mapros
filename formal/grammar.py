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

    def substitute(self, var, new_var):
        if len(self.data) == 2:
            return Sentence(NEGATION, self.data[1].substitute(var, new_var))
        if len(self.data) == 3:
            if isinstance(self.data[1], BinaryConnector):
                return Sentence(
                    self.data[0].substitute(var, new_var),
                    self.data[1],
                    self.data[2].substitute(var, new_var),
                )
            elif self.data[1] == var:
                return self
            else:
                return Sentence(
                    self.data[0], self.data[1], self.data[2].substitute(var, new_var)
                )

    def __eq__(self, other):
        return self.data == other.data


class IDSentence:
    def __init__(self, id):
        if id is None:
            raise ValueError("The id of an IDSentence may not be None.")
        self.id = id

    def __str__(self):
        return str(self.id)

    def __eq__(self, other):
        return other.id == self.id

    def substitute(self, var, new_var):
        # TODO
        pass


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

    def __eq__(self, other):
        return self.data == other.data

    def __str__(self):
        if len(self.data) == 1:
            return str(self.data[0])
        return str_with_arity(self.data[0], self.data[1])

    def substitute(self, var, new_var):
        return AtomicSentence(
            (self.data[0], tuple(x.substitute(var, new_var) for x in self.data[1]))
        )


class Term:
    def __init__(self, *data):
        self.data = data
        if not check_term(self):
            raise ValueError("This is not a correct term.")

    def __eq__(self, other):
        return self.data == other.data

    def __str__(self):
        if len(self.data) == 1:
            return str(self.data[0])
        return str_with_arity(self.data[0], self.data[1])

    def substitute(self, var, new_var):
        return Term(
            self.data[0], tuple(x.substitute(var, new_var) for x in self.data[1])
        )


class Predicate:
    def __init__(self, arity, name=None):
        self.arity = arity
        self.name = name
        if not isinstance(arity, int) or arity < 0:
            raise ValueError("The arity of a predicate can not be negative.")

    def __eq__(self, other):
        return self.arity == other.arity and self.name == other.name

    def __str__(self):
        return self.name


class LogicFunction:
    def __init__(self, arity, name=None):
        self.arity = arity
        self.name = name
        if not isinstance(arity, int) or arity < 0:
            raise ValueError("The arity of a function can not be negative.")

    def __eq__(self, other):
        return self.arity == other.arity and self.name == other.name

    def __str__(self):
        return self.name


class __Negation(Enum):
    NEGATION = auto()

    def __str__(self):
        return "NOT"


NEGATION = __Negation.NEGATION


class Quantifier(Enum):
    UNIVERSAL = auto()
    EXISTENTIAL = auto()

    def __str__(self):
        smap = {self.UNIVERSAL: "FORALL", self.EXISTENTIAL: "EXISTS"}
        return smap[self]


class BinaryConnector(Enum):
    CONJUNCTION = auto()
    DISJUNCTION = auto()
    IMPLICATION = auto()
    BICONDITIONAL = auto()

    def __str__(self):
        smap = {
            self.CONJUNCTION: "AND",
            self.DISJUNCTION: "OR",
            self.IMPLICATION: "=>",
            self.BICONDITIONAL: "<=>",
        }
        return smap[self]


class Constant:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name

    def substitute(self, var, new_var):
        return self


class PredicateConstant:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name


class Variable:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name

    def substitute(self, var, new_var):
        if self == var:
            return new_var
        else:
            return self


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
    if isinstance(x, Constant):
        return True
    if isinstance(x, Variable):
        return True
    if not isinstance(x, Term):
        return False
    if len(x.data) == 2:
        fct = x.data[0]
        if not isinstance(fct, LogicFunction):
            return False
        args = x.data[1]
        return check_terms(fct.arity, args)
    return False


def check_atomic_sentence(x):
    if isinstance(x, bool):
        return True
    if isinstance(x, PredicateConstant):
        return True
    if not isinstance(x, AtomicSentence):
        return False
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
    if check_atomic_sentence(x):
        return True
    if not isinstance(x, Sentence):
        return False
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
