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
    unaryconnector : "negation"
    binaryconnector : "AND" | "OR" | "=>" | "<=>"
    unarysentence: unaryconnector "(" sentence ")"
    binarysentence: "(" sentence ")" binaryconnector "(" sentence ")"
    quantifier : "FORALL" | "EXISTS"
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

    def unaryconnector(self, connector):
        return "negation"

    def unarysentence(self, unarysentence):
        connector, sentence = unarysentence
        return UnaryConnectorSentence(UnaryConnector.from_str(connector), sentence)

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
    pass
