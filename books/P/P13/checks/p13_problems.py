"""Independent exact checks of the numerical and symbolic exercise answers.

Expected values below are transcribed from answers.md; calculations start from
the problem data. Quoted answer fragments guard against checking stale answers.
Only the general proof in P13-11 is marked MANUAL.
"""
from pathlib import Path
import re
import sys

import numpy as np
import sympy as sp
from scipy import stats

R = sp.Rational
ROOT = Path(__file__).resolve().parents[1]
ANS = (ROOT / "answers.md").read_text(encoding="utf-8")
PROBS = (ROOT / "problems.md").read_text(encoding="utf-8")
BLOCKS = {
    m.group(1): m.group(2)
    for m in re.finditer(
        r"^\*\*(P13-\d+)\*\*\n(.*?)(?=^\*\*P13-\d+\*\*|\Z)",
        ANS, re.M | re.S,
    )
}
failures = 0


def eq(actual, expected):
    if isinstance(actual, (tuple, list, sp.MatrixBase)):
        assert len(actual) == len(expected), (actual, expected)
        for a, b in zip(actual, expected):
            eq(a, b)
    else:
        assert sp.simplify(actual - expected) == 0, (actual, expected)


def near(actual, expected, atol=0.001):
    np.testing.assert_allclose(np.asarray(actual, float), expected, rtol=0, atol=atol)


def text_has(pid, *fragments):
    for fragment in fragments:
        assert fragment in BLOCKS[pid], (pid, "missing answer fragment", fragment)


def run(pid, check):
    global failures
    try:
        check()
    except Exception as exc:
        failures += 1
        print(f"FAIL {pid} {type(exc).__name__}: {exc}")
    else:
        print(f"PASS {pid}")


def fit(x, y):
    x, y = sp.Matrix(x), sp.Matrix(y)
    design = sp.ones(len(x), 1).row_join(x)
    # Solve the normal equations instead of substituting the slope formula.
    coef = (design.T * design).inv() * design.T * y
    predicted = design * coef
    residual = y - predicted
    mean = sum(y) / len(y)
    total = sum((v - mean) ** 2 for v in y)
    error = residual.dot(residual)
    return coef, predicted, residual, error, total


def anova(groups):
    groups = [list(map(sp.sympify, g)) for g in groups]
    values = sum(groups, [])
    mean = sum(values) / len(values)
    means = [sum(g) / len(g) for g in groups]
    between = sum(len(g) * (m - mean) ** 2 for g, m in zip(groups, means))
    within = sum(sum((v - m) ** 2 for v in g) for g, m in zip(groups, means))
    total = sum((v - mean) ** 2 for v in values)
    return mean, between, within, total


def p01():
    eq(anova([[0, 2], [3, 4, 5], [7]]), [R(7, 2), R(51, 2), 4, R(59, 2)])
    text_has("P13-01", "SS_B=51/2,SS_W=4,SS_T=59/2")


def p02():
    n, k = 12, 4
    f = R(18, k - 1) / R(16, n - k)
    eq([f, k - 1, n - k], [3, 3, 8])
    text_has("P13-02", "选 C")


def p03():
    coef, fitted, residual, error, _ = fit([-1, 0, 1], [2, 1, 6])
    eq(coef, [3, 2])
    eq(fitted, [1, 3, 5])
    eq(residual, [1, -2, 1])
    eq(error, 6)
    slope0 = sp.Rational(sum(x*y for x, y in zip([-1, 0, 1], [2, 1, 6])), sum(x*x for x in [-1, 0, 1]))
    residual0 = sp.Matrix([2, 1, 6]) - sp.Matrix([-1, 0, 1]) * slope0
    eq([slope0, residual0, residual0.dot(residual0)], [2, [4, 1, 4], 33])
    text_has("P13-03", "3+2x", "(1,-2,1)", "SS_E=6", "SS_E=33")


def p04():
    h = [R(1, 4), R(1)]
    eq([2*sp.sqrt(v) for v in h], [1, 2])
    eq([2*sp.sqrt(1+v) for v in h], [sp.sqrt(5), 2*sp.sqrt(2)])
    assert R(9, 16) == (R(3, 2)/2)**2
    sig = 2
    opts = {"A": sig*sp.sqrt(h[0]), "B": sig*sp.sqrt(1+h[0]), "C": sig*(1+h[0]), "D": sig*(1+sp.sqrt(h[0]))}
    eq([opts["A"], opts["B"], opts["C"], opts["D"]], [1, sp.sqrt(5), R(5, 2), 3])
    text_has("P13-04", "h_1=1/4", "h_2=1", "9/16", "选 B")


def p05():
    dfw = R(24, 2)
    dft = 14
    dfb = dft - dfw
    n, k = dft + 1, dfb + 1
    ssb = 9 * dfb
    eq([n, k, ssb, ssb + 24, dfb, dfw, R(9, 2)], [15, 3, 18, 42, 2, 12, R(9, 2)])
    assert R(9, 2) > 3.89
    near(stats.f.isf(.05, int(dfb), int(dfw)), 3.89, .005)
    # Counterexample to the implication "not all equal => pairwise unequal".
    mu = [0, 0, 1]
    assert len(set(mu)) > 1 and mu[0] == mu[1]
    text_has("P13-05", "n=15,k=3,F=4.5", "不能断定每两组都不同")


def p06():
    covariance = R(-2, 3) * 2 * 3
    byx, bxy = covariance / 4, covariance / 9
    ayx, axy = 1 - byx * 2, 2 - bxy
    eq([ayx, byx, axy, bxy], [3, -1, R(22, 9), R(-4, 9)])
    eq([axy + bxy * 4, (4 - ayx) / byx, byx * bxy], [R(2, 3), -1, R(4, 9)])
    text_has("P13-06", "22/9-4y/9", "x=2/3", "得 $-1$")


def p07():
    b, sxx, error = 1, 10, 10
    regression = b ** 2 * sxx
    r2 = regression / (regression + error)
    eq(r2, R(1, 2))
    for n, df, critical, expected_t, expected_se in [(6, 4, R(2776, 1000), 2, R(1, 2)), (18, 16, R(2120, 1000), 4, R(1, 4))]:
        var = R(error, df)
        se = sp.sqrt(var / sxx)
        t = b / se
        eq([var, se, t], [R(5, 2) if n == 6 else R(5, 8), expected_se, expected_t])
        interval = [b-critical*se, b+critical*se]
        if n == 6:
            near(interval, [-.388, 2.388], .001)
            assert abs(t) < critical
        else:
            near(interval, [.47, 1.53], .001)
            assert abs(t) > critical
    text_has("P13-07", "R^2", "1/2", "(-0.388,2.388)", "(0.470,1.530)")


def p08():
    x = sp.Matrix([-1, 0, 1, 2])
    z = sp.Matrix([-1, 1, 3, 5])
    y = sp.Matrix([0, 1, 1, 4])
    X = sp.ones(4, 1).row_join(x).row_join(z)
    s = sp.symbols("s", real=True)
    family = sp.Matrix([R(9, 10)-s, R(6, 5)-2*s, s])
    normal = X.T * X
    assert normal.det() == 0 and X.rank() == 2
    eq(normal * family - X.T*y, [0, 0, 0])
    assert len(normal.nullspace()) == 1
    eq(X*family, [R(-3, 10), R(9, 10), R(21, 10), R(33, 10)])
    eq(X*normal.nullspace()[0], [0, 0, 0, 0])
    text_has("P13-08", "选 C", "9/10-s,\\,6/5-2s,\\,s")


def p09():
    c = sp.symbols("c", real=True)
    x = [1, R(1, 2), R(1, 3), R(1, 4)]
    u = [1/v for v in map(sp.sympify, x)]
    coef, _, _, _, _ = fit(u, [3, 5, c, 9])
    roots = sp.solve(coef[1] - 2, c)
    eq(roots, [7])
    a, b = [v.subs(c, roots[0]) for v in coef]
    eq([a, b, a+b/2], [1, 2, 2])
    assert 2 > max(x)
    aa, bb = sp.symbols("a b", real=True)
    y = [3, 5, 7, 9]
    q_original = sum((yi-aa-bb/xi)**2 for xi, yi in zip(x, y))
    q_transformed = sum((yi-aa-bb*ui)**2 for ui, yi in zip(u, y))
    eq(q_original, q_transformed)
    text_has("P13-09", "c=7,\\hat a=1", "这次计算属于外推", "没有取 $\\ln y$")


def p10():
    # Realize every given cell mean with two observations, mean +/- 1.
    cells = [[[sp.sympify(v)-1, sp.sympify(v)+1] for v in row] for row in [[8, 12, 16], [14, 15, 10]]]
    nr, nc, m = 2, 3, 2
    grand = sum(v for row in cells for cell in row for v in cell) / (nr*nc*m)
    rows = [sum(v for cell in row for v in cell)/(nc*m) for row in cells]
    cols = [sum(v for row in cells for v in row[j])/(nr*m) for j in range(nc)]
    ssr = nc*m*sum((v-grand)**2 for v in rows)
    ssc = nr*m*sum((v-grand)**2 for v in cols)
    error = sum(sum((v-sum(cell)/2)**2 for v in cell) for row in cells for cell in row)
    ssi = m*sum((sum(cells[i][j])/2-rows[i]-cols[j]+grand)**2 for i in range(nr) for j in range(nc))
    f = sp.expand(ssi / (error / (nr*nc*(m-1))))
    eq([ssr, ssc, error, ssi, f], [3, 14, 12, 78, 39])
    eq([ssr/(error/6), (ssc/2)/(error/6), (ssi/2)/(error/6)], [R(3,2), R(7,2), R(39,2)])
    near(stats.f.isf(.05, 1, 6), 5.99, .005)
    near(stats.f.isf(.05, 2, 6), 5.14, .005)
    text_has("P13-10", "SS_{\\text{行}}=3", "SS_{\\text{列}}=14", "SS_{\\text{交互}}=78")


def p12():
    groups = [[0, 2], [2, 4], [4, 6, 8]]
    y = sp.Matrix(sum(groups, []))
    X = sp.Matrix([[1, 0, 0]]*2 + [[1, 1, 0]]*2 + [[1, 0, 1]]*3)
    coef = (X.T*X).inv()*X.T*y
    predicted = X*coef
    eq(X.T*X, sp.Matrix([[7, 2, 3], [2, 2, 0], [3, 0, 3]]))
    eq(X.T*y, [26, 6, 18])
    eq(coef, [1, 2, 5])
    eq(predicted, [1, 1, 3, 3, 6, 6, 6])
    eq(y-predicted, [-1, 1, -1, 1, -2, 0, 2])
    mean, between, within, total = anova(groups)
    eq([mean, between, within, total], [R(26, 7), R(220, 7), 12, R(304, 7)])
    error = (y-predicted).dot(y-predicted)
    f = (total-error)/2/(error/4)
    eq([error, 1-error/total, f], [12, R(55, 76), R(110, 21)])
    assert f < 6.94
    eq(f, (between/2)/(within/4))
    X2 = sp.Matrix([[1, 1, 0]]*2 + [[1, 0, 1]]*2 + [[1, 0, 0]]*3)
    coef2 = (X2.T*X2).inv()*X2.T*y
    eq(coef2, [6, -5, -3])
    eq(X2*coef2, predicted)
    text_has("P13-12", "55/76", "110/21", "(6,-5,-3)")


def p13():
    a, b = sp.symbols("a b", real=True)
    mean = sp.Matrix([1, 2])
    covariance = sp.Matrix([[4, -3], [-3, 9]])
    w = sp.Matrix([-b, 1])
    expected_square = (w.T*covariance*w)[0] + (mean[1]-a-b*mean[0])**2
    sol = sp.solve([sp.diff(expected_square, a), sp.diff(expected_square, b)], [a, b])
    eq([sol[a], sol[b]], [R(11, 4), R(-3, 4)])
    H = sp.hessian(expected_square, (a, b))
    assert H[0, 0] > 0 and H.det() > 0
    w = w.subs(sol)
    eq([mean[1]-sol[a]-sol[b]*mean[0], (covariance*w)[0], (w.T*covariance*w)[0]], [0, 0, R(27, 4)])
    eq(sol[b]**2*covariance[0, 0]/covariance[1, 1], R(1, 4))
    text_has("P13-13", "a=11/4,b=-3/4", "27/4", "解释比例为 $1/4$")


def p14():
    a, b = sp.symbols("a b", real=True)
    v = sp.symbols("v", positive=True)
    data = [(-1, 2), (0, 1), (1, 6)]
    q = sum((y-a-b*x)**2 for x, y in data)
    loglike = -R(3, 2)*sp.log(2*sp.pi*v)-q/(2*v)
    sol = sp.solve([sp.diff(loglike, a), sp.diff(loglike, b)], [a, b])
    profile = loglike.subs(sol)
    root = sp.solve(sp.diff(profile, v), v)
    eq([sol[a], sol[b], *root, q.subs(sol)/(len(data)-2)], [3, 2, 2, 6])
    eq(sp.diff(profile, v), 3*(2-v)/(2*v**2))
    assert sp.limit(profile, v, 0, dir="+") == -sp.oo
    assert sp.limit(profile, v, sp.oo) == -sp.oo
    text_has("P13-14", "\\hat v_{\\mathrm{ML}}=2", "无偏估计为 6")


def p15():
    # Each group has sample variance 2 and the prescribed mean.
    groups = [[m-2, m, m, m, m+2] for m in range(4)]
    mean, between, within, total = anova(groups)
    mse = within/(20-4)
    f = between/3/mse
    eq([mean, between, within, mse, f], [R(3, 2), 25, 32, 2, R(25, 6)])
    assert f > 3.239
    pairs = [(i, j) for i in range(4) for j in range(i+1, 4)]
    m = len(pairs)
    eq([m, R(1, 20)/m, R(1, 20)/(2*m)], [6, R(1, 120), R(1, 240)])
    se = sp.sqrt(mse*(R(1, 5)+R(1, 5)))
    ts = [(j-i)/se for i, j in pairs]
    eq(ts, [sp.sqrt(5)/2, sp.sqrt(5), 3*sp.sqrt(5)/2, sp.sqrt(5)/2, sp.sqrt(5), sp.sqrt(5)/2])
    assert [pair for pair, t in zip(pairs, ts) if t > 3.008] == [(0, 3)]
    near(stats.t.isf(.05/12, 16), 3.008, .0005)
    near(stats.f.isf(.05, 3, 16), 3.239, .0005)
    text_has("P13-15", "只有第 1、4 组", "1/120", "1/240")


def check_option(pid, letter, actual, expected):
    assert bool(actual) == expected, (letter, actual, expected)
    selected = re.search(r"选 ([ABCD])", BLOCKS[pid]).group(1)
    assert expected == (selected == letter)


if __name__ == "__main__":
    expected_ids = {f"P13-{i:02d}" for i in range(1, 16)}
    assert set(BLOCKS) == expected_ids
    assert set(re.findall(r"^\*\*(P13-\d+)\*\*", PROBS, re.M)) == expected_ids
    checks = {1: p01, 2: p02, 3: p03, 4: p04, 5: p05, 6: p06,
              7: p07, 8: p08, 9: p09, 10: p10, 12: p12, 13: p13, 14: p14, 15: p15}
    for number in range(1, 16):
        pid = f"P13-{number:02d}"
        if number == 11:
            assert "（证明）" in PROBS.split("**P13-11**")[1].split("**P13-12**")[0]
            print(f"MANUAL {pid} 正规方程与平方和分解的普遍性证明")
        else:
            run(pid, checks[number])

    # Every option is evaluated, including the wrong rejection tail in 02-D.
    correct = (R(18, 3)/R(16, 8), 3, 8, "right")
    options02 = [(R(9, 8), 3, 8, "right"), (3, 4, 8, "right"),
                 (3, 3, 8, "right"), (R(1, 3), 8, 3, "right")]
    for letter, candidate in zip("ABCD", options02):
        run(f"P13-02({letter})", lambda c=candidate, l=letter: check_option("P13-02", l, c == correct, l == "C"))
    X = sp.Matrix([[1, -1, -1], [1, 0, 1], [1, 1, 3], [1, 2, 5]])
    null = X.nullspace()
    predictions_unique = all(X*v == sp.zeros(4, 1) for v in null)
    options08 = [((X.T*X).det() != 0), (not predictions_unique),
                 ((X.T*X).det() == 0 and len(null) > 0 and predictions_unique),
                 all(v[1] == 0 and v[2] == 0 for v in null)]
    for letter, actual in zip("ABCD", options08):
        run(f"P13-08({letter})", lambda a=actual, l=letter: check_option("P13-08", l, a, l == "C"))
    sys.exit(bool(failures))
