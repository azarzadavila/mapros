from lark import Lark, Transformer


class LeanTheorem:
    def __init__(self, name=None, hypotheses=None):
        self.name = name
        if hypotheses is None:
            hypotheses = []
        self.hypotheses = hypotheses


lean_string = r"""
    lean: "theorem" NAME hypothesis*
    NAME: /\w+/
    hypothesis.2: "(" string ")"
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

    def hypothesis(self, hyp):
        (hyp,) = hyp
        return hyp

    def S(self, s):
        return s.value

    def string(self, s):
        return "".join(s)

    def lean(self, lean_s):
        return LeanTheorem(lean_s[0], list(lean_s[1:]))


def parse(s):
    tree = parser.parse(s)
    return LeanTransformer().transform(tree)
