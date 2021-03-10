from django.test import TestCase

from main.context import Context
from main.sentences import SequenceLimit, ForAll, Inequality, InequalityType, Identifier
from main.tactic import LetGoalLimit
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
