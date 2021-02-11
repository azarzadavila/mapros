class LeanHtml:
    def __init__(self, start, theorem_proof):
        """

        :param start: List containing the open/import before the proof
        :param theorem_proof: proof
        """
        self.start = start
        self.theorem_proof = theorem_proof

    def to_html(self):
        res = "<h1>Starting instructions</h1>\n"
        res += "<ul>\n"
        for s in self.start:
            res += "<li>" + s.to_html() + "</li>\n"
        res += "</ul>\n"
        res += self.theorem_proof.to_html()
        return res


class ImportHtml:
    def __init__(self, package_name):
        self.package_name = package_name

    def to_html(self):
        return "import " + self.package_name


class OpenHtml:
    def __init__(self, package_name):
        self.package_name = package_name

    def to_html(self):
        return "open " + self.package_name


class TheoremProofHtml:
    def __init__(self, name, hypotheses, statements, proof):
        self.name = name
        self.hypotheses = hypotheses
        self.statements = statements
        self.proof = proof

    def to_html(self):
        res = "<h1>Theorem " + self.name + ":</h1>\n"
        res += "Let:\n<br>\n"
        res += "<ul>"
        for s in self.hypotheses:
            res += "<li>" + s.to_html() + "</li>\n"
        res += "</ul>\n"
        res += "Then,\n<br>\n"
        for s in self.statements:
            res += "<li>" + s.to_html() + "</li>\n"
        res += "<h2> Proof:</h2>\n"
        res += self.proof.to_html()
        return res


class HypothesisHtml:
    def __init__(self, hyp):
        self.hyp = hyp

    def to_html(self):
        return self.hyp


class StatementHtml:
    def __init__(self, stmt):
        self.stmt = stmt

    def to_html(self):
        return self.stmt


class ProofHtml:
    def __init__(self, proof_content):
        self.proof_content = proof_content

    def to_html(self):
        res = "<ol>\n"
        for content in self.proof_content:
            res += "<li>"
            if isinstance(content, ProofHtml):
                res += "\n<br>\n"
                res += content.to_html()
                res += "\n"
            else:
                res += content
            res += "</li>"
        res += "</ol>"
        return res
