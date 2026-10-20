"""Recompute from problem data; expected values are transcribed from answers.md.

No stochastic tests. Symbolic inequalities check entire parameter ranges.
Answer anchors and the selected letters are also checked against the actual file.
"""
from itertools import product
from pathlib import Path
import re
import sys

import numpy as np
import sympy as sp

R = sp.Rational
ROOT = Path(__file__).resolve().parents[1]
ANS = (ROOT / "answers.md").read_text(encoding="utf-8")
PROBS = (ROOT / "problems.md").read_text(encoding="utf-8")
blocks = dict(re.findall(r"\*\*(M4-\d+)\*\*\n(.*?)(?=\n\*\*M4-|\Z)", ANS, re.S))
failed = 0


def eq(actual, expected):
    if isinstance(actual, (list, tuple, sp.MatrixBase, np.ndarray)):
        a, b = list(actual), list(expected)
        assert len(a) == len(b), (a, b)
        for x, y in zip(a, b):
            eq(x, y)
    else:
        assert sp.simplify(actual - expected) == 0, (actual, expected)


def anchors(pid, *items):
    for item in items:
        assert item in blocks[pid], (pid, "answer text differs", item)


def choices(pid, truth):
    chosen = re.search(r"\*\*答案：\*\* \(([A-D])\)", blocks[pid])[1]
    assert sum(bool(v) for v in truth) == 1
    for letter, value in zip("ABCD", truth):
        assert bool(value) == (letter == chosen), (pid, letter, value)
        assert f"({letter})" in blocks[pid]
        print(f"PASS {pid} 选项{letter}")


def entropy(values):
    _, counts = np.unique(values, return_counts=True)
    p = counts / counts.sum()
    return -np.sum(p * np.log2(p))


def gain(x, y):
    x, y = np.asarray(x), np.asarray(y)
    return entropy(y) - sum(np.mean(x == v) * entropy(y[x == v]) for v in np.unique(x))


def variance(n, sigma2, rho):
    # Sum the covariance matrix, independently of the simplified formula.
    cov = sp.ones(n) * sigma2 * rho + sp.eye(n) * sigma2 * (1 - rho)
    return sp.simplify(sum(cov) / n**2)


def leaf_fit(residual, groups):
    out = sp.zeros(len(residual), 1)
    for g in groups:
        avg = sum(residual[i] for i in g) / len(g)
        for i in g:
            out[i] = avg
    return out


def mse(y, f):
    return sp.expand(sum((a-b)**2 for a, b in zip(y, f)) / len(y))


def p01():
    x = np.array([-1, 2, 3, 5, 8])
    y = np.array([0, 1, 1, 0, 0])
    order = np.argsort(np.abs(x))
    vote = lambda idx: int(y[idx].sum() > len(idx) / 2)
    k3, k5 = vote(order[:3]), vote(order[:5])
    sq3 = vote(np.argsort(x*x)[:3])
    choices("M4-01", [k3 == 0, k3 == 1, k5 == 1, sq3 != k3])
    eq([k3, k5], [1, 0])


def p02():
    y = [1, 1, 1, 1, 0, 0, 0, 0]
    x = [0, 0, 1, 1, 1, 1, 1, 1]
    h = entropy(y[2:])
    ig = gain(x, y)
    candidates = [1-h/2, 3*h/4, 1-3*h/4, 1]
    choices("M4-02", [np.isclose(ig, c, atol=1e-12) for c in candidates])
    assert abs(ig - .3113) < .00005
    anchors("M4-02", "0.3113", r"\frac68H(\frac13)")


def p03():
    d = 1
    while 1-R(3, 4)**d < R(3, 4):
        d += 1
    eq(d, 5)
    assert 1-R(3, 4)**(d-1) < R(3, 4)
    anchors("M4-03", "$d=5$", r"\frac{243}{1024}")


def p04():
    eta = sp.symbols("eta", real=True)
    f, h = sp.ones(2, 1), sp.Matrix([-1, 3])
    record = sp.Matrix([R(1, 2), R(5, 2)])
    equations = list(f + eta*h - record)
    solution = sp.solve(equations, eta)
    eq(solution[eta], R(1, 2))
    truth = [all(e.subs(eta, step) == 0 for e in equations)
             for step in [R(1, 4), R(1, 2), 1]]
    choices("M4-04", truth + [not bool(solution)])
    other = list(f + eta*h - sp.Matrix([R(1, 2), 3]))
    eq([sp.solve(e, eta)[0] for e in other], [R(1, 2), R(2, 3)])
    assert sp.solve(other, eta) == []
    anchors("M4-04", r"\eta=\frac12", "不存在共同解")


def p05():
    m = sp.symbols("m", real=True)
    j = sum((x-m)**2 for x in [0, 2, 7])
    center = sp.solve(sp.diff(j, m), m)[0]
    eq([center, j.subs(m, center), j.subs(m, 2), j.subs(m, 2)-j.subs(m, center)], [3, 26, 29, 3])
    assert sp.diff(j, m, 2) > 0
    anchors("M4-05", "最优中心为 3", "$3$", "3(\\mu-3)^2+26")


def p06():
    s = sp.symbols("s", real=True)
    a, b = sp.Matrix([s, 3]), sp.Matrix([3*s, 1])
    da, db = a.dot(a), b.dot(b)
    feasible = sp.reduce_inequalities([s > 0, db < da], s).as_set()
    assert feasible == sp.Interval.open(0, 1)
    eq([da.subs(s, R(1, 2)), db.subs(s, R(1, 2)), da.subs(s, 2), db.subs(s, 2)], [R(37, 4), R(13, 4), 13, 37])
    assert da.subs(s, 1) == db.subs(s, 1)
    anchors("M4-06", "$0<s<1$", "预测从 1 变成 0")


def p07():
    # The first bound follows from monotonicity of (1/2)**d.
    boundary = sp.log(R(1, 64)) / sp.log(R(1, 2))
    eq(boundary, 6)
    w = sp.symbols("w", real=True)
    e2 = sp.integrate(2*w**2*(1-w), (w, 0, 1))
    e4 = sp.integrate(2*w**4*(1-w), (w, 0, 1))
    cv2_coefficient = sp.simplify((e4-e2**2)/e2**2)
    minimum_d = sp.ceiling(cv2_coefficient / R(1, 10)**2)
    eq(minimum_d, 140)
    assert sp.Interval(1, boundary).intersect(sp.Interval(minimum_d, sp.oo)) == sp.EmptySet
    anchors("M4-07", "$1\\le d\\le6$", "$d\\ge140$", "没有同时满足")


def p08():
    X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    y = np.array([0, 1, 1, 0])
    assert np.allclose([gain(X[:, j], y) for j in range(2)], [0, 0])
    assert np.mean(y != 0) == .5
    pred = np.empty(4, dtype=int)
    for v in [0, 1]:
        mask = X[:, 0] == v
        assert gain(X[mask, 1], y[mask]) == 1
        for u in [0, 1]:
            leaf = mask & (X[:, 1] == u)
            assert entropy(y[leaf]) == 0
            pred[leaf] = y[leaf][0]
    assert np.mean(pred != y) == 0
    anchors("M4-08", "两个根节点增益都为 0", "错误率为 0", r"(1,0)\mapsto1")


def p09():
    v, r = sp.symbols("v r", real=True)
    solution = sp.solve([variance(2, v, r)-R(5, 2), variance(5, v, r)-R(8, 5)], [v, r], dict=True)[0]
    eq([solution[v], solution[r]], [4, R(1, 4)])
    b = sp.symbols("B", positive=True)
    # Count diagonal and off-diagonal entries for arbitrary tree count.
    vb = sp.simplify((b*solution[v]+b*(b-1)*solution[v]*solution[r])/b**2)
    eq(vb, 1+3/b)
    bound = sp.solve(sp.Eq(vb, R(6, 5)), b)[0]
    eq(bound, 15)
    assert variance(14, 4, R(1, 4)) > R(6, 5)
    assert variance(15, 4, R(1, 4)) == R(6, 5)
    assert sp.ask(sp.Q.positive(sp.simplify(vb-1)))
    eq(sp.limit(vb, b, sp.oo), 1)
    anchors("M4-09", r"\sigma^2=4", r"\rho=\frac14", "至少 15 棵", "有限棵树不能")


def p10():
    y = sp.Matrix([0, 2, 4, 6])
    f0 = sp.ones(4, 1)*sum(y)/4
    groups = [[0, 1], [2, 3]]
    h1 = leaf_fit(y-f0, groups)
    f1 = f0+h1/2
    r2 = y-f1
    h2 = leaf_fit(r2, groups)
    f2 = f1+h2/2
    eq(h1, [-2, -2, 2, 2])
    eq(f1, [2, 2, 4, 4])
    eq(r2, [-2, 0, 0, 2])
    eq(h2, [-1, -1, 1, 1])
    eq(f2, [R(3, 2), R(3, 2), R(9, 2), R(9, 2)])
    eq(mse(y, f2), R(5, 4))
    eq(f1+h1/2, [1, 1, 5, 5])
    assert h1 != h2
    anchors("M4-10", "h_2=(-1,-1,1,1)", r"\frac54", "不符合题设规则")


def p11():
    alpha = sp.symbols("alpha", real=True)
    points = [0, 2]
    old_center = sp.Integer(0)
    mean = R(sum(points), len(points))
    new_center = (1-alpha)*old_center + alpha*mean
    old_j = sum((x-old_center)**2 for x in points)
    new_j = sp.expand(sum((x-new_center)**2 for x in points))
    eq(old_j, 4)
    eq(new_j-old_j, 2*alpha*(alpha-2))
    assert sp.solve_univariate_inequality(new_j <= old_j, alpha, relational=False) == sp.Interval(0, 2)
    assert sp.solve_univariate_inequality(new_j > old_j, alpha, relational=False) == sp.Union(
        sp.Interval.open(-sp.oo, 0), sp.Interval.open(2, sp.oo))
    eq([new_j.subs(alpha, a) for a in [-1, 0, 1, 2, 3]], [10, 4, 2, 4, 10])
    anchors("M4-11", r"0\le\alpha\le2", r"2\alpha(\alpha-2)")


def p12():
    t = sp.symbols("t", real=True)
    x = [sp.Integer(0), sp.Integer(2), sp.Integer(3), t]
    mu = [(x[0]+x[1])/2, (x[2]+x[3])/2]
    strict = [(x[i]-mu[int(i >= 2)])**2 < (x[i]-mu[int(i < 2)])**2 for i in range(4)]
    stable = sp.reduce_inequalities([t > 3]+strict, t).as_set()
    assert stable == sp.Interval.open(3, 7)
    alt = [sum(x[:3])/3, t]
    js = sum((v-mu[int(i >= 2)])**2 for i, v in enumerate(x))
    jt = sum((v-alt[int(i >= 3)])**2 for i, v in enumerate(x))
    worse = sp.reduce_inequalities([t > 3, js > jt], t).as_set().intersect(stable)
    assert worse == sp.Interval.open(3+4/sp.sqrt(3), 7)
    eq([m.subs(t, 6) for m in mu+alt], [1, R(9, 2), R(5, 3), 6])
    eq([js.subs(t, 6), jt.subs(t, 6)], [R(13, 2), R(14, 3)])
    assert js.subs(t, 6) > jt.subs(t, 6)
    anchors("M4-12", "$3<t<7$", r"3+\frac4{\sqrt3}<t<7", r"\frac{13}2", r"\frac{14}3")


def p13():
    eta = sp.symbols("eta", real=True)
    y = sp.Matrix([-2, 0, 4, 6])
    f = sp.ones(4, 1)*2
    h = leaf_fit(y-f, [[0, 1], [2, 3]])
    eq(h, [-3, -3, 3, 3])
    loss = mse(y, f+eta*h)
    eq(loss, 1+9*(1-eta)**2)
    assert sp.solve_univariate_inequality(loss < mse(y, f), eta, relational=False) == sp.Interval.open(0, 2)
    opt = sp.solve(sp.diff(loss, eta), eta)[0]
    eq([opt, loss.subs(eta, opt)], [1, 1])
    assert sp.diff(loss, eta, 2) > 0
    eq(y-(f+h), [-1, 1, -1, 1])
    free_loss = mse(y, f+eta*(y-f))
    eq(sp.solve(free_loss, eta), [1])
    anchors("M4-13", "1+9(1-\\eta)^2", "$0<\\eta<2$", "最小均方误差为 1")


def p14():
    # Exhaustively enumerate all bootstrap draws, rather than reuse the formula.
    draws = list(product(range(4), repeat=4))
    absent = sum(0 not in d for d in draws)
    distinct_sum = sum(len(set(d)) for d in draws)
    eq([R(absent, len(draws)), R(distinct_sum, len(draws))], [R(81, 256), R(175, 64)])
    both = sum(0 not in a and 0 not in b for a in draws for b in draws)
    eq(R(both, len(draws)**2), R(6561, 65536))
    anchors("M4-14", r"\frac{81}{256}", r"\frac{175}{64}", r"\frac{6561}{65536}")


def p15():
    fold_sizes = np.array([3, 3, 3])
    candidates = np.array([1, 3, 5])
    train_sizes = fold_sizes.sum() - fold_sizes
    assert np.all(candidates[:, None] <= train_sizes[None, :])
    assert "每折恰有 3 个样本" in PROBS and "6 个样本训练" in PROBS
    counts = np.array([[0, 2, 1], [1, 0, 1], [1, 1, 1]])
    assert np.all((0 <= counts) & (counts <= fold_sizes))
    rates = counts.sum(axis=1)/fold_sizes.sum()
    assert np.allclose(rates, [1/3, 2/9, 1/3])
    assert np.allclose(rates, (counts/fold_sizes).mean(axis=1))
    k = int(candidates[np.argmin(rates)])
    labels = [0, 1, 1, 0, 0]
    prediction = int(sum(labels[:k]) > k/2)
    eq([k, prediction], [3, 1])
    anchors("M4-15", r"\frac13,\frac29,\frac13", "$k=3$", "预测为 1")


def p16():
    z, y = sp.symbols("z y", real=True)
    p = 1/(1+sp.exp(-z))
    ce = -y*sp.log(p)-(1-y)*sp.log(1-p)
    grad = -sp.diff(ce, z)
    labels, f = [1, 0], sp.Matrix([sp.log(3), -sp.log(3)])
    g = sp.Matrix([sp.simplify(grad.subs({y: yi, z: fi})) for yi, fi in zip(labels, f)])
    eq(g, [R(1, 4), -R(1, 4)])
    h0 = leaf_fit(g, [[0, 1]])
    eq(h0, [0, 0])
    h1 = leaf_fit(g, [[0], [1]])
    newf = f+h1
    eq(newf, [sp.log(3)+R(1, 4), -sp.log(3)-R(1, 4)])
    loss0 = sum(ce.subs({y: yi, z: fi}) for yi, fi in zip(labels, f))
    loss1 = sum(ce.subs({y: yi, z: fi}) for yi, fi in zip(labels, newf))
    eq(sp.expand_log(loss0, force=True), sp.expand_log(2*sp.log(R(4, 3)), force=True))
    assert abs(float(loss1) - float(2*sp.log(1+sp.exp(-R(1, 4))/3))) < 1e-12
    assert float(loss1) < float(loss0)
    assert abs(float(loss0)-.5754) < .00005 and abs(float(loss1)-.4616) < .00005
    assert g != sp.zeros(2, 1)
    anchors("M4-16", "0.5754", "0.4616", r"2\ln(1+e^{-1/4}/3)")


def p17():
    va, vb = variance(20, 4, R(1, 4)), variance(20, 2, R(1, 10))
    ea, eb = R(1, 2)**2+va+R(1, 4), 1+vb+R(1, 4)
    eq([va, vb, ea, eb], [R(23, 20), R(29, 100), R(33, 20), R(77, 50)])
    assert eb < ea
    b = sp.symbols("B", positive=True)
    eb_general = 1+(b*2+b*(b-1)*R(1, 5))/b**2+R(1, 4)
    boundary = sp.solve(sp.Eq(eb_general, ea), b)[0]
    eq(boundary, 9)
    eq(eb_general.subs(b, 9), ea)
    assert eb_general.subs(b, 10) < ea
    assert sp.diff(eb_general, b).simplify().is_negative
    anchors("M4-17", r"\frac{23}{20}", r"\frac{29}{100}", r"\frac{33}{20}", r"\frac{77}{50}", "至少需要 10 棵")


if __name__ == "__main__":
    expected_ids = {f"M4-{i:02}" for i in range(1, 18)}
    assert set(blocks) == expected_ids
    assert set(re.findall(r"^\*\*(M4-\d+)\*\*", PROBS, re.M)) == expected_ids
    checks = {1: p01, 2: p02, 3: p03, 4: p04, 5: p05, 6: p06, 7: p07,
              8: p08, 9: p09, 10: p10, 11: p11, 12: p12, 13: p13, 14: p14,
              15: p15, 16: p16, 17: p17}
    for i in range(1, 18):
        pid = f"M4-{i:02}"
        try:
            checks[i]()
            print(f"PASS {pid}")
            if i == 11:
                print(f"MANUAL {pid} 证明题：人工核对固定分堆的平方分解、系数符号与严格下降及等号条件；数值反例已自动验算")
        except Exception as exc:
            failed += 1
            print(f"FAIL {pid} {type(exc).__name__}: {exc}")
    sys.exit(bool(failed))
