from lark import Lark, Transformer


class IntervalExpr:
    def __init__(self, inter_type, start, end):
        if inter_type == "set.Ioo":
            self.left = "]"
            self.right = "["
        elif inter_type == "set.Icc":
            self.left = "["
            self.right = "]"
        self.start = start
        self.end = end

    def to_html(self):
        return self.left + self.start + ", " + self.end + self.right


class Expression:
    def __init__(self, items):
        self.items = items

    def to_html(self):
        s = ""
        for item in self.items:
            if isinstance(item, str):
                s += item
            else:
                s += item.to_html()
        return s


class Assertion:
    def __init__(self, s):
        self.s = s

    def to_html(self):
        return self.s


class DeclarationAssertion:
    def __init__(self, symbols, set_class):
        self.symbols = symbols
        self.set_class = set_class

    def to_html(self):
        s = ""
        for symbol in self.symbols[:-1]:
            s += symbol + ", "
        s += self.symbols[-1]
        s += "∈ " + self.set_class
        return s


class FunctionAssertion:
    def __init__(self, name, start_set, end_set):
        self.name = name
        self.start_set = start_set
        self.end_set = end_set

    def to_html(self):
        return self.name + ":" + self.start_set + "→" + self.end_set


class ContinuousHypothesis:
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

    def to_html(self):
        return self.name + " is continous on " + self.expr.to_html()


class DifferentiableHypothesis:
    def __init__(self, dom, name, expr):
        self.dom = dom
        self.name = name
        self.expr = expr

    def to_html(self):
        return (
            self.name
            + " is differentiable on "
            + self.expr.to_html()
            + " to "
            + self.dom
        )


class ExistentialResult:
    def __init__(self, assertions, goal):
        self.assertions = assertions
        self.goal = goal

    def to_html(self):
        s = "∃"
        s += self.assertions[0].to_html()
        if self.assertions[1:]:
            s += "with\n<br>\n<ul>\n"
            for assertion in self.assertions[1:]:
                s += "<li>"
                s += assertion.to_html()
                s += "</li>\n"
            s += "</ul>"
        s += "such that\n<br>\n"
        s += self.goal.to_html()
        return s


class LeanTheorem:
    def __init__(self, name=None, hypotheses=None, result=None):
        self.name = name
        if hypotheses is None:
            hypotheses = []
        self.hypotheses = hypotheses
        self.result = result

    def to_html(self):
        s = "<em>Theorem</em> : " + self.name + "<br>\n"
        s += "Let\n<br>\n"
        s += "<ul>\n"
        for hypothesis in self.hypotheses:
            s += "<li>"
            s += hypothesis.to_html()
            s += "</li>\n"
        s += "</ul>\n"
        s += "Then,\n<br>\n"
        s += self.result.to_html()
        return s


lean_string = r"""
    lean: "theorem" LETTER_LIKE hypotheses ":" result
    hypotheses: _hypothesis*
    _hypothesis: "(" hypothesis ")" | "{" hypothesis "}"
    hypothesis: function_declaration | declaration | named_hypothesis | basic_hypothesis
    function_declaration: LETTER_LIKE ":" DOMAIN "→" DOMAIN
    declaration: LETTER_LIKE* ":" DOMAIN
    DOMAIN: LETTER_LIKE
    named_hypothesis: LETTER_LIKE ":" _named_hyp
    _named_hyp: continuous_on | differentiable_on | expr
    continuous_on: "continuous_on" LETTER_LIKE expr
    differentiable_on: "differentiable_on" DOMAIN LETTER_LIKE expr
    basic_hypothesis: LETTER_LIKE*
    result: existential_result | goal
    existential_result: "∃" hypotheses "," expr
    goal: LETTER_LIKE*
    !expr: LETTER_LIKE
          | interval
          | SEP+ expr
          | expr SEP+ expr
          | "(" expr ")"
    !unary_expr: LETTER_LIKE
               | SEP+ unary_expr
               | "(" expr ")"
    interval: INTERVAL_TYPE unary_expr SEP+ unary_expr
    INTERVAL_TYPE: "set.Ioo" | "set.Icc"
    SEP: " " | "\n" | "\r" | "\t"
    LETTER_LIKE: /[^\s:\n\t\r\(\){}]+/
    %import common.WS
    %ignore WS
"""

parser = Lark(lean_string, start="lean")


class LeanTransformer(Transformer):
    def __init__(self):
        super().__init__()

    def lean(self, res):
        name, hypotheses, result = res
        return LeanTheorem(name, hypotheses, result)

    def hypotheses(self, hyps):
        return list(hyps)

    def hypothesis(self, hyp):
        (hyp,) = hyp
        return hyp

    def function_declaration(self, fct):
        name, domain, image_domain = fct
        return FunctionAssertion(name, domain, image_domain)

    def declaration(self, decl):
        vars = decl[:-1]
        domain = decl[-1]
        return DeclarationAssertion(vars, domain)

    def DOMAIN(self, dom):
        return dom.value

    def named_hypothesis(self, hyp):
        name = hyp[0]
        hyps = hyp[1]
        return hyps

    def continuous_on(self, hyp):
        name, expr = hyp
        return ContinuousHypothesis(name, expr)

    def differentiable_on(self, hyp):
        dom, name, expr = hyp
        return DifferentiableHypothesis(dom, name, expr)

    def basic_hypothesis(self, hyp):
        return " ".join(hyp)

    def result(self, res):
        (res,) = res
        return res

    def existential_result(self, res):
        hyps = res[0]
        goal = res[1]
        return ExistentialResult(hyps, goal)

    def goal(self, res):
        return " ".join(res)

    def expr(self, exp):
        return Expression(exp)

    def unary_expr(self, unary_expr):
        return unary_expr[0]

    def interval(self, inter):
        inter_type = inter[0]
        start = inter[1]
        end = inter[-1]
        return IntervalExpr(inter_type, start, end)

    def INTERVAL_TYPE(self, inter):
        return inter.value

    def SEP(self, sep):
        return sep.value

    def LETTER_LIKE(self, v):
        return v.value


def parse(s):
    tree = parser.parse(s)
    return LeanTransformer().transform(tree)


def lean_to_html(path):
    file = open(path)
    s = file.read()
    lean_theorem = parse(s)
    html = lean_theorem.to_html()
    html_file = open("result.html", "w")
    html_file.write(html)


if __name__ == "__main__":
    lean_to_html("example.txt")
    # lean_to_html("easy.txt")
