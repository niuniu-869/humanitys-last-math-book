## L.14 · 二次型与正定（题目）

| 题号 | 档 | 方法 |
|---|---|---|
| L14-01 | A | 方法 1 |
| L14-02 | A | 方法 2 |
| L14-03 | A | 方法 3 |
| L14-04 | A | 方法 5（选择） |
| L14-05 | B | 方法 5（证明） |
| L14-06 | B | 方法 6 |
| L14-07 | B | 方法 7（填空） |
| L14-08 | B | 方法 8 |
| L14-09 | B | 方法 4（选择） |
| L14-10 | C | 方法 2、7 |
| L14-11 | C | 方法 9 |
| L14-12 | C | 方法 7、9 |
| L14-13 | B | 方法 8、9 |
| L14-14 | B | 方法 1、8 |
| L14-15 | B | 方法 9 |

### A 基础

**L14-01**〔A｜方法 1 · 考查：先对称化再求秩〕给定不对称矩阵
$$B=\begin{pmatrix}2&4&0\\0&5&3\\0&0&1\end{pmatrix}.$$
写出 $q(\boldsymbol{x})=\boldsymbol{x}^{\mathsf T}B\boldsymbol{x}$ 的对称矩阵，并求这个二次型的秩。

**L14-02**〔A｜方法 2 · 考查：由主轴和半轴反求二次型〕椭圆 $q(x,y)=1$ 的主轴方向为 $(1,1)^{\mathsf T}$、$(1,-1)^{\mathsf T}$，对应半轴长分别为 $1/\sqrt2$、$1/\sqrt6$。写出 $q$ 的对称矩阵和展开式，并给出一个正交变换后的标准形。

**L14-03**〔A｜方法 3 · 考查：没有平方项时先构造可逆换元〕用配方法把
$$q=2x_1x_2+2x_1x_3+2x_2x_3$$
化为标准形，要求先构造平方项，再写出一个可逆换元、逆变换和二次型的秩。

**L14-04**〔A｜方法 5 · 考查：正定、半正定与不定的区分〕下列矩阵中，正定的是（ ）。

A. $\begin{pmatrix}1&2\\2&1\end{pmatrix}$　　B. $\begin{pmatrix}1&0\\0&0\end{pmatrix}$　　C. $\begin{pmatrix}2&1\\1&2\end{pmatrix}$　　D. $\begin{pmatrix}0&1\\1&2\end{pmatrix}$

### B 进阶

**L14-05**〔B｜方法 5 · 考查：秩亏时加正对角项仍正定〕设 $A$ 是 $m\times n$ 实矩阵，$r(A)<n$，且 $k>0$。证明 $A^{\mathsf T}A+kE_n$ 正定。

**L14-06**〔B｜方法 6 · 考查：三阶参数矩阵同时判断正定和负定〕设
$$A(t)=\begin{pmatrix}t&1&0\\1&t&1\\0&1&t\end{pmatrix}.$$
分别求使 $A(t)$ 正定、负定的 $t$ 的取值范围。

**L14-07**〔B｜方法 7 · 考查：特征方向与球面最值的对应〕设 $A$ 是 $2\times2$ 实对称矩阵，迹为 $8$，且单位向量 $\boldsymbol v=\frac1{\sqrt2}(1,1)^{\mathsf T}$ 是特征值为 $5$ 的特征向量。在 $\lVert\boldsymbol x\rVert=3$ 上，求二次型的最大值、最小值及取到的方向。

**L14-08**〔B｜方法 8 · 考查：秩亏最小二乘的全部最小点〕令
$$B=\begin{pmatrix}1&1\\2&2\\3&3\end{pmatrix},\qquad \boldsymbol b=(1,2,4)^{\mathsf T},\qquad F(\boldsymbol x)=\lVert B\boldsymbol x-\boldsymbol b\rVert^2.$$
求 $F$ 的梯度和 Hessian，并写出全部驻点及最小值。

**L14-09**〔B｜方法 4 · 考查：含零特征值时区分三种关系〕设
$$A=\operatorname{diag}(1,-2,0),\quad B=\operatorname{diag}(3,-4,0),\quad C=\operatorname{diag}(1,2,0).$$
下列说法正确的是（ ）。

A. $A$ 与 $B$ 相似，因为它们的秩相同。

B. $A$ 与 $B$ 合同，因为它们的正、负惯性指数都为 $(1,1)$。

C. $A$ 与 $C$ 合同，因为它们都有一个零特征值。

D. $A$ 与 $C$ 等价但不合同，因为它们的秩相同。

### C 提高

**L14-10**〔C｜方法 2、7 · 考查：由特征对反求矩阵，再求球面最值〕实对称矩阵 $A$ 的单位特征向量
$$\boldsymbol q_1=\frac1{\sqrt2}(1,1)^{\mathsf T},\qquad \boldsymbol q_2=\frac1{\sqrt2}(1,-1)^{\mathsf T}$$
分别对应特征值 $6$、$2$。求 $A$ 及二次型 $\boldsymbol{x}^{\mathsf T}A\boldsymbol{x}$ 的表达式；再求它在 $\lVert\boldsymbol{x}\rVert=2$ 上的最大值、最小值和取到的点。

拆法：先做 L14-02、L14-07。

**L14-11**〔C｜方法 9 · 考查：半正定奇异 Hessian 不能直接判别〕分别判断
$$f(x,y)=x^4+2y^2,\qquad g(x,y)=x^4-y^4$$
在原点的极值类型。要求先写出梯度和 Hessian，再说明二阶判别为什么失效，最后用函数值定义完成判断。

拆法：先做 L14-04、L14-08。

**L14-12**〔C｜方法 7、9 · 考查：对称矩阵迭代的稳定区间〕设 $\eta\in\mathbb R$，
$$A=\operatorname{diag}(1,4,9),\qquad \boldsymbol x_{k+1}=(E-\eta A)\boldsymbol x_k.$$
求使对任意初始向量都收敛到零向量的 $\eta$ 的范围；再求使特征值为 $1$、$9$ 的两个方向每步收缩因子的绝对值相等的 $\eta$ 及共同绝对值。若 $\boldsymbol x_0=(1,0,1)^{\mathsf T}$，取该 $\eta$ 迭代两步，求 $\boldsymbol x_2$。

拆法：先做 L14-07。

### 章末混合练习

**L14-13**〔B〕令
$$B=\begin{pmatrix}1&1\\2&2\\3&3\end{pmatrix},\qquad \boldsymbol b=(1,2,4)^{\mathsf T},\qquad F(\boldsymbol x)=\lVert B\boldsymbol x-\boldsymbol b\rVert^2.$$
求全部最小点和最小值，并说明为什么最小点不唯一。

**L14-14**〔B〕设
$$B=\begin{pmatrix}1&2&0\\0&1&0\\0&0&0\end{pmatrix},\qquad q(\boldsymbol x)=\boldsymbol x^{\mathsf T}B\boldsymbol x.$$
比较 $\boldsymbol x^{\mathsf T}B\boldsymbol x$ 与 $\boldsymbol x^{\mathsf T}B^{\mathsf T}\boldsymbol x$，求共同的 Hessian 和二次型的秩。

**L14-15**〔B〕求函数
$$h(x,y)=x^3-3x+y^2$$
的全部驻点，并用 Hessian 判别每个驻点的类型与函数值。
