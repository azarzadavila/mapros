from abc import ABC
import re
from main.language import Language


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
    def from_natural(cls, s: str):
        match = re.search(r"\$(\w+_n, )*(\w+_n)\$ are real-valued sequences", s)
        if not match:
            return None
        identifiers = []
        prev = match[0][1:match.start(match.lastindex)]
        prev = prev.split(", ")
        for ident in prev:
            if ident:
                identifiers.append(ident[:-2])
        identifiers.append(match[match.lastindex][:-2])
        return cls(identifiers)

    @classmethod
    def from_lean(cls, s: str):
        match = re.search(r"(\w+ )+: ℕ → ℝ", s)
        if not match:
            return None
        identifiers = []
        prev = match[0][:match.end(match.lastindex)]
        prev = prev.split(" ")
        for ident in prev:
            if ident:
                identifiers.append(ident)
        return cls(identifiers)
