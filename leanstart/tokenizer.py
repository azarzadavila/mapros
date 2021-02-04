from lark import Lark

grammar = r"""
    start: _SEP* token (_SEP+ token)* _SEP*
    token: symbol | command | ident | other
    symbol: /have|intro|use/
    command: /import|open|theorem/
    ident: _atomic_ident
    _atomic_ident: _atomic_ident_start _atomic_ident_rest*
    _atomic_ident_start: LETTER_LIKE
    LETTER_LIKE: /[a-zA-Z]/
    _atomic_ident_rest: _atomic_ident_start | /[0-9]/
    //other should actually tell not to match symbols and commands
    other: /\S+/
    //token: symbol | command | ident | string | char | numeral | decimal | quoted_symbol | doc_comment | mod_doc_comment
    //      | field_notation
    _SEP: /\s/
"""

parser = Lark(grammar)
file = open("examples/ex1.lean")
s = file.read()
print(parser.parse(s).pretty())
