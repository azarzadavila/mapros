import os

from django.test import TestCase

import leanclient.client_wrapper as client_wrapper
from main.manager import Manager, extract_goal, extract_error

sandwich_hyp = [
    "$a_n, b_n, c_n$ are real-valued sequences",
    r"$l \in \mathbb{R}$",
    r"$a_n \rightarrow l$",
    r"$c_n \rightarrow l$",
    r"$\forall n : a_n \leq b_n$",
    r"$\forall n : b_n \leq c_n$",
]
sandwich_goal = r"$b_n \rightarrow l$"
sandwich_proof = [
    r"Let $\epsilon$",
    r"Let's choose $N_a$ such that H1 uses $\epsilon$",
    r"Let's choose $N_c$ such that H2 uses $\epsilon$",
    r"Let $N = max(N_a, N_c)$",
    r"We claim $N$ works",
    r"By inequality properties, $N_a \leq N$",
    r"By inequality properties, $N_c \leq N$",
    r"Let $n$",
    r"$a_n \leq b_n$ by H3 with n",
    r"$b_n \leq c_n$ by H4 with n",
    r"By inequality properties, $N_a \leq n$",
    r"Let's choose n in H2",
    r"$|a_n - l| < \epsilon$ by A10 with A9",
    r"By inequality properties, $N_c \leq n$",
    r"Let's choose n in A3",
    r"$|c_n - l| < \epsilon$ by A13 with A12",
    r"$Let's use absolute value inequality property on A11 A14 and on goal$",
    r"Let's separate A11",
    r"Let's separate A14",
    r"Let's split the goal and do on all subgoals",
    r"By linear arithmetic",
]


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
        for proof in sandwich_proof:
            manager.add_proof_line(proof)
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
intros ε A1,
cases H1 ε A1 with N_a A2,
cases H2 ε A1 with N_c A3,
let N := max N_a N_c,
use N,
have A4 : N_a ≤ N := by obvious_ineq,
have A5 : N_c ≤ N := by obvious_ineq,
intros n A6,
have A7 : a n ≤ b n := H3 n,
have A8 : b n ≤ c n := H4 n,
have A9 : N_a ≤ n := by obvious_ineq,
have A10 := H2 n,
have A11 : |a n - l| < ε := A10 A9,
have A12 : N_c ≤ n := by obvious_ineq,
have A13 := A3 n,
have A14 : |c n - l| < ε := A13 A12,
rw abs_sub_lt_iff at A11 A14 ⊢,
cases A11,
cases A14,
split;
linarith,
end"""
        actual, _ = manager.to_lean(header=False)
        self.assertEqual(actual, expected)

    def test_client_wrapper(self):
        manager = Manager()
        manager.theorem_name = "sandwich"
        for hyp in sandwich_hyp:
            manager.add_hypothesis(hyp)
        manager.set_initial_goal(sandwich_goal)
        for proof in sandwich_proof:
            manager.add_proof_line(proof)
        text, lines = manager.to_lean()
        file = open(client_wrapper.LEAN_DIR_SRC + "result.lean", "w")
        file.write(text)
        file.close()
        client_wrapper.states("result.lean", lines)


class TestExtract(TestCase):
    def test_extract_goal(self):
        states, err = client_wrapper.states("sandwich.lean", [33])
        state = states[0]
        self.assertEqual(extract_goal(state), "is_limit b l")

    def test_extract_error(self):
        states, err = client_wrapper.states("sandwich_error.lean", [40])
        expected = r"unknown identifier 'He'"
        self.assertEqual(extract_error(err), expected)

    def test_extract_error_multi(self):
        states, err = client_wrapper.states("sandwich_error_multiline.lean", [40])
        expected = r"""type mismatch at application
  ha ε hc
term
  hc
has type
  is_limit c l
but is expected to have type
  ε > 0"""
        self.assertEqual(extract_error(err), expected)
