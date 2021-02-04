class Import:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "import " + self.name


class Open:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "open " + self.name


class Theorem:
    def __init__(self, name, hypotheses, statement):
        self.name = name
        self.hypotheses = hypotheses
        self.statement = statement

    def __str__(self):
        s = "theorem " + self.name + "\n"
        for hyp in self.hypotheses:
            s += "(" + str(hyp) + ")\n"
        s += ":\n" + self.statement
        return s


class LeanProof:
    def __init__(self, start=None, theorem=None, proof=None):
        self.start = start
        self.theorem = theorem
        self.proof = proof

    def __str__(self):
        res = ""
        for s in self.start:
            res += str(s) + "\n"
        res += str(self.theorem)
        res += "\n:="
        res += str(self.proof)
        return res
