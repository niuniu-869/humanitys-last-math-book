"""Compute from the question expressions; constants on the right are answer targets."""

from pathlib import Path
import re

import sympy as s

x = s.symbols("x", real=True)
R = s.Rational
failed = 0
answers = (Path(__file__).resolve().parents[1] / "answers.md").read_text()
problems = (Path(__file__).resolve().parents[1] / "problems.md").read_text()


def equal(actual, expected):
    assert s.simplify(actual - expected) == 0, (actual, expected)


def limit(expr, point=0, direction="+-"):
    return s.limit(expr, x, point, dir=direction)


def options(number, actual, expected):
    for letter, value, target in zip("ABCD", actual, expected):
        assert bool(value) == target, (letter, value, target)
        print(f"PASS C7-{number:02d}({letter})")


def p01():
    f, g = 2 + s.sin(x), 3 + x
    value = limit(f / g)
    derivative_value = limit(s.diff(f, x) / s.diff(g, x))
    equal(value, R(2, 3))
    equal(derivative_value, 1)
    options(1, [value == 1, value == R(2, 3) and limit(g) != 0,
                value == 0, value.is_finite is False], [False, True, False, False])


def p02():
    f, g = s.log(1 + x) - s.log(1 - x), s.sin(3 * x)
    equal(limit(f), 0)
    equal(limit(g), 0)
    equal(limit(s.diff(g, x)), 3)
    equal(limit(f / g), R(2, 3))
    equal(limit(s.diff(f, x) / s.diff(g, x)), R(2, 3))


def p03():
    polynomials = [3 - 2 * (x - 2) + 6 * (x - 2)**2,
                   3 - 2 * x + 3 * x**2,
                   3 - 2 * (x - 2) + 3 * (x - 2)**2,
                   3 + 2 * (x - 2) + 3 * (x - 2)**2]
    jets = [[s.diff(p, x, k).subs(x, 2) for k in range(3)] for p in polynomials]
    options(3, [jet == [3, -2, 6] for jet in jets], [False, False, True, False])


def p04():
    f = s.exp(x)
    polynomial = s.series(f, x, 0, 3).removeO()
    value = polynomial.subs(x, -R(1, 10))
    equal(value, R(905, 1000))
    third = s.diff(f, x, 3)
    assert s.diff(third, x).is_positive
    bound = third.subs(x, 0) * R(1, 10)**3 / s.factorial(3)
    equal(bound, R(1, 6000))
    error = (value - f.subs(x, -R(1, 10))).evalf(50)
    assert 0 < error < bound


def p05():
    f = s.log(1 + x) / (1 + x)
    target = x - R(3, 2) * x**2 + R(11, 6) * x**3
    for k in range(4):
        equal(s.diff(f, x, k).subs(x, 0), s.diff(target, x, k).subs(x, 0))
    equal(s.diff(f, x, 3).subs(x, 0), 11)
    equal(limit((f - target) / x**3), 0)


def p06():
    exponent = (s.log(1 + x) - x) / x**2
    equal(s.exp(limit(exponent)), s.exp(-R(1, 2)))
    replacement = s.exp(s.log(1 + x) / x**2)
    equal(limit(replacement, direction="-"), 0)
    assert limit(replacement, direction="+") == s.oo


def p07():
    a = s.symbols("a", real=True)
    numerator = s.log(1 + x) - x + a * x**2
    pole_coefficient = limit(numerator / x**2)
    assert s.solve(pole_coefficient, a) == [R(1, 2)]
    equal(limit(numerator.subs(a, R(1, 2)) / x**3), R(1, 3))
    k = s.symbols("k", positive=True)
    for sign in [-1, 1]:
        expr = numerator.subs(a, R(1, 2) + sign * k) / x**3
        assert limit(expr, direction="+") == sign * s.oo
        assert limit(expr, direction="-") == -sign * s.oo


def p08():
    f = s.sin(x**2) - x**2
    sixth, fifth = limit(f / x**6), limit(f / x**5)
    equal(sixth, -R(1, 6))
    options(8, [sixth == 0, limit(f / (-x**6 / 6)) == 1,
                fifth.is_finite and fifth != 0,
                limit((f + x**3 / 6) / x**3) == 0], [False, True, False, False])


def p10():
    f, endpoint = s.log(1 + x), R(1, 5)
    bounds = []
    for n in range(1, 5):
        # The derivative magnitude decreases on this whole interval.
        magnitude = (-1)**n * s.diff(f, x, n + 1)
        positive_x = s.symbols("positive_x", nonnegative=True)
        assert s.diff(magnitude, x).subs(x, positive_x).is_negative
        maximum = magnitude.subs(x, 0)
        equal(maximum, s.factorial(n))
        bounds.append(maximum * endpoint**(n + 1) / s.factorial(n + 1))
    assert next(i + 1 for i, bound in enumerate(bounds) if bound < R(1, 10000)) == 4
    equal(bounds[2], R(1, 2500))
    equal(bounds[3], R(1, 15625))
    polynomial = s.series(f, x, 0, 5).removeO()
    value = polynomial.subs(x, endpoint)
    equal(value, R(1367, 7500))
    assert 0 < (f.subs(x, endpoint) - value).evalf(50) < bounds[-1]
    positive_x = s.symbols("positive_x", positive=True)
    assert s.diff(f, x, 5).subs(x, positive_x).is_positive


def p09():
    h = s.symbols("h", positive=True)
    # The remainder identity reduces the symmetric difference to two
    # second-derivative values, each lying in [2, 6].
    lower = (R(2) + R(2)) / 4 * h**2
    upper = (R(6) + R(6)) / 4 * h**2
    equal(lower, h**2)
    equal(upper, 3 * h**2)
    t = s.symbols("t", real=True)
    equal(((t**2).subs(t, h) + (t**2).subs(t, -h)) / 2 - (t**2).subs(t, 0), h**2)
    equal(((3*t**2).subs(t, h) + (3*t**2).subs(t, -h)) / 2 - (3*t**2).subs(t, 0), 3*h**2)
    print("MANUAL C7-09 对称差式的中值点证明；取等函数已代数核对")


def p11():
    # These are arbitrary vanishing remainder factors, not one example f.
    ep, em, eta = s.symbols("ep em eta", real=True)
    plus = 2 * x + (-R(3, 2) + ep) * x**2
    minus = -2 * x + (-R(3, 2) + em) * x**2
    q1 = (plus + minus) / (1 - s.cos(2 * x))
    equal(limit(q1).subs({ep: 0, em: 0}), -R(3, 2))
    # MVT gives exactly f'(xi)*(sin(x)-x), with f'(xi)=2+eta, eta -> 0.
    q2 = (2 + eta) * (s.sin(x) - x) / x**3
    equal(limit(q2).subs(eta, 0), -R(1, 3))
    # o(x^2) alone need not remain small after division by x^3.
    remainder = x**3
    equal(limit(remainder / x**2), 0)
    assert limit(remainder / x**3) != 0


def p12():
    a = s.symbols("a", real=True)
    numerator = s.log(1 + x) - x + x**2 / 2
    denominator = s.sin(a * x) - a * s.sin(x)
    nc, dc = limit(numerator / x**3), limit(denominator / x**3)
    excluded = s.solve(dc, a)
    assert excluded == [-1, 0, 1]
    for value in excluded:
        equal(denominator.subs(a, value), 0)
    equal(nc / dc, 2 / (a * (1 - a**2)))
    positive_set = s.solve_univariate_inequality(nc / dc > 0, a, relational=False)
    assert positive_set == s.Union(s.Interval.open(-s.oo, -1), s.Interval.open(0, 1))


def p13():
    f = (s.exp(x**2) - 1) / x
    at_zero = limit(f)
    equal(at_zero, 0)
    derivative = limit((f - at_zero) / x)
    equal(derivative, 1)
    equal(at_zero + derivative * x, x)


def p14():
    n = s.symbols("n", positive=True, integer=True)
    expr = n**2 * (s.log(1 + 1 / n) - 1 / (n + 1))
    equal(s.limit(expr, n, s.oo), R(1, 2))


def p15():
    h = s.exp(-x) - 1 + x
    positive_x = s.symbols("positive_x", positive=True)
    # Positive derivative on the entire domain plus opposite endpoint signs
    # establishes exactly one root, rather than just finding one numerically.
    # SymPy does not infer 1-exp(-x)>0 directly. Its derivative is positive
    # and its value at zero is zero, which establishes the sign on x>0.
    equal(s.diff(h, x).subs(x, 0), 0)
    assert s.diff(h, x, 2).subs(x, positive_x).is_positive
    assert h.subs(x, 0) - R(1, 4) < 0
    assert h.subs(x, 2) - R(1, 4) > 0
    root = s.nsolve(h - R(1, 4), (R(1, 10), 2), solver="bisect", prec=60, maxsteps=250)
    assert 0 < root < 2
    assert abs((h - R(1, 4)).subs(x, root)) < s.Float("1e-50")
    equal(limit(h / x**2), R(1, 2))


if __name__ == "__main__":
    checks = {1: p01, 2: p02, 3: p03, 4: p04, 5: p05, 6: p06,
              7: p07, 8: p08, 9: p09, 10: p10, 11: p11, 12: p12,
              13: p13, 14: p14, 15: p15}
    ids = {int(i) for i in re.findall(r"^\*\*C7-(\d+)\*\*", problems, re.M)}
    assert ids == set(checks) | {9}, "Question/check coverage mismatch"
    for number in sorted(ids):
        try:
            assert f"**C7-{number:02d}**" in answers
            checks[number]()
            if number != 9:
                print(f"PASS C7-{number:02d}")
        except Exception as error:
            failed += 1
            print(f"FAIL C7-{number:02d} {type(error).__name__}: {error}")
    raise SystemExit(bool(failed))
