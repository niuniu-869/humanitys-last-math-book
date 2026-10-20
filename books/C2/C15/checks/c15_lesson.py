"""Recompute all 20 numbered examples, including their numerical claims.

Checks also cover the short exercises attached to the examples. Symbolic
convergence tests verify endpoints; finite sums only verify approximations.
The original lesson is never rewritten by this script.
"""
import sys

import sympy as sp


n = sp.symbols("n", integer=True, positive=True)
x, t, u = sp.symbols("x t u", real=True)
q = sp.symbols("q", positive=True)
failures = 0


def equal(a, b):
    return sp.simplify(sp.expand_trig(a-b)) == 0


def close(a, b, tolerance):
    return abs(float(sp.N(a-b, 40))) <= tolerance


def converges(term, start=1):
    term = sp.simplify(term)
    if sp.Sum(sp.simplify(abs(term)), (n, start, sp.oo)).is_convergent():
        return True
    return bool(sp.Sum(term, (n, start, sp.oo)).is_convergent())


def branch(expression):
    expression = sp.piecewise_fold(expression)
    return expression.args[0][0] if isinstance(expression, sp.Piecewise) else expression


def ratio(term):
    return sp.limit(sp.simplify(abs(term.subs(n, n+1)/term)), n, sp.oo)


def partial(term, last, first=0):
    return sp.Add(*(term.subs(n, j) for j in range(first, last+1)))


def check(k, test):
    global failures
    try:
        assert bool(test()), "computed result differs from lesson"
    except Exception as exc:
        failures += 1
        print(f"FAIL 例{k}: {type(exc).__name__}: {exc}")
    else:
        print(f"PASS 例{k}")


def example01():
    domain = sp.solve_univariate_inequality((1-x)**2 < (1+x)**2, x, relational=False)
    # The additional exercise has separate |x|<1 and |x|>1 comparisons.
    # Compare with |x|^n inside and |x|^{-n} outside the unit interval.
    positive = sp.symbols("positive", positive=True)
    original = q**n/(1+q**(2*n))
    inner = sp.limit((original/q**n).subs(q, sp.exp(-positive)), n, sp.oo)
    outer = sp.limit((original/q**(-n)).subs(q, sp.exp(positive)), n, sp.oo)
    return (domain == sp.Interval.open(0, sp.oo)
            and not converges(1/n)
            and sp.solve((1-x)+(1+x), x) == []
            and inner == outer == 1
            and not converges(sp.Rational(1, 2))
            and not converges((-1)**n/2))


def example02():
    term = (x-1)**n/(n*2**n)
    r = ratio(term)
    region = sp.solve_univariate_inequality(r < 1, x, relational=False)
    return (region == sp.Interval.open(-1, 3)
            and converges(term.subs(x, -1)) and not converges(term.subs(x, 3))
            and ratio(x**n/n**2) == abs(x)
            and converges(1/n**2) and converges((-1)**n/n**2))


def example03():
    term = x**(2*n+1)/(4**n*(2*n+1))
    return (equal(ratio(term), x**2/4)
            and not converges(term.subs(x, 2), 0)
            and not converges(term.subs(x, -2), 0))


def example04():
    derivative = branch(sp.summation(n*x**(n-1), (n, 1, sp.oo)))
    integral = branch(sp.summation(x**n/n, (n, 1, sp.oo)))
    twice = branch(sp.summation(n*(n-1)*x**(n-2), (n, 2, sp.oo)))
    return (equal(derivative, 1/(1-x)**2) and equal(integral, -sp.log(1-x))
            and equal(twice, 2/(1-x)**3)
            and converges((-1)**n/n) and not converges(1/n))


def example05():
    total = branch(sp.summation(n*x**n, (n, 1, sp.oo)))
    squared = branch(sp.summation(n**2*x**n, (n, 1, sp.oo)))
    return (equal(total, x/(1-x)**2) and equal(squared, x*(1+x)/(1-x)**3)
            and ratio(n*x**n) == abs(x)
            and not converges(n) and not converges(n*(-1)**n))


def example06():
    proposed = sp.log((1+x)/(1-x))/2
    term = x**(2*n+1)/(2*n+1)
    derivative = branch(sp.summation(sp.diff(term, x), (n, 0, sp.oo)))
    return (equal(sp.diff(proposed, x), derivative) and proposed.subs(x, 0) == 0
            and equal(ratio(term), x**2)
            and not converges(term.subs(x, 1), 0)
            and not converges(term.subs(x, -1), 0))


def example07():
    total = sp.summation(1/((2*n+1)*3**n), (n, 0, sp.oo))
    target = sp.sqrt(3)*sp.log(2+sp.sqrt(3))/2
    return close(total, target, 1e-35) and close(total, sp.Rational(11405, 10000), 5e-5)


def example08():
    term = n/sp.Rational(21, 20)**n
    total = sp.summation(term, (n, 1, sp.oo))
    first100 = sp.summation(term, (n, 1, 100))
    return total == 420 and close(first100, sp.Rational(4016, 10), 0.05)


def example09():
    term = x**n/sp.factorial(n)
    sine = (-1)**n*x**(2*n+1)/sp.factorial(2*n+1)
    cosine = (-1)**n*x**(2*n)/sp.factorial(2*n)
    return (equal(sp.summation(term, (n, 0, sp.oo)), sp.exp(x))
            and ratio(term) == 0
            and equal(sp.summation(sine, (n, 0, sp.oo)), sp.sin(x))
            and equal(sp.summation(cosine, (n, 0, sp.oo)), sp.cos(x))
            and all(close(partial(term, last).subs(x, sp.Rational(1, 10)), value, tolerance)
                    for last, value, tolerance in [(1, sp.Rational(11, 10), 1e-20),
                        (2, sp.Rational(1105, 1000), 1e-20),
                        (3, sp.Rational(1105167, 1000000), 5e-7)])
            and close(sp.exp(sp.Rational(1, 10)), sp.Rational(1105171, 1000000), 5e-7)
            and all(close(sp.exp(sp.Rational(1, 10))
                          - partial(term, last).subs(x, sp.Rational(1, 10)), value, tolerance)
                    for last, value, tolerance in [(1, sp.Rational(52, 10000), 5e-5),
                        (2, sp.Rational(17, 100000), 5e-6),
                        (3, sp.Rational(4, 1000000), 5e-7)])
            and close(sp.Rational(1, 10)-sp.Rational(1, 10)**3/6,
                      sp.Rational(99833, 1000000), 5e-7))


def example10():
    term = sp.E*(x-1)**n/sp.factorial(n)
    return (equal(sp.summation(term, (n, 0, sp.oo)), sp.exp(x))
            and ratio(term) == 0
            and all(sp.diff(sp.exp(x), x, k).subs(x, 1) == sp.E for k in range(8)))


def example11():
    term = (-1)**n*x**(2*n)/sp.factorial(n)
    antiderivative = (-1)**n*x**(2*n+1)/(sp.factorial(n)*(2*n+1))
    integral = sp.integrate(sp.exp(-t**2), (t, 0, x))
    return (equal(sp.summation(term, (n, 0, sp.oo)), sp.exp(-x**2))
            and equal(sp.diff(antiderivative, x), term)
            and equal(sp.summation(antiderivative, (n, 0, sp.oo)), integral)
            and ratio(term) == ratio(antiderivative) == 0)


def example12():
    log_term = (-1)**n*x**(n+1)/(n+1)
    arctan_term = (-1)**n*x**(2*n+1)/(2*n+1)
    return (equal(branch(sp.summation(log_term, (n, 0, sp.oo))), sp.log(1+x))
            and sp.summation(log_term.subs(x, 1), (n, 0, sp.oo)) == sp.log(2)
            and not converges(log_term.subs(x, -1), 0)
            and converges(log_term.subs(x, 1), 0)
            and equal(branch(sp.summation(arctan_term, (n, 0, sp.oo))), sp.atan(x))
            and sp.summation(arctan_term.subs(x, 1), (n, 0, sp.oo)) == sp.pi/4
            and sp.summation(arctan_term.subs(x, -1), (n, 0, sp.oo)) == -sp.pi/4
            and partial(log_term, 1).subs(x, sp.Rational(1, 10)) == sp.Rational(95, 1000)
            and close(sp.log(sp.Rational(11, 10)), sp.Rational(9531, 100000), 5e-6)
            and close(partial(log_term, 2).subs(x, sp.Rational(1, 10)),
                      sp.Rational(9533, 100000), 5e-6))


def example13():
    polynomial = sp.series(sp.sqrt(1+x), x, 0, 4).removeO()
    approximation = 2*polynomial.subs(x, sp.Rational(1, 40))
    printed_intermediates = 2*(1+sp.Rational(125, 10000)-sp.Rational(78125, 10**9)
                              +sp.Rational(98, 10**8))
    true_value = sp.sqrt(sp.Rational(41, 10))
    return (equal(polynomial, 1+x/2-x**2/8+x**3/16)
            and close(approximation, sp.Rational(2024846, 10**6), 5e-7)
            and close(true_value, sp.Rational(20248457, 10**7), 5e-8)
            and close(printed_intermediates-true_value, sp.Rational(4, 10**8), 1e-8)
            and close(sp.Rational(2025, 1000)-true_value, sp.Rational(15, 10**5), 5e-6))


def example14():
    term = (-1)**(n+1)*2**(2*n-1)*x**(2*n)/sp.factorial(2*n)
    return (equal(sp.summation(term, (n, 1, sp.oo)), sp.sin(x)**2)
            and equal(partial(term, 2, 1), x**2-x**4/3) and ratio(term) == 0)


def example15():
    term = (-1)**n*(sp.Rational(1, 2)**(n+1)-sp.Rational(1, 4)**(n+1))*u**n/2
    target = 1/((u+1)**2+4*(u+1)+3)
    # Direct Taylor coefficients are independent of the partial fractions in the lesson.
    coefficients = all(equal(sp.diff(target, u, k).subs(u, 0)/sp.factorial(k),
                             term.subs({n: k, u: 1})) for k in range(10))
    return (coefficients and equal(ratio(term), abs(u)/2)
            and not converges(term.subs(u, -2), 0)
            and not converges(term.subs(u, 2), 0)
            and target.subs(u, 0) == sp.Rational(1, 8)
            and sp.summation(n**2/sp.factorial(n), (n, 0, sp.oo)) == 2*sp.E)


def example16():
    integral = sp.integrate(sp.exp(-x**2), (x, 0, 1))
    term = (-1)**n/(sp.factorial(n)*(2*n+1))
    approximation = partial(term, 4)
    extra = partial(term, 5)
    bound = abs(term.subs(n, 5))
    return (close(approximation, sp.Rational(74749, 10**5), 5e-6)
            and bound == sp.Rational(1, 1320)
            and abs(sp.N(approximation-integral, 40)) < bound < sp.Rational(1, 1000)
            and close(integral, sp.Rational(747, 1000), 0.001)
            and close(integral, sp.Rational(74682, 10**5), 5e-6)
            and close(extra, sp.Rational(74673, 10**5), 5e-6)
            and abs(sp.N(extra-integral, 40)) < sp.Rational(1, 10000))


def example17():
    term = 2/((2*n+1)*3**(2*n+1))
    three, four = partial(term, 2), partial(term, 3)
    tail_bound = term.subs(n, 3)/(1-sp.Rational(1, 9))
    threshold = sp.solve_univariate_inequality(1/(x+1) < sp.Rational(1, 1000),
                                               x, relational=False)
    positive_counts = threshold.intersect(sp.Interval(1, sp.oo))
    minimum_count = sp.floor(positive_counts.start)+1
    quotient = sp.simplify(term.subs(n, n+1)/term)
    return (minimum_count == 1000
            and sp.simplify(sp.Rational(1, 9)-quotient).is_positive
            and close(sp.summation(term, (n, 0, sp.oo)), sp.log(2), 1e-35)
            and close(three, sp.Rational(693004, 10**6), 5e-7)
            and 0 < sp.N(sp.log(2)-three, 40) < tail_bound < sp.Rational(1, 1000)
            and close(tail_bound, sp.Rational(147, 10**6), 5e-7)
            and close(four, sp.Rational(693135, 10**6), 5e-7)
            and close(sp.log(2), sp.Rational(693147, 10**6), 5e-7))


def example18():
    return sp.expand((1+sp.sqrt(3)*sp.I)**6) == 64 and sp.expand((1-sp.I)**10) == -32*sp.I


def example19():
    theta = sp.pi/6
    def dot(m, k):
        left = sp.expand_complex(sp.exp(sp.I*m*theta))
        right = sp.expand_complex((1+sp.I)*sp.exp(sp.I*k*theta))
        return sp.simplify(sp.re(left)*sp.re(right)+sp.im(left)*sp.im(right))
    a, b = sp.symbols("a b", real=True)
    # Coordinate rotation gives cos(a-b)+sin(a-b), independently of conjugate products.
    coordinate_dot = sp.cos(a)*(sp.cos(b)-sp.sin(b))+sp.sin(a)*(sp.sin(b)+sp.cos(b))
    expected = sp.sqrt(2)*sp.cos(sp.pi/12)
    return (equal(coordinate_dot, sp.cos(a-b)+sp.sin(a-b))
            and equal(dot(3, 1), expected) and equal(dot(5, 3), expected)
            and close(expected, sp.Rational(1366, 1000), 0.0005))


def example20():
    integrated_term = sp.integrate(sp.sin(n*x)/n**2, (x, 0, sp.pi))
    expected_term = (1-(-1)**n)/n**3
    odd_sum = 2*sp.summation(1/(2*n+1)**3, (n, 0, sp.oo))
    full_sum = sp.summation(expected_term, (n, 1, sp.oo))
    differentiated_at_zero = sp.diff(sp.sin(n*x)/n**2, x).subs(x, 0)
    return (converges(1/n**2) and equal(integrated_term, expected_term)
            and equal(full_sum, odd_sum)
            and equal(full_sum.rewrite(sp.zeta), 7*sp.zeta(3)/4)
            and not converges(differentiated_at_zero)
            and sp.simplify(abs((-1)**n/n**2)) == 1/n**2)


def extra_exercises():
    """Short exercises added in the second editing pass (sin 0.1, sin x^2, even-power sum, sin x / x)."""
    import math
    s_even = branch(sp.summation(x**(2*n+1), (n, 0, sp.oo)))
    ok = equal(sp.diff(-sp.log(1-x**2)/2, x), s_even) and equal(s_even, x/(1-x**2)) and (-sp.log(1-x**2)/2).subs(x, 0) == 0
    ok = ok and equal(sp.series(sp.sin(x**2), x, 0, 11).removeO(), x**2 - x**6/6 + x**10/120)
    integral = sp.N(sp.Integral(sp.sin(x)/x, (x, 0, 1)), 20)
    three = 1 - sp.Rational(1, 18) + sp.Rational(1, 600)
    ok = ok and abs(float(integral - three)) < sp.Rational(1, 35280) and sp.Rational(1, 35280) < sp.Rational(1, 1000)
    ok = ok and abs(math.sin(0.1) - (0.1 - 0.1**3/6) - 0.1**5/120) < 1e-9
    z = sum(1j**k/math.factorial(k) for k in range(6))
    ok = ok and abs(z.real - 0.5417) < 5e-5 and abs(z.imag - 0.8417) < 5e-5
    return ok


if __name__ == "__main__":
    for k in range(1, 21):
        check(k, globals()[f"example{k:02}"])
    check("附加小题", extra_exercises)
    sys.exit(bool(failures))
