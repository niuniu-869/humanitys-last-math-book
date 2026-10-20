## L.13 · 实对称矩阵（题目）

| 题号 | 档 | 方法 |
|---|---|---|
| L13-01 | A | 方法 1 |
| L13-02 | A | 方法 2 |
| L13-03 | A | 方法 3 |
| L13-04 | A | 方法 4 |
| L13-05 | A | 方法 5 |
| L13-06 | B | 方法 1（证明） |
| L13-07 | B | 方法 2 |
| L13-08 | B | 方法 3 |
| L13-09 | B | 方法 4 |
| L13-10 | B | 方法 5 |
| L13-11 | B | 方法 5（应用） |
| L13-12 | C | 方法 5（证明） |
| L13-13 | C | 方法 5、跨章 |
| L13-14 | C | 方法 1、2 |
| L13-15 | B | 混合 |
| L13-16 | A | 混合 |
| L13-17 | C | 混合 |
| L13-18 | B | 混合 |

### A 基础

**L13-01**〔A｜方法 1 · 考查：反对称矩阵特征值的实部〕设实矩阵 $A^{\mathsf T}=-A$，且 $A\boldsymbol v=\lambda\boldsymbol v$，$\boldsymbol v\ne\boldsymbol0$。用“把 $\bar{\boldsymbol v}^{\mathsf T}A\boldsymbol v$ 算两遍”的方法证明 $\lambda$ 的实部为零（记作 $\operatorname{Re}\lambda=0$）。再求 $\begin{pmatrix}0&-2\\2&0\end{pmatrix}$ 的特征值。

**L13-02**〔A｜方法 2 · 考查：用正交补补出单根特征向量〕三阶实对称矩阵 $A$ 的特征值为 $-1,2,5$，属于 $-1,2$ 的特征向量分别为 $\boldsymbol u=(1,1,0)^{\mathsf T}$、$\boldsymbol v=(1,-1,2)^{\mathsf T}$。求属于 $5$ 的全部特征向量。

**L13-03**〔A｜方法 3 · 考查：正交可对角化的充要条件〕（选择）下列说法正确的是（ ）。

(A) 每个实对称矩阵都能用正交矩阵对角化。

(B) 能用正交矩阵对角化的实矩阵一定对称。

(C) 实特征值全为实数，就足以保证矩阵能用正交矩阵对角化。

(D) 矩阵有重特征值时，特征空间的任意一组基都两两正交。

**L13-04**〔A｜方法 4 · 考查：参数矩阵的正交对角化〕令 $A_t=\begin{pmatrix}2&t\\t&2\end{pmatrix}$，$Q=\frac1{\sqrt2}\begin{pmatrix}1&1\\1&-1\end{pmatrix}$。(1) 求 $Q^{\mathsf T}A_tQ$；(2) 当 $t>2$ 时，说明所得对角矩阵的两个对角元一正一负，并按从大到小排列它们。

**L13-05**〔A｜方法 5 · 考查：由一个特征方向读出其余谱信息〕令 $A=\begin{pmatrix}3&1&1\\1&3&1\\1&1&3\end{pmatrix}$，且 $\boldsymbol q=\frac1{\sqrt3}(1,1,1)^{\mathsf T}$。已知 $A\boldsymbol q=5\boldsymbol q$。求 $A$ 在 $\boldsymbol q$ 的正交补上的特征值，并求 $A(1,-1,0)^{\mathsf T}$。

### B 进阶

**L13-06**〔B｜方法 1 · 考查：正交矩阵的实特征值〕证明：若实矩阵 $Q$ 满足 $Q^{\mathsf T}Q=E$，且 $Q\boldsymbol v=\lambda\boldsymbol v$ 有非零实特征向量 $\boldsymbol v$，则 $\lambda=1$ 或 $\lambda=-1$。再说明旋转矩阵 $R=\begin{pmatrix}0&-1\\1&0\end{pmatrix}$ 为什么没有非零实特征向量。

**L13-07**〔B｜方法 2 · 考查：正交补何时仍是不变方向〕设 $B_t=\begin{pmatrix}1&t\\0&2\end{pmatrix}$，已知 $(1,0)^{\mathsf T}$ 是特征值 $1$ 的特征向量。求 $t$ 取何值时，它的正交补仍是 $B_t$ 的一个特征方向，并写出此时的另一个特征值。

**L13-08**〔B｜方法 3 · 考查：同特征多项式不等于相似〕令 $A=\operatorname{diag}(1,1,2)$，$B=\begin{pmatrix}1&1&0\\0&1&0\\0&0&2\end{pmatrix}$。(1) 说明二者特征多项式相同；(2) 比较特征值 $1$ 的几何重数，判断 $A,B$ 是否相似。

**L13-09**〔B｜方法 4 · 考查：由方程描述的特征空间先求基再正交化〕已知三阶实对称矩阵 $A$ 的特征值为 $2,2,5$，且特征值 $2$ 的特征空间为 $x_1+x_2+x_3=0$。先从这个方程求一组基，再在该空间内施密特正交化；最后补上特征值 $5$ 的单位特征向量，写出一个正交矩阵 $Q$ 及相应的 $\Lambda$。

**L13-10**〔B｜方法 5 · 考查：多项式作用在特征方向上〕设 $A=2E+3\boldsymbol q\boldsymbol q^{\mathsf T}$，其中 $\boldsymbol q=\frac1{\sqrt3}(1,-1,1)^{\mathsf T}$。令 $p(s)=s^2-3s+1$，求 $p(A)(1,2,0)^{\mathsf T}$。

**L13-11**〔B｜方法 5 · 考查：未中心化数据的协方差〕三个二维数据点为 $(1,1)^{\mathsf T},(3,3)^{\mathsf T},(2,0)^{\mathsf T}$。先求均值并中心化，再按讲义的 $1/m$ 约定求协方差矩阵 $C$，最后求沿单位方向的最大方差值。

### C 提高

**L13-12**〔C｜方法 5 · 考查：谱分解与矩阵幂的归纳〕设 $A$ 是实对称矩阵，只有两个特征值 $\lambda,\mu$，其中 $\mu$ 为单根，且其单位特征向量为 $\boldsymbol q$。证明对任意正整数 $k$，$A^k=\lambda^kE+(\mu^k-\lambda^k)\boldsymbol q\boldsymbol q^{\mathsf T}$。

**L13-13**〔C｜方法 5 · 考查：幂等矩阵、秩与谱分解的综合〕设三阶实对称矩阵 $A$ 满足 $A^2=A$ 且 $r(A)=2$。(1) 证明 $A$ 的特征值只能是 $0,1$；(2) 写出一个正交对角化的形式，并求 $|A+E|$；(3) 说明 $A$ 是到某个二维子空间的正交投影。

**L13-14**〔C｜方法 1、2 · 考查：复特征值时正交性定理为何不能启动〕令 $R=\begin{pmatrix}0&-1\\1&0\end{pmatrix}$。(1) 求其复特征值；(2) 说明为什么本章“实对称矩阵的特征向量正交”不能用于 $R$，并说明它没有非零实特征向量。

### 章末混合练习

**L13-15**〔B〕令 $A=\begin{pmatrix}2&1\\1&2\end{pmatrix}$。不直接乘开 $A^6$，求 $A^6(1,-1)^{\mathsf T}$ 与 $A^6(1,1)^{\mathsf T}$。（答案标注：L.12 的对角化与本章正交特征向量。）

**L13-16**〔A〕令 $\boldsymbol q=\frac1{\sqrt5}(1,2)^{\mathsf T}$，$P=\boldsymbol q\boldsymbol q^{\mathsf T}$。(1) 验证 $P^2=P$；(2) 求 $P(3,4)^{\mathsf T}$。（答案标注：L.10 投影矩阵。）

**L13-17**〔C〕三阶实对称矩阵 $A$ 的特征值为 $0,2,2$，属于 $0$ 的单位特征向量为 $\boldsymbol q=\frac1{\sqrt3}(1,1,1)^{\mathsf T}$。求 $A$，并判断方程 $A\boldsymbol x=(1,0,1)^{\mathsf T}$ 是否有解。（答案标注：方法 5 与线性方程组。）

**L13-18**〔B〕若 $A=Q\Lambda Q^{\mathsf T}$，其中 $Q$ 正交、$\Lambda=\operatorname{diag}(\lambda_1,\lambda_2,\lambda_3)$，证明 $A^{\mathsf T}=A$，并说明 $\operatorname{tr}A=\lambda_1+\lambda_2+\lambda_3$。（答案标注：L.3 转置与迹的运算。）
