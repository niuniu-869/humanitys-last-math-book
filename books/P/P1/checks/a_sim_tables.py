"""P.1 讲义里的模拟表（固定随机种子）与例题数值的独立核对。"""
import itertools
from fractions import Fraction as F
from math import comb, factorial
import numpy as np

def ok(tag, cond):
    print(f"PASS {tag}" if bool(cond) else f"FAIL {tag}")

# 第 3 节：掷两颗骰子，点数和为 7 的频率
rng = np.random.default_rng(1)
print("表1 掷两颗骰子，点数和为 7 的频率")
last = None
for n in [10, 100, 1000, 10**4, 10**5, 10**6]:
    a = rng.integers(1, 7, n); b = rng.integers(1, 7, n)
    last = ((a + b) == 7).mean()
    print(f"  n={n}: {last:.4f}")
ok("表1收敛到1/6", abs(last - 1/6) < 0.002)

# 第 6 节：随机点落在单位圆内
rng = np.random.default_rng(7)
print("表2 单位正方形里随机撒点，落进四分之一圆的频率")
for n in [100, 1000, 10**4, 10**5, 10**6]:
    x = rng.random(n); y = rng.random(n)
    f = (x*x + y*y < 1).mean()
    print(f"  n={n}: {f:.4f}, 4f={4*f:.4f}")
ok("表2 4f接近pi", abs(4*f - np.pi) < 0.01)

# 第 5 节：生日问题
def bd(n):
    p = F(1)
    for i in range(n): p *= F(365 - i, 365)
    return 1 - p
print("表3 生日问题")
for n in [10, 20, 23, 30, 40, 50]:
    print(f"  n={n}: {float(bd(n)):.4f}")
ok("生日23", round(float(bd(23)), 4) == 0.5073 and round(float(bd(22)), 4) == 0.4757)

# 例题核对
O = list(itertools.product(range(1, 7), repeat=2))
ok("两骰 S>=10", F(sum(a+b >= 10 for a, b in O), 36) == F(1, 6))
ok("两骰 至少一个6", F(sum(6 in o for o in O), 36) == F(11, 36) and 1 - F(25, 36) == F(11, 36))
ok("两骰 S分布", all(F(sum(a+b == s for a, b in O), 36) == F(6 - abs(s-7), 36) for s in range(2, 13)))
ok("两骰 较大点数", all(F(sum(max(a, b) == m for a, b in O), 36) == F(2*m-1, 36) for m in range(1, 7)))
ok("袋中取球 无放回", F(comb(3,1)*comb(5,1), comb(8,2)) == F(15, 28))
ok("袋中取球 有放回", F(2*3*5, 64) == F(15, 32))
ok("相邻", F(2*factorial(4), factorial(5)) == F(2, 5))
ok("次品抽样", F(comb(5,2)*comb(95,8), comb(100,10)) == F(1335, 19012))
ok("几何 会面", 1 - F(3, 4)**2 == F(7, 16))
ok("加法公式例", (F(6,10)+F(5,10)-F(8,10), F(6,10)-F(3,10)) == (F(3,10), F(3,10)))
ok("三事件容斥", F(3,4) - F(1,16)*2 + 0 == F(5,8))
ok("2^-k", sum(F(1, 2**k) for k in range(1, 60)) + F(1, 2**59) == 1)
ok("问题分配", F(3, 4) == F(sum(1 for o in itertools.product('AB', repeat=2) if 'A' in o), 4))
ok("针", abs(2*1/(np.pi*2) - 1/np.pi) < 1e-12)
