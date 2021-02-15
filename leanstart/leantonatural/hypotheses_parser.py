from lark import Lark, Transformer

import leanhtml as lhtml

grammar = r"""
    start: _SEP* (function_declaration | declaration | named_hypothesis) _SEP*
    function_declaration: IDENTIFIER (_SEP* IDENTIFIER)* _SEP* ":" _SEP* DOMAIN _SEP* "→" _SEP* DOMAIN
    declaration: IDENTIFIER (_SEP+ IDENTIFIER)* _SEP* ":" _SEP* DOMAIN
    named_hypothesis: IDENTIFIER _SEP* ":" _SEP* _named_hypothesis
    _named_hypothesis: expr
    expr: basic_expr (_SEP+ basic_expr)*
    basic_expr: par_expr | interval | LETTER_LIKE
    par_expr: "(" _SEP* expr _SEP* ")"
    interval.2: INTERVAL_TYPE _SEP+ (par_expr | LETTER_LIKE) _SEP+ (par_expr | LETTER_LIKE)
    INTERVAL_TYPE: "set.Ioo" | "set.Ico" | "set.Ioc" | "set.Icc"
    IDENTIFIER: /[^\s\(\)]+/
    DOMAIN: /[^\s\(\)]+/
    LETTER_LIKE: /[^\s\(\)]+/
    _SEP: /\s/
"""

parser = Lark(grammar)


class HypothesisTransformer(Transformer):
    def start(self, node):
        return node[0]

    def function_declaration(self, node):
        start_domain = node[-2]
        end_domain = node[-1]
        identifiers = node[:-2]
        return lhtml.FunctionDeclarationHtml(identifiers, start_domain, end_domain)

    def declaration(self, node):
        dom = node[-1]
        identifiers = node[:-1]
        return lhtml.DeclarationHtml(identifiers, dom)

    def named_hypothesis(self, node):
        identifier = node[0]  # the identifier is not really useful in the output
        _named_hyp = node[1]
        return lhtml.HypothesisHtml(_named_hyp)

    def expr(self, node):
        return lhtml.ExprHtml(list(node))

    def basic_expr(self, node):
        return node[0]

    def par_expr(self, node):
        return lhtml.ParExprHtml(node[0])

    def interval(self, node):
        inter_type = node[0]
        inter_start = lhtml.BasicHtml(node[1])
        inter_end = lhtml.BasicHtml(node[2])
        return lhtml.IntervalHtml(inter_type, inter_start, inter_end)

    def LETTER_LIKE(self, terminal):
        return terminal

    def IDENTIFIER(self, terminal):
        return terminal

    def DOMAIN(self, terminal):
        return terminal


def transform(s):
    tree = parser.parse(s)
    print(tree.pretty())
    return HypothesisTransformer().transform(tree)


def transform_list(hypotheses):
    res = []
    for s in hypotheses:
        res.append(transform(s))
    return res
