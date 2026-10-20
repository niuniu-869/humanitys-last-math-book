"""Exact independent checks for all 23 numbered examples and their numeric tables."""
from functools import lru_cache
from itertools import combinations, permutations, product
import sys

import numpy as np
import sympy as s

R = s.Rational
failures = 0


def check(k, actual, expected):
    global failures
    good = actual == expected
    print(f"{'PASS' if good else 'FAIL'} 例{k}")
    if not good:
        failures += 1
        print(f"  computed={actual}; lesson={expected}")


def uniform(outcomes):
    outcomes = list(outcomes)
    return {o: R(1, len(outcomes)) for o in outcomes}


def probability(space, event):
    return sum((w for o, w in space.items() if event(o)), s.S.Zero)


def conditional(space, event, given):
    return probability(space, lambda o: event(o) and given(o))/probability(space, given)


def binary_space(n, p):
    return {o: p**sum(o)*(1-p)**(n-sum(o)) for o in product((0, 1), repeat=n)}


def rounded(value, digits):
    return round(float(value), digits)


dice = uniform(product(range(1, 7), repeat=2))
has6 = lambda o: 6 in o
large = lambda o: sum(o) >= 10
check(1, (conditional(dice, has6, large), conditional(dice, large, has6)), (R(5, 6), R(5, 11)))
check("1 随堂", conditional(dice, lambda o: sum(o) == 7, lambda o: o[0] != o[1]), R(1, 5))

coins = uniform(product((0, 1), repeat=2))
check(2, (conditional(coins, all, any), conditional(coins, all, lambda o: o[0])), (R(1, 3), R(1, 2)))

pa, pb, pu = R(1, 2), R(2, 5), R(4, 5)
pab = pa+pb-pu
table = {(1, 1): pab, (1, 0): pa-pab, (0, 1): pb-pab, (0, 0): 1-pu}
check(3, (conditional(table, lambda o: o[0], lambda o: o[1]),
          conditional(table, lambda o: o[1], lambda o: o[0]),
          conditional(table, lambda o: o[1], lambda o: not o[0]),
          conditional(table, lambda o: not o[0], lambda o: not o[1])),
      (R(1, 4), R(1, 5), R(3, 5), R(1, 3)))

balls = uniform(permutations(range(8), 2))
replacement = uniform(product(range(8), repeat=2))
first_second = lambda o: o[0] < 5 and o[1] >= 5
check(4, (probability(balls, first_second), probability(replacement, first_second)), (R(15, 56), R(15, 64)))
check("4 随堂", probability(balls, lambda o: o[0] >= 5 and o[1] >= 5), R(3, 28))
cards = list(combinations(range(52), 3))
card_probability = R(sum(all(c < 13 for c in hand) for hand in cards), len(cards))
check(5, (card_probability, rounded(card_probability, 4)), (R(11, 850), 0.0129))

# Construct a full terminating tree, including paths that deviate from the phrase.
tree6 = {"first_other": 1-R(1, 5), "second_other": R(1, 5)*(1-R(1, 2)),
         "third_other": R(1, 5)*R(1, 2)*(1-R(3, 10)),
         "phrase": R(1, 5)*R(1, 2)*R(3, 10)}
check(6, (sum(tree6.values()), tree6["phrase"]), (1, R(3, 100)))

bags = {0: (1, 1, 1, 0, 0), 1: (1, 0, 0, 0, 0)}
space = {(b, i): R(1, 10) for b in bags for i in range(5)}
check(7, probability(space, lambda o: bags[o[0]][o[1]]), R(2, 5))
space = {(b, i): (R(1, 3) if b == 0 else R(2, 3))/5 for b in bags for i in range(5)}
check("7 随堂", probability(space, lambda o: bags[o[0]][o[1]]), R(1, 3))

source = (1, 1, 0)
destination = (1, 0, 0)
space = uniform(product(range(3), range(4)))
check(8, probability(space, lambda o: (destination+(source[o[0]],))[o[1]]), R(5, 12))
space = uniform(permutations(range(10), 2))
check(9, probability(space, lambda o: o[1] < 3), R(3, 10))

boxes = ((1, 1, 0), (1, 0, 0), (0, 0, 0))
space = uniform(product(range(3), range(3)))
event = lambda o: boxes[o[0]][o[1]]
check(10, (probability(space, event), tuple(conditional(space, lambda o, k=k: o[0] == k, event) for k in range(3))),
      (R(1, 3), (R(2, 3), R(1, 3), 0)))

def diagnostic_space(prior, n):
    out = {}
    for d in (0, 1):
        for sequence, weight in binary_space(n, R(95, 100) if d else R(5, 100)).items():
            out[(d,)+sequence] = (prior if d else 1-prior)*weight
    return out

space = diagnostic_space(R(1, 100), 1)
post = conditional(space, lambda o: o[0], lambda o: o[1])
check(11, (probability(space, lambda o: o[1]), post, rounded(100*post, 1)), (R(59, 1000), R(19, 118), 16.1))
check("11 四格表", tuple(int(space[o]*100000) for o in ((1, 1), (1, 0), (0, 1), (0, 0))), (950, 50, 4950, 94050))
priors = (R(1, 1000), R(1, 100), R(1, 10), R(1, 2))
posteriors = [conditional(diagnostic_space(p, 1), lambda o: o[0], lambda o: o[1]) for p in priors]
check("11 先验表", [rounded(100*v, 2 if i == 0 else 1) for i, v in enumerate(posteriors)], [1.87, 16.1, 67.9, 95.0])
rng = np.random.default_rng(2025)
sick = rng.random(100000) < .01
positive = np.where(sick, rng.random(100000) < .95, rng.random(100000) < .05)
check("11 模拟表", (int(sick.sum()), int((sick & positive).sum()), int((~sick & positive).sum()), int(positive.sum()),
                   round(float(sick[positive].mean()), 4)), (1029, 978, 4997, 5975, .1637))

for n, expected in ((1, R(1, 2)), (2, R(2, 3))):
    space = {}
    for coin in range(3):
        for o, weight in binary_space(n, s.S.One if coin == 0 else R(1, 2)).items():
            space[(coin,)+o] = weight/3
    check(12 if n == 1 else "12 随堂", conditional(space, lambda o: o[0] == 0, lambda o: all(o[1:])), expected)

a = lambda o: o[0] % 2 == 1
b = lambda o: sum(o) == 7
c = lambda o: sum(o) == 8
pa, pb, pc = [probability(dice, f) for f in (a, b, c)]
pab = probability(dice, lambda o: a(o) and b(o))
pac = probability(dice, lambda o: a(o) and c(o))
check(13, (pa, pb, pc, pab, pac, pab == pa*pb, pac == pa*pc),
      (R(1, 2), R(1, 6), R(5, 36), R(1, 12), R(1, 18), True, False))

space = {(a, b): (R(2, 5) if a else R(3, 5))*(R(7, 10) if b else R(3, 10))
         for a, b in product((0, 1), repeat=2)}
check(14, (probability(space, all), probability(space, any), space[(1, 0)], space[(0, 0)], sum(space.values())),
      (R(7, 25), R(41, 50), R(3, 25), R(9, 50), 1))

events = (lambda o: o[0], lambda o: o[1], lambda o: o[0] == o[1])
marginals = [probability(coins, e) for e in events]
pairs = [probability(coins, lambda o, i=i, j=j: events[i](o) and events[j](o)) for i, j in combinations(range(3), 2)]
triple = probability(coins, lambda o: all(e(o) for e in events))
check(15, (marginals, pairs, triple, triple == s.prod(marginals)),
      ([R(1, 2)]*3, [R(1, 4)]*3, R(1, 4), False))

space = binary_space(3, R(9, 10))
check(16, tuple(probability(space, f) for f in (all, any, lambda o: sum(o) == 2)),
      (R(729, 1000), R(999, 1000), R(243, 1000)))
space = {(a, b): (R(3, 5) if a else R(2, 5))*R(1, 2) for a, b in product((0, 1), repeat=2)}
check("16 随堂", probability(space, any), R(4, 5))

space = binary_space(10, R(7, 10))
dist = [probability(space, lambda o, k=k: sum(o) == k) for k in range(11)]
check(17, (rounded(dist[7], 4), rounded(sum(dist[8:]), 4), sum(dist), max(range(11), key=dist.__getitem__)),
      (.2668, .3828, 1, 7))
check("17 分布表", [rounded(v, 4) for v in dist], [.0000, .0001, .0014, .0090, .0368, .1029, .2001, .2668, .2335, .1211, .0282])
rng = np.random.default_rng(11)
counts = (rng.random((10000, 10)) < .7).sum(axis=1)
check("17 模拟表", (round(float((counts == 7).mean()), 4), round(float((counts >= 8).mean()), 4)), (.2660, .3801))
check("17 随堂", rounded(1-R(5, 6)**6, 4), .6651)

# Iterate the probability of no hit; do not use the lesson's final power expression.
values = []
for n, chance in ((4, R(1, 6)), (24, R(1, 36))):
    no_hit = s.S.One
    for _ in range(n):
        no_hit *= 1-chance
    values.append(1-no_hit)
check(18, ([rounded(v, 4) for v in values], values[0] > R(1, 2) > values[1]), ([.5177, .4914], True))

@lru_cache(None)
def win(a, b):
    if a == 4:
        return s.S.One
    if b == 4:
        return s.S.Zero
    return R(3, 5)*win(a+1, b)+R(2, 5)*win(a, b+1)

check(19, rounded(win(0, 0), 4), .7102)
space = binary_space(5, R(7, 10))
last = probability(space, lambda o: o[4] and sum(o[:4]) == 2)
unrestricted = probability(space, lambda o: sum(o) == 3)
check(20, (rounded(last, 4), unrestricted, last < unrestricted), (.1852, R(3087, 10000), True))

space = diagnostic_space(R(1, 100), 2)
both = probability(space, lambda o: all(o[1:]))
single = probability(space, lambda o: o[1])
post2 = conditional(space, lambda o: o[0], lambda o: all(o[1:]))
sequential = post*R(95, 100)/(post*R(95, 100)+(1-post)*R(5, 100))
check(21, (both, post2, sequential, rounded(100*post2, 1), both == single**2),
      (R(23, 2000), R(361, 460), R(361, 460), 78.5, False))
check("21 舍入", (rounded(single**2, 4), rounded(both/single**2, 1),
                 rounded(R(161, 1000)*R(95, 100)/(R(161, 1000)*R(95, 100)+R(839, 1000)*R(5, 100)), 3)),
      (.0035, 3.3, .785))

given = lambda o: sum(o) == 1
unconditional_independent = probability(coins, all) == probability(coins, lambda o: o[0])*probability(coins, lambda o: o[1])
conditional_independent = conditional(coins, all, given) == conditional(coins, lambda o: o[0], given)*conditional(coins, lambda o: o[1], given)
check(22, (probability(coins, all), conditional(coins, lambda o: o[0], given),
           conditional(coins, lambda o: o[1], given), conditional(coins, all, given),
           unconditional_independent, conditional_independent),
      (R(1, 4), R(1, 2), R(1, 2), 0, True, False))

space = {}
for category in (0, 1):
    prior, p, q = (R(3, 10), R(3, 5), R(2, 5)) if category else (R(7, 10), R(1, 20), R(1, 50))
    for a, b in product((0, 1), repeat=2):
        space[(category, a, b)] = prior*(p if a else 1-p)*(q if b else 1-q)
single = conditional(space, lambda o: o[0], lambda o: o[1])
both = conditional(space, lambda o: o[0], lambda o: all(o[1:]))
check(23, (single, both, space[(1, 1, 1)], space[(0, 1, 1)],
           rounded(single, 3), rounded(both, 3), rounded(100*single, 1), rounded(100*both, 1)),
      (R(36, 43), R(720, 727), R(9, 125), R(7, 10000), .837, .990, 83.7, 99.0))

sys.exit(bool(failures))
