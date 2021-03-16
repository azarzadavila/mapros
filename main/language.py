from typing import List, Type


class Language:
    def to_lean(self) -> str:
        raise NotImplementedError

    def to_natural(self, in_math=False) -> str:
        raise NotImplementedError

    @classmethod
    def from_natural(cls, s: str, context=None, in_math=False):
        raise NotImplementedError

    @classmethod
    def from_lean(cls, s: str, context=None):
        raise NotImplementedError


def from_natural(s, context, languages: List[Type[Language]], in_math=False):
    for lang in languages:
        match = lang.from_natural(s, context, in_math)
        if match:
            return match
    return None


def from_lean(s, context, languages: List[Type[Language]]):
    for lang in languages:
        match = lang.from_lean(s, context)
        if match:
            return match
    return None
