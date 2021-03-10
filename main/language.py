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
