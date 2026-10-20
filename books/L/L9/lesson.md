## L.9 · 线性方程组解的结构

一片街区里有四个路口围成一圈，车辆不会凭空多出或消失，所以每个路口都满足「驶入 = 驶出」。把每段路上每小时的车流量设成未知数，每个路口列一个方程，就得到一个线性方程组。

这个方程组有个特点：四个方程加起来，每段路的流量在驶入和驶出里各出现一次，正好抵消，所以其中一个方程是多余的。解于是不唯一，留下一个自由参数。它告诉调度员：让一部分车沿整个环多绕一圈，每个路口仍然平衡。调度员要知道的是全部解组成的集合长什么样：哪些量能自由调，哪些量被别的量锁死。

L.4 已经会解具体的方程组，但有没有解、有多少解，要消元到底才知道。19 世纪后半叶，人们逐步认识到答案只取决于两个数：系数矩阵的秩和增广矩阵的秩。这个判据在不同的书里挂着不同的名字，如鲁歇–卡佩利定理、克罗内克–卡佩利定理。

用 L.3 以来的语言说，$A\boldsymbol x=\boldsymbol b$ 问的是：变换 $A$ 把哪些向量送到 $\boldsymbol b$？第 1 节会看到，有没有解、有几个解，在变换里各有一个画面。

本章第 1 节用秩判断有没有解、解是否唯一；第 2 节用有限几个解写出齐次方程组的全部解；第 3 节说明非齐次方程组的全部解是「一个特解加上零空间」；第 4 节处理系数里带参数的方程组；第 5 节反过来，用解空间推出关于秩的结论；第 6 节是支线，讨论两个方程组的公共解和同解。

### 1. 方程组什么时候有解，什么时候解唯一？

先拿老朋友④投影试一试。它的矩阵是

$$A=\frac12\begin{pmatrix}1&1\\1&1\end{pmatrix},$$

作用是把平面垂直地压到直线 $x_2=x_1$ 上。按列来看，$A\boldsymbol x$ 是两列以 $x_1,x_2$ 为系数的组合，两列都是 $\frac12(1,1)^{\mathsf T}$，所以

$$A\boldsymbol x=\frac{x_1+x_2}{2}\begin{pmatrix}1\\1\end{pmatrix}.$$

无论 $\boldsymbol x$ 取什么，结果都落在直线 $x_2=x_1$ 上。

现在解两个方程组：$A\boldsymbol x=(1,0)^{\mathsf T}$ 和 $A\boldsymbol x=(1,1)^{\mathsf T}$。

第一个无解。$(1,0)^{\mathsf T}$ 不是 $(1,1)^{\mathsf T}$ 的倍数，不在变换的像上。

第二个有无穷多个解。要求 $\frac{x_1+x_2}{2}=1$，也就是 $x_1+x_2=2$，于是 $(2,0)^{\mathsf T}$、$(0,2)^{\mathsf T}$、$(3,-1)^{\mathsf T}$ 都是解，整条直线 $x_1+x_2=2$ 都被压到同一个点 $(1,1)$。这些解两两之差都是 $(-1,1)^{\mathsf T}$ 的倍数，而 $A(-1,1)^{\mathsf T}=\boldsymbol 0$：这个方向整个被压到了原点。

![粗实线 $x_2=x_1$ 是④的像；直线 $x_1+x_2=2$ 整条被压到 $(1,1)$，都是解；$(1,0)$ 不在像上，无解；虚线整条被压到原点](fig/L9-n2.pdf){width=62%}

这个小例子里藏着本节的两句话：有没有解，看 $\boldsymbol b$ 在不在像里；解有几个，看有没有方向被压到原点。像就是列空间 $C(A)$，被压到原点的方向组成零空间 $N(A)$（L.8.1、L.8.4）。下面把这两句话都换成秩，这样只知道秩也能下结论。

#### 有没有解：比较两个秩

把 $\boldsymbol b$ 添到 $A$ 的右边，得到增广矩阵 $(A\mid\boldsymbol b)$。它的列比 $A$ 多一个 $\boldsymbol b$，所以它的列空间包含 $C(A)$。分两种情况：

- $\boldsymbol b\in C(A)$ 时，$\boldsymbol b$ 能由 $A$ 的列线性表示，添进来不带来新方向，两个列空间相同，$r(A\mid\boldsymbol b)=r(A)$。
- $\boldsymbol b\notin C(A)$ 时，从 $A$ 的列里取一个极大无关组（$r(A)$ 个向量），再添上 $\boldsymbol b$。由 L.7.2，无关组添一个向量后如果相关，这个向量就能由原来的组表示；$\boldsymbol b$ 不能被表示，所以添上后仍然无关。$(A\mid\boldsymbol b)$ 的其余列都能由这 $r(A)+1$ 个向量表示，所以它们是 $(A\mid\boldsymbol b)$ 的列的极大无关组（L.7.4），$r(A\mid\boldsymbol b)=r(A)+1$。

所以

$$A\boldsymbol x=\boldsymbol b\ \text{有解}\iff r(A)=r(A\mid\boldsymbol b).$$

在阶梯形里，这就是没有矛盾行。矛盾行形如 $(0,\dots,0\mid d)$，$d\ne0$，它让增广矩阵比 $A$ 多出一个非零行。

#### 解有几个：看零空间

设 $\boldsymbol x_1,\boldsymbol x_2$ 都是解，两式相减，

$$A(\boldsymbol x_1-\boldsymbol x_2)=\boldsymbol b-\boldsymbol b=\boldsymbol 0,$$

两个解之差在零空间里。反过来，一个解加上零空间里的任何向量 $\boldsymbol\xi$，$A(\boldsymbol x_1+\boldsymbol\xi)=\boldsymbol b+\boldsymbol 0=\boldsymbol b$，仍是解。

所以有解的前提下，零空间只有零向量时解唯一；零空间里有一个非零向量 $\boldsymbol\xi$，所有的 $k\boldsymbol\xi$ 都在里面，解就有无穷多个。由秩–零化度定理（L.8.4），$\dim N(A)=n-r(A)$，所以解唯一当且仅当 $r(A)=n$。

把两部分合起来。设 $A$ 是 $m\times n$ 矩阵：

$$\begin{cases}r(A)<r(A\mid\boldsymbol b) & \text{无解},\\ r(A)=r(A\mid\boldsymbol b)=n & \text{唯一解},\\ r(A)=r(A\mid\boldsymbol b)<n & \text{无穷多解，有 }n-r(A)\text{ 个自由未知量}.\end{cases}$$

本节的主干就是这三行。

三种说法对照如下：

| 方程组 | 列向量 | 变换 |
|---|---|---|
| $r(A)=r(A\mid\boldsymbol b)$，有解 | $\boldsymbol b$ 能由 $A$ 的列线性表示 | $\boldsymbol b$ 在像里 |
| $r(A)=n$，有解时唯一 | $A$ 的列线性无关 | 没有方向被压到原点 |
| $r(A)<n$，有解时无穷多 | $A$ 的列线性相关 | 有方向被压到原点 |

这三行有三个常用的特殊情形。

第一，齐次方程组 $A\boldsymbol x=\boldsymbol 0$ 总有零解，因为增广的那一列全是零，不改变秩。所以它有非零解当且仅当 $r(A)<n$。

第二，方程个数 $m$ 少于未知数个数 $n$ 时，$r(A)\le m<n$，齐次方程组必有非零解。$A$ 是方阵时，$r(A)<n$ 就是 $|A|=0$（L.6.3）。

第三，若 $r(A)=m$（行满秩），则 $A\boldsymbol x=\boldsymbol b$ 对任何 $\boldsymbol b$ 都有解。理由是增广矩阵只有 $m$ 行，秩不超过 $m$，又不小于 $r(A)=m$，只能等于 $m$。

**方法 1（秩判别法）**

1. 把增广矩阵 $(A\mid\boldsymbol b)$ 化成行阶梯形。
2. 数左边 $A$ 那部分的非零行，得 $r(A)$；数整个矩阵的非零行，得 $r(A\mid\boldsymbol b)$。
3. 两个秩不等就无解，相等就有解。
4. 有解时，再拿 $r(A)$ 和未知数个数 $n$ 比：相等则唯一，小于则有无穷多解。

**例 1**　设 $A=\begin{pmatrix}1&1&2\\2&1&3\\1&0&1\end{pmatrix}$，判断 $A\boldsymbol x=\boldsymbol b$ 在 $\boldsymbol b=(1,3,2)^{\mathsf T}$ 和 $\boldsymbol b'=(1,3,1)^{\mathsf T}$ 时解的情况。

两个右端项的消元步骤完全相同，可以并排放在竖线右边一起做。

第一步，第 2 行减第 1 行的 2 倍，第 3 行减第 1 行：

$$\left(\begin{array}{ccc|cc}1&1&2&1&1\\2&1&3&3&3\\1&0&1&2&1\end{array}\right)\to\left(\begin{array}{ccc|cc}1&1&2&1&1\\0&-1&-1&1&1\\0&-1&-1&1&0\end{array}\right).$$

第二步，新的第 3 行减新的第 2 行：

$$\to\left(\begin{array}{ccc|cc}1&1&2&1&1\\0&-1&-1&1&1\\0&0&0&0&-1\end{array}\right).$$

第三步，数秩。左边有两个非零行，$r(A)=2<3$。对 $\boldsymbol b$，第 3 行是 $0=0$，$r(A\mid\boldsymbol b)=2=r(A)$，有无穷多解，自由未知量 $3-2=1$ 个。对 $\boldsymbol b'$，第 3 行是 $0=-1$，$r(A\mid\boldsymbol b')=3$，无解。

原因是 $A$ 的第 3 行等于第 2 行减第 1 行，有解时右端也须满足 $b_3=b_2-b_1$，$\boldsymbol b'$ 不满足。

> 判断方程组 $x_1+x_2=3$，$x_1-x_2=1$，$2x_1+x_2=5$，$x_1+2x_2=4$ 解的情况。
>
> 答案：4 个方程、2 个未知数，消元后 $r(A)=r(A\mid\boldsymbol b)=2=n$，有唯一解 $x_1=2$，$x_2=1$。方程比未知数多，只要没有矛盾，解仍可唯一。

下一道例题不给数字，考的是齐次和非齐次之间的推断，这是选择题的高频考点。

**例 2**　设 $A$ 是 $m\times n$ 矩阵，判断下列说法的对错：(1) 若 $A\boldsymbol x=\boldsymbol 0$ 只有零解，则 $A\boldsymbol x=\boldsymbol b$ 有唯一解；(2) 若 $A\boldsymbol x=\boldsymbol 0$ 有非零解，则 $A\boldsymbol x=\boldsymbol b$ 有无穷多解；(3) 若 $A\boldsymbol x=\boldsymbol b$ 有无穷多解，则 $A\boldsymbol x=\boldsymbol 0$ 有非零解。

(1)(2) 都错。只有零解说明 $r(A)=n$，有非零解说明 $r(A)<n$，它们管的是「解有几个」，管不了「有没有解」。反例：$A=\begin{pmatrix}1\\1\end{pmatrix}$，$\boldsymbol b=(1,2)^{\mathsf T}$ 时方程是 $x=1$ 和 $x=2$，互相矛盾，(1) 不成立；$A=\begin{pmatrix}1&1\\1&1\end{pmatrix}$，$\boldsymbol b=(1,2)^{\mathsf T}$ 时齐次方程组有非零解，非齐次方程组却无解，(2) 不成立。

(3) 对。有两个不同的解，它们的差就是齐次方程组的一个非零解。

规律是：齐次方程组只反映 $r(A)$ 和 $n$ 的比较，决定的是解有几个；有没有解要另看 $\boldsymbol b$ 在不在列空间里。所以从齐次推非齐次，只能推出「如果有解，那么唯一（或无穷多）」。

合上书，用④说出「有没有解」和「解有几个」各自对应变换的哪个画面，再写出那三行判别式。

### 2. 齐次方程组的无穷多个解，怎样用有限几个写全？

$A\boldsymbol x=\boldsymbol 0$ 有非零解时，解有无穷多个，不可能一个个列出来。但它们组成零空间 $N(A)$，是一个子空间，而子空间只要给出一组基就完全确定了。

先拿老朋友⑤三阶压扁试一试：

$$A=\begin{pmatrix}1&2&1\\2&4&3\\3&6&4\end{pmatrix}\to\begin{pmatrix}1&2&0\\0&0&1\\0&0&0\end{pmatrix}.$$

右边是它的行最简形。主元在第 1、3 列，$x_2$ 是自由未知量，方程化为 $x_1=-2x_2$，$x_3=0$。令 $x_2=1$，得 $(-2,1,0)^{\mathsf T}$，全部解就是它的倍数 $k(-2,1,0)^{\mathsf T}$。⑤把空间压成一个平面，被压到原点的只有这一条直线，一个向量就把无穷多个解写全了。

#### 基础解系

设 $r(A)=r<n$。如果 $\boldsymbol\xi_1,\dots,\boldsymbol\xi_{n-r}$ 满足三条：

1. 都是 $A\boldsymbol x=\boldsymbol 0$ 的解；
2. 线性无关；
3. 每个解都能由它们线性表示，

就称它们是 $A\boldsymbol x=\boldsymbol 0$ 的一个**基础解系**。它就是 $N(A)$ 的一组基。于是全部解可以写成

$$\boldsymbol x=k_1\boldsymbol\xi_1+k_2\boldsymbol\xi_2+\cdots+k_{n-r}\boldsymbol\xi_{n-r},\qquad k_1,\dots,k_{n-r}\ \text{为任意常数},$$

叫作齐次方程组的**通解**。

基础解系不唯一，正像一个子空间有许多组基。由 L.8.2，$n-r$ 维空间里任意 $n-r$ 个无关的向量都是基。所以检验一组向量是不是基础解系，只需查三件事：都是解，线性无关，个数等于 $n-r$。第 3 条「能表示全部解」不必再验证，维数替我们保证了。

**方法 2（求基础解系与通解）**

1. 把系数矩阵化成行最简形，数出 $r$，找出 $n-r$ 个自由未知量。
2. 用自由未知量表示每个主元未知量。
3. 让自由未知量依次取一组单位向量，读出 $n-r$ 个解，就是基础解系。有分数时，可以让自由未知量取分母的倍数（例如取 2），只是把基向量伸缩了一下。
4. 写出通解 $k_1\boldsymbol\xi_1+\cdots+k_{n-r}\boldsymbol\xi_{n-r}$。

第 3 步读出的解为什么一定无关？第 $k$ 个解在第 $k$ 个自由未知量的位置上不为零，在其余自由未知量的位置上都是 0。设它们的组合等于零向量，只看第 $k$ 个自由未知量那个分量，就得到第 $k$ 个系数为 0。每个 $k$ 都这样看，系数全为 0。

**例 3**　求方程组 $\begin{cases}2x_1+x_2-x_3+x_4=0\\4x_1+2x_2+x_3-x_4=0\\2x_1+x_2+2x_3-2x_4=0\end{cases}$ 的基础解系与通解。

第一步，消元。第 2 行减第 1 行的 2 倍得 $(0,0,3,-3)$，第 3 行减第 1 行也得 $(0,0,3,-3)$，再用第 3 行减第 2 行，成为零行：

$$A\to\begin{pmatrix}2&1&-1&1\\0&0&3&-3\\0&0&0&0\end{pmatrix}.$$

第二步，化成行最简形。第 2 行除以 3，再加到第 1 行，最后把第 1 行除以 2：

$$\to\begin{pmatrix}1&\frac12&0&0\\0&0&1&-1\\0&0&0&0\end{pmatrix}.$$

第三步，读出关系。主元在第 1、3 列，$r=2$，$x_2,x_4$ 自由：

$$x_1=-\tfrac12x_2,\qquad x_3=x_4.$$

第四步，取值。为了避开分数，$x_2$ 取 2、$x_4$ 取 0，得 $\boldsymbol\xi_1=(-1,2,0,0)^{\mathsf T}$；$x_2$ 取 0、$x_4$ 取 1，得 $\boldsymbol\xi_2=(0,0,1,1)^{\mathsf T}$。它们在自由未知量的位置上是 $(2,0)$ 和 $(0,1)$，按上面的理由无关；个数 $2=4-2$。通解为

$$\boldsymbol x=k_1(-1,2,0,0)^{\mathsf T}+k_2(0,0,1,1)^{\mathsf T}.$$

> 求 $\begin{cases}x_1+x_2+x_3+x_4=0\\x_1-x_2+2x_3-x_4=0\end{cases}$ 的基础解系与通解。
>
> 答案：行最简形给出 $x_1=-\frac32x_3$，$x_2=\frac12x_3-x_4$。取 $x_3=2,x_4=0$ 得 $(-3,1,2,0)^{\mathsf T}$，取 $x_3=0,x_4=1$ 得 $(0,-1,0,1)^{\mathsf T}$，通解是它们的任意组合。

下一道例题没有方程，只给了一个基础解系，问怎样的组合仍是基础解系。用的就是上面的「查三件事」。

**例 4**　设 $\boldsymbol\eta_1,\boldsymbol\eta_2,\boldsymbol\eta_3$ 是 $A\boldsymbol x=\boldsymbol 0$ 的一个基础解系，下列各组是否也是基础解系？(1) $\boldsymbol\eta_1+\boldsymbol\eta_2,\ \boldsymbol\eta_2+\boldsymbol\eta_3,\ \boldsymbol\eta_3+\boldsymbol\eta_1$；(2) $\boldsymbol\eta_1-\boldsymbol\eta_2,\ \boldsymbol\eta_2-\boldsymbol\eta_3,\ \boldsymbol\eta_3-\boldsymbol\eta_1$；(3) $\boldsymbol\eta_1,\ \boldsymbol\eta_1+\boldsymbol\eta_2$。

三组都是解，因为零空间对线性组合封闭。由原来的基础解系有 3 个向量，知道 $n-r=3$。

(1) 三个新向量写成 $(\boldsymbol\eta_1,\boldsymbol\eta_2,\boldsymbol\eta_3)K$，系数矩阵 $K$ 的三列是各自的组合系数：

$$K=\begin{pmatrix}1&0&1\\1&1&0\\0&1&1\end{pmatrix},\qquad |K|=2\ne0.$$

由 L.8.3，原来的组无关时，新组无关当且仅当 $K$ 可逆，所以三个新向量无关，个数也对，是基础解系。

(2) 三个向量相加等于 $\boldsymbol 0$，线性相关，不是。

(3) 两个向量无关，但个数 $2<3$，张不满三维的解空间，不是。「无关」与「个数」缺一不可。

合上书，说出基础解系要满足的三个条件，以及为什么知道 $n-r$ 以后，「能表示全部解」这一条可以不验证。

### 3. 非齐次方程组的全部解长什么样？

非齐次方程组 $A\boldsymbol x=\boldsymbol b$（$\boldsymbol b\ne\boldsymbol 0$）能不能也这样写？

这里多数人会卡一下，因为直觉上「解」都该是同一类东西。可是零向量不是它的解：$A\boldsymbol 0=\boldsymbol 0\ne\boldsymbol b$，所以解集不经过原点。

而几个向量的全部线性组合里一定有零向量（系数全取 0）。解集里没有零向量，所以它不可能写成「几个向量的全部组合」。它是什么样子，还是先拿⑤看。

#### 先看一个画面

⑤的第 3 列是 $(1,3,4)^{\mathsf T}$，所以解 $A\boldsymbol x=(1,3,4)^{\mathsf T}$ 时，取 0 份第 1 列、0 份第 2 列、1 份第 3 列就行，$\boldsymbol\eta^*=(0,0,1)^{\mathsf T}$ 是一个解。

再看 $(-2,1,1)^{\mathsf T}$：

$$A\begin{pmatrix}-2\\1\\1\end{pmatrix}=-2\begin{pmatrix}1\\2\\3\end{pmatrix}+\begin{pmatrix}2\\4\\6\end{pmatrix}+\begin{pmatrix}1\\3\\4\end{pmatrix}=\begin{pmatrix}1\\3\\4\end{pmatrix},$$

也是解。它和 $\boldsymbol\eta^*$ 之差是 $(-2,1,0)^{\mathsf T}$，正是第 2 节求出的零空间方向。从 $\boldsymbol\eta^*$ 出发沿这个方向走多远都行，$A\boldsymbol x$ 一直不变，因为走的那一段被压成了零。

![虚线是零空间，实线是全部解，两线平行；从 $\boldsymbol\eta^*=(0,0,1)$ 沿 $\boldsymbol\xi=(-2,1,0)$ 走到 $(-2,1,1)$，仍在实线上](fig/L9-n3.pdf){width=62%}

#### 一般的结论

设 $\boldsymbol\eta^*$ 是 $A\boldsymbol x=\boldsymbol b$ 的某一个解，叫作**特解**。第 1 节已经证过两件事：任一解 $\boldsymbol x$ 与 $\boldsymbol\eta^*$ 之差满足 $A(\boldsymbol x-\boldsymbol\eta^*)=\boldsymbol 0$；反过来，对任何 $\boldsymbol\xi\in N(A)$，

$$A(\boldsymbol\eta^*+\boldsymbol\xi)=\boldsymbol b+\boldsymbol 0=\boldsymbol b.$$

前一件说每个解都形如 $\boldsymbol\eta^*+\boldsymbol\xi$，后一件说这样的向量都是解。所以全部解恰好是 $\{\boldsymbol\eta^*+\boldsymbol\xi:\boldsymbol\xi\in N(A)\}$。用基础解系写出来，**通解**是

$$\boldsymbol x=\boldsymbol\eta^*+k_1\boldsymbol\xi_1+\cdots+k_{n-r}\boldsymbol\xi_{n-r}.$$

可以记成「一个落脚点，加上所有能自由走动的方向」。落脚点是特解，自由走动的方向是零空间，沿零空间走，$A\boldsymbol x$ 不变。

落脚点换成别的解也行，写出的集合相同。能走的方向却只有零空间这一组，多不得也少不得。

#### 几个解的组合还是不是解？

先在平面上看。方程 $x_1+2x_2=4$ 的两个解 $(4,0)^{\mathsf T}$、$(0,2)^{\mathsf T}$ 之差在零空间里，之和 $(4,2)^{\mathsf T}$ 却满足 $4+4=8$，跑到了另一条直线上。

![实线（解集）是虚线（零空间）平移到 $\boldsymbol\eta^*$ 处；两解之差在虚线上，两解之和 $(4,2)$ 落在点线 $x_1+2x_2=8$ 上，不再是解](fig/L9-n1.pdf){width=60%}

一般地，设 $\boldsymbol\eta_1,\dots,\boldsymbol\eta_s$ 都是 $A\boldsymbol x=\boldsymbol b$ 的解，由矩阵乘法的线性，

$$A(c_1\boldsymbol\eta_1+\cdots+c_s\boldsymbol\eta_s)=c_1\boldsymbol b+\cdots+c_s\boldsymbol b=(c_1+\cdots+c_s)\boldsymbol b.$$

所以组合仍是 $A\boldsymbol x=\boldsymbol b$ 的解，当且仅当系数之和为 1；是 $A\boldsymbol x=\boldsymbol 0$ 的解，当且仅当系数之和为 0。系数和为 1 保住了 $\boldsymbol b$，系数和为 0 把 $\boldsymbol b$ 消掉。两个解之和的系数和是 2，得到的是 $A\boldsymbol x=2\boldsymbol b$ 的解，正是图里的点线。

**方法 3（求非齐次方程组的通解）**

1. 把增广矩阵化成行最简形，先用方法 1 确认有解。
2. 令自由未知量全取 0，读出特解 $\boldsymbol\eta^*$。
3. 把最后一列换成 0，按方法 2 读出基础解系。
4. 写成 $\boldsymbol\eta^*+k_1\boldsymbol\xi_1+\cdots+k_{n-r}\boldsymbol\xi_{n-r}$。

**例 5**　求 $\begin{cases}x_1+2x_2-x_3+x_4=2\\2x_1+4x_2-x_3+3x_4=5\\x_1+2x_2+x_3+3x_4=4\end{cases}$ 的通解。

第一步，用第 1 行消去下面两行的 $x_1$：第 2 行减第 1 行的 2 倍，第 3 行减第 1 行。

$$\left(\begin{array}{cccc|c}1&2&-1&1&2\\2&4&-1&3&5\\1&2&1&3&4\end{array}\right)\to\left(\begin{array}{cccc|c}1&2&-1&1&2\\0&0&1&1&1\\0&0&2&2&2\end{array}\right).$$

第二步，第 3 行减第 2 行的 2 倍，成为零行；再把第 2 行加到第 1 行，消掉第 1 行的 $x_3$：

$$\to\left(\begin{array}{cccc|c}1&2&0&2&3\\0&0&1&1&1\\0&0&0&0&0\end{array}\right).$$

第三步，判断。$r(A)=r(A\mid\boldsymbol b)=2<4$，有无穷多解，方程化为

$$x_1=3-2x_2-2x_4,\qquad x_3=1-x_4.$$

第四步，读解。令 $x_2=x_4=0$，得特解 $\boldsymbol\eta^*=(3,0,1,0)^{\mathsf T}$。去掉常数项，$x_2=1,x_4=0$ 得 $\boldsymbol\xi_1=(-2,1,0,0)^{\mathsf T}$；$x_2=0,x_4=1$ 得 $\boldsymbol\xi_2=(-2,0,-1,1)^{\mathsf T}$。通解是

$$\boldsymbol x=(3,0,1,0)^{\mathsf T}+k_1(-2,1,0,0)^{\mathsf T}+k_2(-2,0,-1,1)^{\mathsf T}.$$

> 求 $\begin{cases}x_1-x_2+x_3=1\\2x_1-2x_2+3x_3=4\end{cases}$ 的通解。
>
> 答案：第 2 行减第 1 行的 2 倍得 $x_3=2$，代回得 $x_1=x_2-1$。特解 $(-1,0,2)^{\mathsf T}$，基础解系 $(1,1,0)^{\mathsf T}$，通解 $(-1,0,2)^{\mathsf T}+k(1,1,0)^{\mathsf T}$。

下一道例题只给秩和几个解，特解与基础解系都要从已知的解里拼出来，用的正是「系数和为 1 或 0」。

**例 6**　四元方程组 $A\boldsymbol x=\boldsymbol b$ 的系数矩阵秩为 3，$\boldsymbol\eta_1,\boldsymbol\eta_2,\boldsymbol\eta_3$ 是它的三个解，$\boldsymbol\eta_1=(2,3,4,5)^{\mathsf T}$，$\boldsymbol\eta_2+\boldsymbol\eta_3=(1,2,3,4)^{\mathsf T}$。求通解。

第一步，定基础解系的个数：$n-r=4-3=1$，只需找一个非零的齐次解。

第二步，凑系数和为 0 的组合。已知量是 $\boldsymbol\eta_1$ 和 $\boldsymbol\eta_2+\boldsymbol\eta_3$，取 $2\boldsymbol\eta_1-(\boldsymbol\eta_2+\boldsymbol\eta_3)$，系数和是 $2-1-1=0$：

$$\boldsymbol\xi=2\boldsymbol\eta_1-(\boldsymbol\eta_2+\boldsymbol\eta_3)=(4,6,8,10)^{\mathsf T}-(1,2,3,4)^{\mathsf T}=(3,4,5,6)^{\mathsf T}.$$

它是 $A\boldsymbol x=\boldsymbol 0$ 的非零解，单独一个就构成基础解系。

第三步，特解取 $\boldsymbol\eta_1$，通解为

$$\boldsymbol x=(2,3,4,5)^{\mathsf T}+k(3,4,5,6)^{\mathsf T}.$$

为什么不用更顺手的 $\boldsymbol\eta_1-(\boldsymbol\eta_2+\boldsymbol\eta_3)$？它的系数和是 $-1$，得到的是 $A\boldsymbol x=-\boldsymbol b$ 的解。

最后看「一个特解加零空间」在机器学习里的样子。

**例 7**　线性回归是最基本的机器学习模型：用几个特征的加权和 $w_1x_1+w_2x_2+w_3x_3$ 预测一个量，权重 $\boldsymbol w=(w_1,w_2,w_3)^{\mathsf T}$ 要满足数据给出的方程组。某连锁店用三家门店的数据预测周利润（万元），三个特征依次是线上订单数、线下订单数、总订单数（百单）。三家店的特征分别是 $(2,1,3)$、$(1,3,4)$、$(3,2,5)$，利润分别是 5、5、8。把三家店的特征作为三行排成矩阵 $X$，要求预测与实际完全吻合，就是解 $X\boldsymbol w=\boldsymbol y$，$\boldsymbol y=(5,5,8)^{\mathsf T}$。求全部满足要求的权重，并说明能否据此判断「哪种订单更赚钱」。

第一步，求秩。总订单数等于线上加线下，所以 $X$ 的第 3 列等于前两列之和；前两列不成比例，$r(X)=2$。

第二步，判断有解并找特解。$\boldsymbol y=2\times(2,1,3)^{\mathsf T}+1\times(1,3,2)^{\mathsf T}$ 是前两列的组合，$r(X\mid\boldsymbol y)=2$，有解，特解 $\boldsymbol w^*=(2,1,0)^{\mathsf T}$。

第三步，找零空间。由 L.3.1，$X\boldsymbol w$ 就是以 $w_1,w_2,w_3$ 为系数把 $X$ 的三列组合起来。所以列之间的关系「第 1 列 + 第 2 列 − 第 3 列 = $\boldsymbol 0$」，把系数抄下来，正好是 $X(1,1,-1)^{\mathsf T}=\boldsymbol 0$。$N(X)$ 的维数是 $3-2=1$，$(1,1,-1)^{\mathsf T}$ 就是它的基。全部权重是

$$\boldsymbol w=(2,1,0)^{\mathsf T}+t(1,1,-1)^{\mathsf T},\qquad t\ \text{任意}.$$

第四步，解读。$t=2$ 时 $\boldsymbol w=(4,3,-2)^{\mathsf T}$，像是说「总订单越多利润越少」；$t=-1$ 时 $\boldsymbol w=(1,0,1)^{\mathsf T}$，又像是线下订单毫无贡献。可这些权重对任何门店的预测都相同，因为一家店的特征总满足「总数 = 线上 + 线下」，与 $(1,1,-1)^{\mathsf T}$ 的点积为零。

所以单个权重的大小不能解读，数据本身分不开三个特征各自的作用。实际做法是删掉多余的特征，或者在全部解里约定取长度最短的那个（L.15.4）。

合上书，用两行写出「通解 = 特解 + 齐次通解」的理由，再说明几个解的组合在什么条件下仍是解。

### 4. 系数里带参数时，怎样分情况讨论？

本章的方程组里，每个系数都是参数的整式，如 $\lambda$、$a-3$，所以每个子式都是参数的多项式。由 L.7.5，秩是最高阶非零子式的阶数。设参数取遍所有值时秩的最大值是 $r_0$，在取到它的参数值处，有一个 $r_0$ 阶子式不为零，所以这个子式作为多项式不恒为零，只有有限个根。不是根的参数值处它不为零，秩 $\ge r_0$；$r_0$ 又是最大值，所以秩 $=r_0$。秩下降的特殊值，就是让这类子式（消元时表现为某个主元）等于零的值。

所以先找出让秩下降的参数值，其余的值一起处理，再把特殊值逐个代入，按方法 1、3 判断并求解。可以记成「秩在哪个参数值下降，就在哪里分岔」。

找这些特殊值有两条路。

- 行列式路线。系数矩阵是方阵时，$|A|\ne0$ 等价于 $r(A)=n$，此时有唯一解，所以只需解 $|A|=0$。
- 消元路线。不是方阵、行列式难算，或者 $|A|$ 对所有参数都为零（比如有两行永远成比例）时，就带着参数消元，看哪些主元位置上的式子可能为零。

消元时不能除以含参数的式子，除非先把它为零的情形分出去。这是这类题最常丢分的一步。

**方法 4（含参数方程组的讨论）**

1. 用上面两条路之一找出特殊值（方阵时其余的值都有唯一解）。
2. 把每个特殊值代回增广矩阵，比较 $r(A)$ 与 $r(A\mid\boldsymbol b)$。
3. 有无穷多解时，按方法 3 写出通解。

**例 8**　讨论 $\lambda$ 取何值时，方程组 $\begin{cases}\lambda x_1+x_2+x_3=1\\x_1+\lambda x_2+x_3=\lambda\\x_1+x_2+\lambda x_3=\lambda^2\end{cases}$ 有唯一解、无解、无穷多解，并在有解时求解。

系数矩阵是方阵，走行列式路线。

第一步，算 $|A|$，分三小步。

- 每行元素之和都是 $\lambda+2$，所以把第 2、3 列加到第 1 列（倍加不改变行列式，L.6.2、L.6.4），第 1 列全变成 $\lambda+2$。
- 按第 1 列提出公因子 $\lambda+2$（行列式对一列是线性的）。
- 第 2、3 行各减第 1 行（倍加不变），化成上三角形，行列式等于对角元之积：

$$|A|=(\lambda+2)\begin{vmatrix}1&1&1\\1&\lambda&1\\1&1&\lambda\end{vmatrix}=(\lambda+2)\begin{vmatrix}1&1&1\\0&\lambda-1&0\\0&0&\lambda-1\end{vmatrix}=(\lambda+2)(\lambda-1)^2.$$

特殊值是 $\lambda=1$ 和 $\lambda=-2$。

第二步，$\lambda\ne1$ 且 $\lambda\ne-2$ 时有唯一解，分四小步求出来。

（a）求三个未知数之和。三个方程相加得

$$(\lambda+2)(x_1+x_2+x_3)=1+\lambda+\lambda^2,$$

记 $s=x_1+x_2+x_3=\frac{\lambda^2+\lambda+1}{\lambda+2}$。

（b）每个方程只留一个未知数。第一个方程是 $\lambda x_1+(x_2+x_3)=1$，把 $x_2+x_3=s-x_1$ 代进去，得 $(\lambda-1)x_1+s=1$。同样，后两个方程变成 $(\lambda-1)x_2+s=\lambda$，$(\lambda-1)x_3+s=\lambda^2$。

（c）把右边减 $s$ 通分：

$$1-s=\frac{1-\lambda^2}{\lambda+2},\qquad\lambda-s=\frac{\lambda-1}{\lambda+2},\qquad\lambda^2-s=\frac{\lambda^3+\lambda^2-\lambda-1}{\lambda+2}=\frac{(\lambda+1)^2(\lambda-1)}{\lambda+2},$$

第三个分子按 $\lambda^2(\lambda+1)-(\lambda+1)$ 分解。

（d）因为 $\lambda\ne1$，三式分别除以 $\lambda-1$：

$$x_1=-\frac{\lambda+1}{\lambda+2},\qquad x_2=\frac{1}{\lambda+2},\qquad x_3=\frac{(\lambda+1)^2}{\lambda+2}.$$

第三步，$\lambda=1$。三个方程都是 $x_1+x_2+x_3=1$，$r(A)=r(A\mid\boldsymbol b)=1<3$，无穷多解，通解为

$$\boldsymbol x=(1,0,0)^{\mathsf T}+k_1(-1,1,0)^{\mathsf T}+k_2(-1,0,1)^{\mathsf T}.$$

第四步，$\lambda=-2$。三个方程相加，左边是 $0$，右边是 $1-2+4=3$，矛盾，无解。用秩说：$A$ 的三行之和是零行，而前两行不成比例，$r(A)=2$；增广矩阵三行之和是 $(0,0,0\mid3)$，$r(A\mid\boldsymbol b)=3$。

> 讨论 $a,b$ 取何值时，$\begin{cases}x_1+x_2+x_3=1\\x_1+2x_2+3x_3=2\\x_1+3x_2+ax_3=b\end{cases}$ 有唯一解、无解、无穷多解，并在无穷多解时求通解。
>
> 答案：消元得三行 $(1,1,1\mid1)$、$(0,1,2\mid1)$、$(0,0,a-5\mid b-3)$。$a\ne5$ 时唯一解；$a=5,b\ne3$ 时无解；$a=5,b=3$ 时无穷多解，通解 $(0,1,0)^{\mathsf T}+k(1,-2,1)^{\mathsf T}$。

例 8 用行列式找特殊值。下一道例题有两个参数，行列式只能定出 $a$，管不到右端的 $b$，所以直接带着参数消元。

**例 9**　讨论 $a,b$ 取何值时，$\begin{cases}x_1+x_2+x_3+x_4=0\\x_2+2x_3+2x_4=1\\-x_2+(a-3)x_3-2x_4=b\\3x_1+2x_2+x_3+ax_4=-1\end{cases}$ 有唯一解、无解、无穷多解，并在无穷多解时求通解。

第一步，消元。第 4 行减第 1 行的 3 倍，得 $(0,-1,-2,a-3\mid-1)$；再把第 2 行分别加到第 3、4 行：

$$\left(\begin{array}{cccc|c}1&1&1&1&0\\0&1&2&2&1\\0&-1&a-3&-2&b\\3&2&1&a&-1\end{array}\right)\to\left(\begin{array}{cccc|c}1&1&1&1&0\\0&1&2&2&1\\0&0&a-1&0&b+1\\0&0&0&a-1&0\end{array}\right).$$

第二步，找分岔点。主元可能为零的位置只有两个 $a-1$，所以分 $a\ne1$ 和 $a=1$ 两种情况。这里不能把第 3 行直接除以 $a-1$。

第三步，$a\ne1$。四个主元都不为零，$r(A)=r(A\mid\boldsymbol b)=4$，有唯一解，从下往上回代即可求出。

第四步，$a=1$。后两行变成 $(0,0,0,0\mid b+1)$ 和零行，$r(A)=2$。若 $b\ne-1$，出现矛盾行，无解。若 $b=-1$，$r(A\mid\boldsymbol b)=2<4$，有无穷多解。此时用第 1 行减去第 2 行，方程化为 $x_1=-1+x_3+x_4$，$x_2=1-2x_3-2x_4$，通解为

$$\boldsymbol x=(-1,1,0,0)^{\mathsf T}+k_1(1,-2,1,0)^{\mathsf T}+k_2(1,-2,0,1)^{\mathsf T}.$$

把两道例题并排看。行列式路线一步就能定出特殊值，但只看系数、看不到右端项，而且只适用于方阵；消元路线慢一些，却同时看到系数和右端项。所以方阵而且右端只含同一个参数时，先算行列式；有两个参数或不是方阵时，直接消元。

合上书，说出含参数的方程组为什么只需在 $|A|=0$ 的根处单独讨论，以及消元时哪一步最容易出错。

### 5. 只知道秩和几个解，能写出通解、推出秩的关系吗？

这一节反过来，用解空间的维数推出矩阵的秩满足什么关系。考研常考三个结论，套路相同，都是把条件翻译成零空间的语言，再比维数。

第一个结论最常用；第二个是 L.10 最小二乘的基础；第三个专门对付伴随矩阵，它的证明要用到第一个。

#### 第一个结论：$AB=O$ 时 $r(A)+r(B)\le n$

先看具体的（$O$ 表示零矩阵）：

$$A=\begin{pmatrix}1&1\\1&1\end{pmatrix},\qquad B=\begin{pmatrix}1&2\\-1&-2\end{pmatrix},\qquad AB=O.$$

$A$ 的零空间是 $(1,-1)^{\mathsf T}$ 方向，$B$ 的两列 $(1,-1)^{\mathsf T}$、$(2,-2)^{\mathsf T}$ 都在这个方向上。$B$ 的列被零空间关住了，它的秩不可能超过零空间的维数 $2-1=1$。

一般地，设 $A$ 是 $m\times n$ 矩阵，$B$ 是 $n\times p$ 矩阵，$AB=O$，则 $r(A)+r(B)\le n$。证明三步：

1. 把 $B$ 按列分块（L.3.7），$AB=(A\boldsymbol b_1,\dots,A\boldsymbol b_p)=O$，所以每一列 $\boldsymbol b_j$ 都是 $A\boldsymbol x=\boldsymbol 0$ 的解。
2. 于是 $B$ 的列都在 $N(A)$ 里，它们张成的列空间也在里面：$C(B)\subseteq N(A)$。
3. 子空间的维数不超过包含它的子空间，$r(B)=\dim C(B)\le\dim N(A)=n-r(A)$，移项即得。

记法是「$B$ 的每一列都掉进了 $A$ 的零空间」。

**方法 5（用解空间推秩）**

1. 条件里出现 $AB=O$、$A^{\mathsf T}A$、伴随矩阵 $A^*$（L.6.8）或已知几个解时，先把它翻译成「某些向量在零空间里」或「两个零空间相同」。
2. 用秩–零化度定理 $\dim N(A)=n-r(A)$ 比较维数，再用「非零矩阵的秩至少是 1」之类的基本事实收尾。

**例 10**　设 $A=\begin{pmatrix}1&2&-2\\2&-1&\lambda\\3&1&-1\end{pmatrix}$，$B$ 是非零的三阶矩阵，$AB=O$。求 $\lambda$，并说明 $|B|=0$。

第一步，$B\ne O$，所以 $r(B)\ge1$。由第一个结论，$r(A)\le3-r(B)\le2$，$A$ 不可逆，$|A|=0$。

第二步，按第 1 行展开：

$$|A|=1\cdot(1-\lambda)-2\cdot(-2-3\lambda)+(-2)\cdot(2+3)=5\lambda-5,$$

所以 $\lambda=1$。

第三步，这时 $A$ 的第 3 行等于前两行之和，前两行不成比例，$r(A)=2$。于是 $r(B)\le3-2=1<3$，$B$ 不可逆，$|B|=0$。

> 设 $A$ 是 $4\times3$ 矩阵，$r(A)=2$，三阶矩阵 $B\ne O$ 满足 $AB=O$，求 $r(B)$ 并说明理由。
>
> 答案：$r(B)\le3-2=1$，又 $B\ne O$ 时 $r(B)\ge1$，所以 $r(B)=1$。这里的 $n$ 是 $A$ 的列数 3，不是行数 4。

#### 第二个结论：实矩阵 $r(A^{\mathsf T}A)=r(A)$

先看具体的：$A=\begin{pmatrix}1&2\\2&4\end{pmatrix}$ 的秩是 1，$A^{\mathsf T}A=\begin{pmatrix}5&10\\10&20\end{pmatrix}$ 第 2 行是第 1 行的 2 倍，秩也是 1。

一般地，设 $A$ 是实的 $m\times n$ 矩阵。证明的思路是：证明 $A$ 和 $A^{\mathsf T}A$ 的零空间相同。它们的列数都是 $n$，由秩–零化度定理，秩就相同。

1. 若 $A\boldsymbol x=\boldsymbol 0$，则 $A^{\mathsf T}A\boldsymbol x=A^{\mathsf T}\boldsymbol 0=\boldsymbol 0$，所以 $N(A)\subseteq N(A^{\mathsf T}A)$。
2. 若 $A^{\mathsf T}A\boldsymbol x=\boldsymbol 0$，两边左乘 $\boldsymbol x^{\mathsf T}$，得
$$\boldsymbol x^{\mathsf T}A^{\mathsf T}A\boldsymbol x=(A\boldsymbol x)^{\mathsf T}(A\boldsymbol x)=\lVert A\boldsymbol x\rVert^2=0.$$
这里用了 $(A\boldsymbol x)^{\mathsf T}=\boldsymbol x^{\mathsf T}A^{\mathsf T}$（L.3.6），以及向量与自己的点积是长度的平方（L.2.2；$\lVert\boldsymbol a\rVert$ 就是高中的 $|\boldsymbol a|$，用双竖线是为了和数的绝对值区分）。长度为零的向量只有零向量，所以 $A\boldsymbol x=\boldsymbol 0$，反方向的包含也成立。
3. $N(A^{\mathsf T}A)=N(A)$，两者都有 $n$ 列，$r(A^{\mathsf T}A)=n-\dim N(A)=r(A)$。

第 2 步是关键，它只在实数范围里成立。换成复数就不对了：$A=(1,\mathrm{i})^{\mathsf T}$ 的秩是 1，而 $A^{\mathsf T}A=1+\mathrm{i}^2=0$，秩是 0。实数时「$\boldsymbol x^{\mathsf T}\boldsymbol x$ 是长度的平方」，复数时这一步不能照搬。

推论：$A$ 的列线性无关（$r(A)=n$）时，$n$ 阶方阵 $A^{\mathsf T}A$ 可逆。L.10.2 解最小二乘问题要用到它。

#### 第三个结论：伴随矩阵的秩只有三种

设 $A$ 是 $n$ 阶方阵（$n\ge2$），伴随矩阵 $A^*$ 的秩只有三种可能：

$$r(A^*)=\begin{cases}n, & r(A)=n,\\ 1, & r(A)=n-1,\\ 0, & r(A)<n-1.\end{cases}$$

先拿⑤看中间那种情形。⑤的秩是 $2=3-1$，算出它的伴随矩阵（每个元素是相应的代数余子式，L.6.8）：

$$A^*=\begin{pmatrix}-2&-2&2\\1&1&-1\\0&0&0\end{pmatrix}.$$

三列都是 $(-2,1,0)^{\mathsf T}$ 的倍数，秩是 1，而 $(-2,1,0)^{\mathsf T}$ 正是⑤的零空间方向。

证明按 $r(A)$ 分三种情况，每种只用一样旧工具。

1. $r(A)=n$ 时，$|A^*|=|A|^{n-1}\ne0$（L.6.8），$A^*$ 可逆。
2. $r(A)<n-1$ 时，$A$ 的 $n-1$ 阶子式全为零（L.7.5：秩是最高阶非零子式的阶数）。$A^*$ 的每个元素都是一个代数余子式，即带符号的 $n-1$ 阶子式，所以 $A^*=O$。
3. $r(A)=n-1$ 时，$AA^*=|A|E=O$。由第一个结论，$r(A)+r(A^*)\le n$，得 $r(A^*)\le1$；又有一个 $n-1$ 阶子式不为零，$A^*\ne O$，所以 $r(A^*)=1$。

第 3 步顺带说明了⑤的现象：由 $AA^*=O$，$A^*$ 的每一列都在 $N(A)$ 里；又 $\dim N(A)=n-(n-1)=1$，所以 $A^*$ 的任一非零列都能单独充当基础解系。

**例 11**　设 $n$ 阶矩阵 $A$（$n\ge2$）满足 $|A|=0$，元素 $a_{11}$ 的代数余子式 $A_{11}\ne0$。求 $A\boldsymbol x=\boldsymbol 0$ 的通解。

第一步，定秩。$A_{11}\ne0$ 说明有一个 $n-1$ 阶子式不为零，$r(A)\ge n-1$；又 $|A|=0$，$r(A)\le n-1$。所以 $r(A)=n-1$，基础解系只含一个向量。

第二步，找这个向量。$AA^*=|A|E=O$，所以 $A^*$ 的每一列都是解。$A^*$ 的第 $i$ 行第 $j$ 列是 $A_{ji}$（L.6.8），所以它的第 1 列由第 1 行元素的代数余子式组成，即 $(A_{11},A_{12},\dots,A_{1n})^{\mathsf T}$。它的第一个分量 $A_{11}\ne0$，非零。

第三步，通解为 $\boldsymbol x=k(A_{11},A_{12},\dots,A_{1n})^{\mathsf T}$。

合上书，默写三个结论的证明骨架，并说明第二个结论的哪一步用到了「长度为零的向量是零向量」。

### 6. 两个方程组的公共解和同解怎么判断？

两个方程组 $A\boldsymbol x=\boldsymbol 0$ 与 $B\boldsymbol x=\boldsymbol 0$（未知数个数相同）的**公共解**，是同时满足两组方程的解，也就是把两组方程联立：

$$\begin{pmatrix}A\\B\end{pmatrix}\boldsymbol x=\boldsymbol 0.$$

公共解的全体是 $N(A)\cap N(B)$，求公共解就是解这个上下拼起来的方程组。若已知其中一组的通解，也可以把通解代入另一组，求出参数应满足的条件。

**例 12**　求方程组 (I) $\begin{cases}x_1+x_2=0\\x_2-x_4=0\end{cases}$ 与 (II) $\begin{cases}x_1-x_2+x_3=0\\x_2-x_3+x_4=0\end{cases}$ 的公共解。

联立四个方程。由 (I)，$x_1=-x_2$，$x_4=x_2$。代入 (II) 的第一式，$-x_2-x_2+x_3=0$，得 $x_3=2x_2$。再代入 (II) 的第二式检验，$x_2-2x_2+x_2=0$ 恒成立。所以公共解为

$$\boldsymbol x=k(-1,1,2,1)^{\mathsf T}.$$

两个方程组**同解**，指解集完全相同，即 $N(A)=N(B)$。判据是

$$A\boldsymbol x=\boldsymbol 0\ \text{与}\ B\boldsymbol x=\boldsymbol 0\ \text{同解}\iff r(A)=r(B)=r\begin{pmatrix}A\\B\end{pmatrix}.$$

理由用维数。$N(A)\cap N(B)\subseteq N(A)$，两者相等当且仅当维数相等，由秩–零化度定理，即 $r\begin{pmatrix}A\\B\end{pmatrix}=r(A)$。同样，交集与 $N(B)$ 相等当且仅当 $r\begin{pmatrix}A\\B\end{pmatrix}=r(B)$。两个条件同时成立时，$N(A)=N(A)\cap N(B)=N(B)$。

只成立前一个，说明 $A\boldsymbol x=\boldsymbol 0$ 的解都是 $B\boldsymbol x=\boldsymbol 0$ 的解，反过来未必。

**方法 6（公共解与同解）**

1. 求公共解：把两组方程上下拼起来解，或把一组的通解代入另一组。
2. 判断同解：比较 $r(A)$、$r(B)$ 和拼起来的矩阵的秩，三者相等才同解。

> 判断 $\begin{cases}x_1+x_2=0\\x_2+x_3=0\end{cases}$ 与 $\begin{cases}x_1-x_3=0\\x_1+2x_2+x_3=0\end{cases}$ 是否同解。
>
> 答案：第二组的两行分别是第一组两行之差与之和，两组的秩都是 2，拼起来的秩仍是 2，所以同解，公共的通解是 $k(1,-1,1)^{\mathsf T}$。

合上书，说明同解为什么要求三个秩都相等，只有 $r(A)=r\begin{pmatrix}A\\B\end{pmatrix}$ 时能推出什么。

### 本章小结

| 方法 | 什么时候用 | 对应题号 |
|---|---|---|
| 方法 1（秩判别法） | 判断有无解、解是否唯一；齐次与非齐次之间的推断 | L9-01、L9-12、L9-14 |
| 方法 2（求基础解系与通解） | 齐次方程组的全部解；判断一组向量是否为基础解系 | L9-02、L9-11 |
| 方法 3（求非齐次方程组的通解） | 特解加齐次通解；由已知的几个解拼出通解 | L9-03、L9-06、L9-10、L9-11、L9-12 |
| 方法 4（含参数方程组的讨论） | 系数或右端含参数时分情况讨论 | L9-07、L9-10、L9-14 |
| 方法 5（用解空间推秩） | $AB=O$ 推秩，$r(A^{\mathsf T}A)=r(A)$，$r(A^*)$ 与伴随矩阵的列 | L9-05、L9-08 |
| 方法 6（公共解与同解） | 两个方程组的公共解、同解判断 | L9-04、L9-09 |

秩的等式链 $r(A)=\text{主元个数}=\dim C(A)=n-\dim N(A)$ 在本章添上一环：$\dim N(A)$ 就是基础解系所含向量的个数。

$n$ 阶方阵 $A$ 可逆的等价条件：

| 来自 | 条件 |
|---|---|
| L.4 | 消元后有 $n$ 个主元；$A\boldsymbol x=\boldsymbol b$ 对每个 $\boldsymbol b$ 都有唯一解；$A\boldsymbol x=\boldsymbol 0$ 只有零解 |
| L.5 | $A$ 可逆；存在 $B$ 使 $AB=E$ |
| L.6 | $\lvert A\rvert\ne0$ |
| L.7 | 列（行）向量组线性无关；$r(A)=n$ |
| L.8 | 列向量构成 $\mathbb{R}^n$ 的一组基；零空间只有零向量 |
| L.9（本章新增） | $A^{\mathsf T}A$ 可逆；$A^*$ 可逆（$n\ge2$） |
