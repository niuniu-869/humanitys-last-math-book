"""Check all 12 numbered lesson examples with exact or stable numerical methods."""
from collections import Counter
from functools import lru_cache
from itertools import permutations, product
import sys

import numpy as np
import sympy as sp

Q = sp.Rational


@lru_cache(None)
def quicksort_outcomes(order):
    """Enumerate fresh uniform pivot choices, executing K3.2.4 PARTITION."""
    if len(order) < 2:
        return {(order, 0): sp.S.One}
    outcomes = Counter()
    for s in range(len(order)):
        a = list(order)
        hi = len(a) - 1
        a[s], a[hi] = a[hi], a[s]
        pivot = a[hi]
        i, comparisons = -1, 0
        for j in range(hi):
            comparisons += 1
            if a[j] <= pivot:
                i += 1
                a[i], a[j] = a[j], a[i]
        q = i + 1
        a[q], a[hi] = a[hi], a[q]
        for (left, lc), lp in quicksort_outcomes(tuple(a[:q])).items():
            for (right, rc), rp in quicksort_outcomes(tuple(a[q + 1:])).items():
                result = left + (a[q],) + right
                outcomes[(result, comparisons + lc + rc)] += lp * rp / len(a)
    return dict(outcomes)


def executed_distribution(order):
    result = Counter()
    for (sorted_order, comparisons), probability in quicksort_outcomes(tuple(order)).items():
        assert sorted_order == tuple(sorted(order))
        result[comparisons] += probability
    assert sum(result.values()) == 1
    return dict(result)


@lru_cache(None)
def comparison_distribution(n):
    if n < 2:
        return {0: sp.S.One}
    result = Counter()
    for left in range(n):
        for x, px in comparison_distribution(left).items():
            for y, py in comparison_distribution(n - 1 - left).items():
                result[n - 1 + x + y] += px * py / n
    return dict(result)


def pair_sets(n):
    result = []
    for order in permutations(range(1, n + 1)):
        priority = {v: i for i, v in enumerate(order)}
        pairs = set()

        def sort(keys):
            if len(keys) < 2:
                return
            pivot = min(keys, key=priority.get)
            pairs.update(tuple(sorted((pivot, x))) for x in keys if x != pivot)
            sort([x for x in keys if x < pivot])
            sort([x for x in keys if x > pivot])

        sort(list(range(1, n + 1)))
        result.append(pairs)
    return result


def ex01():
    assert executed_distribution((2, 5, 9)) == {2: Q(1, 3), 3: Q(2, 3)}
    for n in range(7):
        for order in permutations(range(n)):
            assert executed_distribution(order) == comparison_distribution(n)
    means = [sum(x * p for x, p in comparison_distribution(n).items()) for n in range(2, 7)]
    assert means == [1, Q(8, 3), Q(29, 6), Q(37, 5), Q(103, 10)]
    d = comparison_distribution(6)
    assert min(d) == 8 and max(d) == 15 and d[15] == Q(2, 45)


def ex02():
    for n, expected in [(4, Q(29, 6)), (6, Q(103, 10))]:
        outcomes = pair_sets(n)
        assert Q(sum(map(len, outcomes)), len(outcomes)) == expected
        assert sum((n - d) * Q(2, d + 1) for d in range(1, n)) == expected


def ex03():
    outcomes = pair_sets(6)
    actual = [Q(sum(sum(key in pair for pair in s) for s in outcomes), len(outcomes))
              for key in (1, 3)]
    assert actual == [Q(29, 10), Q(23, 6)]


def ex04():
    n, m = sp.symbols("n m", integer=True, positive=True)
    i = sp.symbols("i", integer=True)
    assert sp.summation(1 / m, (i, 1, n)) == n / m
    # Fully dependent indicators also realize the rewritten example.
    dependent = [(0, Q(3, 4)), (6, Q(1, 4))]
    assert sum(value * weight for value, weight in dependent) == Q(3, 2)
    loads = [slots.count(0) for slots in product(range(4), repeat=6)]
    assert Q(sum(loads), len(loads)) == Q(3, 2)
    chains = [[x for x in (5, 2, 8, 1, 9, 3) if x % 4 == s] for s in range(4)]
    assert chains == [[8], [5, 1, 9], [2], [3]]
    assert chains[1].index(9) + 1 == 3 and chains[2].index(2) + 1 == 1


def ex05():
    n, m = sp.symbols("n m", integer=True, positive=True)
    j = sp.symbols("j", integer=True)
    upper = sp.summation(1 / m, (j, 1, n - 1))
    assert sp.simplify(upper - (n - 1) / m) == 0
    assert sp.simplify(n / m - upper).is_positive
    # All Z_i share W: the two outcomes have probabilities 1-1/m and 1/m.
    attained = 0 * (1 - 1 / m) + (n - 1) * (1 / m)
    assert sp.simplify(attained - upper) == 0
    # A joint model with strongly dependent collision indicators still obeys the bound.
    outcomes = [(0, 0, 0), (0, 1, 2), (1, 2, 0)]
    pair_prob = [Q(sum(s[i] == s[j] for s in outcomes), 3)
                 for i in range(3) for j in range(i + 1, 3)]
    actual = Q(sum(sum(s[0] == x for x in s[1:]) for s in outcomes), 3)
    assert pair_prob == [Q(1, 3)] * 3 and actual == Q(2, 3)


def ex06():
    def collision(n):
        return 1 - sp.prod(Q(365 - i, 365) for i in range(n))
    p22, p23 = collision(22), collision(23)
    assert p22 < Q(1, 2) < p23
    assert abs(float(p22) - 0.4757) < 0.00005
    assert abs(float(p23) - 0.5073) < 0.00005
    assert sp.binomial(23, 2) == 253
    assert abs(float(Q(253, 365)) - 0.69) < 0.005
    bound = sp.exp(-Q(253, 365))
    assert float(1 - p23) <= float(bound) < 0.5
    assert abs(float(bound) - 0.49999825) < 0.000000005


def ex07():
    n, m = 10 ** 5, 2 ** 32
    exponent = n * (n - 1) / (2 * m)
    approximate = -np.expm1(-exponent)
    exact = -np.expm1(np.log1p(-np.arange(n, dtype=float) / m).sum())
    half = np.sqrt(2 * np.log(2) * m)
    assert abs(exponent - 1.16) < 0.005
    assert abs(exact - 0.69) < 0.005 and abs(exact - approximate) < 0.00001
    assert abs(half - 77000) < 500
    assert abs(m / 1e9 - 4.29) < 0.005


def ex08():
    A, B, C = sp.Matrix([[1, 2], [3, 4]]), sp.Matrix([[0, 1], [1, 0]]), sp.Matrix([[2, 1], [4, 4]])
    assert A * B == sp.Matrix([[2, 1], [4, 3]])
    assert A * B - C == sp.Matrix([[0, 0], [0, -1]])
    expected = [((0, 0), (0, 0), (0, 0)), ((0, 1), (2, 4), (2, 4)),
                ((1, 0), (1, 3), (1, 4)), ((1, 1), (3, 7), (3, 8))]
    passed = []
    for bits, row in zip(((0, 0), (1, 0), (0, 1), (1, 1)), expected):
        r = sp.Matrix(bits)
        actual = tuple(tuple(v) for v in (B * r, A * (B * r), C * r))
        assert actual == row
        passed.append(A * (B * r) == C * r)
    assert passed == [True, True, False, False]


def ex09():
    threshold = Q(1, 10 ** 6)
    t = next(k for k in range(1, 100) if Q(1, 2) ** k < threshold)
    assert t == 20 and 2 ** t == 1048576 and 2 ** (t - 1) == 524288
    n = sp.symbols("n", integer=True, positive=True)
    # Three dense matrix-vector products per round; the fixed factor does not change the order.
    cost = t * 3 * n ** 2
    assert sp.degree(cost, n) == 2


def ex10():
    accepted = Counter(x for x in range(8) if x not in (0, 7))
    p = Q(sum(accepted.values()), 8)
    k = sp.symbols("k", integer=True, positive=True)
    mean = sp.summation(k * (1 - p) ** (k - 1) * p, (k, 1, sp.oo))
    assert p == Q(3, 4) and mean == Q(4, 3) and 3 * mean == 4
    assert {x: Q(count, 8) / p for x, count in accepted.items()} == {x: Q(1, 6) for x in range(1, 7)}


def ex11():
    draws = [3 * (u - 1) + v - 1 for u, v in product((1, 2, 3), repeat=2)]
    assert Counter(draws) == Counter(range(9))
    retry = Q(sum(j >= 5 for j in draws), len(draws))
    a = sp.symbols("a")
    acceptance = {1: sp.S.One}
    for x, threshold in ((2, 3), (3, 2)):
        immediate = Q(sum(j < threshold for j in draws), len(draws))
        # An auxiliary rejection returns to the SAME candidate's state.
        acceptance[x] = sp.solve(a - immediate - retry * a, a)[0]
    assert acceptance == {1: 1, 2: Q(3, 5), 3: Q(2, 5)}
    for j in range(5):
        immediate = Q(draws.count(j), len(draws))
        assert sp.solve(a - immediate - retry * a, a) == [Q(1, 5)]
    accepted = {x: Q(1, 3) * acceptance[x] for x in (1, 2, 3)}
    p = sum(accepted.values())
    assert p == Q(2, 3) and 1 / p == Q(3, 2)
    k = sp.symbols("k", integer=True, positive=True)
    final = [sp.summation((1 - p) ** (k - 1) * accepted[x], (k, 1, sp.oo))
             for x in (1, 2, 3)]
    assert final == [Q(1, 2), Q(3, 10), Q(1, 5)]


def ex12():
    costs, depths = {0: sp.S.Zero, 1: sp.S.Zero}, {0: 0, 1: 0}
    reached = set()
    for n in range(2, 101):
        keys = list(range(n))
        q = n // 4
        ranks = []
        for candidate in keys:
            rank = 1 + sum(other < candidate for other in keys if other != candidate)
            if q + 1 <= rank <= n - q:
                ranks.append(rank)
        p = Q(len(ranks), n)
        assert len(ranks) == n - 2 * q and p >= Q(1, 2)
        assert (1 / p == 2) == (n % 4 == 0)
        local_cost = (n - 1) / p + n - 1
        assert local_cost <= 3 * (n - 1)
        children = [(rank - 1, n - rank) for rank in ranks]
        for left, right in children:
            reached.update((left, right))
            assert left + right == n - 1 and max(left, right) <= Q(3 * n, 4)
        depths[n] = 1 + max(max(depths[left], depths[right]) for left, right in children)
        costs[n] = local_cost + sum(costs[left] + costs[right] for left, right in children) / len(ranks)
        bound_depth, size_bound = 0, Q(n)
        while size_bound > 1:
            bound_depth += 1
            size_bound *= Q(3, 4)
        assert depths[n] <= bound_depth
        assert costs[n] <= 3 * n * bound_depth
    assert {2, 3, 5, 6, 7}.issubset(reached)
    # The four residue classes verify the size and success bounds for all n.
    k = sp.symbols("k", integer=True, nonnegative=True)
    for residue in range(4):
        n = 4 * k + residue
        assert sp.expand(2 * (n - 2 * k) - n) == residue
        assert sp.simplify(3 * n / 4 - (n - k - 1)) == 1 - Q(residue, 4)


if __name__ == "__main__":
    failed = 0
    for number in range(1, 13):
        try:
            globals()[f"ex{number:02}"]()
        except Exception as exc:
            failed += 1
            print(f"FAIL 例{number} {type(exc).__name__}: {exc}")
        else:
            print(f"PASS 例{number}")
    sys.exit(bool(failed))
