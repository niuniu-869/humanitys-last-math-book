import sympy as s
import mpmath as mp

mp.mp.dps = 40

x, t, u = s.symbols('x t u', real=True)

def same(a, b):
    return s.simplify(a - b) == 0

def check(k, ok):
    print(f"{'PASS' if ok else 'FAIL'} 例{k}")
    if not ok:
        raise AssertionError(k)

# 1--9: first-class substitution, transformations, and the auxiliary-function proof.
check(1, same(s.diff(s.exp(x**2)/2, x), x*s.exp(x**2)))
check(2, same(s.diff(-s.log(s.cos(x)), x), s.tan(x)) and same(s.diff(s.log(s.log(x)), x), 1/(x*s.log(x))))
check(3, same(s.diff(s.atan(x/2)/2, x), 1/(4+x**2)) and same(s.diff(s.asin(x/3), x), 1/s.sqrt(9-x**2)))
check(4, same(s.diff(s.atan((x+1)/2)/2, x), 1/(x**2+2*x+5)))
check(5, same(s.diff(-s.cos(x)+s.cos(x)**3/3, x), s.sin(x)**3) and same(s.diff(s.sin(x)**3/3-s.sin(x)**5/5, x), s.sin(x)**2*s.cos(x)**3))
check(6, same(s.diff(s.log(1/s.cos(x)+s.tan(x)), x), 1/s.cos(x)))
check(7, same(s.diff(s.atan(s.exp(x)), x), 1/(s.exp(x)+s.exp(-x))))
T = s.symbols('T', positive=True)
N = 100*s.log(1+T**2)
check(8, same(s.diff(N, T), 200*T/(1+T**2)) and same(N.subs(T, 10), 100*s.log(101)))
G = (1+x**2)*s.Function('f')(x)
check(9, same(s.diff(G, x), 2*x*s.Function('f')(x)+(1+x**2)*s.diff(s.Function('f')(x), x)))
print('MANUAL lesson-09 proof: Rolle theorem; PASS above checks only the auxiliary identity')

# 10--14: second-class substitutions.
ans10 = 2*s.asin(x/2) + x*s.sqrt(4-x**2)/2
check(10, same(s.diff(ans10, x), s.sqrt(4-x**2)))
check(11, same(s.diff(s.log(x+s.sqrt(x**2+1)), x), 1/s.sqrt(x**2+1)))
xp = s.symbols('xp', positive=True)
ans12 = s.sqrt(xp**2-1)-s.acos(1/xp)
check(12, same(s.diff(ans12, xp), s.sqrt(xp**2-1)/xp))
check(13, same(s.diff(2*s.atan(s.sqrt(x-1)), x), 1/(x*s.sqrt(x-1))))
ans14 = s.log(x)-s.log(1+x**4)/4
check(14, same(s.diff(ans14, x), 1/(x*(x**4+1))))

# 15--18: definite substitution and parameter-dependent integrals.
check(15, s.integrate(s.sqrt(1-x**2), (x, 0, 1)) == s.pi/4)
check(16, same(s.integrate(1/(1+s.sqrt(x)), (x, 0, 4)), 4-2*s.log(3)))
f = s.Function('f')
F17 = s.Rational(1,2)*s.Integral(f(u), (u, 0, x**2))
check(17, same(s.diff(F17.doit(), x), x*f(x**2)))
A, B = s.symbols('A B', real=True)
H = s.Integral(f(u), (u, 0, x))/x
check('18-general-derivative', same(s.diff(H, x), f(x)/x-s.Integral(f(u), (u, 0, x))/x**2))
# These checks cover algebra and representative cases; the text supplies the general limit argument.
for name, func, expected in [('polynomial', A*x+B*x**2, A/2), ('sine', s.sin(x), s.Rational(1,2))]:
    y = s.symbols('y', real=True)
    sample_H = s.integrate(func.subs(x, y), (y, 0, x))/x
    for direction in ('-', '+'):
        check('18-'+name+'-'+direction,
              s.limit(sample_H/x, x, 0, dir=direction) == expected
              and s.limit(s.diff(sample_H, x), x, 0, dir=direction) == expected)
for sign in (-1, 1):
    # f(y)=y*abs(y); t is in [0,1], so its branch is fixed by the sign of x.
    sample_H = s.integrate(sign*(x*t)**2, (t, 0, 1))
    check('18-x-abs-x-'+str(sign), s.limit(sample_H/x, x, 0) == 0
          and s.limit(s.diff(sample_H, x), x, 0) == 0)

# 19--24: symmetry and interval reflection.
check(19, s.integrate((x+s.sqrt(1-x**2))**2, (x, -1, 1)) == 2)
check(20, same(s.integrate(1/(1+s.exp(x)), (x, -2, 2)), 2))
check(21, 100*s.sqrt(2)*s.integrate(s.sin(x), (x, 0, s.pi)) == 200*s.sqrt(2))
check(22, s.integrate(s.sin(x)/(s.sin(x)+s.cos(x)), (x, 0, s.pi/2)) == s.pi/4)
base23 = s.integrate(s.sin(x)/(1+s.cos(x)**2), (x, 0, s.pi))
check(23, same(base23, s.pi/2) and same(s.pi*base23/2, s.pi**2/4))
check('23-original-integral', abs(mp.quad(lambda v: v*mp.sin(v)/(1+mp.cos(v)**2), [0, mp.pi])-mp.pi**2/4) < mp.mpf('1e-30'))
check(24, abs(mp.quad(lambda v: mp.log(1+mp.tan(v)), [0, mp.pi/4])-mp.pi*mp.log(2)/8) < mp.mpf('1e-30'))

# 25--30: integration by parts.
check(25, same(s.diff((x-1)*s.exp(x), x), x*s.exp(x)))
check(26, same(s.diff(x*s.log(x)-x, x), s.log(x)) and same(s.diff(x*s.atan(x)-s.log(1+x**2)/2, x), s.atan(x)))
check(27, same(s.diff((x**2-2*x+2)*s.exp(x), x), x**2*s.exp(x)))
I28 = s.exp(x)*(s.sin(x)-s.cos(x))/2
check(28, same(s.diff(I28, x), s.exp(x)*s.sin(x)))
check(29, same(s.diff(2*(s.sqrt(x)-1)*s.exp(s.sqrt(x)), x), s.exp(s.sqrt(x))))
f0 = s.sin(x)/x
ans30 = s.cos(x)-2*s.sin(x)/x
check(30, same(s.diff(ans30, x), x*s.diff(s.diff(f0, x), x)))

# 31--33: definite integration by parts and Wallis.
check(31, s.integrate(s.atan(x), (x, 0, 1)) == s.pi/4-s.log(2)/2)
check(32, s.integrate(s.sin(x)**5, (x, 0, s.pi/2)) == s.Rational(8,15) and s.integrate(s.cos(x)**6, (x, 0, s.pi/2)) == 5*s.pi/32)
check(33, abs(mp.quad(lambda v: v**4*mp.sqrt(1-v*v), [0, 1])-mp.pi/32) < mp.mpf('1e-30'))

# 34--38: rational functions and partial fractions.
check(34, same(s.diff(s.log(x)/2-s.log(x+1)+s.log(x+2)/2, x), 1/(x*(x+1)*(x+2))))
ans35 = x**2/2 - x + s.Rational(4,3)*s.log(x-1) + s.Rational(11,3)*s.log(x+2)
check(35, same(s.diff(ans35, x), (x**3+2*x+1)/(x**2+x-2)))
ans36 = s.log(x)-s.log(x-1)-1/(x-1)
check(36, same(s.diff(ans36, x), 1/(x*(x-1)**2)))
check(37, same(s.diff(s.log(x-1)/2-s.log(x**2+1)/4-s.atan(x)/2, x), 1/((x-1)*(x**2+1))) and same(s.diff(s.log(x**2+2*x+5)+s.atan((x+1)/2)/2, x), (2*x+3)/(x**2+2*x+5)))
check(38, s.integrate(1/((x+1)*(x**2+1)), (x, 0, 1)) == s.log(2)/4+s.pi/8)

# 39--41: rationalization substitutions.
check(39, s.integrate(1/(1+s.sin(x)+s.cos(x)), (x, 0, s.pi/2)) == s.log(2))
xx = s.symbols('xx', positive=True)
ans40 = 2*s.sqrt(xx)-3*xx**s.Rational(1,3)+6*xx**s.Rational(1,6)-6*s.log(1+xx**s.Rational(1,6))
check(40, same(s.diff(ans40, xx), 1/(s.sqrt(xx)+xx**s.Rational(1,3))))
check(41, same(s.diff(x-s.log(s.exp(x)+1), x), 1/(s.exp(x)+1)))

# 42--46: method choice and Riemann sums.
check(42, same(s.diff((x**2-1)*s.exp(x**2)/2, x), x**3*s.exp(x**2)))
check(43, same(s.integrate(s.integrate(s.exp(-t**2), (t, x, 1)), (x, 0, 1)), (1-s.exp(-1))/2))
check(44, s.log(2) == s.integrate(1/(1+x), (x, 0, 1)) and s.pi/4 == s.integrate(1/(1+x**2), (x, 0, 1)))
nn = s.symbols('nn', positive=True)
lower45 = nn**2/(nn**2+nn)
upper45 = nn**2/(nn**2+1)
check(45, s.limit(lower45, nn, s.oo) == 1 and s.limit(upper45, nn, s.oo) == 1)
check(46, same(s.integrate(s.log(1+x), (x, 0, 1)), 2*s.log(2)-1))

# Sixteen exercise groups, with two questions after example 32.
primitives = [
    ('after-01', s.exp(x**3)/3, x**2*s.exp(x**3)),
    ('after-04', s.asin((x+1)/2), 1/s.sqrt(3-2*x-x**2)),
    ('after-06', s.log(1/s.sin(x)-s.cos(x)/s.sin(x)), 1/s.sin(x)),
    ('after-10', -s.sqrt(1-x**2)/x, 1/(x**2*s.sqrt(1-x**2))),
    ('after-11', -s.sqrt(x**2+1)/x, 1/(x**2*s.sqrt(x**2+1))),
    ('after-25', -x*s.cos(x)+s.sin(x), x*s.sin(x)),
    ('after-34', (s.log(x-1)-s.log(x+1))/2, 1/(x**2-1)),
    ('after-42', (x**3-1)*s.exp(x**3)/3, x**5*s.exp(x**3)),
]
for name, primitive, integrand in primitives:
    check('exercise-'+name, same(s.diff(primitive, x), integrand))
definites = [
    ('after-15', 1/(s.sqrt(x)*(1+s.sqrt(x))), 1, 4, 2*s.log(s.Rational(3,2))),
    ('after-19', x*s.cos(x)+s.sin(x)**2, -s.pi, s.pi, s.pi),
    ('after-20', 1/(1+2**x), -1, 1, 1),
    ('after-32-a', s.cos(x)**7, 0, s.pi/2, s.Rational(16,35)),
    ('after-32-b', s.sin(x)**4, 0, s.pi/2, 3*s.pi/16),
    ('after-39', 1/(2+s.cos(x)), 0, s.pi/2, s.sqrt(3)*s.pi/9),
    ('after-44', s.sin(s.pi*x), 0, 1, 2/s.pi),
    ('after-46', x*s.exp(x), 0, 1, 1),
]
for name, integrand, lo, hi, expected in definites:
    check('exercise-'+name, same(s.integrate(integrand, (x, lo, hi)), expected))
check('exercise-after-22', abs(mp.quad(lambda v: mp.sin(v)**3/(mp.sin(v)**3+mp.cos(v)**3), [0, mp.pi/2])-mp.pi/4) < mp.mpf('1e-30'))

# Verify printed approximations from their actual sums or integrals.
def rounded(k, actual, printed, digits):
    check(k, abs(actual-mp.mpf(printed)) <= mp.mpf(10)**(-digits)/2)

rounded('08-count-one-decimal', mp.quad(lambda v: 200*v/(1+v*v), [0, 10]), '461.5', 1)
rounded('08-count-integer', mp.quad(lambda v: 200*v/(1+v*v), [0, 10]), '462', 0)
rate = 200*t/(1+t**2)
check('08-speed-maximum', s.solve(s.diff(rate, t), t) == [-1, 1]
      and rate.subs(t, 1) == 100
      and same(s.diff(rate, t), 200*(1-t**2)/(1+t**2)**2))
for count, printed, digits in [(4, '0.46875', 5), (10, '0.385', 3), (100, '0.33835', 5), (1000, '0.33383', 5)]:
    total = mp.fsum((mp.mpf(j)/count)**2/count for j in range(1, count+1))
    rounded('table-S-'+str(count), total, printed, digits)
rounded('44-sum-1-n1000', mp.fsum(1/mp.mpf(1000+j) for j in range(1, 1001)), '0.69290', 5)
rounded('44-sum-2-n1000', mp.fsum(mp.mpf(1000)/(1000**2+j*j) for j in range(1, 1001)), '0.78515', 5)
rounded('44-limit-1', mp.log(2), '0.69315', 5)
rounded('44-limit-2', mp.pi/4, '0.78540', 5)
rounded('46-limit', 4/mp.e, '1.4715', 4)
product_root = mp.exp(mp.fsum(mp.log(1+mp.mpf(j)/1000) for j in range(1, 1001))/1000)
rounded('46-product-n1000', product_root, '1.4720', 4)
