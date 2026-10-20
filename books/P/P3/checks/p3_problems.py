"""Recompute exercises from their premises, then compare with answers.md.

Expected constants below transcribe the printed answers; computed values come
from enumeration, symbolic equations, or exact probability sums.
"""
from collections import Counter
from itertools import combinations, product
from pathlib import Path
import re
import sys

import sympy as s

R = s.Rational
failed = 0
root = Path(__file__).resolve().parents[1]
answers = (root / "answers.md").read_text(encoding="utf-8")
problems = (root / "problems.md").read_text(encoding="utf-8")
blocks = dict(re.findall(r"\*\*(P3-\d+)\*\*\n(.*?)(?=\n\*\*P3-|\Z)", answers, re.S))


def equal(actual, expected):
    if isinstance(expected, dict):
        return actual.keys() == expected.keys() and all(
            equal(actual[k], expected[k]) for k in expected
        )
    if isinstance(expected, (list, tuple)):
        return len(actual) == len(expected) and all(
            equal(a, b) for a, b in zip(actual, expected)
        )
    if isinstance(expected, (bool, str, set, s.Set)):
        return actual == expected
    return s.simplify(actual - expected) == 0


def check(pid, actual, expected, anchors=()):
    global failed
    good = equal(actual, expected)
    good = good and all(text in blocks[pid] for text in anchors)
    print(("PASS " if good else "FAIL ") + pid)
    if not good:
        failed += 1
        print(f"  computed={actual}; expected={expected}")


def choices(pid, actual, letter):
    for index, value in enumerate(actual):
        check(pid + " " + "ABCD"[index], bool(value), "ABCD"[index] == letter)
    check(pid, sum(bool(v) for v in actual), 1,
          ("**答案：** (" + letter + ")",))


def pmf(values):
    counts = Counter(values)
    return {k: R(v, len(values)) for k, v in counts.items()}


def probability(dist, predicate):
    return sum((p for x, p in dist.items() if predicate(x)), s.S.Zero)


def binomial(n, p):
    # Enumerate the finite Bernoulli sequences, rather than use a mode formula.
    dist = Counter()
    for seq in product((0, 1), repeat=n):
        mass = s.prod(p if bit else 1 - p for bit in seq)
        dist[sum(seq)] += mass
    return dict(dist)


# P3-01: the random variable maps five equiprobable outcomes to three values.
omega = list(range(-2, 3))
d = pmf([w * w for w in omega])
check("P3-01", ({w for w in omega if w * w > 1}, d,
                probability(d, lambda x: x > 1), len(set(d.values())) == 1),
      ({-2, 2}, {0: R(1, 5), 1: R(2, 5), 4: R(2, 5)}, R(2, 5), False),
      (r"\frac25", "不等可能"))

t = s.symbols("t", real=True)
masses = [t, 1 - 3 * t, 2 * t]
allowed = s.reduce_inequalities([v >= 0 for v in masses], t).as_set()
check("P3-02", (sum(masses), allowed, masses[1].subs(t, R(1, 3))),
      (1, s.Interval(0, R(1, 3)), 0), (r"0\le t\le\frac13", "P(X=0)=0"))

d = {-1: R(1, 4), 1: R(1, 2), 3: R(1, 4)}
f1 = probability(d, lambda x: x <= 1)
choices("P3-03", [probability(d, lambda x: x < 1) == R(3, 4),
                   probability(d, lambda x: -1 < x <= 3) == R(1, 2),
                   probability(d, lambda x: -1 <= x < 3) == R(3, 4),
                   d[1] == f1 == R(3, 4)], "C")

p = s.symbols("p", positive=True)
roots = [v for v in s.solve((1 - p) ** 2 - R(9, 16), p) if 0 < v < 1]
pv = roots[0]
check("P3-04", (roots, (1 - pv) ** 2 * pv), ([R(1, 4)], R(9, 64)),
      (r"p=\frac14", r"P(T=3)=\frac9{64}"))

lam = s.symbols("lambda", positive=True)
pois = lambda k, rate: s.exp(-rate) * rate ** k / s.factorial(k)
rates = s.solve(pois(1, lam) / pois(0, lam) - 2, lam)
check("P3-05", (rates, pois(2, rates[0])), ([2], 2 * s.exp(-2)),
      (r"\lambda=2", "P(Y=2)=2e^{-2}"))

d = pmf([u + u for u in (0, 1)])
b = binomial(2, R(1, 2))
choices("P3-06", [all(d.get(k, 0) == b[k] for k in b),
                   d.get(0, 0) == 0, d.get(1, 0) == R(1, 2),
                   d[0] == d[2] == R(1, 2)], "D")
check("P3-06", d, {0: R(1, 2), 2: R(1, 2)}, ("只能取 $0,2$",))

masses_p3_07 = s.binomial(4, 2) * p ** 2 * (1 - p) ** 2
roots = [v for v in s.solve(masses_p3_07 - R(3, 8), p) if 0 < v < 1]
d = binomial(4, roots[0])
dv = {k: s.simplify(v) for k, v in d.items()}
modes = {k for k, v in dv.items() if v == max(dv.values())}
check("P3-07", (roots, modes), ([R(1, 2)], {2}),
      (r"p=\frac12", "唯一最可能值为 $2$"))

geo = lambda k, prob: (1 - prob) ** (k - 1) * prob
cond = geo(3, R(1, 2)) / sum(geo(k, R(1, 2)) for k in range(1, 4))
choices("P3-08", [cond == v for v in [R(1, 2), R(1, 4), R(1, 8), R(1, 7)]], "D")

# P3-09: enumerate subsets for every admissible population composition.
subsets = list(combinations(range(8), 3))
distributions = {
    marked: pmf([sum(x < marked for x in sub) for sub in subsets])
    for marked in range(9)
}
solutions = [marked for marked, dist in distributions.items()
             if dist.get(0, 0) == dist.get(3, 0)]
check("P3-09", (solutions, distributions[solutions[0]]),
      ([4], {0: R(1, 14), 1: R(3, 7), 2: R(3, 7), 3: R(1, 14)}),
      ("$D=4$", r"\frac1{14},\frac37,\frac37,\frac1{14}"))

# The inclusion argument and quantifiers of this proof require human review.
print("MANUAL P3-10 证明：区间包含关系、正分母与尾部相减")

# P3-11: enumerate the 16 paths and retain their original probability weights.
joint = Counter()
for seq in product((0, 1), repeat=4):
    first = next((i + 1 for i, bit in enumerate(seq) if bit), s.oo)
    mass = s.prod(R(1, 3) if bit else R(2, 3) for bit in seq)
    joint[(sum(seq), first)] += mass
den = sum(v for (count, first), v in joint.items() if count == 2)
conditional = {first: v / den for (count, first), v in joint.items() if count == 2}
num = sum(v for (count, first), v in joint.items() if count == 2 and first <= 2)
den2 = sum(v for (count, first), v in joint.items() if first <= 2)
check("P3-11", (conditional, num, den2, num / den2),
      ({1: R(1, 2), 2: R(1, 3), 3: R(1, 6)}, R(20, 81), R(5, 9), R(4, 9)),
      (r"(2) $\frac49$", r"\frac12$ | $\frac13$ | $\frac16"))

j = s.symbols("j", integer=True, nonnegative=True)
q = s.symbols("q", positive=True)
odd_sum = s.summation(q ** (2 * j), (j, 0, s.oo))
# SymPy returns the convergent expression first, with condition q**2 < 1.
series = odd_sum.args[0][0] if isinstance(odd_sum, s.Piecewise) else odd_sum
odd_mass = (1 - q) * series
q_roots = [v for v in s.solve((1 - q) / odd_mass - R(3, 4), q) if 0 < v < 1]
qv = q_roots[0]
finite = sum((1 - qv) * qv ** (k - 1) for k in (1, 3, 5))
check("P3-12", (1 - qv, s.simplify(finite / odd_mass.subs(q, qv))),
      (R(1, 2), R(63, 64)), (r"p=\frac12", r"\frac{63}{64}"))

universe = set(range(1, 7))
a = {x for x in universe if abs(x - 3) <= 1}
b = {x for x in universe if x % 2 == 0}
check("P3-13", (R(len(a | b), 6), R(len(a & b), 6) == R(len(a), 6) * R(len(b), 6)),
      (R(2, 3), False), (r"P(A\cup B)=\frac23", "不独立"))

low, high = binomial(3, R(1, 4))[2], binomial(3, R(3, 4))[2]
total = R(1, 3) * low + R(2, 3) * high
check("P3-14", (low, high, total, R(2, 3) * high / total),
      (R(9, 64), R(27, 64), R(21, 64), R(6, 7)),
      (r"P(X=2)=\frac{21}{64}", r"P(\overline H\mid X=2)=\frac67"))

# Dynamic convolution avoids both enumeration of 2**100 paths and cancellation.
dist = [s.S.One]
for _ in range(100):
    new = [s.S.Zero] * (len(dist) + 1)
    for k, mass in enumerate(dist):
        new[k] += mass * R(99, 100)
        new[k + 1] += mass * R(1, 100)
    dist = new
exact = dist[0] / (dist[0] + dist[1])
rate = 100 * R(1, 100)
approx = pois(0, rate) / (pois(0, rate) + pois(1, rate))
check("P3-15", (sum(dist), exact, approx, abs(approx - exact)),
      (1, R(99, 199), R(1, 2), R(1, 398)),
      (r"\frac{99}{199}", r"\frac12", r"\frac1{398}"))

rate = s.symbols("r", positive=True)
rv = s.solve(s.exp(-15 * rate) - R(1, 8), rate)[0]
five = s.simplify(5 * rv)
at_least = 1 - pois(0, five)
conditional = s.simplify(pois(1, five) / at_least)
check("P3-16", (five, at_least, conditional), (s.log(2), R(1, 2), s.log(2)),
      (r"概率为 $\frac12$", r"概率为 $\ln2$"))

# Keep the numerical checks connected to the printed question inventory.
ids = re.findall(r"^\*\*(P3-\d+)\*\*", problems, re.M)
check("P3-coverage", (ids, set(blocks)),
      ([f"P3-{i:02}" for i in range(1, 17)], set(ids)))
sys.exit(bool(failed))
