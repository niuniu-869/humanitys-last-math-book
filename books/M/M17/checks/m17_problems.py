"""Recompute each exercise from independent standard-normal coordinates.

Expected expressions are transcribed from answers.md; anchor checks keep those
fixtures tied to the printed answers. Choice truth values are computed for all
four options, then compared with the answer letter read from answers.md.
"""

from pathlib import Path
import re
import sys

import sympy as sp


R = sp.Rational
ROOT = Path(__file__).resolve().parents[1]
ANSWERS = (ROOT / "answers.md").read_text(encoding="utf-8")
BLOCKS = {
    match.group(1): match.group(2)
    for match in re.finditer(
        r"^\*\*(M17-\d+)\*\*\n(.*?)(?=^\*\*M17-|\Z)",
        ANSWERS,
        re.M | re.S,
    )
}


def equal(actual, expected):
    assert sp.simplify(actual - expected) == 0, (actual, expected)


def printed(number, *expressions):
    block = BLOCKS[f"M17-{number:02d}"]
    for expression in expressions:
        assert expression in block, f"Answer fixture absent: {expression}"


def moments(expression, coordinates):
    """Mean/variance of an affine expression in independent N(0,1) inputs."""
    expression = sp.expand(expression)
    poly = sp.Poly(expression, *coordinates)
    assert poly.total_degree() <= 1
    mean = expression.subs(dict.fromkeys(coordinates, 0))
    variance = sum(sp.diff(expression, z) ** 2 for z in coordinates)
    return sp.simplify(mean), sp.simplify(variance)


def mse(expression, coordinates):
    mean, variance = moments(expression, coordinates)
    return sp.expand(mean ** 2 + variance)


def covariance(left, right, coordinates):
    return sp.simplify(sum(sp.diff(left, z) * sp.diff(right, z) for z in coordinates))


def choice(number, truth):
    # Every option is evaluated, including invalid or false alternatives.
    selected = ["ABCD"[i] for i, value in enumerate(truth) if bool(value)]
    assert len(selected) == 1, truth
    match = re.search(r"\*\*答案：\*\* \(([ABCD])\)", BLOCKS[f"M17-{number:02d}"])
    assert match and selected == [match.group(1)], (truth, selected)


e1, e2, z = sp.symbols("e1 e2 z", real=True)


def problem01():
    a = sp.symbols("a", positive=True)
    _, total_variance = moments(a * e1 + R(3, 5) * e2, (e1, e2))
    coefficient = sp.solve(total_variance - 1, a)[0]
    mean, variance = moments(5 * coefficient + R(3, 5) * e2, (e2,))
    options = [(R(16, 5), R(9, 25)), (4, R(3, 5)), (4, R(9, 25)), (4, R(16, 25))]
    choice(1, [mean == m and variance == v for m, v in options])


def problem02():
    mean, variance = moments(R(3, 5) * e1 - R(4, 5) * e2, (e1, e2))
    options = [(0, R(49, 25)), (0, R(-7, 25)), (0, R(1, 25)), (0, 1)]
    choice(2, [v > 0 and mean == m and variance == v for m, v in options])


def problem03():
    bars = [R(3, 4), R(1, 2), R(1, 8)]
    actual = [1 - bars[1] / bars[0], 1 - bars[2] / bars[1], bars[2] / (1 - bars[2])]
    for result, expected in zip(actual, [R(1, 3), R(3, 4), R(1, 7)]):
        equal(result, expected)
    printed(3, r"\beta_2=1/3", r"\beta_3=3/4", r"\mathrm{SNR}_3=1/7")


def problem04():
    x0 = sp.symbols("x0", real=True)
    xt = x0 / 2 + sp.sqrt(3) * e1 / 2
    initial = sp.solve(xt.subs(e1, -1 / sp.sqrt(3)) - 1, x0)[0]
    mean, variance = moments(xt.subs(x0, initial), (e1,))
    equal(initial, 3)
    equal(mean, R(3, 2))
    equal(variance, R(3, 4))
    printed(4, "x_0=3", "N(3/2,3/4)")


def problem05():
    x1 = sp.sqrt(3) * e1 / 2
    x2 = x1 / 2 + sp.sqrt(3) * e1 / 2
    independent_x2 = x1 / 2 + sp.sqrt(3) * e2 / 2
    mean, variance = moments(x2, (e1,))
    _, independent_variance = moments(independent_x2, (e1, e2))
    equal(mean, 0)
    equal(variance, R(27, 16))
    equal(independent_variance, R(15, 16))
    equal(variance - independent_variance, R(3, 4))
    assert variance != independent_variance
    printed(5, "不成立", "N(0,27/16)", "多了 $3/4$")


def problem06():
    x1 = sp.sqrt(3) * e1 / 2
    x2 = x1 / 2 + sp.sqrt(3) * e2 / 2
    y = sp.sqrt(15) * z / 4
    mx, vx = moments(x2, (e1, e2, z))
    my, vy = moments(y, (e1, e2, z))
    _, difference_variance = moments(x2 - y, (e1, e2, z))
    given_e1 = sp.solve(x1 - 1, e1)[0]
    conditional_x_mean, _ = moments(x2.subs(e1, given_e1), (e2, z))
    conditional_y_mean, _ = moments(y, (e2, z))
    choice(6, [
        difference_variance == 0,
        conditional_x_mean == conditional_y_mean,
        sp.simplify(vx - sp.sqrt(15) / 4) == 0,
        mx == my and vx == vy,
    ])
    equal(difference_variance, R(15, 8))
    equal(conditional_x_mean, R(1, 2))
    equal(covariance(x1, x2, (e1, e2, z)), R(3, 8))
    equal(moments(x2 - x1 / 2, (e1, e2, z))[1], R(3, 4))
    equal(covariance(x1, y, (e1, e2, z)), 0)
    equal(moments(y - x1 / 2, (e1, e2, z))[1], R(9, 8))
    assert covariance(x1, x2, (e1, e2, z)) != covariance(x1, y, (e1, e2, z))
    printed(6, "3/8,3/4,0,9/8", "不能保证路径分布相同")


def problem07():
    b1, b2 = sp.symbols("b1 b2", real=True)
    bar = (1 - b1) * (1 - b2)
    solution = sp.solve(bar - R(1, 4), b2)[0]
    equal(solution, (R(3, 4) - b1) / (1 - b1))
    allowed = sp.reduce_inequalities([b1 > 0, b1 < 1, solution > 0, solution < 1], b1)
    assert allowed.as_set() == sp.Interval.open(0, R(3, 4))
    swapped = bar.xreplace({b1: b2, b2: b1})
    equal(bar, swapped)
    equal_candidates = sp.solve(bar.subs(b2, b1) - R(1, 4), b1)
    feasible = [value for value in equal_candidates if 0 < value < R(3, 4)]
    assert feasible == [R(1, 2)]
    printed(7, r"\dfrac{3/4-\beta_1}{1-\beta_1}", r"0<\beta_1<3/4", r"\beta_1=1/2")


def problem08():
    a = sp.symbols("a", real=True)
    snr2, snr3 = a ** 2 / (1 - a ** 2), a ** 3 / (1 - a ** 3)
    feasible = sp.reduce_inequalities([a > 0, a < 1, snr2 >= R(1, 3), snr3 <= R(1, 7)], a)
    strict = sp.reduce_inequalities([a > 0, a < 1, snr2 > R(1, 3), snr3 <= R(1, 7)], a)
    assert feasible.as_set() == sp.FiniteSet(R(1, 2))
    assert strict.as_set() == sp.EmptySet
    printed(8, "b=1/2", "严格不等式后无解")


def problem09():
    a, b = sp.symbols("a b", real=True)
    u = 1 + sp.sqrt(3) * e1 / 2
    v = -R(1, 2) + sp.sqrt(3) * e2 / 2
    mean, _ = moments(a * u + b * v, (e1, e2))
    weights = sp.solve([a + b - 1, mean], (a, b))
    equal(weights[a], R(1, 3))
    equal(weights[b], R(2, 3))
    assert all(weight >= 0 for weight in weights.values())
    mean, variance = moments((a * u + b * v).subs(weights), (e1, e2))
    equal(mean, 0)
    equal(variance, R(5, 12))
    printed(9, "a=1/3", "b=2/3", "N(0,5/12)")


def problem10():
    r = sp.symbols("r", positive=True)
    initial, epsilon, prediction = sp.symbols("initial epsilon prediction", real=True)
    xt = sp.sqrt(r) * initial + sp.sqrt(1 - r) * epsilon
    reconstructed = (xt - sp.sqrt(1 - r) * prediction) / sp.sqrt(r)
    multiplier = sp.simplify((reconstructed - initial) ** 2 / (prediction - epsilon) ** 2)
    equal(multiplier, (1 - r) / r)
    first, second = [sp.simplify(multiplier.subs(r, value) / 25) for value in [R(4, 5), R(1, 5)]]
    equal(first, R(1, 100))
    equal(second, R(4, 25))
    equal(second / first, 16)
    printed(10, r"\frac{1-r}{r}", "1/100", "4/25", "16 倍")


def problem12():
    r, s = sp.symbols("r s", positive=True)
    m, a, b, c = sp.symbols("m a b c", real=True)
    y = sp.sqrt(r) * (m + s * z) + sp.sqrt(1 - r) * e1
    loss = mse(e1 - a * y - b, (z, e1))
    optimum = sp.solve([sp.diff(loss, a), sp.diff(loss, b)], (a, b))
    v = r * s ** 2 + 1 - r
    equal(optimum[a], sp.sqrt(1 - r) / v)
    equal(optimum[b], -m * sp.sqrt(r) * sp.sqrt(1 - r) / v)
    minimum = sp.simplify(loss.subs(optimum))
    equal(minimum, r * s ** 2 / v)
    # Positive definite quadratic: first leading minor v + r*m^2,
    # determinant v. Under 0 < r < 1 and s > 0 both are positive.
    quadratic = sp.hessian(loss, (a, b)) / 2
    equal(quadratic[0, 0], v + r * m ** 2)
    equal(quadratic.det(), v)
    restricted_loss = mse(e1 - c * y, (z, e1))
    best_c = sp.solve(sp.diff(restricted_loss, c), c)[0]
    restricted_minimum = sp.simplify(restricted_loss.subs(c, best_c))
    equal(best_c, sp.sqrt(1 - r) / (v + r * m ** 2))
    equal(restricted_minimum, r * (s ** 2 + m ** 2) / (v + r * m ** 2))
    gap = sp.factor(restricted_minimum - minimum)
    equal(gap, r * (1 - r) * m ** 2 / (v * (v + r * m ** 2)))
    # With the stipulated positive factors, only m = 0 makes the gap zero.
    assert sp.solve(sp.together(gap).as_numer_denom()[0], m) == [0]
    printed(12, "a=\\sqrt{1-r}/v", "b=-m\\sqrt{r(1-r)}/v", "rs^2/v",
            "c=\\sqrt{1-r}/(v+rm^2)", "r(s^2+m^2)/(v+rm^2)",
            "r(1-r)m^2/[v(v+rm^2)]", "当且仅当 $m=0$")


def problem13():
    k, t = sp.symbols("k t", integer=True, positive=True)
    first = sp.product(k / (k + 1), (k, 1, t))
    second = sp.product(k / (k + 1), (k, 1, t)) * sp.product((k + 2) / (k + 1), (k, 1, t))
    equal(first, 1 / (t + 1))
    equal(second, (t + 2) / (2 * (t + 1)))
    equal(sp.limit(first, t, sp.oo), 0)
    equal(sp.limit(second, t, sp.oo), R(1, 2))
    equal(sp.limit(sp.sqrt(first), t, sp.oo), 0)
    equal(sp.limit(sp.sqrt(second), t, sp.oo), 1 / sp.sqrt(2))
    equal(sp.limit(1 - first, t, sp.oo), 1)
    equal(sp.limit(1 - second, t, sp.oo), R(1, 2))
    equal(first / (1 - first), 1 / t)
    assert first.subs(t, 98) > R(1, 100)
    assert first.subs(t, 99) <= R(1, 100)
    printed(13, "1/(t+1)", "(t+2)/[2(t+1)]", "N(x_0/\\sqrt2,1/2)", "1/t", "99")


def problem14():
    theta = sp.symbols("theta", real=True)
    pairs = [(1, 0), (0, 1)]
    inputs = [R(1, 2) * x0 + sp.sqrt(3) * eps / 2 for x0, eps in pairs]
    equal(inputs[0], R(1, 2))
    equal(inputs[1], sp.sqrt(3) / 2)
    loss = sum((eps - theta * x) ** 2 for x, (_, eps) in zip(inputs, pairs)) / 2
    gradient = sp.diff(loss, theta)
    optimum = sp.solve(gradient, theta)[0]
    equal(optimum, sp.sqrt(3) / 2)
    equal(loss.subs(theta, optimum), R(1, 8))
    assert sp.diff(gradient, theta) > 0
    equal(-R(1, 2) * gradient.subs(theta, 0), sp.sqrt(3) / 4)
    equal(loss, (theta - sp.sqrt(3) / 2) ** 2 / 2 + R(1, 8))
    printed(14, "1/2", "\\sqrt3/2", "1/8", "\\sqrt3/4")


def problem15():
    x = sp.symbols("x", real=True)
    exponent = -(x - 1) ** 2 / 4 - (x + 1) ** 2 / 2
    center = sp.solve(sp.diff(exponent, x), x)[0]
    variance = -1 / sp.diff(exponent, x, 2)
    product_density = sp.exp(exponent) / (2 * sp.sqrt(2) * sp.pi)
    normalizer = sp.integrate(product_density, (x, -sp.oo, sp.oo))
    equal(center, -R(1, 3))
    equal(variance, R(2, 3))
    equal(normalizer, sp.exp(-R(2, 3)) / sp.sqrt(6 * sp.pi))
    normal_density = sp.exp(-(x - center) ** 2 / (2 * variance)) / sp.sqrt(2 * sp.pi * variance)
    equal(product_density / normalizer, normal_density)
    mean_sum, variance_sum = moments(1 + sp.sqrt(2) * e1 - 1 + e2, (e1, e2))
    equal(mean_sum, 0)
    equal(variance_sum, 3)
    printed(15, "N(-1/3,2/3)", "Z=e^{-2/3}/\\sqrt{6\\pi}", "N(0,3)")


def main():
    failures = 0
    for number in range(1, 16):
        label = f"M17-{number:02d}"
        if number == 11:
            print(f"MANUAL {label} 归纳证明及极限、单调性须人工核对")
            continue
        try:
            globals()[f"problem{number:02d}"]()
            print(f"PASS {label}")
        except Exception as exc:
            failures += 1
            print(f"FAIL {label} {type(exc).__name__}: {exc}")
    return failures > 0


if __name__ == "__main__":
    sys.exit(main())
