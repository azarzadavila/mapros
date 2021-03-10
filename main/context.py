class Context:
    def __init__(self):
        self.identifiers = {}
        self.current_goal = None
        self.c_anonymous = 0

    def get(self, ident):
        return self.identifiers.get(ident)

    def add(self, ident, name):
        if ident not in self.identifiers:
            self.identifiers[ident] = {}
        if "class" not in self.identifiers[ident]:
            self.identifiers[ident]["class"] = set()
        self.identifiers[ident]["class"].add(name)

    def associate(self, ident, hyp):
        if ident not in self.identifiers:
            self.identifiers[ident] = {}
        self.identifiers[ident]["associate"] = hyp

    def next_anonymous(self):
        self.c_anonymous += 1
        return "A{}".format(self.c_anonymous)
