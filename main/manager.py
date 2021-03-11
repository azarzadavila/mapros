from main.context import Context
from main.sentences import RealValuedSequences, RealDeclaration, SequenceLimit, ForAll
from main.tactic import (
    LetGoalLimit,
    ChooseNEpsilonLimit,
    LetMax,
    Use,
    ByInequalityProperties,
    LetNInequality,
    BySentenceWith,
    LetsChooseIn,
    AbsoluteValueIneqProperty,
    Cases,
    SplitGoal,
    DoAllSubgoals,
    LinearArithmetic,
)


class Manager:
    def __init__(self):
        self.context = Context()
        self.hypotheses = []
        self.initial_goal = None
        self.theorem_name = "anonymous"
        self.proof = []

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

    def add_proof_line(self, nat):
        possible = [
            DoAllSubgoals,
            LetGoalLimit,
            ChooseNEpsilonLimit,
            LetMax,
            Use,
            ByInequalityProperties,
            LetNInequality,
            BySentenceWith,
            LetsChooseIn,
            AbsoluteValueIneqProperty,
            Cases,
            SplitGoal,
            LinearArithmetic,
        ]
        i = 0
        match = None
        while not match and i < len(possible):
            match = possible[i].from_natural(nat, self.context)
            i += 1
        if not match:
            raise ValueError("Unrecognized tactic")
        # TODO get lean response if needed
        self.proof.append({"type": "user", "obj": match})

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
        for proof_line in self.proof:
            obj = proof_line["obj"]
            s += obj.to_lean()
            if not isinstance(obj, DoAllSubgoals):
                s += ","
            s += "\n"
        s += "end"
        return s
