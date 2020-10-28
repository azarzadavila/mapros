import abc
from enum import Enum, auto


class Sentence(metaclass=abc.ABCMeta):
    pass


class ConstantPredicate(Sentence):
    def __init__(self, symbol):
        self.symbol = symbol


class Predicate(Sentence):
    def __init__(self, symbol, *terms):
        self.symbol = symbol
        self.terms = list(terms)
        for term in self.terms:
            if not isinstance(term, Term):
                raise ValueError("incorrect term")


class UnaryConnectorSentence(Sentence):
    def __init__(self, connector, sentence):
        self.connector = connector
        self.sentence = sentence
        if not isinstance(connector, UnaryConnector):
            raise ValueError("incorrect connector")
        if not is_sentence(sentence):
            raise ValueError("incorrect sentence")


class BinaryConnectorSentence(Sentence):
    def __init__(self, connector, sentence1, sentence2):
        self.connector = connector
        self.sentence1 = sentence1
        self.sentence2 = sentence2
        if not isinstance(connector, BinaryConnector):
            raise ValueError("incorrect connector")
        if not is_sentence(sentence1) or not is_sentence(sentence2):
            raise ValueError("incorrect sentence")


class QuantifierSentence(Sentence):
    def __init__(self, quantifier, var, sentence):
        self.quantifier = quantifier
        self.var = var
        self.sentence = sentence
        if not isinstance(quantifier, Quantifier):
            raise ValueError("incorrect quantifier")
        if not isinstance(var, Variable):
            raise ValueError("incorrect variable")
        if not is_sentence(sentence):
            raise ValueError("incorrect sentence")


class Term(metaclass=abc.ABCMeta):
    pass


class Constant(Term):
    def __init__(self, symbol):
        self.symbol = symbol


class Variable(Term):
    def __init__(self, symbol):
        self.symbol = symbol


class Function(Term):
    def __init__(self, symbol, *terms):
        self.symbol = symbol
        self.terms = list(terms)
        for term in self.terms:
            if not isinstance(term, Term):
                raise ValueError("incorrect term")


class UnaryConnector(Enum):
    NEGATION = auto()

    def __str__(self):
        smap = {self.NEGATION: "NOT"}
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


class Quantifier(Enum):
    UNIVERSAL = auto()
    EXISTENTIAL = auto()

    def __str__(self):
        smap = {self.UNIVERSAL: "FORALL", self.EXISTENTIAL: "EXISTS"}
        return smap[self]


def is_sentence(sentence):
    return isinstance(sentence, Sentence) or isinstance(sentence, bool)
