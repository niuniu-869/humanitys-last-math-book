## L.8 · 向量空间（速记）

| 提示 | 内容 |
|---|---|
| 子空间 | 非空、对加法和数乘封闭（⇔ 对线性组合封闭）；必含 $\boldsymbol{0}$，不含零向量立刻排除 |
| 三类常见子空间 | 张成 $\operatorname{span}$；列空间 $C(A)=\{A\boldsymbol{x}\}$（变换的像，使 $A\boldsymbol{x}=\boldsymbol{b}$ 有解的 $\boldsymbol{b}$）；零空间 $N(A)=\{A\boldsymbol{x}=\boldsymbol{0}\}$（被压到原点的方向） |
| 不是子空间 | $\boldsymbol{b}\ne\boldsymbol{0}$ 时 $A\boldsymbol{x}=\boldsymbol{b}$ 的解集；两个子空间的并（如 $x_1x_2=0$）；否定只需一个反例 |
| 基、维数 | 基 = 无关且张成；表示唯一；任意两组基个数相同（替换定理），个数叫 $\dim V$；$\dim\mathbb{R}^n=n$ |
| $\dim V=d$ 时 | $d+1$ 个向量必相关；$d$ 个无关向量就是基；无关组可扩充成基；$W\subseteq V$ 且维数相等 ⇒ $W=V$ |
| 方法 2 | 向量作列、行变换，取**原来的**主元列为基；$\dim\operatorname{span}(\boldsymbol{a}_i)=r(\boldsymbol{a}_i)$；扩充时先查新向量不在原张成里 |
| 过渡矩阵 | 基 = 尺子，换基 = 换尺子量同一个箭头；$(\boldsymbol{\beta})=(\boldsymbol{\alpha})P$，$P$ 的第 $j$ 列 = $\boldsymbol{\beta}_j$ 的旧坐标；有分量时 $(A\mid B)\to(E\mid P)$ |
| 坐标变换 | $\boldsymbol{x}=P\boldsymbol{y}$（旧 = $P$·新）；新坐标解 $P\boldsymbol{y}=\boldsymbol{x}$；$(\boldsymbol{\alpha})P$ 是基 ⇔ $P$ 可逆 |
| 易错：方向 | 管基时 $P$ 从旧到新，管坐标时从新到旧；从新基到旧基的过渡矩阵是 $P^{-1}$ |
| 秩–零化度 | $\dim N(A)=n-r(A)$，$n$ 是**列数**；$\dim C(A)+\dim N(A)=n$ |
| 四个子空间 | $C(A)$：$r$；$C(A^{\mathsf T})$：$r$；$N(A)$：$n-r$；$N(A^{\mathsf T})$：$m-r$ |
| 正交补 | $N(A)=C(A^{\mathsf T})^{\perp}$，$C(A)=N(A^{\mathsf T})^{\perp}$；$A\boldsymbol{x}=\boldsymbol{b}$ 有解 ⇔ $\boldsymbol{b}$ 与左零空间正交；$\boldsymbol{x}=\boldsymbol{x}_r+\boldsymbol{x}_n$，$A\boldsymbol{x}=A\boldsymbol{x}_r$ |
| 易错：行变换 | 行空间不变（取变换后的非零行）；列空间会变（取变换前的主元列） |
| 一般线性空间 | 八条运算律；$P_n$ 维数 $n+1$（基 $1,t,\dots,t^n$），$\mathbb{R}^{m\times n}$ 维数 $mn$（基 $E_{ij}$）；用坐标化成数组计算 |
| 线性变换的矩阵 | $T(\boldsymbol{\alpha})=(\boldsymbol{\alpha})A$，第 $j$ 列 = $T\boldsymbol{\alpha}_j$ 的坐标；换基 $B=P^{-1}AP$（$P$ 译出、$A$ 作用、$P^{-1}$ 译回） |
