"""C.20 习题独立验算；只有完整证明保留 MANUAL。"""
import sympy as sp


def check(qid, condition):
    print(f"{'PASS' if bool(condition) else 'FAIL'} {qid}")


x, y, h, k = sp.symbols('x y h k', real=True)
r, t = sp.symbols('r t', positive=True)
n = sp.symbols('n', integer=True, positive=True)

half_plane = sp.solve_univariate_inequality(2*x-y >= 0, y)
circle_on_line = sp.solve(3-x**2-(2*x)**2, x)
check('C20-01', half_plane == (y <= 2*x)
      and set(circle_on_line) == {-sp.sqrt(15)/5, sp.sqrt(15)/5}
      and (3-x**2-y**2).subs({x: 0, y: 0}) > 0)

# 四个选项分别核对等高线、截线和无界性。
q2 = x**2-4*y**2
zero_lines = sp.solve(q2, y)
one_branches = sp.solve(q2-1, y)
options_02 = [
    set(zero_lines) == {-x/2, x/2} and sp.diff(q2.subs(x, 0), y, 2) < 0,
    sp.simplify(zero_lines[0]**2+x**2).is_constant(x),
    sp.simplify(q2.subs(x, 0)-4*y**2) == 0,
    all(sp.limit(b, x, sp.oo).is_finite for b in one_branches),
]
check('C20-02', options_02 == [True, False, False, False])

left = sp.limit(h**2/h, h, 0, dir='-')
right = sp.limit(h/h, h, 0, dir='+')
dy03 = sp.limit(k/k, k, 0)
has_dx = left == right
options_03 = [has_dx and left == 0 and dy03 == 1,
              has_dx and right == 1 and dy03 == 1,
              not has_dx and dy03 == 1, not has_dx and not dy03.is_finite]
check('C20-03', options_03 == [False, False, True, False])

q4 = sp.log(x**2+y**2+1)
check('C20-04', tuple(sp.diff(q4, v).subs({x: 1, y: 2}) for v in (x, y))
      == (sp.Rational(1, 3), sp.Rational(2, 3)))

# 斜率非零、两轴和曲线路径分别检查。
q5 = x**3*y/(x**6+y**2)
slope = sp.symbols('slope', real=True, nonzero=True)
c = sp.symbols('c', real=True)
curve = sp.cancel(q5.subs(y, c*x**3))
check('C20-05', sp.limit(q5.subs(y, slope*x), x, 0) == 0
      and q5.subs(y, 0) == 0 and q5.subs(x, 0) == 0
      and sp.simplify(curve-c/(1+c**2)) == 0
      and curve.subs(c, 1) == sp.Rational(1, 2)
      and curve.subs(c, -1) == -sp.Rational(1, 2))

# 径向区间给出闭性、有界性；连续性由题设保证。
radial_sets = [sp.Interval(1, 2), sp.Interval.Ropen(0, 1), sp.Interval(1, sp.oo)]
compact = [bool(I.boundary.is_subset(I) and I.inf.is_finite and I.sup.is_finite)
           for I in radial_sets]
disk_values = sp.calculus.util.function_range(x, x, sp.Interval.open(-1, 1))
outer_values = sp.Union(
    sp.calculus.util.function_range(x, x, sp.Interval(-sp.oo, -1)),
    sp.calculus.util.function_range(x, x, sp.Interval(1, sp.oo)))
constant_values = [sp.calculus.util.function_range(sp.S.Zero, r, I) for I in radial_sets]
check('C20-06', compact == [True, False, False]
      and not disk_values.contains(disk_values.inf)
      and not disk_values.contains(disk_values.sup)
      and outer_values.inf == -sp.oo and outer_values.sup == sp.oo
      and all(v == sp.FiniteSet(0) for v in constant_values))

q7 = x**3/(x**2+y**2)
angle = sp.symbols('angle', real=True)
polar7 = sp.trigsimp(q7.subs({x: r*sp.cos(angle), y: r*sp.sin(angle)}))
dx7 = sp.limit(q7.subs(y, 0)/x, x, 0)
dy7 = sp.limit(q7.subs(x, 0)/y, y, 0)
rem7 = sp.cancel(q7-dx7*x-dy7*y)
check('C20-07', sp.trigsimp(polar7-r*sp.cos(angle)**3) == 0
      and sp.limit(r, r, 0) == 0 and (dx7, dy7) == (1, 0)
      and sp.cancel(rem7+x*y**2/(x**2+y**2)) == 0
      and sp.limit(rem7.subs({x: t, y: t})/(sp.sqrt(2)*t), t, 0)
      == -1/(2*sp.sqrt(2)))

u = sp.symbols('u', positive=True)
q8 = sp.exp(y*sp.log(u))
dx8, dy8 = (sp.diff(q8, v) for v in (u, y))
coeff8 = [v.subs({u: 1, y: 1}) for v in (dx8, dy8)]
approx8 = 1+coeff8[0]*sp.Rational(2, 100)-coeff8[1]*sp.Rational(3, 100)
check('C20-08', coeff8 == [1, 0] and approx8 == sp.Rational(51, 50)
      and dy8.subs({u: sp.Rational(51, 50), y: 1}) > 0)

# A 使用讲义已证的充分条件；其余选项逐项计算反例。
q9b = x*y/(x**2+y**2)
counter_b = (sp.limit(q9b.subs(y, 0)/x, x, 0) == 0
             and sp.limit(q9b.subs(x, 0)/y, y, 0) == 0
             and sp.simplify(q9b.subs(y, x)) == sp.Rational(1, 2))
counter_c = (sp.limit(r, r, 0) == 0
             and sp.limit(sp.Abs(x)/x, x, 0, dir='+') == 1
             and sp.limit(sp.Abs(x)/x, x, 0, dir='-') == -1)
q9d = x**2*sp.sin(1/x)
counter_d = (sp.limit(r**2/r, r, 0) == 0
             and sp.limit(q9d/x, x, 0) == 0
             and sp.simplify(sp.diff(q9d, x).subs(x, 1/(2*n*sp.pi))) == -1)
# 若两偏导与基点值的差都不超过 a，则余项商不超过 2a。
a = sp.symbols('a', positive=True)
check('C20-09', sp.limit(2*a, a, 0) == 0 and counter_b and counter_c and counter_d)

q10 = (x**2+y**2)*sp.sin(1/sp.sqrt(x**2+y**2))
dx10 = sp.diff(q10, x)
claimed10 = 2*x*sp.sin(1/sp.sqrt(x**2+y**2))-x/sp.sqrt(x**2+y**2)*sp.cos(1/sp.sqrt(x**2+y**2))
check('C20-10', sp.simplify(dx10-claimed10) == 0
      and sp.limit(r**2/r, r, 0) == 0
      and sp.limit(q10.subs(y, 0)/x, x, 0) == 0
      and sp.limit(q10.subs(x, 0)/y, y, 0) == 0
      and sp.simplify(dx10.subs({x: 1/(2*n*sp.pi), y: 0})) == -1
      and sp.simplify(dx10.subs({x: 1/((2*n+1)*sp.pi), y: 0})) == 1)

# 展开式自动检查，完整不等式证明仍作人工核对。
q11 = x**2*y
coeff11 = [sp.diff(q11, v).subs({x: 1, y: 1}) for v in (x, y)]
rem11 = sp.expand(q11.subs({x: 1+h, y: 1+k})-1-coeff11[0]*h-coeff11[1]*k)
check('C20-11-代数', coeff11 == [2, 1] and rem11 == h**2+2*h*k+h**2*k
      and rem11.subs(h, 0) == 0 and rem11.subs(k, 0) == h**2
      and sp.limit((2*r**2+r**3)/r, r, 0) == 0)
print('MANUAL C20-11-证明')

q12 = x*y
plane12 = q12.subs({x: 1, y: 2})+sp.diff(q12, x).subs({x: 1, y: 2})*(x-1) \
    +sp.diff(q12, y).subs({x: 1, y: 2})*(y-2)
point12 = {x: sp.Rational(102, 100), y: sp.Rational(197, 100)}
rem12 = sp.expand((q12-plane12).subs({x: 1+h, y: 2+k}))
check('C20-12', sp.expand(plane12) == 2*x+y-2
      and plane12.subs(point12) == sp.Rational(201, 100)
      and (q12-plane12).subs(point12) == -sp.Rational(6, 10000)
      and rem12 == h*k
      and rem12.subs({h: r, k: t}) > 0 and rem12.subs({h: r, k: -t}) < 0)

q13 = sp.expand(x**2+(1-x)**2)
crit13 = sp.solve(sp.diff(q13, x), x)
vals13 = {z: q13.subs(x, z) for z in [0, 1, *crit13]}
check('C20-13', crit13 == [sp.Rational(1, 2)]
      and {z for z, v in vals13.items() if v == min(vals13.values())} == {sp.Rational(1, 2)}
      and vals13[sp.Rational(1, 2)] == sp.Rational(1, 2)
      and {z for z, v in vals13.items() if v == max(vals13.values())} == {0, 1}
      and max(vals13.values()) == 1)

q14 = x**2+y**2+2*x
min_points = sp.solve([x+1, y], (x, y))
max_points = sp.solve([x**2+y**2-4, x-2], (x, y))
near14 = q14.subs({x: 2-1/n, y: 0})
check('C20-14', sp.expand(q14+1) == sp.expand((x+1)**2+y**2)
      and sp.expand(8-q14) == sp.expand((4-x**2-y**2)+2*(2-x))
      and min_points == {x: -1, y: 0} and max_points == [(2, 0)]
      and q14.subs(min_points) == -1 and q14.subs({x: 2, y: 0}) == 8
      and sp.limit(near14, n, sp.oo) == 8)

# 距离的绝对值保留到双侧极限结束。
s = sp.symbols('s', real=True)
normal_length = sp.sqrt(sum(v**2 for v in (2, -1, 1)))
ratio15 = sp.Abs(2*s-sp.sin(s)+1-sp.cos(s))/(normal_length*sp.Abs(s))
check('C20-15', sp.limit(ratio15, s, 0, dir='+') == 1/sp.sqrt(6)
      and sp.limit(ratio15, s, 0, dir='-') == 1/sp.sqrt(6))
