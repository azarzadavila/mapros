from main.context import Context
from main.sentences import RealValuedSequences, RealDeclaration, SequenceLimit, ForAll


class Manager:
    def __init__(self):
        self.context = Context()
        self.hypotheses = []
        self.initial_goal = None
        self.theorem_name = "anonymous"

    def add_hypothesis(self, nat):
        match = RealValuedSequences.from_natural(nat, self.context)
        if not match:
            match = RealDeclaration.from_natural(nat, self.context)
        if not match:
            match = SequenceLimit.from_natural(nat, self.context)
        if not match:
            match = ForAll.from_natural(nat, self.context)
        if not match:
            raise ValueError("Unrecognized hypothesis")
        self.hypotheses.append(match)

    def set_initial_goal(self, nat):
        match = SequenceLimit.from_natural(nat, self.context)
        if not match:
            raise ValueError("Unrecognized goal")
        self.initial_goal = match
        self.context.current_goal = match

    def ident_hypotheses(self):
        res = []
        count = 1
        for hyp in self.hypotheses:
            if isinstance(hyp, RealValuedSequences) or isinstance(hyp, RealDeclaration):
                res.append(None)
            else:
                res.append("H{}".format(count))
                count += 1
        return res

    def to_lean(self):
        s = "theorem " + self.theorem_name
        s += "\n"
        ident_hyp = self.ident_hypotheses()
        for i in range(len(ident_hyp)):
            s += "("
            if ident_hyp[i]:
                s += ident_hyp[i] + " : "
            s += self.hypotheses[i].to_lean()
            s += ")"
            s += "\n"
        s += ":\n"
        s += self.initial_goal.to_lean() + "\n"
        s += ":=\n"
        s += "begin\n"
        s += "sorry,\n"
        s += "end"
        return s
