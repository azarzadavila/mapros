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
        return self.hyp.to_html()


class FunctionDeclarationHtml:
    def __init__(self, identifiers, start_domain, end_domain):
        self.identifiers = identifiers
        self.start_domain = start_domain
        self.end_domain = end_domain

    def to_html(self):
        res = ""
        for s in self.identifiers[:-1]:
            res += s
            res += ", "
        res += self.identifiers[-1]
        res += " : " + self.start_domain + " → " + self.end_domain
        return res


class DeclarationHtml:
    def __init__(self, identifiers, domain):
        self.identifiers = identifiers
        self.domain = domain

    def to_html(self):
        res = ""
        for s in self.identifiers[:-1]:
            res += s
            res += ", "
        res += self.identifiers[-1]
        res += " ∈ " + self.domain
        return res


class ExprHtml:
    def __init__(self, expr):
        self.expr = expr

    def to_html(self):
        res = ""
        for s in self.expr:
            if isinstance(s, str):
                res += s
            else:
                res += s.to_html()
        return res


class BasicHtml:
    def __init__(self, s):
        self.s = s

    def to_html(self):
        if isinstance(self.s, str):
            return self.s
        else:
            return self.s.to_html()


class ParExprHtml:
    def __init__(self, expr):
        self.expr = expr

    def to_html(self):
        return "(" + self.expr.to_html() + ")"


class IntervalHtml:
    def __init__(self, inter_type, start, end):
        inter_type_start = inter_type[-2]
        inter_type_end = inter_type[-1]
        self.left = "]" if inter_type_start == "o" else "["
        self.right = "[" if inter_type_end == "o" else "]"
        self.start = start
        self.end = end

    def to_html(self):
        return self.left + self.start.to_html() + ", " + self.end.to_html() + self.right


class DerivHtml:
    def __init__(self, fct, point):
        self.fct = fct
        self.point = point

    def to_html(self):
        return self.fct.to_html() + "'(" + self.point.to_html() + ")"


class ContinuousOnHtml:
    def __init__(self, fct, on):
        self.fct = fct
        self.on = on

    def to_html(self):
        return self.fct.to_html() + " is continuous on " + self.on.to_html()


class DifferentiableOnHtml:
    def __init__(self, im_diff, fct, on):
        self.im_diff = im_diff
        self.fct = fct
        self.on = on

    def to_html(self):
        return (
            self.fct.to_html()
            + " is differentiable on "
            + self.on.to_html()
            + " to "
            + self.im_diff.to_html()
        )


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
