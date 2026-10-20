"""Recompute every determinate answer; only the proof is MANUAL.

Expected expressions below transcribe answers.md. Source anchors ensure that
the transcription still occurs in that answer. Calculations use the problem
data, symbolic differentiation, or finite differences independently.
"""
from pathlib import Path
import re
import sys

import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
ANSWERS = (ROOT / "answers.md").read_text(encoding="utf-8")
PROBLEMS = (ROOT / "problems.md").read_text(encoding="utf-8")
BLOCKS = dict(re.findall(
    r"(?ms)^\*\*(M10-\d+)\*\*\n(.*?)(?=^\*\*M10-|\Z)", ANSWERS
))
R = sp.Rational
failures = 0


def equal(actual, expected):
    if isinstance(actual, sp.MatrixBase):
        assert actual.shape == expected.shape
        assert all(sp.simplify(x) == 0 for x in actual - expected)
    else:
        assert sp.simplify(actual - expected) == 0, (actual, expected)


def close(actual, expected, atol=1e-10):
    np.testing.assert_allclose(actual, expected, atol=atol, rtol=0)


def softmax(x):
    x = np.asarray(x, dtype=float)
    e = np.exp(x - x.max())
    return e / e.sum()


def clip(g, threshold):
    g = np.asarray(g, dtype=float)
    norm = np.linalg.norm(g)
    return g * min(1.0, threshold / norm) if norm else g.copy()


def choice(pid, values):
    # Each value is evaluated from an option's mathematical assertion.
    chosen = re.search(r"\*\*答案：\*\*\s*\(([A-D])\)", BLOCKS[pid])[1]
    actual = [letter for letter, value in zip("ABCD", values) if bool(value)]
    assert actual == [chosen], (actual, chosen)
    return " (" + ", ".join(f"{a}={bool(b)}" for a, b in zip("ABCD", values)) + ")"


def run(number, calculation, anchors):
    global failures
    pid = f"M10-{number:02d}"
    try:
        for anchor in anchors:
            assert anchor in BLOCKS[pid], f"Answer transcription drift: {anchor}"
        detail = calculation() or ""
        print(f"PASS {pid}{detail}")
    except Exception as exc:
        failures += 1
        print(f"FAIL {pid} {type(exc).__name__}: {exc}")


def p01():
    joint, first, second = R(1, 32), R(1, 2), R(1, 4)
    third = joint / (first * second)
    equal(third, R(1, 4))
    equal(-sp.log(first * second * third) / 3, R(5, 3) * sp.log(2))


def p02():
    bits = sp.Integer(3)
    ppl = 2 ** bits
    return choice("M10-02", [ppl == 3, sp.Eq(ppl, sp.exp(3)), ppl == 8, ppl == R(1, 8)])


def p03():
    h1 = sp.simplify(sp.tanh(sp.log(3) / 2).rewrite(sp.exp))
    h2 = sp.tanh(h1 - R(1, 2))
    equal(h1, R(1, 2))
    equal(h2, 0)
    close(softmax([float(h2), -float(h2)]), [.5, .5])


def p04():
    W = sp.diag(2, R(1, 2))
    h = sp.Matrix([sp.sqrt(3) / 2, 0])
    J = sp.diag(*[1 - v**2 for v in h]) * W
    norm = max(J.singular_values())
    equal(J.T * J, sp.eye(2) / 4)
    # Option C is disproved by this nonzero direction; D by a short gradient.
    direction = sp.Matrix([1, 0])
    return choice("M10-04", [norm == 2, norm == R(1, 2),
                            (J * direction).norm() > direction.norm(),
                            np.isclose(np.linalg.norm(clip([.01, 0], 1)), 1)])


def p10():
    a, b, initial = sp.symbols("a b initial", real=True)
    k = sp.symbols("k", integer=True, nonnegative=True)
    params = sp.solve([a + b - R(3, 4), a*R(3, 4) + b - R(5, 8)], [a, b])
    equal(params[a], R(1, 2))
    equal(params[b], R(1, 4))
    r = sp.Function("r")
    general = sp.rsolve(r(k+1) - params[a]*r(k) - params[b], r(k), {r(0): initial})
    equal(general.subs(initial, 1), R(1, 2) + 2**(-k-1))
    equal(sp.limit(general, k, sp.oo), R(1, 2))
    equal(sp.diff(general, initial), 2**(-k))
    equal(sp.limit(sp.diff(general, initial), k, sp.oo), 0)


def p06():
    lengths = [2, 4]
    bits = [1, 4]
    total = sum(n * b for n, b in zip(lengths, bits))
    average = R(total, sum(lengths))
    equal(average, 3)
    equal(2**average, 8)
    equal(2**(-sp.Integer(total)), R(1, 2)**18)
    unweighted = sp.sqrt(sp.prod(2**b for b in bits))
    equal(unweighted, 4 * sp.sqrt(2))
    assert sp.simplify(unweighted - 2**average) != 0


def p07():
    w, u, b = sp.symbols("w u b", real=True)
    h = sp.Integer(0)
    objective = sp.Integer(0)
    xs, ys = [1, -1, 2], [1, 0, 1]
    for x, y in zip(xs, ys):
        h = sp.tanh(w * h + u * x + b)
        objective += (sp.log(1 + sp.exp(h)) - y * h) / 3
    point = {w: R(1, 2), u: 0, b: 0}
    # Direct differentiation of the fully expanded objective is independent
    # of the BPTT recurrence used in the written solution.
    for variable, expected in [(u, -R(13, 24)), (b, -R(5, 24)), (w, 0)]:
        equal(sp.diff(objective, variable).subs(point), expected)
    a1, a2, a3 = sp.symbols("a1 a2 a3", real=True)
    downstream = sp.log(1 + sp.exp(sp.tanh(a3))) - sp.tanh(a3)
    equal(sp.diff(downstream / 3, a3).subs(a3, 0), -R(1, 6))
    h2 = sp.tanh(a2)
    h3 = sp.tanh(h2 / 2)
    downstream = sp.log(1 + sp.exp(h2)) + sp.log(1 + sp.exp(h3)) - h3
    equal(sp.diff(downstream / 3, a2).subs(a2, 0), R(1, 12))
    h1 = sp.tanh(a1)
    h2, h3 = sp.tanh(h1 / 2), sp.tanh(sp.tanh(h1 / 2) / 2)
    downstream = sum(sp.log(1 + sp.exp(v)) - y * v for v, y in zip([h1, h2, h3], ys))
    equal(sp.diff(downstream / 3, a1).subs(a1, 0), -R(1, 8))


def p08():
    table = {"bos": [R(3, 5), R(3, 10), R(1, 10)],
             "a": [R(1, 10), R(1, 5), R(7, 10)],
             "b": [R(1, 5), R(3, 10), R(1, 2)]}
    symbols, target = ["a", "b", "eos"], ["b", "eos"]
    prefix, probability, inputs = "bos", sp.Integer(1), []
    for token in target:
        inputs.append(prefix)
        probability *= table[prefix][symbols.index(token)]
        prefix = token
    assert inputs == ["bos", "b"]
    equal(probability, R(3, 20))
    loss = -sp.log(probability) / len(target)
    equal(loss, sp.log(R(20, 3)) / 2)
    equal(sp.exp(loss), sp.sqrt(R(20, 3)))
    close(float(loss), .9486, 5e-5)
    close(float(sp.exp(loss)), 2.5820, 5e-5)
    prefix, probability, generated = "bos", sp.Integer(1), []
    for _ in range(10):
        row = table[prefix]
        index = max(range(3), key=lambda j: row[j])
        prefix = symbols[index]
        generated.append(prefix)
        probability *= row[index]
        if prefix == "eos":
            break
    assert generated == ["a", "eos"]
    equal(probability, R(21, 50))


def p05():
    H = np.array([[0., 0.], [2., 0.], [2., 0.]])
    old = softmax([0, 0]) @ H[:2]
    weights = softmax([0, 0, 0])
    context = weights @ H
    close(old, [1, 0])
    return choice("M10-05", [np.allclose(context, [1, 0]),
                            np.allclose(weights, [1/3]*3) and np.allclose(context, [4/3, 0]),
                            np.isclose(weights[0], 0), np.isclose(weights[1], 1)])


def p11():
    f, c0 = sp.symbols("f c0", positive=True)
    c = c0
    for _ in range(4):
        c = f * c
    equal(c.subs(c0, 1), f**4)
    equal(sp.diff(c, c0), f**4)
    roots = sp.solve(sp.Eq(f**4, R(1, 2)), f)
    assert len(roots) == 1
    r = roots[0]
    equal(r, 2**(-R(1, 4)))
    beta = sp.symbols("beta", real=True)
    threshold = sp.solve(sp.Eq(1 / (1 + sp.exp(-beta)), r), beta)[0]
    expected = sp.log(r / (1-r))
    close(float(threshold), float(expected))
    close(float(threshold), 1.6649, 5e-5)
    # Positive derivatives establish the whole half-line, not just samples.
    assert sp.diff(f**4, f).is_positive
    sigmoid_derivative = sp.diff(1 / (1 + sp.exp(-beta)), beta)
    assert sp.simplify(sigmoid_derivative).is_positive
    equal((sp.tanh(c) / 2).subs({f: r, c0: 1}), sp.tanh(R(1, 2)) / 2)
    close(float(sp.tanh(R(1, 2)) / 2), .2311, 5e-5)
    z = sp.symbols("z", real=True)
    boundaries = sp.solve(sp.Eq((1-z)**4, R(1, 2)), z)
    feasible = [v for v in boundaries if 0 < float(v) < 1]
    assert len(feasible) == 1
    equal(feasible[0], 1-r)
    # Substituting z=1-f shows monotonic decrease on 0<z<1.
    equal(sp.diff((1-z)**4, z).subs(z, 1-f), -4*f**3)


def p12():
    theta = sp.symbols("theta", real=True)
    p = sp.exp(theta) / (sp.exp(theta) + sp.exp(-theta))
    loss = -(2 * sp.log(p) + sp.log(1-p)) / 3
    derivative = sp.simplify(sp.diff(loss, theta))
    roots = sp.solve(derivative, theta)
    assert len(roots) == 1
    optimum = roots[0]
    equal(optimum, sp.log(2) / 2)
    equal(derivative, 2*p - R(4, 3))
    assert sp.simplify(sp.diff(p, theta)).is_positive
    minimum = sp.simplify(loss.subs(theta, optimum))
    equal(minimum, sp.log(3) - R(2, 3) * sp.log(2))
    equal(sp.exp(minimum), 3 / 2**R(2, 3))


def p13():
    g1, g2 = np.array([6., 0]), np.array([0., 8])
    together = clip(g1 + g2, 5)
    separately = clip(g1, 5) + clip(g2, 5)
    close(together, [3, 4])
    close(separately, [5, 5])
    close(np.linalg.norm(separately), 5 * np.sqrt(2))
    assert not np.allclose(together, separately)
    close(np.array([1., -1]) - .1 * together, [.7, -1.4])


def p14():
    # First two rows are coordinates; the third enforces the sum of weights.
    system = sp.Matrix([[0, 2, 0], [0, 0, 3], [1, 1, 1]])
    weights = system.inv() * sp.Matrix([R(1, 2), R(3, 2), 1])
    equal(weights, sp.Matrix([R(1, 4), R(1, 4), R(1, 2)]))
    scores = sp.Matrix([sp.log(v / weights[0]) for v in weights])
    equal(scores, sp.Matrix([0, 0, sp.log(2)]))
    close(softmax(np.array(scores, dtype=float).ravel()), np.array(weights, dtype=float).ravel())
    impossible = system.inv() * sp.Matrix([2, 3, 1])
    equal(impossible, sp.Matrix([-1, 1, 1]))
    assert any(v <= 0 for v in impossible)


if __name__ == "__main__":
    run(1, p01, [r"p_3=1/4", r"L=\frac53\ln2"])
    run(2, p02, ["(C)", "$2^3=8$"])
    run(3, p03, ["h_1=1/2", "h_2=0", "(1/2,1/2)"])
    run(4, p04, ["(B)", "长度 $0.01$ 保持不变"])
    run(5, p05, ["(B)", "(4/3,0)"])
    run(6, p06, ["平均值为 3", "几何平均的倒数为 8", "$2^{-18}$", r"$4\sqrt2$，不正确"])
    run(7, p07, ["=(-1/6,1/12,-1/8)", "u=-13/24", "b=-5/24", "w=0"])
    run(8, p08, [r"\langle\mathrm{bos}\rangle,b", "$3/20$", r"\frac12\ln(20/3)",
                "0.9486", r"\sqrt{20/3}", "2.5820", r"a,\langle\mathrm{eos}\rangle", "$21/50$"])
    proof_block = re.search(r"(?s)\*\*M10-09\*\*(.*?)\*\*M10-10\*\*", PROBLEMS)[1]
    if "证明" in proof_block and "谱范数的次乘性" in BLOCKS["M10-09"]:
        print("MANUAL M10-09 证明：核查链式法则、因子次序与范数上界")
    else:
        failures += 1
        print("FAIL M10-09 证明题或证明骨架缺失")
    run(10, p10, ["a=1/2,b=1/4", "s_k=1/2+2^{-(k+1)}", "极限为 $1/2$", "s_0=2^{-k}"])
    run(11, p11, [r"c_4=f^4", r"c_0=f^4", r"r=2^{-1/4}", r"\beta\ge\ln\frac r{1-r}",
                 "1.6649", r"\frac12\tanh(1/2)", "0.2311", r"0<z\le1-2^{-1/4}"])
    run(12, p12, [r"\theta=\frac12\ln2", r"\ln3-\frac23\ln2", "$3/2^{2/3}$"])
    run(13, p13, ["(3,4)", "(5,5)", r"5\sqrt2", "两种次序不等价", "(7/10,-7/5)"])
    run(14, p14, ["(1/4,1/4,1/2)", r"(0,0,\ln2)", "(2) 不存在", r"\alpha_1=-1"])
    expected_ids = {f"M10-{i:02d}" for i in range(1, 15)}
    if set(BLOCKS) != expected_ids:
        failures += 1
        print("FAIL M10-14 答案题号集合不完整")
    try:
        table = re.findall(r"^\| (M10-\d+) \| ([ABC]) \|", PROBLEMS, re.M)
        statements = re.findall(r"^\*\*(M10-\d+)\*\*〔([ABC])", PROBLEMS, re.M)
        assert table == statements
        assert [pid for pid, _ in table] == list(BLOCKS)
        assert set(pid for pid, _ in table) == expected_ids
        assert [sum(level == c for _, level in table) for c in "ABC"] == [5, 6, 3]
        summary = (ROOT / "lesson.md").read_text(encoding="utf-8").split("### 本章小结")[1]
        referenced = set()
        for row in summary.splitlines():
            if row.startswith("| 方法 "):
                cell = row.split("|")[-2]
                if "M10-" in cell:
                    referenced.update("M10-" + n for n in re.findall(r"\d{2}", cell.replace("M10-", "")))
        assert referenced == expected_ids
        print("PASS 题号配套 题号表、题干、答案与讲义小结一致；A5/B6/C3")
    except (AssertionError, IndexError) as exc:
        failures += 1
        print(f"FAIL 题号配套 {exc}")
    sys.exit(bool(failures))
