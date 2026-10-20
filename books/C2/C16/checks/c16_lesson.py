import sympy as sp

n = sp.symbols("n", integer=True, positive=True)
x = sp.symbols("x", real=True)
pi = sp.pi

def report(name, ok):
    print(("PASS " if ok else "FAIL ") + name)

f = 3+2*sp.cos(x)-sp.sin(2*x)
projection_terms = [sp.integrate(term, (x, -pi, pi)) for term in
                    (3*sp.cos(x), 2*sp.cos(x)**2, -sp.sin(2*x)*sp.cos(x))]
report("投影示范", projection_terms == [0, 2*pi, 0] and sp.integrate(f*sp.cos(x), (x, -pi, pi))/pi == 2)
for label, expr, expected in [
    ("余弦零频", sp.cos(0*x)**2, 2*pi),
    ("正弦零频", sp.sin(0*x)**2, 0),
    ("余弦异频", sp.cos(n*x), 0),
    ("余弦同频", sp.cos(n*x)**2, pi),
    ("正弦同频", sp.sin(n*x)**2, pi),
    ("正弦余弦", sp.sin(n*x)*sp.cos(n*x), 0),
]:
    report("正交性-"+label, sp.simplify(sp.integrate(expr, (x, -pi, pi))-expected) == 0)

# 例 1：f(x)=x 的奇函数系数。
b1 = sp.simplify(2/pi * sp.integrate(x*sp.sin(n*x), (x, 0, pi)))
report("例1", sp.simplify(b1 - 2*(-1)**(n+1)/n) == 0)

# 随堂方波：偶数项为 0，奇数项为 4/(n*pi)。
b_square = sp.simplify(2/pi * sp.integrate(sp.sin(n*x), (x, 0, pi)))
report("例1方波", sp.simplify(b_square - 2*(1-(-1)**n)/(n*pi)) == 0)

# 例 2：端点处使用周期延拓后的左右极限。
left, right = sp.Integer(-1), 1+x**2
S0 = (sp.limit(left, x, 0, dir="-")+sp.limit(right, x, 0, dir="+"))/2
Spi = (sp.limit(right, x, pi, dir="-")+sp.limit(left, x, -pi, dir="+"))/2
report("例2", S0 == 0 and sp.simplify(Spi-pi**2/2) == 0)

for cutoff, expected in [(1, "1.2732"), (3, "0.8488"), (7, "0.9216"), (21, "1.0289"), (101, "1.0062")]:
    partial = sum(4*sp.sin(k*x)/(k*pi) for k in range(1, cutoff+1, 2))
    report(f"方波表-N{cutoff}-pi/2", f"{float(partial.subs(x, pi/2)):.4f}" == expected)
    report(f"方波表-N{cutoff}-0", partial.subs(x, 0) == 0)

# 例 3：x^2 的 a0、an 与两项级数结论。
a0_x2 = sp.simplify(2/pi * sp.integrate(x**2, (x, 0, pi)))
an_x2 = sp.simplify(2/pi * sp.integrate(x**2*sp.cos(n*x), (x, 0, pi)))
m = sp.symbols("m", integer=True, positive=True)
sum_value = sp.summation(1/m**2, (m, 1, sp.oo))
report("例3", a0_x2 == 2*pi**2/3 and sp.simplify(an_x2 - 4*(-1)**n/n**2) == 0 and sp.simplify(pi**2 - pi**2/3 - 4*sum_value) == 0)
alternating = sp.summation((-1)**(m+1)/m**2, (m, 1, sp.oo))
report("例3-交错求和", sp.simplify(alternating-pi**2/12) == 0 and sp.simplify(a0_x2/2-4*alternating) == 0)

roof_a0 = 2/pi*sp.integrate(x, (x, 0, pi))
roof_an = sp.simplify(2/pi*sp.integrate(x*sp.cos(n*x), (x, 0, pi)))
report("第3节-余弦展开", roof_a0 == pi and sp.simplify(roof_an-2*((-1)**n-1)/(pi*n**2)) == 0)
report("第3节-奇偶下标", sp.simplify(roof_an.subs(n, 2*m)) == 0 and sp.simplify(roof_an.subs(n, 2*m-1)+4/(pi*(2*m-1)**2)) == 0)

# 例 4：区间 [0,2] 的余弦级数系数。
l = sp.Integer(2)
a0_x = sp.simplify(2/l * sp.integrate(x, (x, 0, l)))
an_x = sp.simplify(2/l * sp.integrate(x*sp.cos(n*pi*x/l), (x, 0, l)))
target = sp.simplify(4*((-1)**n-1)/(n**2*pi**2))
report("例4", a0_x == 2 and sp.simplify(an_x-target) == 0)
report("例4-换下标", sp.simplify(an_x.subs(n, 2*m)) == 0 and sp.simplify(an_x.subs(n, 2*m-1)+8/(pi**2*(2*m-1)**2)) == 0)
