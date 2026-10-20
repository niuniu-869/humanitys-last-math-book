"""Independent calculations; expected expressions are transcribed from answers.md.

SymPy integrates densities and differentiates likelihoods. Finite Bernoulli
sample spaces are enumerated exactly, including every multiple-choice option.
SciPy supplies independently computed distribution quantiles when needed.
"""
from itertools import product
from pathlib import Path
import re
import sys

import numpy as np
import sympy as sp
from scipy.stats import chi2, f, norm, t

R = sp.Rational
ROOT = Path(__file__).resolve().parents[1]
ANSWERS = (ROOT / "answers.md").read_text(encoding="utf-8")
PROBLEMS = (ROOT / "problems.md").read_text(encoding="utf-8")
BLOCKS = dict(re.findall(
    r"\*\*(P11-\d+)\*\*\n(.*?)(?=\n\*\*P11-|\Z)", ANSWERS, re.S))
failures = 0
p = sp.symbols("p", positive=True)
n = sp.symbols("n", integer=True, positive=True)


def equal(actual, expected):
    assert sp.simplify(actual - expected) == 0, (actual, expected)


def near(actual, expected, atol=5e-4):
    assert np.allclose(np.asarray(actual, dtype=float), expected,
                       rtol=0, atol=atol), (actual, expected)


def text_has(pid, *parts):
    for part in parts:
        assert part in BLOCKS[pid], (pid, "answer text missing", part)


def run(pid, check):
    global failures
    try:
        check()
        print(f"PASS {pid}")
    except Exception as exc:
        failures += 1
        print(f"FAIL {pid}: {type(exc).__name__}: {exc}")


def choices(pid, actual, expected):
    # Each option has its own computed truth value, not merely an answer letter.
    for letter, got, want in zip("ABCD", actual, expected, strict=True):
        def check(got=got, want=want):
            assert bool(got) == want, (got, want)
        run(f"{pid} 选项{letter}", check)
    selected = "".join(k for k, v in zip("ABCD", actual) if bool(v))
    assert len(selected) == 1, selected
    text_has(pid, f"**答案：** ({selected})")


def bernoulli_expectation(size, statistic):
    return sp.expand(sum(
        statistic(xs) * p**sum(xs) * (1-p)**(size-sum(xs))
        for xs in product((0, 1), repeat=size)))


def p01():
    a1, a2 = R(10, 5), R(30, 5)
    mu, v = sp.symbols("mu v")
    sol = sp.solve([mu-a1, v+mu**2-a2], (mu, v), dict=True)[0]
    equal(sol[mu], 2)
    equal(sol[v], 2)
    equal((30-5*a1**2)/4, R(5, 2))
    text_has("P11-01", r"\hat\mu=2", r"\hat\sigma^2=2", r"s^2=5/2")


def p02():
    e_square = bernoulli_expectation(4, lambda xs: (R(sum(xs), 4))**2)
    e_product = bernoulli_expectation(4, lambda xs: xs[0]*xs[1])
    claims = [sp.simplify(e_square-p**2) == 0,
              sp.simplify(e_product-p**2) != 0,
              sp.simplify(e_product-p**2) == 0,
              sp.simplify(e_square-(p**2+4*p*(1-p))) == 0]
    choices("P11-02", claims, [False, False, True, False])
    equal(e_square, p**2+p*(1-p)/4)


def p03():
    q = sp.symbols("q", real=True)
    likelihood = q**5
    critical = sp.solve(sp.diff(likelihood, q), q)
    candidates = [sp.S.Zero, sp.S.One] + [x for x in critical if 0 <= x <= 1]
    best = max(candidates, key=lambda x: likelihood.subs(q, x))
    claims = [best == R(1, 2), best == 1, best == R(5, 6), not candidates]
    choices("P11-03", claims, [False, True, False, False])


def p04():
    z, sigma, total_width = R(196, 100), 2, R(8, 10)
    minimum = sp.ceiling((2*z*sigma/total_width)**2)
    equal(minimum, 97)
    assert 2*z*sigma/sp.sqrt(minimum) <= total_width
    assert 2*z*sigma/sp.sqrt(minimum-1) > total_width
    equal(z*sigma/sp.sqrt(100), R(392, 1000))
    text_has("P11-04", "$97$", "$0.392$")


def p05():
    qhi, qlo = 17.535, 2.180
    near([qhi, qlo], chi2.isf([.025, .975], 8))
    interval = np.array([8*4/qhi, 8*4/qlo])
    options = [[32/qlo, 32/qhi], [36/qhi, 36/qlo],
               np.sqrt([32/qhi, 32/qlo]), [32/qhi, 32/qlo]]
    claims = [np.allclose(v, interval) for v in options]
    choices("P11-05", claims, [False, False, False, True])
    near(chi2.cdf(32/interval[0], 8)-chi2.cdf(32/interval[1], 8), .95, 3e-5)


def p06():
    theta, x, mean, logs = sp.symbols("theta x mean logs", positive=True)
    first = sp.integrate(x*theta*x**(theta-1), (x, 0, 1))
    moment = sp.solve(first-mean, theta)[0]
    equal(moment, mean/(1-mean))
    # logs denotes -sum(log(x_i)), which is positive.
    log_likelihood = n*sp.log(theta)-(theta-1)*logs
    mle = sp.solve(sp.diff(log_likelihood, theta), theta)[0]
    equal(mle, n/logs)
    equal(sp.diff(log_likelihood, theta, 2), -n/theta**2)
    samples = [[R(1, 2), R(1, 2)], [R(1, 4), R(3, 4)]]
    expected = [1/sp.log(2), 2/sp.log(R(16, 3))]
    for xs, want in zip(samples, expected):
        equal(moment.subs(mean, sum(xs)/2), 1)
        got = mle.subs({n: 2, logs: -sum(sp.log(v) for v in xs)})
        equal(sp.expand_log(got, force=True), sp.expand_log(want, force=True))
    assert abs(float(expected[0]-expected[1])) > .2
    text_has("P11-06", r"1/\ln2", r"2/\ln(16/3)", "不成立")


def p07():
    bias = (1-2*p)/(n+2)
    variance = n*p*(1-p)/(n+2)**2
    mse = (n*p*(1-p)+(1-2*p)**2)/(n+2)**2
    for size in range(1, 7):
        est = lambda xs: R(sum(xs)+1, size+2)
        e1 = bernoulli_expectation(size, est)
        e2 = bernoulli_expectation(size, lambda xs: est(xs)**2)
        equal(e1-p, bias.subs(n, size))
        equal(e2-e1**2, variance.subs(n, size))
        direct_mse = bernoulli_expectation(size, lambda xs: (est(xs)-p)**2)
        equal(direct_mse, mse.subs(n, size))
    equal(sp.limit(mse, n, sp.oo), 0)
    assert sp.solve(bias, p) == [R(1, 2)]
    assert sp.simplify(bias) != 0
    text_has("P11-07", "不是无偏估计，但相合", "$p=1/2$")


def p08():
    n1, n2, sumsq1, sumsq2 = 5, 7, 5*8, 7*6
    s1, s2 = sumsq1/(n1-1), sumsq2/(n2-1)
    near([s1, s2], [10, 7])
    pooled = (sumsq1+sumsq2)/(n1+n2-2)
    near(pooled, 8.2)
    near([2.228, 9.197, 6.227],
         [t.isf(.025, 10), f.isf(.025, 6, 4), f.isf(.025, 4, 6)])
    half = 2.228*np.sqrt(pooled*(1/n1+1/n2))
    near([2-half, 2+half], [-1.736, 5.736])
    ratio = np.array([s2/s1/9.197, s2/s1*6.227])
    near(ratio, [.076, 4.359])
    assert ratio[0] < 1 < ratio[1]
    assert ratio[0] < 2 < ratio[1]  # Unequal ratios are also retained.
    text_has("P11-08", "[-1.736,", "5.736]", "[0.076,", "4.359]", "不能断定")


def p09():
    phat = 100/400
    half = 1.96*np.sqrt(phat*(1-phat)/400)
    near([phat-half, phat+half], [.208, .292])
    assert min(100, 400-100) >= 10
    formal = 0+np.array([-1, 1])*1.96*np.sqrt(0*(1-0)/20)
    near(formal, [0, 0], 0)
    assert min(0, 20) < 10
    probability = R(9, 10)**20
    near(float(probability), .1216, 5e-5)
    assert probability > 0
    text_has("P11-09", "[0.208,", "0.292]", "[0,0]", "$0.1216$")


def p11():
    theta, u, alpha = sp.symbols("theta u alpha", positive=True)
    xs = [3, 4, 5]
    feasible = [R(max(xs), 2), min(xs)]
    assert feasible == [R(5, 2), 3]
    equal(sp.diff(theta**(-n), theta), -n*theta**(-n-1))
    # Uniform(theta, 2*theta) becomes Uniform(0,1) under (X-theta)/theta.
    cdf_one = sp.integrate(1/theta, (sp.Symbol("x"), theta, theta*(1+u)))
    equal(cdf_one, u)
    cdf_max = cdf_one**n
    ev = sp.integrate(u*sp.diff(cdf_max, u), (u, 0, 1))
    em = sp.simplify(theta*(1+ev))
    correction = sp.simplify(theta/em)
    equal(correction, (n+1)/(2*n+1))
    a = 1+alpha**(1/n)
    coverage = sp.simplify(1-cdf_max.subs(u, a-1))
    equal(coverage, 1-alpha)
    # Verify interval inversion numerically on a deterministic parameter grid.
    for nn in (2, 3, 8):
        aa = 1+.05**(1/nn)
        for th in np.linspace(.1, 5, 80):
            for maximum in (.3, 2, 5):
                assert (aa <= maximum/th <= 2) == (maximum/2 <= th <= maximum/aa)
    text_has("P11-11", "[M/2,m]", r"c_n=(n+1)/(2n+1)",
             r"[M/2,\ M/(1+\alpha^{1/n})]")


def p12():
    lam, x = sp.symbols("lam x", positive=True)
    density = lam*sp.exp(-lam*x)
    likelihood = sp.prod(density.subs(x, v) for v in (1, 3))
    for threshold in (2, 4, 5):
        likelihood *= sp.integrate(density, (x, threshold, sp.oo))
    equal(likelihood, lam**2*sp.exp(-15*lam))
    best = sp.solve(sp.diff(likelihood, lam), lam)[0]
    equal(best, R(2, 15))
    tail = sp.integrate(density, (x, 3, sp.oo))
    equal(tail.subs(lam, best), sp.exp(-R(2, 5)))
    wrong_likelihood = sp.prod(density.subs(x, v) for v in (1, 3, 2, 4, 5))
    wrong = sp.solve(sp.diff(wrong_likelihood, lam), lam)[0]
    equal(wrong, R(1, 3))
    total = sp.symbols("total", positive=True)
    all_censored = sp.exp(-total*lam)
    assert sp.diff(all_censored, lam).is_negative
    equal(sp.limit(all_censored, lam, 0, dir="+"), 1)
    assert sp.solve(all_censored-1, lam) == []  # No positive maximizer.
    text_has("P11-12", r"\hat\lambda=2/15", r"\hat q=e^{-2/5}", "不存在最大似然估计")


def p13():
    m = sp.symbols("m", positive=True, integer=True)
    sigma = sp.symbols("sigma", positive=True)
    z = sp.symbols("z", real=True)
    normal_density = sp.exp(-z**2/2)/sp.sqrt(2*sp.pi)
    e2 = sp.integrate(z**2*normal_density, (z, -sp.oo, sp.oo))
    e4 = sp.integrate(z**4*normal_density, (z, -sp.oo, sp.oo))
    equal(sigma**2/m*m*e2, sigma**2)
    equal((sigma**2/m)**2*m*(e4-e2**2), 2*sigma**4/m)
    k = sp.symbols("k", positive=True, integer=True)
    excess = (2*sigma**4/m-2*sigma**4/(2*m-1)).subs(m, k+1)
    assert sp.factor(excess).is_positive
    # Disjoint row differences have diagonal covariance 2*sigma^2*I.
    for size in (2, 3, 7):
        contrasts = np.zeros((size, 2*size))
        for j in range(size):
            contrasts[j, 2*j:2*j+2] = [-1, 1]
        near(contrasts @ contrasts.T, 2*np.eye(size), 0)
        qlo, qhi = chi2.isf([.975, .025], size)
        near(chi2.cdf(qhi, size)-chi2.cdf(qlo, size), .95, 1e-12)
        for observed in (.2, 1, 4):
            interval = [size*observed/qhi, size*observed/qlo]
            near([size*observed/interval[1], size*observed/interval[0]],
                 [qlo, qhi], 1e-12)
    text_has("P11-13", r"2\sigma^4/m", r"\chi^2(m)", "$S^2$ 更有效")


def p14():
    sigma2, tau2 = sp.symbols("sigma2 tau2", positive=True)
    transform = sp.Matrix([[1, 0], [1, 1]])
    covariance = transform*sp.diag(sigma2, tau2)*transform.T
    equal(covariance[0, 1], sigma2)
    d = np.array([3, 7, 2, 7, 5])-np.array([2, 5, 1, 4, 3])
    near([d.mean(), d.var(ddof=1)], [1.8, .7], 1e-12)
    half = 2.776*d.std(ddof=1)/np.sqrt(len(d))
    near(d.mean()+np.array([-1, 1])*half, [.761, 2.839])
    text_has("P11-14", "[0.761,", "2.839]", r"\sigma^2>0")


def p15():
    for size in range(2, 8):
        ek = bernoulli_expectation(size, lambda xs: sum(xs)*(size-sum(xs)))
        equal(ek, size*(size-1)*p*(1-p))
        equal(ek/(size*(size-1)), p*(1-p))
        equal(ek/size**2, R(size-1, size)*p*(1-p))
    q = sp.symbols("q", real=True)
    likelihood = q**2*(1-q)**3
    candidates = [0, 1]+[v for v in sp.solve(sp.diff(likelihood, q), q) if 0 <= v <= 1]
    mle = max(candidates, key=lambda v: likelihood.subs(q, v))
    equal(mle*(1-mle), R(24, 100))
    equal(R(2*(5-2), 5*4), R(30, 100))
    text_has("P11-15", r"c_n=1/[n(n-1)]", "$0.24$", "$0.30$")


def p16():
    near([1.753, 7.261], [t.isf(.05, 15), chi2.isf(.95, 15)])
    lower_mu = 3-1.753*np.sqrt(4/16)
    upper_mean = 5-2*lower_mu
    upper_sd = abs(-2)*np.sqrt(15*4/7.261)
    near([upper_mean, upper_sd], [.753, 5.749])
    near(t.cdf(1.753, 15), .95, 1e-4)
    near(chi2.sf(7.261, 15), .95, 1e-5)
    text_has("P11-16", "$0.753$", "$5.749$")


if __name__ == "__main__":
    expected_ids = [f"P11-{i:02d}" for i in range(1, 17)]
    assert re.findall(r"^\*\*(P11-\d+)\*\*", PROBLEMS, re.M) == expected_ids
    assert list(BLOCKS) == expected_ids
    for number, check in [(1, p01), (2, p02), (3, p03), (4, p04), (5, p05),
                          (6, p06), (7, p07), (8, p08), (9, p09)]:
        run(f"P11-{number:02d}", check)
    print("MANUAL P11-10 证明：展开两两差值并逐项取期望")
    for number, check in [(11, p11), (12, p12), (13, p13), (14, p14),
                          (15, p15), (16, p16)]:
        run(f"P11-{number:02d}", check)
    sys.exit(bool(failures))
