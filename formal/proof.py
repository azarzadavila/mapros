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

    def add_statement(self, statement, position):
        """
        Adds a new statement at the given position
        :param statement: object that passes check_sentence
        :param position: tuple indicating the position at which to add the statement
        """
        # TODO
        pass

    def add_statement_proof(self, statement_proof, position):
        """
        Adds a new statement proof at the given position
        :param statement_proof: StatementProof
        :param position: tuple indicating the position at which to add the statement proof
        """
        # TODO
        pass

    def add_statement_with_rule(self, position, rule, *args):
        """
        Adds a new proof at the given position by using an inference rule
        :param position: tuple indicating the position at which to add the proof
        :param rule: inference rule
        :param args: statements to pass to the inference rule
        """
        # TODO
        pass

    def check_proof(self, position):
        """
        Checks if the proof at the given position is correct
        :param position: tuple indicating the position at which to check the proof
        :return: true if the proof is correct, false otherwise
        """
        # TODO
        pass

    def print(self, tab=0):
        print_tab(tab)
        if self.parent_id is not None:
            print(self.parent_id, end=" ")
        print(self.statement)
        for child in self.children:
            child.print(tab + 1)
        print_tab(tab)
        print("Proof : ", self.statement_proof)
