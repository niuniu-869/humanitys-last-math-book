"""Independent symbolic/numerical checks of all numbered lesson examples.

General proofs are explicitly MANUAL; computable claims within them are still
checked.
"""

import sys

import numpy as np
import sympy as s


x = s.symbols("x", real=True)
n = s.symbols("n", integer=True, positive=True)
R = s.Rational
failures = []


def equal(actual, expected):
    assert s.simplify(actual - expected) == 0, (actual, expected)


def near(actual, expected, tolerance):
    assert abs(float(actual) - expected) <= tolerance, (actual, expected, tolerance)


def run(label, check):
    try:
        check()
    except Exception as error:
        failures.append(label)
        print(f"FAIL {label} {type(error).__name__}: {error}")
    else:
        print(f"PASS {label}")


def example01():
    eps = s.symbols("eps", positive=True)
    # For |x-1|<delta, the supremum error is delta*(2+delta).
    # For eps<=3 use delta=eps/3; for eps>=3 use delta=1.
    small = s.reduce_inequalities([eps <= 3, (eps / 3) * (2 + eps / 3) > eps], eps)
    large = s.reduce_inequalities([eps >= 3, 1 * (2 + 1) > eps], eps)
    assert small is s.false and large is s.false
    delta = min(s.Integer(1), R(1, 10) / 3)
    equal(delta, R(1, 30))
    assert (1 + delta)**2 - 1 < R(1, 10)
    assert 1 - (1 - delta)**2 < R(1, 10)
    # Check the displayed rounded subinterval, as stated in the lesson.
    assert R(967, 1000)**2 > R(935, 1000)
    assert R(1033, 1000)**2 < R(1068, 1000)


def example02():
    a, b = s.symbols("a b", real=True)
    left = s.limit(s.sin(3 * x) / x, x, 0, dir="-")
    right = s.limit(b * (s.sqrt(1 + x) - 1) / x, x, 0, dir="+")
    assert s.solve([left - a, right - a], (a, b)) == {a: 3, b: 6}


def example03():
    expression = s.Abs(x - 1) / (x**2 - 1)
    assert s.solveset(x**2 - 1, x, domain=s.S.Reals) == s.FiniteSet(-1, 1)
    assert [s.limit(expression, x, 1, dir=d) for d in ("-", "+")] == [-R(1, 2), R(1, 2)]
    assert [s.limit(expression, x, -1, dir=d) for d in ("-", "+")] == [s.oo, -s.oo]


def example04():
    expression = x / s.log(s.Abs(x))
    assert s.solveset(s.log(s.Abs(x)), x, domain=s.S.Reals) == s.FiniteSet(-1, 1)
    assert s.solveset(s.Abs(x), x, domain=s.S.Reals) == s.FiniteSet(0)
    assert [s.limit(expression, x, 0, dir=d) for d in ("-", "+")] == [0, 0]
    for point in (-1, 1):
        assert [s.limit(expression, x, point, dir=d) for d in ("-", "+")] == [-s.oo, s.oo]


def example05():
    equal(s.limit(s.log(s.sin(x) / x), x, 0), 0)
    equal(s.limit(s.atan((2 * x**2 + 1) / (x**2 - 3)), x, s.oo), s.atan(2))


def example06():
    # A counterexample at zero suffices to refute the asserted implication.
    rational_points, irrational_points = 1 / n, s.sqrt(2) / n
    assert rational_points.is_rational is True
    assert irrational_points.is_rational is False
    images = []
    for points in (rational_points, irrational_points):
        equal(s.limit(points, n, s.oo), 0)
        images.append(s.Integer(1) if points.is_rational else s.Integer(-1))
    assert images[0] != images[1]
    assert [s.Abs(value) for value in images] == [1, 1]


def example07():
    expressions = [((1 + 2 * x)**R(1, 3) - 1) / s.log(1 + 3 * x),
                   s.asin(2 * x) / (s.exp(3 * x) - 1)]
    for expression, expected in zip(expressions, (R(2, 9), R(2, 3))):
        for direction in ("-", "+"):
            equal(s.limit(expression, x, 0, dir=direction), expected)


def example08():
    logs = [s.log(s.cos(x)) / x**2, s.log(x + s.exp(x)) / x]
    for log_expression, expected in zip(logs, (-R(1, 2), s.Integer(2))):
        for direction in ("-", "+"):
            equal(s.limit(log_expression, x, 0, dir=direction), expected)
    near(s.exp(-R(1, 2)), 0.6065, 0.00005)
    near(s.exp(2), 7.389, 0.0005)
    near(s.exp(logs[0].subs(x, R(1, 100))).evalf(40), 0.60653, 0.000005)
    near(s.exp(logs[1].subs(x, R(1, 1000))).evalf(40), 7.378, 0.0005)


def example09():
    expression = s.log(1 + s.exp(x))
    equal(s.limit(expression, x, -s.oo), 0)
    equal(s.limit(expression / s.exp(x), x, -s.oo), 1)
    approximation = np.exp(-10.0)
    exact = np.log1p(np.exp(-10.0))
    near(approximation, 4.5400e-5, 0.00005e-5)
    near(exact, 4.5399e-5, 0.00005e-5)
    near(abs(approximation - exact) / exact, 2e-5, 0.5e-5)


def example12():
    expression = x**5 - 3 * x + 1
    assert [expression.subs(x, point) for point in (-2, -1, 0, 1, 2)] == [-25, 3, 1, -1, 27]
    poly = s.Poly(expression, x)
    for lo, hi in [(-2, -1), (0, 1), (1, 2)]:
        assert expression.subs(x, lo) * expression.subs(x, hi) < 0
        assert poly.count_roots(lo, hi) >= 1
    assert poly.count_roots(-s.oo, s.oo) >= 3


def example14():
    expression = x**2 - 2
    lo, hi = s.Integer(1), s.Integer(2)
    mids, values, before = [], [], []
    for _ in range(6):
        before.append((lo, hi))
        mid = (lo + hi) / 2
        value = expression.subs(x, mid)
        mids.append(mid)
        values.append(value)
        if expression.subs(x, lo) * value < 0:
            hi = mid
        else:
            lo = mid
    assert mids == [R(3, 2), R(5, 4), R(11, 8), R(23, 16), R(45, 32), R(91, 64)]
    assert before == [(1, 2), (1, R(3, 2)), (R(5, 4), R(3, 2)),
                      (R(11, 8), R(3, 2)), (R(11, 8), R(23, 16)), (R(45, 32), R(23, 16))]
    for value, expected in zip(values, (0.25, -0.4375, -0.1094, 0.0664, -0.0225, 0.0217)):
        near(value, expected, 0.00005)
    assert (lo, hi) == (R(45, 32), R(91, 64))
    assert lo < s.sqrt(2) < hi
    near(s.sqrt(2), 1.41421, 0.000005)
    length, steps = s.Integer(1), 0
    while length >= R(1, 10**6):
        length /= 2
        steps += 1
    assert steps == 20 and 2 * length >= R(1, 10**6)
    assert 2**19 == 524288 and 2**20 == 1048576


def followups():
    a, b = s.symbols("a b", real=True)
    left = s.limit(s.sin(2 * x) / x, x, 0, dir="-")
    right = s.limit(b * (1 - s.cos(x)) / x**2, x, 0, dir="+")
    assert s.solve([left - a, right - a], (a, b)) == {a: 2, b: 4}
    jump = 1 / (1 + s.exp(1 / x))
    assert [s.limit(jump, x, 0, dir=d) for d in ("-", "+")] == [1, 0]
    equal(s.limit(s.sqrt((x**2 - 1) / (x - 1)), x, 1), s.sqrt(2))
    equal(s.limit(s.log(1 + x**2) / (s.atan(x) * (s.exp(2 * x) - 1)), x, 0), R(1, 2))
    equal(s.limit(s.log((2 + s.cos(x)) / 3) / x**2, x, 0), -R(1, 6))


if __name__ == "__main__":
    checks = {1: example01, 2: example02, 3: example03, 4: example04,
              5: example05, 6: example06, 7: example07, 8: example08,
              9: example09, 12: example12, 14: example14}
    proof_notes = {
        10: "证明：有限区间有界与无穷远的极限界拼接。",
        11: "证明：闭区间最小值能取到，且该点函数值严格为正。",
        13: "证明：f(x)-x 在两端非严格异号，先单独处理端点为零。",
    }
    for number in range(1, 15):
        if number in proof_notes:
            print(f"MANUAL 例{number} {proof_notes[number]}")
        else:
            run(f"例{number}", checks[number])
    print("MANUAL 例1 证明：严格邻域内的误差小于所算上界，任意 eps 的代数界已验。")
    print("MANUAL 例6 证明：一般的正向推论用绝对值函数连续；反例已独立核对。")
    print("MANUAL 例12 证明：三个互不相交区间各用零点定理，端点与根数已独立核对。")
    run("随堂计算题", followups)
    print("MANUAL 随堂证明 例10后补端点得有界；例13后作平移差，端点值互为相反数。")
    sys.exit(bool(failures))
