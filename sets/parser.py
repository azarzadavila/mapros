from lark import Lark, Transformer
from sets.real import Real
from sets.real_interval import RealInterval

latex_parser = Lark(
    r"""
    latex_sentence: declaration | interval
    declaration: variable " \in \mathbb{R}" 
    order: variable order_operator variable
    variable: V1 | V2
    order_operator: GR | LO | GEQ | LEQ | EQ
    GR: ">"
    LO: "<"
    GEQ: "\geq"
    LEQ: "\leq"
    EQ: "="
    V1: /\w+/
    V2: /\\\w+/
    interval: bracket variable "," variable bracket
    bracket: BRACKET_RIGHT | BRACKET_LEFT
    BRACKET_RIGHT: "["
    BRACKET_LEFT: "]"
    %import common.WS
    %ignore WS
    """,
    start="latex_sentence",
)


def is_number(var):
    try:
        float(var)
        return True
    except ValueError:
        return False


class LatexTransformer(Transformer):
    def latex_sentence(self, latex):
        (latex,) = latex
        return latex

    def declaration(self, declaration):
        (symbol,) = declaration
        return symbol

    def variable(self, var):
        (var,) = var
        if is_number(var):
            return float(var)
        return Real(symbol=var)

    def V1(self, v):
        return v.value

    def V2(self, v):
        return v.value

    def bracket(self, brack):
        (brack,) = brack
        return brack

    def BRACKET_LEFT(self, brack):
        return brack.value

    def BRACKET_RIGHT(self, brack):
        return brack.value

    def interval(self, inter):
        left, start, end, right = inter
        include_start = left == "["
        include_end = right == "]"
        return RealInterval(start, end, include_start, include_end)


def parse(s):
    tree = latex_parser.parse(s)
    return LatexTransformer().transform(tree)
