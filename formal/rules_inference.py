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
    UnaryConnectorSentence,
    UnaryConnector,
    BinaryConnectorSentence,
    BinaryConnector,
    QuantifierSentence,
    Quantifier,
)


class SentenceProof(namedtuple("SentenceProof", ["rule", "proofs", "args"])):
    pass


def not_negation(negation):
    if (
        not isinstance(negation, UnaryConnectorSentence)
        or negation.connector != UnaryConnector.NEGATION
    ):
        raise ValueError("sentence is not a negation")


def not_conjunction(conjunction):
    if (
        not isinstance(conjunction, BinaryConnectorSentence)
        or conjunction.connector != BinaryConnector.CONJUNCTION
    ):
        raise ValueError("sentence is not a conjunction")


def not_disjunction(disjunction):
    if (
        not isinstance(disjunction, BinaryConnectorSentence)
        or disjunction.connector != BinaryConnector.DISJUNCTION
    ):
        raise ValueError("sentence is not a disjunction")


def not_implication(implication):
    if (
        not isinstance(implication, BinaryConnectorSentence)
        or implication.connector != BinaryConnector.IMPLICATION
    ):
        raise ValueError("sentence is not an implication")


def not_biconditional(biconditional):
    if (
        not isinstance(biconditional, BinaryConnectorSentence)
        or biconditional.connector != BinaryConnector.BICONDITIONAL
    ):
        raise ValueError("sentence is not a biconditional")


def not_universal(universal):
    if (
        not isinstance(universal, QuantifierSentence)
        or universal.quantifier != Quantifier.UNIVERSAL
    ):
        raise ValueError("sentence is not an universal")


def not_existential(existential):
    if (
        not isinstance(existential, QuantifierSentence)
        or existential.quantifier != Quantifier.EXISTENTIAL
    ):
        raise ValueError("sentence is not an existential")


def reductio_ad_absurdum(hypothesis, sentence, sentence_false):
    """
    TODO how to see if hypothesis is an hypothesis ?
    """
    if not UnaryConnectorSentence(UnaryConnector.NEGATION, sentence) == sentence_false:
        raise ValueError("sentence is not the negation of the sentence")
    return UnaryConnectorSentence(UnaryConnector.NEGATION, hypothesis)


def double_negation_elimination(sentence):
    not_negation(sentence)
    not_negation(sentence.sentence)
    return sentence.sentence.sentence


def double_negation_introduction(sentence):
    return UnaryConnectorSentence(
        UnaryConnector.NEGATION,
        UnaryConnectorSentence(UnaryConnector.NEGATION, sentence),
    )


def deduction_theorem(hypothesis, sentence):
    """
    TODO how to see if hypothesis is an hypothesis ?
    """
    return BinaryConnectorSentence(BinaryConnector.IMPLICATION, hypothesis, sentence)


def modus_ponens(sentence, hypothesis):
    not_implication(sentence)
    if not sentence.sentence1 == hypothesis:
        raise ValueError("hypothesis is not respected")
    return sentence.sentence2


def modus_tollens(sentence, conclusion_neg):
    not_implication(sentence)
    not_negation(conclusion_neg)
    if not sentence.sentence2 == conclusion_neg.sentence:
        raise ValueError("sentence is not the negation of the conclusion")
    return UnaryConnectorSentence(UnaryConnector.NEGATION, sentence.sentence1)


def adjunction(sentence1, sentence2):
    return BinaryConnectorSentence(BinaryConnector.CONJUNCTION, sentence1, sentence2)


def simplification1(sentence):
    not_conjunction(sentence)
    return sentence.sentence1


def simplification2(sentence):
    not_conjunction(sentence)
    return sentence.sentence2


def simplification(sentence):
    return simplification1(sentence)


def addition(sentence1, sentence2):
    return BinaryConnectorSentence(BinaryConnector.DISJUNCTION, sentence1, sentence2)


def case_analysis(implication1, implication2, disjunction):
    not_implication(implication1)
    not_implication(implication2)
    not_disjunction(disjunction)
    if (
        not disjunction.sentence1 == implication1.sentence1
        or not disjunction.sentence2 == implication2.sentence1
    ):
        raise ValueError("one of the implications is not in the disjunction")
    if not implication1.sentence2 == implication2.sentence2:
        raise ValueError("conclusion is not the same for both implications")
    return implication1.sentence2


def disjunctive_syllogism1(disjunction, sentence):
    not_disjunction(disjunction)
    if (
        not UnaryConnectorSentence(UnaryConnector.NEGATION, disjunction.sentence1)
        == sentence
    ):
        raise ValueError(
            "sentence is not the negation of the first arg of the disjunction"
        )
    return disjunction.sentence2


def disjunctive_syllogism2(disjunction, sentence):
    not_disjunction(disjunction)
    if (
        not UnaryConnectorSentence(UnaryConnector.NEGATION, disjunction.sentence2)
        == sentence
    ):
        raise ValueError(
            "sentence is not the negation of the second arg of the disjunction"
        )
    return disjunction.sentence1


def disjunctive_syllogism(disjunction, sentence):
    return disjunctive_syllogism1(disjunction, sentence)


def constructive_dilemma(implication1, implication2, disjunction):
    not_implication(implication1)
    not_implication(implication2)
    not_disjunction(disjunction)
    if not disjunction.sentence1 == implication1.sentence1:
        raise ValueError(
            "hypothesis of the first implication is not the first arg of the disjunction"
        )
    if not disjunction.sentence2 == implication2.sentence1:
        raise ValueError(
            "hypothesis of the second implication is not the second arg of the disjunction"
        )
    return BinaryConnectorSentence(
        BinaryConnector.DISJUNCTION, implication1.sentence2, implication2.sentence2
    )


def biconditional_introduction(implication1, implication2):
    not_implication(implication1)
    not_implication(implication2)
    if not implication1.sentence1 == implication2.sentence2:
        raise ValueError(
            "hypothesis of the first implication is not the conclusion of the second implication"
        )
    if not implication2.sentence1 == implication1.sentence2:
        raise ValueError(
            "hypothesis of the second implication is not the conclusion of the first implication"
        )
    return BinaryConnectorSentence(
        BinaryConnector.BICONDITIONAL, implication1.sentence1, implication2.sentence1
    )


def biconditional_elimination1(biconditional, sentence):
    not_biconditional(biconditional)
    if not biconditional.sentence1 == sentence:
        raise ValueError(
            "sentence does not correspond to the first element of the biconditional"
        )
    return biconditional.sentence2


def biconditional_elimination2(biconditional, sentence):
    not_biconditional(biconditional)
    if not biconditional.sentence2 == sentence:
        raise ValueError(
            "sentence does not correspond to the second element of the biconditional"
        )
    return biconditional.sentence1


def biconditional_elimination(biconditional, sentence):
    return biconditional_elimination1(biconditional, sentence)


def biconditional_neg1(biconditional, neg_sentence):
    not_biconditional(biconditional)
    not_negation(neg_sentence)
    if (
        not UnaryConnectorSentence(UnaryConnector.NEGATION, biconditional.sentence1)
        == neg_sentence
    ):
        raise ValueError(
            "sentence does not correspond to the negation of the first hypothesis"
        )
    return UnaryConnectorSentence(UnaryConnector.NEGATION, biconditional.sentence2)


def biconditional_neg2(biconditional, neg_sentence):
    not_biconditional(biconditional)
    not_negation(neg_sentence)
    if (
        not UnaryConnectorSentence(UnaryConnector.NEGATION, biconditional.sentence2)
        == neg_sentence
    ):
        raise ValueError(
            "sentence does not correspond to the negation of the second hypothesis"
        )
    return UnaryConnectorSentence(UnaryConnector.NEGATION, biconditional.sentence1)


def biconditional_neg(biconditional, neg_sentence):
    return biconditional_neg1(biconditional, neg_sentence)


def biconditional_disjunction1(biconditional, disjunction):
    not_biconditional(biconditional)
    not_disjunction(disjunction)
    if (
        not biconditional.sentence1 == disjunction.sentence1
        or not biconditional.sentence2 == disjunction.sentence2
    ):
        raise ValueError(
            "one side of biconditional does not correspond to the other side of the disjunction"
        )
    return BinaryConnectorSentence(
        BinaryConnector.CONJUNCTION, biconditional.sentence1, biconditional.sentence2
    )


def biconditional_disjunction2(biconditional, disjunction):
    not_biconditional(biconditional)
    not_disjunction(disjunction)
    if (
        not biconditional.sentence1 == disjunction.sentence2
        or not biconditional.sentence2 == disjunction.sentence1
    ):
        raise ValueError(
            "one side of biconditional does not correspond to the other side of the disjunction"
        )
    return BinaryConnectorSentence(
        BinaryConnector.CONJUNCTION, biconditional.sentence1, biconditional.sentence2
    )


def biconditional_disjunction(biconditional, disjunction):
    return biconditional_disjunction1(biconditional, disjunction)


def biconditional_disjunction_neg1(biconditional, disjunction):
    not_biconditional(biconditional)
    not_disjunction(disjunction)
    not_negation(disjunction.sentence1)
    not_negation(disjunction.sentence2)
    if (
        not biconditional.sentence1 == disjunction.sentence1.sentence
        or not biconditional.sentence2 == disjunction.sentence2.sentence
    ):
        raise ValueError(
            "one side of biconditional does not correspond to the negation to the other side of the disjunction"
        )
    return BinaryConnectorSentence(
        BinaryConnector.CONJUNCTION,
        UnaryConnectorSentence(UnaryConnector.NEGATION, biconditional.sentence1),
        UnaryConnectorSentence(UnaryConnector.NEGATION, biconditional.sentence2),
    )


def biconditional_disjunction_neg2(biconditional, disjunction):
    not_biconditional(biconditional)
    not_disjunction(disjunction)
    not_negation(disjunction.sentence1)
    not_negation(disjunction.sentence2)
    if (
        not biconditional.sentence1 == disjunction.sentence2.sentence
        or not biconditional.sentence2 == disjunction.sentence1.sentence
    ):
        raise ValueError(
            "one side of biconditional does not correspond to the negation to the other side of the disjunction"
        )
    return BinaryConnectorSentence(
        BinaryConnector.CONJUNCTION,
        UnaryConnectorSentence(UnaryConnector.NEGATION, biconditional.sentence1),
        UnaryConnectorSentence(UnaryConnector.NEGATION, biconditional.sentence2),
    )


def biconditional_disjunction_neg(biconditional, disjunction):
    return biconditional_disjunction_neg1(biconditional, disjunction)


def universal_generalization(sentence, var, new_var):
    # TODO check conditions
    return QuantifierSentence(
        Quantifier.UNIVERSAL, new_var, sentence.substitute(var, new_var)
    )


def universal_instantiation(sentence, new_var):
    # TODO check conditions
    not_universal(sentence)
    return sentence.sentence.substitute(sentence.var, new_var)


def existential_generalization(sentence, var, new_var):
    # TODO check conditions
    return QuantifierSentence(
        Quantifier.EXISTENTIAL, new_var, sentence.substitute(var, new_var)
    )


def existential_instantiation(sentence, new_var):
    # TODO check conditions
    not_existential(sentence)
    return sentence.sentence.substitute(sentence.var, new_var)


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
    "biconditional_disjunction1": biconditional_disjunction1,
    "biconditional_disjunction2": biconditional_disjunction2,
    "biconditional_disjunction": biconditional_disjunction,
    "biconditional_disjunction_neg1": biconditional_disjunction_neg1,
    "biconditional_disjunction_neg2": biconditional_disjunction_neg2,
    "biconditional_disjunction_neg": biconditional_disjunction_neg,
    "universal_generalization": universal_generalization,
    "universal_instantiation": universal_instantiation,
    "existential_generalization": existential_generalization,
    "existential_instantiation": existential_instantiation,
}
