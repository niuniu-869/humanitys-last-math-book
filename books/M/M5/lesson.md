## M.5 · PCA 的完整推导：拉格朗日乘子与特征值

经济管理里常要把几十个指标合成一个「综合指数」：给一座城市的营商环境打分，要把用电量、人口、税收、道路里程等许多个数合成一两个数。AI 里常把上千维的词向量画到平面上，看哪些词聚成一堆。这两件事用的是同一个工具，叫主成分分析（PCA）：在许多维的数据里，找出数据变化最大的几个方向，只保留它们。

开头那个综合指数带着一个具体的问题：几个指标合成一个数，每个指标占多大的权重才合理？本章最后一节把它算出来。

这个想法有两个问题作源头。一个是几何问题：给定平面上的一堆点，用哪条直线代表它们，使点到直线的距离平方之和最小？Pearson 在 1901 年研究过「离一堆点最近的直线和平面」。另一个是统计问题：许多个相互关联的指标，能不能归结成少数几个综合指标，同时让综合指标保留尽量多的变化？Hotelling 在 1933 年从「方差最大」的角度处理它，并取名「主成分」。两个问题的答案是同一个，本章的第 3 节和第 6 节分别给出推导，并说明为什么相同。

M.4.7 的 k-means 是不要标签的「分组」，M.4.2 的维数灾难说明维数太高时很多方法失灵；PCA 是不要标签的「降维」。L.15 把 PCA 作为 SVD 的一个用途点过一下，本章给完整的推导，所用的工具是 C.24 的拉格朗日乘子、L.13 的谱定理、L.14.8 的向量求导和 P.7 的协方差矩阵。

三件套里的位置：数据没有标签，没有预测目标。「模型」是把 $d$ 维数据投影到 $k$ 个相互垂直的方向上；「损失」是投影之后重建回原来的 $d$ 维所产生的误差（第 6 节）；「更新」不用迭代，答案是一次特征分解就得出来的闭式解。本章用到的几个量，先列一张形状账本（$n$ 个样本，每个样本 $d$ 个指标）：

| 对象 | 记号 | 形状 |
|---|---|---|
| 数据矩阵，每行一个样本 | $X$，中心化后记 $X_c$ | $n\times d$ |
| 一个方向 | $\boldsymbol w$ | $d$ 维列向量 |
| 指标两两之间的协方差 | $S$ | $d\times d$ |
| 样本在方向 $\boldsymbol w$ 上的坐标（得分） | $X_c\boldsymbol w$ | $n$ 维向量 |
| 留 $k$ 个方向时的得分 | $X_cW$，$W$ 的列是 $k$ 个方向 | $n\times k$ |

记号：$\boldsymbol x_{c,i}$ 是中心化后第 $i$ 个样本，当作列向量；$^{\mathsf T}$ 是转置，$I$ 是单位矩阵，$\mathrm{diag}$ 是以给定的数为对角线的对角矩阵。

本章的顺序：第 1、2 节准备零件（中心化、协方差矩阵、投影方差）；第 3 节用拉格朗日乘子推出主成分是特征向量；第 4 节找第二、第三个主成分；第 5 节算保留了多少信息；第 6 节换个问法，证明「最大方差」和「最小重建误差」是同一个问题；第 7 节处理单位不同的指标；第 8 节说明实际计算为什么用 SVD；第 9 节把一道 PCA 题从头到尾算一遍。老朋友①（五个点）在这里换了一个用法：把 $(x,y)=(1,2),(2,3),(3,5),(4,6),(5,9)$ 看成平面上的五个点，没有「自变量」和「标签」之分。

### 1. 几十个指标，能不能压成两三个综合指标？

先看最小的情形：两个指标。五个点 $(1,2),(2,3),(3,5),(4,6),(5,9)$ 大致排在一条斜线上，两个指标变化的方向大致一致，也许用一个综合指标就能概括。要说清「大致在一条线上」，需要一个衡量两个指标一起变化的量。

PCA 看的是数据**围绕平均值**的分散情况，所以第一步是中心化：每个指标减去自己的平均值。设 $n\ge2$ 个样本、$d\ge1$ 个指标，数据矩阵 $X\in\mathbb R^{n\times d}$ 的第 $i$ 行是样本 $\boldsymbol x_i^{\mathsf T}$，平均值 $\bar{\boldsymbol x}=\frac1n\sum_i\boldsymbol x_i$。中心化后的第 $i$ 行是 $\boldsymbol x_i^{\mathsf T}-\bar{\boldsymbol x}^{\mathsf T}$，所有行合成 $X_c\in\mathbb R^{n\times d}$。老朋友①的平均值是 $(3,5)$，中心化后

$$X_c=\begin{pmatrix}-2&-3\\-1&-2\\0&0\\1&1\\2&4\end{pmatrix}.$$

**样本协方差矩阵**（P.7）定义为

$$S=\frac1{n-1}X_c^{\mathsf T}X_c\in\mathbb R^{d\times d}.$$

它的第 $(j,k)$ 个元素是第 $j$ 个指标与第 $k$ 个指标的样本协方差 $\frac1{n-1}\sum_i(x_{ij}-\bar x_j)(x_{ik}-\bar x_k)$；对角线上是各指标的方差。除以 $n-1$ 而不是 $n$ 是 P.10.3 的样本方差约定（协方差的含义见 P.7）；改成除以 $n$ 只是把所有元素乘同一个数，不改变后面要找的方向。

老朋友①：$X_c^{\mathsf T}X_c=\begin{pmatrix}10&17\\17&30\end{pmatrix}$（例如 $(-2)(-3)+(-1)(-2)+0+1\cdot1+2\cdot4=17$），所以

$$S=\frac14\begin{pmatrix}10&17\\17&30\end{pmatrix}=\begin{pmatrix}2.5&4.25\\4.25&7.5\end{pmatrix}.$$

对角线 2.5 和 7.5 是两个指标各自的方差，4.25 是它们的协方差，为正，说明样本里这两个指标同增同减的趋势占多数。

$S$ 有两个后面要用的性质。**对称**：$S^{\mathsf T}=S$，因为 $(X_c^{\mathsf T}X_c)^{\mathsf T}=X_c^{\mathsf T}X_c$。**半正定**：对任意向量 $\boldsymbol w$，

$$\boldsymbol w^{\mathsf T}S\boldsymbol w=\frac1{n-1}(X_c\boldsymbol w)^{\mathsf T}(X_c\boldsymbol w)=\frac1{n-1}\lVert X_c\boldsymbol w\rVert^2\ge0 .$$

这里 $\lVert\cdot\rVert$ 是向量的长度，用双竖线是为了和绝对值 $|x|$ 区分。由 L.13 的谱定理，对称矩阵有正交的特征向量，半正定说明特征值都 $\ge0$。

**例 1**　三个指标、四个样本，原始数据按行为 $(1,2,3)$、$(3,2,1)$、$(2,4,3)$、$(2,0,1)$。求中心化数据矩阵和样本协方差矩阵 $S$。

例 1 把上面对两个指标做的两步原样做在三个指标上，只是矩阵从 $2\times2$ 变成 $3\times3$：先减平均值，再算 $\frac1{n-1}X_c^{\mathsf T}X_c$。平均值：第一列 $(1+3+2+2)/4=2$，第二列 $(2+2+4+0)/4=2$，第三列 $(3+1+3+1)/4=2$。

$$X_c=\begin{pmatrix}-1&0&1\\1&0&-1\\0&2&1\\0&-2&-1\end{pmatrix},\qquad X_c^{\mathsf T}X_c=\begin{pmatrix}2&0&-2\\0&8&4\\-2&4&4\end{pmatrix}.$$

$n-1=3$，所以 $S=\frac13X_c^{\mathsf T}X_c$，对角线是 $\frac23,\frac83,\frac43$。形状核对：$X_c$ 是 $4\times3$，$X_c^{\mathsf T}X_c$ 是 $3\times3$。

> 老朋友①中，若把两个指标都乘 2（即点变成 $(2,4),(4,6),\dots$），$S$ 变成什么？
>
> 答案：每个指标放大 2 倍，方差放大 4 倍，协方差也放大 4 倍，$S=\begin{pmatrix}10&17\\17&30\end{pmatrix}$。

有了 $S$，还没有回答本章的问题：数据往哪个方向散得最开？下一节先把「沿某个方向散得多开」算成一个数。

合上书，写出 $S$ 的定义，说明为什么它是对称的、半正定的。

### 2. 把数据投影到一个方向上，方差是多少？

压成一个综合指标，就是选一个方向，把每个点投影到这个方向上，用投影的位置当作新指标。方向由单位向量 $\boldsymbol w$（$\lVert\boldsymbol w\rVert=1$）给出。中心化后的点 $\boldsymbol x_{c,i}$ 在这个方向上的坐标是 $t_i=\boldsymbol w^{\mathsf T}\boldsymbol x_{c,i}$（L.2：它是点在方向 $\boldsymbol w$ 上的有符号投影坐标，投影线段的长度是它的绝对值）。写成一列，$\boldsymbol t=X_c\boldsymbol w\in\mathbb R^n$。

**这组新指标 $t_1,\dots,t_n$ 的方差是多少？** 因为中心化后 $\sum_i\boldsymbol x_{c,i}=\boldsymbol 0$，所以 $t_i$ 的平均值 $\boldsymbol w^{\mathsf T}\cdot\frac1n\sum_i\boldsymbol x_{c,i}=0$，所以方差就是平方和除以 $n-1$：

$$\frac1{n-1}\sum_it_i^2=\frac1{n-1}\lVert X_c\boldsymbol w\rVert^2=\frac1{n-1}\boldsymbol w^{\mathsf T}X_c^{\mathsf T}X_c\boldsymbol w=\boldsymbol w^{\mathsf T}S\boldsymbol w .$$

**投影方差 $=\boldsymbol w^{\mathsf T}S\boldsymbol w$。** 这个式子把「数据沿某个方向散得多开」写成了 $S$ 的二次型。

老朋友①，先猜：沿横轴 $(1,0)$、纵轴 $(0,1)$ 和斜线方向 $(1,1)/\sqrt2$，哪个方向的投影方差最大？算一算：

| 方向 $\boldsymbol w$ | $(1,0)$ | $(0,1)$ | $\tfrac1{\sqrt2}(1,1)$ | $(0.6,\,0.8)$ |
|---|---|---|---|---|
| $\boldsymbol w^{\mathsf T}S\boldsymbol w$ | 2.5 | 7.5 | 9.25 | 9.78 |

例如 $(0.6,0.8)$：$0.36\times2.5+2\times0.6\times0.8\times4.25+0.64\times7.5=0.9+4.08+4.8=9.78$。沿斜线的方向（9.25、9.78）比两个坐标轴方向都大。原因是两个指标同增同减（协方差 4.25 为正），斜线方向把两个指标的变化叠在了一起；协方差若为负，斜线方向反而会互相抵消。方差最大的方向在哪里？我们想在所有单位向量里找使 $\boldsymbol w^{\mathsf T}S\boldsymbol w$ 最大的那一个。

**例 2**　仍用老朋友①的 $S$。上表只试了四个方向，现在让方向 $\boldsymbol w=(\cos\theta,\sin\theta)$ 连续转一圈，把投影方差写成 $\theta$ 的函数，并求使其最大的 $\theta$。

二维时方向只有一个自由量 $\theta$，可以直接做；第 3 节的办法对任意维数都管用，这里的结果正好拿来对照。

$$f(\theta)=2.5\cos^2\theta+8.5\sin\theta\cos\theta+7.5\sin^2\theta .$$

用二倍角公式 $\cos^2\theta=\frac{1+\cos2\theta}2$，$\sin^2\theta=\frac{1-\cos2\theta}2$，$\sin\theta\cos\theta=\frac{\sin2\theta}2$：

$$f(\theta)=5-2.5\cos2\theta+4.25\sin2\theta .$$

形如 $A\cos x+B\sin x$ 的式子最大值是 $\sqrt{A^2+B^2}$，所以 $-2.5\cos2\theta+4.25\sin2\theta$ 的最大值是 $\sqrt{2.5^2+4.25^2}=\sqrt{24.3125}\approx4.931$，所以最大方差 $\approx9.931$。取最大值时 $\tan2\theta=4.25/(-2.5)$，$2\theta$ 在第二象限，$2\theta\approx120.5^\circ$，$\theta\approx60.2^\circ$（方向的角度模 $180^\circ$，一般写成 $\theta_*+m\pi$，$m$ 为整数；取 $0\le\theta<\pi$ 的代表），方向 $(\cos\theta,\sin\theta)\approx(0.4965,\,0.8680)$。

![投影方差随方向的变化：横轴是方向角 $\theta$，纵轴是 $\boldsymbol w^{\mathsf T}S\boldsymbol w$。实线在 $\theta\approx60.2^\circ$ 处取最大值 9.93，在 $\theta\approx150.2^\circ$ 处取最小值 0.07；虚线是均值 5](fig/M5-n2.pdf){width=70%}

> 同一个 $S$，$\theta=45^\circ$ 时投影方差是多少？
>
> 答案：$f=5-2.5\cos90^\circ+4.25\sin90^\circ=9.25$，与表里一致。

合上书，写出方向 $\boldsymbol w$ 上的投影方差 $\boldsymbol w^{\mathsf T}S\boldsymbol w$ 是怎么从 $t_i$ 的平方和得到的，并说明二维时它如何随 $\theta$ 变化。

维数多了，没有二倍角公式可用，需要一个对任意 $d$ 都管用的办法。

### 3. 方差最大的方向是哪一个？

例 2 里方差最大的方向是 $\boldsymbol w\approx(0.4965,0.8680)$。拿 $S$ 去乘这个方向：

$$S\boldsymbol w\approx\begin{pmatrix}4.930\\8.620\end{pmatrix}\approx9.931\begin{pmatrix}0.4965\\0.8680\end{pmatrix}.$$

乘出来的向量与 $\boldsymbol w$ 平行，比例恰好是最大方差 9.931。换成 $45^\circ$ 的方向 $(1,1)/\sqrt2$，$S\boldsymbol w=(6.75,\,11.75)/\sqrt2$，就与 $(1,1)$ 不平行了。这是巧合吗？

逐个试方向的办法，二维还行，维数一高方向多得数不清，试出来也说不出最大值点有什么特征。下面用拉格朗日乘子法证明这不是巧合：最大值点一定满足 $S\boldsymbol w$ 平行于 $\boldsymbol w$。

问题：在 $\lVert\boldsymbol w\rVert=1$ 的限制下，使 $f(\boldsymbol w)=\boldsymbol w^{\mathsf T}S\boldsymbol w$ 最大。这是带等式约束的极值，用拉格朗日乘子法（C.24.7）。

为什么必须加 $\lVert\boldsymbol w\rVert=1$？没有约束时，把 $\boldsymbol w$ 乘 10，$f$ 乘 100，只要 $S\ne0$ 就没有最大值。我们关心的是方向，所以把长度固定为 1。

**C.24.7 的结论回顾**：在 $g(\boldsymbol w)=0$ 的约束下，设 $f,g$ 有连续的一阶偏导数、$\boldsymbol w$ 是约束下的极值点且 $\nabla g(\boldsymbol w)\ne\boldsymbol 0$，则极值点处 $\nabla f=\lambda\nabla g$（梯度平行），$\lambda$ 叫拉格朗日乘子。这里 $g(\boldsymbol w)=\boldsymbol w^{\mathsf T}\boldsymbol w-1$，$\nabla g=2\boldsymbol w$，在单位球面上不为零。

**定理**　设 $S$ 是对称矩阵。$\boldsymbol w^{\mathsf T}S\boldsymbol w$ 在 $\boldsymbol w^{\mathsf T}\boldsymbol w=1$ 下的最大值点是 $S$ 的最大特征值 $\lambda_1$ 对应的单位特征向量（正负号任取；$\lambda_1$ 重复时有无穷多个，第 4 节末再说），最大值是 $\lambda_1$。

思路：先用拉格朗日条件得到「最大值点一定是特征向量」，再看这个点的函数值等于对应的特征值。

*第一步，求梯度。* 由 L.14.8，$S$ 对称时 $\nabla(\boldsymbol w^{\mathsf T}S\boldsymbol w)=2S\boldsymbol w$。（二维核对：$S=\begin{pmatrix}a&b\\b&c\end{pmatrix}$，$\boldsymbol w^{\mathsf T}S\boldsymbol w=aw_1^2+2bw_1w_2+cw_2^2$，对 $w_1$ 求偏导得 $2aw_1+2bw_2$，正是 $2S\boldsymbol w$ 的第一个分量。）

*第二步，写出拉格朗日条件。* $\nabla f=\lambda\nabla g$ 即 $2S\boldsymbol w=\lambda\cdot2\boldsymbol w$，两边除以 2：

$$S\boldsymbol w=\lambda\boldsymbol w .$$

这正是特征方程：极值点 $\boldsymbol w$ 必须是 $S$ 的单位特征向量，乘子 $\lambda$ 就是对应的特征值。

*第三步，求函数值。* 在这样的点上，$f(\boldsymbol w)=\boldsymbol w^{\mathsf T}S\boldsymbol w=\boldsymbol w^{\mathsf T}(\lambda\boldsymbol w)=\lambda\boldsymbol w^{\mathsf T}\boldsymbol w=\lambda$。

*第四步，选最大的。* 单位球面是有界闭集，$f$ 连续，所以最大值一定存在（C 册的最值定理），最大值点必须满足第二步的条件（这是必要条件，反过来不是每个满足它的点都是最大值点）。所以最大值一定在这些候选点里；候选点的函数值是各个特征值，取最大的，就是 $\lambda_1$。$\blacksquare$

可以用谱定理（L.13）再验一遍。设单位正交的特征向量为 $\boldsymbol u_1,\dots,\boldsymbol u_d$，特征值 $\lambda_1\ge\cdots\ge\lambda_d$。$\boldsymbol u_1,\dots,\boldsymbol u_d$ 是 $\mathbb R^d$ 的一组单位正交基，所以任一单位向量可以写成 $\boldsymbol w=\sum c_i\boldsymbol u_i$，$c_i=\boldsymbol u_i^{\mathsf T}\boldsymbol w$，且 $1=\lVert\boldsymbol w\rVert^2=\sum c_i^2$。把 $\boldsymbol w=\sum c_i\boldsymbol u_i$ 代入，用 $S\boldsymbol u_j=\lambda_j\boldsymbol u_j$ 和 $\boldsymbol u_i^{\mathsf T}\boldsymbol u_j=0$（$i\ne j$）让交叉项消失，得

$$\boldsymbol w^{\mathsf T}S\boldsymbol w=\sum_i\lambda_ic_i^2\le\lambda_1\sum_ic_i^2=\lambda_1,$$

等号当且仅当 $\boldsymbol w$ 落在属于 $\lambda_1$ 的方向上。两种推导结论一致。

结论里最该记住的是：**数据方差最大的方向，是协方差矩阵最大特征值的特征向量；这个方向上的方差，就是那个特征值。** 它叫第一**主成分**方向。

**方法 1（求第一主成分）**

1. 中心化，算 $S=\frac1{n-1}X_c^{\mathsf T}X_c$。
2. 解特征方程 $\lvert S-\lambda I\rvert=0$，取最大的特征值 $\lambda_1$。
3. 解 $(S-\lambda_1I)\boldsymbol w=\boldsymbol 0$，取一个非零解 $\boldsymbol v$，令 $\boldsymbol w_1=\boldsymbol v/\lVert\boldsymbol v\rVert$。
4. 方向 $\boldsymbol w_1$ 上的方差是 $\lambda_1$；每个样本的得分是 $t_i=\boldsymbol w_1^{\mathsf T}\boldsymbol x_{c,i}$。

**例 3**　求老朋友①的第一主成分。

例 3 问的就是例 2 的问题：同一个 $S$，求方差最大的方向。这次不扫角度，改用方法 1，两种做法的结果应当一致。

第一步，$S=\begin{pmatrix}2.5&4.25\\4.25&7.5\end{pmatrix}$。特征方程：

$$\lvert S-\lambda I\rvert=(2.5-\lambda)(7.5-\lambda)-4.25^2=\lambda^2-10\lambda+0.6875=0 .$$

（迹 $2.5+7.5=10$，行列式 $18.75-18.0625=0.6875$。）

第二步，$\lambda=5\pm\sqrt{25-0.6875}\approx5\pm4.9308$，$\lambda_1\approx9.9308$，$\lambda_2\approx0.0692$。

第三步，$(S-\lambda_1I)\boldsymbol w=\boldsymbol 0$ 的第一行：$(2.5-9.9308)w_1+4.25w_2=0$，所以 $w_2=1.7484\,w_1$，取 $(1,1.7484)$，长度 $\sqrt{1+3.057}=2.014$，单位化得 $\boldsymbol w_1\approx(0.4965,\,0.8680)$。

与例 2 一致：方向角 $60.2^\circ$，方差 $9.93$。每个点的得分是 $t_i=0.4965x_{c1}+0.8680x_{c2}$：

$$\boldsymbol t\approx(-3.597,\,-2.233,\,0,\,1.365,\,4.465).$$

这五个数的方差 $=9.93$，两个指标被压成了一个。

![老朋友①的五个点（实心圆）围绕平均值 $(3,5)$（十字）；实线是第一主成分方向；短虚线是垂直于它的第二主成分方向；灰色点线是每个点到实线的垂线，很短，因为五个点几乎都在这条线上](fig/M5-n1.pdf){width=65%}

> 求 $S=\begin{pmatrix}3&1\\1&3\end{pmatrix}$ 的第一主成分方向与方差。
>
> 答案：特征值 4 和 2，$S(1,1)^{\mathsf T}=4(1,1)^{\mathsf T}$，所以 $\boldsymbol w_1=(1,1)/\sqrt2$，方差 4。

**可默写的骨架（拉格朗日乘子法推出主成分）**

1. 目标 $f=\boldsymbol w^{\mathsf T}S\boldsymbol w$，约束 $g=\boldsymbol w^{\mathsf T}\boldsymbol w-1=0$。
2. 梯度 $\nabla f=2S\boldsymbol w$，$\nabla g=2\boldsymbol w\ne\boldsymbol 0$。
3. 拉格朗日条件 $\nabla f=\lambda\nabla g$，得 $S\boldsymbol w=\lambda\boldsymbol w$。
4. 此时 $f=\lambda$，最大值取最大特征值，$\boldsymbol w$ 是它的单位特征向量。

定理里的两个条件都不能省。没有 $\lVert\boldsymbol w\rVert=1$，$f$ 没有最大值（前面已说）。$S$ 不对称时，$\nabla(\boldsymbol w^{\mathsf T}A\boldsymbol w)=(A+A^{\mathsf T})\boldsymbol w$，不再是 $2A\boldsymbol w$，结论就错了。例如 $A=\begin{pmatrix}0&2\\0&0\end{pmatrix}$，$\boldsymbol w^{\mathsf T}A\boldsymbol w=2w_1w_2$，在单位圆上最大值是 1（取在 $(1,1)/\sqrt2$），而 $A$ 的特征值全是 0。协方差矩阵天然对称，所以本章不会碰到这种情况。

合上书，不看上面，从「最大化 $\boldsymbol w^{\mathsf T}S\boldsymbol w$，约束 $\lVert\boldsymbol w\rVert=1$」出发，推到 $S\boldsymbol w=\lambda\boldsymbol w$，并说明最大值是多少。

### 4. 第二、第三个主成分怎么找？

只留一个方向，信息往往不够。第二个方向应当捕捉第一个方向没捕捉到的变化。

二维时这个方向不用找：与 $\boldsymbol w_1$ 垂直的单位向量只有 $\pm(-0.8680,\,0.4965)$（例 3 图里的短虚线），沿它的方差 $\boldsymbol w^{\mathsf T}S\boldsymbol w\approx0.0692$，正是另一个特征值 $\lambda_2$。三维以上，与 $\boldsymbol w_1$ 垂直的方向有一整个平面甚至更多，要在其中挑方差最大的，就得再用一次拉格朗日乘子法。

为什么要求垂直？不要求的话，单位球面上最大的仍是 $\boldsymbol w_1$，找不出新方向。垂直还有统计上的含义：两组得分 $\boldsymbol t^{(1)}=X_c\boldsymbol w_1$ 与 $\boldsymbol t=X_c\boldsymbol w$ 的协方差是 $\boldsymbol w_1^{\mathsf T}S\boldsymbol w$（与 $\boldsymbol w^{\mathsf T}S\boldsymbol w$ 的推导相同）。因为 $S\boldsymbol w_1=\lambda_1\boldsymbol w_1$，$\boldsymbol w_1^{\mathsf T}S\boldsymbol w=\lambda_1\boldsymbol w_1^{\mathsf T}\boldsymbol w$，所以 $\boldsymbol w\perp\boldsymbol w_1$ 时两个新指标的协方差为零：不相关，不重复。

问题：在 $\boldsymbol w^{\mathsf T}\boldsymbol w=1$ 和 $\boldsymbol w_1^{\mathsf T}\boldsymbol w=0$ 两个约束下，最大化 $\boldsymbol w^{\mathsf T}S\boldsymbol w$。

两个约束，就有两个乘子。理由和一个约束时相同：在极值点，目标的梯度 $\nabla f$ 不能有任何「沿着约束曲面走」的分量，所以它必须落在各约束梯度张成的空间里，也就是 $\nabla g_1,\nabla g_2$ 的线性组合，每个约束带一个系数：$\nabla f=\lambda\nabla g_1+\mu\nabla g_2$，其中 $g_1=\boldsymbol w^{\mathsf T}\boldsymbol w-1$，$g_2=\boldsymbol w_1^{\mathsf T}\boldsymbol w$，$\nabla g_2=\boldsymbol w_1$：

$$2S\boldsymbol w=2\lambda\boldsymbol w+\mu\boldsymbol w_1 .$$

（C.24.7 的多约束版本还要求两个约束梯度线性无关。这里是 $2\boldsymbol w$ 与 $\boldsymbol w_1$，因为 $\boldsymbol w\perp\boldsymbol w_1$ 且 $\boldsymbol w\ne\boldsymbol 0$，满足。）

*第一步，把 $\mu$ 消去。* 左乘 $\boldsymbol w_1^{\mathsf T}$：左边 $2\boldsymbol w_1^{\mathsf T}S\boldsymbol w=2(S\boldsymbol w_1)^{\mathsf T}\boldsymbol w=2\lambda_1\boldsymbol w_1^{\mathsf T}\boldsymbol w=0$（先用 $S$ 对称，再用 $S\boldsymbol w_1=\lambda_1\boldsymbol w_1$，最后用约束 $g_2$）；右边 $2\lambda\cdot0+\mu\boldsymbol w_1^{\mathsf T}\boldsymbol w_1=\mu$。所以 $\mu=0$。

*第二步，回到特征方程。* $\mu=0$ 后条件变成 $S\boldsymbol w=\lambda\boldsymbol w$，$\boldsymbol w$ 还是特征向量，而且与 $\boldsymbol w_1$ 垂直。

*第三步，选最大的。* 方差仍是 $\lambda$。$S$ 对称，不同特征值的特征向量互相垂直（L.13），拉格朗日条件已经把候选限制在特征向量里；其中与 $\boldsymbol u_1$ 垂直的是 $\boldsymbol u_2,\dots,\boldsymbol u_d$（特征值互异时；有重特征值时见本节末），比较它们的特征值，最大的是 $\lambda_2$。

继续下去，第 $j$ 个主成分方向取第 $j$ 大特征值的单位特征向量，两两垂直。

**方法 2（逐个找主成分）**

1. 解 $\lvert S-\lambda I\rvert=0$，特征值从大到小排好 $\lambda_1\ge\lambda_2\ge\cdots$。
2. 对每个 $\lambda_j$ 求单位特征向量 $\boldsymbol w_j$（L.13：不同特征值的特征向量自动垂直）。
3. 第 $j$ 个主成分的得分 $\boldsymbol t_j=X_c\boldsymbol w_j$，方差 $\lambda_j$，各主成分的得分两两不相关。

**例 4**　和例 3 相比，指标从两个变成三个，而且要找全部主成分，不只第一个。$S=\begin{pmatrix}6&2&0\\2&3&0\\0&0&1\end{pmatrix}$，求全部主成分方向与方差。

$S$ 是块对角的，前两个指标一块，第三个单独，特征方程分块算：

$$\lvert S-\lambda I\rvert=(1-\lambda)\begin{vmatrix}6-\lambda&2\\2&3-\lambda\end{vmatrix}=(1-\lambda)(\lambda^2-9\lambda+14)=(1-\lambda)(\lambda-7)(\lambda-2).$$

特征值 $7,2,1$。$\lambda=7$：$(S-7I)\boldsymbol w=0$ 前两行 $-w_1+2w_2=0$，$2w_1-4w_2=0$，$w_3=0$，$\boldsymbol w_1=(2,1,0)/\sqrt5$。$\lambda=2$：$4w_1+2w_2=0$，$\boldsymbol w_2=(1,-2,0)/\sqrt5$。$\lambda=1$：$\boldsymbol w_3=(0,0,1)$。三个方向两两垂直，如 $\boldsymbol w_1\cdot\boldsymbol w_2=(2-2)/5=0$。

> 求 $S=\begin{pmatrix}5&0\\0&2\end{pmatrix}$ 的主成分方向。
>
> 答案：$S$ 已经是对角阵，特征值 5 和 2，方向就是坐标轴 $(1,0)$ 与 $(0,1)$：方差最大的方向是第一个指标本身。

如果恰好有两个特征值相等，比如 $\lambda_2=\lambda_3$，这个特征值的特征子空间是二维的，其中任意一对垂直的单位方向都同样好（方法 2 第 2 步要在这个子空间里选正交的单位向量），主成分方向就不唯一。这时数据在那个平面里「各个方向一样散」，没有哪一个方向特别。$\lambda_1$ 重复时同理，第一主成分方向也不唯一。

合上书，说出第二个主成分为什么是 $S$ 的第二大特征值对应的特征向量，以及得分为什么两两不相关。

每个主成分都有自己的方差 $\lambda_j$，它们从大到小排成一列。留几个才够，下一节来量。

### 5. 只留 $k$ 个主成分，丢了多少信息？

留几个主成分合适？需要一个衡量「保留了多少」的数。所有指标的总方差是 $S$ 的迹 $\mathrm{tr}\,S=\sum_jS_{jj}$。例 3 解特征方程时已经露出一个线索：老朋友①的 $S$ 对角线之和 $2.5+7.5=10$，两个特征值之和 $9.9308+0.0692$ 也是 10。这不是巧合。

**定理**　$\mathrm{tr}\,S=\lambda_1+\lambda_2+\cdots+\lambda_d$。

证明：由谱定理 $S=Q\Lambda Q^{\mathsf T}$，$Q$ 的列是单位正交的特征向量，$\Lambda=\mathrm{diag}(\lambda_1,\dots,\lambda_d)$。迹有性质 $\mathrm{tr}(AB)=\mathrm{tr}(BA)$（两边都是 $\sum_{i,j}A_{ij}B_{ji}$，例如两个 $2\times2$ 矩阵相乘，对角线元素之和不因乘的顺序改变）。把 $A=Q$、$B=\Lambda Q^{\mathsf T}$ 代入，再用 $Q^{\mathsf T}Q=I$，所以 $\mathrm{tr}(Q\Lambda Q^{\mathsf T})=\mathrm{tr}(\Lambda Q^{\mathsf T}Q)=\mathrm{tr}\Lambda=\sum\lambda_j$。$\blacksquare$

这个式子说：原来 $d$ 个指标的方差之和，恰好等于 $d$ 个主成分的方差之和，总量不变，只是重新分配，集中到前几个方向上。第 $j$ 个主成分的**方差贡献率**是 $\lambda_j/\sum_i\lambda_i$，前 $k$ 个的**累计贡献率**是 $\sum_{j\le k}\lambda_j/\sum_i\lambda_i$。

常按累计贡献率选 $k$：常用 85%–95% 作参考线，不是定理，要看用途。贡献率的分母 $\mathrm{tr}\,S$ 必须大于 0（数据不是全相同），$k$ 取 $1,\dots,d$。也可以把 $\lambda_j$ 画成一条随 $j$ 下降的折线（碎石图），在折线明显变平的地方切一刀。

**例 5**　接着例 3、例 4：求例 4 的 $S$ 和老朋友①的贡献率与累计贡献率。

用上面的定理，分母就是迹。例 4：$\mathrm{tr}\,S=6+3+1=10=7+2+1$ ✓。贡献率 $70\%$、$20\%$、$10\%$，累计 $70\%$、$90\%$、$100\%$。留两个主成分，保留 90% 的方差。

老朋友①：$\mathrm{tr}\,S=10=9.9308+0.0692$，第一主成分贡献率 $99.31\%$。五个点几乎全排在一条线上，只留一个综合指标，保留了 99.31% 的方差。

> 特征值为 $8,4,2,1,1$，累计贡献率首次达到 90% 时 $k$ 是多少？
>
> 答案：总和 16；$8/16=50\%$，$12/16=75\%$，$14/16=87.5\%$，$15/16=93.75\%$。$k=4$。

![例 5 的碎石图与累计贡献率：左，特征值 $7,2,1$ 的折线；右，累计贡献率 $70\%,90\%,100\%$ 的阶梯，虚线是 $90\%$ 的水平线](fig/M5-n4.pdf){width=85%}

有一个提醒：PCA 找的是方差最大的方向，它不看标签，所以方差大不等于对预测有用。如果两类样本是沿一个低方差的方向分开的，最大方差方向可能把两类混在一起，用 PCA 降维反而丢掉了区分信息。这类问题要用有标签的办法。

合上书，写出 $\mathrm{tr}\,S=\sum\lambda_j$ 的证明思路，并说明累计贡献率怎么算。

### 6. 换个问法：哪条直线离所有点最近？

回头看例 3 的图：五个点到实线的垂线都很短。Pearson 当年问的就是这件事：给定一堆点，哪条直线使点到它的距离平方之和最小？先在一个点上算。老朋友①的第一个点 $\boldsymbol x_c=(-2,-3)$，它在 $\boldsymbol w_1$ 上的坐标是 $-3.597$（例 3 的得分），坐标的平方约 12.94，而 $\lVert\boldsymbol x_c\rVert^2=13$。点与它的投影点之差垂直于直线，所以点到直线的距离平方是 $13-12.94\approx0.06$。

一般地，设直线过中心点（平均值点），方向为单位向量 $\boldsymbol w$。点 $\boldsymbol x_c$ 投影到直线上的位置是 $(\boldsymbol w^{\mathsf T}\boldsymbol x_c)\boldsymbol w$，这是用一个数重建出的近似；它与原来的点之间的距离就是**重建误差**。由勾股定理：

$$\lVert\boldsymbol x_c\rVert^2=(\boldsymbol w^{\mathsf T}\boldsymbol x_c)^2+\lVert\boldsymbol x_c-(\boldsymbol w^{\mathsf T}\boldsymbol x_c)\boldsymbol w\rVert^2 ,$$

于是点到直线的距离平方 $=\lVert\boldsymbol x_c\rVert^2-(\boldsymbol w^{\mathsf T}\boldsymbol x_c)^2$。对所有点求和。其中 $\sum_i\lVert\boldsymbol x_{c,i}\rVert^2=\mathrm{tr}(X_c^{\mathsf T}X_c)=(n-1)\mathrm{tr}\,S$（$X_c^{\mathsf T}X_c$ 的对角线元素就是各指标的平方和）；$\sum_i(\boldsymbol w^{\mathsf T}\boldsymbol x_{c,i})^2=\boldsymbol w^{\mathsf T}X_c^{\mathsf T}X_c\boldsymbol w=(n-1)\boldsymbol w^{\mathsf T}S\boldsymbol w$（第 2 节）。于是

$$E(\boldsymbol w)=\sum_i\lVert\boldsymbol x_{c,i}\rVert^2-\sum_i(\boldsymbol w^{\mathsf T}\boldsymbol x_{c,i})^2=(n-1)\,\mathrm{tr}\,S-(n-1)\,\boldsymbol w^{\mathsf T}S\boldsymbol w .$$

第一项（总平方和）是数据自带的，与 $\boldsymbol w$ 无关；所以**重建误差最小等价于投影方差最大**。第 3 节的答案直接搬过来：最优直线的方向是 $\boldsymbol w_1$，最小误差

$$E_{\min}=(n-1)(\mathrm{tr}\,S-\lambda_1)=(n-1)(\lambda_2+\cdots+\lambda_d).$$

以上假定直线过平均值点，最优直线确实必须如此。设直线过点 $\boldsymbol c$、方向仍是 $\boldsymbol w$，则 $\boldsymbol x_{c,i}-\boldsymbol c$ 到它的距离平方是 $\lVert\boldsymbol x_{c,i}-\boldsymbol c\rVert^2-(\boldsymbol w^{\mathsf T}(\boldsymbol x_{c,i}-\boldsymbol c))^2$。对 $i$ 求和并展开，含 $\boldsymbol c$ 的交叉项只有 $-2\boldsymbol c^{\mathsf T}\sum_i\boldsymbol x_{c,i}$ 与 $2(\boldsymbol w^{\mathsf T}\boldsymbol c)\sum_i(\boldsymbol w^{\mathsf T}\boldsymbol x_{c,i})$，两项都带 $\sum_i\boldsymbol x_{c,i}=\boldsymbol 0$，消去后总误差等于 $E(\boldsymbol w)+n\big(\lVert\boldsymbol c\rVert^2-(\boldsymbol w^{\mathsf T}\boldsymbol c)^2\big)$。因为 $\lvert\boldsymbol w^{\mathsf T}\boldsymbol c\rvert\le\lVert\boldsymbol c\rVert$（$\boldsymbol w$ 是单位向量），后一项不小于 0，$\boldsymbol c=\boldsymbol 0$ 时最小。

留 $k$ 个主成分（方向 $\boldsymbol w_1,\dots,\boldsymbol w_k$ 两两垂直、长度为 1）时，把中心化的点重建为 $\hat{\boldsymbol x}_c=\sum_{j\le k}(\boldsymbol w_j^{\mathsf T}\boldsymbol x_c)\boldsymbol w_j$，也就是向 $k$ 个方向张成的子空间做正交投影（L.10，L.15.5 的最佳近似结论与此一致）。同样由勾股定理（$\boldsymbol x_c$ 分成 $k$ 个正交分量 $(\boldsymbol w_j^{\mathsf T}\boldsymbol x_c)\boldsymbol w_j$ 与剩下的部分，因为 $\boldsymbol w_j$ 两两垂直且长度为 1，各分量互相垂直，交叉项为零），$\lVert\boldsymbol x_c-\hat{\boldsymbol x}_c\rVert^2=\lVert\boldsymbol x_c\rVert^2-\sum_{j\le k}(\boldsymbol w_j^{\mathsf T}\boldsymbol x_c)^2$，对样本求和，得 $(n-1)\big(\mathrm{tr}\,S-\sum_{j\le k}\lambda_j\big)$（把平均值加回去，就得到原坐标下的重建点）：重建误差是 $(n-1)$ 乘「丢掉的那些特征值之和」。Pearson 的问题与 Hotelling 的问题是同一个问题的两面：方差保留得越多，丢掉的就越少。

![勾股关系：对一个中心化的点 $\boldsymbol x_c$，实线是 $\boldsymbol x_c$，在方向 $\boldsymbol w$ 上的投影长度 $\boldsymbol w^{\mathsf T}\boldsymbol x_c$ 是沿直线的粗线段，垂直的虚线段是重建误差；两段的平方和等于 $\lVert\boldsymbol x_c\rVert^2$](fig/M5-n3.pdf){width=60%}

**例 6**　例 3 已经找到老朋友①的最优直线，这里求它的重建误差，并与回归直线 $y=1.7x-0.1$ 的残差平方和 1.1 比较。

用刚得到的公式算老朋友①：$E_{\min}=(n-1)\lambda_2=4\times0.0692\approx0.2769$。

两条线的「近」不是同一种近。回归（M.2）量的是**竖直**距离：$x$ 当作已知，只看 $y$ 的预测差，残差平方和 1.1。PCA 量的是点到直线的**垂直**距离，两个指标地位对等，误差平方和 $4\lambda_2\approx0.2769$。拿同一批点、两条直线、两种量法比一比：PCA 直线的垂直误差 $0.2769$；回归直线的垂直误差是 $1.1/(1+1.7^2)=110/389\approx0.2828$，比 PCA 的大（PCA 的直线正是使垂直误差最小的）；回归直线的竖直误差 $1.1$。竖直距离不小于垂直距离，所以数值大不说明回归线「更差」，只说明量的是另一种误差。

斜率也略有不同：回归直线斜率 1.7；PCA 直线的斜率 $0.8680/0.4965\approx1.748$。

两个方法并排看，先想想它们的区别在哪：回归把 $x$ 当作给定的输入，要预测 $y$；PCA 把两个指标对等地看，没有输入输出之分。指标 $x,y$ 单位变了（比如 $y$ 的单位缩小十倍），回归线只是跟着变形，PCA 的方向却可能彻底改变。这个麻烦下一节处理。

> 若只有 3 个样本，两个指标，$S$ 的特征值为 $4$ 和 $1$，最优直线的重建误差是多少？
>
> 答案：$(n-1)\lambda_2=2\times1=2$。

合上书，说出为什么重建误差最小等价于投影方差最大，并写出丢掉的特征值与重建误差之间的关系。

### 7. 指标单位不同（元、百分比、人数）时怎么办？

上一节末尾说换单位会改变 PCA 的方向。先猜：把老朋友①的第二个指标放大十倍（比如从「厘米」换成「毫米」），第一主成分方向还是 $60.2^\circ$ 吗？算出来是

$$S=\begin{pmatrix}2.5&42.5\\42.5&750\end{pmatrix},\qquad\lambda\approx752.4,\ 0.09,\qquad\boldsymbol w_1\approx(0.057,\,0.998).$$

第一主成分几乎就是第二个指标本身，第一个指标被忽略了。方向从 $60.2^\circ$ 变成了 $86.8^\circ$，只是因为换了单位。因为方差大的指标在总方差里占的份额大，PCA 就围着它转。

办法是先**标准化**：每个指标减平均值、再除以自己的标准差 $s_j$，得到 $z_{ij}=(x_{ij}-\bar x_j)/s_j$。除以标准差以后单位约掉了，每列的方差都是 1，协方差矩阵变成**相关矩阵** $R$（对角线全是 1，其余是相关系数 $r_{jk}=S_{jk}/(s_js_k)$）。这相当于在 $R$ 上做 PCA。若某个指标的标准差为 0，即所有样本取值相同，它没有变化可言，先把这一列删去，否则要除以 0。

求出的方向 $\boldsymbol w$ 属于标准化之后的变量 $z$。要给一个原样本打分，先把 $\boldsymbol x_c$ 的每个分量除以对应的 $s_j$，再与 $\boldsymbol w$ 作点积，不能直接用 $\boldsymbol w^{\mathsf T}\boldsymbol x_c$。

**例 7**　和例 3 相比，这次先把数据标准化，PCA 做在相关矩阵上。老朋友①标准化后，求主成分与贡献率，并说明换单位后结果不变。

有了 $R$，后面的做法同前。$r=4.25/\sqrt{2.5\times7.5}=0.9815$，$R=\begin{pmatrix}1&r\\r&1\end{pmatrix}$。二阶的 $R$ 好算：$R(1,1)^{\mathsf T}=(1+r)(1,1)^{\mathsf T}$，$R(1,-1)^{\mathsf T}=(1-r)(1,-1)^{\mathsf T}$。特征值 $1+r=1.9815$，$1-r=0.0185$，方向 $(1,1)/\sqrt2$ 和 $(1,-1)/\sqrt2$，第一主成分的贡献率 $1.9815/2=99.07\%$。

把 $y$ 的原始数据各乘一个正数（比如十倍），再重新中心化、标准化，得到的标准化数据和 $R$ 都和以前一样，所以结果与单位无关：$r$ 和 $R$ 照旧。

> 二阶相关矩阵 $R$ 中 $r=0.6$ 时，第一主成分的贡献率是多少？
>
> 答案：$(1+0.6)/2=80\%$。

![单位的影响：左，第二个指标放大十倍后的数据（两轴比例尺不同，纸面上的斜率不代表数据里的方向，实际方向是 $(0.057,0.998)$，几乎竖直），实线是第一主成分方向；右，标准化之后的数据，第一主成分方向（实线）是对角线，与单位无关](fig/M5-n5.pdf){width=90%}

不要一律标准化。若所有指标本来就在同一个尺度上，大小差异本身有意义（比如图像的各个像素亮度），标准化反而会把有意义的差别抹掉。

合上书，说出换单位为什么会改变 PCA 的方向，标准化怎样解决这个问题，以及标准化后用哪个矩阵。

### 8. 实际计算时，为什么用 SVD？

前面的路线是算 $S$、解特征方程，手算很顺。常用的实现（如 scikit-learn 的 PCA）不这样做，而是对中心化数据矩阵直接做 SVD（L.15）：

$$X_c=U\Sigma V^{\mathsf T},\qquad U\in\mathbb R^{n\times q},\ \Sigma\in\mathbb R^{q\times q},\ V\in\mathbb R^{d\times q},$$

$q$ 是矩阵的秩（程序里 `full_matrices=False` 返回 $\min(n,d)$ 列，其中秩以外的奇异值为 0）；$\Sigma$ 是对角矩阵，对角线上依次是奇异值，即 $\Sigma=\mathrm{diag}(\sigma_1\ge\cdots\ge\sigma_q>0)$。代入 $S$：

$$S=\frac1{n-1}X_c^{\mathsf T}X_c=\frac1{n-1}V\Sigma U^{\mathsf T}U\Sigma V^{\mathsf T}=V\,\frac{\Sigma^2}{n-1}\,V^{\mathsf T},$$

其中用了 $U^{\mathsf T}U=I$。右边的 $V$ 列单位正交，中间是对角阵，所以 $S\boldsymbol v_j=V\frac{\Sigma^2}{n-1}V^{\mathsf T}\boldsymbol v_j=\frac{\sigma_j^2}{n-1}\boldsymbol v_j$（$V^{\mathsf T}\boldsymbol v_j$ 是第 $j$ 个坐标向量）。这就是 $S$ 的谱分解：**$V$ 的列就是主成分方向，特征值是 $\lambda_j=\sigma_j^2/(n-1)$，得分矩阵是 $X_cV=U\Sigma$**。

老朋友①：$\sigma=(6.3026,\,0.5262)$，$\sigma^2/4=(9.9308,\,0.0692)$，与例 3 相同。

为什么用 SVD 比先算 $S$ 好？有三个原因，各带一组数。

- 数值稳定。条件数是最大奇异值与最小非零奇异值之比，条件数越大，结果对舍入误差越敏感，所以越小越好。$X_c$ 列满秩时，$X_c^{\mathsf T}X_c$ 的条件数是 $X_c$ 的平方：老朋友①是 $11.98$ 对 $143.4$，同样的舍入误差对结果的影响会放大得更多。
- 省空间。$n=100$ 个样本、$d=10^4$ 维时，$S$ 有 $10^8$ 个元素（每个 8 字节，约 800MB），而 $X_c$ 只有 $10^6$ 个。
- 秩小的时候不浪费。$n<d$ 时 $S$ 的秩至多是 $n-1$，$n\ll d$ 时大部分特征值是 0，SVD 一次给出全部有用的部分。

代码里就是几行：

```python
Xc = X - X.mean(axis=0)                          # (n, d) 中心化
U, s, Vt = np.linalg.svd(Xc, full_matrices=False)
var = s**2 / (len(X) - 1)                        # 各主成分的方差
scores = Xc @ Vt.T                               # (n, m) 每个样本的得分，m=min(n,d)
W2 = Vt[:2].T                                    # (d, 2) 前两个主成分方向
scores2 = Xc @ W2                                # (n, 2) 前两个主成分的得分
```

**例 8**　和例 3 相比，不再解特征方程，改用 SVD。有四个词元，模型给每个词元一串三个数（这是为了手算而假设的数据）：$(6,2,3)$、$(4,6,3)$、$(-2,-2,3)$、$(-4,2,3)$。用 SVD 求前两个主成分、得分和贡献率，并把二维得分画成平面散点。

这道题把方法用在 AI 里最常见的场合：模型把每个词元表示成一串数（嵌入向量），要把这些高维向量画到平面上。思路是对中心化数据做 SVD，再取前两个方向。

*第一步，中心化。* 三列平均 $(1,2,3)$，$X_c$ 的四行是 $(5,0,0)$、$(3,4,0)$、$(-3,-4,0)$、$(-5,0,0)$。第三列全是 0：这个指标原来恒为 3，没有变化。

*第二步，求奇异值。* $X_c^{\mathsf T}X_c$ 的非零部分是 $\begin{pmatrix}68&24\\24&32\end{pmatrix}$，特征方程 $\lambda^2-100\lambda+1600=0$，$\lambda=80,\ 20$。奇异值 $\sigma=\sqrt{80}=4\sqrt5\approx8.944$、$\sqrt{20}=2\sqrt5\approx4.472$。$\lambda=80$ 的单位特征向量 $\boldsymbol v_1=(2,1,0)/\sqrt5$，$\lambda=20$ 的是 $\boldsymbol v_2=(1,-2,0)/\sqrt5$。方差 $\lambda_j=\sigma_j^2/(n-1)=80/3,\ 20/3$，贡献率 $80\%$、$20\%$，两个主成分就保留了全部方差（第三个指标没有变化）。

*第三步，得分。* $X_c\boldsymbol v_1=(10,10,-10,-10)/\sqrt5\approx(4.472,4.472,-4.472,-4.472)$，$X_c\boldsymbol v_2=(5,-5,5,-5)/\sqrt5\approx(2.236,-2.236,2.236,-2.236)$。四个词元在平面上是四个点 $(\pm4.472,\pm2.236)$。两个方向与例 4 的前两个主成分相同，只是特征值不同。

真实的嵌入向量有几百维。比如 $n=100$ 个词元、每个 $d=768$ 维，做法完全相同：$X_c\in\mathbb R^{100\times768}$，做 SVD，取 $V$ 的前两列 $W_2\in\mathbb R^{768\times2}$，得分 $X_cW_2\in\mathbb R^{100\times2}$。因为 $X_c$ 的各列之和为零，等价于全 1 向量 $\boldsymbol 1$ 满足 $\boldsymbol 1^{\mathsf T}X_c=\boldsymbol 0$，所以 $X_c^{\mathsf T}$ 的零空间至少有一维，$X_c$ 的秩至多是 $n-1=99$，$S$ 是 $768\times768$ 的矩阵但最多有 99 个非零特征值（$n\ll d$）。

> 同样的 $X_c$，前两个主成分的累计贡献率怎么从 SVD 算出？
>
> 答案：$(\sigma_1^2+\sigma_2^2)/\sum_j\sigma_j^2$，因为 $\lambda_j=\sigma_j^2/(n-1)$，分子分母的 $n-1$ 约掉。

合上书，从 $X_c=U\Sigma V^{\mathsf T}$ 推出 $S$ 的谱分解，说明主成分方向、方差和得分各是什么。

### 9. 一道 PCA 大题怎样从头写到尾？

把前面的步骤接起来。

**方法 3（PCA 手算全流程）**

1. 中心化：每列减去列平均。
2. 协方差矩阵 $S=\frac1{n-1}X_c^{\mathsf T}X_c$。
3. 特征分解：特征值从大到小，单位特征向量（正交化）。
4. 贡献率与累计贡献率，定 $k$。
5. 得分：$\boldsymbol t_j=X_c\boldsymbol w_j$，即把每个样本投影到前 $k$ 个方向上。
6. 若问重建误差，用 $(n-1)\times$ 丢掉的特征值之和。

**例 9**　和例 3、例 4 相比，这是从原始数据开始的完整一遍，每一步都用前面的方法。五个样本，每个有三个指标：$(57,51,10)$、$(59,47,10)$、$(60,50,10)$、$(62,51,8)$、$(62,51,12)$。用 PCA 降到二维，并求累计贡献率与重建误差。

$S$ 的结构和例 4 一样，是一个二阶块加单独的一列，特征分解只需解一个二次方程。

*第一步，中心化。* 三列平均分别是 $60,\,50,\,10$。

$$X_c=\begin{pmatrix}-3&1&0\\-1&-3&0\\0&0&0\\2&1&-2\\2&1&2\end{pmatrix}.$$

*第二步，协方差矩阵。* 先算 $X_c^{\mathsf T}X_c$。各列的平方和：第一列 $9+1+0+4+4=18$，第二列 $1+9+0+1+1=12$，第三列 $0+0+0+4+4=8$。交叉积：第一、二列 $(-3)(1)+(-1)(-3)+0+2\cdot1+2\cdot1=4$；第三列与第一列 $2\cdot(-2)+2\cdot2=0$，与第二列 $1\cdot(-2)+1\cdot2=0$。除以 $n-1=4$：

$$S=\begin{pmatrix}4.5&1&0\\1&3&0\\0&0&2\end{pmatrix}.$$

*第三步，特征分解。* 块对角：第三个指标单独，特征值 2，方向 $(0,0,1)$。前两个指标：$\lambda^2-7.5\lambda+12.5=0$，$\lambda=5,\ 2.5$。$\lambda=5$：$-0.5w_1+w_2=0$，$\boldsymbol w_1=(2,1,0)/\sqrt5$。$\lambda=2.5$：$2w_1+w_2=0$，$\boldsymbol w_2=(1,-2,0)/\sqrt5$。验证 $S\boldsymbol w_1$：$(9+1,\ 2+3,\ 0)/\sqrt5=5\boldsymbol w_1$ ✓。特征值从大到小：$5,\ 2.5,\ 2$，方向依次是 $(2,1,0)/\sqrt5$、$(1,-2,0)/\sqrt5$、$(0,0,1)$。

*第四步，贡献率。* 总方差 $4.5+3+2=9.5=5+2.5+2$。贡献率 $52.6\%$、$26.3\%$、$21.1\%$；前两个累计 $78.9\%$。降到二维保留 78.9% 的方差；要保留 90% 以上就需要三个主成分。

*第五步，得分。* $t_1=(2x_{c1}+x_{c2})/\sqrt5$，$t_2=(x_{c1}-2x_{c2})/\sqrt5$：

$$\begin{array}{c|ccccc}&\text{样本1}&\text{样本2}&\text{样本3}&\text{样本4}&\text{样本5}\\\hline t_1&-2.236&-2.236&0&2.236&2.236\\t_2&-2.236&2.236&0&0&0\end{array}$$

核对方差：$t_1$ 的平方和 $4\times5=20$，除以 4 得 5，与 $\lambda_1$ 一致。

*第六步，重建误差。* 丢掉第三个主成分，$E=(n-1)\lambda_3=4\times2=8$，恰好等于第三列的平方和 $\sum x_{c3}^2=8$。样本 4 和 5 在平面上重合在同一点，因为它们只在被丢掉的第三个指标上不同。

![例 9 的二维得分图：横轴 $t_1$，纵轴 $t_2$。五个样本用实心圆标出，样本 4、5 重合在 $(2.236,0)$，因为它们只在被丢掉的第三个主成分上不同；虚线是坐标轴。](fig/M5-n6.pdf){width=60%}

> 用同一个 $S$，只留一个主成分的重建误差是多少？
>
> 答案：丢掉 $\lambda_2+\lambda_3=4.5$，误差 $4\times4.5=18$。

回到开头的问题：几个指标合成一个综合指标，权重凭什么定？例 9 的第一个综合指标是 $t_1=(2x_{c1}+x_{c2})/\sqrt5$，三个指标的权重是 $(0.894,\,0.447,\,0)$。它们由数据自己定出来：在权重向量长度为 1 的前提下，让综合指标的方差最大。这个综合指标保留了 $5/9.5=52.6\%$ 的总方差，加上第二个综合指标共保留 $78.9\%$。第三个指标与前两个不相关，自己的方差只有 2，小于两个主成分的 5 和 2.5，所以没有进入这两个综合指标。要注意权重取决于单位，指标换了单位，权重也会变，这就是第 7 节要先标准化的原因。

合上书，对一个 $3\times3$ 的协方差矩阵，从「最大化投影方差」写到「前两个主成分的累计贡献率」，每一步说明依据。

### 本章小结

主线上，PCA 是无标签的一章：模型是把数据投影到前 $k$ 个相互垂直的方向；损失是重建误差，它等价于最大化投影方差（第 6 节）；对 PCA 来说，解可以由一次特征分解（或 SVD）直接得到，不像梯度下降那样一步步更新（数值软件内部算特征分解时另有迭代）。本章没有新的「损失 ⇐ 概率假设」行，因为它不涉及标签与概率模型。


| 方法 | 什么时候用 | 对应题号 |
|---|---|---|
| 方法 1（求第一主成分） | 找数据方差最大的方向；写拉格朗日推导 | M5-01、M5-02、M5-03、M5-06、M5-09、M5-10 |
| 方法 2（逐个找主成分） | 已知协方差矩阵，求全部主成分与方差；证明得分不相关 | M5-04、M5-08、M5-11、M5-12 |
| 贡献率与累计贡献率 | 决定保留几个主成分，$\mathrm{tr}\,S=\sum\lambda_j$ | M5-05、M5-07、M5-12 |
| 重建误差 $(n-1)\sum_{\text{丢掉}}\lambda_j$ | 证明最小重建误差等价于最大方差；与回归比较 | M5-05、M5-13 |
| 标准化后用相关矩阵 | 指标单位不同；二阶 $R$ 的特征值 $1\pm r$ | M5-10 |
| 用 SVD 求主成分 | 实际计算；$\lambda_j=\sigma_j^2/(n-1)$，得分 $U\Sigma$ | M5-07 |
| 方法 3（PCA 手算全流程） | 一道题从数据写到降维结果 | M5-05、M5-07、M5-08、M5-09、M5-10、M5-12、M5-13、M5-14、M5-15 |
