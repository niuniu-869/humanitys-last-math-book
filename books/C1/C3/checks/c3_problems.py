"""Recompute all determinate answers; expected values are transcribed from answers.md.

Limits, parameter sets, domains, and bisection steps are computed symbolically.
Oscillation is checked with exact subsequences, never with a finite sample plot.
Only the general existence proof is marked MANUAL.
"""

import re
import sys
from pathlib import Path

import sympy as s
from sympy.calculus.util import continuous_domain


x, a, t = s.symbols("x a t", real=True)
n = s.symbols("n", integer=True, positive=True)
R = s.Rational
ROOT = Path(__file__).resolve().parents[1]
answers = (ROOT / "answers.md").read_text(encoding="utf-8")
blocks = dict(re.findall(r"\*\*(C3-\d+)\*\*\n(.*?)(?=\n\*\*C3-|\Z)", answers, re.S))
failures = []


def equal(actual, expected):
    assert s.simplify(actual - expected) == 0, (actual, expected)


def anchor(pid, *texts):
    for text in texts:
        assert text in blocks[pid], (pid, "answer text drift", text)


def run(pid, check):
    try:
        check()
    except Exception as error:
        failures.append(pid)
        print(f"FAIL {pid} {type(error).__name__}: {error}")
    else:
        print(f"PASS {pid}")


def choices(pid, actual, expected):
    # Every option is evaluated, including the false ones.
    for letter, value, want in zip("ABCD", actual, expected):
        def check(value=value, want=want):
            assert bool(value) == want, (value, want)
        run(f"{pid}({letter})", check)
    selected = "".join(letter for letter, value in zip("ABCD", actual) if bool(value))
    assert len(selected) == 1, selected
    anchor(pid, f"选 ({selected})")


def check01():
    left = s.limit(x + 2, x, 1, dir="-")
    right = s.limit(x + 2, x, 1, dir="+")
    point = s.Integer(0)
    equal(left, 3)
    equal(right, 3)
    continuous = left == right == point
    # Changing the separately defined point leaves both punctured branches intact.
    changed_limit = s.limit(x + 2, x, 1)
    choices("C3-01", [continuous, continuous,
                       left == right and left != point and right != point,
                       changed_limit != left], [False, False, True, False])


def check02():
    delta = s.symbols("delta", positive=True)
    f = 2 - 3 * x
    slope_size = abs(s.expand(f.subs(x, 1 + delta) - f.subs(x, 1)) / delta)
    eps = R(6, 100)
    largest = s.solve(s.Eq(slope_size * delta, eps), delta)[0]
    equal(largest, R(1, 50))
    equal(abs(f.subs(x, 1 + largest) - f.subs(x, 1)), eps)
    allowed = s.solve_univariate_inequality(slope_size * delta <= eps, delta, relational=False)
    allowed = allowed.intersect(s.Interval.open(0, s.oo))
    assert allowed == s.Interval(0, R(1, 50), left_open=True)
    anchor("C3-02", "$0.02$")


def check03():
    expression = x**2 + x
    endpoints = [s.limit(expression, x, -1, dir="+"), s.limit(expression, x, 1, dir="-")]
    assert endpoints == [0, 2]
    assert continuous_domain(expression, x, s.Interval(-1, 1)) == s.Interval(-1, 1)
    anchor("C3-03", "$a=0$", "$b=2$", "在 $-1$ 检查右连续", "在 $1$ 检查左连续")


def check04():
    expression = (x**2 - 4) / (x - 2)
    candidates = s.solveset(x - 2, x, domain=s.S.Reals)
    assert candidates == s.FiniteSet(2)
    left, right = [s.limit(expression, x, 2, dir=d) for d in ("-", "+")]
    assert left == right == 4 and left != 7
    assert s.cancel(expression) == x + 2
    anchor("C3-04", "唯一的间断点是 $2$", "可去间断点", "$f(2)$ 改成 $4$")


def check05():
    h = s.atan(1 / x)
    left, right = [s.limit(h, x, 0, dir=d) for d in ("-", "+")]
    point = s.pi / 2
    equal(left, -s.pi / 2)
    equal(right, s.pi / 2)
    transformed = []
    for outer in (s.cos, lambda u: u**2, s.sin):
        values = [s.simplify(outer(v)) for v in (left, right, point)]
        transformed.append(values[0] == values[1] == values[2])
    choices("C3-05", [not transformed[0], transformed[1], transformed[2], left == right],
            [False, True, False, False])


def check06():
    u = s.symbols("u", real=True)
    outer = s.Piecewise((u + 1, u < 1), (3, True))
    # A nonzero real x selects a definite branch on each side of zero.
    z = s.symbols("z", real=True, nonzero=True)
    p = s.simplify(outer.subs(u, 1 - z**2))
    q = s.simplify(outer.subs(u, 1 + z**2))
    assert p == 2 - z**2 and q == 3
    equal(s.limit(p, z, 0), 2)
    equal(s.limit(q, z, 0), 3)
    equal(outer.subs(u, 1), 3)
    assert s.limit(p, z, 0) != outer.subs(u, 1)
    anchor("C3-06", "p(x)=2$", "q(x)=3$", "$p$ 在 $0$ 不连续", "$q$ 在 $0$ 连续")


def check07():
    numerator = s.sqrt(1 + x) - 1 - x / 2
    expression = numerator / (x * s.log(1 + x))
    for direction in ("-", "+"):
        equal(s.limit(expression, x, 0, dir=direction), -R(1, 8))
    # Independently validate the exact rationalization and the failed replacement.
    y = s.symbols("y", positive=True)
    identity = numerator + x**2 / (2 * (s.sqrt(1 + x) + 1)**2)
    equal(identity.subs(x, y**2 - 1), 0)
    replaced = (x / 2 - x / 2) / (x * s.log(1 + x))
    assert s.limit(replaced, x, 0) != s.limit(expression, x, 0)
    anchor("C3-07", "$-1/8$")


def check08():
    base = 1 + x
    exponent = 1 / s.Abs(x)
    for direction, expected in (("-", -1), ("+", 1)):
        product_limit = s.limit(exponent * (base - 1), x, 0, dir=direction)
        equal(product_limit, expected)
        log_limit = s.limit(exponent * s.log(base), x, 0, dir=direction)
        equal(log_limit, expected)
    assert s.exp(-1) != s.exp(1)
    anchor("C3-08", "双侧极限不存在", "$e^{-1}$", "$e$")


def check09():
    expression = 1 / (x - 1)
    domain = continuous_domain(expression, x, s.Interval(0, 2))
    roots = s.solveset(expression, x, domain=s.Interval(0, 2))
    left, right = [s.limit(expression, x, 1, dir=d) for d in ("-", "+")]
    assert expression.subs(x, 0) * expression.subs(x, 2) < 0
    assert (left, right) == (-s.oo, s.oo)
    interval = s.Interval(0, 2)
    midpoint = (interval.start + interval.end) / 2
    choices("C3-09", [roots != s.S.EmptySet, left == right == 0,
                       roots == s.S.EmptySet and domain != s.Interval(0, 2),
                       expression.subs(x, midpoint) == 0], [False, False, True, False])


def check11():
    quotient = (s.exp(a * x) - 1) / (s.exp(x) - 1)
    limit = s.limit(quotient, x, 0)
    equal(limit, a)
    equal(s.limit(quotient.subs(a, 0), x, 0), 0)
    point = a**2
    first = s.solveset(limit - point, a, domain=s.S.Reals)
    second = s.solveset(s.Abs(limit) - s.Abs(point), a, domain=s.S.Reals)
    third = s.solveset(limit**2 - limit - (point**2 - point), a, domain=s.S.Reals)
    assert first == s.FiniteSet(0, 1)
    assert second == s.FiniteSet(-1, 0, 1)
    assert third == s.FiniteSet(0, 1, (-1 - s.sqrt(5)) / 2, (-1 + s.sqrt(5)) / 2)
    for parameter in third:
        expression = quotient.subs(a, parameter)
        equal(s.limit(expression**2 - expression, x, 0), (point**2 - point).subs(a, parameter))
    anchor("C3-11", r"\{0,1\}", r"\{-1,0,1\}", r"(-1-\sqrt5)/2", r"(-1+\sqrt5)/2")


def check12():
    # Derive the complete admissible parameter intervals for both squared roots.
    branch_ranges = []
    for squared_root in (1 + t, 1 - t):
        condition = s.reduce_inequalities([t >= 0, squared_root >= 0, squared_root <= 4], t)
        branch_ranges.append(condition.as_set())
    assert branch_ranges == [s.Interval(0, 3), s.Interval(0, 1)]
    # These boundaries partition all real parameters; root counts are constant
    # on their open cells, since neither squared root crosses 0 or 4 there.
    for parameter, count in [(-1, 0), (0, 2), (R(1, 2), 4), (1, 3), (2, 2), (3, 2), (4, 0)]:
        roots = s.solveset(s.Abs(x**2 - 1) - parameter, x, domain=s.Interval(-2, 2))
        assert len(roots) == count, (parameter, roots)
        for root in roots:
            equal(s.Abs(root**2 - 1), parameter)
    g = x**2 - R(3, 2)
    lo, hi = s.Integer(1), s.Integer(2)
    steps = []
    for _ in range(3):
        mid = (lo + hi) / 2
        value = g.subs(x, mid)
        if g.subs(x, lo) * value < 0:
            hi = mid
        else:
            lo = mid
        assert g.subs(x, lo) * g.subs(x, hi) < 0
        steps.append((mid, value, lo, hi))
    assert steps == [(R(3, 2), R(3, 4), 1, R(3, 2)),
                     (R(5, 4), R(1, 16), 1, R(5, 4)),
                     (R(9, 8), -R(15, 64), R(9, 8), R(5, 4))]
    length, count = s.Integer(1), 0
    while length >= R(1, 1000):
        length /= 2
        count += 1
    assert count == 10 and 2 * length >= R(1, 1000)
    anchor("C3-12", "$[9/8,5/4]$", "$10$ 步", "$0<t<1$ | 4", "$t=1$ | 3", "$1<t\\le3$ | 2")


def check13():
    expression = s.log((x**2 - 1) / (x - 1))
    domain = continuous_domain(expression, x, s.S.Reals)
    assert domain == s.Union(s.Interval.open(-1, 1), s.Interval.open(1, s.oo))
    for direction in ("-", "+"):
        equal(s.limit(expression, x, 1, dir=direction), s.log(2))
    assert s.limit(expression, x, -1, dir="+") == -s.oo
    anchor("C3-13", r"(-1,1)\cup(1,+\infty)", r"f(1)=\ln2", "不能补有限")


def check14():
    seq = (-1)**n / n
    equal(s.limit(s.Abs(seq), n, s.oo), 0)
    ratio_limit = s.limit((s.exp(x) - 1) / x, x, 0)
    equal(ratio_limit, 1)
    b = (s.exp(seq) - 1) / seq
    c = (s.exp(seq) - 1) / s.Abs(seq)
    for parity, wanted in [(0, 1), (1, -1)]:
        equal(s.limit(b.subs(n, 2 * n + parity), n, s.oo), 1)
        equal(s.limit(c.subs(n, 2 * n + parity), n, s.oo), wanted)
    anchor("C3-14", r"b_n\to1", "偶数项趋于 $1$", "奇数项趋于 $-1$")


def check15():
    # For |x|=t<1, log(1-t) <= F(x) <= log(1+t). Both bounds tend to 0.
    bound_domain = s.reduce_inequalities([t > 0, t < 1, 1 - t > 0], t).as_set()
    assert bound_domain == s.Interval.open(0, 1)
    for sign in (-1, 1):
        equal(s.limit(s.log(1 + sign * t), t, 0, dir="+"), 0)
    sequence_limits = []
    for phase in (s.pi / 2, 3 * s.pi / 2):
        points = 1 / (phase + 2 * s.pi * n)
        equal(s.limit(points, n, s.oo), 0)
        sine = s.simplify(s.sin(1 / points))
        value = s.log(1 + points * sine) / points
        sequence_limits.append(s.limit(value, n, s.oo))
    assert sequence_limits == [1, -1]
    anchor("C3-15", "$F$ 在 $0$ 连续", "没有极限", r"\to1", r"\to-1")


if __name__ == "__main__":
    checks = {1: check01, 2: check02, 3: check03, 4: check04, 5: check05,
              6: check06, 7: check07, 8: check08, 9: check09, 11: check11,
              12: check12, 13: check13, 14: check14, 15: check15}
    assert set(blocks) == {f"C3-{i:02d}" for i in range(1, 16)}
    for number in range(1, 16):
        pid = f"C3-{number:02d}"
        if number == 10:
            print(f"MANUAL {pid} 证明：复合与乘积连续，辅助函数在两端严格异号。")
        else:
            run(pid, checks[number])
    sys.exit(bool(failures))
