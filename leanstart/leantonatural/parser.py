from lark import Lark, Transformer

import leanstart.leantonatural.leanhtml as lhtml

grammar = r"""
    start: _SEP* atomic_start (_SEP+ atomic_start)* _SEP+ theorem_proof
    atomic_start: import_rule | open
    import_rule: "import" _SEP+ IMPORT
    IMPORT: /\S+/
    open: "open" _SEP+ OPEN
    OPEN: /\S+/
    theorem_proof: "theorem" _SEP+ NAME _SEP* hypotheses _SEP* ":" _SEP* statements _SEP* ":=" _SEP* proof _SEP*
    hypotheses: (_SEP* hypothesis)*
    hypothesis: "(" _content* ")"
    !_content: NOT_PAR | "(" _content* ")"
    statements: STATEMENT (_SEP* "," _SEP* STATEMENT)*
    proof: "begin" (_SEP+ proof_content)+ _SEP+ "end"
    proof_content: proof | PROOF_CONTENT (_SEP+ PROOF_CONTENT)*
    PROOF_CONTENT: /(?!(begin|end)\b)\S+/i
    NOT_PAR: /[^\(\)]+/
    STATEMENT: /:[^=]+|[^,:]+/
    NAME: /\S+/
    _SEP: /\s/
"""

parser = Lark(grammar)


class LeanTransformer(Transformer):
    def start(self, node):
        start_html = node[:-1]
        theorem_proof_html = node[-1]
        return lhtml.LeanHtml(start_html, theorem_proof_html)

    def atomic_start(self, node):
        (node,) = node
        return node

    def import_rule(self, node):
        (node,) = node
        return node

    def IMPORT(self, terminal):
        return lhtml.ImportHtml(terminal)

    def open(self, node):
        (node,) = node
        return node

    def OPEN(self, terminal):
        return lhtml.OpenHtml(terminal)

    def theorem_proof(self, node):
        name = node[0]
        hypotheses = node[1]
        statements = node[2]
        proof = node[3]
        return lhtml.TheoremProofHtml(name, hypotheses, statements, proof)


def transform(s):
    tree = parser.parse(s)
    return LeanTransformer().transform(tree)
