## L.8 · 向量空间（题目）

| 题号 | 档 | 方法 |
|---|---|---|
| L8-01 | A | 方法 1 |
| L8-02 | A | 方法 2 |
| L8-03 | A | 方法 3 |
| L8-04 | A | 方法 4 |
| L8-05 | B | 方法 1 |
| L8-06 | B | 方法 3 |
| L8-07 | B | 方法 5 |
| L8-08 | B | 方法 4 |
| L8-09 | B | 方法 5 |
| L8-10 | B | 方法 3 |
| L8-11 | C | 方法 5 |
| L8-12 | 章末混合 | 交集与线性方程组 |
| L8-13 | 章末混合 | 方法 6、7与换基 |
| L8-14 | 章末混合 | 方法 4、5与线性方程组 |

### A 基础

**L8-01**〔A｜方法 1 · 考查：零向量、封闭性与并集的辨别〕下列集合中是 $\mathbb{R}^3$ 子空间的是（　）。

(A) $\{\boldsymbol{x}:x_1+x_2+x_3=1\}$

(B) $\{\boldsymbol{x}:x_1x_2=0\}$

(C) $\{\boldsymbol{x}:x_1=x_2=x_3\}$

(D) $\{\boldsymbol{x}:x_1^2+x_2^2+x_3^2=1\}$

**L8-02**〔A｜方法 2 · 考查：取原矩阵主元列并扩充基〕设
$\boldsymbol{v}_1=(1,0,1,0)^{\mathsf T}$，$\boldsymbol{v}_2=(0,1,1,1)^{\mathsf T}$，$\boldsymbol{v}_3=(1,1,2,1)^{\mathsf T}$，$\boldsymbol{v}_4=(0,0,1,1)^{\mathsf T}$，令 $V=\operatorname{span}(\boldsymbol{v}_1,\boldsymbol{v}_2,\boldsymbol{v}_3,\boldsymbol{v}_4)$。求 $V$ 的一组基和维数，并把这组基扩充成 $\mathbb{R}^4$ 的一组基。

**L8-03**〔A｜方法 3 · 考查：过渡矩阵方向与坐标变换〕设 $(\boldsymbol{\alpha}_1,\boldsymbol{\alpha}_2,\boldsymbol{\alpha}_3)$ 是旧基，
$\boldsymbol{\beta}_1=\boldsymbol{\alpha}_1+\boldsymbol{\alpha}_2$，$\boldsymbol{\beta}_2=\boldsymbol{\alpha}_1-\boldsymbol{\alpha}_2$，$\boldsymbol{\beta}_3=\boldsymbol{\alpha}_3$。求从旧基到新基的过渡矩阵 $P$，并求旧坐标为 $(3,1,2)^{\mathsf T}$ 的向量在新基下的坐标。

**L8-04**〔A｜方法 4 · 考查：由零空间反求约束与秩〕设
$N=\operatorname{span}\{(1,1,0)^{\mathsf T},(0,0,1)^{\mathsf T}\}\subset\mathbb R^3$。求一个没有零行的矩阵 $A$，使 $N(A)=N$，并求 $r(A)$ 与 $\dim N(A)$。

### B 进阶

**L8-05**〔B｜方法 1 · 考查：交与并的封闭性证明〕设 $W_1,W_2$ 是 $\mathbb{R}^n$ 的子空间。证明 $W_1\cap W_2$ 是子空间，并证明 $W_1\cup W_2$ 是子空间当且仅当 $W_1\subseteq W_2$ 或 $W_2\subseteq W_1$。

**L8-06**〔B｜方法 3 · 考查：复合过渡矩阵与坐标变换〕设旧基为 $(\boldsymbol\alpha)$，中间基为 $(\boldsymbol\beta)$，新基为 $(\boldsymbol\gamma)$，且
$$(\boldsymbol\beta)=(\boldsymbol\alpha)P,\quad P=\begin{pmatrix}1&1\\1&-1\end{pmatrix},\qquad (\boldsymbol\gamma)=(\boldsymbol\beta)Q,\quad Q=\begin{pmatrix}2&0\\1&1\end{pmatrix}.$$ 求从旧基到新基的过渡矩阵，并求旧坐标为 $(5,-1)^{\mathsf T}$ 的向量在新基下的坐标。

**L8-07**〔B｜方法 5 · 考查：由秩和左零空间反推四个子空间〕设 $A$ 是一个 $3\times4$ 矩阵，$r(A)=2$，且
$$N(A^{\mathsf T})=\operatorname{span}\{(1,1,-1)^{\mathsf T}\}.$$ 求四个基本子空间的维数，并写出 $A\boldsymbol{x}=\boldsymbol b$ 有解的充要条件。

**L8-08**〔B｜方法 4 · 考查：参数导致的秩变化〕设
$A_t=\begin{pmatrix}1&0&1&0\\0&1&0&1\\1&1&1&t\end{pmatrix}$。求使 $\dim N(A_t)=2$ 的 $t$，并在该值下写出 $N(A_t)$ 的一组基。

**L8-09**〔B｜方法 5 · 考查：四个子空间与列空间取基规则〕设
$A=\begin{pmatrix}1&2&0&1\\0&1&1&1\\1&3&1&2\end{pmatrix}$。求 $C(A)$、$C(A^{\mathsf T})$、$N(A)$、$N(A^{\mathsf T})$ 的一组基，并说明为什么 $C(A)$ 的基要取原矩阵的主元列。

### C 提高

**L8-10**〔B｜方法 3 · 考查：两组坐标相同时的非零向量〕设新基相对于旧基的过渡矩阵为
$P=\begin{pmatrix}2&1&0\\1&2&0\\0&0&3\end{pmatrix}$。求所有在旧基和新基下坐标相同的非零向量，并写出这些向量的旧坐标。

拆法：先做 L8-03、L8-06。

**L8-11**〔C｜方法 5 · 考查：由零空间反造矩阵并核对四个子空间〕已知 $\mathbb{R}^4$ 中的子空间
$N=\operatorname{span}\{(1,1,0,0)^{\mathsf T},(0,0,1,1)^{\mathsf T}\}$。构造一个最少行数、没有零行的矩阵 $A$，使 $N(A)=N$；再求这个 $A$ 的四个子空间各自的一组基，并写出 $A\boldsymbol{x}=\boldsymbol{b}$ 有解的条件。

拆法：先做 L8-04、L8-07。

### 章末混合练习

**L8-12**设 $W=\operatorname{span}\{(1,0,1)^{\mathsf T},(0,1,1)^{\mathsf T}\}$，$U=\{\boldsymbol{x}\in\mathbb{R}^3:x_1-x_2=0\}$。求 $W\cap U$ 的一组基和维数，并说明你的求法为什么没有把 $W$ 当成整个 $\mathbb{R}^3$。

**L8-13**在 $P_2$ 上定义 $T(p)=p'(t)+p(0)t$。先求 $T$ 在基 $(1,t,t^2)$ 下的矩阵；再求它在新基 $(1+t,1-t,t^2)$ 下的矩阵。

**L8-14**设
$A=\begin{pmatrix}1&2&1\\2&4&2\\0&1&1\end{pmatrix}$，$\boldsymbol{b}=(1,2,1)^{\mathsf T}$。求解 $A\boldsymbol{x}=\boldsymbol{b}$ 的全部解，并说明对一般的 $\boldsymbol{b}=(b_1,b_2,b_3)^{\mathsf T}$，方程有解的充要条件是什么；同时给出 $N(A)$ 与 $N(A^{\mathsf T})$ 的一组基。
