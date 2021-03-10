from typing import Type

from django.test import TestCase

from main.context import Context
from main.language import Language
from main.sentences import (
    RealValuedSequences,
    RealDeclaration,
    SequenceLimit,
    Inequality,
    ForAll,
)


def test_bijective(self, cls: Type[Language], natural, lean, context=None):
    obj = cls.from_natural(natural, context)
    self.assertEqual(obj.to_natural(), natural)
    self.assertEqual(obj.to_lean(), lean)
    obj = cls.from_lean(lean, context)
    self.assertEqual(obj.to_natural(), natural)
    self.assertEqual(obj.to_lean(), lean)


class RealValuedSequencesTest(TestCase):
    def test_basic(self):
        natural = "$a_n, b_n, c_n$ are real-valued sequences"
        lean = "a b c : ℕ → ℝ"
        test_bijective(self, RealValuedSequences, natural, lean)


class RealDeclarationTest(TestCase):
    def test_basic(self):
        natural = r"$l \in \mathbb{R}$"
        lean = "l : ℝ"
        test_bijective(self, RealDeclaration, natural, lean)


class SequenceLimitTest(TestCase):
    def test_basic(self):
        natural = r"$a_n \rightarrow l$"
        lean = "is_limit a l"
        test_bijective(self, SequenceLimit, natural, lean)


class InequalityTest(TestCase):
    def test_basic(self):
        nat_gt = "$a > b$"
        lean_gt = "a > b"
        test_bijective(self, Inequality, nat_gt, lean_gt)
        nat_ge = r"$a \geq b$"
        lean_ge = "a ≥ b"
        test_bijective(self, Inequality, nat_ge, lean_ge)
        nat_lt = "$a < b$"
        lean_lt = "a < b"
        test_bijective(self, Inequality, nat_lt, lean_lt)
        nat_le = r"$a \leq b$"
        lean_le = "a ≤ b"
        test_bijective(self, Inequality, nat_le, lean_le)

    def test_sequence(self):
        nat = r"$a_n \leq b_n$"
        lean = "a n ≤ b n"
        context = Context()
        context.add("a", "sequence")
        context.add("b", "sequence")
        test_bijective(self, Inequality, nat, lean, context)


class ForAllTest(TestCase):
    def test_inequality(self):
        natural = r"$\forall x : x < a$"
        lean = "∀ x : x < a"
        test_bijective(self, ForAll, natural, lean)
