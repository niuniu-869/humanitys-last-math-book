"""P.6 题目独立验算。"""
from fractions import Fraction
import sympy as sp

def report(pid, condition):
    print(("PASS " if condition else "FAIL ") + pid)
    return condition

ok = True
x, y, z = sp.symbols("x y z", real=True)

table = {(0, 1): Fraction(18, 100), (0, 2): Fraction(12, 100), (0, 3): Fraction(10, 100),
         (1, 1): Fraction(8, 100), (1, 2): Fraction(22, 100), (1, 3): Fraction(30, 100)}
px0 = sum(v for (a, _), v in table.items() if a == 0)
py3 = sum(v for (_, b), v in table.items() if b == 3)
opts = [px0, table[(0, 2)] + table[(0, 3)], px0 + py3 - table[(0, 3)], Fraction(80, 100)]
ok &= report("P6-01", opts == [Fraction(40,100), Fraction(22,100), Fraction(70,100), Fraction(80,100)] and opts.count(Fraction(70,100)) == 1)

area = sp.integrate(2-y, (y, 0, 2))
ok &= report("P6-02", area == 2 and sp.integrate(2-y, (y, 0, 1))/area == sp.Rational(3,4))
fy = sp.integrate(2, (x, y, 1))
ok &= report("P6-03", sp.simplify(fy - 2*(1-y)) == 0 and sp.integrate(2*(1-y), (y, sp.Rational(1,2), 1)) == sp.Rational(1,4))
ok &= report("P6-04", sp.Rational(2,3)**3 == sp.Rational(8,27) and sp.diff(z**3, z) == 3*z**2)

pa = sp.integrate(sp.integrate(x+y, (y, 0, 1-x)), (x, 0, 1))
joint_x_a = sp.integrate(x+y, (y, 0, 1-x))
ok &= report("P6-05", pa == sp.Rational(1,3) and sp.simplify(joint_x_a/pa - sp.Rational(3,2)*(1-x**2)) == 0 and sp.integrate(joint_x_a/pa, (x, sp.Rational(1,2), 1)) == sp.Rational(5,16))

theta = sp.symbols('theta', real=True)
f = 1 + theta*(2*x-1)*(2*y-1)
fx = sp.integrate(f, (y, 0, 1)); fy2 = sp.integrate(f, (x, 0, 1))
quad = sp.integrate(sp.integrate(f, (y, 0, sp.Rational(1,2))), (x, 0, sp.Rational(1,2)))
ok &= report("P6-06", sp.simplify(fx-1) == 0 and sp.simplify(fy2-1) == 0 and sp.simplify(quad-(sp.Rational(1,4)+theta/16)) == 0 and sp.solve(sp.Eq(quad, sp.Rational(1,4)), theta) == [0])

ok &= report("P6-07", sp.integrate(sp.Rational(1,2), (x, 0, z)) == z/2 and sp.integrate(sp.Rational(1,2), (x, 0, 1)) == sp.Rational(1,2) and sp.simplify(sp.integrate(sp.Rational(1,2), (x, z-2, 1)) - (3-z)/2) == 0 and sp.integrate((3-z)/2, (z, 2, 3)) == sp.Rational(1,4))

rho = sp.Rational(1,2)
ok &= report("P6-08", rho*sp.Rational(3,2)*2 == sp.Rational(3,2) and 9*(1-rho**2) == sp.Rational(27,4) and rho*sp.Rational(2,3)*3 == 1 and 4*(1-rho**2) == 3)

vals = [sp.binomial(3,k)*sp.binomial(2,2-k)/sp.binomial(5,2) for k in range(3)]
ok &= report("P6-09", vals == [sp.Rational(1,10), sp.Rational(3,5), sp.Rational(3,10)] and sum(vals) == 1)
print("MANUAL P6-10")

ok &= report("P6-11", sp.diff(2*z-z**2, z) == 2*(1-z) and sp.integrate(2*(1-z), (z, sp.Rational(1,2), 1)) == sp.Rational(1,4))

flow = sp.integrate(sp.integrate(1, (y, 0, z*x)), (x, 0, 1))
fhigh = 1 - sp.integrate(sp.integrate(1, (y, z*x, 1)), (x, 0, 1/z))
ok &= report("P6-12", flow == z/2 and sp.simplify(fhigh-(1-1/(2*z))) == 0 and 1-fhigh.subs(z,2) == sp.Rational(1,4))

a = sp.symbols('a')
ok &= report("P6-13", sp.solve(sp.Eq(a-2, 0), a) == [2] and 2**2*4+9 == 25)

cond_area = sp.integrate(1-y, (y, 0, 1))
inter_area = sp.integrate(sp.integrate(1, (x, 1-y, y)), (y, sp.Rational(1,2), 1))
ok &= report("P6-14", cond_area == sp.Rational(1,2) and inter_area == sp.Rational(1,4) and inter_area/cond_area == sp.Rational(1,2))

raise SystemExit(0 if ok else 1)
