from lark import Lark
import re

grammar = r"""
    theorem: "theorem" _WS NAME _WS? hypotheses ":" _WS? result
    NAME: /\w+/
    hypotheses: (_hypothesis _WS?)+
    _hypothesis: "(" hypothesis ")"
    hypothesis: named_hypothesis
    named_hypothesis: NAME _WS? ":" _WS? _expression{NAMED_CONTENT} (_WS? _expression{NAMED_CONTENT})*
    NAMED_CONTENT: /[^\(\)→]/+
    container: NOT_PAR | "(" container ")"
    _expression{content}: content | "(" content ")"
    NOT_PAR: /[^\(\)]+/
    result: other
    other: /\w+/
    _WS: " "
"""

parser = Lark(grammar, start="theorem", parser="lalr", lexer="contextual")


def preprocess(s):
    s = re.sub(r"\s+", " ", s)
    return s.strip()


s = "theorem exists_ratio_deriv_eq_ratio_slope (ha : a < b)(hb : b) (hc : (a+b) < (c+d)) : this"

print(parser.parse(preprocess(s)).pretty())
