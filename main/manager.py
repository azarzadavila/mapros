import re

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

HEADER = r"""import data.real.basic
notation `|` x `|` := abs x
@[user_attribute]
meta def ineq_rules : user_attribute :=
{ name := `ineq_rules,
  descr := "lemmas usable to prove inequalities" }
attribute [ineq_rules] add_lt_add le_max_left le_max_right
meta def obvious_ineq := `[linarith <|> apply_rules ineq_rules]
run_cmd add_interactive [`obvious_ineq]
definition is_limit (a : ℕ → ℝ) (l : ℝ) :=
∀ ε > 0, ∃ N, ∀ n ≥ N, | a n - l | < ε
"""

START = len(HEADER.split("\n"))


def extract_goal(state):
    goal = state.split("\n")[-1]
    match = re.search(r"⊢ (.+)", goal)
    if not match:
        return None
    return match[1]


def extract_goals(states):
    return list(map(lambda state: extract_goal(state), states))


def extract_error(msg):
    msg = msg.split("\n")
    index = 0
    match = None
    while not match and index < len(msg):
        match = re.search(r"state", msg[index])
        index += 1
    if not match:
        return None
    index -= 1
    if index == -1:
        return None
    return "\n".join(msg[:index])


def extract_variable(state, ident):
    state = state.split("\n")
    for line in state:
        match = re.match(r"([^:]+) : (.+)", line)
        if match:
            idents = match[1].split(" ")
            for cur in idents:
                if cur == ident:
                    if match[2][-1] == ",":
                        return match[2][:-1]
                    return match[2]
    return None


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

    def to_lean(self, header=True):
        s = ""
        if header:
            s += HEADER
        start = 1
        if header:
            start += START - 1
        lines = []
        s += "theorem " + self.theorem_name
        s += "\n"
        start += 1
        ident_hyp = self.ident_hypotheses()
        for i in range(len(ident_hyp)):
            s += "("
            if ident_hyp[i]:
                s += ident_hyp[i] + " : "
            s += self.hypotheses[i].to_lean()
            s += ")"
            s += "\n"
            start += 1
        s += ":\n"
        start += 1
        s += self.initial_goal.to_lean() + "\n"
        start += 1
        s += ":=\n"
        start += 1
        s += "begin\n"
        lines.append(start)
        start += 1
        for proof_line in self.proof:
            obj = proof_line["obj"]
            s += obj.to_lean()
            if not isinstance(obj, DoAllSubgoals):
                s += ","
            lines.append(start)
            s += "\n"
            start += 1
        s += "end"
        return s, lines
