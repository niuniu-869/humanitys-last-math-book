"""Recompute answers from symbolic identities, limits and exact inequalities.

Expected values are assertions, never inputs to the computations. Text anchors
tie those assertions to answers.md. Infinite-series verdicts use analytic tests;
finite numerical sums are only supplemental checks.
"""
from pathlib import Path
import re
import sys

import numpy as np
import sympy as s

ROOT = Path(__file__).resolve().parents[1]
TEXT = (ROOT / "answers.md").read_text(encoding="utf-8")
PARTS = dict(re.findall(r"\*\*(C14-\d+)\*\*\n(.*?)(?=\n\*\*C14-|\Z)", TEXT, re.S))
n, k, N, m = s.symbols("n k N m", integer=True, positive=True)
x, T = s.symbols("x T", positive=True)
failures = 0


def eq(actual, expected):
    assert s.simplify(actual - expected) == 0, (actual, expected)


def anchors(pid, *snippets):
    for snippet in snippets:
        assert snippet in PARTS[pid], (pid, "answer text mismatch", snippet)


def run(label, work):
    global failures
    try:
        work()
        print("PASS", label)
    except Exception as exc:
        failures += 1
        print("FAIL", label, type(exc).__name__, str(exc))


def choice(pid, results):
    selected = re.search(r"\*\*答案：\*\* \(([A-D])\)", PARTS[pid]).group(1)
    for letter, actual in zip("ABCD", results):
        def check_option(letter=letter, actual=actual):
            assert bool(actual) == (letter == selected), (letter, actual, selected)
        run(f"{pid}({letter})", check_option)


def p01():
    partial = 3 - 2 / (n + 1)
    eq(partial.subs(n, 1), 2)
    term = s.factor(partial - partial.subs(n, n - 1))
    eq(term, 2 / (n * (n + 1)))
    eq(s.limit(partial, n, s.oo), 3)
    eq(partial.subs(n, 1) + s.summation(term, (n, 2, s.oo)), 3)
    anchors("C14-01", "$u_1=2$", "$u_n=2/[n(n+1)]$", "和为 $3$")


def p02():
    q = -s.Rational(2, 3)
    total = s.summation(q**k, (k, 0, s.oo))
    converges = abs(q) < 1
    choice("C14-02", [not converges, converges and total == s.Rational(3, 5),
                      converges and total == -s.Rational(2, 5),
                      converges and total == 3])
    eq(s.summation(q**k, (k, 1, s.oo)), -s.Rational(2, 5))


def p03():
    partial = 1 + (-1)**n / 2
    odd = s.limit(partial.subs(n, 2*k-1), k, s.oo)
    even = s.limit(partial.subs(n, 2*k), k, s.oo)
    term = s.simplify(partial - partial.subs(n, n-1))
    term_odd = s.limit(term.subs(n, 2*k-1), k, s.oo)
    term_even = s.limit(term.subs(n, 2*k), k, s.oo)
    converges = odd == even
    bounded = s.Rational(1, 2) <= odd <= even <= s.Rational(3, 2)
    choice("C14-03", [converges and odd == 1, bounded and converges,
                      not converges and term_odd == term_even == 1, odd != even])
    anchors("C14-03", "$S_{2k-1}=1/2$", "$S_{2k}=3/2$", "$u_n=S_n-S_{n-1}=(-1)^n$")


def p05():
    factor = (n+1)**2 / (n*(n+2))
    product = s.product(factor, (n, 1, N))
    eq(product, 2*(N+1)/(N+2))
    eq(s.limit(s.log(product), N, s.oo), s.log(2))
    # Each separate logarithmic series has an infinite partial-sum limit.
    for ratio in [(n+1)/n, (n+2)/(n+1)]:
        assert s.limit(s.log(s.product(ratio, (n, 1, N))), N, s.oo) == s.oo
    anchors("C14-05", r"S_N=\ln\dfrac{2(N+1)}{N+2}", "和为 $\\ln2$", "不能直接")


def p06():
    odd_term, even_term = 3/2**(2*k-1), 1/2**(2*k)
    eq(s.simplify(even_term/odd_term), s.Rational(1, 6))
    eq(s.simplify(odd_term.subs(k, k+1)/even_term), s.Rational(3, 2))
    roots = [s.limit(term**(1/index), k, s.oo)
             for term, index in [(odd_term, 2*k-1), (even_term, 2*k)]]
    for root in roots:
        eq(root, s.Rational(1, 2))
        assert root < 1
    assert s.summation(odd_term+even_term, (k, 1, s.oo)).is_finite
    anchors("C14-06", "奇数 $n$ 为 $1/6$", "偶数 $n$ 为 $3/2$", "根值极限为 $1/2$", "级数收敛")


def p07():
    b = s.symbols("b", positive=True)
    term = b**n*s.factorial(n)**2/s.factorial(2*n)
    ratio = s.combsimp(term.subs(n, n+1)/term)
    rho = s.limit(ratio, n, s.oo)
    eq(rho, b/4)
    region = s.solve_univariate_inequality(rho < 1, b, relational=False)
    region = region.intersect(s.Interval.open(0, s.oo))
    assert region == s.Interval.open(0, 4)
    boundary = s.solve(rho-1, b)[0]
    gap = s.factor(ratio.subs(b, boundary)-1)
    assert gap.is_positive
    eq(term.subs({b: boundary, n: 1}), 2)
    anchors("C14-07", "$0<b<4$ 时收敛", "$b\\ge4$ 时发散", "$u_n\\ge u_1=2$")


def p08():
    odd, even = 1/k, 1/k+1/k**2
    assert s.simplify(even-odd).is_positive
    pair = s.simplify(odd-even)
    even_partial = s.summation(pair, (k, 1, m))
    eq(s.limit(even_partial, m, s.oo), -s.pi**2/6)
    eq(s.limit(even_partial+1/(m+1), m, s.oo), -s.pi**2/6)
    assert s.Sum(odd+even, (k, 1, s.oo)).is_convergent() is s.false
    anchors("C14-08", "条件收敛", "$-\\pi^2/6$", "不能直接用莱布尼茨判别法")


def p09():
    a = 1/(n*s.log(n))
    premise_a = s.limit(n*a, n, s.oo) == 0
    integral_a = s.integrate(1/(x*s.log(x)), (x, 2, T))
    conclusion_a = s.limit(integral_a, T, s.oo).is_finite
    b = n**(-s.Rational(3, 2))
    premise_b = s.limit(n*n*b, n, s.oo) == s.oo
    conclusion_b = not bool(s.Sum(b, (n, 2, s.oo)).is_convergent())
    c = n**-2
    premise_c = s.limit(c.subs(n, n+1)/c, n, s.oo) == 1
    conclusion_c = not bool(s.Sum(c, (n, 2, s.oo)).is_convergent())
    upper = 1/(n*(n+1))
    upper_sum = s.summation(upper, (n, 2, s.oo))
    eq(upper_sum, s.Rational(1, 2))
    # C follows from the stated pointwise bound and a finite upper sum.
    choice("C14-09", [not (premise_a and not conclusion_a),
                      not (premise_b and not conclusion_b),
                      upper.is_positive and upper_sum.is_finite,
                      not (premise_c and not conclusion_c)])


def p10():
    magnitude = 1/(n*(n+1))
    eq(s.summation(magnitude, (n, 1, s.oo)), 1)
    assert s.factor(magnitude-magnitude.subs(n, n+1)).is_positive
    eq(s.limit(magnitude, n, s.oo), 0)
    term = (-1)**(n-1)*magnitude
    lower = s.summation(term, (n, 1, 4))
    upper = s.summation(term, (n, 1, 3))
    eq(lower, s.Rational(11, 30))
    eq(upper, s.Rational(5, 12))
    omitted = magnitude.subs(n, N+1)
    minimum = next(i for i in range(1, 100) if omitted.subs(N, i) < s.Rational(1, 200))
    assert minimum == 13
    assert omitted.subs(N, minimum-1) >= s.Rational(1, 200)
    # Numerical corroboration of the analytic odd/even partial-sum bounds.
    indices = np.arange(1, 20001, dtype=np.float64)
    partial = np.sum((-1.0)**(indices-1)/(indices*(indices+1)))
    assert float(lower) < partial < float(upper)
    anchors("C14-10", "绝对收敛", "$11/30\\le S\\le5/12$", "$N=13$")


def p12():
    p = s.symbols("p", real=True)
    domain = s.Interval.open(0, s.oo)
    bias = n**(-2*p)
    exponent = -bias.as_powers_dict()[n]
    convergent = s.solve_univariate_inequality(exponent > 1, p, relational=False).intersect(domain)
    absolute = s.solve_univariate_inequality(p > 1, p, relational=False).intersect(domain)
    conditional = convergent - absolute
    divergent = domain - convergent
    assert absolute == s.Interval.open(1, s.oo)
    assert conditional == s.Interval.Lopen(s.Rational(1, 2), 1)
    assert divergent == s.Interval.Lopen(0, s.Rational(1, 2))
    positive_p = s.symbols("r", positive=True)
    amplitude = x**(-positive_p)
    assert s.diff(amplitude, x).is_negative
    eq(s.limit(amplitude, x, s.oo), 0)
    # Both parity branches give the same absolute-comparison limit.
    for sign in [-1, 1]:
        eq(s.limit(s.Abs(sign+x**(-positive_p)), x, s.oo), 1)
        eq(s.limit(1+sign*x**(-positive_p), x, s.oo), 1)
    # Positive divergent bias plus a convergent alternating sum tends to +oo.
    assert s.summation(bias.subs(p, s.Rational(1, 2)), (n, 1, s.oo)) == s.oo
    anchors("C14-12", "$p>1$ 时绝对收敛", "$1/2<p\\le1$ 时条件收敛",
            "$0<p\\le1/2$ 时发散", "趋于 $+\\infty$")


def p04():
    y = s.Function("y")
    closed = s.rsolve(y(n+1)-(y(n)+2)/3, y(n), {y(1): 0})
    eq(closed, 1-3**(-(n-1)))
    eq(s.limit(closed, n, s.oo), 1)
    eq(s.summation(1-closed, (n, 1, s.oo)), s.Rational(3, 2))
    eq(s.summation(s.simplify(closed.subs(n, n+1)-closed), (n, 1, s.oo)), 1)
    anchors("C14-04", "$x_n=1-3^{-(n-1)}\\to1$", "第一个级数发散", "$3/2$、$1$")


def p13():
    term = s.integrate(x**(n-1)*(1-x)**2, (x, 0, 1))
    eq(term, 2/(n*(n+1)*(n+2)))
    partial = s.summation(term, (n, 1, N))
    eq(partial, s.Rational(1, 2)-1/((N+1)*(N+2)))
    eq(s.limit(partial, N, s.oo), s.Rational(1, 2))
    anchors("C14-13", "$u_n=2/[n(n+1)(n+2)]$",
            "$S_N=1/2-1/[(N+1)(N+2)]$", "和为 $1/2$")


def p14():
    term = s.exp(1/n)-1-1/n
    eq(s.limit(n*n*term, n, s.oo), s.Rational(1, 2))
    expansion = s.series(s.exp(x)-1-x, x, 0, 3).removeO()
    eq(expansion, x*x/2)
    assert s.Sum(n**-2, (n, 1, s.oo)).is_convergent() is s.true
    assert s.Sum(n**-1, (n, 1, s.oo)).is_convergent() is s.false
    anchors("C14-14", "极限为 $1/2$", "$\\sum d_n$ 收敛", "$\\sum nd_n$ 发散")


def p15():
    bound = 1/(n*(n+1))
    assert bound.is_positive
    total = s.summation(bound, (n, 1, s.oo))
    eq(total, 1)
    assert total.is_finite
    # A summable bound gives absolute convergence for every allowed update.
    M = N + m
    finite_tail = s.summation(bound, (n, N, M-1))
    eq(finite_tail, 1/N-1/M)
    tail = s.limit(finite_tail, m, s.oo)
    eq(tail, 1/N)
    minimum = next(i for i in range(1, 200) if tail.subs(N, i) < s.Rational(1, 100))
    assert minimum == 101
    # All-positive maximal updates attain the bound, including at N = 100.
    output = s.summation(bound, (n, 1, N-1))
    eq(output.subs(N, 1), 0)
    eq(output.subs(N, N+1)-output, bound.subs(n, N))
    eq(s.limit(output, N, s.oo)-output, tail)
    eq(tail.subs(N, minimum-1), s.Rational(1, 100))
    weak_output = s.summation(1/n, (n, 1, N-1))
    eq(weak_output.subs(N, 1), 0)
    eq(s.expand_func(weak_output.subs(N, N+1)-weak_output), 1/N)
    assert s.limit(weak_output, N, s.oo) == s.oo
    anchors("C14-15", "$|q-q_N|\\le1/N$", "$N=101$", "较弱上界不能保证收敛")


if __name__ == "__main__":
    expected = [f"C14-{i:02d}" for i in range(1, 16)]
    assert list(PARTS) == expected
    problems = (ROOT / "problems.md").read_text(encoding="utf-8")
    assert re.findall(r"^\*\*(C14-\d+)\*\*", problems, re.M) == expected
    assert re.findall(r"^\| (C14-\d+) \|", problems, re.M) == expected
    for index, work in [(1, p01), (2, p02), (3, p03), (4, p04), (5, p05),
                        (6, p06), (7, p07), (8, p08), (9, p09), (10, p10),
                        (12, p12), (13, p13), (14, p14), (15, p15)]:
        run(f"C14-{index:02d}", work)
    print("MANUAL C14-11 平方不等式、比较判别及绝对收敛的完整证明需人工复核")
    sys.exit(bool(failures))
