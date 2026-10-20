"""Recompute the twenty numbered examples without changing lesson.md.

For inequality examples, verify symbolic derivative/sign certificates and
endpoint identities; numerical sampling is not treated as a proof.
"""
import sys
import sympy as s

x, t = s.symbols("x t", real=True)
p = s.symbols("p", positive=True)
R = s.Rational
failures = 0


def eq(actual, expected):
    assert s.simplify(actual-expected) == 0, (actual, expected)


def positive(expr):
    return s.solve_univariate_inequality(expr>0, x, relational=False)


def roots(expr):
    return s.solveset(expr, x, domain=s.S.Reals)


def example(number, work, prefix="例"):
    global failures
    try:
        work()
        print(f"PASS {prefix}{number}")
    except Exception as exc:
        failures += 1
        print(f"FAIL {prefix}{number} {type(exc).__name__}: {exc}")


def e01():
    d = s.diff(x**3-3*x,x)
    assert roots(d) == s.FiniteSet(-1,1)
    assert positive(d) == s.Interval.open(-s.oo,-1) | s.Interval.open(1,s.oo)
    assert positive(-d) == s.Interval.open(-1,1)


def e02():
    for f in [s.exp(p)-1-p, p-s.log(1+p)]:
        eq(f.subs(p,0),0)
        increasing = positive(s.diff(f,p).subs(p,x))
        assert increasing.intersect(s.Interval.open(0,s.oo)) == s.Interval.open(0,s.oo)


def e03():
    f = s.sin(x)-x+x**3/6
    assert [s.diff(f,x,n).subs(x,0) for n in range(3)] == [0,0,0]
    eq(s.diff(f,x,3),1-s.cos(x))
    assert s.calculus.util.function_range(s.diff(f,x,3),x,s.S.Reals) == s.Interval(0,2)
    zeros = s.solveset(s.diff(f,x,3),x,domain=s.S.Reals)
    n = s.symbols("n", integer=True)
    # Compare the computed lattice map, not SymPy's bound-variable identity.
    assert isinstance(zeros,s.ImageSet) and zeros.base_set == s.S.Integers
    eq(zeros.lamda(n),2*n*s.pi)
    assert s.simplify(zeros.lamda(n+1)-zeros.lamda(n)) > 0


def e04():
    # x=t^3 preserves all real x, avoiding complex fractional-power branches.
    f = t**3-R(3,2)*t**2
    d = s.cancel(s.diff(f,t)/s.diff(t**3,t))
    eq(d,1-1/t)
    assert s.solveset(d,t,domain=s.S.Reals) == s.FiniteSet(1)
    dx = d.subs(t,x)
    assert positive(dx) == s.Interval.open(-s.oo,0) | s.Interval.open(1,s.oo)
    assert positive(-dx) == s.Interval.open(0,1)
    eq(f.subs(t,0),0)
    eq(f.subs(t,1),-R(1,2))
    assert s.limit(f/t**3,t,0,dir="-") == s.oo
    assert s.limit(f/t**3,t,0,dir="+") == -s.oo


def e05():
    f = x*x*s.exp(-x)
    assert roots(s.diff(f,x)) == s.FiniteSet(0,2)
    eq(s.diff(f,x,2).subs(x,0),2)
    eq(s.diff(f,x,2).subs(x,2),-2*s.exp(-2))
    eq(f.subs(x,0),0)
    eq(f.subs(x,2),4*s.exp(-2))


def e06():
    f = s.exp(x)+s.exp(-x)+2*s.cos(x)-4
    assert [s.diff(f,x,n).subs(x,0) for n in range(5)] == [0,0,0,0,4]
    eq(s.limit(f/x**4,x,0),R(1,6))


def e07():
    f = 2*x**3-9*x*x+12*x
    critical = roots(s.diff(f,x)).intersect(s.Interval.open(0,3))
    assert critical == s.FiniteSet(1,2)
    values = [f.subs(x,v) for v in [0,1,2,3]]
    assert values == [0,5,4,9]
    assert min(values)==0 and max(values)==9


def e08():
    radius = p
    height = 1000/(s.pi*radius**2)
    S = 2*s.pi*radius**2+2*s.pi*radius*height
    d = s.diff(S,radius)
    critical = s.solve(d,radius)
    assert len(critical)==1
    r = critical[0]
    eq(r**3,500/s.pi)
    eq(height.subs(radius,r),2*r)
    eq(s.expand(d*radius**2),4*s.pi*radius**3-2000)
    assert s.simplify(s.diff(d*radius**2,radius)).is_positive
    assert f"{float(r):.2f}" == "5.42"
    assert f"{float(height.subs(radius,r)):.2f}" == "10.84"
    assert f"{float(S.subs(radius,r)):.1f}" == "553.6"


def e09():
    sales = 1000-20*x
    profit = (x-15)*sales
    critical = s.solve(s.diff(profit,x),x)
    assert critical == [R(65,2)]
    eq(s.diff(profit,x,2),-40)
    assert 15<critical[0]<50
    eq(sales.subs(x,critical[0]),350)
    eq(profit.subs(x,critical[0]),6125)


def e10():
    f = x*s.exp(-x)
    eq(s.diff(f,x,2),(x-2)*s.exp(-x))
    assert positive(s.diff(f,x,2)) == s.Interval.open(2,s.oo)
    assert positive(-s.diff(f,x,2)) == s.Interval.open(-s.oo,2)
    eq(f.subs(x,2),2*s.exp(-2))


def e11():
    # Both curves are parameterized by x=t^3 with real t.
    for f, expected, changes in [(t,-2/(9*t**5),True),(t**4,4/(9*t**2),False)]:
        d = s.diff(f,t)/(3*t*t)
        dd = s.simplify(s.diff(d,t)/(3*t*t))
        eq(dd,expected)
        assert s.limit(f,t,0)==0
        domain_pos = positive(dd.subs(t,x))
        if changes:
            assert domain_pos == s.Interval.open(-s.oo,0)
            assert positive(-dd.subs(t,x)) == s.Interval.open(0,s.oo)
        else:
            assert domain_pos == s.S.Reals-s.FiniteSet(0)
        assert s.limit(dd,t,0,dir="+").is_finite is False


def e12():
    u,v=s.symbols("u v",positive=True)
    gap=(u*u+v*v)/2-u*v
    eq(gap,(u-v)**2/2)
    assert s.solve(gap,u)==[v]
    assert s.diff(s.exp(p),p,2).is_positive
    # u=sqrt(a), v=sqrt(b); equality iff a=b.
    eq(s.exp((s.log(u*u)+s.log(v*v))/2),u*v)


def e13():
    f=x*s.exp(1/x)
    assert s.limit(f,x,0,dir="+")==s.oo
    eq(s.limit(f,x,0,dir="-"),0)
    for end in [-s.oo,s.oo]:
        k=s.limit(f/x,x,end)
        eq(k,1)
        eq(s.limit(f-k*x,x,end),1)


def e14():
    f=s.log(1+s.exp(-x))
    eq(s.limit(f,x,s.oo),0)
    eq(s.limit(f+x,x,-s.oo),0)
    eq(s.diff(f,x),-1/(1+s.exp(x)))
    eq(s.diff(f,x,2),s.exp(x)/(1+s.exp(x))**2)
    assert s.diff(f,x).is_negative
    assert s.simplify(s.diff(f,x,2)).is_positive
    # The zero is a limiting value, never an attained minimum.
    assert f.is_positive


def e15():
    f=x*x/(x-1)
    eq(f,x+1+1/(x-1))
    d,dd=s.diff(f,x),s.diff(f,x,2)
    assert roots(d)==s.FiniteSet(0,2)
    eq(dd,2/(x-1)**3)
    assert positive(d)==s.Interval.open(-s.oo,0) | s.Interval.open(2,s.oo)
    assert positive(dd)==s.Interval.open(1,s.oo)
    assert positive(-dd)==s.Interval.open(-s.oo,1)
    eq(f.subs(x,0),0)
    eq(f.subs(x,2),4)
    assert s.limit(f,x,1,dir="+")==s.oo
    assert s.limit(f,x,1,dir="-")==-s.oo
    for end in [-s.oo,s.oo]:
        eq(s.limit(f-(x+1),x,end),0)
    assert s.calculus.util.continuous_domain(f,x,s.S.Reals).contains(1)==s.false


def e16():
    g=s.exp(x)/x
    d=s.diff(g,x)
    eq(d,(x-1)*s.exp(x)/x**2)
    assert positive(d)==s.Interval.open(1,s.oo)
    assert positive(-d)==s.Interval.open(-s.oo,0) | s.Interval.open(0,1)
    eq(g.subs(x,1),s.E)
    eq(s.limit(g,x,-s.oo),0)
    assert s.limit(g,x,0,dir="-")==-s.oo
    assert s.limit(g,x,0,dir="+")==s.oo
    assert s.limit(g,x,s.oo)==s.oo
    # Count open monotone branch ranges, adding the shared minimum once.
    branch_ranges=[s.Interval.open(-s.oo,0),s.Interval.open(s.E,s.oo),s.Interval.open(s.E,s.oo)]
    for k,expected in [(-1,1),(0,0),(1,0),(s.E,1),(s.E+1,2)]:
        count=sum(bool(I.contains(k)) for I in branch_ranges)+int(k==g.subs(x,1))
        assert count==expected


def e17():
    f=s.sin(x)
    interval=s.Interval(0,s.pi/2)
    assert s.calculus.util.function_range(s.diff(f,x,2),x,interval)==s.Interval(-1,0)
    chord=(f.subs(x,s.pi/2)-f.subs(x,0))/(s.pi/2)
    eq(chord,2/s.pi)
    h=f/x
    u=s.simplify(s.diff(h,x)*x*x)
    eq(u,x*s.cos(x)-s.sin(x))
    eq(u.subs(x,0),0)
    eq(s.diff(u,x),-x*s.sin(x))
    assert s.calculus.util.function_range(s.sin(x),x,s.Interval.Lopen(0,s.pi/2)) == s.Interval.Lopen(0,1)
    eq(h.subs(x,s.pi/2),2/s.pi)


def e18():
    f=x*x-2
    step=s.cancel(x-f/s.diff(f,x))
    eq(step,(x+2/x)/2)
    value=s.S(2)
    displayed=["1.5000000","1.4166667","1.4142157","1.4142136"]
    errors=["8.6e-02","2.5e-03","2.1e-06","1.6e-12"]
    for expected,err in zip(displayed,errors):
        value=step.subs(x,value)
        assert f"{float(value):.7f}"==expected
        actual_error=(value-s.sqrt(2)).evalf(40)
        assert f"{float(actual_error):.1e}"==err
    # The explicitly discussed failure must really cycle 0 -> 1 -> 0.
    g=x**3-2*x+2
    failstep=x-g/s.diff(g,x)
    eq(failstep.subs(x,0),1)
    eq(failstep.subs(x,1),0)


def e19():
    f=x*x
    K=abs(s.diff(f,x,2))/(1+s.diff(f,x)**2)**R(3,2)
    eq(K.subs(x,0),2)
    eq(1/K.subs(x,0),R(1,2))
    eq(K.subs(x,1),2/5**R(3,2))
    eq(1/K.subs(x,1),5*s.sqrt(5)/2)
    assert f"{float(K.subs(x,1)):.3f}"=="0.179"
    assert f"{float(1/K.subs(x,1)):.2f}"=="5.59"


def e20():
    f=s.log(p)
    K=s.simplify(abs(s.diff(f,p,2))/(1+s.diff(f,p)**2)**R(3,2))
    eq(K,p/(1+p*p)**R(3,2))
    critical=s.solve(s.diff(K,p),p)
    assert critical==[s.sqrt(2)/2]
    eq(s.diff(K,p),(1-2*p*p)/(1+p*p)**R(5,2))
    eq(K.subs(p,critical[0]),2*s.sqrt(3)/9)
    eq(f.subs(p,critical[0]),-s.log(2)/2)
    assert f"{float(K.subs(p,critical[0])):.3f}"=="0.385"
    eq(s.limit(K,p,0,dir="+"),0)
    eq(s.limit(K,p,s.oo),0)


def q01():
    d = s.diff(x*s.exp(-x), x)
    eq(d, (1-x)*s.exp(-x))
    assert roots(d) == s.FiniteSet(1)
    assert positive(d) == s.Interval.open(-s.oo, 1)
    assert positive(-d) == s.Interval.open(1, s.oo)


def q02():
    # Real cube-root substitution preserves order and avoids complex powers.
    f = t**3-3*t**2
    d = s.cancel(s.diff(f, t)/(3*t**2))
    eq(d, 1-2/t)
    assert s.solveset(d, t, domain=s.S.Reals) == s.FiniteSet(2)
    assert positive(d.subs(t, x)) == s.Interval.open(-s.oo, 0) | s.Interval.open(2, s.oo)
    assert positive(-d.subs(t, x)) == s.Interval.open(0, 2)
    assert s.limit(f/t**3, t, 0, dir="-") == s.oo
    assert s.limit(f/t**3, t, 0, dir="+") == -s.oo
    eq(f.subs(t, 0), 0)
    eq(f.subs(t, 2), -4)
    eq((t**3).subs(t, 2), 8)


def q03():
    f = x**3-3*x
    assert roots(s.diff(f, x)) == s.FiniteSet(-1, 1)
    assert [s.diff(f, x, 2).subs(x, v) for v in [-1, 1]] == [-6, 6]
    assert [f.subs(x, v) for v in [-1, 1]] == [2, -2]


def q04():
    f = x**3-3*x
    stationary = roots(s.diff(f, x)).intersect(s.Interval.open(-2, R(1, 2)))
    assert stationary == s.FiniteSet(-1)
    candidates = [-2, -1, R(1, 2)]
    values = [f.subs(x, v) for v in candidates]
    assert values == [-2, 2, -R(11, 8)]
    assert candidates[values.index(max(values))] == -1
    assert candidates[values.index(min(values))] == -2


def q05():
    distance_squared = x*x+(x*x-3)**2
    stationary = roots(s.diff(distance_squared, x))
    assert stationary == s.FiniteSet(0, -s.sqrt(R(5, 2)), s.sqrt(R(5, 2)))
    values = {v: s.simplify(distance_squared.subs(x, v)) for v in stationary}
    assert values[0] == 9
    assert min(values.values()) == R(11, 4)
    minima = {v for v, value in values.items() if value == min(values.values())}
    assert minima == {-s.sqrt(R(5, 2)), s.sqrt(R(5, 2))}
    for v in minima:
        eq(v*v, R(5, 2))
        eq(s.sqrt(values[v]), s.sqrt(11)/2)
    for end in [-s.oo, s.oo]:
        assert s.limit(distance_squared, x, end) == s.oo


def q06():
    f = x**3-3*x
    dd = s.diff(f, x, 2)
    assert positive(dd) == s.Interval.open(0, s.oo)
    assert positive(-dd) == s.Interval.open(-s.oo, 0)
    assert roots(dd) == s.FiniteSet(0)
    eq(f.subs(x, 0), 0)


def q07():
    f = x+1/x
    assert s.calculus.util.continuous_domain(f, x, s.S.Reals) == s.S.Reals-s.FiniteSet(0)
    assert s.limit(f, x, 0, dir="+") == s.oo
    assert s.limit(f, x, 0, dir="-") == -s.oo
    for end in [-s.oo, s.oo]:
        slope = s.limit(f/x, x, end)
        eq(slope, 1)
        eq(s.limit(f-slope*x, x, end), 0)


def q08():
    f = x+s.atan(x)
    assert s.calculus.util.continuous_domain(f, x, s.S.Reals) == s.S.Reals
    for end, intercept in [(-s.oo, -s.pi/2), (s.oo, s.pi/2)]:
        slope = s.limit(f/x, x, end)
        eq(slope, 1)
        eq(s.limit(f-slope*x, x, end), intercept)


def q09():
    f = x*x/(x+1)
    d, dd = s.diff(f, x), s.diff(f, x, 2)
    eq(d, x*(x+2)/(x+1)**2)
    eq(dd, 2/(x+1)**3)
    assert roots(d) == s.FiniteSet(-2, 0)
    assert positive(d) == s.Interval.open(-s.oo, -2) | s.Interval.open(0, s.oo)
    assert positive(-d) == s.Interval.open(-2, -1) | s.Interval.open(-1, 0)
    assert [f.subs(x, v) for v in [-2, 0]] == [-4, 0]
    assert positive(dd) == s.Interval.open(-1, s.oo)
    assert positive(-dd) == s.Interval.open(-s.oo, -1)
    assert s.limit(f, x, -1, dir="+") == s.oo
    assert s.limit(f, x, -1, dir="-") == -s.oo
    for end in [-s.oo, s.oo]:
        eq(s.limit(f-(x-1), x, end), 0)


def q10():
    f = x**3-3*x
    d = s.diff(f, x)
    assert roots(d) == s.FiniteSet(-1, 1)
    assert positive(d) == s.Interval.open(-s.oo, -1) | s.Interval.open(1, s.oo)
    assert positive(-d) == s.Interval.open(-1, 1)
    # Count open monotone branch ranges, then add shared endpoints once.
    endpoints = [-s.oo, -s.S.One, s.S.One, s.oo]
    heights = [s.limit(f, x, end) for end in endpoints]
    assert heights == [-s.oo, 2, -2, s.oo]
    ranges = [s.Interval.open(min(lo, hi), max(lo, hi))
              for lo, hi in zip(heights, heights[1:])]
    for m, expected in [(-3, 1), (-2, 2), (0, 3), (2, 2), (3, 1)]:
        count = sum(bool(I.contains(-m)) for I in ranges) + sum(h == -m for h in heights[1:-1])
        assert count == expected
    for m in [-2, 2]:
        assert len(roots(f+m)) == 2


def q11():
    f = x*x/2
    K = abs(s.diff(f, x, 2))/(1+s.diff(f, x)**2)**R(3, 2)
    eq(K.subs(x, 0), 1)
    eq(1/K.subs(x, 0), 1)


def loss_values():
    loss = s.log(1+s.exp(-x))
    for score, expected, rounded in [(-s.log(3), s.log(4), "1.386"),
                                      (0, s.log(2), "0.693"),
                                      (s.log(3), s.log(R(4, 3)), "0.288")]:
        value = s.simplify(loss.subs(x, score))
        eq(value, expected)
        assert f"{float(value):.3f}" == rounded


def curvature_parameters():
    # Mathematical targets only; the existing drawing is awaiting a separate fix.
    f = x*x
    slope, second = s.diff(f, x), s.diff(f, x, 2)
    tangent = f.subs(x, 1)+slope.subs(x, 1)*(x-1)
    eq(tangent, 2*x-1)
    eq(tangent.subs(x, R(85, 100)), R(70, 100))
    eq(tangent.subs(x, R(115, 100)), R(130, 100))
    K = abs(second)/(1+slope**2)**R(3, 2)
    radius = 1/K
    center_x = x-slope*(1+slope**2)/second
    center_y = f+(1+slope**2)/second
    eq(center_x.subs(x, 0), 0)
    eq(center_y.subs(x, 0), R(1, 2))
    eq(radius.subs(x, 0), R(1, 2))
    circle_branch = center_y.subs(x, 0)-s.sqrt(radius.subs(x, 0)**2-x*x)
    for order in [0, 1, 2]:
        eq(s.diff(circle_branch, x, order).subs(x, 0), s.diff(f, x, order).subs(x, 0))


for number, work in enumerate([e01,e02,e03,e04,e05,e06,e07,e08,e09,e10,e11,e12,e13,e14,e15,e16,e17,e18,e19,e20],1):
    example(number,work)

for number, work in enumerate([q01,q02,q03,q04,q05,q06,q07,q08,q09,q10,q11],1):
    example(number, work, "随堂")
example("三个罚分值", loss_values, "例14-")
example("理论参数（不含图文件验收）", curvature_parameters, "C8-n5-")

sys.exit(bool(failures))
