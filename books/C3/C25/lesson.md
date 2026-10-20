## C.25 · 二重积分

一场暴雨过后，气象站只有几处雨量计的读数，每个地方的雨深不一样。要知道一个县总共下了多少水，就得把整个县的雨深按面积累加。城市规划里算一座城市有多少人口，是把各处的人口密度按面积累加。概率里也一样：两个随机量同时落进某个区域的概率，是密度函数在这块区域上的累加；正态分布前面那个常数 $\frac1{\sqrt{2\pi}}$，也要靠一块平面区域上的累加才能算出来（第 9 节）。

这种「对一块平面区域按面积累加」的运算，就是二重积分。一元的定积分是把区间切成小段、每段当矩形、再加起来，二重积分把区间换成平面区域、小段换成小块，其余的想法一字不改。一元积分只会沿一条线累加，面对一块平面区域，旧办法没有现成的算法。后来逐步形成了两个关键办法：把区域一层层切成薄片，每片是一个一元积分，于是二重积分化成两次一元积分（第 4 到 6 节）；以及换变量，把难算的区域换成好算的（第 8、10 节）。本章结尾会回到开头的雨量问题，把它算出来。

本章的顺序是这样的。第 1、2、3 节给出定义、性质和平均值；第 4 到 7 节讲怎样用两次定积分把它算出来，包括积分限怎么定、次序怎么换、对称性怎样省事；第 8 节换到极坐标，第 9 节用它算出一个积不出原函数的积分；第 10 节讲一般的换变量；第 11 节讲积分里带参数时的求导。

### 1. 一块区域上随位置变化的量，总共有多少？

设平面上有一块有界闭区域 $D$（有界：能装进一个足够大的圆里；闭：包含它自己的边界），每一点 $(x,y)$ 处有一个量 $f(x,y)\ge0$，比如雨深（毫米）或人口密度（人/平方千米）。总量怎么算？

量如果处处相等，总量就是「值乘面积」。现在 $f$ 随位置变化，沿用一元积分的办法，分四步：

1. **分割**：把 $D$ 分成 $n$ 个小块，面积分别是 $\Delta\sigma_1,\dots,\Delta\sigma_n$；
2. **近似**：每一小块里取一点 $(\xi_i,\eta_i)$，小块上的量当作处处等于 $f(\xi_i,\eta_i)$，小块上的总量约为 $f(\xi_i,\eta_i)\Delta\sigma_i$；
3. **求和**：$\sum_{i=1}^nf(\xi_i,\eta_i)\Delta\sigma_i$；
4. **取极限**：小块越分越细（每个小块的直径，也就是块内两点最远的距离，最大的那个趋于 0），看这个和有没有极限。

极限存在，并且与怎么分割、怎么取点都无关，就称为 $f$ 在 $D$ 上的**二重积分**，记作

$$\iint_Df(x,y)\,\mathrm d\sigma=\lim_{\lambda\to0}\sum_{i=1}^nf(\xi_i,\eta_i)\,\Delta\sigma_i ,$$

$\lambda$ 是最大的小块直径，$\mathrm d\sigma$ 叫面积元，在直角坐标下也写成 $\mathrm dx\,\mathrm dy$。$f$ 在有界闭区域 $D$ 上连续（边界是分段光滑的曲线）时，二重积分一定存在：分得很细的小块上 $f$ 变化很小，块里取哪一点对和几乎没有影响，所以和趋于同一个极限，与分割、取点无关。

以上先按 $f\ge0$ 讲。对一般的有界函数，令 $f^+=\max(f,0)$，$f^-=\max(-f,0)$（$f=f^+-f^-$，两个都 $\ge0$），若两者的二重积分都存在，就定义 $\iint_Df=\iint_Df^+-\iint_Df^-$。本章用到的区域和连续函数都满足这一条件，下面的性质对可正可负的 $f$ 同样成立。

几何上，$f\ge0$ 时 $z=f(x,y)$ 是 $D$ 上方的一张曲面，每一项 $f(\xi_i,\eta_i)\Delta\sigma_i$ 是一根小柱体的体积，所以二重积分是以 $D$ 为底、曲面为顶的**曲顶柱体的体积**。取 $f\equiv1$，每项就是 $\Delta\sigma_i$，二重积分等于区域 $D$ 的面积 $\sigma$。

拿老朋友之一的碗 $f=x^2+y^2$ 试一试，区域是单位正方形 $D=[0,1]\times[0,1]$。把它分成 $n\times n$ 个边长 $\frac1n$ 的小方块，每块取右上角的点，$\Delta\sigma=\frac1{n^2}$：

$$\sum=\frac1{n^2}\sum_{i=1}^n\sum_{j=1}^n\Big(\frac{i^2}{n^2}+\frac{j^2}{n^2}\Big).$$

对 $j$ 求和时 $i^2$ 出现 $n$ 次，对 $i$ 求和时 $j^2$ 出现 $n$ 次，两部分相同，所以

$$\sum=\frac1{n^4}\cdot2n\sum_{i=1}^ni^2=\frac2{n^3}\cdot\frac{n(n+1)(2n+1)}6=\frac{(n+1)(2n+1)}{3n^2}.$$

| $n$ | 2 | 4 | 10 | 100 |
|---|---|---|---|---|
| 和 | 1.25 | 0.9375 | 0.77 | 0.6767 |

分得越细，和越接近 $\frac23\approx0.6667$，这就是碗在单位正方形上方的体积。第 4 节会用另一条路径算出同样的 $\frac23$。

![把单位正方形分成 $4\times4$ 个小块，以 $f=x^2+y^2$ 在每块右上角的值为高作小柱体（柱顶用浅灰填充），所有小柱体体积之和是 0.9375；虚线是曲面沿网格线的截线，分得越细，柱体的总体积越接近曲顶柱体的体积 $\frac23$](fig/C25-n1.pdf){width=72%}

**例 1**　设 $D=[0,2]\times[0,2]$，$f=x+y$。把 $D$ 分成 $2\times2$ 个边长为 1 的小方块，分别取右上角和中心作为 $(\xi_i,\eta_i)$，算出两个和，再和精确值比较。

右上角的点是 $(1,1),(2,1),(1,2),(2,2)$，函数值 $2,3,3,4$，每块面积 1，和为 $12$。

中心的点是 $(0.5,0.5),(1.5,0.5),(0.5,1.5),(1.5,1.5)$，函数值 $1,2,2,3$，和为 $8$。

精确值分三步看。

第一步，补成长方体：平面 $z=x+y$ 在 $D$ 上从高 $0$ 升到 $4$，把立体补成 $[0,2]^2\times[0,4]$ 的长方体（体积 16），平面过它的中心 $(1,1,2)$。

第二步，写出对称：把长方体绕中心转半圈，即 $(x,y,z)\mapsto(2-x,2-y,4-z)$。平面上的点满足 $z=x+y$，像点满足 $4-z=(2-x)+(2-y)$，即 $z'=x'+y'$，所以平面被送回它自己。

第三步，两半互换：平面下方的部分被送到平面上方，两部分体积相等，所以曲顶柱体体积是 $16\div2=8$。

取中心点时恰好得到精确值。原因在每个小方块内部：以中心为界，$x$ 方向左右各偏离 $\pm0.5$，$y$ 方向上下也各偏离 $\pm0.5$，线性函数 $x+y$ 的这些偏差成对抵消，所以块内的平均值就等于中心处的值。取右上角时，每块取到的都是块内的最大值，和就偏大。对一般的 $f$，细分以后两种取法的和都趋于同一个极限，这才是定义要求的。

> 设 $D=[0,1]\times[0,1]$，$f=xy$，分成 $2\times2$ 块，取右上角，求和。
>
> 答案：右上角是 $(\frac12,\frac12),(1,\frac12),(\frac12,1),(1,1)$，函数值 $\frac14,\frac12,\frac12,1$，每块面积 $\frac14$，和 $=\frac14\cdot\frac94=\frac9{16}$。

合上书，写出二重积分定义的四步，并说明 $f\ge0$ 时它的几何意义。

### 2. 二重积分有哪些和定积分一样的性质？

先看例 1 的 $f=x+y$ 和 $g=x+y+1$ 在右上角取点的和：$f$ 的四个值是 $2,3,3,4$，$g$ 的是 $3,4,4,5$，和分别是 12 和 16。多出的 4 正是常数 1 的和（四块，每块面积 1），而且 $g$ 逐块都不小于 $f$，和也不小。黎曼和的加法、数乘和大小比较都是这样逐项成立的，取极限以后仍然保留。设下面各个积分都存在。

1. **线性**：$\iint_D(af+bg)\,\mathrm d\sigma=a\iint_Df\,\mathrm d\sigma+b\iint_Dg\,\mathrm d\sigma$；
2. **对区域可加**：$D$ 分成两块 $D_1,D_2$（只在边界上相接，没有重叠的部分，边界上共享一条线是允许的），则 $\iint_D=\iint_{D_1}+\iint_{D_2}$；
3. **面积**：$\iint_D1\,\mathrm d\sigma=\sigma$（$D$ 的面积）；
4. **比较**：在 $D$ 上 $f\le g$，则 $\iint_Df\,\mathrm d\sigma\le\iint_Dg\,\mathrm d\sigma$；特别地 $\big|\iint_Df\,\mathrm d\sigma\big|\le\iint_D|f|\,\mathrm d\sigma$；
5. **估值**：在 $D$ 上 $m\le f\le M$，则 $m\sigma\le\iint_Df\,\mathrm d\sigma\le M\sigma$。

第 5 条由第 4 条和第 3 条得到：对 $m\le f\le M$ 两边积分，常数的积分是「常数乘面积」。它的画面是：曲顶柱体的体积夹在最矮的平顶柱体和最高的平顶柱体之间。

**方法 1（用性质估值与比较）**　要估计一个积不出的二重积分，先在区域上找 $f$ 的最小值 $m$ 和最大值 $M$，再用 $m\sigma$、$M\sigma$ 夹住；要比较两个积分的大小，比较两个被积函数在区域上的大小，注意是在**这块区域上**比较。

**例 2**　估计 $I=\iint_D(x+y+10)\,\mathrm d\sigma$ 的范围，$D$ 是圆盘 $x^2+y^2\le4$。

不求精确值，只用被积函数在区域上的最小值和最大值夹出范围。

先在 $D$ 上求 $x+y$ 的范围。由 $(x-y)^2\ge0$ 得 $2xy\le x^2+y^2$，所以 $(x+y)^2\le2(x^2+y^2)\le8$（$D$ 上 $x^2+y^2\le4$），有 $|x+y|\le2\sqrt2$，所以 $10-2\sqrt2\le f\le10+2\sqrt2$。面积 $\sigma=4\pi$，所以

$$4\pi(10-2\sqrt2)\le I\le4\pi(10+2\sqrt2),\qquad\text{即}\quad90.1\le I\le161.2 .$$

估值只给范围。这个积分的精确值是 $40\pi\approx125.7$，第 7 节用对称性可以算出。

> 估计 $\iint_D(x^2+y^2+1)\,\mathrm d\sigma$，$D$ 是单位圆盘 $x^2+y^2\le1$。
>
> 答案：$D$ 上 $1\le x^2+y^2+1\le2$，面积 $\pi$，所以 $\pi\le I\le2\pi$。

**例 3**　设 $I_1=\iint_{D_1}(x+y)^2\,\mathrm d\sigma$，$I_2=\iint_{D_1}(x+y)^3\,\mathrm d\sigma$，其中 $D_1$ 由 $x\ge0$，$y\ge0$，$x+y\le1$ 围成。再设 $I_3=\iint_{D_2}(x+y)^2\,\mathrm d\sigma$，$I_4=\iint_{D_2}(x+y)^3\,\mathrm d\sigma$，其中 $D_2$ 是圆盘 $(x-2)^2+(y-1)^2\le2$。比较 $I_1,I_2$ 与 $I_3,I_4$ 的大小。

和例 2 不同，这里不夹范围，只比较两个积分谁大；被积函数相同、区域不同，要在各自的区域上比较。

在 $D_1$ 上 $0\le x+y\le1$，所以 $(x+y)^3\le(x+y)^2$，$I_2\le I_1$。

在 $D_2$ 上，圆心 $(2,1)$，半径 $\sqrt2$。$x+y$ 沿圆心到边界的方向 $(1,1)/\sqrt2$ 变化最快，最小值是 $3-\sqrt2\cdot\sqrt2=1$，理由：$x+y=3+(x-2)+(y-1)$，而向量 $\boldsymbol a=(x-2,y-1)$ 的长度 $\lVert\boldsymbol a\rVert\le\sqrt2$（双竖线表示向量的长度），它与 $(1,1)$ 的点积不小于 $-\sqrt2\cdot\sqrt2=-2$，所以 $x+y\ge1$，$(x+y)^3\ge(x+y)^2$，$I_4\ge I_3$。

同样两个被积函数，在 $D_1$ 上三次方小，在 $D_2$ 上三次方大，大小关系反过来，取决于 $x+y$ 与 1 的大小。

> 设 $D$ 是 $|x|+|y|\le1$，比较 $\iint_D(x^2+y^2)\,\mathrm d\sigma$ 与 $\iint_D\sqrt{x^2+y^2}\,\mathrm d\sigma$ 的大小。
>
> 答案：在 $D$ 上 $x^2+y^2\le(|x|+|y|)^2\le1$，所以 $x^2+y^2\le\sqrt{x^2+y^2}$，前者的积分不大于后者。

这几条性质只能夹出范围或比较大小，还说不出积分到底是多少。下一节先看一个比积分本身更直观的量，区域上的平均值。

合上书，说出估值性质是怎样从比较性质和面积性质得到的。

### 3. 一块区域上的平均值是多少？

一元时，$f$ 在 $[a,b]$ 上的平均值是 $\frac1{b-a}\int_a^bf\,\mathrm dx$（C.9）。二重积分也一样，以 $x^2$ 在 $[0,1]$ 上的平均值 $\frac13$ 为例：积分 $\frac13$ 除以长度 1。

设 $D$ 的面积为 $\sigma>0$。把 $D$ 分成 $n$ 块面积相等的小块，各取一点，$n$ 个函数值的平均是 $\frac1n\sum f(\xi_i,\eta_i)=\frac1\sigma\sum f(\xi_i,\eta_i)\Delta\sigma$，右边的和趋于二重积分。所以称

$$\bar f=\frac1\sigma\iint_Df(x,y)\,\mathrm d\sigma$$

为 $f$ 在 $D$ 上的**平均值**。它的几何意义：曲顶柱体的体积除以底面积，就是把曲顶抹平以后的高度。

一元时平均值一定被取到。二元也一样。

**二重积分中值定理**　若 $f$ 在连通的有界闭区域 $D$（面积 $\sigma>0$，连通指 $D$ 是一整块）上连续，则存在 $(\xi,\eta)\in D$，使

$$\iint_Df\,\mathrm d\sigma=f(\xi,\eta)\,\sigma .$$

**证明**

1. 由最值定理（C.20.3），$f$ 在 $D$ 上有最小值 $m$ 和最大值 $M$；
2. 由估值性质，$m\sigma\le\iint_Df\,\mathrm d\sigma\le M\sigma$，除以 $\sigma$ 得 $m\le\bar f\le M$；
3. 由介值定理（C.20.3），$f$ 在 $D$ 上取遍 $m$ 与 $M$ 之间的值，所以有 $(\xi,\eta)\in D$ 使 $f(\xi,\eta)=\bar f$。$\blacksquare$

连通这个条件去掉就不成立：$D$ 是两个相距很远的面积相同的小圆盘，$f$ 在一个圆盘上取 1，在另一个上取 3，$f$ 在 $D$ 上仍然连续，平均值是 2，却没有一点的函数值是 2。

**方法 2（区域上的平均值与中值定理）**　求平均值就是算出积分再除以面积。题目里出现「积分除以面积」并且让区域缩成一点，就用中值定理把它换成一个函数值，再用连续性取极限。

**例 4**　求 $f=\sqrt{1-x^2-y^2}$ 在单位圆盘 $D:x^2+y^2\le1$ 上的平均值。

选一个图像就是半个球的函数，积分可以当成体积直接读出来，不用先学计算方法。

被积函数的图像是单位球的上半部分，所以 $\iint_Df\,\mathrm d\sigma$ 是半个单位球的体积 $\frac12\cdot\frac43\pi=\frac{2\pi}3$（球的体积公式由 C.13 的截面法得到）。面积 $\sigma=\pi$，平均值 $\bar f=\frac23$。

平均值 $\frac23$ 小于最大值 1，这符合预期：曲面在中心最高，向边缘降到 0。

> 求 $f=1-\sqrt{x^2+y^2}$ 在单位圆盘上的平均值。
>
> 答案：图像是底面半径 1、高 1 的圆锥，体积 $\frac13\pi\cdot1^2\cdot1=\frac\pi3$，面积 $\pi$，平均值 $\frac13$。

**例 5**　求 $\displaystyle\lim_{r\to0^+}\frac1{\pi r^2}\iint_{x^2+y^2\le r^2}\mathrm e^{x^2-y^2}\cos(x+y)\,\mathrm d\sigma$。

和例 4 不同，这里不要算积分。被积函数积不出来，但这个式子正是函数在小圆盘上的平均值。

由中值定理，它等于 $\mathrm e^{\xi^2-\eta^2}\cos(\xi+\eta)$，$(\xi,\eta)$ 在半径为 $r$ 的圆盘里。$r\to0^+$ 时 $(\xi,\eta)\to(0,0)$，被积函数连续，所以极限是它在原点的值 $\mathrm e^0\cos0=1$。

$(\xi,\eta)$ 随 $r$ 变，我们不知道它具体在哪，但它被困在越缩越小的圆盘里，这就够了。

> 求 $\displaystyle\lim_{r\to0^+}\frac1{\pi r^2}\iint_{x^2+y^2\le r^2}\frac{x+2}{y^2+1}\,\mathrm d\sigma$。
>
> 答案：被积函数连续，极限是原点处的值 $\frac{0+2}{0+1}=2$。

平均值和中值定理告诉我们积分总对应一个合理的值，但怎样把它算出来还没有办法。下一节找一条能算出数的路。

合上书，写出中值定理的三步证明，说出每一步用了本章的哪条性质或哪个定理。

### 4. 矩形区域上的二重积分，怎样化成两次定积分？

定义是四步，算起来却没法照做。一元时有牛顿–莱布尼茨公式（C.10）；二元要把它化回一元。想法来自 C.13 的截面法：体积等于截面面积沿一个方向的积分。

先拿例 1 的 $f=x+y$ 在 $[0,2]^2$ 上试。用平面 $x=x_0$ 去切，截面是 $y$ 从 0 到 2 的一块，面积 $\int_0^2(x_0+y)\,\mathrm dy=2x_0+2$；$x_0$ 从 0 走到 2，把截面面积积起来，$\int_0^2(2x+2)\,\mathrm dx=8$，正是例 1 用对称算出的精确值。下面把这个做法写成一般公式。

设 $D=[a,b]\times[c,d]$ 是矩形，$f\ge0$ 连续。用垂直于 $x$ 轴的平面 $x=x_0$ 切曲顶柱体，截面是 $y$ 从 $c$ 到 $d$、曲线 $z=f(x_0,y)$ 下面的一块，面积是一个一元定积分

$$A(x_0)=\int_c^df(x_0,y)\,\mathrm dy .$$

![用平面 $x=x_0$ 切曲顶柱体，图中用宽度 $\mathrm dx$ 的薄片（阴影）示意，在 $x=x_0$ 处的截面面积是 $A(x_0)=\int_c^df(x_0,y)\,\mathrm dy$；$x_0$ 从 $a$ 走到 $b$，截面扫过整个立体，体积是 $\int_a^bA(x)\,\mathrm dx$](fig/C25-n2.pdf){width=70%}

$x_0$ 从 $a$ 走到 $b$，截面扫过整个立体，体积就是 $\int_a^bA(x)\,\mathrm dx$。所以

$$\iint_Df\,\mathrm d\sigma=\int_a^b\Big(\int_c^df(x,y)\,\mathrm dy\Big)\mathrm dx=\int_a^b\mathrm dx\int_c^df(x,y)\,\mathrm dy .$$

到这里只做了一件事：体积等于截面面积沿 $x$ 方向的积分。右边叫**累次积分**：先算里面一层，把 $x$ 当作常数、对 $y$ 积分，得到 $x$ 的函数 $A(x)$，再对 $x$ 积分。改用垂直于 $y$ 轴的平面切，得到另一个次序：

$$\iint_Df\,\mathrm d\sigma=\int_c^d\mathrm dy\int_a^bf(x,y)\,\mathrm dx .$$

两个次序算的是同一个体积，所以对连续函数两种次序的结果相等（这个结论叫富比尼定理，上面是它的几何理由）。$f$ 取负值时，定理仍然成立：把 $f$ 写成正部 $f^+=\max(f,0)$ 减去负部 $f^-=\max(-f,0)$，两个都 $\ge0$，各自用上面的几何理由，再由线性性质合并。

回到老朋友碗 $f=x^2+y^2$ 在 $[0,1]^2$ 上：

$$A(x)=\int_0^1(x^2+y^2)\,\mathrm dy=x^2+\frac13,\qquad\iint_D=\int_0^1\Big(x^2+\frac13\Big)\mathrm dx=\frac13+\frac13=\frac23 .$$

和第 1 节的数值表一致。

被积函数是 $\alpha(x)\beta(y)$ 的乘积、区域是矩形时，里层 $\int\beta(y)\,\mathrm dy$ 是常数，可以提到外面，二重积分等于两个一元积分的乘积：

$$\iint_{[a,b]\times[c,d]}\alpha(x)\beta(y)\,\mathrm d\sigma=\int_a^b\alpha(x)\,\mathrm dx\cdot\int_c^d\beta(y)\,\mathrm dy .$$

**方法 3（矩形上的累次积分）**

1. 选一个次序，先把里层的另一个变量当常数，求一元积分；
2. 再对外层变量积分；
3. 里层的原函数难求时，考虑换次序。

**例 6**　计算 $\displaystyle\iint_D(x+2y)\,\mathrm d\sigma$，$D=[0,2]\times[0,1]$。

这里把例 1 的 $x+y$ 换成 $x+2y$，区域换成长方形，做法同上；被积函数是简单的多项式，两个次序都好算，所以可以互相验算。

先对 $y$ 积分，把 $x$ 当常数：

$$\int_0^1(x+2y)\,\mathrm dy=\Big[xy+y^2\Big]_{y=0}^{y=1}=x+1 .$$

再对 $x$ 积分：

$$\int_0^2(x+1)\,\mathrm dx=\Big[\frac{x^2}2+x\Big]_0^2=4 .$$

用另一个次序验算：$\int_0^2(x+2y)\,\mathrm dx=2+4y$，$\int_0^1(2+4y)\,\mathrm dy=4$。

> 计算 $\iint_D(3x+y)\,\mathrm d\sigma$，$D=[0,1]\times[0,2]$。
>
> 答案：$\int_0^2(3x+y)\,\mathrm dy=6x+2$，$\int_0^1(6x+2)\,\mathrm dx=5$。

**例 7**　计算 $\displaystyle\iint_D x\,\mathrm e^{xy}\,\mathrm d\sigma$，$D=[0,1]\times[0,1]$。

和例 6 不同，两个次序的难度不一样，所以要选。

先对 $y$ 积分，$x$ 是常数，$\mathrm e^{xy}$ 对 $y$ 的原函数是 $\frac1x\mathrm e^{xy}$，乘上前面的 $x$ 正好抵消：

$$\int_0^1x\,\mathrm e^{xy}\,\mathrm dy=\mathrm e^{xy}\Big|_{y=0}^{y=1}=\mathrm e^x-1 .$$

再对 $x$ 积分：

$$\int_0^1(\mathrm e^x-1)\,\mathrm dx=\mathrm e-2 .$$

如果先对 $x$ 积分，$\int_0^1x\,\mathrm e^{xy}\,\mathrm dx$ 要用分部积分，结果带着 $\frac1y$ 和 $\frac1{y^2}$，下一步积分就很难了。次序选对，几步就完。

> 计算 $\iint_D y\,\mathrm e^{xy}\,\mathrm d\sigma$，$D=[0,1]\times[0,2]$。
>
> 答案：先对 $x$ 积分，$\int_0^1y\,\mathrm e^{xy}\,\mathrm dx=\mathrm e^y-1$，再 $\int_0^2(\mathrm e^y-1)\,\mathrm dy=\mathrm e^2-3$。

矩形的积分限都是常数，真实的区域边界常常是曲线。下一节看积分限怎样随位置变化。

合上书，用「截面面积再积分」推出累次积分公式，并说明为什么次序可以交换。

### 5. 区域的边界是曲线时，积分上下限怎么定？

矩形的上下限都是常数，一般的区域不是。拿第 4 节的做法试一个三角形 $x\ge0,\ y\ge0,\ x+y\le1$：用 $x=0.5$ 切，截面是 $y$ 从 0 到 0.5 的一段；用 $x=0.2$ 切，是 $y$ 从 0 到 0.8 的一段。截面的上端随 $x$ 变，等于 $1-x$。这样的区域有一般的写法。设区域 $D$ 夹在两条竖直线 $x=a$ 和 $x=b$ 之间，下边界是曲线 $y=\varphi_1(x)$，上边界是 $y=\varphi_2(x)$，这样的区域叫 **X 型区域**。它的截面（用 $x=x_0$ 切）是 $y$ 从 $\varphi_1(x_0)$ 到 $\varphi_2(x_0)$ 的一段，所以

$$\iint_Df\,\mathrm d\sigma=\int_a^b\mathrm dx\int_{\varphi_1(x)}^{\varphi_2(x)}f(x,y)\,\mathrm dy .$$

类似地，夹在 $y=c$ 与 $y=d$ 之间，左边界 $x=\psi_1(y)$，右边界 $x=\psi_2(y)$ 的叫 **Y 型区域**：

$$\iint_Df\,\mathrm d\sigma=\int_c^d\mathrm dy\int_{\psi_1(y)}^{\psi_2(y)}f(x,y)\,\mathrm dx .$$

定限的办法是**穿线法**，一定要先画图：

![穿线法：区域 $D$ 由 $y=x$ 与 $y=x^2$ 围成。左：作竖直线（虚线箭头）从下往上穿过区域，进入处在曲线 $y=x^2$ 上，离开处在直线 $y=x$ 上，$x$ 的范围是 $0$ 到 $1$。右：作水平线从左往右穿过，进入处在 $x=y$ 上，离开处在 $x=\sqrt y$ 上，$y$ 的范围是 $0$ 到 $1$](fig/C25-n3.pdf){width=92%}

**方法 4（穿线法定限）**

1. 画出区域，标出边界曲线的交点；
2. 想先对 $y$ 积分，就作一条竖直线，从下往上穿过区域：进入时碰到的曲线是下限，离开时碰到的是上限；这条线能移动到的 $x$ 范围是外层的上下限；
3. 想先对 $x$ 积分，作水平线，从左往右穿，同理；
4. 如果穿过区域时进入的（或离开的）曲线会变，就在变的地方把区域分成几块，分别积分再相加。

**例 8**　计算 $\displaystyle\iint_Dxy\,\mathrm d\sigma$，$D$ 由 $y=x$ 与 $y=x^2$ 围成。

区域由两条曲线围成，要先画图、再穿线；两种穿法都做一遍，对照着看上下限是怎样来的。

先画图：两曲线交于 $(0,0)$ 和 $(1,1)$。用竖直线穿，进入处是 $y=x^2$，离开处是 $y=x$，$0\le x\le1$：

$$\int_0^1x\,\mathrm dx\int_{x^2}^xy\,\mathrm dy=\int_0^1x\cdot\frac{x^2-x^4}2\,\mathrm dx=\frac12\Big(\frac14-\frac16\Big)=\frac1{24}.$$

换成水平线穿：进入处 $x=y$，离开处 $x=\sqrt y$，$0\le y\le1$：

$$\int_0^1y\,\mathrm dy\int_y^{\sqrt y}x\,\mathrm dx=\int_0^1y\cdot\frac{y-y^2}2\,\mathrm dy=\frac12\Big(\frac13-\frac14\Big)=\frac1{24},$$

两个次序相同。

> 计算 $\iint_Dy\,\mathrm d\sigma$，$D$ 由 $y=x^2$ 与 $y=2-x$ 围成。
>
> 答案：交点的横坐标是 $-2$ 和 $1$，竖直线穿：$-2\le x\le1$，$x^2\le y\le2-x$。里层 $\int_{x^2}^{2-x}y\,\mathrm dy=\frac{(2-x)^2-x^4}2$，外层 $\int_{-2}^1\frac{(2-x)^2-x^4}2\,\mathrm dx=\frac{36}5$。

**例 9**　求由平面 $x+y+z=1$ 与三个坐标平面围成的四面体的体积。

和例 8 不同，现在被积函数是曲顶（这里是平面）的高。四面体在 $xy$ 平面上的底是三角形 $D:x\ge0,y\ge0,x+y\le1$，高是 $z=1-x-y$：

$$V=\iint_D(1-x-y)\,\mathrm d\sigma=\int_0^1\mathrm dx\int_0^{1-x}(1-x-y)\,\mathrm dy=\int_0^1\frac{(1-x)^2}2\,\mathrm dx=\frac16 .$$

里层积分：$y$ 从 0 到 $1-x$，$\int(1-x-y)\,\mathrm dy=\frac{(1-x)^2}2$。结果 $\frac16$ 与「底面积 $\frac12$ 乘高 1 除以 3」一致。

**例 10**　计算 $\displaystyle\iint_D\frac{x^2}{y^2}\,\mathrm d\sigma$，$D$ 由 $x=2$，$y=x$，$xy=1$ 围成。

三个交点是 $(1,1)$、$(2,2)$、$(2,\frac12)$。要选次序，所以先看两种穿法。

竖直线穿：进入处是 $y=\frac1x$，离开处是 $y=x$，$1\le x\le2$，一块就够。

水平线穿：$y<1$ 时，进入处是曲线 $x=\frac1y$，离开处是 $x=2$；$y>1$ 时，进入处变成直线 $x=y$。要分两块（$y$ 的范围是 $\frac12$ 到 2，$y=1$ 处进入的曲线从 $xy=1$ 换成 $y=x$）。

所以选竖直线穿，先对 $y$ 积分：

$$\int_1^2x^2\,\mathrm dx\int_{1/x}^x\frac1{y^2}\,\mathrm dy=\int_1^2x^2\Big(x-\frac1x\Big)\mathrm dx=\int_1^2(x^3-x)\,\mathrm dx=\frac94 .$$

里层积分：$\int y^{-2}\,\mathrm dy=-\frac1y$，代入上下限得 $-\frac1x+x$。

这里的里层积分都积得出来。如果里层的原函数写不出来，又可以改变穿线的方向，就有办法了。

合上书，用穿线法写出例 8 的两种累次积分，并说出什么时候要把区域分成几块。

### 6. 先对 $x$ 积分积不出来时怎么办？

有些累次积分里层的原函数写不出来，换一个次序就变得容易。看这个：

$$\int_0^1\mathrm dx\int_x^1\frac{\sin y}{y}\,\mathrm dy .$$

$\frac{\sin y}y$ 没有初等原函数（C.11），里层积不出来。但这个累次积分是某个二重积分写成的，换成另一个次序，$y$ 变成外层，里层只对 $x$ 积分，$\frac{\sin y}y$ 对 $x$ 来说是常数。

换次序的做法只有一条：**先从积分限还原出区域，画图，再按另一种方向穿线。**

![还原区域：累次积分 $\int_0^1\mathrm dx\int_x^1\frac{\sin y}y\,\mathrm dy$ 的限是 $0\le x\le1$，$x\le y\le1$，区域是三角形（浅灰阴影）。左：竖直线穿，进入处 $y=x$，离开处 $y=1$。右：水平线穿，进入处 $x=0$，离开处 $x=y$，$0\le y\le1$](fig/C25-n4.pdf){width=85%}

由外层 $0\le x\le1$ 和里层 $x\le y\le1$ 画出三角形，顶点 $(0,0),(0,1),(1,1)$。换成水平线穿：进入处是 $x=0$，离开处是直线 $y=x$ 即 $x=y$，$y$ 从 0 到 1。

**方法 5（交换积分次序）**

1. 从累次积分的上下限写出区域的不等式，画图；
2. 标出边界曲线的交点；
3. 按另一个方向穿线，重新写上下限（需要时分块）；
4. 被积函数照抄，积分变量换了就重新积分。

**例 11**　交换次序并计算 $\displaystyle\int_0^1\mathrm dx\int_x^1\frac{\sin y}y\,\mathrm dy$。

里层积不出，所以换次序；区域的画法和穿线沿用例 8，只是这次要从积分限倒着还原区域。

按方法 5 的步骤：区域是上图的三角形，水平线穿，

$$\int_0^1\mathrm dy\int_0^y\frac{\sin y}y\,\mathrm dx=\int_0^1\frac{\sin y}y\cdot y\,\mathrm dy=\int_0^1\sin y\,\mathrm dy=1-\cos1 .$$

里层对 $x$ 积分时，$\frac{\sin y}y$ 是常数，积出来是乘以长度 $y$，正好把分母约掉。

> 交换次序并计算 $\int_0^2\mathrm dx\int_x^2\mathrm e^{-y^2}\,\mathrm dy$。
>
> 答案：区域 $0\le x\le2$，$x\le y\le2$，换成 $0\le y\le2$，$0\le x\le y$：$\int_0^2y\,\mathrm e^{-y^2}\,\mathrm dy=\frac{1-\mathrm e^{-4}}2$。

**例 12**　把 $\displaystyle\int_0^1\mathrm dx\int_0^{x^2}f\,\mathrm dy+\int_1^3\mathrm dx\int_0^{(3-x)/2}f\,\mathrm dy$ 写成先对 $x$ 积分的一个累次积分。

和例 11 不同，这里有两块，换次序之后反而合成一块。

第一块 $0\le x\le1$，$0\le y\le x^2$，第二块 $1\le x\le3$，$0\le y\le\frac{3-x}2$。曲线 $y=x^2$ 与直线 $y=\frac{3-x}2$ 在 $x=1$，$y=1$ 处相交（方程还有一个根 $x=-\frac32$，不在 $0\le x\le3$ 内，略去）。两块合起来的区域，下边界是 $y=0$，上边界先是抛物线、再是直线，在 $(1,1)$ 处上边界由抛物线换成直线，$y$ 的最大值是 1。

固定 $y\in[0,1]$ 画水平线：进入处是抛物线，由 $y=x^2$ 得 $x=\sqrt y$（区域在 $y$ 轴右侧，$x\ge0$，所以只取正根）；离开处是直线，由 $y=\frac{3-x}2$ 得 $x=3-2y$。这样一块就够：

$$\int_0^1\mathrm dy\int_{\sqrt y}^{3-2y}f\,\mathrm dx .$$

**例 13**　计算 $\displaystyle\int_0^1\mathrm dx\int_{\sqrt x}^1\sqrt{1+y^3}\,\mathrm dy$。

和例 11 一样，里层的原函数写不出来，换次序可解；这次区域的边界是曲线 $x=y^2$ 一侧，换完以后外层要凑微分。

$\sqrt{1+y^3}$ 的原函数写不出来，所以换次序。由 $0\le x\le1$，$\sqrt x\le y\le1$ 得区域，用水平线穿：$0\le y\le1$，$0\le x\le y^2$：

$$\int_0^1\mathrm dy\int_0^{y^2}\sqrt{1+y^3}\,\mathrm dx=\int_0^1y^2\sqrt{1+y^3}\,\mathrm dy .$$

里层对 $x$ 积分，$\sqrt{1+y^3}$ 是常数，积出来乘以长度 $y^2$，恰好凑出 $\mathrm d(1+y^3)=3y^2\,\mathrm dy$。令 $u=1+y^3$：

$$\frac13\int_1^2\sqrt u\,\mathrm du=\frac13\cdot\frac23\big(2\sqrt2-1\big)=\frac29\big(2\sqrt2-1\big).$$

有人会想：把里外两层的上下限对调一下就行，也就是 $\int_0^1\mathrm dy\int_y^1$ 之类。这样不行。里层的限 $x\le y\le1$ 里含有外层变量 $x$，对调以后 $y$ 的范围依赖的变量就变了，区域已经不是原来那一块。例 11 里正确的结果是 $0\le x\le y$，限的位置和形状都变了，只有先画区域才能写对。

换次序靠的是把区域看清。有些区域和被积函数本身带着对称，连换次序都可以省掉，下一节看怎样直接利用。

合上书，说出交换积分次序的四个步骤，并说明为什么不能只把上下限“对调”。

### 7. 区域和被积函数有对称性时，能省掉哪些计算？

例 2 里被积函数 $x+y+10$ 的 $x+y$ 那一部分，在圆盘上的积分不用算也知道是 0：圆盘关于两条坐标轴都对称：$\iint x\,\mathrm d\sigma=0$，因为点 $(x,y)$ 与 $(-x,y)$ 处的 $x$ 互为相反数；$\iint y\,\mathrm d\sigma=0$，因为 $(x,y)$ 与 $(x,-y)$ 处的 $y$ 互为相反数。把这个想法写成规则。

**奇偶对称**　若 $D$ 关于 $y$ 轴对称（$(x,y)\in D$ 时 $(-x,y)\in D$），则

- $f(-x,y)=-f(x,y)$（对 $x$ 是奇函数）时，$\iint_Df\,\mathrm d\sigma=0$；
- $f(-x,y)=f(x,y)$（对 $x$ 是偶函数）时，$\iint_Df\,\mathrm d\sigma=2\iint_{D\cap\{x\ge0\}}f\,\mathrm d\sigma$。

关于 $x$ 轴对称同理，把 $x$ 换成 $y$。区域关于点 $(a,b)$ 中心对称（$(x,y)\in D$ 时 $(2a-x,2b-y)\in D$）时，若 $f(2a-x,2b-y)=-f(x,y)$，积分也为 0；例如 $D$ 关于 $(1,1)$ 对称时，$x+y-2$ 在成对的两点处互为相反数。理由：把 $D$ 分成对称的小块配成一对，一对里两个函数值互为相反数或相等。

**轮换对称**　若 $D$ 关于直线 $y=x$ 对称（$(x,y)\in D$ 时 $(y,x)\in D$），则

$$\iint_Df(x,y)\,\mathrm d\sigma=\iint_Df(y,x)\,\mathrm d\sigma .$$

理由：把积分变量的名字 $x,y$ 互换，区域不变，积分值不变。常用的一个推论：$\iint_Dx^2\,\mathrm d\sigma=\iint_Dy^2\,\mathrm d\sigma$。

**方法 6（用对称性化简）**　先检查区域有什么对称性，再检查被积函数对相应的变量是奇还是偶。**两条要同时成立**：区域关于 $y$ 轴对称，但被积函数对 $x$ 是偶函数（比如 $f=y$，它不含 $x$），就不能得出 0。检查的变量要和对称的方向配对。区域不对称时也不能用：$D=[0,1]^2$ 不关于 $y$ 轴对称，$\iint_Dx\,\mathrm d\sigma=\frac12\ne0$。

**例 14**　计算 $\displaystyle\iint_D(x+y)^2\,\mathrm d\sigma$，$D:|x|+|y|\le1$。

区域用第 2 节随堂小题里的菱形，被积函数展开以后有三项，每一项要分别问：区域对它对称吗，它的奇偶性是什么。

先展开：$(x+y)^2=x^2+2xy+y^2$。

$D$ 是菱形，关于两条坐标轴都对称，$2xy$ 对 $x$ 是奇函数，所以 $\iint_D2xy\,\mathrm d\sigma=0$。

$D$ 关于 $y=x$ 对称，所以 $\iint_Dx^2=\iint_Dy^2$。算 $\iint_Dx^2$：竖直线穿，$-1\le x\le1$，$-(1-|x|)\le y\le1-|x|$，

$$\iint_Dx^2\,\mathrm d\sigma=\int_{-1}^1x^2\cdot2(1-|x|)\,\mathrm dx=4\int_0^1x^2(1-x)\,\mathrm dx=4\Big(\frac13-\frac14\Big)=\frac13 .$$

最后一步用了被积函数对 $x$ 是偶函数。所以 $\iint_D(x+y)^2=\frac13+0+\frac13=\frac23$。

> 用对称性算出例 2 里的精确值：$\iint_D(x+y+10)\,\mathrm d\sigma$，$D:x^2+y^2\le4$。
>
> 答案：圆盘关于两条坐标轴对称，$x$ 和 $y$ 两项都是奇函数，积分为 0。剩下 $10\sigma=10\cdot4\pi=40\pi$。

**例 15**　计算 $\displaystyle\iint_D\big(x\,\mathrm e^{y}+y\big)\,\mathrm d\sigma$，$D$ 由 $y=x^2$ 与 $y=1$ 围成。

和例 14 不同，只有一条对称轴，被积函数分成两项，要分别看。

$D$ 关于 $y$ 轴对称。第一项 $x\mathrm e^y$ 对 $x$ 是奇函数，积分为 0，不管 $\mathrm e^y$ 能不能积出来。第二项 $y$ 对 $x$ 是偶函数，没有简化，直接算：

$$\iint_Dy\,\mathrm d\sigma=\int_{-1}^1\mathrm dx\int_{x^2}^1y\,\mathrm dy=\int_{-1}^1\frac{1-x^4}2\,\mathrm dx=\frac12\Big(2-\frac25\Big)=\frac45 .$$

所以答案是 $\frac45$。

对称性只对特殊的区域和函数有用。圆盘上 $x^2+y^2$ 这样的函数，对称性帮不上忙，要换一套坐标。

合上书，说出奇偶对称使用时要同时检查的两件事，并用 $y$ 轴对称的区域举一个不能用的例子。

### 8. 圆形、扇形区域上，为什么要换成极坐标？

圆盘 $x^2+y^2\le1$ 用穿线法写成 $-1\le x\le1$，$-\sqrt{1-x^2}\le y\le\sqrt{1-x^2}$，里层积出来是带根号的式子。被积函数如果是 $x^2+y^2$ 或者 $\sqrt{x^2+y^2}$ 这样的组合，积起来也很麻烦。这些情形里，用到的是点到原点的距离 $r$ 和角度 $\theta$。

极坐标回顾：平面上的点 $(x,y)$ 可以用它到原点的距离 $r\ge0$ 和 $x$ 轴正向转到它的有向角 $\theta$ 来记，$x=r\cos\theta$，$y=r\sin\theta$，$r^2=x^2+y^2$。圆盘 $x^2+y^2\le R^2$ 就是 $0\le r\le R$，$0\le\theta\le2\pi$，一个「矩形」；圆 $x^2+y^2=2x$ 配方是 $(x-1)^2+y^2=1$，代入得 $r=2\cos\theta$。

要换的是面积元。在 $r$ 到 $r+\Delta r$、$\theta$ 到 $\theta+\Delta\theta$ 之间的一小块是一段扇环，它的面积是两个扇形面积之差：

$$\frac12(r+\Delta r)^2\Delta\theta-\frac12r^2\Delta\theta=\Big(r+\frac{\Delta r}2\Big)\Delta r\,\Delta\theta\ \approx\ r\,\Delta r\,\Delta\theta .$$

![极坐标下的小块：圆心在原点，两条半径夹角 $\Delta\theta$，两个同心圆半径为 $r$ 与 $r+\Delta r$，中间的扇环（浅灰阴影）近似一个长为 $r\Delta\theta$（弧长）、宽为 $\Delta r$ 的小矩形，面积约 $r\,\Delta r\,\Delta\theta$](fig/C25-n5.pdf){width=60%}

长方形的两条边是弧长 $r\Delta\theta$ 和径向的宽 $\Delta r$，乘起来也是 $r\Delta r\Delta\theta$。所以面积元 $\mathrm d\sigma=r\,\mathrm dr\,\mathrm d\theta$，不是 $\mathrm dr\,\mathrm d\theta$：离原点越远，同样的 $\Delta\theta$ 对应的弧越长，小块越大，多出来的因子就是 $r$。

设 $D'$ 是 $D$ 在 $(r,\theta)$ 平面里对应的区域，则

$$\iint_Df(x,y)\,\mathrm d\sigma=\iint_{D'}f(r\cos\theta,\,r\sin\theta)\,r\,\mathrm dr\,\mathrm d\theta .$$

极坐标下的区域用「射线穿」来定限：作一条从原点出发、方向为 $\theta$ 的射线，若它与区域的交集是一段，进入处的 $r_1(\theta)$ 和离开处的 $r_2(\theta)$ 就是里层上下限，$\theta$ 的范围是外层。若交集有好几段，要把区域分成几块分别积分。射线一出发就在区域里（原点在区域内或边界上）时，$r_1=0$。

核对：圆盘面积 $\iint_D1\,\mathrm d\sigma=\int_0^{2\pi}\mathrm d\theta\int_0^Rr\,\mathrm dr=2\pi\cdot\frac{R^2}2=\pi R^2$。如果漏掉 $r$，得到的是 $2\pi R$，连量纲都不对（面积应该是长度的平方）。

**方法 7（极坐标）**

1. 区域是圆盘、圆环、扇形，或被积函数含 $x^2+y^2$、$\frac yx$，就考虑极坐标；
2. 用 $x=r\cos\theta$，$y=r\sin\theta$ 改写被积函数和边界；
3. 画图，用射线穿定出 $\theta$ 的范围和 $r$ 的上下限；
4. 面积元写成 $r\,\mathrm dr\,\mathrm d\theta$，不要漏掉 $r$。

**例 16**　计算 $\displaystyle\iint_D(x^2+y^2)\,\mathrm d\sigma$，$D:x^2+y^2\le1$。

区域选最简单的圆盘，圆心在原点，被积函数 $x^2+y^2$ 就是 $r^2$。

被积函数 $x^2+y^2=r^2$，区域 $0\le r\le1$，$0\le\theta\le2\pi$：

$$\int_0^{2\pi}\mathrm d\theta\int_0^1r^2\cdot r\,\mathrm dr=2\pi\cdot\frac14=\frac\pi2 .$$

与第 7 节对照：这个圆盘关于 $y=x$ 对称，所以 $\iint_Dy^2=\iint_Dx^2=\frac12\cdot\frac\pi2=\frac\pi4$，不用再算。

> 计算 $\iint_D(x^2+y^2)\,\mathrm d\sigma$，$D:x^2+y^2\le4$。
>
> 答案：$\int_0^{2\pi}\mathrm d\theta\int_0^2r^3\,\mathrm dr=2\pi\cdot4=8\pi$。

**例 17**　计算 $\displaystyle\iint_D\sqrt{x^2+y^2}\,\mathrm d\sigma$，$D:x^2+y^2\le2x$。

和例 16 不同，圆心不在原点，圆过原点。边界 $r^2=2r\cos\theta$，即 $r=2\cos\theta$。射线从原点出发，$r$ 从 0 到 $2\cos\theta$，要 $\cos\theta\ge0$，所以 $-\frac\pi2\le\theta\le\frac\pi2$：

$$\int_{-\pi/2}^{\pi/2}\mathrm d\theta\int_0^{2\cos\theta}r\cdot r\,\mathrm dr=\int_{-\pi/2}^{\pi/2}\frac{8\cos^3\theta}3\,\mathrm d\theta=\frac83\cdot\frac43=\frac{32}9 .$$

最后一步：$\int_{-\pi/2}^{\pi/2}\cos^3\theta\,\mathrm d\theta=2\int_0^{\pi/2}(1-\sin^2\theta)\cos\theta\,\mathrm d\theta=2\big(1-\frac13\big)=\frac43$（令 $u=\sin\theta$，$\mathrm du=\cos\theta\,\mathrm d\theta$，$u$ 从 0 到 1，$\int_0^1(1-u^2)\mathrm du=\frac23$）。

**例 18**　计算 $\displaystyle\iint_D\arctan\frac yx\,\mathrm d\sigma$，$D:1\le x^2+y^2\le4,\ 0\le y\le x$。

和例 17 不同，区域是一块扇环，被积函数 $\arctan\frac yx=\theta$（$\theta\in[0,\frac\pi4]$，所以反正切正好还原角度）。$1\le r\le2$，$0\le\theta\le\frac\pi4$：

$$\int_0^{\pi/4}\theta\,\mathrm d\theta\int_1^2r\,\mathrm dr=\frac{\pi^2}{32}\cdot\frac32=\frac{3\pi^2}{64} .$$

被积函数只与 $\theta$ 有关，区域又是「矩形」，二重积分分成两个一元积分的乘积。

> 计算 $\iint_Dx\,\mathrm d\sigma$，$D:x^2+y^2\le2x$。
>
> 答案：$\int_{-\pi/2}^{\pi/2}\cos\theta\,\mathrm d\theta\int_0^{2\cos\theta}r^2\,\mathrm dr=\frac83\int_{-\pi/2}^{\pi/2}\cos^4\theta\,\mathrm d\theta=\frac83\cdot\frac{3\pi}8=\pi$。几何上 $D$ 是圆心 $(1,0)$、半径 1 的圆盘，$\iint x$ 等于「面积 $\pi$ 乘平均的 $x$ 坐标 1」。

极坐标把圆盘变成了矩形。开头提到的 $\mathrm e^{-x^2}$ 没有原函数，它能不能也借极坐标绕过去，是下一节的事。

合上书，用扇环的面积推出 $\mathrm d\sigma=r\,\mathrm dr\,\mathrm d\theta$，并说出什么时候用极坐标。

### 9. $\mathrm e^{-x^2}$ 找不到初等原函数，为什么它在整条实轴上的积分等于 $\sqrt\pi$？

概率里最常用的函数是正态分布的密度 $\frac1{\sqrt{2\pi}}\mathrm e^{-x^2/2}$。密度曲线下的总面积必须是 1，所以要知道 $\int_{-\infty}^{+\infty}\mathrm e^{-x^2/2}\,\mathrm dx$ 是多少。$\mathrm e^{-x^2}$ 的原函数不是初等函数（C.11），牛顿–莱布尼茨公式用不上。本节用二重积分绕过它：把积分平方，变成平面上的积分，再用极坐标。

**无界区域上的二重积分。** 区域 $D$ 无界（例如整个平面）时，本节取嵌套的有界区域 $D_R=D\cap\{x^2+y^2\le R^2\}$，先在 $D_R$ 上积分，再让 $R\to\infty$：$\iint_D=\lim_{R\to\infty}\iint_{D_R}$。被积函数 $f\ge0$ 时，$R$ 增大，区域变大，积分不会减小，所以极限一定存在（有限或 $+\infty$）。非负这个条件去掉就不行：$f=\sin(x^2+y^2)$ 在 $D_R$ 上的积分是 $\pi(1-\cos R^2)$，$R\to\infty$ 时来回摆动，没有极限。

换成别的嵌套的、逐渐铺满 $D$ 的有界区域列（铺满指每个有界区域最终都被列中某一块装下），$f\ge0$ 时极限相同：两列区域互相装得下，两个极限互相夹住。下面的证明正是用正方形和圆盘互相夹。圆盘列 $D_R$ 在极坐标里就是 $0\le r\le R$，所以也可以直接写成 $\int_0^{+\infty}\mathrm dr$ 的反常积分。

**高斯积分**　$\displaystyle\int_{-\infty}^{+\infty}\mathrm e^{-x^2}\,\mathrm dx=\sqrt\pi$。

**证明**

想法：积分 $\int\mathrm e^{-x^2}\mathrm dx$ 直接求原函数走不通。但设它为 $K$，$K^2$ 是两个同样的积分相乘，写成 $\int\mathrm e^{-x^2}\mathrm dx\cdot\int\mathrm e^{-y^2}\mathrm dy$，按第 4 节的乘积公式正好是平面上的二重积分，而平面上的积分可以用极坐标算。

第一步，用有界区域逼近。记 $G(a)=\int_{-a}^a\mathrm e^{-x^2}\,\mathrm dx$。正方形 $S_a=[-a,a]^2$ 上的被积函数 $\mathrm e^{-(x^2+y^2)}=\mathrm e^{-x^2}\cdot\mathrm e^{-y^2}$ 是乘积，由第 4 节的乘积公式，

$$\iint_{S_a}\mathrm e^{-(x^2+y^2)}\,\mathrm d\sigma=G(a)^2 .$$

第二步，夹逼。半径为 $a$ 和 $\sqrt2a$ 的圆盘 $D_a$、$D_{\sqrt2a}$ 满足 $D_a\subset S_a\subset D_{\sqrt2a}$（正方形的内切圆与外接圆）。被积函数处处为正，积分区域越大积分越大：

$$\iint_{D_a}\ \le\ G(a)^2\ \le\ \iint_{D_{\sqrt2a}} .$$

![正方形 $S_a$（实线）夹在两个圆盘之间：内切圆盘半径 $a$（虚线），外接圆盘半径 $\sqrt2a$（点线）。被积函数 $\mathrm e^{-(x^2+y^2)}$ 恒正，所以正方形上的积分夹在两个圆盘上的积分之间](fig/C25-n6.pdf){width=55%}

第三步，圆盘上的积分用极坐标算。半径为 $R$ 的圆盘：

$$\iint_{D_R}\mathrm e^{-(x^2+y^2)}\,\mathrm d\sigma=\int_0^{2\pi}\mathrm d\theta\int_0^R\mathrm e^{-r^2}\,r\,\mathrm dr=2\pi\cdot\frac{1-\mathrm e^{-R^2}}2=\pi\big(1-\mathrm e^{-R^2}\big).$$

里层积分之所以能算，是因为极坐标多出的因子 $r$ 恰好是 $\mathrm e^{-r^2}$ 的导数的一部分。

第四步，取极限。夹逼式变成

$$\pi\big(1-\mathrm e^{-a^2}\big)\le G(a)^2\le\pi\big(1-\mathrm e^{-2a^2}\big),$$

$a\to\infty$ 时两边都趋于 $\pi$，所以 $G(a)^2\to\pi$，$K=\lim G(a)=\sqrt\pi$（$K>0$）。$\blacksquare$

这就回答了本节的问题。要得到正态密度里的 $\mathrm e^{-t^2/2}$，令 $t=\sqrt2\,x$（$\mathrm dt=\sqrt2\,\mathrm dx$）：

$$\int_{-\infty}^{+\infty}\mathrm e^{-t^2/2}\,\mathrm dt=\sqrt2\int_{-\infty}^{+\infty}\mathrm e^{-x^2}\,\mathrm dx=\sqrt{2\pi},$$

所以 $\frac1{\sqrt{2\pi}}\mathrm e^{-t^2/2}$ 在整条实轴上的积分是 1，这就是标准正态分布密度前面那个常数的来历。

**方法 8（无界区域）**　被积函数非负时，先在有界区域（常用圆盘）上积分，再让半径趋于无穷，也可以直接化成极坐标下的反常积分 $\int_0^{+\infty}$。

**例 19**　计算 $\displaystyle\iint_D\frac1{(x^2+y^2)^2}\,\mathrm d\sigma$，$D:x^2+y^2\ge1$。

和有界的例子相比，只多一步：外层变成反常积分。极坐标下 $1\le r<+\infty$，$0\le\theta\le2\pi$：

$$\int_0^{2\pi}\mathrm d\theta\int_1^{+\infty}\frac1{r^4}\,r\,\mathrm dr=2\pi\int_1^{+\infty}r^{-3}\,\mathrm dr=2\pi\cdot\frac12=\pi .$$

反常积分收敛（C.12：$p=3>1$）。如果指数换成 $\frac1{x^2+y^2}$，里层变成 $\int_1^{+\infty}r^{-1}\,\mathrm dr$，发散。

> 计算 $\iint_D\frac1{(x^2+y^2)^{3/2}}\,\mathrm d\sigma$，$D:x^2+y^2\ge1$。
>
> 答案：$\int_0^{2\pi}\mathrm d\theta\int_1^{+\infty}r^{-3}\,r\,\mathrm dr=2\pi\int_1^{+\infty}r^{-2}\,\mathrm dr=2\pi$。

**例 20**　**（AI）** 扩散模型每一步给数据加一份噪声，噪声的大小分布用函数 $p(x,y)=\frac1{2\pi}\mathrm e^{-(x^2+y^2)/2}$ 描述（这个函数是二维的标准正态密度，它为什么这样写，M.17 和 P.6 才讲）。这里只做积分：先算 $p$ 在整个平面上的积分，再算它在单位圆盘上的积分。

和例 19 相比，被积函数换成了 $\mathrm e^{-r^2/2}$ 这类含 $x^2+y^2$ 的函数，仍然用极坐标；整个平面上的积分是无界区域，用方法 8。

整个平面：

$$\iint_{\mathbb R^2}p\,\mathrm d\sigma=\int_0^{2\pi}\mathrm d\theta\int_0^{+\infty}\frac1{2\pi}\mathrm e^{-r^2/2}\,r\,\mathrm dr=\int_0^{+\infty}\mathrm e^{-r^2/2}\,r\,\mathrm dr=1 .$$

里层 $\int\mathrm e^{-r^2/2}\,r\,\mathrm dr=-\mathrm e^{-r^2/2}$，从 0 到 $+\infty$ 得 1。积分等于 1，说明 $p$ 作为「分布」是合格的：总量是 1。

单位圆盘：

$$\iint_{x^2+y^2\le1}p\,\mathrm d\sigma=\int_0^{2\pi}\mathrm d\theta\int_0^1\frac1{2\pi}\mathrm e^{-r^2/2}\,r\,\mathrm dr=1-\mathrm e^{-1/2}\approx0.3935 .$$

总量 1 里约有 39% 落在半径为 1 的圆盘里，P.6 会把它解释为噪声向量落进圆盘的概率。

> 计算 $\iint_{\mathbb R^2}\mathrm e^{-(x^2+4y^2)}\,\mathrm d\sigma$。
>
> 答案：被积函数是 $\mathrm e^{-x^2}\cdot\mathrm e^{-4y^2}$ 的乘积，$\int\mathrm e^{-x^2}\,\mathrm dx=\sqrt\pi$，令 $u=2y$ 得 $\int\mathrm e^{-4y^2}\,\mathrm dy=\frac12\sqrt\pi$，所以结果是 $\frac\pi2$。

高斯积分用的是极坐标，而极坐标只是换变量的一种。换成别的变量，面积元该乘什么，是下一节的问题。

合上书，写出高斯积分证明的四步：逼近、夹逼、极坐标、取极限。

### 10. 一般地换元时，面积被放大了多少倍？

极坐标的面积元 $r\,\mathrm dr\,\mathrm d\theta$ 是从扇环的面积算出来的。换成别的变量时，面积元该乘什么？

先看线性的换元：$x=2u+v$，$y=u+3v$。$uv$ 平面上的单位正方形，两条边 $(1,0)$、$(0,1)$ 分别变成 $(2,1)$、$(1,3)$，整个正方形变成以它们为邻边的平行四边形。

它的面积由 C.19.5 的向量积得到：平面向量 $(a_1,a_2)$ 和 $(b_1,b_2)$ 补上第三个坐标 0 后，向量积是 $(0,0,a_1b_2-a_2b_1)$，所以平行四边形面积是 $|2\cdot3-1\cdot1|=5$。

线性换元把每个小正方形都放大成面积 5 倍的小平行四边形，于是 $\mathrm dx\,\mathrm dy=5\,\mathrm du\,\mathrm dv$。

一般的换元 $x=x(u,v)$，$y=y(u,v)$ 不是线性的，但在小范围内近似线性。考虑 $uv$ 平面上以 $(u,v)$ 为角、边长 $\Delta u$、$\Delta v$ 的小矩形。全微分告诉我们，在 $(u,v)$ 附近 $x,y$ 的改变量近似是 $\Delta u,\Delta v$ 的线性函数（C.20.5）。小矩形沿 $u$ 方向的边变成位移 $(x_u\Delta u,\ y_u\Delta u)$，沿 $v$ 方向的边变成 $(x_v\Delta v,\ y_v\Delta v)$。小矩形的像近似是以这两个位移为邻边的平行四边形，面积约为

$$\big|x_u\Delta u\cdot y_v\Delta v-y_u\Delta u\cdot x_v\Delta v\big|=\big|x_uy_v-x_vy_u\big|\,\Delta u\,\Delta v .$$

![$uv$ 平面上的小矩形（左）被映成 $xy$ 平面上的一块弯曲小四边形（右），它近似是以 $(x_u\Delta u,y_u\Delta u)$、$(x_v\Delta v,y_v\Delta v)$ 为邻边的平行四边形（浅灰），面积放大 $|J|$ 倍](fig/C25-n7.pdf){width=85%}

放大倍数里的式子叫**雅可比行列式**：

$$J=\frac{\partial(x,y)}{\partial(u,v)}=\begin{vmatrix}x_u&x_v\\y_u&y_v\end{vmatrix}=x_uy_v-x_vy_u .$$

**二重积分的换元公式**　设 $D'$ 与 $D$ 是有界区域，变换 $(u,v)\mapsto(x(u,v),y(u,v))$ 在包含 $D'$ 的一个开集上有连续偏导数，在 $D'$ 内部是一一对应且 $J\ne0$，并把 $D'$ 映到 $D$，则

$$\iint_Df(x,y)\,\mathrm dx\,\mathrm dy=\iint_{D'}f\big(x(u,v),y(u,v)\big)\,|J|\,\mathrm du\,\mathrm dv .$$

用极坐标核对：$x=r\cos\theta$，$y=r\sin\theta$，

$$J=\begin{vmatrix}x_r&x_\theta\\y_r&y_\theta\end{vmatrix}=\begin{vmatrix}\cos\theta&-r\sin\theta\\\sin\theta&r\cos\theta\end{vmatrix}=r\cos^2\theta+r\sin^2\theta=r ,$$

正是 $r\,\mathrm dr\,\mathrm d\theta$ 里的 $r$。极坐标在 $r=0$ 这条线上 $J=0$，它在 $(r,\theta)$ 平面里是一条线段，面积为 0，不影响积分。这类 $J=0$ 只出现在面积为零的地方（一个点或一条曲线），略去它们不影响积分，所以上面的条件是充分条件，不必在整个 $D'$ 上都满足。本章的例题都属于这种情形。$J$ 在一整块区域上为 0 的换元则不能用。

一一对应这个条件不能去掉：$x=u^2$，$y=v$，$D'=[-1,1]\times[0,1]$，$J=2u$，只在 $u=0$ 处为 0，但 $D=[0,1]^2$ 里的每个点被 $\pm\sqrt x$ 盖了两次，$\iint_{D'}|J|\,\mathrm du\,\mathrm dv=2$，而 $D$ 的面积是 1。

新变量常以 $u=u(x,y)$、$v=v(x,y)$ 的形式给出，反解 $x,y$ 很麻烦。这时先算 $\frac{\partial(u,v)}{\partial(x,y)}$，再取倒数：从 $(u,v)$ 到 $(x,y)$ 再回到 $(u,v)$，面积一共放大 1 倍，所以两个放大倍数互为倒数。用矩阵的话说：两个变换在小范围内的线性近似是一对互逆的变换，它们的行列式（放大倍数）互为倒数（L.6）：

$$\frac{\partial(x,y)}{\partial(u,v)}=\Big(\frac{\partial(u,v)}{\partial(x,y)}\Big)^{-1}.$$

**方法 9（雅可比换元）**

1. 看区域的边界或被积函数里反复出现的组合，令它们为 $u,v$，使新区域成为矩形或简单区域；
2. 求 $|J|$（反解不便时先算 $\frac{\partial(u,v)}{\partial(x,y)}$ 再取倒数）；
3. 被积函数、区域、面积元三样一起换掉。

**例 21**　求椭圆 $\frac{x^2}4+\frac{y^2}9\le1$ 的面积，并计算 $\displaystyle\iint_D\Big(\frac{x^2}4+\frac{y^2}9\Big)\mathrm d\sigma$。

用最简单的线性换元：把椭圆拉成圆，面积元乘上常数 $|J|$，然后回到例 16。

令 $x=2u$，$y=3v$，椭圆变成单位圆盘 $u^2+v^2\le1$，$J=\begin{vmatrix}2&0\\0&3\end{vmatrix}=6$。

面积 $=6\cdot\pi=6\pi$。被积函数变成 $u^2+v^2$，由例 16：

$$\iint_D\Big(\frac{x^2}4+\frac{y^2}9\Big)\mathrm d\sigma=6\iint_{u^2+v^2\le1}(u^2+v^2)\,\mathrm du\,\mathrm dv=6\cdot\frac\pi2=3\pi .$$

> 求椭圆 $\frac{x^2}9+\frac{y^2}4\le1$ 的面积。
>
> 答案：令 $x=3u$，$y=2v$，$|J|=6$，椭圆变成单位圆盘，面积 $6\pi$。

**例 22**　$D$ 是第一象限里由 $xy=1$，$xy=2$，$y=x$，$y=2x$ 围成的区域，计算 $\displaystyle\iint_Dy^2\,\mathrm d\sigma$。

被积函数和区域里都有 $xy$ 和 $\frac yx$，令 $u=xy$，$v=\frac yx$，区域变成 $1\le u\le2$，$1\le v\le2$。

和例 21 不同，这里反解 $x,y$ 麻烦，所以用倒数：

$$\frac{\partial(u,v)}{\partial(x,y)}=\begin{vmatrix}y&x\\-\dfrac y{x^2}&\dfrac1x\end{vmatrix}=\frac yx+\frac yx=2v,\qquad|J|=\frac1{2v}.$$

被积函数 $y^2=uv$（因为 $uv=xy\cdot\frac yx=y^2$）。于是

$$\iint_Dy^2\,\mathrm d\sigma=\int_1^2\!\!\int_1^2uv\cdot\frac1{2v}\,\mathrm du\,\mathrm dv=\frac12\int_1^2u\,\mathrm du\cdot\int_1^2\mathrm dv=\frac12\cdot\frac32\cdot1=\frac34 .$$

> 用换元 $u=x+y$，$v=x-y$ 重算例 14：$\iint_D(x+y)^2\,\mathrm d\sigma$，$D:|x|+|y|\le1$。
>
> 答案：$|x|+|y|\le1$ 等价于 $|u|\le1$ 且 $|v|\le1$，$x=\frac{u+v}2$，$y=\frac{u-v}2$，$|J|=\frac12$。原式 $=\int_{-1}^1\!\int_{-1}^1u^2\cdot\frac12\,\mathrm du\,\mathrm dv=\frac12\cdot\frac23\cdot2=\frac23$，与例 14 一致。

换元处理的是区域和被积函数怎么换。还有一类问题，变量不在区域里，而是在被积函数里当参数，下一节看这样的积分怎样求导。

合上书，用「小矩形变成近似平行四边形」推出 $|J|$，并用它核对极坐标的 $r$。

### 11. 积分里带一个参数时，能不能先对参数求导再积分？

算定积分

$$\int_0^1\frac{x^2-x}{\ln x}\,\mathrm dx ,$$

找原函数会失败。换个角度，把指数 2 换成 $t$：

$$T(t)=\int_0^1\frac{x^t-x}{\ln x}\,\mathrm dx ,\qquad t\ge1 .$$

被积函数在 $x\to0^+$ 时趋于 0，在 $x\to1$ 时由洛必达法则趋于 $t-1$，补上这两个端点值就是连续函数。我们要的是 $T(2)$，而 $T(1)=0$。如果允许把对 $t$ 的求导移到积分号里面，$\frac\partial{\partial t}\frac{x^t-x}{\ln x}=\frac{x^t\ln x}{\ln x}=x^t$，$\ln x$ 被约掉：

$$T'(t)=\int_0^1x^t\,\mathrm dx=\frac1{t+1}.$$

积回去，$T(t)=\ln(t+1)+C$，由 $T(1)=0$ 得 $C=-\ln2$，所以 $T(2)=\ln\frac32$。

关键是「求导移进积分号」凭什么成立。

**积分号下求导**　设 $f(x,t)$ 和它对 $t$ 的偏导数 $f_t(x,t)=\frac{\partial f}{\partial t}$ 在矩形 $a\le x\le b$，$\alpha\le t\le\beta$ 上连续，$\varphi(t)=\int_a^bf(x,t)\,\mathrm dx$，则在 $\alpha<t<\beta$ 内

$$\varphi'(t)=\int_a^bf_t(x,t)\,\mathrm dx .$$

**证明**　思路：先积分、交换次序，再求导。

第一步，记 $g(t)=\int_a^bf_t(x,t)\,\mathrm dx$，把它从 $\alpha$ 积到 $t$。这是矩形上 $f_t$ 的二重积分，可以交换次序（第 4 节）：

$$\int_\alpha^tg(s)\,\mathrm ds=\int_a^b\Big(\int_\alpha^tf_t(x,s)\,\mathrm ds\Big)\mathrm dx .$$

第二步，里面对 $s$ 积分的是 $f$ 对 $s$ 的偏导数，由牛顿–莱布尼茨公式等于 $f(x,t)-f(x,\alpha)$，所以

$$\int_\alpha^tg(s)\,\mathrm ds=\varphi(t)-\varphi(\alpha) .$$

第三步，两边对 $t$ 求导。右边得 $\varphi'(t)$；左边是变上限积分，$g$ 连续时导数是 $g(t)$。$g$ 连续是因为 $f_t$ 在有界闭矩形上连续，从而一致连续（有界闭集上的连续函数，对所有位置可以同时取同一个 $\delta$，类似 C.3 的闭区间情形），所以对任给的 $\varepsilon>0$，$|h|$ 足够小时对所有 $x$ 同时有 $|f_t(x,t+h)-f_t(x,t)|<\varepsilon$，于是 $|g(t+h)-g(t)|\le\int_a^b|f_t(x,t+h)-f_t(x,t)|\,\mathrm dx\le(b-a)\varepsilon$，$g$ 连续。$\blacksquare$

这个定理的条件是充分条件，其中矩形要有限：第一步交换次序要在有限矩形上做。无界区间不能只凭连续性把求导移进积分号，必须另加收敛方面的条件。比如 $\varphi(t)=\int_0^{+\infty}\frac{\sin tx}x\,\mathrm dx$（$t>0$）换元 $u=tx$ 后是一个与 $t$ 无关的数，$\varphi'(t)=0$；硬把导数移进去，得到的 $\int_0^{+\infty}\cos tx\,\mathrm dx$ 却根本不收敛。

积分限也含参数时，把 $\Phi(t)=\int_{u(t)}^{v(t)}f(x,t)\,\mathrm dx$ 看成 $F(u,v,t)=\int_u^vf(x,t)\,\mathrm dx$ 的复合。三个偏导数各来自一条已知的结论。$F_v=f(v,t)$（变上限求导），$F_u=-f(u,t)$（变下限求导多一个负号），$F_t=\int_u^vf_t\,\mathrm dx$（上下限固定时，刚证的定理）。三项各管一个来源：参数在被积函数里、在上限里、在下限里。由链式法则 $\Phi'=F_uu'+F_vv'+F_t$：

$$\Phi'(t)=\int_{u(t)}^{v(t)}f_t(x,t)\,\mathrm dx+f\big(v(t),t\big)v'(t)-f\big(u(t),t\big)u'(t).$$

**方法 10（积分号下求导）**

1. 被积函数里的参数挪不出积分号、或原积分算不出时，把它看成参数的函数；
2. 检查 $f$、$f_t$ 在有界闭矩形上连续；
3. 先算 $\int f_t\,\mathrm dx$；积分限含参数时，再加上「上限处的值乘上限的导数」，减去「下限处的值乘下限的导数」；
4. 需要原函数时，积回去并用一个容易算的参数值定常数。

**例 23**　设 $\Phi(t)=\int_t^{t^2}\frac{\sin tx}x\,\mathrm dx$（$t>0$），求 $\Phi'(t)$。

和本节开头的 $T(t)$ 不同，参数同时出现在被积函数和上下限里，所以要用三项的公式，三项都要算。

第一项，对 $t$ 求偏导，分母的 $x$ 被约掉：

$$\int_t^{t^2}\cos tx\,\mathrm dx=\frac{\sin tx}t\Big|_{x=t}^{x=t^2}=\frac{\sin t^3-\sin t^2}t .$$

第二项，上限 $t^2$ 处的值乘 $v'=2t$：$\frac{\sin t^3}{t^2}\cdot2t=\frac{2\sin t^3}t$。

第三项，减去下限 $t$ 处的值乘 $u'=1$：$\frac{\sin t^2}t$。

三项合起来，

$$\Phi'(t)=\frac{3\sin t^3-2\sin t^2}t .$$

> 用 $T(t)$ 算 $\displaystyle\int_0^1\frac{x^3-x}{\ln x}\,\mathrm dx$。
>
> 答案：开头的 $T(t)=\ln(t+1)-\ln2$，$T(3)=\ln4-\ln2=\ln2$。

合上书，把「先积分、交换次序、再求导」三步重新写一遍。

### 本章小结

本章在主线上的位置：重积分是「把区域切成小块，每块当柱体，加起来」。定积分的四步（分割、近似、求和、取极限）原样搬到平面区域上，计算则靠截面法化回两次一元积分，这是「切细了再加起来」在二维的样子；后面的 C.26–C.28 把它推到三维和曲线、曲面上。

回到开头的问题。设一个县是半径 10 千米的圆盘，取圆心为原点、10 千米为单位，雨深（毫米）是 $f=40(1-x^2-y^2)$。由例 16，$\iint_D(x^2+y^2)\,\mathrm d\sigma=\frac\pi2$，面积 $\pi$，所以 $\iint_Df\,\mathrm d\sigma=40\big(\pi-\frac\pi2\big)=20\pi$，平均雨深是 $\frac{20\pi}\pi=20$ 毫米。县的面积是 $100\pi$ 平方千米，约 $3.14\times10^8$ 平方米，总降水量约为 $0.02\times3.14\times10^8\approx6.3\times10^6$ 立方米。正态分布的常数 $\frac1{\sqrt{2\pi}}$ 在第 9 节算出，落进区域的概率在例 20 里算过一个。

逐章长大的两张表在本章新增如下。

| 谁推出谁 | 本章新增 |
|---|---|
| 边界分段光滑的有界闭区域上连续 $\Rightarrow$ 二重积分存在 | 本章新增 |
| 连续函数在矩形上 $\Rightarrow$ 两个累次积分相等 | 本章新增 |
| 被积函数非负 $\Rightarrow$ 无界区域上可以先取有界块再取极限、可交换次序 | 本章新增 |

| 一元积分的说法 | 二重积分里对应的说法 |
|---|---|
| 平均值 $\frac1{b-a}\int f$ 与中值定理 | 平均值 $\frac1\sigma\iint f$ 与二重积分中值定理（本章新增） |
| 换元要换限、换回 | 雅可比行列式 $\lvert J\rvert$（本章新增），极坐标是 $J=r$ |
| 计算：求原函数，代入上下限 | 累次积分：先对一个变量积，再对另一个变量积，每一层仍用牛顿–莱布尼茨公式（本章新增） |

| 方法 | 什么时候用 | 对应题号 |
|---|---|---|
| 方法 1（性质估值与比较） | 积不出时给范围；比较两个积分大小（注意在这块区域上比较） | C25-01、C25-13 |
| 方法 2（平均值与中值定理） | 区域上的平均值；「积分除以面积」再让区域缩成一点 | C25-02、C25-14 |
| 方法 3（矩形上的累次积分） | 矩形区域；两个次序难易不同时选对次序 | C25-03 |
| 方法 4（穿线法定限） | 区域边界是曲线；先画图，竖直线或水平线穿 | C25-04、C25-15 |
| 方法 5（交换积分次序） | 里层原函数积不出；从积分限还原区域，画图，换方向穿 | C25-05、C25-11 |
| 方法 6（对称性） | 区域关于坐标轴、$y=x$ 或某点对称，被积函数有奇偶性 | C25-06 |
| 方法 7（极坐标） | 圆盘、圆环、扇形；被积函数含 $x^2+y^2$、$\frac yx$；面积元 $r\,\mathrm dr\,\mathrm d\theta$ | C25-07、C25-12、C25-15 |
| 方法 8（无界区域） | 非负被积函数，先在圆盘上积分再让半径趋于无穷；高斯积分 | C25-09 |
| 方法 9（雅可比换元） | 边界或被积函数里反复出现 $u(x,y)$、$v(x,y)$ | C25-08 |
| 方法 10（积分号下求导） | 积分里带参数；积分限含参数时多两项 | C25-10 |
