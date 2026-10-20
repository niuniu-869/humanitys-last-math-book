"""Check the posterior mean sign and the fixed-variance Gaussian KL term."""

import sys

import sympy as sp


def equal(actual, expected):
    assert sp.simplify(actual - expected) == 0, (actual, expected)


def mean_difference():
    # a = alpha_t, r = bar_alpha_(t-1); both lie in (0, 1).
    a, r = sp.symbols("a r", positive=True)
    xt, eps, predicted = sp.symbols("xt eps predicted", real=True)
    beta, bar = 1 - a, a * r
    initial = (xt - sp.sqrt(1 - bar) * eps) / sp.sqrt(bar)
    posterior = (sp.sqrt(r) * beta * initial
                 + sp.sqrt(a) * (1 - r) * xt) / (1 - bar)
    model = (xt - beta * predicted / sp.sqrt(1 - bar)) / sp.sqrt(a)
    difference = sp.simplify(posterior - model)
    equal(difference, -beta * (eps - predicted) / sp.sqrt(a * (1 - bar)))
    variance = sp.symbols("variance", positive=True)
    equal(difference ** 2 / (2 * variance),
          beta ** 2 * (eps - predicted) ** 2 / (2 * variance * a * (1 - bar)))


def gaussian_kl():
    mq, mp, z = sp.symbols("mq mp z", real=True)
    vq, vp = sp.symbols("vq vp", positive=True)
    x = mq + sp.sqrt(vq) * z
    logq = -sp.log(2 * sp.pi * vq) / 2 - (x - mq) ** 2 / (2 * vq)
    logp = -sp.log(2 * sp.pi * vp) / 2 - (x - mp) ** 2 / (2 * vp)
    poly = sp.Poly(sp.expand(logq - logp), z)
    assert poly.degree() == 2
    # Under q, E[z] = 0 and E[z^2] = 1.
    kl = poly.nth(0) + poly.nth(2)
    constant = (sp.log(vp / vq) + vq / vp - 1) / 2
    equal(kl, (mq - mp) ** 2 / (2 * vp) + constant)
    equal(sp.diff(constant, mp), 0)
    equal(constant.subs(vp, vq), 0)
    beta = sp.Rational(1, 10)
    posterior_variance = beta * (1 - (1 - beta) ** 2) / (1 - (1 - beta) ** 3)
    value = constant.subs({vp: beta, vq: posterior_variance})
    assert value > 0
    assert abs(float(value) - 0.02810088) < 5e-9


def main():
    failures = 0
    for name, check in [("后验均值差符号", mean_difference), ("固定方差KL常数", gaussian_kl)]:
        try:
            check()
            print(f"PASS {name}")
        except Exception as exc:
            failures += 1
            print(f"FAIL {name} {type(exc).__name__}: {exc}")
    return failures > 0


if __name__ == "__main__":
    sys.exit(main())
