#!/usr/bin/env python3
"""Read printed answers and compare with independently calculated results."""
from pathlib import Path
import math
import re

import numpy as np
import sympy as sp
from scipy.stats import binom, chi2, norm, t

ROOT = Path(__file__).resolve().parents[1]
ANS = (ROOT / "answers.md").read_text(encoding="utf-8")
PROB = (ROOT / "problems.md").read_text(encoding="utf-8")


def part(k, text=ANS):
    return re.search(rf"(?ms)^\*\*P12-{k:02d}\*\*(.*?)(?=^\*\*P12-|\Z)", text).group(1)


def check(label, ok, detail=""):
    print(f"{'PASS' if bool(ok) else 'FAIL'} {label} {detail}")


def number(k, pattern, computed, digits):
    match = re.search(pattern, part(k))
    printed = float(match.group(1).rstrip(".")) if match else float("nan")
    check(f"P12-{k:02d}-number", abs(printed - computed) <= .51 * 10**(-digits),
          f"printed={printed} computed={computed:.9f}")


def choice(k, truths):
    chosen = re.search(r"\*\*答案：\*\* \(([A-D])\)", part(k))
    check(f"P12-{k:02d}-choice", chosen is not None and
          [chr(65+i) for i, ok in enumerate(truths) if ok] == [chosen.group(1)])
    for i, truth in enumerate(truths):
        letter = chr(65+i)
        # Each option must also be addressed explicitly in the answer.
        check(f"P12-{k:02d}-option-{letter}", f"({letter})" in part(k),
              f"computed_truth={bool(truth)}")


n, p0 = 12, .4
c = max(k for k in range(n+1) if binom.cdf(k, n, p0) <= .05)
number(1, r"最大 \$c=(\d+)", c, 0)
number(1, r"le1\)=([0-9.]+)", binom.cdf(1, n, p0), 4)
number(1, r"le2\)=([0-9.]+)", binom.cdf(2, n, p0), 4)
check("P12-01-decision", (1 <= c) == bool(re.search(r"时拒绝 \$H_0", part(1))))

u = 1.8
pv = 2*norm.sf(abs(u))
number(2, r"approx([0-9.]+)>0.05", pv, 4)
# The distribution of U under H0 specifies no probability that H0 is true.
# Two mixtures with the same null law give distinct posterior probabilities.
post = [prior*norm.pdf(u)/(prior*norm.pdf(u)+(1-prior)*norm.pdf(u-2))
        for prior in (.2, .8)]
choice(2, [np.isclose(norm.sf(u), pv), pv > .05,
           all(np.isclose(q, pv) for q in post), abs(u) > norm.isf(.025)])

stat = (10.6-10)/(1.2/math.sqrt(8))
number(3, r"sqrt8\)=([0-9.]+)", stat, 3)
check("P12-03-decision", (stat <= t.isf(.05, 7)) ==
      part(3).lstrip().startswith("**答案：** 不拒绝"))
threshold = 4*chi2.isf(.05, 11)/11
number(4, r"approx([0-9.]+)", threshold, 3)
check("P12-04-boundary", not (threshold > threshold) and "、不拒绝" in part(4))

lo, hi = 100+norm.isf(.05), 102.5-norm.isf(.2)
number(5, r"approx\[([0-9.]+),", lo, 6)
number(5, r"approx\[[0-9.]+,([0-9.]+)", hi, 6)
mid = (lo+hi)/2
valid = lambda c: norm.sf(c-100) <= .05+1e-12 and norm.cdf(c-102.5) <= .2+1e-12
choice(5, [mid <= lo and mid >= hi,
           valid(lo) and valid(mid) and valid(hi),
           valid(102.5+norm.isf(.2)),
           np.isclose(lo, hi) and valid(lo)])
check("P12-05-reversed-bounds", lo < hi and not valid(lo-.01) and not valid(hi+.01))

sw2 = (9*.8**2+11*.7**2)/20
stat = .6/math.sqrt(sw2*(1/10+1/12))
number(6, r"=([0-9.]+),\\qquad s_w", sw2, 4)
number(6, r"s_w=([0-9.]+)", math.sqrt(sw2), 4)
number(6, r"1/12\}\)=([0-9.]+)", stat, 3)
check("P12-06-decisions", t.isf(.05,20) < stat < t.isf(.025,20)
      and "双侧不拒绝，事先规定的右侧检验拒绝" in part(6))
check("P12-06-posthoc", np.isclose(2*t.sf(t.isf(.05,20),20), .10))

d = np.array([1,2,0,1,2], dtype=float)
e = 10*d+5
td = d.mean()/(d.std(ddof=1)/math.sqrt(5))
te = (e.mean()-5)/(e.std(ddof=1)/math.sqrt(5))
number(7, r"t=([0-9.]+)>", td, 3)
number(7, r"s_d\^2=([0-9.]+)", d.var(ddof=1), 1)
number(7, r"mu_D=(-?[0-9.]+)", (0-5)/10, 1)
check("P12-07-transform", np.isclose(td,te) and td > t.isf(.025,4)
      and r"H_0:\mu_E=5" in part(7) and "拒绝原假设" in part(7))

z = norm.isf(.025)
se = math.sqrt((1/z)**2+(1/z)**2)
ci = np.array([1.5-z*se, 1.5+z*se])
number(8, r"approx\[([0-9.]+),", ci[0], 4)
number(8, r"approx\[[0-9.]+,([0-9.]+)", ci[1], 4)
wrong_ci = np.array([1.5-z*math.sqrt(2), 1.5+z*math.sqrt(2)])
number(8, r"\[(-1\.[0-9]+),", wrong_ci[0], 4)
number(8, r"\[-1\.[0-9]+,([0-9.]+)", wrong_ci[1], 4)
choice(8, [ci[0] <= 0 <= ci[1],
           np.allclose(ci, [1.5-math.sqrt(2),1.5+math.sqrt(2)]) and ci[0]>0,
           np.allclose(ci,[-.5,3.5]), np.allclose(ci,wrong_ci)])

obs = np.array([1,2,3,4,5,5])
merged = obs.reshape(3,2).sum(axis=1)
expected = obs.sum()/3
stat = ((merged-expected)**2/expected).sum()
number(9, r"=([0-9.]+)\.\$\$", stat, 3)
check("P12-09-conditions", obs.sum()/6 < 5 <= expected and
      "不能直接使用" in part(9) and "合并后不拒绝" in part(9) and stat < chi2.isf(.05,2))
number(9, r"自由度为 \$3-1=(\d+)", len(merged)-1, 0)

minimum = (3*(norm.isf(.05)+norm.isf(.1)))**2
number(10, r"最小样本量为 \$n=(\d+)", math.ceil(minimum), 0)
number(10, r"approx([0-9.]+)", minimum, 4)
for n in (77,78):
    lower, upper = 6*norm.isf(.05)/math.sqrt(n), 2-6*norm.isf(.1)/math.sqrt(n)
    check(f"P12-10-feasible-{n}", (lower <= upper) == (n == 78),
          f"bounds={lower:.6f},{upper:.6f}")
number(10, r"\[([0-9.]+),", 6*norm.isf(.05)/math.sqrt(78), 6)
number(10, r"\[[0-9.]+,([0-9.]+)", 2-6*norm.isf(.1)/math.sqrt(78), 6)
number(10, r"下界约 \$([0-9.]+)", 6*norm.isf(.05)/math.sqrt(77), 6)
number(10, r"上界约 \$([0-9.]+)", 2-6*norm.isf(.1)/math.sqrt(77), 6)
print("MANUAL P12-10-proof 阈值等价与所有更小整数的不可行性")

freq_match = re.search(r"频数为 \$\((\d+),(\d+),(\d+)\)",part(11,PROB))
freq = np.array([int(v) for v in freq_match.groups()])
values = np.arange(3)
sample = np.repeat(values, freq)
phat = sample.mean()/2
p = sp.symbols("p", positive=True)
loglike = sum(int(o)*sp.log(sp.binomial(2,int(k))*p**int(k)*(1-p)**int(2-k))
              for k,o in zip(values,freq))
roots = sp.solve(sp.diff(loglike,p), p)
expected = freq.sum()*binom.pmf(values,2,phat)
stat = ((freq-expected)**2/expected).sum()
number(11, r"hat p=([0-9.]+)", phat, 1)
number(11, r"chi\^2=(\d+)", stat, 0)
reported_expected = re.search(r"期望次数均为 \$\((\d+),(\d+),(\d+)\)",part(11))
check("P12-11-realizable-MLE", len(sample)==100 and sample.sum()==100
      and roots==[sp.Rational(1,2)] and sp.diff(loglike,p,2).subs(p,phat)<0
      and reported_expected is not None
      and np.allclose(expected,[float(v) for v in reported_expected.groups()]))
check("P12-11-df-decisions", chi2.isf(.05,1)<stat<chi2.isf(.05,2)
      and "估参检验拒绝，事先固定参数的检验不拒绝" in part(11))
number(11, r"3-1-1=(\d+)", len(expected)-1-1, 0)
number(11, r"3-1=(\d+)", len(expected)-1, 0)

x = np.array([2,4,3,5,6],float)
tt = (x.mean()-4.5)/(x.std(ddof=1)/math.sqrt(len(x)))
qq = (len(x)-1)*x.var(ddof=1)
number(12, r"bar x=(\d+)", x.mean(), 0)
number(12, r"s\^2=10/4=([0-9.]+)", x.var(ddof=1), 1)
number(12, r"sqrt5\}=(-?[0-9.]+)", tt, 3)
number(12, r"times2.5\}\{1\}=(\d+)", qq, 0)
check("P12-12-decisions", abs(tt)<t.isf(.025,4) and qq>chi2.isf(.05,4)
      and "均值检验不拒绝，方差检验拒绝" in part(12))

c = min(k for k in range(13) if binom.sf(k-1,12,.5)<=.05)
number(13, r"临界值为 \$(\d+)", c, 0)
number(13, r"功效约为 \$([0-9.]+)", binom.sf(c-1,12,.75), 6)
number(13, r"299\}\{4096\}\\approx([0-9.]+)", binom.sf(8,12,.5), 4)
number(13, r"79\}\{4096\}\\approx([0-9.]+)", binom.sf(9,12,.5), 6)
check("P12-13-minimum", binom.sf(c-2,12,.5)>.05>=binom.sf(c-1,12,.5))

interval = re.search(r"区间为 \$\[(-?[\d.]+),(-?[\d.]+)\]", part(14,PROB))
lo, hi = map(float,interval.groups())
check("P12-14-contains-zero", lo<=0<=hi and
      part(14).lstrip().startswith("**答案：** 在 $0.05$ 下不拒绝"))
# The nesting constraint alone permits either result at 90%.
nested = [(-.20,.05),(-.20,-.01)]
check("P12-14-information", all(lo<=a<=b<=hi for a,b in nested)
      and len({a<=0<=b for a,b in nested})==2 and "不能确定" in part(14))

ids = {f"P12-{k:02d}" for k in range(1,15)}
table_ids = set(re.findall(r"^\| (P12-\d+) ",PROB,re.M))
body_ids = set(re.findall(r"^\*\*(P12-\d+)\*\*",PROB,re.M))
answer_ids = set(re.findall(r"^\*\*(P12-\d+)\*\*",ANS,re.M))
lesson = (ROOT/"lesson.md").read_text(encoding="utf-8")
summary = lesson.split("### 本章小结")[1]
check("P12-index", table_ids==body_ids==answer_ids==ids and
      set(re.findall(r"P12-\d+",summary))<=ids)
for row in summary.splitlines():
    m = re.match(r"\| 方法 (\d+).*?\|.*?\| (.*?) \|",row)
    if m:
        for pid in re.findall(r"P12-(\d+)",m.group(2)):
            check(f"P12-summary-{pid}", f"方法 {m.group(1)}" in part(int(pid),PROB))
