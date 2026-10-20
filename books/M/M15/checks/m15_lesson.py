"""独立核对 lesson.md 中例 1--14 的数值与结论。"""
import math
import numpy as np


def report(k, ok):
    print(f"{'PASS' if ok else 'FAIL'} 例{k}")


# 例 1
report(1, abs(0.9 ** 2 - 0.81) < 1e-12 and abs(0.9 ** 3 - 0.729) < 1e-12)

# 例 2
A = np.array([[1 - 0.45, -0.45, 0], [-0.45, 1, -0.45], [0, -0.45, 1]], dtype=float)
b = np.array([0, 0, 0.5])
v = np.linalg.solve(A, b)
report(2, np.allclose(v, [0.4288, 0.5241, 0.7358], atol=5e-4))

# 例 3
q = [1, 0.9 * v[1], 0.9 * v[2], 0.9 * v[0]]
report(3, abs(q[0] - 1) < 1e-12 and abs(q[1] - 0.4717) < 5e-4
       and abs(q[2] - 0.6622) < 5e-4 and abs(q[3] - 0.3859) < 5e-4)

# 例 4
V = np.zeros(3)
for _ in range(4):
    V = np.array([0.9 * max(V[0], V[1]), 0.9 * max(V[0], V[2]), max(1, 0.9 * V[1])])
report(4, np.allclose(V, [0.81, 0.9, 1.0]))

# 例 5
q3 = 0.5
q2 = 0.5 * (0.9 * q3)
q3 = q3 + 0.5 * (1 - q3)
q1 = 0.5 * (0.9 * q2)
report(5, abs(q2 - 0.225) < 1e-12 and abs(q3 - 0.75) < 1e-12 and abs(q1 - 0.10125) < 1e-12)

# 例 6
grad6 = 0.3 * 0.5 + 0.2 * (-0.5)
report(6, abs(grad6 - 0.05) < 1e-12)

# 例 7
z = np.array([2.0, 1.0, 0.0])
p = np.exp(z) / np.exp(z).sum()
z_new = z + np.array([-p[0], -p[1], 1 - p[2]])
p_new = np.exp(z_new) / np.exp(z_new).sum()
report(7, abs(p[2] - 0.09) < 5e-4 and abs(p_new[2] - 0.2953) < 5e-4)

# 例 8
var_before = 0.125 - 0.05 ** 2
var_after = 0.0625 - 0.05 ** 2
report(8, abs(var_before - 0.1225) < 1e-12 and abs(var_after - 0.06) < 1e-12)

# 例 9
std9 = math.sqrt((0.75 ** 2 + 3 * 0.25 ** 2) / 4)
w9 = [(1 - 0.25) / std9] + [(0 - 0.25) / std9] * 3
report(9, abs(std9 - 0.4330127019) < 1e-9 and abs(w9[0] - 1.7320508076) < 1e-9
       and abs(w9[1] + 0.5773502692) < 1e-9)

# 例 10
rows10 = [(2, 1.1, 2.2, 2.2, 2.2), (2, 1.5, 3.0, 2.4, 2.4),
          (-2, 0.7, -1.4, -1.6, -1.6), (-2, 1.5, -3.0, -2.4, -3.0)]
ok10 = True
for _, _, raw, clipped, expected in rows10:
    ok10 &= abs(min(raw, clipped) - expected) < 1e-12
report(10, ok10)

# 例 11
report(11, abs(1 / (1 + math.exp(-1)) - 0.7311) < 5e-5
       and abs(math.log(0.7 / 0.3) - 0.8473) < 5e-5)

# 例 12
theta12 = np.array([0.5, -0.5])
loss12 = -math.log(1 / (1 + math.exp(-1)))
report(12, np.allclose(theta12, [0.5, -0.5]) and abs(loss12 - 0.3133) < 5e-5)

# 例 13
pa = math.exp(2) / (math.exp(2) + 1)
pa_ref = 0.2 * math.exp(2) / (0.2 * math.exp(2) + 0.8)
report(13, abs(pa - 0.8808) < 5e-5 and abs(pa_ref - 0.6488) < 5e-5)

# 例 14
loss14_0 = math.log(2)
delta14 = 0.5 * (0.4 - (-0.2))
sig14 = 1 / (1 + math.exp(-delta14))
loss14_1 = -math.log(sig14)
weight14 = 0.5 * (1 - sig14)
report(14, abs(loss14_0 - 0.6931) < 5e-5 and abs(delta14 - 0.3) < 1e-12
       and abs(loss14_1 - 0.5544) < 5e-5 and abs(weight14 - 0.2128) < 5e-5)

# 编辑稿新增的随堂小题与回扣
V2 = np.array([0.0, 0.0, 0.0])
for _ in range(5):
    V2 = np.array([0.9 * max(V2[0], V2[1]), 0.9 * max(V2[0], V2[2]), max(2, 0.9 * V2[1])])
report("4小题", np.allclose(V2, [1.62, 1.8, 2.0]))
report("5小题", abs(0.225 + 0.5 * (0 + 0.9 * 0.75 - 0.225) - 0.45) < 1e-12)
report("6小题", abs(0.5 * (0.8 - (0.5 * 0.8 + 0.5 * 0.2)) - 0.15) < 1e-12)
vals = [(1 - 0.6) * 0.5, (0 - 0.6) * 0.5, (1 - 0.6) * -0.5, (0 - 0.6) * -0.5]
pr = [0.3, 0.2, 0.2, 0.3]
m8 = sum(a * b for a, b in zip(vals, pr))
s8 = sum(a * a * b for a, b in zip(vals, pr))
report("8小题", abs(m8 - 0.05) < 1e-12 and abs(s8 - 0.065) < 1e-12 and abs(s8 - m8 ** 2 - 0.0625) < 1e-12)
report("11小题", abs(math.log(9) - 2.197) < 1e-3)
report("13小题", abs(math.e / (math.e + 1) - 0.7311) < 5e-5)
report("回到开头", abs(1 / (1 + math.exp(-math.log(7 / 3) / 0.5)) - 0.8448) < 5e-5)
report("基线依赖动作反例", abs(0.5 * (1 - 0.5) - 0.25) < 1e-12)
