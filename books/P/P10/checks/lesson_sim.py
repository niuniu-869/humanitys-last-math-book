"""P.10 讲义里模拟结果表的数字（固定种子），并与精确值比对。"""
import numpy as np
from scipy import stats
rng = np.random.default_rng(2026)
R = 100000
# 10.3: 样本量 5 的 N(0,1) 样本，S^2 用 n-1 与 n 做分母
X = rng.standard_normal((R, 5))
s2 = X.var(axis=1, ddof=1); b2 = X.var(axis=1, ddof=0)
print(f"INFO 分母n-1 均值 {s2.mean():.4f}；分母n 均值 {b2.mean():.4f}")
print("PASS" if abs(s2.mean() - 1) < 0.02 and abs(b2.mean() - 0.8) < 0.02 else "FAIL", "sim-103")
# 10.5: (n-1)S^2/sigma^2 ~ chi2(4)，与 Xbar 的相关
V = 4 * s2
xb = X.mean(axis=1)
c = stats.chi2.ppf(0.95, 4)
print(f"INFO V均值 {V.mean():.4f} 方差 {V.var():.4f} P(V>{c:.3f})={np.mean(V>c):.4f} corr(Xbar,S2)={np.corrcoef(xb,s2)[0,1]:.4f} corr(|Xbar|,S2)={np.corrcoef(np.abs(xb),s2)[0,1]:.4f}")
print("PASS" if abs(V.mean()-4)<0.05 and abs(V.var()-8)<0.2 and abs(np.mean(V>c)-0.05)<0.004 and abs(np.corrcoef(xb,s2)[0,1])<0.02 else "FAIL", "sim-105")
# 10.6: T = Xbar/(S/sqrt5) 的尾部概率
T = xb / (np.sqrt(s2) / np.sqrt(5))
Z = xb * np.sqrt(5)
for name, thr in (("1.96", 1.96), ("2.776", 2.776)):
    sim_t = np.mean(np.abs(T) > thr); sim_z = np.mean(np.abs(Z) > thr)
    ex_t = 2 * stats.t.sf(thr, 4); ex_z = 2 * stats.norm.sf(thr)
    print(f"INFO |.|>{name}: 用S {sim_t:.4f}（t(4)精确 {ex_t:.4f}） 用sigma {sim_z:.4f}（精确 {ex_z:.4f}）")
    print("PASS" if abs(sim_t-ex_t)<0.004 and abs(sim_z-ex_z)<0.004 else "FAIL", f"sim-106-{name}")
