## C.12 · 反常积分

有一类积分，积分区间伸向无穷远。如果把一项长期付款简化为按固定的年支付率连续支付，并且一直付下去，它今天值多少钱？相邻两位顾客到来之间的等待时间，平均要等多久？一条正态曲线下的总面积为什么刚好是 1？这些问题的答案都是积到无穷远的积分，而 C.9 对定积分的定义要求区间有限、函数有界，直接套用不了。

这段历史有两条线。18 世纪，欧拉想把阶乘推广到非整数：整数处的值已经知道，只靠有限个点上的插值，定不下整条曲线；他最后从一个积分里找到了它，这就是第 4 节的 $\Gamma$ 函数。另一条线是 19 世纪的柯西：当时「积到无穷远」还只是一句直观的话，他要给它一个严格定义，才把「先积到有限处、再让上限跑向无穷」写成极限。

办法很朴素：先积到一个有限的位置 $b$，用牛顿–莱布尼茨公式算出结果，再让 $b$ 跑向无穷远，看结果有没有极限。另一个问题是怎样把阶乘 $n!$ 推广到非整数。第 4 节将用一个积分给出这种推广，并把有限区间与无穷区间上的两种积分形式联系起来。

本章把这个想法用到两种情形：第 1 节是区间伸到无穷远，第 2 节是函数在某一点冲向无穷大。两者合称反常积分，名字里的「反常」就是 C.9 的定义管不了。第 3 节问：积不出原函数时，怎样判断它有没有极限；第 4 节用欧拉的 $\Gamma$ 函数，把前面的方法综合一遍。

### 1. 积分区间伸到无穷远，面积还可能是有限的吗？

先拿两个老朋友 $\frac1{x^2}$ 和 $\frac1x$ 看。两条曲线都从 $x=1$ 伸向右边，都越来越贴近 $x$ 轴，先猜一猜：它们下方的面积都是有限的吗？从 $x=1$ 向右，各积到 $b$，看表：

| $b$ | 10 | 100 | 1000 | $10^6$ |
|---|---|---|---|---|
| $\int_1^b\frac{\mathrm{d}x}{x^2}=1-\frac1b$ | 0.9 | 0.99 | 0.999 | 0.999999 |
| $\int_1^b\frac{\mathrm{d}x}{x}=\ln b$ | 2.3026 | 4.6052 | 6.9078 | 13.8155 |

第一行趋于 1，第二行虽然增长很慢，却没有上界。两条曲线都伸向无穷远，形状也都是「越来越贴近 $x$ 轴」，面积却一个有限、一个无限。所以「被积函数趋于 0」并不是收敛的理由，要看它趋于 0 的快慢。

![$y=\frac1{x^2}$（实线）与 $y=\frac1x$（虚线）在 $[1,+\infty)$ 上：实线下方（浅灰）积到 $b$ 时面积是 $1-\frac1b$，永远不超过 1；虚线下方积到 $b$ 时面积是 $\ln b$，随 $b$ 无限增大；竖直点线标出 $b=10$](fig/C12-n1.pdf){width=70%}

这样的积分有了定义。设 $f$ 在 $[a,+\infty)$ 上连续，规定

$$\int_a^{+\infty}f(x)\,\mathrm{d}x=\lim_{b\to+\infty}\int_a^bf(x)\,\mathrm{d}x.$$

极限存在（是一个有限的数），就说这个**反常积分收敛**，极限值就是它的值；极限不存在或为无穷，就说**发散**。类似地，$\int_{-\infty}^bf=\lim_{a\to-\infty}\int_a^bf$。

两头都伸向无穷远时，拆成两半：

$$\int_{-\infty}^{+\infty}f(x)\,\mathrm{d}x=\int_{-\infty}^cf(x)\,\mathrm{d}x+\int_c^{+\infty}f(x)\,\mathrm{d}x,$$

两半**都收敛**，整个积分才收敛。$c$ 取哪里都行，值不依赖于 $c$。仅有对称截断 $\lim_{R\to\infty}\int_{-R}^R$ 的极限存在，不能判定反常积分收敛：比如 $f(x)=x$，$\int_{-R}^Rx\,\mathrm{d}x=0$，但右半 $\int_0^{+\infty}x\,\mathrm{d}x$ 趋于正无穷，左半趋于负无穷，整个积分发散。已知两侧都收敛时，才可以用对称截断计算积分值。

如果 $F$ 是 $f$ 的原函数，就是把牛顿–莱布尼茨公式的上限换成极限：

$$\int_a^{+\infty}f(x)\,\mathrm{d}x=F(+\infty)-F(a),\qquad F(+\infty)=\lim_{x\to+\infty}F(x).$$

当 $F(+\infty)$ 的极限不存在时，积分发散。

上面的表格对应一个一般的结论，叫 **$p$ 积分**：

$$\int_1^{+\infty}\frac{\mathrm{d}x}{x^p}\ \begin{cases}=\dfrac1{p-1},&p>1,\\[1mm]\text{发散},&p\le1.\end{cases}$$

证明只要积到 $b$，先写出有限积分。$p\ne1$ 时

$$\int_1^bx^{-p}\,\mathrm{d}x=\frac{b^{1-p}-1}{1-p}.$$

- $p>1$：$1-p<0$，$b^{1-p}\to0$，分子趋于 $-1$、分母 $1-p<0$，极限是 $\frac1{p-1}$，收敛。
- $p<1$：$1-p>0$，$b^{1-p}\to+\infty$，极限是 $+\infty$，发散。
- $p=1$：$\int_1^b\frac{\mathrm{d}x}x=\ln b\to+\infty$，发散。

分界在 $p=1$：$\frac1x$ 衰减得「刚好不够快」，哪怕多一点点（$p=1.001$）就够了。C.14 里的级数 $\sum\frac1n$ 与 $\sum\frac1{n^2}$ 也是这样，那里的积分判别法会把两者精确地连起来。

**方法 1（无穷区间的反常积分）**

1. 先求原函数 $F$（用 C.11 的方法）。
2. 积到 $b$：$\int_a^bf=F(b)-F(a)$，再令 $b\to+\infty$ 求极限，极限要单独算（常用洛必达法则，C.8）。
3. 两头无穷时在中间任取一点拆开，两半分别判断；只要有一半发散就发散。

**例 1**　求 $\int_0^{+\infty}\mathrm{e}^{-\lambda x}\,\mathrm{d}x$（$\lambda>0$）和 $\int_0^{+\infty}x\mathrm{e}^{-x}\,\mathrm{d}x$。

先从最简单的指数函数开始，第二个再多一个因子 $x$。

第一个，原函数是 $-\frac1\lambda\mathrm{e}^{-\lambda x}$，$\lambda>0$ 时 $\mathrm{e}^{-\lambda b}\to0$：

$$\int_0^{+\infty}\mathrm{e}^{-\lambda x}\,\mathrm{d}x=\Big[-\frac1\lambda\mathrm{e}^{-\lambda x}\Big]_0^{+\infty}=0+\frac1\lambda=\frac1\lambda.$$

第二个比第一个多一个因子 $x$，用分部积分。仿照 C.11.5 例 25，取 $u=x$，$\mathrm{d}v=\mathrm{e}^{-x}\mathrm{d}x$，则 $\mathrm{d}u=\mathrm{d}x$，$v=-\mathrm{e}^{-x}$：

$$\int x\mathrm{e}^{-x}\,\mathrm{d}x=-x\mathrm{e}^{-x}+\int\mathrm{e}^{-x}\,\mathrm{d}x=-(x+1)\mathrm{e}^{-x}+C.$$

上限处的极限要单独算：$\lim_{b\to+\infty}(b+1)\mathrm{e}^{-b}=\lim\frac{b+1}{\mathrm{e}^b}=\lim\frac1{\mathrm{e}^b}=0$（洛必达）。所以

$$\int_0^{+\infty}x\mathrm{e}^{-x}\,\mathrm{d}x=\big[-(x+1)\mathrm{e}^{-x}\big]_0^{+\infty}=0+1=1.$$

> 求 $\int_{-\infty}^0\mathrm{e}^{x}\,\mathrm{d}x$。
>
> 答案：$[\mathrm{e}^x]_{-\infty}^0=1-0=1$。

**例 2**　求 $\int_2^{+\infty}\frac{\mathrm{d}x}{x\ln^2x}$ 和 $\int_2^{+\infty}\frac{\mathrm{d}x}{x\ln x}$。

$p$ 积分里的 $x^p$ 换成 $\ln x$ 的幂，分界还在 1 吗？两个被积函数很像，分母只差一个 $\ln x$ 的幂。都用凑微分（C.11.1）：$\frac{\mathrm{d}x}x=\mathrm{d}\ln x$。

$$\int_2^{+\infty}\frac{\mathrm{d}\ln x}{\ln^2x}=\Big[-\frac1{\ln x}\Big]_2^{+\infty}=\frac1{\ln2},\qquad \int_2^{+\infty}\frac{\mathrm{d}\ln x}{\ln x}=\big[\ln\ln x\big]_2^{+\infty}=+\infty.$$

第一个收敛，第二个发散，规律和 $p$ 积分一样：把 $u=\ln x$ 当新变量，就是 $\int\frac{\mathrm{d}u}{u^2}$ 和 $\int\frac{\mathrm{d}u}u$，只是发散得更慢：要 $x$ 超过五亿多，$\ln\ln x$ 才超过 3。

**例 3**　一项永续年金按每年 1000 元的固定速率连续支付，永远付下去，贴现率是连续复利 $5\%$。求它的现值 $PV$（present value，今天的价值）。

和例 1 相比，积分没有变，只是换成一个应用：把无穷多笔付款加起来。

先说什么叫现值。把 1 元存入连续复利 $r$ 的账户，$t$ 年后变成 $\mathrm{e}^{rt}$ 元，反过来，$t$ 年后的 1 元今天只值 $\mathrm{e}^{-rt}$ 元。时间从 $t$ 到 $t+\mathrm{d}t$ 这一小段，付出 $1000\,\mathrm{d}t$ 元，它的现值是 $1000\mathrm{e}^{-rt}\,\mathrm{d}t$，把所有时刻的加起来：

$$PV=\int_0^{+\infty}1000\,\mathrm{e}^{-0.05t}\,\mathrm{d}t=1000\cdot\frac1{0.05}=20000\ \text{元}.$$

用例 1 的第一个结果，$\lambda=0.05$。无穷多笔付款，现值却是有限的，因为越远的钱越不值钱。如果只付 100 年，现值是 $20000(1-\mathrm{e}^{-5})\approx19865$，已经和永续年金几乎一样。

**例 4**　一家店平均每小时有 2 位顾客到来，相邻两位顾客之间的间隔 $T$（小时）服从指数分布，概率密度是 $f(x)=2\mathrm{e}^{-2x}$（$x\ge0$）。求总概率，以及平均间隔。

和例 3 相比，被积函数仍是 $\mathrm{e}^{-\lambda x}$ 型，换成概率里的用法。

这里的 $f$ 叫概率密度，意思是：$T$ 落在 $[a,b]$ 里的概率等于曲线下的面积 $\int_a^bf(x)\,\mathrm{d}x$。$T$ 一定取某个非负值，所以总面积应该是 1；$f$ 里的系数 2 正是使总面积等于 1 的那个数。由例 1：

$$\int_0^{+\infty}2\mathrm{e}^{-2x}\,\mathrm{d}x=2\cdot\frac12=1.$$

平均值怎样算？先看离散的小情形：掷一枚骰子，点数 $x_i=1,\dots,6$ 的概率都是 $\frac16$，平均点数是 $\sum x_ip_i=\frac{1+2+\cdots+6}6=3.5$，每个值乘上它出现的概率再加起来。连续的情形里，$x$ 附近宽度 $\mathrm{d}x$ 的一小段，概率是 $f(x)\,\mathrm{d}x$，所以把 $\sum$ 换成积分：每个值 $x$ 乘上它的概率 $f(x)\,\mathrm{d}x$，加起来：

$$\int_0^{+\infty}x\cdot2\mathrm{e}^{-2x}\,\mathrm{d}x=\frac12\int_0^{+\infty}(2x)\mathrm{e}^{-2x}\,\mathrm{d}(2x)=\frac12\int_0^{+\infty}u\mathrm{e}^{-u}\,\mathrm{d}u=\frac12.$$

最后一步令 $u=2x$，用例 1 的第二个积分。平均间隔是半小时，与「每小时来 2 位」互相吻合。

**例 5**　判断 $\int_{-\infty}^{+\infty}\frac{\mathrm{d}x}{1+x^2}$ 与 $\int_{-\infty}^{+\infty}\frac{x\,\mathrm{d}x}{1+x^2}$ 的敛散。

和例 1 到例 4 相比，积分区间两头都是无穷，要拆成两半分别判断。

第一个在 0 处拆开，每一半 $\int_0^{+\infty}\frac{\mathrm{d}x}{1+x^2}=\big[\arctan x\big]_0^{+\infty}=\frac\pi2$，另一半同样，所以整个积分收敛，值是 $\pi$。

第二个的被积函数是奇函数，看起来应当抵消成 0。但看一半：$\int_0^{b}\frac{x\,\mathrm{d}x}{1+x^2}=\frac12\ln(1+b^2)\to+\infty$，一半就发散了，整个积分发散。奇函数「积分为 0」的规律（C.11.4）在有限对称区间上要求可积；对整条实轴，必须先证明左右两侧分别收敛，才能用它。这里两侧都发散，所以不能用。

这一节里区间都伸向无穷远，被积函数始终有限。可是还有另一种情形：区间有限，函数却在区间里的某一点冲向无穷大，上面的做法还管不管用，第 2 节来回答。

合上书，写出无穷区间反常积分的定义，说明为什么 $\int_{-\infty}^{+\infty}$ 要拆成两半分别判断，并说出 $p$ 积分的分界在哪里。

### 2. 被积函数在某一点冲向无穷大时，积分还有意义吗？

上一节的区间伸到无穷远，这一节区间有限，函数却在某个点附近冲向无穷大。看 $\frac1{\sqrt x}$ 和 $\frac1x$ 在 $x=0$ 附近，从 $\varepsilon$ 积到 1：

| $\varepsilon$ | 0.01 | $10^{-4}$ | $10^{-6}$ |
|---|---|---|---|
| $\int_\varepsilon^1\frac{\mathrm{d}x}{\sqrt x}=2-2\sqrt\varepsilon$ | 1.8 | 1.98 | 1.998 |
| $\int_\varepsilon^1\frac{\mathrm{d}x}x=\ln\frac1\varepsilon$ | 4.6052 | 9.2103 | 13.8155 |

第一行趋于 2，第二行无界。和第 1 节完全平行：先避开出问题的点，再让这个距离趋于 0。

![$y=\frac1{\sqrt x}$（实线）与 $y=\frac1x$（虚线）在 $(0,1]$ 上：两条曲线在 $x=0$ 处都冲向无穷；实线下方（浅灰）在 $[\varepsilon,1]$ 上的面积 $2-2\sqrt\varepsilon$ 不超过 2；虚线下方 $[\varepsilon,1]$ 上的面积 $\ln\frac1\varepsilon$ 随 $\varepsilon\to0$ 无限增大](fig/C12-n2.pdf){width=70%}

设 $f$ 在 $(a,b]$ 上连续，在 $a$ 附近无界（这样的点 $a$ 叫**瑕点**），规定

$$\int_a^bf(x)\,\mathrm{d}x=\lim_{\varepsilon\to0^+}\int_{a+\varepsilon}^bf(x)\,\mathrm{d}x.$$

瑕点在右端点 $b$ 时，对应 $\lim_{\varepsilon\to0^+}\int_a^{b-\varepsilon}f$。瑕点 $c$ 在区间里面时，在 $c$ 处拆成两半，**两半都收敛**才收敛。

最容易出错的是内部的瑕点。$\int_{-1}^1\frac{\mathrm{d}x}{x^2}$ 如果不看 $x=0$ 处的问题，直接用牛顿–莱布尼茨公式：$\big[-\frac1x\big]_{-1}^1=-1-1=-2$，一个正函数的积分得到负数，显然不对。正确的做法是在 0 拆开，$\int_0^1\frac{\mathrm{d}x}{x^2}=\lim_{\varepsilon\to0^+}\big(\frac1\varepsilon-1\big)=+\infty$，发散。

瑕点的 $p$ 积分同样有分界，方向却和第 1 节相反：

$$\int_0^1\frac{\mathrm{d}x}{x^p}\ \begin{cases}=\dfrac1{1-p},&p<1,\\[1mm]\text{发散},&p\ge1.\end{cases}$$

先从 $\varepsilon$ 积到 1，$p\ne1$ 时

$$\int_\varepsilon^1x^{-p}\,\mathrm{d}x=\frac{1-\varepsilon^{1-p}}{1-p}.$$

- $p<1$：$1-p>0$，$\varepsilon^{1-p}\to0$，极限 $\frac1{1-p}$，收敛。
- $p>1$：$1-p<0$，$\varepsilon^{1-p}\to+\infty$，分子趋于 $-\infty$、分母为负，商趋于 $+\infty$，发散。
- $p=1$：$\int_\varepsilon^1\frac{\mathrm{d}x}x=\ln\frac1\varepsilon\to+\infty$，发散。

为什么方向相反？用倒数换元 $x=\frac1t$ 就看明白了（例 8 也用它）。$\mathrm{d}x=-\frac{\mathrm{d}t}{t^2}$，所以 $\frac{\mathrm{d}x}{x^p}=-t^{p-2}\,\mathrm{d}t$；同时 $x$ 从 $1$ 增至 $b$ 时，$t$ 从 $1$ 减至 $\frac1b$。反转上下限，负号消去：

$$\int_1^b\frac{\mathrm{d}x}{x^p}=\int_{1/b}^1\frac{\mathrm{d}t}{t^{2-p}}.$$

令 $b\to+\infty$，无穷远处的条件 $p>1$ 就对应零点附近的条件 $2-p<1$。

**方法 2（无界函数的反常积分）**

1. 找瑕点：被积函数在哪个点附近无界（分母为零、$\ln x$ 的 $x=0$、$\frac1{\sqrt{1-x^2}}$ 的 $x=\pm1$）。
2. 瑕点在端点：积到 $\varepsilon$ 之外，用牛顿–莱布尼茨公式后令 $\varepsilon\to0^+$；瑕点在内部：先拆开。
3. 拆开的目标是让每一段至多有一个需要取极限的端点：内部瑕点处必须拆，某一段两头都有问题时再在中间取一个普通点拆。分别判断所有单侧积分，全部收敛时原积分才收敛。

**反常积分的换元与分部。** 做法是：先在有限的区间上做（这时是普通的定积分，C.11.3、C.11.6 的公式都成立），再取极限。具体说：

- 换元时，$x=\varphi(t)$ 在对应的开区间上严格单调，并有连续的导数；各端点（含无穷远）按极限对应。先在避开问题端点的有限区间上用 C.11.3 的换元公式，再分别取端点极限。
- 分部时同样先截断；只有边界项和余下的积分分别具有有限的极限时，才能拆开写成它们的差。

**例 6**　求 $\int_0^1\ln x\,\mathrm{d}x$ 和 $\int_0^1x\ln x\,\mathrm{d}x$。

做法同第 2 节开头的表：避开 $x=0$，积到 $\varepsilon$ 为止，再令 $\varepsilon\to0^+$。和第 1 节相比，区间有限，问题出在被积函数。

$\ln x$ 在 $x=0$ 处趋于 $-\infty$，瑕点在左端点。由 C.11.5 例 26，原函数是 $x\ln x-x$：

$$\int_0^1\ln x\,\mathrm{d}x=\lim_{\varepsilon\to0^+}\big[x\ln x-x\big]_\varepsilon^1=-1-\lim_{\varepsilon\to0^+}(\varepsilon\ln\varepsilon-\varepsilon)=-1.$$

其中 $\lim_{\varepsilon\to0^+}\varepsilon\ln\varepsilon=\lim\frac{\ln\varepsilon}{1/\varepsilon}=\lim\frac{1/\varepsilon}{-1/\varepsilon^2}=\lim(-\varepsilon)=0$（洛必达，$\frac\infty\infty$ 型）。

> 求 $\int_0^1x\ln x\,\mathrm{d}x$。
>
> 答案：分部，$u=\ln x$，$\mathrm{d}v=x\,\mathrm{d}x$，原函数 $\frac{x^2}2\ln x-\frac{x^2}4$，下限处 $\varepsilon^2\ln\varepsilon\to0$，积分 $=-\frac14$。

**例 7**　判断 $\int_0^1\frac{\mathrm{d}x}{\sqrt{1-x^2}}$ 与 $\int_0^2\frac{\mathrm{d}x}{(x-1)^2}$ 的敛散，收敛的求值。

和例 6 相比，一个瑕点在端点，另一个在区间内部。

第一个的瑕点在右端点 $x=1$，原函数是 $\arcsin x$：

$$\int_0^1\frac{\mathrm{d}x}{\sqrt{1-x^2}}=\lim_{\varepsilon\to0^+}\arcsin(1-\varepsilon)-\arcsin0=\frac\pi2.$$

第二个的瑕点 $x=1$ 在区间内部，要拆开。先单独看左半，写出左侧截断式：

$$\int_0^{1-\varepsilon}\frac{\mathrm{d}x}{(x-1)^2}=\Big[\frac1{1-x}\Big]_0^{1-\varepsilon}=\frac1\varepsilon-1.$$

令 $\varepsilon\to0^+$，极限是 $+\infty$，左半已经发散，整个积分发散。

如果不拆，直接代端点，会得到 $\big[-\frac1{x-1}\big]_0^2=-2$，和前面的 $\int_{-1}^{1}\frac{\mathrm{d}x}{x^2}$ 是同一个错误：原函数 $-\frac1{x-1}$ 在 $x=1$ 处断开，不能跨过去代入。

**例 8**　求 $\int_1^{+\infty}\frac{\mathrm{d}x}{x\sqrt{x^2-1}}$。

和例 7 相比，这一题把两种问题放在了一起：一头是无穷远，一头是瑕点。

这个积分有两个问题点：上限是无穷远，下限 $x=1$ 是瑕点。按方法 2 第 3 步，在中间任选一个普通点（例如 $x=2$）分成两段，每段只有一个问题端点；下面对两段同时用倒数换元，为书写方便合在一起写。

先在有限区间 $[1+\varepsilon,R]$ 上换元 $x=\frac1t$，$\mathrm{d}x=-\frac{\mathrm{d}t}{t^2}$，$\sqrt{x^2-1}=\frac{\sqrt{1-t^2}}t$（$t>0$），$x$ 从 $1+\varepsilon$ 到 $R$ 对应 $t$ 从 $\frac1{1+\varepsilon}$ 减到 $\frac1R$，反转上下限：

$$\int_{1+\varepsilon}^R\frac{\mathrm{d}x}{x\sqrt{x^2-1}}=\int_{1/R}^{1/(1+\varepsilon)}\frac{\mathrm{d}t}{\sqrt{1-t^2}}.$$

右边的被积函数在 $t=0$ 处连续，在 $t=1$ 处是例 7 的瑕点、已知收敛，所以可以先固定 $\varepsilon$，令 $R\to+\infty$（下限 $\frac1R\to0$，被积函数在 $t=0$ 连续，极限存在），再令 $\varepsilon\to0^+$（上限 $\frac1{1+\varepsilon}\to1$，由例 7，极限存在），得到：

$$\int_1^{+\infty}\frac{\mathrm{d}x}{x\sqrt{x^2-1}}=\int_0^1\frac{\mathrm{d}t}{\sqrt{1-t^2}}=\frac\pi2.$$

无穷远变成了 $t=0$，瑕点 $x=1$ 变成了 $t=1$ 处的瑕点；被积函数在 $t=0$ 处变得很安稳。结果就是例 7 的第一个积分。换元把「无穷区间」和「瑕积分」互相转化，这是二者共用一套判别法的原因。

**例 9**　求 $\int_0^{+\infty}x^2\mathrm{e}^{-x}\,\mathrm{d}x$。

和例 1 的第二个积分相比多了一次幂，分部积分要做两次，每次的边界项都是 $x$ 的幂乘 $\mathrm{e}^{-x}$，上限处趋于 0，下限处为 0。取 $u=x^2$，$v=-\mathrm{e}^{-x}$：

$$\int_0^{+\infty}x^2\mathrm{e}^{-x}\,\mathrm{d}x=\big[-x^2\mathrm{e}^{-x}\big]_0^{+\infty}+2\int_0^{+\infty}x\mathrm{e}^{-x}\,\mathrm{d}x=0+2\cdot1=2.$$

积出来的是 $2!$。第 4 节会看到，这不是巧合。

前两节每个例子都先求出原函数再取极限。可是 $\mathrm{e}^{-x^2}$ 这样的函数写不出原函数，这条路就断了，而它的积分有没有一个有限值，仍然是一个该回答的问题，第 3 节来处理。

合上书，说出瑕点在端点和在内部各怎样处理，并解释为什么 $\int_{-1}^1\frac{\mathrm{d}x}{x^2}$ 不能直接用牛顿–莱布尼茨公式。

### 3. 求不出原函数时，怎样判断反常积分是否收敛？

$\int_0^{+\infty}\mathrm{e}^{-x^2}\,\mathrm{d}x$ 的原函数写不成初等函数（C.11.9），前两节「先求原函数」的路走不通。但这个积分有没有一个有限值，不必算出原函数就能回答，办法是和已知的比。

先看一个其实能直接算的小情形。$\int_1^{+\infty}\frac{\mathrm{d}x}{1+x^2}=\frac\pi2-\frac\pi4=\frac\pi4\approx0.785$，假装不会算：$\frac1{1+x^2}<\frac1{x^2}$，曲线在 $\frac1{x^2}$ 的下方，而后者下方的面积是 1（$p=2$），所以前者积到 $b$ 的面积 $S(b)$ 随 $b$ 增大不减，又始终不超过 1，必有极限。下面把这个想法写成一般的形式。

设 $f\ge0$ 在 $[a,+\infty)$ 上连续。令 $S(b)=\int_a^bf(x)\,\mathrm{d}x$，因为 $f\ge0$，$S$ 随 $b$ 增大而不减。（瑕点 $a$ 的情形照搬：令 $S(\varepsilon)=\int_{a+\varepsilon}^bf$，$\varepsilon$ 减小时区间变大，$S$ 同样不减，$\varepsilon\to0^+$ 时有有限极限当且仅当有上界。）对这里的单调不减函数 $S(b)$，当 $b\to+\infty$ 时，它有有限极限，当且仅当它有上界（C.1.9 的单调有界准则）。所以

$$\int_a^{+\infty}f\ \text{收敛}\iff S(b)\ \text{有上界}.$$

这就是比较判别法的全部来源。

**比较判别法。** 以下每次只比较一个问题端点：无穷远处比较 $[A,+\infty)$ 上的尾部；有限端点处比较它一侧的一小段。设 $f,g$ 在所比较的区间内连续，避开问题端点后都是普通定积分。它只判断这一段的敛散，其他问题端点仍须单独检查。设 $0\le f(x)\le g(x)$，则：

- $\int g$ 收敛 $\Rightarrow$ $\int f$ 收敛；
- $\int f$ 发散 $\Rightarrow$ $\int g$ 发散。

证明：$S_f(b)\le S_g(b)\le\int_a^{+\infty}g$，所以 $S_f$ 有上界，第一条成立；第二条是第一条的逆否命题。

$f\ge0$ 这个条件不能去掉：$f=-1$、$g=\frac1{x^2}$ 在 $[1,+\infty)$ 上满足 $f\le g$，$\int g$ 收敛，但 $\int f=-\infty$。

实际中很少恰好有 $f\le g$ 这样的现成不等式，更常见的是两个函数在问题点附近「差不多大」。极限形式把这句话说清楚：设问题点附近 $f\ge0$、$g>0$，$\lim\frac{f(x)}{g(x)}=l$（对无穷远是 $x\to+\infty$，对瑕点 $a$ 是 $x\to a^+$）。为什么比值的极限能换来不等式？按极限的定义，存在 $\delta>0$，当 $x$ 进入问题点的 $\delta$ 邻域（无穷远则 $x>1/\delta$）时，$\big|\frac fg-l\big|$ 小于所取的误差；$l=+\infty$ 时改用无穷极限的定义，$\frac fg$ 最终大于任意给定的正数，取 1 即可。邻域之外剩下一段普通定积分，有限，不影响敛散。于是：$0<l<+\infty$ 时，问题点附近 $\frac fg$ 夹在 $\frac l2$ 与 $2l$ 之间，即 $\frac l2g\le f\le2lg$，$f$ 与 $g$ 互相控制，由比较判别法同敛散；$l=0$ 时问题点附近 $f\le g$，只能由 $g$ 收敛推出 $f$ 收敛，反过来不行；$l=+\infty$ 时问题点附近 $f\ge g$，只能由 $g$ 发散推出 $f$ 发散。下面是结论：

- $0<l<+\infty$：$\int f$ 与 $\int g$ 同时收敛或同时发散；
- $l=0$：$\int g$ 收敛 $\Rightarrow$ $\int f$ 收敛；
- $l=+\infty$：$\int g$ 发散 $\Rightarrow$ $\int f$ 发散。

后两条只能单向用。$f=\frac1{x^2}$、$g=\frac1x$ 在无穷远处 $l=0$，$\int g$ 发散，$\int f$ 却收敛；$f=\frac1x$、$g=\frac1{x^2}$ 的 $l=+\infty$，$\int g$ 收敛，$\int f$ 却发散。

怎样找比较的对象？比较的「尺子」常用 $p$ 积分：无穷远处 $\frac1{x^p}$（$p>1$ 收敛），有限瑕点 $a$ 处 $\frac1{|x-a|^p}$（$p<1$ 收敛）。若被积函数有幂函数的主要部分 $\frac{c}{x^p}$（或 $\frac c{|x-a|^p}$，$c>0$），读出 $p$ 就行。「主要部分」指满足 $\frac{f(x)}{c/x^p}\to1$ 的那个式子：分子分母各保留趋于问题点时最重要的一项（例如无穷远处取最高次项），$1-\cos x$ 这类用 C.2.9 的等价无穷小 $\frac{x^2}2$。使用前要检验比值确实趋于 1；最高次项相消时（例如 $(x+1)-x$），要往下一项看。

**方法 3（比较判别法）**

1. 先检查问题点附近的符号。若函数为负，先对 $-f$ 判断；若有正有负，可对 $|f|$ 判断绝对收敛，不能由「不绝对收敛」直接推出原积分发散。
2. 选择已知敛散性的非负函数作比较。若存在幂函数的主要部分，无穷远处用 $c/x^p$，有限问题点 $a$ 附近用 $c/|x-a|^p$，分别按 $p>1$、$p<1$ 判断。找不到幂函数的主要部分时，可以改用指数函数、对数型函数，或直接找上界、下界（例 11 就是这样）。
3. 内部瑕点两侧分别判断；每段至多保留一个问题端点，所有段都收敛才收敛。

**例 10**　判断 $\int_1^{+\infty}\frac{\mathrm{d}x}{\sqrt{x^3+x}}$ 的敛散。

先看问题点只有无穷远的情形，目标是读出 $p$，再和第 1 节的 $p$ 积分比。

$x\to+\infty$ 时，分母里 $x^3$ 是主要部分，被积函数的主要部分是 $\frac1{x^{3/2}}$，比值 $\frac{1/\sqrt{x^3+x}}{1/x^{3/2}}=\frac1{\sqrt{1+x^{-2}}}\to1$ 确认了这一点。取 $g=\frac1{x^{3/2}}$，$p=\frac32>1$，收敛。直接验证不等式也行：$\sqrt{x^3+x}\ge\sqrt{x^3}$，所以 $\frac1{\sqrt{x^3+x}}\le\frac1{x^{3/2}}$，由比较判别法，收敛。

> 判断 $\int_2^{+\infty}\frac{x\,\mathrm{d}x}{\sqrt{x^3-1}}$ 的敛散。
>
> 答案：主要部分 $\frac{x}{x^{3/2}}=\frac1{x^{1/2}}$，$p=\frac12\le1$。取 $g=\frac1{\sqrt x}$，$\lim\frac fg=\lim\frac{x^{3/2}}{\sqrt{x^3-1}}=1$，发散。

**例 11**　判断 $\int_0^{+\infty}\mathrm{e}^{-x^2}\,\mathrm{d}x$ 的敛散。

和例 10 相比，被积函数不是 $\frac1{x^p}$ 的样子，要改用 $\mathrm{e}^{-x}$ 当尺子。

这个积分只有一个问题点：上限无穷远。把 $[0,1]$ 一段分出去，它是普通的定积分，有限。剩下 $[1,+\infty)$ 上，$x\ge1$ 时 $x^2\ge x$，所以 $\mathrm{e}^{-x^2}\le\mathrm{e}^{-x}$，而 $\int_1^{+\infty}\mathrm{e}^{-x}\,\mathrm{d}x=\mathrm{e}^{-1}$ 收敛，由比较判别法，$\int_1^{+\infty}\mathrm{e}^{-x^2}\,\mathrm{d}x$ 收敛。整个积分收敛。

![$x\ge1$ 时实线 $y=\mathrm{e}^{-x^2}$ 在虚线 $y=\mathrm{e}^{-x}$ 下方：浅灰是 $\int_1^{+\infty}\mathrm{e}^{-x^2}\mathrm{d}x$，被虚线下方（浅灰加斜线阴影，面积 $\mathrm{e}^{-1}$）压住，所以有限；$[0,1]$ 一段是普通的定积分](fig/C12-n3.pdf){width=70%}

它的值是 $\frac{\sqrt\pi}2$，求法要等 C.25.9：把它放进二重积分，用极坐标。这也说明，反常积分收敛，并不保证被积函数有初等原函数。

**例 12**　判断 $\int_0^1\frac{\mathrm{d}x}{\sqrt{x(1-x)}}$ 的敛散，收敛的求值。

和例 10、例 11 相比，问题点换成了两个瑕点。

这一题有两个瑕点：$x=0$ 和 $x=1$。在 $x=\frac12$ 处拆开，两半各含一个。$x\to0^+$ 时，被积函数与 $\frac1{\sqrt x}$ 的比值是 $\frac1{\sqrt{1-x}}\to1$，主要部分是 $\frac1{\sqrt x}$，$p=\frac12<1$，收敛；$x\to1^-$ 时，主要部分是 $\frac1{\sqrt{1-x}}$，$p=\frac12<1$，收敛。所以整个积分收敛。

值可以用 $x=\sin^2t$ 求，$t\in[0,\frac\pi2]$。严格说，要先在 $[\varepsilon,1-\delta]$ 上换元，再令 $\varepsilon,\delta\to0^+$；下面的被积函数换元后是常数 2，极限显然存在，所以直接写结果：$\mathrm{d}x=2\sin t\cos t\,\mathrm{d}t$，$\sqrt{x(1-x)}=\sin t\cos t$，

$$\int_0^1\frac{\mathrm{d}x}{\sqrt{x(1-x)}}=\int_0^{\pi/2}2\,\mathrm{d}t=\pi.$$

**例 13**　$a$ 取什么值时，$\int_0^{+\infty}\frac{\mathrm{d}x}{x^a(1+x)}$ 收敛？

和例 12 相比，两个需要检查的位置不是同一类（一个在零点、一个在无穷远），而且带着参数 $a$。

这一题要分别检查两个位置：$x=0$ 与无穷远。在 $x=1$ 处拆开。

- $x\to0^+$：$a>0$ 时 $x=0$ 是瑕点，$a\le0$ 时可以连续补定义。两种情形都由 $\frac1{x^a}$ 的零点积分统一判断：主要部分是 $\frac1{x^a}$，$p=a$，收敛当且仅当 $a<1$。
- $x\to+\infty$：主要部分是 $\frac1{x^{a+1}}$，在无穷远处 $p=a+1$，收敛当且仅当 $a+1>1$，即 $a>0$。

两段都收敛才行，所以 $0<a<1$。只看一头会错：$a=2$ 时无穷远一头很好，但 $x=0$ 处发散。

**例 14**　求 $I=\int_0^{\pi/2}\ln\sin x\,\mathrm{d}x$。

和例 6 相比，这里不通过求原函数来计算，而是利用 C.11.4 的区间再现，把未知积分本身列入一个等式。

这一题分两步：先确定它收敛，再求值。

先看收敛。瑕点在 $x=0$，那里 $\ln\sin x\to-\infty$，$\sin x\approx x$，应当和例 6 的 $\ln x$ 差不多。严格些，$\sin x$ 在 $[0,\frac\pi2]$ 上的二阶导数 $-\sin x\le0$，曲线位于两端点 $(0,0)$、$(\frac\pi2,1)$ 的连线 $y=\frac{2x}\pi$ 之上，所以 $\frac{2x}\pi\le\sin x\le1$。取对数（$\ln$ 递增）再变号：

$$0\le-\ln\sin x\le\ln\frac\pi{2x}.$$

右边令 $x=\frac\pi2t$，$\int_0^{\pi/2}\ln\frac\pi{2x}\,\mathrm{d}x=\frac\pi2\int_0^1\ln\frac1t\,\mathrm{d}t=\frac\pi2$，用到例 6 的 $\int_0^1\ln t\,\mathrm{d}t=-1$。由比较判别法 $\int_0^{\pi/2}(-\ln\sin x)\,\mathrm{d}x$ 收敛，因此整个 $I$ 收敛。

再求值，用区间再现（C.11.4）。$x\to\frac\pi2-x$ 把 $\sin$ 换成 $\cos$，两个积分相加能凑出 $\sin x\cos x$。令 $x\to\frac\pi2-x$，得 $I=\int_0^{\pi/2}\ln\cos x\,\mathrm{d}x$。两式相加：

$$2I=\int_0^{\pi/2}\ln(\sin x\cos x)\,\mathrm{d}x=\int_0^{\pi/2}\ln\sin2x\,\mathrm{d}x-\frac\pi2\ln2.$$

最后一步用 $\sin x\cos x=\frac12\sin2x$。右边第一项令 $u=2x$：

$$\int_0^{\pi/2}\ln\sin2x\,\mathrm{d}x=\frac12\int_0^{\pi}\ln\sin u\,\mathrm{d}u=\frac12\cdot2I=I.$$

后一个等号是因为 $\sin u$ 关于 $u=\frac\pi2$ 对称，$[0,\pi]$ 上的积分是 $[0,\frac\pi2]$ 上的 2 倍。代回：$2I=I-\frac\pi2\ln2$，所以

$$I=-\frac\pi2\ln2.$$

这里每一步拆开、换元的积分都收敛，所以可以像普通积分一样做。

**绝对收敛。** 被积函数有正有负时，比较判别法不能直接用。如果 $\int|f|$ 收敛，就说 $\int f$ **绝对收敛**，这时 $\int f$ 本身也收敛。证明分三步。

1. 构造非负函数 $h=f+|f|$，则 $0\le h\le2|f|$。
2. 由 $\int|f|$ 收敛，$\int2|f|$ 收敛；由比较判别法，$\int h$ 收敛。
3. 在有限区间上 $f=h-|f|$，两个积分相减，再令端点取极限，两项都有有限极限，所以 $\int f$ 收敛。

反过来不对。$\int_1^{+\infty}\frac{\sin x}x\,\mathrm{d}x$ 收敛，但不绝对收敛，分两步看。

第一步，它收敛。分部一次（$u=\frac1x$，$\mathrm{d}v=\sin x\,\mathrm{d}x$）：

$$\int_1^b\frac{\sin x}x\,\mathrm{d}x=\Big[-\frac{\cos x}x\Big]_1^b-\int_1^b\frac{\cos x}{x^2}\,\mathrm{d}x.$$

$b\to+\infty$ 时边界项趋于 $\cos1$；余项被 $\frac1{x^2}$ 控制（$\big|\frac{\cos x}{x^2}\big|\le\frac1{x^2}$），绝对收敛，所以也收敛。

第二步，$\int_1^{+\infty}\frac{|\sin x|}x\,\mathrm{d}x$ 发散。思路是找一个发散的下界：把 $|\sin x|$ 换成更小的 $\sin^2x$，它能拆成一个像 $\frac1{2x}$ 的发散项和一个收敛项。由 $|\sin x|\ge\sin^2x=\frac{1-\cos2x}2$，

$$\frac{|\sin x|}x\ge\frac1{2x}-\frac{\cos2x}{2x}.$$

在有限区间上积分，

$$\int_1^b\frac{|\sin x|}x\,\mathrm{d}x\ge\frac12\ln b-\int_1^b\frac{\cos2x}{2x}\,\mathrm{d}x.$$

右边第二项有有限极限：令 $u=2x$，它化成 $\frac12\int_2^{2b}\frac{\cos u}u\,\mathrm{d}u$，与第一步是同一类积分，分部一次，边界项趋于常数，余项被 $\frac1{u^2}$ 控制，绝对收敛。而 $\frac12\ln b\to+\infty$，于是 $\int_1^b\frac{|\sin x|}x\,\mathrm{d}x\to+\infty$，$\int_1^{+\infty}\frac{|\sin x|}x\,\mathrm{d}x$ 发散。

这样的积分叫**条件收敛**。

本章新增的关系是：绝对收敛 $\Rightarrow$ 收敛；收敛 $\not\Rightarrow$ 绝对收敛（反例 $\frac{\sin x}x$）。

比较判别法只回答「收不收敛」，给不出值。但有一族积分不但收敛，值还很有规律：例 1 在 $\lambda=1$ 时给出 $1$、$1$，例 9 给出 $2$，已经露出苗头，第 4 节把它追到底。

合上书，叙述比较判别法的极限形式，并用它判断例 13 里两个问题点各自的条件。

### 4. 阶乘能推广到非整数吗？

按已有的定义，$n!$ 定义在非负整数 $n$ 上。能不能找一条光滑的曲线，穿过所有点 $(n+1,\,n!)$，用它定义「$\frac12$ 的阶乘」？欧拉给出的答案是一个积分。

本章的例 1 和例 9 其实已经见过它的样子：

$$\int_0^{+\infty}\mathrm{e}^{-x}\,\mathrm{d}x=1=0!,\qquad \int_0^{+\infty}x\mathrm{e}^{-x}\,\mathrm{d}x=1=1!,\qquad \int_0^{+\infty}x^2\mathrm{e}^{-x}\,\mathrm{d}x=2=2!.$$

猜想 $\int_0^{+\infty}x^n\mathrm{e}^{-x}\,\mathrm{d}x=n!$。把指数推广到实数 $s-1$，并要求积分收敛（下面会看到这要求 $s>0$），就得到：对 $s>0$，定义 **$\Gamma$ 函数**（读作伽马函数）

$$\Gamma(s)=\int_0^{+\infty}x^{s-1}\mathrm{e}^{-x}\,\mathrm{d}x .$$

指数写成 $s-1$ 而不是 $s$，是为了让后面的公式漂亮：$\Gamma(n+1)=n!$。

**它收敛吗？** 积分有两个问题点（$s<1$ 时 $x=0$ 是瑕点，上限是无穷远），在 $x=1$ 处拆开。

- 在 $(0,1]$ 上，$x^{s-1}\mathrm{e}^{-x}$ 与 $x^{s-1}$ 的比值是 $\mathrm{e}^{-x}\to1$，所以这一端收敛当且仅当 $x^{s-1}$ 的零点积分收敛，即 $p=1-s<1$，$s>0$。
- 在 $[1,+\infty)$ 上，$x^2\cdot x^{s-1}\mathrm{e}^{-x}=x^{s+1}\mathrm{e}^{-x}\to0$（指数比任何幂增长得快），所以对每个固定实数 $s$，充分大的 $x$ 处 $x^{s-1}\mathrm{e}^{-x}\le\frac1{x^2}$，收敛。

所以 $s>0$ 时 $\Gamma(s)$ 有定义，这就是 $s>0$ 这个条件的来由；$s\le0$ 时在 0 附近至少和 $\frac1x$ 一样大，发散。

**递推公式。** 对 $\Gamma(s+1)=\int_0^{+\infty}x^s\mathrm{e}^{-x}\,\mathrm{d}x$ 分部，取 $u=x^s$，$\mathrm{d}v=\mathrm{e}^{-x}\mathrm{d}x$：

$$\Gamma(s+1)=\big[-x^s\mathrm{e}^{-x}\big]_0^{+\infty}+s\int_0^{+\infty}x^{s-1}\mathrm{e}^{-x}\,\mathrm{d}x=s\,\Gamma(s).$$

边界项为 0：$x\to+\infty$ 时 $x^s\mathrm{e}^{-x}\to0$，$x\to0^+$ 时 $x^s\to0$（$s>0$）。再加上 $\Gamma(1)=\int_0^{+\infty}\mathrm{e}^{-x}\,\mathrm{d}x=1$，从 $\Gamma(1)$ 起一步步推：

$$\Gamma(n+1)=n\,\Gamma(n)=n(n-1)\Gamma(n-1)=\cdots=n!\,\Gamma(1)=n!.$$

![$\Gamma(s)$ 的曲线（实线）穿过点 $(1,1)$、$(2,1)$、$(3,2)$、$(4,6)$、$(5,24)$（实心点），即 $\Gamma(n+1)=n!$；虚线标出 $s=\frac12$ 处的值 $\Gamma(\frac12)=\sqrt\pi\approx1.7725$，$s\to0^+$ 时曲线冲向无穷](fig/C12-n4.pdf){width=70%}

这条曲线正是欧拉要找的光滑曲线，它穿过所有的 $(n+1,n!)$。$\frac12$ 的阶乘定义为 $\Gamma(\frac32)$。

**$\Gamma(\frac12)$ 的值。** 令 $x=t^2$，$\mathrm{d}x=2t\,\mathrm{d}t$：

$$\Gamma\Big(\frac12\Big)=\int_0^{+\infty}x^{-1/2}\mathrm{e}^{-x}\,\mathrm{d}x=2\int_0^{+\infty}\mathrm{e}^{-t^2}\,\mathrm{d}t.$$

右边的 $\int_0^{+\infty}\mathrm{e}^{-t^2}\mathrm{d}t$ 正是例 11 的积分，值为 $\frac{\sqrt\pi}2$，再乘前面的系数 2 得 $\sqrt\pi$。这个值本章先拿来用，它的求法（二重积分加极坐标）在 C.25.9。有了 $\Gamma(\frac12)=\sqrt\pi$，递推给出全部半整数处的值：$\Gamma(\frac32)=\frac12\sqrt\pi$，$\Gamma(\frac52)=\frac32\cdot\frac12\sqrt\pi=\frac34\sqrt\pi$。

概率里的 $\chi^2$ 分布和 $t$ 分布，密度函数里都带一个含 $\Gamma$ 的系数，作用是使曲线下的总面积等于 1（和例 4 里的系数 2 同理，见 P.10.4、P.10.6），这是 $\Gamma$ 今天最常见的用处。

**方法 4（用 $\Gamma$ 函数算积分）**

1. 对 $\int_0^{+\infty}x^\alpha\mathrm{e}^{-\beta x^k}\,\mathrm{d}x$，本方法先讨论 $\beta>0$、$k>0$ 的情形。零点附近要求 $\alpha>-1$；无穷远处由指数衰减保证收敛。
2. 令 $t=\beta x^k$，则 $x=(t/\beta)^{1/k}$，$\mathrm{d}x=\frac1k\beta^{-1/k}t^{1/k-1}\,\mathrm{d}t$，因而

$$\int_0^{+\infty}x^\alpha\mathrm{e}^{-\beta x^k}\,\mathrm{d}x=\frac1k\beta^{-(\alpha+1)/k}\,\Gamma\Big(\frac{\alpha+1}k\Big).$$

3. 令 $s=\frac{\alpha+1}k$。$s$ 是正整数或正半整数时，用 $\Gamma(s+1)=s\Gamma(s)$ 递推到 $\Gamma(1)$ 或 $\Gamma(\frac12)$；其他 $s>0$ 保留为 $\Gamma(s)$，本章不要求把它化成初等常数。

**例 15**　求 $\int_0^{+\infty}x^3\mathrm{e}^{-2x}\,\mathrm{d}x$。

例 9 的 $\int x^n\mathrm{e}^{-x}$ 就是 $\Gamma(n+1)$。现在指数里多了系数 2，用换元把它变回去。

令 $t=2x$，$x=\frac t2$，$\mathrm{d}x=\frac{\mathrm{d}t}2$：

$$\int_0^{+\infty}\Big(\frac t2\Big)^3\mathrm{e}^{-t}\frac{\mathrm{d}t}2=\frac1{2^4}\Gamma(4)=\frac{3!}{16}=\frac38.$$

> 求 $\int_0^{+\infty}x^4\mathrm{e}^{-x/3}\,\mathrm{d}x$。
>
> 答案：$t=\frac x3$，$x=3t$，积分 $=3^5\int_0^{+\infty}t^4\mathrm{e}^{-t}\,\mathrm{d}t=243\cdot4!=5832$。

**例 16**　求 $\int_0^{+\infty}x^3\mathrm{e}^{-x^2}\,\mathrm{d}x$ 和 $\int_0^{+\infty}x^2\mathrm{e}^{-x^2}\,\mathrm{d}x$。

和例 15 相比，指数里是 $x^2$ 而不是 $x$。先取实数 $m>-1$（零点附近要求 $m>-1$，无穷远处由指数衰减保证收敛）。令 $t=x^2$，$x=\sqrt t$，$\mathrm{d}x=\frac{\mathrm{d}t}{2\sqrt t}$：

$$\int_0^{+\infty}x^m\mathrm{e}^{-x^2}\,\mathrm{d}x=\frac12\int_0^{+\infty}t^{(m-1)/2}\mathrm{e}^{-t}\,\mathrm{d}t=\frac12\Gamma\Big(\frac{m+1}2\Big).$$

$m=3$ 时是 $\frac12\Gamma(2)=\frac12$；$m=2$ 时是 $\frac12\Gamma(\frac32)=\frac{\sqrt\pi}4$，用到了 $\Gamma(\frac12)=\sqrt\pi$。

**例 17**　求 $\Gamma\big(\frac72\big)$。

和例 15、例 16 相比，这一题不用积分，只用 $\Gamma$ 的递推。

连续用 $\Gamma(s+1)=s\Gamma(s)$，每次下降 1，落到 $\frac12$：

$$\Gamma\Big(\frac72\Big)=\frac52\cdot\frac32\cdot\frac12\,\Gamma\Big(\frac12\Big)=\frac{15}8\sqrt\pi.$$

**例 18**　证明 $\int_0^1\big(\ln\frac1x\big)^n\,\mathrm{d}x=n!$（$n$ 为正整数）。

和例 15、例 16 相比，被积函数含对数，要先换元变成 $\Gamma$。

这个形式也能通过换元化成 $\Gamma$ 函数。$x=0$ 是瑕点（$\ln\frac1x\to+\infty$），要把它换成 $\Gamma$。令 $x=\mathrm{e}^{-t}$，则 $\ln\frac1x=t$，$\mathrm{d}x=-\mathrm{e}^{-t}\mathrm{d}t$；$x:0\to1$ 对应 $t:+\infty\to0$：

$$\int_0^1\Big(\ln\frac1x\Big)^n\mathrm{d}x=\int_{+\infty}^0t^n\cdot(-\mathrm{e}^{-t})\,\mathrm{d}t=\int_0^{+\infty}t^n\mathrm{e}^{-t}\,\mathrm{d}t=\Gamma(n+1)=n!.$$

瑕点换成了无穷远，一个有限区间上的积分换成了无穷区间上的积分。

回到开头的问题。永续年金的现值是 20000 元（例 3），顾客的平均间隔是半小时（例 4），最后一个是正态曲线下的总面积为什么刚好是 1。标准正态曲线是 $\frac1{\sqrt{2\pi}}\mathrm{e}^{-x^2/2}$，系数里的 $\sqrt{2\pi}$ 要等于 $\int_{-\infty}^{+\infty}\mathrm{e}^{-x^2/2}\,\mathrm{d}x$。被积函数是偶函数，$x\ge1$ 时 $\mathrm{e}^{-x^2/2}\le\mathrm{e}^{-x/2}$，两半都收敛（同例 11），所以它是 $2\int_0^{+\infty}\mathrm{e}^{-x^2/2}\,\mathrm{d}x$。用方法 4，$\alpha=0$，$\beta=\frac12$，$k=2$：

$$\int_0^{+\infty}\mathrm{e}^{-x^2/2}\,\mathrm{d}x=\frac12\Big(\frac12\Big)^{-1/2}\Gamma\Big(\frac12\Big)=\frac{\sqrt2}2\sqrt\pi=\sqrt{\frac\pi2}.$$

整条曲线下的面积是 $\frac1{\sqrt{2\pi}}\cdot2\sqrt{\frac\pi2}=1$。系数 $\frac1{\sqrt{2\pi}}$ 正是为了把积分值 $\sqrt{2\pi}$ 约成 1（这里用到的 $\Gamma(\frac12)=\sqrt\pi$ 来自 C.25.9）。

合上书，推出 $\Gamma(s+1)=s\Gamma(s)$（分部积分，边界项为什么为 0），并由它写出 $\Gamma(n+1)=n!$。

### 本章小结

| 方法 | 什么时候用 | 对应题号 |
|---|---|---|
| 方法 1（无穷区间） | 上限或下限是 $\pm\infty$：积到 $b$ 再取极限；$p$ 积分 $\int_1^{+\infty}x^{-p}$ 当 $p>1$ 收敛 | C12-01、C12-02、C12-05、C12-06、C12-11、C12-12 |
| 方法 2（瑕积分） | 被积函数在某点无界：避开瑕点再取极限，内部瑕点要拆开；$\int_0^1x^{-p}$ 当 $p<1$ 收敛 | C12-02、C12-03、C12-07、C12-10、C12-11、C12-12 |
| 方法 3（比较判别法） | 求不出原函数：找问题点附近的主要部分 $\frac c{x^p}$，与 $p$ 积分比较；内部瑕点两侧分别判断、每段至多一个问题端点；绝对收敛 $\Rightarrow$ 收敛 | C12-05、C12-07、C12-08、C12-09、C12-10、C12-11、C12-12 |
| 方法 4（$\Gamma$ 函数） | $x^{\alpha}\mathrm{e}^{-\beta x^k}$ 型积分，换元成 $\Gamma(s)$（$\beta>0$、$k>0$、$\alpha>-1$）；$\Gamma(s+1)=s\Gamma(s)$，$\Gamma(n+1)=n!$（$n=0,1,2,\dots$），$\Gamma(\frac12)=\sqrt\pi$ | C12-04、C12-08、C12-12 |

章末混合练习 C12-13 至 C12-15 混入前面各章的内容，要先认出该用哪一种方法。

本章在主线上的位置：定积分是「切细了再加起来」的极限；本章问的是，区间伸到无穷远、或者函数冲向无穷大时，这个极限还在不在。办法是先在有限处用牛顿–莱布尼茨公式，再取极限，所以 C.11 的换元、分部等计算方法都能用上。

**谁推出谁**（沿用 C.9、C.10 的关系图，标出本章新增）：

$$\text{在有限闭区间上连续}\Rightarrow\text{在该区间上可积（C.9）},\qquad \text{绝对收敛}\ \overset{\text{本章新增}}{\Longrightarrow}\ \text{收敛},\qquad \text{收敛}\ \overset{\text{本章新增}}{\not\Longrightarrow}\ \text{绝对收敛}.$$

最后一个箭头不成立的标准反例是 $\int_1^{+\infty}\frac{\sin x}x\,\mathrm{d}x$（条件收敛）。另外，反常积分收敛，并不保证被积函数有初等原函数：$\int_0^{+\infty}\mathrm{e}^{-x^2}\mathrm{d}x$ 收敛，原函数却不是初等函数。
