from formal.grammar import IDSentence
from formal.rules_inference import MAP_RULE, StatementProof

# TODO internal current node
# TODO first element without proof
# TODO all elements without proof
# TODO external elements


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
    if len(position) == common:
        return False
    if len(reference) == common and len(position) == len(reference) + 1:
        return True
    if len(position) == common + 1:
        return position[-1] < reference[common]
    return False


def change_add_tuple(position, statement_proof):
    """
    Consider a shift to the positions in sentences at statement_proof from position
    For example, if position is (2,3) and statement proof has a sentence (2,3,1) then that sentence will be changed to
    (2,4,1)
    :param position: tuple
    :param statement_proof: StatementProof instance
    """
    if statement_proof is not None:
        for i in range(len(statement_proof.sentences)):
            if isinstance(statement_proof.sentences[i], tuple):
                if statement_proof.sentences[i][: len(position)] == position:
                    statement_proof.sentences[i] = (
                        position[:-1]
                        + (position[-1] + 1,)
                        + statement_proof.sentences[len(position) :]
                    )


class Proof:
    def __init__(self, statement, children, statement_proof):
        self.statement = statement
        self.children = children
        self.statement_proof = statement_proof

    def get_proof(self, position):
        """
        Gets the proof at the given position
        :param position: tuple indicating the position
        :return: proof at the given position
        """
        current = self
        for i in position:
            if i < len(current.children):
                current = current.children[i]
            else:
                raise ValueError("Incorrect position : {}".format(position))
        return current

    def add_statement_child(self, statement, position):
        """
        Adds a new statement, by creating a child proof to the parent at the given position
        :param statement:
        :param position: tuple indicating the position of the parent
        """
        parent = self.get_proof(position)
        parent.children.append(Proof(statement, [], None))

    def change_position_child(self, position):
        """
        Changes the StatementProof that need change due to the addition of a new proof at position.
        This method is recursive and will be applied to each child
        :param position: tuple
        """
        change_add_tuple(position, self.statement_proof)
        for child in self.children:
            child.change_position_child(position)

    def change_position_parent(self, position):
        """
        Changes the StatementProof that need change due to the addition of a new proof at position.
        This method should be called from the parent from which a new child proof was added
        :param position: tuple
        """
        change_add_tuple(position, self.statement_proof)
        for child in self.children[position[-1] + 1 : len(self.children)]:
            child.change_position_child(position)

    def add_statement(self, statement, position):
        """
        Adds a new statement at the given position if such parent exists
        :param statement:
        :param position: tuple indicating the position of the proof
        """
        parent = self.get_proof(position[:-1])
        if position[-1] > len(parent.children):
            raise ValueError("Incorrect position to add a proof : {}".format(position))
        parent.children.insert(position[-1], Proof(statement, [], None))
        parent.change_position(position)

    def add_statement_rule(self, position, rule, *args):
        """
        Adds a new proof at the given position if such parent exists by using an inference rule
        :param position: tuple indicating the position of the proof
        :param rule: string indicating the inference rule to use
        :param args: sentences to use for the rule, either as external sentences,
                     tuple indicating a position in this proof or directly a sentence
        """
        parent = self.get_proof(position[:-1])
        if position[-1] > len(parent.children):
            raise ValueError("Incorrect position to add a proof : {}".format(position))
        args = list(args)
        rule_fct = MAP_RULE[rule]
        statement = rule_fct(*map(self.get_statement, args))
        statement_proof = StatementProof(rule, args)
        parent.children.insert(position[-1], Proof(statement, [], statement_proof))
        parent.change_position(position)

    def edit_statement(self, statement, position):
        """
        Edit a statement
        :param statement: new statement to replace the previous one
        :param position: tuple indicating the position of the proof
        """
        proof = self.get_proof(position)
        proof.statement = statement

    def edit_statement_proof(self, statement_proof, position):
        """
        Edit the statement proof of a proof
        :param statement_proof: StatementProof instance
        :param position: tuple indicating the position of the proof
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
        if isinstance(arg, IDSentence):
            # TODO retrieve the sentence from an IDSentence
            pass
        return arg

    def add_statement_with_rule_child(self, position, rule, *args):
        """
        Adds a new proof as a child of the given position by using an inference rule
        :param position: parent position
        :param rule: string indicating the inference rule to use
        :param args: sentences to use for the rule, either as external sentences,
                     tuple indicating a position in this proof or directly a sentence
        """
        parent = self.get_proof(position)
        args = list(args)
        rule_fct = MAP_RULE[rule]
        statement = rule_fct(*map(self.get_statement, args))
        statement_proof = StatementProof(rule, args)
        parent.children.append(Proof(statement, [], statement_proof))

    def check_proof(self, position):
        """
        Checks if the proof at the given position is correct
        :param position: tuple indicating the position at which to check the proof
        :return: true if the proof is correct, false otherwise
        """
        proof = self.get_proof(position)
        if proof.statement_proof is None:
            return False
        if proof.statement_proof.rule == "premise":
            return True
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
