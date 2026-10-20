"""Recompute the exercises from their inputs; expected values mirror answers.md."""

from pathlib import Path
import re
import sys

import numpy as np
import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
ANSWERS = (ROOT / "answers.md").read_text(encoding="utf-8")
BLOCKS = dict(re.findall(r"\*\*(M9-\d+)\*\*\n(.*?)(?=\n\*\*M9-|\Z)", ANSWERS, re.S))
R = sp.Rational
M = sp.Matrix
failures = 0


def equal(actual, expected):
    if isinstance(actual, sp.MatrixBase):
        assert actual.shape == expected.shape
        assert all(sp.simplify(a - b) == 0 for a, b in zip(actual, expected)), (actual, expected)
    else:
        assert sp.simplify(actual - expected) == 0, (actual, expected)


def text_has(pid, *tokens):
    for token in tokens:
        assert token in BLOCKS[pid], (pid, "answer text changed", token)


def report(pid, fn):
    global failures
    try:
        fn()
        print(f"PASS {pid}")
    except Exception as exc:
        failures += 1
        print(f"FAIL {pid}: {type(exc).__name__}: {exc}")


def choice(pid, actual, expected, letter):
    assert len(actual) == len(expected) == 4
    for i, (value, want) in enumerate(zip(actual, expected)):
        report(f"{pid} 选项 {'ABCD'[i]}", lambda value=value, want=want: equal(int(bool(value)), int(want)))
    text_has(pid, f"选 ({letter})")
    assert ["ABCD"[i] for i, value in enumerate(actual) if value] == [letter]


def softmax(z):
    values = z.applyfunc(sp.exp)
    return values / sum(values)


def cosine(a, b):
    return sp.simplify(a.dot(b) / sp.sqrt(a.dot(a) * b.dot(b)))


def grad(expr, symbols):
    return M([sp.diff(expr, s) for s in symbols])


def p01():
    e = sp.eye(3)
    c1, c2 = cosine(e[:, 0], e[:, 1]), cosine(e[:, 0], e[:, 2])
    distance = (e[:, 0] - e[:, 1]).norm()
    choice("M9-01", [c1 == 1, c1 > c2, distance == 2, c1 == c2 == 0], [0, 0, 0, 1], "D")
    equal(distance, sp.sqrt(2))
    text_has("M9-01", r"\sqrt2", "两个余弦都是 0")


def p02():
    symbols = sp.symbols("e0:6", real=True)
    E = M(3, 2, symbols)
    O = M([[0, 0, 1], [1, 0, 0], [0, 0, 1]])
    H = M([[-1, 2], [3, 0], [-1, 2]])
    solution = sp.solve(list(O * E - H), symbols, dict=True)
    assert len(solution) == 1
    equal(E.subs(solution[0]), M([[3, 0], [symbols[2], symbols[3]], [-1, 2]]))
    equal(len(solution[0]), 4)
    text_has("M9-02", r"3&0\\a&b\\-1&2", "4 个元素")


def p03():
    U, v = M([[1, 0], [0, 1], [0, 0]]), M([sp.log(2), sp.log(3)])
    z = U * v
    equal(z, M([sp.log(2), sp.log(3), 0]))
    p = softmax(z)
    equal(p, M([R(1, 3), R(1, 2), R(1, 6)]))
    equal(-sp.log(p[1]), sp.log(2))
    text_has("M9-03", "(1/3,1/2,1/6)", r"\ell=\ln2")


def p04():
    z = sp.eye(2) / (1 / sp.log(3))
    rows = [-sp.log(softmax(z[i, :].T)[i]) for i in range(2)]
    cols = [-sp.log(softmax(z[:, i])[i]) for i in range(2)]
    for i in range(2):
        equal(softmax(z[i, :].T)[i], R(3, 4))
    for loss in [sum(rows) / 2, sum(cols) / 2, (sum(rows) + sum(cols)) / 4]:
        equal(loss, sp.log(R(4, 3)))
    text_has("M9-04", "$3/4$", r"\ln(4/3)")


def p05():
    sequences = [[0, 0, 1], [1, 2]]
    X = sp.zeros(3)
    count = 0
    for sequence in sequences:
        for i, center in enumerate(sequence):
            for j, context in enumerate(sequence):
                if 0 < abs(i - j) <= 1:
                    X[center, context] += 1
                    count += 1
    equal(X, M([[2, 1, 0], [1, 0, 1], [0, 1, 0]]))
    equal(count, 6)
    ac, bc = cosine(X[0, :], X[2, :]), cosine(X[1, :], X[2, :])
    equal(ac, 1 / sp.sqrt(5))
    equal(bc, 0)
    assert X[1, 2] > 0 and X[0, 2] == 0 and ac > bc
    text_has("M9-05", r"2&1&0\\1&0&1\\0&1&0", "总数为 6", r"1/\sqrt5")


def p06():
    x, y = sp.symbols("x y", real=True)
    U, target = M([[1, 0], [0, 1], [1, 1]]), M([R(1, 6), R(1, 3), R(1, 2)])
    z = U * M([x, y])
    equations = [z[i] - z[2] - sp.log(target[i] / target[2]) for i in [0, 1]]
    solutions = sp.solve(equations, [x, y], dict=True)
    assert len(solutions) == 1
    equal(M([solutions[0][x], solutions[0][y]]), M([sp.log(R(3, 2)), sp.log(3)]))
    p = softmax(z.subs(solutions[0]))
    equal(p, target)
    equal(-sp.log(p[2]), sp.log(2))
    text_has("M9-06", r"x=\ln(3/2),y=\ln3", "唯一解", r"损失为 $\ln2$")


def p07():
    x, y = sp.symbols("x y", real=True)
    symbols = sp.symbols("u0:6", real=True)
    U, v = M(3, 2, symbols), M([x, y])
    z = U * v
    loss = -z[2] + sp.log(sum(sp.exp(s) for s in z))
    point = dict(zip(symbols, [1, 0, -1, 0, 0, 0])) | {x: 0, y: 2}
    gv = grad(loss, [x, y]).subs(point)
    gu = M(3, 2, grad(loss, symbols)).subs(point)
    value = sp.simplify(loss.subs(point))
    equal(gv, sp.zeros(2, 1))
    equal(gu, M([[0, R(2, 3)], [0, R(2, 3)], [0, -R(4, 3)]]))
    equal(value, sp.log(3))
    only_target = gu[0, :] == sp.zeros(1, 2) and gu[1, :] == sp.zeros(1, 2) and gu[2, :] != sp.zeros(1, 2)
    choice("M9-07", [gv == sp.zeros(2, 1) and gu != sp.zeros(3, 2), gu == sp.zeros(3, 2), only_target, value == 0], [1, 0, 0, 0], "A")
    text_has("M9-07", r"0&2/3\\0&2/3\\0&-4/3", r"\ell=\ln3")


def p08():
    x, y, a, b, c, d = sp.symbols("x y a b c d", real=True)
    so, sn = a * x + b * y, c * x + d * y
    loss = sp.log(1 + sp.exp(-so)) + 2 * sp.log(1 + sp.exp(sn))
    point = {x: 0, y: sp.log(2), a: 1, b: 0, c: 0, d: 1}
    equal(loss.subs(point), sp.log(18))
    equal(grad(loss, [x, y]).subs(point), M([-R(1, 2), R(4, 3)]))
    equal(grad(loss, [a, b]).subs(point), M([0, -sp.log(2) / 2]))
    equal(grad(loss, [c, d]).subs(point), M([0, 4 * sp.log(2) / 3]))
    deduplicated = sp.log(1 + sp.exp(-so)) + sp.log(1 + sp.exp(sn))
    equal(deduplicated.subs(point), sp.log(6))
    equal(grad(deduplicated, [x, y]).subs(point), M([-R(1, 2), R(2, 3)]))
    text_has("M9-08", r"\ell=\ln18", "(-1/2,4/3)", r"(0,-\ln2/2)", r"(0,4\ln2/3)", r"\ln6", "(-1/2,2/3)")


def p09():
    f = sp.symbols("f", positive=True)
    solutions = sp.solve(81 ** R(3, 4) / f ** R(3, 4) - R(27, 8), f)
    assert solutions == [16]
    frequencies = M([81, solutions[0], 1])
    weights = frequencies.applyfunc(lambda q: q ** R(3, 4))
    p = weights / sum(weights)
    equal(p, M([R(3, 4), R(2, 9), R(1, 36)]))
    raw = frequencies[1] / sum(frequencies)
    equal(raw, R(8, 49))
    assert p[1] > raw
    text_has("M9-09", "$f_1=16$", "(3/4,2/9,1/36)", "$8/49$ 大")


def p10():
    h = sp.symbols("h", positive=True)
    # r = exp(1/tau) > 1; halving tau replaces r by r**2.
    r = 1 + h
    old_p, new_p = 1 / (1 + r), 1 / (1 + r ** 2)
    old_loss, new_loss = -sp.log(old_p), -sp.log(new_p)
    assert sp.factor(new_p - old_p).is_negative
    assert sp.expand(r ** 2 - r).is_positive
    assert sp.simplify(old_loss - sp.log(2)).is_positive
    assert new_loss.is_positive
    claims = [sp.factor(new_p - old_p).is_positive,
              sp.factor(old_p - new_p).is_positive,
              sp.simplify(old_loss - sp.log(2)) == 0,
              sp.simplify(new_loss - 2 * sp.log(1 + r ** 2)) == 0]
    choice("M9-10", claims, [0, 1, 0, 0], "B")
    for tau in [0.5, 1.0, 2.0]:
        S = np.array([[0., 1.], [1., 0.]])
        losses = []
        for temp in [tau, tau / 2]:
            z = S / temp
            row = np.logaddexp.reduce(z, axis=1) - np.diag(z)
            col = np.logaddexp.reduce(z, axis=0) - np.diag(z)
            losses.append((row.mean() + col.mean()) / 2)
        assert losses[1] > losses[0]
        assert np.isclose(losses[1], np.logaddexp(0, 2 / tau))
    text_has("M9-10", r"新总损失为 $\ln(1+e^{2/\tau})$")


def p12():
    t = sp.symbols("t", real=True)
    scores = M([t, -t])
    p = softmax(scores)
    J = sum(-sp.log(p[label]) for label in [0, 0, 0, 1]) / 4
    expected_J = sp.log(sp.exp(t) + sp.exp(-t)) - t / 2
    equal(sp.expand_log(J, force=True), expected_J)
    derivative = sp.diff(J, t)
    r = sp.symbols("r", positive=True)
    stationary = sp.solve(2 * r / (1 + r) - R(3, 2), r)
    assert stationary == [3]
    equal(derivative, 2 * sp.exp(2 * t) / (1 + sp.exp(2 * t)) - R(3, 2))
    equal(sp.diff(J, t, 2), 4 * sp.exp(2 * t) / (1 + sp.exp(2 * t)) ** 2)
    optimum = sp.log(stationary[0]) / 2
    equal(p.subs(t, optimum), M([R(3, 4), R(1, 4)]))
    minimum = sp.log(4) - R(3, 4) * sp.log(3)
    equal(J.subs(t, optimum), minimum)
    updated = -derivative.subs(t, 0)
    equal(updated, R(1, 2))
    equal(sp.logcombine(J.subs(t, updated) - (sp.log(1 + sp.E) - R(3, 4)), force=True), 0)
    values = [float(J.subs(t, val)) for val in [optimum, updated, 0]]
    assert values[0] < values[1] < values[2]
    assert [round(value, 4) for value in values] == [0.5623, 0.5633, 0.6931]
    text_has("M9-12", r"J(t)=\ln(e^t+e^{-t})-t/2", r"t_*=\frac12\ln3", "(3/4,1/4)", "0.5623", "0.5633", "0.6931", "$t_1=1/2$")


def p13():
    symbols = sp.symbols("e0:4", real=True)
    E = M(2, 2, symbols)
    O, G = M([[1, 0], [0, 1], [1, 0]]), M([[1, 2], [3, 4], [-1, 1]])
    # The differential is linear in dH, so a linear J realizes the given local G.
    H = O * E
    J = sum(H[i, j] * G[i, j] for i in range(3) for j in range(2))
    actual = M(2, 2, grad(J, symbols))
    equal(actual, M([[0, 3], [3, 4]]))
    equal(actual, O.T * G)
    equal(sp.eye(2) - actual / 10, M([[1, -R(3, 10)], [-R(3, 10), R(3, 5)]]))
    assert actual[0, :] != G[2, :]
    text_has("M9-13", r"0&3\\3&4", r"1&-3/10\\-3/10&3/5")


def p14():
    s0, s1 = sp.symbols("s0 s1", real=True)
    L = -s0 + sp.log(sp.exp(s0) + sp.exp(s1))
    B = sp.log(1 + sp.exp(-s0)) + sp.log(1 + sp.exp(s1))
    point = {s0: sp.log(3), s1: 0}
    equal(L.subs(point), sp.log(R(4, 3)))
    equal(B.subs(point), sp.log(R(8, 3)))
    gl, gb = grad(L, [s0, s1]).subs(point), grad(B, [s0, s1]).subs(point)
    equal(gl, M([-R(1, 4), R(1, 4)]))
    equal(gb, M([-R(1, 4), R(1, 2)]))
    assert M.hstack(gl, gb).det() != 0
    text_has("M9-14", r"L=\ln(4/3),B=\ln(8/3)", "(-1/4,1/4)", "(-1/4,1/2)", "更新方向不同")


def p15():
    vectors = dict(zip("abcdef", map(M, [[2, 1], [1, 0], [0, -1], [4, 0], [1, R(1, 2)], [-1, 0]])))
    q = vectors["a"] - vectors["b"] + vectors["c"]
    equal(q, M([1, 0]))
    candidates = {key: value for key, value in vectors.items() if key not in "abc"}
    cs = {key: cosine(q, value) for key, value in candidates.items()}
    ds = {key: (q - value).norm() for key, value in candidates.items()}
    equal(M(list(cs.values())), M([1, 2 / sp.sqrt(5), -1]))
    equal(M(list(ds.values())), M([3, R(1, 2), 2]))
    assert max(cs, key=lambda key: float(cs[key])) == "d"
    assert min(ds, key=lambda key: float(ds[key])) == "e"
    equal(q, vectors["b"])
    text_has("M9-15", "(1,0)", "余弦规则选 $d$", "距离规则选 $e$", "$3,1/2,2$")


if __name__ == "__main__":
    for number, fn in [(1, p01), (2, p02), (3, p03), (4, p04), (5, p05),
                       (6, p06), (7, p07), (8, p08), (9, p09), (10, p10),
                       (12, p12), (13, p13), (14, p14), (15, p15)]:
        report(f"M9-{number:02d}", fn)
    print("MANUAL M9-11 证明题：链式法则、归一化与同时更新的求和论证需人工审阅")
    sys.exit(1 if failures else 0)
