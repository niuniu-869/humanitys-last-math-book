"""Independently check all nine numbered examples in lesson.md.

Exact claims use rational arithmetic. Printed decimal approximations allow
one unit of their last printed digit, including intermediate truncation.
"""

from pathlib import Path
import os
import re
import sys

os.environ["OPENBLAS_NUM_THREADS"] = "1"
import numpy as np
import sympy as s


ROOT = Path(__file__).resolve().parents[1]
LESSON = (ROOT / "lesson.md").read_text(encoding="utf-8")
EXAMPLES = dict(re.findall(r"\*\*例 (\d+)\*\*(.*?)(?=\*\*例 \d+\*\*|\Z)", LESSON, re.S))
M = s.Matrix
R = s.Rational
FAILURES = []
OLD = M([[1, 2], [2, 3], [3, 5], [4, 6], [5, 9]])


def equal(actual, expected):
    if isinstance(actual, s.MatrixBase):
        assert actual.shape == expected.shape, (actual, expected)
        assert all(s.simplify(v) == 0 for v in actual - expected), (actual, expected)
    else:
        assert s.simplify(actual - expected) == 0, (actual, expected)


def near(actual, expected, tol):
    assert np.allclose(np.array(actual, dtype=float), np.array(expected, dtype=float),
                       rtol=0, atol=tol), (actual, expected)


def has(example, *snippets):
    for snippet in snippets:
        assert snippet in EXAMPLES[str(example)], ("lesson changed", snippet)


def center(X):
    mean = s.ones(1, X.rows)*X/X.rows
    return X-s.ones(X.rows, 1)*mean, mean


def covariance(X):
    Xc, _ = center(X)
    return Xc.T*Xc/(X.rows-1)


def old_numeric():
    Xc, _ = center(OLD)
    S = np.array(covariance(OLD), dtype=float)
    values, vectors = np.linalg.eigh(S)
    w = vectors[:, -1]
    if w[0] < 0:
        w = -w
    return np.array(Xc, dtype=float), values[::-1], w


def ex1():
    X = M([[1, 2, 3], [3, 2, 1], [2, 4, 3], [2, 0, 1]])
    Xc, mean = center(X)
    equal(mean, M([[2, 2, 2]]))
    equal(Xc, M([[-1, 0, 1], [1, 0, -1], [0, 2, 1], [0, -2, -1]]))
    gram = Xc.T*Xc
    equal(gram, M([[2, 0, -2], [0, 8, 4], [-2, 4, 4]]))
    equal(covariance(X), gram/3)
    assert Xc.shape == (4, 3) and gram.shape == (3, 3)
    equal(covariance(2*OLD), 4*covariance(OLD))
    has(1, r"2&0&-2\\0&8&4\\-2&4&4", r"\frac23,\frac83,\frac43")


def ex2():
    theta = s.symbols("theta", real=True)
    w = M([s.cos(theta), s.sin(theta)])
    f = (w.T*covariance(OLD)*w)[0]
    expected = 5-R(5, 2)*s.cos(2*theta)+R(17, 4)*s.sin(2*theta)
    equal(s.trigsimp(f-expected), 0)
    amplitude = s.sqrt(R(5, 2)**2+R(17, 4)**2)
    near(amplitude, 4.931, 0.001)
    near(5+amplitude, 9.931, 0.001)
    angle = np.arctan2(4.25, -2.5)/2
    near(np.degrees(angle*2), 120.5, 0.1)
    near(np.degrees(angle), 60.2, 0.1)
    near([np.cos(angle), np.sin(angle)], [0.4965, 0.8680], 0.0001)
    equal(f.subs(theta, s.pi/4), R(37, 4))
    has(2, r"5-2.5\cos2\theta+4.25\sin2\theta", "9.931", "60.2", "0.4965")


def ex3():
    S = covariance(OLD)
    lam = s.symbols("lam")
    equal((S-lam*s.eye(2)).det(), lam**2-10*lam+R(11, 16))
    Xc, values, w = old_numeric()
    near(values, [9.9308, 0.0692], 0.0001)
    near(values[0]-5, 4.9307, 0.0001)
    near(w, [0.4965, 0.8680], 0.0001)
    near(w[1]/w[0], 1.7484, 0.0001)
    near(1/w[0], 2.014, 0.001)
    scores = Xc@w
    near(scores, [-3.597, -2.233, 0, 1.365, 4.465], 0.001)
    near(np.var(scores, ddof=1), 9.93, 0.01)
    has(3, r"\lambda^2-10\lambda+0.6875", "9.9308", "0.0692", "-3.597", "4.465")


def ex4():
    S = M([[6, 2, 0], [2, 3, 0], [0, 0, 1]])
    Q = M([[2/s.sqrt(5), 1/s.sqrt(5), 0],
           [1/s.sqrt(5), -2/s.sqrt(5), 0], [0, 0, 1]])
    equal(Q.T*Q, s.eye(3))
    equal(Q.T*S*Q, s.diag(7, 2, 1))
    lam = s.symbols("lam")
    equal((S-lam*s.eye(3)).det(), (1-lam)*(lam-7)*(lam-2))
    has(4, "特征值 $7,2,1$", "(2,1,0)/", "(1,-2,0)/", "(0,0,1)")


def ex5():
    S = M([[6, 2, 0], [2, 3, 0], [0, 0, 1]])
    vals = sorted(S.eigenvals(), reverse=True)
    rates = [100*v/s.trace(S) for v in vals]
    assert rates == [70, 20, 10]
    assert [sum(rates[:k]) for k in range(1, 4)] == [70, 90, 100]
    old_values = sorted(covariance(OLD).eigenvals(), reverse=True)
    near(100*old_values[0]/sum(old_values), 99.31, 0.01)
    values = [8, 4, 2, 1, 1]
    k = next(k for k in range(1, 6) if R(sum(values[:k]), sum(values)) >= R(9, 10))
    equal(k, 4)
    has(5, r"70\%", r"20\%", r"10\%", r"99.31\%")


def ex6():
    Xc, values, w = old_numeric()
    residual = Xc-np.outer(Xc@w, w)
    error = np.sum(residual**2)
    near(error, 0.2769, 0.0001)
    near(error, 4*values[1], 1e-12)
    design = np.column_stack((np.array(OLD[:, 0], dtype=float).ravel(), np.ones(5)))
    y = np.array(OLD[:, 1], dtype=float).ravel()
    beta = np.linalg.lstsq(design, y, rcond=None)[0]
    near(beta, [1.7, -0.1], 1e-12)
    near(np.sum((y-design@beta)**2), 1.1, 1e-12)
    near(w[1]/w[0], 1.748, 0.001)
    assert error < np.sum((y-design@beta)**2)
    has(6, "0.2769", "y=1.7x-0.1", "1.1", "1.748")


def ex7():
    S = covariance(OLD)
    D = s.diag(*[s.sqrt(S[i, i]) for i in range(2)])
    corr = D.inv()*S*D.inv()
    r = corr[0, 1]
    near(r, 0.9815, 0.0001)
    Q = M([[1, 1], [1, -1]])/s.sqrt(2)
    equal(Q.T*corr*Q, s.diag(1+r, 1-r))
    near([1+r, 1-r], [1.9815, 0.0185], 0.0001)
    near((1+r)*50, 99.07, 0.01)
    scale = s.diag(1, 10)
    new_S = scale*S*scale
    new_D = s.diag(*[s.sqrt(new_S[i, i]) for i in range(2)])
    equal(new_D.inv()*new_S*new_D.inv(), corr)
    # Also check the nearby SVD values obtained from the original data.
    Xc, _, _ = old_numeric()
    sigmas = np.linalg.svd(Xc, compute_uv=False)
    near(sigmas, [6.3026, 0.5262], 0.0001)
    near(sigmas[0]/sigmas[1], 11.98, 0.01)
    near((sigmas[0]/sigmas[1])**2, 143.4, 0.1)
    has(7, "0.9815", "1.9815", "0.0185", r"99.07\%")


def ex8():
    X = M([[6, 2, 3], [4, 6, 3], [-2, -2, 3], [-4, 2, 3]])
    Xc, mean = center(X)
    equal(mean, M([[1, 2, 3]]))
    equal(Xc, M([[5, 0, 0], [3, 4, 0], [-3, -4, 0], [-5, 0, 0]]))
    gram = Xc.T*Xc
    equal(gram, M([[68, 24, 0], [24, 32, 0], [0, 0, 0]]))
    assert gram.eigenvals() == {s.Integer(80): 1, s.Integer(20): 1, s.Integer(0): 1}
    V = M([[2, 1], [1, -2], [0, 0]])/s.sqrt(5)
    sigma = s.diag(4*s.sqrt(5), 2*s.sqrt(5))
    scores = Xc*V
    equal(scores, M([[10, 5], [10, -5], [-10, 5], [-10, -5]])/s.sqrt(5))
    U = scores*sigma.inv()
    equal(U.T*U, s.eye(2))
    equal(V.T*V, s.eye(2))
    equal(U*sigma*V.T, Xc)
    equal(covariance(scores), s.diag(R(80, 3), R(20, 3)))
    equal(covariance(scores)/s.trace(covariance(X)), s.diag(R(4, 5), R(1, 5)))
    equal(Xc-scores*V.T, s.zeros(4, 3))
    near([sigma[0, 0], sigma[1, 1]], [8.944, 4.472], 0.001)
    has(8, "(6,2,3)", "(4,6,3)", "(-2,-2,3)", "(-4,2,3)",
        "80/3", "20/3", r"80\%", r"20\%")
    n, d = 100, 768
    H = np.eye(n)-np.ones((n, n))/n
    near(H@H, H, 1e-12)
    equal(np.linalg.matrix_rank(H), 99)
    # An explicit centered matrix reaches the bound, so 99 is sharp.
    Xc = np.zeros((n, d))
    Xc[:n-1, :n-1] = np.eye(n-1)
    Xc[n-1, :n-1] = -1
    near(Xc.sum(axis=0), np.zeros(d), 0)
    U, sigmas, Vt = np.linalg.svd(Xc, full_matrices=False)
    rank = np.linalg.matrix_rank(Xc)
    equal(rank, 99)
    W2 = Vt[:2].T
    scores = Xc@W2
    assert W2.shape == (768, 2) and scores.shape == (100, 2)
    assert (Xc.T@Xc).shape == (768, 768)
    near(scores, U[:, :2]*sigmas[:2], 1e-12)
    near(np.cov(scores, rowvar=False), np.diag(sigmas[:2]**2/(n-1)), 1e-12)
    retained = np.sum(sigmas[:2]**2)/np.sum(sigmas**2)
    near(retained, np.sum(sigmas[:2]**2/(n-1))/np.sum(sigmas**2/(n-1)), 1e-12)
    has(8, r"100\times768", r"768\times2", r"100\times2", "n-1=99")


def ex9():
    X = M([[57, 51, 10], [59, 47, 10], [60, 50, 10], [62, 51, 8], [62, 51, 12]])
    Xc, mean = center(X)
    equal(mean, M([[60, 50, 10]]))
    equal(Xc, M([[-3, 1, 0], [-1, -3, 0], [0, 0, 0], [2, 1, -2], [2, 1, 2]]))
    S = covariance(X)
    equal(S, M([[R(9, 2), 1, 0], [1, 3, 0], [0, 0, 2]]))
    Q = M([[2/s.sqrt(5), 1/s.sqrt(5), 0],
           [1/s.sqrt(5), -2/s.sqrt(5), 0], [0, 0, 1]])
    equal(Q.T*S*Q, s.diag(5, R(5, 2), 2))
    equal(Q.T*Q, s.eye(3))
    vals = [5, R(5, 2), 2]
    near([100*v/s.trace(S) for v in vals], [52.6, 26.3, 21.1], 0.1)
    near(100*sum(vals[:2])/s.trace(S), 78.9, 0.1)
    assert sum(vals[:2])/s.trace(S) < R(9, 10)
    T = Xc*Q[:, :2]
    near(T, [[-2.236, -2.236], [-2.236, 2.236], [0, 0], [2.236, 0], [2.236, 0]], 0.001)
    residual = Xc-T*Q[:, :2].T
    equal(sum(v*v for v in residual), 8)
    equal(covariance(T)[0, 0], 5)
    equal(T[3, :], T[4, :])
    residual1 = Xc-Xc*Q[:, :1]*Q[:, :1].T
    equal(sum(v*v for v in residual1), 18)
    has(9, "4.5&1&0", "5,\\ 2.5,\\ 2", r"78.9\%", "4\\times2=8")


def scaled_spectrum():
    scaled = OLD*s.diag(1, 10)
    S = covariance(scaled)
    equal(S, M([[R(5, 2), R(85, 2)], [R(85, 2), 750]]))
    values, vectors = np.linalg.eigh(np.array(S, dtype=float))
    w = vectors[:, -1]
    if w[0] < 0:
        w = -w
    near(values[::-1], [752.4, 0.09], 0.1)
    near(values[0], 0.09, 0.01)
    near(w, [0.057, 0.998], 0.001)
    near(np.degrees(np.arctan2(w[1], w[0])), 86.8, 0.1)


def rank_one_code():
    X = np.array([[1, 1, 0, 0], [-1, -1, 0, 0], [0, 0, 0, 0]], dtype=float)
    blocks = re.findall(r"```python\n(.*?)```", LESSON, re.S)
    assert len(blocks) == 1
    env = {"np": np, "X": X}
    exec(compile(blocks[0], "lesson.md PCA code", "exec"), env)
    assert np.linalg.matrix_rank(env["Xc"]) == 1
    assert env["U"].shape == (3, 3)
    assert env["s"].shape == (3,)
    assert env["Vt"].shape == (3, 4)
    assert env["scores"].shape == (3, 3)
    assert env["W2"].shape == (4, 2)
    assert env["scores2"].shape == (3, 2)
    near(env["s"], [2, 0, 0], 1e-12)
    near(env["scores2"], env["scores"][:, :2], 1e-12)
    near(env["scores2"]@env["W2"].T, X, 1e-12)


def quick_question(number):
    if number == 1:
        equal(covariance(2*OLD), M([[10, 17], [17, 30]]))
    elif number == 2:
        w = M([1, 1])/s.sqrt(2)
        equal((w.T*covariance(OLD)*w)[0], R(37, 4))
    elif number == 3:
        S = M([[3, 1], [1, 3]])
        assert S.eigenvals() == {s.Integer(4): 1, s.Integer(2): 1}
        w = M([1, 1])/s.sqrt(2)
        equal(S*w, 4*w)
        equal(w.dot(w), 1)
    elif number == 4:
        S = s.diag(5, 2)
        for j, value in enumerate([5, 2]):
            equal(S*s.eye(2)[:, j], value*s.eye(2)[:, j])
    elif number == 5:
        values = [8, 4, 2, 1, 1]
        equal(next(k for k in range(1, 6)
                   if R(sum(values[:k]), sum(values)) >= R(9, 10)), 4)
    elif number == 6:
        equal((3-1)*min(s.diag(4, 1).eigenvals()), 2)
    elif number == 7:
        S = M([[1, R(3, 5)], [R(3, 5), 1]])
        equal(max(S.eigenvals())/s.trace(S), R(4, 5))
    elif number == 8:
        sigmas = s.symbols("s1:4", positive=True)
        n = s.symbols("n", integer=True, positive=True)
        variances = [v**2/n for v in sigmas]
        equal(sum(variances[:2])/sum(variances),
              (sigmas[0]**2+sigmas[1]**2)/sum(v**2 for v in sigmas))
    elif number == 9:
        S = M([[R(9, 2), 1, 0], [1, 3, 0], [0, 0, 2]])
        equal(4*(s.trace(S)-max(S.eigenvals())), 18)


if __name__ == "__main__":
    assert set(EXAMPLES) == {str(i) for i in range(1, 10)}
    for number in range(1, 10):
        try:
            globals()[f"ex{number}"]()
        except Exception as error:
            FAILURES.append(number)
            print(f"FAIL 例{number}: {error}")
        else:
            print(f"PASS 例{number}")
    extras = [("缩放后的谱", scaled_spectrum), ("秩不足时的正文代码", rank_one_code)]
    extras += [(f"引用块{i}", lambda i=i: quick_question(i)) for i in range(1, 10)]
    for label, check in extras:
        try:
            check()
        except Exception as error:
            FAILURES.append(label)
            print(f"FAIL {label}: {error}")
        else:
            print(f"PASS {label}")
    sys.exit(bool(FAILURES))
