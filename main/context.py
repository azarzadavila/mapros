class Context:
    def __init__(self):
        self.identifiers = {}

    def get(self, ident):
        return self.identifiers.get(ident)

    def add(self, ident, name):
        if ident not in self.identifiers:
            self.identifiers[ident] = set()
        self.identifiers[ident].add(name)
