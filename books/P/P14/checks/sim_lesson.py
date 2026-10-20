"""讲义里模拟表的数字（固定种子）。"""
import numpy as np

rng = np.random.default_rng(2026)
n = 100000
p = np.array([1 / 2, 1 / 4, 1 / 8, 1 / 8])
x = rng.choice(4, size=n, p=p)
len_mine = np.array([1, 2, 3, 3])      # 码字 0,10,110,111
len_uniform = np.array([2, 2, 2, 2])
len_wrong = np.array([3, 3, 2, 1])     # q' = (1/8,1/8,1/4,1/2)
a, b, c = len_mine[x].mean(), len_uniform[x].mean(), len_wrong[x].mean()
print(f"SIM 按p配码 {a:.3f} 等长码 {b:.3f} 按q'配码 {c:.3f} 样本频率 {np.bincount(x) / n}")
print("PASS 按p配码≈7/4" if abs(a - 1.75) < .01 else "FAIL 按p配码")
print("PASS 等长码=2" if b == 2 else "FAIL 等长码")
print("PASS 按q'配码≈2.625" if abs(c - 2.625) < .02 else "FAIL 按q'配码")
