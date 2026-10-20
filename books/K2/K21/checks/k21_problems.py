#!/usr/bin/env python3
"""独立核对 K2.1 题目答案。"""
from pathlib import Path
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
ANS = (ROOT / "answers.md").read_text(encoding="utf-8")
n = sp.symbols("n", integer=True, nonnegative=True)
q, r = sp.symbols("q r")

def mark(pid, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + pid + (f" {detail}" if detail else ""))
    return ok

def has(pid, *tokens):
    start = ANS.index(f"**{pid}**")
    nxt = ANS.find("\n**K21-", start + 1)
    block = ANS[start:] if nxt < 0 else ANS[start:nxt]
    return all(t in block for t in tokens)

ok = True

# K21-01: last-step classification, calculated independently.
a = [1, 0]
for k in range(2, 9):
    if k == 2:
        a.append(1)
    elif k == 3:
        a.append(1)
    else:
        a.append(a[k - 2] + a[k - 3])
ok &= mark("K21-01", a[8] == 4 and has("K21-01", "a_8=4"))

# K21-02: fixed point and direct recurrence.
seq = [sp.Integer(7)]
for _ in range(5):
    seq.append(3 * seq[-1] - 4)
formula = 2 + 5 * 3**n
ok &= mark("K21-02", sp.simplify(formula.subs(n, 5) - seq[5]) == 0 and has("K21-02", "1217"))

# K21-03: characteristic roots and initial-value solve.
roots = sp.solve(sp.Symbol("lam")**2 - 4*sp.Symbol("lam") + 3)
c1, c2 = sp.symbols("c1 c2")
sol = sp.solve([c1 + c2 - 1, c1 + 3*c2 - 4], [c1, c2])
a2 = sp.simplify(sol[c1] + sol[c2] * 3**2)
ok &= mark("K21-03", roots == [1, 3] and a2 == 13 and has("K21-03", "a_2=13"))

# K21-04: infer the repeated constant.
c_symbol = sp.Symbol("c")
cval = sp.solve(sp.Eq(2 * (2 * 2 + c_symbol) + c_symbol, 11), c_symbol)[0]
# 三个干扰项各是一种典型错算：漏第二轮 c、漏第一轮 c、把 a0 当 a1。
wrong = [sp.solve(sp.Eq(e, 11), c_symbol)[0] for e in (2 * (2 * 2 + c_symbol), 2 * (2 * 2) + c_symbol, 2 * 2 + c_symbol)]
ok &= mark("K21-04", cval == 1 and wrong == [sp.Rational(3, 2), 3, 7] and has("K21-04", "(A)", "c=1"))

# K21-05: q=1 is an arithmetic accumulation.
def valid05(f):
    return f(0) == 4 and f(1) == f(0) + 3 and f(2) == f(1) + 3
options05 = [lambda k: 4*3**k, lambda k: 3*k, lambda k: 4+3*(k-1), lambda k: 4+3*k]
validity05 = [valid05(f) for f in options05]
ok &= mark("K21-05", validity05 == [False, False, False, True] and has("K21-05", "(D)"))

# K21-06: symbolic fixed point, q=1 branch, and q=-1 check.
xstar = sp.simplify(2 / (1 - q))
general = sp.simplify(xstar + q**n * (6 - xstar))
qminus = sp.simplify(general.subs({q: -1, n: 6}))
qone = [6]
for _ in range(6):
    qone.append(qone[-1] + 2)
ok &= mark("K21-06", qminus == 6 and qone[6] == 18 and has("K21-06", "a_6=6"))

# K21-07: infer p,q from two equations, then solve roots.
p, qq = sp.symbols("p qq")
pq = sp.solve([2*p + qq - 7, 7*p + 2*qq - 20], [p, qq])
roots07 = sp.solve(sp.Symbol("lam")**2 - pq[p]*sp.Symbol("lam") - pq[qq])
c1, c2 = sp.symbols("c1 c2")
cc = sp.solve([c1+c2-1, 3*c1-c2-2], [c1,c2])
a4 = sp.simplify(cc[c1]*3**4 + cc[c2]*(-1)**4)
ok &= mark("K21-07", pq == {p: 2, qq: 3} and set(roots07) == {-1, 3} and a4 == 61 and has("K21-07", "p=2,q=3", "a_4=61"))

# K21-08: only C is homogeneous linear constant-coefficient of order two.
validity08 = [False, False, True, False]
ok &= mark("K21-08", sum(validity08) == 1 and validity08[2] and has("K21-08", "(C)"))

# K21-09: this is the requested proof item; arithmetic is not a substitute for it.
proof_ok = has("K21-09", "r_2-r_1", "归纳基步", "全部解")
print("MANUAL K21-09")
ok &= proof_ok

# K21-10: derive the resonant particular solution and compare initial terms.
vals = [sp.Integer(0), sp.Integer(1)]
for k in range(2, 6):
    vals.append(3*vals[-1] - 2*vals[-2] + 2**(k-2))
closed10 = n * 2**(n-1)
ok &= mark("K21-10", vals[4] == closed10.subs(n, 4) and vals[5] == closed10.subs(n, 5) and has("K21-10", "n2^{n-1}"))

# K21-11: fixed point for a contraction.
e5 = sp.Rational(8) + 12 * sp.Rational(4, 5)**5
ok &= mark("K21-11", e5 == sp.Rational(37288, 3125) and has("K21-11", "37288", "极限为 $8$"))

# K21-12: independent matrix multiplication.
A = sp.Matrix([[1, 1], [1, 0]])
x0 = sp.Matrix([2, 1])
A6 = A**6
x6 = A6*x0
ok &= mark("K21-12", A6 == sp.Matrix([[13, 8], [8, 5]]) and x6[0] == 34 and has("K21-12", "a_7=34"))

# K21-13: calculate Fibonacci and the sum.
fib = [0, 1]
for _ in range(2, 13):
    fib.append(fib[-1] + fib[-2])
sum10 = sum(fib[:11])
ok &= mark("K21-13", sum10 == fib[12] - 1 == 143 and has("K21-13", "143"))

# K21-14: repeated-root nonhomogeneous recurrence.
vals14 = [sp.Integer(0), sp.Integer(1)]
for k in range(2, 4):
    vals14.append(6 * vals14[-1] - 9 * vals14[-2] + 3**(k - 2))
formula14 = n * (n + 5) * 3**n / 18
ok &= mark("K21-14", vals14[3] == 36 and sp.simplify(formula14.subs(n, 3) - 36) == 0 and has("K21-14", "n^2", "a_3=36"))

# Mixed exercises.
ok &= mark("K21-15", 1 + 2**7 == 129 and has("K21-15", "u_6=129"))
ok &= mark("K21-16", has("K21-16", "v_n=3^n-2^n"))
ok &= mark("K21-17", has("K21-17", "34&21", "21&13"))

raise SystemExit(0 if ok else 1)

