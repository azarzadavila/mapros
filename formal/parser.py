from lark import Lark

sentence_parser = Lark(
    r"""
    sentence: "true" | "false"
            | /\w/
            | /\w/ "(" [term ("," term)*] ")"
            | unaryconnector "(" sentence ")"
            | unaryconnector /\w/
            | "(" sentence ")" binaryconnector "(" sentence ")"
            | /\w/ binaryconnector /\w/
            | /\w/ binaryconnector "(" sentence ")"
            | "(" sentence ")" binaryconnector /\w/
            | quantifier /\w/ "(" sentence ")"
    term: /\w/ | /\w/ "(" [term ("," term)*] ")"
    unaryconnector : "-"
    binaryconnector : "AND" | "OR" | "=>" | "<=>"
    quantifier : "FORALL" | "EXISTS"

    %import common.WS
    %ignore WS

""",
    start="sentence",
)


def parse(s):
    """
    Parses the sentence string to a Sentence instance with Lark
    :param s: Sentence in string format
    :return: Sentence instance
    """
    pass
