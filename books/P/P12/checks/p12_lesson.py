#!/usr/bin/env python3
"""Recompute examples, simulations and inline exercises against lesson text."""
from pathlib import Path
import math
import re

import numpy as np
from scipy.stats import binom, chi2, f, norm, poisson, t

TEXT = (Path(__file__).resolve().parents[1]/"lesson.md").read_text(encoding="utf-8")
NUM = r"(-?\d+(?:\.\d+)?)"


def section(k):
    return re.search(rf"(?ms)\*\*例 {k}\*\*.*?(?=\*\*例 {k+1}\*\*|### 本章小结|\Z)",TEXT).group(0)


def check(name, ok, detail=""):
    print(f"{'PASS' if bool(ok) else 'FAIL'} {name} {detail}")


def reported(name, text, pattern, computed, tol):
    match = re.search(pattern, text)
    value = float(match.group(1)) if match else float("nan")
    check(name, abs(value-computed)<=tol, f"printed={value} computed={computed:.9f}")


def val(k, pattern, computed, tol):
    reported(f"例{k}",section(k),pattern,computed,tol)


def decision(k, pattern, computed):
    m = re.search(pattern, section(k))
    check(f"例{k}-判定", m is not None and (m.group(1)=="拒绝")==bool(computed))


val(1, r"P\(X\\le4\)="+NUM, binom.cdf(4,10,.7), .00005)
decision(1, r"第三步.*?，(不拒绝|拒绝) \$H_0", 3<=4)
decision(1, r"命中 5 次，不在拒绝域，(不拒绝|拒绝)", 5<=4)
val(2, r"观察值 \$u=.*?="+NUM+r">1.96", (172.1-170)/(6/math.sqrt(36)), 1e-10)
decision(2, r"第三步.*?，(不拒绝|拒绝) \$H_0", abs(2.1)>norm.isf(.025))
val(3, r"Phi\(1.5\)\]="+NUM, 2*norm.sf((501.5-500)/(4/math.sqrt(16))), .00005)
decision(3,r"两个水平下都(不拒绝|拒绝)", 2*norm.sf(1.5)<.01)

beta = norm.cdf((100+1.645*5/4-103)/(5/4))
val(4,r"Phi\(-0.755\)="+NUM,beta,.0005)
val(4,r"功效为 \$"+NUM,1-beta,.0005)
val(5,r"Phi\(2.6\)\]="+NUM,2*norm.sf((502.6-500)/(4/4)),.00005)
decision(5,r"2.6>1.96\$，(不拒绝|拒绝)",2.6>norm.isf(.025))

x = np.array([12.1,11.6,12.4,11.9,12.3,11.7])
se = x.std(ddof=1)/math.sqrt(len(x))
val(6,r"bar x="+NUM,x.mean(),1e-10)
val(6,r"\$s="+NUM,x.std(ddof=1),.00005)
for mu, pattern, verdict in [(11.8,r"1.52<2.571\$，(不拒绝|拒绝)",False),
                              (11.6,r"3.04>2.571\$，(不拒绝|拒绝)",True)]:
    stat = (x.mean()-mu)/se
    val(6,rf"mu_0={mu}\$.*?0.1317\}}="+NUM,stat,.005)
    decision(6,pattern,abs(stat)>t.isf(.025,5))
val(7,r"1.5/3\}="+NUM,(10.8-10)/(1.5/3),1e-10)
decision(7,r"第三步.*?，(不拒绝|拒绝)",1.6>t.isf(.05,8))

a = np.array([50.1,49.8,50.4,50.0,49.7,50.3])
b = np.array([50.6,50.9,50.4,50.7,51.0,50.5,50.8])
sw2 = (5*a.var(ddof=1)+6*b.var(ddof=1))/11
se8 = math.sqrt(sw2*(1/6+1/7))
stat8 = (a.mean()-b.mean())/se8
val(8,r"\}\}="+NUM,stat8,.005)
decision(8,r"2.201\$，(不拒绝|拒绝)",abs(stat8)>t.isf(.025,11))
sw9 = (39*1.1**2+44*1.2**2)/83
se9 = math.sqrt(sw9*(1/40+1/45))
val(9,r"\{83\}="+NUM,sw9,.0005)
val(9,r"\{0.2508\}="+NUM,-.39/se9,.0005)
decision(9,r"1.989\$，(不拒绝|拒绝)",abs(-.39/se9)>t.isf(.025,83))

# Read the actual paired observations from the printed table.
rows = []
for label in ("之前","之后"):
    line = re.search(rf"(?m)^\| {label} \|(.+)\|$", section(10)).group(1)
    rows.append(np.array([float(s.strip()) for s in line.split("|") if s.strip()]))
before, after = rows
d = before-after
paired = d.mean()/(d.std(ddof=1)/math.sqrt(len(d)))
pooled = (before.var(ddof=1)+after.var(ddof=1))/2
indep = d.mean()/math.sqrt(pooled*2/len(d))
val(10,r"183/\\sqrt6\}="+NUM,paired,.005)
val(10,r"s_1\^2="+NUM,before.var(ddof=1),.005)
val(10,r"s_2\^2="+NUM,after.var(ddof=1),.005)
val(10,r"s_w="+NUM,math.sqrt(pooled),.005)
val(10,r"\{1.09\}="+NUM,indep,.005)
decision(10,r"\n(不拒绝|拒绝)，\$p",abs(paired)>t.isf(.025,5))
decision(10,r"自由度 10，(不拒绝|拒绝)",abs(indep)>t.isf(.025,10))

val(11,r"\{4\}="+NUM,9*9/4,1e-12)
decision(11,r"20.25>16.919\$，(不拒绝|拒绝)",9*9/4>chi2.isf(.05,9))
ratio = a.var(ddof=1)/b.var(ddof=1)
val(12,r"\{0.04667\}="+NUM,ratio,.0005)
val(12,r"\$p="+NUM,2*f.sf(ratio,5,6),.005)
decision(12,r"1.607<5.988\$，(不拒绝|拒绝)",ratio>f.isf(.025,5,6))
lo13, hi13 = -.39-t.isf(.025,83)*se9, -.39+t.isf(.025,83)*se9
val(13,r"即 \$\["+NUM,lo13,.0005)
val(13,r"即 \$\[-0.889,\\,"+NUM,hi13,.0005)
check("例13-包含0", lo13<=0<=hi13 and "区间包含 0，所以不能拒绝" in section(13))

# Values use the rounded quantiles printed in the example.
# The 0.01 tolerance permits propagation from 8.7798 rounded to 8.78.
n14 = ((1.645+1.2816)*6/2)**2
val(14,r"approx"+NUM,n14,.01)
val(14,r"取 \$n="+NUM,math.ceil(n14),0)
n15 = (1.96+.8416)**2*(.09+.0979)/.01**2
val(15,r"approx"+NUM,n15,.05)
val(15,r"每组至少 \}"+NUM,math.ceil(n15),0)
pooled_p = (.10+.11)/2
refined = (1.96*math.sqrt(2*pooled_p*(1-pooled_p))+
           .8416*math.sqrt(.09+.0979))**2/.01**2
val(15,r"更细的公式算出每组 "+NUM,math.ceil(refined),0)

obs = np.array([30,14,12,26,25,13])
q16 = ((obs-20)**2/20).sum()
val(16,r"\{310\}\{20\}="+NUM,q16,0)
decision(16,r"15.5>11.07\$，(不拒绝|拒绝)",q16>chi2.isf(.05,5))
counts = np.array([7,15,22,22,17,9,5,2,1])
lam = np.dot(np.arange(9),counts)/counts.sum()
exp = 100*np.r_[poisson.pmf(np.arange(6),lam),poisson.sf(5,lam)]
obs17 = np.r_[counts[:6],counts[6:].sum()]
q17 = ((obs17-exp)**2/exp).sum()
val(17,r"\{290\}\{100\}="+NUM,lam,1e-10)
line = re.search(r"(?m)^\| 期望 \$E_i\$ \|(.+)\|$",section(17)).group(1)
printed_e = np.array([float(s) for s in line.split("|") if s.strip()])
check("例17-期望次数",np.allclose(printed_e,exp,atol=.005,rtol=0))
val(17,r"0.046="+NUM,q17,.005)
decision(17,r"远大于 0.63，(不拒绝|拒绝)",q17>chi2.isf(.05,5))

d = np.r_[np.ones(6),-np.ones(2),np.zeros(32)]
rng = np.random.default_rng(2026)
boot = d[rng.integers(0,len(d),(10000,len(d)))].mean(axis=1)
ci = np.percentile(boot,[2.5,97.5])
val(18,r"95% 区间 \$\["+NUM,ci[0],.0005)
val(18,r"95% 区间 \$\[-0.025,\\,"+NUM,ci[1],.0005)
val(18,r"平均的标准差是 "+NUM,boot.std(),.0005)
check("例18-主区间包含0",ci[0]<=0<=ci[1] and "所以不能拒绝" in section(18))

rng = np.random.default_rng(5)
for mu in (170,172):
    draws = mu+6*rng.standard_normal((10000,36))
    u = draws.mean(axis=1)-170
    pv = 2*norm.sf(abs(u))
    if mu==170:
        reported("模拟-误拒百分比",TEXT,NUM+r"% 的实验拒绝",100*(abs(u)>1.96).mean(),.005)
    row = re.search(rf"(?m)^\| \$\\mu={mu}\$.*?\| (.+)\|$",TEXT).group(1)
    printed = np.array([float(s) for s in row.split("|") if s.strip()])
    calc = np.array([(pv<=level).mean() for level in (.01,.05,.10,.50)])
    check(f"模拟-p表-{mu}",np.allclose(printed,calc,atol=.0005+1e-12,rtol=0),
          f"computed={calc}")

# All ten numerical inline exercises; recall prompts are not proof exercises.
exercises = re.findall(r"(?m)^> 答案：(.*)$",TEXT)
check("随堂-覆盖数",len(exercises)==10)
reported("随堂1-p9",exercises[0],r"11\}\{1024\}="+NUM,binom.sf(8,10,.5),.00005)
reported("随堂1-p8",exercises[0],r"56\}\{1024\}="+NUM,binom.sf(7,10,.5),.00005)
reported("随堂1-临界值",exercises[0],r"\$c="+NUM,
         min(k for k in range(11) if binom.sf(k-1,10,.5)<=.05),0)
reported("随堂2-p",exercises[1],r"Phi\(2.6\)\]="+NUM,2*norm.sf(2.6),.00005)
reported("随堂3-p",exercises[3],r"\$p="+NUM,2*norm.sf((52.2-50)/(3/3)),.00005)
check("随堂4-区间对偶",a.mean()-b.mean()+t.isf(.025,11)*se8<0 and
      exercises[6].startswith("区间不含 0，拒绝"))
reported("随堂5-样本量",exercises[7],r"取 "+NUM,math.ceil(((1.96+.8416)*4)**2),0)
reported("随堂6-统计量",exercises[8],r"50\}="+NUM,2*(60-50)**2/50,0)
check("随堂6-判定",4>chi2.isf(.05,1) and "拒绝；" in exercises[8])
reported("随堂7-漏抽概率",exercises[9],r"\^\{40\}="+NUM,(39/40)**40,.0005)
reported("随堂7-极限",exercises[9],r"approx"+NUM,math.exp(-1),.0005)
check("自助小例子-均值",np.mean([3,7,4,9,5])==5.6 and np.mean([3,4,4,5,9])==5.0)
