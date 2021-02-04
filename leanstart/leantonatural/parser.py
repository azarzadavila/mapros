from lark import Lark

grammar = r"""
    start: _SEP* atomic_start (_SEP+ atomic_start)* _SEP+ theorem_proof
    atomic_start: import | open
    import: "import" _SEP+ IMPORT
    IMPORT: /\S+/
    open: "open" _SEP+ OPEN
    OPEN: /\S+/
    theorem_proof: "theorem" _SEP+ NAME _SEP* hypotheses _SEP* ":" _SEP* statements _SEP* ":=" _SEP*
    hypotheses: (_SEP* hypothesis)*
    hypothesis: "(" _content* ")"
    !_content: NOT_PAR | "(" _content* ")"
    statements: STATEMENT (_SEP* "," _SEP* STATEMENT)*
    NOT_PAR: /[^\(\)]+/
    STATEMENT: /:[^=]+|[^,:]+/
    NAME: /\S+/
    _SEP: /\s/
"""

parser = Lark(grammar)
s = r"""
import data.nat.prime

open nat

theorem infinitude_of_prime (hello) (here is another)(again)((nani:)a) : exists a, prime p :=
"""
print(parser.parse(s).pretty())
