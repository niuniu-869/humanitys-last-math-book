"""Check examples from their original inputs, including adjacent short tasks.

Values that an early draft got wrong (example 8's constant-discriminator value,
the sequential-update length in section 9) are checked against the corrected lesson text.
An unregistered discrepancy, missing erratum, or failed assertion is a FAIL.
"""
from pathlib import Path
import sys

import numpy as np
import sympy as s

ROOT = Path(__file__).resolve().parents[1]
LESSON = (ROOT / "lesson.md").read_text(encoding="utf-8")
R = s.Rational


def close(actual, printed, digits=4):
    # Absolute tolerance is half a unit in the last printed decimal place.
    np.testing.assert_allclose(actual, printed, rtol=0, atol=0.5 * 10**(-digits) + 1e-12)


def same(actual, expected):
    assert s.simplify(s.expand_log(actual - expected, force=True)) == 0, (actual, expected)


def gaussian(x, mean=0, variance=1):
    return np.exp(-(np.asarray(x) - mean)**2 / (2 * variance)) / np.sqrt(2 * np.pi * variance)


def kl(q, p):
    q, p = np.asarray(q, dtype=float), np.asarray(p, dtype=float)
    active = q > 0
    return np.sum(q[active] * np.log(q[active] / p[active]))


def gan(p, g):
    p, g = np.asarray(p), np.asarray(g)
    d = p / (p + g)
    a, b = p > 0, g > 0
    value = np.sum(p[a] * np.log(d[a])) + np.sum(g[b] * np.log(1 - d[b]))
    mix = (p + g) / 2
    js = (kl(p, mix) + kl(g, mix)) / 2
    close(value, 2 * js - np.log(4), 12)
    return d, value, js


def example1():
    densities = gaussian(np.array([1., 2.]))
    close(densities, [0.2420, 0.0540])
    joint = np.array([0.4, 0.6]) * densities
    close(joint, [0.0968, 0.0324])
    close(joint.sum(), 0.1292)
    close(np.log(joint.sum()), -2.0465)
    posterior = joint / joint.sum()
    close(posterior, [0.7492, 0.2508])
    assert posterior[0] > posterior[1]
    short_joint = 0.5 * densities
    close(short_joint, [0.1210, 0.0270])
    close(short_joint.sum(), 0.1480)
    close(short_joint[0] / short_joint.sum(), 0.8176)


def example2():
    x = np.array([1., 4.])
    a, b = np.log(x.mean()), np.log(x).mean()
    close([a, b, a - b], [0.9163, 0.6931, 0.2231])
    assert a > b
    x = np.array([1., 9.])
    a, b = np.log(x.mean()), np.log(x).mean()
    close([a, b, a - b], [1.6094, 1.0986, 0.5108])


def example3():
    prior, q = np.array([0.4, 0.6]), np.array([0.5, 0.5])
    conditional = gaussian(np.array([1., 2.]))
    joint = conditional * prior
    posterior = joint / joint.sum()
    elbo = np.sum(q * np.log(joint / q))
    reconstruction = np.sum(q * np.log(conditional))
    prior_kl = kl(q, prior)
    gap = np.log(joint.sum()) - elbo
    close([elbo, reconstruction, prior_kl, gap], [-2.1893, -2.1689, 0.0204, 0.1428])
    close(reconstruction - prior_kl, elbo, 12)
    close(gap, kl(q, posterior), 12)
    close(np.sum(posterior * np.log(joint / posterior)), np.log(joint.sum()), 12)
    q = np.array([0.2, 0.8])
    short_elbo = np.sum(q * np.log(joint / q))
    close(short_elbo, -2.7105)
    close(np.log(joint.sum()) - short_elbo, 0.664, 3)


def example4():
    x = np.array([-2., -1., 0., 3., 4.])
    mu, weights = np.array([-1., 1.]), np.array([0.5, 0.5])
    likelihoods = []
    for iteration in range(3):
        joint = gaussian(x[:, None], mu) * weights
        likelihoods.append(np.log(joint.sum(axis=1)).sum())
        r = joint / joint.sum(axis=1)[:, None]
        if iteration == 0:
            close(r[:3, 0], [0.982, 0.881, 0.5], 3)
            close(r[3:, 0], [0.0025, 0.0003])
            close(r.sum(axis=0), [2.366, 2.634], 3)
        if iteration == 1:
            close(mu, [-1.199, 2.595], 3)
            close(weights, [0.473, 0.527], 3)
        if iteration == 2:
            close(mu, [-1.025, 3.373], 3)
        mu = (r * x[:, None]).sum(axis=0) / r.sum(axis=0)
        weights = r.mean(axis=0)
    close(likelihoods, [-14.719, -10.172, -9.225], 3)
    assert np.all(np.diff(likelihoods) > 0)


def example5():
    # Gauss-Hermite quadrature integrates these Gaussian polynomials exactly
    # up to floating point precision, without using the textbook moment values.
    nodes, weights = np.polynomial.hermite.hermgauss(12)
    eps, weights = np.sqrt(2) * nodes, weights / np.sqrt(np.pi)
    z = 1 + 0.5 * eps
    path_mu, path_sigma = 2 * z, 2 * z * eps
    score = z**2 * (z - 1) / 0.25
    close([weights @ path_mu, weights @ path_sigma, weights @ score], [2, 1, 2], 10)
    close(weights @ (path_mu - weights @ path_mu)**2, 1, 10)
    close(weights @ (score - weights @ score)**2, 21.75, 10)
    sampled_z = 1 + 0.5 * 0.8
    close([sampled_z, 2 * sampled_z, 2 * sampled_z * 0.8], [1.4, 2.8, 2.24], 10)
    sampled_z = 1 + 0.5 * (-0.4)
    close([sampled_z, 2 * (sampled_z - 2), 2 * (sampled_z - 2) * (-0.4)],
          [0.8, -2.4, 0.96], 10)
    close([weights @ (2 * (z - 2)), weights @ (2 * (z - 2) * eps)], [-2, 1], 10)


def example6():
    nodes, weights = np.polynomial.hermite.hermgauss(12)
    eps, weights = np.sqrt(2) * nodes, weights / np.sqrt(np.pi)
    parts = []
    for mu, sigma in [(1, 0.5), (0, 2), (2, 1)]:
        z = mu + sigma * eps
        # Compute the expected log density ratio directly.
        parts.append(weights @ (np.log(gaussian(z, mu, sigma**2)) - np.log(gaussian(z))))
    close(parts[:2], [0.8181, 0.8069])
    close(sum(parts[:2]), 1.625, 3)
    close(parts[2], 2, 10)


def example7():
    mu, sigma = s.symbols("mu sigma", positive=True)
    z = mu + sigma * R(4, 5)
    reconstruction = (3 - 2 * z)**2 / 2
    prior = (mu**2 + sigma**2 - 1 - s.log(sigma**2)) / 2
    loss = reconstruction + prior
    point = {mu: 1, sigma: R(1, 2)}
    same(z.subs(point), R(7, 5))
    same((2 * z).subs(point), R(14, 5))
    same(reconstruction.subs(point), R(1, 50))
    close(float(loss.subs(point)), 0.8381)
    same(s.diff(loss, mu).subs(point), R(3, 5))
    same(s.diff(loss, sigma).subs(point), -R(91, 50))
    assert s.diff(loss, mu).subs(point) > 0
    assert s.diff(loss, sigma).subs(point) < 0


def example8():
    p, g = np.array([0.6, 0.4]), np.array([0.2, 0.8])
    d, value, js = gan(p, g)
    close(d, [0.75, 1 / 3], 12)
    close(value, -1.2137)
    mix = (p + g) / 2
    close([kl(p, mix), kl(g, mix), js], [0.0811, 0.0915, 0.0863])
    constant_value = np.sum(p * np.log(0.5) + g * np.log(0.5))
    close(constant_value, -1.3863)
    close(constant_value, 2 * np.log(0.5), 12)
    assert value > constant_value
    assert not np.isclose(constant_value, np.log(0.5))
    assert r"2\log\frac12=-\log4" in LESSON or r"V=-\log4" in LESSON
    d, value, js = gan([0.5, 0.5], [0.25, 0.75])
    close(d, [2 / 3, 0.4], 12)
    close(value, -1.3187)
    excess = value + np.log(4)
    close(excess, 0.0676)
    close(excess, 2 * js, 12)
    assert abs(excess - 0.0338) > 0.03
    assert "高 $0.0676$" in LESSON or "高 0.0676" in LESSON


def example9():
    d, value, js = gan([0.5, 0.5], [1., 0.])
    close(d, [1 / 3, 1.], 12)
    close(js, 0.2158)
    close(value, -0.9548)
    close(value + np.log(4), 0.43, 2)
    assert js < np.log(2)
    x, y, eta = s.symbols("x y eta", real=True)
    simultaneous_norm = (x - eta * y)**2 + (y + eta * x)**2
    same(simultaneous_norm, (1 + eta**2) * (x**2 + y**2))
    # Literal sequential assignment uses the NEW x in the y update.
    state = s.Matrix([1, 0])
    step = R(1, 10)
    sequential = s.Matrix([[1, -step], [step, 1 - step**2]])
    first, second = sequential * state, sequential**2 * state
    same(first.dot(first), R(101, 100))
    same(second.dot(second), R(1019701, 1000000))
    assert second.dot(second) != (1 + step**2) * first.dot(first)
    assert "每一步距离平方乘以" in LESSON and "同时更新" in LESSON


def main():
    failures = 0
    for number in range(1, 10):
        try:
            globals()[f"example{number}"]()
            warning = {
                8: "；已核验恒定取值与 JS 差值",
                9: "；已核验同时更新与依次更新的区别",
            }.get(number, "")
            print(f"PASS 例{number}{warning}")
        except Exception as exc:
            failures += 1
            print(f"FAIL 例{number} {type(exc).__name__}: {exc}")
    return int(failures != 0)


if __name__ == "__main__":
    sys.exit(main())
