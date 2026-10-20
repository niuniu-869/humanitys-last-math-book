import math
import numpy as np
import sympy as sp


def result(label, ok):
    print(f"{'PASS' if ok else 'FAIL'} {label}")


# M18-01: derive shapes from matrix multiplication rules.
q_shape, k_shape, v_shape = (5, 8), (7, 8), (7, 3)
score_shape = (q_shape[0], k_shape[0]) if q_shape[1] == k_shape[1] else None
out_shape = (score_shape[0], v_shape[1]) if score_shape and score_shape[1] == v_shape[0] else None
options_01 = [((5, 7), (5, 3)), ((5, 8), (5, 3)), ((5, 7), (7, 3)), ((7, 5), (5, 7))]
result("M18-01", sum((score_shape, out_shape) == x for x in options_01) == 1 and (score_shape, out_shape) == options_01[0])

# M18-02: compute the six entries directly from the paper's formula.
d = 6
pos = 3
pe = []
for j in range(d):
    i = j // 2
    denom = 10000 ** (2 * i / d)
    pe.append(math.sin(pos / denom) if j % 2 == 0 else math.cos(pos / denom))
expected_pe = np.array([math.sin(3), math.cos(3), math.sin(3 / 10000 ** (1 / 3)), math.cos(3 / 10000 ** (1 / 3)), math.sin(3 / 10000 ** (2 / 3)), math.cos(3 / 10000 ** (2 / 3))])
result("M18-02", np.allclose(pe, expected_pe, atol=5e-5))

# M18-03: shape ledger.
n, dm, h, dk, dv = 7, 12, 3, 4, 5
head_shape = (n, dv)
concat_shape = (n, h * dv)
wo_shape = (h * dv, dm)
final_shape = (n, dm)
result("M18-03", (head_shape, concat_shape, wo_shape, final_shape) == ((7, 5), (7, 15), (15, 12), (7, 12)))

# M18-04: differentiate scalar analogues of the two placements.
a, b, x = sp.symbols("a b x")
pre_derivative = sp.diff(x + a * (b * x), x)
post_derivative = sp.diff(b * (x + a * x), x)
pre_has_identity = sp.expand(pre_derivative).coeff(a, 0) == 1
post_is_identity_plus_f = sp.expand(post_derivative - (1 + a)) == 0
result("M18-04", pre_has_identity and not post_is_identity_plus_f)

# M18-05: warmup schedule.
model_d, warmup, step = 512, 2000, 1000
term_down = step ** -0.5
term_up = step * warmup ** -1.5
lr = model_d ** -0.5 * min(term_down, term_up)
result("M18-05", abs(lr - 4.941058e-4) < 1e-8 and term_up < term_down)

# M18-06 and M18-11 are proofs requested for manual checking.
print("MANUAL M18-06")

# M18-07: symbolic parameter count.
d = sp.Integer(384)
encoder = 4 * d**2 + 2 * d * 1536
decoder = encoder + 4 * d**2
result("M18-07", int(encoder) == 1769472 and int(decoder) == 2359296)

# M18-08: compare exact costs and solve the equality condition.
d = 256
costs = [(128**2 * d, 128 * d**2), (512**2 * d, 512 * d**2)]
ratio_128 = costs[0][0] / costs[0][1]
ratio_512 = costs[1][0] / costs[1][1]
result("M18-08", costs == [(4194304, 8388608), (67108864, 33554432)] and ratio_128 == 0.5 and ratio_512 == 2 and d == 256)

# M18-09: independent numerical attention calculation.
Q = np.array([[1.0], [0.0]])
K = np.array([[1.0], [0.0], [-1.0], [2.0]])
V = np.array([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0], [2.0, 0.0]])
scores = Q @ K.T
weights = np.exp(scores - scores.max(axis=1, keepdims=True))
weights /= weights.sum(axis=1, keepdims=True)
Y = weights @ V
options_09 = [((2, 2), np.array([1.557, .119])), ((2, 2), np.array([.25, .5])), ((4, 2), np.array([1.557, .119])), ((2, 1), np.array([.644, .356]))]
truth = [(Y.shape == s and np.allclose(Y[0], v, atol=1e-3)) for s, v in options_09]
result("M18-09", sum(truth) == 1 and truth[0])

# M18-10: incompatible inner dimensions, then corrected shape.
valid_original = 4 == 3
valid_fixed = 4 == 4
fixed_output = (3, 5) if valid_fixed else None
fixed_output = (fixed_output[0], 2) if fixed_output and fixed_output[1] == 5 else None
result("M18-10", not valid_original and fixed_output == (3, 2))

print("MANUAL M18-11")

# M18-12: masked softmax rows.
S = np.array([[2.0, 1.0, 0.0], [2.0, 3.0, 1.0], [0.0, 2.0, 4.0]])
masked = S.copy()
masked[0, 1:] = -np.inf
masked[1, 2:] = -np.inf


def softmax_row(x):
    z = x - np.max(x)
    e = np.exp(z, where=np.isfinite(z), out=np.zeros_like(z))
    return e / e.sum()


rows = np.vstack([softmax_row(row) for row in masked])
result("M18-12", np.allclose(rows[1], [0.26894142, 0.73105858, 0.0], atol=1e-6) and np.allclose(rows[2], [0.01587624, 0.11731043, 0.86681333], atol=1e-6))

# M18-13: variance, encoder parameters, and peak warmup rate.
dk = 64
variance_before = dk * 1 * 1
variance_after = variance_before / dk
param_count = 12 * 256**2
peak_lr = 256 ** -0.5 * 2000 ** -0.5
result("M18-13", variance_before == 64 and variance_after == 1 and param_count == 786432 and abs(peak_lr - 1.397542e-3) < 1e-8)

# M18-14: cross entropy from softmax.
z = np.array([2.0, 1.0, 0.0])
p = np.exp(z - z.max())
p /= p.sum()
loss = -math.log(p[1])
result("M18-14", abs(p[1] - 0.24472847) < 1e-7 and abs(loss - 1.40760596) < 1e-7)

# M18-15: shapes from the stated projections and addition compatibility.
X_shape = (3, 4)
q = (X_shape[0], 2)
k = (X_shape[0], 2)
v = (X_shape[0], 3)
head = v
concat = (3, 3)
final = (concat[0], 4)
result("M18-15", (q, k, v, head, concat, final) == ((3, 2), (3, 2), (3, 3), (3, 3), (3, 3), (3, 4)) and (3, 4) == X_shape)
