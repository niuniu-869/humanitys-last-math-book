"""P.1 题目独立验算；数值由组合、集合或几何计算得到，再核对答案文本。"""
from fractions import Fraction as F
from itertools import combinations, permutations, product
from math import comb, factorial
from pathlib import Path
import re
import sympy as sp

ANS = Path(__file__).resolve().parents[1] / "answers.md"
text = ANS.read_text(encoding="utf-8")

def section(tag):
    m = re.search(rf"\*\*{tag}\*\*(.*?)(?=\n\*\*P1-|\Z)", text, re.S)
    return m.group(1) if m else ""

def ok(tag, cond):
    print(f"PASS {tag}" if bool(cond) else f"FAIL {tag}")

def answer(tag, *parts):
    s = section(tag)
    ok(tag, all(p in s for p in parts))

# P1-01
omega = {(m, M) for m in range(1, 7) for M in range(m, 7)}
event = {(m, M) for m, M in omega if M - m == 2}
answer("P1-01", "(1,3)", "(2,4)", "(3,5)", "(4,6)")
ok("P1-01集合", len(omega) == 21 and len(event) == 4)

# P1-02：真值表独立验证德摩根律
truth = list(product([False, True], repeat=3))
target02 = lambda A, B, C: not ((not (A or (not B))) or C)
equiv = all(target02(A, B, C) == ((A or (not B)) and (not C)) for A, B, C in truth)
answer("P1-02", "**答案：** (A)")
ok("P1-02布尔", equiv)
opt02 = [
    lambda A, B, C: (A or (not B)) and (not C),
    lambda A, B, C: ((not A) or B) and (not C),
    lambda A, B, C: A or (not B) or (not C),
    lambda A, B, C: (A or (not B)) and C,
]
ok("P1-02选项", all(opt02[0](*w) == target02(*w) for w in truth) and all(any(opt02[i](*w) != target02(*w) for w in truth) for i in [1, 2, 3]))
# P1-06：真值表独立验证分配律化简
equiv06 = all(((A or B) and ((not A) or C)) == ((A and C) or ((not A) and B)) for A, B, C in truth)
answer("P1-06", "**答案：** (A)")
ok("P1-06布尔", equiv06)
opt06 = [
    lambda A, B, C: (A and C) or ((not A) and B),
    lambda A, B, C: (A and B) or ((not A) and C),
    lambda A, B, C: A or (B and C),
    lambda A, B, C: (A and C) or (A and B),
]
target06 = lambda A, B, C: (A or B) and ((not A) or C)
ok("P1-06选项", all(target06(*w) == opt06[0](*w) for w in truth) and all(any(target06(*w) != opt06[i](*w) for w in truth) for i in [1, 2, 3]))

# P1-03
given03 = [F(45, 100), F(20, 100), F(10, 100)]
pUnion = sum(given03)
pNone = 1 - pUnion
changed_none = 1 - sum(given03[:2]) - F(40, 100)
answer("P1-03", "0.75", "0.25", "不能实现")
ok("P1-03计算", all(p >= 0 for p in given03 + [pNone]) and (pUnion, pNone, changed_none) == (F(75, 100), F(25, 100), F(-5, 100)))

# P1-04
dice3 = list(product(range(1, 7), repeat=3))
p04 = F(sum(w.count(6) == 1 and 2 in w for w in dice3), len(dice3))
answer("P1-04", "**答案：** (D)", r"\dfrac18")
ok("P1-04计数", p04 == F(3 * (5**2 - 4**2), 6**3) == F(1, 8))
opt04 = [F(1, 24), F(1, 9), F(25, 72), F(1, 8)]
mistakes04 = [
    F(sum(w[0] == 6 and w.count(6) == 1 and 2 in w for w in dice3), len(dice3)),
    F(sum(w.count(6) == 1 and w.count(2) == 1 for w in dice3), len(dice3)),
    F(sum(w.count(6) == 1 for w in dice3), len(dice3)),
]
ok("P1-04选项", mistakes04 == opt04[:3] and opt04[3] == p04 and all(v != p04 for v in opt04[:3]))

# P1-05
ordered = list(product(range(1, 7), repeat=2))
count_diff1 = sum(abs(i - j) == 1 for i, j in ordered)
answer("P1-05", r"\dfrac5{18}")
ok("P1-05计数", F(count_diff1, len(ordered)) == F(5, 18))

# P1-07：按三重交被计数的次数计算“恰好一个”和“至少两个”。
p = [F(36, 100), F(48, 100), F(30, 100)]
pairs = [F(12, 100), F(10, 100), F(8, 100)]
triple = F(4, 100)
exactly_one = sum(p) - 2 * sum(pairs) + 3 * triple
at_least_two = sum(pairs) - 2 * triple
answer("P1-07", "0.66", "0.22")
ok("P1-07容斥", (exactly_one, at_least_two) == (F(66, 100), F(22, 100)))

# P1-08 is a proof and therefore manual by design.
print("MANUAL P1-08")

# P1-09
arrangements = list(permutations(range(7)))
adjacent = sum(any(abs(w.index(i) - w.index(j)) == 1 for i, j in combinations(range(3), 2)) for w in arrangements)
p_adj = F(adjacent, len(arrangements))
answer("P1-09", r"\dfrac57")
ok("P1-09排列", p_adj == 1 - F(factorial(4) * comb(5, 3) * factorial(3), factorial(7)) == F(5, 7))

# P1-10: derive all eight cells as affine functions of t and intersect nonnegative constraints.
t = sp.symbols("t", real=True)
pA, pB, pC = map(sp.Rational, ("0.40", "0.45", "0.35"))
pAB, pAC, pBC = map(sp.Rational, ("0.15", "0.10", "0.08"))
cells = [t, pAB-t, pAC-t, pBC-t,
         pA-pAB-pAC+t, pB-pAB-pBC+t, pC-pAC-pBC+t]
union10 = sp.expand(sum(cells))
cells.append(1 - union10)
interval = sp.reduce_inequalities([c >= 0 for c in cells], t)
answer("P1-10", "0.08", "0.87", "0.95", "0.13-t")
ok("P1-10八格", bool(sp.simplify_logic(sp.Equivalent(interval, sp.And(t >= 0, t <= sp.Rational(2, 25))))) and sp.simplify(sum(cells)) == 1 and union10.subs(t, 0) == sp.Rational(87, 100) and union10.subs(t, sp.Rational(2, 25)) == sp.Rational(95, 100))
ok("P1-10还原题设", [sp.expand(sum(cells[i] for i in ids)) for ids in [(0, 1, 2, 4), (0, 1, 3, 5), (0, 2, 3, 6), (0, 1), (0, 2), (0, 3)]] == [pA, pB, pC, pAB, pAC, pBC])

# P1-11
a = sp.symbols("a", real=True)
x = sp.symbols("x", real=True)
total11 = sp.integrate(2 - x, (x, 0, 2))
p_low = sp.integrate(a, (x, 0, a)) / total11
p_high = (sp.integrate(a, (x, 0, 2-a)) + sp.integrate(2-x, (x, 2-a, a))) / total11
valid_roots = [r for p, lo, hi in [(p_low, 0, 1), (p_high, 1, 2)] for r in sp.solve(sp.Eq(p, sp.Rational(3, 4)), a) if lo <= r <= hi]
answer("P1-11", "a^2/2", "1-(2-a)^2/2", r"2-\dfrac{\sqrt2}{2}")
ok("P1-11几何", sp.simplify(p_low-a**2/2) == 0 and sp.simplify(p_high-(1-(2-a)**2/2)) == 0 and valid_roots == [2-sp.sqrt(2)/2])
ok("P1-11边界", p_low.subs(a, 0) == 0 and p_low.subs(a, 1) == p_high.subs(a, 1) == sp.Rational(1, 2) and p_high.subs(a, 2) == 1)

# P1-12
num12 = sum(red[1] == 5 for red in combinations(range(1, 9), 3))
den12 = comb(8, 3)
answer("P1-12", r"\dfrac3{14}")
ok("P1-12位置", num12 == comb(4, 1) * comb(3, 1) and F(num12, den12) == F(3, 14))

# P1-13
answer("P1-13", r"\dfrac25")
setA = sp.solve_univariate_inequality(x**2-5*x+6 <= 0, x, relational=False)
setB = sp.solve_univariate_inequality(sp.Abs(x-4) <= sp.Rational(1, 2), x, relational=False)
ok("P1-13区间", (setA.union(setB).intersect(sp.Interval(0, 5))).measure / 5 == sp.Rational(2, 5))

# P1-14
x = sp.symbols("x")
area14 = sp.integrate(3*x - 1, (x, sp.Rational(1, 3), sp.Rational(1, 2))) + sp.integrate(x, (x, sp.Rational(1, 2), 1))
answer("P1-14", r"\dfrac5{12}")
triangle14 = sp.Polygon((sp.Rational(1, 3), sp.Rational(2, 3)), (sp.Rational(1, 2), sp.Rational(1, 2)), (sp.Rational(1, 2), 1))
trapezoid14 = sp.Polygon((sp.Rational(1, 2), sp.Rational(1, 2)), (1, 0), (1, 1), (sp.Rational(1, 2), 1))
ok("P1-14面积", abs(triangle14.area) == sp.Rational(1, 24) and abs(trapezoid14.area) == sp.Rational(3, 8) and abs(triangle14.area) + abs(trapezoid14.area) == area14 == sp.Rational(5, 12))

# P1-15
good15 = comb(4, 0) * comb(4, 3) + comb(4, 2) * comb(4, 1)
answer("P1-15", r"\dfrac12")
ok("P1-15组合", F(good15, comb(8, 3)) == F(1, 2))
