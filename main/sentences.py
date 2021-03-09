from abc import ABC
import re

from main.context import Context
from main.language import Language

from enum import Enum, auto


class InequalityType(Enum):
    GT = auto()
    GE = auto()
    LT = auto()
    LE = auto()


MAP_INEQ_LEAN = {
    InequalityType.GT: ">",
    InequalityType.GE: "≥",
    InequalityType.LT: "<",
    InequalityType.LE: "≤",
}

MAP_LEAN_INEQ = {
    ">": InequalityType.GT,
    "≥": InequalityType.GE,
    "<": InequalityType.LT,
    "≤": InequalityType.LE,
}

MAP_INEQ_NAT = {
    InequalityType.GT: ">",
    InequalityType.GE: r"\geq",
    InequalityType.LT: "<",
    InequalityType.LE: r"\leq",
}

MAP_NAT_INEQ = {
    ">": InequalityType.GT,
    r"\geq": InequalityType.GE,
    "<": InequalityType.LT,
    r"\leq": InequalityType.LE,
}


class Sentence(Language, ABC):
    pass


class RealValuedSequences(Sentence):
    def __init__(self, identifiers):
        self.identifiers = identifiers

    def to_lean(self) -> str:
        s = ""
        for ident in self.identifiers:
            s += ident + " "
        s += ": ℕ → ℝ"
        return s

    def to_natural(self) -> str:
        s = "$"
        for ident in self.identifiers[:-1]:
            s += ident + "_n, "
        s += self.identifiers[-1] + "_n"
        s += "$ "
        s += "are real-valued sequences"
        return s

    @classmethod
    def from_natural(cls, s: str, context: Context = None):
        match = re.search(r"\$(\w+_n, )*(\w+_n)\$ are real-valued sequences", s)
        if not match:
            return None
        identifiers = []
        prev = match[0][1 : match.start(match.lastindex)]
        prev = prev.split(", ")
        for ident in prev:
            if ident:
                identifiers.append(ident[:-2])
        identifiers.append(match[match.lastindex][:-2])
        return cls(identifiers)

    @classmethod
    def from_lean(cls, s: str, context: Context = None):
        match = re.search(r"(\w+ )+: ℕ → ℝ", s)
        if not match:
            return None
        identifiers = []
        prev = match[0][: match.end(match.lastindex)]
        prev = prev.split(" ")
        for ident in prev:
            if ident:
                identifiers.append(ident)
        return cls(identifiers)


class RealDeclaration(Sentence):
    def __init__(self, ident):
        self.ident = ident

    def to_lean(self) -> str:
        return self.ident + " : ℝ"

    def to_natural(self) -> str:
        return "$" + self.ident + r" \in \mathbb{R}$"

    @classmethod
    def from_natural(cls, s: str, context: Context = None):
        match = re.search(r"\$(\w+) \\in \\mathbb\{R\}\$", s)
        if not match:
            return None
        return cls(match[1])

    @classmethod
    def from_lean(cls, s: str, context: Context = None):
        match = re.search(r"(\w+) : ℝ", s)
        if not match:
            return None
        return cls(match[1])


class SequenceLimit(Sentence):
    def __init__(self, seq, lim):
        self.seq = seq
        self.lim = lim

    def to_lean(self) -> str:
        return "is_limit " + self.seq + " " + self.lim

    def to_natural(self) -> str:
        return "$" + self.seq + "_n " + r"\rightarrow " + self.lim + "$"

    @classmethod
    def from_natural(cls, s: str, context: Context = None):
        match = re.search(r"\$(\w+)_n \\rightarrow (\w+)\$", s)
        if not match:
            return None
        return cls(match[1], match[2])

    @classmethod
    def from_lean(cls, s: str, context: Context = None):
        match = re.search(r"is_limit (\w+) (\w+)", s)
        if not match:
            return None
        return cls(match[1], match[2])


class Inequality(Sentence):
    def __init__(self, ident1, ineq_type, ident2):
        self.ident1 = ident1
        self.ineq_type = ineq_type
        self.ident2 = ident2

    def to_lean(self) -> str:
        return self.ident1 + " " + MAP_INEQ_LEAN[self.ineq_type] + " " + self.ident2

    def to_natural(self) -> str:
        return (
            "$"
            + self.ident1
            + " "
            + MAP_INEQ_NAT[self.ineq_type]
            + " "
            + self.ident2
            + "$"
        )

    @classmethod
    def from_natural(cls, s: str, context: Context = None):
        ineq_symbols = r">|\\geq|<|\\leq"
        match = re.search(r"\$(\w+) (" + ineq_symbols + r") (\w+)\$", s)
        if not match:
            return None
        return cls(match[1], MAP_NAT_INEQ[match[2]], match[3])

    @classmethod
    def from_lean(cls, s: str, context: Context = None):
        ineq_symbols = "|".join(MAP_LEAN_INEQ.keys())
        match = re.search(r"(\w+) (" + ineq_symbols + r") (\w+)", s)
        if not match:
            return None
        return cls(match[1], MAP_LEAN_INEQ[match[2]], match[3])


class ForAll(Sentence):
    def __init__(self, ident, sentence: Sentence):
        self.ident = ident
        self.sentence = sentence

    def to_lean(self) -> str:
        return "∀ " + self.ident + " : " + self.sentence.to_lean()

    def to_natural(self) -> str:
        return r"$\forall " + self.ident + " : $" + self.sentence.to_natural()

    @classmethod
    def from_natural(cls, s: str, context: Context):
        match = re.match(r"\$\\forall (\w+) : \$(.+)", s)
        if not match:
            return None
        sentence = context.from_natural(match[2], cls)
        if not sentence:
            return None
        return cls(match[1], sentence)

    @classmethod
    def from_lean(cls, s: str, context: Context):
        match = re.match(r"∀ (\w+) : (.+)", s)
        if not match:
            return None
        sentence = context.from_lean(match[2], cls)
        if not sentence:
            return None
        return cls(match[1], sentence)
