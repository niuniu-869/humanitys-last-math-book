"""Independent checks of all 12 numbered examples and four inline exercises.

The two known prose errors are reported as NOTE and recorded in the notes;
PASS concerns the example's mathematical answer, not those erroneous words.
Simulation outputs are reproduced using the existing author's seed/order.
"""
import sys

import numpy as np
import sympy as sp

R = sp.Rational
x, t = sp.symbols("x t", real=True)
y = sp.symbols("y", positive=True)
failures = []


def equal(actual, expected):
    assert sp.simplify(actual - expected) == 0, (actual, expected)


def run(label, test):
    try:
        test()
    except Exception as exc:
        failures.append(label)
        print(f"FAIL {label}: {type(exc).__name__}: {exc}")
    else:
        print(f"PASS {label}")


def pushforward(distribution, transform):
    output = {}
    for value, probability in distribution.items():
        out = transform(value)
        output[out] = output.get(out, 0) + probability
    return output


def example1():
    distribution = {}
    for first in range(1, 7):
        for second in range(1, 7):
            out = abs(first + second - 7)
            distribution[out] = distribution.get(out, 0) + R(1, 36)
    assert distribution == dict(enumerate([R(n, 36) for n in (6, 10, 8, 6, 4, 2)]))
    equal(sum(distribution.values()), 1)


def example2():
    distribution = dict(zip(range(-2, 3), [R(1, 10), R(1, 5), R(3, 10), R(1, 4), R(3, 20)]))
    assert pushforward(distribution, lambda v: v**2) == {0: R(3, 10), 1: R(9, 20), 4: R(1, 4)}
    assert pushforward(distribution, lambda v: max(0, v)) == {0: R(3, 5), 1: R(1, 4), 2: R(3, 20)}


def example3():
    upper = sp.solve(x**2 - y, x)[1]
    cdf = sp.integrate(R(1, 2), (x, 0, upper))
    equal(cdf, sp.sqrt(y) / 2)
    equal(sp.diff(cdf, y), 1 / (4 * sp.sqrt(y)))
    equal(sp.integrate(sp.diff(cdf, y), (y, 0, 4)), 1)
    equal(sp.integrate(R(1, 2), (x, 0, R(1, 10))), R(1, 20))
    ratio = R(1, 10)**2 / R(1, 10)
    assert ratio != R(1, 100)
    print(f"NOTE 例3前说明：长度比实算为 {ratio}，原文的百分之一不正确。")


def example4():
    cdf = sp.integrate(sp.exp(-x**2 / 2) / sp.sqrt(2 * sp.pi),
                       (x, -sp.sqrt(y), sp.sqrt(y)))
    equal(cdf, sp.erf(sp.sqrt(y) / sp.sqrt(2)))
    result = sp.diff(cdf, y)
    equal(result, sp.exp(-y / 2) / sp.sqrt(2 * sp.pi * y))
    equal(sp.integrate(result, (y, 0, sp.oo)), 1)


def example5():
    first = sp.integrate(R(1, 3), (x, -y, y))
    second = sp.integrate(R(1, 3), (x, -1, y))
    equal(first, 2 * y / 3)
    equal(second, (y + 1) / 3)
    equal(sp.diff(first, y), R(2, 3))
    equal(sp.diff(second, y), R(1, 3))
    equal(first.subs(y, 1), second.subs(y, 1))
    equal(second.subs(y, 2), 1)
    equal(sp.integrate(sp.diff(first, y), (y, 0, 1))
          + sp.integrate(sp.diff(second, y), (y, 1, 2)), 1)


def example6():
    atom = sp.integrate(R(1, 3), (x, -1, 0))
    cdf = atom + sp.integrate(R(1, 3), (x, 0, y))
    equal(atom, R(1, 3))
    equal(cdf, (y + 1) / 3)
    equal(sp.diff(cdf, y), R(1, 3))
    equal(cdf.subs(y, 0), atom)
    equal(cdf.subs(y, 2), 1)
    assert 0 < atom < 1  # There is both an atom and a continuous component.


def example7():
    inverse = sp.solve(1 / x - y, x)[0]
    cdf = sp.integrate(1, (x, inverse, 2))
    equal(sp.diff(cdf, y), 1 / y**2)
    equal(cdf.subs(y, R(1, 2)), 0)
    equal(cdf.subs(y, 1), 1)
    equal(sp.integrate(sp.diff(cdf, y), (y, R(1, 2), 1)), 1)
    assert sp.diff(x**2, x).subs(x, y) > 0
    print("NOTE 例7开头：例3的平方在其取值范围内严格递增，无须非单调分段处理。")


def example8():
    mu, b, value = sp.symbols("mu b value", real=True)
    sigma, magnitude = sp.symbols("sigma magnitude", positive=True)
    normal_pdf = sp.exp(-(x - mu)**2 / (2 * sigma**2)) / (sigma * sp.sqrt(2 * sp.pi))
    for coefficient in (magnitude, -magnitude):
        inverse = sp.solve(coefficient * x + b - value, x)[0]
        result = normal_pdf.subs(x, inverse) * sp.Abs(sp.diff(inverse, value))
        target = sp.exp(-(value - (coefficient * mu + b))**2 / (2 * coefficient**2 * sigma**2)) / (sp.Abs(coefficient) * sigma * sp.sqrt(2 * sp.pi))
        equal(result, target)
    standardized = normal_pdf.subs(x, mu + sigma * value) * sigma
    equal(standardized, sp.exp(-value**2 / 2) / sp.sqrt(2 * sp.pi))
    equal(R(170) + 6 * R(1, 2), 173)


def example9():
    original = sp.exp(-x**2 / 2) / sp.sqrt(2 * sp.pi)
    # Evaluating the antiderivative avoids a symbolic definite-integral
    # branch error: log(y) can be negative even when y is positive.
    primitive = sp.integrate(original, x)
    equal(sp.diff(primitive, x), original)
    cdf = primitive.subs(x, sp.log(y)) - sp.limit(primitive, x, -sp.oo)
    equal(cdf.subs(y, 1), R(1, 2))
    equal(cdf.subs(y, sp.exp(-1)) + cdf.subs(y, sp.exp(1)), 1)
    result = sp.diff(cdf, y)
    equal(result, sp.exp(-sp.log(y)**2 / 2) / (y * sp.sqrt(2 * sp.pi)))
    # Substitute y=exp(x) to check all mass without numerical tail truncation.
    pulled_back = sp.simplify(result.subs(y, sp.exp(x)) * sp.exp(x))
    equal(sp.integrate(pulled_back, (x, -sp.oo, sp.oo)), 1)


def example10():
    first = sp.integrate(R(1, 3), (x, -sp.sqrt(y), sp.sqrt(y)))
    second = sp.integrate(R(1, 3), (x, -1, sp.sqrt(y)))
    equal(sp.diff(first, y), 1 / (3 * sp.sqrt(y)))
    equal(sp.diff(second, y), 1 / (6 * sp.sqrt(y)))
    equal(first.subs(y, 1), second.subs(y, 1))
    equal(second.subs(y, 4), 1)
    equal(sp.integrate(sp.diff(first, y), (y, 0, 1)), R(2, 3))
    equal(sp.integrate(sp.diff(second, y), (y, 1, 4)), R(1, 3))


def example11():
    u = sp.symbols("u", real=True)
    v = sp.symbols("v", positive=True)
    # Here v=1-u is positive; retain this fact while simplifying the log.
    inverse = sp.expand_log(sp.solve(sp.exp(-3 * x) - v, x)[0]).subs(v, 1 - u)
    equal(inverse, -sp.log(1 - u) / 3)
    equal(inverse.subs(u, R(1, 2)), sp.log(2) / 3)
    assert round(float(inverse.subs(u, R(1, 2))), 3) == 0.231
    for input_value, minutes in [(R(1, 2), 13.9), (R(1, 10), 2.1), (R(9, 10), 46.1)]:
        assert round(60 * float(inverse.subs(u, input_value)), 1) == minutes
    mean = sp.integrate(x * 3 * sp.exp(-3 * x), (x, 0, sp.oo)) * 60
    before20 = sp.integrate(3 * sp.exp(-3 * x), (x, 0, R(1, 3)))
    after30 = sp.integrate(3 * sp.exp(-3 * x), (x, R(1, 2), sp.oo))
    equal(mean, 20)
    equal(before20, 1 - sp.exp(-1))
    equal(after30, sp.exp(-R(3, 2)))
    assert round(float(before20), 4) == 0.6321
    assert round(float(after30), 4) == 0.2231
    rng = np.random.default_rng(2026)
    draws = -np.log1p(-rng.random(100000)) * 20
    assert round(draws.mean(), 2) == 19.91
    assert round(np.mean(draws <= 20), 4) == 0.6344
    assert round(np.mean(draws > 30), 4) == 0.2212


def example12():
    probabilities = [R(665, 1000), R(245, 1000), R(90, 1000)]
    cumulative = [sum(probabilities[:i]) for i in range(4)]
    assert cumulative == [0, R(665, 1000), R(910, 1000), 1]
    for i, probability in enumerate(probabilities):
        equal(sp.integrate(1, (x, cumulative[i], cumulative[i + 1])), probability)
    numeric_cdf = np.array([float(v) for v in cumulative[1:]])
    assert np.array_equal(np.searchsorted(numeric_cdf, [.30, .72, .95], side="right"), [0, 1, 2])
    rng = np.random.default_rng(2026)
    rng.random(100000)  # Example 11 consumes the first block in the author script.
    counts = np.bincount(np.searchsorted(numeric_cdf, rng.random(100000), side="right"), minlength=3) / 100000
    assert np.array_equal(np.round(counts, 3), [.668, .242, .090])
    for i in range(6):
        equal(sp.integrate(1, (x, R(i, 6), R(i + 1, 6))), R(1, 6))
        equal(sp.floor(6 * R(2 * i + 1, 12)) + 1, i + 1)
    phi196 = (1 + sp.erf(R(196, 100) / sp.sqrt(2))) / 2
    assert abs(float(phi196) - 0.975) < 0.000003


def inline1():
    distribution = {-1: R(1, 5), 0: R(3, 10), 1: R(2, 5), 2: R(1, 10)}
    assert pushforward(distribution, lambda v: v**2) == {0: R(3, 10), 1: R(3, 5), 4: R(1, 10)}


def inline2():
    cdf = sp.integrate(sp.exp(-x), (x, 0, sp.sqrt(y)))
    equal(cdf, 1 - sp.exp(-sp.sqrt(y)))
    equal(sp.diff(cdf, y), sp.exp(-sp.sqrt(y)) / (2 * sp.sqrt(y)))
    equal(sp.integrate(sp.diff(cdf, y), (y, 0, sp.oo)), 1)


def inline3():
    inverse = sp.solve(2 * x + 3 - y, x)[0]
    cdf = sp.integrate(sp.exp(-x), (x, 0, inverse))
    equal(sp.diff(cdf, y), sp.exp(-(y - 3) / 2) / 2)
    equal(cdf.subs(y, 3), 0)
    equal(sp.limit(cdf, y, sp.oo), 1)


def inline4():
    first = sp.integrate(R(1, 3), (x, -sp.sqrt(y), sp.sqrt(y)))
    second = sp.integrate(R(1, 3), (x, -sp.sqrt(y), 1))
    equal(sp.diff(first, y), 1 / (3 * sp.sqrt(y)))
    equal(sp.diff(second, y), 1 / (6 * sp.sqrt(y)))
    equal(first.subs(y, 1), second.subs(y, 1))
    equal(second.subs(y, 4), 1)


for index, test in enumerate([example1, example2, example3, example4, example5, example6,
                              example7, example8, example9, example10, example11, example12], 1):
    run(f"例{index}", test)
for index, test in enumerate([inline1, inline2, inline3, inline4], 1):
    run(f"随堂{index}", test)
sys.exit(bool(failures))
