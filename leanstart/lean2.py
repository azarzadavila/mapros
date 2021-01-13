from lark import Lark, Transformer

lean = r"""
theorem: "theorem" LETTER_LIKE hypotheses ":" result
hypotheses: _hypothesis*
_hypothesis: "(" hypothesis ")" | "{" hypothesis "}"
hypothesis: function_declaration | declaration | named_hypothesis | basic
declaration: LETTER_LIKE* ":" DOMAIN
DOMAIN: LETTER_LIKE
named_hypothesis: LETTER_LIKE ":" LETTER_LIKE
basic: LETTER_LIKE*
result: LETTER_LIKE*
LETTER_LIKE: /[^\s\n\t\r:\(\)\[\]]+/
%import common.WS
%ignore WS
"""

parser = Lark(lean, start="theorem")
s1 = "theorem mean (a b) (c : d) (a b : R) : x+a=d+1"
x = parser.parse(s1)
for child in x.children[1].children:
    print(child)
