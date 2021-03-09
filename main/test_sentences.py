from django.test import TestCase

from main.sentences import RealValuedSequences


class RealValuedSequencesTest(TestCase):
    def test_basic(self):
        natural = "$a_n, b_n, c_n$ are real-valued sequences"
        seq = RealValuedSequences.from_natural(natural)
        self.assertEqual(seq.to_natural(), natural)
        lean = "a b c : ℕ → ℝ"
        self.assertEqual(seq.to_lean(), lean)
        seq = RealValuedSequences.from_lean(lean)
        self.assertEqual(seq.to_lean(), lean)
        self.assertEqual(seq.to_natural(), natural)
