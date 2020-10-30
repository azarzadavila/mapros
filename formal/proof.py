from formal.rules_inference import MAP_RULE, SentenceProof

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


def change_add_tuple(position, sentence_proof):
    """
    Consider a shift to the positions in proofs at sentence_proof from position
    For example, if position is (2,3) and sentence proof has a proof (2,3,1) then that sentence will be changed to
    (2,4,1)
    :param position: tuple
    :param sentence_proof: SentenceProof instance
    """
    if sentence_proof is not None:
        for i in range(len(sentence_proof.proofs)):
            if isinstance(sentence_proof.proofs[i], tuple):
                if sentence_proof.proofs[i][: len(position)] == position:
                    sentence_proof.proofs[i] = (
                        position[:-1]
                        + (position[-1] + 1,)
                        + sentence_proof.proofs[len(position) :]
                    )


class Proof:
    def __init__(self, sentence, children, sentence_proof):
        self.sentence = sentence
        self.children = children
        self.sentence_proof = sentence_proof

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

    def add_sentence_child(self, sentence, position):
        """
        Adds a new sentence, by creating a child proof to the parent at the given position
        :param sentence:
        :param position: tuple indicating the position of the parent
        """
        parent = self.get_proof(position)
        parent.children.append(Proof(sentence, [], None))

    def change_position_child(self, position):
        """
        Changes the SentenceProof that need change due to the addition of a new proof at position.
        This method is recursive and will be applied to each child
        :param position: tuple
        """
        change_add_tuple(position, self.sentence_proof)
        for child in self.children:
            child.change_position_child(position)

    def change_position_parent(self, position):
        """
        Changes the SentenceProof that need change due to the addition of a new proof at position.
        This method should be called from the parent from which a new child proof was added
        :param position: tuple
        """
        change_add_tuple(position, self.sentence_proof)
        for child in self.children[position[-1] + 1 : len(self.children)]:
            child.change_position_child(position)

    def add_sentence(self, sentence, position):
        """
        Adds a new sentence at the given position if such parent exists
        :param sentence:
        :param position: tuple indicating the position of the proof
        """
        parent = self.get_proof(position[:-1])
        if position[-1] > len(parent.children):
            raise ValueError("Incorrect position to add a proof : {}".format(position))
        parent.children.insert(position[-1], Proof(sentence, [], None))
        parent.change_position_child(position)

    def from_existential_instantiation(self, position, var):
        # TODO
        pass

    def is_free_in_premises(self, position, var):
        # TODO
        pass

    def exists(self, position, var):
        # TODO
        pass

    def apply_rule(self, position, rule, proofs, args):
        """
        Applies the given rule if it had to be considered to add a proof at position
        :param position:
        :param rule:
        :param proofs:
        :param args:
        :return: the generated sentence or None if the could not be applied
        """
        try:
            parent = self.get_proof(position[:-1])
            if position[-1] > len(parent.children):
                raise ValueError(
                    "incorrect position to apply a rule : {}".format(position)
                )
            proofs = list(proofs)
            for proof in proofs:
                if isinstance(proof, tuple):
                    if not check_scope(proof, position):
                        raise ValueError(
                            "incorrect scope : {} in {}".format(proof, position)
                        )
            if rule == "premise":
                return True
            elif rule == "hypothesis":
                return position[-1] == 0
            elif rule == "reductio_ad_absurdum":
                hypothesis = self.get_proof(proofs[0])
                if not hypothesis.sentence_proof == "hypothesis":
                    raise ValueError("sentence proof is not an hypothesis")
            elif rule == "deduction_theorem":
                hypothesis = self.get_proof(proofs[0])
                if not hypothesis.sentence_proof == "hypothesis":
                    raise ValueError("sentence proof is not an hypothesis")
            elif rule == "universal_generalization":
                var = args[0]
                if self.from_existential_instantiation(position, var):
                    raise ValueError("variable comes from an existential instantiation")
                if self.is_free_in_premises(position, var):
                    raise ValueError("variable is free in a premise")
            elif rule == "universal_instantiation":
                pass
            elif rule == "existential_generalization":
                pass
            elif rule == "existential_instantiation":
                new_var = args[1]
                if self.exists(position, new_var):
                    raise ValueError("variable already exists")
            rule_fct = MAP_RULE[rule]
            sentence = rule_fct(*map(self.get_sentence, proofs), *args)
            return sentence
        except (ValueError, TypeError):
            return None

    def add_sentence_rule(self, position, rule, proofs, args):
        """
        Adds a new proof at the given position if such parent exists by using an inference rule
        :param position: tuple indicating the position of the proof
        :param rule: string indicating the inference rule to use
        :param proofs: tuple indicating positions for the proofs to use
        :param args: additional args required by the rule (e.g. a variable to rename)
        """
        parent = self.get_proof(position[:-1])
        sentence = self.apply_rule(position, rule, proofs, args)
        if sentence is None:
            raise ValueError("incorrect rule application")
        sentence_proof = SentenceProof(rule, proofs, args)
        parent.children.insert(position[-1], Proof(sentence, [], sentence_proof))
        parent.change_position_child(position)

    def edit_sentence(self, sentence, position):
        """
        Edit a sentence
        :param sentence: new sentence to replace the previous one
        :param position: tuple indicating the position of the proof
        """
        proof = self.get_proof(position)
        proof.sentence = sentence

    def edit_sentence_proof(self, sentence_proof, position):
        """
        Edit the sentence proof of a proof
        :param sentence_proof: SentenceProof instance
        :param position: tuple indicating the position of the proof
        """
        proof = self.get_proof(position)
        proof.sentence_proof = sentence_proof

    def get_sentence(self, arg):
        """
        Returns the sentence associated with arg
        :param arg: a tuple indicating a position
        :return: sentence
        """
        if isinstance(arg, tuple):
            proof = self.get_proof(arg)
            return proof.sentence
        # if isinstance(arg, IDSentence):
        # TODO retrieve the sentence from an IDSentence
        # pass
        raise ValueError("Arg is neither a tuple nor a IDSentence")

    def add_sentence_with_rule_child(self, position, rule, proofs, args):
        """
        Adds a new proof as a child of the given position by using an inference rule
        :param position: parent position
        :param rule: string indicating the inference rule to use
        :param proofs: proofs to use
        :param args: additional args required by the rule (e.g. a variable to rename)
        """
        parent = self.get_proof(position)
        self.add_sentence_rule(position + (len(parent.children),), rule, proofs, args)

    def check_proof(self, position):
        """
        Checks if the proof at the given position is correct
        :param position: tuple indicating the position at which to check the proof
        :return: true if the proof is correct, false otherwise
        """
        proof = self.get_proof(position)
        if proof.sentence_proof is None:
            return False
        sentence = self.apply_rule(
            position,
            proof.sentence_proof.rule,
            proof.sentence_proof.proofs,
            proof.sentence_proof.args,
        )
        if sentence is None:
            return False
        if not proof.sentence == sentence:
            return False
        for i in range(len(proof.children)):
            if not self.check_proof(position + (i,)):
                return False
        return True
