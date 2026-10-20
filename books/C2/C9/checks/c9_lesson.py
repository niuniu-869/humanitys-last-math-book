"""Recalculate all 15 numbered examples without altering lesson.md.

General existence in Example 15 remains a manual proof. Its numerical
coefficient and interval length are checked separately. Examples 12-13
have definite answers and are checked by symbolic squeezing, not MANUAL.
"""
import sys

import numpy as np
import sympy as s
from sympy.calculus.util import continuous_domain, function_range


x = s.symbols("x", real=True)
b = s.symbols("b", positive=True)
n, i = s.symbols("n i", integer=True, positive=True)
R = s.Rational
failures = 0


def same(actual, expected):
    if isinstance(actual, (list, tuple)):
        return len(actual) == len(expected) and all(same(v, w) for v, w in zip(actual, expected))
    if actual == expected:
        return True
    if isinstance(actual, (s.Set, bool, np.bool_, s.logic.boolalg.BooleanAtom)):
        return actual == expected
    return s.simplify(s.sympify(actual) - s.sympify(expected)) == 0


def need(actual, expected):
    if not same(actual, expected):
        raise AssertionError(f"computed {actual}; expected {expected}")


def example1():
    total = s.summation((2 * i / n) * (2 / n), (i, 1, n))
    need(total, 2 * (1 + 1 / n))
    need(s.limit(total, n, s.oo), 2)
    need(s.integrate(x, (x, 0, 2)), 2)


def example2():
    total = s.summation((i * b / n)**2 * b / n, (i, 1, n))
    need(total, b**3 * (1 + 1 / n) * (2 + 1 / n) / 6)
    result = s.limit(total, n, s.oo)
    need(result, b**3 / 3)
    need([result.subs(b, v) for v in (1, 2, 3)], [R(1, 3), R(8, 3), 9])
    need(result, s.integrate(x**2, (x, 0, b)))


def example3():
    times = np.array([0, 1, 2, 3, 4])
    speeds = np.array([0.4, 0.8, 1.0, 1.2, 1.4])
    widths = np.diff(times)
    left = np.dot(speeds[:-1], widths)
    right = np.dot(speeds[1:], widths)
    need(bool(np.all(np.diff(speeds) > 0)), True)
    need(bool(np.allclose([left, right, (left + right) / 2], [3.4, 4.4, 3.9],
                         rtol=0, atol=1e-12)), True)


def example4():
    need(s.solve(x - 1, x), [1])
    need([s.integrate(x - 1, (x, lo, hi)) for lo, hi in [(0, 1), (1, 3), (0, 3)]],
         [-R(1, 2), 2, R(3, 2)])


def example5():
    points = [(0, 0), (R(1, 5), R(3, 5)), (R(1, 2), R(4, 5)), (1, 1)]
    pieces = []
    for (u, v), (w, z) in zip(points, points[1:]):
        line = v + (z - v) * (x - u) / (w - u)
        pieces.append(s.integrate(line, (x, u, w)))
    need(pieces, [R(6, 100), R(21, 100), R(45, 100)])
    need(sum(pieces), R(72, 100))
    need(sum(pieces) > s.integrate(x, (x, 0, 1)), True)


def example6():
    floor_jumps = [j for j in range(1, 4)
                   if s.limit(s.floor(x), x, j, dir="-") != s.floor(j)]
    need(floor_jumps, [1, 2, 3])
    floor_values = s.FiniteSet(*(s.floor(R(j, 2)) for j in range(7)))
    need(floor_values, s.FiniteSet(0, 1, 2, 3))
    floor_ok = all(value.is_finite for value in floor_values) and len(floor_jumps) < s.oo
    # Check the bound and continuity away from zero, rather than infer
    # discontinuities from finitely sampled oscillations.
    need(function_range(s.sin(x), x, s.S.Reals), s.Interval(-1, 1))
    domain = continuous_domain(s.sin(1 / x), x, s.Interval.Lopen(0, 1))
    need(domain, s.Interval.Lopen(0, 1))
    positive_peaks = 1 / (2 * s.pi * n + s.pi / 2)
    negative_peaks = 1 / (2 * s.pi * n + 3 * s.pi / 2)
    need([s.limit(t, n, s.oo) for t in (positive_peaks, negative_peaks)], [0, 0])
    need([s.simplify(s.sin(1 / t)) for t in (positive_peaks, negative_peaks)], [1, -1])
    sine_ok = domain == s.Interval.Lopen(0, 1)
    unbounded_limit = s.limit(1 / s.sqrt(x), x, 0, dir="+")
    need(unbounded_limit, s.oo)
    need([bool(floor_ok), sine_ok, bool(unbounded_limit.is_finite)], [True, True, False])


def example7():
    need(s.integrate(3 * x**2 - 2 * x + 5, (x, 0, 1)), 5)


def example8():
    # Solve for integrals over the three disjoint segments.
    u, v, w = s.symbols("u v w")
    values = s.solve([u - 3, u + v + w - 7, w - 1], (u, v, w))
    need((values[v], -values[v] - values[w]), (3, -4))


def example9():
    need(s.integrate(s.Abs(x - 1), (x, 0, 3)), R(5, 2))


def example10():
    values = [s.integrate(f, (x, lo, hi)) for lo, hi in [(0, 1), (1, 2)]
              for f in [x, x**2]]
    need(values, [R(1, 2), R(1, 3), R(3, 2), R(7, 3)])
    need((values[0] > values[1], values[2] < values[3]), (True, True))


def example11():
    f = s.exp(-x**2)
    need(function_range(f, x, s.Interval(0, 1)), s.Interval(s.exp(-1), 1))
    edges = [s.S.Zero, R(1, 2), s.S.One]
    lower = sum((v - u) * f.subs(x, v) for u, v in zip(edges, edges[1:]))
    upper = sum((v - u) * f.subs(x, u) for u, v in zip(edges, edges[1:]))
    need((lower, upper), ((s.exp(-R(1, 4)) + s.exp(-1)) / 2,
                         (1 + s.exp(-R(1, 4))) / 2))
    exact = s.integrate(f, (x, 0, 1))
    value = float(exact.evalf(30))
    need(float(lower) <= value <= float(upper), True)
    need(abs(value - 0.7468) < 0.00005, True)
    # Printed decimal ranges are checked as inequalities themselves,
    # since rounded endpoints cannot replace an exact bound logically.
    need(0.367 <= value <= 1 and 0.573 <= value <= 0.890, True)
    need(bool(np.allclose([float(s.exp(-1)), float(s.exp(-R(1, 4))),
                           float(lower), float(upper)],
                          [0.368, 0.779, 0.573, 0.889], rtol=0, atol=0.0005)), True)


def vanishing_integral(endpoint):
    # On [0, endpoint], 0 <= x^n/(1+x) <= x^n. Verify the factor
    # responsible for this bound over the whole interval symbolically.
    gap = s.cancel(1 - 1 / (1 + x))
    bounds = function_range(gap, x, s.Interval(0, endpoint))
    need(bounds.inf >= 0, True)
    need(x.is_real, True)
    upper = s.integrate(x**n, (x, 0, endpoint))
    need(s.limit(upper, n, s.oo), 0)
    # Independent positive quadrature for several n, including larger n.
    nodes, weights = np.polynomial.legendre.leggauss(100)
    samples = float(endpoint) * (nodes + 1) / 2
    for power in [1, 2, 8, 32, 64]:
        value = float(endpoint) / 2 * np.dot(weights, samples**power / (1 + samples))
        cap = float(upper.subs(n, power))
        need(0 < value <= cap + 1e-13, True)


def example12():
    vanishing_integral(R(1, 2))
    cap = R(1, 2) * R(1, 2)**n
    need(s.limit(cap, n, s.oo), 0)


def example13():
    vanishing_integral(s.S.One)
    delta = s.symbols("delta", positive=True)
    # Fix 0 < delta < 1 by parameterizing delta=1/(1+t), t>0.
    t = s.symbols("t", positive=True)
    cap = (1 - delta)**n + delta
    fixed_cap = cap.subs(delta, 1 / (1 + t))
    need(s.limit(fixed_cap, n, s.oo), 1 / (1 + t))


def example14():
    average = s.integrate(x**2, (x, 0, 2)) / 2
    roots = s.solveset(x**2 - average, x, domain=s.Interval(0, 2))
    need(average, R(4, 3))
    need(roots, s.FiniteSet(2 / s.sqrt(3)))
    need(abs(float(2 / s.sqrt(3)) - 1.155) < 0.0005, True)


def example15():
    # Only check the cancellation and separation of the two points.
    interval = s.Interval(0, R(1, 2))
    need(2 * interval.measure, 1)
    need(interval.sup < 1, True)


def supplementary():
    # Unnumbered computations cited in the review are checked independently.
    need((R(14, 64), R(30, 64)), (R(7, 32), R(15, 32)))
    need(s.summation(i**2, (i, 1, n)), n * (n + 1) * (2 * n + 1) / 6)
    need(s.integrate(s.sqrt(4 - x**2), (x, -2, 2)), 2 * s.pi)
    need(s.integrate(s.Abs(x), (x, -1, 1)), 1)
    need(s.integrate(x, (x, -1, 2)), R(3, 2))
    need(s.integrate(x, (x, 0, 1)) ** 2, R(1, 4))


try:
    supplementary()
    print("PASS 补充核对")
except Exception as exc:
    failures += 1
    print(f"FAIL 补充核对 {type(exc).__name__}: {exc}")


for number in range(1, 16):
    try:
        globals()[f"example{number}"]()
        suffix = " 系数与区间核对" if number == 15 else ""
        print(f"PASS 例{number}{suffix}")
    except Exception as exc:
        failures += 1
        print(f"FAIL 例{number} {type(exc).__name__}: {exc}")
    if number == 15:
        print("MANUAL 例15 证明：积分中值点不超过 1/2，与端点 1 不同，罗尔条件齐全")
sys.exit(bool(failures))
