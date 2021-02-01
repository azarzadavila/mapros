from lark import Lark
import re

grammar = r"""
    theorem: "theorem" _WS NAME _WS? hypotheses ":" _WS? result
    NAME: /\w+/
    hypotheses: (_hypothesis _WS?)+
    _hypothesis: "(" hypothesis ")"
    hypothesis: function_declaration | named_hypothesis
    function_declaration: NAME _WS? ":" _WS? DOMAIN _WS? "→" _WS? DOMAIN
    named_hypothesis: NAME _WS? ":" _WS? _expression{NAMED_CONTENT} (_WS? _expression{NAMED_CONTENT})*
    NAMED_CONTENT: /[^\(\)→]+/
    DOMAIN: /[^\(\)→ ]+/
    container: NOT_PAR | "(" container ")"
    _expression{content}: content | "(" content ")"
    NOT_PAR: /[^\(\)]+/
    result: other
    other: /\w+/
    _WS: " "
"""

parser = Lark(grammar, start="theorem", parser="earley")


def preprocess(s):
    s = re.sub(r"\s+", " ", s)
    return s.strip()


s = "theorem exists_ratio_deriv_eq_ratio_slope (ha : a < b)(hb : b) (hc : (a+b) < (c+d)) (g : R → R): this"

print(parser.parse(preprocess(s)).pretty())
