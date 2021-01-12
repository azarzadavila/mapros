from lark import Lark, Transformer


class Assertion:
    def __init__(self, s):
        self.s = s

    def to_html(self):
        return self.s


class Result:
    def __init__(self, goal):
        self.goal = goal

    def to_html(self):
        return self.goal


class ExistentialResult(Result):
    def __init__(self, assertions, goal):
        super().__init__(goal)
        self.assertions = assertions

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
    assertion.2: "(" string ")" | "{" string "}"
    goal: string
    string : S+
    S: /./
    %import common.WS
    %ignore WS
"""

parser = Lark(lean_string, start="lean")


class LeanTransformer(Transformer):
    def __init__(self):
        super().__init__()

    def NAME(self, name):
        return name.value

    def assertion(self, assertion):
        (assertion,) = assertion
        return Assertion(assertion)

    def assertions(self, assertions):
        return list(assertions)

    def S(self, s):
        return s.value

    def string(self, s):
        return "".join(s)

    def result(self, res):
        (res,) = res
        return res

    def goal(self, s):
        (s,) = s
        return Result(s)

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
