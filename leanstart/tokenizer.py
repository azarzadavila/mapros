from lark import Lark

grammar = r"""
    start: _SEP* token (_SEP+ token)* _SEP*
    token: symbol | command | other
    symbol: /have/
    command: /import|open|theorem/
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
