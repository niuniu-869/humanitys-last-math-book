"""独立验算 K1.6 题目；结果由逻辑枚举和符号计算得到。"""
from itertools import product
import sympy as sp


def report(qid, ok):
    print(f"{'PASS' if ok else 'FAIL'} {qid}")


def report_manual(qid, ok):
    print(f"MANUAL {qid}" if ok else f"FAIL {qid}")


def sat(clauses, assignment):
    return all(any((assignment[v] if sign else not assignment[v]) for v, sign in c) for c in clauses)


def simplify(clauses, assignment):
    return [tuple((v, sign) for v, sign in clause if v not in assignment)
            for clause in clauses
            if not any(v in assignment and assignment[v] == sign for v, sign in clause)]


def propagate(clauses, initial):
    assignment = dict(initial)
    while True:
        remaining = simplify(clauses, assignment)
        if () in remaining:
            return False, assignment
        unit = next((clause[0] for clause in remaining if len(clause) == 1), None)
        if unit is None:
            return True, assignment
        assignment[unit[0]] = unit[1]


def forward(initial, rules):
    facts, rounds, scans = set(initial), [], 0
    while True:
        added = set()
        for body, head in rules:
            scans += 1
            if set(body) <= facts and head not in facts:
                added.add(head)
        if not added:
            return facts, rounds, scans
        rounds.append(added)
        facts |= added


def backward(initial, rules, target):
    known, seen, expanded = set(initial), [], []

    def visit(goal):
        if goal not in seen:
            seen.append(goal)
        if goal in known:
            return True
        for index, (body, head) in enumerate(rules, 1):
            if head == goal:
                expanded.append(index)
                if all(visit(premise) for premise in body):
                    known.add(goal)
                    return True
        return False

    # The query exercises have no cyclic dependency.
    return visit(target), seen, expanded


def majority(k, q):
    return sum(sp.binomial(k, i) * q**i * (1-q)**(k-i)
               for i in range(k//2 + 1, k+1))


# K16-01
clauses01 = [(("p", False),), (("p", True), ("q", True)), (("q", False), ("r", True)),
             (("r", False), ("s", True)), (("s", False), ("t", True)), (("t", False), ("u", True))]
a01 = {"p": False, "q": True, "r": True, "s": True, "t": True, "u": True}
remaining01 = simplify(clauses01, {"p": False, "q": True})
report("K16-01", remaining01 == [(("r", True),), (("r", False), ("s", True)),
                                 (("s", False), ("t", True)), (("t", False), ("u", True))]
       and propagate(clauses01, {"p": False, "q": True}) == (True, a01)
       and sat(clauses01, a01))

# K16-02
vals = [(False, False), (False, True), (True, False), (True, True)]
truth = [x ^ y for x, y in vals]
opts02 = [lambda x, y: x or y,
          lambda x, y: (not x) or (not y),
          lambda x, y: (x or y) and ((not x) or (not y)),
          lambda x, y: ((not x) or y) and (x or (not y))]
ok02 = [all(f(x, y) == truth[i] for i, (x, y) in enumerate(vals)) for f in opts02]
report("K16-02", ok02 == [False, False, True, False])

# K16-03
facts = {"a", "b"}
rules = [(("a", "b"), "c"), (("c",), "d"), (("b", "d"), "e"),
         (("f",), "g"), (("d", "e"), "h"), (("h",), "c")]
facts, rounds, scans = forward(facts, rules)
report("K16-03", rounds == [{"c"}, {"d"}, {"e"}, {"h"}]
       and facts == {"a", "b", "c", "d", "e", "h"} and scans == 30)

# K16-04
q04 = sp.Rational(97, 100)
n04 = 1
while q04**(n04 + 1) >= sp.Rational(1, 2):
    n04 += 1
report("K16-04", n04 == 22 and q04**22 >= sp.Rational(1, 2) > q04**23
       and round(float(q04**22), 5) == 0.51166
       and round(float(q04**23), 5) == 0.49631)

# K16-05
low, high = sp.Rational(2, 5), sp.Rational(3, 5)
vlow, vhigh = majority(3, low), majority(3, high)
options05 = [vlow > low and vhigh > high, vlow < low and vhigh > high,
             vlow == low and vhigh == high, vlow < low and vhigh < high]
report("K16-05", options05 == [False, True, False, False]
       and vlow == sp.Rational(352, 1000) and vhigh == sp.Rational(648, 1000))

# K16-06
clauses06 = [(("a", False), ("b", True), ("c", True)),
             (("a", False), ("b", True), ("c", False)),
             (("a", False), ("b", False), ("c", True)),
             (("a", False), ("b", False), ("c", False)),
             (("a", True), ("d", True))]
first06 = propagate(clauses06, {"a": True})
true06 = propagate(clauses06, {"a": True, "b": True})
false06 = propagate(clauses06, {"a": True, "b": False})
back06 = propagate(clauses06, {"a": False})
models06 = [bits for bits in product([False, True], repeat=4)
            if sat(clauses06, dict(zip("abcd", bits)))]
report("K16-06", first06 == (True, {"a": True})
       and true06 == (False, {"a": True, "b": True, "c": True})
       and false06 == (False, {"a": True, "b": False, "c": True})
       and back06 == (True, {"a": False, "d": True})
       and set(models06) == {(False, b, c, True) for b, c in product([False, True], repeat=2)})

# K16-07: 实际执行归结，整数正负号分别表示文字及其否定。
def resolve(c1, c2):
    out = set()
    for lit in c1:
        if -lit in c2:
            out.add(frozenset((c1 - {lit}) | (c2 - {-lit})))
    return out


c07 = list(map(frozenset, [{1, 2}, {-1, 3}, {-2, 3}, {-3}, {-1, -2}]))
steps07 = [(c07[1], c07[3], frozenset({-1})),
           (c07[2], c07[3], frozenset({-2})),
           (c07[0], frozenset({-1}), frozenset({2})),
           (frozenset({2}), frozenset({-2}), frozenset())]
resolution_ok = all(expected in resolve(left, right) for left, right, expected in steps07)
clauses07 = [tuple(("pqr"[abs(lit)-1], lit > 0) for lit in clause) for clause in c07]
all_unsat = not any(sat(clauses07, dict(zip("pqr", bits)))
                    for bits in product([False, True], repeat=3))
invalid07 = resolve(c07[0], c07[4])
report_manual("K16-07", resolution_ok and all_unsat and frozenset() not in invalid07
              and sat([clauses07[0], clauses07[4]], {"p": True, "q": False}))

# K16-08
facts08 = {"a", "b"}
rules08 = [(("a",), "c"), (("b", "c"), "d"), (("d",), "e"), (("b",), "f"),
           (("f", "e"), "g"), (("a",), "x"), (("x",), "y")]
closure08, rounds08, _ = forward(facts08, rules08)
query08 = backward(facts08, rules08, "g")
report("K16-08", closure08 == set("abcdefgxy")
       and rounds08 == [{"c", "f", "x"}, {"d", "y"}, {"e"}, {"g"}]
       and query08 == (True, list("gfbedca"), [5, 4, 3, 2, 1]))

# K16-09
facts09 = {"a"}
rules09 = [(("a",), "b"), (("c",), "d")]
closure09, _, _ = forward(facts09, rules09)
clauses09 = [(("a", True),), (("a", False), ("b", True)), (("c", False), ("d", True))]
possible09 = {bits[3] for bits in product([False, True], repeat=4)
              if sat(clauses09, dict(zip("abcd", bits)))}
closed09 = "真" if "d" in closure09 else "假"
open09 = "未知" if possible09 == {False, True} else ("真" if True in possible09 else "假")
options09 = [("真", "真"), ("假", "未知"), ("假", "假"), ("未知", "假")]
report("K16-09", [(closed09, open09) == option for option in options09]
       == [False, True, False, False] and closure09 == {"a", "b"})

# K16-10
q10 = sp.Rational(3, 5)
k10, values10 = 1, []
while True:
    values10.append(majority(k10, q10))
    if values10[-1] >= sp.Rational(7, 10):
        break
    k10 += 2
report("K16-10", k10 == 7 and values10 == list(map(sp.Rational,
       ["0.6", "0.648", "0.68256", "0.710208"])))

# K16-11
independent11 = sum(sp.binomial(5, i) * sp.Rational(3, 5)**i * sp.Rational(2, 5)**(5-i) for i in range(3, 6))
joint11 = [((True,)*5, sp.Rational(3, 5)), ((False,)*5, sp.Rational(2, 5))]
real11 = sum(weight for bits, weight in joint11 if sum(bits) > 2)
pair11 = sum(weight for bits, weight in joint11 if bits[0] and bits[1])
report("K16-11", independent11 == sp.Rational(4266, 6250)
       and real11 == sp.Rational(3, 5) and pair11 != sp.Rational(3, 5)**2)

# K16-12
premises12 = [(("p", True), ("q", True)), (("p", False), ("r", True)),
              (("q", False), ("s", True)), (("r", False), ("s", False))]
all_assignments12 = [{"p": p, "q": qv, "r": r, "s": s} for p in [False, True] for qv in [False, True]
                     for r in [False, True] for s in [False, True]]
counter_valid = any(sat(premises12 + [(("r", False),), (("s", False),)], a) for a in all_assignments12)
counter_r = [a for a in all_assignments12 if sat(premises12, a) and not a["r"]]
report("K16-12", not counter_valid and {"p": False, "q": True, "r": False, "s": True} in counter_r
       and propagate(premises12, {"r": False, "s": False})[0] is False
       and propagate(premises12, {"r": False}) ==
       (True, {"p": False, "q": True, "r": False, "s": True}))

# K16-13
facts13 = {"a", "b"}
rules13 = [(("a",), "c"), (("b",), "f"), (("b", "c"), "d"), (("d",), "e"),
           (("f", "e"), "g"), (("g",), "h"), (("h", "c"), "z"),
           (("a",), "x"), (("x",), "y")]
closure13, rounds13, scans13 = forward(facts13, rules13)
query13 = backward(facts13, rules13, "z")
report("K16-13", rounds13 == [{"c", "f", "x"}, {"d", "y"}, {"e"}, {"g"}, {"h"}, {"z"}]
       and closure13 == set("abcdefghxyz") and scans13 == 63
       and query13 == (True, list("zhgfbedca"), [7, 6, 5, 2, 4, 3, 1]))

# K16-14
# Enumerate all 3^4 sequences, independently of the geometric-sum derivation.
correct14, error14 = sp.Rational(3, 5), sp.Rational(1, 10)
outcomes14 = [("correct", correct14), ("false_pass", (1-correct14)*error14),
              ("reject", (1-correct14)*(1-error14))]
delivered14 = good14 = exists14 = total14 = sp.S.Zero
for sequence in product(outcomes14, repeat=4):
    weight = sp.prod(probability for _, probability in sequence)
    total14 += weight
    first = next((kind for kind, _ in sequence if kind != "reject"), None)
    if first is not None:
        delivered14 += weight
    if first == "correct":
        good14 += weight
    if any(kind == "correct" for kind, _ in sequence):
        exists14 += weight
report("K16-14", total14 == 1 and delivered14 == sp.Rational("0.98320384")
       and good14/delivered14 == sp.Rational("0.9375")
       and good14 == sp.Rational("0.9217536")
       and exists14 == sp.Rational("0.9744") and good14 < exists14)
