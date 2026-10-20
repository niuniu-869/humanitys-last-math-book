#!/usr/bin/env python3
"""独立核对 lesson.md 中例 1--8 的数值和结论。"""
import sympy as sp


R = sp.Rational


def report(tag, ok):
    print(f"{'PASS' if ok else 'FAIL'} {tag}")


# 例 1：三点的带标签值与间隔。
w = sp.Matrix([1, 3])
b = -6
xs = [sp.Matrix([3, 3]), sp.Matrix([4, 3]), sp.Matrix([1, 1])]
ys = [1, 1, -1]
vals = [yi * (w.dot(x) + b) for yi, x in zip(ys, xs)]
report("例1", vals == [6, 7, 2] and min(vals) / sp.sqrt(w.dot(w)) == 2 / sp.sqrt(10))

# 例 2：原问题候选点满足三条约束，目标值为 1/4。
w2 = sp.Matrix([R(1, 2), R(1, 2)])
b2 = -2
vals2 = [w2.dot(sp.Matrix([3, 3])) + b2,
         w2.dot(sp.Matrix([4, 3])) + b2,
         -(w2.dot(sp.Matrix([1, 1])) + b2)]
report("例2", vals2 == [1, R(3, 2), 1] and w2.dot(w2) / 2 == R(1, 4))

# 例 3：KKT 解。
x1, x2, al = sp.symbols("x1 x2 al")
sol3 = sp.solve([2 * x1 - al, 2 * x2 - al, x1 + x2 - 2], [x1, x2, al], dict=True)[0]
report("例3", sol3 == {x1: 1, x2: 1, al: 2} and sol3[x1] ** 2 + sol3[x2] ** 2 == 2)

# 例 4：边界约束下的投影点和放宽约束下的无约束点。
x1, x2, al = sp.symbols("x1 x2 al")
sol4 = sp.solve([2 * (x1 - 2) + al, 2 * (x2 - 1) + al, x1 + x2 - 2], [x1, x2, al], dict=True)[0]
report("例4", sol4 == {x1: R(3, 2), x2: R(1, 2), al: 1}
       and (2 + 1 <= 5) and sp.solve([2 * (x1 - 2), 2 * (x2 - 1)], [x1, x2]) == {x1: 2, x2: 1})

# 例 5：消去 alpha_3 后的对偶边界最大值。
a1, a2 = sp.symbols("a1 a2", nonnegative=True)
d5 = 2 * a1 + 2 * a2 - 4 * a1 ** 2 - 10 * a1 * a2 - R(13, 2) * a2 ** 2
boundary = sp.solve(sp.diff(d5.subs(a2, 0), a1), a1)[0]
report("例5", boundary == R(1, 4) and d5.subs({a1: boundary, a2: 0}) == R(1, 4)
       and sp.diff(d5, a2).subs({a1: boundary, a2: 0}) < 0)

# 例 6：由支持向量恢复分类器并预测。
w6 = sp.Matrix([R(1, 2), R(1, 2)])
b6 = -2
score6 = w6.dot(sp.Matrix([2, 3])) + b6
report("例6", b6 == 1 - w6.dot(sp.Matrix([3, 3]))
       and b6 == -1 - w6.dot(sp.Matrix([1, 1]))
       and score6 == R(1, 2) and 1 / sp.sqrt(w6.dot(w6)) == sp.sqrt(2))

# 例 7：两条直线的软间隔目标值比较。
xs7 = [sp.Matrix([3, 3]), sp.Matrix([4, 3]), sp.Matrix([1, 1]), sp.Matrix([R(7, 2), 3])]
ys7 = [1, 1, -1, -1]
wA, bA = sp.Matrix([R(1, 2), R(1, 2)]), -2
wB, bB = sp.Matrix([R(4, 13), R(7, 13)]), -R(24, 13)


def soft_value(wv, bv):
    zvals = [yi * (wv.dot(xv) + bv) for yi, xv in zip(ys7, xs7)]
    xis = [max(R(0), 1 - z) for z in zvals]
    return wv.dot(wv) / 2 + sum(xis), zvals, xis


vA, zA, xiA = soft_value(wA, bA)
vB, zB, xiB = soft_value(wB, bB)
report("例7", zA == [1, R(3, 2), 1, -R(5, 4)] and xiA == [0, 0, 0, R(9, 4)]
       and vA == R(5, 2) and zB == [R(9, 13), 1, 1, -R(11, 13)]
       and xiB == [R(4, 13), 0, 0, R(24, 13)] and vB == R(793, 338) and vB < vA)

# 完整检查软间隔的平稳、两组可行性及两组互补松弛。
alphas7 = [R(1), R(7, 26), R(7, 26), R(1)]
mus7 = [1-a for a in alphas7]
recovered7 = sum((a*y*x for a, y, x in zip(alphas7, ys7, xs7)), sp.zeros(2, 1))
report("例7-KKT", recovered7 == wB and sum(a*y for a, y in zip(alphas7, ys7)) == 0
       and all(a >= 0 and mu >= 0 and 1-a-mu == 0 for a, mu in zip(alphas7, mus7))
       and all(xi >= 0 and z-1+xi >= 0 for xi, z in zip(xiB, zB))
       and all(a*(z-1+xi) == 0 and mu*xi == 0
               for a, mu, z, xi in zip(alphas7, mus7, zB, xiB)))
dual7 = sum(alphas7)-recovered7.dot(recovered7)/2
report("例7-最优性证书", dual7 == vB == R(61, 26))

# 例 8：二次核的异或分类函数与核值。


def phi(x):
    return sp.Matrix([x[0] ** 2, sp.sqrt(2) * x[0] * x[1], x[1] ** 2])


kval = (sp.Matrix([2, 1]).dot(sp.Matrix([1, 3]))) ** 2
phi_val = phi(sp.Matrix([2, 1])).dot(phi(sp.Matrix([1, 3])))
x1s, x2s = sp.symbols("x1 x2")
classifier = sp.Rational(1, 8) * (2 * (x1s + x2s) ** 2 - 2 * (x1s - x2s) ** 2)
report("例8", kval == 25 and phi_val == 25 and sp.expand(classifier - x1s * x2s) == 0)

xs8 = [sp.Matrix(p) for p in [(1, 1), (-1, -1), (1, -1), (-1, 1)]]
ys8 = sp.Matrix([1, 1, -1, -1])
K8 = sp.Matrix(4, 4, lambda i, j: xs8[i].dot(xs8[j])**2)
Phi8 = sp.Matrix.hstack(*(phi(x) for x in xs8))
report("例8-核矩阵", K8 == sp.Matrix([[4, 4, 0, 0], [4, 4, 0, 0],
                                   [0, 0, 4, 4], [0, 0, 4, 4]])
       and K8 == Phi8.T*Phi8 and all(e >= 0 for e in K8.eigenvals()))
s, aa, cc = sp.symbols("s aa cc", real=True)
a8 = sp.Matrix([aa, s-aa, cc, s-cc])
weighted8 = a8.multiply_elementwise(ys8)
d8 = sp.expand(sum(a8)-(weighted8.T*K8*weighted8)[0]/2)
sstar = sp.solve(sp.diff(d8, s), s)[0]
report("例8-对偶最大值", d8 == 2*s-4*s*s and sstar == R(1, 4)
       and sp.diff(d8, s, 2) < 0 and d8.subs(s, sstar) == R(1, 4))
astar8 = a8.subs({s: sstar, aa: R(1, 8), cc: R(1, 8)})
weights8 = astar8.multiply_elementwise(ys8)
scores8 = K8*weights8
w8 = Phi8*weights8
report("例8-最优性证书", all(a >= 0 for a in astar8) and astar8.dot(ys8) == 0
       and scores8 == ys8 and w8.dot(w8)/2 == d8.subs(s, sstar))

# 四道引用块均有确定数值，不能标为 MANUAL。
distances = [abs(sum(x)-4)/sp.sqrt(2) for x in xs]
report("随堂1", distances == [sp.sqrt(2), 3/sp.sqrt(2), sp.sqrt(2)]
       and min(distances) == sp.sqrt(2))
xx, alpha = sp.symbols("xx alpha")
L = (xx-3)**2+alpha*(xx-1)
sol = sp.solve([sp.diff(L, xx), xx-1], [xx, alpha], dict=True)[0]
report("随堂2", sol == {xx: 1, alpha: 4} and sol[alpha] >= 0
       and sp.diff(L, xx, 2) > 0)
d = 2*alpha-2*alpha**2
astar = sp.solve(sp.diff(d, alpha), alpha)[0]
report("随堂3", astar == R(1, 2) and d.subs(alpha, astar) == R(1, 2)
       and sp.diff(d, alpha, 2) < 0)
report("随堂4", kval == phi_val == 25)
zs = [-1, 0, 1, 2]
report("损失表", [max(0, 1-z) for z in zs] == [2, 1, 0, 0]
       and [f"{float(sp.log(1+sp.exp(-z))):.4f}" for z in zs]
       == ["1.3133", "0.6931", "0.3133", "0.1269"])

