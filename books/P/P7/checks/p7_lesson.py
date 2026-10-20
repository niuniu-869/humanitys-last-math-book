"""讲义例题里的数值（作者自检）。"""
from fractions import Fraction as F
from math import comb, sqrt
import numpy as np
from scipy import stats
import sympy as sp

def chk(name, ok):
    print(("PASS " if ok else "FAIL ") + name)

S = {s: F(6 - abs(s - 7), 36) for s in range(2, 13)}
M = {m: F(2 * m - 1, 36) for m in range(1, 7)}
ES = sum(s * p for s, p in S.items()); VS = sum(s * s * p for s, p in S.items()) - ES**2
EM = sum(m * p for m, p in M.items())
chk("例1 E(S)=7", ES == 7 and sum(s * p * 36 for s, p in S.items()) == 252)
chk("例2 E(M)=161/36", EM == F(161, 36))
kk = sp.symbols("kk", integer=True, positive=True)
chk("例6 期望不存在", sp.summation(2**kk * 2**(-kk), (kk, 1, sp.oo)) == sp.oo)
P5 = {(0, 1): F(20, 100), (0, 2): F(15, 100), (0, 3): F(5, 100), (1, 1): F(10, 100), (1, 2): F(25, 100), (1, 3): F(25, 100)}
EX = sum(x * p for (x, y), p in P5.items()); EY = sum(y * p for (x, y), p in P5.items())
EXY = sum(x * y * p for (x, y), p in P5.items()); EY2 = sum(y * y * p for (x, y), p in P5.items())
VX = EX - EX**2; VY = EY2 - EY**2; C = EXY - EX * EY
chk("例3 E(X),E(Y)", (EX, EY) == (F(3, 5), 2))
chk("例5 保费 950", 50000 * F(9, 1000) + 500000 * F(1, 1000) == 950)
x = sp.symbols("x")
chk("例4 f=2(1-x) 期望 1/3", sp.integrate(x * 2 * (1 - x), (x, 0, 1)) == sp.Rational(1, 3))
chk("例7 E(e^X)=e-1", sp.simplify(sp.integrate(sp.exp(x), (x, 0, 1)) - (sp.E - 1)) == 0)
chk("练习 E(sqrt X)=4/5", sp.integrate(sp.sqrt(x) * 2 * x, (x, 0, 1)) == sp.Rational(4, 5))
chk("例8 E(XY)=1.35, E(Y^2)=4.6", EXY == F(135, 100) and EY2 == F(46, 10))
chk("例9 E|D1-D2|=35/18", sum(F(abs(i - j), 36) for i in range(1, 7) for j in range(1, 7)) == F(35, 18))
v = np.array([[1, 0], [0, 2], [2, 2]]); w = np.array([.5, .3, .2])
chk("例10 注意力 (0.9,1.0)", np.allclose(w @ v, [0.9, 1.0]))
dist = {0: F(3, 10), 1: F(3, 10), 4: F(4, 10)}
chk("例2节 E(X^2)=1.9", sum(k * p for k, p in dist.items()) == F(19, 10))
# 例 12 n=3
import itertools
chk("例12 n=3 配对期望 1", F(sum(sum(i == p[i] for i in range(3)) for p in itertools.permutations(range(3))), 6) == 1)
chk("例13 超几何期望 1.5", sum(k * F(comb(6, k) * comb(14, 5 - k), comb(20, 5)) for k in range(0, 6)) == F(3, 2))
Emax = EM; Emin = sum(m * F(13 - 2 * m, 36) for m in range(1, 7))
chk("例14 E(Mm)=49/4 与乘积", Emin == F(91, 36) and Emax + Emin == 7 and F(49, 4) == sum(F(i * j, 36) for i in range(1, 7) for j in range(1, 7)) and abs(float(Emax * Emin) - 11.304) < 1e-3)
cond0 = [P5[(0, y)] / F(2, 5) for y in (1, 2, 3)]; cond1 = [P5[(1, y)] / F(3, 5) for y in (1, 2, 3)]
e0 = sum(y * p for y, p in zip((1, 2, 3), cond0)); e1 = sum(y * p for y, p in zip((1, 2, 3), cond1))
chk("例15 条件期望 13/8, 9/4", (e0, e1) == (F(13, 8), F(9, 4)) and F(2, 5) * e0 + F(3, 5) * e1 == 2)
yy = sp.Symbol("y"); chk("例16 三角形 E(Y)=1/3", sp.integrate(sp.integrate(2 * yy, (yy, 0, x)), (x, 0, 1)) == sp.Rational(1, 3))
xx = sp.symbols("xx"); chk("例17 迷宫 10", sp.solve(sp.Eq(xx, sp.Rational(1, 3) * 2 + sp.Rational(1, 3) * (3 + xx) + sp.Rational(1, 3) * (5 + xx)), xx)[0] == 10)
gg = sp.symbols("gg")
chk("例18 几何期望 10/7", sp.solve(sp.Eq(gg, sp.Rational(7, 10) + sp.Rational(3, 10) * (1 + gg)), gg)[0] == sp.Rational(10, 7))
chk("练习 迷宫 3.5", sp.solve(sp.Eq(xx, sp.Rational(1, 2) + sp.Rational(1, 4) * (2 + xx) + sp.Rational(1, 4) * (3 + xx)), xx)[0] == sp.Rational(7, 2))
chk("例19 E(H)=1.75", F(7, 2) / 2 == F(7, 4))
# 方差
chk("例20 Var(Y)=0.6, Var(X)=0.24", (VY, VX) == (F(3, 5), F(6, 25)))
chk("练习 Var=1.24", F(14, 10) - F(4, 10)**2 == F(124, 100))
chk("例21 Var=1/18", sp.integrate(x**2 * 2 * (1 - x), (x, 0, 1)) - sp.Rational(1, 9) == sp.Rational(1, 18))
chk("例22 Var(S)=35/6, E(S^2)=329/6", VS == F(35, 6) and sum(s * s * p for s, p in S.items()) == F(329, 6))
chk("例23 sd=0.171", abs(sqrt(35 / 12 / 100) - 0.1708) < 1e-3 and F(35, 12) / 100 == F(7, 240))
rng = np.random.default_rng(1)
q = rng.standard_normal((200000, 64)); k = rng.standard_normal((200000, 64)); sc = (q * k).sum(1)
chk("例24 模拟 方差 63.9 / 0.998", abs(sc.var() - 63.9) < 0.06 and abs((sc / 8).var() - 0.998) < 0.001)
# 第6节
pp = sp.symbols("p", positive=True); EX2 = sp.symbols("EX2")
sol = sp.solve(sp.Eq(EX2, pp + (1 - pp) * (1 + 2 / pp + EX2)), EX2)[0]
chk("例6节 几何 E(X^2)=(2-p)/p^2", sp.simplify(sol - (2 - pp) / pp**2) == 0)
chk("例25 B(100,0.7)", (100 * .7, 100 * .7 * .3) == (70.0, 21.000000000000004) or abs(100 * .7 * .3 - 21) < 1e-9)
chk("例25 sd 4.58, 0.0458", abs(sqrt(21) - 4.5826) < 1e-3 and abs(sqrt(21) / 100 - 0.0458) < 1e-4)
lam = sp.symbols("lam", positive=True)
chk("例26 λ=2, E(X^2)=6", sp.solve(sp.Eq(lam * sp.exp(-lam), lam**2 / 2 * sp.exp(-lam)), lam) == [2] and 2 + 4 == 6)
chk("例27 P(Y>14)=0.1587", abs(stats.norm.sf(1) - 0.1587) < 1e-4)
chk("例28 λ/(1+λ)", sp.simplify(sp.integrate(sp.exp(-x) * lam * sp.exp(-lam * x), (x, 0, sp.oo)) - lam / (1 + lam)) == 0 and abs(np.exp(-1) - 0.368) < 1e-3)
chk("④ 指数 λ=3 的均值 20 分钟", F(1, 3) * 60 == 20)
# 第7节
chk("例29 Cov=0.15", C == F(3, 20))
cells = sum((x - F(3, 5)) * (y - 2) * p for (x, y), p in P5.items()); chk("例29 定义逐格 0.15", cells == F(3, 20))
chk("例30 Var(X+Y)=1.14, Var(Y-X)=0.54, 练习 0.96", (VX + VY + 2 * C, VX + VY - 2 * C, 4 * VX + VY - 4 * C) == (F(114, 100), F(54, 100), F(96, 100)))
d = {1: F(2, 10), 2: F(25, 100), 3: F(3, 10), 4: F(25, 100)}
chk("例30 直接验证", d[1] + d[2] + d[3] + d[4] == 1 and sum(k * p for k, p in d.items()) == F(26, 10) and sum(k * k * p for k, p in d.items()) == F(79, 10))
chk("例31 和差协方差", (2 + 2 + 2 * 1, 2 + 2 - 2 * 1, 2 - 2) == (6, 2, 0))
pv = F(3, 10)
covh = F(6 * 5, 20 * 19) - F(9, 100)
varh = 5 * pv * (1 - pv) + 2 * 10 * covh
chk("例32 Cov=-0.21/19, Var=1.05*15/19", covh == -F(21, 100) / 19 and varh == F(105, 100) * F(15, 19))
# 超几何方差直接
hv = stats.hypergeom(20, 6, 5).var(); chk("例32 超几何方差 scipy", abs(hv - float(varh)) < 1e-9)
w = sp.symbols("w"); Vr = 4 * w**2 + 9 * (1 - w)**2 + 2 * w * (1 - w) * (-3)
ws = sp.solve(sp.diff(Vr, w), w)[0]
chk("例33 w=12/19, Var=27/19", ws == sp.Rational(12, 19) and sp.simplify(Vr.subs(w, ws)) == sp.Rational(27, 19) and sp.expand(Vr) == 19 * w**2 - 24 * w + 9)
chk("例33 平均收益 6.74", abs(8 - 2 * 12 / 19 - 6.7368) < 1e-3 and abs(sqrt(27 / 19) - 1.192) < 1e-3)
# 第8节
chk("例34 ρ=√10/8", abs(float(C) / sqrt(float(VX * VY)) - sqrt(10) / 8) < 1e-12)
chk("例35 Var(2X-Y)=13", 4 * 4 + 9 - 2 * 2 * 1 * (0.5 * 2 * 3) == 13)
chk("例36 线性关系 rho=-1", -3 / abs(-3) == -1)
b = C / VX; a = EY - b * EX
chk("例37 预测 5/8, 13/8, 残差 0.50625", (b, a) == (F(5, 8), F(13, 8)) and (1 - F(10, 64)) * F(6, 10) == F(50625, 100000) and a + b == F(9, 4))
# 第9节
chk("例38 Y=X^2 不相关不独立", sum(F(x, 3) * x * x for x in (-1, 0, 1)) == 0 and F(1, 3) * F(2, 3) == F(2, 9))
from math import acos
cap = acos(.9) - .9 * sqrt(1 - .81); pr = 2 * cap / np.pi
chk("例39 圆盘 P(|X|>0.9)=0.0374, 平方 0.0014", abs(pr - 0.0374) < 1e-4 and abs(pr**2 - 0.0014) < 1e-4 and 2 * .81 > 1.62 - 1e-9)
chk("例40 ⑦ Cov=1, ρ=1/2", F(1, 2) * 2 == 1 and abs(1 / (sqrt(2) * sqrt(2)) - 0.5) < 1e-12)
# 第10节
zz = sp.symbols("zz"); phi = sp.exp(-zz**2 / 2) / sp.sqrt(2 * sp.pi)
chk("例41 E(Z^4)=3", sp.simplify(sp.integrate(zz**4 * phi, (zz, -sp.oo, sp.oo))) == 3)
Sg5 = sp.Matrix([[sp.Rational(24, 100), sp.Rational(15, 100)], [sp.Rational(15, 100), sp.Rational(6, 10)]])
chk("例42 aΣa=1.14, det=0.1215", (sp.Matrix([[1, 1]]) * Sg5 * sp.Matrix([1, 1]))[0] == sp.Rational(114, 100) and Sg5.det() == sp.Rational(1215, 10000))
Sg7 = sp.Matrix([[2, 1], [1, 2]]); A = sp.Matrix([[1, 1], [1, -1]])
chk("例43 AΣAᵀ=diag(6,2)", A * Sg7 * A.T == sp.diag(6, 2) and A * Sg7 == sp.Matrix([[3, 3], [1, -1]]))
pts = np.array([[2, 1], [1, 2], [-1, -2], [-2, -1]]); Sg = pts.T @ pts / 4
chk("例44 PCA Σ,特征值 4.5/0.5, 90%", np.allclose(Sg, [[2.5, 2], [2, 2.5]]) and np.allclose(np.linalg.eigvalsh(Sg), [0.5, 4.5]) and np.allclose(((pts @ np.array([1, 1]) / sqrt(2))**2).mean(), 4.5))
# 第11节
chk("例45 P(X+Y>3)=0.110, P(X-Y>1)=0.240", abs(stats.norm.sf(3 / sqrt(6)) - 0.110) < 1e-3 and abs(stats.norm.sf(1 / sqrt(2)) - 0.240) < 1e-3 and abs(3 / sqrt(6) - 1.225) < 1e-3)
chk("例46 P(2X-Y>5)=0.1587", abs(stats.norm.sf(1) - 0.1587) < 1e-4 and 4 * 4 + 9 == 25)
chk("例47 0.132 与误当独立 0.240", abs(stats.norm.sf(1 / sqrt(.8)) - 0.132) < 1e-3 and abs(1 / sqrt(.8) - 1.118) < 1e-3 and abs(stats.norm.sf(1 / sqrt(2)) - 0.240) < 1e-3)
chk("例48 0.084", abs(stats.norm.sf(3 / sqrt(6)) * stats.norm.cdf(1 / sqrt(2)) - 0.084) < 1e-3 and abs(stats.norm.cdf(1 / sqrt(2)) - 0.760) < 1e-3)
# 第12节
L = np.linalg.cholesky(np.array([[2., 1], [1, 2]]))
chk("例49 Cholesky 与点", np.allclose(L @ L.T, [[2, 1], [1, 2]]) and np.allclose(L @ [1, -1], [1.414, -0.518], atol=1e-3))
chk("例50 x=1.4", abs(1 + 0.5 * 0.8 - 1.4) < 1e-12)
Q = sp.Matrix([[1, 1], [-1, 1]]) / sp.sqrt(2)
chk("例51 QΣQᵀ=diag(3,1)", sp.simplify(Q * Sg7 * Q.T) == sp.diag(3, 1))
chk("例12节 ⑦ 特征值 3,1", sorted(np.linalg.eigvalsh(np.array([[2., 1], [1, 2]]))) == [1.0, 3.0])
# 编辑稿新增数值
vv = F(9, 1000) * 50000**2 + F(1, 1000) * 500000**2 - 950**2
chk("编辑 例5 方差与标准差 16480", abs(sqrt(vv) - 16480) < 1 and abs(float(vv) - 2.72e8) < 1e6)
chk("编辑 例3 Cov(X,2Y)=0.30, Var 相加 0.84, 差 0.30", 2 * C == F(3, 10) and VX + VY == F(84, 100) and F(114, 100) - (VX + VY) == F(3, 10))
chk("编辑 随堂 Y 预测 X", C / VY == F(1, 4) and EX - C / VY * EY == F(1, 10) and (1 - C**2 / (VX * VY)) * VX == F(2025, 10000))
Sg7b = sp.Matrix([[2, 1], [1, 2]]); Ab = sp.Matrix([[1, 0], [1, 1]])
chk("编辑 随堂 (X,X+Y) 协方差矩阵", Ab * Sg7b * Ab.T == sp.Matrix([[2, 3], [3, 6]]))
xx, yy = sp.symbols("xx yy")
dens = 1 / (2 * sp.pi * sp.sqrt(3)) * sp.exp(-(xx**2 - xx * yy + yy**2) / 3)
std = 1 / (2 * sp.pi * sp.sqrt(2 * 2 * (1 - sp.Rational(1, 4)))) * sp.exp(-(xx**2 / 2 - 2 * sp.Rational(1, 2) * xx * yy / 2 + yy**2 / 2) / (2 * (1 - sp.Rational(1, 4))))
chk("编辑 第12节 ⑦ 密度", sp.simplify(dens - std) == 0 and Sg7b.det() == 3 and sp.simplify(Sg7b.inv() * 3 - sp.Matrix([[2, -1], [-1, 2]])) == sp.zeros(2))
chk("编辑 N(1,1) 与 E(1) 同均值同方差", stats.expon(scale=1).mean() == 1 and stats.expon(scale=1).var() == 1)
chk("编辑 随堂 B(20,.1), E(4)", 20 * .1 == 2 and abs(20 * .1 * .9 - 1.8) < 1e-12 and 1 / 4 == .25 and 1 / 16 == .0625)
chk("编辑 例16 E(X)=2/3", sp.integrate(x * 2 * x, (x, 0, 1)) == sp.Rational(2, 3))
