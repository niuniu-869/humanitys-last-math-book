"""编辑稿新增的模拟：方差不等且小组方差大时 F 检验的实际误判率（固定种子）。"""
import numpy as np
from scipy import stats

rng = np.random.default_rng(1307)
T = 100000
sizes, sds = (4, 20, 20), (3, 1, 1)
g = [rng.normal(0, s, (T, n)) for n, s in zip(sizes, sds)]
allv = np.concatenate(g, axis=1)
gm = allv.mean(1, keepdims=True)
ssb = sum(x.shape[1] * (x.mean(1) - gm[:, 0]) ** 2 for x in g)
ssw = sum(((x - x.mean(1, keepdims=True)) ** 2).sum(1) for x in g)
k, n = 3, sum(sizes)
rate = ((ssb / (k - 1)) / (ssw / (n - k)) > stats.f.ppf(.95, k - 1, n - k)).mean()
print("PASS 方差不等小组方差大 误判率约31%" if 0.30 < rate < 0.33 else f"FAIL 方差不等 {rate}")
# 新增随堂小题的答案
d = np.array([[5, 6, 7], [8, 8, 11], [11, 13, 12.]])
gm = d.mean()
sr, sc = 3 * ((d.mean(1) - gm) ** 2).sum(), 3 * ((d.mean(0) - gm) ** 2).sum()
se = ((d - gm) ** 2).sum() - sr - sc
print("PASS 双因素小题" if (sr, sc, se) == (54, 6, 4) else "FAIL 双因素小题")
x, y = np.arange(1, 6.), np.array([5, 3, 2, 3, 5.])
print("PASS U形小题 斜率0" if abs(np.polyfit(x, y, 1)[0]) < 1e-12 else "FAIL U形小题")
x = np.arange(4.); y = np.array([1, 3, 4, 8.])
b1, b0 = np.polyfit(x, y, 1)
s2 = ((y - b0 - b1 * x) ** 2).sum() / 2
h = .25
t = stats.t.ppf(.975, 2)
ok = abs(b0 + b1 * 1.5 - 4) < 1e-9 and abs(t * s2**.5 * h**.5 - 2.04) < .01 and abs(t * s2**.5 * (1 + h)**.5 - 4.56) < .01
print("PASS 预测小题" if ok else "FAIL 预测小题")
X = np.column_stack([np.ones(6), [-1, -1, 0, 0, 1, 1], [-1, 1, -1, 1, -1, 1]])
yy = np.array([2, 4, 3, 7, 7, 9.])
bb = np.linalg.lstsq(X, yy, rcond=None)[0]
print("PASS 多元小题" if np.allclose(bb, [16 / 3, 5 / 2, 4 / 3]) and abs(((yy - X @ bb) ** 2).sum() - 5 / 3) < 1e-9 else "FAIL 多元小题")
