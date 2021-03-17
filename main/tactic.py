from abc import ABC
import re
from typing import List

from main.language import Language, from_natural, from_lean
from main.sentences import (
    SequenceLimit,
    IdentifierEpsilon,
    Identifier,
    Inequality,
    ForAllNatIneqThen,
)


class Tactic(Language, ABC):
    def to_extract(self) -> List:
        raise NotImplementedError


def _sentences_match_letgoallimit():
    return [IdentifierEpsilon, Identifier]


class LetGoalLimit(Tactic):
    def __init__(self, ident, hyp):
        self.ident = ident
        self.hyp = hyp

    def to_lean(self) -> str:
        return "intros " + self.ident.to_lean() + " " + self.hyp

    def to_natural(self, in_math=False) -> str:
        return "Let $" + self.ident.to_natural() + "$"

    @classmethod
    def from_natural(cls, s: str, context=None, in_math=False):
        match = re.fullmatch(r"Let \$(\\?\w+)\$", s)
        if not match:
            return None
        if not isinstance(context.current_goal, SequenceLimit):
            return None
        ident = from_natural(
            match[1], context, _sentences_match_letgoallimit(), in_math
        )
        if not ident:
            return None
        hyp = context.next_anonymous()
        context.associate(ident.to_lean(), hyp)
        return cls(ident, hyp)

    @classmethod
    def from_lean(cls, s: str, context=None):
        match = re.fullmatch(r"intros (\w+) (\w+)", s)
        if not match:
            return None
        if not isinstance(context.current_goal, SequenceLimit):
            return None
        ident = from_lean(match[1], context, _sentences_match_letgoallimit())
        if not ident:
            return None
        hyp = match[2]
        context.associate(ident.to_lean(), hyp)
        return cls(ident, hyp)

    def to_extract(self) -> List:
        return [self.hyp]


def _sentences_match_choosenepsilonlimit():
    return [IdentifierEpsilon, Identifier]


class ChooseNEpsilonLimit(Tactic):
    def __init__(self, limit_def, eps, hyp_eps, n_chosen, hyp_n):
        self.limit_def = limit_def
        self.eps = eps
        self.hyp_eps = hyp_eps
        self.n_chosen = n_chosen
        self.hyp_n = hyp_n

    def to_lean(self) -> str:
        return (
            "cases "
            + self.limit_def
            + " "
            + self.eps.to_lean()
            + " "
            + self.hyp_eps
            + " with "
            + self.n_chosen
            + " "
            + self.hyp_n
        )

    def to_natural(self, in_math=False) -> str:
        return (
            "Let's choose $"
            + self.n_chosen
            + "$ such that "
            + self.limit_def
            + " uses $"
            + self.eps.to_natural()
            + "$"
        )

    @classmethod
    def from_natural(cls, s: str, context=None, in_math=False):
        match = re.fullmatch(
            r"Let's choose \$(\w+)\$ such that (\w+) uses \$(\\?\w+)\$", s
        )
        if not match:
            return None
        n_chosen = match[1]
        limit_def = match[2]
        eps = from_natural(
            match[3], context, _sentences_match_choosenepsilonlimit(), in_math
        )
        hyp_eps = context.get(eps.to_lean()).get("associate")
        if not hyp_eps:
            return None
        hyp_n = context.next_anonymous()
        context.associate(n_chosen, hyp_n)
        return cls(limit_def, eps, hyp_eps, n_chosen, hyp_n)

    @classmethod
    def from_lean(cls, s: str, context=None):
        match = re.fullmatch(r"cases (\w+) (\w+) (\w+) with (\w+) (\w+)", s)
        if not match:
            return None
        limit_def = match[1]
        eps = from_lean(match[2], context, _sentences_match_choosenepsilonlimit())
        hyp_eps = match[3]
        n_chosen = match[4]
        hyp_n = match[5]
        return cls(limit_def, eps, hyp_eps, n_chosen, hyp_n)

    def to_extract(self) -> List:
        return [self.hyp_n]


class LetMax(Tactic):
    def __init__(self, ident, ident1, ident2):
        self.ident = ident
        self.ident1 = ident1
        self.ident2 = ident2

    def to_lean(self) -> str:
        return "let " + self.ident + " := max " + self.ident1 + " " + self.ident2

    def to_natural(self, in_math=False) -> str:
        return (
            "Let $"
            + self.ident
            + " = \\max\\left("
            + self.ident1
            + ", "
            + self.ident2
            + "\\right)$"
        )

    @classmethod
    def from_natural(cls, s: str, context=None, in_math=False):
        match = re.fullmatch(
            r"Let \$(\w+) ?= ?\\?max ?(?:\\left)?\((\w+), (\w+) ?(?:\\right)?\)\$", s
        )
        if not match:
            return None
        return cls(match[1], match[2], match[3])

    @classmethod
    def from_lean(cls, s: str, context=None):
        match = re.fullmatch(r"let (\w+) := max (\w+) (\w+)", s)
        if not match:
            return None
        return cls(match[1], match[2], match[3])

    def to_extract(self) -> List:
        return []


class Use(Tactic):
    def __init__(self, ident):
        self.ident = ident

    def to_lean(self) -> str:
        return "use " + self.ident

    def to_natural(self, in_math=False) -> str:
        return "We claim $" + self.ident + "$ works"

    @classmethod
    def from_natural(cls, s: str, context=None, in_math=False):
        match = re.fullmatch(r"We claim \$(\w+)\$ works", s)
        if not match:
            return None
        return cls(match[1])

    @classmethod
    def from_lean(cls, s: str, context=None):
        match = re.fullmatch(r"use (\w+)", s)
        if not match:
            return None
        return cls(match[1])

    def to_extract(self) -> List:
        return []


def _sentences_match_byinequalityproperties():
    return [Inequality]


class ByInequalityProperties(Tactic):
    def __init__(self, ident, sentence):
        self.ident = ident
        self.sentence = sentence

    def to_lean(self) -> str:
        return (
            "have "
            + self.ident
            + " : "
            + self.sentence.to_lean()
            + " := by obvious_ineq"
        )

    def to_natural(self, in_math=False) -> str:
        return "By inequality properties, " + self.sentence.to_natural()

    @classmethod
    def from_natural(cls, s: str, context=None, in_math=False):
        match = re.fullmatch(r"By inequality properties, (.+)", s)
        if not match:
            return None
        sentence = from_natural(
            match[1], context, _sentences_match_byinequalityproperties(), in_math
        )
        if not sentence:
            return None
        ident = context.next_anonymous()
        return cls(ident, sentence)

    @classmethod
    def from_lean(cls, s: str, context=None):
        match = re.fullmatch(r"have (\w+) : (.+) := by obvious_ineq", s)
        if not match:
            return None
        sentence = from_lean(
            match[2], context, _sentences_match_byinequalityproperties()
        )
        if not sentence:
            return None
        return cls(match[1], sentence)

    def to_extract(self) -> List:
        return [self.ident]


class LetNInequality(Tactic):
    def __init__(self, ident, hyp):
        self.ident = ident
        self.hyp = hyp

    def to_lean(self) -> str:
        return "intros " + self.ident + " " + self.hyp

    def to_natural(self, in_math=False) -> str:
        return "Let $" + self.ident + "$"

    @classmethod
    def from_natural(cls, s: str, context=None, in_math=False):
        match = re.fullmatch(r"Let \$(\w+)\$", s)
        if not match:
            return None
        if not isinstance(context.current_goal, ForAllNatIneqThen):
            return None
        ident = match[1]
        hyp = context.next_anonymous()
        return cls(ident, hyp)

    @classmethod
    def from_lean(cls, s: str, context=None):
        match = re.fullmatch(r"intros (\w+) (\w+)", s)
        if not match:
            return None
        if not isinstance(context.current_goal, ForAllNatIneqThen):
            return None
        ident = match[1]
        hyp = match[2]
        return cls(ident, hyp)

    def to_extract(self) -> List:
        return [self.hyp]


def _sentences_match_bysentencewith():
    return [Inequality]


class BySentenceWith(Tactic):
    def __init__(self, ident, sentence, hyp, with_w):
        self.ident = ident
        self.sentence = sentence
        self.hyp = hyp
        self.with_w = with_w

    def to_lean(self) -> str:
        return (
            "have "
            + self.ident
            + " : "
            + self.sentence.to_lean()
            + " := "
            + self.hyp
            + " "
            + self.with_w
        )

    def to_natural(self, in_math=False) -> str:
        return self.sentence.to_natural() + " by " + self.hyp + " with " + self.with_w

    @classmethod
    def from_natural(cls, s: str, context=None, in_math=False):
        match = re.fullmatch(r"(.+) by (\w+) with (\w+)", s)
        if not match:
            return None
        sentence = from_natural(match[1], context, _sentences_match_bysentencewith())
        if not sentence:
            return None
        ident = context.next_anonymous()
        return cls(ident, sentence, match[2], match[3])

    @classmethod
    def from_lean(cls, s: str, context=None):
        match = re.fullmatch(r"have (\w+) : (.+) := (\w+) (\w+)", s)
        if not match:
            return None
        sentence = from_lean(match[2], context, _sentences_match_bysentencewith())
        if not sentence:
            return None
        return cls(match[1], sentence, match[3], match[4])

    def to_extract(self) -> List:
        return [self.ident]


class LetsChooseIn(Tactic):
    def __init__(self, ident, hyp, point):
        self.ident = ident
        self.hyp = hyp
        self.point = point

    def to_lean(self) -> str:
        return "have " + self.ident + " := " + self.hyp + " " + self.point

    def to_natural(self, in_math=False) -> str:
        return "Let's choose " + self.point + " in " + self.hyp

    @classmethod
    def from_natural(cls, s: str, context=None, in_math=False):
        match = re.fullmatch(r"Let's choose (\w+) in (\w+)", s)
        if not match:
            return None
        ident = context.next_anonymous()
        return cls(ident, match[2], match[1])

    @classmethod
    def from_lean(cls, s: str, context=None):
        match = re.fullmatch(r"have (\w+) := (\w+) (\w+)", s)
        if not match:
            return None
        return cls(match[1], match[2], match[3])

    def to_extract(self) -> List:
        return [self.ident]


class AbsoluteValueIneqProperty(Tactic):
    def __init__(self, identifiers):
        self.identifiers = identifiers

    def to_lean(self) -> str:
        s = "rw abs_sub_lt_iff at"
        for ident in self.identifiers:
            if ident == "goal":
                ident = "⊢"
            s += " " + ident
        return s

    def to_natural(self, in_math=False) -> str:
        s = "Let's use absolute value inequality property on"
        for ident in self.identifiers[:-1]:
            s += " " + ident
        s += " and on " + self.identifiers[-1]
        return s

    @classmethod
    def from_natural(cls, s: str, context=None, in_math=False):
        match = re.fullmatch(
            r"Let's use absolute value inequality property on((:? \w+)*) and on (\w+)",
            s,
        )
        if not match:
            return None
        firsts = match[1]
        firsts = firsts.split(" ")
        if len(firsts) > 0:
            firsts = firsts[1:]
        firsts.append(match[3])
        return cls(firsts)

    @classmethod
    def from_lean(cls, s: str, context=None):
        match = re.fullmatch(r"rw abs_sub_lt_iff at((?: (?:\w+|⊢))+)", s)
        if not match:
            return None
        idents = match[1].split(" ")
        idents = idents[1:]
        for i in range(len(idents)):
            if idents[i] == "⊢":
                idents[i] = "goal"
        return cls(idents)

    def to_extract(self) -> List:
        res = []
        for ident in self.identifiers:
            if ident != "goal":
                res.append(ident)
        return res


class Cases(Tactic):
    def __init__(self, ident):
        self.ident = ident

    def to_lean(self) -> str:
        return "cases " + self.ident

    def to_natural(self, in_math=False) -> str:
        return "Let's separate " + self.ident

    @classmethod
    def from_natural(cls, s: str, context=None, in_math=False):
        match = re.fullmatch(r"Let's separate (\w+)", s)
        if not match:
            return None
        return cls(match[1])

    @classmethod
    def from_lean(cls, s: str, context=None):
        match = re.fullmatch(r"cases (\w+)", s)
        if not match:
            return None
        return cls(match[1])

    def to_extract(self) -> List:
        return [self.ident + "_left", self.ident + "_right"]


class SplitGoal(Tactic):
    def to_lean(self) -> str:
        return "split"

    def to_natural(self, in_math=False) -> str:
        return "Let's split the goal"

    @classmethod
    def from_natural(cls, s: str, context=None, in_math=False):
        match = re.fullmatch(r"Let's split the goal", s)
        if not match:
            return None
        return cls()

    @classmethod
    def from_lean(cls, s: str, context=None):
        match = re.fullmatch(r"split", s)
        if not match:
            return None
        return cls()

    def to_extract(self) -> List:
        return []


def _sentences_match_doallsubgoals():
    return [SplitGoal]


class DoAllSubgoals(Tactic):
    def __init__(self, tactic):
        self.tactic = tactic

    def to_lean(self) -> str:
        return self.tactic.to_lean() + ";"

    def to_natural(self, in_math=False) -> str:
        return self.tactic.to_natural() + " and do on all subgoals"

    @classmethod
    def from_natural(cls, s: str, context=None, in_math=False):
        match = re.fullmatch(r"(.+) and do on all subgoals", s)
        if not match:
            return None
        tactic = from_natural(match[1], context, _sentences_match_doallsubgoals())
        if not tactic:
            return None
        return cls(tactic)

    @classmethod
    def from_lean(cls, s: str, context=None):
        match = re.fullmatch(r"(.+);", s)
        if not match:
            return None
        tactic = from_lean(match[1], context, _sentences_match_doallsubgoals())
        if not tactic:
            return None
        return cls(tactic)

    def to_extract(self) -> List:
        return []


class LinearArithmetic(Tactic):
    def to_lean(self) -> str:
        return "linarith"

    def to_natural(self, in_math=False) -> str:
        return "By linear arithmetic"

    @classmethod
    def from_natural(cls, s: str, context=None, in_math=False):
        match = re.fullmatch(r"By linear arithmetic", s)
        if not match:
            return None
        return cls()

    @classmethod
    def from_lean(cls, s: str, context=None):
        match = re.fullmatch(r"linarith", s)
        if not match:
            return None
        return cls()

    def to_extract(self) -> List:
        return []
