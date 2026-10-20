"""Independently recompute the exercises; expected values mirror answers.md.

Symbolic identities, convergence tests and high-precision numerics are used
instead of finite partial sums as evidence of convergence. Text anchors tie
the expected values to the published answers. Only C15-11 is a proof.
"""
import re
import sys
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
TEXT = (ROOT / "answers.md").read_text(encoding="utf-8")
BLOCKS = dict(re.findall(
    r"\*\*(C15-\d+)\*\*\n(.*?)(?=\n\*\*C15-|\Z)", TEXT, re.S
))
n = sp.symbols("n", integer=True, positive=True)
x, u = sp.symbols("x u", real=True)
q = sp.symbols("q", positive=True)
failures = 0


def equal(a, b):
    return sp.simplify(a - b) == 0


def converges(term, start=1):
    term = sp.simplify(term)
    if sp.Sum(sp.simplify(abs(term)), (n, start, sp.oo)).is_convergent():
        return True
    return bool(sp.Sum(term, (n, start, sp.oo)).is_convergent())


def branch(expression):
    expression = sp.piecewise_fold(expression)
    return expression.args[0][0] if isinstance(expression, sp.Piecewise) else expression


def interior(term):
    ratio = sp.limit(sp.simplify(abs(term.subs(n, n + 1) / term)), n, sp.oo)
    return sp.solve_univariate_inequality(ratio < 1, x, relational=False)


def closed_domain(term, radius, center=0):
    left, right = center - radius, center + radius
    return sp.Interval(left, right,
                       left_open=not converges(term.subs(x, left)),
                       right_open=not converges(term.subs(x, right)))


def check(pid, test, anchors=(), suffix=""):
    global failures
    try:
        assert all(a in BLOCKS[pid] for a in anchors), "answer text differs"
        assert bool(test()), "computed result differs"
    except Exception as exc:
        failures += 1
        print(f"FAIL {pid}{suffix}: {type(exc).__name__}: {exc}")
    else:
        print(f"PASS {pid}{suffix}")


def choice(pid, actual, selected):
    match = re.search(r"\*\*答案：\*\* \(([A-D])\)", BLOCKS[pid])
    for label, result in zip("ABCD", actual):
        check(pid, lambda r=result, k=label: bool(r) == (k == selected)
              and match is not None and match[1] == selected,
              suffix=f" ({label})")


def problem01():
    domain = sp.solve_univariate_inequality(abs(2 - x**2) < 1, x, relational=False)
    wanted = sp.Union(sp.Interval.open(-sp.sqrt(3), -1),
                      sp.Interval.open(1, sp.sqrt(3)))
    total = branch(sp.summation(q**n, (n, 0, sp.oo)))
    return domain == wanted and equal(total.subs(q, 2 - x**2), 1 / (x**2 - 1))


def problem03():
    f = x**2 * (sp.exp(x) - 1)
    return (equal(sp.series(f, x, 0, 6).removeO(), x**3 + x**4/2 + x**5/6)
            and sp.diff(f, x, 5).subs(x, 0) == 20)


def problem04():
    t = sp.Rational(1, 5)
    approximation = 1 - t**2 / 2
    first_omitted = t**4 / sp.factorial(4)
    error = sp.N(sp.cos(t) - approximation, 50)
    term = t**(2*n) / sp.factorial(2*n)
    ratio = sp.simplify(term.subs(n, n + 1) / term)
    return (approximation == sp.Rational(49, 50)
            and first_omitted == sp.Rational(1, 15000)
            and 0 < error < first_omitted < sp.Rational(1, 10000)
            and ratio.subs(n, 2) < 1
            and sp.diff(ratio, n).is_negative
            and sp.limit(term, n, sp.oo) == 0)


def problem05():
    # max_{|x|<=1} |x|^n/(n*2^n) = 1/(n*2^n).
    magnitude = q**n / (n * 2**n)
    maximum = magnitude.subs(q, 1)
    bound = 2**(-n)
    return (sp.diff(magnitude, q).is_positive
            and sp.simplify(bound - maximum).is_nonnegative
            and sp.summation(bound, (n, 1, sp.oo)) == 1
            and sp.denom(x**n/(n*2**n)).has(x) is False)


def problem07():
    term = x**(n+1)/(n*(n+1))
    proposed = x + (1-x)*sp.log(1-x)
    twice = branch(sp.summation(sp.diff(term, x, 2), (n, 1, sp.oo)))
    left = sp.summation(term.subs(x, -1), (n, 1, sp.oo))
    right = sp.summation(term.subs(x, 1), (n, 1, sp.oo))
    return (interior(term) == sp.Interval.open(-1, 1)
            and closed_domain(term, 1) == sp.Interval(-1, 1)
            and equal(sp.diff(proposed, x, 2), twice)
            and proposed.subs(x, 0) == 0
            and sp.diff(proposed, x).subs(x, 0) == 0
            and equal(left, 2*sp.log(2)-1) and right == 1)


def problem08():
    f = sp.log(x) + sp.log(2-x)
    term = -(x-1)**(2*n)/n
    polynomial = sp.Add(*(term.subs(n, j) for j in range(1, 6)))
    radius_ratio = sp.limit(sp.simplify(abs(term.subs(n, n+1)/term)), n, sp.oo)
    return (equal(sp.series(f, x, 1, 11).removeO(), polynomial)
            and equal(sp.diff(f, x), sp.diff(sp.log(1-(x-1)**2), x))
            and sp.diff(f, x, 5).subs(x, 1) == 0
            and sp.diff(f, x, 6).subs(x, 1) == -240
            and equal(radius_ratio, (x-1)**2)
            and closed_domain(term, 1, center=1) == sp.Interval.open(0, 2))


def problem09():
    omega = sp.expand_complex(sp.exp(sp.I*sp.pi/3))
    terms = [sp.expand_complex(sp.exp(sp.I*k*sp.pi/3)) for k in range(20)]
    # A six-term zero block and period six reduce every N to six residues.
    residues = [sp.simplify(sum(terms[:r])) for r in range(6)]
    return (equal(omega**6, 1) and omega != 1
            and all(equal(terms[k+3], -terms[k]) for k in range(3))
            and equal(sum(terms[:6]), 0)
            and [r for r, value in enumerate(residues) if value == 0] == [0]
            and equal(sum(terms), sp.Rational(3, 2)+sp.sqrt(3)*sp.I/2))


def flat_taylor_facts():
    h = sp.exp(-1/x**2)
    # All derivatives of h at zero are supplied in the question. For n>=1,
    # D^n[(x+c)h] = (x+c)h^(n) + n*h^(n-1), hence the correction vanishes.
    hn, hprev, c = sp.symbols("hn hprev c")
    correction = (x+c)*hn+n*hprev
    assert correction.subs({x: 0, hn: 0, hprev: 0}) == 0
    for gap in ((x-1)*h, (x+1)*h):
        assert all(sp.limit(sp.diff(gap, x, j), x, 0, dir=side) == 0
                   for j in range(4) for side in ("+", "-"))
    coefficient = 1/sp.factorial(n)
    ratio = sp.limit(coefficient.subs(n, n+1)/coefficient, n, sp.oo)
    total = sp.summation(x**n/sp.factorial(n), (n, 0, sp.oo))
    t = sp.symbols("t", real=True)
    assert sp.exp(-t**2).is_positive  # t=1/x: h has no nonzero real zeros.
    assert equal(total, sp.exp(x))
    f_points = sp.solveset(x-1, x, domain=sp.S.Reals) | sp.FiniteSet(0)
    g_points = sp.solveset(x+1, x, domain=sp.S.Reals) | sp.FiniteSet(0)
    domain = sp.S.Reals if ratio == 0 else None
    actual = (domain, f_points, g_points)
    options = [
        (sp.Interval.open(-1, 1), sp.FiniteSet(0), sp.FiniteSet(0)),
        (sp.S.Reals, sp.S.Reals, sp.S.Reals),
        (sp.S.Reals, sp.FiniteSet(0, 1), sp.FiniteSet(-1, 0)),
        (sp.S.Reals, sp.FiniteSet(0), sp.FiniteSet(0)),
    ]
    return [actual == option for option in options]


def problem12():
    a = sp.symbols("a0:10")
    candidate = sum(a[j]*x**j for j in range(10))
    residual = sp.expand((1-x)*sp.diff(candidate, x)-2*candidate-1)
    equations = [a[0]] + [residual.coeff(x, j) for j in range(9)]
    solution = sp.solve(equations, a, dict=True)[0]
    formula = (n+1)/2
    total = (1/(1-x)**2-1)/2
    term = formula*x**n
    return (all(solution[a[j]] == sp.Rational(j+1, 2) for j in range(1, 10))
            and solution[a[0]] == 0
            and equal((n+1)*formula.subs(n, n+1), (n+2)*formula)
            and equal((1-x)*sp.diff(total, x)-2*total, 1)
            and total.subs(x, 0) == 0
            and equal(branch(sp.summation(term, (n, 1, sp.oo))), total)
            and interior(term) == sp.Interval.open(-1, 1)
            and closed_domain(term, 1) == sp.Interval.open(-1, 1))


def problem13():
    return sp.limit((sp.log(1+x)-x+x**2/2)/(sp.sin(x)-x), x, 0) == -2


def problem14():
    integral = sp.integrate(x**2/(1+x**2), (x, 0, sp.Rational(1, 2)))
    term = (-1)**n/((2*n+3)*2**(2*n+3))
    series = sp.summation(term, (n, 0, sp.oo))
    term_integral = sp.integrate((-1)**n*x**(2*n+2), (x, 0, sp.Rational(1, 2)))
    expected = sp.Rational(1, 2)-sp.atan(sp.Rational(1, 2))
    return (equal(integral, expected) and equal(series, expected)
            and equal(term_integral, term) and converges(abs(term), 0))


def problem15():
    total = branch(sp.summation((n-1)*x**n, (n, 2, sp.oo)))
    critical = sp.solve(sp.diff(total, x), x)
    points = [sp.Rational(-1, 2), sp.Rational(1, 2)] + critical
    values = [(sp.simplify(total.subs(x, p)), p) for p in points]
    return (equal(total, x**2/(1-x)**2) and critical == [0]
            and min(values) == (0, 0) and max(values) == (1, sp.Rational(1, 2)))


if __name__ == "__main__":
    assert set(BLOCKS) == {f"C15-{k:02}" for k in range(1, 16)}
    check("C15-01", problem01, (r"(-\sqrt3,-1)\cup(1,\sqrt3)", r"\frac1{x^2-1}"))
    term02 = (x+1)**(2*n)/(9**n*n**2)
    interval02 = interior(term02)
    radius02 = (interval02.end-interval02.start)/2
    domain02 = closed_domain(term02, radius02, -1)
    options02 = [(9, sp.Interval(-10, 8)), (3, sp.Interval.open(-4, 2)),
                 (3, sp.Interval(-3, 3)), (3, sp.Interval(-4, 2))]
    choice("C15-02", [radius02 == r and domain02 == d for r, d in options02], "D")
    check("C15-03", problem03, (r"x^3+\frac{x^4}{2}+\frac{x^5}{6}", r"f^{(5)}(0)=20"))
    check("C15-04", problem04, (r"\frac{49}{50}", r"偏小", r"\frac1{15000}"))
    check("C15-05", problem05, (r"M_n=2^{-n}", r"M_n=1", "级数一致收敛", "上连续"))
    g_term = (-1)**(n-1)*2**n*x**n/n
    derivative = sp.diff(g_term, x)
    antiderivative = (-1)**(n-1)*2**n*x**(n+1)/(n*(n+1))
    interval06 = interior(g_term)
    radius06 = interval06.end
    pair06 = (closed_domain(derivative, radius06), closed_domain(antiderivative, radius06))
    open_half = sp.Interval.open(-sp.Rational(1, 2), sp.Rational(1, 2))
    closed_half = sp.Interval(-sp.Rational(1, 2), sp.Rational(1, 2))
    original_half = sp.Interval.Lopen(-sp.Rational(1, 2), sp.Rational(1, 2))
    options06 = [(original_half, original_half), (sp.Interval.open(-1, 1), sp.Interval(-1, 1)),
                 (open_half, closed_half), (open_half, open_half)]
    choice("C15-06", [pair06 == option for option in options06], "C")
    check("C15-07", problem07, (r"[-1,1]", r"x+(1-x)\ln(1-x)", r"S(1)=1", r"S(-1)=2\ln2-1"))
    check("C15-08", problem08, (r"\frac{(x-1)^{2n}}n", r"0<x<2", r"f^{(5)}(1)=0", r"f^{(6)}(1)=-240"))
    check("C15-09", problem09, (r"N=6j", r"S_{20}=\frac32+\frac{\sqrt3}{2}i"))
    choice("C15-10", flat_taylor_facts(), "C")
    print("MANUAL C15-11 阿贝尔定理的有界通项证明；人工逐步核对")
    check("C15-12", problem12, (r"a_0=0", r"a_1=1", r"(n+1)a_{n+1}=(n+2)a_n",
                               r"a_n=\frac{n+1}{2}", r"\frac12\left(\frac1{(1-x)^2}-1\right)", r"(-1,1)"))
    check("C15-13", problem13, (r"极限为 $-2$",))
    check("C15-14", problem14, (r"\frac12-\arctan\frac12",))
    check("C15-15", problem15, (r"最小值为 $0$", r"$x=0$", r"最大值为 $1$", r"$x=\frac12$"))
    sys.exit(bool(failures))
