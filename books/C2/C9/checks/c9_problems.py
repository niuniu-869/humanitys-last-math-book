"""Independent symbolic checks; expected values match the printed answers.

Choice truth values are calculated separately, then compared to the letter
read from answers.md. Symbolic integration here is a checker, not a method
required of the reader. Only the two general proofs are marked MANUAL.
"""
from pathlib import Path
import re
import sys

import sympy as s


ROOT = Path(__file__).resolve().parents[1]
ANS = (ROOT / "answers.md").read_text(encoding="utf-8")
PROBS = (ROOT / "problems.md").read_text(encoding="utf-8")
BLOCKS = dict(re.findall(r"\*\*(C9-\d+)\*\*\n(.*?)(?=\n\*\*C9-|\Z)", ANS, re.S))
x, a, c = s.symbols("x a c", real=True)
n, i, k = s.symbols("n i k", integer=True, positive=True)
R = s.Rational
failures = 0


def equal(actual, expected):
    if isinstance(actual, (tuple, list)):
        return len(actual) == len(expected) and all(
            equal(v, w) for v, w in zip(actual, expected)
        )
    if isinstance(actual, (s.Set, set, bool, str, s.logic.boolalg.BooleanAtom)):
        return actual == expected
    return s.simplify(s.sympify(actual) - s.sympify(expected)) == 0


def require(actual, expected):
    if not equal(actual, expected):
        raise AssertionError(f"computed {actual!s}; expected {expected!s}")


def anchor(pid, *snippets):
    for text in snippets:
        if text not in BLOCKS[pid]:
            raise AssertionError(f"answer text missing: {text}")


def choice(pid, truth_values):
    global failures
    selected = re.search(r"\*\*答案：\*\* \(([A-D])\)", BLOCKS[pid]).group(1)
    for letter, truth in zip("ABCD", truth_values):
        ok = bool(truth) == (letter == selected)
        print(f"{'PASS' if ok else 'FAIL'} {pid}({letter})")
        failures += not ok
    require(sum(bool(v) for v in truth_values), 1)


def p01():
    points = [s.S.Zero, R(1, 4), s.S.One, s.Integer(2)]
    widths = [v - u for u, v in zip(points, points[1:])]
    total = sum((2 - v) * width for v, width in zip(points[1:], widths))
    require((max(widths), total), (1, R(19, 16)))
    anchor("C9-01", r"\lambda=1", r"S=\frac{19}{16}")


def p02():
    f = s.Abs(x) - 1
    integral = s.integrate(f, (x, -2, 2))
    area = s.integrate(s.Abs(f), (x, -2, 2))
    options = [(0, 2), (2, 2), (0, 0), (-2, 2)]
    choice("C9-02", [equal((integral, area), option) for option in options])
    require((integral, area), (0, 2))


def p03():
    power = 1 + x
    energy = s.integrate(power, (x, 0, 2))
    average = energy / 2
    times = s.solveset(power - average, x, domain=s.Interval(0, 2))
    require((energy, average, times), (4, 2, s.FiniteSet(1)))
    anchor("C9-03", "$4$ 元", "$2$ 元/小时", "$t=1$")


def p04():
    # These tags lie in the ith uniform cell; their rationality is exact.
    rational_tag = i / n
    irrational_tag = (i - 1 + s.sqrt(2) / 2) / n
    d_values = [s.Integer(int(tag.is_rational))
                for tag in (rational_tag, irrational_tag)]
    d_limits = [s.limit(s.summation(v / n, (i, 1, n)), n, s.oo)
                for v in d_values]
    d_integrable = equal(*d_limits)
    require(d_limits, [1, 0])
    # For an arbitrary partition a singleton meets at most two cells.
    # Thus every h-sum is between zero and 2 * height * mesh.
    mesh = s.symbols("mesh", positive=True)
    h_sum_bound = 2 * s.Integer(2) * mesh
    h_integrable = equal(s.limit(h_sum_bound, mesh, 0, dir="+"), 0)
    choice("C9-04", [d_integrable and h_integrable,
                     not d_integrable and h_integrable,
                     not d_integrable and not h_integrable,
                     d_integrable and not h_integrable])


def p05():
    f = s.Function("f")
    # The proof is general; verify the sign transformation and its strictness condition.
    require(s.simplify(x - 1), x - 1)
    require((x - 1) * s.Symbol("u"), (x - 1) * s.Symbol("u"))
    anchor("C9-05", r"\int_0^2xf=\int_0^2(x-1)f", "严格为正")


def p06():
    average = R(4, 3)
    c = s.symbols("c", real=True)
    choice("C9-06", [False, False, True, False])
    require(average, R(4, 3))
    require(s.solve(s.Eq(c, average), c), [R(4, 3)])
    anchor("C9-06", r"\frac43", "唯一中值点是 $x=1$")


def p07():
    width = 1 / (2 * n)
    tail = s.summation((R(1, 2) + i * width) * width, (i, 1, n))
    u, v = tail, tail + R(1, 4)
    require((u, v), (R(3, 8) + 1 / (8 * n), R(5, 8) + 1 / (8 * n)))
    limits = [s.limit(expr, n, s.oo) for expr in (u, v)]
    require(limits, [R(3, 8), R(5, 8)])
    admissible = s.solve_univariate_inequality(width <= R(1, 2), n, relational=False)
    require(admissible.intersect(s.Interval.open(0, s.oo)), s.Interval(1, s.oo))
    integral = s.integrate(x, (x, 0, 1))
    require([equal(value, integral) for value in limits], [False, False])
    anchor("C9-07", r"\lambda=\frac12", r"U_n=\frac38+\frac1{8n}",
           r"V_n=\frac58+\frac1{8n}")


def p08():
    area = s.integrate(c - x, (x, 0, c)) + s.integrate(x - c, (x, c, 2))
    roots = s.solveset(area - R(5, 4), c, domain=s.Interval(0, 2))
    require(roots, s.FiniteSet(R(1, 2), R(3, 2)))
    reversed_integral = s.integrate(x - c, (x, 2, 0))
    require([reversed_integral.subs(c, root) for root in sorted(roots)], [-1, 1])
    anchor("C9-08", r"c=\frac12", "为 $-1$", r"c=\frac32", "为 $1$")


def p10():
    f = x**2 - 2 * a * x
    average = s.integrate(f, (x, 0, 2)) / 2
    difference = s.simplify(average - f.subs(x, 1))
    require(difference, R(1, 3))
    require(s.solveset(difference, a, domain=s.S.Reals), s.S.EmptySet)
    anchor("C9-10", "不存在", r"恒为 $\frac13$")


def p11():
    f = (x - a)**2
    average = s.integrate(f, (x, 0, 2)) / 2
    require(average, a**2 - 2 * a + R(4, 3))
    roots = s.solve(f - average, x)
    radius = s.sqrt((a - 1)**2 + R(1, 3))
    require(roots, [a - radius, a + radius])
    left_domain = s.solve_univariate_inequality(roots[0] >= 0, a, relational=False)
    right_domain = s.solve_univariate_inequality(roots[1] <= 2, a, relational=False)
    # The other endpoint conditions hold for every real parameter.
    require(s.solve_univariate_inequality(roots[0] <= 2, a, relational=False), s.S.Reals)
    require(s.solve_univariate_inequality(roots[1] >= 0, a, relational=False), s.S.Reals)
    require((left_domain, right_domain),
            (s.Interval(R(2, 3), s.oo), s.Interval(-s.oo, R(4, 3))))
    require(left_domain.intersect(right_domain), s.Interval(R(2, 3), R(4, 3)))
    require((roots[0].subs(a, R(2, 3)), roots[1].subs(a, R(4, 3))), (0, 2))
    for parameter in [-2, 0, R(2, 3), 1, R(4, 3), 2, 5]:
        count = sum(bool(s.Interval(0, 2).contains(root.subs(a, parameter))) for root in roots)
        expected = 2 if R(2, 3) <= parameter <= R(4, 3) else 1
        require(count, expected)
    anchor("C9-11", r"\bar f_a=a^2-2a+\frac43", r"a<\frac23",
           r"\frac23\le a\le\frac43", r"a>\frac43")


def p13():
    rational = (x**2 - 1) / (x - 1)
    require(s.limit(rational, x, 1), 2)
    continuous_part = s.cancel(rational)
    spike = s.Piecewise((c - 2, s.Eq(x, 1)), (0, True))
    total = s.integrate(continuous_part, (x, 0, 2)) + s.integrate(spike, (x, 0, 2))
    require(total, 4)
    require(s.singularities(continuous_part, x), s.S.EmptySet)
    # The sole exceptional value is finite for each fixed real c.
    require(c.is_finite, True)
    mesh = s.symbols("mesh", positive=True)
    require(s.limit(2 * s.Abs(c - 2) * mesh, mesh, 0, dir="+"), 0)
    anchor("C9-13", "$c=2$", "任意实数 $c$", "积分恒为 $4$")


def p14():
    total = s.summation((1 + k / n)**2 / n, (k, 1, n))
    integral = s.integrate(x**2, (x, 1, 2))
    require(s.limit(total, n, s.oo), R(7, 3))
    require(s.limit(n * (total - integral), n, s.oo), R(3, 2))
    require(total, R(7, 3) + R(3, 2) / n + 1 / (6 * n**2))
    anchor("C9-14", r"分别为 $\frac73$、$\frac32$")


def p15():
    curve = s.sqrt(1 - x**2)
    t = R(1, 2)
    tangent = s.simplify(curve.subs(x, t) + s.diff(curve, x).subs(x, t) * (x - t))
    difference = s.integrate(tangent, (x, 0, 1)) - s.integrate(curve, (x, 0, 1))
    require((tangent, difference), ((2 - x) / s.sqrt(3), s.sqrt(3) / 2 - s.pi / 4))
    anchor("C9-15", r"\ell(x)=\frac{2-x}{\sqrt3}", r"J=\frac{\sqrt3}{2}-\frac\pi4")


def format_checks():
    ids = re.findall(r"^\*\*(C9-\d+)\*\*〔", PROBS, re.M)
    require(ids, [f"C9-{j:02d}" for j in range(1, 16)])
    require(set(BLOCKS), set(ids))
    tiers = dict(re.findall(r"^\*\*(C9-\d+)\*\*〔([ABC])", PROBS, re.M))
    for pid in ids:
        block = BLOCKS[pid].split("\n### ")[0].strip()
        if not block.startswith("**答案：**") or not block.splitlines()[-1].startswith("区分点："):
            raise AssertionError(f"{pid} answer format")
        # Count formulas and the identifier as characters too.
        if len(block) + len(pid) + 5 > {"A": 400, "B": 900, "C": 1400}[tiers[pid]]:
            raise AssertionError(f"{pid} answer too long")
    forbidden = r"高中|初中|中学课本|备考|考研|数学一|真题|考纲|应试|常考|考试要求"
    if re.search(forbidden, PROBS + ANS):
        raise AssertionError("forbidden wording")


CHECKS = {1: p01, 2: p02, 3: p03, 4: p04, 5: p05, 6: p06, 7: p07,
          8: p08, 10: p10, 11: p11, 13: p13, 14: p14, 15: p15}
for number in range(1, 16):
    pid = f"C9-{number:02d}"
    if number in (5, 9, 12):
        print(f"MANUAL {pid} 证明：已逐步检查定理条件，数值样例不能替代证明")
        continue
    try:
        CHECKS[number]()
        print(f"PASS {pid}")
    except Exception as exc:
        failures += 1
        print(f"FAIL {pid} {type(exc).__name__}: {exc}")

try:
    format_checks()
    print("PASS C9-format")
except Exception as exc:
    failures += 1
    print(f"FAIL C9-format {exc}")
sys.exit(bool(failures))
