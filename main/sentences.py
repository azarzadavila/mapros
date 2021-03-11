from abc import ABC
import re

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


def from_natural(s: str, cls, context=None, in_math=False):
    if cls == ForAll:
        match = Inequality.from_natural(s, context, in_math)
        return match
    if cls == Inequality:
        match = AbsoluteDiff.from_natural(s, context, in_math)
        if not match:
            match = ApplySequence.from_natural(s, context, in_math)
        if not match:
            match = IdentifierEpsilon.from_natural(s, context, in_math)
        if not match:
            match = Identifier.from_natural(s, context, in_math)
        return match
    if cls == AbsoluteDiff:
        match = ApplySequence.from_natural(s, context, in_math)
        if not match:
            match = Identifier.from_natural(s, context, in_math)
        return match
    raise NotImplementedError


def from_lean(s: str, cls, context=None):
    if cls == ForAll:
        match = Inequality.from_lean(s)
        return match
    if cls == Inequality:
        match = AbsoluteDiff.from_lean(s, context)
        if not match:
            match = ApplySequence.from_lean(s, context)
        if not match:
            match = IdentifierEpsilon.from_lean(s, context)
        if not match:
            match = Identifier.from_lean(s)
        return match
    if cls == AbsoluteDiff:
        match = ApplySequence.from_lean(s, context)
        if not match:
            match = Identifier.from_lean(s, context)
        return match
    raise NotImplementedError


class Sentence(Language, ABC):
    pass


class IdentifierEpsilon(Language):
    def to_lean(self) -> str:
        return "ε"

    def to_natural(self, in_math=False) -> str:
        return r"\epsilon"

    @classmethod
    def from_natural(cls, s: str, context=None, in_math=False):
        match = re.search(r"\\epsilon", s)
        if not match:
            return None
        return cls()

    @classmethod
    def from_lean(cls, s: str, context=None):
        match = re.search(r"ε", s)
        if not match:
            return None
        return cls()


class Identifier(Language):
    def __init__(self, ident):
        self.ident = ident

    def to_lean(self) -> str:
        return self.ident

    def to_natural(self, in_math=False) -> str:
        return self.ident

    @classmethod
    def from_natural(cls, s: str, context=None, in_math=False):
        match = re.search(r"(\w+)", s)
        if not match:
            return None
        return cls(match[1])

    @classmethod
    def from_lean(cls, s: str, context=None):
        match = re.search(r"(\w+)", s)
        if not match:
            return None
        return cls(match[1])


class RealValuedSequences(Sentence):
    def __init__(self, identifiers):
        self.identifiers = identifiers

    def to_lean(self) -> str:
        s = ""
        for ident in self.identifiers:
            s += ident + " "
        s += ": ℕ → ℝ"
        return s

    def to_natural(self, in_math=False) -> str:
        s = ""
        if not in_math:
            s += "$"
        for ident in self.identifiers[:-1]:
            s += ident + "_n, "
        s += self.identifiers[-1] + "_n"
        s += "$ "
        s += "are real-valued sequences"
        if in_math:
            s += " $"
        return s

    @classmethod
    def from_natural(cls, s: str, context=None, in_math=False):
        if not in_math:
            match = re.search(r"\$(\w+_n, )*(\w+_n)\$ are real-valued sequences", s)
        else:
            match = re.search(r"(\w+_n, )*(\w+_n)\$ are real-valued sequences \$", s)
        if not match:
            return None
        identifiers = []
        prev = match[0][1 : match.start(match.lastindex)]
        prev = prev.split(", ")
        for ident in prev:
            if ident:
                identifiers.append(ident[:-2])
                context.add(ident[:-2], "sequence")
        identifiers.append(match[match.lastindex][:-2])
        context.add(match[match.lastindex][:-2], "sequence")
        return cls(identifiers)

    @classmethod
    def from_lean(cls, s: str, context=None):
        match = re.search(r"(\w+ )+: ℕ → ℝ", s)
        if not match:
            return None
        identifiers = []
        prev = match[0][: match.end(match.lastindex)]
        prev = prev.split(" ")
        for ident in prev:
            if ident:
                identifiers.append(ident)
                context.add(ident, "sequence")
        return cls(identifiers)


class RealDeclaration(Sentence):
    def __init__(self, ident):
        self.ident = ident

    def to_lean(self) -> str:
        return self.ident + " : ℝ"

    def to_natural(self, in_math=False) -> str:
        s = ""
        if not in_math:
            s += "$"
        s += self.ident + r" \in \mathbb{R}"
        if not in_math:
            s += "$"
        return s

    @classmethod
    def from_natural(cls, s: str, context=None, in_math=False):
        if not in_math:
            match = re.search(r"\$(\w+) \\in \\mathbb\{R\}\$", s)
        else:
            match = re.search(r"(\w+) \\in \\mathbb\{R\}", s)
        if not match:
            return None
        context.add(match[1], "real")
        return cls(match[1])

    @classmethod
    def from_lean(cls, s: str, context=None):
        match = re.search(r"(\w+) : ℝ", s)
        if not match:
            return None
        context.add(match[1], "real")
        return cls(match[1])


class SequenceLimit(Sentence):
    def __init__(self, seq, lim):
        self.seq = seq
        self.lim = lim

    def to_lean(self) -> str:
        return "is_limit " + self.seq + " " + self.lim

    def to_natural(self, in_math=False) -> str:
        s = ""
        if not in_math:
            s += "$"
        s += self.seq + "_n " + r"\rightarrow " + self.lim
        if not in_math:
            s += "$"
        return s

    @classmethod
    def from_natural(cls, s: str, context=None, in_math=False):
        if not in_math:
            match = re.search(r"\$(\w+)_n \\rightarrow (\w+)\$", s)
        else:
            match = re.search(r"(\w+)_n \\rightarrow (\w+)", s)
        if not match:
            return None
        return cls(match[1], match[2])

    @classmethod
    def from_lean(cls, s: str, context=None):
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
        return (
            self.ident1.to_lean()
            + " "
            + MAP_INEQ_LEAN[self.ineq_type]
            + " "
            + self.ident2.to_lean()
        )

    def to_natural(self, in_math=False) -> str:
        s = ""
        if not in_math:
            s += "$"
        s += (
            self.ident1.to_natural(True)
            + " "
            + MAP_INEQ_NAT[self.ineq_type]
            + " "
            + self.ident2.to_natural(True)
        )
        if not in_math:
            s += "$"
        return s

    @classmethod
    def from_natural(cls, s: str, context=None, in_math=False):
        ineq_symbols = r">|\\geq|<|\\leq"
        if not in_math:
            match = re.search(r"\$(.+) (" + ineq_symbols + r") (.+)\$", s)
        else:
            match = re.search(r"(.+) (" + ineq_symbols + r") (.+)", s)
        if not match:
            return None
        ident1 = from_natural(match[1], Inequality, context, True)
        if not ident1:
            return None
        ident2 = from_natural(match[3], Inequality, context, True)
        if not ident2:
            return None
        return cls(ident1, MAP_NAT_INEQ[match[2]], ident2)

    @classmethod
    def from_lean(cls, s: str, context=None):
        ineq_symbols = "|".join(MAP_LEAN_INEQ.keys())
        match = re.search(r"(.+) (" + ineq_symbols + r") (.+)", s)
        if not match:
            return None
        ident1 = from_lean(match[1], Inequality, context)
        if not ident1:
            return None
        ident2 = from_lean(match[3], Inequality, context)
        if not ident2:
            return None
        return cls(ident1, MAP_LEAN_INEQ[match[2]], ident2)


class ApplySequence(Sentence):
    def __init__(self, ident, point):
        self.ident = ident
        self.point = point

    def to_lean(self) -> str:
        s = self.ident + " " + self.point
        return s

    def to_natural(self, in_math=False) -> str:
        s = ""
        if not in_math:
            s += "$"
        s += self.ident + "_" + self.point
        if not in_math:
            s += "$"
        return s

    @classmethod
    def from_natural(cls, s: str, context=None, in_math=False):
        if not in_math:
            match = re.search(r"\$(\w+)_(\w+)\$", s)
        else:
            match = re.search(r"(\w+)_(\w+)", s)
        if not match:
            return None
        ident = match[1]
        point = match[2]
        if context.get(ident):
            if "class" in context.get(ident):
                if "sequence" in context.get(ident)["class"]:
                    return cls(ident, point)
        return None

    @classmethod
    def from_lean(cls, s: str, context=None):
        match = re.search(r"(\w+) (\w+)", s)
        if not match:
            return None
        ident = match[1]
        point = match[2]
        if context.get(ident):
            if "class" in context.get(ident):
                if "sequence" in context.get(ident)["class"]:
                    return cls(ident, point)
        return None


class ForAll(Sentence):
    def __init__(self, ident, sentence: Sentence):
        self.ident = ident
        self.sentence = sentence

    def to_lean(self) -> str:
        return "∀ " + self.ident + ", " + self.sentence.to_lean()

    def to_natural(self, in_math=False) -> str:
        s = ""
        if not in_math:
            s += "$"
        s += r"\forall " + self.ident + " : " + self.sentence.to_natural(True)
        if not in_math:
            s += "$"
        return s

    @classmethod
    def from_natural(cls, s: str, context=None, in_math=False):
        if not in_math:
            match = re.search(r"\$\\forall (\w+) : (.+)\$", s)
        else:
            match = re.search(r"\\forall (\w+) : (.+)", s)
        if not match:
            return None
        sentence = from_natural(match[2], cls, context, True)
        if not sentence:
            return None
        return cls(match[1], sentence)

    @classmethod
    def from_lean(cls, s: str, context=None):
        match = re.search(r"∀ (\w+), (.+)", s)
        if not match:
            return None
        sentence = from_lean(match[2], cls, context)
        if not sentence:
            return None
        return cls(match[1], sentence)


class ForAllNatIneqThen(Sentence):
    def __init__(self, ident, ineq, sentence):
        self.ident = ident
        self.ineq = ineq
        self.sentence = sentence  # TODO

    def to_lean(self) -> str:
        return (
            "∀ (" + self.ident + " : ℕ), " + self.ineq.to_lean() + " → " + self.sentence
        )

    def to_natural(self, in_math=False) -> str:
        return (
            r"$\forall "
            + self.ident
            + r" \in \mathbb{N} : "
            + self.ineq.to_natural(True)
            + " \Rightarrow "
            + self.sentence
            + "$"
        )

    @classmethod
    def from_natural(cls, s: str, context=None, in_math=False):
        match = re.search(
            r"\$\\forall (\w+) \\in \\mathbb\{N\} : (.+) \\Rightarrow (.+)\$", s
        )
        if not match:
            return None
        ident = match[1]
        ineq = Inequality.from_natural(match[2], context, True)
        if not ineq:
            return None
        sentence = match[3]
        return cls(ident, ineq, sentence)

    @classmethod
    def from_lean(cls, s: str, context=None):
        match = re.search(r"∀ \((\w+) : ℕ\), (.+) → (.+)", s)
        if not match:
            return None
        ident = match[1]
        ineq = Inequality.from_lean(match[2], context)
        if not ineq:
            return None
        sentence = match[3]
        return cls(ident, ineq, sentence)


class AbsoluteDiff(Sentence):
    def __init__(self, sentence1, sentence2):
        self.sentence1 = sentence1
        self.sentence2 = sentence2

    def to_lean(self) -> str:
        return "|" + self.sentence1.to_lean() + " - " + self.sentence2.to_lean() + "|"

    def to_natural(self, in_math=False) -> str:
        s = ""
        if not in_math:
            s += "$"
        s += "|"
        s += self.sentence1.to_natural(True)
        s += " - "
        s += self.sentence2.to_natural(True)
        s += "|"
        if not in_math:
            s += "$"
        return s

    @classmethod
    def from_natural(cls, s: str, context=None, in_math=False):
        if not in_math:
            match = re.search(r"\$\|(.+) - (.+)\|\$", s)
        else:
            match = re.search(r"\|(.+) - (.+)\|", s)
        if not match:
            return None
        sentence1 = from_natural(match[1], cls, context, True)
        if not sentence1:
            return None
        sentence2 = from_natural(match[2], cls, context, True)
        if not sentence2:
            return None
        return cls(sentence1, sentence2)

    @classmethod
    def from_lean(cls, s: str, context=None):
        match = re.search(r"\|(.+) - (.+)\|", s)
        if not match:
            return None
        sentence1 = from_lean(match[1], cls, context)
        if not sentence1:
            return None
        sentence2 = from_lean(match[2], cls, context)
        if not sentence2:
            return None
        return cls(sentence1, sentence2)
