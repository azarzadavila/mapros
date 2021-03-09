from main.sentences import Inequality, ForAll


class Context:
    def from_natural(self, s: str, cls):
        if cls == ForAll:
            match = Inequality.from_natural(s)
            return match
        raise NotImplementedError

    def from_lean(self, s: str, cls):
        if cls == ForAll:
            match = Inequality.from_lean(s)
            return match
        raise NotImplementedError
