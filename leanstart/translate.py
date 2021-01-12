from lark import Lark, Transformer


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
        s += self.goal
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
    lean: "theorem" NAME assertions ":" result
    result: existential_result | goal
    NAME: /\w+/
    existential_result: "∃" assertions "," string
    assertions: assertion*
    assertion.2: "(" assertion_type ")" | "{" assertion_type "}"
    assertion_type: declaration | function_declaration | assertion_basic
    assertion_basic: string
    function_declaration.2: WORD ":" string "→" string
    declaration.2: WORD* ":" WORD
    goal: string
    string : S+
    S: /./
    WORD: /[^\s:]/
    %import common.WS
    %ignore WS
"""

parser = Lark(lean_string, start="lean")


class LeanTransformer(Transformer):
    def __init__(self):
        super().__init__()

    def NAME(self, name):
        return name.value

    def WORD(self, word):
        return word.value

    def goal(self, goal):
        (goal,) = goal
        return Assertion(goal)

    def assertion_type(self, assertion):
        (assertion,) = assertion
        return assertion

    def assertion_basic(self, assertion):
        (assertion,) = assertion
        return Assertion(assertion)

    def assertion(self, assertion):
        (assertion,) = assertion
        return assertion

    def declaration(self, decl):
        vars = decl[:-1]
        set_class = decl[-1]
        return DeclarationAssertion(vars, set_class)

    def function_declaration(self, decl):
        name, start_set, end_set = decl
        return FunctionAssertion(name, start_set, end_set)

    def assertions(self, assertions):
        return list(assertions)

    def S(self, s):
        return s.value

    def string(self, s):
        return "".join(s)

    def result(self, res):
        (res,) = res
        return res

    def existential_result(self, result):
        assertions, goal = result
        return ExistentialResult(assertions, goal)

    def lean(self, lean_s):
        name, hypotheses, result = lean_s
        return LeanTheorem(name, hypotheses, result)


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
