from abc import ABC
import re

from main.language import Language
from main.sentences import SequenceLimit, IdentifierEpsilon, Identifier


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
        match = re.match(r"Let's choose \$(\w+)\$ such that (\w+) uses \$(\\?\w+)\$", s)
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
        match = re.match(r"cases (\w+) (\w+) (\w+) with (\w+) (\w+)", s)
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
        match = re.match(r"Let \$(\w+) = max\((\w+), (\w+)\)\$", s)
        if not match:
            return None
        return cls(match[1], match[2], match[3])

    @classmethod
    def from_lean(cls, s: str, context=None):
        match = re.match(r"let (\w+) := max (\w+) (\w+)", s)
        if not match:
            return None
        return cls(match[1], match[2], match[3])
