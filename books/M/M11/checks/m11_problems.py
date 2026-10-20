"""独立重算 M.11 习题，并核对答案中的关键结论。"""
from pathlib import Path
import re
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
ANS = (ROOT / "answers.md").read_text(encoding="utf-8")
PROB = (ROOT / "problems.md").read_text(encoding="utf-8")

def block(qid):
    m = re.search(rf"\*\*{qid}\*\*\n(.*?)(?=\n\*\*M11-|\Z)", ANS, re.S)
    return m.group(1) if m else ""

def ok(qid, condition):
    print(f"{'PASS' if condition else 'FAIL'} {qid}")

def sm(x):
    x = np.asarray(x, dtype=float)
    e = np.exp(x - np.max(x))
    return e / e.sum()

p01 = sm([1, 0]); out01 = p01 @ np.array([[2., 0.], [0., 2.]])
ok("M11-01", np.allclose(p01, [.73105858, .26894142]) and np.allclose(out01, [1.46211716, .53788284]) and "1.4621" in block("M11-01"))
ok("M11-02", "27" in block("M11-02") and all(s in block("M11-02") for s in ["4\\times2", "4\\times5", "4\\times4"]))

S03 = np.array([[0., 1., 2.], [1., 0., 1.], [2., 1., 0.]])
masked03 = S03.copy(); masked03[np.triu_indices(3, 1)] = -np.inf
A03 = np.array([sm(row) for row in masked03])
opts03 = [np.array([[1,0,0],[.7311,.2689,0],[.6652,.2447,.09]]), np.array([[.09,.2447,.6652],[.2689,.7311,0],[1,0,0]]), np.array([[1,0,0],[.2689,.7311,0],[1/3,1/3,1/3]]), np.array([[1,0,0],[.09,.2447,0],[.09,.2447,.6652]])]
ok("M11-03", [np.allclose(x, A03, atol=5e-4) for x in opts03] == [True,False,False,False] and "(A)" in block("M11-03"))

ok("M11-04", np.var([2.,2.,2.,2.]) == 0 and "方差为 $0$" in block("M11-04") and "相互独立" in block("M11-04"))

import sympy as sp
t_ = sp.symbols("t", real=True)
s1 = t_/sp.sqrt(2)  # q=(t,0) 与 k1、k2 的点积除以 sqrt(2)
a1 = sp.exp(s1)/(sp.exp(s1)+1); a2 = 1-a1
out05 = [a1*1+a2*3, a1*2+a2*0]
sol05 = sp.solve(sp.Eq(out05[1], sp.Rational(1, 2)), t_)
ok("M11-05", len(sol05) == 1 and sp.simplify(out05[0].subs(t_, sol05[0]) - sp.Rational(5, 2)) == 0
   and sp.simplify(sol05[0] + sp.sqrt(2)*sp.log(3)) == 0 and "-\\sqrt2\\ln3" in block("M11-05"))

d, dk, dv = 48, 64, 32
cproj = lambda n: 2*n*d*(2*dk+dv)          # 三个投影
catt = lambda n: 2*n*n*(dk+dv)            # QK^T 与 AV
nmin = next(n for n in range(1, 10**4) if catt(n) > cproj(n))
ratio06 = sp.Rational(cproj(256)+catt(256), cproj(128)+catt(128))
ok("M11-06", cproj(1) == 15360 and catt(1) == 192 and nmin == 81 and cproj(128)+catt(128) == 5111808
   and ratio06 == sp.Rational(42, 13) and "81" in block("M11-06") and "42/13" in block("M11-06"))

ok("M11-07", np.isclose(2*(4-1), 6) and "(C)" in block("M11-07") and "重新求二次矩" in block("M11-07"))

ok("M11-08", "分母" in block("M11-08") and "o_i=o'_i" in block("M11-08"))
print("MANUAL M11-08")

weights09 = sm([0., np.log(2.), np.log(3.)]); vals = np.array([1.,2.,4.])
same = weights09[::-1] @ vals[::-1]; one = weights09[::-1] @ vals
ok("M11-09", np.isclose(weights09 @ vals, 17/6) and np.isclose(same, 17/6) and np.isclose(one, 11/6) and "(A)" in block("M11-09"))

out12 = (1*0 + 2*1) / (1+2)
out13 = (1*0 + 3*3) / (1+3)
out23 = (2*1 + 3*3) / (2+3)
ok("M11-10", np.isclose(out12, 2/3) and np.isclose(out13, 9/4) and np.isclose(out23, 11/5) and all(s in block("M11-10") for s in ["2/3", "9/4", "11/5"]))

U_, V_, a_, b_, c_, d_ = sp.symbols("U V a b c d", real=True)
T_ = sp.expand(U_*(a_*U_+b_*V_) + V_*(c_*U_+d_*V_))
mom = {0: 1, 1: 0, 2: 1, 3: 0, 4: 3}
def E(expr):  # U,V 独立，按给定矩逐项求期望
    tot = 0
    for term in sp.Add.make_args(sp.expand(expr)):
        coeff, pu, pv = term, 0, 0
        pu = sp.degree(term, U_); pv = sp.degree(term, V_)
        coeff = term / (U_**pu * V_**pv)
        tot += coeff * mom[pu] * mom[pv]
    return sp.expand(tot)
var11 = sp.expand(E(T_**2) - E(T_)**2)
v0110 = var11.subs({a_: 0, b_: 1, c_: 1, d_: 0})
ok("M11-11", sp.simplify(E(T_) - (a_+d_)) == 0 and sp.simplify(var11 - (2*a_**2+2*d_**2+(b_+c_)**2)) == 0
   and v0110 == 4 and "不存在" in block("M11-11") and "除以 $2$" in block("M11-11"))
print("MANUAL M11-11")
print("MANUAL M11-12")

ok("M11-13", all(s in block("M11-13") for s in ["1/7", "2/7", "4/7", "c+\\ln2", "-\\ln2,0,\\ln2"]))

X14 = sp.Matrix([[1, 2], [3, 1]]); WQ = sp.Matrix([[1, 0], [t_, 1]]); WK = sp.Matrix([[1, 1], [0, 1]]); WV = sp.Matrix([1, 0])
Q14, K14, V14 = X14*WQ, X14*WK, X14*WV
sc = [(Q14[1, :]*K14[j, :].T)[0]/sp.sqrt(2) for j in range(2)]
w = [sp.exp(sc[0])/(sp.exp(sc[0])+sp.exp(sc[1])), sp.exp(sc[1])/(sp.exp(sc[0])+sp.exp(sc[1]))]
o2 = w[0]*V14[0] + w[1]*V14[1]
o2_at = sp.simplify(o2.subs(t_, sp.Rational(-7, 2)))
sol14 = sp.solve(sp.Eq(sc[0], sc[1]), t_)
ok("M11-14", V14[0] == 1 and o2_at == 2 and sol14 == [sp.Rational(-7, 2)] and Q14 == sp.Matrix([[1+2*t_, 2], [3+t_, 1]])
   and "-7/2" in block("M11-14") and "1+2t" in block("M11-14"))
ok("M11-15", "第 1、2、3、4 个位置" in block("M11-15") and "第 1、2 个位置" in block("M11-15") and "3 个" in block("M11-15"))

ids = re.findall(r"^\*\*(M11-\d+)\*\*", PROB, re.M)
ok("题号连续", ids == [f"M11-{i:02d}" for i in range(1, 16)])
