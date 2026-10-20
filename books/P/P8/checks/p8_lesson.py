"""Independent numeric/symbolic audit of all 16 lesson examples.

Binomial probabilities are summed from their PMF; exponential-sum tails
use the finite Erlang series. Simulations reproduce the author's seeds,
but limits and conclusions are checked symbolically, not by simulation.
The negative-axis remark is checked against its exact value: the normal
approximation puts about 0.038 below -0.5 (and 0.078 below 0).
"""
from math import erf, exp, fsum, lgamma, log, sqrt
from pathlib import Path
import sys

import numpy as np
import sympy as s

R = s.Rational
x = s.symbols("x", real=True)
n = s.symbols("n", integer=True, positive=True)
root = Path(__file__).resolve().parents[1]
failures = 0


def check(label, ok):
    global failures
    print(f"{'PASS' if bool(ok) else 'FAIL'} {label}")
    failures += not bool(ok)


def close(value, shown, places):
    return abs(float(value)-shown) <= 0.5*10**(-places)+1e-12


def phi(z):
    return (1+erf(float(z)/sqrt(2)))/2


def binom_pmf(n, p, k):
    # Exact rational inputs avoid underflow for large n and tiny p.
    return s.binomial(n, k)*p**k*(1-p)**(n-k)


def erlang_tail(shape, threshold):
    return fsum(exp(-threshold+j*log(threshold)-lgamma(j+1))
                for j in range(shape))


# 1: integrate the exponential tail, independently of a distribution API.
tail = s.integrate(s.exp(-x/3)/3, (x, 12, s.oo))
check("例1", R(3, 12) == R(1, 4) and s.simplify(tail-s.exp(-4)) == 0
      and close(tail, .0183, 4))

# 2: enumerate all 36 equally likely pairs.
dice_sums = np.array([a+b for a in range(1, 7) for b in range(1, 7)])
mu = R(int(dice_sums.sum()), len(dice_sums))
var = sum((s.Integer(v)-mu)**2 for v in dice_sums)/len(dice_sums)
actual = R(int(np.count_nonzero(np.abs(dice_sums-7) >= 4)), 36)
check("例2", mu == 7 and var == R(35, 6) and var/4**2 == R(35, 96)
      and actual == R(1, 6) and close(var/16, .365, 3))

# 3: include 60 and 80; equality on the endpoints matters.
mu, var = 100*R(7, 10), 100*R(7, 10)*R(3, 10)
actual = sum(binom_pmf(100, R(7, 10), j)
             for j in range(101) if abs(j-mu) >= 10)
check("例3", var/10**2 == R(21, 100) and close(actual, .037, 3)
      and float(var/100/actual) > 5)

# 4: complement of the two-sided deviation event.
lower = 1-R(25, (30-15)**2)
check("例4", lower == R(8, 9) and close(lower, .889, 3)
      and close(phi(3)-phi(-3), .9973, 4))

# 5: for any fixed epsilon, n>epsilon leaves just the rare nonzero atom.
rare_probability = 1/n
mean = n*rare_probability
check("例5", s.limit(rare_probability, n, s.oo) == 0
      and s.simplify(mean) == 1 and s.limit(mean, n, s.oo) != 0)

# 6: solve the guarantee exactly and check the previous integer fails it.
needed = s.ceiling(R(1, 4)/(R(1, 20)*R(1, 100)**2))
check("例6", needed == 50000 and R(1, 4)/(needed*R(1, 100)**2) <= R(1, 20)
      and R(1, 4)/((needed-1)*R(1, 100)**2) > R(1, 20))

# 7: compute the die's variance directly; reproduce the declared seed.
die_mean = sum(map(s.Integer, range(1, 7)))/6
die_var = sum((s.Integer(j)-die_mean)**2 for j in range(1, 7))/6
needed = s.ceiling(die_var/(R(1, 20)*R(1, 10)**2))
check("例7 次数与理论标准差", die_mean == R(7, 2) and die_var == R(35, 12)
      and needed == 5834 and close(R(196, 100)**2*die_var/R(1, 10)**2, 1120, 0))
rng = np.random.default_rng(20261017)
displayed = [(10, .560, .540, .080, 3), (100, .172, .171, .423, 3),
             (1000, .0553, .0540, .931, 4), (10000, .0174, .0171, 1., 4)]
ok = True
for size, sd, theory, inside, digits in displayed:
    means = np.concatenate([rng.integers(1, 7, (200, size)).mean(axis=1)
                            for _ in range(10)])
    measured_sd = np.sqrt(np.mean((means-means.mean())**2))
    ok &= (close(measured_sd, sd, digits)
           and close(sqrt(float(die_var)/size), theory, digits)
           and close(np.mean(np.abs(means-3.5) < .1), inside, 3))
check("例7 模拟表（种子 20261017）", ok)

# 8: integrate the quarter disk and reproduce all three runs in order.
quarter_area = s.integrate(s.sqrt(1-x*x), (x, 0, 1))
p = quarter_area
check("例8 期望、标准误差与极限", s.simplify(4*p-s.pi) == 0
      and s.limit(16*p*(1-p)/n, n, s.oo) == 0)
rng = np.random.default_rng(7)
ok = True
for size, estimate, se, est_digits, se_digits in [
    (100, 3.080, .164, 3, 3), (10000, 3.162, .0164, 3, 4),
    (1000000, 3.1437, .00164, 4, 5)]:
    points = rng.random((size, 2))
    hit = np.count_nonzero(np.sum(points*points, axis=1) < 1)
    ok &= close(4*R(hit, size), estimate, est_digits)
    ok &= close(4*s.sqrt(p*(1-p)/size), se, se_digits)
check("例8 模拟表（种子 7）", ok)

# 9: compute the Cauchy tail and its characteristic function, then scale.
cauchy_density = 1/(s.pi*(1+x*x))
tail = 2*s.integrate(cauchy_density, (x, 1, s.oo))
t = s.symbols("t", positive=True)
characteristic = s.simplify(2*s.integrate(s.cos(t*x)*cauchy_density, (x, 0, s.oo)))
average_cf = s.simplify(characteristic.subs(t, t/n)**n)
first_positive = s.integrate(x*cauchy_density, (x, 0, s.oo))
check("例9 平均的分布与不收敛", tail == R(1, 2) and first_positive == s.oo
      and s.simplify(characteristic-s.exp(-t)) == 0
      and s.simplify(average_cf-characteristic) == 0)
rng = np.random.default_rng(3)
ok = True
for size, shown in [(1, .507), (10, .500), (100, .516), (1000, .514)]:
    means = rng.standard_cauchy((4000, size)).mean(axis=1)
    ok &= close(np.mean(np.abs(means) > 1), shown, 3)
check("例9 模拟表（种子 3）", ok)

# 10: variance of an independent average, not the variance of the sum.
sd = [s.sqrt(R(4, size)) for size in [4, 64, 1024]]
needed = s.ceiling(R(4)/R(5, 100)**2)
check("例10", sd == [1, R(1, 4), R(1, 16)] and needed == 1600
      and R(4, 1599) > R(5, 100)**2)

# 11: directly sum the binomial mass and calculate both normal versions.
actual = sum(binom_pmf(100, R(7, 10), j) for j in range(75, 101))
z = R(9, 2)/s.sqrt(21)
check("例11", close(actual, .1631, 4) and close(1-phi(z), .1631, 4)
      and close(1-phi(5/s.sqrt(21)), .1376, 4)
      and close(z, .982, 3) and close(5/s.sqrt(21), 1.091, 3))

# 12: rational binomial summation, then continuity-corrected normal integral.
actual = sum(binom_pmf(1000, R(1, 2), j) for j in range(480, 521))
z = R(41, 2)/s.sqrt(250)
check("例12", close(actual, .8052, 4) and close(2*phi(z)-1, .8052, 4)
      and close(2*phi(20/s.sqrt(250))-1, .7941, 4) and close(z, 1.297, 3))

# 13: this is the lesson's uncorrected normal sample-size approximation.
threshold = s.ceiling((R(196, 100)*R(1, 2)/R(1, 100))**2)
check("例13", threshold == 9604 and R(2, 100)*s.sqrt(threshold) >= R(196, 100)
      and R(2, 100)*s.sqrt(threshold-1) < R(196, 100))

# 14: derive uniform moments by integration, then standardize the sum.
mu = s.integrate(x, (x, 0, 1))
var = s.integrate(x*x, (x, 0, 1))-mu**2
z = (26-48*mu)/s.sqrt(48*var)
check("例14", 48*mu == 24 and 48*var == 4 and z == 1
      and close(1-phi(z), .1587, 4) and 12*var == 1 and 12*mu-6 == 0)

# 15: exponential moments and exact Erlang tail via its finite series.
mu = s.integrate(x*s.exp(-x), (x, 0, s.oo))
var = s.integrate(x*x*s.exp(-x), (x, 0, s.oo))-mu**2
z = (R(12, 10)-mu)/s.sqrt(var/50)
check("例15", mu == 1 and var == 1 and close(1-phi(z), .0786, 4)
      and close(erlang_tail(50, 60), .0844, 4)
      and erlang_tail(50, 60) > 1-phi(z))

# 16: numeric plug-in error bar only; paired model comparison lacks joint data.
p = R(400, 500)
se = s.sqrt(p*(1-p)/500)
margin = R(196, 100)*se
check("例16 误差条计算", p == R(4, 5) and close(se, .0179, 4)
      and close(margin, .035, 3) and close(p-margin, .765, 3)
      and close(p+margin, .835, 3) and close(s.sqrt(p*(1-p)/2000), .0089, 4)
      and s.simplify(s.sqrt(p*(1-p)/2000)/se) == R(1, 2)
      and R(82, 100)-p < margin)

# Supplementary numbered-section tables and the short in-text exercises.
ok = True
for j, exact, poisson, normal in [
    (0, .1351, .1353, .1058), (1, .2707, .2707, .2175),
    (2, .2709, .2707, .2766), (4, .0902, .0902, .1058)]:
    exact_value = binom_pmf(1000, R(1, 500), j)
    poisson_value = s.exp(-2)*2**j/s.factorial(j)
    normal_value = phi((j+.5-2)/sqrt(1.996))-phi((j-.5-2)/sqrt(1.996))
    ok &= close(exact_value, exact, 4) and close(poisson_value, poisson, 4)
    ok &= close(normal_value, normal, 4)
check("例11前 二项、泊松、正态对比表", ok)

# Explicitly verify the documented discrepancy; never relabel the original
# negative-axis assertion as correct just to keep the verification green.
negative_axis = phi(-2/sqrt(1.996))
below_minus_half = phi(-2.5/sqrt(1.996))
lesson = (root / "lesson.md").read_text(encoding="utf-8")
registered = "落在 $-0.5$ 的左边" in lesson and "约 $0.038$" in lesson  # 讲义说的是 -0.5 左边约 0.038
check("例11前 -0.5 左边约0.038（负半轴约0.078442）",
      registered and close(negative_axis, .078442, 6)
      and not close(negative_axis, .038, 3) and close(below_minus_half, .038, 3))

check("例15前 指数和上尾表", all(
    close(erlang_tail(m, m+1.96*sqrt(m)), shown, 4)
    for m, shown in [(1, .0518), (5, .0433), (30, .0340), (200, .0288)])
    and close(1-phi(1.96), .0250, 4))
check("例后小题", R(5, 20) == R(1, 4)
      and s.simplify(s.sqrt(4*n)/s.sqrt(n)) == 2
      and (R(429, 2)-200)/s.sqrt(400*R(1, 2)*R(1, 2)) == R(145, 100))

# --- 编辑二版新增数值 ---
check("编辑 第2节入口 切比雪夫 n=100、1000", R(1, 400)/R(1, 100) == R(1, 4)
      and R(1, 4000)/R(1, 100) == R(1, 40))
check("编辑 例6后小题 12500", R(1, 4)/(R(1, 20)*R(2, 100)**2) == 12500)
check("编辑 模拟后 n=1000 切比雪夫下界约0.71", close(1-R(35, 12)/(1000*R(1, 100)), .71, 2))
check("编辑 方差无界反例 Var=i^2", s.simplify(
    s.summation(s.Symbol('i')**2, (s.Symbol('i'), 1, n))/n**2 - (n+1)*(2*n+1)/(6*n)) == 0)
xx = s.symbols("xx", positive=True)
check("编辑 方差无穷的例子 E=3、E[X^2]发散",
      s.integrate(R(3, 2)*xx**R(-5, 2), (xx, 1, s.oo)) == 1
      and s.integrate(xx*R(3, 2)*xx**R(-5, 2), (xx, 1, s.oo)) == 3
      and s.integrate(xx**2*R(3, 2)*xx**R(-5, 2), (xx, 1, s.oo)) == s.oo)
check("编辑 例8后小题 约10.8倍", close((.0164/.005)**2, 10.76, 2)
      and close(16*(np.pi/4)*(1-np.pi/4)/.005**2, 107870, -2))
check("编辑 例14后小题 0.0416", close(1-phi((55-50)/sqrt(100/12)), .0416, 4))
check("编辑 回到开头 2Φ(2)-1", close(2*phi(2)-1, .9545, 4)
      and abs(1/(2*sqrt(10000))-.005) < 1e-12)
check("编辑 指数和上尾 n=30 高出三成", close(erlang_tail(30, 30+1.96*sqrt(30))/(1-phi(1.96)), 1.36, 2))

sys.exit(bool(failures))
