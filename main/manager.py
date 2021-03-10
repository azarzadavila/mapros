from main.context import Context
from main.sentences import RealValuedSequences, RealDeclaration, SequenceLimit, ForAll


class Manager:
    def __init__(self):
        self.context = Context()
        self.hypotheses = []

    def add_hypothesis(self, nat):
        match = RealValuedSequences.from_natural(nat, self.context)
        if not match:
            match = RealDeclaration.from_natural(nat, self.context)
        if not match:
            match = SequenceLimit.from_natural(nat, self.context)
        if not match:
            match = ForAll.from_natural(nat, self.context)
        if not match:
            raise ValueError("Unrecognized hypothesis")
        if not (
            isinstance(match, RealValuedSequences) or isinstance(match, RealDeclaration)
        ):
            self.hypotheses.append(match)
