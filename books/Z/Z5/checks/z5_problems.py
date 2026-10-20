"""Z.5 习题的独立验算。"""
from itertools import combinations, combinations_with_replacement, permutations, product
from math import comb
from pathlib import Path
import re
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
ANS = (ROOT / "answers.md").read_text(encoding="utf-8")
PROBS = (ROOT / "problems.md").read_text(encoding="utf-8")
FAIL = 0


def check(qid, condition):
    global FAIL
    if condition:
        print(f"PASS {qid}")
    else:
        FAIL += 1
        print(f"FAIL {qid}")


def has(qid, *parts):
    block = ANS[ANS.index(f"**{qid}**"):]
    next_mark = block.find("\n\n**", 5)
    if next_mark >= 0:
        block = block[:next_mark]
    return all(str(p) in block for p in parts)


def options(qid):
    block = PROBS.split(f"**{qid}**", 1)[1].split("\n**Z5-", 1)[0]
    return [int(value) for value in re.findall(r"\([A-D]\)\s*\$(-?\d+)\$", block)]


# 方法 1：枚举“最后一位”的两个互不重叠情形。
digits = "0123456"
z501 = sum(
    1 for p in permutations(digits, 4)
    if p[0] != "0" and int("".join(p)) % 5 == 0
)
check("Z5-01", z501 == 220 and has("Z5-01", 220))

# 方法 2：直接用组合数核对选择题的四个候选值。
z502 = sp.binomial(7, 3) - sp.binomial(4, 3) - sp.binomial(3, 3)
z502_options = [comb(4, 2) * 3, 4 * 3 * 2, int(z502), comb(7, 3)]
check("Z5-02", z502_options == options("Z5-02") and z502 == 30 and has("Z5-02", "(C)", 30))

# 方法 3：总排列减去甲乙捆绑。
z503 = sp.factorial(6) - 2 * sp.factorial(5)
check("Z5-03", z503 == 480 and has("Z5-03", 480))

# 独立枚举原题中的四个正奇数，核对换元后的隔板公式。
z504 = sum(sum(values) == 14 for values in product(range(1, 15, 2), repeat=4))
check("Z5-04", z504 == comb(8, 3) == 56 and has("Z5-04", 56))

# 方法 6：由二项式展开直接取系数。
x = sp.symbols("x")
z505 = sp.expand((1 + x) ** 5 * (1 - 2 * x) ** 4).coeff(x, 3)
terms = [comb(5, 3-j) * comb(4, j) * (-2)**j for j in range(4)]
z505_options = [terms[-1], sum(abs(t) for t in terms), sum(terms[:-1]), int(z505)]
check("Z5-05", sum(terms) == z505 == 18 and z505_options == options("Z5-05")
      and has("Z5-05", "(D)", 18))

# 方法 4、7：先求满射，再扣除 1、2 号书同组的满射。
surj = 3**5 - 3 * 2**5 + 3
same12 = 3 * (3**3 - 2 * 2**3 + 1)
z506 = surj - same12
check("Z5-06", z506 == 114 and has("Z5-06", 114))

# 范德蒙德恒等式是证明题，枚举小参数验证等式本身。
vandermonde = all(
    sum(sp.binomial(m, j) * sp.binomial(n, k - j) for j in range(k + 1))
    == sp.binomial(m + n, k)
    for m in range(1, 7) for n in range(1, 7) for k in range(0, m + n + 1)
)
check("Z5-07", vandermonde, )
print("MANUAL Z5-07")

# 构造七个互斥区域，以实际集合运算独立核对题目数据和交并条件。
regions = {(1, 0, 0): 13, (0, 1, 0): 9, (0, 0, 1): 7,
           (1, 1, 0): 8, (1, 0, 1): 5, (0, 1, 1): 4, (1, 1, 1): 4}
sets = [{(bits, i) for bits, size in regions.items() if bits[j]
         for i in range(size)} for j in range(3)]
a, b, c = sets
z508 = len((a | b) & (a | c))
z508_options = [len(a), z508, len(a) + len(b & c), len(a | b | c)]
check("Z5-08", [len(a), len(b), len(c), len(a & b), len(a & c), len(b & c), len(a & b & c)]
      == [30, 25, 20, 12, 9, 8, 4] and z508 == 34
      and z508_options == options("Z5-08") and has("Z5-08", "(B)", 34))

# 隔板总数减去两个上限越界事件，并加回交集。
z509 = sp.binomial(14, 2) - sp.binomial(9, 2) - sp.binomial(8, 2) + sp.binomial(3, 2)
check("Z5-09", z509 == 30 and has("Z5-09", 30))

# 不同球分别选择盒子，再用容斥排除空盒。
z510 = 3**8 - 3 * 2**8 + 3
check("Z5-10", z510 == 5796 and has("Z5-10", 5796))

# 余数证明题，数值情形由枚举核对，证明文字人工阅读。
z511_numeric = all(
    any((a - b) % n == 0 for a, b in combinations(values, 2))
    for n in range(1, 7)
    for values in combinations_with_replacement(range(n), n + 1)
)
z511_counterexamples = all(
    not any((a - b) % n == 0 for a, b in combinations(range(1, n + 1), 2))
    for n in range(1, 12)
)
check("Z5-11", z511_numeric and z511_counterexamples)
print("MANUAL Z5-11")

# 恰有两封装对：选择正确位置，再乘 D_4。
d4 = sum((-1) ** j * sp.binomial(4, j) * sp.factorial(4 - j) for j in range(5))
z512 = sp.binomial(6, 2) * d4
check("Z5-12", z512 == 135 and d4 == 9 and has("Z5-12", 135, 9))

# 按原变量枚举，独立于答案的换元和容斥。
z513 = sum(a + b + c + d == 18 and c % 2 == 0
           for a, b, c, d in product(range(2, 7), range(1, 5), range(19), range(19)))
f_values = [sum(comb(s - 2*t + 2, 2) for t in range(s // 2 + 1)) for s in (15, 10, 11, 6)]
check("Z5-13", f_values == [444, 161, 203, 50]
      and f_values[0] - f_values[1] - f_values[2] + f_values[3] == z513 == 130
      and has("Z5-13", 130, *f_values))

# 这是构造鸽巢的证明题，枚举小 n 检查“同奇数部分”确实推出整除。
def odd_part(a):
    while a % 2 == 0:
        a //= 2
    return a


z514_numeric = all(
    any(odd_part(a) == odd_part(b) and (a % b == 0 or b % a == 0)
        for a, b in combinations(subset, 2))
    for n in range(1, 8)
    for subset in combinations(range(1, 2 * n + 1), n + 1)
)
check("Z5-14", z514_numeric)
print("MANUAL Z5-14")

raise SystemExit(1 if FAIL else 0)
