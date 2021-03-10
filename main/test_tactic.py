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
)
from main.tactic import LetGoalLimit, ChooseNEpsilonLimit
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
