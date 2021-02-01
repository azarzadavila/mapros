from lark import Lark
import re

grammar = r"""
    theorem: "theorem" _WS NAME _WS hypotheses ":" _WS result
    NAME: /\w+/
    hypotheses: (_hypothesis _WS)+
    _hypothesis: "(" hypothesis ")"
    hypothesis: other
    result: other
    other: /\w+/
    _WS: " "
"""

parser = Lark(grammar, start="theorem", parser="lalr", lexer="contextual")


def preprocess(s):
    s = re.sub(r"\s+", " ", s)
    return s.strip()


s = "theorem exists_ratio_deriv_eq_ratio_slope (okey) (another) : this"

print(parser.parse(preprocess(s)).pretty())
