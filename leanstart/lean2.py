from lark import Lark, Transformer

lean = r"""
theorem: "theorem" LETTER_LIKE _hypothesis* ":" result
_hypothesis: "(" hypothesis ")" | "{" hypothesis "}"
hypothesis: declaration | basic
declaration: LETTER_LIKE ":" LETTER_LIKE
basic: LETTER_LIKE*
result: LETTER_LIKE*
LETTER_LIKE: /[^\s\n\t\r:\(\)\[\]]+/
%import common.WS
%ignore WS
"""

parser = Lark(lean, start="theorem")
s1 = "theorem mean (a b) (c : d) : x+a=d+1"
print(parser.parse(s1))
