"""L.2 验算：讲义例题、随堂练习、全部题目与选择题的每个选项。每项独立重算后比对。"""
import sympy as sp

M = lambda *xs: sp.Matrix(xs)
R = sp.Rational


def report(tag, ok):
    print(f"{'PASS' if ok else 'FAIL'} {tag}")


def dot(a, b):
    return (a.T * b)[0]


def norm(a):
    return sp.sqrt(dot(a, a))


def cos(a, b):
    return sp.nsimplify(sp.simplify(dot(a, b) / (norm(a) * norm(b))))


def eq(x, y):
    return sp.simplify(sp.sympify(x) - sp.sympify(y)) == 0


def veq(a, b):
    return sp.simplify(a - b) == sp.zeros(*a.shape)


def proj(a, b):
    t = dot(a, b) / dot(a, a)
    return t, t * a, b - t * a


def foot(a, c, y):
    """点 y 到超平面 a^T x = c：返回 t、垂足、距离。"""
    t = (dot(a, y) - c) / dot(a, a)
    return t, y - t * a, sp.Abs(dot(a, y) - c) / norm(a)


def center(a):
    m = sum(a) / len(a)
    return a - m * sp.ones(len(a), 1)


u, v, w = M(5, 4, 1, 2), M(4, 5, 2, 1), M(1, 2, 5, 4)
one4 = sp.ones(4, 1)

# ---------- 讲义 ----------
report("讲义 第1节 ±1 投票", dot(M(1, 1, -1, 0), M(1, 0, -1, -1)) == 2)
report("讲义 例1 u·v=44, u·w=26, u·2v=88", (dot(u, v), dot(u, w), dot(u, 2 * v)) == (44, 26, 88))
report("讲义 例1 练习 v·w=28>26", dot(v, w) == 28 and dot(v, w) > dot(u, w))

x1, x2, x3, y1, y2, y3, z1, z2, z3, k = sp.symbols("x1 x2 x3 y1 y2 y3 z1 z2 z3 k", real=True)
A, B, C = M(x1, x2, x3), M(y1, y2, y3), M(z1, z2, z3)
laws = [dot(A, B) - dot(B, A), dot(A, B + C) - dot(A, B) - dot(A, C), dot(k * A, B) - k * dot(A, B)]
report("讲义 运算律（交换、分配、数乘）", all(sp.expand(e) == 0 for e in laws))
report("讲义 不能约去：(1,0)·(0,1)=(1,0)·(0,5)=0", dot(M(1, 0), M(0, 1)) == 0 == dot(M(1, 0), M(0, 5)))

# 例 2：构造满足 a·a=4, b·b=9, a·b=-1 的具体向量
a2, b2 = M(2, 0), M(R(-1, 2), sp.sqrt(R(35, 4)))
ok = (dot(a2, a2), dot(b2, b2), dot(a2, b2)) == (4, 9, -1)
report("讲义 例2 (2a-b)·(a+3b)=-24", ok and eq(dot(2 * a2 - b2, a2 + 3 * b2), -24))

report("讲义 余弦定理推导：|a-b|^2 展开", sp.expand(dot(A - B, A - B) - (dot(A, A) - 2 * dot(A, B) + dot(B, B))) == 0)
# 二维里 a·b = |a||b|cosθ（用极角直接验证）
r1, r2, p1, p2 = sp.symbols("r1 r2 p1 p2", positive=True)
Ap, Bp = M(r1 * sp.cos(p1), r1 * sp.sin(p1)), M(r2 * sp.cos(p2), r2 * sp.sin(p2))
report("讲义 二维 a·b=|a||b|cos(夹角)", sp.simplify(dot(Ap, Bp) - r1 * r2 * sp.cos(p1 - p2)) == 0)
report("讲义 |ka|=|k||a|", sp.simplify(norm(k * A) - sp.Abs(k) * norm(A)) == 0)

# 柯西–施瓦茨：图 LA1-5 的两条抛物线
t = sp.symbols("t", real=True)
f1 = sp.expand(dot(M(1, 2) + t * M(2, 1), M(1, 2) + t * M(2, 1)))
t1 = sp.solve(sp.diff(f1, t), t)[0]
f2 = sp.expand(dot(M(2, 4) + t * M(1, 2), M(2, 4) + t * M(1, 2)))
report("讲义 图LA1-5 不共线 f 最小 1.8 于 t=-0.8", t1 == R(-4, 5) and f1.subs(t, t1) == R(9, 5))
report("讲义 图LA1-5 共线 f(-2)=0、判别式=0", f2.subs(t, -2) == 0 and sp.discriminant(f2, t) == 0)
report("讲义 柯西–施瓦茨判别式 = 4[(a·b)^2-|a|^2|b|^2]",
       sp.expand(sp.discriminant(sp.expand(dot(A + t * B, A + t * B)), t) - 4 * (dot(A, B) ** 2 - dot(A, A) * dot(B, B))) == 0)
# 三角不等式：(|a|+|b|)^2-|a+b|^2 = 2(|a||b|-a·b) ≥ 0，用拉格朗日恒等式
lag = dot(A, A) * dot(B, B) - dot(A, B) ** 2 - ((x1 * y2 - x2 * y1) ** 2 + (x1 * y3 - x3 * y1) ** 2 + (x2 * y3 - x3 * y2) ** 2)
report("讲义 柯西–施瓦茨（拉格朗日恒等式独立核对）", sp.expand(lag) == 0)

a3, b3 = M(1, 2, 2, 4), M(2, 0, 1, 2)
report("讲义 例3 cos=4/5, |a-b|=√10",
       dot(a3, b3) == 12 and norm(a3) == 5 and norm(b3) == 3 and cos(a3, b3) == R(4, 5) and eq(norm(a3 - b3), sp.sqrt(10)))
report("讲义 例3 练习 夹角 π/3", sp.acos(cos(M(1, 1, 1, 1), M(1, 1, 1, -1))) == sp.pi / 3)

a4, b4 = M(2, 0), M(R(1, 2), sp.sqrt(3) / 2)
ok = norm(a4) == 2 and eq(norm(b4), 1) and eq(sp.acos(cos(a4, b4)), sp.pi / 3)
report("讲义 例4 a 与 a-b 夹角 π/6", ok and eq(sp.acos(cos(a4, a4 - b4)), sp.pi / 6))

# 例 5：代入消元后求驻点
yy, zz = sp.symbols("yy zz", real=True)
g = (9 - 2 * yy - 2 * zz) ** 2 + yy ** 2 + zz ** 2
st = sp.solve([sp.diff(g, yy), sp.diff(g, zz)], [yy, zz], dict=True)[0]
report("讲义 例5 最小值 9 于 (1,2,2)", st == {yy: 2, zz: 2} and g.subs(st) == 9 and 9 - 2 * 2 - 2 * 2 == 1)
th = sp.symbols("th", real=True)
h = 3 * 2 * sp.cos(th) - 4 * 2 * sp.sin(th)
crit = sp.solve(sp.diff(h, th), th)
vals = [sp.simplify(h.subs(th, c)) for c in crit]
pt = M(R(6, 5), R(-8, 5))
report("讲义 例5 练习 3x-4y 最大 10 于 (6/5,-8/5)",
       max(vals) == 10 and dot(pt, pt) == 4 and 3 * pt[0] - 4 * pt[1] == 10)

tt, pp, ee = proj(M(2, 1), M(1, 3))
report("讲义 例6 t=1, p=(2,1), e=(-1,2), 距离 √5",
       tt == 1 and pp == M(2, 1) and ee == M(-1, 2) and dot(ee, M(2, 1)) == 0 and eq(norm(ee), sp.sqrt(5)))
s_ = sp.symbols("s_", real=True)
dist2 = sp.expand(dot(M(1, 3) - s_ * M(2, 1), M(1, 3) - s_ * M(2, 1)))
report("讲义 例6 直线上最近点就是垂足（对 s 求最小）", sp.solve(sp.diff(dist2, s_), s_) == [1] and dist2.subs(s_, 2) > dist2.subs(s_, 1))
tt, pp, ee = proj(M(1, 2, 2), M(3, 3, 0))
report("讲义 例6 练习 t=1, e=(2,1,-2), 距离 3", tt == 1 and ee == M(2, 1, -2) and dot(ee, M(1, 2, 2)) == 0 and norm(ee) == 3)
tt, pp, ee = proj(M(1, 1, 1), M(3, 0, 3))
report("讲义 例7 (3,0,3) 投影 t=2=平均数, e=(1,-2,1)", tt == 2 == sp.Rational(6, 3) and ee == M(1, -2, 1) and sum(ee) == 0)
tt, pp, ee = proj(one4, u)
report("讲义 第5节 u 在 1 上投影 t=3，残差即 u'=(2,1,-2,-1)", tt == 3 and ee == M(2, 1, -2, -1))
t_a, p_a, _ = proj(M(2, 1), M(1, 3))
t_2a, p_2a, _ = proj(M(4, 2), M(1, 3))
sl = lambda a, b: dot(a, b) / norm(a)
report("讲义 对比 a→2a：t 减半，带符号长度和 p 不变",
       t_2a == t_a / 2 and veq(p_2a, p_a) and eq(sl(M(4, 2), M(1, 3)), sl(M(2, 1), M(1, 3))))

n3 = M(1, 2, 2)
report("讲义 第4节 (2,-1)⊥(1,2)；(-2,1,0),(-2,0,1)⊥(1,2,2) 且不共线",
       dot(M(1, 2), M(2, -1)) == 0 and dot(n3, M(-2, 1, 0)) == 0 and dot(n3, M(-2, 0, 1)) == 0
       and sp.Matrix.hstack(M(-2, 1, 0), M(-2, 0, 1)).rank() == 2)
tt, ff, dd = foot(M(1, 2), 5, M(4, 3))
dline = sp.expand(dot(M(4, 3) - M(5 - 2 * s_, s_), M(4, 3) - M(5 - 2 * s_, s_)))
smin = sp.solve(sp.diff(dline, s_), s_)[0]
report("讲义 例8 距离 √5，垂足 (3,1)（另用参数化求最小核对）",
       tt == 1 and ff == M(3, 1) and eq(dd, sp.sqrt(5)) and M(5 - 2 * smin, smin) == M(3, 1) and eq(sp.sqrt(dline.subs(s_, smin)), sp.sqrt(5)))
tt, ff, dd = foot(M(2, -1, 2), 3, M(1, 2, 3))
report("讲义 例8 练习 距离 1，垂足 (1/3,7/3,7/3)", tt == R(1, 3) and ff == M(R(1, 3), R(7, 3), R(7, 3)) and dd == 1 and dot(M(2, -1, 2), ff) == 3)

report("讲义 第5节 三人长度都是 √46", norm(u) == norm(v) == norm(w) == sp.sqrt(46))
report("讲义 第5节 直接余弦 44/46、26/46", cos(u, v) == R(44, 46) and cos(u, w) == R(26, 46))
report("讲义 第2/5节 v 换成 2v 余弦不变", cos(u, 2 * v) == cos(u, v))
report("讲义 第5节 w = 6·1 - u", w == 6 * one4 - u)
uc, vc, wc = center(u), center(v), center(w)
report("讲义 第5节 去均值 u',v',w'", uc == M(2, 1, -2, -1) and vc == M(1, 2, -1, -2) and wc == -uc)
report("讲义 第5节 去均值余弦 0.8、-1", cos(uc, vc) == R(4, 5) and cos(uc, wc) == -1)
zc = center(M(5, 5, 3, 3))
report("讲义 第5节 练习 (5,5,3,3) ±0.949",
       zc == M(1, 1, -1, -1) and abs(float(cos(zc, uc)) - 0.949) < 5e-4 and abs(float(cos(zc, wc)) + 0.949) < 5e-4)

# 第 1 节：点积没有结合律
a_, b_, c_ = M(1, 0), M(1, 1), M(0, 1)
report("讲义 第1节 (a·b)c ≠ a(b·c)", dot(a_, b_) * c_ != a_ * dot(b_, c_))
# 第 5 节 例 9：检索按余弦取 d1，按点积会取 d2，d3 与 q 正交
q9, d91, d92, d93 = M(1, 2, 2), M(2, 1, 2), M(8, -4, 8), M(2, -2, 1)
docs9 = [d91, d92, d93]
report("讲义 例9 长度 3、12、3，点积 8、16、0",
       [norm(x) for x in [q9] + docs9] == [3, 3, 12, 3] and [dot(q9, x) for x in docs9] == [8, 16, 0])
cos9 = [cos(q9, x) for x in docs9]
report("讲义 例9 余弦 8/9、4/9、0，按余弦取 d1，按点积取 d2",
       cos9 == [R(8, 9), R(4, 9), 0] and max(range(3), key=lambda i: cos9[i]) == 0
       and max(range(3), key=lambda i: dot(q9, docs9[i])) == 1)
report("讲义 例9 单位化后点积等于余弦", all(eq(dot(q9 / norm(q9), x / norm(x)), c) for x, c in zip(docs9, cos9)))
# 第 2 节：三角不等式的等号条件
tri_a = M(1, 2, 2)
report("讲义 第2节 三角不等式 同向取等、反向与正交严格",
       eq(norm(tri_a + 2 * tri_a), norm(tri_a) + norm(2 * tri_a))
       and bool(norm(tri_a - 2 * tri_a) < norm(tri_a) + norm(-2 * tri_a))
       and bool(norm(tri_a + M(2, -1, 0)) < norm(tri_a) + norm(M(2, -1, 0))))
# 第 4 节：t 的符号与所在一侧（例 8：(4,3) 在 a 所指一侧，原点在另一侧）
t_y, _, _ = foot(M(1, 2), 5, M(4, 3))
t_o, _, _ = foot(M(1, 2), 5, M(0, 0))
report("讲义 第4节 t 的符号：(4,3) 为正、原点为负", t_y > 0 and t_o < 0
       and dot(M(1, 2), M(4, 3)) > 5 and dot(M(1, 2), M(0, 0)) < 5)

# ---------- 题目 ----------
# L2-01
aa = M(1, 2)
def acute(kv):
    c = cos(aa, M(kv, 1))
    return bool(c > 0) and bool(c < 1)
samples = [R(n, 4) for n in range(-24, 25)] + [R(1, 2), -2, 2]
truth = {kv: acute(kv) for kv in samples}
opts = {"A": lambda q: q > -2, "B": lambda q: q >= -2, "C": lambda q: q > -2 and q != 2, "D": lambda q: q > -2 and q != R(1, 2)}
right = {o: all(bool(f(kv)) == truth[kv] for kv in samples) for o, f in opts.items()}
report("L2-01 选项A错（k=1/2 同向）", not right["A"] and cos(aa, M(R(1, 2), 1)) == 1)
report("L2-01 选项B错（k=-2 直角）", not right["B"] and cos(aa, M(-2, 1)) == 0)
report("L2-01 选项C错（k=2 是锐角，k=1/2 漏排）", not right["C"] and cos(aa, M(2, 1)) == R(4, 5) and 1 * 2 - 2 * 1 == 0)
report("L2-01 选项D对", right["D"])

# L2-02
kk = sp.symbols("kk", real=True)
v2a, v2b = M(kk, 0, 1), M(1, 1, 0)
sol = sp.solve(sp.Eq(dot(v2a, v2b) / (norm(v2a) * norm(v2b)), -R(1, 2)), kk)
sq = sp.solve(sp.Eq(dot(v2a, v2b) ** 2 * 4, dot(v2a, v2a) * dot(v2b, v2b)), kk)
report("L2-02 k=-1（平方后 ±1，k=1 是 π/3 要舍）",
       sol == [-1] and sorted(sq) == [-1, 1]
       and sp.acos(cos(M(-1, 0, 1), v2b)) == 2 * sp.pi / 3 and sp.acos(cos(M(1, 0, 1), v2b)) == sp.pi / 3)

# L2-03
xx = sp.symbols("xx", real=True)
xs = sp.solve(sp.Eq(dot(one4[:3, :], M(xx, 2, 3)) / 3, 2), xx)
tt, pp, ee = proj(M(1, 1, 1), M(xs[0], 2, 3))
report("L2-03 x=1, e=(-1,0,1), t=平均数", xs == [1] and pp == M(2, 2, 2) and ee == M(-1, 0, 1) and tt == sum(M(1, 2, 3)) / 3)

# L2-04：a 换成 -2a，符号向量逐项比较
t_old, p_old, e_old = proj(A, B)
t_new, p_new, e_new = proj(-2 * A, B)
ell = lambda a, b: dot(a, b) / norm(a)
report("L2-04 选项A错：新系数是 -t/2 不是 -2t", eq(t_new, -t_old / 2) and not eq(t_new, -2 * t_old))
report("L2-04 选项B错：投影不是 -2p", veq(p_new, p_old) and not veq(p_new, -2 * p_old))
report("L2-04 选项C错：带符号长度变号", eq(ell(-2 * A, B), -ell(A, B)) and not eq(ell(-2 * A, B), ell(A, B)))
report("L2-04 选项D对：投影和残差都不变", veq(p_new, p_old) and veq(e_new, e_old))
# 数值再核一次
a4n, b4n = M(1, 2, 2), M(3, 3, 0)
report("L2-04 数值核对 a=(1,2,2), b=(3,3,0)",
       proj(-2 * a4n, b4n)[0] == -R(1, 2) and proj(-2 * a4n, b4n)[1] == proj(a4n, b4n)[1] and ell(-2 * a4n, b4n) == -3)

q = M(4, 4, 4, 4)
report("L2-05 直接余弦 6/√46 ≈0.885（与三人相同）",
       eq(cos(q, u), 6 / sp.sqrt(46)) and cos(q, v) == cos(q, u) == cos(q, w) and abs(float(cos(q, u)) - 0.885) < 5e-4)
report("L2-05 去均值后是零向量", center(q) == sp.zeros(4, 1))

ab = sp.symbols("ab", real=True)
abv = sp.solve(sp.Eq(9 + 2 * ab + 16, 37), ab)[0]
a6, b6 = M(3, 0), M(2, 2 * sp.sqrt(3))
ok = norm(a6) == 3 and norm(b6) == 4 and eq(norm(a6 + b6), sp.sqrt(37)) and dot(a6, b6) == abv == 6
report("L2-06(1) a·b=6, |a-b|=√13, 夹角 π/3", ok and eq(norm(a6 - b6), sp.sqrt(13)) and eq(sp.acos(cos(a6, b6)), sp.pi / 3))
f6 = sp.expand(dot(a6 + t * b6, a6 + t * b6))
t6 = sp.solve(sp.diff(f6, t), t)[0]
report("L2-06(2) t=-3/8，最小值 3√3/2，此时与 b 正交",
       t6 == R(-3, 8) and eq(sp.sqrt(f6.subs(t, t6)), 3 * sp.sqrt(3) / 2) and eq(dot(a6 + t6 * b6, b6), 0)
       and eq(f6, 16 * t ** 2 + 12 * t + 9))

h7 = 6 * sp.cos(th) - 4 * sp.sin(th)
report("L2-07 椭圆参数化后 3x-4y 单调减", sp.simplify(sp.diff(h7, th) + 6 * sp.sin(th) + 4 * sp.cos(th)) == 0)
grid = [h7.subs(th, sp.pi / 3 * i / 200) for i in range(201)]
report("L2-07 可行弧最大 6 于 (2,0)，最小 3-2√3 于 (1,√3/2)", h7.subs(th, 0) == 6 and h7.subs(th, sp.pi / 3) == 3 - 2 * sp.sqrt(3)
       and max(float(z) for z in grid) <= 6 + 1e-12 and min(float(z) for z in grid) >= float(3 - 2 * sp.sqrt(3)) - 1e-12)
tq = sp.symbols("tq", real=True)
eqpts = [tv * M(3, -2) for tv in sp.solve(sp.Eq(dot(tq * M(3, -2), tq * M(3, -2)), 4), tq)]
vals7 = {tuple(pq): 3 * pq[0] - 2 * pq[1] for pq in eqpts}
report("L2-07 柯西等号点均不满足 x≥1,y≥0",
       len(eqpts) == 2 and all(pq[0] < 1 or pq[1] < 0 for pq in eqpts))


# L2-08
report("L2-08 选项C对：|a+b|^2-|a-b|^2=4a·b", sp.expand(dot(A + B, A + B) - dot(A - B, A - B) - 4 * dot(A, B)) == 0)
report("L2-08 选项A反例", dot(M(1, 0), M(0, 1)) == 0 and dot(M(0, 1), M(1, 0)) == 0 and dot(M(1, 0), M(1, 0)) == 1)
a8b, b8b, c8b = M(1, 0), M(0, 1), M(0, 5)
report("L2-08 选项B反例：b-c=(0,-4) 与 a 正交、不共线",
       dot(a8b, b8b) == dot(a8b, c8b) and b8b - c8b == M(0, -4) and sp.Matrix.hstack(a8b, b8b - c8b).rank() == 2)
a8 = M(1, 2, 3)
report("L2-08 选项D反例 b=-2a 取等但反向",
       eq(sp.Abs(dot(a8, -2 * a8)), norm(a8) * norm(-2 * a8)) and dot(a8, -2 * a8) == -2 * dot(a8, a8) and cos(a8, -2 * a8) == -1)

# L2-09
r_, s9, h9 = M(4, 3, 4, 5), M(2, 1, 4, 5), M(5, 4, 3, 4)
c_rs, c_rh = cos(r_, s9), cos(r_, h9)
report("L2-09(1) 直接余弦 0.944 < 0.970，选小何",
       dot(r_, s9) == 52 and dot(r_, h9) == 64 and abs(float(c_rs) - 0.944) < 5e-4 and c_rh == R(64, 66) and c_rh > c_rs
       and dot(r_, r_) * dot(s9, s9) == 3036)
rc, sc, hc = center(r_), center(s9), center(h9)
report("L2-09(2) 去均值余弦 0.894 与 0，选小孙",
       rc == M(0, -1, 0, 1) and sc == M(-1, -2, 1, 2) and hc == M(1, 0, -1, 0)
       and eq(cos(rc, sc), 2 / sp.sqrt(5)) and cos(rc, hc) == 0)
mr, ms, mh = sum(r_) / 4, sum(s9) / 4, sum(h9) / 4
report("L2-09(3) 点积分解 64=64+0，52=48+4",
       dot(r_, h9) == mr * mh * 4 + dot(rc, hc) and dot(r_, s9) == mr * ms * 4 + dot(rc, sc)
       and mr * mh * 4 == 64 and mr * ms * 4 == 48 and dot(rc, hc) == 0 and dot(rc, sc) == 4)
report("L2-09(3) 长度平方分解 66=64+2，66=64+2，46=36+10",
       [(m * m * 4, dot(x, x)) for m, x in ((mr, rc), (mh, hc), (ms, sc))] == [(64, 2), (64, 2), (36, 10)]
       and dot(r_, r_) == 66 and dot(h9, h9) == 66 and dot(s9, s9) == 46)

# L2-10
n10, P10, R10 = M(1, 1, 1), M(3, 0, 3), M(0, 3, 3)
report("L2-10(1) P、R 同侧（3 和 3）", dot(n10, P10) - 3 == 3 and dot(n10, R10) - 3 == 3)
report("L2-10 直线 PR 与 π 平行", dot(n10, R10 - P10) == 0 and R10 - P10 == M(-3, 3, 0))
tt, F10, d10 = foot(n10, 3, P10)
Ps = 2 * F10 - P10
report("L2-10(2) F=(2,-1,2)，P*=(1,-2,1) 在另一侧",
       tt == 1 and F10 == M(2, -1, 2) and dot(n10, F10) == 3 and Ps == M(1, -2, 1) and dot(n10, Ps) - 3 == -3)
X1, X2 = sp.symbols("X1 X2", real=True)
Xp = M(X1, X2, 3 - X1 - X2)
report("L2-10(2) π 上任一点 |x-P|^2=|x-P*|^2（恒等式）", sp.expand(dot(Xp - P10, Xp - P10) - dot(Xp - Ps, Xp - Ps)) == 0)
report("L2-10(2) 证明中的正交：n·(x-F)=0，F-P=-n", sp.expand(dot(n10, Xp - F10)) == 0 and F10 - P10 == -n10)
print("MANUAL L2-10(2) 证明书写")
sv = sp.symbols("sv", real=True)
seg_pt = Ps + sv * (R10 - Ps)
s_hit = sp.solve(sp.Eq(dot(n10, seg_pt), 3), sv)[0]
X_opt = seg_pt.subs(sv, s_hit)
fsum = lambda X: norm(X - P10) + norm(X - R10)
report("L2-10(3) 交点 s=1/2，(1/2,1/2,2)，最小值 √30",
       s_hit == R(1, 2) and X_opt == M(R(1, 2), R(1, 2), 2) and eq(norm(R10 - Ps), sp.sqrt(30)) and eq(fsum(X_opt), sp.sqrt(30)))
import itertools, math
best = min((float(fsum(M(R(i, 4), R(j, 4), 3 - R(i, 4) - R(j, 4)))), i, j)
           for i, j in itertools.product(range(-8, 13), range(-8, 13)))
report("L2-10(3) 平面网格搜索最小值 ≥ √30 且在 (1/2,1/2) 处取到",
       best[0] >= math.sqrt(30) - 1e-12 and (best[1], best[2]) == (2, 2))

# L2-11
q11, d1, d2, d3 = M(1, 1, 0, 0), M(4, 0, 0, 0), M(1, 1, 1, 0), M(3, 3, 0, 0)
docs = {"d1": d1, "d2": d2, "d3": d3}
by_dot = sorted(docs, key=lambda n: -dot(q11, docs[n]))
by_cos = sorted(docs, key=lambda n: -float(cos(q11, docs[n])))
report("L2-11(1) 点积排序 d3>d1>d2", by_dot == ["d3", "d1", "d2"] and [dot(q11, docs[n]) for n in by_dot] == [6, 4, 2])
report("L2-11(1) 余弦排序 d3>d2>d1，余弦 0.707、0.816、1",
       by_cos == ["d3", "d2", "d1"] and cos(q11, d3) == 1 and abs(float(cos(q11, d1)) - 0.707) < 5e-4
       and abs(float(cos(q11, d2)) - 0.816) < 5e-4)
Q4, D4 = M(*sp.symbols("q1:5", real=True)), M(*sp.symbols("e1:5", real=True))
report("L2-11(2) |q-d|^2 = |q|^2+|d|^2-2|q||d|cosθ（cosθ 按定义代入）",
       sp.simplify(dot(Q4 - D4, Q4 - D4) - (dot(Q4, Q4) + dot(D4, D4) - 2 * norm(Q4) * norm(D4) * (dot(Q4, D4) / (norm(Q4) * norm(D4))))) == 0)
print("MANUAL L2-11(2) 证明书写")
unit = lambda x: x / norm(x)
d_unit = {n: sp.nsimplify(sp.simplify(dot(q11 - unit(x), q11 - unit(x)))) for n, x in docs.items()}
by_ud = sorted(docs, key=lambda n: float(d_unit[n]))
report("L2-11(3) 只单位化文档：距离平方 1、3-4/√3≈0.691、3-2√2≈0.172",
       eq(d_unit["d1"], 1) and eq(d_unit["d2"], 3 - 4 / sp.sqrt(3)) and eq(d_unit["d3"], 3 - 2 * sp.sqrt(2))
       and abs(float(d_unit["d2"]) - 0.691) < 5e-4 and abs(float(d_unit["d3"]) - 0.172) < 5e-4)
report("L2-11(3) 只单位化文档：距离排序与余弦排序一致", by_ud == by_cos)
report("L2-11(3) 距离平方 = 3-2√2 cosθ", all(eq(d_unit[n], 3 - 2 * sp.sqrt(2) * cos(q11, docs[n])) for n in docs))
d_raw = {n: dot(q11 - x, q11 - x) for n, x in docs.items()}
by_raw = sorted(docs, key=lambda n: d_raw[n])
report("L2-11(3) 不单位化距离平方 10,1,8，排序 d2,d3,d1 与余弦不一致",
       (d_raw["d1"], d_raw["d2"], d_raw["d3"]) == (10, 1, 8) and by_raw == ["d2", "d3", "d1"] and by_raw != by_cos)
# 一般命题：文档长度相同时，固定查询下距离排序与余弦排序一致；查询长度只改变公共项和正比例系数
L = sp.symbols("L", positive=True)
Qnorm = sp.symbols("Qnorm", positive=True)
C1, C2 = sp.symbols("C1 C2", real=True)
expr_same = (Qnorm**2 + L**2 - 2*Qnorm*L*C1) - (Qnorm**2 + L**2 - 2*Qnorm*L*C2)
report("L2-11(3) 一般命题：文档等长时距离差与余弦差反号", sp.factor(expr_same) == -2*Qnorm*L*(C1-C2))

# L2-12（取 n=5 的符号向量）
bs = sp.symbols("b1:6", real=True)
bv, one5 = M(*bs), sp.ones(5, 1)
bbar = sum(bs) / 5
dev2 = sum((bi - bbar) ** 2 for bi in bs)
report("L2-12(1) n|b|^2-(Σb)^2 = Σ_{i<j}(bi-bj)^2 ≥ 0，为 0 当且仅当全相等",
       sp.expand(5 * dot(bv, bv) - dot(one5, bv) ** 2 - sum((bs[i] - bs[j]) ** 2 for i in range(5) for j in range(i + 1, 5))) == 0)
tb, pb, eb = proj(one5, bv)
report("L2-12(2) 投影系数=平均数，|b|^2-n·b̄^2 = 残差平方 = 离差平方和",
       eq(tb, bbar) and dot(eb, one5) == 0 and sp.expand(dot(bv, bv) - 5 * bbar ** 2 - dev2) == 0 and sp.expand(dot(eb, eb) - dev2) == 0)
cs = sp.symbols("c1:5", real=True)
lam = sp.symbols("lam", real=True)
Lg = sum(ci ** 2 for ci in cs) - lam * (sum(cs) - 1)
crit12 = sp.solve([sp.diff(Lg, ci) for ci in cs] + [sum(cs) - 1], list(cs) + [lam], dict=True)
report("L2-12(3) n=4 时和为 1 下平方和最小 1/4，于 c_i=1/4",
       len(crit12) == 1 and all(crit12[0][ci] == R(1, 4) for ci in cs) and sum(crit12[0][ci] ** 2 for ci in cs) == R(1, 4))
report("L2-12(3) 不用非负：(2,-1) 平方和 5 ≥ 1/2", 2 + (-1) == 1 and 2 ** 2 + (-1) ** 2 == 5 and 5 >= R(1, 2))
print("MANUAL L2-12 证明书写（等号条件、两种证法的关系）")

# L2-13
a1_, a2_ = M(1, 0, 1), M(0, 1, 1)
c1, c2 = sp.symbols("c1 c2", real=True)
bsym = M(*sp.symbols("w1:4", real=True))
expr = dot(bsym, c1 * a1_ + c2 * a2_) - (c1 * dot(bsym, a1_) + c2 * dot(bsym, a2_))
report("L2-13(1) 分配律恒等式", sp.expand(expr) == 0)
bin_ = c1 * a1_ + c2 * a2_
report("L2-13(1) 张成中与 a1、a2 都正交的只有 0",
       sp.solve([dot(bin_, a1_), dot(bin_, a2_)], [c1, c2], dict=True) == [{c1: 0, c2: 0}])
print("MANUAL L2-13(1) 证明书写")
b13 = M(1, -1, 0)
report("L2-13(2) 反例 b=(1,-1,0)", dot(b13, a1_ + a2_) == 0 and dot(b13, a1_) == 1 and a1_ + a2_ == M(1, 1, 2))
ns = sp.Matrix.hstack(a1_, a2_).T.nullspace()
n13 = M(1, 1, -1)
report("L2-13(3) 法向量 (1,1,-1)", len(ns) == 1 and sp.Matrix.hstack(ns[0], n13).rank() == 1 and dot(n13, a1_) == 0 == dot(n13, a2_))
pl = sp.Matrix([[1, 1, -1]]).nullspace()
report("L2-13(3) x+y-z=0 的解集 = span(a1,a2)",
       sp.Matrix.hstack(*pl).rank() == 2 and sp.Matrix.hstack(*pl, a1_, a2_).rank() == 2)
y13 = M(2, 3, 4)
report("L2-13(3) (2,3,4) 代入得 1≠0，不在张成里（与 L.1 例 3 一致）",
       dot(n13, y13) == 1 and sp.Matrix.hstack(a1_, a2_, y13).rank() == 3)

P1, P2 = M(40, 10), M(10, 40)
a14 = M(1, 1)
report("L2-14(1) 直线 x+y=50", dot(a14, P2 - P1) == 0 and dot(a14, P1) == 50 == dot(a14, P2))
def nearest_on_segment(gv):
    sv = sp.symbols("sv", real=True)
    X = P1 + sv * (P2 - P1)
    d2 = sp.expand(dot(gv - X, gv - X))
    s_star = sp.solve(sp.diff(d2, sv), sv)[0]
    s_opt = min(max(s_star, 0), 1)
    return s_star, s_opt, sp.sqrt(d2.subs(sv, s_opt))
s_star, s_opt, dmin = nearest_on_segment(M(35, 35))
tt, F14, d14 = foot(a14, 50, M(35, 35))
report("L2-14(2) 垂足 (25,25)，s=1/2，距离 10√2", F14 == M(25, 25) and s_star == s_opt == R(1, 2) and eq(dmin, 10 * sp.sqrt(2)) and eq(d14, dmin))
s_star, s_opt, dmin = nearest_on_segment(M(55, 15))
tt, F14, d14 = foot(a14, 50, M(55, 15))
report("L2-14(3) 垂足 (45,5) 在线段外 s=-1/6，最近为 p1，距离 5√10",
       F14 == M(45, 5) and s_star == R(-1, 6) and s_opt == 0 and eq(dmin, 5 * sp.sqrt(10))
       and eq(dmin ** 2, d14 ** 2 + dot(F14 - P1, F14 - P1)) and d14 ** 2 == 200)
