## L.2 · 点积、长度、夹角与投影

搜索引擎和推荐系统每天都在回答同一个问题：两样东西像不像。早期的文献检索只按关键词做「是或否」的匹配，排不出相关程度。20 世纪 60—70 年代，萨尔顿和合作者在 SMART 检索系统上逐步换了做法：把文档和查询都写成向量（最简单的是记每个词出现几次），按两个向量夹角的余弦排序，余弦越接近 1，内容越相关，这就是向量空间模型。今天的检索和推荐系统里，余弦相似度仍是常用的一种度量。

可是几千维的向量画不出来，「夹角」从哪里来？办法是反过来，用算式定义夹角的余弦，这要求算出的数落在 $-1$ 到 1 之间。保证这一点的不等式由柯西 1821 年在《分析教程》里证明，后来布尼亚科夫斯基和施瓦茨给出积分形式，所以叫柯西–施瓦茨不等式。

本章先定义点积（第 1 节），再用它定义 $n$ 维的长度与夹角（第 2 节），然后讲投影（第 3 节）和线性方程的解集（第 4 节），最后用余弦相似度找口味相近的用户（第 5 节）。

### 1. 两个向量有多像？

推荐网站想用一个数说出两位用户的口味有多像。L.1 的加法和数乘只会得出向量，需要一种新的运算。

先看简化版：每部电影只记喜欢 $+1$、不喜欢 $-1$、没看 $0$。两位用户甲、乙记作 $(1,1,-1,0)^{\mathsf T}$、$(1,0,-1,-1)^{\mathsf T}$（$^{\mathsf T}$ 是 L.1 的转置）。逐部电影把两人的数相乘：意见一致得 $+1$，相反得 $-1$，有人没看得 0。再加起来，

$$1\cdot1+1\cdot0+(-1)(-1)+0\cdot(-1)=2,$$

正是「意见一致的部数减去意见相反的部数」。

一般地，两个 $n$ 维向量的**点积**（也叫内积）是

$$\boldsymbol a\cdot\boldsymbol b=a_1b_1+a_2b_2+\cdots+a_nb_n .$$

结果是一个数，不是向量；两个向量必须同维。

点积也写成 $\boldsymbol a^{\mathsf T}\boldsymbol b$。这里规定：行向量乘列向量，就是对应位置相乘再相加。例如行 $(1,2)$ 乘列 $(3,4)^{\mathsf T}$，行里第 1 个数配列里第 1 个数，第 2 个配第 2 个，得 $1\cdot3+2\cdot4=11$。

可以把点积想成逐个位置投票：同号赞成，异号反对，票的分量是两数之积。这个比喻有一处会误导人：分量整体放大，票也跟着变重，例 1 就会碰到。

**例 1**　设 $\boldsymbol u=(5,4,1,2)^{\mathsf T}$，$\boldsymbol v=(4,5,2,1)^{\mathsf T}$，$\boldsymbol w=(1,2,5,4)^{\mathsf T}$，求 $\boldsymbol u\cdot\boldsymbol v$、$\boldsymbol u\cdot\boldsymbol w$ 和 $\boldsymbol u\cdot(2\boldsymbol v)$。

逐个位置相乘再相加：

$$\boldsymbol u\cdot\boldsymbol v=5\cdot4+4\cdot5+1\cdot2+2\cdot1=44,$$

$$\boldsymbol u\cdot\boldsymbol w=5\cdot1+4\cdot2+1\cdot5+2\cdot4=26.$$

三个向量的分量平方和都是 46，长短相同，可以直接比点积：$\boldsymbol v$ 比 $\boldsymbol w$ 更像 $\boldsymbol u$。再算 $\boldsymbol u\cdot(2\boldsymbol v)=88$，翻了一倍，可 $2\boldsymbol v$ 和 $\boldsymbol v$ 方向完全相同。点积会被长度带着走，这个毛病留给第 2 节解决。

> 求 $\boldsymbol v\cdot\boldsymbol w$。比较 $\boldsymbol w$ 与 $\boldsymbol u$、$\boldsymbol v$ 的点积，哪个更大？
>
> 答案：$\boldsymbol v\cdot\boldsymbol w=4+10+10+4=28>26=\boldsymbol u\cdot\boldsymbol w$，与 $\boldsymbol v$ 的点积更大。

#### 运算律和两个不能搬的习惯

点积的每一项 $a_ib_i$ 都是实数乘法，实数的交换律、分配律逐项照搬，所以

$$\boldsymbol a\cdot\boldsymbol b=\boldsymbol b\cdot\boldsymbol a,\qquad \boldsymbol a\cdot(\boldsymbol b+\boldsymbol c)=\boldsymbol a\cdot\boldsymbol b+\boldsymbol a\cdot\boldsymbol c,\qquad (k\boldsymbol a)\cdot\boldsymbol b=k(\boldsymbol a\cdot\boldsymbol b).$$

此外 $\boldsymbol a\cdot\boldsymbol a=a_1^2+\cdots+a_n^2\ge0$，只有 $\boldsymbol a=\boldsymbol 0$ 时等于 0。含点积的式子于是可以像多项式一样展开。

但点积的结果是数，实数的两个习惯不能搬过来。

第一个是结合律。$(\boldsymbol a\cdot\boldsymbol b)\boldsymbol c$ 是 $\boldsymbol c$ 的倍数，$\boldsymbol a(\boldsymbol b\cdot\boldsymbol c)$ 是 $\boldsymbol a$ 的倍数，一般不相等，所以 $\boldsymbol a\cdot\boldsymbol b\cdot\boldsymbol c$ 这种写法有歧义。

第二个是约分。$(1,0)\cdot(0,1)=(1,0)\cdot(0,5)=0$，可 $(0,1)\ne(0,5)$。可见 $\boldsymbol a\cdot\boldsymbol b=\boldsymbol a\cdot\boldsymbol c$ 不能约去 $\boldsymbol a$，它只说明 $\boldsymbol a\cdot(\boldsymbol b-\boldsymbol c)=0$。

**方法 1（算点积）**

1. 有分量时，逐个位置相乘再相加。
2. 没有分量、只给出几个点积时，按运算律展开，化成已知的点积。

**例 2**　已知 $\boldsymbol a\cdot\boldsymbol a=4$，$\boldsymbol b\cdot\boldsymbol b=9$，$\boldsymbol a\cdot\boldsymbol b=-1$，求 $(2\boldsymbol a-\boldsymbol b)\cdot(\boldsymbol a+3\boldsymbol b)$。

和例 1 不同，这里没有分量，只能展开。按分配律逐项相乘，

$$(2\boldsymbol a-\boldsymbol b)\cdot(\boldsymbol a+3\boldsymbol b)=2\,\boldsymbol a\cdot\boldsymbol a+6\,\boldsymbol a\cdot\boldsymbol b-\boldsymbol b\cdot\boldsymbol a-3\,\boldsymbol b\cdot\boldsymbol b.$$

由交换律 $\boldsymbol b\cdot\boldsymbol a=\boldsymbol a\cdot\boldsymbol b=-1$，代入已知的三个点积：

$$2\cdot4+6\cdot(-1)-(-1)-3\cdot9=-24.$$

#### 二维、三维里的几何意义

先说长度。由勾股定理，平面向量 $(a_1,a_2)^{\mathsf T}$ 的长度是 $\sqrt{a_1^2+a_2^2}$；空间向量再多用一次勾股定理，是 $\sqrt{a_1^2+a_2^2+a_3^2}$。

长度记作 $\lVert\boldsymbol a\rVert$，它就是高中课本里的 $|\boldsymbol a|$。用双竖线，是为了和数的绝对值 $|x|$ 分开，考研数学和 AI 论文都这样写。对照点积的定义，

$$\boldsymbol a\cdot\boldsymbol a=\lVert\boldsymbol a\rVert^2.$$

再看夹角。把 $\boldsymbol a,\boldsymbol b$ 从原点画出。不共线时，两个终点和原点构成三角形，三边长是 $\lVert\boldsymbol a\rVert$、$\lVert\boldsymbol b\rVert$、$\lVert\boldsymbol a-\boldsymbol b\rVert$，原点处的角是 $\theta$。共线时是退化的三角形，下面的算式照样成立。思路是把第三边长的平方算两遍。

第一遍用余弦定理：

$$\lVert\boldsymbol a-\boldsymbol b\rVert^2=\lVert\boldsymbol a\rVert^2+\lVert\boldsymbol b\rVert^2-2\lVert\boldsymbol a\rVert\lVert\boldsymbol b\rVert\cos\theta.$$

第二遍用点积。先按分配律逐项展开，再由交换律 $\boldsymbol b\cdot\boldsymbol a=\boldsymbol a\cdot\boldsymbol b$ 合并两个交叉项：

$$\lVert\boldsymbol a-\boldsymbol b\rVert^2=(\boldsymbol a-\boldsymbol b)\cdot(\boldsymbol a-\boldsymbol b)=\boldsymbol a\cdot\boldsymbol a-\boldsymbol a\cdot\boldsymbol b-\boldsymbol b\cdot\boldsymbol a+\boldsymbol b\cdot\boldsymbol b=\lVert\boldsymbol a\rVert^2-2\,\boldsymbol a\cdot\boldsymbol b+\lVert\boldsymbol b\rVert^2.$$

两式相等，消去两边相同的 $\lVert\boldsymbol a\rVert^2+\lVert\boldsymbol b\rVert^2$，再同除以 $-2$：

$$\boldsymbol a\cdot\boldsymbol b=\lVert\boldsymbol a\rVert\lVert\boldsymbol b\rVert\cos\theta .$$

![三边是 $\boldsymbol a$、$\boldsymbol b$、$\boldsymbol a-\boldsymbol b$ 的三角形（共线时退化）：第三边长的平方算两遍，两式相等就得到点积公式](fig/LA1-3.pdf){width=70%}

这里默认 $\boldsymbol a,\boldsymbol b$ 都是非零向量，零向量没有夹角。非零向量的长度为正，所以点积的符号就是 $\cos\theta$ 的符号：点积为 0 是直角；点积为正时 $0\le\theta<\frac{\pi}{2}$，再排除同向（$\theta=0$）才是锐角；点积为负时 $\frac{\pi}{2}<\theta\le\pi$，再排除反向（$\theta=\pi$）才是钝角。

L.1 例 5 里注意力的权重，第一步就是这样用点积打分：向量长短相近时，方向越一致，分数越高（M.11）。

合上书，用余弦定理重新推一遍点积公式，说清楚哪一步用了点积的运算律。

### 2. 维数高到画不出图时，长度和夹角怎么定义？

例 1 里 $\boldsymbol v$ 换成 $2\boldsymbol v$，方向没变，点积却翻倍。二维、三维里的补救办法是除以两个长度，得到 $\cos\theta$：向量伸长时点积和长度同比例变大，比值不变。

四维向量画不出来，长度和夹角都还没有定义。办法是把上一节的两个结论反过来当定义。

#### 长度

对 $n$ 维向量，定义

$$\lVert\boldsymbol a\rVert=\sqrt{\boldsymbol a\cdot\boldsymbol a}=\sqrt{a_1^2+\cdots+a_n^2}.$$

由定义，$\lVert k\boldsymbol a\rVert=\sqrt{k^2\,\boldsymbol a\cdot\boldsymbol a}=|k|\,\lVert\boldsymbol a\rVert$。长度为 1 的向量叫**单位向量**；非零向量除以自己的长度，就得到同方向的单位向量，叫单位化。两点的距离是 $\lVert\boldsymbol a-\boldsymbol b\rVert$。

上一节的展开现在写成

$$\lVert\boldsymbol a\pm\boldsymbol b\rVert^2=\lVert\boldsymbol a\rVert^2\pm2\,\boldsymbol a\cdot\boldsymbol b+\lVert\boldsymbol b\rVert^2 .$$

#### 定义夹角之前要过的一关

自然的想法是定义

$$\cos\theta=\frac{\boldsymbol a\cdot\boldsymbol b}{\lVert\boldsymbol a\rVert\lVert\boldsymbol b\rVert}.$$

但这个比值必须落在 $[-1,1]$ 里，才配叫余弦。这件事不能用「$|\cos\theta|\le1$」来证，因为 $n$ 维的 $\theta$ 正是要用这个比值来定义的，那样就绕成了圈。

**柯西–施瓦茨不等式**　对任意 $\boldsymbol a,\boldsymbol b\in\mathbb R^n$，

$$|\boldsymbol a\cdot\boldsymbol b|\le\lVert\boldsymbol a\rVert\lVert\boldsymbol b\rVert,$$

等号成立当且仅当 $\boldsymbol a,\boldsymbol b$ 共线（L.1.3）。

#### 柯西–施瓦茨不等式的证明

思路：手头唯一靠得住的不等式是「长度的平方不小于 0」。要让交叉项 $\boldsymbol a\cdot\boldsymbol b$ 出现，得把 $\boldsymbol a$、$\boldsymbol b$ 加起来再平方；在 $\boldsymbol b$ 前放一个可调的倍数 $t$，就得到对每个 $t$ 都成立的一族不等式。所以看

$$f(t)=\lVert\boldsymbol a+t\boldsymbol b\rVert^2=\lVert\boldsymbol b\rVert^2t^2+2(\boldsymbol a\cdot\boldsymbol b)t+\lVert\boldsymbol a\rVert^2 .$$

先在具体向量上走一遍。取 $\boldsymbol a=(1,2)^{\mathsf T}$、$\boldsymbol b=(3,1)^{\mathsf T}$，则

$$f(t)=(1+3t)^2+(2+t)^2=10t^2+10t+5\ge0 .$$

开口向上又不小于 0，判别式就不能为正：$10^2-4\cdot10\cdot5\le0$。三个系数正是 $\lVert\boldsymbol b\rVert^2$、$2\,\boldsymbol a\cdot\boldsymbol b$、$\lVert\boldsymbol a\rVert^2$，这就是 $(\boldsymbol a\cdot\boldsymbol b)^2=25\le5\times10$。

一般情形完全照搬，分五步：

1. $\boldsymbol b=\boldsymbol 0$ 时两边都是 0，不等式成立。下面设 $\boldsymbol b\ne\boldsymbol 0$，于是二次项系数 $\lVert\boldsymbol b\rVert^2>0$。
2. 对一切实数 $t$，$f(t)\ge0$，因为它是长度的平方。
3. 判别式不大于 0。理由：若有两个不同的根 $r_1<r_2$，则 $f(t)=\lVert\boldsymbol b\rVert^2(t-r_1)(t-r_2)$，取 $r_1<t<r_2$ 时它是负数，与第 2 步矛盾。
4. 写出判别式：$4(\boldsymbol a\cdot\boldsymbol b)^2-4\lVert\boldsymbol a\rVert^2\lVert\boldsymbol b\rVert^2\le0$，移项开方，得 $|\boldsymbol a\cdot\boldsymbol b|\le\lVert\boldsymbol a\rVert\lVert\boldsymbol b\rVert$。
5. 等号成立，即判别式为 0，即有某个 $t_0$ 使 $f(t_0)=0$。长度为 0 的只有零向量，所以 $\boldsymbol a+t_0\boldsymbol b=\boldsymbol 0$，两向量共线。反过来，$\boldsymbol a=k\boldsymbol b$ 时两边都等于 $|k|\lVert\boldsymbol b\rVert^2$。

![$f(t)$ 开口向上且不小于 0，最多碰 $t$ 轴一次；只有共线时（与 $t$ 轴相切的那条）才碰到，对应等号](fig/LA1-5.pdf){width=62%}

有了柯西–施瓦茨，对非零向量 $\boldsymbol a,\boldsymbol b$，就用前面那个比值定义它们的**夹角** $\theta\in[0,\pi]$。余弦在 $[0,\pi]$ 上严格递减，取遍 $[-1,1]$，所以这样的 $\theta$ 存在且唯一。零向量没有夹角，因为分母为 0。

从这里开始，$n$ 维的长度和夹角只按这两个公式算，不再依赖画图。

#### 三角不等式

柯西–施瓦茨还推出三角不等式：

$$\lVert\boldsymbol a+\boldsymbol b\rVert\le\lVert\boldsymbol a\rVert+\lVert\boldsymbol b\rVert .$$

两边都非负，比较平方即可。左边平方是 $\lVert\boldsymbol a\rVert^2+2\,\boldsymbol a\cdot\boldsymbol b+\lVert\boldsymbol b\rVert^2$，右边平方是 $\lVert\boldsymbol a\rVert^2+2\lVert\boldsymbol a\rVert\lVert\boldsymbol b\rVert+\lVert\boldsymbol b\rVert^2$，只差中间一项；柯西–施瓦茨说 $\boldsymbol a\cdot\boldsymbol b\le\lVert\boldsymbol a\rVert\lVert\boldsymbol b\rVert$，所以左边不超过右边。等号要求中间两项相等，即两者同向：其中一个是另一个的非负倍数。

**方法 2（求长度和夹角）**

1. 有分量时，算出点积和两个长度，代公式。
2. 没有分量时，先求长度的平方，用 $\lVert\boldsymbol a\pm\boldsymbol b\rVert^2$ 的展开式化成已知量，最后再开方。

**例 3**　$\boldsymbol a=(1,2,2,4)^{\mathsf T}$，$\boldsymbol b=(2,0,1,2)^{\mathsf T}$，求夹角余弦和 $\lVert\boldsymbol a-\boldsymbol b\rVert$。

$$\boldsymbol a\cdot\boldsymbol b=2+0+2+8=12,\qquad \lVert\boldsymbol a\rVert=\sqrt{25}=5,\qquad \lVert\boldsymbol b\rVert=\sqrt9=3,$$

所以 $\cos\theta=\frac{12}{15}=\frac45$。再由 $\boldsymbol a-\boldsymbol b=(-1,2,1,2)^{\mathsf T}$ 得 $\lVert\boldsymbol a-\boldsymbol b\rVert=\sqrt{10}$。

> 求 $(1,1,1,1)^{\mathsf T}$ 与 $(1,1,1,-1)^{\mathsf T}$ 的夹角。
>
> 答案：点积 2，两个长度都是 2，$\cos\theta=\frac12$，$\theta=\frac{\pi}{3}$。

**例 4**　已知 $\lVert\boldsymbol a\rVert=2$，$\lVert\boldsymbol b\rVert=1$，夹角为 $\frac{\pi}{3}$，求 $\boldsymbol a$ 与 $\boldsymbol a-\boldsymbol b$ 的夹角 $\varphi$。

这次没有分量，按方法 2 第 2 条走。

第一步，由夹角求点积：$\boldsymbol a\cdot\boldsymbol b=2\cdot1\cdot\cos\frac{\pi}{3}=1$。

第二步，算分子：$\boldsymbol a\cdot(\boldsymbol a-\boldsymbol b)=\lVert\boldsymbol a\rVert^2-\boldsymbol a\cdot\boldsymbol b=4-1=3$。

第三步，分母里的长度先平方：$\lVert\boldsymbol a-\boldsymbol b\rVert^2=4-2\cdot1+1=3$，所以 $\lVert\boldsymbol a-\boldsymbol b\rVert=\sqrt3$。

于是

$$\cos\varphi=\frac{3}{2\sqrt3}=\frac{\sqrt3}{2},\qquad \varphi=\frac{\pi}{6}.$$

#### 用柯西–施瓦茨求最值

**方法 3（柯西–施瓦茨求最值）**

1. 把一次式写成点积 $\boldsymbol c\cdot\boldsymbol x$，平方和写成 $\lVert\boldsymbol x\rVert^2$。
2. 由 $(\boldsymbol c\cdot\boldsymbol x)^2\le\lVert\boldsymbol c\rVert^2\lVert\boldsymbol x\rVert^2$ 得到一侧的界。
3. 由等号条件 $\boldsymbol x=t\boldsymbol c$ 找出取到界的点，并检查它满足全部条件。

**例 5**　已知 $x+2y+2z=9$，求 $x^2+y^2+z^2$ 的最小值和最小值点。

第一步，写成点积。取 $\boldsymbol c=(1,2,2)^{\mathsf T}$、$\boldsymbol x=(x,y,z)^{\mathsf T}$，条件是 $\boldsymbol c\cdot\boldsymbol x=9$，而 $\lVert\boldsymbol c\rVert^2=9$。

第二步，用不等式：

$$81=(\boldsymbol c\cdot\boldsymbol x)^2\le\lVert\boldsymbol c\rVert^2\lVert\boldsymbol x\rVert^2=9(x^2+y^2+z^2),$$

即 $x^2+y^2+z^2\ge9$。

第三步，找取等的点。等号要求 $\boldsymbol x=t\boldsymbol c$，代入条件得 $9t=9$，$t=1$，点 $(1,2,2)$ 满足条件，平方和正好是 9。所以最小值是 9。

> 已知 $x^2+y^2=4$，求 $3x-4y$ 的最大值和最大值点。
>
> 答案：$|3x-4y|\le5\cdot2=10$。等号要求 $(x,y)=t(3,-4)$，又要 $3x-4y>0$，所以 $t>0$；由 $\lVert(x,y)\rVert=5t=2$ 得点 $(\frac65,-\frac85)$，最大值 10。

本节是一条链：长度 → 柯西–施瓦茨（保证比值在 $[-1,1]$）→ 夹角 → 三角不等式。合上书，写出柯西–施瓦茨证明的五步，说出为什么要看 $\lVert\boldsymbol a+t\boldsymbol b\rVert^2$。

### 3. 一个向量在另一个方向上占多少？

给定方向 $\boldsymbol a$，能不能把向量 $\boldsymbol b$ 拆成「沿 $\boldsymbol a$ 的一份」加「和 $\boldsymbol a$ 垂直的一份」？$n$ 维里先要把「垂直」说清楚。

$\boldsymbol a\cdot\boldsymbol b=0$ 时，称 $\boldsymbol a$ 与 $\boldsymbol b$ **正交**，记作 $\boldsymbol a\perp\boldsymbol b$。对非零向量，正交就是夹角为 $\frac{\pi}{2}$；零向量与任何向量正交。

由展开式，$\lVert\boldsymbol a+\boldsymbol b\rVert^2=\lVert\boldsymbol a\rVert^2+\lVert\boldsymbol b\rVert^2$ 当且仅当中间项 $2\,\boldsymbol a\cdot\boldsymbol b=0$，即 $\boldsymbol a\perp\boldsymbol b$。这是 $n$ 维的勾股定理。

#### 投影公式

设 $\boldsymbol a\ne\boldsymbol 0$，要把 $\boldsymbol b$ 写成

$$\boldsymbol b=\boldsymbol p+\boldsymbol e,\qquad \boldsymbol p\ \text{是}\ \boldsymbol a\ \text{的倍数},\quad \boldsymbol e\perp\boldsymbol a.$$

第一步，设 $\boldsymbol p=t\boldsymbol a$，这样只剩一个未知数 $t$，而 $\boldsymbol e=\boldsymbol b-t\boldsymbol a$。

第二步，用垂直条件定 $t$。$(\boldsymbol b-t\boldsymbol a)\cdot\boldsymbol a=0$，展开得 $\boldsymbol a\cdot\boldsymbol b-t\,\boldsymbol a\cdot\boldsymbol a=0$。因为 $\boldsymbol a\ne\boldsymbol 0$，$\boldsymbol a\cdot\boldsymbol a>0$，可以除过去：

$$t=\frac{\boldsymbol a\cdot\boldsymbol b}{\boldsymbol a\cdot\boldsymbol a},\qquad \boldsymbol p=\frac{\boldsymbol a\cdot\boldsymbol b}{\boldsymbol a\cdot\boldsymbol a}\,\boldsymbol a,\qquad \boldsymbol e=\boldsymbol b-\boldsymbol p.$$

$\boldsymbol p$ 叫 $\boldsymbol b$ 在 $\boldsymbol a$ 上的**投影**，$\boldsymbol e$ 叫**残差**。

投影还是直线 $\{s\boldsymbol a\}$ 上离 $\boldsymbol b$ 最近的点。任取直线上一点 $\boldsymbol q=s\boldsymbol a$，把 $\boldsymbol b-\boldsymbol q$ 拆成两段：

$$\boldsymbol b-\boldsymbol q=\boldsymbol e+(\boldsymbol p-\boldsymbol q).$$

$\boldsymbol p-\boldsymbol q$ 是 $\boldsymbol a$ 的倍数，所以和 $\boldsymbol e$ 正交。由勾股定理，

$$\lVert\boldsymbol b-\boldsymbol q\rVert^2=\lVert\boldsymbol e\rVert^2+\lVert\boldsymbol p-\boldsymbol q\rVert^2\ge\lVert\boldsymbol e\rVert^2,$$

只有 $\boldsymbol q=\boldsymbol p$ 时取等号。所以 $\boldsymbol b$ 到这条直线的距离是 $\lVert\boldsymbol e\rVert$。

![残差 $\boldsymbol e$ 垂直于直线，$\boldsymbol b$ 到 $\boldsymbol q$ 是直角三角形的斜边，比到垂足长](fig/LA1-7.pdf){width=62%}

#### 三个长得很像的量

题目问「$\boldsymbol b$ 在 $\boldsymbol a$ 方向上占多少」时，可能要三个不同的量：

- 系数 $t=\dfrac{\boldsymbol a\cdot\boldsymbol b}{\boldsymbol a\cdot\boldsymbol a}$，它说 $\boldsymbol p$ 是 $\boldsymbol a$ 的几倍；
- **带符号长度** $\dfrac{\boldsymbol a\cdot\boldsymbol b}{\lVert\boldsymbol a\rVert}$，由点积公式它等于 $\lVert\boldsymbol b\rVert\cos\theta$，也就是 $\boldsymbol p$ 的长度带上正负号：与 $\boldsymbol a$ 同向为正，夹角为钝角时为负；
- 投影向量 $\boldsymbol p$ 本身。

**方法 4（投影与残差）**

1. 算 $t=\frac{\boldsymbol a\cdot\boldsymbol b}{\boldsymbol a\cdot\boldsymbol a}$，得 $\boldsymbol p=t\boldsymbol a$、$\boldsymbol e=\boldsymbol b-\boldsymbol p$。
2. 验算 $\boldsymbol e\cdot\boldsymbol a=0$。
3. 到直线 $\{s\boldsymbol a\}$ 的距离是 $\lVert\boldsymbol e\rVert$。
4. 看清题目要哪个量：问「投影向量」报告 $\boldsymbol p$，问「在 $\boldsymbol a$ 方向上占多长」报告带符号长度 $\frac{\boldsymbol a\cdot\boldsymbol b}{\lVert\boldsymbol a\rVert}$。

**例 6**　设 $\boldsymbol b=(1,3)^{\mathsf T}$，$\boldsymbol a=(2,1)^{\mathsf T}$。(1) 求 $\boldsymbol b$ 在 $\boldsymbol a$ 上的投影、残差，以及 $\boldsymbol b$ 到直线 $\{s\boldsymbol a\}$ 的距离；(2) 把 $\boldsymbol a$ 换成 $2\boldsymbol a$、$-\boldsymbol a$，三个量各怎么变？

(1) 第一步，$\boldsymbol a\cdot\boldsymbol b=2+3=5$，$\boldsymbol a\cdot\boldsymbol a=4+1=5$，所以 $t=1$，$\boldsymbol p=(2,1)^{\mathsf T}$。

第二步，$\boldsymbol e=\boldsymbol b-\boldsymbol p=(-1,2)^{\mathsf T}$，验算 $\boldsymbol e\cdot\boldsymbol a=-2+2=0$。

第三步，距离 $\lVert\boldsymbol e\rVert=\sqrt5$。

(2) 代同样的公式：

| 方向向量 | $t$ | 带符号长度 | 投影向量 $\boldsymbol p$ |
|---|---|---|---|
| $\boldsymbol a=(2,1)^{\mathsf T}$ | $1$ | $\sqrt5$ | $(2,1)^{\mathsf T}$ |
| $2\boldsymbol a=(4,2)^{\mathsf T}$ | $\frac{10}{20}=\frac12$ | $\frac{10}{\sqrt{20}}=\sqrt5$ | $(2,1)^{\mathsf T}$ |
| $-\boldsymbol a=(-2,-1)^{\mathsf T}$ | $\frac{-5}{5}=-1$ | $\frac{-5}{\sqrt5}=-\sqrt5$ | $(2,1)^{\mathsf T}$ |

投影向量始终不变，它只取决于那条直线。$t$ 跟着代表向量的长短变；带符号长度不管长短，只看正方向朝哪边。只有 $\boldsymbol a$ 是单位向量时，带符号长度才等于 $t$。

> 求 $\boldsymbol b=(3,3,0)^{\mathsf T}$ 在 $\boldsymbol a=(1,2,2)^{\mathsf T}$ 上的投影、残差、距离和带符号长度。
>
> 答案：$t=\frac99=1$，$\boldsymbol p=(1,2,2)^{\mathsf T}$，$\boldsymbol e=(2,1,-2)^{\mathsf T}$，验算 $\boldsymbol e\cdot\boldsymbol a=2+2-4=0$，距离 3。

**例 7**　把 $\boldsymbol b=(3,0,3)^{\mathsf T}$ 投影到 $\boldsymbol 1=(1,1,1)^{\mathsf T}$ 上，解释 $t$ 和残差。

计算和例 6 一样，新的是含义。$t=\frac{3+0+3}{3}=2$，正是三个分量的平均数。$\boldsymbol p=(2,2,2)^{\mathsf T}$，$\boldsymbol e=(1,-2,1)^{\mathsf T}$ 是各分量减去平均数，叫离差；验算 $\boldsymbol e\cdot\boldsymbol 1=1-2+1=0$，说的就是「离差之和为 0」。

一般地，投影到全 1 方向时，分子是各分量之和，分母是个数，所以 $t$ 就是平均数。再由「垂足最近」，用一个常数去近似一组数、按误差平方和比较时，最好的常数是平均数。

![投影到全 1 方向得到平均数 2，残差是离差 $+1,-2,+1$，和为 0，即残差与全 1 向量正交](fig/LA1-8.pdf){width=58%}

平面上投影到 $(1,1)^{\mathsf T}$，就是把点垂直地压到直线 $y=x$ 上。L.3 会把这个「压」写成一个矩阵。

合上书，从「残差与 $\boldsymbol a$ 正交」出发重新推出 $t$，再用勾股定理说明垂足最近。

### 4. 一个线性方程在 n 维空间里是什么形状？

线性方程 $a_1x_1+\cdots+a_nx_n=c$ 的左边正是点积 $\boldsymbol a\cdot\boldsymbol x$，所以点积能看清它的解集；判断一个点落在解集的哪一侧，就是线性分类器做的事（M.2）。

$x+2y=5$ 是一条直线，它朝哪个方向？换成 $x_1+2x_2+2x_3-x_4=5$，解集又是什么形状？

#### 解集垂直于系数向量

设 $\boldsymbol a\ne\boldsymbol 0$，$\boldsymbol x_0$ 是方程 $\boldsymbol a^{\mathsf T}\boldsymbol x=c$ 的一个解，即 $\boldsymbol a^{\mathsf T}\boldsymbol x_0=c$。把 $\boldsymbol a\cdot\boldsymbol x=c$ 与 $\boldsymbol a\cdot\boldsymbol x_0=c$ 相减，由分配律左边合成 $\boldsymbol a\cdot(\boldsymbol x-\boldsymbol x_0)$，右边是 0，所以

$$\boldsymbol a^{\mathsf T}\boldsymbol x=c\iff\boldsymbol a\cdot(\boldsymbol x-\boldsymbol x_0)=0 .$$

也就是说，$\boldsymbol x$ 是解，当且仅当从 $\boldsymbol x_0$ 到 $\boldsymbol x$ 的箭头与 $\boldsymbol a$ 正交。

在平面上，与 $(1,2)^{\mathsf T}$ 正交的向量都是 $(2,-1)^{\mathsf T}$ 的倍数。所以 $x+2y=5$ 的解集，是过 $\boldsymbol x_0=(1,2)$、垂直于 $(1,2)^{\mathsf T}$ 的直线（图 L2-n1 的粗实线）。

到了空间，与 $\boldsymbol a$ 正交的向量组成什么？以 $\boldsymbol a=(1,2,2)^{\mathsf T}$ 为例，分三步看。

第一步，写成方程。$(x,y,z)^{\mathsf T}\perp\boldsymbol a$，就是 $x+2y+2z=0$。

第二步，解出来。$y$、$z$ 可以任取，$x=-2y-2z$ 随之定出，所以这些向量是

$$\begin{pmatrix}-2y-2z\\y\\z\end{pmatrix}=y\begin{pmatrix}-2\\1\\0\end{pmatrix}+z\begin{pmatrix}-2\\0\\1\end{pmatrix}.$$

第三步，认出形状。右边是两个不共线向量的全部线性组合，由 L.1.3，它们张成一个过原点的平面。

所以与 $\boldsymbol a$ 正交的向量铺成一个过原点的平面，$x+2y+2z=c$ 的解集就是把这个平面平移到 $\boldsymbol x_0$。

一般地，$n$ 维里把 $\{\boldsymbol x:\boldsymbol a^{\mathsf T}\boldsymbol x=c\}$ 叫作**超平面**，$\boldsymbol a$ 叫它的**法向量**。$c$ 变化时超平面平行移动（图中两条虚线），$c\ne0$ 时不过原点。开头的 $x_1+2x_2+2x_3-x_4=5$，就是 $\mathbb R^4$ 里过一个解、垂直于 $(1,2,2,-1)^{\mathsf T}$ 的超平面，比全空间少一维。

![直线 $x+2y=5$ 上两点之差都与法向量 $\boldsymbol a=(1,2)^{\mathsf T}$ 垂直，$c$ 变化时直线平行移动；点 $(4,3)$ 沿 $\boldsymbol a$ 退一步到垂足 $(3,1)$，距离 $\sqrt5$](fig/L2-n1.pdf){width=60%}

#### 点到超平面的距离

点 $\boldsymbol y$ 离超平面多远？图中从 $(4,3)$ 沿 $-\boldsymbol a$ 退一步就落到直线上，退的方向正是法向量。所以设垂足为

$$\boldsymbol f=\boldsymbol y-t\boldsymbol a,$$

只剩 $t$ 待定。要求 $\boldsymbol f$ 在超平面上：$\boldsymbol a\cdot\boldsymbol y-t\,\boldsymbol a\cdot\boldsymbol a=c$，所以

$$t=\frac{\boldsymbol a\cdot\boldsymbol y-c}{\boldsymbol a\cdot\boldsymbol a},\qquad \boldsymbol f=\boldsymbol y-t\boldsymbol a,\qquad d=\lVert t\boldsymbol a\rVert=\frac{|\boldsymbol a\cdot\boldsymbol y-c|}{\lVert\boldsymbol a\rVert}.$$

$t$ 的符号说明 $\boldsymbol y$ 在哪一侧：$\boldsymbol a\cdot\boldsymbol y>c$ 时 $t>0$，$\boldsymbol y$ 在法向量所指的一侧；$\boldsymbol a\cdot\boldsymbol y<c$ 时在另一侧。

垂足最近的理由和第 3 节相同：超平面上任一点 $\boldsymbol x$ 都有 $\boldsymbol a\cdot(\boldsymbol f-\boldsymbol x)=c-c=0$，所以 $\boldsymbol y-\boldsymbol x=t\boldsymbol a+(\boldsymbol f-\boldsymbol x)$ 的两段正交，再用勾股定理。

**方法 5（点到超平面的距离）**

1. 把方程写成 $\boldsymbol a^{\mathsf T}\boldsymbol x=c$，系数向量就是法向量。
2. 按上面三个公式算 $t$、垂足 $\boldsymbol f$ 和距离 $d$。
3. 把垂足代回方程验算；需要时由 $t$ 的符号判断点在哪一侧。

**例 8**　求点 $\boldsymbol y=(4,3)^{\mathsf T}$ 到直线 $x+2y=5$ 的距离和垂足。

第一步，$\boldsymbol a=(1,2)^{\mathsf T}$，$c=5$。

第二步，$\boldsymbol a\cdot\boldsymbol y-c=10-5=5$，$\boldsymbol a\cdot\boldsymbol a=5$，所以 $t=1$，

$$\boldsymbol f=(4,3)^{\mathsf T}-(1,2)^{\mathsf T}=(3,1)^{\mathsf T},\qquad d=\frac{5}{\sqrt5}=\sqrt5 .$$

第三步，代回 $3+2\cdot1=5$，垂足确实在直线上。

> 求点 $(1,2,3)$ 到平面 $2x-y+2z=3$ 的距离和垂足。
>
> 答案：$\boldsymbol a=(2,-1,2)^{\mathsf T}$，$\boldsymbol a\cdot\boldsymbol y-c=6-3=3$，$t=\frac39=\frac13$，垂足 $(\frac13,\frac73,\frac73)$，距离 $\frac33=1$。

合上书，说清楚为什么线性方程的解集垂直于系数向量，再推一遍距离公式。

### 5. 推荐系统怎样找到口味相近的用户？

推荐系统要找口味相近的用户。点积会被长度带着走（例 1），比较方向要用余弦。两个非零向量的**余弦相似度**，就是它们夹角的余弦 $\frac{\boldsymbol a\cdot\boldsymbol b}{\lVert\boldsymbol a\rVert\lVert\boldsymbol b\rVert}$。

L.1 第 1 节三位用户小林、小周、小吴的打分，正是例 1 的 $\boldsymbol u$、$\boldsymbol v$、$\boldsymbol w$。三人的长度都是 $\sqrt{46}$，所以

$$\cos(\boldsymbol u,\boldsymbol v)=\frac{44}{46}\approx0.957,\qquad \cos(\boldsymbol u,\boldsymbol w)=\frac{26}{46}\approx0.565 .$$

可是 L.1 例 2 算过 $\boldsymbol w=6\cdot\boldsymbol 1-\boldsymbol u$：小林越喜欢的片，小吴越不喜欢，两人口味正好相反，余弦却是正的 0.565。

问题出在打分全是正数。每个人的打分里都有一大块「整体打分水平」，也就是第 3 节例 7 说的沿 $\boldsymbol 1$ 的那一份。这一块大家方向相同，把余弦都抬了上去。

补救办法是把这一份去掉，只比较残差，也就是每人先减去自己的平均分。三人的平均分都是 3，

$$\boldsymbol u'=(2,1,-2,-1)^{\mathsf T},\quad \boldsymbol v'=(1,2,-1,-2)^{\mathsf T},\quad \boldsymbol w'=(-2,-1,2,1)^{\mathsf T}=-\boldsymbol u'.$$

于是

$$\cos(\boldsymbol u',\boldsymbol v')=\frac{2+2+2+2}{\sqrt{10}\sqrt{10}}=0.8,\qquad \cos(\boldsymbol u',\boldsymbol w')=-1 .$$

| | 小林与小周 | 小林与小吴 |
|---|---|---|
| 直接算余弦 | 0.957 | 0.565 |
| 减去平均分后的余弦 | 0.8 | $-1$ |

去掉整体打分水平以后，口味相反才显示成了 $-1$。

**方法 6（余弦相似度）**

1. 比较口味、内容是否相近时，用余弦而不用点积。
2. 打分类数据先把每个向量减去自己的平均分，也就是去掉它在 $\boldsymbol 1$ 上的投影，再算余弦。

> 按方法 6 算 $(5,5,3,3)^{\mathsf T}$ 与 $\boldsymbol u$、$\boldsymbol w$ 的余弦相似度。
>
> 答案：平均数 4，去均值后是 $(1,1,-1,-1)^{\mathsf T}$，长度 2。与 $\boldsymbol u'$：$\frac{2+1+2+1}{2\sqrt{10}}\approx0.949$；与 $\boldsymbol w'=-\boldsymbol u'$：约 $-0.949$。

检索增强生成（RAG）让大模型先查资料再回答：资料库里每段文字事先由另一个模型变成一个向量，意思相近的文字，向量方向也相近（叫嵌入，M.9 讲）；提问也变成向量 $\boldsymbol q$；系统取出与 $\boldsymbol q$ 余弦最大的几段，交给大模型参考。

嵌入要不要也先去均值？判断线索是：所有向量若共享一块公共成分（平均向量不算短），余弦就会被它抬高，该先减去平均向量，打分就是这样。实际的嵌入有时也有这种偏向；本例按简化直接比余弦。

**例 9**　问题的向量是 $\boldsymbol q=(1,2,2)^{\mathsf T}$，三段资料的向量是 $\boldsymbol d_1=(2,1,2)^{\mathsf T}$、$\boldsymbol d_2=(8,-4,8)^{\mathsf T}$、$\boldsymbol d_3=(2,-2,1)^{\mathsf T}$。按余弦相似度应取哪一段？按点积呢？

第一步，算长度：$\lVert\boldsymbol q\rVert=\lVert\boldsymbol d_1\rVert=\lVert\boldsymbol d_3\rVert=3$，$\lVert\boldsymbol d_2\rVert=12$。

第二步，算与 $\boldsymbol q$ 的点积：

$$\boldsymbol q\cdot\boldsymbol d_1=2+2+4=8,\qquad \boldsymbol q\cdot\boldsymbol d_2=8-8+16=16,\qquad \boldsymbol q\cdot\boldsymbol d_3=2-4+2=0 .$$

第三步，余弦依次为 $\frac89\approx0.889$、$\frac{16}{36}\approx0.444$、0，所以取 $\boldsymbol d_1$；$\boldsymbol d_3$ 与问题正交，在本例的简化打分里得分为 0。

按点积会取 $\boldsymbol d_2$，可它方向离 $\boldsymbol q$ 更远，点积大只因为它长。

合上书，说出直接算余弦会出什么问题，以及去均值和第 3 节的投影是什么关系。

### 本章小结

| 方法 | 什么时候用 | 对应题号 |
|---|---|---|
| 方法 1（算点积） | 有分量逐项乘加；只给点积时展开 | L2-01、L2-08、L2-13 |
| 方法 2（求长度和夹角） | 求夹角、长度；没分量时先平方再展开 | L2-02、L2-06、L2-08、L2-11 |
| 方法 3（柯西–施瓦茨求最值） | 一次式与平方和之间的最值、证不等式 | L2-07、L2-12 |
| 方法 4（投影与残差） | 投影向量、带符号长度、到过原点直线的距离、平均数 | L2-03、L2-04、L2-06、L2-12 |
| 方法 5（点到超平面的距离） | 线性方程、法向量、距离与垂足、在哪一侧 | L2-10、L2-13、L2-14 |
| 方法 6（余弦相似度） | 比较口味或内容；打分先去均值 | L2-05、L2-09、L2-11 |
