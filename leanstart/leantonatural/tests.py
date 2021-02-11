# import leanstart.leantonatural.parser as parser
import parser
from lean_to_html import lean_to_html


def parser_test():
    s = r"""
    import data.nat.prime

    open nat

    theorem infinitude_of_prime (hello) (here is another)(again)((nani:)a) : exists a, prime p :=
    begin
        p1
        begin
            p2
        end
        p3 p4
    end
    """
    print(parser.parser.parse(s).pretty())


def html_test():
    s = r"""
    import data.nat.prime
    open nat
    theorem infinitude_of_prime (h1 : hyp1) (h2 : hyp2 (inside)) : exists a, prime p :=
    begin
        p1
        begin
            p2
        end
        p3 p4
    end
    """
    lean_to_html(input_string=s, output_file="html_test.html")


parser_test()
html_test()
