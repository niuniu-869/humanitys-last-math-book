## L.10 · 正交与最小二乘

网店记下了几个月来每月的广告费和销量，想知道多投一万元广告大约能多卖多少件。把每个月画成平面上的一个点，这些点大体沿一条直线排开，却不会恰好共线，因为销量还受别的因素影响。要找的是离这些点「最近」的那条直线。估房价、预测销量用的线性回归，也是机器学习里最基础的模型之一，做的都是这件事。

把直线写成 $y=C+Dt$，每个数据点给出一个关于 $C,D$ 的一次方程。点多于两个时，这个方程组一般无解。无解时该取哪个 $\boldsymbol x$，就是本章的问题。

这个问题最早在天文和大地测量里变得紧迫。18 世纪的学者要从几十次带误差的观测定出轨道的几个参数，方程比未知数多，还互相矛盾。常用的办法是挑出几个方程来解，换一个人挑，答案就不同。1805 年，勒让德提出：取使误差平方和最小的那组参数。它不需要人为挑选，换谁算都一样。高斯 1809 年也发表了它，并称更早就在用，两人有优先权之争；高斯还从误差的概率分布给出了理由（M.2.1）。

C.24.5 用偏导数推过两个参数的情形。本章换个看法：误差平方和是长度的平方，平方和最小就是距离最近，而最近点由「垂直」刻画。

第 1 节说清最近点长什么样；第 2 节把它算出来；第 3 节看各方向两两垂直时为何好算；第 4 节研究由这样的方向排成的正交矩阵；第 5 节把任意一组基改造成两两垂直的；第 6 节回到数据，拟合直线。

### 1. 方程组无解时，哪个 x 让 Ax 离 b 最近？

先看一个小方程组：

$$x_1=6,\qquad x_1+x_2=0,\qquad x_1+2x_2=0.$$

前两个方程给出 $x_1=6$、$x_2=-6$，代入第三个得 $6-12=-6\ne0$，所以无解。写成 $A\boldsymbol x=\boldsymbol b$：

$$A=\begin{pmatrix}1&0\\1&1\\1&2\end{pmatrix},\qquad \boldsymbol b=\begin{pmatrix}6\\0\\0\end{pmatrix}.$$

用变换的语言看：$A$ 把平面 $\mathbb R^2$ 送进 $\mathbb R^3$，像是两列 $\boldsymbol a_1=(1,1,1)^{\mathsf T}$、$\boldsymbol a_2=(0,1,2)^{\mathsf T}$ 张成的一张过原点的平面，也就是列空间 $C(A)$。$\boldsymbol x$ 取遍 $\mathbb R^2$ 时，$A\boldsymbol x=x_1\boldsymbol a_1+x_2\boldsymbol a_2$ 走遍这张平面。无解就是 $\boldsymbol b$ 不在这张平面上。

够不着 $\boldsymbol b$，就退一步，在平面上找离它最近的点 $\boldsymbol p=A\hat{\boldsymbol x}$，用 $\hat{\boldsymbol x}$（读作「$x$ 帽」）代替不存在的解。距离用 L.2 的长度 $\lVert\cdot\rVert$ 来量，要最小化的是

$$\lVert\boldsymbol b-A\boldsymbol x\rVert^2=(6-x_1)^2+(0-x_1-x_2)^2+(0-x_1-2x_2)^2 .$$

右边三项正是三个方程误差的平方，所以「离 $\boldsymbol b$ 最近」就是「误差平方和最小」。

L.2.3 处理过直线的情形：垂足最近，残差与直线垂直。现在直线换成了平面，自然猜想仍是垂足最近，即残差 $\boldsymbol e=\boldsymbol b-\boldsymbol p$ 与平面里的每个向量都垂直。对一般的子空间 $S=\operatorname{span}(\boldsymbol a_1,\dots,\boldsymbol a_k)\subseteq\mathbb R^n$，这个猜想是对的：

**垂足最近**　设 $\boldsymbol b\in\mathbb R^n$，$\boldsymbol p\in S$，$\boldsymbol e=\boldsymbol b-\boldsymbol p$。如果 $\boldsymbol e$ 与每个 $\boldsymbol a_i$ 都正交，那么 $\boldsymbol p$ 是 $S$ 中离 $\boldsymbol b$ 最近的点，而且是唯一的最近点。

证明分两步。

第一步，只查生成向量就够了。$S$ 中任一向量可以写成 $c_1\boldsymbol a_1+\cdots+c_k\boldsymbol a_k$，按点积的分配律，

$$\boldsymbol e\cdot(c_1\boldsymbol a_1+\cdots+c_k\boldsymbol a_k)=c_1(\boldsymbol e\cdot\boldsymbol a_1)+\cdots+c_k(\boldsymbol e\cdot\boldsymbol a_k)=0,$$

所以 $\boldsymbol e$ 与整个 $S$ 正交。

第二步，用勾股定理。任取 $\boldsymbol q\in S$，把 $\boldsymbol b-\boldsymbol q$ 拆成 $\boldsymbol e+(\boldsymbol p-\boldsymbol q)$。$\boldsymbol p-\boldsymbol q$ 仍在 $S$ 里，由第一步它与 $\boldsymbol e$ 正交。两个正交向量之和的长度平方等于各自长度平方之和，因为展开 $(\boldsymbol u+\boldsymbol v)\cdot(\boldsymbol u+\boldsymbol v)$ 时交叉项 $2\,\boldsymbol u\cdot\boldsymbol v=0$。于是

$$\lVert\boldsymbol b-\boldsymbol q\rVert^2=\lVert\boldsymbol e\rVert^2+\lVert\boldsymbol p-\boldsymbol q\rVert^2\ge\lVert\boldsymbol e\rVert^2,$$

等号只在 $\boldsymbol q=\boldsymbol p$ 时成立。

![$\boldsymbol b$、$\boldsymbol p$、平面上任一点 $\boldsymbol q$ 构成直角在 $\boldsymbol p$ 的直角三角形，斜边 $\lVert\boldsymbol b-\boldsymbol q\rVert$ 不短于直角边 $\lVert\boldsymbol e\rVert$，所以垂足最近](fig/L10-n1.pdf){width=62%}

满足这个条件的 $\boldsymbol p$ 叫 $\boldsymbol b$ 在 $S$ 上的**正交投影**，简称投影。上面只证了「残差垂直 $\Rightarrow$ 最近」；反方向要等第 2 节说明垂直的 $\boldsymbol p$ 总存在以后才能下结论。

$S=C(A)$ 时，「$\boldsymbol e$ 与每一列正交」可以写成 $A^{\mathsf T}\boldsymbol e=\boldsymbol 0$，因为 $A^{\mathsf T}\boldsymbol e$ 的第 $i$ 个分量就是第 $i$ 列与 $\boldsymbol e$ 的点积。也就是说，残差落在左零空间 $N(A^{\mathsf T})$ 里（L.8.5）。

**方法 1（残差与每个生成向量正交）**

1. 设 $\boldsymbol p=x_1\boldsymbol a_1+\cdots+x_k\boldsymbol a_k$。
2. 对每个 $i$ 列方程 $(\boldsymbol b-\boldsymbol p)\cdot\boldsymbol a_i=0$，共 $k$ 个，解出系数。
3. 写出 $\boldsymbol p$ 和 $\boldsymbol e=\boldsymbol b-\boldsymbol p$，验算 $\boldsymbol e$ 与每个 $\boldsymbol a_i$ 的点积为 0。到 $S$ 的距离是 $\lVert\boldsymbol e\rVert$。

**例 1**　对开头的方程组，求使误差平方和最小的 $\hat{\boldsymbol x}$、对应的 $\boldsymbol p$ 和最小平方和。

思路：按方法 1 列两个正交条件，算点积。

第一步，把 $\boldsymbol p=x_1\boldsymbol a_1+x_2\boldsymbol a_2$ 代入 $(\boldsymbol b-\boldsymbol p)\cdot\boldsymbol a_1=0$，用分配律拆开，含 $x_1,x_2$ 的项留左边，$\boldsymbol b\cdot\boldsymbol a_1$ 移右边，得 $x_1(\boldsymbol a_1\cdot\boldsymbol a_1)+x_2(\boldsymbol a_2\cdot\boldsymbol a_1)=\boldsymbol b\cdot\boldsymbol a_1$；$\boldsymbol a_2$ 同理。

第二步，算点积：$\boldsymbol a_1\cdot\boldsymbol a_1=3$，$\boldsymbol a_1\cdot\boldsymbol a_2=0+1+2=3$，$\boldsymbol a_2\cdot\boldsymbol a_2=5$，$\boldsymbol b\cdot\boldsymbol a_1=6$，$\boldsymbol b\cdot\boldsymbol a_2=0$。代入得

$$3x_1+3x_2=6,\qquad 3x_1+5x_2=0.$$

第三步，两式相减得 $2x_2=-6$，$x_2=-3$，再得 $x_1=5$。于是

$$\boldsymbol p=5\boldsymbol a_1-3\boldsymbol a_2=(5,2,-1)^{\mathsf T},\qquad \boldsymbol e=\boldsymbol b-\boldsymbol p=(1,-2,1)^{\mathsf T}.$$

验算 $\boldsymbol e\cdot\boldsymbol a_1=1-2+1=0$，$\boldsymbol e\cdot\boldsymbol a_2=0-2+2=0$。最小平方和 $\lVert\boldsymbol e\rVert^2=6$。

你可能会想：为何不把 $\boldsymbol b$ 分别投影到 $\boldsymbol a_1$、$\boldsymbol a_2$ 上再相加？试一下。按 L.2.3 的公式 $\frac{\boldsymbol b\cdot\boldsymbol a_i}{\boldsymbol a_i\cdot\boldsymbol a_i}\boldsymbol a_i$，两个投影是 $\frac63\boldsymbol a_1=(2,2,2)^{\mathsf T}$ 和 $\frac05\boldsymbol a_2=\boldsymbol 0$，相加得 $(2,2,2)^{\mathsf T}$。它的残差 $(4,-2,-2)^{\mathsf T}$ 与 $\boldsymbol a_2$ 的点积是 $-6$，不垂直，所以不是最近点。

毛病出在 $\boldsymbol a_1$、$\boldsymbol a_2$ 不垂直：沿 $\boldsymbol a_1$ 量出的那一份在 $\boldsymbol a_2$ 方向上也有分量，分开量再相加会重复或遗漏。第 3 节会看到，生成向量两两垂直时，这个直接的做法恰好是对的。

> 平面 $z=x+y$ 由 $(1,0,1)^{\mathsf T}$、$(0,1,1)^{\mathsf T}$ 张成。求 $\boldsymbol b=(0,0,3)^{\mathsf T}$ 在这张平面上的投影，以及 $\boldsymbol b$ 到平面的距离。
>
> 答案：两个正交条件是 $2x_1+x_2=3$、$x_1+2x_2=3$，得 $x_1=x_2=1$，$\boldsymbol p=(1,1,2)^{\mathsf T}$，$\boldsymbol e=(-1,-1,1)^{\mathsf T}$，距离是 $\lVert\boldsymbol e\rVert=\sqrt3$。

合上书，画出 $\boldsymbol b$、$\boldsymbol p$、$\boldsymbol e$ 和平面上任一点 $\boldsymbol q$，说明垂足为什么最近、残差为什么只需与生成向量正交。

### 2. 这个最近点怎样算出来？

例 1 的方程里，左边的系数是两列两两的点积，右边是 $\boldsymbol b$ 与各列的点积。把这个规律用矩阵写出来，就得到对任何 $A$ 都能用的公式。

#### 正规方程

第 1 节已经把「$\boldsymbol e$ 与每一列正交」写成 $A^{\mathsf T}\boldsymbol e=\boldsymbol 0$。代入 $\boldsymbol e=\boldsymbol b-A\hat{\boldsymbol x}$：

$$A^{\mathsf T}(\boldsymbol b-A\hat{\boldsymbol x})=\boldsymbol 0 .$$

按分配律展开、移项，得到

$$A^{\mathsf T}A\,\hat{\boldsymbol x}=A^{\mathsf T}\boldsymbol b .$$

它叫**正规方程**（normal 意为「垂直」），它的解叫 $A\boldsymbol x=\boldsymbol b$ 的**最小二乘解**。

$A^{\mathsf T}$ 的第 $i$ 行是 $\boldsymbol a_i^{\mathsf T}$，所以 $A^{\mathsf T}A$ 的第 $(i,j)$ 元是 $\boldsymbol a_i\cdot\boldsymbol a_j$，$A^{\mathsf T}\boldsymbol b$ 的第 $i$ 个分量是 $\boldsymbol a_i\cdot\boldsymbol b$，正好是例 1 的系数。

正规方程什么时候有唯一解？L.9.5 证明过 $r(A^{\mathsf T}A)=r(A)$。$A^{\mathsf T}A$ 是 $k$ 阶方阵，所以它可逆当且仅当 $r(A)=k$，即 $A$ 的各列线性无关（列满秩）。这时

$$\hat{\boldsymbol x}=(A^{\mathsf T}A)^{-1}A^{\mathsf T}\boldsymbol b .$$

**方法 2（正规方程）**

1. 算出 $A^{\mathsf T}A$ 和 $A^{\mathsf T}\boldsymbol b$。
2. 解 $A^{\mathsf T}A\hat{\boldsymbol x}=A^{\mathsf T}\boldsymbol b$。
3. 写出 $\boldsymbol p=A\hat{\boldsymbol x}$、$\boldsymbol e=\boldsymbol b-\boldsymbol p$，验算 $A^{\mathsf T}\boldsymbol e=\boldsymbol 0$。

**例 2**　求下面方程组的最小二乘解和残差：

$$A=\begin{pmatrix}1&1\\1&1\\1&-1\\1&0\end{pmatrix},\qquad \boldsymbol b=\begin{pmatrix}3\\4\\2\\0\end{pmatrix}.$$

和例 1 相比，改用矩阵写法，方程多了一个。前两个方程 $x_1+x_2=3$ 与 $x_1+x_2=4$ 就矛盾。

第一步，算两个乘积。$A^{\mathsf T}A$ 的元素是两列的点积，$A^{\mathsf T}\boldsymbol b$ 的分量是各列与 $\boldsymbol b$ 的点积，例如两列之间是 $1+1-1+0=1$，第二列与 $\boldsymbol b$ 是 $3+4-2+0=5$。

$$A^{\mathsf T}A=\begin{pmatrix}4&1\\1&3\end{pmatrix},\qquad A^{\mathsf T}\boldsymbol b=\begin{pmatrix}9\\5\end{pmatrix}.$$

第二步，解 $4x_1+x_2=9$、$x_1+3x_2=5$。由第二式 $x_1=5-3x_2$，代入第一式得 $20-11x_2=9$，所以 $x_2=1$，$x_1=2$。

第三步，验算：

$$\boldsymbol p=A\hat{\boldsymbol x}=(3,3,1,2)^{\mathsf T},\qquad \boldsymbol e=(0,1,1,-2)^{\mathsf T},\qquad A^{\mathsf T}\boldsymbol e=(0+1+1-2,\ 0+1-1+0)^{\mathsf T}=\boldsymbol 0 .$$

> 求 $A=\begin{pmatrix}1&1\\1&2\\2&-1\\0&1\end{pmatrix}$、$\boldsymbol b=(4,4,0,3)^{\mathsf T}$ 的最小二乘解和残差。
>
> 答案：$A^{\mathsf T}A=\begin{pmatrix}6&1\\1&7\end{pmatrix}$，$A^{\mathsf T}\boldsymbol b=(8,15)^{\mathsf T}$，$\hat{\boldsymbol x}=(1,2)^{\mathsf T}$，$\boldsymbol e=(1,-1,0,1)^{\mathsf T}$。

#### 投影矩阵

列满秩时，投影是 $\boldsymbol p=A\hat{\boldsymbol x}=A(A^{\mathsf T}A)^{-1}A^{\mathsf T}\boldsymbol b$。把 $\boldsymbol b$ 前面的矩阵记作

$$P=A(A^{\mathsf T}A)^{-1}A^{\mathsf T},$$

叫到 $C(A)$ 的**投影矩阵**。用变换的语言说，$P$ 把每个向量垂直地压到 $C(A)$ 上。

最简单的情形只有一个非零列 $\boldsymbol a$。这时 $A^{\mathsf T}A$ 是数，

$$P=\frac{\boldsymbol a\boldsymbol a^{\mathsf T}}{\boldsymbol a^{\mathsf T}\boldsymbol a},\qquad P\boldsymbol b=\frac{\boldsymbol a^{\mathsf T}\boldsymbol b}{\boldsymbol a^{\mathsf T}\boldsymbol a}\,\boldsymbol a,$$

正是 L.2.3 的投影公式。取 $\boldsymbol a=(1,1)^{\mathsf T}$，$\boldsymbol a^{\mathsf T}\boldsymbol a=2$，得到

$$P=\frac12\begin{pmatrix}1&1\\1&1\end{pmatrix},$$

这就是 L.3 的老朋友④。它把平面垂直地压到直线 $y=x$ 上，见下图。

![老朋友④把每个点沿虚线垂直地压到直线 $y=x$ 上：$(3,1)^{\mathsf T}$ 落到 $(2,2)^{\mathsf T}$；直线上的点不动，所以 $P^2=P$](fig/L10-n3.pdf){width=55%}

投影矩阵有两个性质，考研常用。

第一，$P^2=P$。展开 $P^2=A(A^{\mathsf T}A)^{-1}(A^{\mathsf T}A)(A^{\mathsf T}A)^{-1}A^{\mathsf T}$，中间的 $(A^{\mathsf T}A)(A^{\mathsf T}A)^{-1}=E$ 消掉，剩下的就是 $P$。几何上，$P\boldsymbol b$ 已经在 $C(A)$ 里，再投影一次不动。

第二，$P^{\mathsf T}=P$。转置时三个因子倒序（L.3.6），得 $P^{\mathsf T}=A\big((A^{\mathsf T}A)^{-1}\big)^{\mathsf T}A^{\mathsf T}$。中间的因子不变：$\big((A^{\mathsf T}A)^{-1}\big)^{\mathsf T}=\big((A^{\mathsf T}A)^{\mathsf T}\big)^{-1}=(A^{\mathsf T}A)^{-1}$（L.5.1），即对称矩阵的逆仍对称。所以 $P^{\mathsf T}=P$。

#### 列不满秩时

列线性相关时，$A^{\mathsf T}A$ 不可逆，最小二乘解也不唯一。但正规方程一定有解。这是考研常见的证明题，按 L.9.1，只需证明系数矩阵与增广矩阵的秩相等：

1. 增广矩阵多一列，秩不会变小：$r(A^{\mathsf T}A)\le r(A^{\mathsf T}A\mid A^{\mathsf T}\boldsymbol b)$。
2. 按列分块（L.3.7），$(A^{\mathsf T}A\mid A^{\mathsf T}\boldsymbol b)=A^{\mathsf T}(A\mid\boldsymbol b)$。乘积的秩不超过每个因子的秩（L.7.7），所以它不超过 $r(A^{\mathsf T})=r(A)$。
3. 由 L.9.5，$r(A)=r(A^{\mathsf T}A)$。于是 $r(A^{\mathsf T}A)\le r(\text{增广})\le r(A^{\mathsf T}A)$，三个数只能相等。

#### 解不唯一时，投影仍唯一

设 $\hat{\boldsymbol x}_1$、$\hat{\boldsymbol x}_2$ 都满足正规方程，它们的残差都与各列垂直，由第 1 节，$A\hat{\boldsymbol x}_1$ 和 $A\hat{\boldsymbol x}_2$ 都是那个唯一的最近点 $\boldsymbol p$：

$$A\hat{\boldsymbol x}_1=\boldsymbol p,\qquad A\hat{\boldsymbol x}_2=\boldsymbol p .$$

两式相减得 $A(\hat{\boldsymbol x}_1-\hat{\boldsymbol x}_2)=\boldsymbol 0$，所以两个解之差落在零空间 $N(A)$ 里：沿被 $A$ 压到原点的方向挪动 $\hat{\boldsymbol x}$，$A\hat{\boldsymbol x}$ 不变。

现在补上第 1 节留下的反方向：正规方程总有解，所以残差垂直的 $\boldsymbol p$ 总存在，它是唯一的最近点（第 1 节：等号仅在 $\boldsymbol q=\boldsymbol p$ 时成立），任何最近点都只能是它。于是「最近」与「残差垂直」等价。

合上书，写出正规方程，说明 $P^2=P$ 的理由，再默写正规方程必有解的三步。

### 3. 什么样的基能让投影一步算完？

正规方程要解一个 $k$ 元方程组。如果 $A^{\mathsf T}A$ 是对角矩阵，它就拆成 $k$ 个一元方程，各算各的。$A^{\mathsf T}A$ 的非对角元是 $\boldsymbol a_i\cdot\boldsymbol a_j$，所以要的是各列两两正交；各列长度还都是 1 时，$A^{\mathsf T}A=E$，直接得 $\hat{\boldsymbol x}=A^{\mathsf T}\boldsymbol b$。

两两正交的一组非零向量叫**正交向量组**；每个长度又都是 1，叫**规范正交组**（也叫标准正交组），记作 $\boldsymbol q_1,\dots,\boldsymbol q_k$，条件是

$$\boldsymbol q_i\cdot\boldsymbol q_j=\begin{cases}1,&i=j,\\0,&i\ne j.\end{cases}$$

例如 $\mathbb R^4$ 中的

$$\boldsymbol q_1=\tfrac12(1,1,1,1)^{\mathsf T},\quad \boldsymbol q_2=\tfrac12(1,1,-1,-1)^{\mathsf T},\quad \boldsymbol q_3=\tfrac12(1,-1,1,-1)^{\mathsf T},\quad \boldsymbol q_4=\tfrac12(1,-1,-1,1)^{\mathsf T}.$$

每个长度都是 $\frac12\sqrt4=1$；任两个的点积是四个 $\pm\frac14$ 相加，正负各半，等于 0。

**两两正交的非零向量一定线性无关。**思路是用点积把一个系数单独挑出来。设

$$c_1\boldsymbol a_1+\cdots+c_k\boldsymbol a_k=\boldsymbol 0 .$$

两边与 $\boldsymbol a_i$ 作点积。左边除了 $c_i(\boldsymbol a_i\cdot\boldsymbol a_i)$ 以外，各项都因正交而等于 0，右边是 0，所以 $c_i\lVert\boldsymbol a_i\rVert^2=0$。$\boldsymbol a_i\ne\boldsymbol 0$，只能 $c_i=0$。$i$ 是任取的，所以全部系数为 0，无关得证。由此，$\mathbb R^n$ 中 $n$ 个规范正交的向量是 $n$ 个无关的向量，构成一组基（L.8.2），叫**规范正交基**。

这里有一对容易混的概念。先想一想：$(1,0)^{\mathsf T}$ 和 $(1,1)^{\mathsf T}$ 线性无关吗？正交吗？线性无关只要求谁也不能由别人拼出来，两个向量不共线就够了；正交要求点积为 0，而它们的点积是 1。所以正交推出无关，无关推不出正交。

规范正交基下求坐标不用解方程。设 $\boldsymbol b=x_1\boldsymbol q_1+\cdots+x_n\boldsymbol q_n$，两边与 $\boldsymbol q_j$ 作点积，右边只剩 $x_j$，所以

$$\boldsymbol b=(\boldsymbol q_1\cdot\boldsymbol b)\,\boldsymbol q_1+\cdots+(\boldsymbol q_n\cdot\boldsymbol b)\,\boldsymbol q_n .$$

投影也一样。把规范正交的 $\boldsymbol q_1,\dots,\boldsymbol q_k$ 排成 $n\times k$ 矩阵 $Q$，$Q^{\mathsf T}Q$ 的第 $(i,j)$ 元是 $\boldsymbol q_i\cdot\boldsymbol q_j$，所以 $Q^{\mathsf T}Q=E$，正规方程给出 $\hat{\boldsymbol x}=Q^{\mathsf T}\boldsymbol b$，即

$$\boldsymbol p=(\boldsymbol q_1\cdot\boldsymbol b)\,\boldsymbol q_1+\cdots+(\boldsymbol q_k\cdot\boldsymbol b)\,\boldsymbol q_k,\qquad P=QQ^{\mathsf T}.$$

投影就是在各个方向上的投影之和。规范正交基像几把互相垂直的尺子，各量各的。

**方法 3（正交基下逐个方向投影）**

1. 先验证生成向量都非零、两两点积为 0。
2. 投影是 $\boldsymbol p=\sum_i\dfrac{\boldsymbol a_i\cdot\boldsymbol b}{\boldsymbol a_i\cdot\boldsymbol a_i}\,\boldsymbol a_i$，每一项是 L.2.3 的投影；规范正交时系数就是 $\boldsymbol q_i\cdot\boldsymbol b$。
3. 生成向量张成全空间时，这些系数就是坐标。

**例 3**　用上面的 $\boldsymbol q_1,\dots,\boldsymbol q_4$：求 $\boldsymbol b=(5,3,1,-1)^{\mathsf T}$ 在这组基下的坐标。

逐个作点积：

$$\boldsymbol q_1\cdot\boldsymbol b=\tfrac12(5+3+1-1)=4,\quad \boldsymbol q_2\cdot\boldsymbol b=\tfrac12(5+3-1+1)=4,\quad \boldsymbol q_3\cdot\boldsymbol b=\tfrac12(5-3+1+1)=2,\quad \boldsymbol q_4\cdot\boldsymbol b=\tfrac12(5-3-1-1)=0,$$

所以 $\boldsymbol b=4\boldsymbol q_1+4\boldsymbol q_2+2\boldsymbol q_3$。

> 求 $(1,2,3,4)^{\mathsf T}$ 在同一组基下的坐标。
>
> 答案：四个点积依次是 $5$、$\frac12(1+2-3-4)=-2$、$\frac12(1-2+3-4)=-1$、$0$，所以它等于 $5\boldsymbol q_1-2\boldsymbol q_2-\boldsymbol q_3$。

合上书，说明规范正交基下坐标为什么就是点积，再举一个无关但不正交的例子。

### 4. 各列是两两垂直的单位向量的方阵，有什么特别？

把 $\mathbb R^n$ 的一组规范正交基排成方阵 $Q=(\boldsymbol q_1,\dots,\boldsymbol q_n)$，由上一节 $Q^{\mathsf T}Q=E$。满足这个等式的方阵叫**正交矩阵**。它代表什么样的变换？先拿老朋友试。

老朋友③（转 $90^\circ$）$\begin{pmatrix}0&-1\\1&0\end{pmatrix}$ 的两列 $(0,1)^{\mathsf T}$、$(-1,0)^{\mathsf T}$ 长度都是 1，点积是 0，所以它是正交矩阵。老朋友②（剪切）$\begin{pmatrix}1&1\\0&1\end{pmatrix}$ 的两列 $(1,0)^{\mathsf T}$、$(1,1)^{\mathsf T}$ 点积是 1，不是。

![实线是单位正方形，虚线是它的像。左：老朋友③转出的仍是同样大小的正方形；右：老朋友②推出的平行四边形，一边长 $\sqrt2$，直角变成 $45^\circ$](fig/L10-n4.pdf){width=72%}

下面的性质都只从 $Q^{\mathsf T}Q=E$ 推出。

**逆就是转置。**$Q$ 是方阵，由 L.5.2，$Q^{\mathsf T}Q=E$ 推出 $QQ^{\mathsf T}=E$，所以 $Q^{-1}=Q^{\mathsf T}$，求逆不用消元。$QQ^{\mathsf T}=E$ 还说明各行也是规范正交的。

**保持点积，从而保持长度和夹角。**由 $(AB)^{\mathsf T}=B^{\mathsf T}A^{\mathsf T}$，

$$(Q\boldsymbol x)\cdot(Q\boldsymbol y)=(Q\boldsymbol x)^{\mathsf T}(Q\boldsymbol y)=\boldsymbol x^{\mathsf T}Q^{\mathsf T}Q\boldsymbol y=\boldsymbol x^{\mathsf T}\boldsymbol y=\boldsymbol x\cdot\boldsymbol y .$$

取 $\boldsymbol y=\boldsymbol x$ 得 $\lVert Q\boldsymbol x\rVert=\lVert\boldsymbol x\rVert$。非零向量的夹角由点积和长度定义（L.2.2），所以也不变。正交矩阵代表的变换只转动或翻面，不拉伸，也不压扁。

**行列式是 $\pm1$。**由乘积公式（L.6.4），$|Q^{\mathsf T}Q|=|Q^{\mathsf T}|\,|Q|=|Q|^2$（转置不改变行列式），而 $|E|=1$，所以 $|Q|^2=1$，$|Q|=\pm1$：$+1$ 是纯转动，$-1$ 带一次翻面。

**反过来不成立。**老朋友②的行列式是 1，却不是正交矩阵。

**乘积和逆仍是正交矩阵。**由转置倒序和结合律，$(Q_1Q_2)^{\mathsf T}(Q_1Q_2)=Q_2^{\mathsf T}(Q_1^{\mathsf T}Q_1)Q_2=Q_2^{\mathsf T}Q_2=E$：乘积仍保长度，可能是转动也可能含翻面。$Q^{-1}=Q^{\mathsf T}$ 的各列是 $Q$ 的各行，也规范正交。

**方法 4（判断与使用正交矩阵）**

1. 判断：验证各列（或各行）长度为 1、两两点积为 0。只算行列式不够。
2. 求逆：$Q^{-1}=Q^{\mathsf T}$。
3. 使用：$\lVert Q\boldsymbol x\rVert=\lVert\boldsymbol x\rVert$，$|Q|=\pm1$；求含正交矩阵的行列式时，常把 $E$ 换成 $Q^{\mathsf T}Q$，再用乘积公式。

**例 4**　确定 $a,b,c$，使 $Q=\begin{pmatrix}a&\frac23&\frac23\\ \frac23&b&-\frac23\\ \frac23&-\frac23&c\end{pmatrix}$ 为正交矩阵，并求 $Q^{-1}$ 和 $|Q|$。

第一步，长度为 1 只给出 $a,b,c=\pm\frac13$，定不了符号，所以要用两两正交。第一、二列的点积为 0：

$$\tfrac23a+\tfrac23b-\tfrac49=0,\quad\text{即}\quad a+b=\tfrac23 .$$

同样，第一、三列给出 $a+c=\frac23$，第二、三列给出 $b+c=\frac23$。三式相加得 $2(a+b+c)=2$，即 $a+b+c=1$，再分别减去三式，得 $a=b=c=\frac13$。

第二步，求逆和行列式。$Q=\frac13\begin{pmatrix}1&2&2\\2&1&-2\\2&-2&1\end{pmatrix}$ 是对称的，所以 $Q^{-1}=Q^{\mathsf T}=Q$。按第一行展开（三个余子式依次是 $-3$、$6$、$-6$，中间一项带负号），

$$\begin{vmatrix}1&2&2\\2&1&-2\\2&-2&1\end{vmatrix}=1\cdot(-3)-2\cdot6+2\cdot(-6)=-27,$$

提出三行各自的 $\frac13$，$|Q|=\frac1{27}\cdot(-27)=-1$，这个变换含有一次翻面。

> 求所有使 $\begin{pmatrix}\frac35&x\\ \frac45&y\end{pmatrix}$ 为正交矩阵的 $x,y$，以及对应的行列式。
>
> 答案：两列正交要求 $\frac35x+\frac45y=0$，第二列长度为 1 要求 $x^2+y^2=1$，得 $(x,y)=(-\frac45,\frac35)$ 或 $(\frac45,-\frac35)$，行列式分别是 $1$（旋转）和 $-1$（反射）。

**例 5**　设 $A$ 是正交矩阵，$|A|=-1$，证明 $|E+A|=0$。

例 4 用的是「各列规范正交」这一条。这里没有数字，已知只有 $A^{\mathsf T}A=E$ 和 $|A|=-1$。后者只能通过乘积公式 $|XA|=|X|\,|A|$ 用上，所以要把 $E+A$ 写成「某个矩阵乘 $A$」，这就是把 $E$ 换成 $A^{\mathsf T}A$ 的理由：

$$|E+A|=|A^{\mathsf T}A+A|=|(A^{\mathsf T}+E)A|=|A^{\mathsf T}+E|\cdot|A|=-|A^{\mathsf T}+E| .$$

又 $A^{\mathsf T}+E=(A+E)^{\mathsf T}$，转置不改变行列式，所以 $|A^{\mathsf T}+E|=|E+A|$。于是 $|E+A|=-|E+A|$，只能是 0。

合上书，从 $Q^{\mathsf T}Q=E$ 推出正交矩阵的性质，说出例 5 为什么把 $E$ 换成 $A^{\mathsf T}A$。

### 5. 怎样把任意一组基改造成规范正交基？

第 3、4 节的好处都要先有规范正交基，手里却常只有普通的基。想法是一个一个地处理：每来一个新向量，就减去它在已处理好的各方向上的投影，只留下垂直的部分。

先看两个向量 $\boldsymbol a_1=(1,1,0)^{\mathsf T}$、$\boldsymbol a_2=(1,0,1)^{\mathsf T}$。第一个不用动，取 $\boldsymbol b_1=\boldsymbol a_1$。$\boldsymbol a_2$ 在 $\boldsymbol b_1$ 上的投影是 $\frac{\boldsymbol a_2\cdot\boldsymbol b_1}{\boldsymbol b_1\cdot\boldsymbol b_1}\boldsymbol b_1=\frac12\boldsymbol b_1$，减掉它，剩下

$$\boldsymbol b_2=\boldsymbol a_2-\tfrac12\boldsymbol b_1=\big(\tfrac12,-\tfrac12,1\big)^{\mathsf T},$$

验算 $\boldsymbol b_1\cdot\boldsymbol b_2=\frac12-\frac12+0=0$。$\boldsymbol b_2$ 是 $\boldsymbol a_1,\boldsymbol a_2$ 的组合，$\boldsymbol a_2$ 又能由 $\boldsymbol b_1,\boldsymbol b_2$ 拼回来，所以两组向量张成同一张平面。

![$\boldsymbol a_2$ 减去它在 $\boldsymbol b_1$ 上的投影（粗点线），剩下的部分（虚线）平移到原点就是 $\boldsymbol b_2$，它与 $\boldsymbol b_1$ 垂直](fig/L10-n5.pdf){width=55%}

一般地，设 $\boldsymbol a_1,\dots,\boldsymbol a_k$ 线性无关，**施密特正交化**依次取

$$\boldsymbol b_1=\boldsymbol a_1,\qquad \boldsymbol b_j=\boldsymbol a_j-\frac{\boldsymbol a_j\cdot\boldsymbol b_1}{\boldsymbol b_1\cdot\boldsymbol b_1}\boldsymbol b_1-\cdots-\frac{\boldsymbol a_j\cdot\boldsymbol b_{j-1}}{\boldsymbol b_{j-1}\cdot\boldsymbol b_{j-1}}\boldsymbol b_{j-1}\quad(j=2,\dots,k),$$

最后单位化：$\boldsymbol q_j=\boldsymbol b_j/\lVert\boldsymbol b_j\rVert$。下面说清三件事。

**为什么 $\boldsymbol b_j$ 与前面每个 $\boldsymbol b_i$ 都正交？**$\boldsymbol b_1,\dots,\boldsymbol b_{j-1}$ 已经两两正交，由方法 3，$\boldsymbol a_j$ 在它们张成的子空间上的投影就是各方向投影之和。公式减掉的正是这个投影，剩下的是残差，由第 1 节它与这个子空间垂直。这一步依赖前面的 $\boldsymbol b_i$ 已经正交；减去在原来的 $\boldsymbol a_i$ 上的投影，就犯了例 1 后面那个错误。

**为什么张成不变？**对 $j$ 归纳。设前 $j-1$ 个已经张成相同。由公式，$\boldsymbol b_j$ 是 $\boldsymbol a_j$ 减去前面 $\boldsymbol b_i$ 的组合，这些 $\boldsymbol b_i$ 都在 $\operatorname{span}(\boldsymbol a_1,\dots,\boldsymbol a_{j-1})$ 里；反过来，$\boldsymbol a_j$ 等于 $\boldsymbol b_j$ 加上前面 $\boldsymbol b_i$ 的组合。两边互含，所以 $\operatorname{span}(\boldsymbol b_1,\dots,\boldsymbol b_j)=\operatorname{span}(\boldsymbol a_1,\dots,\boldsymbol a_j)$。

**为什么 $\boldsymbol b_j\ne\boldsymbol 0$？**若 $\boldsymbol b_j=\boldsymbol 0$，$\boldsymbol a_j$ 就等于前面 $\boldsymbol b_i$ 的组合，落在 $\operatorname{span}(\boldsymbol a_1,\dots,\boldsymbol a_{j-1})$ 里，与线性无关矛盾。

**方法 5（施密特正交化）**

1. $\boldsymbol b_1=\boldsymbol a_1$。
2. 对 $j=2,3,\dots$，从 $\boldsymbol a_j$ 里逐个减去它在已得的 $\boldsymbol b_1,\dots,\boldsymbol b_{j-1}$ 上的投影。
3. 每得到一个 $\boldsymbol b_j$，验算它与前面各个的点积为 0。中间的 $\boldsymbol b_j$ 可以乘一个正数去分母，因为投影与方向向量的长短无关。
4. 最后把每个 $\boldsymbol b_j$ 除以自己的长度。

**例 6**　把 $\boldsymbol a_1=(1,1,0)^{\mathsf T}$、$\boldsymbol a_2=(1,0,1)^{\mathsf T}$、$\boldsymbol a_3=(0,1,1)^{\mathsf T}$ 化为规范正交基。

前两步上面已经做了：$\boldsymbol b_1=(1,1,0)^{\mathsf T}$，$\boldsymbol b_2=(\frac12,-\frac12,1)^{\mathsf T}$，去分母取 $\boldsymbol b_2=(1,-1,2)^{\mathsf T}$。

第三步要减去两个投影，先算点积：$\boldsymbol a_3\cdot\boldsymbol b_1=1$，$\boldsymbol b_1\cdot\boldsymbol b_1=2$，$\boldsymbol a_3\cdot\boldsymbol b_2=0-1+2=1$，$\boldsymbol b_2\cdot\boldsymbol b_2=6$。所以

$$\boldsymbol b_3=\begin{pmatrix}0\\1\\1\end{pmatrix}-\frac12\begin{pmatrix}1\\1\\0\end{pmatrix}-\frac16\begin{pmatrix}1\\-1\\2\end{pmatrix}=\begin{pmatrix}-\frac23\\ \frac23\\ \frac23\end{pmatrix},$$

去分母取 $(-1,1,1)^{\mathsf T}$。验算 $\boldsymbol b_1\cdot\boldsymbol b_3=-1+1+0=0$，$\boldsymbol b_2\cdot\boldsymbol b_3=-1-1+2=0$。

最后单位化：

$$\boldsymbol q_1=\tfrac{1}{\sqrt2}(1,1,0)^{\mathsf T},\qquad \boldsymbol q_2=\tfrac{1}{\sqrt6}(1,-1,2)^{\mathsf T},\qquad \boldsymbol q_3=\tfrac{1}{\sqrt3}(-1,1,1)^{\mathsf T}.$$

> 把 $(1,1,1,1)^{\mathsf T}$、$(1,2,3,4)^{\mathsf T}$ 正交化（不必单位化）。
>
> 答案：$\boldsymbol b_2=(1,2,3,4)^{\mathsf T}-\frac{10}{4}(1,1,1,1)^{\mathsf T}=(-\frac32,-\frac12,\frac12,\frac32)^{\mathsf T}$，去分母为 $(-3,-1,1,3)^{\mathsf T}$。减去的 $\frac{10}{4}$ 正是四个分量的平均数，和 L.2 例 7 一样；第 6 节会用到这一点。

#### 写成矩阵：A = QR

施密特正交化可以写成一个矩阵分解。看例 6 的前两个向量：由 $\boldsymbol b_1=\boldsymbol a_1$、$\boldsymbol b_2=\boldsymbol a_2-\frac12\boldsymbol b_1$ 反解出 $\boldsymbol a_1,\boldsymbol a_2$，再把 $\boldsymbol b_1=\sqrt2\,\boldsymbol q_1$、$\boldsymbol b_2=\frac{\sqrt6}{2}\boldsymbol q_2$ 代进去：

$$\boldsymbol a_1=\sqrt2\,\boldsymbol q_1,\qquad \boldsymbol a_2=\tfrac{\sqrt2}{2}\,\boldsymbol q_1+\tfrac{\sqrt6}{2}\,\boldsymbol q_2 .$$

系数按列排起来，第 $j$ 列放 $\boldsymbol a_j$ 的系数（L.3.1，矩阵乘向量是各列的组合）：

$$(\boldsymbol a_1,\boldsymbol a_2)=(\boldsymbol q_1,\boldsymbol q_2)\begin{pmatrix}\sqrt2&\frac{\sqrt2}{2}\\0&\frac{\sqrt6}{2}\end{pmatrix},\qquad\text{即}\quad A=QR .$$

一般情形分三点。

第一，$R$ 是上三角矩阵。由「张成不变」，$\boldsymbol a_j$ 在 $\operatorname{span}(\boldsymbol q_1,\dots,\boldsymbol q_j)$ 里，只用到前 $j$ 个 $\boldsymbol q$，所以 $R$ 的第 $j$ 列在第 $j$ 行以下都是 0。

第二，$R=Q^{\mathsf T}A$。这里 $Q$ 是 $n\times k$ 矩阵，$k<n$ 时不是方阵，也就不是第 4 节的正交矩阵；但它的列规范正交，由第 3 节仍有 $Q^{\mathsf T}Q=E$，只是 $QQ^{\mathsf T}\ne E$。在 $A=QR$ 两边左乘 $Q^{\mathsf T}$，就得 $R=Q^{\mathsf T}A$。

第三，$R$ 可逆。$\boldsymbol a_j$ 等于 $\boldsymbol b_j$ 加上前面各 $\boldsymbol q_i$ 的组合，后者与 $\boldsymbol q_j$ 正交，所以对角元 $\boldsymbol q_j\cdot\boldsymbol a_j=\boldsymbol q_j\cdot\boldsymbol b_j$；又 $\boldsymbol q_j=\boldsymbol b_j/\lVert\boldsymbol b_j\rVert$，它等于 $\lVert\boldsymbol b_j\rVert>0$。三角矩阵的行列式是对角元之积，不为 0。

用在最小二乘上：$A^{\mathsf T}A=R^{\mathsf T}(Q^{\mathsf T}Q)R=R^{\mathsf T}R$，$A^{\mathsf T}\boldsymbol b=R^{\mathsf T}Q^{\mathsf T}\boldsymbol b$，正规方程两边左乘 $(R^{\mathsf T})^{-1}$，只剩上三角方程组 $R\hat{\boldsymbol x}=Q^{\mathsf T}\boldsymbol b$，往回代就行。

合上书，写出三个向量的施密特正交化公式，说明 $\boldsymbol b_3$ 为什么与前两个都正交、为什么不是零向量。

### 6. 怎样用一堆数据拟合一条直线或一个线性模型？

用直线 $y=C+Dt$ 拟合 $m$ 个数据点 $(t_i,y_i)$，就是要求 $m$ 个方程 $C+Dt_i=y_i$ 同时成立，写成 $A\boldsymbol x=\boldsymbol b$：

$$A=\begin{pmatrix}1&t_1\\ \vdots&\vdots\\1&t_m\end{pmatrix},\qquad \boldsymbol x=\begin{pmatrix}C\\D\end{pmatrix},\qquad \boldsymbol b=\begin{pmatrix}y_1\\ \vdots\\y_m\end{pmatrix}.$$

$A$ 叫**设计矩阵**，每个数据点占一行，每个待定参数占一列。

取最小二乘解，就是让 $\lVert\boldsymbol b-A\boldsymbol x\rVert^2=\sum_i e_i^2$ 最小，其中残差 $e_i=y_i-(C+Dt_i)$。只要 $t_i$ 里至少有两个不同的值，两列就线性无关，$C,D$ 唯一。注意 $e_i$ 是数据点与直线在竖直方向上的差，不是点到直线的垂直距离，因为我们用 $t$ 预测 $y$，误差按 $y$ 来量。

![左：拟合直线 $y=-0.5+1.6t$，空心方块是平均点，在直线上；右：残差放大画出，虚线段是竖直方向的差，正负抵消、和为 0](fig/L10-n2.pdf){width=62%}

斜率公式可以用第 5 节的正交化推出：先把两列改造成互相垂直的，再用方法 3 各算各的。

第一步，正交化。记 $\bar t$、$\bar y$ 为平均数，$\boldsymbol 1$ 为全 1 列。按第 5 节，第二列 $\boldsymbol t$ 减去它在 $\boldsymbol 1$ 上的投影 $\bar t\,\boldsymbol 1$（第 5 节小题里，投影系数是平均数），得到分量为 $t_i-\bar t$ 的向量，它与 $\boldsymbol 1$ 正交，因为 $\sum(t_i-\bar t)=0$。

第二步，换写法。把直线改写成

$$C+Dt=(C+D\bar t)+D(t-\bar t),$$

同一条直线换了写法，新设计矩阵的两列张成的列空间不变，所以投影和最小平方和不变。

第三步，各算各的。由方法 3，$\boldsymbol 1$ 方向的系数是 $C+D\bar t=\frac{\boldsymbol 1\cdot\boldsymbol b}{\boldsymbol 1\cdot\boldsymbol 1}=\bar y$；另一个方向的系数是

$$D=\frac{\sum(t_i-\bar t)\,y_i}{\sum(t_i-\bar t)^2}=\frac{\sum(t_i-\bar t)(y_i-\bar y)}{\sum(t_i-\bar t)^2},$$

第二个等号用了 $\sum(t_i-\bar t)\,\bar y=\bar y\sum(t_i-\bar t)=0$。于是 $C=\bar y-D\bar t$，拟合直线经过平均点 $(\bar t,\bar y)$。

**方法 6（最小二乘拟合）**

1. 写出设计矩阵：每个数据点一行，每个参数一列。
2. 解正规方程。拟合直线时可以直接用斜率公式：先求 $\bar t$、$\bar y$，再算 $D$，最后 $C=\bar y-D\bar t$。
3. 验算：残差之和为 0，$\sum t_ie_i=0$，也就是残差与两列都正交。

**例 7**　设计矩阵的两列是 $\boldsymbol 1$ 和 $\boldsymbol t=(1,2,3,4)^{\mathsf T}$，$\boldsymbol b=(1,3,4,6)^{\mathsf T}$，求最小二乘解 $(C,D)$ 和残差。

第一步，平均数：$\bar t=2.5$，$\bar y=3.5$。

第二步，离差：$t_i-\bar t$ 依次是 $-1.5,-0.5,0.5,1.5$，$y_i-\bar y$ 依次是 $-2.5,-0.5,0.5,2.5$。

第三步，代入斜率公式：

$$D=\frac{3.75+0.25+0.25+3.75}{2.25+0.25+0.25+2.25}=\frac85=1.6,\qquad C=3.5-1.6\times2.5=-0.5 .$$

直线是 $y=-0.5+1.6t$。四个预测值是 $1.1,2.7,4.3,5.9$，残差是 $-0.1,0.3,-0.3,0.1$。验算：和为 0，$\sum t_ie_i=-0.1+0.6-0.9+0.4=0$。

> 用斜率公式求拟合 $(0,1)$、$(1,1)$、$(2,4)$ 的直线。
>
> 答案：$\bar t=1$，$\bar y=2$，$D=\frac{(-1)(-1)+0\cdot(-1)+1\cdot2}{1+0+1}=1.5$，$C=2-1.5=0.5$，直线是 $y=0.5+1.5t$，残差 $0.5,-1,0.5$，和为 0。

参数多于两个时多几列即可，例如拟合 $y=C+Dt+Et^2$，每行是 $(1,t_i,t_i^2)$。

参数成千上万时，机器学习不解正规方程，而用 C.22.5 的梯度下降，每次沿负梯度走一小步：

$$\boldsymbol x\leftarrow\boldsymbol x-\eta\,\nabla f(\boldsymbol x),$$

$\nabla f$ 是各偏导数排成的向量，步长 $\eta$ 叫学习率。

对 $f(C,D)=\sum_i e_i^2$（$e_i=y_i-C-Dt_i$）逐项求偏导，$e_i$ 对 $C$、$D$ 的偏导是 $-1$、$-t_i$，由链式法则：

$$\frac{\partial f}{\partial C}=-2\sum_i e_i,\qquad \frac{\partial f}{\partial D}=-2\sum_i t_ie_i .$$

这两个和是 $\boldsymbol e$ 与两列的点积，即 $A^{\mathsf T}\boldsymbol e$ 的两个分量，所以 $\nabla f=-2A^{\mathsf T}\boldsymbol e$。梯度为零就是 $A^{\mathsf T}\boldsymbol e=\boldsymbol 0$，恰好是正规方程；每一步只算残差和 $A^{\mathsf T}$ 乘向量，不用求逆。

**例 8**　用梯度下降拟合 $(0,1)$、$(1,1)$、$(2,4)$：从 $C=D=0$ 出发，学习率 $\eta=0.1$，手算两步，并与上面小题的解 $(0.5,1.5)$ 比较。

更新公式是 $\boldsymbol x\leftarrow\boldsymbol x+2\eta A^{\mathsf T}\boldsymbol e=\boldsymbol x+0.2\,A^{\mathsf T}\boldsymbol e$。

第一步，$\boldsymbol x_0=\boldsymbol 0$ 时残差 $\boldsymbol e=\boldsymbol b=(1,1,4)^{\mathsf T}$，$A^{\mathsf T}\boldsymbol e=(6,9)^{\mathsf T}$，所以

$$\boldsymbol x_1=0.2\,(6,9)^{\mathsf T}=(1.2,\ 1.8)^{\mathsf T}.$$

第二步，$A\boldsymbol x_1=(1.2,3.0,4.8)^{\mathsf T}$，残差 $\boldsymbol e=(-0.2,-2.0,-0.8)^{\mathsf T}$，$A^{\mathsf T}\boldsymbol e=(-3.0,-3.6)^{\mathsf T}$，所以

$$\boldsymbol x_2=(1.2,\ 1.8)^{\mathsf T}+0.2\,(-3.0,-3.6)^{\mathsf T}=(0.6,\ 1.08)^{\mathsf T}.$$

平方和 $f$ 从 18 降到 4.68、2.16；第 30 步约是 $(0.502,1.499)$，$f$ 接近最小值 $1.5$。迭代收敛到的点梯度为零，满足正规方程，由第 2 节它就是最小二乘解。学习率取大了可能越走越远：这组数据取 $\eta=0.2$，$f$ 第一步就从 18 涨到 58.32。

合上书，推出斜率公式，再说明梯度下降停住的点为什么就是最小二乘解。

### 本章小结

| 方法 | 什么时候用 | 对应题号 |
|---|---|---|
| 方法 1（残差与每个生成向量正交） | 求到子空间的投影和距离 | L10-01、L10-15 |
| 方法 2（正规方程） | 最小二乘解、投影矩阵 | L10-05、L10-06、L10-11、L10-14、L10-17 |
| 方法 3（正交基下逐个方向投影） | 正交基下求投影、坐标 | L10-02、L10-12 |
| 方法 4（判断与使用正交矩阵） | 判断正交、求逆、行列式 | L10-03、L10-07、L10-10、L10-16、L10-17 |
| 方法 5（施密特正交化） | 造规范正交基；QR | L10-08、L10-12 |
| 方法 6（最小二乘拟合） | 拟合直线或线性模型、梯度下降 | L10-04、L10-09、L10-13 |
