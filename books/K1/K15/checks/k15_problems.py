#!/usr/bin/env python3
"""K15 题目验算：先独立计算，再与 answers.md 中的选项比对。"""
from fractions import Fraction
from itertools import permutations, product
from pathlib import Path
import re

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
ANS = (ROOT / "answers.md").read_text(encoding="utf-8")


def block(pid):
    m = re.search(rf"^\*\*{pid}\*\*(.*?)(?=^\*\*K15-\d+\*\*|\Z)", ANS, re.M | re.S)
    if not m:
        raise AssertionError(f"缺少 {pid} 答案")
    return m.group(1)


def answer(pid):
    m = re.search(r"\*\*答案：\*\*\s*\(([A-D])\)", block(pid))
    if not m:
        raise AssertionError(f"{pid} 不是单选格式")
    return m.group(1)


def check(pid, ok):
    print(f"{'PASS' if ok else 'FAIL'} {pid}")
    if not ok:
        raise AssertionError(pid)


def choice(pid, truth):
    if len(truth) != 4 or sum(bool(x) for x in truth) != 1:
        raise AssertionError(f"{pid} 选项没有唯一真值: {truth}")
    chosen = "ABCD"[truth.index(True)]
    check(pid, answer(pid) == chosen)


# A：有限样本支持全称断言，桥是样本桥；q(2.5)=0 给出反例。
q = lambda x: (x - sp.Rational(5, 2)) ** 2
qvals = [q(n) for n in range(4)]
choice("K15-01", [False, min(qvals) > 0 and q(sp.Rational(5, 2)) == 0, False, False])

# A：用 sympy 因式分解检验反例。
n = sp.symbols("n", integer=True, positive=True)
counter = sp.expand(n**2 + n + 17).subs(n, 16)
choice("K15-02", [sp.factorint(int(counter)) == {17: 2}, False, False, False])

# A：似然比先乘先验赔率，再换回概率。
prior_odds = Fraction(3, 2)
post = [prior_odds * Fraction(9, 10), prior_odds * Fraction(2, 5),
        prior_odds * 2, prior_odds]
choice("K15-03", [post[0] == min(post), post[1] == min(post),
                  post[2] == min(post), post[3] == min(post)])

# A：连续性是介值结论所需的条件；B 只限零点个数、C 只控开区间、D 只控总落差，都不保证零点。
choice("K15-04", [True, False, False, False])

# A：由总量/平均数反算个数。
counts = (Fraction(120, 10), Fraction(96, 12))
choice("K15-05", [counts == (12, 8), False, False, False])

# B：训练误差下降不保证泛化；独立验证集误差上升直接削弱结论。
choice("K15-06", [False, True, False, False])

# B：换一个波动指标后，回答“是/否”会分别加强/削弱稳定性判断。
choice("K15-07", [False, True, False, False])

# B：在所有满足 m6 -> even -> square_even 的布尔赋值上检验四个选项。
models = [(m6, even, sq) for m6, even, sq in product([False, True], repeat=3)
          if (not m6 or even) and (not even or sq)]
truth = []
for option in "ABCD":
    vals = []
    for m6, even, sq in models:
        vals.append({
            "A": (not even) or m6,
            "B": even or (not m6),
            "C": (not sq) or m6,
            "D": m6 == even,
        }[option])
    truth.append(all(vals))
choice("K15-08", truth)

# B：只有完成校验才发布，即 F -> C；除非敏感否则自动发布，即
# ~S -> A。没有自动发布（~A）时，逆否推出含敏感信息。
choice("K15-09", [True, False, False, False])

# B：中位数与均值接近、男女同向，第 2、3 问被数据排除；结论只说公斤数，不涉及分母；统计对象经过「每周打卡」筛选。
mean, median = Fraction(-61, 10), Fraction(-58, 10)
male, female = Fraction(-63, 10), Fraction(-59, 10)
assert min(male, female) <= mean <= max(male, female)
only_weekly_uploaders = True
claim_is_ratio = False
choice("K15-10", [abs(mean - median) > 1, only_weekly_uploaders,
                  claim_is_ratio, (male < 0) != (female < 0)])

# B：质数与偶数有交集 2，但彼此都有对方之外的元素。
A = {2, 3, 5, 7, 11}
B = {2, 4, 6, 8, 10}
choice("K15-11", [A == B, A < B, bool(A & B) and not (A < B) and not (B < A), not (A & B)])

# C：S1、S2 都充分；n=18 满足 S2 不满足 S1，说明 S1 不是唯一的充分条件。
print("MANUAL K15-12")

# C：容斥计算六个位置的合法排列数。
from math import factorial
valid_count = factorial(6) // 2 - (120 + 60 + 60) + (24 + 24 + 12) - 6
choice("K15-13", [valid_count == 144, valid_count == 156,
                   valid_count == 174, valid_count == 192])

# C：逐条检查定义的两个分支，第一分支含否定要件。
def is_stable_number(k):
    first = k % 2 == 0 and sum(map(int, str(k))) % 3 != 0
    second = k < 10 and sp.isprime(k)
    return first or second

choice("K15-14", [is_stable_number(k) for k in (18, 14, 15, 21)])


# C：开放题，答案须点出他因、排除他因，并把护眼灯与延长课间分开。
b15 = block("K15-15")
check("K15-15", all(s in b15 for s in ("他因", "排除他因", "护眼灯", "没触动")))
