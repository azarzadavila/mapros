from lark import Lark, Transformer


class LeanTheorem:
    def __init__(self, name=None, hypotheses=None, result=None):
        self.name = name
        if hypotheses is None:
            hypotheses = []
        self.hypotheses = hypotheses
        self.result = result


lean_string = r"""
    lean: "theorem" NAME hypotheses ":" result
    result: "∃" hypotheses "," string | string
    NAME: /\w+/
    hypotheses: hypothesis*
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

    def hypotheses(self, hyps):
        return list(hyps)

    def S(self, s):
        return s.value

    def string(self, s):
        return "".join(s)

    def result(self, res):
        if len(res) == 1:
            return res
        else:
            hyp, goal = res
            return [hyp, goal]

    def lean(self, lean_s):
        name, hypotheses, result = lean_s
        return LeanTheorem(name, hypotheses, result)


def parse(s):
    tree = parser.parse(s)
    return LeanTransformer().transform(tree)
