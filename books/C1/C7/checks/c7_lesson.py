"""Independent symbolic/numerical checks of all 24 numbered lesson examples."""

from pathlib import Path
import re

import sympy as s

x = s.symbols("x", real=True)
R = s.Rational
failed = 0


def equal(actual, expected):
    assert s.simplify(actual - expected) == 0, (actual, expected)


def limit(expr, point=0, direction="+-"):
    return s.limit(expr, x, point, dir=direction)


def rounded(actual, printed, places):
    assert abs(actual.evalf(60) - R(str(printed))) <= R(1, 2) * R(10)**(-places), (actual, printed)


def taylor(f, polynomial, degree, center=0):
    # Compare derivatives, independently of the lesson's algebraic expansions.
    for k in range(degree + 1):
        equal(s.diff(f, x, k).subs(x, center), s.diff(polynomial, x, k).subs(x, center))


def e01():
    f = (s.exp(x) - 1 - x) / x**2
    equal(limit(f), R(1, 2))
    for value, target in [(R(1, 10), "0.51709"), (R(1, 100), "0.50167"),
                          (R(1, 1000), "0.50017")]:
        rounded(f.subs(x, value), target, 5)
    equal(limit((1 - s.cos(x)) / x**2), R(1, 2))


def e02():
    f, g = 1 - s.cos(x), x + x**2
    equal(limit(f / g), 0)
    equal(limit(s.diff(f, x) / s.diff(g, x)), 0)
    equal(limit(s.diff(g, x)), 1)
    equal(limit(s.diff(f, x, 2) / s.diff(g, x, 2)), R(1, 2))


def e03():
    equal(limit((x - s.atan(x)) / x**3), R(1, 3))


def e04():
    a = s.symbols("a", positive=True)
    n = s.symbols("n", positive=True, integer=True)
    equal(limit(s.log(x) / x**a, s.oo, "-"), 0)
    equal(limit(x**n / s.exp(x), s.oo, "-"), 0)


def e05():
    equal(limit(x * s.log(x), direction="+"), 0)
    equal(limit(x**2 * s.log(x), direction="+"), 0)
    equal(limit(x * (s.pi / 2 - s.atan(x)), s.oo, "-"), 1)


def e06():
    equal(limit(1 / x - 1 / (s.exp(x) - 1)), R(1, 2))


def e07():
    value = s.exp(limit(s.log(s.cos(x)) / x**2))
    equal(value, s.exp(-R(1, 2)))
    rounded(value, "0.6065", 4)
    equal(limit(s.exp(x * s.log(x)), direction="+"), 1)
    equal(limit(s.exp(x * s.log(1 + x**-2)), s.oo, "-"), 1)


def e08():
    # Bounded oscillations give the original limits by squeeze.
    equal(limit(x / s.sin(x)), 1)
    equal(limit(s.Abs(x)), 0)
    equal(limit(1 / x, s.oo, "-"), 0)
    equal(limit(x**2 * s.sin(1 / x) / s.sin(x)), 0)
    equal(limit((x + s.sin(x)) / x, s.oo, "-"), 1)
    k = s.symbols("k", integer=True, positive=True)
    derivative1 = s.diff(x**2 * s.sin(1 / x), x) / s.cos(x)
    sequence_limits = [s.limit(derivative1.subs(x, point), k, s.oo)
                       for point in [1 / (2 * s.pi * k), 1 / ((2 * k + 1) * s.pi)]]
    assert sequence_limits == [-1, 1]
    derivative2 = s.diff(x + s.sin(x), x)
    assert [s.simplify(derivative2.subs(x, point))
            for point in [2 * s.pi * k, (2 * k + 1) * s.pi]] == [2, 0]
    f, g = x, s.sqrt(1 + x**2)
    equal(limit(f / g, s.oo, "-"), 1)
    derivative_ratio = s.diff(f, x) / s.diff(g, x)
    equal(limit(derivative_ratio, s.oo, "-"), 1)
    positive_x = s.symbols("positive_x", positive=True)
    assert s.diff(g, x).subs(x, positive_x).is_positive


def e09():
    f = s.log(s.exp(x) + s.exp(3 * x)) / x
    equal(limit(f, s.oo, "-"), 3)
    for value, target, places in [(1, "3.1269", 4), (2, "3.0091", 4),
                                   (5, "3.000009", 6), (10, "3.0000000002", 10)]:
        rounded(f.subs(x, value), target, places)
    # Split equal inputs from unequal inputs to avoid an ambiguous sign(gap).
    gap = s.symbols("gap", positive=True)
    equal(limit(s.log(1 + s.exp(-gap * x)) / x, s.oo, "-"), 0)
    equal(limit(s.log(2) / x, s.oo, "-"), 0)


def e10():
    f = s.sqrt(x)
    p = 2 + (x - 4) / 4 - (x - 4)**2 / 64
    taylor(f, p, 2, 4)
    point = R(41, 10)
    equal(p.subs(x, point), R("2.02484375"))
    rounded(f.subs(x, point), "2.0248457", 7)
    rounded(f.subs(x, point) - p.subs(x, point), "0.0000019", 7)
    rounded(R("2.025") - f.subs(x, point), "0.00015", 5)
    taylor(s.log(x), (x - 1) - (x - 1)**2 / 2 + (x - 1)**3 / 3, 3, 1)


def e11():
    taylor(x * s.exp(x), x + x**2 + x**3 / 2, 3)


def e12():
    taylor(s.exp(-x**2), 1 - x**2 + x**4 / 2, 4)
    taylor(s.cos(2 * x), 1 - 2 * x**2 + R(2, 3) * x**4, 4)
    # The displayed intermediate expansion must retain its remainder order.
    taylor(s.cos(x), 1 - x**2 / 2 + x**4 / 24, 4)


def e13():
    taylor(s.exp(x) * s.sin(x), x + x**2 + x**3 / 3, 3)
    taylor(x * s.exp(x), x + x**2 + x**3 / 2, 3)
    # Product coefficients through x^3, including the cross term 1/2 - 1/6.
    equal(s.expand((1 + x + x**2 / 2) * (x - x**3 / 6)).coeff(x, 3), R(1, 3))


def e14():
    taylor(s.tan(x), x + x**3 / 3, 3)
    equal(s.expand((x + s.symbols("a") * x**3) * (1 - x**2 / 2)).coeff(x, 3), s.symbols("a") - R(1, 2))


def e15():
    equal(s.diff(x**2 * s.log(1 + x), x, 5).subs(x, 0), 40)


def e16():
    f = s.tan(x) - s.sin(x)
    equal(limit(f / x**3), R(1, 2))
    rounded(f.subs(x, R(1, 10)), "0.0005013", 7)
    equal((x**3 / 2).subs(x, R(1, 10)), R("0.0005"))


def e17():
    equal(limit((x - s.sin(x)) / x**3), R(1, 6))


def e18():
    equal(limit((s.cos(x) - s.exp(-x**2 / 2)) / x**4), -R(1, 12))
    equal(limit((s.exp(x) - 1 - x - x**2 / 2) / x**3), R(1, 6))


def e19():
    equal(limit(1 / s.sin(x)**2 - 1 / x**2), R(1, 3))


def e20():
    a, b = s.symbols("a b", real=True)
    f = x - (a + b * s.cos(x)) * s.sin(x)
    coefficients = [s.diff(f, x, k).subs(x, 0) / s.factorial(k) for k in (1, 3, 5)]
    solution = s.solve(coefficients[:2], (a, b), dict=True)
    assert solution == [{a: R(4, 3), b: -R(1, 3)}]
    equal(coefficients[2].subs(solution[0]), R(1, 30))
    equal(limit(f.subs(solution[0]) / x**5), R(1, 30))


def e21():
    def polynomial(n):
        return sum(1 / s.factorial(k) for k in range(n + 1))
    degree = next(n for n in range(10) if (s.E - polynomial(n)).evalf(50) < R(1, 1000))
    assert degree == 6
    assert s.E < R(28, 10)
    assert R(28, 10) / s.factorial(7) < R(1, 1000)
    assert 1 / s.factorial(6) > R(1, 1000)
    rounded(R(28, 10) / s.factorial(7), "0.00056", 5)
    rounded(1 / s.factorial(6), "0.0014", 4)
    rounded(polynomial(6), "2.71806", 5)
    rounded(s.E - polynomial(6), "0.00023", 5)
    sine_error = abs(s.sin(R(1, 2)) - (R(1, 2) - R(1, 2)**3 / 6))
    bound = R(1, 2)**5 / s.factorial(5)
    assert sine_error.evalf(50) < bound
    rounded(bound, "0.00026", 5)


def e22():
    third = s.diff(s.sqrt(x), x, 3)
    positive_x = s.symbols("positive_x", positive=True)
    assert s.diff(third, x).subs(x, positive_x).is_negative
    maximum = third.subs(x, 4)
    equal(maximum, R(3, 256))
    bound = maximum * R(1, 10)**3 / s.factorial(3)
    rounded(bound, "0.00000195", 8)
    actual = s.sqrt(R(41, 10)) - R("2.02484375")
    assert 0 < actual.evalf(50) < bound


def e23():
    radius, maximum, tolerance = R("0.3466"), R("1.42"), R(1, 2)**24
    assert s.log(2) / 2 < radius
    assert s.exp(radius) < maximum
    bound = lambda n: maximum * radius**(n + 1) / s.factorial(n + 1)
    assert next(n for n in range(12) if bound(n) < tolerance) == 7
    rounded(bound(6), "0.00000017", 8)
    rounded(bound(7), "0.0000000073", 10)
    endpoint = s.log(2) / 2
    p6 = sum(endpoint**k / s.factorial(k) for k in range(7))
    assert (s.exp(endpoint) - p6).evalf(50) > tolerance


def e24():
    # Check the global inequalities by positive derivatives and zero values.
    positive_x = s.symbols("positive_x", positive=True)
    gaps = [s.log(1 + x) - x + x**2 / 2, x - s.log(1 + x)]
    for gap in gaps:
        equal(gap.subs(x, 0), 0)
        assert s.factor(s.diff(gap, x)).subs(x, positive_x).is_positive
    equal(s.diff(s.log(1 + x), x, 2), -1 / (1 + x)**2)
    equal(s.diff(s.log(1 + x), x, 3), 2 / (1 + x)**3)


if __name__ == "__main__":
    lesson = (Path(__file__).resolve().parents[1] / "lesson.md").read_text()
    numbers = {int(n) for n in re.findall(r"\*\*例 (\d+)\*\*", lesson)}
    assert numbers == set(range(1, 25)), "Numbered example coverage changed"
    for number in sorted(numbers):
        try:
            globals()[f"e{number:02d}"]()
            print(f"PASS 例{number}")
        except Exception as error:
            failed += 1
            print(f"FAIL 例{number} {type(error).__name__}: {error}")
    raise SystemExit(bool(failed))
