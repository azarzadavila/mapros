from lark import Lark, Transformer
from formal.grammar import *

sentence_parser = Lark(
    r"""
    sentence: "true" | "false"
            | LITERAL
            | /\w/ "(" [term ("," term)*] ")"
            | unarysentence
            | binarysentence
            | quantifiersentence
    term: /\w/ | /\w/ "(" [term ("," term)*] ")"
    LITERAL: /\w/
    unaryconnector : "negation"
    binaryconnector : "AND" | "OR" | "=>" | "<=>"
    unarysentence: unaryconnector "(" sentence ")"
    binarysentence: "(" sentence ")" binaryconnector "(" sentence ")"
    quantifier : "FORALL" | "EXISTS"
    quantifiersentence : quantifier /\w/ "(" sentence ")"

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

    def LITERAL(self, literal):
        return ConstantPredicate(symbol=literal.value)


def parse(s):
    """
    Parses the sentence string to a Sentence instance with Lark
    :param s: Sentence in string format
    :return: Sentence instance
    """
    pass
