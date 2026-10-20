## L.7 · 线性相关与秩（题目）

| 题号 | 档 | 方法 |
|---|---|---|
| L7-01 | A | 方法 1 |
| L7-02 | A | 方法 6 |
| L7-03 | A | 方法 3 |
| L7-04 | A | 方法 8 |
| L7-05 | B | 方法 2 |
| L7-06 | B | 方法 4 |
| L7-07 | B | 方法 5 |
| L7-08 | B | 方法 5 |
| L7-09 | B | 方法 6 |
| L7-10 | B | 方法 7 |
| L7-11 | C | 方法 5、方法 6 |
| L7-12 | C | 方法 6、方法 8 |
| L7-13 | C | 方法 8 |
| L7-14 | — | 综合 |
| L7-15 | — | 综合 |
| L7-16 | — | 综合 |
| L7-17 | — | 综合 |

### A 基础

**L7-01**〔A｜方法 1 · 考查：排成列数主元并写相关关系〕判断
\[
\boldsymbol a_1=(1,0,1,2)^{\mathsf T},\quad \boldsymbol a_2=(0,1,1,1)^{\mathsf T},\quad \boldsymbol a_3=(1,1,2,3)^{\mathsf T}
\]
是否线性相关；若相关，写出一个非零相关关系。

**L7-02**〔A｜方法 6 · 考查：化阶梯形求矩阵的秩〕求
\[
A=\begin{pmatrix}1&2&0&1\\2&4&1&3\\0&1&1&1\end{pmatrix}
\]
的秩，并指出一个不为零的二阶子式。

**L7-03**〔A｜方法 3 · 考查：唯一表示的前提〕单选。已知 \(\boldsymbol\alpha_1,\boldsymbol\alpha_2\) 线性无关，且 \(\boldsymbol\alpha_1,\boldsymbol\alpha_2,\boldsymbol\beta\) 线性相关。下列说法正确的是（  ）

(A) \(\boldsymbol\alpha_1\) 一定能由 \(\boldsymbol\alpha_2,\boldsymbol\beta\) 表示；  
(B) \(\boldsymbol\beta\) 能由 \(\boldsymbol\alpha_1,\boldsymbol\alpha_2\) 唯一表示；  
(C) \(\boldsymbol\beta\) 一定是零向量；  
(D) 三个向量中任意两个都线性相关。

**L7-04**〔A｜方法 8 · 考查：两个外积相加的秩〕设
\[
\boldsymbol u=(1,0,1)^{\mathsf T},\quad \boldsymbol w=(0,1,1)^{\mathsf T},\quad
\boldsymbol v=(1,1,0)^{\mathsf T},\quad \boldsymbol z=(1,0,1)^{\mathsf T}.
\]
求 $r(\boldsymbol u\boldsymbol v^{\mathsf T}+\boldsymbol w\boldsymbol z^{\mathsf T})$。
### B 进阶

**L7-05**〔B｜方法 2 · 考查：按定义找出相关关系〕已知 $\boldsymbol\alpha_1,\boldsymbol\alpha_2,\boldsymbol\alpha_3$ 线性无关，且
\[
\boldsymbol\beta_1=\boldsymbol\alpha_1+\boldsymbol\alpha_2,\quad
\boldsymbol\beta_2=\boldsymbol\alpha_1-\boldsymbol\alpha_3,\quad
\boldsymbol\beta_3=2\boldsymbol\alpha_1+\boldsymbol\alpha_2-\boldsymbol\alpha_3.
\]
证明 $\boldsymbol\beta_1,\boldsymbol\beta_2,\boldsymbol\beta_3$ 线性相关，并写出一个非零相关关系。
**L7-06**〔B｜方法 4 · 考查：非方阵系数矩阵与替换定理〕已知 $\boldsymbol\alpha_1,\boldsymbol\alpha_2,\boldsymbol\alpha_3$ 线性无关，且
\[
\boldsymbol\beta_1=\boldsymbol\alpha_1+\boldsymbol\alpha_2,\quad
\boldsymbol\beta_2=\boldsymbol\alpha_2+\boldsymbol\alpha_3,\quad
\boldsymbol\beta_3=\boldsymbol\alpha_1+\boldsymbol\alpha_3,\quad
\boldsymbol\beta_4=2\boldsymbol\alpha_1+\boldsymbol\alpha_2+\boldsymbol\alpha_3.
\]
证明这四个向量线性相关，并写出全部相关关系（用参数表示）。
**L7-07**〔B｜方法 5 · 考查：不能用列变换后的列认极大无关组〕单选。把矩阵的列向量排成矩阵后，为了求原向量组的一个极大无关组，下面哪种做法正确（  ）

(A) 先任意做列交换，再把阶梯形的主元列当作原来的主元列；
(B) 只做初等行变换，阶梯形的主元位置对应原矩阵中的那些列；
(C) 把矩阵转置后做行变换，再把非零行当作原向量；
(D) 只要行最简形有三行非零行，就任选原来的三个向量作极大无关组。

**L7-08**〔B｜方法 5 · 考查：参数改变极大无关组的选取〕设
\[
\boldsymbol a_1=(1,0,1)^{\mathsf T},\quad \boldsymbol a_2=(0,1,1)^{\mathsf T},\quad
\boldsymbol a_3=(1,1,2)^{\mathsf T},\quad \boldsymbol a_4=(1,2,t)^{\mathsf T}.
\]
(1) 求使 $\{\boldsymbol a_1,\boldsymbol a_2,\boldsymbol a_4\}$ 成为极大线性无关组的 $t$ 的范围；(2) 在其余参数值下给出一个极大无关组，并表示 $\boldsymbol a_4$。
**L7-09**〔B｜方法 6 · 考查：非对称参数矩阵的三种秩〕讨论
\[
A(t)=\begin{pmatrix}1&1&1\\1&t&t\\1&t&t^2\end{pmatrix}
\]
的秩随实数 $t$ 的变化，要求说明秩为 $1$、$2$、$3$ 时分别对应哪些参数。
**L7-10**〔B｜方法 7 · 考查：矩阵等价与向量组等价的区别〕单选。下列说法正确的是（  ）

(A) 两个同型矩阵秩相等，当且仅当它们等价；
(B) 两个向量组秩相等，就一定能互相线性表示；
(C) 矩阵等价要求两个矩阵的每一列都能由对方对应列表示；
(D) 向量组互相线性表示只要向量个数相同，不必检查系数关系。

### C 提高

**L7-11**〔C｜方法 5、方法 6 · 考查：参数导致极大无关组改变〕设
\[
\boldsymbol a_1=(1,0,1)^{\mathsf T},\quad \boldsymbol a_2=(0,1,1)^{\mathsf T},\quad \boldsymbol a_3=(1,1,2)^{\mathsf T},\quad \boldsymbol a_4=(1,2,t)^{\mathsf T}.
\]
(1) 求使向量组秩为 2 的所有 \(t\)；(2) 对这些 \(t\)，给出一个极大无关组并表示其余向量；(3) 当 \(t\ne3\) 时，求一个极大无关组。

拆法：先做 L7-01、L7-08。

**L7-12**〔C｜方法 6、方法 8 · 考查：非方阵乘可逆因子〕令
\[
A(t)=\begin{pmatrix}1&t&0\\0&1&1\end{pmatrix},\quad
B=\begin{pmatrix}1&0&1\\0&1&1\\0&0&1\end{pmatrix}.
\]
(1) 求 $r(A(t))$；(2) 说明为什么 $r(A(t)B)=r(A(t))$，并给出其秩随 $t$ 的变化。
**L7-13**〔C｜方法 8 · 考查：两个秩一矩阵相加〕设
\[
\Delta(t)=\begin{pmatrix}1&1&0\\ t&0&t\\1+t&1&t\end{pmatrix}.
\]
求 $r(\Delta(t))$ 随 $t$ 的变化，并说明上界来自哪条秩不等式。

拆法：先做 L7-04、L7-12。
### 章末混合练习

**L7-14**〔综合考查：L.3 的按列分块与线性无关〕已知 \(\boldsymbol a_1,\boldsymbol a_2\) 线性无关，\(\boldsymbol b_1=\boldsymbol a_1+\boldsymbol a_2\)，\(\boldsymbol b_2=2\boldsymbol a_1-\boldsymbol a_2\)。求 \(\boldsymbol b_1,\boldsymbol b_2\) 是否线性无关，并说明 \(\boldsymbol a_1\) 能否由 \(\boldsymbol b_1,\boldsymbol b_2\) 表示。

**L7-15**〔综合考查：参数秩与非零子式〕讨论
\[
C(t)=\begin{pmatrix}1&1&1\\1&t&t\\1&t&t^2\end{pmatrix}
\]
的秩随 $t$ 的变化，并在秩小于 $3$ 的参数处给出一个非零低阶子式。
**L7-16**〔综合考查：相似形的秩不等式〕设 $A$ 为三阶矩阵，$P$ 为三阶可逆矩阵，且 $r(A)=2$。判断并说明：是否总有
\[
r(PA+PAP^{-1})\le2？
\]
再给出一组 $P,A$ 使等号成立。
**L7-17**〔综合考查：齐次方程组的全部关系〕设
\[
D=\begin{pmatrix}1&0&1&2\\0&1&1&1\end{pmatrix}.
\]
求列向量组的秩，并写出 $D\boldsymbol x=\boldsymbol0$ 的全部解；由此说明全部非零线性关系。