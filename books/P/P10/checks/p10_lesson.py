"""独立核对 lesson.md 的 19 道例题、随堂题和分位数表：数值由数据、定义或分布函数重算，再与讲义文本比对。"""
from fractions import Fraction as Fr
from math import ceil, comb, sqrt
from pathlib import Path

import numpy as np
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
LESSON = (ROOT / "lesson.md").read_text(encoding="utf-8")


def result(k, condition):
    print(f"PASS 例{k}" if condition else f"FAIL 例{k}")


def med(v):
    v = sorted(v)
    n = len(v)
    return v[n // 2] if n % 2 else Fr(v[n // 2 - 1] + v[n // 2], 2)


def five(v):
    """本章约定：n 为奇数时，两半都不含总的中位数。"""
    v = sorted(v)
    n = len(v)
    lo, hi = v[: n // 2], v[(n + 1) // 2:]
    return (v[0], med(lo), med(v), med(hi), v[-1])


# 例 1–2 及随堂题：独立事件与伯努利联合概率。
p1 = stats.norm.sf((164 - 170) / 6) ** 4
result(1, abs(p1 - 0.5011) < 0.0001 and "0.5011" in LESSON and Fr(1, 2) ** 4 == Fr(1, 16) and "0.0625" in LESSON)
result(2, abs(0.6**3 * 0.4**2 - 0.03456) < 1e-12 and "0.03456" in LESSON)

# 例 3 及随堂题：五数概括、异常点，按本章四分位数约定从数据重算。
d3 = [12, 15, 16, 18, 19, 21, 22, 25, 27, 31, 58]
f3 = five(d3)
iqr3 = f3[3] - f3[1]
out3 = [x for x in d3 if x > f3[3] + 1.5 * iqr3 or x < f3[1] - 1.5 * iqr3]
d3b = [3, 5, 6, 8, 9, 12, 14, 30]
f3b = five(d3b)
iqr3b = f3b[3] - f3b[1]
out3b = [x for x in d3b if x > f3b[3] + Fr(3, 2) * iqr3b or x < f3b[1] - Fr(3, 2) * iqr3b]
result(3, f3 == (12, 16, 21, 27, 58) and out3 == [58] and Fr(sum(d3), 11) == 24 and "(12,16,21,27,58)" in LESSON
       and f3b == (3, Fr(11, 2), Fr(17, 2), 13, 30) and out3b == [30] and "(3,5.5,8.5,13,30)" in LESSON)

# 例 4：不等宽分组的柱高 = 个数/(n·组宽)，面积和为 1。
edges = [(10, 20), (20, 30), (30, 60)]
cnt = [sum(a <= x < b for x in d3) for a, b in edges]
h = [Fr(c, 11 * (b - a)) for c, (a, b) in zip(cnt, edges)]
area = sum(hh * (b - a) for hh, (a, b) in zip(h, edges))
result(4, cnt == [5, 4, 2] and area == 1 and all(f"{float(x):.4f}" in LESSON for x in h))

# 例 5 及随堂题：样本均值与样本方差。
d5 = np.array([4, 7, 5, 9, 10])
d5b = np.array([2, 4, 6])
result(5, d5.mean() == 7 and d5.var(ddof=1) == 6.5 and "\\sqrt{6.5}\\approx2.55" in LESSON
       and d5b.mean() == 4 and d5b.var(ddof=1) == 4)

# 例 6：离散均匀 1..6 的方差 35/12，标准差 ≤ 0.1 的最小 n。
vals = np.arange(1, 7)
var6 = Fr(sum(int(v) ** 2 for v in vals), 6) - Fr(sum(int(v) for v in vals), 6) ** 2
n6 = next(n for n in range(1, 10000) if var6 / n <= Fr(1, 100))
result(6, var6 == Fr(35, 12) and n6 == 292 and ceil(float(var6) * 100) == 292 and "至少 292" in LESSON)

# 例 7：均值与估计标准误。
d7 = np.array([71.2, 69.8, 70.5, 72.1, 70.9])
se7 = d7.std(ddof=1) / sqrt(5)
result(7, abs(d7.mean() - 70.9) < 1e-12 and abs(d7.var(ddof=1) - 0.725) < 1e-12 and abs(se7 - 0.381) < 0.0005
       and "70.9\\pm0.38" in LESSON)

# 卡方分位数表与第 4 节 n=10、n=50 的数值。
tab = {1: 3.841, 2: 5.991, 5: 11.070, 10: 18.307}
ok_tab = all(abs(stats.chi2.isf(0.05, k) - v) < 0.0005 for k, v in tab.items())
ok_10 = (abs(stats.chi2.isf(0.025, 10) - 20.483) < 0.0005 and abs(stats.chi2.isf(0.975, 10) - 3.247) < 0.0005
         and abs(stats.chi2.isf(0.95, 10) - 3.940) < 0.0005)
ok_50 = abs(stats.chi2.isf(0.05, 50) - 67.505) < 0.0005 and abs(stats.norm.sf(1.75) - 0.040) < 0.001

# 例 8–10：chi-square 分布。
result(8, ok_tab and ok_10 and ok_50 and abs(stats.chi2.isf(0.95, 5) - 1.145) < 0.0005
       and abs(stats.chi2.cdf(3.940, 10) - 0.05) < 0.001 and "1.145" in LESSON)
result(9, abs(stats.chi2.sf(73.2 / 4, 10) - 0.05) < 0.001 and "73.2/4=18.3" in LESSON)
result(10, 2 * 5 + 5**2 == 35 and "n(n+2)" in LESSON)

# 例 11–13：正态样本的均值、方差及独立性。
result(11, abs((2 * stats.norm.cdf(1.5) - 1) - 0.8664) < 0.0001 and abs((2 * stats.norm.cdf(3) - 1) - 0.9973) < 0.0001)
c12 = stats.chi2.isf(0.05, 8) / 2
result(12, abs(c12 - 7.754) < 0.001 and (16 / 64) * 16 == 4 and 32 / 8 == 4)
result(13, abs(0.5 * stats.chi2.cdf(8, 8) - 0.2833) < 0.0005 and abs(stats.chi2.cdf(8, 8) - 0.5665) < 0.0005)

# t 分位数表。
ttab = {4: 2.776, 8: 2.306, 10: 2.228, 20: 2.086, 30: 2.042}
ok_t = all(abs(stats.t.isf(0.025, k) - v) < 0.0005 for k, v in ttab.items()) and abs(stats.norm.isf(0.025) - 1.960) < 0.0005

# 例 14–16：t 分布对称性、单样本和合并方差。
result(14, ok_t and abs(stats.t.isf(0.05, 8) - 1.860) < 0.0005 and abs(2 * stats.t.sf(2.306, 8) - 0.05) < 0.001
       and abs(stats.t.cdf(-2.262, 9) - 0.025) < 0.0005)
d15 = np.array([9.8, 10.2, 10.4, 9.9, 10.2])
t15 = (d15.mean() - 10) / (d15.std(ddof=1) / sqrt(5))
p15 = 2 * stats.t.sf(abs(t15), 4)
result(15, abs(((d15 - d15.mean()) ** 2).sum() - 0.24) < 1e-12 and abs(t15 - 0.913) < 0.0005
       and abs(p15 - 0.413) < 0.001 and "0.913" in LESSON and "0.413" in LESSON)
sw16 = Fr(5 * Fr(42, 10) + 8 * 3, 13)
result(16, sw16 == Fr(45, 13) and "t(13)" in LESSON)

# 例 17–19：F 分布倒数关系、方差比和 t^2，与分布函数对照。
f05_5_10, f05_10_5 = stats.f.isf(0.05, 5, 10), stats.f.isf(0.05, 10, 5)
f95_5_10 = stats.f.isf(0.95, 5, 10)
result(17, abs(f05_5_10 - 3.326) < 0.0005 and abs(f05_10_5 - 4.735) < 0.0005 and abs(f95_5_10 - 1 / f05_10_5) < 1e-9
       and abs(1 / 4.735 - 0.2112) < 0.0001 and abs(stats.f.isf(0.95, 6, 8) - 1 / 4.147) < 0.0005)
result(18, abs(stats.f.isf(0.05, 7, 9) - 3.293) < 0.0005 and abs(stats.f.isf(0.025, 7, 9) - 4.197) < 0.0005
       and abs(stats.f.isf(0.025, 9, 7) - 4.823) < 0.0005 and abs(stats.f.isf(0.975, 7, 9) - 0.2073) < 0.0005)
t10 = stats.t.isf(0.025, 10)
result(19, abs(t10**2 - stats.f.isf(0.05, 1, 10)) < 1e-9 and abs(t10 - 2.228138852) < 1e-8
       and abs(t10**2 - 4.964602744) < 1e-8 and abs(sqrt(4.965) - 2.228228) < 1e-6
       and abs(stats.f.sf(4.965, 1, 10) - 0.05) < 0.001)
