from lark import Lark, Transformer
from sets.real import Real
from sets.real_interval import RealInterval
from sets import command
from sets.utils import Order

latex_parser = Lark(
    r"""
    latex_sentence: declaration | interval | order
    declaration: variable " \in \mathbb{R}" 
    order: variable order_operator variable
    variable: V1 | V2
    order_operator: LT | LE | EQ | GT | GE
    LT: "<"
    LE: "\leq"
    EQ: "="
    GT: ">"
    GE: "\geq"
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
    def __init__(self, receiver):
        super().__init__()
        self._receiver = receiver

    def latex_sentence(self, latex):
        (latex,) = latex
        return latex

    def declaration(self, declaration):
        (symbol,) = declaration
        return command.NewVariableCommand(self._receiver, symbol)

    def variable(self, var):
        (var,) = var
        if is_number(var):
            return float(var)
        return var

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

    def order(self, o):
        var1, order_op, var2 = o
        return command.OrderCommand(self._receiver, order_op, var1, var2)

    def order_operator(self, order_op):
        (order_op,) = order_op
        return order_op

    def LT(self, lt):
        return Order.LT

    def LE(self, le):
        return Order.LE

    def EQ(self, eq):
        return Order.EQ

    def GT(self, gt):
        return Order.GT

    def GE(self, ge):
        return Order.GE

    def interval(self, inter):
        left, start, end, right = inter
        include_start = left == "["
        include_end = right == "]"
        return command.NewIntervalCommand(
            self._receiver, start, end, include_start, include_end, symbol="I"
        )


def parse(s, receiver):
    tree = latex_parser.parse(s)
    return LatexTransformer(receiver).transform(tree)
