from django.test import TestCase

from formal.grammar import (
    ConstantPredicate,
    BinaryConnector,
    Sentence,
    BinaryConnectorSentence,
)
from formal.proof import check_scope, Proof
from formal.rules_inference import SentenceProof

BC = BinaryConnector


class SimpleUnits(TestCase):
    def test_scope(self):
        self.assertTrue(check_scope((1,), (2,)))
        self.assertTrue(check_scope((1,), (2, 1)))
        self.assertTrue(check_scope((1,), (2, 1, 3)))
        self.assertTrue(check_scope((2, 1), (2, 3)))
        self.assertTrue(check_scope((2, 1), (2, 3, 2)))
        self.assertFalse(check_scope((3,), (2,)))
        self.assertFalse(check_scope((1, 1), (2,)))
        self.assertFalse(check_scope((2, 1, 1), (2, 2,)))
        self.assertTrue(check_scope((2, 1, 1), (2, 1,)))


class CompleteFirstOrderProof(TestCase):
    def test_ex1(self):
        A = ConstantPredicate("A")
        B = ConstantPredicate("B")
        C = ConstantPredicate("C")
        proof = Proof(
            BinaryConnectorSentence(BinaryConnector.IMPLICATION, A, C), [], None
        )
        proof.add_sentence_child(A, ())
        proof.edit_sentence_proof(SentenceProof("hypothesis", [], []), (0,))
        proof.add_sentence_child(
            BinaryConnectorSentence(BinaryConnector.IMPLICATION, A, B), ()
        )
        proof.edit_sentence_proof(SentenceProof("premise", [], []), (1,))
        proof.add_sentence_child(
            BinaryConnectorSentence(BinaryConnector.IMPLICATION, B, C), ()
        )
        proof.edit_sentence_proof(SentenceProof("premise", [], []), (2,))
        proof.add_sentence_with_rule_child((), "modus_ponens", [(1,), (0,)], [])
        proof.add_sentence_with_rule_child((), "modus_ponens", [(2,), (3,)], [])
        proof.edit_sentence_proof(
            SentenceProof("deduction_theorem", [(0,), (4,)], []), ()
        )
        self.assertTrue(proof.check_proof((0,)))
        self.assertTrue(proof.check_proof((1,)))
        self.assertTrue(proof.check_proof((2,)))
        self.assertTrue(proof.check_proof((3,)))
        self.assertTrue(proof.check_proof((4,)))
        self.assertTrue(proof.check_proof(()))
