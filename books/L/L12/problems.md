## L.12 · 相似与对角化（题目）

| 题号 | 档 | 方法 |
|---|---|---|
| L12-01 | A | 方法 1 |
| L12-02 | A | 方法 1 |
| L12-03 | A | 方法 3 |
| L12-04 | A | 方法 4 |
| L12-05 | A | 方法 5 |
| L12-06 | B | 相似不变量证明 |
| L12-07 | B | 方法 2、3 |
| L12-08 | B | 方法 2 |
| L12-09 | B | 方法 7 |
| L12-10 | B | 方法 6、7 |
| L12-11 | B | 方法 8 |
| L12-12 | C | 方法 6、7 |
| L12-13 | C | 方法 3、4、6 |
| L12-14 | C | 方法 9 |
| L12-15 | B | 章末混合 |
| L12-16 | A | 章末混合 |
| L12-17 | B | 章末混合 |
| L12-18 | C | 章末混合 |

### A 基础

**L12-01**〔A｜方法 1 · 考查：相似不变量与“全相同也未必相似”〕下列哪一对矩阵的迹、行列式和特征多项式都相同，但一定不相似？

(A) $\begin{pmatrix}1&0\\0&2\end{pmatrix}$ 与 $\begin{pmatrix}1&1\\0&2\end{pmatrix}$

(B) $E$ 与 $\begin{pmatrix}1&1\\0&1\end{pmatrix}$

(C) $\begin{pmatrix}1&0\\0&2\end{pmatrix}$ 与 $\begin{pmatrix}2&0\\0&1\end{pmatrix}$

(D) $\begin{pmatrix}1&0\\0&1\end{pmatrix}$ 与 $E$

**L12-02**〔A｜方法 1 · 考查：按定义计算相似变换〕设
$$A=\begin{pmatrix}2&1\\0&3\end{pmatrix},\qquad P=\begin{pmatrix}1&0\\1&1\end{pmatrix}.$$ 
求 $B=P^{-1}AP$，并写出 $B$ 属于特征值 $2$ 的一个特征向量。

**L12-03**〔A｜方法 3 · 考查：非对称矩阵的重根方向〕把
$$A=\begin{pmatrix}1&1&0\\0&2&0\\0&0&2\end{pmatrix}$$
对角化，写出一个 $P$ 和相应的 $\Lambda$，并用 $AP=P\Lambda$ 验算。

**L12-04**〔A｜方法 4 · 考查：只求 $A^n\boldsymbol{x}$ 时分解向量〕设 $A=\begin{pmatrix}3&1\\1&3\end{pmatrix}$，求 $A^n(2,0)^{\mathsf T}$（$n\ge0$）。

**L12-05**〔A｜方法 5 · 考查：迹为零的秩一矩阵〕设
$$A=\begin{pmatrix}2&-1\\4&-2\end{pmatrix}.$$ 
证明 $A^2=O$，并写出 $A^n$（$n\ge0$）。

### B 进阶

**L12-06**〔B｜方法 1 · 证明：相似矩阵特征多项式相同〕若 $B=P^{-1}AP$，其中 $P$ 可逆，证明 $|\lambda E-B|=|\lambda E-A|$。

**L12-07**〔B｜方法 2、3 · 考查：非三角参数矩阵的重根几何重数〕设
$$A(a)=\begin{pmatrix}3&1&-1\\2-a&2&a-2\\3-a&1&a-1\end{pmatrix}.$$ 
先求特征多项式，再判断 $A(a)$ 是否存在可对角化的 $a$；对重根分别求几何重数。

**L12-08**〔B｜方法 2 · 考查：可对角化条件辨析〕下列说法中必然正确的是（ ）。

(A) 一个 $n$ 阶矩阵有 $n$ 个互不相同的特征值时，它一定可对角化。

(B) 一个矩阵可对角化时，它的 $n$ 个特征值一定互不相同。

(C) 某个重根的几何重数小于代数重数时，矩阵仍可能可对角化。

(D) 两个矩阵特征多项式相同，就一定相似。

**L12-09**〔B｜方法 7 · 考查：三阶特征多项式余式〕设
$$A=\begin{pmatrix}0&1&0\\0&0&1\\6&-11&6\end{pmatrix}.$$ 
求 $A^{-1}$，并将 $A^5$ 写成 $c_0E+c_1A+c_2A^2$。

**L12-10**〔B｜方法 6、7 · 考查：换一个不可对角化二阶矩阵〕设 $A=\begin{pmatrix}7&2\\-8&-1\end{pmatrix}$。判断 $A$ 是否可对角化；若不能，令 $N=A-3E$，求 $A^n$（$n\ge1$）。


**L12-11**〔B｜方法 8 · 考查：由通项反求递推〕已知 $a_n=(-1)^n+2\cdot3^n$（$n\ge0$）。求它满足的二阶常系数递推式，并说明特征根是否重根。

### C 提高

**L12-12**〔C｜方法 4、6 · 考查：相似变换后的幂与向量传播〕令
$$S=\begin{pmatrix}1&1&0\\0&1&1\\1&0&1\end{pmatrix},\quad J=\begin{pmatrix}2&1&0\\0&2&0\\0&0&4\end{pmatrix},\quad A=SJS^{-1}.$$ 
求 $A^n(1,0,0)^{\mathsf T}$（$n\ge1$），并说明计算中哪一步用到了左上角二阶块 $\begin{pmatrix}2&1\\0&2\end{pmatrix}=2E+N$ 的幂（方法 6）。

拆法：先做 L12-07、L12-10。

**L12-13**〔C｜方法 3、4、6 · 考查：相似关系、二阶块 $2E+N$ 的幂和向量传播〕令
$$P=\begin{pmatrix}1&1&0\\0&1&1\\0&0&1\end{pmatrix},\quad B=\begin{pmatrix}2&1&0\\0&2&0\\0&0&3\end{pmatrix},\quad A=PBP^{-1}.$$ 
(1) 求 $A$；(2) 求 $A^n(0,0,1)^{\mathsf T}$（$n\ge1$）。

拆法：先做 L12-04、L12-10。

**L12-14**〔C｜方法 9 · 考查：稳态存在不等于从任意初值收敛〕考虑转移矩阵
$$M=\begin{pmatrix}0&1\\1&0\end{pmatrix}.$$ 
(1) 求分量和为 $1$ 的稳态；(2) 从 $\boldsymbol{x}_0=(1,0)^{\mathsf T}$ 出发写出 $\boldsymbol{x}_n$，并说明为什么不能断言 $\boldsymbol{x}_n$ 收敛到稳态。

拆法：先做 L12-05、L12-11。

### 章末混合练习

**L12-15**〔B〕已知 $A$ 与 $\operatorname{diag}(-1,2,3)$ 相似。求 $\det(A^2+E)$ 与 $\operatorname{tr}(A^{-1})$。（答案中标出所用的前章结论。）

**L12-16**〔A〕设 $\boldsymbol{u}=(1,1,0)^{\mathsf T}$、$\boldsymbol{v}=(1,0,1)^{\mathsf T}$、$\boldsymbol{w}=(0,1,1)^{\mathsf T}$。求使
$$c_1\boldsymbol{u}+c_2\boldsymbol{v}+c_3\boldsymbol{w}=(2,3,4)^{\mathsf T}$$
成立的 $c_1,c_2,c_3$，并说明表示是否唯一。

**L12-17**〔B〕用数学归纳法证明：若 $a_0=0,a_1=1,a_{n+2}=a_{n+1}+2a_n$，则
$$a_n=\frac{2^n-(-1)^n}{3}.$$ 
再求 $a_5$。答案中标出所用的前章证明方法。

**L12-18**〔C｜章末混合 · 考查：三阶行稳态与左右特征向量〕设
$$R=\begin{pmatrix}\frac12&\frac12&0\\\frac15&\frac12&\frac3{10}\\0&\frac25&\frac35\end{pmatrix}$$
的每行和为 $1$。求分量和为 $1$ 的行向量 $\boldsymbol{\pi}$，使 $\boldsymbol{\pi}R=\boldsymbol{\pi}$；再说明为什么直接解 $(R-E)\boldsymbol{x}=\boldsymbol{0}$ 得到的不是这个行稳态。

拆法：先做 L12-08、L12-14。
