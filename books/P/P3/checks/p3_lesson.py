"""Check all 21 numbered examples using exact sums or explicit sample spaces.

Four-decimal printed values use a half-unit rounding tolerance. These tests
check mathematical results, not the illustrative simulation frequencies.
"""
from collections import Counter
from itertools import combinations, product
import sys

import sympy as s

R = s.Rational
failed = 0


def eq(a, b):
    return s.simplify(a - b) == 0


def rounded(actual, printed, places=4):
    return abs(float(actual) - printed) < 0.5 * 10 ** (-places)


def check(number, *conditions):
    global failed
    good = all(bool(c) for c in conditions)
    print(("PASS " if good else "FAIL ") + f"例{number}")
    failed += not good


def distribution(values):
    c = Counter(values)
    return {k: R(n, len(values)) for k, n in c.items()}


def event(d, pred):
    return sum((p for k, p in d.items() if pred(k)), s.S.Zero)


def binom(n, p, k):
    return s.binomial(n, k) * p ** k * (1 - p) ** (n - k)


# Enumerating these small spaces provides a route independent of the formulas.
coin = distribution([sum(seq) for seq in product((0, 1), repeat=3)])
check(1, event(coin, lambda k: k <= 2) == R(7, 8),
      event(coin, lambda k: k != 3) == R(7, 8))
dice = list(product(range(1, 7), repeat=2))
check(2, R(sum(a + b == 4 for a, b in dice), 36) == R(1, 12),
      R(sum(max(a, b) <= 2 for a, b in dice), 36) == R(1, 9))
d = distribution([max(pair) for pair in dice])
check(3, set(d) == set(range(1, 7)), sum(d.values()) == 1,
      all(d[k] == R(2 * k - 1, 36) for k in d))
d = distribution([sum(i < 3 for i in sub) for sub in combinations(range(5), 2)])
check(4, d == {0: R(1, 10), 1: R(6, 10), 2: R(3, 10)})
c = s.symbols("c")
cv = s.solve(sum(c * k for k in range(1, 5)) - 1, c)[0]
check(5, cv == R(1, 10), sum(cv * k for k in (1, 2)) == R(3, 10))
counts = [4, 3, 2, 1]
probs = [R(n, sum(counts)) for n in counts]
check(6, probs == [R(4, 10), R(3, 10), R(2, 10), R(1, 10)],
      sum(probs) == 1, sum(probs[:2]) == R(7, 10))

check(7, event(coin, lambda k: R(1, 2) < k <= 2) == R(3, 4),
      event(coin, lambda k: k < 2) == R(1, 2),
      event(coin, lambda k: k <= 2) == R(7, 8))
levels = [0, R(3, 10), R(8, 10), 1]
d = dict(zip((-1, 1, 3), [b - a for a, b in zip(levels, levels[1:])]))
check(8, d == {-1: R(3, 10), 1: R(1, 2), 3: R(1, 5)},
      event(d, lambda k: k < 1) == R(3, 10),
      event(d, lambda k: -1 < k <= 3) == R(7, 10))


def step_cdf_properties(levels, endpoint_values):
    # A finite step function is fully determined by its interval levels and
    # values at the breakpoints; compare each endpoint with the right level.
    monotone = all(a <= b for a, b in zip(levels, levels[1:]))
    right = all(a == b for a, b in zip(endpoint_values, levels[1:]))
    limits = levels[0] == 0 and levels[-1] == 1
    return monotone, right, limits


props = [step_cdf_properties([0, R(2, 5), 1], [R(2, 5), 1]),
         step_cdf_properties([0, R(2, 5), 1], [0, R(2, 5)]),
         step_cdf_properties([0, R(7, 10), R(1, 2), 1], [R(7, 10), R(1, 2), 1])]
check(9, [all(v) for v in props] == [True, False, False],
      props[1] == (True, False, True), props[2] == (False, True, True))

terms = [binom(10, R(7, 10), k) for k in (8, 9, 10)]
check(10, all(rounded(a, b) for a, b in zip(terms, [0.2335, 0.1211, 0.0282])),
      rounded(sum(terms), 0.3828))
nmin = next(n for n in range(1, 100) if 1 - R(5, 6) ** n >= R(95, 100))
check(11, nmin == 17, rounded(1 - R(5, 6) ** 6, 0.6651),
      rounded(s.log(R(1, 20)) / s.log(R(5, 6)), 16.4, places=1))
d = {k: binom(9, R(3, 10), k) for k in range(10)}
check(12, {k for k, p in d.items() if p == max(d.values())} == {2, 3},
      d[2] == d[3], rounded(d[2], 0.2668))

geom = lambda k, p: (1 - p) ** (k - 1) * p
check(13, geom(3, R(7, 10)) == R(63, 1000),
      sum(geom(k, R(7, 10)) for k in range(1, 4)) == R(973, 1000))
k = s.symbols("k", integer=True, positive=True)
tail3 = s.summation(geom(k, R(7, 10)), (k, 4, s.oo))
num = sum(geom(k, R(7, 10)) for k in (4, 5))
check(14, num / tail3 == R(91, 100))
j = s.symbols("j", integer=True, positive=True)
even = s.summation(geom(2 * j, R(1, 6)), (j, 1, s.oo))
check(15, even == R(5, 11))

d = distribution([sum(i < 5 for i in sub) for sub in combinations(range(20), 4)])
expected16 = [0.2817, 0.4696, 0.2167, 0.0310, 0.0010]
check(16, set(d) == set(range(5)), sum(d.values()) == 1,
      all(rounded(d[k], v) for k, v in enumerate(expected16)),
      all(d[k] == s.binomial(5, k) * s.binomial(15, 4 - k) / s.binomial(20, 4) for k in d),
      rounded(1 - d[0], 0.7183), rounded(R(3, 4) ** 4, 0.3164))
d = distribution([sum(i < 7 for i in sub) for sub in combinations(range(10), 5)])
check(17, d == {2: R(1, 12), 3: R(5, 12), 4: R(5, 12), 5: R(1, 12)},
      sum(d.values()) == 1)
# Sequential conditional probabilities, independent of the printed combination ratio.
no_marked = s.prod(R(46 - i, 50 - i) for i in range(5))
check(18, eq(no_marked, s.binomial(46, 5) / s.binomial(50, 5)),
      rounded(no_marked, 0.6470), rounded(1 - no_marked, 0.3530))

pois = lambda k, rate: s.exp(-rate) * rate ** k / s.factorial(k)
rate = 3 * R(1, 2)
check(19, rate == R(3, 2), rounded(pois(0, rate), 0.2231),
      rounded(1 - pois(0, rate), 0.7769))
exact20 = sum(binom(200, R(1, 200), k) for k in range(2, 201))
approx20 = 1 - sum(pois(k, 1) for k in range(2))
check(20, eq(approx20, 1 - 2 / s.E), rounded(approx20, 0.2642),
      rounded(exact20, 0.2642), format(float(exact20), ".4f") == format(float(approx20), ".4f"))
exact21 = 1 - sum(binom(1000, R(1, 500), k) for k in range(3))
approx21 = 1 - sum(pois(k, 2) for k in range(3))
check(21, eq(approx21, 1 - 5 * s.exp(-2)),
      rounded(approx21, 0.3233), rounded(exact21, 0.3233))

sys.exit(bool(failed))
