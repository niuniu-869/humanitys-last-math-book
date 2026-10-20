import math

import numpy as np


def ok(i, condition):
    print(f"{'PASS' if condition else 'FAIL'} 例{i}")


def sigmoid(z):
    return 1 / (1 + np.exp(-z))


# 例 1：完整的一步训练，检查更新后损失下降。
W1 = np.array([[0.5, -0.5], [0.25, 0.5]], dtype=float)
w2 = np.array([1.0, -1.0])
b2 = 0.0
x = np.array([1.0, 2.0])
h = sigmoid(W1 @ x)
p = float(sigmoid(w2 @ h + b2))
loss0 = -math.log(p)
d2 = p - 1
gw2 = d2 * h
gb2 = d2
d1 = d2 * w2 * h * (1 - h)
gW1 = np.outer(d1, x)
W1n, w2n, b2n = W1 - 0.5 * gW1, w2 - 0.5 * gw2, b2 - 0.5 * gb2
pn = float(sigmoid(w2n @ sigmoid(W1n @ x) + b2n))
ok(1, np.allclose([p, loss0], [0.4014, 0.9129], atol=2e-4) and -math.log(pn) < loss0)

# 例 2：sigmoid 链。
ok(2, math.isclose((1 / 4) ** 5, 0.0009765625)
   and math.isclose((1 / 4) ** 10, 0.00000095367431640625))

# 例 3：对角矩阵的两个方向同时消失和爆炸。
D = np.diag([1.5, 0.5])
out = np.linalg.matrix_power(D, 10) @ np.ones(2)
ok(3, np.allclose(out, [1.5**10, 0.5**10]) and out[0] > 50 and out[1] < 0.001)

# 例 4：方差和标准差的十层倍数。
mult = [256 * s**2 for s in (0.1, 1 / 16, 0.05)]
ok(4, np.allclose(mult, [2.56, 1, 0.64])
   and math.isclose(mult[1] ** 10, 1)
   and math.isclose(math.sqrt(mult[2] ** 10), 0.64**5))

# 例 5：BN 前向。
x = np.array([1.0, 3.0, 5.0, 7.0])
mu, var = x.mean(), ((x - x.mean()) ** 2).mean()
y = 2 * (x - mu) / math.sqrt(var) + 1
target = np.array([-1.68328157, 0.10557281, 1.89442719, 3.68328157])
ok(5, math.isclose(mu, 4) and math.isclose(var, 5) and np.allclose(y, target, atol=1e-6))

# 例 6：滑动平均更新。
mu_run = 0.9 * 0 + 0.1 * 4
var_run = 0.9 * 1 + 0.1 * 5
ok(6, math.isclose(mu_run, 0.4) and math.isclose(var_run, 1.4))

# 例 7：两个残差块的 Jacobian。
J1 = np.array([[0.2, 0], [0.1, -0.1]])
J2 = np.array([[0, 0.3], [0.2, 0]])
ordinary = J2 @ J1
residual = (np.eye(2) + J2) @ (np.eye(2) + J1)
ok(7, np.allclose(ordinary, [[0.03, -0.03], [0.04, 0]])
   and np.allclose(residual, [[1.23, 0.27], [0.34, 0.9]]))

# 例 8：Dropout 前向、反向与期望。
x = np.array([2.0, 4.0, 6.0, 8.0])
m = np.array([1.0, 0.0, 1.0, 0.0])
y = m * x / 0.5
dx = m * np.ones(4) / 0.5
expect_first = 0.5 * (2 / 0.5) + 0.5 * 0
ok(8, np.allclose(y, [4, 0, 12, 0]) and np.allclose(dx, [2, 0, 2, 0])
   and math.isclose(expect_first, 2))

# 例 9：线性模型 Dropout 的期望损失，同时枚举全部掩码复核。
w = np.array([1.0, 2.0, -1.0])
x = np.array([2.0, 1.0, 3.0])
y_true = 0.5
q = 0.8
formula = float((w @ x - y_true) ** 2 + (1 - q) / q * np.sum((w * x) ** 2))
enumerated = 0.0
for bits in __import__("itertools").product([0, 1], repeat=3):
    prob = math.prod(q if bit else 1 - q for bit in bits)
    pred = float(np.sum(w * np.array(bits) * x / q))
    enumerated += prob * (pred - y_true) ** 2
ok(9, math.isclose(formula, 4.5) and math.isclose(enumerated, formula))

# 例 10：一维互相关。
x = np.array([1, 3, 2, 5, 4, 6])
k = np.array([1, 0, -1])
y = np.array([np.dot(k, x[i:i + 3]) for i in range(4)])
ok(10, np.allclose(y, [-1, -2, -2, -1]))

# 例 11：二维边缘核。
img = np.zeros((5, 5))
img[:, :3] = 1
k = np.ones((3, 3))
k[:, 1] = 0
k[:, 2] = -1
y = np.array([[np.sum(img[i:i + 3, j:j + 3] * k) for j in range(3)] for i in range(3)])
ok(11, np.allclose(y, np.array([[0, 3, 3]] * 3)))

# 例 12：一维卷积反向。
x = np.array([1, 2, 0, 3, 1])
k = np.array([2, 1, -1])
delta = np.array([1, -1, 2])
gk = np.array([sum(delta[i] * x[i + j] for i in range(3)) for j in range(3)])
gx = np.array([sum(delta[i] * k[j] for i in range(3) for j in range(3) if i + j == m)
               for m in range(5)])
ok(12, np.allclose(gk, [-1, 8, -1]) and np.allclose(gx, [2, -1, 2, 3, -2]))

# 例 13：卷积输出尺寸。
out0 = (32 - 5) // 1 + 1
out2 = (32 + 4 - 5) // 1 + 1
ok(13, (out0, out2) == (28, 32))

# 例 14：步幅大于 1 时向下取整。
a = (224 + 6 - 7) // 2 + 1
b = (10 - 3) // 2 + 1
ok(14, (a, b) == (112, 4))

# 例 15：多通道卷积的形状和参数。
hout = (227 - 11) // 4 + 1
params = 96 * (3 * 11 * 11 + 1)
fc_params = (3 * 227 * 227) * (96 * 55 * 55)
ok(15, hout == 55 and params == 34944 and fc_params > 4.4e10)

# 例 16：最大池化、平均池化和最大池化反向。
a = np.array([[1, 3, 2, 1], [4, 2, 0, 5], [6, 1, 3, 3], [2, 0, 1, 4]], dtype=float)
blocks = [a[:2, :2], a[:2, 2:], a[2:, :2], a[2:, 2:]]
mx = np.array([[blocks[0].max(), blocks[1].max()], [blocks[2].max(), blocks[3].max()]])
av = np.array([[blocks[0].mean(), blocks[1].mean()], [blocks[2].mean(), blocks[3].mean()]])
grad = np.zeros_like(a)
grad[1, 0], grad[1, 3], grad[2, 0], grad[3, 3] = 1, 2, 3, 4
ok(16, np.allclose(mx, [[4, 5], [6, 4]])
   and np.allclose(av, [[2.5, 2], [2.25, 2.75]])
   and np.allclose(grad, [[0, 0, 0, 0], [1, 0, 0, 2], [3, 0, 0, 0], [0, 0, 0, 4]]))
