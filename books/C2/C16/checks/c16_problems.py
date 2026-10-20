import sympy as sp

x = sp.symbols("x", real=True)
pi = sp.pi

def report(name, ok):
    print(("PASS " if ok else "FAIL ") + name)

I = sp.integrate(sp.cos(2*x) * sp.cos(5*x), (x, -pi, pi))
option_truth = [sp.simplify(I) == 0, sp.simplify(I-pi) == 0, sp.simplify(I-2*pi) == 0, sp.simplify(I+pi) == 0]
report("C16-01", option_truth == [True, False, False, False])

a0 = sp.simplify(sp.integrate(x**2, (x, -pi, pi)) / pi)
option_truth = [a0 == 2*pi**2/3, a0 == pi**2/3, a0 == 4*pi**2/3, a0 == 0]
report("C16-02", option_truth == [True, False, False, False])

S_pi = sp.simplify((sp.limit(1+x, x, pi, dir="-") + sp.limit(sp.Integer(-2), x, -pi, dir="+")) / 2)
option_truth = [S_pi == 1+pi, S_pi == -2, S_pi == (pi-1)/2, S_pi == (pi+3)/2]
report("C16-03", option_truth == [False, False, True, False])

odd_limits = [sp.limit(-(2-x), x, 0, dir="-"), sp.limit(2+x, x, 0, dir="+")]
even_limits = [sp.limit(2+x, x, pi, dir="-"), sp.limit(2+2*pi-x, x, pi, dir="+")]
values = (sp.simplify(sum(odd_limits)/2), sp.simplify(sum(even_limits)/2))
option_truth = [values == option for option in [(0, 2+pi), (2, 2+pi), (0, 0), (2, 0)]]
report("C16-04", option_truth == [True, False, False, False])

j = sp.symbols("j", integer=True, positive=True)
u = 1/(pi/2+2*j*pi)
v = 1/(3*pi/2+2*j*pi)
f = sp.sin(1/x)
u_value, v_value = [sp.simplify(f.subs(x, point)) for point in (u, v)]
approach_zero = all(sp.limit(point, j, sp.oo) == 0 for point in (u, v))
interlaced = sp.simplify(u-v).is_positive and sp.simplify(v-u.subs(j, j+1)).is_positive
# 两列点交错趋零而函数值交替为 1、-1，故任意右邻域内都不单调且无右极限。
oscillates = approach_zero and interlaced and u_value == 1 and v_value == -1
left_oscillates = all(sp.simplify(f.subs(x, -point)+value) == 0 for point, value in [(u, u_value), (v, v_value)])
report("C16-05-振荡证据", oscillates and left_oscillates)
# A、B 的理由均不能越过已检出的条件失败；D 用周期归约式独立核对。
t = sp.symbols("t", real=True)
def reduce_period(value):
    # 归约到 [0, 2*pi)，先展开使整数周期位移可被 floor 消去。
    return value-2*pi*sp.floor(sp.expand(value/(2*pi)))

periodic = sp.simplify(reduce_period(t+2*pi)-reduce_period(t)) == 0
conditions_fail = oscillates and left_oscillates
option_truth = [not conditions_fail, not conditions_fail, conditions_fail, not periodic]
report("C16-05", option_truth == [False, False, True, False])

print("MANUAL C16-06")

n = sp.symbols("n", integer=True, positive=True)
k = n*pi/2
an = sp.simplify(sp.integrate(x*(2-x)*sp.cos(k*x), (x, 0, 2)))
a0 = sp.integrate(x*(2-x), (x, 0, 2))
full_an = sp.simplify((sp.integrate((-x)*(2+x)*sp.cos(k*x), (x, -2, 0)) + sp.integrate(x*(2-x)*sp.cos(k*x), (x, 0, 2)))/2)
report("C16-07-偶性折半", sp.simplify(full_an-an) == 0)
report("C16-07-a0", a0 == sp.Rational(4, 3))
target_an = sp.simplify(-8*(1+(-1)**n)/(n**2*pi**2))
m = sp.symbols("m", integer=True, positive=True)
report("C16-07-奇下标", sp.simplify(an.subs(n, 2*m-1)) == 0)
report("C16-07-偶下标", sp.simplify(an.subs(n, 2*m)+4/(m**2*pi**2)) == 0)
sum_value = sp.summation(1/m**2, (m, 1, sp.oo))
series_value_at_0 = a0/2 - sp.Rational(4,1)/pi**2 * sum_value
report("C16-07", sp.simplify(an-target_an) == 0 and sp.simplify(series_value_at_0) == 0)
