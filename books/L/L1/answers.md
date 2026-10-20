## L.1 · 向量与线性组合（答案）

### A 基础

**L1-01**
**答案：** (1) $\boldsymbol{x}=(1,5,3,1)^{\mathsf T}$；(2) $\boldsymbol{y}=\boldsymbol{m}$。

(1) 两边乘 2 再加 $-\boldsymbol{u}$：$\boldsymbol{x}=2\boldsymbol{m}-\boldsymbol{u}=(6,9,4,3)^{\mathsf T}-(5,4,1,2)^{\mathsf T}=(1,5,3,1)^{\mathsf T}$。

(2) 两边乘 3 移项：$\boldsymbol{y}=3\boldsymbol{m}-(\boldsymbol{u}+\boldsymbol{x})$。由 (1)，$\boldsymbol{u}+\boldsymbol{x}=2\boldsymbol{m}$，所以 $\boldsymbol{y}=3\boldsymbol{m}-2\boldsymbol{m}=\boldsymbol{m}$：前两个的平均已经是 $\boldsymbol{m}$，再加进一个 $\boldsymbol{m}$，平均不变。

区分点：巩固「向量等式按运算律移项」；(2) 先整体代入 $\boldsymbol{u}+\boldsymbol{x}=2\boldsymbol{m}$，不必逐个分量硬算。

**L1-02**
**答案：** $k=4$。

设 $\boldsymbol{b}=c_1\boldsymbol{a}_1+c_2\boldsymbol{a}_2=(c_1,\ c_1+c_2,\ c_2)^{\mathsf T}$。第一、三个分量不含 $k$，直接定出 $c_1=1$、$c_2=3$；含 $k$ 的第二个分量用来检验，要求 $k=c_1+c_2=4$。$k\ne4$ 时不能表示。

区分点：巩固「向量等式拆成分量方程，多出来的那条方程就是 $\boldsymbol{b}$ 能被表示的条件」。

**L1-03**
**答案：** (1) $k\ne4$；(2) 直线 $\{c(1,2)^{\mathsf T}\}$；$(3,6)^{\mathsf T}$ 有无穷多种表示，$(1,0)^{\mathsf T}$ 不能表示。

(1) 张成 $\mathbb{R}^2$ 当且仅当不共线：$1\cdot k-2\cdot2\ne0$，$k\ne4$。
(2) $k=4$ 时 $\boldsymbol{a}_2=2\boldsymbol{a}_1$，组合都是 $(c_1+2c_2)\boldsymbol{a}_1$。$(3,6)^{\mathsf T}=3\boldsymbol{a}_1$，凡 $c_1+2c_2=3$ 都行；$(1,0)^{\mathsf T}$ 不是 $\boldsymbol{a}_1$ 的倍数。

区分点：巩固「不共线才张成平面；共线时张成退成直线，系数不唯一」。

**L1-04**
**答案：** (D)。

$\boldsymbol{a}_2=2\boldsymbol{a}_1$，两者共线，任一组合都是 $(c_1+2c_2)\boldsymbol{a}_1$，张成是过原点的直线，(D) 对。(A) 按个数判断张成：共线的两个向量只张成直线。(B) 错：$(3,6,9)^{\mathsf T}=3\boldsymbol{a}_1$，凡 $c_1+2c_2=3$ 都行，如 $(3,0)$、$(1,1)$。(C) 只核对了前两个分量：任一组合的第三个分量都是第一个的 3 倍，而 $4\ne3$，不能表示。

区分点：巩固「共线时张成退成直线、系数不唯一，前几个分量对上后还要检验其余分量」。

**L1-05**
**答案：** (D)。

凸组合 $c_1\boldsymbol{e}_1+c_2\boldsymbol{e}_2=(c_1,c_2)^{\mathsf T}$，$c_1+c_2=1$ 且 $c_1,c_2\ge0$，所以 $x+y=1$、$0\le x\le1$，(D) 对。(A) 漏了非负：$-1<0$。(B) 把夹逼当成充分条件：$(0.2,0.3)^{\mathsf T}$ 两个分量都在 $[0,1]$ 里，但 $0.2+0.3\ne1$。(C) 混淆张成与凸组合：$(1,1)^{\mathsf T}$ 在张成里，系数和却是 2。

区分点：巩固凸组合要同时满足「和为 1」与「非负」，分量在范围内只是必要条件。

### B 进阶

**L1-06**
**答案：** 两个张成互相包含，所以相等。

记 $\boldsymbol{b}_1=\boldsymbol{a}_1+\boldsymbol{a}_2$，$\boldsymbol{b}_2=\boldsymbol{a}_1-\boldsymbol{a}_2$。

右边包含于左边：任取 $x\boldsymbol{b}_1+y\boldsymbol{b}_2$，代入合并得 $(x+y)\boldsymbol{a}_1+(x-y)\boldsymbol{a}_2$，是 $\boldsymbol{a}_1,\boldsymbol{a}_2$ 的组合。

左边包含于右边：先反解，两式相加、相减得 $\boldsymbol{a}_1=\frac12(\boldsymbol{b}_1+\boldsymbol{b}_2)$，$\boldsymbol{a}_2=\frac12(\boldsymbol{b}_1-\boldsymbol{b}_2)$。任取 $c_1\boldsymbol{a}_1+c_2\boldsymbol{a}_2$，代入得 $\frac{c_1+c_2}2\boldsymbol{b}_1+\frac{c_1-c_2}2\boldsymbol{b}_2$，是 $\boldsymbol{b}_1,\boldsymbol{b}_2$ 的组合。

两个方向都成立，两个集合相等。证明没有用到 $\boldsymbol{a}_1,\boldsymbol{a}_2$ 是否共线。

区分点：只说「$\boldsymbol{b}_1,\boldsymbol{b}_2$ 在左边的张成里」只证了一个方向；要反解出 $\boldsymbol{a}_1,\boldsymbol{a}_2$ 才能补上另一个方向。

**L1-07**
**答案：** (D)。

(D)：任给 $(x,y,z)^{\mathsf T}$，设 $c_1(1,1,0)^{\mathsf T}+c_2(0,1,1)^{\mathsf T}+c_3(1,0,1)^{\mathsf T}=(x,y,z)^{\mathsf T}$，得 $c_1+c_3=x$，$c_1+c_2=y$，$c_2+c_3=z$。三式相加得 $c_1+c_2+c_3=\frac{x+y+z}2$，再分别减去三式：$c_2=\frac{-x+y+z}2$，$c_3=\frac{x-y+z}2$，$c_1=\frac{x+y-z}2$。任何向量都能表示，张成是 $\mathbb{R}^3$。

(A) 错：两两不共线是两个向量时的说法，管不了三个；第三个向量等于前两个之差，三者只张成平面 $z=x+y$（讲义例 3）。(B) 错：个数多不等于张成大，四个向量的分量和都是 0，任何组合的分量和也是 0，拼不出 $(0,0,1)^{\mathsf T}$。(C) 错：零向量不添任何方向，剩下两个不共线向量只张成一个平面。

区分点：判断张成要实际解出系数，或找出所有组合都满足的方程；个数、两两关系都不能代替这一步。

**L1-08**
**答案：** (1) 不是；(2) 四个权重的解不唯一，一组解带负数不说明所有解都带负数；(3) $(c_1,c_2,c_3,c_4)=(s-\frac12,\frac34-s,\frac34-s,s)$，$\frac12\le s\le\frac34$；例如 $s=\frac12$ 时为 $(0,\frac14,\frac14,\frac12)$，只用 $\boldsymbol{p}_2,\boldsymbol{p}_3,\boldsymbol{p}_4$。

(1) 对前三个向量设权重为 $c_1,c_2,c_3$。由 $2c_2=1.5$、$2c_3=1.5$ 得 $c_2=c_3=\frac34$，于是 $c_1=1-\frac34-\frac34=-\frac12<0$，所以不是凸组合。

(2) 四个向量只有两个分量方程和一个权重和方程，却有四个未知数，解不唯一。他只检验了 $c_4=\frac14$ 这一组，负数只说明这一组不行。

(3) 令 $c_4=s$。由两个分量方程 $2c_2+2s=1.5$、$2c_3+2s=1.5$，得 $c_2=c_3=\frac34-s$；再由权重和为 1，得 $c_1=s-\frac12$。四个权重全非负当且仅当 $s\ge\frac12$ 且 $s\le\frac34$。取 $s=\frac12$，得到 $(0,\frac14,\frac14,\frac12)$，并且 $\frac14\boldsymbol p_2+\frac14\boldsymbol p_3+\frac12\boldsymbol p_4=(1.5,1.5)^{\mathsf T}$。

区分点：「找到一组带负数的解」不等于「没有全非负的解」；权重不唯一时，要用参数写出全部解，再由非负条件定出参数范围。

**L1-09**
**答案：** (1) $a=5$ 且 $b\ne2$；(2) $a\ne5$（$b$ 任意）；(3) $a=5$、$b=2$，全部表示为 $\boldsymbol{\beta}=c\boldsymbol{\alpha}_1+(1-2c)\boldsymbol{\alpha}_2+c\boldsymbol{\alpha}_3$，$c$ 任意。

按分量列方程：
$$c_1+c_2+c_3=1,\quad c_1+2c_2+3c_3=b,\quad c_1+3c_2+ac_3=3.$$
第二式减第一式、第三式减第二式，消去 $c_1$：$c_2+2c_3=b-1$，$c_2+(a-3)c_3=3-b$；两式再相减消去 $c_2$：$(a-5)c_3=4-2b$。

$a\ne5$ 时 $c_3=\frac{4-2b}{a-5}$ 唯一确定，倒推 $c_2=b-1-2c_3$、$c_1=1-c_2-c_3$ 也唯一。$a=5$ 时左边恒为 0：$b\ne2$ 则矛盾，不能表示；$b=2$ 则 $c_3=c$ 任取，$c_2=1-2c$，$c_1=c$。

用张成看 $a=5$：这时 $\boldsymbol{\alpha}_3=2\boldsymbol{\alpha}_2-\boldsymbol{\alpha}_1$ 是多余的，张成只是平面 $x-2y+z=0$，$\boldsymbol{\beta}$ 在其上当且仅当 $1-2b+3=0$。

区分点：要化到 $(a-5)c_3=4-2b$ 再讨论，$a=5$ 时不能除以 $a-5$；并能解释成「$\boldsymbol{\alpha}_3$ 多余、张成退化成平面」。

### C 提高

**L1-10**
**答案：** (1) $a=5$；(2) 张成是平面 $x-2y+z=0$，只有 $\boldsymbol{\gamma}_3$ 能表示，$\boldsymbol{\gamma}_3=(2+s)\boldsymbol{\alpha}_1+(1-2s)\boldsymbol{\alpha}_2+s\boldsymbol{\alpha}_3$，$s$ 任意；(3) 能。

(1) 对一般的 $(x,y,z)^{\mathsf T}$ 照 L1-09 消元：$c_1+c_2+c_3=x$，$c_1+2c_2+3c_3=y$，$c_1+3c_2+ac_3=z$，后式减前式得 $c_2+2c_3=y-x$，$c_2+(a-3)c_3=z-y$，再相减得
$$(a-5)c_3=x-2y+z .$$
$a\ne5$ 时对任何右端都能解出 $c_3$，再倒推 $c_2,c_1$，任何向量都能表示，三个 $\boldsymbol{\gamma}_i$ 当然都能，与题设矛盾，所以 $a=5$。还要验证 $a=5$ 时确有 $\boldsymbol{\gamma}_i$ 不能表示：这时方程要求 $x-2y+z=0$，而 $\boldsymbol{\gamma}_1$ 代入得 $1-0+1=2\ne0$。

(2) $a=5$ 时，由上面的消元，$(x,y,z)^{\mathsf T}$ 能表示当且仅当 $x-2y+z=0$（这时 $c_3$ 任取都能倒推出 $c_2,c_1$），张成就是这张平面；也可以看出 $\boldsymbol{\alpha}_3=2\boldsymbol{\alpha}_2-\boldsymbol{\alpha}_1$ 是多余的。$\boldsymbol{\gamma}_1$ 得 2，$\boldsymbol{\gamma}_2$ 得 $0-2+1=-1$，都不在平面上；$\boldsymbol{\gamma}_3$ 得 $3-8+5=0$，在平面上。令 $c_3=s$，由 $c_2+2c_3=4-3$ 得 $c_2=1-2s$，再由 $c_1=3-c_2-c_3$ 得 $c_1=2+s$。

(3) 任给 $(x,y,z)^{\mathsf T}$，设 $d_1\boldsymbol{\gamma}_1+d_2\boldsymbol{\gamma}_2+d_3\boldsymbol{\gamma}_3=(x,y,z)^{\mathsf T}$：$d_1+3d_3=x$，$d_2+4d_3=y$，$d_1+d_2+5d_3=z$。第三式减去前两式得 $-2d_3=z-x-y$，$d_3=\frac{x+y-z}2$，再得 $d_1,d_2$。任何向量都能由 $\boldsymbol{\gamma}_1,\boldsymbol{\gamma}_2,\boldsymbol{\gamma}_3$ 表示，三个 $\boldsymbol{\alpha}_i$ 当然都能。

区分点：「不能都表示」要翻译成「张成不是整个空间」，为此先对一般右端消元，证明 $a\ne5$ 时任何向量都能表示；只求出 $a=5$ 而不验证确有 $\boldsymbol{\gamma}_i$ 落在平面外，充分性就缺了；把「表示不唯一」当成「不能表示」也会错。

**L1-11**
**答案：** (1) $\alpha=\frac14$，$\beta=\frac12$，$\gamma=\frac14$；(2) 见下；(3) 原凸组合约束下无解；放宽非负条件后唯一有符号解为 $\alpha=\frac12$，$\beta=\frac23$，$\gamma=-\frac16$。

(1) 四个分量加上「和为 1」共 5 个方程、3 个未知数，先用其中三个定出权重，其余两个检验。为了消去 $\gamma$，把 $\gamma=1-\alpha-\beta$ 代入第一、四个分量：
$$5\alpha+4\beta+(1-\alpha-\beta)=3.5\ \Rightarrow\ 4\alpha+3\beta=2.5;\qquad 2\alpha+\beta+4(1-\alpha-\beta)=2\ \Rightarrow\ 2\alpha+3\beta=2.$$
相减得 $\alpha=\frac14$，再得 $\beta=\frac12$，$\gamma=\frac14$。检验第二、三个分量：$4\cdot\frac14+5\cdot\frac12+2\cdot\frac14=4$，$\frac14+2\cdot\frac12+5\cdot\frac14=2.5$，都对；权重非负。

(2) 看第一个分量。用 $\alpha+\beta+\gamma=1$ 改写：$5\alpha+4\beta+\gamma=5(\alpha+\beta+\gamma)-\beta-4\gamma=5-\beta-4\gamma$。要它等于 5，须 $\beta+4\gamma=0$；而 $\beta,\gamma\ge0$，只能 $\beta=\gamma=0$，于是 $\alpha=1$，组合就是 $\boldsymbol{u}=(5,4,1,2)^{\mathsf T}$，第二个分量是 4 而不是 5，矛盾。

(3) 现在已放宽非负条件，只保留和为 1。同 (1) 的消元：$4\alpha+3\beta+1=5$，$-2\alpha-3\beta+4=1$，即 $4\alpha+3\beta=4$，$2\alpha+3\beta=3$，得 $\alpha=\frac12$，$\beta=\frac23$，$\gamma=-\frac16$；第二、三个分量 $2+\frac{10}3-\frac13=5$，$\frac12+\frac43-\frac56=1$，都对。两条方程把 $\alpha,\beta$ 唯一定出，这组权重是唯一解；和为 1 但 $\gamma<0$，所以 $(5,5,1,1)^{\mathsf T}$ 只是线性组合，不是凸组合，与 (2) 一致。（$\boldsymbol{u},\boldsymbol{v},\boldsymbol{w}$ 和两个目标的分量和都是 12，「和为 1」那条方程其实由分量方程自动保证。）

区分点：(2) 把「分量夹在最大值以内」的推导用在取到最大值的边界上，逼出权重；(3) 说明「和为 1」的解存在不等于是凸组合，非负那一条才是关键。

### 章末混合练习

**L1-12**
**答案：** (1) $k=4$；(2) $\boldsymbol{a}_1+\boldsymbol{a}_2=-\boldsymbol{b}_1+\boldsymbol{b}_2$；(3) 不能。（方法 2 的比较系数、方法 3；高中平面向量）

(1) $\boldsymbol{b}_1\ne\boldsymbol{0}$（否则 $\boldsymbol{a}_1=-2\boldsymbol{a}_2$，与不共线矛盾），所以共线当且仅当 $\boldsymbol{b}_2=\lambda\boldsymbol{b}_1$，即 $2\boldsymbol{a}_1+k\boldsymbol{a}_2=\lambda\boldsymbol{a}_1+2\lambda\boldsymbol{a}_2$。$\boldsymbol{a}_1,\boldsymbol{a}_2$ 不共线，比较系数：$\lambda=2$，$k=4$。

(2) 设 $\boldsymbol{a}_1+\boldsymbol{a}_2=x\boldsymbol{b}_1+y\boldsymbol{b}_2=(x+2y)\boldsymbol{a}_1+(2x+3y)\boldsymbol{a}_2$，比较系数：$x+2y=1$，$2x+3y=1$，得 $x=-1$，$y=1$。

(3) $k=4$ 时 $\boldsymbol{b}_2=2\boldsymbol{b}_1$，张成是直线 $\{x\boldsymbol{b}_1\}$。若 $\boldsymbol{a}_1=x\boldsymbol{a}_1+2x\boldsymbol{a}_2$，比较系数得 $x=1$ 且 $2x=0$，矛盾。

区分点：没有坐标只能比较系数，依据是 $\boldsymbol{a}_1,\boldsymbol{a}_2$ 不共线；(1) 还要先排除 $\boldsymbol{b}_1=\boldsymbol{0}$。

**L1-13**
**答案：** (1) 见下；(2) 在内部，$\lambda=\frac5{12}$，$\mu=\frac13$。（方法 4、方法 2 的比较系数；高中平面向量）

(1) 记点 $A,B,C,P$ 的位置向量分别为 $\boldsymbol a,\boldsymbol b,\boldsymbol c,\boldsymbol p$；条件移项合并得 $\boldsymbol{p}=(1-\lambda-\mu)\boldsymbol{a}+\lambda\boldsymbol{b}+\mu\boldsymbol{c}$，系数和恒为 1。

充分性：三个系数都非负，$\boldsymbol{p}$ 是三个顶点的凸组合，由讲义第 4 节落在三角形内（含边界）。

必要性：$P$ 在三角形内时，第 4 节的反方向论证给出非负、和为 1 的 $c_1,c_2,c_3$ 使 $\boldsymbol{p}=c_1\boldsymbol{a}+c_2\boldsymbol{b}+c_3\boldsymbol{c}$，代入 $c_1=1-c_2-c_3$ 得 $\overrightarrow{AP}=c_2\overrightarrow{AB}+c_3\overrightarrow{AC}$。$\overrightarrow{AB},\overrightarrow{AC}$ 不共线，与已知式比较系数：$\lambda=c_2\ge0$，$\mu=c_3\ge0$，$\lambda+\mu=1-c_1\le1$。

(2) $(2,1)^{\mathsf T}=\lambda(4,0)^{\mathsf T}+\mu(1,3)^{\mathsf T}$：第二个分量给 $\mu=\frac13$，第一个给 $\lambda=\frac5{12}$，$\lambda+\mu=\frac34\le1$。

区分点：必要性里三角形给的是「某一组」权重，要靠 $\overrightarrow{AB},\overrightarrow{AC}$ 不共线、系数唯一，才能断定它就是题中的 $\lambda,\mu$。

**L1-14**
**答案：** (1) 最高 $-2\%$，组合为 $(\frac13,\frac23,0)$，即三分之一股票型、三分之二混合型；(2) 恰好是 $[-3,-2]$ 里的全部值。（方法 4，加上解含一个参数的不等式）

(1) 设权重 $w_1,w_2,w_3\ge0$，$w_1+w_2+w_3=1$。行情好时 $12w_1+6w_2=8$，所以 $w_2=\frac43-2w_1$；再由和为 1，$w_3=1-w_1-w_2=w_1-\frac13$。三个未知数只有两个方程，留下 $w_1$ 一个自由参数，它的范围由「权重非负」决定：$w_2\ge0$ 给 $w_1\le\frac23$，$w_3\ge0$ 给 $w_1\ge\frac13$，$w_1\ge0$ 自动满足，所以 $\frac13\le w_1\le\frac23$。

行情差时的收益率是
$$-6w_1+0\cdot w_2+3w_3=-6w_1+3\Big(w_1-\frac13\Big)=-3w_1-1,$$
随 $w_1$ 增大而减小，在 $w_1=\frac13$ 取最大值 $-2$，此时 $w_2=\frac23$，$w_3=0$。检查：$12\cdot\frac13+6\cdot\frac23=8$，$-6\cdot\frac13=-2$。

(2) $w_1$ 取遍 $[\frac13,\frac23]$ 时，$-3w_1-1$ 取遍 $[-3,-2]$；最小值 $-3$ 在 $(\frac23,0,\frac13)$ 取到。几何上，直线「行情好时收益为 8」穿过三角形 $\boldsymbol{f}_1\boldsymbol{f}_2\boldsymbol{f}_3$，截出的线段两端是 $(8,-3)$ 和 $(8,-2)$。

区分点：要意识到两个方程、三个未知数留下一个自由参数，并由「权重非负」把参数限制在区间里，再在区间上求最值；只会解唯一解的人在这里卡住。
