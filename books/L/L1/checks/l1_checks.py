#!/usr/bin/env python3
"""L.1 验算：讲义例题与随堂小题的数值、全部题目、选择题每个选项。
每项打印 PASS/FAIL <编号>；证明题打印 MANUAL <编号>。期望值取自讲义/答案原文，计算一律现算。"""
import random

import sympy as sp
from sympy import Rational as R

M = lambda *xs: sp.Matrix(xs)  # noqa: E731


def report(tag, ok):
    print(f"{'PASS' if ok else 'FAIL'} {tag}")


def solve_comb(vecs, b, extra=None):
    """解 sum c_i v_i = b（可附加方程），返回解集（sympy dict 列表）。"""
    cs = sp.symbols(f"c1:{len(vecs) + 1}")
    eqs = list(sum((c * v for c, v in zip(cs, vecs)), sp.zeros(len(b), 1)) - b)
    if extra:
        eqs += extra(cs)
    return cs, sp.solve(eqs, cs, dict=True)


def in_span(vecs, b):
    A = sp.Matrix.hstack(*vecs)
    return A.rank() == sp.Matrix.hstack(A, b).rank()


def convex_weights(vecs, b):
    cs, sol = solve_comb(vecs, b, extra=lambda cs: [sum(cs) - 1])
    return cs, sol


u, v, w = M(5, 4, 1, 2), M(4, 5, 2, 1), M(1, 2, 5, 4)
one = M(1, 1, 1, 1)

# ---------------- 讲义 ----------------
report("讲义 u+v", u + v == M(9, 9, 3, 3))
report("讲义 2u", 2 * u == M(10, 8, 2, 4))
report("讲义 转置", u.T.shape == (1, 4) and u.T.T == u)
x = sp.symbols("x1:5")
X = sp.Matrix(x)
a_, b_ = M(1, -2, 0, 3), M(1, 0, 2, 1)
sol = sp.solve(list(2 * X + a_ - 3 * b_), x, dict=True)[0]
report("例1 x=(1,1,3,0)", X.subs(sol) == M(1, 1, 3, 0) and 3 * b_ - a_ == M(2, 2, 6, 0))
c_, d_ = M(2, 1, -1, 0), M(1, 2, 4, 3)
sol = sp.solve(list(3 * X - d_ - c_), x, dict=True)[0]
report("例1后小题", c_ + d_ == M(3, 3, 3, 3) and X.subs(sol) == M(1, 1, 1, 1))
cs, s = solve_comb([M(1, 2), M(3, 1)], M(5, 5))
report("第2节开头 c=(2,1)", s == [{cs[0]: 2, cs[1]: 1}])
cs, s = solve_comb([u, one], w)
report("例2 w=6*1-u", s == [{cs[0]: -1, cs[1]: 6}])
cs, s = solve_comb([u, one], v)
c12 = sp.solve([5 * cs[0] + cs[1] - 4, 4 * cs[0] + cs[1] - 5], cs)
report("例2后小题 v 不能表示", s == [] and c12 == {cs[0]: -1, cs[1]: 9} and c12[cs[0]] + c12[cs[1]] == 8)
E = sp.eye(4)
report("e_i 分解 u", 5 * E[:, 0] + 4 * E[:, 1] + E[:, 2] + 2 * E[:, 3] == u)
report("第3节 a1,a2 不共线 ps-qr", 1 * 1 - 2 * 3 == -5)
def collinear(v1, v2):
    return sp.Matrix.hstack(v1, v2).rank() <= 1
pairs = [(M(i, j), M(k_, l_)) for i in range(-2, 3) for j in range(-2, 3) for k_ in range(-2, 3) for l_ in range(-2, 3)]
report("讲义 共线（含零向量）⇔ ps-qr=0", all(collinear(v1, v2) == (v1[0] * v2[1] - v1[1] * v2[0] == 0) for v1, v2 in pairs))
a1, a2 = M(1, 0, 1), M(0, 1, 1)
xx, yy, zz = sp.symbols("x y z")
c1, c2 = sp.symbols("c1 c2")
comb = c1 * a1 + c2 * a2
report("例3(1) 组合第三分量=前两之和", sp.simplify(comb[2] - comb[0] - comb[1]) == 0)
report("例3(1) b 不在、b' 在", (not in_span([a1, a2], M(2, 3, 4))) and 2 * a1 + 3 * a2 == M(2, 3, 5))
a3 = M(1, 1, 2)
report("例3(2) a3=a1+a2，张成不变", a3 == a1 + a2 and sp.Matrix.hstack(a1, a2, a3).rank() == 2)
e3 = M(0, 0, 1)
report("例3(2) 加 e3 拼出 R3", sp.simplify(xx * a1 + yy * a2 + (zz - xx - yy) * e3 - M(xx, yy, zz)) == sp.zeros(3, 1)
       and sp.Matrix.hstack(a1, a2, e3).rank() == 3)
q1, q2 = M(1, 2, 0), M(0, 1, 1)
comb = c1 * q1 + c2 * q2
report("例3后小题 条件 y=2x+z", sp.simplify(comb[1] - 2 * comb[0] - comb[2]) == 0 and 2 * q1 + q2 == M(2, 5, 1))
p1, p2, p3 = M(40, 10), M(10, 40), M(10, 10)
report("第4节 2/3p1+1/3p2", R(2, 3) * p1 + R(1, 3) * p2 == M(30, 20))
t = sp.symbols("t")
report("第4节 (1-t)p1+tp2 = p1+t(p2-p1)", sp.simplify((1 - t) * p1 + t * p2 - (p1 + t * (p2 - p1))) == sp.zeros(2, 1))
# 两步混合恒等式
k1, k2, k3 = sp.symbols("k1 k2 k3", positive=True)
d = k2 / (1 - k1) * p2 + k3 / (1 - k1) * p3
lhs = k1 * p1 + k2 * p2 + k3 * p3
rhs = k1 * p1 + (1 - k1) * d
report("第4节 两步混合恒等式", sp.simplify(lhs - rhs) == sp.zeros(2, 1))
# 夹逼：随机凸组合蛋白质在 [10,40]
random.seed(1)
ok = True
for _ in range(2000):
    r = [random.random() for _ in range(3)]
    s_ = sum(r)
    r = [ri / s_ for ri in r]
    prot = 40 * r[0] + 10 * r[1] + 10 * r[2]
    ok &= 10 - 1e-12 <= prot <= 40 + 1e-12
report("第4节 夹逼检验", ok)
cs, s = convex_weights([p1, p2, p3], M(20, 20))
report("例4(1) 权重 1/3", s == [{cs[0]: R(1, 3), cs[1]: R(1, 3), cs[2]: R(1, 3)}])
cs, s = convex_weights([p1, p2, p3], M(30, 30))
report("例4(2) 权重 (2/3,2/3,-1/3)", s == [{cs[0]: R(2, 3), cs[1]: R(2, 3), cs[2]: R(-1, 3)}])
cs, s = convex_weights([p1, p2, p3], M(25, 15))
report("例4后小题 (1/2,1/6,1/3)", s == [{cs[0]: R(1, 2), cs[1]: R(1, 6), cs[2]: R(1, 3)}])
h1, h2, h3 = M(1, 0), M(3, 2), M(0, 4)
out = R(1, 2) * h1 + R(3, 10) * h2 + R(1, 5) * h3
H = sp.Matrix.hstack(h1, h2, h3)
report("例5(1) 注意力输出 (1.4,1.4)，各分量夹在最小最大之间", out == M(R(7, 5), R(7, 5))
       and all(min(H.row(i)) <= out[i] <= max(H.row(i)) for i in range(2)))
cs, s = convex_weights([h1, h2, h3], M(2, 3))
report("例5(2) (2,3) 的权重唯一 (-0.1,0.7,0.4)，不是凸组合",
       s == [{cs[0]: R(-1, 10), cs[1]: R(7, 10), cs[2]: R(2, 5)}] and s[0][cs[0]] < 0)
cs5 = sp.symbols("c1:4")
red = sp.solve([cs5[0] + 3 * cs5[1] - 2, cs5[0] + cs5[1] + cs5[2] - 1], [cs5[0], cs5[2]], dict=True)[0]
report("例5(2) 消元中间式 c1=2-3c2，c3=2c2-1",
       sp.simplify(red[cs5[0]] - (2 - 3 * cs5[1])) == 0 and sp.simplify(red[cs5[2]] - (2 * cs5[1] - 1)) == 0)

# ---------------- 题目 ----------------
m = M(3, R(9, 2), 2, R(3, 2))
xs = sp.solve(list((u + X) / 2 - m), x, dict=True)[0]
xv = X.subs(xs)
report("L1-01(1) x=(1,5,3,1)", xv == M(1, 5, 3, 1))
Y = sp.Matrix(sp.symbols("y1:5"))
ys = sp.solve(list((u + xv + Y) / 3 - m), list(Y), dict=True)[0]
report("L1-01(2) y=m，且 u+x=2m", Y.subs(ys) == m and u + xv == 2 * m)

k = sp.symbols("k")
cs, s = solve_comb([M(1, 1, 0), M(0, 1, 1)], M(1, k, 3))
report("L1-02", len(s) == 0 and in_span([M(1, 1, 0), M(0, 1, 1)], M(1, 4, 3))
       and all(not in_span([M(1, 1, 0), M(0, 1, 1)], M(1, kk, 3)) for kk in (0, 3, 5)))

ok = all((sp.Matrix.hstack(M(1, 2), M(2, kk)).rank() == 2) == (kk != 4) for kk in range(-3, 9))
a2k = M(2, 4)
cs, s = solve_comb([M(1, 2), a2k], M(3, 6))
ok &= len(s) == 1 and len(s[0]) == 1  # 一个自由参数 → 无穷多组
ok &= not in_span([M(1, 2), a2k], M(1, 0))
report("L1-03", ok)

A1, A2 = M(1, 2, 3), M(2, 4, 6)
optA_plane = sp.Matrix.hstack(A1, A2).rank() == 2  # A 说是平面 → 实际秩 1
cs, s = solve_comb([A1, A2], M(3, 6, 9))
optB_unique = len(s) == 1 and len(s[0]) == 2     # B 说唯一 → 实际不唯一
optC = in_span([A1, A2], M(1, 2, 4))            # C 说能 → 实际不能
optC_trap = (1 * A1 + 0 * A2)[:2, :] == M(1, 2)   # c1=1,c2=0 前两个分量确实对上
optD = sp.Matrix.hstack(A1, A2).rank() == 1      # D 正确
report("L1-04 选项A错", not optA_plane)
report("L1-04 选项B错", not optB_unique)
report("L1-04 选项C错（前两分量对上但第三分量不对）", (not optC) and optC_trap and (1 * A1)[2] != 4)
report("L1-04 选项D对", optD)

e1, e2 = M(1, 0), M(0, 1)
# A: 2e1-e2 系数和 1 但有负 → 不是凸组合（权重唯一）
cs, s = convex_weights([e1, e2], 2 * e1 - e2)
report("L1-05 选项A错", s and any(val < 0 for val in s[0].values()))
cs, s = convex_weights([e1, e2], M(R(1, 5), R(3, 10)))
report("L1-05 选项B错（(0.2,0.3) 在方框里但不是凸组合）", s == [] and 0 <= R(1, 5) <= 1 and 0 <= R(3, 10) <= 1)
cs, s = convex_weights([e1, e2], M(1, 1))
report("L1-05 选项C错", in_span([e1, e2], M(1, 1)) and s == [])
ok = True
for _ in range(500):
    lam = random.random()
    p = lam * e1 + (1 - lam) * e2
    ok &= abs(p[0] + p[1] - 1) < 1e-12 and 0 <= p[0] <= 1
report("L1-05 选项D对", ok)

a, b = sp.symbols("a b")
al1, al2, al3, be = M(1, 1, 1), M(1, 2, 3), M(1, 3, a), M(1, b, 3)
cs, s = solve_comb([al1, al2, al3], be)
gen = s[0]
ok = sp.simplify(gen[cs[2]] - (4 - 2 * b) / (a - 5)) == 0
ok &= sp.Matrix.hstack(al1, al2, al3).subs(a, 5).rank() == 2
ok &= (not in_span([al1, al2, al3.subs(a, 5)], be.subs(b, 3))) and in_span([al1, al2, al3.subs(a, 5)], be.subs(b, 2))
cc = sp.symbols("cc")
ok &= sp.simplify(cc * al1 + (1 - 2 * cc) * al2 + cc * al3.subs(a, 5) - be.subs(b, 2)) == sp.zeros(3, 1)
ok &= sp.Matrix.hstack(al1, al2, al3).subs(a, 7).rank() == 3
ok &= al1 - 2 * al2 + al3.subs(a, 5) == sp.zeros(3, 1)
ok &= all(sp.expand(vv[0] - 2 * vv[1] + vv[2]) == 0 for vv in (al1, al2))
report("L1-09（含参表示）", ok)

print("MANUAL L1-06 证明书写")
ok = True
for _ in range(20):
    b1 = sp.Matrix([random.randint(-5, 5) for _ in range(3)])
    b2 = sp.Matrix([random.randint(-5, 5) for _ in range(3)])
    S1 = sp.Matrix.hstack(b1, b2)
    S2 = sp.Matrix.hstack(b1 + b2, b1 - b2)
    ok &= S1.rank() == S2.rank() == sp.Matrix.hstack(S1, S2).rank()
report("L1-06 随机数值核对", ok)

opts = {
    "A": [M(1, 0, 1), M(0, 1, 1), M(1, -1, 0)],
    "B": [M(1, -1, 0), M(0, 1, -1), M(1, 0, -1), M(2, -1, -1)],
    "C": [M(1, 2, 0), M(0, 0, 0), M(0, 1, 3)],
    "D": [M(1, 1, 0), M(0, 1, 1), M(1, 0, 1)],
}
for key, vecs in opts.items():
    full = sp.Matrix.hstack(*vecs).rank() == 3
    report(f"L1-07 选项{key}{'对' if key == 'D' else '错'}", full == (key == "D"))
report("L1-07 A中第三个=前两之差", opts["A"][2] == opts["A"][0] - opts["A"][1])
from itertools import combinations
report("L1-07 B 四个向量分量和为 0 且两两不共线",
       all(sum(vv) == 0 for vv in opts["B"]) and all(sp.Matrix.hstack(p_, q_).rank() == 2 for p_, q_ in combinations(opts["B"], 2))
       and not in_span(opts["B"], M(0, 0, 1)))
D1, D2, D3 = opts["D"]
ok = sp.simplify((xx + yy - zz) / 2 * D1 + (yy + zz - xx) / 2 * D2 + (xx - yy + zz) / 2 * D3 - M(xx, yy, zz)) == sp.zeros(3, 1)
report("L1-07 D的显式系数", ok)

# 新 L1-08：正方形四点，目标在前三点三角形外但在四点凸包内
P1, P2, P3, P4 = M(0, 0), M(2, 0), M(0, 2), M(2, 2)
goal = M(R(3, 2), R(3, 2))
cs, s = convex_weights([P1, P2, P3], goal)
report("L1-08(1) 三种向量唯一解 (-1/2,3/4,3/4)", s == [{cs[0]: R(-1, 2), cs[1]: R(3, 4), cs[2]: R(3, 4)}])
cs4, s4 = convex_weights([P1, P2, P3, P4], goal)
gen4 = s4[0]
c4 = cs4[3]
ok = len(s4) == 1 and c4 not in gen4
ok &= all(sp.simplify(gen4[cs4[i]] - e) == 0 for i, e in enumerate([c4 - R(1, 2), R(3, 4) - c4, R(3, 4) - c4]))
report("L1-08(3) 通解", ok)
report("L1-08(2) c4=1/4 时 c1=-1/4", gen4[cs4[0]].subs(c4, R(1, 4)) == R(-1, 4))
feas = [sv for sv in [R(i, 120) for i in range(0, 121)]
        if all((gen4.get(cs4[j], cs4[j])).subs(c4, sv) >= 0 for j in range(4))]
report("L1-08(3) 非负当且仅当 1/2<=s<=3/4（网格）", min(feas) == R(1, 2) and max(feas) == R(3, 4) and len(feas) == 31)
w_half = [(gen4.get(cs4[j], cs4[j])).subs(c4, R(1, 2)) for j in range(4)]
w_34 = [(gen4.get(cs4[j], cs4[j])).subs(c4, R(3, 4)) for j in range(4)]
report("L1-08(3) 端点配法", w_half == [0, R(1, 4), R(1, 4), R(1, 2)] and w_34 == [R(1, 4), 0, 0, R(3, 4)]
       and sum((wi * Pi for wi, Pi in zip(w_half, [P1, P2, P3, P4])), sp.zeros(2, 1)) == goal)

# 新 L1-10：由「不能都表示」反推 a
X3 = M(xx, yy, zz)
cs, s10 = solve_comb([al1, al2, al3], X3)
report("L1-10(1) 一般右端 c3=(x-2y+z)/(a-5)", sp.simplify(s10[0][cs[2]] - (xx - 2 * yy + zz) / (a - 5)) == 0)
g1, g2, g3 = M(1, 0, 1), M(0, 1, 1), M(3, 4, 5)
A5 = [al1, al2, al3.subs(a, 5)]
ok = all(all(in_span([al1, al2, al3.subs(a, av)], g) for g in (g1, g2, g3)) for av in (0, 1, 4, 6, 7))
ok &= (not in_span(A5, g1)) and (not in_span(A5, g2)) and in_span(A5, g3)
report("L1-10(1) a≠5 全能表示，a=5 时 γ1、γ2 不能", ok)
ss = sp.symbols("ss")
report("L1-10(2) 平面 x-2y+z=0 与 γ3 的全部表示",
       all(sp.expand(vv[0] - 2 * vv[1] + vv[2]) == 0 for vv in A5)
       and sp.Matrix.hstack(*A5).rank() == 2
       and [g[0] - 2 * g[1] + g[2] for g in (g1, g2, g3)] == [2, -1, 0]
       and sp.expand((2 + ss) * A5[0] + (1 - 2 * ss) * A5[1] + ss * A5[2] - g3) == sp.zeros(3, 1)
       and A5[2] == 2 * al2 - al1)
csg, sg = solve_comb([g1, g2, g3], X3)
report("L1-10(3) γ 张成 R^3，d3=(x+y-z)/2", len(sg) == 1 and sp.simplify(sg[0][csg[2]] - (xx + yy - zz) / 2) == 0
       and all(in_span([g1, g2, g3], al) for al in A5))

cs, s = convex_weights([u, v, w], M(R(7, 2), 4, R(5, 2), 2))
report("L1-11(1)", s == [{cs[0]: R(1, 4), cs[1]: R(1, 2), cs[2]: R(1, 4)}])
cs, s = convex_weights([u, v, w], M(5, 5, 1, 1))
report("L1-11(3)", s == [{cs[0]: R(1, 2), cs[1]: R(2, 3), cs[2]: R(-1, 6)}])
al, bt, ga = sp.symbols("alpha beta gamma")
report("L1-11(3) 解唯一、各向量分量和都是 12", sum(u) == sum(v) == sum(w) == 12 == sum(M(5, 5, 1, 1)) == sum(M(R(7, 2), 4, R(5, 2), 2))
       and len(solve_comb([u, v, w], M(5, 5, 1, 1))[1][0]) == 3)
report("L1-11(2) 第一分量改写", sp.expand(5 * al + 4 * bt + ga - (5 * (al + bt + ga) - bt - 4 * ga)) == 0 and u[1] != 5)

# L1-12：取随机不共线 a1,a2 数值核对
ok = True
for _ in range(10):
    A_ = sp.Matrix([random.randint(-4, 4) for _ in range(3)])
    B_ = sp.Matrix([random.randint(-4, 4) for _ in range(3)])
    if sp.Matrix.hstack(A_, B_).rank() < 2:
        continue
    kk = sp.symbols("kk")
    bb1, bb2 = A_ + 2 * B_, 2 * A_ + kk * B_
    ks = [kv for kv in range(-6, 10) if sp.Matrix.hstack(bb1, bb2.subs(kk, kv)).rank() < 2]
    ok &= ks == [4]
    ok &= -bb1 + bb2.subs(kk, 3) == A_ + B_
    ok &= not in_span([bb1, bb2.subs(kk, 4)], A_)
report("L1-12", ok)

print("MANUAL L1-13")
lam, mu = sp.symbols("lam mu")
s = sp.solve(list(lam * M(4, 0) + mu * M(1, 3) - M(2, 1)), [lam, mu])
report("L1-13(2)", s == {lam: R(5, 12), mu: R(1, 3)} and s[lam] + s[mu] <= 1)

w1 = sp.symbols("w1")
w2 = R(4, 3) - 2 * w1
w3 = 1 - w1 - w2
ok = sp.simplify(12 * w1 + 6 * w2 - 8) == 0 and sp.simplify(w3 - (w1 - R(1, 3))) == 0
bad = sp.expand(-6 * w1 + 3 * w3)
ok &= bad == -3 * w1 - 1
lo, hi = R(1, 3), R(2, 3)
ok &= bad.subs(w1, lo) == -2 and bad.subs(w1, hi) == -3
# 网格枚举不卖空组合，核对行情差收益的范围
best, worst = -99, 99
for i in range(0, 301):
    for j in range(0, 301 - i):
        ww = (R(i, 300), R(j, 300), R(300 - i - j, 300))
        if 12 * ww[0] + 6 * ww[1] == 8:
            val = -6 * ww[0] + 3 * ww[2]
            best, worst = max(best, val), min(worst, val)
ok &= best == -2 and worst == -3
report("L1-14", ok)
