def print_tab(tab):
    for i in range(tab):
        print("\t", end="")


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
        print_tab(tab)
        if self.parent_id is not None:
            print(self.parent_id, end=" ")
        print(self.statement)
        for child in self.children:
            child.print(tab + 1)
        print_tab(tab)
        print("Proof : ", self.statement_proof)
