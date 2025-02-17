from django.test import TestCase

from main.context import Context
from main.sentences import (
    RealValuedSequences,
    RealDeclaration,
    SequenceLimit,
    Inequality,
    ForAll,
    AbsoluteDiff,
)
from main.test_utils import test_bijective


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
        lean = "∀ x, x < a"
        test_bijective(self, ForAll, natural, lean)


class AbsoluteDiffTest(TestCase):
    def test_basic(self):
        natural = r"$\left|a - b \right|$"
        lean = "|a - b|"
        test_bijective(self, AbsoluteDiff, natural, lean)

    def test_sequence(self):
        natural = r"$\left|a_n - b_n \right|$"
        lean = "|a n - b n|"
        context = Context()
        context.add("a", "sequence")
        context.add("b", "sequence")
        test_bijective(self, AbsoluteDiff, natural, lean, context)

    def test_inequality(self):
        natural = r"$\left|a - b \right| \leq n$"
        lean = "|a - b| ≤ n"
        test_bijective(self, Inequality, natural, lean)

    def test_inequality_sequence(self):
        natural = r"$\left|a_n - b_n \right| \leq n$"
        lean = r"|a n - b n| ≤ n"
        context = Context()
        context.add("a", "sequence")
        context.add("b", "sequence")
        test_bijective(self, Inequality, natural, lean, context)
