from django.test import TestCase

from main.manager import Manager

sandwich_hyp = [
    "$a_n, b_n, c_n$ are real-valued sequences",
    r"$l \in \mathbb{R}$",
    r"$a_n \rightarrow l$",
    r"$c_n \rightarrow l$",
    r"$\forall n : a_n \leq b_n$",
    r"$\forall n : b_n \leq c_n$",
]
sandwich_goal = r"$b_n \rightarrow l$"


class ManagerTest(TestCase):
    def test_basic(self):
        manager = Manager()
        for hyp in sandwich_hyp:
            manager.add_hypothesis(hyp)
        manager.set_initial_goal(sandwich_goal)
        expected = [None, None, "H1", "H2", "H3", "H4"]
        self.assertEqual(manager.ident_hypotheses(), expected)

    def test_to_lean(self):
        manager = Manager()
        manager.theorem_name = "sandwich"
        for hyp in sandwich_hyp:
            manager.add_hypothesis(hyp)
        manager.set_initial_goal(sandwich_goal)
        expected = r"""theorem sandwich
(a b c : ℕ → ℝ)
(l : ℝ)
(H1 : is_limit a l)
(H2 : is_limit c l)
(H3 : ∀ n, a n ≤ b n)
(H4 : ∀ n, b n ≤ c n)
:
is_limit b l
:=
begin
sorry,
end"""
        self.assertEqual(manager.to_lean(), expected)
