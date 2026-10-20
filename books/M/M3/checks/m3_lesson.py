"""Check all 11 examples, their numerical follow-ups and nearby data tables."""

from decimal import Decimal
from pathlib import Path
import re
import sys

import numpy as np
import sympy as sp

TEXT = (Path(__file__).resolve().parents[1] / "lesson.md").read_text(encoding="utf-8")
R = sp.Rational
X_VALUES = [1, 2, 3, 4, 5]
Y = sp.Matrix([2, 3, 5, 6, 9])
V_VALUES = [R(3, 2), R(5, 2), R(9, 2), 6]
YV = sp.Matrix([R("2.4"), R("4.3"), R("7.4"), R("10.6")])


def section(number):
    match = re.search(rf"\*\*例 {number}\*\*(.*?)(?=\*\*例 \d+\*\*|\Z)", TEXT, re.S)
    assert match, f"Missing example {number}"
    return match[1]


def rounded(actual, written):
    """Allow half a unit of the last displayed decimal, not arbitrary tolerance."""
    token = str(written)
    places = max(0, -Decimal(token).as_tuple().exponent)
    tolerance = .5 * 10**(-places) if "." in token else 1e-10
    assert abs(float(actual) - float(token)) <= tolerance + 1e-10, (actual, token)


def row(text, name):
    match = re.search(rf"^\| {re.escape(name)} \|(.+)\|$", text, re.M)
    assert match, name
    return [value.strip().strip("$") for value in match[1].split("|")]


def compare_row(actual, text, name):
    written = row(text, name)
    assert len(actual) == len(written)
    for computed, token in zip(actual, written):
        rounded(computed, token)


def design(values, degree):
    return sp.Matrix([[value**j for j in range(degree + 1)] for value in values])


def fit(values, labels, degree):
    X = design(values, degree)
    return (X.T * X).inv() * X.T * labels


def mse(residual):
    return residual.dot(residual) / len(residual)


def l1_min(z, lam):
    w = sp.Symbol("w", real=True)
    objective = (w - z)**2 / 2 + lam * sp.Abs(w)
    candidates = [sp.S.Zero]
    for sign in (-1, 1):
        stationary = sp.solve(sp.diff((w - z)**2 / 2 + sign * lam * w, w), w)[0]
        if stationary * sign > 0:
            candidates.append(stationary)
    return min(candidates, key=lambda value: objective.subs(w, value))


def auc_pair(scores, labels):
    pos = [score for score, label in zip(scores, labels) if label == 1]
    neg = [score for score, label in zip(scores, labels) if label == 0]
    count = sum(1 if p > n else R(1, 2) if p == n else 0 for p in pos for n in neg)
    return R(count, len(pos) * len(neg))


def auc_roc(scores, labels):
    # Group tied scores and integrate each linear ROC segment.
    pos, neg = sum(labels), len(labels) - sum(labels)
    tp = fp = 0
    points = [(sp.S.Zero, sp.S.Zero)]
    for score in sorted(set(scores), reverse=True):
        group = [label for s, label in zip(scores, labels) if s == score]
        tp += sum(group)
        fp += len(group) - sum(group)
        points.append((R(fp, neg), R(tp, pos)))
    area = sum((x1 - x0) * (y0 + y1) / 2 for (x0, y0), (x1, y1) in zip(points, points[1:]))
    return area, points


def ex1():
    sec = section(1)
    training, validation = [], []
    for degree in range(5):
        coefficients = fit(X_VALUES, Y, degree)
        training.append(mse(Y - design(X_VALUES, degree) * coefficients))
        validation.append(mse(YV - design(V_VALUES, degree) * coefficients))
    compare_row(training, sec, "训练误差")
    compare_row(validation, sec, "验证误差")
    assert min(range(5), key=lambda k: validation[k]) == 1
    assert "应该选直线" in sec
    inner = design(V_VALUES[:2], 2) * fit(X_VALUES, Y, 2)
    for actual, token in zip(inner, ("2.504", "3.775")):
        rounded(actual, token)
    rounded(mse(YV[:2, :] - inner), "0.1432")
    rounded(mse(YV[:2, :] - design(V_VALUES[:2], 1) * fit(X_VALUES, Y, 1)), "0.0125")
    quartic = fit(X_VALUES, Y, 4)
    assert quartic == sp.Matrix([9, -R(175, 12), R(235, 24), -R(29, 12), R(5, 24)])
    for actual, token in zip(design(V_VALUES, 4) * quartic, ("2.055", "4.117", "6.867", "22.0")):
        rounded(actual, token)


def ex2():
    truth = sp.Matrix([R(17, 10) * x - R(1, 10) for x in X_VALUES])
    noise = R(1, 4)
    for x0, expected in (
        (4, [(R("2.89"), R(".05"), R("3.19")), (0, R(".075"), R(".325"))]),
        (6, [(R("26.01"), R(".05"), R("26.31")), (0, R(".275"), R(".525"))]),
    ):
        for degree, (bias2, variance, risk) in enumerate(expected):
            X = design(X_VALUES, degree)
            weights = design([x0], degree) * (X.T * X).inv() * X.T
            mean = (weights * truth)[0]
            actual_bias2 = (mean - (R(17, 10) * x0 - R(1, 10)))**2
            actual_variance = noise * (weights * weights.T)[0]
            assert actual_bias2 == bias2
            assert actual_variance == variance
            assert noise + actual_bias2 + actual_variance == risk
    # Section 3 extends the same calculation to degrees 0 through 4.
    variance_factors = []
    for degree in range(5):
        X = design(X_VALUES, degree)
        weights = design([6], degree) * (X.T * X).inv() * X.T
        variance_factors.append((weights * weights.T)[0])
    assert variance_factors == [R(1, 5), R(11, 10), R(23, 5), R(121, 5), 251]
    assert list(weights) == [1, -5, 10, -10, 5]
    sec = section(2)
    compare_row([noise * value for value in variance_factors], sec, "方差（$\\sigma=0.5$）")
    compare_row([R("26.01"), 0, 0, 0, 0], sec, "偏差²")
    compare_row([R("26.01") + noise * variance_factors[0]] + [noise * value for value in variance_factors[1:]], sec, "偏差²+方差")
    assert "3.19" in sec and "0.325" in sec


def ex3():
    for n, p, train, noise_token, new_token in (
        (100, 21, R(4), "5.06", "6.13"),
        (50, 5, R("1.8"), "2", "2.2"),
    ):
        # A rank-p orthogonal projection has p ones and n-p zeros.
        H = sp.diag(*([1] * p + [0] * (n - p)))
        residual = sp.eye(n) - H
        train_factor = sp.trace(residual.T * residual) / n
        new_factor = (n + sp.trace(H.T * H)) / n
        noise = train / train_factor
        rounded(noise, noise_token)
        rounded(noise * new_factor, new_token)
    assert "估计" in section(3) and "6.13" in section(3)


def ex4():
    sec = section(4)
    means = []
    for degree in range(4):
        errors = []
        for held_out in range(5):
            kept = [j for j in range(5) if j != held_out]
            coefficients = fit([X_VALUES[j] for j in kept], sp.Matrix([Y[j] for j in kept]), degree)
            predicted = (design([X_VALUES[held_out]], degree) * coefficients)[0]
            errors.append((Y[held_out] - predicted)**2)
        mean = sum(errors) / 5
        means.append(mean)
        compare_row(errors + [mean], sec, f"次数 {degree}")
    assert min(range(4), key=lambda k: means[k]) == 2
    # Distinguish the numerical minimum from the explicitly stated simpler-model preference.
    assert "2 稍低" in sec and "预先约定的规则" in sec
    assert "取更简单的模型，也就是次数 1" in sec
    assert "按表里的最小值选次数 2" in sec


def ex5():
    sec = section(5)
    steps = [int(value) for value in row(sec, "步数")]
    train = np.array([float(value) for value in row(sec, "训练损失")])
    validation = np.array([float(value) for value in row(sec, "验证损失")])
    assert np.all(np.diff(train) < 0)
    best = int(np.argmin(validation))
    assert steps[best] == 4000
    assert np.all(np.diff(validation[best:]) > 0)
    assert "应保留 4000 步" in sec


def ex6():
    w, b = sp.symbols("w b", real=True)
    for lam, expected_w, expected_b in ((10, R(".85"), R("2.45")), (1, R(17, 11), R(4, 11))):
        objective = sum((yi - w * xi - b)**2 for xi, yi in zip(X_VALUES, Y)) / 2 + lam * w**2 / 2
        solution = sp.solve([sp.diff(objective, w), sp.diff(objective, b)], (w, b))
        assert solution == {w: expected_w, b: expected_b}
    sec_before = TEXT.split("多个权重时做法相同")[0].rsplit("先在老朋友①上试", 1)[1]
    values = [17 / (sp.S(10) + value) for value in (0, 1, 10, 100)]
    compare_row(values, sec_before, "$w=17/(10+\\lambda)$")
    rounded(R(4, 11), "0.364")
    # Nearby degree-4 ridge table uses centered powers of u=(x-3)/2.
    raw = sp.Matrix([[(R(x - 3, 2))**j for j in range(1, 5)] for x in X_VALUES])
    raw_v = sp.Matrix([[R(x - 3, 2)**j for j in range(1, 5)] for x in V_VALUES])
    mean = sp.ones(1, 5) * raw / 5
    X = raw - sp.ones(5, 1) * mean
    V = raw_v - sp.ones(4, 1) * mean
    centered_y = Y - sp.ones(5, 1) * 5
    train, validation = [], []
    for lam in (0, R(1, 10), 1, 3, 10, 100):
        coefficients = (X.T * X + lam * sp.eye(4)).inv() * X.T * centered_y
        train.append(mse(centered_y - X * coefficients))
        validation.append(mse(YV - sp.ones(4, 1) * 5 - V * coefficients))
    compare_row(train, section(6), "训练误差")
    compare_row(validation, section(6), "验证误差")
    assert min(range(6), key=lambda k: validation[k]) == 3


def ex7():
    w = sp.Matrix([2, -1])
    gradient = sp.Matrix([R(".4"), R(".2")])
    eta, lam = R(".1"), R(".5")
    updated = w - eta * (gradient + lam * w)
    plain = w - eta * gradient
    assert updated == sp.Matrix([R("1.86"), R("-.97")])
    assert plain == sp.Matrix([R("1.96"), R("-1.02")])
    assert all(abs(a) < abs(b) for a, b in zip(updated, plain))
    assert "1.86" in section(7) and "-0.97" in section(7)


def ex8():
    w = sp.Symbol("w", real=True)
    centered_x = [x - 3 for x in X_VALUES]
    centered_y = [y - 5 for y in Y]
    sigma2, tau2 = 1, R(1, 4)
    lam = sigma2 / tau2
    assert lam == 4
    likelihood = sum((yi - w * xi)**2 for xi, yi in zip(centered_x, centered_y)) / (2 * sigma2)
    prior = w**2 / (2 * tau2)
    mle = sp.solve(sp.diff(likelihood, w), w)[0]
    mode = sp.solve(sp.diff(likelihood + prior, w), w)[0]
    repeated = sp.solve(sp.diff(10 * likelihood + prior, w), w)[0]
    assert mle == R("1.7") and mode == R(17, 14) and repeated == R(85, 52)
    rounded(mode, "1.214")
    rounded(mle - mode, "0.486")
    rounded(repeated, "1.635")
    assert abs(repeated - mle) < abs(mode - mle)


def ex9():
    z = [R("2.5"), R(".8"), R("-1.4")]
    fitted = [l1_min(value, 1) for value in z]
    assert fitted == [R("1.5"), 0, R("-.4")]
    w = sp.Symbol("w", real=True)
    ridge = [sp.solve(sp.diff((w - value)**2 / 2 + w**2 / 2, w), w)[0] for value in z]
    assert ridge == [R("1.25"), R(".4"), R("-.7")]
    assert [l1_min(value, R(".5")) for value in (R(".3"), -3, R("1.2"))] == [0, -R("2.5"), R(".7")]
    assert "(1.5,\\,0,\\,-0.4)" in section(9)
    # Also check the five-score ROC example immediately before example 10.
    scores, labels = [R(".057"), R(".153"), R(".349"), R(".615"), R(".826")], [0, 0, 1, 0, 1]
    area, points = auc_roc(scores, labels)
    assert area == auc_pair(scores, labels) == R(5, 6)
    assert points == [(0, 0), (0, R(1, 2)), (R(1, 3), R(1, 2)), (R(1, 3), 1), (R(2, 3), 1), (1, 1)]
    logits = R("1.0904") * sp.Matrix(X_VALUES) - sp.ones(5, 1) * R("3.894")
    for logit, score in zip(logits, scores):
        rounded(1 / (1 + sp.exp(-logit)), f"{float(score):.3f}")


SCORES = [R(".9"), R(".8"), R(".7"), R(".6"), R(".55"), R(".3")]
LABELS = [1, 1, 0, 1, 0, 0]


def ex10():
    assert auc_pair(SCORES, LABELS) == auc_roc(SCORES, LABELS)[0] == R(8, 9)
    predicted = [value >= R(".5") for value in SCORES]
    accuracy = R(sum(p == bool(y) for p, y in zip(predicted, LABELS)), len(LABELS))
    assert accuracy == R(2, 3)
    rounded(accuracy, "0.667")
    rounded(R(8, 9), "0.889")
    swapped = SCORES.copy()
    swapped[2], swapped[3] = swapped[3], swapped[2]
    assert auc_pair(swapped, LABELS) == auc_roc(swapped, LABELS)[0] == 1
    assert "8/9" in section(10) and "AUC $=1$" in section(10)


def ex11():
    scores, labels = [], []
    for score, label in zip(SCORES, LABELS):
        count = 1 if label == 1 else 10
        scores.extend([score] * count)
        labels.extend([label] * count)
    assert len(labels) == 33
    assert auc_pair(scores, labels) == auc_roc(scores, labels)[0] == R(8, 9)
    predicted = [bool(score >= R(".5")) for score in scores]
    tp = sum(pred and label == 1 for pred, label in zip(predicted, labels))
    precision = R(tp, sum(predicted))
    assert precision == R(3, 23)
    original_positive_labels = [label for score, label in zip(SCORES, LABELS) if score >= R(".5")]
    original_precision = R(sum(original_positive_labels), len(original_positive_labels))
    assert original_precision == R(3, 5)
    rounded(precision, "0.13")
    assert "3/23" in section(11)


def main():
    failures = 0
    for number, check in enumerate((ex1, ex2, ex3, ex4, ex5, ex6, ex7, ex8, ex9, ex10, ex11), 1):
        try:
            check()
            print(f"PASS 例{number}")
        except Exception as exc:
            failures += 1
            print(f"FAIL 例{number} {type(exc).__name__}: {exc}")
    return bool(failures)


if __name__ == "__main__":
    sys.exit(main())
