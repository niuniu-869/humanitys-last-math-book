"""P.11 讲义里的模拟表与例题数值验算（固定随机种子，数字与 lesson.md 一致）"""
import numpy as np
from pathlib import Path
import re
import sys
from scipy.integrate import quad
from scipy.stats import norm, t, chi2, f, binom

lesson = (Path(__file__).resolve().parents[1] / "lesson.md").read_text(encoding="utf-8")
failures = 0


def chk(name, got, want, tol):
    global failures
    passed = abs(got - want) <= tol
    failures += not passed
    print(("PASS " if passed else "FAIL ") + f"{name} got={got:.6f} want={want}")


# 第 1 节：三个估计量的重复抽样
rng = np.random.default_rng(2026)
R, n, p = 20000, 10, 0.7
X = rng.random((R, n)) < p
S = X.sum(1)
est = {"p1": S / n, "p2": X[:, 0].astype(float), "p3": (S + 1) / (n + 2)}
rows = re.findall(r"(?m)^\| \$\\hat p_[123].*?\| ([\d.]+) \| ([\d.]+) \| ([\d.]+) \|$", lesson)
assert len(rows) == 3, rows
want = {f"p{i}": tuple(map(float, row)) for i, row in enumerate(rows, 1)}
for k, e in est.items():
    w = want[k]
    chk(f"L11-{k}-mean seed=2026", e.mean(), w[0], 0.0005)
    chk(f"L11-{k}-sd seed=2026", e.std(), w[1], 0.0005)
    chk(f"L11-{k}-in seed=2026", (abs(e - 0.7) <= 0.1 + 1e-9).mean(), w[2], 0.0005)

# 第 5 节：n=5 的 sigma^2 估计
rng = np.random.default_rng(2026)
Z = rng.standard_normal((100000, 5))
chk("L5-sig2hat seed=2026", Z.var(1).mean(), 0.80, 0.005)
chk("L5-S2 seed=2026", Z.var(1, ddof=1).mean(), 1.00, 0.005)
chk("L5-S seed=2026", np.sqrt(Z.var(1, ddof=1)).mean(), 0.94, 0.005)

# 第 8 节：覆盖率与 20 个区间
rng = np.random.default_rng(7)
xb = (170 + 6 * rng.standard_normal((10000, 36))).mean(1)
printed_count = int(re.search(r"其中 (\d+) 个区间盖住了真值", lesson)[1])
chk("L8-cover-count seed=7", (abs(xb - 170) <= 1.96).sum(), printed_count, 0)
rng = np.random.default_rng(2)
xb = (170 + 6 * rng.standard_normal((20, 36))).mean(1)
chk("L8-miss20 seed=2", (abs(xb - 170) > 1.96).sum(), 1, 0)

# 第 9 节：σ 未知时 z 与 t 的覆盖
rng = np.random.default_rng(3)
Y = 170 + 6 * rng.standard_normal((20000, 5))
xb, s = Y.mean(1), Y.std(1, ddof=1)
chk("L9-z seed=3", (abs(xb - 170) <= 1.96 * s / np.sqrt(5)).mean(), 0.878, 0.0005)
chk("L9-t seed=3", (abs(xb - 170) <= 2.776 * s / np.sqrt(5)).mean(), 0.950, 0.0005)

# 例题数值
x = np.array([12.1, 11.6, 12.4, 11.9, 12.3, 11.7])
m, s2 = x.mean(), x.var(ddof=1)
h = t.ppf(.975, 5) * np.sqrt(s2 / 6)
chk("ex19-lo", m - h, 11.66, 0.006); chk("ex19-hi", m + h, 12.34, 0.006)
chk("ex20-lo", 5 * s2 / chi2.isf(.025, 5), 0.0405, 0.0001); chk("ex20-hi", 5 * s2 / chi2.isf(.975, 5), 0.6256, 0.0002)
chk("ex18-lo", chi2.isf(.975, 10) / 180, 0.0180, 0.0001); chk("ex18-hi", chi2.isf(.025, 10) / 180, 0.1138, 0.0001)
chk("ex21-half", t.ppf(.975, 8) * 2.4 / 3, 1.845, 0.001)
A = np.array([50.1, 49.8, 50.4, 50.0, 49.7, 50.3]); B = np.array([50.6, 50.9, 50.4, 50.7, 51.0, 50.5, 50.8])
sw2 = (5 * A.var(ddof=1) + 6 * B.var(ddof=1)) / 11
hh = t.ppf(.975, 11) * np.sqrt(sw2 * (1 / 6 + 1 / 7)); d = A.mean() - B.mean()
chk("ex22-lo", d - hh, -0.949, 0.001); chk("ex22-hi", d + hh, -0.351, 0.001)
r = A.var(ddof=1) / B.var(ddof=1)
chk("ex23-lo", r / f.isf(.025, 5, 6), 0.268, 0.001); chk("ex23-hi", r / f.isf(.975, 5, 6), 11.21, 0.01)
bf = np.array([12.4, 15.1, 9.8, 13.6, 11.2, 14.0]); af = np.array([11.5, 14.0, 9.1, 12.9, 10.6, 13.1]); dd = bf - af
hp = t.ppf(.975, 5) * dd.std(ddof=1) / np.sqrt(6)
chk("ex24-paired-lo", dd.mean() - hp, 0.62, 0.005); chk("ex24-paired-hi", dd.mean() + hp, 1.01, 0.005)
hi = t.ppf(.975, 10) * np.sqrt((5 * bf.var(ddof=1) + 5 * af.var(ddof=1)) / 10 * (2 / 6))
chk("ex24-indep-lo", dd.mean() - hi, -1.61, 0.005); chk("ex24-indep-hi", dd.mean() + hi, 3.24, 0.005)
chk("ex24-s1", bf.std(ddof=1), 1.95, 0.01)
ph = 36 / 400; se = np.sqrt(ph * (1 - ph) / 400)
chk("ex25-lo", ph - 1.96 * se, 0.062, 0.0005); chk("ex25-hi", ph + 1.96 * se, 0.118, 0.0005)
chk("ex25-n", 1.96 ** 2 / (4 * 0.03 ** 2), 1067.1, 0.1)


def cover(n, p, kind):
    k = np.arange(n + 1); ph = k / n; z = 1.96
    if kind == "wald":
        se = np.sqrt(ph * (1 - ph) / n); lo, hi = ph - z * se, ph + z * se
    else:
        c = (ph + z * z / (2 * n)) / (1 + z * z / n)
        hh = z * np.sqrt(ph * (1 - ph) / n + z * z / (4 * n * n)) / (1 + z * z / n); lo, hi = c - hh, c + hh
    return binom.pmf(k, n, p)[(lo <= p) & (p <= hi)].sum()


chk("ex25-wald400", cover(400, .09, "wald"), 0.939, 0.0005); chk("ex25-wald30", cover(30, .05, "wald"), 0.782, 0.0005)
chk("ex25-wilson400", cover(400, .09, "wilson"), 0.956, 0.0005); chk("ex25-wilson30", cover(30, .05, "wilson"), 0.939, 0.0005)
chk("ex26-low", 48.2 - t.isf(.05, 8) * 3 / 3, 46.34, 0.005); chk("ex26-up2", 48.2 + t.isf(.05, 8), 50.06, 0.005)
chk("ex27", 72 / chi2.isf(.95, 8), 26.35, 0.005)
# 第 3-5 节
chk("ex5-mle", 0.6, 6 / 10, 0)
chk("ex9-ce", -(0.5 * np.log(.5) + .3 * np.log(.3) + .2 * np.log(.2)), 1.030, 0.001)
chk("ex10", 4 / 805, 0.00497, 0.00001)
chk("ex12-corrected-EM theta=1 n=4", quad(lambda x: (5/4)*x*4*x**3, 0, 1)[0], 1, 1e-12)
chk("ex14-ratio", (10 + 2) / 3, 4, 0)
chk("ex16-099n100", 0.99 ** 100, 0.366, 0.001)
for nn in (10,):
    chk("ex14-var-ratio-n10", (1 / (3 * nn)) / (1 / (nn * (nn + 2))), 4.0, 1e-9)
print("MANUAL L5-proofs 无偏性与相合性的证明按讲义手工核对")
sys.exit(bool(failures))
