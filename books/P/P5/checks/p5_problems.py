"""Recompute from problem inputs; compare with the claims in answers.md.

Targets below are transcribed from the answer, never used as computational
inputs. Exact integration/enumeration is used instead of random tolerances.
Each multiple-choice option is evaluated separately, including false ones.
"""
from pathlib import Path
import re
import sys

import sympy as sp

R = sp.Rational
x, y, z, t, u = sp.symbols("x y z t u", real=True)
failures = []


def equal(actual, expected):
    assert sp.simplify(actual - expected) == 0, (actual, expected)


def run(pid, test):
    try:
        test()
    except Exception as exc:
        failures.append(pid)
        print(f"FAIL {pid}: {type(exc).__name__}: {exc}")
    else:
        print(f"PASS {pid}")


def pushforward(probabilities, transform):
    result = {}
    for value, mass in probabilities.items():
        target = transform(value)
        result[target] = result.get(target, 0) + mass
    return result


def choice(pid, actual_truth, expected_letter):
    answer_match = re.search(rf"\*\*{pid}\*\*\n\*\*答案：\*\* \(([A-D])\)", answers)
    assert answer_match and answer_match[1] == expected_letter
    for letter, truth in zip("ABCD", actual_truth):
        def check(truth=truth, letter=letter):
            assert bool(truth) == (letter == expected_letter)
        run(f"{pid}({letter})", check)
    assert sum(bool(v) for v in actual_truth) == 1


def p01():
    masses = sp.symbols("p_minus p_zero p_one p_two", real=True)
    merged = pushforward(dict(zip((-1, 0, 1, 2), masses)), lambda v: v * (v - 1))
    solution = sp.solve([merged[0] - R(5, 8), merged[2] - R(3, 8),
                         masses[1] - masses[3]], masses[:3])
    family = [solution.get(p, p) for p in masses]
    bounds = sp.reduce_inequalities([p >= 0 for p in family], masses[3]).as_set()
    assert bounds == sp.Interval(0, R(3, 8))
    equal(sum(family), 1)
    equal(family[2], R(5, 8) - masses[3])
    endpoints = [tuple(p.subs(masses[3], end) for p in family)
                 for end in (bounds.end, bounds.start)]
    assert endpoints == [(0, R(3, 8), R(1, 4), R(3, 8)),
                         (R(3, 8), 0, R(5, 8), 0)]
    # Every target in the claimed interval has a feasible preimage.
    q = sp.symbols("q", real=True)
    inverse = sp.solve(family[2] - q, masses[3])[0]
    feasible = sp.reduce_inequalities([p.subs(masses[3], inverse) >= 0
                                       for p in family], q).as_set()
    assert feasible == sp.Interval(R(1, 4), R(5, 8))


def p02():
    roots = sp.solve(1 - x**2 - y, x)
    lower = roots[1]
    cdf = sp.integrate(1, (x, lower, 1))
    candidates = [sp.sqrt(y), 1 - sp.sqrt(1 - y), sp.sqrt(1 - y), 1 - y]
    choice("P5-02", [sp.simplify(cdf - f) == 0 for f in candidates], "B")
    equal(cdf.subs(y, 0), 0)
    equal(cdf.subs(y, 1), 1)


def p03():
    inverse = sp.solve(sp.log(x) - y, x)[0]
    cdf = sp.integrate(1 / (sp.E - 1), (x, 1, inverse))
    density = sp.diff(cdf, y)
    support = [sp.log(v) for v in (1, sp.E)]
    candidates = [(1 / (sp.E - 1), [0, 1]), (sp.exp(-y) / (sp.E - 1), [0, 1]),
                  (sp.exp(y) / (sp.E - 1), [1, sp.E]),
                  (sp.exp(y) / (sp.E - 1), [0, 1])]
    truth = [sp.simplify(f - density) == 0 and interval == support
             for f, interval in candidates]
    choice("P5-03", truth, "D")
    equal(sp.integrate(density, (y, *support)), 1)
    equal(cdf.subs(y, 0), 0)
    equal(cdf.subs(y, 1), 1)


def p04():
    cdf = 1 - sp.exp(-x**2)
    # v=1-u is positive on the sampling interval; keep that domain
    # while simplifying the logarithm produced by the solver.
    v = sp.symbols("v", positive=True)
    squared_inverse = sp.expand_log(sp.solve(sp.exp(-z) - v, z)[0]).subs(v, 1 - u)
    inverse = sp.sqrt(squared_inverse)
    equal(inverse, sp.sqrt(-sp.log(1 - u)))
    equal(cdf.subs(x, inverse), u)
    quantile = sp.simplify(inverse.subs(u, R(3, 4)))
    equal(quantile, sp.sqrt(sp.log(4)))
    equal(sp.integrate(sp.diff(cdf, x), (x, 0, quantile)), R(3, 4))
    equal(cdf.subs(x, 0), 0)
    equal(sp.limit(cdf, x, sp.oo), 1)
    equal(sp.limit(inverse, u, 0, dir="+"), 0)
    assert sp.limit(inverse, u, 1, dir="-") == sp.oo


def p05():
    masses = {0: R(1, 5), 1: R(1, 2), 4: R(3, 10)}
    # Enumerate vertices of all allowed splits; the objective is linear.
    totals = [r + s for r in (0, masses[1]) for s in (0, masses[4])]
    equal(min(totals), 0)
    equal(max(totals), R(4, 5))
    endpoints = [dict(zip(range(-2, 3), row)) for row in
                 [(R(3, 10), R(1, 2), R(1, 5), 0, 0),
                  (0, 0, R(1, 5), R(1, 2), R(3, 10))]]
    for distribution, target in zip(endpoints, [0, R(4, 5)]):
        assert pushforward(distribution, lambda v: v**2) == masses
        equal(sum(p for v, p in distribution.items() if v > 0), target)
    q = sp.symbols("q", real=True)
    for r, s, lo, hi in [(q, 0, 0, R(1, 2)),
                         (R(1, 2), q - R(1, 2), R(1, 2), R(4, 5))]:
        equal(r + s, q)
        # Both affine splits stay in bounds throughout their entire interval.
        for value, bound in [(sp.sympify(r), masses[1]), (sp.sympify(s), masses[4])]:
            assert all(0 <= value.subs(q, end) <= bound for end in (lo, hi))


def p06():
    first = sp.integrate(R(1, 2), (t, 0, x))
    second = first.subs(x, 1) + sp.integrate(R(1, 4), (t, 1, x))
    equal(first, x / 2)
    equal(second, (x + 1) / 4)
    equal(first.subs(x, 1), second.subs(x, 1))
    equal(first.subs(x, 0), 0)
    equal(second.subs(x, 3), 1)
    inverses = [sp.solve(f - u, x)[0] for f in (first, second)]
    for inverse, expected in zip(inverses, [2 * u, 4 * u - 1]):
        equal(inverse, expected)
    equal(inverses[0].subs(u, R(1, 4)), R(1, 2))
    equal(inverses[1].subs(u, R(3, 4)), 2)
    equal(inverses[0].subs(u, R(1, 2)), inverses[1].subs(u, R(1, 2)))


def p07():
    atom = sp.integrate(R(1, 2), (x, 1, 2))
    interior = sp.integrate(R(1, 2), (x, 0, y))
    at_cap = sp.integrate(R(1, 2), (x, 0, 2))
    only_continuous_mass = sp.integrate(R(1, 2), (y, 0, 1))
    truth = [atom == 0 and only_continuous_mass == 1,
             at_cap == R(1, 2),
             sp.simplify(interior - y / 2) == 0 and interior.subs(y, 0) == 0
             and at_cap == 1 and at_cap - interior.subs(y, 1) == R(1, 2),
             atom == 0]
    choice("P5-07", truth, "C")
    equal(atom, R(1, 2))
    equal(only_continuous_mass + atom, 1)
    transform = sp.Min(x, 1)
    equal(transform.subs(x, R(5, 4)), transform.subs(x, R(7, 4)))
    assert R(5, 4) != R(7, 4)  # Distinct preimages establish noninjectivity.


def p08():
    # CDF uses the two outer intervals, independently of the answer's
    # branch-density calculation.
    fy = sp.integrate(x / 2, (x, 0, y)) + sp.integrate(x / 2, (x, 2 - y, 2))
    fz = sp.integrate(x / 2, (x, 0, 2 * z))
    equal(sp.diff(fy, y), 1)
    equal(sp.diff(fz, z), 2 * z)
    for function, variable in [(fy, y), (fz, z)]:
        equal(function.subs(variable, 0), 0)
        equal(function.subs(variable, 1), 1)
    equal(fy.subs(y, R(1, 2)), R(1, 2))
    equal(fz.subs(z, R(1, 2)), R(1, 4))


def p10():
    px = sp.integrate(1, (u, sp.exp(-t), 1))
    pt = sp.integrate(1, (u, 0, 1 - sp.exp(-t)))
    equal(px, 1 - sp.exp(-t))
    equal(pt, px)
    equal(px.subs(t, 0), 0)
    equal(sp.limit(px, t, sp.oo), 1)
    meeting = sp.solve(u - (1 - u), u)[0]
    equal(meeting, R(1, 2))
    equal(sp.integrate(1, (u, meeting, meeting)), 0)
    equal(sp.integrate(1, (u, 0, meeting)), R(1, 2))
    assert sp.solve_univariate_inequality(u < 1 - u, u, relational=False) == sp.Interval.open(-sp.oo, meeting)


def p11():
    c = sp.symbols("c")
    normalization = sp.solve(sp.integrate(c * (1 + x), (x, 0, 2)) - 1, c)[0]
    equal(normalization, R(1, 4))
    roots = sp.solve(x * (2 - x) - y, x)
    density = normalization * (1 + x)
    cdf = sp.integrate(density, (x, 0, roots[0])) + sp.integrate(density, (x, roots[1], 2))
    equal(cdf, 1 - sp.sqrt(1 - y))
    equal(sp.diff(cdf, y), 1 / (2 * sp.sqrt(1 - y)))
    equal(cdf.subs(y, 0), 0)
    equal(cdf.subs(y, 1), 1)
    equal(sp.integrate(sp.diff(cdf, y), (y, 0, 1)), 1)
    # Solve the inverse equation in r=sqrt(1-y), preserving r >= 0.
    r = sp.symbols("r", nonnegative=True)
    equal(sp.integrate(density, (x, 0, 1 - r)), (3 - 4 * r + r**2) / 8)
    equal(sp.integrate(density, (x, 1 + r, 2)), (5 - 4 * r - r**2) / 8)
    inverse_r = sp.solve(1 - r - u, r)[0]
    inverse_y = 1 - inverse_r**2
    equal(inverse_y, 1 - (1 - u)**2)
    composition = cdf.subs(y, inverse_y)
    composition = sp.refine(composition, sp.Q.positive(1 - u))
    equal(composition, u)


def p12():
    a = sp.log(2)
    cdf = sp.integrate(sp.exp(-x), (x, a - y, a + y))
    equal(cdf, (sp.exp(y) - sp.exp(-y)) / 2)
    atom = sp.integrate(sp.exp(-x), (x, 2 * a, sp.oo))
    equal(atom, R(1, 4))
    equal(1 - cdf.subs(y, a), atom)
    equal(cdf.subs(y, 0), 0)
    equal(sp.integrate(sp.diff(cdf, y), (y, 0, a)) + atom, 1)
    # The continuous branches are one-to-one, hence have singleton
    # preimages of zero mass. Only the final constant branch adds an atom.
    roots = sp.solve(z**2 - z - 1, z)
    positive_root = next(root for root in roots if root.is_positive)
    median = sp.log(positive_root)
    equal(median, sp.log((1 + sp.sqrt(5)) / 2))
    equal(cdf.subs(y, median), R(1, 2))
    assert 0 < median.evalf() < a.evalf()


def p13():
    distribution = {k: sp.binomial(3, k) * R(1, 2)**3 for k in range(4)}
    output = pushforward(distribution, lambda k: k * (3 - k))
    assert output == {0: R(1, 4), 2: R(3, 4)}
    equal(distribution[1] / output[2], R(1, 2))


def p14():
    original_pdf = sp.exp(-(x - 1)**2 / 8) / sp.sqrt(8 * sp.pi)
    denominator = sp.integrate(original_pdf, (x, -1, 3))
    numerator = sp.integrate(original_pdf, (x, 1, 3))
    phi_one = (1 + sp.erf(1 / sp.sqrt(2))) / 2
    equal(denominator, 2 * phi_one - 1)
    equal(numerator / denominator, R(1, 2))
    # The question supplies Phi(1) rounded to four places. Multiplying
    # that table value by 2 doubles its rounding-error bound.
    table_value = R(8413, 10000)
    assert abs(float(phi_one - table_value)) < 0.00005
    equal(2 * table_value - 1, R(6826, 10000))
    assert abs(float(denominator) - 0.6826) < 0.0001


def p15():
    intervals = [sp.Interval.Ropen(R(k, 4), R(k + 1, 4)) for k in range(4)]
    for k, interval in enumerate(intervals):
        equal(interval.measure, R(1, 4))
        equal(sp.floor(4 * (interval.start + interval.end) / 2), k)
    event_a = sp.Union(intervals[0], intervals[2])
    event_b = sp.Interval(0, R(1, 2))
    intersection = event_a.intersect(event_b)
    equal(event_a.measure, R(1, 2))
    equal(event_b.measure, R(1, 2))
    equal(intersection.measure, R(1, 4))
    equal(intersection.measure, event_a.measure * event_b.measure)


def p16():
    # Differentiate the conditional CDFs and integrate over the preimage.
    first = sp.integrate(sp.diff(x**2, x), (x, 0, sp.sqrt(y)))
    second = sp.integrate(sp.diff(2 * x - x**2, x), (x, 0, sp.sqrt(y)))
    mixture = R(1, 3) * first + R(2, 3) * second
    equal(mixture, (4 * sp.sqrt(y) - y) / 3)
    equal(mixture.subs(y, 0), 0)
    equal(mixture.subs(y, 1), 1)
    denominator = mixture.subs(y, R(1, 4))
    numerator = R(1, 3) * first.subs(y, R(1, 4))
    equal(denominator, R(7, 12))
    equal(numerator, R(1, 12))
    equal(numerator / denominator, R(1, 7))


tests = {1: p01, 2: p02, 3: p03, 4: p04, 5: p05, 6: p06, 7: p07,
         8: p08, 10: p10, 11: p11, 12: p12, 13: p13, 14: p14, 15: p15, 16: p16}
chapter = Path(__file__).resolve().parent.parent
answers = (chapter / "answers.md").read_text(encoding="utf-8")
problems = (chapter / "problems.md").read_text(encoding="utf-8")
ids = re.findall(r"^\*\*(P5-\d+)\*\*", problems, re.M)
assert ids == [f"P5-{n:02}" for n in range(1, 17)]
assert ids == re.findall(r"^\*\*(P5-\d+)\*\*", answers, re.M)
for n in range(1, 17):
    if n == 9:
        print("MANUAL P5-09 逐行检查事件改写、连续性与范围外取值")
    else:
        run(f"P5-{n:02}", tests[n])
sys.exit(bool(failures))
