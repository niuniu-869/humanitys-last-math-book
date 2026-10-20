"""Recompute from sample spaces or symbolic constraints; compare with answers.md."""
from itertools import combinations, permutations, product
from pathlib import Path
import re
import sys

import sympy as s

R = s.Rational
failures = 0


def check(tag, actual, expected):
    global failures
    passed = actual == expected
    print(f"{'PASS' if passed else 'FAIL'} {tag}")
    if not passed:
        failures += 1
        print(f"  computed={actual}; answer={expected}")


def probability(space, event):
    return s.simplify(sum(w for outcome, w in space.items() if event(outcome)))


def conditional(space, event, given):
    denominator = probability(space, given)
    assert denominator > 0
    return s.simplify(probability(space, lambda o: event(o) and given(o)) / denominator)


def choices(pid, truth, chosen):
    for label, value in zip("ABCD", truth):
        check(f"{pid}({label})", bool(value), label == chosen)
    check(pid, [label for label, value in zip("ABCD", truth) if value], [chosen])


def binary_space(n, p):
    return {o: p ** sum(o) * (1 - p) ** (n - sum(o))
            for o in product((0, 1), repeat=n)}


# 01: Recover the complete joint table from the three supplied probabilities.
pa, pb, pab = R(2, 3), R(1, 2), R(1, 6)
space = {(1, 1): pab, (1, 0): pa-pab, (0, 1): pb-pab,
         (0, 0): 1-pa-pb+pab}
value = conditional(space, lambda o: o[0], lambda o: o[1])
choices("P2-01", [value == v for v in (R(1, 6), R(1, 4), R(1, 3), R(2, 3))], "C")

# 02: Solve the chain constraint for the missing factor.
z = s.symbols("z", real=True)
factor = s.solve(s.Eq(R(3, 5)*R(1, 2)*z, R(3, 50)), z)[0]
check("P2-02", (factor, R(3, 5)*R(1, 2)*(1-factor)), (R(1, 5), R(6, 25)))

p = s.solve(s.Eq(z*R(3, 4)+(1-z)*R(1, 4), R(2, 5)), z)[0]
check("P2-03", (p, s.cancel(p*R(3, 4)/R(2, 5))), (R(3, 10), R(9, 16)))

space = {(a, b): (R(1, 3) if a else R(2, 3)) * R(1, 2)
         for a, b in product((0, 1), repeat=2)}
pab = probability(space, lambda o: all(o))
pu = probability(space, lambda o: any(o))
pc = conditional(space, lambda o: not o[0], lambda o: not o[1])
choices("P2-04", [pab == 0, pu == R(5, 6), pab == R(1, 3), pc == R(2, 3)], "D")

# 05: Solve for the three disjoint pieces B\C, C\B, BC inside A.
u, v, w = s.symbols("u v w")
pieces = s.solve([u+w-R(3, 5)*R(1, 2), v+w-R(7, 10)*R(2, 7),
                  w-(R(3, 5)+R(7, 10)-1)*R(1, 3)], (u, v, w))
total = sum(pieces.values())
check("P2-05", (total, total == R(3, 5)*R(1, 2)+R(7, 10)*R(2, 7)), (R(2, 5), False))

t = s.symbols("t", real=True)
cells = (t, R(1, 3)-t, R(1, 2)-t, R(1, 6)+t)
domain = s.reduce_inequalities([c >= 0 for c in cells], t).as_set()
pa, pb = sum(cells[:2]), cells[0]+cells[2]
independent_t = s.solve(t-pa*pb, t)
conditional_value = ((cells[1]+cells[2])/(1-cells[0])).subs(t, independent_t[0])
check("P2-06", (domain, independent_t, conditional_value),
      (s.Interval(0, R(1, 3)), [R(1, 6)], R(3, 5)))

space = binary_space(5, R(1, 3))
v1 = conditional(space, lambda o: sum(o[:4]) == 1 and o[4] == 1,
                 lambda o: sum(o) == 2)
v2 = conditional(space, lambda o: sum(o) == 2, lambda o: sum(o) >= 1)
check("P2-07", (v1, v2), (R(2, 5), R(80, 211)))

outcomes = list(permutations(range(1, 7), 3))
count = sum(sum(x <= 2 for x in o) == 2 for o in outcomes)
value = R(count, len(outcomes))
choices("P2-08", [value == v for v in (R(2, 9), R(1, 5), R(1, 15), R(1, 9))], "B")
check("P2-08 次序辨析", R(sum(o[0] <= 2 and o[1] <= 2 and o[2] > 2 for o in outcomes), len(outcomes)), R(1, 15))

print("MANUAL P2-09 证明：在固定条件 C 下使用补事件与加法公式")

x = s.symbols("x", real=True)
conditional_cells = (x, R(1, 4)-x, R(3, 4)-x, x)
domain = s.reduce_inequalities([c >= 0 for c in conditional_cells], x).as_set()
joint = R(1, 2)*R(3, 4)*R(1, 4)+R(1, 2)*x
independent_x = s.solve(joint-R(1, 2)**2, x)[0]
check("P2-10", (domain, s.Interval(joint.subs(x, domain.start), joint.subs(x, domain.end)),
                independent_x, domain.contains(independent_x)),
      (s.Interval(0, R(1, 4)), s.Interval(R(3, 32), R(7, 32)), R(5, 16), s.false))

# 11: Enumerate D and all three outcomes, then normalize the requested slices.
space = {}
for d in (0, 1):
    prior, chance = (R(1, 3), R(3, 4)) if d else (R(2, 3), R(1, 4))
    for o, weight in binary_space(3, chance).items():
        space[(d,)+o] = prior*weight
given_h = lambda o: o[1] == 1 and o[2] == 0
post1 = conditional(space, lambda o: o[0], lambda o: o[1])
post2 = conditional(space, lambda o: o[0], given_h)
predict = conditional(space, lambda o: o[3], given_h)
post3 = conditional(space, lambda o: o[0], lambda o: given_h(o) and o[3])
updated = post2*R(3, 4)/(post2*R(3, 4)+(1-post2)*R(1, 4))
check("P2-11", (post1, post2, predict, post3, updated),
      (R(3, 5), R(1, 3), R(5, 12), R(3, 5), R(3, 5)))

# 12: Solve seven marginal constraints and the triple-intersection constraint.
bits = list(product((0, 1), repeat=3))
weights = s.symbols("w0:8")
equations = [sum(weights)-1]
for indices in ((0,), (1,), (2,), (0, 1), (0, 2), (1, 2)):
    equations.append(sum(w for b, w in zip(bits, weights) if all(b[i] for i in indices))-R(1, 2)**len(indices))
equations.append(weights[-1]-t)
solution = s.solve(equations, weights)
space = {b: solution[w] for b, w in zip(bits, weights)}
expected_cells = {b: t if sum(b) % 2 else R(1, 4)-t for b in bits}
domain = s.reduce_inequalities([w >= 0 for w in space.values()], t).as_set()
union = probability(space, lambda o: any(o))
cond = conditional(space, lambda o: o[0], lambda o: o[1] or o[2])
cond_endpoints = sorted([cond.subs(t, domain.start), cond.subs(t, domain.end)])
check("P2-12", (space, domain, s.expand(union), s.expand(cond),
                s.Interval(union.subs(t, domain.start), union.subs(t, domain.end)),
                s.Interval(*cond_endpoints), s.solve(t-R(1, 2)**3, t)),
      (expected_cells, s.Interval(0, R(1, 4)), R(3, 4)+t, R(2, 3)-4*t/3,
       s.Interval(R(3, 4), 1), s.Interval(R(1, 3), R(2, 3)), [R(1, 8)]))

# Integration is an independent area calculation, not needed in the written solution.
area_b = s.integrate(1-x, (x, 0, 1))
area_ab = s.integrate(1-x, (x, 0, R(1, 2)))
area_other = s.integrate(1-x, (x, R(1, 2), 1))
check("P2-13", (area_ab/area_b, area_other/R(1, 2), area_ab == R(1, 2)*area_b),
      (R(3, 4), R(1, 4), False))

outcomes = list(combinations(range(1, 9), 3))
restricted = [o for o in outcomes if max(o) == 8]
value = R(sum(sum(o[:-1]) % 2 == 1 for o in restricted), len(restricted))
check("P2-14", value, R(4, 7))

p, q = s.symbols("p q", real=True)
solutions = s.solve([p*q-R(3, 8), 1-(1-p)*(1-q)-R(7, 8)], (p, q))
valid = [(a, b) for a, b in solutions if 0 <= b <= a <= 1]
pp, qq = valid[0]
value = s.cancel((pp*(1-qq)+(1-pp)*qq)/(1-(1-pp)*(1-qq)))
check("P2-15", (valid, value), ([(R(3, 4), R(1, 2))], R(4, 7)))

# Check the delivered text as well, including every answer and its character cap.
root = Path(__file__).resolve().parents[1]
problems = (root / "problems.md").read_text()
answers = (root / "answers.md").read_text()
pids = re.findall(r"^\*\*(P2-\d+)\*\*", problems, re.M)
blocks = dict(re.findall(r"^\*\*(P2-\d+)\*\*\n(.*?)(?=^\*\*P2-|\Z)", answers, re.M | re.S))
tiers = dict(re.findall(r"^\*\*(P2-\d+)\*\*〔([ABC])", problems, re.M))
check("题号覆盖", pids == [f"P2-{i:02}" for i in range(1, 16)] and set(pids) == set(blocks), True)
for pid, block in blocks.items():
    body = block.split("\n### ")[0].strip()
    cap = {"A": 400, "B": 900, "C": 1400}[tiers[pid]]
    check(f"{pid} 格式与字数", body.startswith("**答案：**") and
          body.splitlines()[-1].startswith("区分点：") and len(body) <= cap, True)

sys.exit(bool(failures))
