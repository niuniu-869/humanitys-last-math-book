"""讲义里模拟结果表的数字（固定种子），并与精确值比对。"""
import numpy as np
rng = np.random.default_rng(2026)
P = np.array([[0.8, 0.2], [0.3, 0.7]])
N = 100000
# A: 10 万个用户从“活跃”出发，第 n 周仍活跃的比例
state = np.zeros(N, dtype=int)
rows = []
for n in range(0, 5):
    if n > 0:
        u = rng.random(N)
        state = np.where(state == 0, (u >= 0.8).astype(int), np.where(u < 0.3, 0, 1))
    rows.append((n, (state == 0).mean(), (np.linalg.matrix_power(P, n))[0, 0]))
for n, s, e in rows:
    print(f"INFO 第{n}周 模拟 {s:.4f} 精确 {e:.4f}")
    print(("PASS" if abs(s - e) < 0.01 else "FAIL"), f"sim-A-{n}")
# B: 一条长路径中活跃的时间比例
rng = np.random.default_rng(7)
T = 200000
s = 0; cnt = 0
u = rng.random(T)
for t in range(T):
    cnt += (s == 0)
    s = (0 if u[t] < 0.8 else 1) if s == 0 else (0 if u[t] < 0.3 else 1)
print(f"INFO 长路径活跃占比 {cnt/T:.4f}")
print("PASS" if abs(cnt / T - 0.6) < 0.01 else "FAIL", "sim-B")
# C: 吸收链，从活跃/沉默出发
Pa = np.array([[0.6, 0.2, 0.2, 0.0], [0.3, 0.4, 0.0, 0.3], [0, 0, 1, 0], [0, 0, 0, 1]])
rng = np.random.default_rng(11)
for start, ep, et in ((0, 2/3, 40/9), (1, 1/3, 35/9)):
    pay = 0; steps = 0; R = 100000
    for _ in range(R):
        s = start; k = 0
        while s < 2:
            s = rng.choice(4, p=Pa[s]); k += 1
        pay += (s == 2); steps += k
    print(f"INFO 起点{start} 付费比例 {pay/R:.4f}（精确 {ep:.4f}） 平均步数 {steps/R:.3f}（精确 {et:.3f}）")
    print("PASS" if abs(pay / R - ep) < 0.01 and abs(steps / R - et) < 0.05 else "FAIL", f"sim-C-{start}")
