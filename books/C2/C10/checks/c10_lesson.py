"""Recompute every numbered lesson example, plus the inline calculations."""

import sympy as s


x, t = s.symbols("x t", real=True)
R = s.Rational
failures = 0


def eq(actual, expected):
    residual = s.simplify(s.trigsimp(actual - expected))
    if residual != 0:
        # Normalize reciprocal trigonometric functions before combining terms.
        residual = s.trigsimp(s.together((actual - expected).rewrite(s.sin)))
    assert residual == 0, (actual, expected)


def same(actual, expected):
    assert actual == expected, (actual, expected)


def run(label, check):
    global failures
    try:
        check()
    except Exception as error:
        failures += 1
        print(f"FAIL {label}: {error}")
    else:
        print(f"PASS {label}")


run("例1", lambda: eq(s.diff(s.integrate(s.exp(t**2), (t, 1, x)), x), s.exp(x**2)))
run("例2", lambda: eq(s.diff(s.integrate(s.exp(-t**2), (t, 0, x**2)), x),
                      2*x*s.exp(-x**4)))
run("例3", lambda: eq(s.diff(s.integrate(s.sin(t)/t, (t, x, 2*x)), x),
                      (s.sin(2*x)-s.sin(x))/x))


def example04():
    f = s.Function("f")
    H = s.Integral((x**2-t**2)*f(t), (t, 0, x))
    eq(s.diff(H, x), 2*x*s.Integral(f(t), (t, 0, x)))


run("例4", example04)


def example05():
    z = s.symbols("z", positive=True)
    integrand = (z-1)**2/s.sqrt(z)
    expected = R(2, 5)*z**R(5, 2)-R(4, 3)*z**R(3, 2)+2*s.sqrt(z)
    eq(s.integrate(integrand, z), expected)
    eq(s.diff(expected, z), integrand)


run("例5", example05)


def example06():
    first = 1/(s.sin(x)**2*s.cos(x)**2)
    eq(first, 1/s.sin(x)**2 + 1/s.cos(x)**2)
    eq(s.diff(s.tan(x)-s.cot(x), x), first)
    eq(s.diff(s.tan(x)-x, x), s.tan(x)**2)


run("例6", example06)


def example07():
    C = s.symbols("C")
    F = s.integrate(s.exp(x)+2*x, x)+C
    constant = s.solve(F.subs(x, 0)-1, C)[0]
    eq(F.subs(C, constant), s.exp(x)+x**2)


run("例7", example07)
run("例8", lambda: eq(s.integrate(s.sqrt(x)+x**-2, (x, 1, 4)), R(65, 12)))


def example09():
    actual = s.integrate(s.tan(x)**2, (x, 0, s.pi/4))
    eq(actual, 1-s.pi/4)
    same(round(float(actual), 3), 0.215)


run("例9", example09)
run("例10", lambda: eq(s.integrate(s.Max(x, x**2), (x, 0, 2)), R(17, 6)))


def example11():
    density = 2*x
    eq(s.integrate(density, (x, 0, 1)), 1)
    eq(s.integrate(density, (x, R(3, 10), R(4, 5))), R(55, 100))
    cdf = s.integrate(2*t, (t, 0, x))
    eq(cdf, x**2)
    eq(s.diff(cdf, x), density)
    full_cdf = s.Piecewise((0, x < 0), (x**2, x <= 1), (1, True))
    same(full_cdf.subs(x, -1), 0)
    same(full_cdf.subs(x, 2), 1)
    same(s.limit(full_cdf, x, 1, dir="-"), 1)
    same(s.limit(full_cdf, x, 1, dir="+"), 1)
    same(s.limit((x**2 - 1) / (x - 1), x, 1, dir="-"), 2)
    same(s.limit((s.Integer(1) - 1) / (x - 1), x, 1, dir="+"), 0)


run("例11", example11)


def example12():
    numerator = s.integrate(s.sin(t**2), (t, 0, x))
    eq(s.limit(numerator/x**3, x, 0, dir="+"), R(1, 3))
    eq(s.limit(numerator/x**3, x, 0, dir="-"), R(1, 3))


run("例12", example12)


def example13():
    numerator = s.integrate(s.log(1+t), (t, 0, x**2))
    eq(s.limit(numerator/x**4, x, 0, dir="+"), R(1, 2))
    eq(s.limit(numerator/x**4, x, 0, dir="-"), R(1, 2))


run("例13", example13)


def example14():
    A = s.Integral(s.exp(t**2), (t, 0, x))
    B = s.Integral(s.exp(2*t**2), (t, 0, x))
    # Apply the two l'Hopital steps to the actual numerator/denominator.
    # Both integrands are >= 1 on [0,x], so A,B >= x -> infinity.
    first_ratio = s.simplify(s.diff(A**2, x)/s.diff(B, x))
    numerator, denominator = s.fraction(first_ratio)
    second_ratio = s.simplify(s.diff(numerator, x)/s.diff(denominator, x))
    eq(second_ratio, 1/x)
    eq(s.limit(second_ratio, x, s.oo), 0)
    same(s.exp(t**2).is_positive, True)
    same(s.exp(2*t**2).is_positive, True)


run("例14", example14)


def example15():
    F = s.integrate((t-1)*(t-2), (t, 0, x))
    dF = s.diff(F, x)
    same(s.solveset(dF, x, domain=s.S.Reals), s.FiniteSet(1, 2))
    same(s.solve_univariate_inequality(dF > 0, x, relational=False),
         s.Union(s.Interval.open(-s.oo, 1), s.Interval.open(2, s.oo)))
    same(s.solve_univariate_inequality(dF < 0, x, relational=False), s.Interval.open(1, 2))
    eq(F.subs(x, 1), R(5, 6))
    eq(F.subs(x, 2), R(2, 3))


run("例15", example15)
print("MANUAL 例16 证明：链式法则给出 G'=f(x)+f(-x)=0，再由 G(0)=0 得恒等式。")

run("随堂1", lambda: eq(s.diff(s.Integral(s.log(1+t**2), (t, x, 2)), x),
                        -s.log(1+x**2)))


def inline02():
    for positive in [True, False]:
        z = s.symbols("z", positive=True) if positive else s.symbols("z", negative=True)
        expected = 3*s.exp(z)+2/z+s.log(s.Abs(z))
        eq(s.diff(expected, z), 3*s.exp(z)-2/z**2+1/z)


run("随堂2", inline02)
run("随堂3", lambda: eq(s.integrate(s.sin(x), (x, 0, s.pi)), 2))


def domain_counterexample():
    same(s.limit(1/x**2, x, 0), s.oo)
    primitive = -1/x
    eq(primitive.subs(x, 1)-primitive.subs(x, -1), -2)
    same(s.singularities(1/x**2, x).intersect(s.Interval(-1, 1)), s.FiniteSet(0))


run("条件反例", domain_counterexample)

raise SystemExit(bool(failures))
