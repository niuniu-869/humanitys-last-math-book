"""Independent symbolic calculations; expected values transcribe answers.md.

Assertions check every subquestion. Choice assertions check all four options.
Parameter conclusions use exact ranges/derivative certificates, not sampling.
"""
from pathlib import Path
import re
import sys

import sympy as s

x, a, b, c = s.symbols("x a b c", real=True)
R = s.Rational
answers = (Path(__file__).resolve().parents[1] / "answers.md").read_text()
blocks = dict(re.findall(r"\*\*(C8-\d+)\*\*\n(.*?)(?=\n\*\*C8-|\Z)", answers, re.S))
failures = 0


def eq(actual, expected):
    assert s.simplify(actual - expected) == 0, (actual, expected)


def roots(expr):
    return s.solveset(expr, x, domain=s.S.Reals)


def positive(expr, domain):
    result = s.solve_univariate_inequality(expr > 0, x, relational=False)
    return result.intersect(domain)


def check(number, work, anchors=()):
    global failures
    pid = f"C8-{number:02d}"
    try:
        assert pid in blocks
        for anchor in anchors:
            assert anchor in blocks[pid], f"answer drift: {anchor}"
        work()
        print(f"PASS {pid}")
    except Exception as exc:
        failures += 1
        print(f"FAIL {pid} {type(exc).__name__}: {exc}")


def p01():
    f = -1/x
    d = s.diff(f, x)
    domain = s.S.Reals - s.FiniteSet(0)
    eq(d, 1/x**2)
    # (A) has an explicit ordered counterexample; (B) checks both components.
    option_a = bool(f.subs(x, -1) < f.subs(x, 1))
    option_b = positive(d, domain) == domain
    option_c = positive(-d, s.Interval.open(0, s.oo)) == s.Interval.open(0, s.oo)
    option_d = domain.contains(0)
    assert [option_a, option_b, option_c, bool(option_d)] == [False, True, False, False]


def p02():
    left, right = x*x-x, x*x+x
    assert positive(-s.diff(left, x), s.Interval.open(-1, 0)) == s.Interval.open(-1, 0)
    assert positive(s.diff(right, x), s.Interval.open(0, 2)) == s.Interval.open(0, 2)
    assert s.limit(left/x, x, 0, dir="-") != s.limit(right/x, x, 0, dir="+")
    candidates = {-1: left.subs(x, -1), 0: right.subs(x, 0), 2: right.subs(x, 2)}
    assert candidates == {-1: 2, 0: 0, 2: 6}
    assert min(candidates, key=candidates.get) == 0
    assert max(candidates, key=candidates.get) == 2


def p03():
    f = x**4+x**5
    d, dd = s.diff(f, x), s.diff(f, x, 2)
    neighborhood = s.Interval.open(-R(1, 2), 0) | s.Interval.open(0, R(1, 2))
    local_min = positive(f-f.subs(x, 0), neighborhood) == neighborhood
    no_inflection = positive(dd, neighborhood) == neighborhood
    # Option A asserts applicability of the second sufficient condition.
    option_a = d.subs(x, 0) == 0 and dd.subs(x, 0) > 0
    option_b = not local_min
    option_c = local_min and no_inflection
    option_d = not no_inflection
    assert list(map(bool, [option_a, option_b, option_c, option_d])) == [False, False, True, False]
    eq(dd, 4*x*x*(3+5*x))


def p04():
    f = s.cos(x)
    K = abs(s.diff(f, x, 2))/(1+s.diff(f, x)**2)**R(3, 2)
    eq(K.subs(x, 0), 1)
    eq(1/K.subs(x, 0), 1)
    eq(K.subs(x, s.pi/2), 0)
    assert (1/K.subs(x, s.pi/2)).is_finite is False


def p05():
    d = s.diff(x**3/3-a*x*x+x, x)
    stationary = s.solve(s.diff(d, x), x)
    assert stationary == [a]
    eq(s.diff(d, x, 2), 2)
    allowed = s.solve_univariate_inequality(d.subs(x, a) >= 0, a, relational=False)
    assert allowed == s.Interval(-1, 1)
    for endpoint in [-1, 1]:
        assert roots(d.subs(a, endpoint)) == s.FiniteSet(endpoint)
        assert positive(d.subs(a, endpoint), s.S.Reals) == s.S.Reals-s.FiniteSet(endpoint)


def p06():
    f = x**3+a*x*x+b*x+c
    solution = s.solve([s.diff(f, x).subs(x, 1), s.diff(f, x, 2).subs(x, 2), f.subs(x, 2)-4], [a,b,c])
    assert solution == {a: -6, b: 9, c: 2}
    f = f.subs(solution)
    assert roots(s.diff(f, x)) == s.FiniteSet(1, 3)
    assert s.diff(f, x, 2).subs(x, 1) < 0
    assert s.diff(f, x, 2).subs(x, 3) > 0
    assert [f.subs(x, v) for v in [1, 3, 2]] == [6, 2, 4]
    dd = s.diff(f, x, 2)
    assert positive(dd, s.S.Reals) == s.Interval.open(2, s.oo)
    assert positive(-dd, s.S.Reals) == s.Interval.open(-s.oo, 2)


def p07():
    f = s.sqrt(x*x+1)+x+1/(x-1)
    vertical = {1} if s.limit(f, x, 1, dir="+") == s.oo and s.limit(f, x, 1, dir="-") == -s.oo else set()
    lines = set()
    directional = {}
    for end in [s.oo, -s.oo]:
        slope = s.limit(f/x, x, end)
        intercept = s.limit(f-slope*x, x, end)
        assert slope.is_finite and intercept.is_finite
        lines.add((slope, intercept))
        directional[end] = (slope, intercept)
    # The radical is defined and continuous on R; the only pole is 1.
    assert s.solveset(x*x+1, x, domain=s.S.Reals) == s.EmptySet
    option_a = vertical == {1} and lines == {(2, 0), (0, 0)}
    option_b = vertical == set() and lines == {(2, 0), (0, 0)}
    option_c = vertical == {1} and directional[s.oo] == directional[-s.oo] == (2, 0)
    option_d = vertical == {1} and lines == {(2, 1), (0, 0)}
    assert [option_a, option_b, option_c, option_d] == [True, False, False, False]


def p08():
    d = x*(x-2)**2
    assert roots(d) == s.FiniteSet(0, 2)
    assert positive(-d, s.S.Reals) == s.Interval.open(-s.oo, 0)
    assert positive(d, s.S.Reals) == s.Interval.open(0, 2) | s.Interval.open(2, s.oo)
    dd = s.diff(d, x)
    assert roots(dd) == s.FiniteSet(R(2, 3), 2)
    assert positive(dd, s.S.Reals) == s.Interval.open(-s.oo, R(2, 3)) | s.Interval.open(2, s.oo)
    assert positive(-dd, s.S.Reals) == s.Interval.open(R(2, 3), 2)
    # Integration is used only by the independent checker, not the solution.
    f = s.integrate(d, x)+1
    eq(f.subs(x, 0), 1)
    assert s.diff(f, x, 2).subs(x, 0) > 0


def p10():
    f = s.log(x)+x-2
    step = s.simplify(x-f/s.diff(f, x))
    eq(step, x*(3-s.log(x))/(x+1))
    bad = s.simplify(step.subs(x, s.exp(4)))
    eq(bad, -s.exp(4)/(s.exp(4)+1))
    assert bad.is_negative
    domain = s.calculus.util.continuous_domain(f, x, s.S.Reals)
    assert domain.contains(bad) == s.false
    first = step.subs(x, 2)
    second = step.subs(x, first)
    assert f"{float(first):.6f}" == "1.537902"
    assert f"{float(second):.6f}" == "1.557099"
    assert first > 0 and second > 0


def p11():
    h = (1+x)*(x-s.log(1+x))/x**2
    threshold = s.limit(h, x, 0, dir="+")
    eq(threshold, R(1, 2))
    gap = x-a*x*x/(1+x)-s.log(1+x)
    boundary = gap.subs(a, threshold)
    eq(boundary.subs(x, 0), 0)
    eq(s.diff(boundary, x), x*x/(2*(1+x)**2))
    assert positive(s.diff(boundary, x), s.Interval.open(0, s.oo)) == s.Interval.open(0, s.oo)
    eq(gap-boundary, (threshold-a)*x*x/(1+x))
    # The exact derivative certificate proves strict positivity for x>0;
    # the limit forces a<=threshold, so this verifies the full parameter set.
    assert s.solve_univariate_inequality(threshold-a >= 0, a, relational=False) == s.Interval(-s.oo, R(1, 2))
    eq(gap.subs(x, 0), 0)


def p12():
    outside, inside = x*x-x-1, 1-x*x-x
    pieces = [(outside, s.Interval(-s.oo, -1)), (inside, s.Interval(-1, 1)), (outside, s.Interval(1, s.oo))]
    # Derive turning points from stationary points and branch boundaries.
    critical = {-s.S.One, s.S.One}
    for expr, domain in pieces:
        critical.update(roots(s.diff(expr, x)).intersect(domain))
    critical = sorted(critical)
    assert critical == [-1, -R(1, 2), 1]
    F = s.Abs(x*x-1)-x
    heights = [F.subs(x, v) for v in critical]
    assert heights == [1, R(5, 4), -1]
    ends = [-s.oo] + critical + [s.oo]
    exprs = [outside, inside, inside, outside]
    signs = [-1, 1, -1, 1]
    ranges = []
    for lo, hi, expr, sign in zip(ends, ends[1:], exprs, signs):
        domain = s.Interval.open(lo, hi)
        assert positive(sign*s.diff(expr, x), domain) == domain
        v1 = s.limit(expr, x, lo, dir="+")
        v2 = s.limit(expr, x, hi, dir="-")
        ranges.append(s.Interval.open(min(v1,v2), max(v1,v2)))

    def count(level):
        return sum(bool(interval.contains(level)) for interval in ranges) + sum(v == level for v in heights)

    # Thresholds and open-regime ranges are computed, not inferred from samples.
    assert sorted(set(heights)) == [-1, 1, R(5, 4)]
    for level, expected in [(-2,0),(-1,1),(0,2),(1,3),(R(9,8),4),(R(5,4),3),(2,2)]:
        assert count(level) == expected
        algebraic = s.EmptySet
        for expr, domain in pieces:
            algebraic |= roots(expr-level).intersect(domain)
        assert len(algebraic) == expected
    for level, expected in [(-1,s.FiniteSet(1)),(1,s.FiniteSet(-1,0,2)),(R(5,4),s.FiniteSet(-R(1,2),(1-s.sqrt(10))/2,(1+s.sqrt(10))/2))]:
        actual = s.EmptySet
        for expr, domain in pieces:
            actual |= roots(expr-level).intersect(domain)
        assert actual == expected


def p13():
    left, right = x*x, 2*x*x
    for expr, direction in [(left,"-"),(right,"+")]:
        eq(s.limit(expr, x, 0, dir=direction), 0)
        eq(s.limit(expr/x, x, 0, dir=direction), 0)
    assert [s.limit(s.diff(expr,x)/x,x,0,dir=direction) for expr,direction in [(left,"-"),(right,"+")]] == [2,4]
    assert positive(left,s.Interval.open(-s.oo,0)) == s.Interval.open(-s.oo,0)
    assert positive(right,s.Interval.open(0,s.oo)) == s.Interval.open(0,s.oo)


def p14():
    f = (s.exp(x)-1-x)/x**2
    value = s.limit(f,x,0)
    derivative = s.limit((f-value)/x,x,0)
    eq(value,R(1,2))
    eq(derivative,R(1,6))
    assert derivative != 0


def p15():
    f = s.cos(x)-x
    d = s.diff(f,x)
    assert f.subs(x,0)>0 and f.subs(x,1)<0
    sin_range = s.calculus.util.function_range(s.sin(x),x,s.Interval(0,1))
    assert sin_range.inf == 0
    eq(d,-1-s.sin(x))
    first = 1-f.subs(x,1)/d.subs(x,1)
    assert 0<first<1
    assert f"{float(first):.6f}" == "0.750364"
    residual = s.Abs(f.subs(x,first)).evalf(40)
    upper = s.ceiling(residual*10**6)/10**6
    eq(upper,R(18924,10**6))
    root = s.nsolve(f,R(3,4),prec=50)
    assert abs(first.evalf(40)-root) <= residual < upper


def p16():
    S = 2*x*s.sqrt(4-x*x)
    d = s.diff(S,x)
    eq(d,4*(2-x*x)/s.sqrt(4-x*x))
    interior = roots(d).intersect(s.Interval.open(0,2))
    assert interior == s.FiniteSet(s.sqrt(2))
    candidates = [s.S.Zero,s.sqrt(2),s.S(2)]
    assert [S.subs(x,v) for v in candidates] == [0,4,0]
    xx = s.sqrt(2)
    yy = s.sqrt(4-xx*xx)/2
    eq(yy,s.sqrt(2)/2)
    eq(xx*xx+4*yy*yy,4)
    eq(4*xx*yy,4)
    assert positive(S,s.Interval.open(0,2)) == s.Interval.open(0,2)


for number, work, anchors in [
    (1,p01,["**答案：** (B)。"]), (2,p02,["f(0)=0","f(2)=6"]),
    (3,p03,["**答案：** (C)。"]), (4,p04,["K=0","K=1"]),
    (5,p05,[r"-1\le a\le1"]), (6,p06,["a=-6","b=9","c=2"]),
    (7,p07,["**答案：** (A)。"]), (8,p08,["2/3","f(0)=1"]),
    (10,p10,["1.537902","1.557099"]), (11,p11,[r"a\le1/2"]),
    (12,p12,["| 根数 | 0 | 1 | 2 | 3 | 4 | 3 | 2 |"]),
    (13,p13,["f'(0)=0","不存在"]), (14,p14,["f(0)=1/2","f'(0)=1/6"]),
    (15,p15,["0.750364","0.018924"]), (16,p16,["最大面积为 $4$"]),
]:
    check(number, work, anchors)
    if number == 8:
        print("MANUAL C8-09 中值定理证明，人工逐步核对条件与严格不等号")

assert set(blocks) == {f"C8-{i:02d}" for i in range(1,17)}
sys.exit(bool(failures))
