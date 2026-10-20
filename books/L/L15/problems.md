## L.15 · 奇异值分解（题目）

| 题号 | 档 | 方法 |
|---|---|---|
| L15-01 | A | 方法 1 |
| L15-02 | A | 方法 2 |
| L15-03 | A | 方法 2（选择） |
| L15-04 | A | 方法 3 |
| L15-05 | A | 方法 5（选择） |
| L15-06 | B | 方法 2 |
| L15-07 | B | 方法 2、5（选择） |
| L15-08 | B | 方法 1、2（证明） |
| L15-09 | B | 方法 4（选择） |
| L15-10 | B | 方法 6 |
| L15-11 | C | 方法 3、4 |
| L15-12 | C | 方法 5 |
| L15-13 | B | 混合 |
| L15-14 | A | 混合 |
| L15-15 | C | 混合 |

### A 基础

**L15-01**〔A｜方法 1 · 考查：矩形矩阵列正交时直接读出 SVD〕设
$$
A=\begin{pmatrix}1&0\\1&0\\0&2\end{pmatrix}.
$$
写出一组奇异值分解 $A=U\Sigma V^{\mathsf T}$，并列出奇异值。

**L15-02**〔A｜方法 2 · 考查：奇异值是 $A^{\mathsf T}A$ 特征值的平方根〕设
$$
A=\begin{pmatrix}1&2\\2&1\end{pmatrix}.
$$
求奇异值，并给出一组相应的单位右、左奇异向量，使得 $A\boldsymbol v_i=\sigma_i\boldsymbol u_i$。

**L15-03**〔A｜方法 2 · 考查：长方矩阵的 $\Sigma$ 形状与补全 $U$〕（选择）设
$$
A=\begin{pmatrix}1&0\\0&2\\0&0\end{pmatrix}.
$$
下列说法正确的是（　）。

(A) 奇异值是 $1,2$，所以可取 $\Sigma=\operatorname{diag}(2,1)$。

(B) $A^{\mathsf T}A$ 的特征值为 $1,4$，所以奇异值按从大到小为 $2,1$。

(C) 只要分别求出 $AA^{\mathsf T}$、$A^{\mathsf T}A$ 的单位特征向量，就可以任意配对作为 $U,V$ 的列。

(D) 因为 $A$ 有三行，所以必须有三个正奇异值。

**L15-04**〔A｜方法 3 · 考查：秩 1 外积、秩和四个子空间〕设
$$
A=\begin{pmatrix}2&-2&1\\4&-4&2\end{pmatrix}
=\begin{pmatrix}1\\2\end{pmatrix}\begin{pmatrix}2&-2&1\end{pmatrix}.
$$
求 $A$ 的非零奇异值、秩，并给出列空间、零空间、行空间、左零空间的规范正交基。

**L15-05**〔A｜方法 5 · 考查：谱范数、弗罗贝尼乌斯范数和截断误差〕（选择）已知矩阵 $A$ 的奇异值为 $4,2,1$。下列说法正确的是（　）。

(A) $\lVert A\rVert_2=7$。

(B) $\lVert A\rVert_F=5$。

(C) 最佳秩 1 近似的弗罗贝尼乌斯误差为 $\sqrt5$。

(D) 最佳秩 2 近似的谱范数误差为 $2$。

### B 进阶

**L15-06**〔B｜方法 2 · 考查：从 $AA^{\mathsf T}$ 构造 SVD并处理重复奇异值〕设
$$
A=\begin{pmatrix}1&1&0\\1&-1&0\end{pmatrix}.
$$
已知 $m<n$。请从 $AA^{\mathsf T}$ 出发，给出一组完整的 $U,\Sigma,V$，并说明重复奇异值时为什么可以在对应子空间内协调选取左右基。

**L15-07**〔B｜方法 2、5 · 考查：何时不能把特征值直接当奇异值〕（选择）设
$$
A=\begin{pmatrix}1&-2\\2&1\end{pmatrix}.
$$
下列说法正确的是（　）。

(A) $A$ 的特征值为 $1+2\mathrm i,1-2\mathrm i$，所以奇异值为 $1,2$。

(B) $A^{\mathsf T}A=5E$，所以两个奇异值都是 $\sqrt5$。

(C) $\lVert A\rVert_2$ 等于矩阵中最大元素的绝对值，即为 $2$。

(D) 因为 $A$ 不对称，所以它没有奇异值分解。

**L15-08**〔B｜方法 1、2 · 考查：正交左乘不改变奇异值〕设 $A$ 是 $m\times n$ 矩阵，$Q$ 是 $m$ 阶正交矩阵（$Q^{\mathsf T}Q=E$）。证明：$QA$ 与 $A$ 的奇异值完全相同。只写出讲义给过的短证明骨架即可。

**L15-09**〔B｜方法 4 · 考查：满行秩时比较两个投影〕（选择）设
$$
A=\begin{pmatrix}1&0&1\\0&1&1\end{pmatrix}.
$$
下列说法正确的是（　）。

(A) $AA^+=\begin{pmatrix}1&0\\0&1\end{pmatrix}$，而 $A^+A$ 是到行空间的正交投影。

(B) $A^+A=E$，因为 $A$ 的两行线性无关。

(C) $AA^+$ 是 $3\times3$ 矩阵，$A^+A$ 是 $2\times2$ 矩阵。

(D) $A^+=(A^{\mathsf T}A)^{-1}A^{\mathsf T}$，因为 $A^{\mathsf T}A$ 可逆。

**L15-10**〔B｜方法 6 · 考查：第二主方向、双主成分重建和符号等价〕某数据表中心化后为
$$
X=\begin{pmatrix}
3&2&1\\3&-2&-1\\-3&2&-1\\-3&-2&1
\end{pmatrix}.
$$
求第一、第二主成分方向，求保留两个主成分时的平方和重建误差，并说明主方向整体变号是否改变主成分。

### C 提高

**L15-11**〔C｜方法 3、4 · 考查：不相容系统的最小二乘解与零空间〕设
$$
A=\begin{pmatrix}1&0&0\\0&1&0\\1&1&0\end{pmatrix},\qquad
\boldsymbol b=\begin{pmatrix}1\\0\\0\end{pmatrix}.
$$
求长度最小的最小二乘解，并说明零空间如何影响全部最小二乘解。

**L15-12**〔C｜方法 5 · 考查：非对角矩阵的最佳秩 1 近似和谱范数下界〕设
$$
A=\begin{pmatrix}3&1&0\\1&3&0\\0&0&0\end{pmatrix}.
$$
写出一个最佳秩 1 近似 $A_1$，求两种误差；再证明任意秩不超过 $1$ 的 $B$ 都满足 $\lVert A-B\rVert_2\ge2$，并举出一个使等号成立的 $B$。

### 章末混合练习

**L15-13**〔B〕设
$$
A=\begin{pmatrix}1&2\\2&1\end{pmatrix}.
$$
求 $\max_{\lVert\boldsymbol x\rVert=1}\lVert A\boldsymbol x\rVert$，并写出所有取到最大值的单位向量。

**L15-14**〔A〕设
$$
A=\begin{pmatrix}1&0\\0&1\\1&1\end{pmatrix},\qquad
\boldsymbol b=\begin{pmatrix}1\\2\\0\end{pmatrix}.
$$
求 $A(A^{\mathsf T}A)^{-1}A^{\mathsf T}\boldsymbol b$，并说明所得向量与列空间的关系。

**L15-15**〔C〕设
$$
A=\begin{pmatrix}1&1&0\\2&2&0\end{pmatrix},\qquad
\boldsymbol b=\begin{pmatrix}1\\0\end{pmatrix}.
$$
先求最小二乘问题的最短解，再用 SVD 写出 $A^+$ 并验证该解与零空间正交。
