"""Recompute from the problem data; expected values mirror answers.md.

An option passes when its computed truth value agrees with the answer,
including options that are false. Only the general proof is manual.
"""

from pathlib import Path
import re
import sys

import sympy as s


ROOT = Path(__file__).resolve().parents[1]
ANSWERS = (ROOT / "answers.md").read_text(encoding="utf-8")
BLOCKS = dict(re.findall(r"\*\*(M5-\d+)\*\*\n(.*?)(?=\n\*\*M5-|\Z)", ANSWERS, re.S))
FAILURES = []
R = s.Rational
M = s.Matrix


def equal(actual, expected):
    if isinstance(actual, s.MatrixBase):
        assert actual.shape == expected.shape, (actual, expected)
        assert all(s.simplify(v) == 0 for v in actual - expected), (actual, expected)
    else:
        assert s.simplify(actual - expected) == 0, (actual, expected)


def text_has(pid, *snippets):
    for snippet in snippets:
        assert snippet in BLOCKS[pid], (pid, "answer differs", snippet)


def run(pid, calculation):
    try:
        calculation()
    except Exception as error:
        FAILURES.append(pid)
        print(f"FAIL {pid}: {error}")
    else:
        print(f"PASS {pid}")


def center(X):
    mean = s.ones(1, X.rows) * X / X.rows
    return X - s.ones(X.rows, 1) * mean, mean


def covariance(X):
    Xc, _ = center(X)
    return Xc.T * Xc / (X.rows - 1)


def eigenvalues(S):
    return sorted([value for value, count in S.eigenvals().items()
                   for _ in range(count)], reverse=True)


def norm2(v):
    return s.expand(v.dot(v))


def options(pid, truths, expected, chosen):
    text_has(pid, f"选 ({chosen})")
    for letter, actual, wanted in zip("ABCD", truths, expected):
        def check(actual=actual, wanted=wanted):
            assert bool(actual) == wanted, (actual, wanted)
        run(f"{pid} ({letter})", check)
    assert sum(bool(value) for value in truths) == 1


def p01():
    a, b = s.symbols("a b")
    X = M([[1, 2], [-1, 0], [a, b]])
    solved = s.solve(list(s.ones(1, 3) * X), (a, b))
    equal(solved[a], 0)
    equal(solved[b], -2)
    X = X.subs(solved)
    equal(covariance(X), M([[1, 1], [1, 4]]))
    t = X * M([0, 1])
    equal(t, M([2, 0, -2]))
    equal(covariance(t)[0], 4)
    text_has("M5-01", "a=0,b=-2", r"1&1\\1&4", r"(2,0,-2)", "方差为 $4$")


def p02():
    S = s.diag(4, 1)
    S0 = 4 * S / 5
    values = eigenvalues(S0)
    direction = M([1, 0])
    same_direction = S0 * direction == values[0] * direction
    ratio = values[0] / sum(values)
    options("M5-02", [not same_direction, values[0] == 4,
                       values[0] == R(16, 5) and ratio == R(4, 5),
                       ratio == R(16, 25)], [False, False, True, False], "C")
    text_has("M5-02", "16/5", "4/5")


def p03():
    S = M([[5, 2], [2, 2]])
    v = M([2, 1])
    equal(S * v, 6 * v)
    equal((v.T * S * v)[0], 30)
    w = v / s.sqrt(norm2(v))
    equal(w, M([2, 1]) / s.sqrt(5))
    equal((w.T * S * w)[0], eigenvalues(S)[0])
    equal(eigenvalues(S)[0], 6)
    equal(w.dot(M([1, -2])), 0)
    text_has("M5-03", "方差为 $6$", r"(2,1)^{\mathsf T}/\sqrt5", "得分为 $0$")


def p04():
    S = s.diag(5, 2, 1)
    e1, e2, e3 = [s.eye(3)[:, j] for j in range(3)]
    vals = eigenvalues(S)
    q = (e1 + e2) / s.sqrt(2)
    variance = lambda w: (w.T * S * w)[0]
    options("M5-04", [variance(e2) == vals[0], q.dot(e1) == 0,
                       variance(e3) == vals[1],
                       e2.dot(e1) == 0 and variance(e2) == vals[1] == 2],
            [False, False, False, True], "D")


def p05():
    values = eigenvalues(s.diag(9, 4, 2))
    k = next(k for k in range(1, 4) if sum(values[:k]) / sum(values) >= R(4, 5))
    equal(k, 2)
    equal(5 * sum(values[k:]), 10)
    text_has("M5-05", "保留 $2$ 个", "平方和为 $10$")


def p06():
    A = M([[2, 4], [0, 2]])
    x, y = s.symbols("x y", real=True)
    w = M([x, y])
    f = (w.T * A * w)[0]
    gradient = M([s.diff(f, x), s.diff(f, y)])
    equal(gradient, M([4*x + 4*y, 4*x + 4*y]))
    assert gradient != 2*A*w
    assert eigenvalues(A) == [2, 2]
    B = (A + A.T) / 2
    equal(f, (w.T * B * w)[0])
    equal(eigenvalues(B)[0], 4)
    equal(f, 4*(x*x+y*y) - 2*(x-y)**2)
    maximizers = s.solve([x-y, x*x+y*y-1], (x, y))
    assert set(maximizers) == {(s.sqrt(2)/2, s.sqrt(2)/2), (-s.sqrt(2)/2, -s.sqrt(2)/2)}
    text_has("M5-06", "实际最大值为 $4$", r"\pm(1,1)^{\mathsf T}/\sqrt2")


def p07():
    sigmas = M([6, 3, 1])
    variances = sigmas.applyfunc(lambda x: x*x/4)
    equal(variances, M([9, R(9, 4), R(1, 4)]))
    rate = variances[0] / sum(variances)
    error = 4 * sum(variances[2:])
    options("M5-07", [variances[0] == R(6, 4), rate == R(3, 5),
                       error == R(1, 4), error == 1], [False, False, False, True], "D")
    equal(rate, R(18, 23))
    text_has("M5-07", "9,9/4,1/4", "18/23", "=1$")


def p08():
    w1 = M([1, 2]) / s.sqrt(5)
    # Obtain the second direction from the nullspace, not from the answer.
    w2 = w1.T.nullspace()[0]
    w2 = -w2 / s.sqrt(norm2(w2))
    l2 = R(3, 4-1)
    S = 6*w1*w1.T + l2*w2*w2.T
    equal(S, M([[2, 2], [2, 5]]))
    equal(w2, M([2, -1])/s.sqrt(5))
    equal(S*w2, w2)
    point = M([3, 1])
    score = point.dot(w1)
    reconstruction = score*w1
    equal(score, s.sqrt(5))
    equal(reconstruction, M([1, 2]))
    equal(norm2(point - reconstruction), 5)
    text_has("M5-08", r"2&2\\2&5", r"(2,-1)^{\mathsf T}/\sqrt5",
             r"得分为 $\sqrt5$", "误差平方为 $5$")


def p09():
    X = M([[9, -1], [9, 1], [11, -1], [11, 1]])
    Xc, mean = center(X)
    equal(mean, M([[10, 0]]))
    equal(X.T*X/3, s.diag(R(404, 3), R(4, 3)))
    S = covariance(X)
    equal(S, s.eye(2)*R(4, 3))
    theta = s.symbols("theta", real=True)
    w = M([s.cos(theta), s.sin(theta)])
    equal(s.trigsimp((w.T*S*w)[0]), R(4, 3))
    residual = Xc - Xc*w*w.T
    equal(s.trigsimp(sum(v*v for v in residual)), 4)
    equal(eigenvalues(S)[0]/s.trace(S), R(1, 2))
    text_has("M5-09", "404/3,4/3", "4/3,4/3", "任意单位向量", "$1/2$", "平方和为 $4$")


def p10():
    S = M([[9, -3], [-3, 4]])
    D = s.diag(*[s.sqrt(S[i, i]) for i in range(2)])
    corr = D.inv()*S*D.inv()
    equal(corr, M([[1, -R(1, 2)], [-R(1, 2), 1]]))
    w = M([1, -1])/s.sqrt(2)
    equal(corr*w, eigenvalues(corr)[0]*w)
    equal(eigenvalues(corr)[0]/s.trace(corr), R(3, 4))
    point = M([3, 2])
    equal(w.dot(D.inv()*point), 0)
    equal(w.dot(point), 1/s.sqrt(2))
    scale = s.diag(2, 5)
    new_S = scale*S*scale
    equal(new_S, M([[36, -30], [-30, 100]]))
    new_D = s.diag(*[s.sqrt(new_S[i, i]) for i in range(2)])
    equal(new_D.inv()*new_S*new_D.inv(), corr)
    equal(w.dot(new_D.inv()*scale*point), 0)
    text_has("M5-10", r"1&-1/2\\-1/2&1", r"(1,-1)^{\mathsf T}/\sqrt2",
             "$3/4$", "正确得分为 $0$", "均不变")


def p11():
    S = M([[3, 1, 0], [1, 3, 0], [0, 0, 1]])
    expected = {4: M([1, 1, 0])/s.sqrt(2),
                2: M([1, -1, 0])/s.sqrt(2), 1: M([0, 0, 1])}
    assert eigenvalues(S) == [4, 2, 1]
    count = 0
    for value, multiplicity, basis in S.eigenvects():
        assert multiplicity == len(basis) == 1
        unit = basis[0]/s.sqrt(norm2(basis[0]))
        equal(unit*unit.T, expected[value]*expected[value].T)
        for sign in (-1, 1):
            w = sign*unit
            equal(norm2(w), 1)
            equal(S*w, value*w)
            for v in w.T.nullspace():
                equal(v.dot(S*w), 0)
            equal((w.T*S*w)[0], value)
            count += 1
    assert count == 6
    # A perpendicular pair alone need not force an eigenvector.
    w = M([1, 0, 0])
    r = S*w - w.dot(S*w)*w
    equal(r, M([0, 1, 0]))
    equal(r.dot(S*w), 1)
    text_has("M5-11", "全部六个向量", "只有第一对", "4,2,1",
             r"\pm(1,1,0)^{\mathsf T}/\sqrt2",
             r"\pm(1,-1,0)^{\mathsf T}/\sqrt2",
             r"\pm(0,0,1)^{\mathsf T}")


def p12():
    a = s.symbols("a", real=True)
    b = s.symbols("b", nonnegative=True)
    S = M([[3, a, 0], [a, 3, 0], [0, 0, 2]])
    Q = M([[1/s.sqrt(2), 1/s.sqrt(2), 0],
           [1/s.sqrt(2), -1/s.sqrt(2), 0], [0, 0, 1]])
    equal(Q.T*Q, s.eye(3))
    equal(Q.T*S*Q, s.diag(3+a, 3-a, 2))
    assert s.solve((3+a)-(3-a), a) == [0]
    equal(S.subs(a, 0)[:2, :2], 3*s.eye(2))
    assert s.reduce_inequalities([b >= 0, b <= 3, (3+b)/8 >= R(4, 5)], b) == s.false
    # Ordering changes where 3-b crosses 2; solve both branches exactly.
    assert s.solve(3-b-2, b) == [1]
    assert s.reduce_inequalities([b <= 1, R(6, 8) >= R(4, 5)], b) == s.false
    accepted = s.reduce_inequalities([b > 1, b <= 3, (5+b)/8 >= R(4, 5)], b)
    assert accepted == s.And(R(7, 5) <= b, b <= 3)
    branch_small = S.subs(a, b)
    for order, domain in [([3+b, 3-b, s.Integer(2)], (b >= 0, b <= 1)),
                          ([3+b, s.Integer(2), 3-b], (b > 1, b <= 3))]:
        for left, right in zip(order, order[1:]):
            assert s.reduce_inequalities([*domain, left < right], b) == s.false
        assert s.expand(s.prod(v-s.Symbol("z") for v in order)) == s.expand((branch_small-s.Symbol("z")*s.eye(3)).det())
    equal(5*2, 10)
    # Project away the actual last eigenvector in each interval.
    for dropped, expected in [(Q[:, 2], s.Integer(10)), (Q[:, 1], 5*(3-b))]:
        equal(5*(dropped.T*branch_small*dropped)[0], expected)
    # Negative a swaps the first two eigenvectors but preserves the spectrum.
    equal(Q.T*S.subs(a, -b)*Q, s.diag(3-b, 3+b, 2))
    text_has("M5-12", "a>0", "a<0", "a=0", r"x^2+y^2=1",
             r"|a|\ge7/5", "k=2", "k=3", "10,&|a|", "5(3-|a|)")


def p13():
    X = M([[4, 4], [0, 0], [3, 1], [1, 3]])
    Xc, mean = center(X)
    costs = []
    for slope, intercept in [(s.Integer(1), s.Integer(0)), (R(3, 5), R(4, 5))]:
        errors = X[:, 1] - slope*X[:, 0] - intercept*s.ones(4, 1)
        vertical = norm2(errors)
        costs.append((vertical, s.cancel(vertical/(1+slope*slope))))
    assert costs == [(8, 4), (R(32, 5), R(80, 17))]
    slope = Xc[:, 0].dot(Xc[:, 1])/norm2(Xc[:, 0])
    equal(slope, R(3, 5))
    equal(mean[1]-slope*mean[0], R(4, 5))
    S = covariance(X)
    equal(S, M([[10, 6], [6, 10]])/3)
    w = M([1, 1])/s.sqrt(2)
    equal(S*w, eigenvalues(S)[0]*w)
    equal(3*eigenvalues(S)[1], 4)
    text_has("M5-13", "$8,4$", "$32/5,80/17$", r"回归线是 $\ell_2$", r"重建线是 $\ell_1$")


def p14():
    X = M([[1, 1, 0, 0], [-1, -1, 0, 0], [0, 0, 0, 0]])
    U, sigma, V = X.singular_value_decomposition()
    equal(X.rank(), 1)
    equal(sigma, M([[2]]))
    equal(U*sigma*V.T, X)
    expected_u = M([1, -1, 0])/s.sqrt(2)
    expected_v = M([1, 1, 0, 0])/s.sqrt(2)
    equal(expected_u*M([[2]])*expected_v.T, X)
    assert U.rows == 3 and V.rows == 4
    scores = X*expected_v
    equal(scores, M([s.sqrt(2), -s.sqrt(2), 0]))
    equal(covariance(scores)[0], 2)
    equal(X-scores*expected_v.T, s.zeros(3, 4))
    equal(min(X.rows-1, X.cols), 2)
    text_has("M5-14", "秩为 $1$", r"\Sigma=(2)", r"(\sqrt2,-\sqrt2,0)", "方差为 $2$", "误差为 $0$")


def p15():
    X = M([[-4, 1], [4, 1], [-4, -1], [4, -1]])
    S = covariance(X)
    equal(S, s.diag(R(64, 3), R(4, 3)))
    vals = eigenvalues(S)
    k = next(k for k in range(1, 3) if sum(vals[:k])/sum(vals) >= R(9, 10))
    equal(k, 1)
    horizontal = X*M([1, 0])
    vertical = X*M([0, 1])
    equal(horizontal, M([-4, 4, -4, 4]))
    equal(vertical, M([1, 1, -1, -1]))
    assert set(horizontal[:2]) & set(horizontal[2:])
    assert not set(vertical[:2]) & set(vertical[2:])
    equal(vals[0]/sum(vals), R(16, 17))
    equal(vals[1]/sum(vals), R(1, 17))
    text_has("M5-15", "保留 $1$ 个", "(-4,4,-4,4)", "不能区分", "$1/17$", "16/17")


if __name__ == "__main__":
    expected_ids = {f"M5-{i:02d}" for i in range(1, 16)}
    assert set(BLOCKS) == expected_ids
    for number in range(1, 16):
        pid = f"M5-{number:02d}"
        run(pid, globals()[f"p{number:02d}"])
        if number == 11:
            print(f"MANUAL {pid}(1) 不相关条件与特征方向等价的一般证明")
    sys.exit(bool(FAILURES))
