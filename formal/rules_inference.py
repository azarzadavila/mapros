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

StatementProof = namedtuple("StatementProof", ["rule", "sentences"])


def reductio_ad_absurdum(hypothesis, sentence, sentence_false):
    return Sentence(NEGATION, hypothesis)


def double_negation_elimination(sentence):
    return sentence.data[1].data[1]


def double_negation_introduction(sentence):
    return Sentence(NEGATION, Sentence(NEGATION, sentence))


def deduction_theorem(hypothesis, sentence):
    return Sentence(hypothesis, BinaryConnector.IMPLICATION, sentence)


def modus_ponens(sentence, hypothesis):
    return sentence.data[2]


def modus_tollens(sentence, conclusion_neg):
    return Sentence(NEGATION, sentence.data[0])


def adjunction(sentence1, sentence2):
    return Sentence(sentence1, BinaryConnector.CONJUCTION, sentence2)


def simplification1(sentence):
    return sentence.data[0]


def simplification2(sentence):
    return sentence.data[2]


def simplification(sentence):
    return simplification1(sentence)


def addition(sentence1, sentence2):
    return Sentence(sentence1, BinaryConnector.DISJUNCTION, sentence2)


def case_analysis(implication1, implication2, disjunction):
    return implication1.data[2]


def disjunctive_syllogism1(disjunction, sentence):
    return disjunction.data[2]


def disjunctive_syllogism2(disjunction, sentence):
    return disjunction.data[0]


def disjunctive_syllogism(disjunction, sentence):
    return disjunctive_syllogism1(disjunction, sentence)


def constructive_dilemma(implication1, implication2, disjunction):
    return Sentence(
        implication1.data[2], BinaryConnector.DISJUNCTION, implication2.data[2]
    )


def biconditional_introduction(implication1, implication2):
    return Sentence(
        implication1.data[0], BinaryConnector.BICONDITIONAL, implication2.data[0]
    )


def biconditional_elimination1(biconditional, sentence):
    return biconditional.data[2]


def biconditional_elimination2(biconditional, sentence):
    return biconditional.data[0]


def biconditional_elimination(biconditional, sentence):
    return biconditional_elimination1(biconditional, sentence)


def biconditional_neg1(biconditional, neg_sentence):
    return Sentence(NEGATION, biconditional.data[2])


def biconditional_neg2(biconditional, neg_sentence):
    return Sentence(NEGATION, biconditional.data[0])


def biconditional_neg(biconditional, neg_sentence):
    return biconditional_neg1(biconditional, neg_sentence)
