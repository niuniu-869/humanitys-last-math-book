"""独立核对 P.10 习题：数值由 sympy/scipy/枚举/模拟算出，再与答案文本比对；选择题逐项判定。"""
from fractions import Fraction as Fr
from itertools import product
from math import comb, sqrt
from pathlib import Path
import re

import numpy as np
import sympy as sp
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
ANS = (ROOT / "answers.md").read_text(encoding="utf-8")
rng = np.random.default_rng(20261017)
N = 400_000


def block(pid):
    m = re.search(rf"(?ms)^\*\*{re.escape(pid)}\*\*\n(.*?)(?=^\*\*[A-Z]+\d+-\d+\*\*|\Z)", ANS)
    return m.group(1) if m else ""


def check(pid, condition):
    print(f"PASS {pid}" if condition and block(pid) else f"FAIL {pid}")


def choice(pid, truth):
    """truth: 选项 -> 是否成立；要求恰有一项成立且答案行写的就是它。"""
    for k, v in truth.items():
        print(f"  {pid} 选项 {k}: {'真' if v else '假'}")
    right = [k for k, v in truth.items() if v]
    m = re.search(r"\*\*答案：\*\*\s*\(([A-D])\)", block(pid))
    check(pid, len(right) == 1 and m and m.group(1) == right[0])


def ks_ok(sample, dist):
    """模拟样本与理论分布的 KS 检验不拒绝（大样本下 p 值大于 1e-3）。"""
    return stats.kstest(sample, dist.cdf).pvalue > 1e-3


# 01: 有序样本值 (1,1,0,1) 的联合概率。
p = sp.Rational(7, 10)
v01 = p**3 * (1 - p)
check("P10-01", v01 == sp.Rational(1029, 10000) and "0.1029" in block("P10-01"))

# 02: 直接由数据计算均值、离差平方和、两种分母。
x = sp.Matrix([-1, 0, 2, 5])
xb = sum(x) / 4
ss = sum((xi - xb) ** 2 for xi in x)
check("P10-02", xb == sp.Rational(3, 2) and ss == 21 and "s^2=7" in block("P10-02") and "21}4" in block("P10-02"))

# 03: 六个标准化项的平方和；模拟核对分布、期望、方差。
X = rng.normal(3, 2, size=(N, 6))
Y = (((X - 3) / 2) ** 2).sum(axis=1)
check("P10-03", ks_ok(Y[:50000], stats.chi2(6)) and abs(Y.mean() - 6) < 0.05 and abs(Y.var() - 12) < 0.3
      and "chi^2(6)" in block("P10-03") and "E(Y)=6" in block("P10-03") and "=12" in block("P10-03"))

# 04: 逐项判定。A 用模拟方差，B 用 KS，D 用伯努利样本枚举反例。
X = rng.normal(0, 1, size=(N, 5))
xbar, s2 = X.mean(axis=1), X.var(axis=1, ddof=1)
optA = abs(xbar.var() - 1) < 0.05            # 若 A 对，Var(X̄)=σ²=1
optB = ks_ok(4 * s2[:50000], stats.chi2(5))  # 若 B 对，4S² 服从 χ²(5)
optC = abs(np.corrcoef(xbar**2, s2)[0, 1]) < 0.01 and abs(np.corrcoef(np.abs(xbar), s2)[0, 1]) < 0.01
joint = sum(Fr(1, 32) for t in product((0, 1), repeat=5) if sum(t) == 0)  # X̄=0 且 S²=0
pm = sum(Fr(1, 32) for t in product((0, 1), repeat=5) if sum(t) == 0)
ps = sum(Fr(1, 32) for t in product((0, 1), repeat=5) if len(set(t)) == 1)  # S²=0
optD = joint == pm * ps
choice("P10-04", {"A": optA, "B": optB, "C": optC, "D": optD})

# 05 是证明题，按要求由人工核对证明骨架；这里另核对关键常数与无偏性（模拟，非正态总体）。
X = rng.exponential(2.0, size=(N, 4))  # 方差 4，故意用非正态
Yv = rng.exponential(2.0, size=(N, 6))
U = (X.mean(axis=1) - Yv.mean(axis=1)) ** 2 / (Fr(1, 4) + Fr(1, 6)).__float__()
print(f"  P10-05 模拟 E(U)={U.mean():.4f}（理论 σ²=4）")
print("MANUAL P10-05")

# 06: 偏差分解的符号恒等式 + 模拟核对 χ²(6)。
a1, a2, a3 = sp.symbols("a1:4")
xs = [a1, a2, a3]
m = sum(xs) / 3
ident = sp.simplify(sum((t - m) ** 2 for t in xs) + 3 * (m - 1) ** 2 - sum((t - 1) ** 2 for t in xs)) == 0
X = rng.normal(1, 2, size=(N, 3))
Yv = rng.normal(-2, 3, size=(N, 4))
xm = X.mean(axis=1, keepdims=True)
ym = Yv.mean(axis=1, keepdims=True)
Q = (((X - xm) ** 2).sum(axis=1) + 3 * (xm[:, 0] - 1) ** 2) / 4 + ((Yv - ym) ** 2).sum(axis=1) / 9
check("P10-06", ident and ks_ok(Q[:50000], stats.chi2(6)) and abs(Q.mean() - 6) < 0.05 and abs(Q.var() - 12) < 0.3
      and "chi^2(6)" in block("P10-06") and "E(Q)=6" in block("P10-06") and "=12" in block("P10-06"))

# 07: 四个等可能样本点直接枚举协方差、联合概率与边缘乘积。
pts = []
for a, b in product((0, 1), repeat=2):
    mean = Fr(a + b, 2)
    s2v = (Fr(a) - mean) ** 2 + (Fr(b) - mean) ** 2  # 分母 n-1=1
    pts.append((mean, s2v))
w = Fr(1, 4)
EX = sum(w * u for u, _ in pts)
ES = sum(w * v for _, v in pts)
EXS = sum(w * u * v for u, v in pts)
cov = EXS - EX * ES
j07 = sum(w for u, v in pts if u == 0 and v == Fr(1, 2))
m07 = sum(w for u, _ in pts if u == 0) * sum(w for _, v in pts if v == Fr(1, 2))
print(f"  P10-07 E(X̄)={EX}, E(S²)={ES}, E(X̄S²)={EXS}, Cov={cov}, 联合={j07}, 乘积={m07}")
check("P10-07", cov == 0 and EXS == Fr(1, 8) and ES == Fr(1, 4) and j07 == 0 and m07 == Fr(1, 8)
      and "=0" in block("P10-07") and "\\tfrac18" in block("P10-07"))

# 08: 由 B2=5S²/6 化简 R，并对四个选项做模拟判定。
X = rng.normal(0, 1, size=(N, 6))
xbar = X.mean(axis=1)
B2 = X.var(axis=1, ddof=0)
R = sqrt(5) * xbar / np.sqrt(B2)
Rb = sqrt(6) * xbar / np.sqrt(B2)
# 用全部模拟样本做 KS，并用方差（t(5) 为 5/3，t(6) 为 3/2）辅助区分相近的自由度。
choice("P10-08", {"A": ks_ok(R, stats.t(5)) and abs(R.var() - 5 / 3) < 0.05,
                  "B": ks_ok(Rb, stats.t(5)) and abs(Rb.var() - 5 / 3) < 0.05,
                  "C": ks_ok(R, stats.t(6)) and abs(R.var() - 1.5) < 0.05,
                  "D": ks_ok(R, stats.norm) and abs(R.var() - 1) < 0.05})

# 09: σ1²=2σ2² 的两组样本，逐项模拟判定。
X = rng.normal(0, sqrt(2), size=(N, 8))
Yv = rng.normal(0, 1, size=(N, 6))
S1, S2 = X.var(axis=1, ddof=1), Yv.var(axis=1, ddof=1)
r1, r2 = (S1 / S2)[:50000], (S1 / (2 * S2))[:50000]
choice("P10-09", {"A": ks_ok(r1, stats.f(7, 5)), "B": ks_ok(r2, stats.f(5, 7)),
                  "C": ks_ok(r2, stats.f(7, 5)) and ks_ok(1 / r2, stats.f(5, 7)), "D": ks_ok(r2, stats.f(8, 6))})

# 10: U~F(1,3)、V~χ²(3)；E(UV)=E(12X̄²)=3，而 E(U)E(V)=9。
X = rng.normal(0, 1, size=(N, 4))
xbar, s2 = X.mean(axis=1), X.var(axis=1, ddof=1)
Uv, Vv = 4 * xbar**2 / s2, 3 * s2
EU = stats.f(1, 3).mean()
EV = stats.chi2(3).mean()
EUV = 12 * sp.Rational(1, 4)
uv_sim = (Uv * Vv).mean()
check("P10-10", ks_ok(Uv[:50000], stats.f(1, 3)) and ks_ok(Vv[:50000], stats.chi2(3)) and abs(EU - 3) < 1e-12
      and abs(EV - 3) < 1e-12 and EUV == 3 and abs(uv_sim - 3) < 0.05 and EU * EV == 9
      and "F(1,3)" in block("P10-10") and "E(UV)=3" in block("P10-10"))

# 11: 分解恒等式（符号）+ 两个估计量的期望与方差（χ² 公式与模拟）。
xs = sp.symbols("x1:5")
ys = sp.symbols("y1:7")
xm, ym = sum(xs) / 4, sum(ys) / 6
zm = (4 * xm + 6 * ym) / 10
S1s = sum((t - xm) ** 2 for t in xs) / 3
S2s = sum((t - ym) ** 2 for t in ys) / 5
lhs = sum((t - zm) ** 2 for t in xs) + sum((t - zm) ** 2 for t in ys)
ident11 = sp.expand(lhs - (3 * S1s + 5 * S2s + sp.Rational(12, 5) * (xm - ym) ** 2)) == 0
var_w = sp.Rational(1, 64) * 2 * 8      # σ⁴ 的系数
var_all = sp.Rational(1, 81) * 2 * 9
X = rng.normal(0, 1, size=(N, 4))
Yv = rng.normal(0, 1, size=(N, 6))
Sw = (3 * X.var(axis=1, ddof=1) + 5 * Yv.var(axis=1, ddof=1)) / 8
Sall = np.concatenate([X, Yv], axis=1).var(axis=1, ddof=1)
check("P10-11", ident11 and var_w == sp.Rational(1, 4) and var_all == sp.Rational(2, 9) and var_all < var_w
      and abs(Sw.mean() - 1) < 0.01 and abs(Sall.mean() - 1) < 0.01
      and abs(Sw.var() - 0.25) < 0.01 and abs(Sall.var() - 2 / 9) < 0.01
      and "{12}5" in block("P10-11") and "sigma^4}4" in block("P10-11") and "2\\sigma^4}9" in block("P10-11"))

# 12: 二项计数与正态均值两组独立；精确值 5/16·(2Φ(1)−1)，并模拟核对。
pk = sum(comb(4, k) for k in (0, 1)) / 16
px = stats.norm.cdf(1) - stats.norm.cdf(-1)
exact12 = pk * px
T = rng.normal(10, 1, size=(N, 4))
Sx = rng.integers(0, 2, size=(N, 4))
sim12 = np.mean((Sx.sum(axis=1) <= 1) & (np.abs(T.mean(axis=1) - 10) <= 0.5))
check("P10-12", abs(exact12 - 0.2133404663) < 1e-9 and abs(sim12 - exact12) < 0.005 and "0.2133" in block("P10-12"))

# 13: 切比雪夫上界 9/n 不超过 0.04。
min_n13 = next(k for k in range(1, 1000) if Fr(9, k) <= Fr(4, 100))
check("P10-13", min_n13 == 225 and "225" in block("P10-13"))

# 14: 伯努利样本均值与二项总和。
prob14 = comb(25, 8) * 0.4**8 * 0.6**17
check("P10-14", abs(prob14 - stats.binom.pmf(8, 25, 0.4)) < 1e-14 and abs(0.4 * 0.6 / 25 - 0.0096) < 1e-15
      and "0.0096" in block("P10-14") and "0.1200" in block("P10-14"))
