# import leanstart.leantonatural.parser as parser
import parser


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


parser_test()
