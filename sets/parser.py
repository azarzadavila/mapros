from lark import Lark, Transformer
from sets.real import Real

latex_parser = Lark(
    r"""
    declaration: variable " \in \mathbb{R}" 
    variable: V1 | V2
    V1: /\w+/
    V2: /\\\w+/
    
    %import common.WS
    %ignore WS
    """,
    start="declaration",
)


def is_number(var):
    try:
        float(var)
        return True
    except ValueError:
        return False


class LatexTransformer(Transformer):
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


def parse(s):
    tree = latex_parser.parse(s)
    return LatexTransformer().transform(tree)
