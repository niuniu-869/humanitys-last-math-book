#!/usr/bin/env python3
"""M.6 题目独立验算；证明链另作人工核对。"""
import sympy as sp

R = sp.Rational


def report(tag, ok):
    print(f"{'PASS' if ok else 'FAIL'} {tag}")


w = sp.Matrix([2, -1])
pts = [sp.Matrix(p) for p in [(1, 0), (0, 2), (2, 1)]]
distances = [abs(w.dot(p)-1)/w.norm() for p in pts]
choices = [R(1, 5), 1/sp.sqrt(5), 2/sp.sqrt(5), -1/sp.sqrt(5)]
report("M6-01", distances == [1/sp.sqrt(5), 3/sp.sqrt(5), 2/sp.sqrt(5)]
       and [c == min(distances) for c in choices] == [False, True, False, False])

x, y, a1, a2, a3 = sp.symbols("x y a1 a2 a3", real=True)
g2 = [1-x, 1-y, 2-x-y]
L2 = x*x+y*y+sum(a*g for a, g in zip([a1, a2, a3], g2))
eq2 = [sp.diff(L2, z).subs({x: 1, y: 1}) for z in (x, y)]
sol2 = sp.solve(eq2, [a1, a2])
domain2 = sp.reduce_inequalities([sol2[a1] >= 0, sol2[a2] >= 0, a3 >= 0], a3)
report("M6-02-乘子全解", sol2 == {a1: 2-a3, a2: 2-a3}
       and domain2.as_set() == sp.Interval(0, 2))
report("M6-02-选项", all(e.subs({a1: 2, a2: 2, a3: 0}) == 0 for e in eq2)
       and any(e.subs({a1: 0, a2: 0, a3: 0}) != 0 for e in eq2)
       and all(g.subs({x: 1, y: 1}) == 0 for g in g2)
       and (x*x+y*y).subs({x: 1, y: 1}) == 2)

alpha = sp.symbols("alpha", real=True)


def kkt3(xv, av, g):
    L = (x-1)**2+alpha*g
    return (g.subs(x, xv) <= 0 and av >= 0
            and sp.diff(L, x).subs({x: xv, alpha: av}) == 0
            and av*g.subs(x, xv) == 0)


report("M6-03", [kkt3(2, 2, 2-x), kkt3(2, -2, 2-x),
                    kkt3(1, 0, 2-x), kkt3(2, 2, x-2)] == [True, False, False, False])

# 已人工核对任意可行点上的 J >= L >= m = J(xhat)，不假定极值存在。
print("MANUAL M6-04-第一问证明")
L4 = x*x+0*(1-x)
x4 = sp.solve(sp.diff(L4, x), x)[0]
q = sp.symbols("q", nonnegative=True)
report("M6-04-反例", x4 == 0 and L4.subs(x, x4) == 0
       and sp.expand((1+q)**2-1) == q*q+2*q and (x*x).subs(x, 1) == 1)

xs5 = [sp.Matrix(p) for p in [(1, 1), (0, 2), (-1, 1)]]
ys5 = [1, -1, 1]
bad_alpha = [R(1, 2), 0, R(1, 2)]
balance = sum(a*y for a, y in zip(bad_alpha, ys5))
bad_w = sum((a*y*p for a, y, p in zip(bad_alpha, ys5, xs5)), sp.zeros(2, 1))
bad_b = 1-bad_w.dot(xs5[0])
report("M6-05-拒绝伪解", balance == 1 and all(a >= 0 for a in bad_alpha)
       and ys5[1]*(bad_w.dot(xs5[1])+bad_b) == -2)
good_alpha = [1, 2, 1]
good_w = sum((a*y*p for a, y, p in zip(good_alpha, ys5, xs5)), sp.zeros(2, 1))
good_b = 1-good_w.dot(xs5[0])
report("M6-05-真实最优对照", sum(a*y for a, y in zip(good_alpha, ys5)) == 0
       and good_w == sp.Matrix([0, -2]) and good_b == 3
       and all(y*(good_w.dot(p)+good_b) == 1 for y, p in zip(ys5, xs5))
       and good_w.dot(good_w)/2 == sum(good_alpha)-good_w.dot(good_w)/2 == 2)
# 零乘子合法的独立反例：讲义三点的最优解。
old_x = [sp.Matrix(p) for p in [(3, 3), (4, 3), (1, 1)]]
old_y, old_a = [1, 1, -1], [R(1, 4), 0, R(1, 4)]
old_w = sum((a*y*p for a, y, p in zip(old_a, old_y, old_x)), sp.zeros(2, 1))
old_z = [y*(old_w.dot(p)-2) for y, p in zip(old_y, old_x)]
report("M6-05-零乘子反例", all(z >= 1 for z in old_z)
       and all(a*(z-1) == 0 for a, z in zip(old_a, old_z))
       and sum(a*y for a, y in zip(old_a, old_y)) == 0
       and old_w.dot(old_w)/2 == sum(old_a)-old_w.dot(old_w)/2)


def phi(p):
    x, y = p
    return sp.Matrix([1, sp.sqrt(2)*x, sp.sqrt(2)*y, x*x, sp.sqrt(2)*x*y, y*y])


uv = [sp.Matrix([1, 2]), sp.Matrix([2, -1])]
G = sp.Matrix(2, 2, lambda i, j: uv[i].dot(uv[j]))
K = sp.Matrix(2, 2, lambda i, j: (G[i, j]+1)**2)
mapped = sp.Matrix(2, 2, lambda i, j: phi(uv[i]).dot(phi(uv[j])))
wrong = G.copy()
for i in range(2):
    wrong[i, i] = K[i, i]
report("M6-06-核矩阵", K == mapped == sp.Matrix([[36, 1], [1, 36]])
       and wrong == sp.diag(36, 36) and wrong != K)
new_dot = mapped[0, 1]
report("M6-06-选项", [G[0, 1] == 0 and new_dot == 1 and new_dot != 0,
       new_dot == 0, new_dot == 1 and new_dot == 0,
       mapped[0, 0] == mapped[1, 1] == new_dot == 36] == [True, False, False, False])
p, r = sp.symbols("p r", real=True)
report("M6-06-映射恒等式", sp.expand(phi(sp.Matrix([x, y])).dot(phi(sp.Matrix([p, r])))
       - (x*p+y*r+1)**2).simplify() == 0)

# 从起作用约束求候选，再用全部 KKT 条件求参数区间。
u, v, t = sp.symbols("u v t", real=True)
g7 = [1-u, t-u-v]
J7 = (u*u+v*v)/2
L7 = J7+a1*g7[0]+a2*g7[1]
stationary = [sp.diff(L7, z) for z in (u, v)]
cases = [([g7[0], a2], (1, 0, 1, 0), t <= 1, R(1, 2)),
         (g7, (1, t-1, 2-t, t-1), sp.And(t >= 1, t <= 2), (1+(t-1)**2)/2),
         ([a1, g7[1]], (t/2, t/2, 0, t/2), t >= 2, t*t/4)]
solutions = []
for i, (active, expected, domain, value) in enumerate(cases, 1):
    sol = sp.solve(stationary+active, [u, v, a1, a2], dict=True)[0]
    solutions.append(sol)
    feasible = sp.reduce_inequalities([g.subs(sol) <= 0 for g in g7]
                                    + [sol[a1] >= 0, sol[a2] >= 0], t)
    report(f"M6-07-区间{i}", tuple(sol[z] for z in (u, v, a1, a2)) == expected
           and feasible.as_set() == domain.as_set() and sp.simplify(J7.subs(sol)-value) == 0
           and all(sp.simplify((a*g).subs(sol)) == 0 for a, g in zip([a1, a2], g7)))
    gap = L7.subs({a1: sol[a1], a2: sol[a2]})-value
    squares = ((u-sol[u])**2+(v-sol[v])**2)/2
    report(f"M6-07-最优性{i}", sp.simplify(gap-squares) == 0)
report("M6-07-端点", all(sp.simplify(solutions[i][z].subs(t, i+1)
       - solutions[i+1][z].subs(t, i+1)) == 0 for i in range(2) for z in (u, v, a1, a2)))
