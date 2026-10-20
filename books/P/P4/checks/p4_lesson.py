"""独立核对 P.4 讲义例题中的数值与结论。"""
import math
import numpy as np

def close(a, b, tol=1e-8):
    return abs(a - b) < tol

def ok(k, cond):
    print(f"{'PASS' if cond else 'FAIL'} 例{k}")

Phi = lambda z: 0.5 * (1 + math.erf(z / math.sqrt(2)))

ok(1, close(1 / 9, 1 / 9) and close((2**3 - 1**3) / 27, 7 / 27) and close(2**3 / 27, 8 / 27))
ok(2, close(1.5**2 / 4 - 1 / 4, 0.3125) and close(1.5**2 / 4, 0.5625))
ok(3, 2 > 1 and close(2 * 0.1, 0.2) and close(0, 0))
ok(4, close(0.5, 0.5) and close(math.exp(-1) / 2, 0.1839397206) and close(1 - math.exp(-1), 0.6321205588))
ok(5, close(0.5, 0.5) and close((math.atan(1) - math.atan(-1)) / math.pi, 0.5))

ok(6, close((10 - 7) / 10, 0.3) and close((5 - 2) / 10, 0.3))
ok(7, close((6 - 2) / 6, 2 / 3))
cum = np.cumsum([0.4, 0.3, 0.2, 0.1])
ok(8, int(np.searchsorted(cum, 0.83, side="right")) == 2 and close(cum[1], 0.7) and close(cum[2], 0.9))
ok(9, close(2 / 4, 0.5) and close(1 / 4, 0.25))

ok(10, close(math.exp(-1.5), 0.2231301601) and close(math.exp(-0.5) - math.exp(-1), 0.2386512185))
ok(11, close(math.exp(-2.5) / math.exp(-1), math.exp(-1.5)) and close(10 / 40, 0.25))
ok(12, close(-math.log(0.25) / 2, math.log(2)) and close(0.25**2, 0.0625))
ok(13, close(math.log(2) / 0.05, 13.8629436112, 1e-9))

c14 = math.exp(-1) / math.sqrt(math.pi)
ok(14, close(c14 * math.exp(1) * math.sqrt(math.pi), 1) and close(1, 1) and close(0.5, 0.5))
peak15 = 1 / (3 * math.sqrt(2 * math.pi))
inflections15 = (2 - 3, 2 + 3)
ok(15, close(peak15, 0.1329807601) and inflections15 == (-1, 5) and close(0.5, 0.5))

ok(16, close(Phi(2) - Phi(-1), 0.818594614) and close(1 - Phi(2), 0.022750132))
ok(17, close(170 + 1.645 * 6, 179.87))
ok(18, close(Phi(-2), 0.022750132) and close(Phi(1), 0.841344746) and close(1 - Phi(1.5), 0.066807201))
ok(19, close(2 * (1 - Phi(2.5)), 0.0124193307, 1e-8))
ok(20, close((85 - 70) / 10, 1.5) and close((72 - 60) / 5, 2.4) and (1 - Phi(2.4) < 1 - Phi(1.5)))

# 编辑二稿新增的数值
lam = 1 / 0.3
ok("开头", close(lam * math.exp(-lam * 0.3) * 0.0002, 2.4525e-4, 1e-6) and close(math.exp(-lam * 0.2999) - math.exp(-lam * 0.3001), 2.4525e-4, 1e-6))
ok("S3", close(math.exp(-3), 0.0497870684) and close(math.exp(-1.5), 0.2231301601) and close(0.05 * 0 + 3 / 12 * 1, 0.25))
ok("S5", close(-6 / 36, -1 / 6) and close(12 / 36, 1 / 3) and close(0.95**20, 0.3585, 1e-4))
