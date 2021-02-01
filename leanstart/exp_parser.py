from lark import Lark
import re

grammar = r"""
    theorem: "theorem" _WS NAME _WS other
    NAME: /\w+/
    other: /\w+/
    _WS: " "
"""

parser = Lark(grammar, start="theorem", parser="lalr", lexer="contextual")


def preprocess(s):
    s = re.sub(r"\s+", " ", s)
    return s.strip()


s = "theorem exists_ratio_deriv_eq_ratio_slope this"

print(parser.parse(preprocess(s)).pretty())
