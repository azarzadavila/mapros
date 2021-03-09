from typing import Type

from django.test import TestCase

from main.language import Language
from main.sentences import RealValuedSequences, RealDeclaration, SequenceLimit


def test_bijective(self, cls: Type[Language], natural, lean):
    obj = cls.from_natural(natural)
    self.assertEqual(obj.to_natural(), natural)
    self.assertEqual(obj.to_lean(), lean)
    obj = cls.from_lean(lean)
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
