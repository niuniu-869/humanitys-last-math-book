## L.3 · 矩阵是线性变换（速记）

| 提示 | 内容 |
|---|---|
| $A\boldsymbol{x}$ 的定义 | $A=(\boldsymbol{a}_1,\dots,\boldsymbol{a}_n)$ 为 $m\times n$ 时，$A\boldsymbol{x}=x_1\boldsymbol{a}_1+\cdots+x_n\boldsymbol{a}_n\in\mathbb{R}^m$；列数 = $\boldsymbol{x}$ 的分量数 |
| 列看组合，行看点积 | 第 $i$ 个分量 = 第 $i$ 行与 $\boldsymbol{x}$ 的点积；$A\boldsymbol{x}=\boldsymbol{b}$ 有解 ⇔ $\boldsymbol{b}$ 在各列的张成里 |
| 读列 | $A\boldsymbol{e}_j$ = 第 $j$ 列；单位正方形变成以两列为邻边的平行四边形，网格跟着两列走 |
| 老朋友 ① 对称伸缩 | $\begin{pmatrix}2&1\\1&2\end{pmatrix}$：单位圆变斜椭圆；$(1,1)^{\mathsf T}$ 拉长 3 倍，$(-1,1)^{\mathsf T}$ 不动；对称 |
| 老朋友 ② 剪切 | $\begin{pmatrix}1&1\\0&1\end{pmatrix}$：$(x,y)\mapsto(x+y,y)$，面积不变；$k$ 次幂 $\begin{pmatrix}1&k\\0&1\end{pmatrix}$；与它可交换的是 $\begin{pmatrix}a&b\\0&a\end{pmatrix}$ |
| 老朋友 ③ 转 $90^\circ$ | $\begin{pmatrix}0&-1\\1&0\end{pmatrix}$：没有不变的方向；反对称；4 次幂是 $E$；$R_\theta=\begin{pmatrix}\cos\theta&-\sin\theta\\\sin\theta&\cos\theta\end{pmatrix}$ |
| 老朋友 ④ 投影 | $\frac12\begin{pmatrix}1&1\\1&1\end{pmatrix}$：垂直压到 $y=x$；对称；平方等于自己；$(-1,1)^{\mathsf T}$ 被压到原点，撤销不了 |
| 线性变换的矩阵 | 可加 + 齐次 ⇔ 能写成 $A\boldsymbol{x}$，$A=(T(\boldsymbol{e}_1),\dots,T(\boldsymbol{e}_n))$；$T(\boldsymbol{0})\ne\boldsymbol{0}$ 必不线性，$T(\boldsymbol{0})=\boldsymbol{0}$ 不够 |
| 乘积 = 复合 | $BA$ 先做 $A$ 再做 $B$（从右往左读）；$(m\times p)(p\times n)$ 内侧相等才能乘；$(BA)_{ij}$ = $B$ 第 $i$ 行 · $A$ 第 $j$ 列 |
| 和实数不同 | 一般 $AB\ne BA$（$SR\ne RS$）；$AB=O$ 推不出 $A=O$ 或 $B=O$；$AB=AC$ 不能约去 $A$；$(AB)^k\ne A^kB^k$ |
| 二项式定理 | 只在 $AB=BA$ 时可用；$\lambda E$ 与一切同阶方阵可交换，$n$ 阶严格上三角的 $N$ 满足 $N^n=O$ |
| 降次 | 由 $A^2=pA+qE$ 左乘 $A$ 再代回，任何 $A^k$ 都化成 $aA+bE$ |
| 转置 | $(AB)^{\mathsf T}=B^{\mathsf T}A^{\mathsf T}$（次序倒过来）；$A^{\mathsf T}A$ 对称；对称 $A,B$：$AB$ 对称 ⇔ $AB=BA$ |
| 外积 | $\boldsymbol{a}^{\mathsf T}\boldsymbol{b}$ 是数，$\boldsymbol{a}\boldsymbol{b}^{\mathsf T}$ 是矩阵；$A=\boldsymbol{\alpha}\boldsymbol{\beta}^{\mathsf T}$ 时 $A^n=(\boldsymbol{\beta}^{\mathsf T}\boldsymbol{\alpha})^{n-1}A$，$\boldsymbol{\beta}^{\mathsf T}\boldsymbol{\alpha}$ = 对角元之和 |
| 分块 | 左列切法 = 右行切法才能分块乘；分块对角的幂 = 各块的幂；$AB=\sum_k\boldsymbol{a}_k\boldsymbol{b}_k^{\mathsf T}$ |
