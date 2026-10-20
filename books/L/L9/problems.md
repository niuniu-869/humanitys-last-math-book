## L.9 · 线性方程组解的结构（题目）

| 题号 | 档 | 方法 |
|---|---|---|
| L9-01 | A | 方法 1 |
| L9-02 | A | 方法 2 |
| L9-03 | A | 方法 3 |
| L9-04 | A | 方法 6 |
| L9-05 | B | 方法 5 |
| L9-06 | B | 方法 3 |
| L9-07 | B | 方法 4 |
| L9-08 | B | 方法 5 |
| L9-09 | B | 方法 6 |
| L9-10 | C | 方法 4 |
| L9-11 | C | 方法 2、3 |
| L9-12 | — | 章末混合 |
| L9-13 | — | 章末混合 |
| L9-14 | — | 章末混合 |

### A 基础

**L9-01**〔A｜方法 1 · 考查：秩、未知数个数与解的三种结局〕设 $A$ 是 $4\times3$ 矩阵，$r(A)=2$，$r(A\mid\boldsymbol b)=2$。关于 $A\boldsymbol x=\boldsymbol b$，下列说法正确的是（ ）。

(A) 无解。  
(B) 有唯一解，因为增广矩阵的秩为 2。  
(C) 有无穷多解，且有 1 个自由未知量。  
(D) 齐次方程组 $A\boldsymbol x=\boldsymbol0$ 只有零解。

**L9-02**〔A｜方法 2 · 考查：基础解系的取法〕求齐次方程组
$$
\begin{cases}
x_1+x_2+x_4=0,\\
x_2+x_3+2x_4=0
\end{cases}
$$
的一个基础解系和通解。

**L9-03**〔A｜方法 3 · 考查：非齐次解的线性组合〕设 $\boldsymbol\eta_1,\boldsymbol\eta_2,\boldsymbol\eta_3$ 都是 $A\boldsymbol x=\boldsymbol b$ 的解，且 $\boldsymbol b\ne\boldsymbol0$。下列向量中必然仍是 $A\boldsymbol x=\boldsymbol b$ 的解的是（ ）。

(A) $2\boldsymbol\eta_1-\boldsymbol\eta_2$  
(B) $\boldsymbol\eta_1-\boldsymbol\eta_2$  
(C) $\boldsymbol\eta_1+\boldsymbol\eta_2$  
(D) $2\boldsymbol\eta_1-\boldsymbol\eta_2+\boldsymbol\eta_3$

**L9-04**〔A｜方法 6 · 考查：同解判据的适用边界〕有人说：“两个非齐次方程组只要系数矩阵相同、秩相同，就能用方法 6 判断它们同解。”请给出一组最简单的反例，并说明方法 6 为什么不能直接这样用。

### B 进阶

**L9-05**〔B｜方法 5 · 考查：$AB=O$ 与零空间〕设 $A$ 是 $4\times5$ 矩阵，$r(A)=3$；$B$ 是 $5\times2$ 的非零矩阵，且 $AB=O$。下列说法中必然正确的是（ ）。

(A) $B$ 的每一列都属于 $N(A)$。  
(B) $r(B)=2$。  
(C) $r(A)+r(B)\le4$。  
(D) $B$ 可逆。

**L9-06**〔B｜方法 3 · 考查：由几个非齐次解拼出特解和基础解系〕四元方程组 $A\boldsymbol x=\boldsymbol b$ 的秩为 $2$。已知 $\boldsymbol\eta_1,\boldsymbol\eta_2,\boldsymbol\eta_3$ 是它的三个解，并且
$$
\boldsymbol\eta_1=\begin{pmatrix}1\\0\\1\\2\end{pmatrix},\quad
\boldsymbol\eta_1+\boldsymbol\eta_2=\begin{pmatrix}3\\2\\1\\4\end{pmatrix},\quad
2\boldsymbol\eta_1+\boldsymbol\eta_3=\begin{pmatrix}4\\1\\2\\6\end{pmatrix}.
$$
求 $A\boldsymbol x=\boldsymbol b$ 的通解。

**L9-07**〔B｜方法 4 · 考查：参数取特殊值时不能随意约去主元〕讨论参数 $t$ 取何值时，方程组
$$
\begin{cases}
x_1+x_2+x_3=1,\\
x_1+2x_2+3x_3=2,\\
x_1+3x_2+(t+4)x_3=t+2
\end{cases}
$$
有唯一解或无穷多解，并在无穷多解时写出通解。

**L9-08**〔B｜方法 5 · 考查：$AB=O$ 的秩不等式证明〕设 $A$ 是 $m\times n$ 矩阵，$B$ 是 $n\times p$ 矩阵，且 $AB=O$。证明 $r(A)+r(B)\le n$。

**L9-09**〔B｜方法 6 · 考查：带参数的同解判断〕设
$$
\text{(I)}\ \begin{cases}x_1+x_2=0,\\x_2+x_3=0,\end{cases}\qquad
\text{(II)}\ \begin{cases}x_1-x_3=0,\\x_1+t x_2+x_3=0.\end{cases}
$$
求使两组齐次方程组同解的参数 $t$，并写出公共通解。

### C 提高

**L9-10**〔C｜方法 4 · 考查：两个参数、相容性与附加条件〕讨论 $a,b$ 取何值时，方程组
$$
\begin{cases}
x_1+x_2+x_3=2,\\
x_1+2x_2+4x_3=3,\\
2x_1+3x_2+ax_3=b
\end{cases}
$$
有唯一解、无解或无穷多解；在无穷多解时，再求满足 $x_2=x_3$ 的解。

拆法：先做 L9-03、L9-08。

**L9-11**〔C｜方法 2、3 · 考查：由列关系直接写出非齐次通解〕设 $A=(\boldsymbol\alpha_1,\boldsymbol\alpha_2,\boldsymbol\alpha_3,\boldsymbol\alpha_4)$，其中 $\boldsymbol\alpha_2,\boldsymbol\alpha_3,\boldsymbol\alpha_4$ 线性无关，且 $\boldsymbol\alpha_1=2\boldsymbol\alpha_2-\boldsymbol\alpha_3$。令 $\boldsymbol\beta=\boldsymbol\alpha_1+\boldsymbol\alpha_2+\boldsymbol\alpha_3+\boldsymbol\alpha_4$，求 $A\boldsymbol x=\boldsymbol\beta$ 的通解，并说明自由参数的个数。

拆法：先做 L9-03、L9-08。

### 章末混合练习

**L9-12**〔章末混合〕设
$$A=\begin{pmatrix}1&0&1&2\\2&0&2&4\\0&1&1&1\end{pmatrix},\qquad \boldsymbol b=\begin{pmatrix}1\\2\\3\end{pmatrix}.
$$
先用左零空间给出 $A\boldsymbol x=\boldsymbol b$ 有解的条件，再求其全部解。答案中注明使用了本章和 L.8 的哪些方法。

**L9-13**〔章末混合〕在多项式空间 $P_2$ 中，求满足
$$c_1(1+t)+c_2(1-t)+c_3t^2=2+3t+t^2$$
的系数，并判断表示是否唯一。答案中注明使用了 L.8 的哪一节和本章的哪一种判断。

**L9-14**〔章末混合〕设
$$A_\lambda=\begin{pmatrix}1&1&0\\0&\lambda&1\\1&1&1\end{pmatrix},\qquad \boldsymbol b=\begin{pmatrix}1\\2\\3\end{pmatrix}.
$$
先用行列式找出需要单独讨论的 $\lambda$，再判断各情形的解的结构，并在有无穷多解时写出通解。答案中注明使用了 L.6 和本章的方法。
