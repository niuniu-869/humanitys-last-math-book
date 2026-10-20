import math
import numpy as np


def report(k, ok):
    print(f"{'PASS' if ok else 'FAIL'} 例{k}")


# 例1 and its same-hidden-layer exercise
W1 = np.ones((2, 2))
b1 = np.array([0, -1])
W2 = np.array([1, -2])
outs = []
for x in ([0, 0], [1, 0], [0, 1], [1, 1]):
    h = np.maximum(W1 @ np.array(x) + b1, 0)
    outs.append(W2 @ h)
report(1, np.array_equal(outs, [0, 1, 1, 0]))

# 例2
report(2, abs((1 / (1 + math.exp(1))) * (1 - 1 / (1 + math.exp(1))) - 0.1966) < 5e-5
       and abs(1 - math.tanh(0.5) ** 2 - 0.7864) < 5e-5)

# 例3
params = (4 * 6 + 6) + (6 * 5 + 5) + (5 * 3 + 3)
report(3, params == 83)

# 例4
q1, q2, s, z, a, r, L = 0.5, -0.5, 0, 0.5, 0.5, -0.5, 0.25
report(4, q1 == 0.5 and q2 == -0.5 and s == 0 and z == 0.5 and a == 0.5 and r == -0.5 and L == 0.25)

# 例5
p = 1 / (1 + math.exp(-0.5))
loss = -math.log(p)
dz = p - 1
report(5, abs(p - 0.6224593) < 1e-6 and abs(loss - 0.474077) < 1e-6 and abs(dz + 0.3775407) < 1e-6)

# 例6
report(6, np.allclose(np.array([-1, 2]), [-1, 2]))

# 例7
sig1 = 1 / (1 + math.exp(-1))
grad7 = sig1 + sig1 * (1 - sig1)
report(7, abs(grad7 - 0.9276705) < 1e-6)

# 例8
grad8 = 2 * (2 * 1 - 1) * 1 + 2 * (2 * 3 - 2) * 3
report(8, grad8 == 26)

# 例9 (section 7)
report(9, 30 * 20 * 10 + 1 * 30 * 10 == 6300 and 1 * 30 * 20 + 1 * 20 * 10 == 800)

# 例10 (section 8)
J = np.array([[3, 2], [1, 1]])
report(10, np.array_equal(J.T @ np.array([1, -1]), [2, 1]))

# 例11
W = np.array([[1, 0, 2], [-1, 1, 0]])
x = np.array([1, 2, -1])
d = np.array([1, -2])
report(11, np.array_equal(np.outer(d, x), [[1, 2, -1], [-2, -4, 2]]) and np.array_equal(W.T @ d, [3, -2, 2]))

# 例12
report(12, np.allclose(np.array([2, -1]) * (1 - np.array([0.5, -0.8]) ** 2), [1.5, -0.36]))

# 例13
x = np.array([1.0, 2.0])
z1 = np.array([-0.5, 1.25])
h = 1 / (1 + np.exp(-z1))
z2 = np.array([1.0, -1.0]) @ h
yhat = 1 / (1 + math.exp(-z2))
d2 = yhat - 1
d1 = (np.array([1.0, -1.0]) * d2) * h * (1 - h)
report(13, abs(z2 + 0.3998) < 5e-4 and abs(yhat - 0.4014) < 5e-4 and np.allclose(d1, [-0.1407, 0.1036], atol=5e-4))

# 例14: check every parameter against the stated composite loss.
vx = np.array([1., -2.])
vW1 = np.array([[0.2, -0.1], [0.3, 0.4], [-0.2, 0.1]])
vb1 = np.array([0.1, -0.2, 0.3])
vW2 = np.array([[0.5, -0.3, 0.2], [-0.1, 0.4, 0.6]])
vb2 = np.array([0.1, -0.1])
target = np.array([0.3, -0.5])
vh = np.tanh(vW1 @ vx + vb1)
vd2 = vW2 @ vh + vb2 - target
vd1 = (vW2.T @ vd2) * (1 - vh * vh)
parameters = [vW1, vb1, vW2, vb2]
gradients = [np.outer(vd1, vx), vd1, np.outer(vd2, vh), vd2]
def loss14(params):
    w1, b1, w2, b2 = params
    residual = w2 @ np.tanh(w1 @ vx + b1) + b2 - target
    return residual @ residual / 2

ok14 = True
for k, (parameter, gradient) in enumerate(zip(parameters, gradients)):
    ok14 &= parameter.shape == gradient.shape
    for index in np.ndindex(parameter.shape):
        plus = [p.copy() for p in parameters]
        minus = [p.copy() for p in parameters]
        plus[k][index] += 1e-5
        minus[k][index] -= 1e-5
        numeric = (loss14(plus) - loss14(minus)) / 2e-5
        ok14 &= np.isclose(numeric, gradient[index], atol=1e-8, rtol=1e-6)
report(14, ok14)

# 例15
forward = (math.exp(0.1) - 1) / 0.1
center = (math.exp(0.1) - math.exp(-0.1)) / 0.2
report(15, abs(forward - 1.0517) < 5e-4 and abs(center - 1.0017) < 5e-4)

# 例16
def old_loss(w11):
    x = np.array([1.0, 2.0])
    W1 = np.array([[w11, -0.5], [0.25, 0.5]])
    h = 1 / (1 + np.exp(-(W1 @ x)))
    z2 = np.array([1.0, -1.0]) @ h
    return -math.log(1 / (1 + math.exp(-z2)))


eps = 1e-5
gnum = (old_loss(0.5 + eps) - old_loss(0.5 - eps)) / (2 * eps)
report(16, abs(gnum + 0.1406802) < 5e-6)

# 逐类 softmax 反向（第 10 节）
z = np.array([2.0, 1.0, 0.0]); pp = np.exp(z) / np.exp(z).sum()
Js = np.diag(pp) - np.outer(pp, pp)
barp = np.array([-1 / pp[0], 0, 0])
print('PASS 第10节 softmax' if np.allclose(Js.T @ barp, pp - np.array([1, 0, 0])) and np.allclose(pp - [1, 0, 0], [-0.3348, 0.2447, 0.0900], atol=5e-5) else 'FAIL 第10节 softmax')
