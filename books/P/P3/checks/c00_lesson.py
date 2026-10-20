"""P.3 讲义里的例题数值与模拟表（固定随机种子）。"""
import numpy as np
from math import comb, exp, log
from scipy import stats


def ok(name, cond):
    print(("PASS " if cond else "FAIL ") + name)


def close(a, b, tol=5e-5):
    return abs(a - b) < tol


# ---- 第 1、2 节 ----
ok("L3-ex1 {X=2} 三个结果", comb(3, 2) == 3 and close(3 / 8, 0.375))
pS = {s: (6 - abs(s - 7)) / 36 for s in range(2, 13)}
ok("L3-S 分布律和为 1", close(sum(pS.values()), 1))
ok("L3-ex2 P(S=4)=3/36, P(M<=2)=4/36",
   sum(1 for a in range(1, 7) for b in range(1, 7) if a + b == 4) == 3
   and sum(1 for a in range(1, 7) for b in range(1, 7) if max(a, b) <= 2) == 4)
pM = {m: (2 * m - 1) / 36 for m in range(1, 7)}
ok("L3-ex3 M 分布律", all(close(pM[m], sum(1 for a in range(1, 7) for b in range(1, 7) if max(a, b) == m) / 36) for m in pM))
ok("L3-ex4 取球 (1/10,6/10,3/10)", [comb(3, k) * comb(2, 2 - k) / comb(5, 2) for k in range(3)] == [0.1, 0.6, 0.3])
ok("L3-ex5 c=1/10, P(X<=2)=0.3", close(sum(range(1, 5)) * 0.1, 1) and close((1 + 2) * 0.1, 0.3))
ok("L3-ex5 n-gram 前两名 0.7", close((4 + 3) / 10, 0.7))
ok("L3 阳性 0.059", close(0.01 * 0.95 + 0.99 * 0.05, 0.059))
rng = np.random.default_rng(2026)
s = rng.integers(1, 7, size=(100000, 2)).sum(1)
print("dice-table: s, exact, freq")
for k in range(2, 13):
    print(f"  {k}\t{pS[k]:.4f}\t{(s == k).mean():.4f}")
ok("L3-sim 点数和 7 的频率接近 1/6", abs((s == 7).mean() - 1 / 6) < 0.005)

# ---- 第 3 节 ----
pX = [1 / 8, 3 / 8, 3 / 8, 1 / 8]
F = lambda x: sum(pX[k] for k in range(4) if k <= x)
ok("L3-ex6 F(2)-F(0.5)=3/4", close(F(2) - F(0.5), 0.75))
ok("L3-ex6 F 在 1 处的值与左极限", close(F(1), 0.5) and close(F(0.999), 0.125))
ok("L3-ex7 由 F 反求", close(0.3, 0.3) and close(0.8 - 0.3, 0.5) and close(1 - 0.8, 0.2) and close(1.0 - 0.3, 0.7))

# ---- 第 4 节 ----
b = stats.binom(10, 0.7)
ok("L3 B(10,.7) P(7)=0.2668", close(b.pmf(7), 0.2668))
ok("L3 B(10,.7) P(X>=8)=0.3828", close(b.sf(7), 0.3828) and close(b.pmf(8) + b.pmf(9) + b.pmf(10), 0.3828))
ok("L3 最可能值 7", int(np.argmax([b.pmf(k) for k in range(11)])) == 7 and int((10 + 1) * 0.7) == 7)
ok("L3 比值 k=7,8", close(4 * .7 / (7 * .3), 4 / 3, 1e-9) and 3 * .7 / (8 * .3) < 1)
ok("L3-ex9 至少一次 1-(5/6)^6", close(1 - (5 / 6) ** 6, 0.6651))
ok("L3-ex10 n>=29", log(.05) / log(.9) > 28 and 1 - .9 ** 28 < .95 <= 1 - .9 ** 29)
b9 = stats.binom(9, .3)
ok("L3-ex11 B(9,.3) P(2)=P(3)", close(b9.pmf(2), b9.pmf(3), 1e-12) and close(b9.pmf(2), 0.2668))
rng = np.random.default_rng(7)
x = rng.binomial(10, .7, size=100000)
print("binom-table: k, exact, freq")
for k in range(3, 11):
    print(f"  {k}\t{b.pmf(k):.4f}\t{(x == k).mean():.4f}")
print("  P(X>=8) exact", round(b.sf(7), 4), "freq", round((x >= 8).mean(), 4))
ok("L3-sim 二项 7 的频率", abs((x == 7).mean() - b.pmf(7)) < 0.006)

# ---- 第 5 节 ----
ok("L3 几何 P(X=3)=0.063", close(0.3 ** 2 * 0.7, 0.063))
ok("L3-ex12 P(X>3)=0.027 P(X<=3)=0.973", close(0.3 ** 3, 0.027) and close(1 - 0.3 ** 3, 0.973))
ok("L3-ex13 无记忆", close((0.3 ** 3 - 0.3 ** 5) / 0.3 ** 3, 0.91) and close(1 - 0.3 ** 2, 0.91))
ok("L3-ex14 偶数次结束 5/11", close(sum((5 / 6) ** (k - 1) / 6 for k in range(2, 400, 2)), 5 / 11, 1e-9))
rng = np.random.default_rng(11)
g = rng.geometric(.7, size=100000)
print("geom-table: k, exact, freq")
for k in range(1, 7):
    print(f"  {k}\t{.3 ** (k - 1) * .7:.4f}\t{(g == k).mean():.4f}")
print("  mean trials", round(g.mean(), 4), " 1/p =", round(1 / .7, 4))
ok("L3-sim 几何平均 1.43", abs(g.mean() - 1 / .7) < 0.02)
ok("L3-sim 无记忆：已失败 2 次后的剩余次数分布", abs((g[g > 2] - 2 == 1).mean() - 0.7) < 0.01)
print("  conditional  P(X=3|X>2) freq", round((g[g > 2] == 3).mean(), 4))

# ---- 第 6 节 ----
h = stats.hypergeom(20, 5, 4)
print("hyper-table N=20 M=5 n=4:", [round(h.pmf(k), 4) for k in range(5)])
ok("L3-ex15 超几何 P(X>=1)", close(1 - comb(15, 4) / comb(20, 4), 0.7183) and close(h.sf(0), 0.7183))
ok("L3-ex15 放回 B(4,1/4) P(0)=0.3164", close(.75 ** 4, 0.3164))
ok("L3-ex16 取值范围 2..5", [comb(7, k) * comb(3, 5 - k) / comb(10, 5) for k in range(6)][2:] == [comb(7, k) * comb(3, 5 - k) / comb(10, 5) for k in range(2, 6)])
ok("L3-ex16 概率 1/12,5/12,5/12,1/12", all(close(comb(7, k) * comb(3, 5 - k) / comb(10, 5), v) for k, v in zip(range(2, 6), [1 / 12, 5 / 12, 5 / 12, 1 / 12])))
ok("L3-ex17 抽检拒收 0.3530", close(1 - comb(46, 5) / comb(50, 5), 0.3530))
print("hyper vs binom N=1000 M=100 n=5:")
for k in range(4):
    print(f"  {k}\t{stats.hypergeom(1000, 100, 5).pmf(k):.4f}\t{stats.binom(5, .1).pmf(k):.4f}")

# ---- 第 7 节 ----
pp = stats.poisson(3)
ok("L3 泊松 P(0)=0.0498", close(pp.pmf(0), 0.0498))
ok("L3 泊松 P(N<=2)=0.4232", close(pp.cdf(2), 0.4232))
ok("L3 泊松 P(N>=5)=0.1847", close(pp.sf(4), 0.1847))
ok("L3 泊松 P(3)=P(2)=0.2240", close(pp.pmf(3), 0.2240) and close(pp.pmf(2), pp.pmf(3), 1e-12))
ok("L3-ex19 半小时 1-e^-1.5", close(1 - exp(-1.5), 0.7769))
print("poisson vs B(60,0.05):")
for k in range(7):
    print(f"  {k}\t{stats.binom(60, .05).pmf(k):.4f}\t{pp.pmf(k):.4f}")
ok("L3-ex20 B(200,.005) 近似 P(X>=2)", close(stats.binom(200, .005).sf(1), 0.2642) and close(1 - 2 * exp(-1), 0.2642))
ok("L3-ex21 罕见词", close(exp(-2), 0.1353) and close(1 - 5 * exp(-2), 0.3233) and close(stats.binom(1000, .002).sf(2), 0.3233))
