"""P.12 讲义里的模拟表与例题数值验算（固定随机种子，数字与 lesson.md 一致）"""
import numpy as np
from scipy.stats import norm, t, chi2, f, binom, poisson


def chk(name, got, want, tol):
    print(("PASS " if abs(got - want) <= tol else "FAIL ") + f"{name} got={got:.5f} want={want}")


chk("tea", 1 / 70, 0.014, 0.0005)
chk("shoot3", binom.cdf(3, 10, .7), 0.0106, 0.00005)
chk("shoot4", binom.cdf(4, 10, .7), 0.0473, 0.00005)
chk("shoot5", binom.cdf(5, 10, .7), 0.1503, 0.00005)
chk("coin9", binom.sf(8, 10, .5), 11 / 1024, 1e-12)
chk("coin8", binom.sf(7, 10, .5), 56 / 1024, 1e-12)
# 第 1、2 节模拟
rng = np.random.default_rng(5)
rows = {}
for mu in (170, 172):
    X = mu + 6 * rng.standard_normal((10000, 36))
    u = X.mean(1) - 170
    p = 2 * (1 - norm.cdf(abs(u)))
    rows[mu] = (abs(u) > 1.96).mean(), [(p <= a).mean() for a in (.01, .05, .10, .50)]
chk("S1-reject-rate", rows[170][0], 0.0493, 0.00005)
for a, w in zip((.01, .05, .10, .50), (0.010, 0.049, 0.097, 0.499)):
    chk(f"S2-H0-{a}", rows[170][1][(.01, .05, .10, .50).index(a)], w, 0.0006)
for a, w in zip((.01, .05, .10, .50), (0.287, 0.512, 0.633, 0.914)):
    chk(f"S2-H1-{a}", rows[172][1][(.01, .05, .10, .50).index(a)], w, 0.0006)
chk("p-u2.1-two", 2 * (1 - norm.cdf(2.1)), 0.0357, 0.00005)
chk("p-u2.1-one", 1 - norm.cdf(2.1), 0.0179, 0.00005)
chk("p-u1.5", 2 * (1 - norm.cdf(1.5)), 0.1336, 0.00005)
chk("p-u2.6", 2 * (1 - norm.cdf(2.6)), 0.0093, 0.00005)
chk("p-n40000", 2 * (1 - norm.cdf(0.012 * 200)), 0.016, 0.0005)
chk("disease", 1 - 19 / 118, 0.84, 0.005)
# 第 3 节
for al, mu1, n, w in ((.05, 172, 36, .361), (.05, 174, 36, .009), (.05, 172, 100, .046),
                      (.01, 172, 36, .628), (.01, 174, 36, .047), (.01, 172, 100, .157)):
    z = norm.isf(al); sh = (mu1 - 170) * np.sqrt(n) / 6
    chk(f"beta-{al}-{mu1}-{n}", norm.cdf(z - sh), w, 0.0006)
chk("power36", 1 - norm.cdf(1.645 - 2), 0.639, 0.001)
chk("ex4-beta", norm.cdf((100 + 1.645 * 1.25 - 103) / 1.25), 0.225, 0.001)
# 第 4-6 节
x = np.array([12.1, 11.6, 12.4, 11.9, 12.3, 11.7]); s = x.std(ddof=1)
for m0, tt, pp in ((11.8, 1.52, 0.189), (11.6, 3.04, 0.029)):
    T = (x.mean() - m0) / (s / np.sqrt(6))
    chk(f"ex6-t-{m0}", T, tt, 0.006); chk(f"ex6-p-{m0}", 2 * (1 - t.cdf(abs(T), 5)), pp, 0.0006)
chk("ex7-T", (10.8 - 10) / (1.5 / 3), 1.6, 1e-9); chk("ex7-p", 1 - t.cdf(1.6, 8), 0.074, 0.0005)
chk("ex5-ex-z", (52.2 - 50) / (3 / np.sqrt(9)), 2.2, 1e-12); chk("ex5-ex-p", 2 * (1 - norm.cdf(2.2)), 0.0278, 0.00005)
A = np.array([50.1, 49.8, 50.4, 50.0, 49.7, 50.3]); B = np.array([50.6, 50.9, 50.4, 50.7, 51.0, 50.5, 50.8])
sw2 = (5 * A.var(ddof=1) + 6 * B.var(ddof=1)) / 11
T = (A.mean() - B.mean()) / np.sqrt(sw2 * (1 / 6 + 1 / 7))
chk("ex8-t", T, -4.79, 0.005); chk("ex8-p", 2 * t.cdf(T, 11), 0.0006, 0.0001)
sw2 = (39 * 1.1 ** 2 + 44 * 1.2 ** 2) / 83
T = (3.42 - 3.81) / np.sqrt(sw2 * (1 / 40 + 1 / 45))
chk("ex9-sw2", sw2, 1.332, 0.001); chk("ex9-t", T, -1.555, 0.001); chk("ex9-p", 2 * t.cdf(T, 83), 0.124, 0.0005)
chk("ex9-crit", t.isf(.025, 83), 1.989, 0.001)
b = np.array([12.4, 15.1, 9.8, 13.6, 11.2, 14.0]); a = np.array([11.5, 14.0, 9.1, 12.9, 10.6, 13.1]); d = b - a
Tp = d.mean() / (d.std(ddof=1) / np.sqrt(6))
chk("ex10-paired-t", Tp, 10.90, 0.005); chk("ex10-paired-p", 2 * (1 - t.cdf(Tp, 5)), 0.0001, 0.0001)
Ti = (b.mean() - a.mean()) / np.sqrt((5 * b.var(ddof=1) + 5 * a.var(ddof=1)) / 10 * (2 / 6))
chk("ex10-indep-t", Ti, 0.75, 0.005); chk("ex10-indep-p", 2 * (1 - t.cdf(Ti, 10)), 0.47, 0.005)
chk("ex11-chi", 9 * 9 / 4, 20.25, 0); chk("ex11-crit", chi2.isf(.05, 9), 16.919, 0.001); chk("ex11-p", chi2.sf(20.25, 9), 0.016, 0.0005)
r = A.var(ddof=1) / B.var(ddof=1)
chk("ex12-F", r, 1.607, 0.001); chk("ex12-crit", f.isf(.025, 5, 6), 5.988, 0.001); chk("ex12-p", 2 * f.sf(r, 5, 6), 0.58, 0.005)
# 第 7 节
se = np.sqrt(sw2 * (1 / 40 + 1 / 45))
chk("ex13-lo", -0.39 - 1.989 * se, -0.889, 0.001); chk("ex13-hi", -0.39 + 1.989 * se, 0.109, 0.001)
h = t.isf(.025, 5) * s / np.sqrt(6)
chk("S7-lo", x.mean() - h, 11.66, 0.005); chk("S7-hi", x.mean() + h, 12.34, 0.005)
# 第 8 节
za, zb = norm.isf(.05), norm.isf(.10)
chk("ex14-n", ((za + zb) * 6 / 2) ** 2, 77.09, 0.03)
chk("ex14-power78", 1 - norm.cdf(za - 2 * np.sqrt(78) / 6), 0.903, 0.0005)
chk("ex15-n", (norm.isf(.025) + norm.isf(.2)) ** 2 * (.09 + .0979) / .01 ** 2, 14748.2, 0.5)
se2 = np.sqrt((.09 + .0979) / 2000)
chk("ex15-power2000", 1 - norm.cdf(1.96 - .01 / se2) + norm.cdf(-1.96 - .01 / se2), 0.18, 0.005)
chk("ex-n-exercise", ((norm.isf(.025) + norm.isf(.2)) * 4 / 1) ** 2, 125.6, 0.1)
# 第 9 节
O = np.array([30, 14, 12, 26, 25, 13])
chk("ex16-chi", ((O - 20) ** 2 / 20).sum(), 15.5, 1e-9); chk("ex16-p", chi2.sf(15.5, 5), 0.0084, 0.00005)
chk("ex16-crit", chi2.isf(.05, 5), 11.07, 0.001)
cnt = {0: 7, 1: 15, 2: 22, 3: 22, 4: 17, 5: 9, 6: 5, 7: 2, 8: 1}
lam = sum(k * v for k, v in cnt.items()) / 100
chk("ex17-lam", lam, 2.9, 1e-9)
O = np.array([7, 15, 22, 22, 17, 9, 8]); pr = [poisson.pmf(k, lam) for k in range(6)]; pr.append(1 - sum(pr)); E = 100 * np.array(pr)
for i, w in enumerate((5.50, 15.96, 23.14, 22.37, 16.22, 9.40, 7.42)):
    chk(f"ex17-E{i}", E[i], w, 0.005)
chk("ex17-chi", ((O - E) ** 2 / E).sum(), 0.63, 0.005); chk("ex17-p", chi2.sf(((O - E) ** 2 / E).sum(), 5), 0.987, 0.0005)
chk("ex17-allE>=5", float((E >= 5).all()), 1.0, 0)
chk("coin60", (10 ** 2 / 50) * 2, 4.0, 0); chk("coin60-crit", chi2.isf(.05, 1), 3.841, 0.001)
# 第 10 节
dd = np.array([1] * 6 + [-1] * 2 + [0] * 32)
rng = np.random.default_rng(2026)
idx = rng.integers(0, 40, (10000, 40)); m = dd[idx].mean(1)
chk("ex18-lo", np.percentile(m, 2.5), -0.025, 0.0005); chk("ex18-hi", np.percentile(m, 97.5), 0.225, 0.0005)
chk("ex18-sd", m.std(), 0.069, 0.0005)
tl = 0.1 - t.isf(.025, 39) * dd.std(ddof=1) / np.sqrt(40); th = 0.1 + t.isf(.025, 39) * dd.std(ddof=1) / np.sqrt(40)
chk("ex18-t-lo", tl, -0.041, 0.001); chk("ex18-t-hi", th, 0.241, 0.001)
chk("ex18-dmean", dd.mean(), 0.10, 1e-9)
chk("boot-miss40", (39 / 40) ** 40, 0.363, 0.0005)

# 编辑二稿新增：第 3 节入口、各方法随堂小题、开头问题的样本量、合并方差反例
chk("edit-beta-p05", binom.sf(4, 10, .5), 0.623, 0.0005)
_c = 100 + 1.645 * 1.25
chk("edit-m3-beta", norm.cdf((_c - 104) / 1.25), 0.060, 0.0005)
chk("edit-m5-t", 1.5 / (2 * np.sqrt(.2)), 1.677, 0.0005); chk("edit-m5-p", 2 * t.sf(1.5 / (2 * np.sqrt(.2)), 18), 0.111, 0.0005)
chk("edit-m6-chi", 15 * 7 / 4, 26.25, 1e-9); chk("edit-m6-crit", chi2.isf(.05, 15), 24.996, 0.0005); chk("edit-m6-p", chi2.sf(26.25, 15), 0.035, 0.0005)
_v = .09 + .104 * .896
chk("edit-open-n", (norm.isf(.025) + norm.isf(.2)) ** 2 * _v / .004 ** 2, 89861.8, 0.2)
chk("edit-open-power20000", 1 - norm.cdf(norm.isf(.025) - .004 / np.sqrt(_v / 20000)), 0.26, 0.005)
_rng = np.random.default_rng(12); _rej = 0
for _ in range(20000):
    _a = _rng.normal(0, 3, 5); _b = _rng.normal(0, 1, 50)
    _sw = np.sqrt((4 * _a.var(ddof=1) + 49 * _b.var(ddof=1)) / 53)
    _rej += abs((_a.mean() - _b.mean()) / (_sw * np.sqrt(1 / 5 + 1 / 50))) > t.isf(.025, 53)
chk("edit-pooled-unequal", _rej / 20000, 0.39, 0.005)
chk("edit-dice-over", sum(o > 20 for o in (30, 14, 12, 26, 25, 13)), 3, 0)
print("MANUAL S7-duality-proof 对偶证明的等价变形按讲义手工核对")
