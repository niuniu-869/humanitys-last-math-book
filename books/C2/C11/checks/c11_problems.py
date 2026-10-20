import math
import mpmath as mp
import sympy as s
from sympy.integrals.risch import NonElementaryIntegral, risch_integrate

mp.mp.dps = 40

x, a, t, n = s.symbols('x a t n', real=True)

def same(p, q):
    return s.simplify(p - q) == 0

def check(k, ok):
    print(f"{'PASS' if ok else 'FAIL'} {k}")
    if not ok:
        raise AssertionError(k)

integrand01 = x*s.sqrt(1+x**2)
value01 = s.integrate(integrand01, (x, -1, 1))
primitive01 = (1+x**2)**s.Rational(3, 2)/3
check('C11-01-A', same(s.diff(primitive01, x), integrand01)
      and same(primitive01.subs(x, 1)-primitive01.subs(x, -1), value01))
check('C11-01-B', value01 == 0)
check('C11-01-C', s.integrate(s.sqrt(t)/2, (t, 1, 2)) != value01)
check('C11-01-D', same(integrand01.subs(x, -x), -integrand01)
      and 2*s.integrate(integrand01, (x, 0, 1)) != value01)
F = x**2*s.log(x)/2 - x**2/s.Integer(4) + s.Rational(1, 4)
check('C11-02', same(s.diff(F, x), x*s.log(x)) and F.subs(x, 1) == 0)
I_nonzero = s.log(1+a)/a
primitive06 = -s.log(1+a*s.cos(x))/a
check('C11-06-general', same(s.diff(primitive06, x), s.sin(x)/(1+a*s.cos(x)))
      and same(primitive06.subs(x, s.pi/2)-primitive06.subs(x, 0), I_nonzero))
check('C11-06-samples', s.integrate(s.sin(x)/(1+2*s.cos(x)), (x, 0, s.pi/2)) == s.log(3)/2 and s.integrate(s.sin(x)/(1-s.cos(x)/2), (x, 0, s.pi/2)) == -2*s.log(s.Rational(1,2)))
check('C11-06-zero', s.integrate(s.sin(x), (x, 0, s.pi/2)) == 1 and s.limit(I_nonzero, a, 0) == 1)
cum = s.integrate(s.sin(x), (x, 0, s.pi)) + s.integrate(-s.sin(x), (x, s.pi, 3*s.pi/2))
check('C11-05', cum == 3)
q = s.symbols('q', real=True)
cum_second = s.integrate(s.sin(x), (x, 0, s.pi)) + s.integrate(-s.sin(x), (x, s.pi, q))
check('C11-05-unique', s.solveset(cum_second-3, q, domain=s.Interval.open(s.pi, 2*s.pi)) == s.FiniteSet(3*s.pi/2))
opts05 = [(x**2-1)*s.atan(x)/2-x/2, (x**2+1)*s.atan(x)/2-x/2, x**2*s.atan(x)/2-x/2, x**2*s.atan(x)/2+x/2]
derivs05 = [s.simplify(s.diff(v, x)-x*s.atan(x)) for v in opts05]
expected_diffs = [-1/(1+x**2), 0, -1/(2*(1+x**2)), (x**2+s.Rational(1,2))/(1+x**2)]
for letter, actual, expected in zip('ABCD', derivs05, expected_diffs):
    check('C11-07-'+letter, same(actual, expected))
ans06 = s.atan(x)/3 - s.atan(x/2)/6
A, B = s.symbols('A B')
coeffs = s.solve(s.Poly(A*(x**2+4)+B*(x**2+1)-1, x).all_coeffs(), (A, B))
check('C11-04', coeffs == {A: s.Rational(1,3), B: -s.Rational(1,3)}
      and same(s.diff(ans06, x), 1/((x**2+1)*(x**2+4))))
I2 = s.integrate(s.sin(x)**2, (x, 0, s.pi/2))
I4 = s.integrate(s.sin(x)**4, (x, 0, s.pi/2))
I6 = s.integrate(s.sin(x)**6, (x, 0, s.pi/2))
check('C11-08', same((I4-I6)/(I2-I4), s.Rational(1,2)))
G = 2/s.sqrt(3)*s.atan((2*s.tan(x/2)+1)/s.sqrt(3))
left = s.limit(G, x, s.pi, dir='-')
right = s.limit(G, x, s.pi, dir='+')
check('C11-09-limits', left == s.pi/s.sqrt(3) and right == -s.pi/s.sqrt(3)
      and same(left-right, 2*s.pi/s.sqrt(3)))
z = s.symbols('z', real=True)
Gz = G.subs(s.tan(x/2), z)
check('C11-09-derivative', same(s.diff(Gz, z)*(1+z**2)/2, 1/(2+2*z/(1+z**2))))
for direction in ('-', '+'):
    boundary = left if direction == '-' else right
    check('C11-09-difference-quotient-'+direction,
          s.limit((G-boundary)/(x-s.pi), x, s.pi, dir=direction) == s.Rational(1,2))
f = s.Function('f')
F10 = s.Integral(f(t), (t, 0, x))
check('C11-10-auxiliary', same(s.diff(x*F10, x), F10+x*f(x)))
print('MANUAL C11-10 proof: Rolle theorem and endpoint hypotheses')
solvable10 = [x*s.exp(x**2), x**3*s.exp(x**2), s.exp(x)*s.sin(x)]
candidates10 = [s.exp(x**2)/2, (x**2-1)*s.exp(x**2)/2, s.exp(x)*(s.sin(x)-s.cos(x))/2]
raw10 = risch_integrate(s.exp(x**2), x)
for letter, candidate, integrand in zip('ACD', candidates10, solvable10):
    check('C11-03-'+letter, same(s.diff(candidate, x), integrand))
check('C11-03-B', isinstance(raw10, NonElementaryIntegral))
check('C11-11', s.integrate(x*s.log(1+x), (x, 0, 1)) == s.Rational(1,4))
F12 = s.Integral(s.exp(-t**2), (t, 0, x**2))
derivative12 = s.diff(F12, x)
positive = s.symbols('positive', positive=True)
check('C11-12', same(derivative12, 2*x*s.exp(-x**4))
      and derivative12.subs(x, positive).is_positive
      and derivative12.subs(x, -positive).is_negative)
I13 = s.integrate(s.sqrt(1+x**2)/x**2, (x, 1, s.sqrt(3)))
E13 = s.asinh(s.sqrt(3)) - s.log(1+s.sqrt(2)) - 2/s.sqrt(3) + s.sqrt(2)
trig13 = s.integrate(s.sec(t)**3/s.tan(t)**2, (t, s.pi/4, s.pi/3))
recip13 = s.integrate(-s.sqrt(1+t**2)/t, (t, 1, 1/s.sqrt(3)))
check('C11-13', same(I13, E13) and same(recip13, E13))
check('C11-13-trig-limits', abs(complex(s.N(trig13-E13, 50))) < 1e-40)
F13 = s.log(x+s.sqrt(1+x**2)) - s.sqrt(1+x**2)/x
check('C11-13-antiderivative', same(s.diff(F13, x), s.sqrt(1+x**2)/x**2))
check('C11-14', s.integrate(x*s.integrate(s.exp(-t**2), (t, x**2, 1)), (x, 0, 1)) == (1-s.exp(-1))/4)
check('C11-15-auxiliary', same(s.expand((x-a)*f(x)), x*f(x)-a*f(x)))
print('MANUAL C11-15 proof: continuity, sign and contradiction')
i = s.symbols('i', integer=True, positive=True)
for nn in (1000, 10000):
    vals = sum(math.log((nn+2*j)/(nn+2*j-1)) for j in range(1, nn+1))
    lower = sum(1/(nn+2*j) for j in range(1, nn+1))
    upper = sum(1/(nn+2*j-1) for j in range(1, nn+1))
    check(f'C11-17-n{nn}', lower <= vals <= upper and abs(vals-math.log(3)/2) < 1/nn)
nn = s.symbols('nn', positive=True)
check('C11-17-right-midpoint', same(1/(nn+2*i), 1/nn/(1+2*i/nn))
      and same(1/(nn+2*i-1), 1/nn/(1+2*(i-s.Rational(1,2))/nn)))
check('C11-17-integral', s.integrate(1/(1+2*x), (x, 0, 1)) == s.log(3)/2)

# Final mixed exercises (the two proof arguments remain MANUAL).
I16 = mp.quad(lambda v: v/(1+mp.sin(v)**2), [0, mp.pi])
A16 = mp.quad(lambda v: 1/(1+mp.sin(v)**2), [0, mp.pi])
half16 = s.integrate(1/(1+2*x**2), (x, 0, s.oo))
check('C11-16', abs(I16-mp.pi**2/(2*mp.sqrt(2))) < mp.mpf('1e-30')
      and abs(A16-mp.pi/mp.sqrt(2)) < mp.mpf('1e-30')
      and abs(I16-mp.pi*A16/2) < mp.mpf('1e-30')
      and same(2*half16, s.pi/s.sqrt(2)))
vals17 = sum(math.log((1000+2*j)/(1000+2*j-1)) for j in range(1, 1001))
check('C11-17-n1000-direct', abs(vals17-math.log(3)/2) < 0.001)
