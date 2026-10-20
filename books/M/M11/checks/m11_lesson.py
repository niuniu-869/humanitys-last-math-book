"""独立核对 lesson.md 中例 1--6 和随堂数值。"""
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
LESSON = (ROOT / "lesson.md").read_text(encoding="utf-8")

def sm(x):
    x = np.asarray(x, dtype=float)
    e = np.exp(x - np.max(x))
    return e / e.sum()

def check(label, condition):
    print(f"{'PASS' if condition else 'FAIL'} {label}")

X = np.array([[1., 0.], [0., 1.], [1., 1.]])
WQ = np.array([[1., 0.], [1., 1.]])
WK = np.array([[1., 1.], [0., 1.]])
WV = np.eye(2)

# 例 1：查询 x1。
p1 = sm(X[0] @ X.T)
out1 = p1 @ X
check("例1", np.allclose(p1, [.4223188, .1553624, .4223188]) and np.allclose(out1, [.8446376, .5776812]) and "0.8446" in LESSON)

# 例 2：三组投影。
Q = X @ WQ; K = X @ WK; V = X @ WV
check("例2", np.array_equal(Q, [[1, 0], [1, 1], [2, 1]]) and np.array_equal(K, [[1, 1], [0, 1], [1, 2]]) and "Q=\\begin{pmatrix}1&0\\\\1&1\\\\2&1\\end{pmatrix}" in LESSON)

# 例 3：完整自注意力。
S3 = Q @ K.T / np.sqrt(2)
A3 = np.array([sm(row) for row in S3])
out3 = A3 @ V
check("例3", np.allclose(A3, [[.4011,.1978,.4011],[.2840,.1400,.5760],[.3057,.0743,.6200]], atol=5e-4) and np.allclose(out3, [[.8022,.5989],[.8600,.7160],[.9257,.6943]], atol=5e-4) and "0.9257" in LESSON)

# 例 3 后的 Q=K=I 小题。
I = np.eye(2); Vq = np.array([[1.,2.],[3.,4.]])
Aq = np.array([sm(row) for row in I @ I.T / np.sqrt(2)])
outq = Aq @ Vq
check("例3小题", np.allclose(outq, [[1.6604769,2.6604769],[2.3395231,3.3395231]], atol=5e-4) and "1.6605" in LESSON)

# 例 4：三种缩放。
w_raw = sm([16., 8., 0.])
w_sqrt = sm([2., 1., 0.])
w_full = sm([.25, .125, 0.])
check("例4", np.allclose(w_raw, [.9996645,.00033535,.0000001125], atol=5e-7, rtol=0) and np.allclose(w_sqrt, [.66524096,.24472847,.09003057], atol=5e-7, rtol=0) and np.allclose(w_full, [.37575654,.33160398,.29263948], atol=5e-7, rtol=0) and all(s in LESSON for s in ["0.3758", "0.3316", "0.2926", "0.2227"]))

# 例 5：因果掩码。
Sm = S3.copy(); Sm[np.triu_indices(3,1)] = -np.inf
A5 = np.array([sm(row) for row in Sm]); out5 = A5 @ V
check("例5", np.allclose(A5, [[1,0,0],[.6698,.3302,0],[.3057,.0743,.6200]], atol=5e-4) and np.allclose(out5, [[1,0],[.6698,.3302],[.9257,.6943]], atol=5e-4) and "0.6698" in LESSON)

# 例 6：交叉注意力。
Y = np.array([[2.,0.],[0.,2.]])
Q6 = Y @ WQ
S6 = Q6 @ K.T / np.sqrt(2)
A6 = np.array([sm(row) for row in S6]); out6 = A6 @ V
check("例6", np.allclose(A6, [[.4458,.1084,.4458],[.1867,.0454,.7679]], atol=5e-5, rtol=0) and np.allclose(out6, [[.8916,.5542],[.9546,.8133]], atol=5e-5, rtol=0) and "0.7679" in LESSON)

# 随堂数值：d_k=16 与 n=2 的掩码。
check("随堂缩放", np.sqrt(16) == 4 and "除以 $\\sqrt{16}=4" in LESSON)
Ssmall = np.array([[.5,1.],[1.,2.]])
Ssmall[np.triu_indices(2,1)] = -np.inf
Asm = np.array([sm(row) for row in Ssmall])
check("随堂掩码", np.allclose(Asm, [[1,0],[.26894142,.73105858]]) and "0.7311" in LESSON)
check("随堂交叉形状", "$S$ 和 $A$ 是 $2\\times5$" in LESSON and "输出仍是 $2\\times d_v$" in LESSON)
check("首节随堂", "0.5777" in LESSON and "0.8446" in LESSON)
check("交换列随堂", "右乘这个矩阵是交换列" in LESSON and "0&1" in LESSON and "1&1" in LESSON)
