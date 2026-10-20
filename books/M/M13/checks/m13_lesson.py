"""Verify the ten numbered examples against their stated data.

Rounded figures use half a unit in the last printed decimal place.
Numerical and symbolic checks are tied to the current lesson text.
"""
from pathlib import Path
import re
import sys

import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
LESSON = (ROOT / "lesson.md").read_text(encoding="utf-8")
EXAMPLES = dict(re.findall(
    r"(?s)\*\*例 (\d+)\*\*(.*?)(?=\*\*例 \d+\*\*|\Z)", LESSON
))
R = sp.Rational
FAILURES = []


def equal(a, b):
    if isinstance(a, sp.MatrixBase):
        return a.shape == b.shape and all(sp.simplify(x-y) == 0 for x, y in zip(a, b))
    return sp.simplify(a-b) == 0


def rounds(actual, stated, decimals):
    return bool(np.allclose(np.asarray(actual, dtype=float),
                            np.asarray(stated, dtype=float), rtol=0,
                            atol=0.5 * 10**(-decimals) + 1e-12))


def check(number, conditions, fragments=(), detail=""):
    missing = [f for f in fragments if f not in EXAMPLES[str(number)]]
    passed = all(bool(c) for c in conditions) and not missing
    print(f"{'PASS' if passed else 'FAIL'} 例{number}" + (f" {detail}" if detail else ""))
    if not passed:
        FAILURES.append(number)
        print(f"  conditions={list(map(bool, conditions))}; missing={missing}")


# 1: derive softmax probabilities, then average the three true-label losses.
z = np.array([2., 1., 0.])
prob = np.exp(z) / np.exp(z).sum()
ce = -np.log(prob)
logsum = np.log(np.exp(z).sum())
check(1, [rounds(logsum, 2.4076, 4),
          rounds(ce, [0.4076, 1.4076, 2.4076], 4),
          rounds(ce.mean(), 1.4076, 4),
          rounds(np.exp(ce.mean()), 4.09, 2)],
      [r"z=(2,1,0)", "0.4076", "1.4076", "2.4076", "4.09"])

tokens = tuple(range(1, 9))
training_pairs = [(tokens[:i], tokens[i]) for i in range(1, len(tokens))]
selected_positions = {3, 6}
masked_targets = [token for i, token in enumerate(tokens, 1)
                  if i in selected_positions]
check(1, [len(training_pairs) == 7,
          [target for _, target in training_pairs] == list(range(2, 9)),
          all(len(prefix) == target - 1 for prefix, target in training_pairs),
          len(masked_targets) == 2, masked_targets == [3, 6]],
      ["7 对", "2 个"], "随堂目标计数")
uniform = np.exp(np.zeros(3)) / np.exp(np.zeros(3)).sum()
check(1, [rounds(-np.log(uniform), [np.log(3)] * 3, 12),
          rounds(np.exp(-np.log(uniform).mean()), 3, 12)],
      [r"\ln3\approx1.0986", r"e^{\ln3}=3"], "同构小题")

# 2: probabilities and loss figures are correct to the displayed precision.
p2 = list(map(R, ["0.30", "0.50", "0.05", "0.40", "0.20"]))
terms = np.array([float(-sp.log(p)) for p in p2])
product = sp.prod(p2)
masked = -sp.log(R("0.30"))
p_first = sp.symbols("p_first", positive=True)
avg_loss = -sp.log(product) / len(p2)
joint_probability = p_first * product
full_nll = -sp.log(joint_probability)
correct_nll = -sp.log(p_first) + len(p2) * avg_loss
# Distinguish the conditional product from the full sequence probability.
wrong_nll = -sp.log(p_first) + 6 * avg_loss
likelihood_consistent = (
    equal(full_nll, correct_nll)
    and not equal(full_nll, wrong_nll)
    and not equal(joint_probability, product)
)
check(2, [rounds(terms, [1.2040, 0.6931, 2.9957, 0.9163, 1.6094], 4),
          rounds(terms.mean(), 1.4837, 4),
          equal(product, R(6, 10000)),
          rounds(-sp.log(product), 7.4186, 4),
          bool(-sp.log(product) > 0),
          rounds(terms.sum(), float(-sp.log(product)), 12),
          equal(5 * avg_loss, -sp.log(product)),
          rounds(masked, 1.2040, 4),
          likelihood_consistent,
          bool(re.search(r"负对数约为\s*\$7\.4186\$", EXAMPLES["2"]))],
      ["1.4837", r"6\times10^{-4}", r"-\ln P(x_1)+(T-1)L"])

joint = sp.Matrix([[R(1, 20), R(9, 20)], [R(9, 20), R(1, 20)]])
px0 = sum(joint.row(0))
px0_given_y0 = joint[0, 0] / sum(joint.col(0))
check(2, [sum(joint) == 1, px0 == R(1, 2),
          px0_given_y0 == R(1, 10), px0_given_y0 < px0,
          bool(-sp.log(px0_given_y0) > -sp.log(px0))],
      ["不是每个词、每个模型都必然如此"], "L04 条件概率反例")

# 3: label positions, answer mean, full mean, and the adjacent short exercise.
losses3 = list(map(R, ["2.4", "1.6", "0.9", "1.1", "1.5", "0.7", "0.4", "0.2"]))
check(3, [len(losses3) == 9-1,
          sum(losses3[:4]) == 6,
          sum(losses3[4:]) == R("2.8"),
          sum(losses3[4:])/4 == R("0.7"),
          sum(losses3)/8 == R("1.1"),
          sum(map(R, ["0.9", "0.3", "0.6"]))/3 == R("0.6")],
      [r"第 6–9 个", r"=0.7$", r"=1.1$"])

# 4: arithmetic under the chapter's stated 2N-per-token approximation.
N4 = 7 * 10**9
direct = 3 * 2 * N4
chain = 200 * 2 * N4
check(4, [direct == 42 * 10**9,
          chain == 28 * 10**11,
          rounds(R(chain, direct), 66.7, 1)],
      [r"4.2\times10^{10}", r"2.8\times10^{12}", r"200/3\approx66.7"])

# 5: ratios determine alpha; evaluate all reported extrapolations.
alpha = sp.log(R(4, 1) / R(5, 2)) / sp.log(R(10**9, 10**7))
one_decade = 10**(-alpha)
predicted = R(5, 2) * one_decade
check(5, [rounds(alpha, .102, 3), rounds(predicted, 1.98, 2),
          rounds(one_decade, .79, 2), rounds(1-one_decade, .21, 2),
          rounds(2**(-alpha), .93, 2),
          equal(sp.log(R("3.2")/2)/sp.log(100), alpha)],
      [r"\approx0.102", r"\approx1.98", r"\approx0.79", r"\approx0.93"])

# 6: verify the general derivative equation symbolically, not at one example.
n, c, a, b, coef_a, coef_b, E = sp.symbols("N c a b A B E", positive=True)
f6 = E + coef_a * n**(-a) + coef_b * (c/n)**(-b)
df6 = sp.diff(f6, n)
scaled_derivative = sp.simplify(df6 * n**(a+1))
z6 = sp.symbols("z")
candidate_expression = -a*coef_a + b*coef_b*c**(-b)*z6
root_z = sp.solve(candidate_expression, z6)[0]
claimed_z = a*coef_a/(b*coef_b)*c**b
n_star = claimed_z**(1/(a+b))
d_star = c/n_star
check(6, [equal(scaled_derivative,
                 -a*coef_a + b*coef_b*c**(-b)*n**(a+b)),
          equal(root_z, claimed_z),
          equal(n_star*d_star, c),
          equal(sp.diff(sp.log(n_star), c)*c, b/(a+b)),
          equal(sp.diff(sp.log(d_star), c)*c, a/(a+b)),
          equal(b/(a+b)+a/(a+b), 1),
          equal((100**(b/(a+b))).subs(b, a), 10),
          R(14*10**11, 70*10**9) == 20],
      [r"N_*=\Bigl(\frac{aA}{bB}\Bigr)^{\frac1{a+b}}",
       r"D_*=\frac c{N_*}", r"\frac{b}{a+b}", r"\frac{a}{a+b}", "20 个词元"])

# 7: independently multiply the matrices, including the merged-weight route.
W0 = sp.Matrix([[1, 0, 2], [0, 1, 1], [2, 1, 0]])
B7 = sp.Matrix([1, 2, 0])
A7 = sp.Matrix([[R(1, 2), 0, 1]])
x7 = sp.Matrix([2, 1, 1])
delta7 = B7*A7
check(7, [len(W0) == 9, len(B7)+len(A7) == 6,
          equal(delta7, sp.Matrix([[R(1, 2), 0, 1], [1, 0, 2], [0, 0, 0]])),
          delta7.rank() == 1,
          equal(A7*x7, sp.Matrix([2])),
          equal(B7*A7*x7, sp.Matrix([2, 4, 0])),
          equal(W0*x7, sp.Matrix([4, 2, 5])),
          equal((W0+delta7)*x7, sp.Matrix([6, 6, 5])),
          equal((W0+delta7)*x7, W0*x7+B7*(A7*x7))],
      [r"0.5&0&1\\1&0&2\\0&0&0", r"(6,6,5)^{\mathsf T}", "秩为 1"])

# Derive gradients for a nonzero A and x whose product vanishes.
b0, b1, a0, a1 = sp.symbols("b0 b1 a0 a1", real=True)
b_init = sp.Matrix([b0, b1])
a_init = sp.Matrix([[a0, a1]])
x_init = sp.Matrix([1, 1])
y_init = b_init * a_init * x_init
loss_init = y_init[0] + 2 * y_init[1]
initial_values = {b0: 0, b1: 0, a0: 1, a1: -1}
grad_b = sp.Matrix([sp.diff(loss_init, v) for v in (b0, b1)]).subs(initial_values)
grad_a = sp.Matrix([[sp.diff(loss_init, v) for v in (a0, a1)]]).subs(initial_values)
check(7, [a_init.subs(initial_values) != sp.zeros(1, 2),
          x_init != sp.zeros(2, 1),
          equal(a_init.subs(initial_values) * x_init, sp.zeros(1, 1)),
          equal(grad_b, sp.zeros(2, 1)), equal(grad_a, sp.zeros(1, 2)),
          equal(b_init.subs(initial_values) - R(1, 4) * grad_b, sp.zeros(2, 1))],
      detail="L15 非零 A、x 仍可有 Ax=0，首步不动")
check(7, [equal(sp.Matrix([1, 2]) * (sp.Matrix([[1, -1]]) * sp.Matrix([2, 1])),
                sp.Matrix([1, 2]))],
      [r"(1,2)^{\mathsf T}"], "随堂矩阵乘法")

# 8: per-matrix counts and the two different denominators in the percentages.
per_full = 4096**2
per_lora = 8*(4096+4096)
total_lora = 32*2*per_lora
check(8, [per_full == 16777216, per_lora == 65536,
          total_lora == 4194304,
          rounds(R(total_lora * 2 * 4, 10**6), 33.6, 1),
          rounds(100*R(per_lora, per_full), .39, 2),
          R(total_lora, 7*10**9) < R("0.0006")],
      ["65536", "16777216", "4194304", "0.39%", "0.06%", "33.6 MB"])

# 9: take top two BEFORE softmax; also check k=1 yields unit weight.
scores = np.array([2., 1., 0., -1.])
selected = np.argsort(-scores)[:2]
g = np.exp(scores[selected]) / np.exp(scores[selected]).sum()
selected_one = np.argsort(-scores)[:1]
g_one = np.exp(scores[selected_one]) / np.exp(scores[selected_one]).sum()
check(9, [np.array_equal(selected, [0, 1]),
          rounds(g, [.7311, .2689], 4),
          rounds(g.sum(), 1, 12),
          np.array_equal(g_one, [1.])],
      ["0.7311", "0.2689", "权重是 1"])

# 10: exact rational rounding and every stated reconstructed component.
def quantize(values, bits):
    if bits < 2 or int(bits) != bits:
        raise ValueError("bits must be an integer >= 2")
    if max(map(abs, values)) == 0:
        zeros = [sp.Integer(0) for _ in values]
        return sp.Integer(0), zeros, zeros.copy(), zeros.copy()
    step = max(map(abs, values))/(2**(bits-1)-1)
    codes = [sp.sign(w)*sp.floor(abs(w/step)+R(1, 2)) for w in values]
    restored = [qi*step for qi in codes]
    errors = [abs(w-hat) for w, hat in zip(values, restored)]
    return step, codes, restored, errors

w10 = list(map(R, [".30", "-.81", ".05", ".52", "-.22"]))
s10, q10, hat10, err10 = quantize(w10, 4)
so, qo, ho, eo = quantize(w10+[sp.Integer(4)], 4)
check(10, [s10 == R(81, 700),
           rounds(s10, .1157, 4),
           rounds([v/s10 for v in w10], [2.59, -7, .43, 4.49, -1.90], 2),
           q10 == [3, -7, 0, 4, -2],
           rounds(hat10, [.347, -.81, 0, .463, -.231], 3),
           rounds(max(err10), .057, 3),
           rounds(s10/2, .058, 3), max(err10) <= s10/2,
           rounds(so, .571, 3),
           rounds([ho[i] for i in [0, 2, 4]], [.571, 0, 0], 3),
           rounds([eo[i] for i in [0, 2, 4]], [.2714, .05, .22], 4),
           eo[0] > err10[0], eo[4] > err10[4],
           7*10**9*2/10**9 == 14,
           7*10**9/10**9 == 7,
           7*10**9*R(1, 2)/10**9 == R("3.5")],
      [r"q=(3,-7,0,4,-2)", "0.347", "0.463", "0.057", "0.058", "3.5 GB"])

sz, qz, hz, ez = quantize([sp.Integer(0)] * 5, 4)
check(10, [sz == 0, qz == [0] * 5, hz == [0] * 5, ez == [0] * 5],
      detail="全零组量化")

if set(EXAMPLES) != {str(i) for i in range(1, 11)}:
    print("FAIL 例题覆盖范围")
    FAILURES.append("coverage")
sys.exit(bool(FAILURES))
