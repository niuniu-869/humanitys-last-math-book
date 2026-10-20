## L.1 · 向量与线性组合（题目）

| 题号 | 档 | 方法 |
|---|---|---|
| L1-01 | A | 方法 1 |
| L1-02 | A | 方法 2 |
| L1-03 | A | 方法 3 |
| L1-04 | A | 方法 2、3（选择） |
| L1-05 | A | 方法 4（选择） |
| L1-06 | B | 方法 3（证明） |
| L1-07 | B | 方法 3（选择） |
| L1-08 | B | 方法 2、4 |
| L1-09 | B | 方法 2、3 |
| L1-10 | C | 方法 2、3 |
| L1-11 | C | 方法 2、4 |
| L1-12 | B | 混合（答案里标） |
| L1-13 | B | 混合（答案里标，证明） |
| L1-14 | C | 混合（答案里标） |

### A 基础

**L1-01**〔A｜方法 1 · 考查：由平均反求向量〕设 $\boldsymbol{u}=(5,4,1,2)^{\mathsf T}$，$\boldsymbol{m}=(3,4.5,2,1.5)^{\mathsf T}$。(1) 求满足 $\frac12(\boldsymbol{u}+\boldsymbol{x})=\boldsymbol{m}$ 的 $\boldsymbol{x}$；(2) 再求满足 $\frac13(\boldsymbol{u}+\boldsymbol{x}+\boldsymbol{y})=\boldsymbol{m}$ 的 $\boldsymbol{y}$，并说明结果为什么恰好是 $\boldsymbol{m}$。

**L1-02**〔A｜方法 2 · 考查：多出来的方程就是能表示的条件〕若 $\boldsymbol{b}=(1,k,3)^{\mathsf T}$ 能由 $\boldsymbol{a}_1=(1,1,0)^{\mathsf T}$、$\boldsymbol{a}_2=(0,1,1)^{\mathsf T}$ 线性表示，则 $k=$ \_\_\_\_。

**L1-03**〔A｜方法 3 · 考查：平面上张成整个平面的条件〕设 $\boldsymbol{a}_1=(1,2)^{\mathsf T}$，$\boldsymbol{a}_2=(2,k)^{\mathsf T}$。(1) $k$ 取何值时 $\operatorname{span}(\boldsymbol{a}_1,\boldsymbol{a}_2)=\mathbb{R}^2$？(2) $k$ 取其余值时张成是什么？这时 $(3,6)^{\mathsf T}$ 有几种表示方式，$(1,0)^{\mathsf T}$ 能否表示？

**L1-04**〔A｜方法 2、3 · 考查：共线时的张成、系数与检验方程〕（选择）设 $\boldsymbol{a}_1=(1,2,3)^{\mathsf T}$，$\boldsymbol{a}_2=(2,4,6)^{\mathsf T}$。下列说法正确的是（　）。

(A) 有两个向量，所以 $\operatorname{span}(\boldsymbol{a}_1,\boldsymbol{a}_2)$ 是 $\mathbb{R}^3$ 中过原点的平面
(B) $(3,6,9)^{\mathsf T}$ 能由 $\boldsymbol{a}_1,\boldsymbol{a}_2$ 线性表示，并且组合系数唯一
(C) $(1,2,4)^{\mathsf T}$ 能由 $\boldsymbol{a}_1,\boldsymbol{a}_2$ 线性表示，因为取 $c_1=1$、$c_2=0$ 时前两个分量已经对上
(D) $\operatorname{span}(\boldsymbol{a}_1,\boldsymbol{a}_2)$ 是 $\mathbb{R}^3$ 中一条过原点的直线

**L1-05**〔A｜方法 4 · 考查：凸组合的两个条件〕（选择）设 $\boldsymbol{e}_1=(1,0)^{\mathsf T}$，$\boldsymbol{e}_2=(0,1)^{\mathsf T}$。下列说法正确的是（　）。

(A) $2\boldsymbol{e}_1-\boldsymbol{e}_2$ 的系数之和为 1，所以它是 $\boldsymbol{e}_1,\boldsymbol{e}_2$ 的凸组合
(B) 若 $0\le x\le1$ 且 $0\le y\le1$，则 $(x,y)^{\mathsf T}$ 是 $\boldsymbol{e}_1,\boldsymbol{e}_2$ 的凸组合
(C) $\operatorname{span}(\boldsymbol{e}_1,\boldsymbol{e}_2)$ 中的每个向量都能写成 $\boldsymbol{e}_1,\boldsymbol{e}_2$ 的凸组合
(D) $\boldsymbol{e}_1,\boldsymbol{e}_2$ 的任一凸组合 $(x,y)^{\mathsf T}$ 都满足 $x+y=1$，并且 $0\le x\le1$

### B 进阶

**L1-06**〔B｜方法 3 · 考查：两个张成相等要证两个方向〕设 $\boldsymbol{a}_1,\boldsymbol{a}_2$ 是 $\mathbb{R}^n$ 中任意两个向量。证明
$$\operatorname{span}(\boldsymbol{a}_1,\boldsymbol{a}_2)=\operatorname{span}(\boldsymbol{a}_1+\boldsymbol{a}_2,\ \boldsymbol{a}_1-\boldsymbol{a}_2).$$

**L1-07**〔B｜方法 3 · 考查：什么样的向量组张成 $\mathbb{R}^3$〕（选择）下列向量组中，张成整个 $\mathbb{R}^3$ 的是（　）。

(A) $(1,0,1)^{\mathsf T},(0,1,1)^{\mathsf T},(1,-1,0)^{\mathsf T}$，它们两两不共线
(B) $(1,-1,0)^{\mathsf T},(0,1,-1)^{\mathsf T},(1,0,-1)^{\mathsf T},(2,-1,-1)^{\mathsf T}$，一共四个向量
(C) $(1,2,0)^{\mathsf T},(0,0,0)^{\mathsf T},(0,1,3)^{\mathsf T}$，恰好三个向量
(D) $(1,1,0)^{\mathsf T},(0,1,1)^{\mathsf T},(1,0,1)^{\mathsf T}$

**L1-08**〔B｜方法 2、4 · 考查：权重不唯一时不能只看一组解的符号〕设 $\boldsymbol{p}_1=(0,0)^{\mathsf T}$、$\boldsymbol{p}_2=(2,0)^{\mathsf T}$、$\boldsymbol{p}_3=(0,2)^{\mathsf T}$、$\boldsymbol{p}_4=(2,2)^{\mathsf T}$，目标 $\boldsymbol{b}=(1.5,1.5)^{\mathsf T}$。(1) $\boldsymbol{b}$ 是不是 $\boldsymbol{p}_1,\boldsymbol{p}_2,\boldsymbol{p}_3$ 的凸组合？(2) 某同学对四个向量列方程，令 $c_4=\frac14$，发现 $c_1<0$，于是断言 $\boldsymbol{b}$ 不是四个向量的凸组合。他错在哪里？(3) 令 $c_4=s$，写出全部权重，求 $s$ 的范围，并给出一组只有三个权重不为 0 的表示。

**L1-09**〔B｜方法 2、3 · 考查：含参数时讨论表示的存在与唯一〕设 $\boldsymbol{\alpha}_1=(1,1,1)^{\mathsf T}$，$\boldsymbol{\alpha}_2=(1,2,3)^{\mathsf T}$，$\boldsymbol{\alpha}_3=(1,3,a)^{\mathsf T}$，$\boldsymbol{\beta}=(1,b,3)^{\mathsf T}$。问 $a,b$ 取何值时：(1) $\boldsymbol{\beta}$ 不能由 $\boldsymbol{\alpha}_1,\boldsymbol{\alpha}_2,\boldsymbol{\alpha}_3$ 线性表示；(2) $\boldsymbol{\beta}$ 能由它们线性表示，且表示唯一；(3) $\boldsymbol{\beta}$ 能由它们线性表示，但表示不唯一，并写出全部表示式。

### C 提高

**L1-10**〔C｜方法 2、3 · 考查：由「不能表示」反推参数，并验证充分性〕设 $\boldsymbol{\alpha}_1,\boldsymbol{\alpha}_2,\boldsymbol{\alpha}_3$ 同 L1-09，$\boldsymbol{\gamma}_1=(1,0,1)^{\mathsf T}$，$\boldsymbol{\gamma}_2=(0,1,1)^{\mathsf T}$，$\boldsymbol{\gamma}_3=(3,4,5)^{\mathsf T}$。(1) 若 $\boldsymbol{\gamma}_1,\boldsymbol{\gamma}_2,\boldsymbol{\gamma}_3$ 不能都由 $\boldsymbol{\alpha}_1,\boldsymbol{\alpha}_2,\boldsymbol{\alpha}_3$ 线性表示，求 $a$；(2) 对这个 $a$，写出 $\operatorname{span}(\boldsymbol{\alpha}_1,\boldsymbol{\alpha}_2,\boldsymbol{\alpha}_3)$ 的方程，指出哪个 $\boldsymbol{\gamma}_i$ 能被表示，并写出它的全部表示式；(3) 反过来，$\boldsymbol{\alpha}_1,\boldsymbol{\alpha}_2,\boldsymbol{\alpha}_3$ 能否都由 $\boldsymbol{\gamma}_1,\boldsymbol{\gamma}_2,\boldsymbol{\gamma}_3$ 线性表示？

拆法：先做 L1-09（含参数消元）、例 3 后的小题（写出张成的方程）。

**L1-11**〔C｜方法 2、4 · 考查：方程多于未知数时的凸组合，以及不解方程的否定论证〕设 $\boldsymbol{u}=(5,4,1,2)^{\mathsf T}$，$\boldsymbol{v}=(4,5,2,1)^{\mathsf T}$，$\boldsymbol{w}=(1,2,5,4)^{\mathsf T}$，考虑凸组合 $\alpha\boldsymbol{u}+\beta\boldsymbol{v}+\gamma\boldsymbol{w}$（$\alpha,\beta,\gamma\ge0$，$\alpha+\beta+\gamma=1$）。(1) 把 $(3.5,4,2.5,2)^{\mathsf T}$ 写成这样的凸组合；(2) 不解方程组，说明 $(5,5,1,1)^{\mathsf T}$ 不是 $\boldsymbol{u},\boldsymbol{v},\boldsymbol{w}$ 的凸组合；(3) 放宽非负条件，只要求 $(5,5,1,1)^{\mathsf T}=\alpha\boldsymbol{u}+\beta\boldsymbol{v}+\gamma\boldsymbol{w}$ 且 $\alpha+\beta+\gamma=1$，求有符号解，并说明它与 (2) 不矛盾。

拆法：先做 L1-02（多出来的方程用来检验）、L1-08（全部解里找非负的）。

### 章末混合练习

**L1-12**〔B〕设 $\boldsymbol{a}_1,\boldsymbol{a}_2$ 是两个不共线的 $n$ 维向量，$\boldsymbol{b}_1=\boldsymbol{a}_1+2\boldsymbol{a}_2$，$\boldsymbol{b}_2=2\boldsymbol{a}_1+k\boldsymbol{a}_2$。(1) $k$ 为何值时 $\boldsymbol{b}_1,\boldsymbol{b}_2$ 共线？(2) 当 $k=3$ 时，把 $\boldsymbol{a}_1+\boldsymbol{a}_2$ 写成 $\boldsymbol{b}_1,\boldsymbol{b}_2$ 的线性组合；(3) 当 $k$ 取 (1) 中的值时，$\boldsymbol{a}_1$ 能否由 $\boldsymbol{b}_1,\boldsymbol{b}_2$ 线性表示？

**L1-13**〔B〕平面上 $\triangle ABC$ 的三个顶点不共线，取 $\lambda,\mu\in\mathbb R$，点 $P$ 满足 $\overrightarrow{AP}=\lambda\overrightarrow{AB}+\mu\overrightarrow{AC}$。(1) 证明：$P$ 在 $\triangle ABC$ 内部或边上，当且仅当 $\lambda\ge0$，$\mu\ge0$，$\lambda+\mu\le1$；(2) 取 $A(0,0)$，$B(4,0)$，$C(1,3)$，判断 $P(2,1)$ 是否在三角形内部或边上。

**L1-14**〔C〕三只基金在「行情好、行情差」两种情形下的年收益率（%）为 $\boldsymbol{f}_1=(12,-6)^{\mathsf T}$（股票型）、$\boldsymbol{f}_2=(6,0)^{\mathsf T}$（混合型）、$\boldsymbol{f}_3=(0,3)^{\mathsf T}$（债券型），按比例组合、不允许卖空（权重非负、和为 1）。(1) 在行情好时收益率恰为 8% 的所有组合中，行情差时的收益率最高是多少？由哪种组合达到？(2) 这些组合在行情差时的收益率能取到哪些值？

拆法：先做 L1-08（在全部解里找非负的）、L1-09 的 (3)（用一个参数写出全部解）。
