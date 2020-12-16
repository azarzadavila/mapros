from lark import Lark, Transformer

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


class LatexTransformer(Transformer):
    def declaration(self, declaration):
        (symbol,) = declaration
        return symbol

    def variable(self, var):
        (var,) = var
        return var

    def V1(self, v):
        return v.value

    def V2(self, v):
        return v.value


def parse(s):
    tree = latex_parser.parse(s)
    return LatexTransformer().transform(tree)
