## L.3 · 矩阵是线性变换（题目）

| 题号 | 档 | 方法 |
|---|---|---|
| L3-01 | A | 方法 1 |
| L3-02 | A | 方法 2 |
| L3-03 | A | 方法 3 |
| L3-04 | A | 方法 4 |
| L3-05 | A | 方法 3 |
| L3-06 | B | 方法 4 |
| L3-07 | B | 方法 5 |
| L3-08 | B | 方法 5 |
| L3-09 | B | 方法 6 |
| L3-10 | B | 方法 7 |
| L3-11 | C | 方法 4、6 |
| L3-12 | C | 方法 2、5、7 |
| L3-13 | — | 方法 2、6 |
| L3-14 | — | 方法 3 |
| L3-15 | — | 方法 2、6 |

### A 基础

**L3-01**〔A｜方法 1 · 考查：先查形状，再按行与按列计算〕设
$$A=\begin{pmatrix}1&-2&0\\2&1&3\end{pmatrix},\qquad \boldsymbol{x}=(2,-1,1)^{\mathsf T}.$$
判断乘积是否有定义，并求 $A\boldsymbol{x}$。再用列的线性组合写出同一个结果。

**L3-02**〔A｜方法 2 · 考查：矩阵的列是基向量的像〕设
$$A=\begin{pmatrix}0&-1\\1&0\end{pmatrix}.$$
下列说法正确的是（ ）。

(A) $\boldsymbol e_1$ 变到 $(0,1)^{\mathsf T}$，$\boldsymbol e_2$ 变到 $(-1,0)^{\mathsf T}$，单位正方形变成一个保持边长的正方形

(B) $\boldsymbol e_1$ 变到第一行 $(0,-1)^{\mathsf T}$，所以这是顺时针旋转 $90^\circ$

(C) 两列是像的行向量，单位正方形的四个顶点只需看矩阵的对角元

(D) 因为两列互相垂直，所以单位正方形被压成一条线段

**L3-03**〔A｜方法 3 · 考查：线性要同时满足可加性与齐次性〕下列变换中，线性变换是（ ）。

(A) $T(x,y)=(x+1,y)$

(B) $T(x,y)=(x-y,\,2x+y)$

(C) $T(x,y)=(xy,y)$

(D) $T(x,y)=(|x|,y)$

**L3-04**〔A｜方法 4 · 考查：矩阵乘法的次序与形状〕设
$$A=\begin{pmatrix}1&0&2\\0&1&-1\end{pmatrix},\qquad P=\frac12\begin{pmatrix}1&1&0\\1&1&0\\0&0&0\end{pmatrix}.$$
判断 $AP$ 与 $PA$ 哪一个有定义，写出有定义的乘积及其形状，并说明为什么不能把两个次序都当作复合矩阵。

**L3-05**〔A｜方法 3 · 考查：带偏置的变换不是线性变换〕设变换 $T:\mathbb R^2\to\mathbb R^2$ 为
$$T(\boldsymbol{x})=\begin{pmatrix}1&-1\\2&0\end{pmatrix}\boldsymbol{x}+\begin{pmatrix}1\\-2\end{pmatrix}.$$
这里先不做中间的非线性处理。对输入 $(2,3)^{\mathsf T}$ 求输出，并判断 $T$ 是否线性。下列说法正确的是（ ）。

(A) 输出为 $(0,2)^{\mathsf T}$，且 $T$ 线性，因为每个输出都是输入的加权和

(B) 输出为 $(-1,4)^{\mathsf T}$，且 $T$ 线性，因为矩阵部分线性

(C) 输出为 $(0,2)^{\mathsf T}$，但 $T$ 不线性，因为 $T(\boldsymbol0)\ne\boldsymbol0$

(D) 输出为 $(1,-2)^{\mathsf T}$，但 $T$ 不线性，因为矩阵不能乘向量

### B 进阶

**L3-06**〔B｜方法 4 · 考查：零因子与不能约去〕设
$$A=\begin{pmatrix}1&0\\0&0\end{pmatrix},\qquad B=\begin{pmatrix}0&0\\1&0\end{pmatrix}.$$
已知 $AB=O$ 且 $A\ne O$、$B\ne O$。再构造一个非零矩阵 $C$ 使 $CA=O$，并说明为什么不能从 $AB=O$ 约去 $A$ 得到 $B=O$。

**L3-07**〔B｜方法 5 · 考查：不交换时保留乘法次序〕设
$$A=\begin{pmatrix}1&1\\0&0\end{pmatrix},\qquad B=\begin{pmatrix}0&0\\1&0\end{pmatrix},$$
且 $AB\ne BA$。判断下列等式哪些成立，并说明理由：

(A) $(A+B)^2=A^2+AB+BA+B^2$

(B) $(A+B)^2=A^2+2AB+B^2$

(C) $(A-B)(A+B)=A^2-B^2$

(D) $(A+B)(A-B)=A^2-B^2$

**L3-08**〔B｜方法 5 · 考查：由低次关系降次〕设方阵 $A$ 满足
$$A^2=4A-3E.$$
证明
$$A^5=121A-120E.$$

**L3-09**〔B｜方法 6 · 考查：上三角矩阵的乘积〕设 $A=(a_{ij})$、$B=(b_{ij})$ 都是 $n$ 阶上三角矩阵。
证明 $AB$ 仍是上三角矩阵，并证明 $(AB)_{ii}=a_{ii}b_{ii}$（$i=1,\dots,n$）。

**L3-10**〔B｜方法 7 · 考查：外积的列与幂〕设
$$A=\boldsymbol\alpha\boldsymbol\beta^{\mathsf T},\qquad \boldsymbol\alpha=(1,2,-1)^{\mathsf T},\quad \boldsymbol\beta=(2,0,1)^{\mathsf T}.$$
求 $A$ 的第 2 列，说明 $A$ 的每一列都是 $\boldsymbol\alpha$ 的倍数，并求 $A^4$。

### C 提高

**L3-11**〔C｜方法 4、6 · 考查：旋转矩阵的交换关系与对称性〕设
$$R=\begin{pmatrix}0&-1\\1&0\end{pmatrix},\qquad X=\begin{pmatrix}a&b\\c&d\end{pmatrix}.$$
(1) 求满足 $RX=XR$ 的全部 $X$；(2) 在这些 $X$ 中，哪些还是对称矩阵？请说明理由。

**L3-12**〔C｜方法 2、5、7 · 考查：分块幂中同时识别旋转块与幂零块〕令
$$R=\begin{pmatrix}0&-1\\1&0\end{pmatrix},\qquad J=\begin{pmatrix}-1&2\\0&-1\end{pmatrix},\qquad M=\begin{pmatrix}R&O\\O&J\end{pmatrix}.$$
求 $M^n$ 的分块表达式（$n$ 为正整数），并写出 $M^4$。

拆法：先做 L3-02、L3-08，再按分块乘法处理。

### 章末混合练习

**L3-13**〔B〕设
$$P=\frac1{10}\begin{pmatrix}1&3\\3&9\end{pmatrix},$$
且已知 $P^{\mathsf T}=P$、$P^2=P$。
(1) 求被 $P$ 保持不动的全部向量，以及被 $P$ 送到原点的全部向量；(2) 说明 $P$ 是投影到哪条直线上的矩阵；(3) 求 $P(2,1)^{\mathsf T}$。

**L3-14**〔B〕设 $u=(1,0,1)^{\mathsf T}$、$v=(0,1,1)^{\mathsf T}$、$w=(1,1,0)^{\mathsf T}$，并规定线性变换 $T:\mathbb R^3\to\mathbb R^3$ 满足
$$T(u)=(1,0,0)^{\mathsf T},\quad T(v)=(0,1,0)^{\mathsf T},\quad T(w)=(0,0,1)^{\mathsf T}.$$
先把 $(2,3,4)^{\mathsf T}$ 写成 $u,v,w$ 的线性组合，再求 $T(2,3,4)^{\mathsf T}$。

**L3-15**〔C〕设 $\boldsymbol a=(2,-1)^{\mathsf T}$，把 $\boldsymbol x$ 垂直投影到直线 $\{s\boldsymbol a\}$ 得到 $P\boldsymbol x$。题目给出提示：关于这条直线的镜像点可写成 $2P\boldsymbol x-\boldsymbol x$。
(1) 求投影矩阵 $P$ 与镜像变换矩阵 $F$；(2) 求 $\boldsymbol y=(1,3)^{\mathsf T}$ 的镜像；(3) 验证 $F^2=E$，并解释这和“镜像做两次回到原来的点（原向量）”相符。

拆法：先做 L3-13（对称幂等矩阵的像与核）、L3-14（把变换写成矩阵）。
