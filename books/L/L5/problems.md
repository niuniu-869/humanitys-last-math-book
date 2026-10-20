## L.5 · 逆矩阵（题目）

| 题号 | 档 | 方法 |
|---|---|---|
| L5-01 | A | 方法 1 |
| L5-02 | A | 方法 1 |
| L5-03 | A | 方法 2 |
| L5-04 | A | 方法 4 |
| L5-05 | B | 方法 2 |
| L5-06 | B | 方法 2 |
| L5-07 | B | 方法 3 |
| L5-08 | B | 方法 4 |
| L5-09 | B | 方法 4 |
| L5-10 | B | 方法 3 |
| L5-11 | B | 方法 4 |
| L5-12 | C | 方法 4 |
| L5-13 | B | 方法 4 |
| L5-14 | — | 章末混合 |
| L5-15 | — | 章末混合 |
| L5-16 | — | 章末混合 |
| L5-17 | — | 章末混合 |

### A 基础

**L5-01**〔A｜方法 1 · 考查：二阶公式与回代检验〕求
\[
A=\begin{pmatrix}3&2\\1&1\end{pmatrix}
\]
的逆矩阵，并用它解 $A\boldsymbol{x}=(7,3)^{\mathsf T}$。

**L5-02**〔A｜方法 1 · 考查：逆矩阵运算律〕设 $A,B$ 为同阶可逆方阵，且 $A+B$ 可逆，$k\ne0$。下列命题中恒成立的是（ ）。

A. $(AB)^{-1}=A^{-1}B^{-1}$  
B. $(A+B)^{-1}=A^{-1}+B^{-1}$  
C. $(A^{\mathsf T})^{-1}=(A^{-1})^{\mathsf T}$  
D. $(kA)^{-1}=kA^{-1}$

**L5-03**〔A｜方法 2 · 考查：主元判据与零空间证据〕判断
\[
M=\begin{pmatrix}1&2&0\\0&1&1\\1&3&1\end{pmatrix}
\]
是否可逆；若不可逆，给出一个非零向量 $\boldsymbol{x}$ 使 $M\boldsymbol{x}=\boldsymbol{0}$。

**L5-04**〔A｜方法 4 · 考查：$XA=B$ 时从右侧消去〕解矩阵方程
\[
X\begin{pmatrix}1&2\\0&1\end{pmatrix}=\begin{pmatrix}2&5\\1&3\end{pmatrix}。
\]

### B 进阶

**L5-05**〔B｜方法 2 · 考查：方阵条件与单边逆〕设矩阵乘法均有意义。下列说法中正确的是（ ）。

A. 只要 $AB=E$，无论 $A,B$ 是否为方阵，都有 $BA=E$。  
B. 若 $A,B$ 是同阶方阵且 $AB=E$，则 $B=A^{-1}$。  
C. $A\ne O$ 就一定可逆。  
D. $A\boldsymbol{x}=\boldsymbol{b}$ 对某个 $\boldsymbol{b}$ 有解，就能推出 $A$ 可逆。

**L5-06**〔B｜方法 2 · 证明题〕设 $A$ 为 $n$ 阶方阵，且 $A^2=A$、$A\ne E$。证明 $A$ 不可逆。

**L5-07**〔B｜方法 3 · 考查：初等矩阵乘积求逆〕设
\[
E_1=\begin{pmatrix}0&1\\1&0\end{pmatrix},\quad
E_2=\begin{pmatrix}1&0\\2&1\end{pmatrix},\quad
E_3=\begin{pmatrix}1&3\\0&1\end{pmatrix},\quad P=E_3E_2E_1。
\]
利用初等矩阵的逆和乘积逆矩阵次序求 $P^{-1}$，并验证 $PP^{-1}=E$。

**L5-08**〔B｜方法 4 · 考查：整理矩阵方程和因子位置〕设
\[
A=\begin{pmatrix}2&1\\0&3\end{pmatrix}，
\]
求满足 $AX+E=2A$ 的矩阵 $X$。

**L5-09**〔B｜方法 4 · 考查：看似能套逆矩阵、实际不可逆〕设
\[
A=\begin{pmatrix}1&2\\2&4\end{pmatrix},\qquad B=\begin{pmatrix}1&0\\2&1\end{pmatrix}。
\]
关于方程 $AX=B$，下列说法中正确的是（ ）。

A. $A$ 可逆，唯一解为 $X=A^{-1}B$。  
B. $A$ 不可逆，但仍可用 $(A\mid B)\to(E\mid X)$ 求出唯一解。  
C. 方程无解，因为 $A$ 的两行成比例而 $B$ 的两行不成比例。  
D. 方程有无穷多解，因为未知量 $X$ 有四个分量。

**L5-10**〔B｜方法 3 · 考查：分块对角矩阵〕设
\[
M=\begin{pmatrix}A_1&O\\O&A_2\end{pmatrix}，
\]
其中 $A_1,A_2$ 是方阵。证明 $M$ 可逆当且仅当 $A_1,A_2$ 都可逆；在可逆时写出 $M^{-1}$。再判断
\[
A_1=\begin{pmatrix}1&2\\0&1\end{pmatrix},\qquad A_2=\begin{pmatrix}1&1\\1&1\end{pmatrix}
\]
对应的 $M$ 是否可逆，并说明理由。

**L5-11**〔B｜方法 4 · 考查：含左右乘法的矩阵方程〕设
\[
A=\begin{pmatrix}2&1\\0&3\end{pmatrix}，
\]
求满足
\[
AXA^{-1}=XA^{-1}+3E
\]
的矩阵 $X$。

拆法：先做 L5-04、L5-08。

**L5-13**〔B｜方法 4 · 考查：奇异右因子下的矩阵方程〕设
\[
C=\begin{pmatrix}1&2\\2&4\end{pmatrix},\qquad D=\begin{pmatrix}3&6\\1&2\end{pmatrix}。
\]
(1) 求矩阵方程 $XC=D$ 的全部解，并说明为什么解不唯一；(2) 若把 $D$ 的第二行改为 $(1,3)$，判断新的方程是否有解，并说明理由。

拆法：先做 L5-09，再按行看矩阵方程。

### C 提高

**L5-12**〔C｜方法 4 · 考查：由总产出和最终需求反求系数〕某三部门的直接消耗系数矩阵为
\[
C=\begin{pmatrix}0&c&0\\0&0&\frac14\\0&0&0\end{pmatrix},\qquad c\ge0。
\]
已知最终需求为 $\boldsymbol d=(3,4,5)^{\mathsf T}$，总产出为 $\boldsymbol x=(\frac{19}{4},\frac{21}{4},5)^{\mathsf T}$。(1) 求 $c$；(2) 说明在本题给定的 $c$ 下，$(E-C)\boldsymbol x=\boldsymbol d$ 的解是否唯一；(3) 检查 $C$ 的各项是否符合非负直接消耗系数的要求。

拆法：先做 L5-08，再回看第 5 节。

### 章末混合练习

**L5-14** 设 $T:\mathbb R^2\to\mathbb R^2$ 的标准矩阵为 $X$，且
\[
T(1,0)^{\mathsf T}=(2,1)^{\mathsf T},\qquad T(1,1)^{\mathsf T}=(3,3)^{\mathsf T}。
\]
求 $T(0,1)^{\mathsf T}$ 和 $T(2,-1)^{\mathsf T}$，并写出 $X$。（涉及 L.3 的线性变换与向量运算。）

**L5-15** 已知初等矩阵
\[
E_1=\begin{pmatrix}1&0\\2&1\end{pmatrix},\qquad E_2=\begin{pmatrix}1&-1\\0&1\end{pmatrix}，
\]
令 $P=E_2E_1$。求 $P^{-1}$，并验证 $PP^{-1}=E$。（涉及 L.4 的初等矩阵和本章逆的乘积律。）

**L5-16** 设 $A=\begin{pmatrix}1&2\\2&4\end{pmatrix}$，判断方程组 $A\boldsymbol{x}=(3,6)^{\mathsf T}$ 的解的个数，并写出全部解；再判断 $A\boldsymbol{x}=(3,5)^{\mathsf T}$ 是否有解。（涉及 L.3、L.4 的齐次方程与主元。）

**L5-17** 设
\[
A=\begin{pmatrix}1&2\\2&4\end{pmatrix},\quad B=E,\quad C=\begin{pmatrix}3&0\\-1&1\end{pmatrix}。
\]
验证 $B\ne C$ 但 $AB=AC$，并说明这个反例表明约分时缺少哪条条件。（涉及矩阵等式的结合律与本章约分。）
