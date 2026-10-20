"""Recompute every determinate exercise; only M3-08 is a manual proof."""

from pathlib import Path
import re
import sys

import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
ANSWERS = (ROOT / "answers.md").read_text(encoding="utf-8")
PROBLEMS = (ROOT / "problems.md").read_text(encoding="utf-8")
R = sp.Rational


def body(pid):
    match = re.search(
        rf"^\*\*{pid}\*\*\n(.*?)(?=^\*\*M3-\d+\*\*|\Z)",
        ANSWERS, re.M | re.S,
    )
    assert match, f"Missing answer {pid}"
    return match[1].split("\n### ")[0].strip()


def anchor(pid, *texts):
    """Keep the numerical expectations tied to the visible answer."""
    content = body(pid)
    assert content.startswith("**答案：**")
    assert content.splitlines()[-1].startswith("区分点：")
    for text in texts:
        assert text in content, f"Answer changed or missing: {text}"
    tier = "A" if int(pid[-2:]) <= 5 else "C" if pid[-2:] in ("12", "13") else "B"
    assert len(content) <= {"A": 400, "B": 900, "C": 1400}[tier]


def eq(actual, expected):
    if isinstance(actual, sp.MatrixBase):
        assert actual.shape == expected.shape
        assert all(sp.simplify(a - b) == 0 for a, b in zip(actual, expected))
    else:
        assert sp.simplify(actual - expected) == 0, (actual, expected)


def check_options(pid, actual, expected):
    assert len(actual) == len(expected) == 4
    for letter, computed, answer in zip("ABCD", actual, expected):
        assert bool(computed) == answer, f"Option {letter}: {computed}, expected {answer}"
        print(f"PASS {pid} option {letter}: {bool(computed)}")


def scalar_l1(a, z, lam):
    """Find candidates on both open half-lines and at the cusp."""
    w = sp.Symbol("w", real=True)
    objective = a * (w - z) ** 2 / 2 + lam * sp.Abs(w)
    candidates = {sp.S.Zero}
    for sign in (-1, 1):
        smooth = a * (w - z) ** 2 / 2 + sign * lam * w
        for root in sp.solve(sp.diff(smooth, w), w):
            if sign * root > 0:
                candidates.add(root)
    best = min(candidates, key=lambda q: objective.subs(w, q))
    return best, objective.subs(w, best)


def pair_auc(scores, labels):
    positives = [s for s, y in zip(scores, labels) if y == 1]
    negatives = [s for s, y in zip(scores, labels) if y == 0]
    wins = sum(
        (1 if p > n else R(1, 2) if p == n else 0)
        for p in positives for n in negatives
    )
    return R(wins, len(positives) * len(negatives))


def p01():
    pid = "M3-01"
    errors = sp.Matrix([[1, 4, 1], [2, 2, 1], [0, 0, 9]])
    means = [sum(errors.row(i)) / 3 for i in range(3)]
    assert means == [2, R(5, 3), 3]
    # Each option makes both a candidate claim and a numerical CV claim.
    claims = [(0, 1), (1, R(5, 3)), (2, 0), (2, R(1, 3))]
    truth = [means[i] == value and value == min(means) for i, value in claims]
    check_options(pid, truth, [False, True, False, False])
    mixed_minimum = sum(min(errors[:, j]) for j in range(3)) / 3
    eq(mixed_minimum, R(1, 3))
    anchor(pid, "选 (B)", "$2,5/3,3$", "不属于任何一个固定候选")


def p02():
    pid = "M3-02"
    w, z = sp.symbols("w z", real=True)
    fitted = sp.solve(sp.diff((w - z) ** 2 / 2 + w**2 / 2, w), w)[0]
    values = [fitted.subs(z, value) for value in (1, 5)]
    mean = sum(values) / 2
    variance = sum((v - mean) ** 2 for v in values) / 2
    risk = sum((3 + noise - v) ** 2 for noise in (-1, 1) for v in values) / 4
    for actual, expected in zip(
        (mean, (mean - 3) ** 2, variance, risk), (R(3, 2), R(9, 4), 1, R(17, 4))
    ):
        eq(actual, expected)
    anchor(pid, "$E\\hat f=3/2$", "$9/4$", "$1$", "$17/4$")


def p03():
    pid = "M3-03"
    best, minimum = scalar_l1(sp.S.One, -2, 2)
    options = [-1, -R(2, 3), 0, -4]
    values = [(sp.S(q) + 2) ** 2 / 2 + 2 * abs(q) for q in options]
    check_options(pid, [value == minimum for value in values], [False, False, True, False])
    eq(best, 0)
    eq(sp.diff((sp.Symbol("w") + 2) ** 2 / 2 - 2 * sp.Symbol("w"), sp.Symbol("w")), sp.Symbol("w"))
    anchor(pid, "选 (C)", "最小值点为 $0$", "$g'(w)=w<0$")


def p04():
    pid = "M3-04"
    w, b = sp.symbols("w b", real=True)
    x, y = [-1, 0, 1], [1, 2, 6]
    answers = []
    for shift in (0, 4):
        objective = sum((yi + shift - w * xi - b) ** 2 for xi, yi in zip(x, y)) / 2 + w**2 / 2
        solution = sp.solve([sp.diff(objective, w), sp.diff(objective, b)], [w, b])
        answers.append((solution[w], solution[b]))
        assert all(v > 0 for v in sp.hessian(objective, (w, b)).eigenvals())
    assert answers == [(R(5, 3), 3), (R(5, 3), 7)]
    anchor(pid, "$w=5/3,b=3$", "$w=5/3,b=7$")


def p05():
    pid = "M3-05"
    scores, labels = [3, 1, 1, 0], [1, 1, 0, 0]
    result = pair_auc(scores, labels)
    options = [R(3, 4), 1, R(7, 8), R(2, 3)]
    check_options(pid, [result == option for option in options], [False, False, True, False])
    predicted = [s >= 1 for s in scores]
    precision = R(sum(p and y for p, y in zip(predicted, labels)), sum(predicted))
    eq(precision, options[3])
    anchor(pid, "选 (C)", "$7/8$", "$2/3$")


def p06():
    pid = "M3-06"
    noise, p = sp.symbols("noise p", positive=True)
    solution = sp.solve(
        [noise * (1 - p / 40) - R(16, 5), noise * (1 + p / 40) - R(24, 5)],
        (noise, p), dict=True,
    )[0]
    assert solution == {noise: 4, p: 8}
    train = (noise * (1 - p / 80)).subs(solution)
    fresh = (noise * (1 + p / 80)).subs(solution)
    eq(train, R(18, 5))
    eq(fresh, R(22, 5))
    anchor(pid, "$\\sigma^2=4,p=8$", "$3.6$", "$4.4$")


def p07():
    pid = "M3-07"
    x = np.array([0., 2., 10., 12.])
    np.testing.assert_allclose([x.mean(), x.std()], [6, np.sqrt(26)])
    np.testing.assert_allclose((x[:2] - x.mean()) / x.std(), [-6 / np.sqrt(26), -4 / np.sqrt(26)])
    statistics = [(x[indices].mean(), x[indices].std()) for indices in ([2, 3], [0, 1])]
    np.testing.assert_allclose(statistics, [[11, 1], [1, 1]])
    np.testing.assert_allclose((x[:2] - statistics[0][0]) / statistics[0][1], [-11, -9])
    # A held-out feature changes the global statistic, but not the training statistic.
    changed = x.copy()
    changed[0] += 1
    assert changed.mean() != x.mean()
    assert changed[2:].mean() == x[2:].mean()
    validation_ids, train_ids = {0, 1}, {2, 3}
    global_statistic_ids = set(range(len(x)))
    assert global_statistic_ids & validation_ids
    assert not (train_ids & validation_ids)
    final_training_ids = set(range(len(x)))
    assert global_statistic_ids <= final_training_ids
    anchor(pid, "原流程泄漏", "$\\mu=6,s=\\sqrt{26}$", "$\\mu=11,s=1$", "$\\mu=1,s=1$", "$(-11,-9)$", "可以使用全部四个输入")


def p09():
    pid = "M3-09"
    X, y = sp.diag(2, 1), sp.Matrix([3, -1])
    gram = X.T * X
    z = gram.inv() * X.T * y
    assert gram != sp.eye(2)
    eq(z, sp.Matrix([R(3, 2), -1]))
    fitted = sp.Matrix([scalar_l1(gram[i, i], z[i], 1)[0] for i in range(2)])
    eq(fitted, sp.Matrix([R(5, 4), 0]))

    def objective(q):
        residual = y - X * q
        return residual.dot(residual) / 2 + sum(abs(v) for v in q)

    eq(objective(fitted), R(15, 8))
    eq(objective(sp.Matrix([R(1, 2), 0])), 3)
    anchor(pid, "$(5/4,0)^{\\mathsf T}$", "$15/8$", "$3$", "\\ne I")


def p10():
    pid = "M3-10"
    w, rss, tau2, kappa = sp.symbols("w rss tau2 kappa", positive=True)
    # Multiply the negative log likelihood/prior by the noise variance.
    gaussian_prior_penalty = 6 * w**2 / (2 * tau2)
    laplace_prior_penalty = 6 * w / kappa
    eq(sp.solve(gaussian_prior_penalty - 2 * w**2, tau2)[0], R(3, 2))
    eq(sp.solve(laplace_prior_penalty - 3 * w, kappa)[0], 2)
    lambda2 = sp.expand((rss / 2 + 2 * w**2) / 12).coeff(w, 2) * 2
    lambda1 = sp.expand((rss / 2 + 3 * w) / 12).coeff(w, 1)
    eq(lambda2, R(1, 3))
    eq(lambda1, R(1, 4))
    # Symbolic rescaling verifies both the data and penalty coefficients.
    eq(rss / 24 + lambda2 * w**2 / 2, (rss / 2 + 2 * w**2) / 12)
    eq(rss / 24 + lambda1 * w, (rss / 2 + 3 * w) / 12)
    assert R(1, 12) > 0
    anchor(pid, "$\\tau^2=3/2,\\kappa=2$", "$\\widetilde\\lambda_2=1/3,\\widetilde\\lambda_1=1/4$", "最优解都不变")


def p11():
    pid = "M3-11"
    assert "仍以取反前负例分数 $t$ 表示" in PROBLEMS
    t = sp.Symbol("t", real=True)
    # Derive every breakpoint from a positive-negative score equality.
    breaks = sorted({sp.solve(p - t, t)[0] for p in (0, 2)})
    assert breaks == [0, 2]
    bounds = [-sp.oo, *breaks, sp.oo]
    regions = []
    for lo, hi in zip(bounds, bounds[1:]):
        region = sp.Interval.open(lo, hi)
        sample = hi - 1 if lo == -sp.oo else lo + 1 if hi == sp.oo else (lo + hi) / 2
        # Each pair's ordering is fixed on the entire open interval.
        for p in (0, 2):
            winners = sp.solve_univariate_inequality(t < p, t, relational=False)
            assert region.is_subset(winners) or region.intersect(winners) == sp.EmptySet
        regions.append((region, pair_auc([0, 2, 1, sample], [1, 1, 0, 0])))
    regions += [(sp.FiniteSet(b), pair_auc([0, 2, 1, b], [1, 1, 0, 0])) for b in breaks]
    expected = {
        sp.Interval.open(-sp.oo, 0): R(3, 4),
        sp.FiniteSet(0): R(5, 8),
        sp.Interval.open(0, 2): R(1, 2),
        sp.FiniteSet(2): R(3, 8),
        sp.Interval.open(2, sp.oo): R(1, 4),
    }
    assert dict(regions) == expected
    original = sp.Union(*(region for region, auc in regions if auc == R(5, 8)))
    inverted = sp.Union(*(region for region, auc in regions if 1 - auc == R(5, 8)))
    assert original == sp.FiniteSet(0) and inverted == sp.FiniteSet(2)
    for sample in (-1, 0, 1, 2, 3):
        scores = [0, 2, 1, sample]
        eq(pair_auc(scores, [1, 1, 0, 0]) + pair_auc([-s for s in scores], [1, 1, 0, 0]), 1)
    anchor(pid, "只有 $t=0$", "只有 $t=2$", "3/4,&t<0", "5/8,&t=0", "1/2,&0<t<2", "3/8,&t=2", "1/4,&t>2")


def p12():
    pid = "M3-12"
    X, y = sp.Matrix([[1, 1], [-1, -1]]), sp.Matrix([2, -2])
    lam = sp.Symbol("lambda", positive=True)
    u, v = sp.symbols("u v", real=True)
    unregularized = sp.linsolve((X, y), (u, v))
    assert unregularized == sp.FiniteSet((2 - v, v))
    gram = X.T * X
    regularized = gram + lam * sp.eye(2)
    assert regularized.eigenvals() == {lam: 1, lam + 4: 1}
    fitted = regularized.inv() * X.T * y
    eq(fitted, sp.Matrix([4 / (4 + lam)] * 2))
    limit = fitted.applyfunc(lambda term: sp.limit(term, lam, 0, dir="+"))
    norm_squared = u**2 + (2 - u)**2
    minimizer = sp.solve(sp.diff(norm_squared, u), u)[0]
    assert sp.diff(norm_squared, u, 2) > 0
    eq(limit, sp.Matrix([minimizer, 2 - minimizer]))
    eq(limit, sp.Matrix([1, 1]))
    eq(gram.det(), 0)
    anchor(pid, "$(u,2-u)^{\\mathsf T}$", "$\\lambda,\\lambda+4$", "\\frac4{4+\\lambda}", "$(1,1)^{\\mathsf T}$", "逆不存在")


def p13():
    pid = "M3-13"
    lam = sp.Symbol("lambda", nonnegative=True)
    w = sp.Symbol("w", real=True)
    y = [0, 2, 2, 4]
    fits, losses = [], []
    for train, validation in (([2, 3], [0, 1]), ([0, 1], [2, 3])):
        objective = sum((y[i] - w)**2 for i in train) / 2 + lam * w**2 / 2
        fit = sp.solve(sp.diff(objective, w), w)[0]
        fits.append(fit)
        losses.append(sum((y[i] - fit)**2 for i in validation) / len(validation))
    eq(sp.Matrix(fits), sp.Matrix([6 / (2 + lam), 2 / (2 + lam)]))
    cv = sp.factor(sum(losses) / 2)
    eq(cv, 20 / (2 + lam)**2 - 12 / (2 + lam) + 6)
    best = sp.solve(sp.diff(cv, lam), lam)
    assert best == [R(4, 3)]
    # The sign of the derivative certifies the global minimum on lambda >= 0.
    eq(sp.factor(sp.diff(cv, lam)), 4 * (3 * lam - 4) / (lam + 2)**3)
    eq(cv.subs(lam, best[0]), R(21, 5))
    objective = sum((yi - w)**2 for yi in y) / 2 + best[0] * w**2 / 2
    final_fit = sp.solve(sp.diff(objective, w), w)[0]
    fold_fits = [fit.subs(lam, best[0]) for fit in fits]
    eq(final_fit, R(3, 2))
    assert fold_fits == [R(9, 5), R(3, 5)]
    eq(sum(fold_fits) / 2, R(6, 5))
    assert final_fit != sum(fold_fits) / 2
    anchor(pid, "$6/(2+\\lambda),2/(2+\\lambda)$", "\\frac{20}{(2+\\lambda)^2}-\\frac{12}{2+\\lambda}+6", "$\\lambda=4/3$", "$V=21/5$", "$w=3/2$", "$6/5$")


def p14():
    pid = "M3-14"
    w = sp.Symbol("w")
    t = sp.Symbol("t", integer=True, nonnegative=True)
    objective = (w - 3)**2 / 2 + w**2 / 2
    update = w - sp.diff(objective, w) / 4
    first = update.subs(w, 0)
    second = update.subs(w, first)
    fixed = sp.solve(update - w, w)[0]
    eq(first, R(3, 4))
    eq(second, R(9, 8))
    eq(fixed, R(3, 2))
    term = R(3, 2) * (1 - 2**(-t))
    eq(term.subs(t, 0), 0)
    eq(term.subs(t, t + 1), update.subs(w, term))
    eq(sp.limit(term, t, sp.oo), fixed)
    assert fixed != 0
    anchor(pid, "$w_1=3/4,w_2=9/8$", "$w_{t+1}=w_t/2+3/4$", "$w_t=\\frac32(1-2^{-t})$", "说法错误")


def p15():
    pid = "M3-15"
    assert "均值为 $w$、方差为 $2$ 的正态分布" in PROBLEMS
    w = sp.Symbol("w", real=True)
    likelihood_nll = sum((yi - w)**2 / 4 for yi in (1, 3))
    posterior_nll = sp.expand(likelihood_nll + w**2 / 2)
    mode = sp.solve(sp.diff(posterior_nll, w), w)[0]
    variance = 1 / sp.diff(posterior_nll, w, 2)
    eq(mode, 1)
    eq(variance, R(1, 2))
    eq(posterior_nll - (w - 1)**2, R(3, 2))
    density = sp.exp(-posterior_nll)
    normalization = sp.integrate(density, (w, -sp.oo, sp.oo))
    mean = sp.integrate(w * density, (w, -sp.oo, sp.oo)) / normalization
    eq(mean, 1)
    eq(sp.solve(sp.diff(likelihood_nll, w), w)[0], 2)
    X, y = sp.Matrix([1, 1]), sp.Matrix([1, 3])
    eq(((X.T * X + 2 * sp.eye(1)).inv() * X.T * y)[0], mode)
    anchor(pid, "$N(1,1/2)$", "$1$", "$1/2$", "$2$", "\\exp[-(w-1)^2]")


def p16():
    pid = "M3-16"
    scores = np.array([-2., -1., 1., 2.])
    labels = np.array([0, 1, 0, 1])
    probabilities = [1 / (1 + np.exp(-scores)), 1 / (1 + np.exp(-(2 * scores + 3)))]
    results = []
    predictions = []
    for values in probabilities:
        assert np.all(np.diff(values) > 0)
        predicted = values >= .5
        predictions.append(predicted.astype(int).tolist())
        results.append((
            pair_auc(values, labels),
            R(int(np.sum(predicted == labels)), len(labels)),
            R(int(np.sum(predicted & (labels == 1))), int(np.sum(predicted))),
        ))
    assert results == [(R(3, 4), R(1, 2), R(1, 2)), (R(3, 4), R(3, 4), R(2, 3))]
    assert predictions == [[0, 0, 1, 1], [0, 1, 1, 1]]
    anchor(pid, "AUC 都为 $3/4$", "都是 $1/2$", "准确率为 $3/4$", "精确率为 $2/3$", "$(0,0,1,1)$", "$(0,1,1,1)$")


def main():
    cases = {1: p01, 2: p02, 3: p03, 4: p04, 5: p05, 6: p06, 7: p07,
             9: p09, 10: p10, 11: p11, 12: p12, 13: p13, 14: p14, 15: p15, 16: p16}
    expected_ids = [f"M3-{i:02d}" for i in range(1, 17)]
    assert re.findall(r"^\*\*(M3-\d+)\*\*", PROBLEMS, re.M) == expected_ids
    assert re.findall(r"^\*\*(M3-\d+)\*\*", ANSWERS, re.M) == expected_ids
    failures = 0
    for number in range(1, 17):
        pid = f"M3-{number:02d}"
        try:
            if number == 8:
                anchor(pid, "独立性用于消去噪声", "第二次消去交叉项只用了均值的定义")
                print(f"MANUAL {pid} 偏差–方差分解证明")
                continue
            cases[number]()
            print(f"PASS {pid}")
        except Exception as exc:
            failures += 1
            print(f"FAIL {pid} {type(exc).__name__}: {exc}")
    return bool(failures)


if __name__ == "__main__":
    sys.exit(main())
