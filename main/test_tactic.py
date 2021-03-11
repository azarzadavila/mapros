from django.test import TestCase

from main.context import Context
from main.sentences import (
    SequenceLimit,
    ForAll,
    Inequality,
    InequalityType,
    Identifier,
    RealValuedSequences,
    RealDeclaration,
    ForAllNatIneqThen,
)
from main.tactic import (
    LetGoalLimit,
    ChooseNEpsilonLimit,
    LetMax,
    Use,
    ByInequalityProperties,
    LetNInequality,
    BySentenceWith,
)
from main.test_utils import test_bijective


class LetGoalLimitTest(TestCase):
    def test_basic(self):
        context = Context()
        natural = r"Let $\epsilon$"
        lean = "intros ε A1"
        context.current_goal = SequenceLimit("b", "l")
        test_bijective(self, LetGoalLimit, natural, lean, context)

    def test_fail(self):
        context = Context()
        natural = r"Let $\epsilon$"
        lean = "intros ε A1"
        context.current_goal = ForAll(
            "n", Inequality(Identifier("a"), InequalityType.GT, Identifier("b"))
        )
        self.assertIsNone(LetGoalLimit.from_natural(natural, context))
        self.assertIsNone(LetGoalLimit.from_lean(lean, context))


class ChooseNEpsilonLimitTest(TestCase):
    def test_basic(self):
        context = Context()
        RealValuedSequences.from_natural("$a_n, b_n, c_n$ are real-valued", context)
        RealDeclaration.from_natural(r"$l \in \mathbb{R}$", context)
        SequenceLimit.from_natural(r"$a_n \rightarrow l$", context)
        context.current_goal = SequenceLimit.from_natural(
            r"$b_n \rightarrow l$", context
        )
        LetGoalLimit.from_natural(r"Let $\epsilon$", context)
        natural = r"Let's choose $N_a$ such that H1 uses $\epsilon$"
        lean = r"cases H1 ε A1 with N_a A2"
        test_bijective(self, ChooseNEpsilonLimit, natural, lean, context)


class LetMaxTest(TestCase):
    def test_basic(self):
        natural = "Let $N = max(N_a, N_c)$"
        lean = "let N := max N_a N_c"
        test_bijective(self, LetMax, natural, lean)


class UseTest(TestCase):
    def test_basic(self):
        natural = "We claim $N$ works"
        lean = "use N"
        test_bijective(self, Use, natural, lean)


class ByInequalityPropertiesTest(TestCase):
    def test_basic(self):
        natural = r"By inequality properties, $N_a \leq N$"
        lean = r"have A1 : N_a ≤ N := by obvious_ineq"
        test_bijective(self, ByInequalityProperties, natural, lean)


class LetNInequalityTest(TestCase):
    def test_basic(self):
        natural = "Let $n$"
        lean = "intros n A1"
        context = Context()
        context.current_goal = ForAllNatIneqThen(
            "n", Inequality.from_natural(r"$n \leq N$"), r"|b_n - l| < \epsilon$"
        )
        test_bijective(self, LetNInequality, natural, lean, context)

    def test_fail(self):
        natural = "Let $n$"
        lean = "intros n A1"
        self.assertIsNone(LetNInequality.from_natural(natural, Context()))
        self.assertIsNone(LetNInequality.from_lean(lean, Context()))


class BySentenceWithTest(TestCase):
    def test_basic(self):
        natural = r"$a_n \leq b_n$ by H1 with n"
        lean = "have A1 : a n ≤ b n := H1 n"
        context = Context()
        context.add("a", "sequence")
        context.add("b", "sequence")
        test_bijective(self, BySentenceWith, natural, lean, context)
