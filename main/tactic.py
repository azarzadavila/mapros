from abc import ABC
import re

from main.language import Language
from main.sentences import (
    SequenceLimit,
    IdentifierEpsilon,
    Identifier,
    Inequality,
    ForAllNatIneqThen,
)


def from_natural(s: str, cls, context=None, in_math=False):
    if cls == LetGoalLimit:
        match = IdentifierEpsilon.from_natural(s, context, in_math)
        if not match:
            match = Identifier.from_natural(s, context, in_math)
        return match
    if cls == ChooseNEpsilonLimit:
        match = IdentifierEpsilon.from_natural(s, context, in_math)
        if not match:
            match = Identifier.from_natural(s, context, in_math)
        return match
    if cls == ByInequalityProperties:
        match = Inequality.from_natural(s, context, in_math)
        return match
    if cls == BySentenceWith:
        match = Inequality.from_natural(s, context, in_math)
        return match
    raise NotImplementedError


def from_lean(s: str, cls, context=None):
    if cls == LetGoalLimit:
        match = IdentifierEpsilon.from_lean(s)
        if not match:
            match = Identifier.from_lean(s, context)
        return match
    if cls == ChooseNEpsilonLimit:
        match = IdentifierEpsilon.from_lean(s, context)
        if not match:
            match = Identifier.from_lean(s, context)
        return match
    if cls == ByInequalityProperties:
        match = Inequality.from_lean(s, context)
        return match
    if cls == BySentenceWith:
        match = Inequality.from_lean(s, context)
        return match
    raise NotImplementedError


class Tactic(Language, ABC):
    pass


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
        match = re.search(r"Let \$(\\?\w+)\$", s)
        if not match:
            return None
        if not isinstance(context.current_goal, SequenceLimit):
            return None
        ident = from_natural(match[1], cls, context, in_math)
        if not ident:
            return None
        hyp = context.next_anonymous()
        context.associate(ident.to_lean(), hyp)
        return cls(ident, hyp)

    @classmethod
    def from_lean(cls, s: str, context=None):
        match = re.search(r"intros (\w+) (\w+)", s)
        if not match:
            return None
        if not isinstance(context.current_goal, SequenceLimit):
            return None
        ident = from_lean(match[1], cls, context)
        if not ident:
            return None
        hyp = match[2]
        context.associate(ident.to_lean(), hyp)
        return cls(ident, hyp)


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
        match = re.search(
            r"Let's choose \$(\w+)\$ such that (\w+) uses \$(\\?\w+)\$", s
        )
        if not match:
            return None
        n_chosen = match[1]
        limit_def = match[2]
        eps = from_natural(match[3], cls, context, in_math)
        hyp_eps = context.get(eps.to_lean()).get("associate")
        if not hyp_eps:
            return None
        hyp_n = context.next_anonymous()
        context.associate(n_chosen, hyp_n)
        return cls(limit_def, eps, hyp_eps, n_chosen, hyp_n)

    @classmethod
    def from_lean(cls, s: str, context=None):
        match = re.search(r"cases (\w+) (\w+) (\w+) with (\w+) (\w+)", s)
        if not match:
            return None
        limit_def = match[1]
        eps = from_lean(match[2], cls, context)
        hyp_eps = match[3]
        n_chosen = match[4]
        hyp_n = match[5]
        return cls(limit_def, eps, hyp_eps, n_chosen, hyp_n)


class LetMax(Tactic):
    def __init__(self, ident, ident1, ident2):
        self.ident = ident
        self.ident1 = ident1
        self.ident2 = ident2

    def to_lean(self) -> str:
        return "let " + self.ident + " := max " + self.ident1 + " " + self.ident2

    def to_natural(self, in_math=False) -> str:
        return (
            "Let $" + self.ident + " = max(" + self.ident1 + ", " + self.ident2 + ")$"
        )

    @classmethod
    def from_natural(cls, s: str, context=None, in_math=False):
        match = re.search(r"Let \$(\w+) = max\((\w+), (\w+)\)\$", s)
        if not match:
            return None
        return cls(match[1], match[2], match[3])

    @classmethod
    def from_lean(cls, s: str, context=None):
        match = re.search(r"let (\w+) := max (\w+) (\w+)", s)
        if not match:
            return None
        return cls(match[1], match[2], match[3])


class Use(Tactic):
    def __init__(self, ident):
        self.ident = ident

    def to_lean(self) -> str:
        return "use " + self.ident

    def to_natural(self, in_math=False) -> str:
        return "We claim $" + self.ident + "$ works"

    @classmethod
    def from_natural(cls, s: str, context=None, in_math=False):
        match = re.search(r"We claim \$(\w+)\$ works", s)
        if not match:
            return None
        return cls(match[1])

    @classmethod
    def from_lean(cls, s: str, context=None):
        match = re.search(r"use (\w+)", s)
        if not match:
            return None
        return cls(match[1])


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
        match = re.search(r"By inequality properties, (.+)", s)
        if not match:
            return None
        sentence = from_natural(match[1], cls, context, in_math)
        if not sentence:
            return None
        ident = context.next_anonymous()
        return cls(ident, sentence)

    @classmethod
    def from_lean(cls, s: str, context=None):
        match = re.search(r"have (\w+) : (.+) := by obvious_ineq", s)
        if not match:
            return None
        sentence = from_lean(match[2], cls, context)
        if not sentence:
            return None
        return cls(match[1], sentence)


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
        match = re.search(r"Let \$(\w+)\$", s)
        if not match:
            return None
        if not isinstance(context.current_goal, ForAllNatIneqThen):
            return None
        ident = match[1]
        hyp = context.next_anonymous()
        return cls(ident, hyp)

    @classmethod
    def from_lean(cls, s: str, context=None):
        match = re.search(r"intros (\w+) (\w+)", s)
        if not match:
            return None
        if not isinstance(context.current_goal, ForAllNatIneqThen):
            return None
        ident = match[1]
        hyp = match[2]
        return cls(ident, hyp)


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
        match = re.search(r"(.+) by (\w+) with (\w+)", s)
        if not match:
            return None
        sentence = from_natural(match[1], cls, context)
        if not sentence:
            return None
        ident = context.next_anonymous()
        return cls(ident, sentence, match[2], match[3])

    @classmethod
    def from_lean(cls, s: str, context=None):
        match = re.search(r"have (\w+) : (.+) := (\w+) (\w+)", s)
        if not match:
            return None
        sentence = from_lean(match[2], cls, context)
        if not sentence:
            return None
        return cls(match[1], sentence, match[3], match[4])


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
        match = re.search(r"Let's choose (\w+) in (\w+)", s)
        if not match:
            return None
        ident = context.next_anonymous()
        return cls(ident, match[2], match[1])

    @classmethod
    def from_lean(cls, s: str, context=None):
        match = re.search(r"have (\w+) := (\w+) (\w+)", s)
        if not match:
            return None
        return cls(match[1], match[2], match[3])


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
        match = re.search(
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
        match = re.search(r"rw abs_sub_lt_iff at((?: (?:\w+|⊢))+)", s)
        if not match:
            return None
        idents = match[1].split(" ")
        idents = idents[1:]
        for i in range(len(idents)):
            if idents[i] == "⊢":
                idents[i] = "goal"
        return cls(idents)


class Cases(Tactic):
    def __init__(self, ident):
        self.ident = ident

    def to_lean(self) -> str:
        return "cases " + self.ident

    def to_natural(self, in_math=False) -> str:
        return "Let's separate " + self.ident

    @classmethod
    def from_natural(cls, s: str, context=None, in_math=False):
        match = re.search(r"Let's separate (\w+)", s)
        if not match:
            return None
        return cls(match[1])

    @classmethod
    def from_lean(cls, s: str, context=None):
        match = re.search(r"cases (\w+)", s)
        if not match:
            return None
        return cls(match[1])
