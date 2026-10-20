"""编辑稿新增数字的独立验算：第 2、4、6 节的小情形，以及回到开头的税收模型。"""
import sympy as s

x, y, z, t, p, tau, S, T = s.symbols("x y z t p tau S T", positive=True)
fails = 0
def ok(name, a, b):
    global fails
    good = s.simplify(a - b) == 0
    print(("PASS " if good else "FAIL ") + name)
    fails += not good

# 第 2 节：z=uv, u=x+y, v=x-y
ok("第2节 z=uv 的 z_x=2x", s.diff((x+y)*(x-y), x), 2*x)
# 第 4 节：f=s^2 t, z=f(x,xy)
f = S**2*T
f1, f2 = s.diff(f, S), s.diff(f, T)
sub = {S: x, T: x*y}
ok("第4节 z=x^3y", f.subs(sub), x**3*y)
ok("第4节 f1 在 (x,xy)", f1.subs(sub), 2*x**2*y)
ok("第4节 d f1/dx = f11+y f12", s.diff(f1.subs(sub), x), (s.diff(f, S, 2)+y*s.diff(f, S, T)).subs(sub))
ok("第4节 d f1/dx = 4xy", s.diff(f1.subs(sub), x), 4*x*y)
# 第 6 节：球面 z_x=-x/z
zz = s.sqrt(4-x**2-y**2)
ok("第6节 球面 z_x", s.diff(zz, x), -x/zz)
# 回到开头：p^2+p+t-12=0
pt = (-1+s.sqrt(49-4*tau))/2
ok("税收 t=0 时 p=3", pt.subs(tau, 0), 3)
ok("税收 方程成立", (pt**2+pt+tau-12), 0)
ok("税收 dp/dt=-1/7", s.diff(pt, tau).subs(tau, 0), s.Rational(-1, 7))
ok("税收 公式 -Ft/Fp", -1/(2*3+1), s.Rational(-1, 7))
ok("税收 买方 6/7", 1+s.diff(pt, tau).subs(tau, 0), s.Rational(6, 7))
raise SystemExit(1 if fails else 0)
