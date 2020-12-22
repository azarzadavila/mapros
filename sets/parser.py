from lark import Lark, Transformer
from sets import command
from sets.utils import Order

variable_string = r"""
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
"""

premise_parser = Lark(
    r"""
    premise: declaration | interval_declaration | order
    declaration: variable " \in \mathbb{R}"
    interval_declaration: variable EQ interval
    order: variable order_operator variable
    """
    + variable_string,
    start="premise",
)

question_parser = Lark(
    r"""
    question: intersection
    intersection: variable " \cap " variable | variable "\cap " variable
    """
    + variable_string,
    start="question",
)


def is_number(var):
    try:
        float(var)
        return True
    except ValueError:
        return False


class VariableTransformer(Transformer):
    def __init__(self):
        super().__init__()

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
        return start, end, include_start, include_end


class PremiseTransformer(VariableTransformer):
    def __init__(self, receiver):
        super().__init__()
        self._receiver = receiver

    def premise(self, latex):
        (latex,) = latex
        return latex

    def declaration(self, declaration):
        (symbol,) = declaration
        return command.NewVariableCommand(self._receiver, symbol)

    def order(self, o):
        var1, order_op, var2 = o
        return command.OrderCommand(self._receiver, order_op, var1, var2)

    def interval_declaration(self, inter_decl):
        var, inter = inter_decl
        start, end, include_start, include_end = inter
        return command.NewIntervalCommand(
            self._receiver, start, end, include_start, include_end, var
        )


class QuestionTransformer(VariableTransformer):
    def __init__(self, receiver):
        super().__init__()
        self._receiver = receiver

    def question(self, latex):
        (latex,) = latex
        return latex

    def intersection(self, inter):
        var1, var2 = inter
        return command.IntersectionQuestion(self._receiver, var1, var2)


def premise_parse(s, receiver):
    tree = premise_parser.parse(s)
    return PremiseTransformer(receiver).transform(tree)


def question_parse(s, receiver):
    tree = question_parser.parse(s)
    return QuestionTransformer(receiver).transform(tree)
