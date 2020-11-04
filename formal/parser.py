from lark import Lark, Transformer
from formal.grammar import *

sentence_parser = Lark(
    r"""
    sentence: "true" | "false"
            | predicate
            | constant_predicate
            | unarysentence
            | binarysentence
            | quantifiersentence
    term: variable | function
    function: SYMBOL "(" [term ("," term)*] ")"
    variable: SYMBOL
    constant_predicate: SYMBOL
    predicate: SYMBOL "(" [term ("," term)*] ")"
    unaryconnector : NEGATION
    NEGATION: "negation"
    binaryconnector : CONJUNCTION | DISJUNCTION | IMPLICATION | BICONDITIONAL
    CONJUNCTION : "AND"
    DISJUNCTION : "OR"
    IMPLICATION : "=>"
    BICONDITIONAL : "<=>"
    unarysentence: unaryconnector "(" sentence ")"
    binarysentence: "(" sentence ")" binaryconnector "(" sentence ")"
    quantifier : UNIVERSAL | EXISTENTIAL
    UNIVERSAL : "FORALL"
    EXISTENTIAL : "EXISTS"
    quantifiersentence : quantifier variable "(" sentence ")"
    SYMBOL : /\w/

    %import common.WS
    %ignore WS

""",
    start="sentence",
)


class SentenceTransformer(Transformer):
    def sentence(self, sentence):
        (sentence,) = sentence
        return sentence

    NEGATION = lambda self, _: "negation"

    def unaryconnector(self, connector):
        return UnaryConnector.from_str(connector[0])

    def unarysentence(self, unarysentence):
        connector, sentence = unarysentence
        return UnaryConnectorSentence(connector, sentence)

    CONJUNCTION = lambda self, _: "conjunction"
    DISJUNCTION = lambda self, _: "disjunction"
    IMPLICATION = lambda self, _: "implication"
    BICONDITIONAL = lambda self, _: "biconditional"

    def binaryconnector(self, connector):
        return BinaryConnector.from_str(connector[0])

    def binarysentence(self, binarysentence):
        sentence1, connector, sentence2 = binarysentence
        return BinaryConnectorSentence(connector, sentence1, sentence2)

    UNIVERSAL = lambda self, _: "universal"
    EXISTENTIAL = lambda self, _: "existential"

    def quantifier(self, quantifier):
        return Quantifier.from_str(quantifier[0])

    def quantifiersentence(self, quantifiersentence):
        quantifier, variable, sentence = quantifiersentence
        return QuantifierSentence(quantifier, variable, sentence)

    def variable(self, symbol):
        return Variable(symbol=symbol[0])

    def constant_predicate(self, symbol):
        return ConstantPredicate(symbol=symbol[0])

    def term(self, term):
        print(term)
        (term,) = term
        return term

    def SYMBOL(self, symbol):
        return symbol.value

    def predicate(self, predicate):
        symbol = predicate[0]
        terms = predicate[1:]
        return Predicate(symbol, *list(terms))


def parse(s):
    """
    Parses the sentence string to a Sentence instance with Lark
    :param s: Sentence in string format
    :return: Sentence instance
    """
    tree = sentence_parser.parse(s)
    return SentenceTransformer().transform(tree)
