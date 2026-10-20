"""Check all 22 examples, current follow-up exercises and corrected claims."""
from pathlib import Path
import re
import sys

import numpy as np
import sympy as s

ROOT = Path(__file__).resolve().parents[1]
LESSON = (ROOT / "lesson.md").read_text(encoding="utf-8")
n, N = s.symbols("n N", integer=True, positive=True)
x, T = s.symbols("x T", positive=True)
failures = 0


def eq(actual, expected):
    assert s.simplify(actual - expected) == 0, (actual, expected)


def run(label, work):
    global failures
    try:
        work()
        print("PASS", label)
    except Exception as exc:
        failures += 1
        print("FAIL", label, type(exc).__name__, str(exc))


def conv(term, start=1):
    result = s.Sum(term, (n, start, s.oo)).is_convergent()
    assert result in (s.true, s.false), result
    return bool(result)


def e01():
    eq(s.summation(3/s.Integer(10)**n, (n, 1, s.oo)), s.Rational(1, 3))
    eq(s.summation(9/s.Integer(10)**n, (n, 1, s.oo)), 1)
    eq(s.summation(27/s.Integer(100)**n, (n, 1, s.oo)), s.Rational(3, 11))


def e02():
    term = 1/(n*(n+2))
    partial = s.summation(term, (n, 1, N))
    eq(partial, (1+s.Rational(1, 2)-1/(N+1)-1/(N+2))/2)
    eq(s.limit(partial, N, s.oo), s.Rational(3, 4))


def e03():
    product = s.product(1+1/n, (n, 1, N))
    eq(product, N+1)
    assert s.limit(s.log(product), N, s.oo) == s.oo
    eq(s.limit(s.log(1+1/n), n, s.oo), 0)


def e04():
    gamma = s.Rational(9, 10)
    eq(s.summation(gamma**n, (n, 0, s.oo)), 10)
    partial = s.summation(gamma**n, (n, 0, 499))
    assert f"{float(partial):.4f}" == "10.0000"
    assert s.limit(s.summation(s.Integer(1), (n, 1, N)), N, s.oo) == s.oo


def e05():
    eq(s.summation((2**n+3**n)/6**n, (n, 1, s.oo)), s.Rational(3, 2))


def e06():
    terms = [n/(n+1), (1+1/n)**n, n*s.sin(1/n)]
    for term, expected in zip(terms, [1, s.E, 1]):
        limit = s.limit(term, n, s.oo)
        eq(limit, expected)
        assert limit != 0


def e07():
    terms = [1/s.sqrt(n**3), 1/s.sqrt(n), 1/(n*s.sqrt(n))]
    assert [conv(term) for term in terms] == [True, False, True]
    eq(terms[0], terms[2])


def e08():
    z = s.symbols("z", nonnegative=True)
    for power, expected in [(1, s.oo), (2, 1/s.log(2))]:
        function = 1/(x*s.log(x)**power)
        derivative = s.diff(function, x)
        assert s.simplify(derivative.subs(x, 2*s.exp(z))).is_negative
        value = s.integrate(function, (x, 2, s.oo))
        if expected is s.oo:
            assert value == expected
        else:
            eq(value, expected)


def e09():
    alpha = s.symbols("alpha", real=True)
    allowed = s.solve_univariate_inequality(alpha <= 1, alpha, relational=False)
    allowed &= s.solve_univariate_inequality(2*alpha > 1, alpha, relational=False)
    assert allowed == s.Interval.Lopen(s.Rational(1, 2), 1)
    for value, expected in [(1, True), (s.Rational(3, 5), True),
                            (s.Rational(1, 2), False), (s.Rational(3, 2), False)]:
        step = n**(-value)
        actual = not conv(step) and conv(step**2)
        assert actual == expected


def e10():
    for term, upper in [(1/(n*n+n+1), 1/n**2), (1/(2**n+n), 1/2**n)]:
        assert s.factor(upper-term).is_positive
        assert conv(upper)


def e11():
    cases = [(s.sin(1/n), 1/n, 1, False),
             (1-s.cos(1/n), 1/n**2, s.Rational(1, 2), True),
             (s.log(1+1/n**2), 1/n**2, 1, True)]
    for term, reference, expected_limit, expected_conv in cases:
        ratio = s.limit(term/reference, n, s.oo)
        eq(ratio, expected_limit)
        assert ratio.is_positive
        assert conv(reference) == expected_conv


def e12():
    term = 1/n-s.sin(1/n)
    eq(s.limit(term*n**3, n, s.oo), s.Rational(1, 6))
    eq(s.series(x-s.sin(x), x, 0, 4).removeO(), x**3/6)
    assert conv(n**-3)


def e13():
    z = s.symbols("z", nonnegative=True)
    gap = x-s.log(x)
    assert gap.subs(x, 2).is_positive
    assert s.simplify(s.diff(gap, x).subs(x, z+2)).is_positive
    assert not conv(1/n, 2)
    eq(s.limit(1/s.log(n), n, s.oo), 0)


def e14():
    term = n**2/2**n
    ratio = s.simplify(term.subs(n, n+1)/term)
    eq(s.limit(ratio, n, s.oo), s.Rational(1, 2))
    eq(s.summation(term, (n, 1, s.oo)), 6)


def e15():
    for base, expected in [(2, True), (3, False)]:
        term = base**n*s.factorial(n)/n**n
        ratio = s.combsimp(term.subs(n, n+1)/term)
        rho = s.limit(ratio, n, s.oo)
        eq(rho, base/s.E)
        assert bool(rho < 1) == expected
        assert bool(rho > 1) == (not expected)


def e16():
    terms = [(n/(2*n+1))**n, (1-1/n)**(n*n)]
    for term, expected in zip(terms, [s.Rational(1, 2), s.exp(-1)]):
        # Compute log(root) to avoid ambiguous symbolic fractional powers.
        rho = s.exp(s.limit(s.log(term)/n, n, s.oo))
        eq(rho, expected)
        assert rho < 1


def e17():
    b = s.symbols("b", positive=True)
    term = b**n/n
    rho = s.limit(s.simplify(term.subs(n, n+1)/term), n, s.oo)
    eq(rho, b)
    region = s.solve_univariate_inequality(rho < 1, b, relational=False)
    region &= s.Interval.open(0, s.oo)
    assert region == s.Interval.open(0, 1)
    boundary = s.solve(rho-1, b)[0]
    assert not conv(term.subs(b, boundary))


def e18():
    amplitude = 1/n
    assert s.factor(amplitude-amplitude.subs(n, n+1)).is_positive
    eq(s.limit(amplitude, n, s.oo), 0)
    bound = amplitude.subs(n, 1001)
    eq(bound, s.Rational(1, 1001))
    indices = np.arange(1, 1001, dtype=np.float64)
    partial = np.sum((-1.0)**(indices-1)/indices)
    total = float(s.log(2))
    assert f"{partial:.5f}" == "0.69265"
    assert f"{total:.5f}" == "0.69315"
    assert f"{total-partial:.4f}" == "0.0005"
    assert 0 < total-partial <= float(bound)
    # The follow-up's 31 is the minimum for the *bound*, not actual error.
    tolerance = s.Rational(1, 1000)
    bound_minimum = next(i for i in range(1, 100)
                         if s.Rational(1, (i+1)**2) < tolerance)
    assert bound_minimum == 31
    square_total = s.summation((-1)**(n-1)/n**2, (n, 1, s.oo))
    eq(square_total, s.pi**2/12)
    square_partial = s.S.Zero
    actual_minimum = None
    for i in range(1, bound_minimum+1):
        square_partial += s.Rational((-1)**(i-1), i*i)
        if s.Abs(square_total-square_partial) < tolerance:
            actual_minimum = i
            break
    assert actual_minimum == 22
    followup = LESSON.split("> 用余项估计保证", 1)[1].split("**例 19**", 1)[0]
    assert rf"N\ge{bound_minimum}" in followup
    assert f"实际算下来 {actual_minimum} 项就够了" in followup


def e19():
    function = s.log(x)/x
    eq(s.diff(function, x), (1-s.log(x))/x**2)
    eq(s.limit(function, x, s.oo), 0)
    z = s.symbols("z", positive=True)
    assert s.simplify(s.diff(function, x).subs(x, s.exp(1+z))).is_negative
    assert s.log(3) > 1


def e20():
    amplitude = s.sin(1/x)
    eq(s.limit(amplitude, x, s.oo), 0)
    eq(s.diff(amplitude, x), -s.cos(1/x)/x**2)
    # For x >= 1, 0 < 1/x <= 1 < pi/2, so the derivative is negative.
    assert 1 < s.pi/2
    assert s.cos(1).is_positive
    eq(s.limit(n*s.sin(1/n), n, s.oo), 1)
    assert not conv(1/n)


def e21():
    magnitude = (n+1)/2**n
    rho = s.limit(s.simplify(magnitude.subs(n, n+1)/magnitude), n, s.oo)
    eq(rho, s.Rational(1, 2))
    assert rho < 1


def e22():
    for sign in [-1, 1]:
        eq(sign/(s.sqrt(n)+sign), sign*s.sqrt(n)/(n-1)-1/(n-1))
        eq(s.limit(sign/(s.sqrt(n)+sign), n, s.oo), 0)
    amplitude = s.sqrt(x)/(x-1)
    z = s.symbols("z", positive=True)
    assert s.simplify(s.diff(amplitude, x).subs(x, z+1)).is_negative
    eq(s.limit(amplitude, x, s.oo), 0)
    assert s.summation(1/(n-1), (n, 2, s.oo)) == s.oo


def tables():
    expected_geom = {1: "0.5", 2: "0.75", 3: "0.875", 4: "0.9375", 5: "0.96875", 10: "0.99902"}
    for count, expected in expected_geom.items():
        total = s.summation(1/2**n, (n, 1, count))
        digits = len(expected.split(".")[1])
        assert f"{float(total):.{digits}f}" == expected
    for count, expected in [(10, "2.93"), (100, "5.19"), (1000, "7.49"), (1000000, "14.39")]:
        total = np.sum(1/np.arange(1, count+1, dtype=np.float64))
        assert f"{total:.2f}" == expected
    for count, expected_sum, expected_tail in [(10, "1.5498", "0.0952"),
                                               (100, "1.6350", "0.0100"),
                                               (1000, "1.6439", "0.0010")]:
        total = np.sum(1/np.arange(1, count+1, dtype=np.float64)**2)
        tail = float(s.pi**2/6)-total
        assert f"{total:.4f}" == expected_sum
        assert f"{tail:.4f}" == expected_tail
        assert 1/(count+1) <= tail <= 1/count
    # Positive/negative terms of the rearranged alternating harmonic series.
    block = 1/(2*n-1)-1/(4*n-2)-1/(4*n)
    eq(block, (1/(2*n-1)-1/(2*n))/2)
    # Sum the convergent alternating series before grouping. SymPy splits
    # the rational block into divergent harmonic sums and returns nan.
    paired_total = s.summation((-1)**(n-1)/n, (n, 1, s.oo))/2
    eq(paired_total, s.log(2)/2)
    assert f"{float(paired_total):.4f}" == "0.3466"
    for leftover in [1/(2*n-1), 1/(2*n-1)-1/(4*n-2)]:
        eq(s.limit(leftover, n, s.oo), 0)


def zero_sum_counterexample():
    odd, even = 1/n, 1/n
    assert s.simplify(odd-even) == 0
    assert s.factor(even-odd.subs(n, n+1)).is_positive
    even_partial = s.summation(odd-even, (n, 1, N))
    eq(s.limit(even_partial, N, s.oo), 0)
    eq(s.limit(even_partial+1/(N+1), N, s.oo), 0)
    theorem = LESSON.split("**莱布尼茨判别法**", 1)[1].split("证明", 1)[0]
    assert r"0\le S\le u_1" in theorem


def followup_e02():
    term = 1/(n*(n+1))
    partial = s.summation(term, (n, 1, N))
    eq(partial, 1-1/(N+1))
    eq(s.limit(partial, N, s.oo), 1)
    assert r"> 求 $\sum\limits_{n=1}^\infty\dfrac1{n(n+1)}$ 的和。" in LESSON


def followup_e06():
    limit = s.limit(s.cos(1/n), n, s.oo)
    eq(limit, 1)
    assert limit != 0
    assert r"\cos\frac1n\to\cos0=1\ne0" in LESSON


def followup_e07():
    assert conv(n**(-s.Rational(5, 4)))
    assert not conv(n**(-s.Rational(3, 4)))
    assert r"p=\frac54>1$，收敛" in LESSON
    assert r"p=\frac34\le1$，发散" in LESSON


def followup_e09():
    term = 1/(n**2)**s.Rational(1, 3)
    assert not conv(term)
    assert conv(term**2)
    assert r"第一个 $p=\frac23\le1$，发散" in LESSON
    assert r"p=\frac43>1$，收敛" in LESSON


def followup_e10():
    term, upper = 1/(n*n+3), 1/n**2
    assert s.factor(upper-term).is_positive
    assert conv(upper)
    assert r"\frac1{n^2+3}\le\frac1{n^2}" in LESSON


def corrected_conditions():
    # The first harmonic group attains, rather than exceeds, its lower bound.
    k = s.symbols("k", integer=True, positive=True)
    eq(2**(k-1)/2**k, s.Rational(1, 2))
    eq(s.summation(1/n, (n, 2, 2)), s.Rational(1, 2))
    assert "第 1 组恰好等于" in LESSON
    amplitude = 1+1/n
    assert s.factor(amplitude-amplitude.subs(n, n+1)).is_positive
    eq(s.limit(amplitude, n, s.oo), 1)
    assert r"u_n=1+\frac1n" in LESSON
    # Discount alone does not control unbounded rewards.
    eq(s.Rational(1, 2)**n * 2**n, 1)
    assert not conv(s.S.One)


if __name__ == "__main__":
    assert [int(k) for k in re.findall(r"\*\*例 (\d+)\*\*", LESSON)] == list(range(1, 23))
    for index, work in enumerate([e01, e02, e03, e04, e05, e06, e07, e08, e09, e10, e11,
                                  e12, e13, e14, e15, e16, e17, e18, e19, e20, e21, e22], 1):
        run(f"例{index}", work)
    for index, work in [(2, followup_e02), (6, followup_e06), (7, followup_e07),
                        (9, followup_e09), (10, followup_e10)]:
        run(f"例{index}后随堂题", work)
    run("讲义数表与重排数值", tables)
    run("讲义第6节允许和为零", zero_sum_counterexample)
    run("讲义修订后的条件与反例", corrected_conditions)
    sys.exit(bool(failures))
