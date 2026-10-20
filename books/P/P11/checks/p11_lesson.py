"""Recompute all 27 numbered examples without changing lesson.md.

Exact identities use symbolic integration/differentiation or covariance
matrices. Numerical intervals use raw observations and independently obtained
SciPy quantiles. Tolerances reflect the displayed decimal precision.
"""
from pathlib import Path
import re
import sys

import numpy as np
import sympy as sp
from scipy.stats import binom, chi2, f, norm, t

R = sp.Rational
n = sp.symbols("n", positive=True, integer=True)
theta, lam = sp.symbols("theta lam", positive=True)
u, s = sp.symbols("u s", positive=True)
failures = 0
intervals = np.array([12, 31, 8, 22, 17], dtype=float)
uniform_data = [R(1, 2), R(4, 5), R(7, 10), sp.Integer(3)]
heights = np.array([168, 172, 175, 166, 174], dtype=float)
lengths = np.array([12.1, 11.6, 12.4, 11.9, 12.3, 11.7])
group1 = np.array([50.1, 49.8, 50.4, 50.0, 49.7, 50.3])
group2 = np.array([50.6, 50.9, 50.4, 50.7, 51.0, 50.5, 50.8])


def equal(actual, expected):
    assert sp.simplify(actual-expected) == 0, (actual, expected)


def near(actual, expected, atol):
    assert np.allclose(np.asarray(actual, dtype=float), expected,
                       rtol=0, atol=atol), (actual, expected)


def symmetric(center, half):
    return center+np.array([-1, 1])*half


def quantile(distribution, alpha, expected, *args):
    actual = distribution.isf(alpha, *args)
    near(actual, expected, .0005)
    return actual


def maximum_moments():
    density = sp.diff(u**n, u)
    return [sp.integrate((theta*u)**k*density, (u, 0, 1)) for k in (1, 2)]


def ex01():
    data = np.array([2, 4, 3, 1, 5, 3, 2, 4])
    near(data.mean(), 3, 0)


def ex02():
    mean = intervals.mean()
    second = np.mean(intervals**2)
    near([mean, second], [18, 388.4], 1e-10)
    x = sp.symbols("x", positive=True)
    theoretical = sp.integrate(x*lam*sp.exp(-lam*x), (x, 0, sp.oo))
    equal(theoretical, 1/lam)
    near([1/mean, np.sqrt(2/second)], [.0556, .0718], .00005)
    near(60/mean, 3.3, .05)


def ex03():
    mean = sum(uniform_data)/len(uniform_data)
    equal(mean, R(5, 4))
    equal(2*mean, R(5, 2))
    assert max(uniform_data) > 2*mean


def ex04():
    mean = heights.mean()
    ss = np.sum((heights-mean)**2)
    near([mean, ss, ss/5, ss/4], [171, 60, 12, 15], 1e-12)


def ex05():
    p = sp.symbols("p", real=True)
    likelihood = p**6*(1-p)**4
    critical = sp.solve(sp.diff(likelihood, p), p)
    candidates = [0, 1]+[r for r in critical if r.is_real and 0 <= r <= 1]
    best = max(candidates, key=lambda r: likelihood.subs(p, r))
    equal(best, R(3, 5))
    assert sp.diff(sp.log(likelihood), p, 2).subs(p, best) < 0
    k = sp.symbols("k", positive=True)
    equal(sp.diff(k*sp.log(p)+(n-k)*sp.log(1-p), p).subs(p, k/n), 0)


def ex06():
    total = sum(map(int, intervals))
    log_likelihood = len(intervals)*sp.log(lam)-total*lam
    solution = sp.solve(sp.diff(log_likelihood, lam), lam)[0]
    equal(solution, R(1, 18))
    assert sp.diff(log_likelihood, lam, 2).is_negative
    near(float(sp.exp(-30*solution)), .189, .0005)
    near(float(sp.exp(-R(3, 2))), .223, .0005)


def ex07():
    mu, mean = sp.symbols("mu mean", real=True)
    v, ss = sp.symbols("v ss", positive=True)
    # Sum (x_i-mu)^2 = centered sum of squares + n*(mean-mu)^2.
    log_likelihood = -n*sp.log(2*sp.pi*v)/2-(ss+n*(mean-mu)**2)/(2*v)
    mu_hat = sp.solve(sp.diff(log_likelihood, mu), mu)[0]
    equal(mu_hat, mean)
    assert sp.diff(log_likelihood, mu, 2).is_negative
    profile = log_likelihood.subs(mu, mu_hat)
    v_hat = sp.solve(sp.diff(profile, v), v)[0]
    equal(v_hat, ss/n)
    equal(sp.diff(profile, v)*2*v**2, ss-n*v)
    near(np.sqrt(heights.var()), np.sqrt(12), 1e-12)


def ex08():
    lower_bound = max(uniform_data)
    derivative = sp.diff(theta**(-len(uniform_data)), theta)
    assert derivative.is_negative
    equal(lower_bound, 3)
    assert R(5, 2) < lower_bound


def ex09():
    a, b = sp.symbols("a b", positive=True)
    log_likelihood = 50*sp.log(a)+30*sp.log(b)+20*sp.log(1-a-b)
    solution = sp.solve([sp.diff(log_likelihood, a), sp.diff(log_likelihood, b)], (a, b), dict=True)[0]
    probabilities = [solution[a], solution[b], 1-solution[a]-solution[b]]
    assert probabilities == [R(1, 2), R(3, 10), R(1, 5)]
    hessian = sp.hessian(log_likelihood, (a, b)).subs(solution)
    assert hessian.is_negative_definite
    near(float(-log_likelihood.subs(solution)/100), 1.030, .0005)


def ex10():
    times, count, cutoff = [20, 35, 60, 90], 10, 100
    total = sum(times)+(count-len(times))*cutoff
    equal(total, 805)
    ll = len(times)*sp.log(lam)-total*lam
    estimate = sp.solve(sp.diff(ll, lam), lam)[0]
    equal(estimate, R(4, 805))
    near(float(estimate), .00497, .000005)
    near(float(1/estimate), 201, .5)
    near([np.mean(times), total/count], [51.25, 80.5], 1e-10)


def ex11():
    # A centered quadratic form has expectation sigma^2*trace(H).
    # Verify the identity and trace without assuming normality.
    for size in range(2, 9):
        xs = sp.Matrix(sp.symbols(f"x0:{size}"))
        mu = sp.symbols("mu", real=True)
        mean = sum(xs)/size
        lhs = sum((v-mean)**2 for v in xs)
        rhs = sum((v-mu)**2 for v in xs)-size*(mean-mu)**2
        equal(lhs, rhs)
        centering = sp.eye(size)-sp.ones(size)/size
        equal((xs.T*centering*xs)[0], lhs)
        equal(sp.trace(centering), size-1)
        equal(sp.trace(centering)/(size-1), 1)
        equal(sp.trace(centering)/size, R(size-1, size))
        equal(sum([R(1, size)]*size), 1)


def ex12():
    mean, _ = maximum_moments()
    equal(mean, n*theta/(n+1))
    equal((n+1)*mean/n, theta)
    equal(2*sp.integrate(theta*u, (u, 0, 1)), theta)
    equal(R(5, 4)*max(uniform_data), R(15, 4))


def ex13():
    x = sp.symbols("x", positive=True)
    convolution = sp.integrate(lam*sp.exp(-lam*x)*lam*sp.exp(-lam*(s-x)), (x, 0, s))
    equal(convolution, lam**2*s*sp.exp(-lam*s))
    mle_mean = sp.integrate(2/s*convolution, (s, 0, sp.oo))
    equal(mle_mean, 2*lam)
    equal(sp.integrate(s/2*convolution, (s, 0, sp.oo)), 1/lam)
    # n>=2 is parameterized by n=k+1 so convergence is explicit.
    k = sp.symbols("k", integer=True, positive=True)
    gamma_density = lam**(k+1)*s**k*sp.exp(-lam*s)/sp.factorial(k)
    general = sp.integrate((k+1)/s*gamma_density, (s, 0, sp.oo))
    equal(general, (k+1)*lam/k)


def ex14():
    mean, second = maximum_moments()
    variance = sp.factor(second-mean**2)
    equal(second, n*theta**2/(n+2))
    equal(variance, n*theta**2/((n+1)**2*(n+2)))
    corrected = sp.factor(((n+1)/n)**2*variance)
    equal(corrected, theta**2/(n*(n+2)))
    single_mean = sp.integrate(theta*u, (u, 0, 1))
    single_var = sp.integrate((theta*u-single_mean)**2, (u, 0, 1))
    ratio = sp.simplify(4*single_var/n/corrected)
    equal(ratio, (n+2)/3)
    equal(ratio.subs(n, 10), 4)
    equal(ratio.subs(n, 100), 34)


def ex15():
    first = sp.Matrix([R(1, 3)]*3)
    second = sp.Matrix([R(1, 4), R(1, 4), R(1, 2)])
    equal(sum(first), 1)
    equal(sum(second), 1)
    equal(first.dot(first), R(1, 3))
    equal(second.dot(second), R(3, 8))
    assert first.dot(first) < second.dot(second)
    for size in range(2, 7):
        free = list(sp.symbols(f"c0:{size-1}", real=True))
        coefficients = free+[1-sum(free)]
        equal(sum((c-R(1, size))**2 for c in coefficients),
              sum(c*c for c in coefficients)-R(1, size))


def ex16():
    # Direct probability, not the invalid converse of the MSE criterion.
    p, epsilon = R(7, 10), R(1, 5)
    error_probability = sum(prob for x, prob in [(0, 1-p), (1, p)] if abs(x-p) >= epsilon)
    equal(error_probability, 1)
    mean, second = maximum_moments()
    variance = sp.simplify(second-mean**2)
    equal(sp.limit(variance+(mean-theta)**2, n, sp.oo), 0)
    corrected_variance = sp.factor(((n+1)/n)**2*variance)
    equal(sp.limit(corrected_variance, n, sp.oo), 0)
    near(.99**100, .366, .0005)
    near(.99**1000, 4.3e-5, .05e-5)


def ex17():
    for alpha, expected in [(.05, 1.645), (.025, 1.960), (.005, 2.576)]:
        quantile(norm, alpha, expected)
    se = 6/np.sqrt(36)
    near(symmetric(171.2, 1.96*se), [169.24, 173.16], .005)
    near(2*np.array([1.645, 1.96, 2.576])*se, [3.29, 3.92, 5.15], .005)
    minimum = int(np.ceil((1.96*6/1)**2))
    assert minimum == 139
    assert 1.96*6/np.sqrt(minimum) <= 1 < 1.96*6/np.sqrt(minimum-1)


def ex18():
    y, x = sp.symbols("y x", positive=True)
    transformed_cdf = sp.integrate(lam*sp.exp(-lam*x), (x, 0, y/(2*lam)))
    equal(transformed_cdf, 1-sp.exp(-y/2))
    quantile(chi2, .975, 3.247, 10)
    quantile(chi2, .025, 20.483, 10)
    rate_interval = np.array([3.247, 20.483])/(2*intervals.sum())
    near(rate_interval, [.0180, .1138], .00005)
    near(1/rate_interval[::-1], [8.8, 55.4], .05)


def ex19():
    mean, variance = lengths.mean(), lengths.var(ddof=1)
    near([mean, np.sum((lengths-mean)**2), variance], [12, .52, .104], 1e-12)
    near(np.sqrt(variance), .3225, .00005)
    quantile(t, .025, 2.571, 5)
    half = 2.571*np.sqrt(variance/6)
    near(half, .338, .0005)
    near(symmetric(mean, half), [11.66, 12.34], .005)
    half_known = 1.96*.3/np.sqrt(6)
    near(half_known, .240, .0005)
    near(symmetric(mean, half_known), [11.76, 12.24], .005)


def ex20():
    ss = np.sum((lengths-lengths.mean())**2)
    hi = quantile(chi2, .025, 12.833, 5)
    lo = quantile(chi2, .975, .831, 5)
    interval = ss/np.array([hi, lo])
    near(interval, [.0405, .6256], .00005)
    near(np.sqrt(interval), [.201, .791], .0005)
    # The table quantiles have only 3 decimals; carry their rounding errors.
    for printed, exact_endpoint in zip([12.833, .831], interval):
        assert ss/(printed+.0005) <= exact_endpoint <= ss/(printed-.0005)
    assert lengths.var(ddof=1) < interval.mean()
    near(interval[1]/interval[0], 15, .5)


def ex21():
    quantile(t, .025, 2.306, 8)
    half = 2.306*2.4/np.sqrt(9)
    near(half, 1.845, .0005)
    near(symmetric(71.2, half), [69.36, 73.04], .005)


def ex22():
    n1, n2 = len(group1), len(group2)
    v1, v2 = group1.var(ddof=1), group2.var(ddof=1)
    near([group1.mean(), group2.mean()], [50.05, 50.7], 1e-12)
    near(v1, .075, 1e-12)
    near(v2, .04667, .000005)
    pooled = ((n1-1)*v1+(n2-1)*v2)/(n1+n2-2)
    near(pooled, .0595, .00005)
    near(np.sqrt(pooled), .244, .0005)
    quantile(t, .025, 2.201, 11)
    half = 2.201*np.sqrt(pooled*(1/n1+1/n2))
    near(half, .299, .0005)
    interval = symmetric(group1.mean()-group2.mean(), half)
    near(interval, [-.949, -.351], .0005)
    assert interval[1] < 0


def ex23():
    ratio = group1.var(ddof=1)/group2.var(ddof=1)
    near(ratio, 1.607, .0005)
    hi = quantile(f, .025, 5.988, 5, 6)
    reverse_hi = quantile(f, .025, 6.978, 6, 5)
    near(1/reverse_hi, .1433, .00005)
    near(f.isf(.975, 5, 6), 1/reverse_hi, 1e-12)
    interval = [ratio/hi, ratio*reverse_hi]
    near(interval[0], .268, .0005)
    near(interval[1], 11.21, .005)
    assert interval[0] < 1 < interval[1]
    assert interval[0] < 2 < interval[1]


def ex24():
    before = np.array([12.4, 15.1, 9.8, 13.6, 11.2, 14.0])
    after = np.array([11.5, 14.0, 9.1, 12.9, 10.6, 13.1])
    near([before.mean(), after.mean()], [12.683, 11.867], .0005)
    near(before.std(ddof=1), 1.95, .005)
    difference = before-after
    near(difference, [.9, 1.1, .7, .7, .6, .9], 1e-12)
    near(difference.mean(), .817, .0005)
    near(difference.std(ddof=1), .183, .0005)
    independent_se = np.sqrt((before.var(ddof=1)+after.var(ddof=1))/6)
    wrong = symmetric(difference.mean(), t.isf(.025, 10)*independent_se)
    near(wrong, [-1.61, 3.24], .005)
    paired_half = 2.571*difference.std(ddof=1)/np.sqrt(6)
    near(paired_half, .193, .0005)
    paired = symmetric(difference.mean(), paired_half)
    near(paired, [.62, 1.01], .005)
    assert wrong[0] < 0 < wrong[1] and paired[0] > 0


def coverage(size, true_p, score=False):
    k = np.arange(size+1)
    phat, z = k/size, 1.96
    if score:
        # Roots of (phat-p)^2 <= z^2*p*(1-p)/n.
        a = size+z*z
        b = -(2*size*phat+z*z)
        c = size*phat**2
        discriminant = b*b-4*a*c
        lower = (-b-np.sqrt(discriminant))/(2*a)
        upper = (-b+np.sqrt(discriminant))/(2*a)
    else:
        half = z*np.sqrt(phat*(1-phat)/size)
        lower, upper = phat-half, phat+half
    covered = (lower <= true_p) & (true_p <= upper)
    return binom.pmf(k[covered], size, true_p).sum()


def ex25():
    size, successes = 400, 36
    phat = successes/size
    se = np.sqrt(phat*(1-phat)/size)
    near(phat, .09, 1e-12)
    near(se, .0143, .00005)
    near(1.96*se, .0280, .00005)
    near(symmetric(phat, 1.96*se), [.062, .118], .0005)
    assert min(successes, size-successes) >= 10
    minimum = int(np.ceil(1.96**2/(4*.03**2)))
    assert minimum == 1068
    assert 1.96/(2*np.sqrt(minimum)) <= .03 < 1.96/(2*np.sqrt(minimum-1))
    near([coverage(400, .09), coverage(30, .05)], [.939, .782], .0005)
    near([coverage(400, .09, True), coverage(30, .05, True)], [.956, .939], .0005)


def ex26():
    quantile(t, .05, 1.860, 8)
    se = 3/np.sqrt(9)
    near(48.2-1.860*se, 46.34, .005)
    near(symmetric(48.2, 1.860*se), [46.34, 50.06], .005)
    near(t.cdf(1.860, 8), .95, .00005)
    near(t.cdf(1.860, 8)-t.cdf(-1.860, 8), .90, .0001)


def ex27():
    exact_quantile = quantile(chi2, .95, 2.733, 8)
    numerator = (9-1)*3**2
    equal(numerator, 72)
    upper = numerator/exact_quantile
    near(upper, 26.35, .005)
    near(np.sqrt(upper), 5.13, .005)
    # As in example 20, the endpoint retains precision beyond the printed table.
    assert numerator/(2.733+.0005) <= upper <= numerator/(2.733-.0005)
    near(chi2.sf(numerator/upper, 8), .95, .00005)


def q13():
    sw2 = (4*R(3, 10)+4*R(5, 10))/8
    equal(sw2, R(2, 5))
    half = 2.306*np.sqrt(float(sw2)*(1/5+1/5))
    near(half, .922, .0005)
    near(.6-half, -.322, .0005)
    near(.6+half, 1.522, .0005)
    quoted(13, "[-0.32,", "1.52]")


def quoted_exercises():
    # Number only question/answer blocks, excluding the quoted theorem.
    blocks = re.findall(r"(?m)^> .*?(?=\n(?!>)|\Z)", lesson, re.S)
    blocks = [block for block in blocks if "> 答案：" in block]
    assert len(blocks) == 13, len(blocks)
    return blocks


def quoted(number, *parts):
    # 编辑二版：随堂小题挪了位置，按内容而不是按序号找引用块。
    matches = [b for b in quoted_exercises() if all(part in b for part in parts)]
    assert matches, (number, parts)


def q01():
    data = [1, 0, 2, 3, 1, 2, 1]
    equal(R(sum(data), len(data)), R(10, 7))
    quoted(1, r"\frac{10}{7}")


def q02():
    x, mean = sp.symbols("x mean", positive=True)
    moment = sp.integrate(x/theta, (x, 0, theta))
    equal(sp.solve(moment-mean, theta)[0], 2*mean)
    quoted(2, r"\hat\theta=2\bar X")


def q03():
    total = sp.symbols("total", positive=True)
    ll = total*sp.log(lam)-n*lam
    equal(sp.solve(sp.diff(ll, lam), lam)[0], total/n)
    assert sp.diff(ll, lam, 2).is_negative
    zero_likelihood = sp.exp(-n*lam)
    assert sp.diff(zero_likelihood, lam).is_negative
    equal(sp.limit(zero_likelihood, lam, 0, dir="+"), 1)
    assert sp.solve(zero_likelihood-1, lam) == []
    quoted(3, r"\hat\lambda=\bar X", "最大似然估计不存在")


def q04():
    a, b = sp.symbols("a b", positive=True)
    ll = 40*sp.log(a)+40*sp.log(b)+20*sp.log(1-a-b)
    sol = sp.solve([sp.diff(ll, a), sp.diff(ll, b)], (a, b), dict=True)[0]
    assert [sol[a], sol[b], 1-sol[a]-sol[b]] == [R(2, 5), R(2, 5), R(1, 5)]
    assert sp.hessian(ll, (a, b)).subs(sol).is_negative_definite
    quoted(4, "(0.4,0.4,0.2)")


def q05():
    total = sum([10, 25, 40])+(8-3)*50
    ll = 3*sp.log(lam)-total*lam
    equal(total, 325)
    estimate = sp.solve(sp.diff(ll, lam), lam)[0]
    equal(estimate, R(3, 325))
    assert sp.diff(ll, lam, 2).is_negative
    near(float(estimate), .0092, .00005)
    quoted(5, r"\frac3{325}")


def q06():
    mu = sp.symbols("mu", real=True)
    xs = sp.symbols("x1:3", real=True)
    estimates = [(xs[0]+xs[1])/2, (xs[0]+2*xs[1])/2]
    expectations = [sum(sp.diff(est, x)*mu for x in xs) for est in estimates]
    equal(expectations[0], mu)
    equal(expectations[1], 3*mu/2)
    assert sp.solve(expectations[1]-mu, mu) == [0]
    quoted(6, "1.5", "只在", r"\mu=0")


def q07():
    # Independent observations with common finite variance, as in method 5.
    coefficients = [[R(1, 3)]*3, [R(1, 4), R(3, 4), 0]]
    variances = []
    for cs in coefficients:
        equal(sum(cs), 1)
        variances.append(sum(c*c for c in cs))
    equal(variances[0], R(1, 3))
    equal(variances[1], R(5, 8))
    assert variances[0] < variances[1]
    quoted(7, r"\frac58", "$T_1$ 更有效")


def q08():
    # For n>=3 the reciprocal mean's MSE tends to zero.
    k = sp.symbols("k", integer=True, positive=True)
    size = k+2
    density = lam**size*s**(size-1)*sp.exp(-lam*s)/sp.factorial(size-1)
    e1 = sp.integrate(size/s*density, (s, 0, sp.oo))
    e2 = sp.integrate((size/s)**2*density, (s, 0, sp.oo))
    equal(e1-lam, lam/(size-1))
    equal(sp.limit(e2-2*lam*e1+lam**2, k, sp.oo), 0)
    quoted(8, "相合", r"\frac1{n-1}\lambda")


def q09():
    near(symmetric(50, 1.96*4/np.sqrt(16)), [48.04, 51.96], 1e-12)
    quoted(9, "48.04", "51.96")


def q10():
    quantile(t, .025, 2.365, 7)
    half = 2.365*.4/np.sqrt(8)
    near(half, .334, .0005)
    near(symmetric(5, half), [4.67, 5.33], .005)
    quoted(10, "4.67", "5.33")


def q11():
    phat = 30/200
    se = np.sqrt(phat*(1-phat)/200)
    near(se, .0252, .00005)
    near(1.96*se, .0495, .00005)
    near(symmetric(phat, 1.96*se), [.1005, .1995], .00005)
    quoted(11, "0.1005", "0.1995")


def q12():
    quantile(t, .05, 1.753, 15)
    near(50+1.753*2/np.sqrt(16), 50.88, .005)
    quoted(12, "50.88")


def boundary_normal():
    v = sp.symbols("v", positive=True)
    profile = (2*sp.pi*v)**(-n/2)  # All observations equal mu: Q=0.
    assert sp.diff(profile, v).is_negative
    assert sp.limit(profile, v, 0, dir="+") == sp.oo
    assert "观察值全相同" in lesson and "似然无界" in lesson


def boundary_exponential():
    x, epsilon = sp.symbols("x epsilon", positive=True)
    # On (0,1/lam), exp(-lam*x)>=exp(-1); a divergent lower bound suffices.
    bound = sp.integrate(lam/sp.E/x, (x, epsilon, 1/lam))
    assert sp.limit(bound, epsilon, 0, dir="+") == sp.oo
    equal(sp.integrate(0*lam*sp.exp(-lam*x), (x, 0, sp.oo)), 0)
    assert lam.is_positive  # Multiplying 1/X by n-1 at n=1 cannot be unbiased.
    assert "$n=1$ 时 $E(1/X)$ 发散" in lesson


def quadratic_interval():
    p, phat, z, size = sp.symbols("p phat z size", positive=True)
    polynomial = sp.expand(size*(phat-p)**2-z**2*p*(1-p))
    equal(polynomial, (size+z**2)*p**2-(2*size*phat+z**2)*p+size*phat**2)
    actual = polynomial.subs({size: 30, phat: R(1, 30), z: R(196, 100)})
    roots = sorted(float(root) for root in sp.solve(actual, p))
    near(roots, [.0059, .1667], .00005)
    near(roots, [.006, .167], .0005)
    for value in [0, roots[0]/2, sum(roots)/2, (roots[1]+1)/2, 1]:
        assert (float(actual.subs(p, value)) <= 0) == (roots[0] <= value <= roots[1])
    assert 1/30-1.96*np.sqrt((1/30)*(29/30)/30) < 0
    assert "0.0059" in lesson and "0.1667" in lesson


if __name__ == "__main__":
    lesson = (Path(__file__).resolve().parents[1]/"lesson.md").read_text(encoding="utf-8")
    found = [int(v) for v in re.findall(r"^\*\*例 (\d+)\*\*", lesson, re.M)]
    assert found == list(range(1, 28)), found
    for number in found:
        try:
            globals()[f"ex{number:02d}"]()
            print(f"PASS 例{number}")
        except Exception as exc:
            failures += 1
            print(f"FAIL 例{number}: {type(exc).__name__}: {exc}")
    extra = [(f"引用小题{number:02d}", globals()[f"q{number:02d}"])
             for number in range(1, 13)]
    extra += [("引用小题13", q13), ("正态Q=0边界", boundary_normal),
              ("指数n=1边界", boundary_exponential),
              ("二次不等式区间", quadratic_interval)]
    for name, check in extra:
        try:
            check()
            print(f"PASS {name}")
        except Exception as exc:
            failures += 1
            print(f"FAIL {name}: {type(exc).__name__}: {exc}")
    sys.exit(bool(failures))
