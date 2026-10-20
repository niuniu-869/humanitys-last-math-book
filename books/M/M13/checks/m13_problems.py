"""Recompute the exercise data, then compare with the published answers.

Expected values are transcribed from answers.md. Required answer fragments
tie each numerical comparison to the text; choice keys are read from that text.
Only the general proof M13-11 is marked MANUAL.
"""
from pathlib import Path
import re
import sys

import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
TEXT = (ROOT / "answers.md").read_text(encoding="utf-8")
BLOCKS = dict(re.findall(
    r"(?ms)^\*\*(M13-\d+)\*\*\n(.*?)(?=^\*\*M13-\d+\*\*|\Z)", TEXT
))
FAILURES = []
VISITED = set()
R = sp.Rational


def equal(actual, expected):
    if isinstance(actual, sp.MatrixBase):
        return actual.shape == expected.shape and all(
            sp.simplify(a - b) == 0 for a, b in zip(actual, expected)
        )
    return sp.simplify(actual - expected) == 0


def near(actual, expected, atol):
    return bool(np.isclose(float(actual), float(expected), rtol=0, atol=atol))


def check(pid, conditions, fragments=(), label=None):
    VISITED.add(pid)
    missing = [f for f in fragments if f not in BLOCKS[pid]]
    passed = all(bool(c) for c in conditions) and not missing
    name = label or pid
    print(f"{'PASS' if passed else 'FAIL'} {name}")
    if not passed:
        FAILURES.append(name)
        print(f"  conditions={list(map(bool, conditions))}; missing={missing}")
    return passed


def choice(pid, truth, fragments):
    key_match = re.search(r"\*\*答案：\*\*\s*\(([A-D])\)", BLOCKS[pid])
    key = key_match.group(1) if key_match else ""
    option_checks = []
    for letter, value in zip("ABCD", truth):
        agrees = bool(value) == (letter == key)
        option_checks.append(agrees)
        check(pid, [agrees], label=f"{pid}-选项{letter}")
    check(pid, [key in "ABCD" and len(key) == 1, sum(map(bool, truth)) == 1,
                *option_checks], fragments)


# 01: map sequence positions to losses; do not index them as a length-10 list.
loss = dict(zip(range(2, 11), map(R, ["0.8", "1.2", "0.4", "1.5",
                                    "0.6", "0.9", "0.3", "1.1", "0.5"])))
answer_positions = [5, 7, 9, 10]
sft = sum(loss[t] for t in answer_positions) / len(answer_positions)
full = sum(loss.values()) / len(loss)
check("M13-01", [equal(sft, 1), equal(full, R(73, 90))],
      [r"损失为 $1$", r"$73/90\approx0.8111$", r"$7.3/9$"])

# 02: compute the two conditional distributions from the JOINT table.
joint = sp.Matrix([[R(3, 8), R(1, 8)], [R(1, 8), R(3, 8)]])
px = [sum(joint.row(i)) for i in range(2)]
py = [sum(joint.col(j)) for j in range(2)]
q = sp.Matrix(2, 2, lambda i, j: joint[i, j] / py[j] * joint[i, j] / px[i])
qsum = sum(q)
truth02 = [
    equal(q[0, 0], joint[0, 0]),
    equal(qsum, 1),
    equal(q / qsum, joint),
    equal(q[0, 0], R(9, 16)) and equal(qsum, R(5, 4)) and qsum != 1,
]
choice("M13-02", truth02, [r"9/16&1/16\\1/16&9/16", r"=5/4", r"=9/20"])
check("M13-02", [equal(q[0, 0] / qsum, R(9, 20))],
      label="M13-02-归一化反例")

# 03: explicit update and probability evaluations, not verbal truth flags.
theta0 = sp.Integer(0)
theta_prompt = theta0
theta_train = theta0 - 2 * sp.log(3) * R(-1, 2)
p = lambda theta, context: sp.exp(theta + context) / (1 + sp.exp(theta + context))
p_prompt = p(theta_prompt, sp.log(3))
p_train = p(theta_train, 0)
truth03 = [
    equal(p_prompt, p_train) and equal(theta_prompt, sp.log(3))
    and equal(theta_train, sp.log(3)),
    equal(theta_prompt, 0) and equal(theta_train, 0),
    equal(theta_prompt, 0) and equal(theta_train, sp.log(3))
    and equal(p_prompt, R(3, 4)) and equal(p_train, R(3, 4)),
    equal(theta_prompt, 0) and equal(p_prompt, R(1, 2))
    and equal(p_train, R(3, 4)),
]
choice("M13-03", truth03, [r"甲保持 $\theta=0$", r"=\ln3$", r"=3/4$"])

# 04: solve the ratio first, then recover the scale.
alpha = sp.log(R(8, 4)) / sp.log(R(8, 2))
scale = 8 * 2**alpha
check("M13-04", [equal(alpha, R(1, 2)), equal(scale, 8 * sp.sqrt(2)),
                 equal(scale * 32**(-alpha), 2)],
      [r"$\alpha=1/2,C=8\sqrt2,f(32)=2$"])

# 05: inverse inequality, its monotonicity, and a separate forward prediction.
qvar = sp.symbols("q", positive=True)
ratio = qvar**(-R(1, 10))
boundary = sp.solve(sp.Eq(ratio, R(4, 5)), qvar)[0]
prediction = R(5, 2) * 5**(-R(1, 10))
check("M13-05", [equal(boundary, R(5, 4)**10),
                 sp.diff(ratio, qvar).is_negative,
                 near(boundary, 9.3132, 0.00005),
                 near(prediction, 2.1283, 0.00005),
                 prediction != R(5, 2) - R(1, 10) * 5],
      [r"$q\ge(5/4)^{10}\approx9.3132$", r"\approx2.1283$", r"后者会误算成 $2$"])

# 06: evaluate all four proposed claims.
x = sp.symbols("x", positive=True)
u = sp.symbols("u", real=True)
f = 4 * x**(-R(1, 10))
logf = sp.expand_log(sp.log(f), force=True)
v = sp.simplify(logf.subs(x, sp.exp(u)))
ratio100 = sp.simplify(f.subs(x, 100 * x) / f)
ratio10 = sp.simplify(f.subs(x, 10 * x) / f)
truth06 = [
    equal(ratio100, R(4, 5)),
    equal(sp.diff(logf, x), -R(1, 10)) and equal(sp.diff(logf, x, 2), 0),
    equal(sp.diff(v, u), -R(1, 10)) and equal(ratio10, 10**(-R(1, 10))),
    equal(sp.diff(v, u), R(1, 10)),
]
choice("M13-06", truth06, [r"$v=\ln4-0.1u$", r"$-0.1/x$", r"\approx0.6310$"])
check("M13-06", [near(ratio100, 0.6310, 0.00005),
                 near(100 * (1 - ratio100), 36.90, 0.005)],
      label="M13-06-降幅")

# 07: integer storage constraint and an actual exact rank-4 factorization.
target = sp.zeros(6, 10)
for i in range(4):
    target[i, i] = 1
admissible = [r for r in range(1, 61) if r * (6 + 10) < 60]
b7 = sp.eye(4).col_join(sp.zeros(2, 4))
a7 = sp.eye(4).row_join(sp.zeros(4, 6))
check("M13-07", [admissible == [1, 2, 3], target.rank() == 4,
                 all(r < target.rank() for r in admissible),
                 equal(b7 * a7, target), len(b7) + len(a7) == 64],
      [r"$r\in\{1,2,3\}$", r"最小 $r=4$", r"$64$", r"0_{2\times4}",
       r"0_{4\times6}"], label="M13-07-(1)")

# 08: derive gradients from a scalar polynomial with SymPy.
b1, b2, a1, a2, a3 = sp.symbols("b1 b2 a1 a2 a3")
b8 = sp.Matrix([b1, b2])
a8 = sp.Matrix([[a1, a2, a3]])
x8 = sp.Matrix([2, 1, 3])
increment = b8 * a8 * x8
objective = increment[0] + 2 * increment[1]  # frozen W0 adds a constant
gb = sp.Matrix([sp.diff(objective, v) for v in [b1, b2]])
ga = sp.Matrix([[sp.diff(objective, v) for v in [a1, a2, a3]]])
initial = {b1: 0, b2: 0, a1: R(1, 2), a2: 1, a3: -1}
gb0, ga0 = gb.subs(initial), ga.subs(initial)
bnew = b8.subs(initial) - gb0 / 4
anew = a8.subs(initial) - ga0 / 4
updated = dict(zip([b1, b2, a1, a2, a3], list(bnew) + list(anew)))
ga1 = ga.subs(updated)
check("M13-08", [equal(gb0, sp.Matrix([-1, -2])),
                 equal(ga0, sp.zeros(1, 3)),
                 equal(bnew, sp.Matrix([R(1, 4), R(1, 2)])),
                 equal(anew, sp.Matrix([[R(1, 2), 1, -1]])),
                 equal(ga1, sp.Matrix([[R(5, 2), R(5, 4), R(15, 4)]]))],
      [r"=(-1,-2)^{\mathsf T}", r"=(0,0,0)",
       r"$B_1=(1/4,1/2)^{\mathsf T},A_1=A$", r"=(5/2,5/4,15/4)"])

# 07(2): symbolic determinant covers every nonzero t; t=0 is checked directly.
t = sp.symbols("t", real=True)
delta9 = sp.Matrix([[1, 2, 0], [2, 4 + t, 0], [0, 0, t]])
roots9 = sp.solve(delta9.det(), t)
check("M13-07", [equal(delta9.det(), t**2), roots9 == [0],
                 delta9.subs(t, 0).rank() == 1,
                 equal(sp.Matrix([1, 2, 0]) * sp.Matrix([[1, 2, 0]]),
                       delta9.subs(t, 0)),
                 equal(sp.eye(3) * delta9, delta9)],
      [r"仅 $t=0$", r"$r=1$", r"最小 $r=3$", r"=t^2$"], label="M13-07-(2)")

# 10: constrain first, then differentiate; neither test point is stationary.
n, d = sp.symbols("N D", positive=True)
F10 = 2 + 12/n + 3/d
f10 = F10.subs(d, 16/n)
check("M13-10", [equal(f10.subs(n, 4), R(23, 4)),
                 equal(f10.subs(n, 10), R(203, 40)),
                 equal(sp.diff(f10, n).subs(n, 4), -R(9, 16)),
                 equal(sp.diff(f10, n).subs(n, 10), R(27, 400)),
                 4 * 4 == 16 and 10 * R(8, 5) == 16],
      [r"$23/4=5.75$", r"$203/40=5.075$", r"$-9/16$", r"$27/400$",
       "两点都不是最小点"], label="M13-10-(1)")

# 10(2): isolate the derivative's sign and impose the extra feasible boundary.
F11 = 1 + 8/n + 2/d**2
f11 = F11.subs(d, 16/n)
df11 = sp.factor(sp.diff(f11, n))
roots11 = sp.solve(df11, n)
second = sp.diff(f11, n, 2)
sign_form = (n**3 - 512) / (64 * n**2)
check("M13-10", [roots11 == [8], second.is_positive,
                 equal(df11, sign_form),
                 equal(f11.subs(n, 8), R(5, 2)),
                 equal((16/n).subs(n, 8), 2),
                 sp.diff(f11, n).subs(n, 6) < 0,
                 equal(f11.subs(n, 6), R(251, 96)),
                 equal((16/n).subs(n, 6), R(8, 3))],
      [r"$5/2$", r"$(N,D)=(8,2)$", r"$251/96$", r"$(N,D)=(6,8/3)$",
       r"\frac{N^3-512}{64N^2}"], label="M13-10-(2)")

proof_b = sp.Matrix([[1, 0], [0, 1], [1, 1]])
proof_a = sp.Matrix([[1, 0, 1], [0, 1, 1]])
proof_product = proof_b * proof_a
check("M13-11", [proof_b.rank() == 2, proof_a.rank() == 2,
                 proof_product.rank() == 2,
                 equal(proof_product, sp.Matrix([[1, 0, 1], [0, 1, 1], [1, 1, 2]]))],
      [r"1&0&1\\0&1&1\\1&1&2", "秩均为 $2$"], label="M13-11-(2)")
counter_b = sp.Matrix([[1, 0], [2, 0], [3, 0]])
counter_a = sp.Matrix([[0, 0, 0], [0, 1, 0]])
check("M13-11", [counter_b.rank() == 1, counter_a.rank() == 1,
                 equal(counter_b * counter_a, sp.zeros(3, 3)),
                 (counter_b * counter_a).rank() == 0],
      [r"1&0\\2&0\\3&0", r"0&0&0\\0&1&0", r"BA=0_{3\times3}"],
      label="M13-11-(3)")
print("MANUAL M13-11-(1) 证明：B 的列线性无关使左乘保持全部列关系，故秩相等")

# 09: independent byte counts include the frozen base matrix array.
count = 20 * 2
base_parameters = count * 512 * 1024
frozen_bytes = base_parameters * 4
r13 = sp.symbols("r", integer=True, positive=True)
train_parameters = count * r13 * (512 + 1024)
total_bytes = frozen_bytes + train_parameters * 4 * 4
cap = 100_000_000
max_r = int(sp.floor((cap - frozen_bytes) / sp.diff(total_bytes, r13)))
at_max = total_bytes.subs(r13, max_r)
full_bytes = base_parameters * 4 * 4
check("M13-09", [max_r == 16,
                 train_parameters.subs(r13, max_r) == 983040,
                 at_max == 99614720,
                 at_max <= cap < total_bytes.subs(r13, max_r + 1),
                 total_bytes.subs(r13, 17) == 100597760,
                 full_bytes == 335544320,
                 equal(at_max / full_bytes, R(19, 64))],
      [r"最大 $r=16$", r"$983,040$", r"$99,614,720$", r"$19/64=29.6875\%$",
       r"$61,440r$", r"83,886,080+983,040r",
       r"$S(17)=100,597,760$", r"=335,544,320$"])

# 12: start from the two logits; derive the loss and its derivative.
z14 = [sp.Matrix([t, 0]), sp.Matrix([0, t])]
prob14 = [sp.exp(z[0]) / sum(sp.exp(zi) for zi in z) for z in z14]
loss14 = sum(-sp.log(pi) for pi in prob14) / 2
prob_at = [sp.simplify(pi.subs(t, sp.log(3))) for pi in prob14]
loss_at = sp.simplify(loss14.subs(t, sp.log(3)))
dl14 = sp.cancel(sp.diff(loss14, t))
check("M13-12", [prob_at == [R(3, 4), R(1, 4)],
                 equal(loss_at, sp.log(4/sp.sqrt(3))),
                 equal(sp.exp(loss_at), 4/sp.sqrt(3)),
                 equal(dl14, (sp.exp(t)-1)/(2*(1+sp.exp(t)))),
                 sp.solve(dl14, t) == [0],
                 sp.diff(loss14, t, 2).simplify().is_positive,
                 equal(loss14.subs(t, 0), sp.log(2))],
      [r"$3/4,1/4$", r"$L=\ln(4/\sqrt3)$", r"$e^L=4/\sqrt3$",
       r"$t=0$", r"$\ln2$", r"\frac{e^t-1}{2(1+e^t)}"])

# 13: invert the rounding rule and intersect with the stronger error bound.
domain15 = sp.Interval(0, R("0.70"))
fixed15 = [R("-0.70"), R("0.34")]
max_fixed = max(map(abs, fixed15))
s15 = max_fixed / (2**(4-1) - 1)
code15 = [2, -7, 3]
restored15 = [s15 * qi for qi in code15]
# For nonnegative t: floor(t/s+1/2)=2 iff 2 <= t/s+1/2 < 3.
rounding_set = sp.reduce_inequalities(
    [t/s15 + R(1, 2) >= 2, t/s15 + R(1, 2) < 3], t
).as_set().intersect(domain15)
error_set = sp.reduce_inequalities(
    [sp.Abs(t-restored15[0]) <= R("0.04")], t
).as_set().intersect(rounding_set)
actual_fixed_codes = [
    sp.sign(w) * sp.floor(abs(w/s15)+R(1, 2)) for w in fixed15
]
check("M13-13", [domain15.sup <= max_fixed, s15 == R("0.10"),
                 actual_fixed_codes == [-7, 3],
                 rounding_set == sp.Interval(R("0.15"), R("0.25"), right_open=True),
                 restored15 == list(map(R, ["0.20", "-0.70", "0.30"])),
                 error_set == sp.Interval(R("0.16"), R("0.24")),
                 abs(fixed15[0]-restored15[1]) == 0,
                 abs(fixed15[1]-restored15[2]) == R("0.04"),
                 sp.floor(R("0.15")/s15 + R(1, 2)) == 2,
                 sp.floor(R("0.25")/s15 + R(1, 2)) == 3],
      [r"$t\in[0.15,0.25)$", r"$(0.20,-0.70,0.30)^{\mathsf T}$",
       r"$t\in[0.16,0.24]$", r"$s=0.10$", r"$s/2=0.05$"])

# 14: work with exponentiated scores, whose ordering is identical.
vectors = [sp.Matrix([1, 0]), sp.Matrix([0, 1]), sp.Matrix([-1, 2])]
weights = [sp.Integer(3), sp.Integer(2), sp.Integer(1)]
selected = sorted(range(3), key=lambda i: weights[i], reverse=True)[:2]
y16 = sum((weights[i] * vectors[i] for i in selected), sp.zeros(2, 1)) / sum(weights[i] for i in selected)
z = sp.symbols("z", positive=True)  # z = exp(t)
target16 = sp.Matrix([-R(1, 2), R(3, 2)])
candidate_y = (3 * vectors[0] + z * vectors[2]) / (3 + z)
solutions = sp.solve([candidate_y[i] - target16[i] for i in range(2)], [z], dict=True)
zstar = solutions[0][z]
new_weights = [sp.Integer(3), sp.Integer(2), zstar]
new_selected = sorted(range(3), key=lambda i: new_weights[i], reverse=True)[:2]
check("M13-14", [equal(y16, sp.Matrix([R(3, 5), R(2, 5)])),
                 zstar == 9, set(new_selected) == {0, 2},
                 equal(candidate_y.subs(z, zstar), target16),
                 equal(3/(3+zstar), R(1, 4)),
                 equal(zstar/(3+zstar), R(3, 4))],
      [r"=(3/5,2/5)^{\mathsf T}", r"$t=\ln9$", r"$1,3$",
       r"$1/4,3/4$"])

# 15: solve the two vector equations separately.
svar = sp.symbols("s", real=True)
b17, a17 = sp.Matrix([1, 2]), sp.Matrix([[1, -1]])
delta17 = b17 * a17
w17 = sp.eye(2) + delta17
x17 = sp.Matrix([svar, 1])
unchanged = sp.solve(list(w17*x17 - x17), [svar], dict=True)
zero_output = sp.solve(list(w17*x17), [svar], dict=True)
check("M13-15", [unchanged == [{svar: 1}], zero_output == [{svar: R(1, 2)}],
                 delta17.rank() == 1, w17.rank() == 1,
                 equal(w17*x17.subs(svar, 1), x17.subs(svar, 1)),
                 equal(delta17, sp.Matrix([[1, -1], [2, -2]])),
                 equal(w17, sp.Matrix([[2, -1], [2, -1]]))],
      [r"$s=1$", r"$s=1/2$", r"$\operatorname{rank}(BA)=1,\operatorname{rank}(W)=1$",
       "所述命题错误", r"1&-1\\2&-2", r"2&-1\\2&-1"])

expected_ids = {f"M13-{i:02d}" for i in range(1, 16)}
if VISITED != expected_ids or set(BLOCKS) != expected_ids:
    FAILURES.append("coverage")
    print("FAIL M13-覆盖范围")

problems = (ROOT / "problems.md").read_text(encoding="utf-8")
headings = re.findall(r"(?m)^\*\*(M13-\d+)\*\*〔([ABC])", problems)
table = re.findall(r"(?m)^\| (M13-\d+) \| ([ABC])(?:（混合）)? \|", problems)
answer_ids = re.findall(r"(?m)^\*\*(M13-\d+)\*\*$", TEXT)
ordered_ids = sorted(expected_ids)
prerequisites = re.findall(r"拆法：([^\n]+)", problems)
structure_ok = (
    [pid for pid, _ in headings] == ordered_ids == answer_ids
    and table == headings
    and [tier for _, tier in headings] == list("AAAABBBBBCCBBBB")
    and len(prerequisites) == 2
    and all(pid in expected_ids for line in prerequisites
            for pid in re.findall(r"M13-\d+", line))
)
print(f"{'PASS' if structure_ok else 'FAIL'} M13-题号表与答案映射")
if not structure_ok:
    FAILURES.append("numbering")
sys.exit(bool(FAILURES))
