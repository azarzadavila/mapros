from sets.invoker import Invoker
from sets.parser import parse
from sets.proof import Proof

if __name__ == "__main__":
    invoker = Invoker()
    proof = Proof()
    running = True
    while running:
        to_parse = input("\n")
        to_parse.strip()
        if to_parse == "":
            running = False
        else:
            invoker.store_command(parse(to_parse, proof))
    invoker.execute_commands()
