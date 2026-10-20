import math
import numpy as np


def softmax(z, t=1.0):
    z = np.asarray(z, dtype=float) / t
    z -= z.max()
    e = np.exp(z)
    return e / e.sum()


def check(name, condition):
    print(("PASS " if condition else "FAIL ") + name)


# 例 1：从甲开始，贪心在甲、乙之间循环。
rows = {
    "甲": {"甲": 0.1, "乙": 0.6, "丙": 0.3},
    "乙": {"甲": 0.5, "乙": 0.1, "丙": 0.4},
    "丙": {"甲": 0.7, "乙": 0.2, "丙": 0.1},
}
state = "甲"
path = []
for _ in range(4):
    path.append(state)
    state = max(rows[state], key=rows[state].get)
check("例1", path == ["甲", "乙", "甲", "乙"])

# 例 2：累积概率抽样。
p2 = np.array([0.6652, 0.2447, 0.0900])
c2 = np.cumsum(p2)
draw2 = [int(np.searchsorted(c2, u, side="right")) + 1 for u in (0.70, 0.30, 0.95)]
draw2a = int(np.searchsorted(c2, 0.66, side="right")) + 1
draw2b = int(np.searchsorted(c2, 0.67, side="right")) + 1
check("例2", draw2 == [2, 1, 3] and draw2a == 1 and draw2b == 2)

# 例 3：z=(2,1,0)，T=0.5 和 T=2。
p3 = softmax([2, 1, 0], 0.5)
p3b = softmax([2, 1, 0], 2)
check("例3", math.isclose(p3[0], 0.8668133322, abs_tol=1e-9) and math.isclose(p3b[0], 0.5064803911, abs_tol=1e-9))

# 例 4：两个六词分布做 top-3。
p41 = np.array([0.92, 0.03, 0.02, 0.01, 0.01, 0.01])
p42 = np.array([0.25, 0.25, 0.20, 0.15, 0.10, 0.05])
q41 = p41[:3] / p41[:3].sum()
q42 = p42[:3] / p42[:3].sum()
check("例4", np.allclose(q41, [0.9484536082, 0.0309278351, 0.0206185567]) and np.allclose(q42, [5 / 14, 5 / 14, 2 / 7]))

# 例 5：top-p=0.9 的核大小与归一化。
c51 = np.cumsum(p41)
c52 = np.cumsum(p42)
m51 = int(np.searchsorted(c51, 0.9, side="left")) + 1
m52 = int(np.searchsorted(c52, 0.9, side="left")) + 1
q52 = p42[:m52] / p42[:m52].sum()
q54 = np.array([0.6652, 0.2447]) / (0.6652 + 0.2447)
check("例5", m51 == 1 and m52 == 5 and np.allclose(q52, [0.2631578947, 0.2631578947, 0.2105263158, 0.1578947368, 0.1052631579]) and np.allclose(q54, [0.7310693477, 0.2689306523]))

# 例 6：先温度再 top-p 与反过来的顺序不同。
p61 = softmax([2, 1, 0], 2)
m61 = int(np.searchsorted(np.cumsum(p61), 0.85, side="left")) + 1
p62 = softmax([2, 1], 2)
check("例6", m61 == 3 and np.allclose(p62, [0.6224593312, 0.3775406688]))

# 例 7：整句最优为 be，概率 0.36。
paths7 = {"ac": 0.6 * 0.5, "ad": 0.6 * 0.5, "be": 0.4 * 0.9, "bf": 0.4 * 0.1}
check("例7", max(paths7, key=paths7.get) == "be" and math.isclose(paths7["be"], 0.36))

# 例 8：无缓存为三角和，有缓存每步一个；缓存 7B 一个词元为 524288 字节。
uncached = 1000 * 1001 // 2
cached = 1000
one_token = 2 * 32 * 4096 * 2
check("例8", uncached == 500500 and cached == 1000 and one_token == 524288)
