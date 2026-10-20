"""Independently verify all nine numbered examples and nearby calculations.

Rounded decimal claims use half a unit in the last printed place.
The regression split tie is a documented source error, not silently passed.
"""
from pathlib import Path
import re
import sys

import numpy as np
import sympy as sp

R = sp.Rational
ROOT = Path(__file__).resolve().parents[1]
LESSON = (ROOT / "lesson.md").read_text(encoding="utf-8")


def exact(actual, expected):
    if isinstance(actual, (list, tuple, sp.MatrixBase)):
        assert len(actual) == len(expected)
        for a, b in zip(actual, expected):
            exact(a, b)
    else:
        assert sp.simplify(actual-expected) == 0, (actual, expected)


def approx(actual, expected, digits=3):
    a, e = np.asarray(actual, dtype=float), np.asarray(expected, dtype=float)
    assert a.shape == e.shape
    assert np.all(np.abs(a-e) <= .5*10**(-digits)+1e-12), (a, e)


def H(y):
    _, counts = np.unique(y, return_counts=True)
    p = counts / sum(counts)
    return -sum(p*np.log2(p))


def ig(x, y):
    return H(y)-sum(np.mean(x == v)*H(y[x == v]) for v in np.unique(x))


def stump(residual):
    n = len(residual)
    candidates = []
    for k in range(1, n):
        left = sum(residual[:k])/k
        right = sum(residual[k:])/(n-k)
        fit = [left]*k+[right]*(n-k)
        error = sp.simplify(sum((r-h)**2 for r, h in zip(residual, fit)))
        candidates.append((error, k, sp.Matrix(fit)))
    return min(candidates, key=lambda item: (item[0], item[1])), candidates


def cov_average(n, v, r):
    cov = sp.eye(n)*v*(1-r)+sp.ones(n)*v*r
    w = sp.ones(n, 1)/n
    return (w.T*cov*w)[0]


def ex1():
    points = np.array([[1, 1], [2, 1], [1, 3], [2, 2], [5, 4],
                       [4, 4], [5, 5], [4, 5], [6, 4]], dtype=float)
    labels = np.array([0, 0, 0, 0, 0, 1, 1, 1, 1])
    dist = np.linalg.norm(points-[4.6, 4.2], axis=1)
    order = np.argsort(dist)
    assert order[:6].tolist() == [4, 5, 6, 7, 8, 3]
    approx(dist[order[:6]], [.447, .632, .894, 1, 1.414, 3.406])
    votes = [int(sum(labels[order[:k]]) > k/2) for k in [1, 3, 5, 9]]
    assert votes == [0, 1, 1, 0]  # Circle = 0, square = 1.
    close = np.argsort(np.linalg.norm(points-[1.5, 1.5], axis=1))[:3]
    assert set(close) == {0, 1, 3} and np.all(labels[close] == 0)


def ex2():
    q = np.array([1., 2.])
    c = np.array([[2, 1], [1, 3], [-1, 1], [4, 1], [5, 10]], dtype=float)
    dist = np.linalg.norm(c-q, axis=1)
    cos = c@q / (np.linalg.norm(c, axis=1)*np.linalg.norm(q))
    approx(dist, [1.414, 1., 2.236, 3.162, 8.944])
    approx(cos, [.800, .990, .316, .651, 1.])
    assert (np.argsort(dist)[:2]+1).tolist() == [2, 1]
    assert (np.argsort(-cos)[:2]+1).tolist() == [5, 2]
    normdist = np.linalg.norm(c/np.linalg.norm(c, axis=1)[:, None]-q/np.linalg.norm(q), axis=1)
    assert np.allclose(normdist**2, 2-2*cos)
    assert (np.argsort(normdist)[:2]+1).tolist() == [5, 2]


def ex3():
    shell = 1-R(9, 10)**20
    approx(float(shell), .878)
    approx(float(shell)*100, 87.8, 1)
    w = sp.symbols("w")
    e2 = sp.integrate(2*w**2*(1-w), (w, 0, 1))
    e4 = sp.integrate(2*w**4*(1-w), (w, 0, 1))
    exact([e2, e4, e4-e2**2], [R(1, 6), R(1, 15), R(7, 180)])
    cv = sp.sqrt(400*(e4-e2**2))/(400*e2)
    approx(float(cv), .059)
    approx(float(1-R(98, 100)**50), .636)


# Columns: binary features X1, X2, X3; label: Y.
X = np.array([[1, 1, 0], [1, 1, 0], [1, 0, 1], [1, 0, 0],
              [0, 1, 0], [0, 1, 1], [0, 1, 1], [0, 0, 0],
              [0, 0, 0], [0, 0, 0]])
Y = np.array([1, 1, 1, 0, 1, 0, 0, 0, 0, 0])


def ex4():
    approx(H(Y), .971)
    gains = np.array([ig(X[:, j], Y) for j in range(3)])
    approx(gains, [.256, .125, .006])
    approx(H(Y)-gains, [.715, .846, .965])
    assert np.argmax(gains) == 0
    subset = X[:, 0] == 1
    approx(H(Y[subset]), .811)
    approx([ig(X[subset, j], Y[subset]) for j in [1, 2]], [.311, .123])


def tree(x, y, features):
    if np.all(y == y[0]):
        return int(y[0])
    j = max(features, key=lambda c: ig(x[:, c], y))
    children = {}
    for value in np.unique(x[:, j]):
        mask = x[:, j] == value
        children[int(value)] = tree(x[mask], y[mask], [c for c in features if c != j])
    return j, children


def predict(t, row):
    if isinstance(t, int):
        return t
    j, children = t
    return predict(children[row[j]], row)


def ex5():
    built = tree(X, Y, [0, 1, 2])
    expected = (0, {0: (1, {0: 0, 1: (2, {0: 1, 1: 0})}),
                    1: (1, {0: (2, {0: 0, 1: 1}), 1: 1})})
    assert built == expected
    assert [predict(built, row) for row in X] == Y.tolist()
    assert predict(built, [0, 1, 0]) == 1
    assert ig(np.arange(10), Y) == H(Y)


def ex6():
    values = [cov_average(n, 4, R(1, 2)) for n in [1, 10, 100]]
    exact(values, [4, R(11, 5), R(101, 50)])
    exact(cov_average(100, 4, R(1, 5)), R(104, 125))
    b = sp.symbols("b", positive=True)
    expression = (4*b+2*b*(b-1))/b**2
    exact(sp.limit(expression, b, sp.oo), 2)
    assert sp.simplify(expression-2).is_positive


def ex7():
    vbag = cov_average(100, 1, R(7, 10))
    vrf = cov_average(100, R(6, 5), R(3, 10))
    approx([float(vbag), float(vrf)], [.703, .368])
    assert vrf < vbag
    # Sum covariance entries by their counts for 10000 trees.
    big = (10000+10000*9999*R(7, 10))/10000**2
    approx(float(big), .7000, 4)
    assert big > vrf


def ex8():
    y = sp.Matrix([0, 0, 1, 0, 1])
    f = sp.symbols("f", real=True)
    p = 1/(1+sp.exp(-f))
    loss = sum(-yi*sp.log(p)-(1-yi)*sp.log(1-p) for yi in y)
    f0 = sp.log(R(2, 3))
    exact(sp.simplify(sp.diff(loss, f).subs(f, f0)), 0)
    assert sp.simplify(sp.diff(loss, f, 2).subs(f, f0)) > 0
    g = y-sp.ones(5, 1)*R(2, 5)
    exact(g, [-R(2, 5), -R(2, 5), R(3, 5), -R(2, 5), R(3, 5)])
    best, candidates = stump(g)
    error, cut, h = best
    assert cut == 2 and all(error < c[0] for c in candidates if c[1] != cut)
    exact(error, R(2, 3))
    f1 = sp.ones(5, 1)*f0+h/2
    approx([float(f1[0]), float(f1[2])], [-.605, -.272])
    probs = [float(1/(1+sp.exp(-v))) for v in [f1[0], f1[2]]]
    approx(probs, [.353, .432])
    assert probs[0] < .4 < probs[1]
    split = R(2*cut+1, 2)
    function = sp.Piecewise((f1[0], f <= split), (f1[-1], True))
    exact([function.subs(f, x) for x in [R(9, 4), R(5, 2), R(11, 4)]],
          [f0-R(1, 5), f0-R(1, 5), f0+R(2, 15)])
    assert r"x\le2.5" in LESSON and "x>2.5" in LESSON
    assert r"\ln\frac23-\frac15" in LESSON and r"\ln\frac23+\frac2{15}" in LESSON


def ex9():
    x = sp.Matrix([1, 2, 3, 10, 11])
    centers = [sp.Integer(2), sp.Integer(3)]
    values, groups_seen = [], []
    last = None
    for _ in range(10):
        assignment = [min(range(2), key=lambda j: (v-centers[j])**2) for v in x]
        if assignment == last:
            break
        groups_seen.append(assignment)
        values.append(sum((v-centers[c])**2 for v, c in zip(x, assignment)))
        centers = [sum(v for v, c in zip(x, assignment) if c == j)/assignment.count(j) for j in range(2)]
        values.append(sum((v-centers[c])**2 for v, c in zip(x, assignment)))
        last = assignment
    else:
        raise AssertionError("iteration did not stop")
    exact(values, [114, R(77, 2), R(63, 4), R(5, 2)])
    assert groups_seen == [[0, 0, 1, 1, 1], [0, 0, 0, 1, 1]]
    exact(centers, [2, R(21, 2)])
    initial = [sp.Integer(1), sp.Integer(2)]
    a = [min(range(2), key=lambda j: (v-initial[j])**2) for v in x]
    updated = [sum(v for v, c in zip(x, a) if c == j)/a.count(j) for j in range(2)]
    exact(updated, [1, R(13, 2)])


def regression():
    y = sp.Matrix([2, 3, 5, 6, 9])
    f = sp.ones(5, 1)*sum(y)/5
    errors = [sum((y-f).applyfunc(lambda v: v*v))/5]
    results, splits = [], []
    for _ in range(3):
        best, candidates = stump(y-f)
        splits.append(best[1])
        if len(results) == 0:
            ties = [cut for err, cut, _ in candidates if err == best[0]]
            assert ties == [2, 3]
            exact(candidates[1][0], R(55, 6))
        f = f+best[2]/2
        results.append(f)
        errors.append(sum((y-f).applyfunc(lambda v: v*v))/5)
    assert splits == [2, 4, 3]
    approx([float(v) for v in errors], [6, 2.875, .995, .419])
    approx([float(v) for v in results[1]], [3.354, 3.354, 5.438, 5.438, 7.417])
    residual = y-sp.ones(5, 1)*5
    h = sp.Matrix([sum(residual[:3])/3]*3+[sum(residual[3:])/2]*2)
    exact(sp.ones(5, 1)*5+h, [R(10, 3)]*3+[R(15, 2)]*2)
    # x=2.5 与 x=3.5 两种切分的平方误差同为 55/6，讲义不能说其中一种「平方误差更大」
    assert "分在其他位置，平方误差更大" not in LESSON


def distance_simulation():
    rng = np.random.default_rng(20261017)
    ratios = []
    for dimension in [2, 10, 100, 1000]:
        query = rng.random(dimension)
        points = rng.random((2000, dimension))
        distances = np.linalg.norm(points-query, axis=1)
        ratios.append(distances.min()/distances.max())
    row = re.search(r"^\| 最近 ÷ 最远 \|(.+)\|$", LESSON, re.M)
    assert row is not None
    printed = [value.strip() for value in row[1].split("|")]
    assert len(printed) == len(ratios)
    for actual, value in zip(ratios, printed):
        approx(actual, float(value), len(value.split(".")[1]))


def other_examples():
    # Unnumbered dimension, bootstrap, random-feature, and local-minimum examples.
    ds = np.array([2, 10, 50, 100])
    shell_percent = 100*(1-.95**ds)
    approx(shell_percent[0], 9.75, 2)
    approx(shell_percent[1:], [40.1, 92.3, 99.4], 1)
    sides = .01**(1/np.array([2., 10., 100.]))
    approx(sides[:2], [.10, .63], 2)
    approx(sides[2], .955, 3)
    approx(float(R(4, 5)**5), .328)
    approx(float(1-R(4, 5)**5)*100, 67.2, 1)
    exact(R(sp.binomial(8, 2), sp.binomial(9, 3)), R(1, 3))
    x = np.array([[0, 0], [4, 0], [0, 2], [4, 2]])
    js = []
    for centers in [np.array([[0, 1], [4, 1]]), np.array([[2, 0], [2, 2]])]:
        squared = ((x[:, None, :]-centers[None, :, :])**2).sum(axis=2)
        a = squared.argmin(axis=1)
        updated = np.array([x[a == j].mean(axis=0) for j in range(2)])
        assert np.array_equal(centers, updated)
        js.append(squared[np.arange(4), a].sum())
    assert js == [4, 16]


if __name__ == "__main__":
    assert set(map(int, re.findall(r"\*\*例 (\d+)\*\*", LESSON))) == set(range(1, 10))
    checks = [(f"例{i}", globals()[f"ex{i}"]) for i in range(1, 10)]
    regression_label = "例8前回归（数值及分裂并列情况）"
    if "分在其他位置，平方误差更大" in LESSON:
        regression_label += " 原文遗漏2.5与3.5并列最优，已记讲义错误"
    checks += [(regression_label, regression), ("距离模拟（种子20261017、2000点）", distance_simulation),
               ("例外补充（未编号的数值例子）", other_examples)]
    failed = 0
    for label, run in checks:
        try:
            run()
            print(f"PASS {label}")
        except Exception as exc:
            failed += 1
            print(f"FAIL {label} {type(exc).__name__}: {exc}")
    sys.exit(bool(failed))
