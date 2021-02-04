import data.nat.prime

open nat

theorem infinitude_of_primes : ∀ N : nat, ∃ p ≥ N, p ≥ 0:=
begin
  intro N,
  use N+1,
  simp,
end