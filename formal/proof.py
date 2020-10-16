from formal.rules_inference import MAP_RULE, StatementProof

# TODO edit proofs : for example insert a new proof child before a child without deleting the previous one
# TODO internal current node
# TODO first element without proof
# TODO all elements without proof


def print_tab(tab):
    for i in range(tab):
        print("\t", end="")


def check_scope(position, reference):
    """
    Checks if a proof at reference can use the result from position
    :param position: tuple
    :param reference: tuple
    :return: True if reference an use the result from position. False otherwise
    """
    common = 0
    while (
        common < len(position)
        and common < len(reference)
        and position[common] == reference[common]
    ):
        common += 1
    if len(position) == common + 1:
        return position[-1] < reference[common]
    if len(reference) == common + 1 and len(position) == len(reference) + 1:
        return True
    return False


class Proof:
    def __init__(
        self, statement, children, statement_proof, parent=None, parent_id=None
    ):
        self.statement = statement
        self.children = children
        self.statement_proof = statement_proof
        self.parent = parent
        self.parent_id = parent_id

    def get_proof(self, position):
        """
        Gets the proof at the given position
        :param position: tuple indicating the position
        :return: proof at the given position or None if the previous position exists
        """
        current = self
        for i in position:
            if i < len(current.children):
                current = current.children[i]
            elif i == len(current.children):
                return None
            else:
                raise ValueError("Incorrect position : {}".format(position))
        return current

    def add_statement(self, statement, position):
        """
        Adds a new statement or modifies it at the given position
        :param statement: object that passes check_sentence
        :param position: tuple indicating the position at which to add the statement
        """
        proof = self.get_proof(position)
        if proof is None:
            parent = self.get_proof(position[:-1])
            proof = Proof(statement, [], None)
            parent.children.append(proof)
        else:
            proof.statement = statement

    def add_statement_proof(self, statement_proof, position):
        """
        Adds a new statement proof at the given position
        :param statement_proof: StatementProof
        :param position: tuple indicating the position at which to add the statement proof
        """
        proof = self.get_proof(position)
        proof.statement_proof = statement_proof

    def get_statement(self, arg):
        """
        Returns the statement associated with arg
        :param arg: either something that passes check_sentence or a tuple indicating a position
        :return: statement
        """
        if isinstance(arg, tuple):
            proof = self.get_proof(arg)
            return proof.statement
        return arg

    def add_statement_with_rule(self, position, rule, *args):
        """
        Adds a new proof at the given position by using an inference rule
        :param position: tuple indicating the position at which to add the proof
        :param rule: inference rule
        :param args: statements to pass to the inference rule
        """
        proof = self.get_proof(position)
        args = list(args)
        rule_fct = MAP_RULE[rule]
        statement = rule_fct(*map(self.get_statement, args))
        statement_proof = StatementProof(rule, args)
        if proof is None:
            parent = self.get_proof(position[:-1])
            proof = Proof(statement, [], statement_proof)
            parent.children.append(proof)
        else:
            proof.statement = statement
            proof.statement_proof = statement_proof

    def check_proof(self, position):
        """
        Checks if the proof at the given position is correct
        :param position: tuple indicating the position at which to check the proof
        :return: true if the proof is correct, false otherwise
        """
        proof = self.get_proof(position)
        if proof.statement_proof is None:
            return False
        rule_fct = MAP_RULE[proof.statement_proof.rule]
        sentences = proof.statement_proof.sentences
        for sentence in sentences:
            if isinstance(sentence, tuple):
                if not check_scope(sentence, position):
                    return False
        statement = rule_fct(*map(self.get_statement, sentences))
        if not statement == proof.statement:
            return False
        for i in range(len(proof.children)):
            if not self.check_proof(position + (i,)):
                return False
        return True

    def print(self, tab=0):
        print_tab(tab)
        if self.parent_id is not None:
            print(self.parent_id, end=" ")
        print(self.statement)
        for child in self.children:
            child.print(tab + 1)
        print_tab(tab)
        print("Proof : ", self.statement_proof)
