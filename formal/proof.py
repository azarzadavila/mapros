def print_tab(s, tab):
    for i in range(tab):
        print("\t", end="")
    print(s, end="")


class Proof:
    def __init__(
        self, statement, children, statement_proof, parent=None, parent_id=None
    ):
        self.statement = statement
        self.children = children
        self.statement_proof = statement_proof
        self.parent = parent
        self.parent_id = parent_id

    def print(self, tab=0):
        if self.parent_id is not None:
            print_tab(self.parent_id, tab)
        print(self.statement)
        for child in self.children:
            child.print(tab + 1)
        print("Proof : ", self.statement_proof)
