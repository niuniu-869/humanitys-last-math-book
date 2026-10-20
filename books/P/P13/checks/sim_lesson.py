"""讲义里模拟表的数字（固定种子）。"""
import numpy as np
from scipy import stats

rng = np.random.default_rng(2026)
N = 100000


def pair_p(g, i, j):
    a, b = g[:, i, :], g[:, j, :]
    n = a.shape[1]
    sp2 = (a.var(axis=1, ddof=1) + b.var(axis=1, ddof=1)) / 2
    t = (a.mean(1) - b.mean(1)) / np.sqrt(sp2 * 2 / n)
    return 2 * stats.t.sf(np.abs(t), 2 * n - 2)


def f_p(g):
    k, n = g.shape[1:]
    m = g.mean(2)
    ssb = n * ((m - m.mean(1, keepdims=True)) ** 2).sum(1)
    ssw = ((g - m[:, :, None]) ** 2).sum((1, 2))
    return stats.f.sf(ssb / (k - 1) / (ssw / (k * (n - 1))), k - 1, k * (n - 1))


g3 = rng.normal(0, 1, (N, 3, 5))
p01 = pair_p(g3, 0, 1)
anyp = np.min([pair_p(g3, i, j) for i, j in ((0, 1), (0, 2), (1, 2))], axis=0)
fp = f_p(g3)
r1, r3, rf = (p01 < .05).mean(), (anyp < .05).mean(), (fp < .05).mean()
print(f"SIM1 单次 {r1:.4f} 三对任一 {r3:.4f} F {rf:.4f}")
print("PASS 单次约5%" if abs(r1 - .05) < .004 else "FAIL 单次")
print("PASS F约5%" if abs(rf - .05) < .004 else "FAIL F")
print("PASS 三对任一明显大于5%" if r3 > .10 else "FAIL 三对")

g5 = rng.normal(0, 1, (N // 5, 5, 5))
mins = np.min([pair_p(g5, i, j) for i in range(5) for j in range(i + 1, 5)], axis=0)
r5 = (mins < .05).mean()
print(f"SIM2 五组十对任一 {r5:.4f}")
print("PASS 五组>25%" if r5 > .25 else "FAIL 五组")

M = 1_000_000
rho = .5
x = rng.normal(170, 6, M)
y = 170 + rho * (x - 170) + rng.normal(0, 6 * np.sqrt(1 - rho**2), M)
a = y[x > 182].mean()
b = x[y > 182].mean()
exact = 170 + rho * 6 * stats.norm.pdf(2) / stats.norm.sf(2)
print(f"SIM3 父>182 时子均值 {a:.2f}；子>182 时父均值 {b:.2f}；精确 {exact:.2f}；slope {np.polyfit(x, y, 1)[0]:.3f}")
print("PASS 回归到均值" if abs(a - exact) < .15 and abs(b - exact) < .15 else "FAIL 回归到均值")
