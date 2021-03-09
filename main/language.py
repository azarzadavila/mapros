class Language:
    def to_lean(self) -> str:
        raise NotImplementedError

    def to_natural(self) -> str:
        raise NotImplementedError

    @classmethod
    def from_natural(cls, s: str):
        raise NotImplementedError

    @classmethod
    def from_lean(cls, s: str):
        raise NotImplementedError
