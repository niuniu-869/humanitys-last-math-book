import itertools
import math

import numpy as np


def close(a, b, tol=1e-9):
    return np.allclose(np.asarray(a, dtype=float), np.asarray(b, dtype=float), atol=tol, rtol=tol)


def ok(pid, condition):
    print(f"{'PASS' if condition else 'FAIL'} {pid}")


# M8-01
r = 0.4
value = r ** 6
ok("M8-01", math.isclose(value, 0.004096) and value < 1
   and not math.isclose(value, 2.4) and not math.isclose(value, 6 ** 0.4))

# M8-02
sd = 1 / 8
n = 128
variance_factor = n * sd**2
stable_sd = 1 / math.sqrt(n)
ok("M8-02", math.isclose(variance_factor, 2)
   and math.isclose(variance_factor**4, 16)
   and math.isclose(64 * 2, 128)
   and math.isclose(stable_sd, 1 / math.sqrt(128)))

# M8-03
x = np.array([0.0, 2.0, 4.0, 6.0])
mu = x.mean()
var = ((x - mu) ** 2).mean()
bn = 0.5 * (x - mu) / math.sqrt(var) - 1
target = np.array([-1 - 3 / (2 * math.sqrt(5)), -1 - 1 / (2 * math.sqrt(5)),
                   -1 + 1 / (2 * math.sqrt(5)), -1 + 3 / (2 * math.sqrt(5))])
ok("M8-03", math.isclose(mu, 3) and math.isclose(var, 5) and close(bn, target))

# M8-04
q = 0.25
ok("M8-04", math.isclose(9 * (1 - q) / q, 27)
   and math.isclose(q, 0.25)
   and {0.0: 1 - q, 3 / q: q} == {0.0: 0.75, 12.0: 0.25})

# M8-05
t = 4.0
ok("M8-05", math.isclose(max(1.0, t), 4)
   and math.isclose(max(2.0, 0.0), 2)
   and math.isclose(2.0 if t > 1 else 0.0, 2))

# M8-06
z_bound = math.log(3 + 2 * math.sqrt(2))
ok("M8-06", math.isclose(math.exp(z_bound), 3 + 2 * math.sqrt(2))
   and math.isclose(4 * math.exp(0) / (1 + math.exp(0))**2, 1)
   and z_bound > 0)

# M8-07
t = -1.0
A = np.diag([t, -0.5])
B = np.array([[0.0, 1.0], [0.0, 0.0]])
P = (np.eye(2) + B) @ (np.eye(2) + A)
ok("M8-07", close(P, [[0, 0.5], [0, 0.5]])
   and math.isclose(np.linalg.det(P), 0)
   and close(P @ np.array([1.0, 0.0]), [0, 0]))

# M8-08
x = np.array([1.0, 2.0, 0.0, 1.0])
M = np.array([[x[0], x[1]], [x[1], x[2]], [x[2], x[3]]])
sol, *_ = np.linalg.lstsq(M[:2], np.array([5.0, 2.0]), rcond=None)
ok("M8-08", close(sol, [1, 2])
   and close(M @ sol, [5, 2, 2])
   and not close(M @ sol, [5, 2, 3]))

# M8-09
k = 5
p = 2
ok("M8-09", 4 * (3 * k * k + 1) == 304
   and ((20 + 2 * p - k) // 2 + 1, (17 + 2 * p - k) // 2 + 1) == (10, 9))

# M8-10
batch = np.array([2.0])
batch_var = ((batch - batch.mean()) ** 2).mean()
ok("M8-10", math.isclose(batch_var, 0))

# M8-11
independent = list(itertools.product([0, 1], repeat=2))
probs = {(a, b): 0.25 for a, b in independent}
vals = {key: 4 * key[0] - 4 * key[1] for key in probs}
mean_ind = sum(probs[key] * vals[key] for key in probs)
var_ind = sum(probs[key] * (vals[key] - mean_ind) ** 2 for key in probs)
loss_ind = sum(probs[key] * (vals[key] - 1) ** 2 for key in probs)
ok("M8-11", math.isclose(var_ind, 8)
   and math.isclose(loss_ind, 9)
   and math.isclose(np.var([0, 0]), 0)
   and math.isclose(1.0, 1))

# M8-12
v = 1 / 5
objective = max(abs(4 * v - 1), abs(6 * v - 1))
ok("M8-12", math.isclose(objective, 0.2)
   and math.isclose(math.sqrt(3 * v), math.sqrt(3 / 5)))
print("MANUAL M8-12")

# M8-13
A = np.array([[0.0, 1.0], [0.0, 0.0]])
B = A.T
left = (np.eye(2) + B) @ (np.eye(2) + A)
right = (np.eye(2) + A) @ (np.eye(2) + B)
ok("M8-13", close(left, [[1, 1], [1, 2]])
   and close(right, [[2, 1], [1, 1]])
   and not close(left @ np.array([1.0, 0.0]), right @ np.array([1.0, 0.0])))
print("MANUAL M8-13")

# M8-14
def expected_loss(w):
    w1, w2 = w
    base = 0.5 * ((w1 + 2 * w2 - 1) ** 2 + (2 * w1 + w2 - 1) ** 2)
    penalty = 2.5 * (w1 * w1 + w2 * w2)
    return base + penalty

w_star = np.array([3 / 14, 3 / 14])
ok("M8-14", math.isclose(expected_loss(w_star), 5 / 14)
   and close([10 * w_star[0] + 4 * w_star[1], 4 * w_star[0] + 10 * w_star[1]], [3, 3]))
print("MANUAL M8-14")

# M8-15
x = np.array([1.0, 2.0, 0.0, 3.0])
k = np.array([2.0, -1.0])
y = np.array([k[0] * x[i] + k[1] * x[i + 1] for i in range(3)])
delta = y - 1
gk = np.array([sum(delta[i] * x[i + j] for i in range(3)) for j in range(2)])
ok("M8-15", close(y, [0, 4, -3]) and close(delta, [-1, 3, -4])
   and close(gk, [5, -14]) and close(k - 0.1 * gk, [1.5, 0.4]))

# M8-16
x = np.array([1.0, 2.0])
w = np.array([1.0, -1.0])
loss = float((w @ x) ** 2 + np.sum((w * x) ** 2))
ok("M8-16", math.isclose(loss, 6) and not math.isclose(x[0] ** 2, x[1] ** 2))

# M8-17
W = np.array([[0.0, 1.0], [-1.0, 0.0]])
dy = np.array([2.0, 1.0])
ok("M8-17", close((np.eye(2) + W).T @ dy, [1, 3])
   and close(W.T @ dy, [-1, 2]))

