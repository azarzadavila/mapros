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
    raise NotImplementedError


def from_lean(s: str, cls, context=None):
    if cls == LetGoalLimit:
        match = IdentifierEpsilon.from_lean(s)
        if not match:
            match = Identifier.from_lean(s, context)
        return match
    raise NotImplementedError


class Tactic(Language, ABC):
    pass


class LetGoalLimit(Language):
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
        return cls(ident, hyp)
