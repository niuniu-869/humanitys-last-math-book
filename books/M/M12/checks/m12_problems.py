"""Recompute the exercises; expected values below transcribe answers.md.

Numeric tolerances are only for floating-point paths. Symbolic exercises use
exact equality. Choice options are evaluated separately, including false ones.
"""

from pathlib import Path
import re
import sys

import numpy as np
import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
ANSWER = (ROOT / "answers.md").read_text(encoding="utf-8")
PROBLEMS = (ROOT / "problems.md").read_text(encoding="utf-8")
PARTS = dict(re.findall(r"\*\*(M12-\d+)\*\*\n(.*?)(?=\n\*\*M12-|\Z)", ANSWER, re.S))
FAILURES = 0


def same(actual, expected):
    if isinstance(actual, sp.MatrixBase):
        expected = sp.Matrix(expected)
        return actual.shape == expected.shape and all(
            sp.simplify((a - b).rewrite(sp.exp)) == 0 for a, b in zip(actual, expected)
        )
    if isinstance(actual, (sp.Set, tuple, bool, np.bool_)):
        return actual == expected
    return sp.simplify(actual - expected) == 0


def eq(actual, expected):
    assert same(actual, expected), f"computed={actual}; expected={expected}"


def close(actual, expected, atol=1e-12):
    assert np.allclose(actual, expected, rtol=0, atol=atol), (actual, expected)


def answer_contains(pid, *pieces):
    for piece in pieces:
        assert piece in PARTS[pid], f"answer text drift: {pid}: {piece}"


def softmax(values):
    values = np.asarray(values, dtype=float)
    e = np.exp(values - values.max(axis=-1, keepdims=True))
    return e / e.sum(axis=-1, keepdims=True)


def symbolic_softmax(matrix):
    return sp.Matrix([
        [sp.simplify(sp.exp(x) / sum(sp.exp(y) for y in row)) for x in row]
        for row in matrix.tolist()
    ])


def normalize(row, eps=0, center=True):
    row = sp.Matrix([list(row)])
    mean = sum(row) / len(row) if center else 0
    deviations = row - sp.ones(1, len(row)) * mean
    variance = sum(x**2 for x in deviations) / len(row)
    return deviations.applyfunc(lambda x: sp.simplify(x / sp.sqrt(variance + eps)))


def relu(matrix):
    return matrix.applyfunc(lambda x: sp.Max(x, 0))


def rotation(angle):
    return sp.Matrix([[sp.cos(angle), -sp.sin(angle)],
                      [sp.sin(angle), sp.cos(angle)]])


def run(pid, function, manual=False, detail=""):
    global FAILURES
    try:
        assert "**答案：**" in PARTS[pid] and "区分点：" in PARTS[pid]
        function()
    except Exception as error:
        FAILURES += 1
        print(f"FAIL {pid}{detail} {type(error).__name__}: {error}")
    else:
        suffix = " (symbolic identities checked; written proof requires review)" if manual else ""
        print(f"{'MANUAL' if manual else 'PASS'} {pid}{detail}{suffix}")


def choices(pid, computed, expected):
    for label, actual, want in zip("ABCD", computed, expected):
        # False options pass only when their mathematical claim is false.
        run(pid, lambda a=actual, w=want: eq(bool(a), w),
            detail=f" ({label}: {bool(actual)}; expected {want})")
    correct = "".join(label for label, value in zip("ABCD", computed) if value)
    answer_contains(pid, f"**答案：** ({correct})")


def p01():
    n, d, h = 4, 6, 3
    q_heads = [np.zeros((n, d // h)) for _ in range(h)]
    weights = [q @ q.T for q in q_heads]
    params = sum(np.zeros((d, d // h)).size for _ in range(3 * h)) + d*d
    params_six = sum(np.zeros((d, d // 6)).size for _ in range(3 * 6)) + d*d
    eq(params, 144)
    choices("M12-01", [q_heads[0].size == 24, sum(a.size for a in weights) == 16,
                        params == 144, params_six == 2 * params],
            [False, False, True, False])


def p02():
    z = normalize([1, 3], eps=3)
    output = z.multiply_elementwise(sp.Matrix([[2, 1]])) + sp.Matrix([[1, -1]])
    eq(output, [[0, -sp.Rational(1, 2)]])
    eq(sum(x*x for x in z) / len(z) - (sum(z) / len(z))**2, sp.Rational(1, 4))
    answer_contains("M12-02", "(0,-\\tfrac12)", "$1/4$")


def p03():
    p = sp.symbols("p", real=True)
    d = 4
    omega = [sp.Integer(10000)**(-sp.Rational(2*i, d)) for i in range(d // 2)]
    vector = sp.Matrix([f(w*p) for w in omega for f in (sp.sin, sp.cos)])
    norm2 = sp.trigsimp(vector.dot(vector))
    choices("M12-03", [vector.subs(p, 0) == sp.zeros(4, 1), norm2 == 1,
                        omega == [1, sp.Rational(1, 10000)], norm2 == 2],
            [False, False, False, True])


def p04():
    x = sp.Matrix([[1, 5]])
    f = lambda z: sp.zeros(*z.shape)
    eq(x + f(normalize(x)), [[1, 5]])
    eq(normalize(x + f(x)), [[-1, 1]])
    answer_contains("M12-04", "$(1,5)$、$(-1,1)$")


def p05():
    t = sp.symbols("t", real=True)
    w1 = sp.Matrix([[1, -1, 0], [0, 0, 1]])
    w2 = sp.Matrix([[1, 0], [-1, 0], [0, 1]])
    pre = sp.Matrix([[t, 1]]) * w1 + sp.Matrix([[-1, 1, 0]])
    eq(pre, [[t - 1, 1 - t, 1]])
    h = relu(pre)
    a = sp.symbols("a", positive=True)
    branches = [(1-a, [[0, a, 1]]), (1, [[0, 0, 1]]), (1+a, [[a, 0, 1]])]
    for value, hidden_expected in branches:
        hidden = h.subs(t, value)
        eq(hidden, hidden_expected)
        eq(hidden * w2, [[value - 1, 1]])
    eq(sp.solveset(t-1, t, domain=sp.S.Reals), sp.FiniteSet(1))
    answer_contains("M12-05", "$F(t,1)=(t-1,1)$", "$t=1$")


def p06():
    s1 = sp.Matrix([[0, sp.log(3)], [0, -sp.log(3)]])
    # These scores are realizable by a one-dimensional query/key pair.
    eq(sp.Matrix([1, -1]) * sp.Matrix([[0, sp.log(3)]]), s1)
    a1 = symbolic_softmax(s1)
    a2 = symbolic_softmax(sp.zeros(2, 2))
    v1, v2 = sp.Matrix([0, 4]), sp.Matrix([2, 0])
    wo = sp.Matrix([[1, 1], [1, -1]])
    eq(a1, [[sp.Rational(1, 4), sp.Rational(3, 4)],
            [sp.Rational(3, 4), sp.Rational(1, 4)]])
    eq(a2, sp.ones(2, 2) / 2)
    concatenated = (a1 * v1).row_join(a2 * v2)
    eq(concatenated, [[3, 1], [1, 1]])
    y = concatenated * wo
    eq(y, [[4, 2], [2, 0]])
    a = sp.symbols("a", real=True)
    common = sp.Matrix([[a, 1-a]])
    candidate = (common*v1).row_join(common*v2) * wo
    eq(sp.linsolve(list(candidate-y[0, :]), [a]), sp.EmptySet)
    answer_contains("M12-06", "4&2\\\\2&0", "不存在")


def p07():
    x = sp.Matrix([[0, 2], [2, 4], [4, 6]])
    xx = sp.Matrix([[0, 2], [2, 4], [8, 10]])
    ln1, ln2 = normalize(x[0, :]), normalize(xx[0, :])
    bn1 = sp.Matrix([[normalize(x[:, j].T)[0] for j in range(x.cols)]])
    bn2 = sp.Matrix([[normalize(xx[:, j].T)[0] for j in range(xx.cols)]])
    rms = normalize(x[0, :], center=False)
    eq(ln1, [[-1, 1]])
    eq(bn1, [[-sp.sqrt(sp.Rational(3, 2))]*2])
    eq(bn2, [[-5/sp.sqrt(26)]*2])
    eq(rms, [[0, sp.sqrt(2)]])
    ln_same, bn_same = same(ln1, ln2), same(bn1, bn2)
    choices("M12-07", [not ln_same, bn_same, same(rms, ln1), ln_same and not bn_same],
            [False, False, False, True])


def p08():
    a = sp.symbols("a", positive=True)
    b = sp.symbols("b", real=True)
    output = normalize([b-a, b+a], eps=3)
    target = normalize([-1, 1], eps=3)
    eq(target, [[-sp.Rational(1, 2), sp.Rational(1, 2)]])
    equation = output[1]**2 - target[1]**2
    solutions = sp.solveset(equation, a, domain=sp.Interval.open(0, sp.oo))
    eq(solutions, sp.FiniteSet(1))
    for value in solutions:
        eq(output.subs(a, value), target)
    assert b not in output.free_symbols
    assert not same(output.subs(a, 2), target)
    answer_contains("M12-08", "$a=1$、$b\\in\\mathbb R$")


def p09():
    q = sp.Matrix([1, 0, 1, 0])
    k = sp.Matrix([1, 0, 0, 1])
    changed_k = sp.Matrix([1, 0, 1, 0])
    frequencies = (sp.pi/2, sp.pi/4)

    def transform(position):
        return sp.diag(*(rotation(position*w) for w in frequencies))

    def score(m, n, content):
        return sp.simplify((transform(m)*q).dot(transform(n)*content))

    for m, n in [(1, 3), (4, 6)]:
        eq(tuple((n-m)*w for w in frequencies), (sp.pi, sp.pi/2))
        eq(transform(m).T*transform(n), transform(2))
        eq(transform(2)*k, [-1, 0, -1, 0])
        eq(score(m, n, k), -2)
    eq(transform(2)*changed_k, [-1, 0, 0, 1])
    eq(score(4, 6, changed_k), -1)
    eq(k.norm(), sp.sqrt(2))
    eq(changed_k.norm(), k.norm())
    assert score(1, 3, k) != score(4, 6, changed_k)
    answer_contains("M12-09", "(\\pi,\\pi/2)",
                    "s(4,6;\\boldsymbol k)=-2", "s(4,6;\\widetilde{\\boldsymbol k})=-1",
                    "长度均为 $\\sqrt2$", "判断不成立")


def p10():
    layer_shapes = [(8, 8)] * 4 + [(8, 16)] * 2 + [(16, 8)]
    full_shapes = layer_shapes * 2 + [(10, 8)] * 2
    n = sum(np.prod(shape) for shape in full_shapes)
    wrong = 12*2*8**2 + 10*8
    eq(n, 1440)
    eq(wrong, 1616)
    eq(wrong-n, 176)
    budget = 864000
    tokens = budget // (6*n)
    eq(tokens, 100)
    assert 6*n*tokens <= budget < 6*n*(tokens+1)
    eq(2*n*tokens, 288000)
    eq(4*n*tokens, 576000)
    answer_contains("M12-10", "$N=1440$", "100 个词元", "$288000$", "$576000$")


def p11():
    p, k = sp.symbols("p k", real=True)
    position = lambda x: sp.Matrix([sp.sin(x), sp.cos(x), sp.sin(x/100), sp.cos(x/100)])
    def block(angle):
        return sp.Matrix([[sp.cos(angle), sp.sin(angle)], [-sp.sin(angle), sp.cos(angle)]])
    transform = sp.diag(block(k), block(k/100))
    difference = position(p+k)-transform*position(p)
    assert all(sp.trigsimp(sp.expand_trig(v)) == 0 for v in difference)
    eq(sp.trigsimp(position(p).dot(position(p+k))), sp.cos(k)+sp.cos(k/100))
    answer_contains("M12-11", "\\cos k+\\cos(k/100)")


def p12():
    t = sp.symbols("t", positive=True)
    x = sp.Matrix([[t, 0]])
    z = normalize(x)
    eq(z, [[1, -1]])
    xp = x + z * sp.Matrix([[0, 1], [1, 0]])
    eq(xp, [[t-1, 1]])
    mean = sum(xp)/2
    variance = sp.simplify(sum((v-mean)**2 for v in xp)/2)
    eq(variance, (t-2)**2/4)
    eq(sp.solveset(variance, t, domain=sp.Interval.open(0, sp.oo)), sp.FiniteSet(2))
    second = normalize(xp)
    all_solutions = sp.EmptySet
    for assumption, domain, expected in [
        (sp.Q.negative(t-2), sp.Interval.open(0, 2), [[t-1, 2]]),
        (sp.Q.positive(t-2), sp.Interval.open(2, sp.oo), [[t, 1]]),
    ]:
        zn = second.applyfunc(lambda v: sp.simplify(sp.refine(v, assumption)))
        y = xp + relu(zn)
        eq(y, expected)
        all_solutions |= sp.solveset(sum(y)-4, t, domain=domain)
    eq(all_solutions, sp.FiniteSet(3))
    answer_contains("M12-12", "$t\\ne2$", "(t-1,2)", "(t,1)", "$t=3$")


def p13():
    x, p = np.array([[0.], [2.]]), np.array([[0., 1.], [1., 0.]])
    def attention(values, causal=False):
        s = np.zeros((2, 2))
        if causal:
            s[np.triu_indices(2, 1)] = -np.inf
        return softmax(s) @ values
    u, up, c, cp = attention(x), attention(p@x), attention(x, True), attention(p@x, True)
    close(u, [[1], [1]])
    close(up, [[1], [1]])
    close(c, [[0], [1]])
    close(cp, [[2], [1]])
    close(up, p@u)
    assert not np.allclose(cp, p@c)
    answer_contains("M12-13", "C(X)=(0,1)", "C(PX)=(2,1)", "不成立")


def p14():
    t, c = sp.symbols("t c", real=True)
    e = sp.Matrix([[1, 0], [0, 1], [0, 0]])
    z = sp.Matrix([[t, -t]]) * e.T
    p = symbolic_softmax(z)
    solution = sp.solve(p[0]/p[1]-4, t)
    assert solution == [sp.log(2)]
    actual = p.subs(t, solution[0]).applyfunc(sp.simplify)
    eq(actual, [[sp.Rational(4, 7), sp.Rational(1, 7), sp.Rational(2, 7)]])
    eq(-sp.log(actual[2]), sp.log(sp.Rational(7, 2)))
    shifted = symbolic_softmax(z + sp.ones(1, 3)*c)
    eq(shifted, p)
    answer_contains("M12-14", "$t=\\ln2$", "(4/7,1/7,2/7)", "\\ln(7/2)")


def p15():
    e = np.array([[2., 0.], [0., 2.], [0., 0.]])
    tokens = np.array([1, 2, 3]) - 1
    positions = np.arange(2)
    x0 = e[tokens[:-1]] + np.column_stack((np.sin(positions), np.cos(positions)))
    close(x0, [[2, 1], [np.sin(1), 2+np.cos(1)]])
    def ln(x):
        variance = x.var(axis=1, keepdims=True)
        assert np.all(variance > 0)
        return (x-x.mean(axis=1, keepdims=True))/np.sqrt(variance)
    x = x0.copy()
    for _ in range(2):
        x = x + np.zeros_like(ln(x))
        x = x + np.zeros_like(ln(x))
    h = ln(x)
    z = h @ e.T
    close(h, [[1, -1], [-1, 1]])
    close(z, [[2, -2, 0], [-2, 2, 0]])
    probabilities = softmax(z)
    loss = -np.log(probabilities[np.arange(2), tokens[1:]]).mean()
    mistaken_loss = -np.log(probabilities[np.arange(2), tokens[:-1]]).mean()
    s = np.exp(2) + np.exp(-2) + 1
    close(loss, np.log(s)+1)
    close(mistaken_loss, np.log(s)-2)
    close(loss, 3.1429, atol=0.00005)
    close(mistaken_loss, 0.1429, atol=0.00005)
    close(loss-mistaken_loss, 3)
    answer_contains("M12-15", "\\ln S+1", "\\ln S-2", "少算了 3")


def check_document_structure():
    ids = re.findall(r"^\*\*(M12-\d+)\*\*", PROBLEMS, re.M)
    assert ids == [f"M12-{i:02d}" for i in range(1, 16)]
    assert set(PARTS) == set(ids)
    limits = {"A": 400, "B": 900, "C": 1400}
    tiers = dict(re.findall(r"\*\*(M12-\d+)\*\*〔([ABC])", PROBLEMS))
    for pid, body in PARTS.items():
        body = body.split("\n### ")[0]
        assert len(body) <= limits[tiers[pid]], (pid, len(body))


if __name__ == "__main__":
    check_document_structure()
    for number in range(1, 16):
        run(f"M12-{number:02d}", globals()[f"p{number:02d}"], manual=(number == 11))
    sys.exit(bool(FAILURES))
