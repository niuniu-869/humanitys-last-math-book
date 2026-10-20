"""用 SymPy 独立核对 C.20 讲义例题中的数值和结论。"""
import sympy as sp


def report(n, condition):
    print(f"{'PASS' if bool(condition) else 'FAIL'} 例{n}")


x, y = sp.symbols('x y', real=True)

# 例1：根号与对数的两个定义域限制。
report(1, (4 - 1 - 1 >= 0) and (1 - (-1) > 0))
# 例2、3：等高线方程及两点效用相等。
u_rot, v_rot = sp.symbols('u_rot v_rot', real=True)
rotated = (x*y).subs({x: (u_rot+v_rot)/sp.sqrt(2), y: (u_rot-v_rot)/sp.sqrt(2)})
report(2, sp.expand(rotated) == (u_rot**2-v_rot**2)/2)
report(3, sp.sqrt(4*9) == 6 and sp.sqrt(12*3) == 6)
# 例4：估计量 rho 趋于 0。
rho = sp.symbols('rho', nonnegative=True)
report(4, sp.limit(rho, rho, 0) == 0)
# 例5：两条路径给出 0 与 1/2。
h = x*y/(x**2+y**2)
report(5, sp.simplify(h.subs(y, 0)) == 0 and sp.simplify(h.subs(y, x)) == sp.Rational(1, 2))
# 例6：直线给 0，抛物线给 1/2。
k = sp.symbols('k', real=True)
q6 = x*y**2/(x**2+y**4)
report(6, sp.limit(q6.subs(y, k*x), x, 0) == 0 and sp.simplify(q6.subs(x, y**2)) == sp.Rational(1, 2))
# 例7、8：重要极限和有理化。
t = sp.symbols('t', real=True)
report(7, sp.limit(sp.sin(t)/t, t, 0) == 1)
q8 = (x**2+y**2)/(sp.sqrt(x**2+y**2+1)-1)
report(8, sp.simplify(q8 - (sp.sqrt(x**2+y**2+1)+1)) == 0)
# 例9：极坐标统一上界 rho 对所有角度成立，故补值为零。
angle = sp.symbols('angle', real=True)
rad = sp.symbols('rad', positive=True)
q9 = x**2*y/(x**2+y**2)
polar9 = sp.trigsimp(q9.subs({x: rad*sp.cos(angle), y: rad*sp.sin(angle)}))
report(9, sp.trigsimp(polar9-rad*sp.cos(angle)**2*sp.sin(angle)) == 0
       and sp.limit(rad, rad, 0) == 0)
# 例10：以平方半径为变量，在单位圆外侧构造两列不同函数值。
nn = sp.symbols('nn', integer=True, positive=True)
rr = sp.symbols('rr', real=True)
outer1 = 1+1/(2*nn*sp.pi+sp.pi/2)
outer2 = 1+1/(2*nn*sp.pi+3*sp.pi/2)
q10rad = sp.sin(1/(rr-1))
report(10, sp.solve(rr-1, rr) == [1]
       and sp.limit(outer1, nn, sp.oo) == sp.limit(outer2, nn, sp.oo) == 1
       and sp.simplify(q10rad.subs(rr, outer1)) == 1
       and sp.simplify(q10rad.subs(rr, outer2)) == -1)
# 例11：径向闭区间核对定理条件；其余两项直接算端点极限。
closed_radii = sp.Interval(0, 2)
report(11, closed_radii.boundary.is_subset(closed_radii)
       and closed_radii.sup.is_finite
       and sp.limit(sp.sqrt(2)*rad, rad, 1, dir='-') == sp.sqrt(2)
       and sp.limit(1/rad**2, rad, 0, dir='+') == sp.oo)
# 例12--16：偏导数数值。
report(12, (sp.diff(x**2+y**2, x).subs({x:1,y:2}), sp.diff(x**2+y**2, y).subs({x:1,y:2})) == (2,4))
q13 = x**2*y + sp.exp(x*y)
report(13, (sp.diff(q13,x).subs({x:1,y:1}), sp.diff(q13,y).subs({x:1,y:1})) == (2+sp.E, 1+sp.E))
q14 = x**y
report(14, sp.simplify(sp.diff(q14,x) - y*x**(y-1)) == 0
       and sp.simplify(sp.diff(q14,y) - x**y*sp.log(x)) == 0)
Q = 10*sp.sqrt(x*y)
report(15, (sp.diff(Q,x).subs({x:4,y:9}), sp.diff(Q,y).subs({x:4,y:9})) == (sp.Rational(15,2), sp.Rational(10,3)))
L = (2*x+y-5)**2
report(16, (sp.diff(L,x).subs({x:1,y:0}), sp.diff(L,y).subs({x:1,y:0}), L.subs({x:1,y:0})) == (-12,-6,9))
# 例17：h 沿两坐标轴为 0，所以原点偏导均为 0。
report(17, sp.simplify(h.subs(y,0)) == 0 and sp.simplify(h.subs(x,0)) == 0)
# 例18：余项 rho^2，切平面线性部分的数值。
dx, dy = sp.symbols('dx dy', real=True)
dz18 = 2*dx + 4*dy
delta18 = (1+dx)**2 + (2+dy)**2 - 5
report(18, sp.expand(delta18-dz18) == dx**2+dy**2 and dz18.subs({dx:sp.Rational(1,10),dy:-sp.Rational(1,10)}) == -sp.Rational(1,5))
# 例19：沿 y=x，g/r 为 1/2。
report(19, sp.simplify((x*x/sp.sqrt(2*x**2))/sp.sqrt(2*x**2)) == sp.Rational(1, 2))
# 例20、21：全微分、切平面。
z20 = x**2*y**3
report(20, (sp.diff(z20,x), sp.diff(z20,y)) == (2*x*y**3, 3*x**2*y**2))
Z = sp.Symbol('Z')
plane21 = sp.expand((Z-2) - (4*(x-1) + (y-2)))
report(21, sp.expand(plane21 - (Z - 4*x - y + 4)) == 0)
# 例22：线性近似值。
approx22 = 5 + sp.Rational(3,5)*sp.Rational(2,100) + sp.Rational(4,5)*(-sp.Rational(3,100))
report(22, approx22 == sp.Rational(1247,250))
# 例23：统一余项界趋零，沿指定序列的偏导趋于负无穷。
w = (x**2+y**2)*sp.sin(1/(x**2+y**2))
wx_seq = sp.simplify(sp.diff(w, x).subs({x: 1/sp.sqrt(2*nn*sp.pi), y: 0}))
report(23, sp.limit(rad**2/rad, rad, 0) == 0
       and sp.limit(wx_seq, nn, sp.oo) == -sp.oo)
# 例24：沿 y=x 的可微检验值为 1/sqrt(2)。
report(24, sp.simplify((sp.sqrt(x**2)/sp.sqrt(2*x**2)).subs(x, 1)) == 1/sp.sqrt(2))
# 例25：混合偏导相等。
z25 = x**3*y**2 + sp.sin(x*y)
report(25, sp.simplify(sp.diff(z25,x,y)-sp.diff(z25,y,x)) == 0)
# 例26：从分界点的一阶差商求混合偏导，再检查非连续的路径。
q26 = x*y*(x**2-y**2)/(x**2+y**2)
fx_on_y = sp.limit(q26/x, x, 0)
fy_on_x = sp.limit(q26/y, y, 0)
mixed26 = sp.diff(q26, x, y)
report(26, sp.diff(fx_on_y, y) == -1 and sp.diff(fy_on_x, x) == 1
       and sp.simplify(mixed26.subs(y, x)) == 0
       and sp.simplify(mixed26.subs(y, 0)) == 1)
# 例27：拉普拉斯和为 0。
u = sp.log(x**2+y**2)/2
report(27, sp.simplify(sp.diff(u,x,2)+sp.diff(u,y,2)) == 0)
