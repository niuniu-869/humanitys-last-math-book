"""Independent checks of the numbered examples in lesson.md."""
import sympy as sp

x, h, t, w, n, a, b = sp.symbols("x h t w n a b", real=True)


def check(k, condition):
    print(f"{'PASS' if bool(condition) else 'FAIL'} 例{k}")


# 例 1--5
f1 = x**2
check(1, sp.diff(f1, x).subs(x, 3) == 6)
check(2, sp.diff(sp.sqrt(x), x).subs(x, 4) == sp.Rational(1, 4))
check(3, sp.diff(1/x, x).subs(x, 2) == -sp.Rational(1, 4))
f4 = sp.Function("f")
f4_model = 3*x + 2
q4 = sp.limit((f4_model.subs(x, 1+2*h)-f4_model.subs(x, 1-h))/h, h, 0)
check(4, q4 == 9)
L = (w-3)**2
check(5, sp.diff(L, w).subs(w, 1) == -4 and (1-sp.Rational(1, 10)*(-4)) == sp.Rational(7, 5) and L.subs(w, sp.Rational(7, 5)) == sp.Rational(64, 25))

# 例 6--9
curve6 = 1/x
tangent6 = sp.Rational(1, 2) + sp.diff(curve6, x).subs(x, 2)*(x-2)
normal6 = sp.Rational(1, 2) - (1/sp.diff(curve6, x).subs(x, 2))*(x-2)
check(6, sp.expand(tangent6) == -x/sp.Integer(4)+1 and sp.expand(normal6) == 4*x-sp.Rational(15, 2))

roots7 = sp.solve(sp.Eq(t**2-2*t-3, 0), t)
lines7 = {sp.expand(t0**2 + 2*t0*(x-t0)) for t0 in roots7}
check(7, set(roots7) == {-1, 3} and lines7 == {6*x-9, -2*x-1})

sol8 = sp.solve([sp.Eq(a+b, 1), sp.Eq(a, 2)], [a, b], dict=True)[0]
check(8, sol8 == {a: 2, b: -1})

phi0 = sp.symbols("phi0", real=True)
check(9, sp.solve(sp.Eq(phi0, -phi0), phi0) == [0] and sp.limit(sp.Abs(h)*h/h, h, 0, dir="+") == 0 and sp.limit(sp.Abs(h)*h/h, h, 0, dir="-") == 0)

# 例 10--14
check(10, sp.simplify(sp.diff(sp.cos(x), x) + sp.sin(x)) == 0)
check(11, sp.simplify(sp.limit((3**x-2**x)/x, x, 0)-sp.log(sp.Rational(3, 2))) == 0)
y12 = x**2*sp.exp(x)
check(12, sp.simplify(sp.diff(y12, x)-(x**2+2*x)*sp.exp(x)) == 0 and sp.diff(y12, x).subs(x, 0) == 0)
check(13, sp.simplify(sp.diff(sp.tan(x), x)-1/sp.cos(x)**2) == 0 and sp.simplify(sp.diff(1/sp.cos(x), x)-sp.tan(x)/sp.cos(x)) == 0)
y14 = (x**2-1)/(x**2+1)
check(14, sp.simplify(sp.diff(y14, x)-4*x/(x**2+1)**2) == 0)

# 例 15--18
check(15, sp.simplify(sp.diff(sp.sin(3*x), x)-3*sp.cos(3*x)) == 0 and sp.simplify(sp.diff(sp.cos(x**2), x)+2*x*sp.sin(x**2)) == 0)
check(16, sp.simplify(sp.diff(sp.log(sp.cos(2*x)), x)+2*sp.tan(2*x)) == 0)
alpha = sp.symbols("alpha", real=True)
check(17, sp.simplify(sp.diff(sp.log(x), x)-1/x) == 0 and sp.simplify(sp.diff(x**alpha, x)-alpha*x**(alpha-1)) == 0)
sig = lambda z: 1/(1+sp.exp(-z))
z18 = sp.Rational(1, 2)
L18 = (sig(z18)-1)**2
d18 = sp.diff((sig(w)-1)**2, w).subs(w, z18)
check(18, abs(float(d18) + 0.1774) < 0.001)

# 例 19--21
check(19, sp.simplify(sp.diff(sp.log(x), x)-1/x) == 0 and sp.simplify(sp.diff(sp.asin(x), x)-1/sp.sqrt(1-x**2)) == 0 and sp.simplify(sp.diff(sp.atan(x), x)-1/(1+x**2)) == 0)
y20a = sp.asin(2*x)
y20b = x*sp.atan(x)-sp.Rational(1, 2)*sp.log(1+x**2)
check(20, sp.simplify(sp.diff(y20a, x)-2/sp.sqrt(1-4*x**2)) == 0 and sp.simplify(sp.diff(y20b, x)-sp.atan(x)) == 0)
f21 = x**3+x
check(21, f21.subs(x, 1) == 2 and 1/sp.diff(f21, x).subs(x, 1) == sp.Rational(1, 4))

# 例 22--24
y22 = x**2*sp.exp(x)
expected22 = (x**2+40*x+380)*sp.exp(x)
check(22, sp.simplify(sp.diff(y22, x, 20)-expected22) == 0)

expr23 = sp.Rational(1, 2)*(1/(x-1)-1/(x+1))
candidate23 = (-1)**n*sp.factorial(n)/2*(1/(x-1)**(n+1)-1/(x+1)**(n+1))
check("23 函数值", sp.simplify(expr23.subs(x, sp.Rational(3, 2)) - sp.Rational(4, 5)) == 0)
check("23 三阶导数", sp.simplify(sp.diff(expr23, x, 3)-candidate23.subs(n, 3)) == 0)

right24 = sp.limit(2*sp.Abs(h)/h, h, 0, dir="+")
left24 = sp.limit(2*sp.Abs(h)/h, h, 0, dir="-")
check(24, right24 == 2 and left24 == -2)
