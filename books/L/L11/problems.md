## L.11 · 特征值与特征向量（题目）

| 题号 | 档 | 方法 |
|---|---|---|
| L11-01 | A | 方法 1 |
| L11-02 | A | 方法 2 |
| L11-03 | A | 方法 3 |
| L11-04 | A | 方法 4 |
| L11-05 | B | 方法 4 |
| L11-06 | B | 方法 2 |
| L11-07 | B | 方法 3 |
| L11-08 | B | 方法 4 |
| L11-09 | B | 方法 5 |
| L11-10 | B | 方法 6 |
| L11-11 | C | 方法 4 |
| L11-12 | C | 方法 6 |
| L11-13 | 混合 | L.10、方法 3、方法 4 |
| L11-14 | 混合 | L.10、方法 3、方法 4 |
| L11-15 | 混合 | L.10、方法 3、方法 4 |

### A 基础

**L11-01**〔A｜方法 1 · 考查：直接验证特征向量，并区分同一特征值的不同方向〕设
$$A=\begin{pmatrix}2&0&1\\0&3&0\\1&0&2\end{pmatrix}.$$
判断 $(1,0,1)^{\mathsf T}$、$(0,1,0)^{\mathsf T}$、$(1,1,0)^{\mathsf T}$ 是否为 $A$ 的特征向量；若是，写出对应特征值。

**L11-02**〔A｜方法 2 · 考查：二阶特征方程和特征子空间〕求
$$A=\begin{pmatrix}1&2\\2&1\end{pmatrix}$$
的全部特征值，以及每个特征值的全部特征向量。

**L11-03**〔A｜方法 3 · 考查：同时用迹和行列式确定两个参数〕设矩阵
$$A=\begin{pmatrix}a&b\\1&2\end{pmatrix}$$
的特征值为 $3,4$，求 $(a,b)$。

A. $(5,-2)$　　B. $(5,2)$　　C. $(7,-2)$　　D. $(3,2)$

**L11-04**〔A｜方法 4 · 考查：判断多项式矩阵的可逆性并计算行列式〕三阶矩阵 $A$ 的特征值为 $1,1,2$。判断 $A-3E$ 与 $A^2-3A+4E$ 是否可逆，并求
$$|A-3E|.$$

### B 进阶

**L11-05**〔B｜方法 4 · 考查：$A^{-1}$、$A^{\mathsf T}$、$A^*$ 与特征向量的关系〕设 $A$ 可逆，$A\boldsymbol v=2\boldsymbol v$，其中 $\boldsymbol v\ne\boldsymbol0$。下列说法中必然正确的是（ ）。

A. $A^{-1}\boldsymbol v=\frac12\boldsymbol v$

B. $A^{\mathsf T}\boldsymbol v=2\boldsymbol v$

C. $A^*\boldsymbol v=2\boldsymbol v$

D. $(A+E)\boldsymbol v=2\boldsymbol v$

**L11-06**〔B｜方法 2 + 方法 6 · 考查：已知特征向量、参数与重根的几何重数〕设
$$A_a=\begin{pmatrix}2&1&1\\0&2&0\\a&0&3\end{pmatrix}.$$
已知 $(1,0,1)^{\mathsf T}$ 是 $A_a$ 的特征向量。求 $a$，并求所得矩阵的重特征值及其几何重数。

**L11-07**〔B｜方法 3 + 方法 4 · 考查：迹与行列式联立后求多项式矩阵行列式〕三阶矩阵 $A$ 的特征值为 $2,a,\mu$，且
$$\operatorname{tr}A=7,\qquad |A|=12.$$
求 $a,\mu$（不必区分二者顺序），并求 $|2A-E|$。

**L11-08**〔B｜方法 4 · 考查：公共特征向量时何时可以逐项相加〕设 $A,B$ 有一组公共特征向量基 $\boldsymbol v_1,\boldsymbol v_2$，满足
$$A\boldsymbol v_i=\lambda_i\boldsymbol v_i,\qquad B\boldsymbol v_i=\mu_i\boldsymbol v_i\quad(i=1,2).$$
证明 $A+B$ 的特征值为 $\lambda_i+\mu_i$。再用
$$A=\begin{pmatrix}2&0\\0&1\end{pmatrix},\qquad B=\begin{pmatrix}-1&0\\0&3\end{pmatrix}$$
验证这个结论，并说明为什么没有公共特征向量基时不能这样做。

**L11-09**〔B｜方法 5 · 考查：多项式使两个特征值合并〕设 $A\boldsymbol v_1=\lambda_1\boldsymbol v_1$、$A\boldsymbol v_2=\lambda_2\boldsymbol v_2$，其中 $\lambda_1\ne\lambda_2$，且两个向量非零。若多项式 $f$ 满足
$$f(\lambda_1)=f(\lambda_2)=c,$$
证明只要 $\alpha\boldsymbol v_1+\beta\boldsymbol v_2\ne\boldsymbol0$，它就是 $f(A)$ 属于特征值 $c$ 的特征向量。

**L11-10**〔B｜方法 6 · 考查：非上三角参数矩阵的重数〕设
$$A_a=\begin{pmatrix}1&1&0\\-1&3&0\\a-2&2-a&a\end{pmatrix}.$$
求特征多项式，并按 $a=2$ 与 $a\ne2$ 分情况写出各特征值的代数重数和几何重数。

### C 提高

**L11-11**〔C｜方法 4 · 考查：含参数的伴随矩阵表达式何时奇异〕三阶可逆矩阵 $A$ 的特征值为 $1,2,4$。设
$$B=A^*+cA+dE.$$
求所有使 $B$ 奇异的 $(c,d)$ 所满足的条件，并说明每条条件对应哪个特征值方向。

**L11-12**〔C｜方法 6 · 考查：两参数矩阵的重根来源与几何重数〕设
$$A_{a,b}=\begin{pmatrix}1&1&0\\0&2&1\\0&a&b\end{pmatrix}.$$
(1) 求特征多项式；(2) 求使特征多项式有重根的全部实数对 $(a,b)$，并写出重根及其代数重数；(3) 对每种情形求重根的几何重数。

### 章末混合练习

**L11-13**〔B〕令 $\boldsymbol u=(1,2,2)^{\mathsf T}$，在 L.10 中由单列矩阵 $A=\boldsymbol u$ 得投影矩阵
$$P=\frac{\boldsymbol u\boldsymbol u^{\mathsf T}}{\boldsymbol u^{\mathsf T}\boldsymbol u}.$$
求 $P$ 的全部特征值及其代数、几何重数，并求 $|P+2E|$。（答案中标明所用方法。）

**L11-14**〔B〕设 $Q$ 是三阶正交矩阵，$|Q|=-1$，且 $\operatorname{tr}Q=1$。求 $Q$ 的全部特征值及其代数重数，并求 $|Q+2E|$。（答案中标明所用方法。）

**L11-15**〔B〕设三阶矩阵 $A$ 满足
$$A^2-3A+2E=O,\qquad \operatorname{tr}A=4.$$
求 $A$ 的全部可能特征值及其代数重数，并求 $|A|$。（答案中标明所用方法。）