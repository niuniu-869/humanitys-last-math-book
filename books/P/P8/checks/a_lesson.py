"""讲义例题里的数值（作者自检）：固定种子的模拟表也在这里复现。"""
from math import acos, comb, sqrt
import numpy as np
from scipy import stats
from fractions import Fraction as F

def chk(name, ok):
    print(("PASS " if ok else "FAIL ") + name)

chk("E1 马尔可夫 1/4, e^-4=0.0183", F(3, 12) == F(1, 4) and abs(np.exp(-4) - 0.0183) < 1e-4)
chk("E2 切比雪夫 35/96, 真值 1/6", F(35, 6) / 16 == F(35, 96) and F(1 + 2 + 2 + 1, 36) == F(1, 6) and abs(35 / 96 - 0.365) < 1e-3)
S = {s: F(6 - abs(s - 7), 36) for s in range(2, 13)}
chk("E2 S 的方差 35/6", sum(s * s * p for s, p in S.items()) - 49 == F(35, 6))
b = stats.binom(100, .7)
chk("E3 界 0.21, 精确 0.037", abs(21 / 100 - 0.21) < 1e-12 and abs(b.cdf(60) + b.sf(79) - 0.0375) < 1e-4)
chk("E4 下界 8/9, 正态 0.9973", F(1) - F(25, 225) == F(8, 9) and abs(stats.norm.cdf(3) - stats.norm.cdf(-3) - 0.9973) < 1e-4)
chk("练习 5/20", F(5, 20) == F(1, 4))
chk("E5 E(X_n)=1", n_ok := all(n * F(1, n) == 1 for n in range(1, 50)))
chk("E6 n≥50000, 正态 9604", abs(0.25 / (0.05 * 0.0001) - 50000) < 1e-6 and abs((1.96 * .5 / .01)**2 - 9604) < 1e-6 and (98 * 0.02) >= 1.96 and 97 * 0.02 < 1.96)
chk("E7 n≥5834, 正态约1120", abs(35 / 12 / (0.05 * 0.01) - 5833.33) < 0.01 and abs((1.96 * sqrt(35 / 12) / 0.1)**2 - 1120.5) < 0.1)
rng = np.random.default_rng(20261017)
exp_sd = {10: (0.560, 0.540, 0.080), 100: (0.172, 0.171, 0.423), 1000: (0.0553, 0.0540, 0.931), 10000: (0.0174, 0.0171, 1.0)}
ok = True
for n in (10, 100, 1000, 10000):
    m = rng.integers(1, 7, size=(2000, n)).mean(1)
    sd, th, fr = m.std(), sqrt(35 / 12 / n), np.mean(np.abs(m - 3.5) < 0.1)
    e = exp_sd[n]
    ok &= abs(sd - e[0]) < (0.0006 if n < 1000 else 0.00006) and abs(th - e[1]) < 0.00051 and abs(fr - e[2]) < 0.0006
chk("E7 模拟表（种子 20261017）", bool(ok))
rng = np.random.default_rng(7)
est = {}
for n in (100, 10000, 1000000):
    p = rng.random((n, 2)); est[n] = 4 * np.mean((p**2).sum(1) < 1)
se = {n: 4 * sqrt(np.pi / 4 * (1 - np.pi / 4) / n) for n in est}
chk("E8 π 模拟 3.080/3.162/3.1437", abs(est[100] - 3.080) < 1e-9 and abs(est[10000] - 3.162) < 1e-9 and abs(est[1000000] - 3.1437) < 5e-5)
chk("E8 标准误差 0.164/0.0164/0.00164", abs(se[100] - 0.164) < 5e-4 and abs(se[10000] - 0.0164) < 5e-5 and abs(se[1000000] - 0.00164) < 5e-6)
rng = np.random.default_rng(3)
fr = {}
for n in (1, 10, 100, 1000):
    fr[n] = np.mean(np.abs(rng.standard_cauchy((4000, n)).mean(1)) > 1)
chk("E9 柯西 0.507/0.500/0.516/0.514（理论 0.5）", abs(fr[1] - 0.507) < 6e-4 and abs(fr[10] - 0.500) < 6e-4 and abs(fr[100] - 0.516) < 6e-4 and abs(fr[1000] - 0.514) < 6e-4 and abs(2 * stats.cauchy.sf(1) - 0.5) < 1e-12)
chk("E10 批量 sd 1/0.25/0.0625, B≥1600", np.allclose(2 / np.sqrt([4, 64, 1024]), [1, .25, .0625]) and (2 / 0.05)**2 == 1600)
mu, s = 70, sqrt(21)
chk("E11 ③ P(X≥75): 精确 0.1631, 修正 0.1631, 未修正 0.1376", abs(b.sf(74) - 0.1631) < 5e-5 and abs(stats.norm.sf(4.5 / s) - 0.1631) < 1e-4 and abs(stats.norm.sf(5 / s) - 0.1376) < 5e-5 and abs(4.5 / s - 0.982) < 1e-3 and abs(5 / s - 1.091) < 1e-3)
chk("练习 400 次 z=1.45", (214.5 - 200) / 10 == 1.45)
s2 = sqrt(250); ex = stats.binom.cdf(520, 1000, .5) - stats.binom.cdf(479, 1000, .5)
chk("E12 区间 0.8052 / 0.7941", abs(2 * stats.norm.cdf(20.5 / s2) - 1 - 0.8052) < 1e-4 and abs(ex - 0.8052) < 1e-4 and abs(2 * stats.norm.cdf(20 / s2) - 1 - 0.7941) < 1e-4 and abs(20.5 / s2 - 1.297) < 1e-3)
b2 = stats.binom(1000, .002); sg = sqrt(1000 * .002 * .998)
nm = lambda k: stats.norm.cdf((k + .5 - 2) / sg) - stats.norm.cdf((k - .5 - 2) / sg)
ok = all(abs(b2.pmf(k) - e1) < 6e-5 and abs(stats.poisson(2).pmf(k) - e2) < 6e-5 and abs(nm(k) - e3) < 6e-5 for k, e1, e2, e3 in
         [(0, .1351, .1353, .1058), (1, .2707, .2707, .2175), (2, .2709, .2707, .2766), (4, .0902, .0902, .1058)])
chk("§4 泊松/正态比较表, 负半轴 0.038", ok and abs(stats.norm.cdf((-.5 - 2) / sg) - 0.0384) < 1e-4 and abs(sg**2 - 1.996) < 1e-9)
chk("E14 48 个均匀 0.1587", abs(stats.norm.sf(1) - 0.1587) < 1e-4 and 48 / 12 == 4)
chk("E15 0.0786 / 0.0844", abs(stats.norm.sf(0.2 * sqrt(50)) - 0.0786) < 1e-4 and abs(stats.gamma(50).sf(60) - 0.0844) < 1e-4 and abs(0.2 * sqrt(50) - 1.414) < 1e-3)
ex = {1: .0518, 5: .0433, 30: .0340, 200: .0288}
chk("§5 指数和上尾表", all(abs(stats.gamma(n).sf(n + 1.96 * sqrt(n)) - v) < 6e-5 for n, v in ex.items()) and abs(stats.norm.sf(1.96) - 0.0250) < 5e-5)
sd = sqrt(.8 * .2 / 500)
chk("E16 误差条 0.0179, ±0.035, [0.765,0.835], 2000 题 0.0089", abs(sd - 0.0179) < 5e-5 and abs(1.96 * sd - 0.035) < 5e-4 and abs(0.8 - 1.96 * sd - 0.765) < 5e-4 and abs(0.8 + 1.96 * sd - 0.835) < 5e-4 and abs(sqrt(.8 * .2 / 2000) - 0.0089) < 5e-5)
