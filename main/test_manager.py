from django.test import TestCase

from main.manager import Manager


class ManagerTest(TestCase):
    def test_basic(self):
        manager = Manager()
        manager.add_hypothesis("$a_n, b_n, c_n$ are real-valued sequences")
        manager.add_hypothesis(r"$l \in \mathbb{R}$")
        manager.add_hypothesis(r"$a_n \rightarrow l$")
        manager.add_hypothesis(r"$c_n \rightarrow l$")
        manager.add_hypothesis(r"$\forall n : a_n \leq b_n$")
        manager.add_hypothesis(r"$\forall n : b_n \leq c_n$")
        self.assertEqual(len(manager.hypotheses), 4)
