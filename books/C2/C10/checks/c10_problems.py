"""Independently derive exercise results; expected values transcribe answers.md.

All calculations use exact SymPy arithmetic. Multiple-choice options are
tested individually, and the resulting choice is compared with answers.md.
General proofs alone are reported as MANUAL.
"""

from pathlib import Path
import re

import sympy as s


x, t, a = s.symbols("x t a", real=True)
R = s.Rational
ANSWERS = (Path(__file__).resolve().parents[1] / "answers.md").read_text(
    encoding="utf-8"
)
failures = 0


def eq(actual, expected):
    assert s.simplify(actual - expected) == 0, (actual, expected)


def same(actual, expected):
    assert actual == expected, (actual, expected)


def run(number, check, suffix=""):
    global failures
    label = f"C10-{number:02d}{suffix}"
    try:
        check()
    except Exception as error:
        failures += 1
        print(f"FAIL {label}: {error}")
    else:
        print(f"PASS {label}")


def choice(number, actual, expected):
    for letter, truth, target in zip("ABCD", actual, expected):
        run(number, lambda truth=truth, target=target: same(bool(truth), target),
            f"({letter})")
    match = re.search(
        rf"\*\*C10-{number:02d}\*\*\s*\*\*答案：\*\*\s*选 \(([A-D])\)",
        ANSWERS,
    )
    selected = "".join(letter for letter, truth in zip("ABCD", actual) if truth)
    run(number, lambda: same(selected, match[1] if match else None))


# 01: Each statement is evaluated from the integrated polynomial.
F = s.integrate(1 + t**2, (t, 0, x))
dF = s.diff(F, x)
choice(1, [s.simplify(F - (1 + x**2)) == 0,
           s.simplify(dF - (1 + x**2)) == 0,
           bool(F.subs(x, 0).free_symbols), dF.subs(x, 0) == 0],
       [False, True, False, False])


def p02():
    z = s.symbols("z", negative=True)
    integrand = (z**2 + 1) / z
    expected = z**2 / 2 + s.log(-z)
    primitive = s.integrate(integrand, z)
    eq(s.diff(primitive, z), integrand)
    eq(s.diff(expected, z), integrand)
    # Constants, including branch constants, disappear on a fixed interval.
    eq(s.diff(primitive - expected, z), 0)


run(2, p02)
run(3, lambda: eq(s.diff(s.Integral(s.sqrt(1 + t**2), (t, x**2, 1)), x),
                  -2*x*s.sqrt(1 + x**4)))


def p04():
    C = s.symbols("C")
    primitive = s.integrate(3*x**2 - 2, x) + C
    constant = s.solve(primitive.subs(x, 1) - 4, C)[0]
    eq(primitive.subs({C: constant, x: 2}), 9)
    integral = s.integrate(3*x**2 - 2, (x, -1, 2))
    eq(integral, 3)
    difference = primitive.subs(x, 2) - primitive.subs(x, -1)
    eq(difference, integral)
    same(C in difference.free_symbols, False)


run(4, p04)

# 05: Ordinary integrability fails at the interior pole. No principal-value
# convention or improper integral is silently substituted for this question.
integrand = 1 / x
singularities = s.singularities(integrand, x)
interior_poles = singularities.intersect(s.Interval.open(-1, 2))
unbounded = any(s.limit(s.Abs(integrand), x, pole, dir="+") == s.oo
                for pole in interior_poles)
ordinary_integrable = not unbounded
endpoint_difference = s.log(2) - s.log(1)
wrong_endpoint_difference = integrand.subs(x, 2) - integrand.subs(x, -1)
choice(5, [ordinary_integrable and endpoint_difference == s.log(2),
           ordinary_integrable and bool(endpoint_difference.free_symbols),
           unbounded,
           ordinary_integrable and wrong_endpoint_difference == R(3, 2)],
       [False, False, True, False])

# 06: A change at one point does not change the integral. Check the
# resulting function and the four statements from the actual definitions.
phi = s.integrate(t, (t, -1, x))
phi_at_zero = phi.subs(x, 0)
continuous = (s.limit(phi, x, 0, dir="-") == phi_at_zero
              == s.limit(phi, x, 0, dir="+"))
derivative_at_zero = s.limit((phi - phi_at_zero) / x, x, 0)
f_at_zero = s.Integer(2)
choice(6, [not continuous,
           derivative_at_zero == f_at_zero,
           continuous and derivative_at_zero == 0 and derivative_at_zero != f_at_zero,
           continuous and derivative_at_zero is s.nan],
       [False, False, True, False])
run(6, lambda: (eq(phi, (x**2 - 1)/2), eq(derivative_at_zero, 0),
                same(continuous, True), same(f_at_zero, 2)),
    " 单点改值")


def p07():
    f = s.Function("f")
    # SymPy differentiates the original parameter-dependent integral directly.
    H = s.Integral((x + t)*f(t), (t, 0, x**2))
    actual = s.diff(H, x).subs(x, 1).doit()
    actual = actual.subs(s.Integral(f(t), (t, 0, 1)), 3).subs(f(1), 2)
    eq(actual, 11)
    # A concrete continuous f checks that the supplied data are consistent.
    witness = 4 - 2*t
    eq(witness.subs(t, 1), 2)
    eq(s.integrate(witness, (t, 0, 1)), 3)
    eq(s.diff(s.integrate((x + t)*witness, (t, 0, x**2)), x).subs(x, 1), 11)


run(7, p07)


def p08():
    area = s.integrate(a - t, (t, 0, a)) + s.integrate(t - a, (t, a, 2))
    roots = s.solveset(area - R(5, 4), a, domain=s.Interval(0, 2))
    same(roots, s.FiniteSet(R(1, 2), R(3, 2)))
    for root in roots:
        eq(s.integrate(s.Abs(t - root), (t, 0, 2)), R(5, 4))


run(8, p08)
print("MANUAL C10-09 证明：连续性允许求导，周期性使导数为零，代入 x=0 定常数。")


def p10():
    integral = s.integrate(s.exp(t**2), (t, 0, x))
    leading = s.limit(integral / x, x, 0)
    allowed = s.solveset(leading - a, a, domain=s.S.Reals)
    same(allowed, s.FiniteSet(1))
    ratio = (integral - x) / x**3
    eq(s.limit(ratio, x, 0, dir="+"), R(1, 3))
    eq(s.limit(ratio, x, 0, dir="-"), R(1, 3))
    # For every other a, the uncancelled coefficient divided by x^2 diverges.
    eps = s.symbols("eps", positive=True)
    same(s.limit((integral - (1 + eps)*x)/x**3, x, 0), -s.oo)
    same(s.limit((integral - (1 - eps)*x)/x**3, x, 0), s.oo)


run(10, p10)


def p11():
    F = s.integrate((t - 1)**2 - a, (t, 0, x))
    eq(F, x**3/3 - x**2 + (1-a)*x)
    quotient = s.cancel(F / x)
    eq(s.discriminant(3*quotient, x), 12*a - 3)

    # Let r be the distance between the two quadratic roots. This checks the
    # entire parameter ranges by solving inequalities, not only sample values.
    r = s.symbols("r", nonnegative=True)
    a_of_r = (r**2 + 3)/12
    low, high = (3-r)/2, (3+r)/2
    eq(quotient.subs({a: a_of_r, x: low}), 0)
    eq(quotient.subs({a: a_of_r, x: high}), 0)
    lower_inside = s.solve_univariate_inequality(low > 0, r, relational=False)
    upper_inside = s.solve_univariate_inequality(high < 3, r, relational=False)
    admissible = lower_inside.intersect(upper_inside).intersect(s.Interval.open(0, s.oo))
    same(admissible, s.Interval.open(0, 3))
    same(s.calculus.util.function_range(a_of_r, r, admissible),
         s.Interval.open(R(1, 4), 1))
    no_real_pair = s.solve_univariate_inequality(12*a-3 < 0, a, relational=False)
    same(no_real_pair, s.Interval.open(-s.oo, R(1, 4)))
    outside = s.solve_univariate_inequality(low < 0, r, relational=False).intersect(
        s.solve_univariate_inequality(high > 3, r, relational=False))
    same(s.calculus.util.function_range(a_of_r, r, outside), s.Interval.open(1, s.oo))
    same(s.solveset(F.subs(a, R(1, 4)), x, domain=s.Interval(0, 3)),
         s.FiniteSet(0, R(3, 2)))
    same(s.solveset(F.subs(a, 1), x, domain=s.Interval(0, 3)), s.FiniteSet(0, 3))
    eq(F.subs(x, 0), 0)

    # Stationary points and signs are established for the entire 3-root range.
    positive_a = s.symbols("positive_a", positive=True)
    derivative = s.diff(F, x).subs(a, positive_a)
    same(set(s.solve(derivative, x)), {1-s.sqrt(positive_a), 1+s.sqrt(positive_a)})
    eq(F.subs(x, 1-s.sqrt(a)), R(1, 3)-a+2*a**R(3, 2)/3)
    eq(F.subs(x, 1+s.sqrt(a)), R(1, 3)-a-2*a**R(3, 2)/3)
    curvature = s.diff(F, x, 2).subs(a, positive_a)
    same(s.simplify(curvature.subs(x, 1-s.sqrt(positive_a))).is_negative, True)
    same(s.simplify(curvature.subs(x, 1+s.sqrt(positive_a))).is_positive, True)
    for sample_a, expected_count in [(0, 1), (R(1, 4), 2), (R(1, 2), 3), (1, 2), (2, 1)]:
        same(len(s.solveset(F.subs(a, sample_a), x, domain=s.Interval(0, 3))), expected_count)


run(11, p11)


def p12():
    c, d = s.symbols("c d", real=True)
    f = s.Function("f")
    H = s.Integral((t-x)*f(t), (t, x, 1))
    eq(s.diff(H, x, 2), f(x))
    polynomial = x**3/3 - x**2/2 + c*x + d
    recovered = s.diff(polynomial, x, 2)
    eq(recovered, 2*x-1)
    constants = s.solve([polynomial.subs(x, 1), s.diff(polynomial, x).subs(x, 1)], [c, d])
    same(constants, {c: 0, d: R(1, 6)})
    actual = s.integrate((t-x)*recovered.subs(x, t), (t, x, 1))
    eq(actual, polynomial.subs(constants))
    eq(s.integrate(s.Abs(recovered), (x, 0, 1)), R(1, 2))


run(12, p12)


def p13():
    G = s.integrate((2*t-1)**2, (t, 0, x))
    slope = (G.subs(x, 1) - G.subs(x, 0))/(1-0)
    eq(slope, R(1, 3))
    roots = s.solveset(s.diff(G, x)-slope, x, domain=s.Interval.open(0, 1))
    same(roots, s.FiniteSet((1-1/s.sqrt(3))/2, (1+1/s.sqrt(3))/2))
    same(s.calculus.util.continuous_domain(G, x, s.S.Reals), s.S.Reals)
    same(s.calculus.util.continuous_domain(s.diff(G, x), x, s.S.Reals), s.S.Reals)


run(13, p13)


def p14():
    k = s.symbols("k", real=True)
    density = k*(1+x)
    normalization = s.solve(s.integrate(density, (x, 0, 1))-1, k)[0]
    eq(normalization, R(2, 3))
    cdf = s.integrate(density.subs({k: normalization, x: t}), (t, 0, x))
    eq(cdf, R(2, 3)*(x+x**2/2))
    roots = s.solveset(cdf-R(1, 2), x, domain=s.Interval(0, 1))
    same(roots, s.FiniteSet(s.sqrt(10)/2-1))
    density_range = s.calculus.util.function_range(s.diff(cdf, x), x, s.Interval(0, 1))
    same(density_range, s.Interval(R(2, 3), R(4, 3)))


run(14, p14)


def p15():
    Q = s.integrate(t-1, (t, 0, x**2))
    eq(Q, x**4/2-x**2)
    derivative = s.diff(Q, x)
    same(s.solveset(derivative, x, domain=s.S.Reals), s.FiniteSet(-1, 0, 1))
    increasing = s.solve_univariate_inequality(derivative > 0, x, relational=False)
    decreasing = s.solve_univariate_inequality(derivative < 0, x, relational=False)
    same(increasing, s.Union(s.Interval.open(-1, 0), s.Interval.open(1, s.oo)))
    same(decreasing, s.Union(s.Interval.open(-s.oo, -1), s.Interval.open(0, 1)))
    for point, value, sign in [(-1, -R(1, 2), 1), (0, 0, -1), (1, -R(1, 2), 1)]:
        eq(Q.subs(x, point), value)
        same(s.sign(s.diff(Q, x, 2).subs(x, point)), sign)
    same(s.solve_univariate_inequality(Q <= 0, x, relational=False),
         s.Interval(-s.sqrt(2), s.sqrt(2)))


run(15, p15)

raise SystemExit(bool(failures))
