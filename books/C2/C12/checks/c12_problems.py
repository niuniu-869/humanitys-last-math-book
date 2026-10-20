"""Recompute results with SymPy; expected values are transcribed from answers.md.

Convergence uses exact endpoint limits, comparison bounds, and symbolic
parameter sets. Finite numerical samples never decide convergence.
"""

from pathlib import Path
import re
import sys

import sympy as s


x, t, r, eps = s.symbols("x t r eps", positive=True)
a, b, p, c = s.symbols("a b p c", real=True)
ANS = (Path(__file__).resolve().parents[1] / "answers.md").read_text(encoding="utf-8")
BLOCKS = dict(re.findall(r"\*\*(C12-\d+)\*\*\n(.*?)(?=\n\*\*C12-|\Z)", ANS, re.S))
failures = 0


def equal(actual, expected):
    if isinstance(actual, s.Set) or isinstance(expected, s.Set):
        return actual == expected
    if actual == expected:
        return True
    return s.simplify(actual - expected) == 0


def need(actual, expected):
    assert equal(actual, expected), f"computed {actual}, expected {expected}"


def finite(value):
    return value.is_finite is True


def power_condition(exponent, variable, at_zero=False):
    condition = exponent > -1 if at_zero else exponent < -1
    return s.solve_univariate_inequality(condition, variable, relational=False)


def text_has(pid, *tokens):
    for token in tokens:
        assert token in BLOCKS[pid], f"answer text missing {token!r}"


def options(pid, computed, expected, letter):
    text_has(pid, f"**答案：** ({letter})")
    for label, actual, target in zip("ABCD", computed, expected):
        ok = bool(actual) == target
        print(f"{'PASS' if ok else 'FAIL'} {pid} ({label}) computed={bool(actual)}")
        assert ok, f"option {label}"
    assert sum(bool(v) for v in computed) == 1


def run(pid, fn):
    global failures
    try:
        fn()
        print(f"PASS {pid}")
    except Exception as exc:
        failures += 1
        print(f"FAIL {pid} {type(exc).__name__}: {exc}")


def check01():
    cutoff = s.integrate(1 / (x + 1) ** 2, (x, 2, r))
    need(cutoff, s.Rational(1, 3) - 1 / (r + 1))
    need(s.limit(cutoff, r, s.oo), s.Rational(1, 3))
    text_has("C12-01", r"\frac13", r"\frac13-\frac1{b+1}")


def check02():
    exponent = s.simplify(x * s.diff(x ** (-p), x) / x ** (-p))
    near = power_condition(exponent, p, at_zero=True)
    far = power_condition(exponent, p)
    both = near.intersect(far)
    both_diverge = s.S.Reals - near.union(far)
    p1_near = s.limit(s.integrate(1 / x, (x, eps, 1)), eps, 0, dir="+")
    p1_far = s.limit(s.integrate(1 / x, (x, 1, r)), r, s.oo)
    computed = [
        s.Interval.open(-s.oo, 1).is_subset(both),
        s.Interval.open(1, s.oo).is_subset(both_diverge),
        finite(p1_near) and finite(p1_far),
        both == s.S.EmptySet,
    ]
    options("C12-02", computed, [False, False, False, True], "D")


def check03():
    # Integrate on each side with real primitives, avoiding log branches.
    left_primitive = s.log(1 - x)
    right_primitive = s.log(x - 1)
    need(s.diff(left_primitive, x), 1 / (x - 1))
    need(s.diff(right_primitive, x), 1 / (x - 1))
    left = s.limit(left_primitive.subs(x, 1 - eps) - left_primitive.subs(x, 0), eps, 0)
    right = s.limit(right_primitive.subs(x, 3) - right_primitive.subs(x, 1 + eps), eps, 0)
    bounded_after_redefinition = finite(s.limit(1 / (x - 1), x, 1, dir="+"))
    need(left, -s.oo)
    need(right, s.oo)
    computed = [
        finite(left) and finite(right) and equal(left + right, s.log(2)),
        left != -s.oo and right == s.oo,
        left == -s.oo and right == s.oo,
        bounded_after_redefinition,
    ]
    options("C12-03", computed, [False, False, True, False], "C")


def check04():
    actual = s.integrate(x ** s.Rational(7, 2) * s.exp(-x), (x, 0, s.oo))
    need(actual, 105 * s.sqrt(s.pi) / 16)
    text_has("C12-04", r"\frac{105}{16}\sqrt\pi")


def check05():
    f, g = 1 / (x * s.log(x)), 1 / s.sqrt(x)
    ratio = s.limit(f / g, x, s.oo)
    tail = s.limit(s.integrate(f, (x, s.E, r)), r, s.oo)
    g_tail = s.limit(s.integrate(g, (x, s.E, r)), r, s.oo)
    computed = [
        ratio == 0 and finite(tail),
        ratio == 1 and not finite(tail),
        ratio == 0 and not finite(tail),
        ratio == s.oo and not finite(tail),
    ]
    options("C12-05", computed, [False, False, True, False], "C")
    need(g_tail, s.oo)
    # Same comparison ratio, opposite convergence: checks the logical caveat.
    need(s.limit((1 / x**2) / g, x, s.oo), ratio)
    assert finite(s.integrate(1 / x**2, (x, s.E, s.oo)))


def check06():
    terms = [1 / s.sqrt(x), 1 / s.sqrt(x + 1)]
    cutoffs = [s.integrate(term, (x, 1, r)) for term in terms]
    need(s.limit(cutoffs[0] - cutoffs[1], r, s.oo), 2 * (s.sqrt(2) - 1))
    for cutoff in cutoffs:
        need(s.limit(cutoff, r, s.oo), s.oo)
    text_has("C12-06", r"2(\sqrt2-1)", "不能拆成两个反常积分相减")


def check07():
    f = (1 - s.cos(x)) / x**2
    need(s.limit(f, x, 0, dir="+"), s.Rational(1, 2))
    # Obtain the global numerator range symbolically before comparing.
    trig_range = s.calculus.util.function_range(1 - s.cos(x), x, s.S.Reals)
    need(trig_range, s.Interval(0, 2))
    tail_bound = s.integrate(trig_range.sup / x**2, (x, 1, s.oo))
    assert finite(tail_bound)
    # The exact value is not asked, but independently checks the conclusion.
    actual = s.integrate(f, (x, 0, s.oo))
    assert finite(actual)
    text_has("C12-07", "**答案：** 收敛", r"\frac12")


def check08():
    moments = [s.integrate(x**k * s.exp(-x**2), (x, 0, s.oo)) for k in (0, 2)]
    assert all(finite(v) and v.is_positive for v in moments)
    solution = s.solveset(moments[1] - c * moments[0], c, domain=s.S.Reals)
    need(solution, s.FiniteSet(s.Rational(1, 2)))
    need(moments[0], s.sqrt(s.pi) / 2)
    need(moments[1], s.sqrt(s.pi) / 4)
    # Triangle inequality bound in the answer, checked for all real c and x>=0.
    u = s.symbols("u", nonnegative=True)
    for signed_c in (u, -u):
        for abs_branch in (x**2 - signed_c, signed_c - x**2):
            assert s.simplify(x**2 + u - abs_branch).is_nonnegative
    text_has("C12-08", r"c=\frac12", r"\frac{\sqrt\pi}4", r"\frac{\sqrt\pi}2")


def check10():
    # On the right of 1, remove Abs before taking the tail slope.
    f_right = 1 / (s.sqrt(x) * (x - 1) ** a * (1 + x))
    f_left = 1 / (s.sqrt(x) * (1 - x) ** a * (1 + x))
    zero_power = s.limit(s.simplify(x * s.diff(f_left, x) / f_left), x, 0)
    tail_power = s.limit(s.simplify(x * s.diff(f_right, x) / f_right), x, s.oo)
    # At the interior point, the non-power factor tends to 1/2 on both sides.
    interior_power = s.limit(s.simplify((x - 1) * s.diff(f_right, x) / f_right), x, 1, dir="+")
    need(s.limit(1 / (s.sqrt(x) * (1 + x)), x, 1), s.Rational(1, 2))
    need(s.limit(1 / ((1 - x) ** a * (1 + x)), x, 0), 1)
    # On x>1, f/x^(-a-3/2)=(1-1/x)^(-a)/(1+1/x).
    # This positive finite ratio also justifies the borderline power cases.
    need(s.limit((1 - 1 / x) ** (-a) / (1 + 1 / x), x, s.oo), 1)
    need(zero_power, -s.Rational(1, 2))
    assert zero_power > -1
    allowed = power_condition(interior_power, a, at_zero=True).intersect(power_condition(tail_power, a))
    need(allowed, s.Interval.open(-s.Rational(1, 2), 1))
    need(interior_power.subs(a, 1), -1)
    need(tail_power.subs(a, -s.Rational(1, 2)), -1)
    text_has("C12-10", r"-\frac12<a<1")


def check11():
    f = s.log(1 + x) / x**a
    need(s.limit(s.log(1 + x) / x, x, 0), 1)
    zero_power = s.limit(s.simplify(x * s.diff(f, x) / f), x, 0)
    zero_set = power_condition(zero_power, a, at_zero=True)
    delta = s.symbols("delta", positive=True)
    need(s.limit(s.log(1 + x) / x**delta, x, s.oo), 0)
    # For a>1 choose delta=(a-1)/2, yielding an integrable majorant.
    tail_set = power_condition(-a + (a - 1) / 2, a)
    need(zero_set.intersect(tail_set), s.Interval.open(1, 2))
    # For a<=1, x*f=log(1+x)*x**(1-a)>=1 at x>=e.
    q = s.symbols("q", nonnegative=True)
    lower_factor = (x * f).subs(a, 1 - q)
    need(lower_factor, x**q * s.log(1 + x))
    assert s.log(1 + s.E) > 1
    need(s.limit((x * f).subs(a, 2), x, 0), 1)
    need(s.integrate(f.subs(a, s.Rational(3, 2)), (x, 0, s.oo)), 2 * s.pi)
    boundary = s.log(1 + x) / s.sqrt(x)
    need(s.limit(boundary, x, 0), 0)
    need(s.limit(boundary, x, s.oo), 0)
    text_has("C12-11", r"1<a<2", r"I(\frac32)=2\pi")


def check12():
    original = x ** (a - 1) / (1 + s.log(1 / x)) ** b
    transformed = s.simplify(original.subs(x, s.exp(-t)) * s.exp(-t))
    need(transformed, s.exp(-a * t) * (1 + t) ** (-b))
    need(s.limit(transformed, t, 0), 1)
    rate = s.limit(s.diff(s.log(transformed), t), t, s.oo)
    need(rate, -a)
    # The exponential-versus-power comparison follows from the log rate:
    # log(t^2*f)/t -> -a. Negative implies a 1/t^2 upper bound;
    # positive implies f eventually >=1. This covers every real b.
    logarithm = -a * t - b * s.log(1 + t)
    need(s.limit((logarithm + 2 * s.log(t)) / t, t, s.oo), -a)
    decay_set = s.solve_univariate_inequality(rate < 0, a, relational=False)
    growth_set = s.solve_univariate_inequality(rate > 0, a, relational=False)
    need(decay_set, s.Interval.open(0, s.oo))
    need(growth_set, s.Interval.open(-s.oo, 0))
    tail_power = s.limit(s.simplify(t * s.diff(transformed.subs(a, 0), t) / transformed.subs(a, 0)), t, s.oo)
    need(power_condition(tail_power, b), s.Interval.open(1, s.oo))
    need(s.limit(s.integrate(1 / (1 + t), (t, 0, r)), r, s.oo), s.oo)
    # Direct integration of the original x expressions checks both values.
    need(s.integrate(original.subs({a: 0, b: 2}), (x, 0, 1)), 1)
    need(s.integrate(original.subs({a: 1, b: -2}), (x, 0, 1)), 5)
    text_has("C12-12", "$a>0$", "$a=0$ 且 $b>1$", "$K(0,2)=1$", "$K(1,-2)=5$")


def check13():
    f = (x - 1) * s.exp(-x)
    signed = s.integrate(f, (x, 0, s.oo))
    unsigned = s.integrate(-f, (x, 0, 1)) + s.integrate(f, (x, 1, s.oo))
    need(signed, 0)
    need(unsigned, 2 / s.E)
    assert unsigned != abs(signed)
    text_has("C12-13", "$0$", r"\frac2{\mathrm e}")


def check14():
    cutoff = s.integrate(s.log(x) / x**2, (x, t, r))
    tail = s.limit(cutoff, r, s.oo)
    need(tail, (s.log(t) + 1) / t)
    need(s.diff(tail, t), -s.log(t) / t**2)
    need(s.limit(t * tail / s.log(t), t, s.oo), 1)
    text_has("C12-14", r"F(t)=\dfrac{\ln t+1}{t}", r"F'(t)=-\dfrac{\ln t}{t^2}", "极限为 $1$")


def check15():
    f = (a * x**3 + x + 1) / (1 + x**2) ** 2
    coefficient = s.limit(x * f, x, s.oo)
    allowed = s.solveset(coefficient, a, domain=s.S.Reals)
    need(allowed, s.FiniteSet(0))
    # Nonzero coefficient gives a fixed-sign 1/x tail. After cancellation,
    # check both half-lines separately, including absolute integrability.
    f0 = f.subs(a, 0)
    need(s.limit(x**3 * f0, x, s.oo), 1)
    z = s.symbols("z", real=True)
    f0z = f0.subs(x, z)
    halves = [s.integrate(f0z, (z, -s.oo, 0)), s.integrate(f0z, (z, 0, s.oo))]
    assert all(finite(v) for v in halves)
    need(sum(halves), s.pi / 2)
    absolute_halves = -s.integrate(f0z, (z, -s.oo, -1)) + s.integrate(f0z, (z, -1, s.oo))
    assert finite(absolute_halves)
    # Pair f(x) with f(-x) on [0,R] to compute symmetric cutoffs.
    even_pair = s.simplify(f + f.subs(x, -x))
    symmetric = s.integrate(even_pair, (x, 0, r))
    need(s.limit(symmetric, r, s.oo), s.pi / 2)
    assert not symmetric.has(a)
    text_has("C12-15", "仅当 $a=0$", r"\frac\pi2", "所有实数 $a$")


if __name__ == "__main__":
    checks = {
        1: check01, 2: check02, 3: check03, 4: check04,
        5: check05, 6: check06, 7: check07, 8: check08,
        10: check10, 11: check11, 12: check12,
        13: check13, 14: check14, 15: check15,
    }
    assert set(BLOCKS) == {f"C12-{i:02d}" for i in range(1, 16)}
    for number in range(1, 16):
        pid = f"C12-{number:02d}"
        if number == 9:
            print(f"MANUAL {pid} 证明：逐项检查比较判别、有限区间等式及取极限")
        else:
            run(pid, checks[number])
    sys.exit(bool(failures))
