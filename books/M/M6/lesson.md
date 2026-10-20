## M.6 · 拉格朗日对偶与 SVM

有些分类任务只有少量样本，每个样本却带着很多特征，比如几百篇文档、每篇有上万个词的计数。这时分界线画在哪里就格外要紧：稍微画偏一点，新来的样本就会判错。支持向量机（SVM）给出一种选择分界面的办法：在所有能把两类分开的分界面里，挑离最近样本尽量远的那一个。

这个想法马上带来两个问题。第一，「离得远」要写成可以求解的式子，而约束是不等式，C.24 的乘子法只管等式。第二，真实数据常有噪声，两类也未必被直线分开，最大间隔还能不能用？Vapnik 等人从 1960 年代起研究怎样的分界线泛化最好；1992 年，Boser、Guyon 与 Vapnik 用核技巧回答了弯曲分界的问题；1995 年，Cortes 与 Vapnik 允许部分样本越过间隔边界，回答了噪声的问题。本章按概念上的顺序走：先从能被直线分开的少量点（硬间隔）出发，再放宽到有噪声的软间隔，最后讲核，回到开头这个选分界面的问题。

对照三件套：第 1–6 节仍用线性得分 $f(\boldsymbol x)=\boldsymbol w^{\mathsf T}\boldsymbol x+b$（M.2.3），损失在第 6 节换成合页损失加 L2 惩罚；第 7 节用核函数，得到在原坐标中可以弯曲的分类器。更新规则这一次不走梯度下降，改解对偶问题；数学基础是把 C.24 的拉格朗日乘子法推广到不等式约束，这是本章的重点。

本章的顺序：第 1、2 节把「最稳妥」写成「间隔最大」的优化问题；第 3 节把乘子法推广到不等式约束（KKT 条件）；第 4 节得到对偶问题；第 5 节看出分界线只由部分样本决定；第 6 节允许数据分不开；第 7 节用核技巧画弯曲的分界。

### 1. 两类点之间，哪条分界线最稳妥？

本章的老朋友是平面上的三个点，正类 $\boldsymbol x_1=(3,3)$、$\boldsymbol x_2=(4,3)$，负类 $\boldsymbol x_3=(1,1)$。记号说明：粗体 $\boldsymbol x_i$ 表示第 $i$ 个样本，普通字体 $x_1,x_2$ 表示一个点的两个坐标；样本总数记作 $n$。标签记成 $y_i\in\{+1,-1\}$，不用 M.2 的 $0/1$，这样「分对」可以用一个式子写出：$y_i(\boldsymbol w^{\mathsf T}\boldsymbol x_i+b)>0$。

能分开它们的直线有无数条。数据难免有误差，分界线离最近的点越远，点抖动一下就越不容易越过去，所以先要量出「离得多远」。

直线 $\boldsymbol w^{\mathsf T}\boldsymbol x+b=0$（$\boldsymbol w\ne\boldsymbol0$）的法向量是 $\boldsymbol w$（L.2.4）。取直线上任一点 $\boldsymbol x_0$，则 $\boldsymbol w^{\mathsf T}\boldsymbol x_0=-b$。点 $\boldsymbol x$ 到直线的距离，等于 $\boldsymbol x-\boldsymbol x_0$ 在 $\boldsymbol w$ 方向上的投影长度（L.2.3）：

$$\frac{|\boldsymbol w^{\mathsf T}(\boldsymbol x-\boldsymbol x_0)|}{\lVert\boldsymbol w\rVert}=\frac{|\boldsymbol w^{\mathsf T}\boldsymbol x+b|}{\lVert\boldsymbol w\rVert}.$$

$\lVert\boldsymbol w\rVert$ 是向量 $\boldsymbol w$ 的长度。分类全部正确时，每个 $y_i(\boldsymbol w^{\mathsf T}\boldsymbol x_i+b)$ 都是正数，距离可以写成 $y_i(\boldsymbol w^{\mathsf T}\boldsymbol x_i+b)/\lVert\boldsymbol w\rVert$。一条直线的**间隔**，就是所有点到它的距离中最小的那个。

**方法 1（求间隔）**

1. 对每个点算 $y_i(\boldsymbol w^{\mathsf T}\boldsymbol x_i+b)$，全为正才说明这条线把两类分对了。
2. 都除以 $\lVert\boldsymbol w\rVert$ 得到距离。
3. 取最小值，就是间隔。

**例 1**　三个点 $\boldsymbol x_1=(3,3)$、$\boldsymbol x_2=(4,3)$、$\boldsymbol x_3=(1,1)$，直线 $x_1+3x_2-6=0$。求三个点到直线的距离，以及其中最小的一个。

先不管标签，只量距离，直接套上面的距离公式。

这里 $\boldsymbol w=(1,3)^{\mathsf T}$，$b=-6$，$\lVert\boldsymbol w\rVert=\sqrt{10}$。三个点的 $\boldsymbol w^{\mathsf T}\boldsymbol x_i+b$ 是

$$3+9-6=6,\qquad 4+9-6=7,\qquad 1+3-6=-2,$$

取绝对值再除以 $\sqrt{10}$，距离约 $1.897,\ 2.214,\ 0.632$，最小的是 $0.632$，来自 $\boldsymbol x_3$。

如果把 $\boldsymbol x_1,\boldsymbol x_2$ 看作正类、$\boldsymbol x_3$ 看作负类，三个带标签的值 $y_i(\boldsymbol w^{\mathsf T}\boldsymbol x_i+b)$ 是 $6,7,2$，全为正，这条直线把三个点分对了，它的间隔就是 $0.632$。

> 三个点到直线 $x_1+x_2-4=0$ 的最小距离是多少？
>
> 答案：$\lVert\boldsymbol w\rVert=\sqrt2$，三个值 $|3+3-4|,\ |4+3-4|,\ |1+1-4|$ 是 $2,3,2$，距离 $\sqrt2,\ \tfrac{3}{\sqrt2},\ \sqrt2$，最小的是 $\sqrt2\approx1.414$。

合上书，写出点到直线的距离公式，并用它比较两条分界线的间隔。

图里把四条线放在一起：$x_1+x_2=4$ 的间隔最大，$x_1+3x_2=6$ 最小。靠试不是办法，下一节把「找间隔最大的那条」写成一个优化问题。

![四条都能分开三个点的直线，间隔不同；实线 $x_1+x_2=4$ 到最近的两个点距离都是 $\sqrt2$，最大](fig/M6-n1.pdf){width=70%}

### 2. 「间隔最大」怎样写成一个优化问题？

先回到例 1 的三个点。把直线 $x_1+3x_2-6=0$ 两边同乘 2，得 $2x_1+6x_2-12=0$，仍是同一条直线；三个点的值翻倍成 $12,14,-4$，而 $\lVert(2,6)\rVert$ 也翻倍，距离一点没变。可见 $(\boldsymbol w,b)$ 的大小可以随便取，距离只看它们的比值。再看直线 $x_1+x_2-4=0$：三个点带标签的值是 $2,3,2$，两边同除以 2，得到 $\tfrac12x_1+\tfrac12x_2-2=0$，带标签的值变成 $1,\tfrac32,1$，最小的正好是 1。下面把这个操作写成一般的做法。

下面先假定样本中两类都出现，并且能被某条直线严格分开。要求的是

$$\max_{\boldsymbol w,b}\ \min_i\ \frac{y_i(\boldsymbol w^{\mathsf T}\boldsymbol x_i+b)}{\lVert\boldsymbol w\rVert},$$

先对 $i$ 取最小、再对 $\boldsymbol w,b$ 取最大，两层套在一起不好处理。可以利用一个自由度：$(\boldsymbol w,b)$ 乘上任何正数 $c>0$，直线不变，距离也不变，所以我们可以随意规定它们的大小。如果只要求带标签的值尽量大，把 $\boldsymbol w,b$ 放大就能做到，没有最大值，这是必须固定尺度的原因。

规定的办法是：对一条已经分对全部样本的直线，令 $\gamma=\min_iy_i(\boldsymbol w^{\mathsf T}\boldsymbol x_i+b)>0$，再把 $\boldsymbol w,b$ 同时除以 $\gamma$。此时最小的带标签得分恰为 1，间隔写成 $1/\lVert\boldsymbol w\rVert$，并且所有点都满足

$$y_i(\boldsymbol w^{\mathsf T}\boldsymbol x_i+b)\ge1.$$

让 $1/\lVert\boldsymbol w\rVert$ 最大，就是让 $\lVert\boldsymbol w\rVert$ 最小。为了求导时不带出多余的系数，改成最小化 $\tfrac12\lVert\boldsymbol w\rVert^2$（最小点不变）。约束写成「大于或等于 1」，允许点落在间隔边界上；最优时至少有一个约束取等号，否则所有得分都大于 1，还能同时缩小 $\boldsymbol w,b$，保持可行并让目标变小。

**方法 2（硬间隔 SVM 的原问题）**

$$\min_{\boldsymbol w,b}\ \tfrac12\lVert\boldsymbol w\rVert^2\qquad\text{约束：}\ y_i(\boldsymbol w^{\mathsf T}\boldsymbol x_i+b)\ge1,\quad i=1,\dots,n.$$

1. 每个点一条约束，要求它在间隔边界上或正确一侧的带外。
2. 目标是二次函数，约束是一次不等式，这是最好解的一类凸优化。

对老朋友三个点，变量是 $w_1,w_2,b$，问题是：最小化 $\tfrac12(w_1^2+w_2^2)$，约束

$$3w_1+3w_2+b\ge1,\qquad 4w_1+3w_2+b\ge1,\qquad -w_1-w_2-b\ge1.$$

**例 2**　求解上面这个问题：最小化 $\tfrac12(w_1^2+w_2^2)$，满足以上三条约束。

和例 1 相比，这次要在一组不等式约束下求最小值，不再是量一条给定的直线。

直接用 C.24.7 的拉格朗日乘子法不行，它只处理等号约束。这里先猜：约束取等号的应当是离分界线最近的点，看图，$\boldsymbol x_2$ 在 $\boldsymbol x_1$ 的正右侧，离负类更远，最近的一对是 $\boldsymbol x_1,\boldsymbol x_3$，所以猜第 1、3 条取等号。

第一步，解这两个等式：

$$3(w_1+w_2)+b=1,\qquad (w_1+w_2)+b=-1.$$

两式相减得 $w_1+w_2=1$，进而 $b=-2$。

第二步，在 $w_1+w_2=1$ 上求最小。因为 $w_1^2+w_2^2=\tfrac12(w_1+w_2)^2+\tfrac12(w_1-w_2)^2\ge\tfrac12$，等号在 $w_1=w_2$ 时成立，所以 $w_1=w_2=\tfrac12$，目标值 $\tfrac12\cdot\tfrac12=\tfrac14$。

第三步，检查没用上的第 2 条：$4\cdot\tfrac12+3\cdot\tfrac12-2=\tfrac32\ge1$，满足。

> 正类点 $(3,0)$，负类点 $(1,0)$，最小化 $\tfrac12(w_1^2+w_2^2)$，约束 $3w_1+b\ge1$，$-(w_1+b)\ge1$。
>
> 答案：两条约束左边相加，得 $2w_1\ge2$；猜两条都取等号，$w_1=1$，$b=-2$。$w_2$ 只出现在目标里，取 0 最小，最小值 $\tfrac12$，分界线 $x_1=2$ 正好在两点中间。

合上书，把「间隔最大」写成带约束的最小化问题，并说明约束里的 1 是怎么来的。

例 2 的做法是猜出来的，没有证明它最优；点多了，也没法逐个猜哪些约束取等号。下一节把乘子法推广到不等式，给出有章法的办法，第 4 节再回头证明这个猜测是对的。

### 3. 约束是不等式时，拉格朗日乘子法要怎么改？

#### 起作用与不起作用

先看一元的小例子：最小化 $x^2$，约束 $x\ge1$。最低点 $x=0$ 不满足约束，最优点只能落在边界 $x=1$。若约束是 $x\ge-1$，$x=0$ 满足约束，约束根本没起作用。

一般地，把约束写成 $g_i(\boldsymbol x)\le0$，目标记作 $J(\boldsymbol x)$（$f$ 留给后面的分类得分）。设 $\boldsymbol x^*$ 是最优点：

- 若 $g_i(\boldsymbol x^*)<0$，由连续性，在 $\boldsymbol x^*$ 附近作足够小的移动仍满足这一条，它在这里没有限制作用，叫**不起作用**；
- 若 $g_i(\boldsymbol x^*)=0$，最优点贴着这条约束的边界，叫**起作用**。

#### 只有一条约束起作用：乘子为什么非负

只有一条约束起作用且 $\nabla g\ne\boldsymbol0$ 时，和等号约束一样，$\nabla J$ 与 $\nabla g$ 平行（C.24.8），写成 $\nabla J=-\alpha\nabla g$。区别在符号：等号约束里 $\lambda$ 正负都可以，不等式约束里最优点是被边界「顶住」的。

$J$ 下降最快的方向是 $\boldsymbol d=-\nabla J=\alpha\nabla g$，而 $g$ 沿 $\nabla g$ 增大。若 $\alpha<0$，$\boldsymbol d$ 指向 $g<0$ 的一侧，沿它作足够小的移动既满足约束又让 $J$ 下降，原来的点就不可能最优。所以最优点处必须 $\alpha\ge0$。

#### 多条约束同时起作用

这时不能要求 $\nabla J$ 与每个 $\nabla g_i$ 单独平行。例如在 $x\ge0,\ y\ge0$ 下最小化 $x+y$，最优点是原点，$\nabla J=(1,1)$。把约束写成 $g_1=-x\le0$，$g_2=-y\le0$，$\nabla g_1=(-1,0)$，$\nabla g_2=(0,-1)$，$(1,1)$ 与其中任何一个都不平行，却满足 $\nabla J+1\cdot\nabla g_1+1\cdot\nabla g_2=\boldsymbol0$。一般的说法是：$-\nabla J$ 被起作用的约束的梯度以非负的权重合起来平衡。

#### KKT 四条

记 $L(\boldsymbol x,\boldsymbol\alpha)=J(\boldsymbol x)+\sum_i\alpha_ig_i(\boldsymbol x)$。C.24.7 里等号约束写成 $f-\lambda(g-c)$，这里不等式写成 $+\alpha g$，区别只是符号约定，$\alpha\ge0$ 的方向才是新信息。

**方法 3（KKT 条件）** 本章用它求解的目标 $J$ 都可微，约束 $g_i\le0$ 都是一次不等式（可以带常数项）。在这类问题的最优点 $\boldsymbol x^*$，存在 $\alpha_i$ 满足

1. 平稳：$\nabla_{\boldsymbol x}L=\nabla J+\sum_i\alpha_i\nabla g_i=\boldsymbol 0$；
2. 可行：$g_i(\boldsymbol x^*)\le0$；
3. 乘子非负：$\alpha_i\ge0$；
4. 互补松弛：$\alpha_ig_i(\boldsymbol x^*)=0$，即约束不起作用的，乘子为 0。

若目标 $J$ 还是凸函数，满足四条的可行点就是全局最小点（见本节末）。求解时对每条约束讨论「起作用 / 不起作用」两种情况，用条件 1 和 4 解出候选点，再检查 2、3。

**例 3**　最小化 $x_1^2+x_2^2$，约束 $x_1+x_2\ge2$。

例 2 靠看图猜哪条约束取等号。这一道只有一条约束，目标也最简单，正好用 KKT 把「起作用 / 不起作用」两种情形逐个讨论清楚。

写成 $g=2-x_1-x_2\le0$，$L=x_1^2+x_2^2+\alpha(2-x_1-x_2)$，由条件 1：

$$2x_1-\alpha=0,\qquad 2x_2-\alpha=0\ \Rightarrow\ x_1=x_2=\alpha/2.$$

若约束不起作用，$\alpha=0$，得 $\boldsymbol x=\boldsymbol 0$，但 $g=2>0$，违反可行性。所以约束起作用，$x_1+x_2=2$，得 $\boldsymbol x=(1,1)$，$\alpha=2\ge0$，通过。最小值是 2。

> 最小化 $x_1^2+x_2^2$，约束 $x_1+x_2\ge4$，求最优点与 $\alpha$。
>
> 答案：写成 $g=4-x_1-x_2\le0$，平稳条件仍给 $x_1=x_2=\alpha/2$。$\alpha=0$ 违反可行性，所以约束起作用，$x_1+x_2=4$，$\boldsymbol x=(2,2)$，$\alpha=4\ge0$，最小值 8。

**例 4**　和例 3 一样只有一条线性约束，但目标换成 $(x_1-2)^2+(x_2-1)^2$，约束换成 $x_1+x_2\le2$。

无约束的最低点是 $(2,1)$，和为 3，违反约束，所以约束起作用。写成 $g=x_1+x_2-2$，由条件 1：

$$2(x_1-2)+\alpha=0,\qquad 2(x_2-1)+\alpha=0\ \Rightarrow\ x_1=2-\tfrac\alpha2,\ x_2=1-\tfrac\alpha2.$$

代入 $x_1+x_2=2$ 得 $\alpha=1\ge0$，$\boldsymbol x=(1.5,0.5)$。若约束改成 $x_1+x_2\le5$，$(2,1)$ 已满足，取 $\alpha=0$。

> 最小化 $(x-3)^2$，约束 $x\le1$，求最优点与 $\alpha$。
>
> 答案：无约束最低点 $x=3$ 违反，约束起作用，$x=1$。$g=x-1$，$2(x-3)+\alpha=0$ 得 $\alpha=4\ge0$。

#### 凸问题里 KKT 也是充分的

设 $J,g_i$ 是可微的凸函数，$(\boldsymbol x^*,\boldsymbol\alpha)$ 满足 KKT。对任一可行点 $\boldsymbol x$：

1. 因为 $\alpha_i\ge0$、$g_i(\boldsymbol x)\le0$，有 $J(\boldsymbol x)\ge L(\boldsymbol x,\boldsymbol\alpha)$；
2. $L(\cdot,\boldsymbol\alpha)$ 是凸函数，在 $\boldsymbol x^*$ 处梯度为零，所以 $\boldsymbol x^*$ 是它的最小点，$L(\boldsymbol x,\boldsymbol\alpha)\ge L(\boldsymbol x^*,\boldsymbol\alpha)$；
3. 互补松弛使 $L(\boldsymbol x^*,\boldsymbol\alpha)=J(\boldsymbol x^*)$。

合起来 $J(\boldsymbol x)\ge J(\boldsymbol x^*)$，$\boldsymbol x^*$ 就是最小点。这三步也是下一节弱对偶的基础。

凸性不能去掉。最小化 $J=-x^2$，约束 $-1\le x\le1$：在 $x=0$ 处 $J'=0$，两条约束都不起作用，乘子取 0，四条全部满足，可是 $x=0$ 是最大点，$J(\pm1)=-1$ 更小。

SVM 的目标可微且凸，约束都是一次不等式，因此在有最优解时，KKT 四条既是必要条件也是充分条件。这里用的是一次不等式约束的情形，不能把必要性原样推广到任意弯曲的约束。

到这里，不等式约束已经能处理了。但 SVM 有 $n$ 个点就有 $n$ 条约束，每条都要分起作用与否，按这种逐条讨论的办法，最坏要试 $2^n$ 种组合，例 2 靠猜只是运气好。下一节把问题换一种写法，让要找的东西变成只有 $n$ 个乘子。

合上书，说出 KKT 的四条，并解释：为什么只有一条约束起作用时，乘子必须非负。

### 4. 换一个问题来解，为什么反而更容易？

先看最小的情形：正类点 $(1,0)$，负类点 $(-1,0)$。两条约束是 $w_1+b\ge1$ 和 $w_1-b\ge1$，各配一个乘子 $\alpha_1,\alpha_2\ge0$，拉格朗日函数是

$$L=\tfrac12(w_1^2+w_2^2)-\alpha_1(w_1+b-1)-\alpha_2(w_1-b-1).$$

$b$ 只出现在 $-(\alpha_1-\alpha_2)b$ 里。$\alpha_1\ne\alpha_2$ 时，让 $b$ 趋于正或负无穷，$L$ 就能任意小，这样的 $\alpha$ 没有用处，所以只看 $\alpha_1=\alpha_2=\alpha$。这时 $L=\tfrac12(w_1^2+w_2^2)-2\alpha w_1+2\alpha$，对 $w_1$ 配方，在 $w_1=2\alpha$、$w_2=0$ 处最小，最小值是

$$d(\alpha)=2\alpha-2\alpha^2 .$$

它在 $\alpha=\tfrac12$ 处最大，值 $\tfrac12$；而原问题的解是 $\boldsymbol w=(1,0)^{\mathsf T}$，目标值也是 $\tfrac12$。「$\boldsymbol w,b$ 加两条约束」就这样换成了只含 $\alpha$ 的问题。下面对一般的 $n$ 个点做同样的事。

数据在对偶问题里只以内积 $\boldsymbol x_i^{\mathsf T}\boldsymbol x_j$ 的形式出现，这一点到第 7 节成了关键。变量个数是样本数 $n$，和特征的个数无关，这也是开头那种 $n$ 小 $d$ 大的任务适合用它的原因。

约束 $1-y_i(\boldsymbol w^{\mathsf T}\boldsymbol x_i+b)\le0$ 对应乘子 $\alpha_i\ge0$，拉格朗日函数是

$$L(\boldsymbol w,b,\boldsymbol\alpha)=\tfrac12\lVert\boldsymbol w\rVert^2-\sum_i\alpha_i\big[y_i(\boldsymbol w^{\mathsf T}\boldsymbol x_i+b)-1\big].$$

对任何 $\alpha_i\ge0$ 和可行的 $(\boldsymbol w,b)$，括号里非负，所以 $L\le\tfrac12\lVert\boldsymbol w\rVert^2$。记**对偶函数** $d(\boldsymbol\alpha)=\min_{\boldsymbol w,b}L(\boldsymbol w,b,\boldsymbol\alpha)$（下面会看到，有时它是 $-\infty$），那么对每个可行点有 $d(\boldsymbol\alpha)\le L(\boldsymbol w,b,\boldsymbol\alpha)\le\tfrac12\lVert\boldsymbol w\rVert^2$：第一个不等号是因为最小值不会超过在这个点处的函数值，第二个是上一句。也就是说，每个 $\boldsymbol\alpha\ge\boldsymbol 0$ 给出原问题最优值 $p^*$ 的一个下界。要找最好的下界，就解

$$\max_{\boldsymbol\alpha\ge\boldsymbol0}d(\boldsymbol\alpha),$$

这是**对偶问题**，最优值 $d^*\le p^*$（弱对偶）。

在本节两类可分的硬间隔问题中，SVM 的最优点满足 KKT（第 3 节末），设乘子为 $\boldsymbol\alpha^*$。第 3 节「凸问题里 KKT 也是充分的」那三步里的第 2 步说 $(\boldsymbol w^*,b^*)$ 使 $L(\cdot,\boldsymbol\alpha^*)$ 最小，所以 $d(\boldsymbol\alpha^*)=L(\boldsymbol w^*,b^*,\boldsymbol\alpha^*)$；再由互补松弛，它等于 $\tfrac12\lVert\boldsymbol w^*\rVert^2=p^*$。于是 $d^*\ge p^*$，结合弱对偶得 $d^*=p^*$（强对偶）。

**把 $d(\boldsymbol\alpha)$ 写出来。** 固定 $\boldsymbol\alpha\ge\boldsymbol0$，先看 $b$ 的系数。记 $q=\sum_i\alpha_iy_i$，拉格朗日函数里关于 $b$ 的项是 $-bq$。若 $q\ne0$，选合适的 $b$ 就能让 $L$ 任意小，此时 $d(\boldsymbol\alpha)=-\infty$，这个下界没有用处。

只有 $q=0$ 时 $b$ 才消失。令 $\boldsymbol v=\sum_i\alpha_iy_i\boldsymbol x_i$，$L$ 里 $\boldsymbol w$ 的部分是 $\tfrac12\lVert\boldsymbol w\rVert^2-\boldsymbol w^{\mathsf T}\boldsymbol v$，配方得

$$L=\tfrac12\lVert\boldsymbol w-\boldsymbol v\rVert^2+\sum_i\alpha_i-\tfrac12\lVert\boldsymbol v\rVert^2 .$$

第一项在 $\boldsymbol w=\boldsymbol v$ 时取到 0，所以

$$d(\boldsymbol\alpha)=\begin{cases}\displaystyle\sum_i\alpha_i-\tfrac12\Big\lVert\sum_i\alpha_iy_i\boldsymbol x_i\Big\rVert^2,&\sum_i\alpha_iy_i=0,\\[2mm]-\infty,&\sum_i\alpha_iy_i\ne0.\end{cases}$$

于是找最好的下界时，只需考虑 $\sum_i\alpha_iy_i=0$ 的 $\boldsymbol\alpha$。展开 $\lVert\boldsymbol v\rVert^2=\sum_{i,j}\alpha_i\alpha_jy_iy_j\boldsymbol x_i^{\mathsf T}\boldsymbol x_j$，就得到下面的形式；同时 $\boldsymbol w=\boldsymbol v=\sum_i\alpha_iy_i\boldsymbol x_i$。

**方法 4（SVM 的对偶问题）**

$$\max_{\boldsymbol\alpha}\ \sum_i\alpha_i-\tfrac12\sum_{i,j}\alpha_i\alpha_jy_iy_j\,\boldsymbol x_i^{\mathsf T}\boldsymbol x_j\qquad\text{约束：}\ \alpha_i\ge0,\ \ \sum_i\alpha_iy_i=0.$$

1. 算出内积表 $\boldsymbol x_i^{\mathsf T}\boldsymbol x_j$，用等式约束消去一个变量，写出目标。
2. 在 $\alpha_i\ge0$ 的范围内求最大，再由 $\boldsymbol w=\sum\alpha_iy_i\boldsymbol x_i$ 得到 $\boldsymbol w$。

用到老朋友上：内积表为 $\boldsymbol x_1\cdot\boldsymbol x_1=18$，$\boldsymbol x_1\cdot\boldsymbol x_2=21$，$\boldsymbol x_2\cdot\boldsymbol x_2=25$，$\boldsymbol x_1\cdot\boldsymbol x_3=6$，$\boldsymbol x_2\cdot\boldsymbol x_3=7$，$\boldsymbol x_3\cdot\boldsymbol x_3=2$。等式约束 $\alpha_1+\alpha_2-\alpha_3=0$，消去 $\alpha_3=\alpha_1+\alpha_2$，此时

$$\boldsymbol w=\alpha_1\boldsymbol x_1+\alpha_2\boldsymbol x_2-\alpha_3\boldsymbol x_3=\alpha_1(2,2)^{\mathsf T}+\alpha_2(3,2)^{\mathsf T},$$

目标化为

$$D(\alpha_1,\alpha_2)=2\alpha_1+2\alpha_2-\tfrac12\lVert\boldsymbol w\rVert^2=2\alpha_1+2\alpha_2-4\alpha_1^2-10\alpha_1\alpha_2-6.5\alpha_2^2,\qquad\alpha_1,\alpha_2\ge0.$$

**例 5**　求 $D(a,b)=2a+2b-4a^2-10ab-6.5b^2$ 在 $a\ge0,\ b\ge0$ 上的最大值。

接例 2：这个函数就是老朋友的对偶目标（$a=\alpha_1$，$b=\alpha_2$）。例 2 里「两条约束取等号」只是猜测，求出这里的最大值，看它是否等于猜出的 $\tfrac14$。

第一步，内部驻点。令两个偏导为零：

$$2-8a-10b=0,\qquad 2-10a-13b=0 .$$

解得 $a=\tfrac32$，$b=-1$，违反 $b\ge0$。$D$ 是凹二次函数，$a,b$ 很大时趋于 $-\infty$，在允许范围内一定有最大点。最大点若在内部，必是驻点，而唯一的驻点不在允许范围内，所以最大值只能落在边界上。

第二步，边界 $a=0$。$D=2b-6.5b^2$，在 $b=\tfrac2{13}$ 处最大，值 $\tfrac2{13}\approx0.154$。

第三步，边界 $b=0$。$D=2a-4a^2$，在 $a=\tfrac14$ 处最大，值 $\tfrac14$。

第四步，比较：$\tfrac14>\tfrac2{13}$，角点 $(0,0)$ 处 $D=0$，所以最大值是 $\tfrac14$，在 $(a,b)=(\tfrac14,0)$。检查：该点 $\partial D/\partial b=2-\tfrac{10}4-0=-\tfrac12<0$，$b$ 往正方向走只会变小。

回到老朋友：$\boldsymbol\alpha=(\tfrac14,0,\tfrac14)$，$d^*=\tfrac14$，例 2 的猜测点可行，所以 $p^*\le\tfrac14$；弱对偶给出 $p^*\ge d^*=\tfrac14$，夹在一起 $p^*=\tfrac14$，那个猜测是对的。

> 正类点 $(2,0)$、负类点 $(-2,0)$，仿照上面两点的做法，对偶目标是 $d(\alpha)=2\alpha-8\alpha^2$。求它的最大值，并由 $\boldsymbol w=\sum\alpha_iy_i\boldsymbol x_i$ 写出 $\boldsymbol w$。
>
> 答案：配方 $-8(\alpha-\tfrac18)^2+\tfrac18$，$\alpha=\tfrac18$ 时最大，值 $\tfrac18$。$\boldsymbol w=\tfrac18(2,0)-\tfrac18(-2,0)=(\tfrac12,0)$，原问题目标 $\tfrac12\cdot\tfrac14=\tfrac18$，两者相等。

合上书，推出对偶函数，并说明弱对偶为什么成立。

算出来的 $\boldsymbol\alpha=(\tfrac14,0,\tfrac14)$ 里夹着一个 0，这个 0 说明了什么，是下一节的问题。

### 5. 分界线只由哪些点决定？

老朋友的结果里 $\alpha_2=0$。这不是巧合。本节仍是硬间隔，互补松弛（KKT 条件 4）说

$$\alpha_i\big[y_i(\boldsymbol w^{\mathsf T}\boldsymbol x_i+b)-1\big]=0.$$

所以 $\alpha_i>0$ 的点必须恰好落在间隔边界上，$y_i(\boldsymbol w^{\mathsf T}\boldsymbol x_i+b)=1$；严格在带外的点，$\alpha_i=0$。$\alpha_i>0$ 的点叫**支持向量**。由 $\boldsymbol w=\sum_i\alpha_iy_i\boldsymbol x_i$，$\alpha_i=0$ 的项全部消失，分界线只由支持向量决定。（反过来，落在边界上的点，乘子也可以是 0。）

**方法 5（由对偶解得到分类器，硬间隔）**

1. 求出 $\boldsymbol\alpha$，$\boldsymbol w=\sum_i\alpha_iy_i\boldsymbol x_i$。
2. 任取一个支持向量 $\boldsymbol x_s$（$\alpha_s>0$），由 $y_s(\boldsymbol w^{\mathsf T}\boldsymbol x_s+b)=1$ 得 $b=y_s-\boldsymbol w^{\mathsf T}\boldsymbol x_s$。
3. 预测：$f(\boldsymbol x)=\sum_i\alpha_iy_i\,\boldsymbol x_i^{\mathsf T}\boldsymbol x+b$，看符号。

**例 6**　设 $\boldsymbol p=(3,3)^{\mathsf T}$，$\boldsymbol q=(1,1)^{\mathsf T}$，$\boldsymbol w=\tfrac14\boldsymbol p-\tfrac14\boldsymbol q$。求使 $\boldsymbol w^{\mathsf T}\boldsymbol p+b=1$ 与 $\boldsymbol w^{\mathsf T}\boldsymbol q+b=-1$ 同时成立的 $b$，再求 $f(\boldsymbol x)=\boldsymbol w^{\mathsf T}\boldsymbol x+b$ 在 $(2,3)$ 处的值。

接例 5：$\boldsymbol p,\boldsymbol q$ 就是老朋友里的 $\boldsymbol x_1,\boldsymbol x_3$，系数 $\pm\tfrac14$ 是例 5 解出的 $\alpha_1,\alpha_3$（负类取负号）。

$\boldsymbol w=\tfrac14(3,3)^{\mathsf T}-\tfrac14(1,1)^{\mathsf T}=(\tfrac12,\tfrac12)^{\mathsf T}$。用 $\boldsymbol p$ 得 $b=1-(\tfrac32+\tfrac32)=-2$，用 $\boldsymbol q$ 验算 $b=-1-(\tfrac12+\tfrac12)=-2$，两个条件一致。$F(2,3)=\tfrac12\cdot2+\tfrac12\cdot3-2=\tfrac12$。

对分类的意义：这就是老朋友的硬间隔分类器，间隔 $1/\lVert\boldsymbol w\rVert=\sqrt2$，与第 1 节的猜测吻合，$(2,3)$ 判为正类。另一个正类点 $\boldsymbol x_2$ 的 $\boldsymbol w^{\mathsf T}\boldsymbol x_2+b=\tfrac32>1$，在带外，$\alpha_2=0$。删去 $\boldsymbol x_2$，或把它挪到仍满足 $\tfrac12x_1+\tfrac12x_2-2>1$ 的位置（正确一侧的带外），原来的参数仍然最优；$\boldsymbol x_1$ 或 $\boldsymbol x_3$ 一动，边界条件就被破坏，分界线通常要跟着变。

> 上一节随堂小题里的 $\boldsymbol w=(\tfrac12,0)^{\mathsf T}$ 来自 $(2,0)$ 与 $(-2,0)$，两个乘子都是 $\tfrac18$。求 $b$ 和 $(1,7)$ 处的 $F$。
>
> 答案：用 $(2,0)$：$\tfrac12\cdot2+b=1$，$b=0$；用 $(-2,0)$ 验算：$-1+b=-1$，一致。$f(1,7)=\tfrac12>0$，判为正类。

![直线 $x_1+x_2=4$ 是分界线，两条虚线是间隔边界，阴影为间隔带；带外圈的 $\boldsymbol x_1,\boldsymbol x_3$ 是支持向量，未加外圈的 $\boldsymbol x_2$ 在带外且 $\alpha_2=0$。实心点表示正类，空心点表示负类](fig/M6-n2.pdf){width=70%}

预测公式里只需保留乘子非零的样本，它们可能只占一部分，也可能包含全部样本，数量取决于数据和参数；而且数据只以内积 $\boldsymbol x_i^{\mathsf T}\boldsymbol x$ 的形式出现。

合上书，说明为什么 $\alpha_i=0$ 的点不影响分界线，并写出只用支持向量的预测公式。

这一切都建立在两类能被一条直线分开的前提上。只要有一个点位置不巧，硬间隔的约束就无解，下一节处理这种情形。

### 6. 数据有噪声、分不开时怎么办？

给老朋友添一个噪声点 $\boldsymbol x_4=(3.5,3)$，标签为负，它恰是 $\boldsymbol x_1,\boldsymbol x_2$ 连线的中点。一次函数在中点处取两端的平均值：$f(\boldsymbol x_4)=\tfrac12\big(f(\boldsymbol x_1)+f(\boldsymbol x_2)\big)$。若 $\boldsymbol x_1,\boldsymbol x_2$ 都分对，两端的值为正，平均值也为正，$\boldsymbol x_4$ 就得不到负的分数，所以硬间隔的约束无解。

#### 允许越界，代价怎样算？

办法是允许点越界，但要付代价。给每个点一个松弛量 $\xi_i\ge0$，约束放宽成 $y_i(\boldsymbol w^{\mathsf T}\boldsymbol x_i+b)\ge1-\xi_i$，并把总的越界量加进目标：

$$\min\ \tfrac12\lVert\boldsymbol w\rVert^2+C\sum_i\xi_i .$$

$C>0$ 是自己选的超参数。固定 $(\boldsymbol w,b)$，$\xi_i$ 只要满足 $\xi_i\ge1-y_if(\boldsymbol x_i)$ 和 $\xi_i\ge0$，而目标随 $\xi_i$ 增大，所以最优的 $\xi_i$ 取这两个下界里较大的那个：

$$\xi_i=\max\big(0,\ 1-y_i f(\boldsymbol x_i)\big),\qquad f(\boldsymbol x)=\boldsymbol w^{\mathsf T}\boldsymbol x+b .$$

记 $z=yf(\boldsymbol x)$，$\max(0,1-z)$ 叫**合页损失**。于是软间隔 SVM 等价于最小化 $\tfrac12\lVert\boldsymbol w\rVert^2+C\sum\max(0,1-y_if(\boldsymbol x_i))$。把目标除以正数 $C$（最优点不变），就是合页损失之和加上 $\boldsymbol w$ 的 L2 惩罚（M.3）：

$$\sum_i\max(0,1-y_if(\boldsymbol x_i))+\frac1{2C}\lVert\boldsymbol w\rVert^2 .$$

$C$ 越大，同样的越界量付出的代价越大。若数据本来可分，存在一组硬间隔乘子都不超过 $C$ 时，软间隔的最优解就与硬间隔解一致（硬间隔解的 $\xi_i$ 全为 0，乘子又不超过 $C$，满足本节后面写出的全部条件）；若数据不可分（比如这里），增大 $C$ 也不能消除全部越界。$C$ 越小，上式里 $\boldsymbol w$ 的惩罚系数 $\frac1{2C}$ 越大，相当于 M.3 里正则越强。

#### 合页损失和逻辑回归的损失差在哪里？

要和 M.2.4 的交叉熵对比，先把标签换成 $\pm1$。逻辑回归给出 $p=1/(1+e^{-f})$。标签为 $+1$ 时交叉熵是 $-\ln p=\ln(1+e^{-f})$；标签为 $-1$ 时是 $-\ln(1-p)=\ln(1+e^{f})$。两种写成一个式子，就是 $\ln(1+e^{-yf})=\ln(1+e^{-z})$：

| $z=yf$ | $-1$ | $0$ | $1$ | $2$ |
|---|---|---|---|---|
| 合页损失 | 2 | 1 | 0 | 0 |
| 逻辑损失 | 1.3133 | 0.6931 | 0.3133 | 0.1269 |

$z>1$ 时合页损失在这个点附近恒为 0，在最优解处这类点的乘子为 0；$z=1$ 时损失虽然也是 0，却位于折点，不能由此断定乘子为 0。逻辑损失永不为零，每个点始终对参数有一份拉力。逻辑回归先用 M.2 的模型把得分转成概率，再用交叉熵衡量预测；本章的 SVM 直接输出得分和类别，不直接把得分解释为概率。

**例 7**　取 $C=1$，比较两条直线对四个点的目标值。

数据沿用例 2 的三个点，再加上本节开头的噪声点 $\boldsymbol x_4$。例 2 的直线 A 现在会让 $\boldsymbol x_4$ 越界，所以改用软间隔的目标 $\tfrac12\lVert\boldsymbol w\rVert^2+C\sum\xi_i$，比较 A 和另一条直线 B。

两条直线对四个点的得分、$z=yf$ 与松弛量如下（标签 $+,+,-,-$）：

| 直线 | 四个点的 $f$ | 四个点的 $z=yf$ | $\xi=\max(0,1-z)$ |
|---|---|---|---|
| A：$\boldsymbol w=(\tfrac12,\tfrac12)^{\mathsf T}$，$b=-2$ | $1,\ \tfrac32,\ -1,\ \tfrac54$ | $1,\ \tfrac32,\ 1,\ -\tfrac54$ | $0,\ 0,\ 0,\ \tfrac94$ |
| B：$\boldsymbol w=(\tfrac4{13},\tfrac7{13})^{\mathsf T}$，$b=-\tfrac{24}{13}$ | $\tfrac9{13},\ 1,\ -1,\ \tfrac{11}{13}$ | $\tfrac9{13},\ 1,\ 1,\ -\tfrac{11}{13}$ | $\tfrac4{13},\ 0,\ 0,\ \tfrac{24}{13}$ |

A 就是硬间隔解，只有 $\boldsymbol x_4$ 越界，目标值 $\tfrac14+\tfrac94=2.5$。B 的目标值

$$\tfrac12\cdot\tfrac{65}{169}+\tfrac{28}{13}=\tfrac{793}{338}\approx2.346<2.5 .$$

B 比 A 好：它让 $\boldsymbol x_1$ 退进间隔带（仍分对），换来 $\boldsymbol x_4$ 少越界一些。$\boldsymbol x_4$ 仍被判成正类，错判是这个模型付的代价。

#### B 为什么是最优解？

B 是全局最优，因为对偶给出了证书。先写完整的拉格朗日函数，四组量是 $\boldsymbol w,b,\xi_i$ 和乘子 $\alpha_i,\mu_i\ge0$：

$$L=\tfrac12\lVert\boldsymbol w\rVert^2+C\sum_i\xi_i-\sum_i\alpha_i\big[y_if(\boldsymbol x_i)-1+\xi_i\big]-\sum_i\mu_i\xi_i .$$

对 $\xi_i$ 求偏导得 $C-\alpha_i-\mu_i=0$，所以 $0\le\alpha_i\le C$；对 $\boldsymbol w,b$ 的结果和硬间隔相同。互补松弛给出

$$\alpha_i\big(y_if(\boldsymbol x_i)-1+\xi_i\big)=0,\qquad(C-\alpha_i)\xi_i=0 .$$

由此分三种情形。$\alpha_i=0$ 时，由 $(C-\alpha_i)\xi_i=0$ 且 $C>0$ 得 $\xi_i=0$，再由约束 $z\ge1-\xi_i$ 得 $z\ge1$，点在边界上或正确一侧的带外。$0<\alpha_i<C$ 时，同一式得 $\xi_i=0$，再由 $\alpha_i(z-1+\xi_i)=0$ 且 $\alpha_i>0$ 得 $z=1$，恰在边界上。$\alpha_i=C$ 时，由前一式得 $z=1-\xi_i\le1$，在带内、越界，或恰在边界上。

软间隔的对偶问题和方法 4 相同：把 $\boldsymbol w=\sum\alpha_iy_i\boldsymbol x_i$、$\sum\alpha_iy_i=0$、$\mu_i=C-\alpha_i$ 代回，$\xi$ 项消失，得到同一个对偶目标，只把 $\alpha_i\ge0$ 换成 $0\le\alpha_i\le C$。B 是这样得到的：按三种情形的结论，越界的 $\boldsymbol x_1,\boldsymbol x_4$ 取 $\alpha=C=1$，恰在边界上的 $\boldsymbol x_2,\boldsymbol x_3$ 取 $0<\alpha<1$。这时 $\sum\alpha_iy_i=0$ 给出 $\alpha_2=\alpha_3=t$，于是

$$\boldsymbol w=\sum\alpha_iy_i\boldsymbol x_i=(3,3)+t(4,3)-t(1,1)-(3.5,3)=(3t-\tfrac12,\ 2t).$$

$\boldsymbol x_2,\boldsymbol x_3$ 在边界上，即 $4w_1+3w_2+b=1$ 与 $w_1+w_2+b=-1$，相减得 $3w_1+2w_2=2$，也就是 $13t-\tfrac32=2$，$t=\tfrac7{26}$。由此 $\boldsymbol w=(\tfrac4{13},\tfrac7{13})^{\mathsf T}$，$b=-1-w_1-w_2=-\tfrac{24}{13}$，正是 B。

再验证 $\boldsymbol\alpha=(1,\tfrac7{26},\tfrac7{26},1)$ 满足全部条件：每个乘子都在 $[0,1]$，$\sum\alpha_iy_i=1+\tfrac7{26}-\tfrac7{26}-1=0$，互补松弛成立（$\boldsymbol x_2,\boldsymbol x_3$ 在边界上，$\boldsymbol x_1,\boldsymbol x_4$ 的乘子等于 $C$）。对偶目标

$$\sum_i\alpha_i-\tfrac12\lVert\boldsymbol w\rVert^2=\tfrac{33}{13}-\tfrac5{26}=\tfrac{61}{26},$$

恰等于 B 的原目标 $\tfrac{793}{338}=\tfrac{61}{26}$。对偶给出下界，B 又实际达到它，所以 B 是最优解。

软间隔下求 $b$ 要选 $0<\alpha_s<C$ 的点，才能直接用 $b=y_s-\boldsymbol w^{\mathsf T}\boldsymbol x_s$；若没有这样的点，要把已知的 $\boldsymbol w$ 代回上面的得分不等式，求出 $b$ 的允许范围，不能套用硬间隔的等号。

![合页损失（实线）与逻辑损失（虚线）随 $z=yf$ 的变化：合页损失在 $z\ge1$ 处恒为 0，逻辑损失只是越来越小](fig/M6-n3.pdf){width=60%}

合上书，写出软间隔的目标函数，并说明 $\alpha_i=0$、$0<\alpha_i<C$、$\alpha_i=C$ 各对应点在哪里。

软间隔处理了噪声，分界线却仍是一条直线。如果两类点本身就按弯曲的方式排布，比如下一节的异或，无论怎样放宽，直线总有点会分错，需要换一种看法。

### 7. 弯曲的分界线，怎样用线性方法得到？

先看直线分不开的数据，异或：$(1,1),(-1,-1)$ 为正类，$(1,-1),(-1,1)$ 为负类。不存在把这两类完全分开的直线：若 $f(\boldsymbol x)=\boldsymbol w^{\mathsf T}\boldsymbol x+b$，一对相反点的函数值之和都是 $2b$，两个正点要求 $2b>0$，两个负点要求 $2b<0$，相互矛盾。

换一个看法。给每个点配三个新坐标 $\boldsymbol\varphi(\boldsymbol x)=(x_1^2,\ \sqrt2x_1x_2,\ x_2^2)$，$\varphi_2=\sqrt2x_1x_2$ 是第二个新坐标。四个点的新坐标是 $(1,\pm\sqrt2,1)$，正类的第二个坐标是 $+\sqrt2$，负类是 $-\sqrt2$，一个平面 $\varphi_2=0$ 就能分开。在原来的平面上，这个平面对应的分界线是 $x_1x_2=0$，也就是两条坐标轴的并集，它不再是一条直线，所以是非线性的分类边界。

![异或在平面上没有直线可分（左）；换成第二个新坐标 $\sqrt2x_1x_2$ 以后，两类分居 $\pm\sqrt2$（右）。左图的阴影是 $x_1x_2>0$ 的区域（实心圆所在），两条粗实线（坐标轴）就是右图平面 $\varphi_2=0$（图中画成一条竖线）在原平面里的样子](fig/M6-n4.pdf){width=90%}

#### 核技巧：为什么可以直接换掉内积？

按这个思路要先造新坐标再做线性 SVM。但对偶问题和预测公式里数据只以内积出现，所以只需要新坐标之间的内积 $K(\boldsymbol x,\boldsymbol x')=\boldsymbol\varphi(\boldsymbol x)^{\mathsf T}\boldsymbol\varphi(\boldsymbol x')$，把所有 $\boldsymbol x_i^{\mathsf T}\boldsymbol x_j$ 换成 $K(\boldsymbol x_i,\boldsymbol x_j)$，连 $\boldsymbol\varphi$ 都不用算。这就是**核技巧**，$K$ 叫**核函数**。

上面这个 $\boldsymbol\varphi$ 的内积是

$$\boldsymbol\varphi(\boldsymbol x)^{\mathsf T}\boldsymbol\varphi(\boldsymbol x')=x_1^2(x_1')^2+2x_1x_2x_1'x_2'+x_2^2(x_2')^2=(x_1x_1'+x_2x_2')^2=(\boldsymbol x^{\mathsf T}\boldsymbol x')^2 .$$

**方法 6（核化）**

1. 选核函数 $K$，对偶目标里的 $\boldsymbol x_i^{\mathsf T}\boldsymbol x_j$ 换成 $K(\boldsymbol x_i,\boldsymbol x_j)$。
2. 同样解出 $\boldsymbol\alpha$、$b$。
3. 预测 $f(\boldsymbol x)=\sum_i\alpha_iy_iK(\boldsymbol x_i,\boldsymbol x)+b$。

**例 8**　设 $\boldsymbol\varphi(\boldsymbol x)=(x_1^2,\ \sqrt2x_1x_2,\ x_2^2)^{\mathsf T}$，四个点按顺序记 $\boldsymbol u_1=(1,1)$，$\boldsymbol u_2=(-1,-1)$，$\boldsymbol u_3=(1,-1)$，$\boldsymbol u_4=(-1,1)$（这里的 $\boldsymbol u_i$ 与老朋友的 $\boldsymbol x_i$ 无关）。求核矩阵 $K_{ij}=\boldsymbol\varphi(\boldsymbol u_i)^{\mathsf T}\boldsymbol\varphi(\boldsymbol u_j)$，并说明它半正定。

例 5 的对偶目标里用的是内积表 $\boldsymbol x_i^{\mathsf T}\boldsymbol x_j$。这一道把数据换成异或的四个点，内积换成核，先算核矩阵，再用它写出对偶目标。

用 $K=(\boldsymbol u_i^{\mathsf T}\boldsymbol u_j)^2$：$\boldsymbol u_1\cdot\boldsymbol u_2=-2$，平方得 4；$\boldsymbol u_1\cdot\boldsymbol u_3=0$，得 0；$\boldsymbol u_3\cdot\boldsymbol u_4=-2$，得 4；对角线上 $\boldsymbol u_i\cdot\boldsymbol u_i=2$，平方得 4。于是

$$K=\begin{pmatrix}4&4&0&0\\4&4&0&0\\0&0&4&4\\0&0&4&4\end{pmatrix}.$$

半正定的依据：对任意 $\boldsymbol c\in\mathbb R^4$，$\boldsymbol c^{\mathsf T}K\boldsymbol c=\sum_{i,j}c_ic_j\boldsymbol\varphi(\boldsymbol u_i)^{\mathsf T}\boldsymbol\varphi(\boldsymbol u_j)=\big\lVert\sum_ic_i\boldsymbol\varphi(\boldsymbol u_i)\big\rVert^2\ge0$。这段推导没有用到 $\boldsymbol\varphi$ 的具体形式，所以凡是能写成内积的核，核矩阵都是半正定的。这个条件不能丢：$K(\boldsymbol x,\boldsymbol x')=-\boldsymbol x^{\mathsf T}\boldsymbol x'$ 在 $\boldsymbol x\ne\boldsymbol0$ 时 $K(\boldsymbol x,\boldsymbol x)<0$，而任何内积都有 $\boldsymbol\varphi(\boldsymbol x)^{\mathsf T}\boldsymbol\varphi(\boldsymbol x)\ge0$，所以它不是任何新坐标的内积，不能当核用。

> 用 $K=(\boldsymbol x^{\mathsf T}\boldsymbol x')^2$ 算 $K((2,1),(1,3))$，并用 $\boldsymbol\varphi$ 验证。
>
> 答案：$(2+3)^2=25$；$\boldsymbol\varphi(2,1)=(4,2\sqrt2,1)$，$\boldsymbol\varphi(1,3)=(1,3\sqrt2,9)$，内积 $4+12+9=25$。

#### 核矩阵有了，异或怎样真的分开？

把它用到异或的分类：设 $\alpha_1+\alpha_2=s$，等式约束给出 $\alpha_3+\alpha_4=s$，把核矩阵和 $y=(+,+,-,-)$ 代入：$\sum\alpha_i=2s$，$\sum_{i,j}\alpha_i\alpha_jy_iy_jK_{ij}=4(\alpha_1+\alpha_2)^2+4(\alpha_3+\alpha_4)^2=8s^2$（不同类的核值为 0，同类的为 4），所以对偶目标是 $2s-\tfrac12\cdot8s^2=2s-4s^2$，$s=\tfrac14$ 时最大。因为 $\boldsymbol\varphi(\boldsymbol u_1)=\boldsymbol\varphi(\boldsymbol u_2)$、$\boldsymbol\varphi(\boldsymbol u_3)=\boldsymbol\varphi(\boldsymbol u_4)$，只有 $\alpha_1+\alpha_2$ 与 $\alpha_3+\alpha_4$ 影响结果，取四个 $\alpha_i=\tfrac18$，预测函数

$$f(\boldsymbol x)=\tfrac18\big[(x_1+x_2)^2+(x_1+x_2)^2-(x_1-x_2)^2-(x_1-x_2)^2\big]+b=x_1x_2+b,$$

在正类支持点 $(1,1)$ 处 $f=1+b=1$，所以 $b=0$。分类函数是 $f(\boldsymbol x)=x_1x_2$，四个点的 $f$ 是 $1,1,-1,-1$，都在间隔边界上。

#### 还有哪些常用的核？

常用的另一个核是高斯核 $K=\exp\!\big(-\lVert\boldsymbol x-\boldsymbol x'\rVert^2/(2\sigma^2)\big)$，其中 $\sigma>0$ 是控制核值随距离下降快慢的参数，$\sigma$ 越大下降越慢。它的新坐标有无穷多个：把 $e^{\boldsymbol x^{\mathsf T}\boldsymbol x'/\sigma^2}$ 按 $e^t=\sum_{k}t^k/k!$ 展开，就是各次多项式核 $(\boldsymbol x^{\mathsf T}\boldsymbol x')^k$ 的加权和，再乘上只与 $\boldsymbol x$、$\boldsymbol x'$ 各自有关的因子。上面的展开已经说明这样的新坐标存在，本章只需要这个事实。

核技巧的代价落在样本数上：保存全部核值要 $n\times n$ 个数，样本很多时成本很高。M.7 从同一个异或问题出发，看多层网络怎样自己从数据里学出新坐标。

回到开头的问题：样本少、特征多，分界线画在哪里？本章的回答是，在所有能分对的分界线里取间隔最大的（第 1、2 节）。求它要解对偶问题，变量个数只有样本数 $n$，与特征数无关，而且分界线只由支持向量决定（第 4、5 节）。老朋友的三个点给出分界线 $x_1+x_2=4$，间隔 $\sqrt2$。加上噪声点 $\boldsymbol x_4$ 以后，用软间隔求得的最优直线是 B，目标值 $\tfrac{61}{26}$（第 6 节）。两类按弯曲方式排布时用核，异或得到 $f=x_1x_2$（第 7 节）。

合上书，写出 SVM 对偶问题，并说明：为什么只有支持向量对分界线有影响，核函数又是在哪一步替换进去的。

### 本章小结

| 方法 | 什么时候用 | 对应题号 |
|---|---|---|
| 方法 1（求间隔） | 点到直线的距离；比较分界线 | M6-01、M6-07 |
| 方法 2（硬间隔原问题） | 把「间隔最大」写成优化问题；例 2 | — |
| 方法 3（KKT 条件） | 不等式约束的最优化；讨论起作用与不起作用 | M6-02、M6-03、M6-07 |
| 方法 4（对偶问题） | 化成只含 $\alpha$ 的问题 | M6-04、M6-05 |
| 方法 5（对偶解到分类器） | 由 $\alpha$ 求 $\boldsymbol w,b$，辨认支持向量 | M6-05 |
| 方法 6（核化） | 数据线性不可分；用核替换内积 | M6-06 |

在全书的主线上，本章没有新增模型，而是换了一种求参数的办法：得分仍是 $\boldsymbol w^{\mathsf T}\boldsymbol x+b$（第 7 节在新坐标里仍是线性得分），损失换成合页损失加 L2 惩罚，参数由对偶问题解出，不走梯度下降。逐章长大的「损失 ⇐ 概率假设」表本章不新增行：合页损失不是从伯努利似然推出来的，SVM 的得分也不直接表示概率（对照 M.2 的交叉熵）。这些乘子方法还会在 M.15 的带约束优化中出现。
