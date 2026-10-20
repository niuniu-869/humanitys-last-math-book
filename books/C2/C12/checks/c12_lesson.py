"""Independently check every numbered example and its immediate follow-up.

Improper integrals with interior poles or two infinite endpoints are split.
Example 14 uses NumPy quadrature after removing the logarithmic endpoint
singularity; convergence is checked separately by an exact comparison limit.
"""

import sys

import numpy as np
import sympy as s


x, t, r, eps, lam = s.symbols("x t r eps lam", positive=True)
a = s.symbols("a", real=True)
failures = 0


def need(actual, expected):
    if isinstance(actual, s.Set) or isinstance(expected, s.Set):
        ok = actual == expected
    else:
        ok = actual == expected or s.simplify(actual - expected) == 0
    assert ok, f"computed {actual}, expected {expected}"


def run(number, fn):
    global failures
    try:
        fn()
        print(f"PASS 例{number}")
    except Exception as exc:
        failures += 1
        print(f"FAIL 例{number} {type(exc).__name__}: {exc}")


def example01():
    need(s.integrate(s.exp(-lam * x), (x, 0, s.oo)), 1 / lam)
    need(s.integrate(x * s.exp(-x), (x, 0, s.oo)), 1)
    need(s.limit((r + 1) * s.exp(-r), r, s.oo), 0)
    need(s.integrate(s.exp(x), (x, -s.oo, 0)), 1)


def example02():
    for power, expected in [(2, 1 / s.log(2)), (1, s.oo)]:
        cutoff = s.integrate(1 / (x * s.log(x) ** power), (x, 2, r))
        need(s.limit(cutoff, r, s.oo), expected)


def example03():
    f = 1000 * s.exp(-s.Rational(5, 100) * t)
    need(s.integrate(f, (t, 0, s.oo)), 20000)
    finite_value = s.integrate(f, (t, 0, 100))
    need(finite_value, 20000 * (1 - s.exp(-5)))
    assert round(float(finite_value)) == 19865


def example04():
    density = 2 * s.exp(-2 * x)
    need(s.integrate(density, (x, 0, s.oo)), 1)
    need(s.integrate(x * density, (x, 0, s.oo)), s.Rational(1, 2))


def example05():
    f = 1 / (1 + x**2)
    left = s.integrate(f, (x, -s.oo, 0))
    right = s.integrate(f, (x, 0, s.oo))
    need(left, s.pi / 2)
    need(right, s.pi / 2)
    need(left + right, s.pi)
    odd = x / (1 + x**2)
    left_odd = s.limit(s.integrate(odd, (x, -r, 0)), r, s.oo)
    right_odd = s.limit(s.integrate(odd, (x, 0, r)), r, s.oo)
    need(left_odd, -s.oo)
    need(right_odd, s.oo)
    need(s.integrate(odd, (x, -r, r)), 0)


def example06():
    for power, expected in [(0, -1), (1, -s.Rational(1, 4))]:
        cutoff = s.integrate(x**power * s.log(x), (x, eps, 1))
        need(s.limit(cutoff, eps, 0, dir="+"), expected)
        need(s.limit(eps ** (power + 1) * s.log(eps), eps, 0, dir="+"), 0)


def example07():
    need(s.integrate(1 / s.sqrt(1 - x**2), (x, 0, 1)), s.pi / 2)
    f = 1 / (x - 1) ** 2
    for lo, hi in [(0, 1 - eps), (1 + eps, 2)]:
        cutoff = s.integrate(f, (x, lo, hi))
        need(s.limit(cutoff, eps, 0, dir="+"), s.oo)
    # The displayed -2 is explicitly the invalid endpoint subtraction.
    primitive = -1 / (x - 1)
    need(primitive.subs(x, 2) - primitive.subs(x, 0), -2)


def example08():
    f = 1 / (x * s.sqrt(x**2 - 1))
    primitive = s.atan(s.sqrt(x**2 - 1))
    need(s.diff(primitive, x), f)
    # Both endpoints are independently checked, with sqrt(2) as a split.
    left = primitive.subs(x, s.sqrt(2)) - s.limit(primitive, x, 1, dir="+")
    right = s.limit(primitive, x, s.oo) - primitive.subs(x, s.sqrt(2))
    need(left, s.pi / 4)
    need(right, s.pi / 4)
    need(left + right, s.pi / 2)


def example09():
    need(s.integrate(x**2 * s.exp(-x), (x, 0, s.oo)), 2)
    need(s.limit(x**2 * s.exp(-x), x, 0), 0)
    need(s.limit(x**2 * s.exp(-x), x, s.oo), 0)


def example10():
    f = 1 / s.sqrt(x**3 + x)
    g = x ** (-s.Rational(3, 2))
    need(s.limit(f / g, x, s.oo), 1)
    assert s.integrate(g, (x, 1, s.oo)).is_finite
    # The follow-up has a different tail exponent and diverges.
    other = x / s.sqrt(x**3 - 1)
    comparator = 1 / s.sqrt(x)
    need(s.limit(other / comparator, x, s.oo), 1)
    need(s.limit(s.integrate(comparator, (x, 2, r)), r, s.oo), s.oo)


def example11():
    need(s.integrate(s.exp(-x**2), (x, 0, s.oo)), s.sqrt(s.pi) / 2)
    need(s.integrate(s.exp(-x), (x, 1, s.oo)), s.exp(-1))
    domain = s.solve_univariate_inequality(x**2 >= x, x, relational=False)
    assert s.Interval(1, s.oo).is_subset(domain)


def example12():
    f = 1 / s.sqrt(x * (1 - x))
    need(s.limit(f * s.sqrt(x), x, 0, dir="+"), 1)
    need(s.limit(f * s.sqrt(1 - x), x, 1, dir="-"), 1)
    need(s.integrate(f, (x, 0, s.Rational(1, 2))), s.pi / 2)
    need(s.integrate(f, (x, s.Rational(1, 2), 1)), s.pi / 2)


def example13():
    f = x ** (-a) / (1 + x)
    slope = s.simplify(x * s.diff(f, x) / f)
    at_zero = s.limit(slope, x, 0)
    at_infinity = s.limit(slope, x, s.oo)
    need(s.limit(s.simplify(f * x**a), x, 0), 1)
    need(s.limit(s.simplify(f * x ** (a + 1)), x, s.oo), 1)
    near_set = s.solve_univariate_inequality(at_zero > -1, a, relational=False)
    far_set = s.solve_univariate_inequality(at_infinity < -1, a, relational=False)
    need(near_set.intersect(far_set), s.Interval.open(0, 1))
    need(at_zero.subs(a, 2), -2)
    need(at_infinity.subs(a, 2), -3)


def example14():
    # On a sufficiently short interval, log(sin x)<0, so this is |log(sin x)|.
    need(s.limit(-s.sqrt(x) * s.log(s.sin(x)), x, 0, dir="+"), 0)
    assert s.integrate(1 / s.sqrt(x), (x, 0, 1)).is_finite
    # x=(pi/2)u^2 replaces log(x) by an integrable u*log(u) endpoint.
    expected = -np.pi * np.log(2) / 2
    values = []
    for order in (256, 512):
        nodes, weights = np.polynomial.legendre.leggauss(order)
        u = (nodes + 1) / 2
        value = np.dot(weights / 2, np.pi * u * np.log(np.sin(np.pi * u**2 / 2)))
        values.append(value)
        assert abs(value - expected) < 2e-9, (order, value, expected)
    assert abs(values[1] - values[0]) < 2e-9


def example15():
    need(s.integrate(x**3 * s.exp(-2 * x), (x, 0, s.oo)), s.Rational(3, 8))
    need(s.integrate(x**4 * s.exp(-x / 3), (x, 0, s.oo)), 5832)


def example16():
    for power, expected in [(3, s.Rational(1, 2)), (2, s.sqrt(s.pi) / 4)]:
        need(s.integrate(x**power * s.exp(-x**2), (x, 0, s.oo)), expected)
    m = s.symbols("m", positive=True)
    actual = s.integrate(x**m * s.exp(-x**2), (x, 0, s.oo))
    need(s.gammasimp(actual), s.gamma((m + 1) / 2) / 2)


def example17():
    # Integrate the defining density, rather than copying the recurrence.
    need(s.integrate(x ** s.Rational(5, 2) * s.exp(-x), (x, 0, s.oo)), 15 * s.sqrt(s.pi) / 8)


def example18():
    n = s.symbols("n", integer=True, positive=True)
    transformed = s.simplify(s.log(1 / x).subs(x, s.exp(-t)) ** n * s.exp(-t))
    need(transformed, t**n * s.exp(-t))
    actual = s.integrate(transformed, (t, 0, s.oo))
    need(s.combsimp(actual), s.factorial(n))


if __name__ == "__main__":
    examples = [
        example01, example02, example03, example04, example05, example06,
        example07, example08, example09, example10, example11, example12,
        example13, example14, example15, example16, example17, example18,
    ]
    for number, fn in enumerate(examples, 1):
        run(number, fn)
    print("MANUAL 例18 证明：人工核对截断换元与端点对应；一般积分恒等式已作符号验算")
    sys.exit(bool(failures))
