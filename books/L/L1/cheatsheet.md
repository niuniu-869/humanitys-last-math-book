## L.1 · 向量与线性组合（速记）

| 提示 | 内容 |
|---|---|
| $n$ 维向量 | 一串有顺序的 $n$ 个实数，外加加法、数乘两条规定；默认是列向量，横写记作 $(a_1,\dots,a_n)^{\mathsf T}$；相等 ⇔ 维数相同且各分量相等 |
| 加法、数乘 | 逐个分量做：$\boldsymbol a+\boldsymbol b=(a_i+b_i)$，$k\boldsymbol a=(ka_i)$；维数不同不能相加；运算律从实数继承，可以移项 |
| 清单与箭头 | 清单用来算，箭头用来想；$n\ge4$ 画不出，结论只靠定义和运算律推 |
| 线性组合 | $c_1\boldsymbol a_1+\cdots+c_k\boldsymbol a_k$；$\boldsymbol b$ 能被线性表示 ⇔ 方程组有解（方法 2） |
| 方法 2 | 设系数、按分量列方程；方程多于未知数时，先用几个方程唯一定出系数，其余的检验，对不上就不能表示 |
| $\boldsymbol e_i$ | $\boldsymbol b=b_1\boldsymbol e_1+\cdots+b_n\boldsymbol e_n$，系数就是分量 |
| 张成 | $\operatorname{span}$ = 全部线性组合，总过原点；$\boldsymbol b\in\operatorname{span}$ ⇔ $\boldsymbol b$ 能被线性表示 |
| 共线 | 一个是另一个的倍数，零向量与任何向量共线；平面上 $(p,q)^{\mathsf T},(r,s)^{\mathsf T}$ 共线 ⇔ $ps-qr=0$ |
| 张成的形状 | 一个非零向量 → 直线；两个不共线 → 平面（在 $\mathbb R^2$ 里是整个平面）；共线的第二个向量什么也不添，且系数不唯一 |
| 方法 3 | 新向量能由旧向量表示 → 张成不变（多余的箭头，L.7 叫线性相关）；不能 → 张成变大一档 |
| 比较系数 | $\boldsymbol a_1,\boldsymbol a_2$ 不共线时，$c_1\boldsymbol a_1+c_2\boldsymbol a_2=d_1\boldsymbol a_1+d_2\boldsymbol a_2\Rightarrow c_1=d_1,\ c_2=d_2$ |
| 凸组合 | 系数非负且和为 1；只要求和为 1 → 过两点的直线，再要求非负 → 线段 $\boldsymbol p_1+t(\boldsymbol p_2-\boldsymbol p_1)$，$0\le t\le1$；三点 → 三角形（两步混合） |
| 方法 4 | 列方程，加上 $c_1+\cdots+c_k=1$，解出后查符号；权重唯一时有负数就不是凸组合，不唯一时要在全部解里找全非负的 |
| 易错：夹逼 | 凸组合每个分量夹在最小值与最大值之间，这是必要条件，不是充分条件 |
| 易错：两两不共线 | 在 $\mathbb R^3$ 里，三个两两不共线的向量也可能只张成一个平面 |
