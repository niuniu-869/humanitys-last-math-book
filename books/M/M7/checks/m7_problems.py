import math
import numpy as np


def report(pid, ok):
    print(f"{'PASS' if ok else 'FAIL'} {pid}")


def numerical_gradient(fn, value, eps=1e-5):
    value = np.asarray(value, dtype=float)
    result = np.zeros_like(value)
    for index in np.ndindex(value.shape):
        plus, minus = value.copy(), value.copy()
        plus[index] += eps
        minus[index] -= eps
        result[index] = (fn(plus) - fn(minus)) / (2 * eps)
    return result


# M7-01
x = np.array([1.0, -1.0])
W1 = np.array([[1.0, -1.0], [2.0, 1.0]])
b1 = np.array([0.0, -1.0])
z1 = W1 @ x + b1
h = np.maximum(z1, 0)
report('M7-01', np.allclose(z1, [2, 0]) and np.allclose(h, [2, 0]) and np.isclose(np.array([1, 2]) @ h - 1, 1))

# M7-02, every option is checked
sig = 1 / (1 + math.exp(-0.5))
truth = [sig * (1 - sig), 1 - math.tanh(0.5) ** 2, 1]
options = [[0.6225, 0.7864, 0], [0.2350, 0.7864, 1], [0.2350, 0.2136, 1], [0.3775, 0.7864, 1]]
flags = [np.allclose(o, truth, atol=5e-4) for o in options]
report('M7-02', flags == [False, True, False, False])

# M7-03
params = 4 * 5 + 4 + 3 * 4 + 3
report('M7-03', params == 39)

# M7-04: the mask imposes exactly one nonzero constraint.
mask = (np.array([-1, 0, 2]) > 0).astype(int)
target = np.array([0, 0, 3])
flags = [np.linalg.matrix_rank(np.diag(mask)) == 3,
         np.array_equal(mask, [0, 0, 1]) and target[2] == 3,
         np.array_equal(mask * [1, 0, 7], target),
         not np.array_equal(mask * target, target)]
report('M7-04', flags == [False, True, False, False])

# M7-05
p = 1 / (1 + math.exp(-2))
du = p + 2 * p * (1 - p) + 2
def loss05(v):
    u = 2 * v[0] + v[1]
    return u / (1 + np.exp(-u)) + (u - 1) ** 2
report('M7-05', np.allclose([2 * du, du], [6.1816, 3.0908], atol=5e-5, rtol=0)
       and np.allclose(numerical_gradient(loss05, [1, 0]), [2 * du, du]))

# M7-06
point = np.array([2.0, -1.0])
J = np.array([[2 * point[0], 1], [point[1], point[0]], [1, -1]])
up = np.array([1, 2, -1])
gx = J.T @ up
def loss06(v):
    return up @ np.array([v[0] ** 2 + v[1], v[0] * v[1], v[0] - v[1]])
report('M7-06', J.shape == (3, 2) and np.array_equal(gx, [1, 6])
       and np.allclose(numerical_gradient(loss06, point), gx))

# M7-07: a local scalar loss with the specified per-sample derivatives.
X = np.array([[1., -1.], [2., 1.]])
W = np.array([[1., 2.], [-1., 0.]])
G = np.array([[2., -1.], [-2., 3.]])
gX, gW, gb = G @ W / 2, G.T @ X / 2, G.sum(axis=0) / 2
report('M7-07', np.array_equal(gX, [[1.5, 2], [-2.5, -2]])
       and np.array_equal(gW, [[-1, -2], [2.5, 2]]) and np.array_equal(gb, [0, 1])
       and np.allclose(numerical_gradient(lambda v: np.sum(G * (v @ W.T)) / 2, X), gX)
       and np.allclose(numerical_gradient(lambda v: np.sum(G * (X @ v.T)) / 2, W), gW)
       and np.allclose(numerical_gradient(lambda v: np.sum(G * (X @ W.T + v)) / 2, [0, 0]), gb))

# M7-08 is a proof.
print('MANUAL M7-08')

# M7-09, every option is checked against the full composite function.
mix = np.array([[1., 1.], [0., 1.]])
up = np.array([1., 2.])
actual = numerical_gradient(lambda z: up @ np.tanh(mix @ z), [0, 0])
flags = [np.allclose(actual, v) for v in ([1, 2], [3, 2], [1, 3], [0, 0])]
report('M7-09', flags == [False, False, True, False])

# M7-10
s = math.tanh(1)
expected = [s * s + s * (1 - s * s), s * (1 - s * s), s]
def loss10(v):
    w, b, c = v
    return 0.5 * (w * np.tanh(w + b) + c) ** 2
separate = numerical_gradient(lambda v: 0.5 * (v[1] * np.tanh(v[0])) ** 2, [1, 1])
report('M7-10', np.allclose(numerical_gradient(loss10, [1, 0, 0]), expected)
       and np.allclose(separate, [s * (1 - s * s), s * s])
       and np.isclose(sum(separate), expected[0]))

# M7-11
x = np.array([1.0, -1.0])
W1 = np.array([[1.0, 0.0], [-1.0, 1.0]])
b1 = np.zeros(2)
W2 = np.array([[1.0, 2.0], [0.0, 1.0]])
b2 = np.array([0.0, 1.0])
W3 = np.array([2.0, -1.0])
z1 = W1 @ x + b1
a1 = np.maximum(z1, 0)
z2 = W2 @ a1 + b2
a2 = np.maximum(z2, 0)
z3 = W3 @ a2
d3 = z3 - 2
gW3 = np.outer([d3], a2)
d2 = (W3 * d3) * (z2 > 0)
gW2 = np.outer(d2, a1)
d1 = (W2.T @ d2) * (z1 > 0)
gW1 = np.outer(d1, x)
report('M7-11', np.allclose(z1, [1, -2]) and np.allclose(z2, [1, 1]) and np.allclose(z3, 1)
       and np.array_equal(gW3[0], [-1, -1]) and np.array_equal(gW2, [[-2, 0], [1, 0]])
       and np.array_equal(gW1, [[-2, 2], [0, 0]]) and d3 == -1
       and np.array_equal(d2, [-2, 1]) and np.array_equal(d1, [-2, 0]))

# M7-12
def loss(w):
    h = 1 / (1 + np.exp(-w * np.array([1., 2.])))
    return np.sum((2 * h) ** 2) / 4


x = np.array([1., 2.])
h = 1 / (1 + np.exp(-0.2 * x))
g = np.sum(2 * h * h * (1 - h) * x)
eps = 1e-5
gnum = (loss(0.2 + eps) - loss(0.2 - eps)) / (2 * eps)
rel = abs(g - gnum) / max(abs(g), abs(gnum))
report('M7-12', abs(g - 0.84755063) < 5e-9 and rel < 1e-8)

# M7-13
p = 1 / (1 + math.exp(-0.5))
w, b = 0.3 - 0.2 * (p - 1) * 2, -0.1 - 0.2 * (p - 1)
report('M7-13', abs(w - 0.4510163) < 1e-6 and abs(b - (-0.0244919)) < 1e-6)

# M7-14
z = np.array([1.0, 0.0, -1.0])
p = np.exp(z) / np.exp(z).sum()
delta = p - np.array([0.0, 1.0, 0.0])
hvec = np.array([1.0, 2.0])
gW = np.outer(delta, hvec)
report('M7-14', gW.shape == (3, 2) and gW.size + delta.size == 9
       and np.allclose(p, [0.66524096, 0.24472847, 0.09003057])
       and np.allclose(gW, [[0.6652, 1.3305], [-0.7553, -1.5105], [0.0900, 0.1801]], atol=5e-5, rtol=0))

# M7-15
W1 = np.array([[1, 2], [0, 1]])
b1 = np.array([1, 0])
W2 = np.array([2, -1])
combined_W = 2 * W2 @ W1
combined_b = 2 * (W2 @ b1 + 3) - 1
x = np.array([1, -1])
points = np.array([-2, -1, 0])
values = 2 * np.maximum(points + 1, 0) - 1
report('M7-15', np.array_equal(combined_W, [4, 6]) and combined_b == 9
       and combined_W @ x + combined_b == 7
       and 2 * (W2 @ (W1 @ x + b1) + 3) - 1 == 7
       and np.array_equal(values, [-1, -1, 1])
       and values[1] - values[0] != values[2] - values[1])
