"""P.4 讲义里的例题数值与模拟表（固定随机种子）。"""
import numpy as np
from math import exp, log, pi, sqrt, comb
from scipy import stats, integrate


def ok(name, cond):
    print(("PASS " if cond else "FAIL ") + name)


def close(a, b, tol=5e-5):
    return abs(a - b) < tol


Phi = stats.norm.cdf
# ---- 第 1 节 ----
f = lambda x: x ** 2 / 9
ok("L4-ex1 c=1/9", close(integrate.quad(f, 0, 3)[0], 1))
ok("L4-ex1 P(1<X<=2)=7/27", close(integrate.quad(f, 1, 2)[0], 7 / 27, 1e-9))
ok("L4-ex1 F(x)=x^3/27 在 2 处 8/27", close(8 / 27, integrate.quad(f, 0, 2)[0], 1e-9))
print("slices of f=x^2/9 on (0,3), width 1:", [round(integrate.quad(f, i, i + 1)[0], 4) for i in range(3)])
print("width 0.5 heights:", [round(integrate.quad(f, i * .5, i * .5 + .5)[0] / .5, 4) for i in range(6)])
ok("L4-ex2 F=x^2/4 -> f=x/2, P(1<X<=1.5)=0.3125", close(1.5 ** 2 / 4 - 1 / 4, 0.3125) and close(integrate.quad(lambda x: x / 2, 1, 1.5)[0], 0.3125, 1e-9) and close(integrate.quad(lambda x: x / 2, 0, 2)[0], 1))
ok("L4-ex3 f=2 on [0,1/2]", close(integrate.quad(lambda x: 2, 0, .5)[0], 1) and close(2 * 0.1, 0.2))
ok("L4-ex4 k=1/2, P(X>1)=e^-1/2", close(integrate.quad(lambda x: .5 * exp(-abs(x)), -np.inf, np.inf)[0], 1) and close(exp(-1) / 2, 0.18394, 1e-5) and close(1 - exp(-1), 0.63212, 1e-5))
ok("L4-ex5 arctan", close(.5 + np.arctan(1) / pi - (.5 + np.arctan(-1) / pi), 0.5))

# ---- 第 2 节 ----
ok("L4-ex6 U(0,10)", close((10 - 7) / 10, 0.3) and close((5 - 2) / 10, 0.3))
ok("L4-ex7 判别式 2/3", close(sum(1 for x in np.linspace(0, 6, 600001) if x * x - 4 >= 0) / 600001, 2 / 3, 1e-4))
cum = np.cumsum([.4, .3, .2, .1]); print("cum", cum)
ok("L4-ex8 r=0.83 落在第三段", int(np.searchsorted(cum, 0.83, side='right')) == 2 and close(cum[1], 0.7) and close(cum[2], 0.9))
ok("L4-ex9 U(-1,3)", close(stats.uniform(-1, 4).cdf(1) - stats.uniform(-1, 4).cdf(-1), .5) and close(stats.uniform(-1, 4).sf(2), .25))
rng = np.random.default_rng(3)
r = rng.random(100000)
draw = np.searchsorted(cum, r, side='right')
print("sampling freq (很,不,还,太):", [round((draw == i).mean(), 4) for i in range(4)])

# ---- 第 3 节 ----
lam = 3.0
ok("L4 P(T>0.5h)=e^-1.5", close(exp(-1.5), 0.2231))
ok("L4 N=0 in 30min = e^-1.5", close(stats.poisson(1.5).pmf(0), exp(-1.5), 1e-12))
ok("L4 分钟制 e^-0.05t", close(exp(-.5), .6065) and close(exp(-1), .3679) and close(exp(-3), 0.0498))
print("table t(min), exp, expsim, minute-slices geometric")
rng = np.random.default_rng(5)
T = rng.exponential(20.0, size=100000)           # 分钟
G = rng.geometric(.05, size=100000)               # 每分钟 5% 的切片模型
for t in (10, 20, 30, 60):
    print(f"  {t}\t{exp(-.05 * t):.4f}\t{(T > t).mean():.4f}\t{(G > t).mean():.4f}\t{.95 ** t:.4f}")
print("  mean exp sim", round(T.mean(), 2), "geo sim", round(G.mean(), 2))
ok("L4-ex10 区间概率 0.2387", close(exp(-.5) - exp(-1), 0.2387))
ok("L4-ex11 无记忆", close(exp(-.05 * 50) / exp(-.05 * 20), exp(-1.5), 1e-12))
ok("L4-ex11 均匀对照 1/4 vs 1/2", close(10 / 40, .25) and close(30 / 60, .5))
ok("L4-ex12 λ=ln2, P(X>4)=1/16", close(log(4) / 2, 0.6931) and close(.25 ** 2, .0625) and close(exp(-log(4) / 2 * 2), .25))
ok("L4-ex13 中位数 13.86 分钟", close(log(2) / .05, 13.8629, 1e-3) and close(log(2) / 3 * 60, 13.8629, 1e-3))

# ---- 第 4 节 ----
ok("L4 峰高 N(0,1) N(0,4)", close(1 / sqrt(2 * pi), .3989, 1e-4) and close(1 / (2 * sqrt(2 * pi)), .1995, 1e-4))
ok("L4-ex14 f=c e^{-x^2+2x}", close(integrate.quad(lambda x: exp(-1) / sqrt(pi) * exp(-x * x + 2 * x), -np.inf, np.inf)[0], 1))
ok("L4-ex15 N(2,9) 峰高 0.1330", close(1 / (3 * sqrt(2 * pi)), 0.1330, 1e-4))
print("B(40,.5) vs N(20,10) density:")
for k in (15, 18, 20, 22):
    print(f"  {k}\t{stats.binom(40, .5).pmf(k):.4f}\t{stats.norm(20, sqrt(10)).pdf(k):.4f}")
ok("L4 ∫ e^{-x²/2}=√(2π)", close(integrate.quad(lambda x: exp(-x * x / 2), -np.inf, np.inf)[0], sqrt(2 * pi), 1e-8))

# ---- 第 5 节 ----
print("Phi:", {z: round(Phi(z), 4) for z in (.5, 1, 1.5, 1.96, 2, 2.5, 3)})
ok("L4 3σ", [round(Phi(k) - Phi(-k), 4) for k in (1, 2, 3)] == [.6827, .9545, .9973])
ok("L4 z_α", [round(stats.norm.isf(a), 3) for a in (.05, .025, .005)] == [1.645, 1.96, 2.576])
ok("L4-ex16 身高", close(Phi(2) - Phi(-1), .8186) and close(1 - Phi(2), .0228))
ok("L4-ex17 179.87", close(170 + 1.645 * 6, 179.87))
ok("L4-ex18 μ=6σ=2", close(Phi(-2), .0228) and close(Phi(1), .8413) and close(1 - Phi(1.5), .0668))
ok("L4-ex19 权重 0.0124", close(2 * (1 - Phi(2.5)), .0124, 1e-4))
ok("L4-ex20 标准化比较 1.5 vs 2.4", close((85 - 70) / 10, 1.5) and close((72 - 60) / 5, 2.4) and 1 - Phi(2.4) < 1 - Phi(1.5))
print("tail", round(1 - Phi(1.5), 4), round(1 - Phi(2.4), 4))
rng = np.random.default_rng(9)
x = rng.normal(170, 6, size=100000)
print("height sim table (区间, 理论, 频率):")
for a, b in ((164, 176), (158, 182), (152, 188), (164, 182)):
    print(f"  ({a},{b})\t{Phi((b - 170) / 6) - Phi((a - 170) / 6):.4f}\t{((x > a) & (x < b)).mean():.4f}")
print("  X>182 freq", round((x > 182).mean(), 4))
