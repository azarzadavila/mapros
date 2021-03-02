# import leanstart.leantonatural.parser as parser
import parser
from lean_to_html import lean_to_html


def parser_test():
    s = r"""
    import data.nat.prime

    open nat

    theorem infinitude_of_prime (hello) (here is another)(again)((nani:)a) : exists a, prime p :=
    begin
        p1
        begin
            p2
        end
        p3 p4
    end
    """
    print(parser.parser.parse(s).pretty())


def html_test():
    s = r"""
    import data.nat.prime
    open nat
    theorem infinitude_of_prime (h1 : hyp1) (h2 : hyp2 (inside)) : exists a, prime p :=
    begin
        p1
        begin
            p2
        end
        p3 p4
    end
    """
    lean_to_html(input_string=s, output_file="html_test.html")


def html_test_interval():
    s = r"""
    import data.nat.prime
    open nat
    theorem infinitude_of_prime (a b : R) (h1 : set.Icc a b) (h2 : set.Ico a b) (h3 : set.Ioc a b) (h4 : set.Icc a b) : exists a, prime p :=
    begin
        p1
        begin
            p2
        end
        p3 p4
    end
    """
    lean_to_html(input_string=s, output_file="html_test_interval.html")


def html_test_deriv():
    s = r"""
    import data.nat.prime
    open nat
    theorem infinitude_of_prime (a b : R) (f : R → R) (h1 : b = deriv f a) : exists a, prime p :=
    begin
        p1
        begin
            p2
        end
        p3 p4
    end
    """
    lean_to_html(input_string=s, output_file="html_test_deriv.html")


def html_test_continuous_on():
    s = r"""
    import data.nat.prime
    open nat
    theorem infinitude_of_prime (a b : R) (f : R → R) (h1 : continuous_on f (set.Icc a b)) : exists a, prime p :=
    begin
        p1
        begin
            p2
        end
        p3 p4
    end
    """
    lean_to_html(input_string=s, output_file="html_test_continuous_on.html")


def html_test_differentiable_on():
    s = r"""
    import data.nat.prime
    open nat
    theorem infinitude_of_prime (a b : R) (f : R → R) (h1 : differentiable_on R f (set.Icc a b)) : exists a, prime p :=
    begin
        p1
        begin
            p2
        end
        p3 p4
    end
    """
    lean_to_html(input_string=s, output_file="html_test_differentiable_on.html")


def html_test_complicated():
    s = r"""
    open nat
    theorem irrational_nrt_of_n_not_dvd_multiplicity (x : ℝ) (n : ℕ) (m : ℤ) (hm : m ≠ 0) (p : ℕ)
  (hp : fact p.prime) (hxr : x ^ n = m)
  (hv : (multiplicity (p : ℤ) m) .get (finite_int_iff.2 ⟨hp.ne_one, hm⟩) % n ≠ 0) :
  irrational x :=
begin
  rcases nat.eq_zero_or_pos n with rfl | hnpos,
  { rw [eq_comm, pow_zero, ← int.cast_one, int.cast_inj] at hxr,
    simpa [hxr, multiplicity.one_right (mt is_unit_iff_dvd_one.1
      (mt int.coe_nat_dvd.1 hp.not_dvd_one)), nat.zero_mod] using hv },
  refine irrational_nrt_of_notint_nrt _ _ hxr _ hnpos,
  rintro ⟨y, rfl⟩,
  rw [← int.cast_pow, int.cast_inj] at hxr, subst m,
  have : y ≠ 0, { rintro rfl, rw zero_pow hnpos at hm, exact hm rfl },
  erw [multiplicity.pow' (nat.prime_iff_prime_int.1 hp)
    (finite_int_iff.2 ⟨hp.ne_one, this⟩), nat.mul_mod_right] at hv,
  exact hv rfl
end
    """
    lean_to_html(input_string=s, output_file="html_test_complicated.html")


parser_test()
html_test()
html_test_interval()
html_test_deriv()
html_test_continuous_on()
html_test_differentiable_on()
html_test_complicated()