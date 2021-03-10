class Context:
    def __init__(self):
        self.identifiers = {}
        self.current_goal = None
        self.c_anonymous = 0

    def get(self, ident):
        return self.identifiers.get(ident)

    def add(self, ident, name):
        if ident not in self.identifiers:
            self.identifiers[ident] = set()
        self.identifiers[ident].add(name)

    def next_anonymous(self):
        self.c_anonymous += 1
        return "A{}".format(self.c_anonymous)
