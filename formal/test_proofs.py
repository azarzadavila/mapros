from django.test import TestCase

from formal.grammar import PredicateConstant, BinaryConnector, Sentence
from formal.proof import check_scope, Proof
from formal.rules_inference import StatementProof

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
    def test_simple(self):
        A = PredicateConstant("A")
        B = PredicateConstant("B")
        proof = Proof(Sentence(A, BC.CONJUNCTION, B), [], None)
        proof.add_statement_child(A, ())
        proof.add_statement_child(B, ())
        proof.edit_statement_proof(StatementProof("premise", []), (0,))
        proof.edit_statement_proof(StatementProof("premise", []), (1,))
        proof.edit_statement_proof(StatementProof("adjunction", [(0,), (1,)]), ())
        self.assertTrue(proof.check_proof(()))
