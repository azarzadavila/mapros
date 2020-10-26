"""
This file contains rules of inference that allow a syntactical transformation of sentences to another sentence.
The list of rules of inference is mainly inspired from sections rules for classical sentential calculus and
rules of classical predicate calculus from
https://en.wikipedia.org/wiki/List_of_rules_of_inference#Rules_of_classical_predicate_calculus

The files is separated between functions that generate the new sentence,
named tuple that explain how the transformation happened.
"""
from collections import namedtuple
from formal.grammar import (
    Sentence,
    IDSentence,
    AtomicSentence,
    Term,
    Predicate,
    LogicFunction,
    NEGATION,
    Quantifier,
    BinaryConnector,
    Constant,
    Variable,
)


class StatementProof(namedtuple("StatementProof", ["rule", "sentences"])):
    def __str__(self):
        if len(self.sentences) == 0:
            return self.rule
        s = self.rule
        s += " ("
        for i in range(len(self.sentences) - 1):
            s += str(self.sentences[i])
            s += ", "
        s += str(self.sentences[-1])
        s += ")"
        return s


def not_implication(implication):
    if not implication.data[1] == BinaryConnector.IMPLICATION:
        raise ValueError("The passed sentence is not an implication")


def not_conjunction(conjunction):
    if not conjunction.data[1] == BinaryConnector.CONJUNCTION:
        raise ValueError("The passed sentence is not a conjunction")


def not_disjunction(disjunction):
    if not disjunction.data[1] == BinaryConnector.DISJUNCTION:
        raise ValueError("The passed sentence is not a disjunction")


def not_biconditional(biconditional):
    if not biconditional.data[1] == BinaryConnector.BICONDITIONAL:
        raise ValueError("The passed sentence is not a biconditional")


def not_universal(universal):
    if not universal.data[0] == Quantifier.UNIVERSAL:
        raise ValueError("The passed sentence is not an universal")


def not_existential(existential):
    if not existential.data[0] == Quantifier.EXISTENTIAL:
        raise ValueError("The passed sentence is not an existential")


def reductio_ad_absurdum(hypothesis, sentence, sentence_false):
    """
    TODO how to see if hypothesis is an hypothesis ?
    """
    if not Sentence(NEGATION, sentence) == sentence_false:
        raise ValueError("The sentence passed is not the negation of the sentence")
    return Sentence(NEGATION, hypothesis)


def double_negation_elimination(sentence):
    if not sentence.data[0] == NEGATION and sentence.data[1].data[1] == NEGATION:
        raise ValueError("This is not a double negation")
    return sentence.data[1].data[1]


def double_negation_introduction(sentence):
    return Sentence(NEGATION, Sentence(NEGATION, sentence))


def deduction_theorem(hypothesis, sentence):
    """
    TODO how to see if hypothesis is an hypothesis ?
    """
    return Sentence(hypothesis, BinaryConnector.IMPLICATION, sentence)


def modus_ponens(sentence, hypothesis):
    not_implication(sentence)
    if not sentence.data[0] == hypothesis:
        raise ValueError("The hypothesis is not respected")
    return sentence.data[2]


def modus_tollens(sentence, conclusion_neg):
    not_implication(sentence)
    if not sentence.data[2] == conclusion_neg.data[1]:
        raise ValueError("The passed sentence is not the negation of the conclusion")
    return Sentence(NEGATION, sentence.data[0])


def adjunction(sentence1, sentence2):
    return Sentence(sentence1, BinaryConnector.CONJUNCTION, sentence2)


def simplification1(sentence):
    not_conjunction(sentence)
    return sentence.data[0]


def simplification2(sentence):
    not_conjunction(sentence)
    return sentence.data[2]


def simplification(sentence):
    return simplification1(sentence)


def addition(sentence1, sentence2):
    return Sentence(sentence1, BinaryConnector.DISJUNCTION, sentence2)


def case_analysis(implication1, implication2, disjunction):
    not_implication(implication1)
    not_implication(implication2)
    not_disjunction(disjunction)
    if (
        not disjunction.data[0] == implication1.data[0]
        or not disjunction.data[2] == implication2.data[0]
    ):
        raise ValueError("One of the implications is not in the disjunction")
    if not implication1.data[2] == implication2.data[2]:
        raise ValueError("The conclusion is not the same for both implications")
    return implication1.data[2]


def disjunctive_syllogism1(disjunction, sentence):
    not_disjunction(disjunction)
    if not Sentence(NEGATION, disjunction.data[0]) == sentence:
        raise ValueError(
            "The passed sentence is not the negation of the first arg of the disjunction"
        )
    return disjunction.data[2]


def disjunctive_syllogism2(disjunction, sentence):
    not_disjunction(disjunction)
    if not Sentence(NEGATION, disjunction.data[2]) == sentence:
        raise ValueError(
            "The passed sentence is not the negation of the second arg of the disjunction"
        )
    return disjunction.data[0]


def disjunctive_syllogism(disjunction, sentence):
    return disjunctive_syllogism1(disjunction, sentence)


def constructive_dilemma(implication1, implication2, disjunction):
    not_implication(implication1)
    not_implication(implication2)
    not_disjunction(disjunction)
    if not disjunction.data[0] == implication1.data[0]:
        raise ValueError(
            "The hypothesis of the first implication is not the first arg of the disjunction"
        )
    if not disjunction.data[2] == implication2.data[0]:
        raise ValueError(
            "The hypothesis of the second implication is not the second arg of the disjunction"
        )
    return Sentence(
        implication1.data[2], BinaryConnector.DISJUNCTION, implication2.data[2]
    )


def biconditional_introduction(implication1, implication2):
    not_implication(implication1)
    not_implication(implication2)
    if not implication1.data[0] == implication2.data[2]:
        raise ValueError(
            "The hypothesis of the first implication is not the conclusion of the second implication"
        )
    if not implication2.data[0] == implication1.data[2]:
        raise ValueError(
            "The hypothesis of the second implication is not the conclusion of the first implication"
        )
    return Sentence(
        implication1.data[0], BinaryConnector.BICONDITIONAL, implication2.data[0]
    )


def biconditional_elimination1(biconditional, sentence):
    not_biconditional(biconditional)
    if not biconditional[0] == sentence:
        raise ValueError(
            "The passed sentence does not correspond to the first element of the biconditional"
        )
    return biconditional.data[2]


def biconditional_elimination2(biconditional, sentence):
    not_biconditional(biconditional)
    if not biconditional[2] == sentence:
        raise ValueError(
            "The passed sentence does not correspond to the second element of the biconditional"
        )
    return biconditional.data[0]


def biconditional_elimination(biconditional, sentence):
    return biconditional_elimination1(biconditional, sentence)


def biconditional_neg1(biconditional, neg_sentence):
    not_biconditional(biconditional)
    if not Sentence(NEGATION, biconditional.data[0]) == neg_sentence:
        raise ValueError(
            "The passed sentence does not correspond to the negation of the first hypothesis"
        )
    return Sentence(NEGATION, biconditional.data[2])


def biconditional_neg2(biconditional, neg_sentence):
    not_biconditional(biconditional)
    if not Sentence(NEGATION, biconditional.data[2]) == neg_sentence:
        raise ValueError(
            "The passed sentence does not correspond to the negation of the second hypothesis"
        )
    return Sentence(NEGATION, biconditional.data[0])


def biconditional_neg(biconditional, neg_sentence):
    return biconditional_neg1(biconditional, neg_sentence)


def universal_generalization(sentence, var, new_var):
    # TODO check conditions
    return Sentence(Quantifier.UNIVERSAL, new_var, sentence.substitute(var, new_var))


def universal_instantiation(sentence, new_var):
    # TODO check conditions
    not_universal(sentence)
    return sentence.data[2].substitute(sentence.data[1], new_var)


def existential_generalization(sentence, var, new_var):
    # TODO check conditions
    return Sentence(Quantifier.EXISTENTIAL, new_var, sentence.substitute(var, new_var))


def existential_instantiation(sentence, new_var):
    # TODO check conditions
    not_existential(sentence)
    return sentence[2].substitute(sentence.data[1], new_var)


MAP_RULE = {
    "reductio_ad_absurdum": reductio_ad_absurdum,
    "double_negation_elimination": double_negation_elimination,
    "double_negation_introduction": double_negation_introduction,
    "deduction_theorem": deduction_theorem,
    "modus_ponens": modus_ponens,
    "modus_tollens": modus_tollens,
    "adjunction": adjunction,
    "simplification1": simplification1,
    "simplification2": simplification2,
    "simplification": simplification,
    "addition": addition,
    "case_analysis": case_analysis,
    "disjunctive_syllogism1": disjunctive_syllogism1,
    "disjunctive_syllogism2": disjunctive_syllogism2,
    "disjunctive_syllogism": disjunctive_syllogism,
    "constructive_dilemma": constructive_dilemma,
    "biconditional_introduction": biconditional_introduction,
    "biconditional_elimination1": biconditional_elimination1,
    "biconditional_elimination2": biconditional_elimination2,
    "biconditional_elimination": biconditional_elimination,
    "biconditional_neg1": biconditional_neg1,
    "biconditional_neg2": biconditional_neg2,
    "biconditional_neg": biconditional_neg,
    "universal_generalization": universal_generalization,
    "universal_instantiation": universal_instantiation,
    "existential_generalization": existential_generalization,
    "existential_instantiation": existential_instantiation,
}
