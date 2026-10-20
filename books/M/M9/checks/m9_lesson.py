"""Independently check all numbered examples and their adjacent numerical exercises."""

from pathlib import Path
import re
import sys

import numpy as np
import sympy as sp


failures = 0
corpus = [[0, 2, 4], [0, 3, 6], [1, 2, 5], [1, 3, 7], [1, 2, 4]]
ROOT = Path(__file__).resolve().parents[1]
LESSON = (ROOT / "lesson.md").read_text(encoding="utf-8")
BLOCKS = dict(re.findall(r"\*\*例 (\d+)\*\*(.*?)(?=\*\*例 \d+\*\*|\Z)", LESSON, re.S))
rounding_notes = {}


def close(actual, expected, digits=4):
    a, b = np.asarray(actual, dtype=float), np.asarray(expected, dtype=float)
    assert a.shape == b.shape, (a.shape, b.shape)
    assert np.allclose(a, b, atol=0.5 * 10 ** (-digits) + 1e-12, rtol=0), (a, b)


def exact(actual, expected):
    assert np.array_equal(np.asarray(actual), np.asarray(expected)), (actual, expected)


def softmax(z):
    z = np.asarray(z, dtype=float)
    e = np.exp(z - z.max())
    return e / e.sum()


def cos(a, b):
    return np.dot(a, b) / np.linalg.norm(a) / np.linalg.norm(b)


def recorded_rounding(number, actual, old, corrected, digits):
    # 早期稿先舍入再相加得到 old，讲义已改为全精度舍入的 corrected；两者都显式核对，不靠放宽容差
    assert corrected in BLOCKS[str(number)]
    assert f"{actual:.{digits}f}" == corrected
    assert abs(actual - float(old)) > 0.5 * 10 ** (-digits)
    rounding_notes[number] = f"全精度舍入为 {corrected}，不是先舍入再相加的 {old}"


def cooccurrence(sentences, size=8, radius=1):
    X = np.zeros((size, size), dtype=int)
    for sentence in sentences:
        for i, center in enumerate(sentence):
            for j, context in enumerate(sentence):
                if 0 < abs(i - j) <= radius:
                    X[center, context] += 1
    return X


def example1():
    O = np.eye(8, dtype=int)[corpus[0]]
    exact(O.shape, (3, 8))
    exact(O @ O.T, np.eye(3, dtype=int))
    exact(O.T @ O, np.diag([1, 0, 1, 0, 1, 0, 0, 0]))
    short = np.eye(5, dtype=int)[[2, 0, 2]]
    exact(short.T @ short, np.diag([1, 0, 2, 0, 0]))
    for i in range(8):
        for j in range(8):
            if i != j:
                close(np.linalg.norm(np.eye(8)[i] - np.eye(8)[j]), np.sqrt(2), 12)


def example2():
    X = cooccurrence(corpus)
    expected = [[0, 0, 1, 1, 0, 0, 0, 0], [0, 0, 2, 1, 0, 0, 0, 0],
                [1, 2, 0, 0, 2, 1, 0, 0], [1, 1, 0, 0, 0, 0, 1, 1],
                [0, 0, 2, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0]]
    exact(X, expected)
    close(cos(X[0], X[1]), 3 / np.sqrt(10), 12)
    close(cos(X[0], X[1]), 0.9487)
    augmented = cooccurrence(corpus + [[0, 2, 5]])
    close(cos(augmented[0], augmented[1]), 1, 12)


def example3():
    X = cooccurrence(corpus)
    close([cos(X[4], X[5]), cos(X[4], X[6]), cos(X[0], X[4])], [1, 0, 0.7071])


def example4():
    rows = {0: [1., .2], 1: [.9, .4], 2: [-.5, .8], 4: [.1, -.9]}
    E = np.zeros((8, 2))
    for index, row in rows.items():
        E[index] = row
    exact(np.eye(8)[corpus[0]] @ E, [[1., .2], [-.5, .8], [.1, -.9]])
    close([cos(E[0], E[1]), cos(E[0], E[4])], [.976, -.087], 3)
    exact(30000 * 256, 7680000)
    exact((np.zeros((10, 30000)) @ np.zeros((30000, 256))).shape, (10, 256))
    exact(50000 * 300, 15000000)
    X = cooccurrence(corpus)
    left, singular, right = np.linalg.svd(X)
    exact(np.linalg.matrix_rank(X), 4)
    close(singular[:4], [3.35, 3.35, 1.66, 1.66], 2)
    reduced = left[:, :4] * singular[:4]
    close(reduced @ right[:4], X, 10)
    close(reduced @ reduced.T, X @ X.T, 10)
    for i in range(8):
        for j in range(8):
            close(cos(reduced[i], reduced[j]), cos(X[i], X[j]), 10)


def example5():
    U = np.array([[1., 1.], [1., 0.], [1., -1.]])
    z = U @ np.ones(2)
    exact(z, [2, 1, 0])
    close(np.exp(z), [7.389, 2.718, 1.], 3)
    close(np.exp(z).sum(), 11.107, 3)
    p = softmax(z)
    close(p, [.6652, .2447, .0900])
    close(-np.log(p[0]), .4076)
    close(np.log(np.exp(z).sum()), 2.4076)
    close(-np.log(p[2]), 2.408, 3)
    exact(cooccurrence(corpus).sum(), 20)


def example6():
    # Count ordered position pairs directly, independently of the boundary formula.
    counts = [sum(0 < abs(i - j) <= 2 for j in range(10)) for i in range(10)]
    exact(counts, [2, 3, 4, 4, 4, 4, 4, 4, 3, 2])
    exact(sum(counts), 34)


def example7():
    x, y = sp.symbols("x y", real=True)
    symbols = sp.symbols("u0:6", real=True)
    U = sp.Matrix(3, 2, symbols)
    v = sp.Matrix([x, y])
    z = U * v
    loss = -z[0] + sp.log(sum(sp.exp(a) for a in z))
    point = dict(zip(symbols, [1, 1, 1, 0, 1, -1])) | {x: 1, y: 1}
    gv = np.array([float(sp.diff(loss, s).subs(point)) for s in [x, y]])
    gu = np.array([float(sp.diff(loss, s).subs(point)) for s in symbols]).reshape(3, 2)
    close(gv, [0, -.4248])
    close(gu, [[-.3348, -.3348], [.2447, .2447], [.0900, .0900]])
    p = softmax(np.array([2., 1., 0.]))
    close(p - [1, 0, 0], [-.3348, .2447, .0900])
    close(p @ np.array([[1, 1], [1, 0], [1, -1]]), [1, .5752])
    vn = np.ones(2) - gv
    un = np.array([[1., 1.], [1., 0.], [1., -1.]]) - gu
    close(vn, [1, 1.4248])
    close(un, [[1.3348, 1.3348], [.7553, -.2447], [.9100, -1.0900]])
    pn = softmax(un @ vn)
    close(pn, [.9262, .0547, .0191])
    close(-np.log(pn[0]), .0767)
    assert -np.log(pn[0]) < float(loss.subs(point))
    other_loss = loss + z[0] - z[2]
    close([float(sp.diff(other_loss, s).subs(point)) for s in [x, y]], [0, 1.5752])


def example8():
    x, y = sp.symbols("x y", real=True)
    v = sp.Matrix([x, y])
    vectors = [sp.Matrix([1, 1]), sp.Matrix([1, -1]), sp.Matrix([0, -1])]
    scores = [u.dot(v) for u in vectors]
    point = {x: 1, y: 1}
    exact([score.subs(point) for score in scores], [2, 0, -1])
    terms = [sp.log(1 + sp.exp(-scores[0]))] + [sp.log(1 + sp.exp(s)) for s in scores[1:]]
    values = [float(term.subs(point)) for term in terms]
    close(values, [.1269, .6931, .3133])
    close(sum(values), 1.1333)
    loss = sum(terms)
    gradient = np.array([float(sp.diff(loss, s).subs(point)) for s in [x, y]])
    close(gradient, [.3808, -.8881])
    sigmoid = lambda a: 1 / (1 + np.exp(-a))
    close([sigmoid(2) - 1, sigmoid(0), sigmoid(-1)], [-.1192, .5, .2689])
    close(sum(values[:2]), .8201)
    recorded_rounding(8, sum(values[:2]), "0.8200", "0.8201", 4)
    assert np.dot(-gradient, [1, 1]) > 0
    assert np.dot(-gradient, [1, -1]) < 0
    assert np.dot(-gradient, [0, -1]) < 0


def example9():
    frequency = np.bincount(np.concatenate(corpus), minlength=8)
    exact(frequency, [2, 3, 3, 2, 2, 1, 1, 1])
    exact(frequency.sum(), 15)
    weights = frequency ** .75
    close([3 ** .75, 2 ** .75], [2.2795, 1.6818])
    close(weights.sum(), 12.604, 3)
    p = weights / weights.sum()
    raw = frequency / frequency.sum()
    close(p[[1, 7]], [.1809, .0793])
    close(raw[[1, 7]], [.2, .0667])
    assert p[1] < raw[1] and p[7] > raw[7]


def example10():
    vectors = np.array([[.9, 2.1], [-1.1, 1.9], [1., .1], [-1., 0.], [.8, 1.2], [-.9, 1.1], [.1, -1.5]])
    q = vectors[0] - vectors[2] + vectors[3]
    close(q, [-1.1, 2.], 12)
    similarities = np.array([cos(q, v) for v in vectors])
    close(similarities[[1, 5, 4, 6, 0]], [.9998, .9833, .4617, -.9063, .6155])
    allowed = [i for i in range(len(vectors)) if i not in [0, 2, 3]]
    assert max(allowed, key=lambda i: similarities[i]) == 1


def example11():
    S = np.array([[.8, .1, .3], [.2, .7, .0], [.1, .2, .9]])
    z = S / .5
    close(z[0], [1.6, .2, .6], 12)
    close(np.exp(z[0]), [4.953, 1.221, 1.822], 3)
    # Keep intermediate values at full precision; only the final displayed sum is rounded.
    close(np.round(np.exp(z[0]), 3).sum(), 7.996, 12)
    close(np.exp(z[0]).sum(), 7.997, 3)
    assert "7.997" in BLOCKS["11"]
    rows = np.logaddexp.reduce(z, axis=1) - np.diag(z)
    cols = np.logaddexp.reduce(z, axis=0) - np.diag(z)
    close(softmax(z[0])[0], .6194)
    close(rows, [.4790, .4790, .3705])
    close(rows.mean(), .4428)
    close(cols.mean(), .4440)
    close((rows.mean() + cols.mean()) / 2, .4434)
    close(-np.log(softmax(np.zeros(3))[0]), 1.0986)
    colder = softmax(S[0] / .1)[0]
    close(colder, .9924)
    assert colder > softmax(z[0])[0]


if __name__ == "__main__":
    examples = [example1, example2, example3, example4, example5, example6,
                example7, example8, example9, example10, example11]
    for number, check in enumerate(examples, 1):
        try:
            check()
            suffix = f"（{rounding_notes[number]}）" if number in rounding_notes else ""
            print(f"PASS 例{number}{suffix}")
        except Exception as exc:
            failures += 1
            print(f"FAIL 例{number}: {type(exc).__name__}: {exc}")
    sys.exit(1 if failures else 0)
