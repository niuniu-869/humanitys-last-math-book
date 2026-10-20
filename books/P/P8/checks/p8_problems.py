"""Recompute each exercise from its distribution, then compare with answers.md.

Expected values below are answer keys, never substitutes for computation.
Visible-answer anchors also detect drift between this key and the book.
Only P8-06 is a proof requiring manual review. No random simulation is used
as evidence of a limit or a universal inequality.
"""
from pathlib import Path
import re
import sys

import numpy as np
import sympy as s

ROOT = Path(__file__).resolve().parents[1]
ANS = (ROOT / "answers.md").read_text(encoding="utf-8")
PROBS = (ROOT / "problems.md").read_text(encoding="utf-8")
BLOCKS = dict(re.findall(
    r"\*\*(P8-\d+)\*\*\n(.*?)(?=\n\*\*P8-|\Z)", ANS, re.S))
R = s.Rational
n = s.symbols("n", integer=True, positive=True)
x = s.symbols("x", real=True)
failures = 0


def check(pid, label, condition, anchors=()):
    global failures
    ok = bool(condition) and all(t in BLOCKS[pid] for t in anchors)
    print(f"{'PASS' if ok else 'FAIL'} {pid} {label}")
    failures += not ok


def eq(a, b):
    return s.simplify(a - b) == 0


def moments(values, probs):
    assert eq(sum(probs), 1)
    mu = sum(v * p for v, p in zip(values, probs))
    var = sum((v - mu)**2 * p for v, p in zip(values, probs))
    return s.simplify(mu), s.simplify(var)


def choice(pid, truth):
    selected = re.search(r"\*\*答案：\*\* \(([A-D])\)", BLOCKS[pid])[1]
    for letter, actual in zip("ABCD", truth):
        check(pid, f"选项 {letter}", bool(actual) == (letter == selected))


def phi(z):
    return (1 + s.erf(s.sympify(z) / s.sqrt(2))) / 2


def rounded(z, value, places=4):
    return abs(float(z) - value) <= 0.5 * 10**(-places) + 1e-12


# 01: two admissible laws refute the three unjustified claims.
values = [0, 8]
probs = [R(3, 4), R(1, 4)]
mu, _ = moments(values, probs)
tail = sum(p for v, p in zip(values, probs) if v >= 8)
constant_tail = s.Integer(2 >= 8)
bound = mu / 8
check("P8-01", "反例满足均值条件", eq(mu, 2), ("1/4", "1/8"))
choice("P8-01", [eq(constant_tail, R(1, 4)), bound <= R(1, 4),
                  constant_tail >= R(1, 4), tail <= R(1, 8)])

# 02: recover the radius from both endpoints, not from interval length.
radius = min(-1 - (-7), 5 - (-1))
lower = 1 - R(9, radius**2)
check("P8-02", "补事件下界", eq(lower, R(3, 4)), (r"\frac34",))

# 03: compute all four means and variances by affine transformation.
mu_s, var_s = 36 * 2, 36 * 9
mu_bar, var_bar = R(mu_s, 36), R(var_s, 36**2)
transforms = [(mu_s, var_s, 2, 18), (mu_s, var_s, 72, 324),
              (mu_bar, var_bar, 2, 18), (mu_bar, var_bar, 2, R(1, 2))]
transformed = [(s.cancel((s.sympify(m) - c) / d), s.cancel(s.sympify(v) / d**2))
               for m, v, c, d in transforms]
choice("P8-03", [eq(m, 0) and eq(v, 1) for m, v in transformed])
check("P8-03", "错误选项的矩", transformed[:3] ==
      [(R(35, 9), 1), (0, R(1, 324)), (0, R(1, 1296))],
      ("35/9", "1/324", "1/1296"))

# 04: enumerate the strict integer event before expanding its boundary.
included = [k for k in range(201) if 76 < k < 85]
mu, var = 200 * R(2, 5), 200 * R(2, 5) * R(3, 5)
zlo = (min(included) - R(1, 2) - mu) / s.sqrt(var)
zhi = (max(included) + R(1, 2) - mu) / s.sqrt(var)
check("P8-04", "区间和两个标准化端点",
      (min(included), max(included)) == (77, 84)
      and eq(zlo, -R(7, 2)/s.sqrt(48))
      and eq(zhi, R(9, 2)/s.sqrt(48)),
      (r"\Phi(4.5/\sqrt{48})-\Phi(-3.5/\sqrt{48})", "76.5,84.5"))

# 05: exact tail functions suffice for every epsilon, including epsilon>1.
vals = [-1, 0, 1]
yp = [1/(2*n), 1-1/n, 1/(2*n)]
wp = [R(1, 2), 0, R(1, 2)]
ym, yv = moments(vals, yp)
wm, wv = moments(vals, wp)
ytail = sum(p for v, p in zip(vals, yp) if abs(v) >= R(1, 2))
wtail = sum(p for v, p in zip(vals, wp) if abs(v) >= R(1, 2))
yconv = eq(s.limit(ytail, n, s.oo), 0)
wconv = eq(s.limit(wtail, n, s.oo), 0)
scaled_second = s.simplify(n * (yv + ym**2))
choice("P8-05", [yconv and wconv, not yconv, yconv and not wconv,
                  eq(s.limit(scaled_second, n, s.oo), 0)])
check("P8-05", "期望及放大后的二阶矩",
      eq(ym, 0) and eq(wm, 0) and eq(scaled_second, 1),
      ("E(Y_n^2)=1/n", r"E[(\sqrt nY_n)^2]=1"))

print("MANUAL P8-06 逐行检查均值漂移、方差相加、事件包含和任意 epsilon")

# 07: integrals decide which theorem has finite moments available.
density = 2/x**3
mass = s.integrate(density, (x, 1, s.oo))
mu = s.integrate(x*density, (x, 1, s.oo))
second = s.integrate(x*x*density, (x, 1, s.oo))
check("P8-07", "矩与定理条件", eq(mass, 1) and eq(mu, 2)
      and second == s.oo and mu.is_finite and not second.is_finite,
      ("E(X_1)=2", r"E(X_1^2)=+\infty", "不能使用本章方法 5", "依概率收敛到 2"))

# 08: derive the two bounds, then verify the whole counterexample law.
mu, second = s.Integer(1), s.Integer(3)
bounds = [mu/4, (second-mu**2)/(4-mu)**2]
cm, cv = moments([0, 3], [R(2, 3), R(1, 3)])
ctail = sum(p for v, p in zip([0, 3], [R(2, 3), R(1, 3)]) if v >= 4)
check("P8-08", "两个上界及反例", bounds == [R(1, 4), R(2, 9)]
      and min(bounds) == R(2, 9) and eq(cm, mu)
      and eq(cv+cm**2, second) and eq(ctail, 0),
      ("1/4", "2/9", "P(X=0)=2/3", "P(X=3)=1/3"))

# 09: integrate the transformed variable, compare to a Bernoulli indicator.
am = s.integrate(x**2, (x, 0, 1))
av = s.integrate(x**4, (x, 0, 1))-am**2
bm = s.integrate(1, (x, 0, R(1, 3)))
bv = bm*(1-bm)
sizes = [s.ceiling(v/R(1, 100)**2) for v in (av, bv)]
check("P8-09", "两个估计量的矩与极限", eq(am, R(1, 3))
      and eq(bm, am) and eq(av, R(4, 45)) and eq(bv, R(2, 9))
      and all(eq(s.limit(v/n, n, s.oo), 0) for v in (av, bv)),
      ("4/(45n)", "2/(9n)", "依概率极限都为 $1/3$"))
check("P8-09", "两个最小样本数", sizes == [889, 2223]
      and all(v/m <= R(1, 10000) < v/(m-1)
              for v, m in zip((av, bv), sizes)), ("889", "2223"))

# 10: exact support, exact moments, normal approximation and integer search.
mu, var = moments([-1, 0, 1], [R(1, 4), R(1, 2), R(1, 4)])
var_s = 80*var
probability = lambda k: 2*phi((R(k)+R(1, 2))/s.sqrt(var_s))-1
k = next(j for j in range(81) if float(probability(j)) >= .95)
check("P8-10", "最小阈值与边界概率", eq(mu, 0) and eq(var_s, 40)
      and k == 12 and rounded(probability(k), .9519)
      and rounded(probability(k-1), .9310), ("k=12", "0.9519,0.9310", "不是严格保证"))

# 11: solve for probabilities, then sum the masses of each event.
k = s.symbols("k", positive=True)
a, b, c = s.symbols("a b c", real=True)
sol = s.solve([a+b+c-1, -k*a+k*c, k*k*(a+c)-1], (a, b, c))
t = s.symbols("t", positive=True)
valid = all(s.factor(v.subs(k, 1+t)).is_positive for v in sol.values())
check("P8-11", "三点分布", valid and eq(sum(sol.values()), 1)
      and eq(sol[a], 1/(2*k**2)) and eq(sol[c], sol[a])
      and eq(sol[b], 1-1/k**2), ("a=c=1/(2k^2)", "b=1-1/k^2"))
events = [sum(sol[p] for v, p in [(-k, a), (0, b), (k, c)] if pred(abs(v)))
          for pred in [lambda v: v >= k, lambda v: v > k, lambda v: v < k]]
check("P8-11", "三个事件与上界取等", all(eq(u, v) for u, v in
      zip(events, [1/k**2, 0, 1-1/k**2]))
      and eq(events[0], (sol[a]*k*k+sol[c]*k*k)/k**2),
      ("1/k^2,0,1-1/k^2", "不能把统一上界减小"))

# 12: integrate exponential moments and condition on the two possible sizes.
mu = s.integrate(x*s.exp(-x), (x, 0, s.oo))
var = s.integrate(x*x*s.exp(-x), (x, 0, s.oo))-mu**2
sizes, weights = [100, 400], [R(1, 2), R(1, 2)]
mean_t = sum(w*mu for w in weights)
second_t = sum(w*(mu**2+var/m) for m, w in zip(sizes, weights))
var_t = second_t-mean_t**2
mean_n = sum(w*m for m, w in zip(sizes, weights))
approx = sum(w*(2*phi(R(1, 10)/s.sqrt(var/m))-1)
             for m, w in zip(sizes, weights))
check("P8-12", "全期望与条件近似", eq(mean_t, 1) and eq(var_t, R(1, 160))
      and eq(mean_n, 250) and eq(var/mean_n, R(1, 250))
      and var_t != var/mean_n and rounded(approx, .8186),
      ("E(T)=1", "1/160", "1/250", "0.8186"))

# 13: derive the success probability from the continuous density.
p = s.integrate(2*x, (x, 0, R(1, 2)))
included = [j for j in range(401) if abs(R(j, 400)-R(1, 4)) < R(1, 20)]
mu, var = 400*p, 400*p*(1-p)
zlo = (min(included)-R(1, 2)-mu)/s.sqrt(var)
zhi = (max(included)+R(1, 2)-mu)/s.sqrt(var)
approx = phi(zhi)-phi(zlo)
check("P8-13", "密度到二项事件", eq(p, R(1, 4)) and eq(mu/400, p)
      and (min(included), max(included)) == (81, 119)
      and eq(zhi, R(39, 2)/s.sqrt(75)) and eq(zlo, -zhi)
      and rounded(approx, .9757), ("E(F)=1/4", "80.5,119.5", "0.9757"))

# 14: enumerate the joint law; do not infer independence from covariance.
us, ps = [-1, 0, 1], [R(1, 3)]*3
vs = [u*u for u in us]
um, uv = moments(us, ps)
vm, vv = moments(vs, ps)
cov = sum(p*u*v for p, u, v in zip(ps, us, vs))-um*vm
joint = sum(p for u, v, p in zip(us, vs, ps) if u == 0 and v == 0)
product = sum(p for u, p in zip(us, ps) if u == 0)*sum(
    p for v, p in zip(vs, ps) if v == 0)
zm, zv = moments([u+v for u, v in zip(us, vs)], ps)
needed = s.ceiling(zv/(R(1, 10)**2*R(1, 20)))
check("P8-14", "协方差、非独立与平均的矩", eq(cov, 0)
      and eq(joint, R(1, 3)) and eq(product, R(1, 9)) and joint != product
      and eq(zm, R(2, 3)) and eq(zv, R(8, 9))
      and eq(zv, uv+vv+2*cov), ("协方差为 0", "不独立", "8/(9n)"))
check("P8-14", "保证次数及前一整数", needed == 1778
      and zv/(needed*R(1, 100)) <= R(1, 20)
      and zv/((needed-1)*R(1, 100)) > R(1, 20), ("1778",))

# 15: compute binomial terms first; form the conditional ratio afterwards.
trials, p = 2000, R(1, 2000)
q = 1-p
p0, p1 = q**trials, s.binomial(trials, 1)*p*q**(trials-1)
exact = s.cancel(p0/(p0+p1))
lam = trials*p
pois0, pois1 = s.exp(-lam), lam*s.exp(-lam)
check("P8-15", "精确比值与泊松比值", eq(exact, R(1999, 3999))
      and eq(pois0/(pois0+pois1), R(1, 2)) and lam < 10,
      ("1999/3999", "1/2", "不足以优先使用正态近似"))

# 16: a block of copied errors has every covariance equal to 9.
copies = 4
block_cov = np.full((copies, copies), 9, dtype=np.int64)
block_sum_var = s.Integer(block_cov.sum())
copy_mean_var = s.cancel(n*block_sum_var/(copies*n)**2)
fresh_mean_var = s.cancel(copies*n*9/(copies*n)**2)
bound_copy = s.simplify(copy_mean_var/R(3, 10)**2)
bound_fresh = s.simplify(fresh_mean_var/R(3, 10)**2)
need_copy = s.ceiling(s.solve(s.Eq(bound_copy, R(1, 20)), n)[0])
need_fresh = s.ceiling(s.solve(s.Eq(bound_fresh, R(1, 20)), n)[0])
check("P8-16", "复制与独立新增的方差、次数", eq(copy_mean_var, 9/n)
      and eq(fresh_mean_var, 9/(4*n)) and need_copy == 2000 and need_fresh == 500
      and bound_copy.subs(n, need_copy-1) > R(1, 20)
      and bound_fresh.subs(n, need_fresh-1) > R(1, 20),
      ("9/n", "2000", "500", "9/(4n)"))

# Editorial invariants: numbered answers, limits including all math, vocabulary.
ids = re.findall(r"^\*\*(P8-\d+)\*\*〔", PROBS, re.M)
tiers = dict(re.findall(r"^\*\*(P8-\d+)\*\*〔([ABC])", PROBS, re.M))
limits = {"A": 400, "B": 900, "C": 1400}
bad_words = r"高中|初中|中学课本|备考|考研|数学一|真题|考纲|应试|常考|考试要求"
for pid in ids:
    body = BLOCKS[pid].split("\n### ")[0].strip()
    check(pid, f"答案格式及字符数 {len(body)}", body.startswith("**答案：**")
          and body.splitlines()[-1].startswith("区分点：")
          and len(body) <= limits[tiers[pid]] and not re.search(bad_words, body))
ok = (ids == [f"P8-{j:02d}" for j in range(1, 17)]
      and set(BLOCKS) == set(ids) and not re.search(bad_words, PROBS))
print(f"{'PASS' if ok else 'FAIL'} P8-format 编号、题答对应及禁用口径")
failures += not ok
sys.exit(bool(failures))
