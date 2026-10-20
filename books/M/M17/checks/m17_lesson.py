"""Check all ten worked examples, including their follow-up calculations.

Exact calculations use SymPy rationals; the long schedule uses NumPy. Displayed
decimals are checked at their printed precision. Only later values computed
from already rounded intermediates receive an explicit propagated tolerance.
"""

import sys

import numpy as np
import sympy as sp


R = sp.Rational


def exact(actual, expected):
    assert sp.simplify(actual - expected) == 0, (actual, expected)


def rounded(actual, expected, decimals, propagated=0):
    tolerance = 0.5 * 10 ** (-decimals) + propagated
    assert abs(float(actual) - expected) <= tolerance + 1e-12, (float(actual), expected, tolerance)


def forward(initial, betas, noises):
    values = []
    current = initial
    for beta, noise in zip(betas, noises):
        current = sp.sqrt(1 - beta) * current + sp.sqrt(beta) * noise
        values.append(sp.simplify(current))
    return values


def marginal(initial, betas):
    # Recur on the mean/variance, independently of the closed-form shortcut.
    mean, variance = initial, sp.S.Zero
    for beta in betas:
        mean = sp.sqrt(1 - beta) * mean
        variance = (1 - beta) * variance + beta
    return sp.simplify(mean), sp.simplify(variance)


def posterior(initial, betas, observed):
    # Complete the square in the two log densities, instead of calling the
    # posterior formulas printed in the lesson.
    u = sp.symbols("u", real=True)
    mean, variance = marginal(initial, betas[:-1])
    beta = betas[-1]
    exponent = -(u - mean) ** 2 / (2 * variance) - (observed - sp.sqrt(1 - beta) * u) ** 2 / (2 * beta)
    center = sp.solve(sp.diff(exponent, u), u)[0]
    width = -1 / sp.diff(exponent, u, 2)
    return sp.simplify(center), sp.simplify(width)


def example1():
    beta = R(1, 10)
    rounded(sp.sqrt(1 - beta), 0.9487, 4)
    rounded(sp.sqrt(beta), 0.3162, 4)
    values = forward(2, [beta] * 3, [R(1, 2), -1, R(1, 5)])
    for actual, expected in zip(values, [2.0555, 1.6338, 1.6132]):
        rounded(actual, expected, 4)
    followup = forward(-1, [beta], [1])[0]
    rounded(followup, -0.6325, 4)
    mean, variance = marginal(-1, [beta])
    rounded(mean, -0.9487, 4)
    exact(variance, beta)


def example2():
    beta = R(1, 10)
    exact((1 - beta) * 4 + beta, R(37, 10))
    exact(4 + beta, R(41, 10))
    exact((1 - beta) * R(1, 4) + beta, R(325, 1000))
    assert abs(R(37, 10) - 1) < abs(4 - 1)
    assert abs(R(325, 1000) - 1) < abs(R(1, 4) - 1)


def example3():
    mean1, var1 = marginal(2, [R(1, 10)])
    mean2, var2 = marginal(2, [R(1, 10)] * 2)
    rounded(mean1, 1.8974, 4)
    exact(var1, R(1, 10))
    exact(mean2, R(18, 10))
    exact(var2, R(19, 100))
    mean, variance = marginal(2, [R(1, 5), R(1, 10)])
    rounded(mean, 1.697, 3)
    exact(variance, R(28, 100))
    exact((1 - R(1, 5)) * (1 - R(1, 10)), R(72, 100))


def example4():
    mean, variance = marginal(2, [R(1, 10)] * 3)
    exact(1 - variance, R(729, 1000))
    rounded(mean / 2, 0.8538, 4)
    rounded(mean, 1.7076, 4)
    exact(variance, R(271, 1000))
    rounded(sp.sqrt(variance), 0.5206, 4)
    path = forward(2, [R(1, 10)] * 3, [R(1, 2), -1, R(1, 5)])[-1]
    assert abs(float(path - mean)) < 0.52
    follow_mean, follow_var = marginal(-1, [R(1, 10)] * 2)
    exact(follow_mean, -R(9, 10))
    exact(follow_var, R(19, 100))


def example5():
    betas = np.linspace(1e-4, 0.02, 1000)
    bars = np.cumprod(1 - betas)
    bar = bars[499]  # Mathematical t = 500 has array index 499.
    rounded(bar, 0.0786, 4)
    rounded(np.sqrt(bar), 0.2803, 4)
    rounded(np.sqrt(1 - bar), 0.9599, 4)
    rounded(0.8 * np.sqrt(bar), 0.2243, 4)
    rounded(1 - bar, 0.9214, 4)
    # Also check the schedule numbers used between examples 5 and 6.
    rounded(np.sum(betas), 10.05, 2)
    rounded(np.exp(-sum(betas)), 4.3e-5, 6)
    assert bars[-1] <= np.exp(-np.sum(betas))
    rounded(bars[-1], 4.0e-5, 6)
    rounded(np.sqrt(bars[-1]), 0.006, 3)
    rounded(bars[99], 0.897, 3)
    for index, expected, decimals in [(99, 8.7, 1), (249, 1.1, 1), (499, 0.085, 3), (999, 4e-5, 5)]:
        rounded(bars[index] / (1 - bars[index]), expected, decimals)


def example6():
    for beta, expected, threshold in [(R(1, 10), 44, 43.7), (R(1, 20), 90, 89.8)]:
        step = 1
        while (1 - beta) ** step >= R(1, 100):
            step += 1
        assert step == expected
        assert (1 - beta) ** (step - 1) >= R(1, 100) > (1 - beta) ** step
        rounded(sp.log(R(1, 100)) / sp.log(1 - beta), threshold, 1)
    rounded(R(9, 10) ** 43, 0.01078, 5)
    rounded(R(9, 10) ** 44, 0.00970, 5)


def example7():
    z, eps, coefficient = sp.symbols("z eps coefficient", real=True)
    bar = R(9, 10) ** 3
    x3 = sp.sqrt(bar) * z + sp.sqrt(1 - bar) * eps
    variance = sp.diff(x3, z) ** 2 + sp.diff(x3, eps) ** 2
    covariance = sp.diff(x3, eps)
    exact(variance, 1)
    exact(covariance, sp.sqrt(R(271, 1000)))
    residual = eps - coefficient * x3
    loss = sp.diff(residual, eps) ** 2 + sp.diff(residual, z) ** 2
    optimum = sp.solve(sp.diff(loss, coefficient), coefficient)[0]
    rounded(optimum, 0.5206, 4)
    exact(loss.subs(coefficient, optimum), R(729, 1000))
    # The pair is jointly normal; hence the affine regression is the
    # conditional mean. The single-point comparison has zero residual.
    fixed, xt = sp.symbols("fixed xt", real=True)
    true_noise = (xt - sp.sqrt(bar) * fixed) / sp.sqrt(1 - bar)
    exact(true_noise.subs(xt, sp.sqrt(bar) * fixed + sp.sqrt(1 - bar) * eps), eps)


def example8():
    mean, variance = marginal(2, [R(1, 10)] * 3)
    xt = mean + sp.sqrt(variance) / 2
    rounded(mean, 1.7076, 4)
    rounded(sp.sqrt(variance) / 2, 0.2603, 4)
    rounded(xt, 1.9679, 4)
    output = sp.symbols("output", real=True)
    loss = (R(1, 2) - output) ** 2
    exact(loss.subs(output, R(1, 5)), R(9, 100))
    exact(sp.diff(loss, output).subs(output, R(1, 5)), -R(3, 5))


def example9():
    observed = R(19679, 10000)
    mean, variance = posterior(2, [R(1, 10)] * 3, observed)
    # The observed x3 came from example 8, rounded to four decimal places.
    rounded(observed / sp.sqrt(R(9, 10)), 2.0744, 4,
            propagated=0.5e-4 / np.sqrt(0.9))
    rounded(R(1, 9), 0.1111, 4)
    rounded(1 / R(19, 100), 5.263, 3)
    rounded(1 / R(19, 100) + 9, 14.263, 3)
    rounded(mean, 1.9731, 4)
    rounded(variance, 0.0701, 4)
    assert observed < mean < 2
    assert variance < R(19, 100) < R(271, 1000)
    # Exact epsilon for the rounded observation is slightly below 0.5.
    noise_form = (observed - R(1, 10) / sp.sqrt(R(271, 1000)) / 2) / sp.sqrt(R(9, 10))
    rounded(noise_form, 1.9731, 4)
    follow_mean, follow_var = posterior(2, [R(1, 10)] * 2, R(18, 10))
    rounded(follow_var, 0.0526, 4)
    rounded(follow_mean, 1.897, 3)
    rounded(sp.sqrt(R(9, 10)) * R(1, 10) / R(19, 100), 0.4993, 4)


def example10():
    beta, x0, current = R(1, 10), 2, R(19679, 10000)
    epsilons, values = [], []
    for t in (3, 2, 1):
        bar = (1 - beta) ** t
        eps = sp.simplify((current - sp.sqrt(bar) * x0) / sp.sqrt(1 - bar))
        next_value = sp.simplify((current - beta / sp.sqrt(1 - bar) * eps) / sp.sqrt(1 - beta))
        if t > 1:
            square_center, _ = posterior(x0, [beta] * t, current)
            exact(next_value, square_center)
        epsilons.append(eps)
        values.append(next_value)
        current = next_value
    for actual, expected in zip(values, [1.9731, 1.9838, 2.0]):
        rounded(actual, expected, 4)
    rounded(epsilons[0], 0.5, 4)
    # The text reuses rounded x, signal coefficients and noise coefficients.
    # First-order propagation gives < 0.00015 for epsilon at these steps.
    rounded(epsilons[1], 0.3972, 4, propagated=0.00015)
    rounded(epsilons[2], 0.2734, 4, propagated=0.00015)
    exact(values[-1], x0)


def main():
    failures = 0
    for number in range(1, 11):
        try:
            globals()[f"example{number}"]()
            print(f"PASS 例{number}")
        except Exception as exc:
            failures += 1
            print(f"FAIL 例{number} {type(exc).__name__}: {exc}")
    return failures > 0


if __name__ == "__main__":
    sys.exit(main())
