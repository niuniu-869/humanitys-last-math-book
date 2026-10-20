## C.11 · 积分的计算方法

一家工厂知道，多生产第 $q$ 件产品要多花多少钱（边际成本）；一个应用知道每一时刻新增用户的速度（每天新增多少人）。想问的是反过来的事：生产 100 件一共花了多少，十天下来累计新增了多少用户。已知变化的快慢、要找回累积的总量（再加上起点已有的数量，才是总数），就是把求导倒过来做。C.10 的牛顿–莱布尼茨公式说，只要找到一个原函数，定积分就能算出来。但积分表里只有最基本的几个函数，遇到 $\int x\mathrm{e}^{x^2}\,\mathrm{d}x$ 这样的式子，表里没有，也没有一条通用的公式可套。

求导永远有章可循：和、积、商、复合，照规则一步步算下去总有结果。求原函数没有这样的保证。牛顿把「已知变化的快慢（他称流数），求变化的总量（流量）」列为基本问题之一；莱布尼茨引入了积分号 $\int$，那是一个拉长的 S，取自「求和」（拉丁文 summa）。随之而来的问题是：求导总能算下去，求原函数却常常卡住。刘维尔后来证明，有些函数的原函数不能由基本初等函数经有限次四则运算和复合写出，$\mathrm{e}^{-x^2}$ 就是一例；它的原函数存在，只是写不成初等形式（第 9 节回到这里）。里施进一步给出了判断初等原函数是否存在并把它求出来的算法。今天的符号计算软件（例如 SymPy）把本章的技巧和这类算法做成了程序，可以代我们动手，但认不出该用哪条技巧的人，也读不懂它的输出。

本章的办法是：把求导的两条主要规则倒过来用。链式法则倒过来是换元法，乘积法则倒过来是分部积分法。每种方法先讲不定积分的形式，紧接着讲它在定积分里的形式。

- 第 1、2 节讲两类换元，第 3 节讲定积分的换元，第 4 节讲不求原函数、借对称性化简的办法；
- 第 5、6 节讲分部积分和它在定积分里的新东西（华里士公式）；
- 第 7、8 节讲有理函数这类有固定程序的积分，以及怎样把三角函数的分式和简单根式化成有理函数；
- 第 9 节讲拿到一个积分先试哪种方法，以及哪些积分写不成初等函数；
- 第 10 节反过来，看一个和式的极限怎样认成定积分。

下面会反复用到 C.10.2 的基本积分表。以下公式都在被积函数有定义的实数区间上使用：分母不能为 0，根号在分母中时根号内须为正。

$$\int x^{\alpha}\,\mathrm{d}x=\frac{x^{\alpha+1}}{\alpha+1}+C\ (\alpha\ne-1),\quad \int\frac{\mathrm{d}x}{x}=\ln|x|+C,\quad \int\mathrm{e}^x\,\mathrm{d}x=\mathrm{e}^x+C,$$

$$\int\sin x\,\mathrm{d}x=-\cos x+C,\quad \int\cos x\,\mathrm{d}x=\sin x+C,\quad \int\frac{\mathrm{d}x}{1+x^2}=\arctan x+C,\quad \int\frac{\mathrm{d}x}{\sqrt{1-x^2}}=\arcsin x+C.$$

### 1. 被积函数里藏着一个复合函数及其导数时，怎么积？

先看三个求导的结果：

$$\frac{\mathrm{d}}{\mathrm{d}x}\sin(x^2)=2x\cos(x^2),\qquad \frac{\mathrm{d}}{\mathrm{d}x}\mathrm{e}^{x^2}=2x\,\mathrm{e}^{x^2},\qquad \frac{\mathrm{d}}{\mathrm{d}x}\ln(1+x^2)=\frac{2x}{1+x^2}.$$

倒过来读，就是 $\int2x\cos(x^2)\,\mathrm{d}x=\sin(x^2)+C$，另外两个同理。它们长得一样：被积函数是「某个外层函数在内层 $x^2$ 处的值」乘上「内层的导数 $2x$」。这正是链式法则求导后留下的样子，所以反过来就能认出它。

设 $F'=f$，即 $F$ 是 $f$ 的一个原函数，$u=u(x)$ 可导。链式法则给出

$$\frac{\mathrm{d}}{\mathrm{d}x}F\big(u(x)\big)=f\big(u(x)\big)\,u'(x),$$

两边求不定积分，得到

$$\int f\big(u(x)\big)\,u'(x)\,\mathrm{d}x=F\big(u(x)\big)+C=\Big[\int f(u)\,\mathrm{d}u\Big]_{u=u(x)}.$$

C.5 讲过微分 $\mathrm{d}u=u'(x)\,\mathrm{d}x$，所以左边的 $u'(x)\,\mathrm{d}x$ 可以整块写成 $\mathrm{d}u$。这就是**第一类换元法**，又叫**凑微分**：把 $u'(x)\,\mathrm{d}x$「凑」成 $\mathrm{d}u$，然后只剩下一个关于 $u$ 的、更简单的积分。式子最右边的方括号加下标 $\big[\cdot\big]_{u=u(x)}$ 的意思是：先算出 $\int f(u)\,\mathrm{d}u=F(u)$，再把 $u$ 代回 $u(x)$。

把它记成一个抓手：**找整体**。在被积函数里找一个整体 $u(x)$（括号里、指数里、根号里、分母），看剩下的部分是不是 $u'(x)$ 的常数倍。是，就把整个积分换成 $\int f(u)\,\mathrm{d}u$。下面这张表是最常用的「凑法」，每一行都是一次求导倒过来读：

| 被积式里有 | 凑成 |
|---|---|
| $\mathrm{d}x$ | $\mathrm{d}(x+b)$，$\ \mathrm{d}x=\frac1a\mathrm{d}(ax+b)$（$a\ne0$） |
| $x\,\mathrm{d}x$ | $\frac12\mathrm{d}(x^2)$ |
| $\frac{\mathrm{d}x}{x}$ | $\mathrm{d}(\ln\lvert x\rvert)$（$x\ne0$） |
| $\frac{\mathrm{d}x}{\sqrt x}$ | $2\,\mathrm{d}(\sqrt x)$（$x>0$） |
| $\mathrm{e}^x\,\mathrm{d}x$ | $\mathrm{d}(\mathrm{e}^x)$ |
| $\cos x\,\mathrm{d}x$、$\sin x\,\mathrm{d}x$ | $\mathrm{d}(\sin x)$、$-\mathrm{d}(\cos x)$ |
| $\frac{\mathrm{d}x}{1+x^2}$ | $\mathrm{d}(\arctan x)$ |

**方法 1（凑微分）**

1. 找整体：在被积函数里找一个候选的内层 $u(x)$。
2. 查剩余：剩下的因子是不是 $u'(x)$ 的常数倍？差一个常数就补上（乘一个再除一个）。
3. 换成 $\int f(u)\,\mathrm{d}u$，用基本积分表算出来。
4. 把 $u$ 换回 $x$ 的式子。

**例 1**　求 $\int x\,\mathrm{e}^{x^2}\,\mathrm{d}x$。

它就是本节开头 $2x\,\mathrm{e}^{x^2}$ 少了系数 2。内层仍是指数里的 $x^2$，它的导数是 $2x$，剩下的因子 $x$ 恰好是 $2x$ 的一半。

第一步，令 $u=x^2$，则 $\mathrm{d}u=2x\,\mathrm{d}x$，即 $x\,\mathrm{d}x=\frac12\mathrm{d}u$。

第二步，代入：

$$\int x\,\mathrm{e}^{x^2}\,\mathrm{d}x=\frac12\int\mathrm{e}^u\,\mathrm{d}u=\frac12\mathrm{e}^u+C.$$

第三步，换回 $x$：

$$\int x\,\mathrm{e}^{x^2}\,\mathrm{d}x=\frac12\mathrm{e}^{x^2}+C.$$

验算：右边求导，$\frac12\mathrm{e}^{x^2}\cdot2x=x\mathrm{e}^{x^2}$。积分题总可以这样求导检验。

> 求 $\int x^2\mathrm{e}^{x^3}\,\mathrm{d}x$。
>
> 答案：令 $u=x^3$，$x^2\mathrm{d}x=\frac13\mathrm{d}u$，原式 $=\frac13\mathrm{e}^{x^3}+C$。

剩下的因子只能差一个常数。差的若是 $x$ 的函数，就补不上：想把 $\int\mathrm{e}^{x^2}\mathrm{d}x$ 写成 $\frac{\mathrm{e}^{x^2}}{2x}+C$，求导得 $\mathrm{e}^{x^2}-\frac{\mathrm{e}^{x^2}}{2x^2}$，多出一项，不对。常数可以在积分号外进出，$x$ 的函数不行。

**例 2**　求 $\int\tan x\,\mathrm{d}x$ 和 $\int\frac{\mathrm{d}x}{x\ln x}$（$x>1$）。

和例 1 相比，整体换了位置：它不在指数里，而在分母里。外层函数是 $\frac1u$，积分是 $\ln|u|$。

第一个积分，$\tan x=\frac{\sin x}{\cos x}$，分子 $\sin x\,\mathrm{d}x=-\mathrm{d}(\cos x)$，令 $u=\cos x$：

$$\int\tan x\,\mathrm{d}x=-\int\frac{\mathrm{d}u}{u}=-\ln|\cos x|+C.$$

第二个积分，老朋友 $\ln x$ 和 $\frac1x$ 同时出现，而 $\frac{\mathrm{d}x}{x}=\mathrm{d}(\ln x)$，令 $u=\ln x$：

$$\int\frac{\mathrm{d}x}{x\ln x}=\int\frac{\mathrm{d}u}{u}=\ln|\ln x|+C.$$

两个例子合起来，是一条常用的结论：在 $f$ 可导且处处不为 0 的区间上，把分母（或分母的某个因子）看成整体 $f$，分子恰是 $f'$（差一个常数倍也行）时，$\int\frac{f'(x)}{f(x)}\mathrm{d}x=\ln|f(x)|+C$。例 2 的第一个积分里整体是 $\cos x$；第二个积分里整体是分母的因子 $\ln x$，分子 $\frac1x$ 正是它的导数。

**例 3**　求 $\int\frac{\mathrm{d}x}{4+x^2}$ 和 $\int\frac{\mathrm{d}x}{\sqrt{9-x^2}}$。

和前两例不同，这里没有一个现成的「内层乘它的导数」，内层的导数藏在常数里：把分母提出一个 4，整体是 $\frac{x}{2}$，而 $\mathrm{d}x=2\,\mathrm{d}\big(\frac x2\big)$。

$$\int\frac{\mathrm{d}x}{4+x^2}=\frac14\int\frac{\mathrm{d}x}{1+(x/2)^2}=\frac12\int\frac{\mathrm{d}(x/2)}{1+(x/2)^2}=\frac12\arctan\frac x2+C.$$

第二个同样，提出 9，$\sqrt{9-x^2}=3\sqrt{1-(x/3)^2}$，$\mathrm{d}x=3\,\mathrm{d}\big(\frac x3\big)$：

$$\int\frac{\mathrm{d}x}{\sqrt{9-x^2}}=\int\frac{\mathrm{d}(x/3)}{\sqrt{1-(x/3)^2}}=\arcsin\frac x3+C.$$

一般地，$\int\frac{\mathrm{d}x}{a^2+x^2}=\frac1a\arctan\frac xa+C$，$\int\frac{\mathrm{d}x}{\sqrt{a^2-x^2}}=\arcsin\frac xa+C$（$a>0$）。

**例 4**　求 $\int\frac{\mathrm{d}x}{x^2+2x+5}$。

比例 3 又多一步：分母里有一次项，先配方，把它变成例 3 的样子。

$$x^2+2x+5=(x+1)^2+4,\qquad \int\frac{\mathrm{d}x}{(x+1)^2+4}=\frac12\arctan\frac{x+1}2+C.$$

这里 $\mathrm{d}x=\mathrm{d}(x+1)$，把 $x+1$ 当整体，套用例 3 的公式。

> 求 $\int\frac{\mathrm{d}x}{\sqrt{3-2x-x^2}}$。
>
> 答案：$3-2x-x^2=4-(x+1)^2$，原式 $=\arcsin\frac{x+1}2+C$。

**例 5**　求 $\int\sin^3x\,\mathrm{d}x$ 和 $\int\sin^2x\cos^3x\,\mathrm{d}x$。

例 1 到例 4 的整体都是一个函数，这里的整体是 $\sin x$ 或 $\cos x$ 自己，被积函数是它们的幂。

被积函数是三角函数的幂。看有没有奇次幂：有，就拆出一个 $\sin x$（或 $\cos x$）和 $\mathrm{d}x$ 凑成 $\mathrm{d}\cos x$（或 $\mathrm{d}\sin x$），剩下的偶次幂用平方关系 $\sin^2x+\cos^2x=1$ 换成另一个函数。

$$\int\sin^3x\,\mathrm{d}x=\int(1-\cos^2x)\sin x\,\mathrm{d}x=-\int(1-u^2)\,\mathrm{d}u=-\cos x+\frac{\cos^3x}3+C\quad(u=\cos x).$$

$$\int\sin^2x\cos^3x\,\mathrm{d}x=\int\sin^2x(1-\sin^2x)\,\mathrm{d}(\sin x)=\frac{\sin^3x}3-\frac{\sin^5x}5+C.$$

如果两个幂都是偶数，就没有可拆的奇次幂。这时用倍角公式降次：$\sin^2x=\frac{1-\cos2x}2$，$\cos^2x=\frac{1+\cos2x}2$。例如 $\int\cos^2x\,\mathrm{d}x=\frac x2+\frac{\sin2x}4+C$。

**例 6**　求 $\int\sec x\,\mathrm{d}x$。

和例 2 的 $\tan x$ 相比，这一题分子里没有现成的分母的导数，要先变形造出来。

$\sec x$ 读作正割，$\sec x=\frac1{\cos x}$；$\tan x$ 的导数是 $\sec^2x$，$\sec x$ 的导数用商法则：$\big(\frac1{\cos x}\big)'=\frac{\sin x}{\cos^2x}=\sec x\tan x$。这一题看不出整体，得先变形。先算 $\sec x+\tan x$ 的导数：

$$(\sec x+\tan x)'=\sec x\tan x+\sec^2x=\sec x(\sec x+\tan x),$$

它恰好是 $\sec x$ 乘上 $\sec x+\tan x$ 自己。这提示把 $\sec x+\tan x$ 当整体，于是乘一个「1」（分子分母同乘 $\sec x+\tan x$），让分子成为分母的导数：

$$\int\sec x\,\mathrm{d}x=\int\frac{\sec x(\sec x+\tan x)}{\sec x+\tan x}\,\mathrm{d}x=\int\frac{\mathrm{d}(\sec x+\tan x)}{\sec x+\tan x}=\ln|\sec x+\tan x|+C.$$

第二个等号用到上面算出的导数。

> 求 $\int\csc x\,\mathrm{d}x$（$\csc x=\frac1{\sin x}$，$\cot x=\frac{\cos x}{\sin x}$）。
>
> 答案：乘 $\csc x-\cot x$，分子成为 $\csc^2x-\csc x\cot x=(\csc x-\cot x)'$，原式 $=\ln|\csc x-\cot x|+C$。

**例 7**　求 $\int\frac{\mathrm{d}x}{\mathrm{e}^x+\mathrm{e}^{-x}}$。

和例 6 一样，这一题要先变形再凑微分，变形的目的也相同：让「整体的导数」出现。

分子分母同乘 $\mathrm{e}^x$ 之前，看不到整体。乘完以后：

$$\int\frac{\mathrm{e}^x\,\mathrm{d}x}{\mathrm{e}^{2x}+1}=\int\frac{\mathrm{d}(\mathrm{e}^x)}{1+(\mathrm{e}^x)^2}=\arctan(\mathrm{e}^x)+C.$$

变形是为了让 $\mathrm{e}^x\,\mathrm{d}x$ 出现。

**例 8**　用连续函数近似描述某应用的新增用户速度：$r(t)=\dfrac{200t}{1+t^2}$（人/天），其中 $t\ge0$ 是开始记录后的天数。求前 $T$ 天累计新增的用户数（$T\ge0$），并算 $T=10$ 时的近似值。

和例 2 相比，这一题只多了一个场景：被积函数是变化率，积分是累计量。

累计新增量是变化率的积分，$N(T)=\int_0^Tr(t)\,\mathrm{d}t$（不含开始记录时已有的用户）。被积式里分子 $t\,\mathrm{d}t=\frac12\mathrm{d}(1+t^2)$，和例 2 一样是分子为分母导数的类型：

$$N(T)=100\int_0^T\frac{\mathrm{d}(1+t^2)}{1+t^2}=100\ln(1+T^2).$$

$T=10$ 时 $N=100\ln101\approx461.5$，也就是累计新增约 462 人。新增速度在 $t=1$ 时最大（100 人/天），之后逐天下降，所以累计新增数只以对数的速度增长。

**回扣 C.6.5：用凑微分找辅助函数。** C.6.5 里为证明「存在 $\xi$ 使某个式子为 0」而构造辅助函数时，是靠观察猜出来的。现在可以有步骤地倒推：把待证式里的 $\xi$ 换成 $x$，看成一个关于 $f$ 的方程，把它解出来，整理成「某个式子 $=$ 常数」的样子，这个式子就是辅助函数。

**例 9**　设 $f$ 在 $[0,1]$ 上连续，在 $(0,1)$ 内可导，$f(0)=f(1)=0$。证明存在 $\xi\in(0,1)$，使 $(1+\xi^2)f'(\xi)+2\xi f(\xi)=0$。

这一题用凑微分的反向：目标是用积分找一个函数，而不是算一个积分。

要找 $F$，使 $F'(x)$ 恰是 $(1+x^2)f'(x)+2xf(x)$ 的某个倍数。办法是先把 $f$ 暂时看成方程 $(1+x^2)f'+2xf=0$ 的未知解，把方程解出来，看哪个组合是常数。两边除以 $(1+x^2)f$，分离出 $\frac{f'}f$：

$$\frac{f'(x)}{f(x)}=-\frac{2x}{1+x^2}\ \Longrightarrow\ \ln|f(x)|=-\ln(1+x^2)+C_1\ \Longrightarrow\ (1+x^2)f(x)=C.$$

右边的积分是例 2 的类型。这只是找线索，不是对题目给定的 $f$ 的断言：线索是 $(1+x^2)f$ 在方程的解上是常数，所以猜 $F(x)=(1+x^2)f(x)$ 的导数带着待证式。下面的证明只用 $F$ 的定义、求导和罗尔定理，不再用除以 $f$ 的那一步，所以 $f$ 可能为 0 也不影响。直接求导验证：

$$F'(x)=2xf(x)+(1+x^2)f'(x).$$

$F$ 在 $[0,1]$ 上连续，在 $(0,1)$ 内可导，$F(0)=f(0)=0$，$F(1)=2f(1)=0$。由罗尔定理（C.6），存在 $\xi\in(0,1)$ 使 $F'(\xi)=0$，就是要证的等式。

这个套路对 $f'+g'f=0$ 型都适用：辅助函数是 $F=f\mathrm{e}^{g}$。

凑微分有一个前提：被积式里要有现成的整体，它的导数还得在旁边。$\int\sqrt{1-x^2}\,\mathrm{d}x$ 里一个这样的整体也没有，根号里 $1-x^2$ 的导数 $-2x$ 不在被积式里。这样的积分怎么办，是下一节的问题。

合上书，写出第一类换元法的公式，并说出它是哪条求导法则倒过来；再对 $\int\frac{x}{1+x^2}\mathrm{d}x$ 说出你找的整体是什么。

### 2. 根号去不掉时，怎样换一个变量？

上一节留下的问题是 $\int\sqrt{1-x^2}\,\mathrm{d}x$。被积函数里有根号，可是被积式里没有 $x\,\mathrm{d}x$ 来配合凑成 $\mathrm{d}(1-x^2)$，直接凑微分行不通。曲线 $y=\sqrt{1-x^2}$ 是单位圆的上半圆，这提示我们用三角函数处理根号；若另求定积分 $\int_0^1\sqrt{1-x^2}\,\mathrm{d}x$，它才对应四分之一单位圆的面积。

根号让这个积分变难。想法反过来：不去找现成的整体，而是主动换一个变量 $x=\varphi(t)$，选得巧，让根号开得出来。令 $x=\sin t$，取 $-\frac\pi2<t<\frac\pi2$，此时 $\cos t>0$，所以 $\sqrt{1-x^2}=\sqrt{1-\sin^2t}=\cos t$，根号消失。

先把这个做法写成一般的结论。设 $x=\varphi(t)$ 在某个区间上可导、$\varphi'(t)\ne0$、严格单调，因此有反函数 $t=\varphi^{-1}(x)$。这就是**第二类换元法**：

$$\int f(x)\,\mathrm{d}x=\Big[\int f\big(\varphi(t)\big)\varphi'(t)\,\mathrm{d}t\Big]_{t=\varphi^{-1}(x)}.$$

证明分两步。设 $G(t)$ 是 $f(\varphi(t))\varphi'(t)$ 的一个原函数，只要证明 $G(\varphi^{-1}(x))$ 的导数是 $f(x)$。

1. 由复合函数求导，$\dfrac{\mathrm{d}}{\mathrm{d}x}G\big(\varphi^{-1}(x)\big)=G'(t)\cdot\dfrac{\mathrm{d}t}{\mathrm{d}x}$，这里 $t=\varphi^{-1}(x)$。
2. $G'(t)=f(\varphi(t))\varphi'(t)$；反函数的导数是 $\dfrac{\mathrm{d}t}{\mathrm{d}x}=\dfrac1{\varphi'(t)}$（C.4.7）。代入，$\varphi'(t)$ 约掉，剩下 $f(\varphi(t))=f(x)$。

因此回到 $x$ 的那一步不是可有可无的：必须用反函数 $t=\varphi^{-1}(x)$ 换回去。这是两类换元最大的操作区别。

把两类放在一起对照：

| | 第一类（凑微分） | 第二类 |
|---|---|---|
| 谁是新变量 | $u=u(x)$，是原来式子里已有的整体 | $x=\varphi(t)$，是自己设的 |
| 起点 | 看出「内层乘内层的导数」 | 被积函数里有去不掉的根号 |
| 换回 | 代回 $u=u(x)$ 即可 | 要用反函数 $t=\varphi^{-1}(x)$ |

同一个外观有时两类都能用。$\int x\sqrt{1-x^2}\,\mathrm{d}x$ 有现成的整体：令 $u=1-x^2$，$x\,\mathrm{d}x=-\frac12\mathrm{d}u$，得 $-\frac13(1-x^2)^{3/2}+C$，一行。用 $x=\sin t$ 也能做，但绕远了。而 $\int\sqrt{1-x^2}\,\mathrm{d}x$ 不适合直接凑微分，本节先用第二类换元处理；第 5 节的分部积分也能求出它。多出来的那个 $x$ 影响的是哪条路更省事，并不决定某种方法是否唯一可用。

**三角代换。** 下表设 $a>0$。三种根式对应三种设法，依据都是平方关系（若 $\sec$ 忘了，$\sec t=\frac1{\cos t}$，且 $1+\tan^2t=\sec^2t$）。求不定积分时先在各个开区间内部使用换元；定积分的端点可以取相应的边界值。

| 被积函数含 | 令 | 化成 | $\mathrm{d}x$ |
|---|---|---|---|
| $\sqrt{a^2-x^2}$ | $x=a\sin t$，$t\in(-\frac\pi2,\frac\pi2)$ | $a\cos t$ | $a\cos t\,\mathrm{d}t$ |
| $\sqrt{a^2+x^2}$ | $x=a\tan t$，$t\in(-\frac\pi2,\frac\pi2)$ | $a\sec t$ | $a\sec^2t\,\mathrm{d}t$ |
| $\sqrt{x^2-a^2}$ | $x=a\sec t$，$t\in(0,\frac\pi2)$（$x>a$） | $a\tan t$ | $a\sec t\tan t\,\mathrm{d}t$ |

限定 $t$ 的范围是为了让开方的符号确定。第一行：$\sqrt{a^2-a^2\sin^2t}=a|\cos t|$，所选的 $t$ 使 $\cos t>0$，所以可以写成 $a\cos t$；这个范围同时让 $\sin t$ 单调，方便换回。第二行：$\sqrt{a^2+a^2\tan^2t}=a|\sec t|$，$t\in(-\frac\pi2,\frac\pi2)$ 时 $\sec t>0$。第三行：$\sqrt{a^2\sec^2t-a^2}=a|\tan t|$，$t\in(0,\frac\pi2)$ 时 $\tan t>0$。第三行示范的是正半轴的一支；$x<-a$ 时可先令 $x=-y$，转到 $y>a$。

积出关于 $t$ 的结果以后，要换回 $x$。最不容易错的办法是画直角三角形：由代换式标出一条直角边和斜边，第三边用勾股定理，然后读出其余的三角函数。图只示意正边长的情形；$x<0$ 时用代换式和 $t$ 的范围确定符号，不把负的 $x$ 直接当边长。

![下面用正边长的直角三角形示意，设 $a>0$，前两图取 $x>0$，第三图取 $x>a$，角 $t$ 位于右下方的锐角：$x=a\sin t$ 时对边 $x$、斜边 $a$，邻边 $\sqrt{a^2-x^2}$；$x=a\tan t$ 时对边 $x$、邻边 $a$，斜边 $\sqrt{a^2+x^2}$；$x=a\sec t$ 时斜边 $x$、邻边 $a$，对边 $\sqrt{x^2-a^2}$](fig/C11-n1.pdf){width=92%}

**方法 2（第二类换元）**

1. 看根式：$\sqrt{a^2-x^2}$、$\sqrt{a^2+x^2}$、$\sqrt{x^2-a^2}$ 分别用 $\sin$、$\tan$、$\sec$ 代换；$\sqrt[n]{ax+b}$ 令整个根式为 $t$；分母次数远高于分子时试倒代换 $x=\frac1t$。
2. 把 $x$、$\mathrm{d}x$ 和根式都换成 $t$ 的式子，积分。
3. 画直角三角形（根式代换则解出 $t=\varphi^{-1}(x)$），换回 $x$。

**例 10**　求 $\int\sqrt{4-x^2}\,\mathrm{d}x$。

和例 1 相比，那里的整体 $x^2$ 本来就在式子里，这里没有，要自己设一个变量把根号开掉。

按表第一行，$a=2$，令 $x=2\sin t$，$t\in(-\frac\pi2,\frac\pi2)$。则 $\sqrt{4-x^2}=2\cos t$，$\mathrm{d}x=2\cos t\,\mathrm{d}t$（$\mathrm{d}x$ 也要换，只换根号会少一个 $\cos t$），代入得

$$\int\sqrt{4-x^2}\,\mathrm{d}x=\int4\cos^2t\,\mathrm{d}t .$$

用降次公式 $\cos^2t=\frac{1+\cos2t}2$，再积分：

$$\int4\cos^2t\,\mathrm{d}t=2\int(1+\cos2t)\,\mathrm{d}t=2t+\sin2t+C=2t+2\sin t\cos t+C .$$

换回 $x$：由 $\sin t=\frac x2$，$t=\arcsin\frac x2$，$\cos t=\frac{\sqrt{4-x^2}}2$（$\cos t>0$，也是三角形的邻边）。于是

$$\int\sqrt{4-x^2}\,\mathrm{d}x=2\arcsin\frac x2+\frac x2\sqrt{4-x^2}+C.$$

> 求 $\int\frac{\mathrm{d}x}{x^2\sqrt{1-x^2}}$。
>
> 答案：$x=\sin t$，原式 $=\int\frac{\mathrm{d}t}{\sin^2t}=-\cot t+C=-\frac{\sqrt{1-x^2}}x+C$。

**例 11**　求 $\int\frac{\mathrm{d}x}{\sqrt{x^2+1}}$。

和例 10 相比，根式变成 $\sqrt{a^2+x^2}$，用第二行的正切代换，最后要积出例 6 的 $\sec$。令 $x=\tan t$，则 $\sqrt{x^2+1}=\sec t$，$\mathrm{d}x=\sec^2t\,\mathrm{d}t$：

$$\int\frac{\sec^2t}{\sec t}\,\mathrm{d}t=\int\sec t\,\mathrm{d}t=\ln|\sec t+\tan t|+C.$$

由所选范围内 $\sec t>0$ 以及 $\sec^2t=1+\tan^2t$，可得 $\sec t=\sqrt{1+x^2}$，$\tan t=x$（这些关系对正负 $x$ 都成立；三角形里对边 $x$、邻边 1、斜边 $\sqrt{x^2+1}$ 只是 $x>0$ 时的示意）：

$$\int\frac{\mathrm{d}x}{\sqrt{x^2+1}}=\ln\big(x+\sqrt{x^2+1}\big)+C.$$

> 求 $\int\frac{\mathrm{d}x}{x^2\sqrt{x^2+1}}$。
>
> 答案：$x=\tan t$，原式 $=\int\frac{\cos t}{\sin^2t}\mathrm{d}t=-\frac1{\sin t}+C=-\frac{\sqrt{x^2+1}}x+C$。

**例 12**　求 $\int\frac{\sqrt{x^2-1}}x\,\mathrm{d}x$（$x>1$）。

和例 11 相比，根式从 $\sqrt{a^2+x^2}$ 变成 $\sqrt{x^2-a^2}$，换成表里第三行。

根式是 $\sqrt{x^2-a^2}$，用第三行。令 $x=\sec t$，$t\in(0,\frac\pi2)$，则 $\sqrt{x^2-1}=\tan t$，$\mathrm{d}x=\sec t\tan t\,\mathrm{d}t$：

$$\int\frac{\tan t}{\sec t}\sec t\tan t\,\mathrm{d}t=\int\tan^2t\,\mathrm{d}t=\int(\sec^2t-1)\,\mathrm{d}t=\tan t-t+C.$$

第三个等号用 $\tan^2t=\sec^2t-1$（即 $1+\tan^2t=\sec^2t$），第四个等号用 $\sec^2t$ 的原函数是 $\tan t$。

三角形里斜边 $x$、邻边 1、对边 $\sqrt{x^2-1}$，所以 $\tan t=\sqrt{x^2-1}$，$t=\arccos\frac1x$：

$$\int\frac{\sqrt{x^2-1}}x\,\mathrm{d}x=\sqrt{x^2-1}-\arccos\frac1x+C.$$

**例 13**　求 $\int\frac{\mathrm{d}x}{x\sqrt{x-1}}$。

和例 10 到例 12 相比，根号里只是一次式，不必用三角函数，换元更简单。

这里根号里是一次式，不需要三角函数。令整个根式为新变量 $t=\sqrt{x-1}$（$t>0$），则 $x=t^2+1$，$\mathrm{d}x=2t\,\mathrm{d}t$：

$$\int\frac{2t\,\mathrm{d}t}{(t^2+1)t}=2\int\frac{\mathrm{d}t}{1+t^2}=2\arctan t+C=2\arctan\sqrt{x-1}+C.$$

**例 14**　求 $\int\frac{\mathrm{d}x}{x(x^4+1)}$（$x>0$）。

和例 13 相比，这里没有根号，换元的目的变了：用倒数把分母里的高次幂挪到分子。

分母的次数（5）远高于分子（0）。这时令 $x=\frac1t$，$\mathrm{d}x=-\frac{\mathrm{d}t}{t^2}$，分母变成 $\frac1t\big(\frac1{t^4}+1\big)=\frac{1+t^4}{t^5}$，高次的幂跑到了分子：

$$\int\frac{t^5}{1+t^4}\cdot\Big(-\frac{\mathrm{d}t}{t^2}\Big)=-\int\frac{t^3}{1+t^4}\mathrm{d}t=-\frac14\ln(1+t^4)+C=\ln x-\frac14\ln(1+x^4)+C.$$

中间一步是凑微分 $t^3\mathrm{d}t=\frac14\mathrm{d}(t^4)$，倒代换后又用回了第一类换元。

两类换元都在不定积分里做，最后总要换回 $x$，这一步既麻烦又容易错。积分如果带着上下限，这一步能不能省掉，上下限又该怎么办？这是下一节的问题。

合上书，说出三种根式各用什么代换，以及换回 $x$ 为什么要靠直角三角形。

### 3. 定积分换元时，上下限怎样跟着变？

先回到上一节开头的半圆：$\int_0^1\sqrt{1-x^2}\,\mathrm{d}x$。按第 2 节的做法，要先求出原函数 $\frac12\big(\arcsin x+x\sqrt{1-x^2}\big)$ 并换回 $x$，再代入 $x=1$ 和 $x=0$。其实不必换回：令 $x=\sin t$，$x=0$ 对应 $t=0$，$x=1$ 对应 $t=\frac\pi2$，求出关于 $t$ 的原函数以后，直接代这两个 $t$ 的值就行。定积分的结果是一个数，所以只要上下限一起换，算出来的数就是答案。下面把这个做法写成一般的结论。

设 $f$ 在 $[a,b]$ 上连续，$x=\varphi(t)$ 在 $[\alpha,\beta]$ 上有连续的导数，$\varphi(\alpha)=a$，$\varphi(\beta)=b$，且当 $t$ 在 $[\alpha,\beta]$ 里变化时，$\varphi(t)$ 始终落在 $[a,b]$ 内。则

$$\int_a^bf(x)\,\mathrm{d}x=\int_\alpha^\beta f\big(\varphi(t)\big)\varphi'(t)\,\mathrm{d}t.$$

证明很短。设 $F$ 是 $f$ 的原函数，由链式法则 $F(\varphi(t))$ 是 $f(\varphi(t))\varphi'(t)$ 的原函数。对右边用牛顿–莱布尼茨公式：

$$\int_\alpha^\beta f\big(\varphi(t)\big)\varphi'(t)\,\mathrm{d}t=F\big(\varphi(\beta)\big)-F\big(\varphi(\alpha)\big)=F(b)-F(a)=\int_a^bf(x)\,\mathrm{d}x.$$

注意公式里 $\varphi$ 不要求单调，也不要求有反函数，因为根本没有「换回」这一步。第一类换元的定积分也一样：写出新变量 $u=u(x)$ 时，上下限换成 $u(a)$、$u(b)$；只是把整体凑成微分而不引入字母，就不用换限。

**方法 3（定积分换元）**

1. 设 $x=\varphi(t)$（或 $u=u(x)$）。
2. 换限：$x=a$ 对应 $t=\alpha$，$x=b$ 对应 $t=\beta$。一个 $x$ 对应几个 $t$ 时，选 $\varphi$ 的取值始终在积分区间内的那一支。
3. 在新变量下积分，直接代入新的上下限，不回代。

**例 15**　求 $\int_0^1\sqrt{1-x^2}\,\mathrm{d}x$。

这就是本节开头的小情形，也是例 10 的定积分版（$a=1$），完整写出来。令 $x=\sin t$，$x=0$ 对应 $t=0$，$x=1$ 对应 $t=\frac\pi2$。被积式变成 $\cos t\cdot\cos t\,\mathrm{d}t$：

$$\int_0^1\sqrt{1-x^2}\,\mathrm{d}x=\int_0^{\pi/2}\cos^2t\,\mathrm{d}t=\Big[\frac t2+\frac{\sin2t}4\Big]_0^{\pi/2}=\frac\pi4.$$

第二个等号用降次公式 $\cos^2t=\frac{1+\cos2t}2$。

这个数正好是单位圆在第一象限的面积（四分之一个圆），换元没有改变积分，只是换了一种方式算同一块面积。

![$x=\sin t$ 把 $x$ 轴上的 $[0,1]$ 对应到弧上的 $t\in[0,\frac\pi2]$：窄条的宽度 $\mathrm{d}x=\cos t\,\mathrm{d}t$，高度 $\sqrt{1-x^2}=\cos t$；阴影是四分之一单位圆，面积 $\frac\pi4$](fig/C11-n2.pdf){width=55%}

> 求 $\int_1^4\frac{\mathrm{d}x}{\sqrt x(1+\sqrt x)}$。
>
> 答案：$t=\sqrt x$，限 $1\to1$、$4\to2$，$\mathrm{d}x=2t\,\mathrm{d}t$，原式 $=\int_1^2\frac{2\,\mathrm{d}t}{1+t}=2\ln\frac32$。

**例 16**　求 $\int_0^4\frac{\mathrm{d}x}{1+\sqrt x}$。

和例 15 相比，同样是定积分换元，但这里换的是根式 $\sqrt x$（例 13 的办法），要看上下限怎样跟着走。

令 $t=\sqrt x$，$x=t^2$，$\mathrm{d}x=2t\,\mathrm{d}t$，限 $0\to0$、$4\to2$：

$$\int_0^2\frac{2t}{1+t}\mathrm{d}t=2\int_0^2\Big(1-\frac1{1+t}\Big)\mathrm{d}t=2\big[t-\ln(1+t)\big]_0^2=4-2\ln3.$$

两道例题都没有再回到 $x$。

**使用上面的换元定理时，要检查换元函数是否满足所列条件。** 例如 $\int_{-1}^{1}\frac{\mathrm{d}x}{1+x^2}=\frac\pi2$。若令 $x=\frac1t$，只按端点取 $t=-1$ 到 $t=1$，新积分区间跨过了 $t=0$，而 $\frac1t$ 在 $t=0$ 没有定义；它也不能把整段 $[-1,1]$ 映到原积分区间内，所以不能这样套公式，硬算还会得到负值。连续可导是本节采用的充分条件，不要把它理解成所有换元做法的必要条件。

**积分号里含 $x$ 时，先换元，让 $x$ 跑到积分限上。** C.10.1 的变限积分求导有一个前提：被积函数里没有 $x$。设 $f$ 连续。遇到 $\int_0^xf(x-t)\,\mathrm{d}t$ 这样的式子，被积函数里的 $x$ 卡住了求导，办法就是换元，让它只出现在积分限里。

- $\int_0^xf(x-t)\,\mathrm{d}t$：令 $u=x-t$，$t=0\to u=x$，$t=x\to u=0$，$\mathrm{d}t=-\mathrm{d}u$，得 $\int_0^xf(u)\,\mathrm{d}u$，导数是 $f(x)$。
- $\int_0^1f(xt)\,\mathrm{d}t$（$x\ne0$）：令 $u=xt$，$\mathrm{d}t=\frac{\mathrm{d}u}x$，$t:0\to1$ 对应 $u:0\to x$，得 $\frac1x\int_0^xf(u)\,\mathrm{d}u$，$x$ 只出现在积分限和系数里，可以求导。

读者容易想到不换元、直接求导：对 $\int_0^xf(x-t)\,\mathrm{d}t$，若只把上限的 $x$ 当变量，得到 $f(x-x)=f(0)$，漏掉了被积函数里 $x$ 的贡献；换元之后的正确导数是 $f(x)$。

**例 17**　设 $f$ 连续，求 $F(x)=\int_0^xt\,f(x^2-t^2)\,\mathrm{d}t$ 的导数 $F'(x)$。

和例 15、例 16 相比，被积函数里多了一个参数 $x$，换元的目的是让它只留在积分限里；用的仍是第一类换元（凑 $t\,\mathrm{d}t$）。

被积函数里有 $x$，所以先换元。内层是 $x^2-t^2$，它对 $t$ 的导数含有 $-2t$，被积函数里恰好有一个 $t$，所以令 $u=x^2-t^2$，$t\,\mathrm{d}t=-\frac12\mathrm{d}u$。限：$t=0\to u=x^2$，$t=x\to u=0$：

$$F(x)=-\frac12\int_{x^2}^{0}f(u)\,\mathrm{d}u=\frac12\int_0^{x^2}f(u)\,\mathrm{d}u.$$

现在 $x$ 只在上限里。上限是 $x^2$，由变限积分求导加链式法则（C.10.1），$F'(x)=\frac12f(x^2)\cdot2x=x\,f(x^2)$。

> 设 $f$ 连续，求 $G(x)=\int_0^xt^2f(x^3-t^3)\,\mathrm{d}t$ 的导数。
>
> 答案：令 $u=x^3-t^3$，$t^2\mathrm{d}t=-\frac13\mathrm{d}u$，限 $t:0\to x$ 对应 $u:x^3\to0$，$G(x)=\frac13\int_0^{x^3}f(u)\,\mathrm{d}u$，$G'(x)=\frac13f(x^3)\cdot3x^2=x^2f(x^3)$。

**例 18**　设 $f$ 连续，$\lim_{x\to0}\frac{f(x)}x=A$。令 $H(x)=\int_0^1f(xt)\,\mathrm{d}t$，求 $H'(0)$，并判断 $H'$ 在 $0$ 处是否连续。

和例 17 相比，这里 $x$ 出现在 $f$ 的自变量里（$xt$），并且要讨论 $x=0$。

难点在 $x=0$ 处不能直接套公式。分三步。

第一步，求 $H(0)$。$f$ 连续，且 $f(x)=x\cdot\frac{f(x)}x\to0\cdot A=0$（$x\to0$），所以 $f(0)=0$。于是 $H(0)=\int_0^1f(0)\,\mathrm{d}t=0$。

第二步，求 $x\ne0$ 时的 $H(x)$。令 $u=xt$，$\mathrm{d}t=\frac{\mathrm{d}u}x$，$t:0\to1$ 对应 $u:0\to x$：

$$H(x)=\frac1x\int_0^xf(u)\,\mathrm{d}u.$$

第三步，按导数的定义求 $H'(0)=\lim_{x\to0}\frac{H(x)-H(0)}x$，用洛必达法则（分子 $\int_0^xf$ 的导数是 $f(x)$）：

$$H'(0)=\lim_{x\to0}\frac{\int_0^xf(u)\,\mathrm{d}u}{x^2}=\lim_{x\to0}\frac{f(x)}{2x}=\frac A2.$$

再看 $x\ne0$ 时，由 $H(x)=\frac1x\int_0^xf(u)\,\mathrm{d}u$ 求导：

$$H'(x)=-\frac1{x^2}\int_0^xf(u)\,\mathrm{d}u+\frac{f(x)}x .$$

令 $x\to0$，分别看两项。第一项由上面刚算的 $\lim\frac{\int_0^xf}{x^2}=\frac A2$，极限是 $-\frac A2$；第二项的极限是 $A$。所以

$$\lim_{x\to0}H'(x)=-\frac A2+A=\frac A2=H'(0),$$

$H'$ 在 0 处连续。

换元可以用来化简被积函数，但有时连原函数也不必求。积分区间要是有对称性，用 $x\to-x$ 这样的换元，也许就能直接看出积分值，这是下一节的问题。

合上书，写出定积分换元的公式，说明为什么不用回代，并举一个换元函数在区间上有断点的例子。

### 4. 不求原函数，能不能借对称性把积分化简？

有些积分的原函数很难求，甚至写不出来，但积分区间有一点对称性，就能不求原函数而把积分变简单。这一节讲三种，用的工具都是 $x\to c-x$（或 $-x$）这类换元，换完以后被积函数不变或变成已知的样子。

#### 对称区间上，积分值能直接看出来吗？

先看两个小情形：$\int_{-1}^{1}x^3\,\mathrm{d}x=\big[\frac{x^4}4\big]_{-1}^{1}=0$，而 $\int_{-1}^{1}x^2\,\mathrm{d}x=\frac23=2\int_0^1x^2\,\mathrm{d}x$。图上看，$x^3$ 在原点两侧的有符号面积抵消，$x^2$ 的两侧一样大。下面对一般的 $f$ 说明这是为什么。设 $f$ 在 $[-a,a]$ 上连续。把积分拆成两半，对 $[-a,0]$ 上的那一半令 $x=-t$：

$$\int_{-a}^{a}f(x)\,\mathrm{d}x=\int_{0}^{a}f(x)\,\mathrm{d}x+\int_{-a}^{0}f(x)\,\mathrm{d}x=\int_0^af(x)\,\mathrm{d}x+\int_0^af(-t)\,\mathrm{d}t.$$

第二个等号里 $t$ 的限是 $a\to0$，$\mathrm{d}x=-\mathrm{d}t$，两个负号抵消，变成 $0\to a$。所以

$$\int_{-a}^{a}f(x)\,\mathrm{d}x=\int_0^a\big[f(x)+f(-x)\big]\mathrm{d}x.$$

$f$ 是奇函数时括号里是 0，积分为 0；$f$ 是偶函数时括号里是 $2f(x)$，积分是 $2\int_0^af$。图上看，奇函数在两侧的有符号面积正好抵消。

![左：偶函数 $f(x)=1-x^2$ 在 $[-1,1]$ 上，左右两块阴影一样大，积分是 $2\int_0^1$；右：奇函数 $g(x)=x^3$ 在 $[-1,1]$ 上，$x>0$ 的阴影在 $x$ 轴上方、$x<0$ 的阴影在下方，两块面积相等、符号相反，积分为 0](fig/C11-n3.pdf){width=85%}

括号里的 $f(x)+f(-x)$ 说明一件事：任何函数都能写成偶部加奇部，在对称区间上，奇部的贡献为零，只有偶部活下来。区间必须关于原点对称，否则奇函数也不再抵消：$\int_{-1}^{2}x\,\mathrm{d}x=\frac32\ne0$。

**方法 4（对称性）**

1. 积分区间是 $[-a,a]$：先看被积函数的奇偶性，把能判断的部分拆开，奇部直接记 0。
2. 被积函数没有明显奇偶性：试 $f(x)+f(-x)$ 是否化简。
3. 被积函数是周期函数，积分区间长度是周期的整数倍：只积一个周期。
4. 积分区间是 $[a,b]$，被积函数换成 $f(a+b-x)$ 后与原来有关系：用区间再现，列方程解出积分。

**例 19**　求 $\int_{-1}^{1}\big(x+\sqrt{1-x^2}\big)^2\,\mathrm{d}x$。

这里仍是例 15 用过的半圆函数 $\sqrt{1-x^2}$，区间换成了 $[-1,1]$，这次不换元，借对称性。

平方展开，一共三项：

$$\big(x+\sqrt{1-x^2}\big)^2=x^2+2x\sqrt{1-x^2}+(1-x^2)=1+2x\sqrt{1-x^2}.$$

$x\sqrt{1-x^2}$ 是奇函数（$x$ 奇，$\sqrt{1-x^2}$ 偶），在 $[-1,1]$ 上积分为 0。剩下 $\int_{-1}^11\,\mathrm{d}x=2$。

> 求 $\int_{-\pi}^{\pi}(x\cos x+\sin^2x)\,\mathrm{d}x$。
>
> 答案：$x\cos x$ 是奇函数，积分为 0；$\sin^2x=\frac{1-\cos2x}2$，$\int_{-\pi}^\pi=\pi$。结果 $\pi$。

**例 20**　求 $\int_{-2}^{2}\frac{\mathrm{d}x}{1+\mathrm{e}^x}$。

和例 19 不同，被积函数既不奇也不偶，拆不出来。用括号里的组合：

$$\frac1{1+\mathrm{e}^x}+\frac1{1+\mathrm{e}^{-x}}=\frac1{1+\mathrm{e}^x}+\frac{\mathrm{e}^x}{\mathrm{e}^x+1}=1.$$

第二项是分子分母同乘 $\mathrm{e}^x$ 得到的。

所以 $\int_{-2}^2\frac{\mathrm{d}x}{1+\mathrm{e}^x}=\int_0^21\,\mathrm{d}x=2$。

> 求 $\int_{-1}^1\frac{\mathrm{d}x}{1+2^x}$。
>
> 答案：$\frac1{1+2^x}+\frac1{1+2^{-x}}=1$，积分 $=\int_0^11\,\mathrm{d}x=1$。

#### 积分区间是整数个周期时，起点重要吗？

先看 $\sin x$，周期是 $2\pi$：$\int_a^{a+2\pi}\sin x\,\mathrm{d}x=\cos a-\cos(a+2\pi)=0$，不论 $a$ 是多少。一般的周期函数也是这样。设 $f$ 以 $T$ 为周期，连续。令 $\Phi(a)=\int_a^{a+T}f(x)\,\mathrm{d}x$，把 $a$ 看成变量。上限、下限都带着 $a$。把 $\Phi(a)$ 写成 $\int_0^{a+T}f-\int_0^af$，再对两个上限分别用变限积分求导（C.10.1），下限的那一项带负号：

$$\Phi'(a)=f(a+T)-f(a)=0.$$

所以 $\Phi$ 是常数，和起点无关：一个周期上的积分不依赖于从哪里开始，$\int_a^{a+T}f=\int_0^Tf$。推论 $\int_0^{nT}f=n\int_0^Tf$（$n$ 是正整数）。区间长度必须正好是整数个周期：$\sin x$ 的周期是 $2\pi$，长度都是 $\pi$ 的 $\int_0^\pi\sin x\,\mathrm{d}x=2$ 与 $\int_{\pi/2}^{3\pi/2}\sin x\,\mathrm{d}x=0$ 就不相等。

**例 21**　求 $\int_0^{100\pi}\sqrt{1-\cos2x}\,\mathrm{d}x$。

和例 19 相比，对称性换成了周期性：不再是 $[-a,a]$，而是整数个周期；被积函数也得先化简。

先化简被积函数：$1-\cos2x=2\sin^2x$，所以 $\sqrt{1-\cos2x}=\sqrt2\,|\sin x|$。读者很容易想到直接写成 $\sqrt2\sin x$，但 $\sin x$ 有正有负，开方得到的是 $|\sin x|$，不能直接去掉绝对值。$|\sin x|$ 的周期是 $\pi$，积分区间 $100\pi$ 是 100 个周期：

$$\int_0^{100\pi}\sqrt2|\sin x|\,\mathrm{d}x=100\sqrt2\int_0^\pi\sin x\,\mathrm{d}x=100\sqrt2\cdot2=200\sqrt2.$$

#### 把区间左右对调，积分值为什么不变？

先看 $\int_0^1x^2\,\mathrm{d}x=\frac13$。作 $x\to1-x$ 的对调，被积函数变成 $(1-x)^2$，而 $\int_0^1(1-x)^2\,\mathrm{d}x=\frac13$，值没有变，只是把同一块面积左右对调。一般的区间 $[a,b]$ 上，在 $\int_a^bf(x)\,\mathrm{d}x$ 里令 $x=a+b-t$：$x=a$ 对应 $t=b$，$x=b$ 对应 $t=a$，$\mathrm{d}x=-\mathrm{d}t$，上下限对调抵消负号：

$$\int_a^bf(x)\,\mathrm{d}x=\int_a^bf(a+b-t)\,\mathrm{d}t=\int_a^bf(a+b-x)\,\mathrm{d}x.$$

翻转一次，积分值不变，被积函数却变了样子。如果新样子和原来有关系，就能列方程解出 $I$。常见的关系有两种：翻转后得到一个「伙伴」$J$，而 $I+J$ 很好算；或者翻转后得到「好算的部分 $-\,I$」，不产生新伙伴，而是把 $I$ 带着负号送回来。

![区间再现：$I$ 的被积函数 $\frac{\sin x}{\sin x+\cos x}$（实线）与伙伴 $J$ 的被积函数 $\frac{\cos x}{\sin x+\cos x}$（虚线）关于 $x=\frac\pi4$ 左右对称，所以两块面积 $I=J$；两条曲线上下相加恒等于 1（点线），所以 $I+J=\frac\pi2$](fig/C11-n4.pdf){width=60%}

**例 22**　求 $I=\int_0^{\pi/2}\frac{\sin x}{\sin x+\cos x}\,\mathrm{d}x$。

和例 19、例 20 不同，区间 $[0,\frac\pi2]$ 并不关于原点对称，但 $x\to a+b-x$ 对任何区间都能做。

这里 $a+b=\frac\pi2$，翻转是 $x\to\frac\pi2-x$，把 $\sin$ 与 $\cos$ 互换。翻转后得到伙伴

$$J=\int_0^{\pi/2}\frac{\cos x}{\sin x+\cos x}\,\mathrm{d}x.$$

翻转不改变积分值，所以 $I=J$。另一方面，两个式子相加，分子分母约去：

$$I+J=\int_0^{\pi/2}1\,\mathrm{d}x=\frac\pi2.$$

两式联立，$I=J=\frac\pi4$。

> 求 $\int_0^{\pi/2}\frac{\sin^3x}{\sin^3x+\cos^3x}\,\mathrm{d}x$。
>
> 答案：翻转后得到伙伴 $J=\int\frac{\cos^3x}{\sin^3x+\cos^3x}$，$I=J$，$I+J=\frac\pi2$，所以 $I=\frac\pi4$。

**例 23**　求 $I=\int_0^\pi\frac{x\sin x}{1+\cos^2x}\,\mathrm{d}x$。

和例 22 不同，这一题的被积函数里有一个单独的 $x$，这是区间再现最典型的用武之地：翻转 $x\to\pi-x$，$\sin(\pi-x)=\sin x$，$\cos^2(\pi-x)=\cos^2x$，只有 $x$ 变成 $\pi-x$：

$$I=\int_0^\pi\frac{(\pi-x)\sin x}{1+\cos^2x}\,\mathrm{d}x=\pi\int_0^\pi\frac{\sin x}{1+\cos^2x}\,\mathrm{d}x-I.$$

直接的想法是分部（取 $u=x$），但 $\int\frac{\sin x}{1+\cos^2x}\mathrm{d}x=-\arctan(\cos x)$，新积分 $\int\arctan(\cos x)\,\mathrm{d}x$ 比原来的更难，所以不走这条路。上面翻转后，$I$ 又出现在右边，带着负号。移项，$2I=\pi\int_0^\pi\frac{\sin x}{1+\cos^2x}\,\mathrm{d}x$，右边的积分凑微分：

$$\int_0^\pi\frac{\sin x}{1+\cos^2x}\,\mathrm{d}x=\Big[-\arctan(\cos x)\Big]_0^\pi=\frac\pi4+\frac\pi4=\frac\pi2,$$

所以 $I=\frac{\pi^2}4$。这个定积分可以借对称性直接计算，不需要先写出被积函数的原函数。

**例 24**　求 $I=\int_0^{\pi/4}\ln(1+\tan x)\,\mathrm{d}x$。

例 23 里翻转后留下的是一个还要另算的积分再减去 $I$，这一题翻转后直接得到常数减去 $I$，同样是把 $I$ 带着负号送回来，只是好算的部分更简单。区间 $[0,\frac\pi4]$ 的 $a+b=\frac\pi4$，翻转 $x\to\frac\pi4-x$。用差角公式，$\tan(\frac\pi4-x)=\frac{1-\tan x}{1+\tan x}$，所以

$$1+\tan\Big(\frac\pi4-x\Big)=\frac{2}{1+\tan x},\qquad I=\int_0^{\pi/4}\big[\ln2-\ln(1+\tan x)\big]\mathrm{d}x=\frac\pi4\ln2-I.$$

解出 $I=\frac\pi8\ln2$。

到这里，被积函数要么有现成的整体，要么区间有对称性。两样都没有的时候，比如 $x\mathrm{e}^x$，就要换一条求导规则倒过来用，这是下一节。

合上书，写出区间再现的公式，说明它为什么成立，并说出例 22 和例 23 各自翻转后出现的是什么。

### 5. 两类不同的函数相乘时，怎样把积分转给另一个因子？

$\int x\mathrm{e}^x\,\mathrm{d}x$ 里，$x$ 和 $\mathrm{e}^x$ 都容易单独积分，乘在一起却没有整体可凑：$x$ 不是 $\mathrm{e}^x$ 的内层，$\mathrm{e}^x$ 也不是 $x$ 的内层。换元法这条路走不通，要换成乘积法则。

$(uv)'=u'v+uv'$ 两边求不定积分，移项得

$$\int u\,\mathrm{d}v=uv-\int v\,\mathrm{d}u .$$

这就是**分部积分公式**。它没有直接算出积分，而是把 $\int u\,\mathrm{d}v$ 换成了 $\int v\,\mathrm{d}u$：对 $\mathrm{d}v$ 的那个因子积分，对 $u$ 的那个因子求导。如果 $u$ 求导后变简单，新积分就比原来容易。

![曲线为 $v=\sqrt u$，从 $A$ 递增到 $B$。浅灰阴影是 $\int_{u_A}^{u_B}v(u)\,\mathrm{d}u$（曲线下方，对 $u$ 积分），斜线阴影是 $\int_{v_A}^{v_B}u(v)\,\mathrm{d}v$（曲线左边，对 $v$ 积分）；两块合起来正好是大矩形面积 $u_Bv_B$ 减去小矩形面积 $u_Av_A$，即 $uv\big|_A^B$](fig/C11-n5.pdf){width=60%}

图上看更清楚：两块面积之和是两个矩形面积之差，已知一块就知道另一块。

这个公式不是「积分也像乘法，各积各的」：$\int x\mathrm{e}^x\,\mathrm{d}x$ 不等于 $\frac{x^2}2\cdot\mathrm{e}^x$，后者求导得 $x\mathrm{e}^x+\frac{x^2}2\mathrm{e}^x$，多出一项。

**选哪个因子求导？** 从 $\int x\mathrm{e}^x\,\mathrm{d}x$ 试起，有两种选法：

- 取 $u=x$，$\mathrm{d}v=\mathrm{e}^x\mathrm{d}x$：$v=\mathrm{e}^x$，$\mathrm{d}u=\mathrm{d}x$，幂次降了一次，新积分 $\int\mathrm{e}^x\mathrm{d}x$ 一步就出来。
- 取 $u=\mathrm{e}^x$，$\mathrm{d}v=x\,\mathrm{d}x$：$v=\frac{x^2}2$，新积分 $\int\frac{x^2}2\mathrm{e}^x\mathrm{d}x$ 的幂次反而升了。

判据有两条：$\mathrm{d}v$ 那一部分要容易积出 $v$；$\int v\,\mathrm{d}u$ 要比 $\int u\,\mathrm{d}v$ 简单。实践中的次序是「反对幂指三」：反三角函数、对数函数、幂函数、指数函数、三角函数，排在前面的优先当 $u$，排在后面的优先放进 $\mathrm{d}v$。理由是：反三角函数和对数的导数是代数式（$\frac1{1+x^2}$、$\frac1x$），求导以后变简单，而它们的原函数反而不好找；幂函数求导降次；指数和三角函数求导、积分都不变复杂，所以放在 $\mathrm{d}v$ 里最安全。

例如 $x^2\ln x$ 里 $\ln x$ 排在前面，取 $u=\ln x$，$\mathrm{d}v=x^2\mathrm{d}x$；$x\sin x$ 里幂排在前面，取 $u=x$，$\mathrm{d}v=\sin x\,\mathrm{d}x$。这是经验次序，不是定理：$\int\frac{\ln x}x\,\mathrm{d}x$ 里 $\frac1x$ 正是 $\ln x$ 的导数，凑微分一步得 $\frac12\ln^2x+C$，分部反而绕远。

**方法 5（分部积分）**

1. 看被积函数是不是两类函数的乘积（幂×指数、幂×三角、幂×对数、指数×三角等）。
2. 按「反对幂指三」选 $u$，其余（连同 $\mathrm{d}x$）作 $\mathrm{d}v$，算出 $v$ 和 $\mathrm{d}u$。
3. 套公式。新积分仍是乘积就再来一次；若原来的积分又出现，就列方程解。

**例 25**　求 $\int x\mathrm{e}^x\,\mathrm{d}x$。

和例 1 相比，指数里从 $x^2$ 换成了 $x$：$x\mathrm{e}^{x^2}$ 有整体可凑，$x\mathrm{e}^x$ 没有，所以改用乘积法则。

按「幂在指数前」取 $u=x$，$\mathrm{d}v=\mathrm{e}^x\mathrm{d}x$，则 $\mathrm{d}u=\mathrm{d}x$，$v=\mathrm{e}^x$：

$$\int x\mathrm{e}^x\,\mathrm{d}x=x\mathrm{e}^x-\int\mathrm{e}^x\,\mathrm{d}x=(x-1)\mathrm{e}^x+C.$$

> 求 $\int x\sin x\,\mathrm{d}x$。
>
> 答案：$u=x$，$\mathrm{d}v=\sin x\,\mathrm{d}x$，$v=-\cos x$，原式 $=-x\cos x+\int\cos x\,\mathrm{d}x=-x\cos x+\sin x+C$。

**例 26**　求 $\int\ln x\,\mathrm{d}x$ 和 $\int\arctan x\,\mathrm{d}x$。

和例 25 的不同在于被积函数只有一个因子，看不出「乘积」。办法是把 $\mathrm{d}x$ 单独当作 $\mathrm{d}v$（相当于乘了一个 1），$v=x$。

$\ln x$ 取 $u=\ln x$，$\mathrm{d}u=\frac{\mathrm{d}x}x$：

$$\int\ln x\,\mathrm{d}x=x\ln x-\int x\cdot\frac1x\,\mathrm{d}x=x\ln x-x+C.$$

老朋友 $\ln x$ 的原函数到这里才有。$\arctan x$ 同样取 $u=\arctan x$，$\mathrm{d}u=\frac{\mathrm{d}x}{1+x^2}$，新积分用凑微分（$x\,\mathrm{d}x=\frac12\mathrm{d}(1+x^2)$）：

$$\int\arctan x\,\mathrm{d}x=x\arctan x-\int\frac{x}{1+x^2}\mathrm{d}x=x\arctan x-\frac12\ln(1+x^2)+C.$$

**例 27**　求 $\int x^2\mathrm{e}^x\,\mathrm{d}x$。

比例 25 多一次幂。取 $u=x^2$，$v=\mathrm{e}^x$，一次分部后幂降到 1，剩下的就是例 25：

$$\int x^2\mathrm{e}^x\,\mathrm{d}x=x^2\mathrm{e}^x-2\int x\mathrm{e}^x\,\mathrm{d}x=x^2\mathrm{e}^x-2(x-1)\mathrm{e}^x+C=(x^2-2x+2)\mathrm{e}^x+C.$$

多项式 $x^n$ 乘指数或三角函数，就要连做 $n$ 次，每次降一次幂。这时可以列表：

| | 求导（左列） | 积分（右列） |
|---|---|---|
| 第 0 行 | $x^2$ | $\mathrm{e}^x$ |
| 第 1 行 | $2x$ | $\mathrm{e}^x$ |
| 第 2 行 | $2$ | $\mathrm{e}^x$ |

左列第 $k$ 行乘右列第 $k$ 行（逐行相乘），符号交替 $+,-,+$：$x^2\mathrm{e}^x-2x\mathrm{e}^x+2\mathrm{e}^x$。表格只是上面反复套公式的缩写。

**例 28**　求 $I=\int\mathrm{e}^x\sin x\,\mathrm{d}x$。

和例 25 到例 27 相比，这里的两个因子求导、积分都不变简单，不会越做越简单，而是转回来。

指数和三角函数哪个当 $u$ 都行，但必须前后保持一致。取 $u=\sin x$，$v=\mathrm{e}^x$：

$$I=\mathrm{e}^x\sin x-\int\mathrm{e}^x\cos x\,\mathrm{d}x.$$

再对新积分分部一次，仍取三角函数当 $u$（$u=\cos x$）：

$$\int\mathrm{e}^x\cos x\,\mathrm{d}x=\mathrm{e}^x\cos x+\int\mathrm{e}^x\sin x\,\mathrm{d}x=\mathrm{e}^x\cos x+I.$$

代回：$I=\mathrm{e}^x\sin x-\mathrm{e}^x\cos x-I$，$I$ 带着负号回来了。移项，

$$I=\frac{\mathrm{e}^x(\sin x-\cos x)}2+C.$$

如果第二次改取 $u=\mathrm{e}^x$，则 $\int\mathrm{e}^x\cos x\,\mathrm{d}x=\mathrm{e}^x\sin x-\int\mathrm{e}^x\sin x\,\mathrm{d}x=\mathrm{e}^x\sin x-I$，代回 $I=\mathrm{e}^x\sin x-\big(\mathrm{e}^x\sin x-I\big)=I$，会把第一次的结果原样倒回来，什么也没得到。所以循环型要「同类函数两次当同一个角色」。这和 C.11.4 区间再现里「翻转一次，把 $I$ 带着负号送回来」是同一个想法：积分算不出来时，设法让它在等式两边各出现一次。

**例 29**　求 $\int\mathrm{e}^{\sqrt x}\,\mathrm{d}x$。

和前面每道例题相比，这一题要把两种方法接起来：换元与分部接力。

整体 $\sqrt x$ 在指数里，但 $\mathrm{d}x$ 里没有对应的导数 $\frac1{2\sqrt x}$。先用第二类换元去掉根号：$t=\sqrt x$，$x=t^2$，$\mathrm{d}x=2t\,\mathrm{d}t$：

$$\int\mathrm{e}^{\sqrt x}\,\mathrm{d}x=2\int t\mathrm{e}^t\,\mathrm{d}t=2(t-1)\mathrm{e}^t+C=2(\sqrt x-1)\mathrm{e}^{\sqrt x}+C.$$

中间一步是例 25。先换元，再分部，两种方法接力。

**例 30**　已知 $f(x)$ 的一个原函数是 $\dfrac{\sin x}x$，求 $\int x\,f'(x)\,\mathrm{d}x$。

和前面不同，这里的函数 $f$ 没有给出，给的是它的原函数。

取 $u=x$，$\mathrm{d}v=f'(x)\,\mathrm{d}x$，则 $v=f(x)$：

$$\int xf'(x)\,\mathrm{d}x=xf(x)-\int f(x)\,\mathrm{d}x.$$

第二项就是 $f$ 的原函数，已知是 $\frac{\sin x}x$（加常数）。第一项要 $f$ 本身：对原函数求导，$f(x)=\Big(\frac{\sin x}x\Big)'=\frac{x\cos x-\sin x}{x^2}$，所以 $xf(x)=\cos x-\frac{\sin x}x$。

$$\int xf'(x)\,\mathrm{d}x=\cos x-\frac{2\sin x}x+C.$$

三类外观相近的积分放在一起：$\int x\mathrm{e}^{x^2}\mathrm{d}x$ 有整体 $x^2$，凑微分，一行；$\int x\mathrm{e}^x\,\mathrm{d}x$ 没有整体，分部；$\int\mathrm{e}^{x^2}\mathrm{d}x$ 两种方法都不行（见第 9 节）。区别全在「指数里的东西对应的导数在不在被积式里」。

分部积分在不定积分里遇到 $\sin^nx$ 这样的幂，要一次次降次。到了定积分里，边界项 $[uv]_a^b$ 是具体的数，常常为零，这会不会让某些积分有现成的递推？这是下一节的问题。

合上书，写出分部积分公式并说出它由哪条求导法则得到，再说明为什么 $\int\ln x\,\mathrm{d}x$ 要把 $\mathrm{d}x$ 当成 $\mathrm{d}v$。

### 6. 定积分的分部积分能带来什么新东西？

不定积分的分部积分（第 5 节）配上牛顿–莱布尼茨公式，就是定积分的分部积分（$u$、$v$ 在 $[a,b]$ 上有连续导数）：

$$\int_a^bu\,\mathrm{d}v=\big[uv\big]_a^b-\int_a^bv\,\mathrm{d}u .$$

它来自 $(uv)'=u'v+uv'$ 两边从 $a$ 积到 $b$，左边由牛顿–莱布尼茨公式得 $[uv]_a^b$。与不定积分的不同在中间那一项：它是一个具体的数，常常是 0。

**例 31**　求 $\int_0^1\arctan x\,\mathrm{d}x$。

这是例 26 的定积分版。由例 26，原函数是 $x\arctan x-\frac12\ln(1+x^2)$，代入上下限：

$$\int_0^1\arctan x\,\mathrm{d}x=\Big[x\arctan x-\frac12\ln(1+x^2)\Big]_0^1=\frac\pi4-\frac12\ln2.$$

下限 $x=0$ 处两项都是 0；这就是边界项常常很简单的原因。

接下来看这一节真正新的东西。记 $I_n=\int_0^{\pi/2}\sin^nx\,\mathrm{d}x$（$n=0,1,2,\dots$），先算前几个：$I_0=\frac\pi2$，$I_1=[-\cos x]_0^{\pi/2}=1$，$I_2$ 用 $\sin^2x=\frac{1-\cos2x}2$ 降次得 $\frac\pi4$。到了 $I_5$、$I_6$，反复降次很繁，改找 $I_n$ 与 $I_{n-2}$ 的关系。

先拿 $I_3$ 试：取 $u=\sin^2x$，$\mathrm{d}v=\sin x\,\mathrm{d}x$，则 $\mathrm{d}u=2\sin x\cos x\,\mathrm{d}x$，$v=-\cos x$，

$$I_3=\big[-\sin^2x\cos x\big]_0^{\pi/2}+2\int_0^{\pi/2}\sin x\cos^2x\,\mathrm{d}x=0+2\int_0^{\pi/2}\sin x(1-\sin^2x)\,\mathrm{d}x=2(I_1-I_3),$$

移项得 $3I_3=2I_1$，$I_3=\frac23$。$I_3$ 被 $I_1$ 表示出来了，一般的 $n$ 照样做：拆出一个 $\sin x$ 当作 $\mathrm{d}v$，其余部分求导，幂次就降下来。设 $n\ge2$，取 $u=\sin^{n-1}x$，$\mathrm{d}v=\sin x\,\mathrm{d}x$，则 $\mathrm{d}u=(n-1)\sin^{n-2}x\cos x\,\mathrm{d}x$，$v=-\cos x$：

$$I_n=\big[-\sin^{n-1}x\cos x\big]_0^{\pi/2}+(n-1)\int_0^{\pi/2}\sin^{n-2}x\cos^2x\,\mathrm{d}x .$$

边界项是 0：$x=\frac\pi2$ 时 $\cos x=0$，$x=0$ 时 $\sin^{n-1}x=0$（$n-1\ge1$）。这正是取区间 $[0,\frac\pi2]$ 的好处，两个端点各让一个因子为零。为了回到 $\sin$ 的幂，把 $\cos^2x$ 换成 $1-\sin^2x$，积分拆成两个：

$$\int_0^{\pi/2}\sin^{n-2}x\cos^2x\,\mathrm{d}x=\int_0^{\pi/2}\sin^{n-2}x(1-\sin^2x)\,\mathrm{d}x=I_{n-2}-I_n ,$$

代回 $I_n$ 的式子：

$$I_n=(n-1)I_{n-2}-(n-1)I_n .$$

$I_n$ 带着系数 $-(n-1)$ 回到了右边。不必再积分，移项得 $nI_n=(n-1)I_{n-2}$，即

$$I_n=\frac{n-1}{n}\,I_{n-2}\qquad(n\ge2).$$

对正整数 $n$ 反复使用，每次下标降 2，最后落到 $I_0=\frac\pi2$ 或 $I_1=1$。例如 $n=6$：$I_6=\frac56I_4=\frac56\cdot\frac34I_2=\frac56\cdot\frac34\cdot\frac12I_0=\frac56\cdot\frac34\cdot\frac12\cdot\frac\pi2$；$n=5$：$I_5=\frac45I_3=\frac45\cdot\frac23I_1=\frac45\cdot\frac23\cdot1$。每一步分子分母各减 2。记 $n!!$ 为从 $n$ 开始隔一个数乘一个、乘到 1 或 2 为止，读作「$n$ 的双阶乘」，例如 $7!!=7\cdot5\cdot3\cdot1$，$6!!=6\cdot4\cdot2$，并约定 $0!!=1$。于是对正整数 $n$ 得到**华里士公式**（$n=0$ 时单独取 $I_0=\frac\pi2$）

$$\int_0^{\pi/2}\sin^nx\,\mathrm{d}x=\begin{cases}\dfrac{(n-1)!!}{n!!}\cdot\dfrac\pi2, & n\ \text{为偶数},\\[2mm]\dfrac{(n-1)!!}{n!!}, & n\ \text{为奇数}.\end{cases}$$

偶数次多一个 $\frac\pi2$，因为最后落在 $I_0$。$\cos^nx$ 的积分值相同：令 $x=\frac\pi2-t$，$\sin x$ 变成 $\cos t$，上下限 $0$ 与 $\frac\pi2$ 对调，$\mathrm{d}x=-\mathrm{d}t$ 的负号再把它们换回来。

**方法 6（华里士公式）**

1. 识别区间和次数：$n$ 为正整数，积分是 $\int_0^{\pi/2}\sin^nx\,\mathrm{d}x$ 或 $\int_0^{\pi/2}\cos^nx\,\mathrm{d}x$。区间不是 $[0,\frac\pi2]$ 时，先用 C.11.4 的对称性折回来：$[0,\pi]$ 上的 $\sin^n$ 是 $[0,\frac\pi2]$ 上的 2 倍；$[0,2\pi]$ 上的 $\sin^n$，$n$ 为偶数时是 4 倍，$n$ 为奇数时为 0。
2. 递推降 2：从 $\frac{n-1}{n}$ 起，分子分母各减 2 一直乘下去。
3. 看落点：$n$ 为奇数，乘到 $\frac23$ 为止（落在 $I_1=1$）；$n$ 为偶数，乘到 $\frac12$ 为止，再乘 $\frac\pi2$（落在 $I_0$）。

**例 32**　求 $\int_0^{\pi/2}\sin^5x\,\mathrm{d}x$ 和 $\int_0^{\pi/2}\cos^6x\,\mathrm{d}x$。

先直接套公式，奇数次和偶数次各一道，对照上面 $n=5$、$n=6$ 的降 2 链。

5 是奇数，从 $\frac45$ 乘到 $\frac23$ 为止，落在 $I_1=1$：

$$\int_0^{\pi/2}\sin^5x\,\mathrm{d}x=\frac45\cdot\frac23=\frac8{15}.$$

6 是偶数，从 $\frac56$ 乘到 $\frac12$，再乘 $\frac\pi2$：

$$\int_0^{\pi/2}\cos^6x\,\mathrm{d}x=\frac56\cdot\frac34\cdot\frac12\cdot\frac\pi2=\frac{5\pi}{32}.$$

> 求 $\int_0^{\pi/2}\cos^7x\,\mathrm{d}x$ 和 $\int_0^{\pi/2}\sin^4x\,\mathrm{d}x$。
>
> 答案：$\frac67\cdot\frac45\cdot\frac23=\frac{16}{35}$；$\frac34\cdot\frac12\cdot\frac\pi2=\frac{3\pi}{16}$。

**例 33**　求 $\int_0^1x^4\sqrt{1-x^2}\,\mathrm{d}x$。

和例 32 相比，被积函数里没有三角函数，要先换元，把它变成华里士公式能管的样子。根号 $\sqrt{1-x^2}$ 用 $x=\sin t$（C.11.3），限 $0\to0$、$1\to\frac\pi2$，$\mathrm{d}x=\cos t\,\mathrm{d}t$：

$$\int_0^{\pi/2}\sin^4t\cos^2t\,\mathrm{d}t=\int_0^{\pi/2}\sin^4t\,(1-\sin^2t)\,\mathrm{d}t=I_4-I_6.$$

由华里士公式 $I_4=\frac{3\pi}{16}$，$I_6=\frac{5\pi}{32}$，所以结果是 $\frac{3\pi}{16}-\frac{5\pi}{32}=\frac\pi{32}$。

同样的换元把 $\int_0^1x^3\sqrt{1-x^2}\,\mathrm{d}x$ 变成 $I_3-I_5=\frac23-\frac8{15}=\frac2{15}$。对 $x^m\sqrt{1-x^2}$ 这一族，$m$ 是偶数时结果里有 $\pi$，$m$ 是奇数时没有。

分部、换元、对称性和华里士公式用的都是「复合」或「乘积」的结构。还有一大类积分两样都没有，比如 $\frac1{x(x+1)(x+2)}$，它既没有现成的整体可凑，也不是两类函数相乘；这就是下一节的有理函数。

合上书，推导 $I_n=\frac{n-1}{n}I_{n-2}$，说清边界项为什么是 0，$I_n$ 又是怎样回到右边的。

### 7. 分式函数的积分，有没有一套固定的程序？

前面的方法要靠观察。先看一个最小的情形：$\frac1{x(x+1)}=\frac1x-\frac1{x+1}$（右边通分就是左边），于是 $\int\frac{\mathrm{d}x}{x(x+1)}=\ln\Big|\frac x{x+1}\Big|+C$。分母里两个因式的分式，拆成两个各含一个因式的分式，每个都会积。这个拆法对一般的有理函数 $\dfrac{P(x)}{Q(x)}$（两个多项式之比）也行，并且有一套固定程序，只需要机械地做下去。

先看两个最简单的：

$$\int\frac{\mathrm{d}x}{(x-a)^k}=\begin{cases}\ln|x-a|+C,&k=1,\\[1mm]\dfrac{(x-a)^{1-k}}{1-k}+C,&k\ge2.\end{cases}$$

任何有理函数都可以写成一个多项式与若干简单分式的和。简单分式的分母可以是一次因式的幂，也可以是不能继续分解为实一次因式的二次因式的幂，下面分别说明这两类。这就是**部分分式分解**。

**第一步：假分式先做除法。** $P$ 的次数不低于 $Q$ 时，用多项式带余除法把它写成「多项式 + 真分式」，真分式指分子次数低于分母。多项式部分直接积分。

**第二步：分母分解。** 实系数多项式 $Q$ 总可以分解成实一次因式 $(x-a)^k$ 和不可约二次因式 $(x^2+px+q)^k$ 的乘积（这是代数基本定理的推论），同一个因式可能重复出现。「不可约二次因式」指 $x^2+px+q$ 满足 $p^2-4q<0$，也就是它没有实根。具体怎么分解，次数不高时靠观察和试根（代入使多项式为 0 的 $x$，找出一次因式），本章的例题分母都已是易分解的形式；一般的四次以上多项式手工分解很难，那是软件做的事。例如 $x^4+1$ 没有实根，也仍然能拆成两个二次式：$x^4+1=(x^2+\sqrt2x+1)(x^2-\sqrt2x+1)$，两个因子的判别式都是 $2-4<0$。

**第三步：写出分解形式。** 每个因式对应一组分式：

- $(x-a)^k$ 对应 $\dfrac{A_1}{x-a}+\dfrac{A_2}{(x-a)^2}+\cdots+\dfrac{A_k}{(x-a)^k}$；
- $(x^2+px+q)^k$ 对应 $\dfrac{B_1x+C_1}{x^2+px+q}+\cdots+\dfrac{B_kx+C_k}{(x^2+px+q)^k}$。

二次因式的分子要写成一次式 $Bx+C$：分母是二次的，真分式的分子可以是一次的。

**第四步：求系数。** 两边通分，比较系数；或者代几个方便的 $x$ 值。单根 $a$ 对应的系数有捷径，叫遮盖法：把分母里的 $(x-a)$ 遮住，把 $x=a$ 代进剩下的部分。它成立的原因是：两边乘 $(x-a)$，再令 $x=a$，其余含 $(x-a)$ 的项都变成 0，只剩下这个单根对应的系数。

**第五步：逐项积分。** 一次因式的项如上；二次因式的项 $\int\frac{Bx+C}{x^2+px+q}\mathrm{d}x$，先把分子拆成分母导数 $2x+p$ 的倍数加常数：

$$Bx+C=\frac B2(2x+p)+\Big(C-\frac{Bp}2\Big),$$

前一部分凑微分得 $\frac B2\ln(x^2+px+q)$，后一部分配方后用例 4 的 $\arctan$ 公式。

**方法 7（部分分式）**

1. 假分式先做除法，写成多项式加真分式。
2. 把分母分解成一次因式与不可约二次因式。
3. 按因式写出分解形式（重因式写全部低次项）。
4. 求系数：比较系数、代值或遮盖法。
5. 逐项积分。

**例 34**　求 $\int\frac{\mathrm{d}x}{x(x+1)(x+2)}$。

它是本节开头那个小情形的加长版：分母是三个互不相同的一次因式。设

$$\frac1{x(x+1)(x+2)}=\frac Ax+\frac B{x+1}+\frac C{x+2}.$$

用遮盖法：求 $A$，遮住 $x$，把 $x=0$ 代进 $\frac1{(x+1)(x+2)}$，$A=\frac12$；求 $B$，$x=-1$ 代进 $\frac1{x(x+2)}$，$B=-1$；求 $C$，$x=-2$ 代进 $\frac1{x(x+1)}$，$C=\frac12$。于是

$$\int\frac{\mathrm{d}x}{x(x+1)(x+2)}=\frac12\ln|x|-\ln|x+1|+\frac12\ln|x+2|+C.$$

> 求 $\int\frac{\mathrm{d}x}{x^2-1}$。
>
> 答案：$\frac1{x^2-1}=\frac12\Big(\frac1{x-1}-\frac1{x+1}\Big)$，原式 $=\frac12\ln\Big|\frac{x-1}{x+1}\Big|+C$。

**例 35**　求 $\int\frac{x^3+2x+1}{x^2+x-2}\mathrm{d}x$。

和例 34 相比，分子次数（3）高于分母（2），是假分式，先做除法：$x^3+2x+1=(x-1)(x^2+x-2)+5x-1$，所以

$$\frac{x^3+2x+1}{x^2+x-2}=x-1+\frac{5x-1}{(x-1)(x+2)}=x-1+\frac{4/3}{x-1}+\frac{11/3}{x+2}.$$

后一步的系数用遮盖法：$x=1$ 时 $\frac{5x-1}{x+2}=\frac43$；$x=-2$ 时 $\frac{5x-1}{x-1}=\frac{-11}{-3}=\frac{11}3$。积分：

$$\int\cdots=\frac{x^2}2-x+\frac43\ln|x-1|+\frac{11}3\ln|x+2|+C.$$

**例 36**　求 $\int\frac{\mathrm{d}x}{x(x-1)^2}$。

和例 34 相比，分母里有重因式，分解里每个因式要写出全部低次项。

分母有重根 $(x-1)^2$，分解里要写出一次和二次两项：

$$\frac1{x(x-1)^2}=\frac Ax+\frac B{x-1}+\frac C{(x-1)^2}.$$

遮盖法对最高次项有效：$A$（遮住 $x$，$x=0$ 代入）$=1$；$C$（遮住 $(x-1)^2$，$x=1$ 代入 $\frac1x$）$=1$。$B$ 遮盖不出，用比较系数：通分后分子 $A(x-1)^2+Bx(x-1)+Cx=1$，比较 $x^2$ 的系数，$A+B=0$，$B=-1$。

$$\int\frac{\mathrm{d}x}{x(x-1)^2}=\ln|x|-\ln|x-1|-\frac1{x-1}+C.$$

**例 37**　求 $\int\frac{\mathrm{d}x}{(x-1)(x^2+1)}$ 和 $\int\frac{2x+3}{x^2+2x+5}\mathrm{d}x$。

和例 36 相比，分母里出现了不可约的二次因式，对应的分子是一次式。

第一个含不可约二次因式 $x^2+1$，设

$$\frac1{(x-1)(x^2+1)}=\frac A{x-1}+\frac{Bx+C}{x^2+1},$$

遮盖法给 $A=\frac12$。通分比较：$1=A(x^2+1)+(Bx+C)(x-1)$，$x^2$ 的系数 $A+B=0$，$B=-\frac12$；常数项 $A-C=1$，$C=-\frac12$。积分时把 $-\frac12\cdot\frac{x+1}{x^2+1}$ 拆成 $-\frac12\cdot\frac{x}{x^2+1}$ 与 $-\frac12\cdot\frac1{x^2+1}$，前者凑微分 $x\,\mathrm{d}x=\frac12\mathrm{d}(x^2+1)$，后者是 $\arctan$：

$$\int\frac{\mathrm{d}x}{(x-1)(x^2+1)}=\frac12\ln|x-1|-\frac14\ln(x^2+1)-\frac12\arctan x+C.$$

第二个只有一个二次因式，不用分解，直接按第五步拆分子：$2x+3=(2x+2)+1$。前一部分凑微分，后一部分配方 $x^2+2x+5=(x+1)^2+4$ 用例 4：

$$\int\frac{2x+3}{x^2+2x+5}\mathrm{d}x=\ln(x^2+2x+5)+\frac12\arctan\frac{x+1}2+C.$$

#### 不可约二次因式重复出现时怎么办？

分母里不可约二次因式出现 $k\ge2$ 次时，要积 $\int\frac{\mathrm{d}x}{(x^2+px+q)^k}$ 这类式子。先配方 $x^2+px+q=\big(x+\frac p2\big)^2+d^2$，其中 $d=\sqrt{q-p^2/4}>0$，令 $y=\frac{x+p/2}{d}$，就回到常数倍的 $\int\frac{\mathrm{d}y}{(1+y^2)^k}$。下面求它的递推，用第 5 节的分部积分。设 $K_n=\int\frac{\mathrm{d}x}{(1+x^2)^n}$，取 $u=\frac1{(1+x^2)^n}$，$\mathrm{d}v=\mathrm{d}x$：

$$K_n=\frac x{(1+x^2)^n}+2n\int\frac{x^2}{(1+x^2)^{n+1}}\mathrm{d}x=\frac x{(1+x^2)^n}+2n(K_n-K_{n+1}),$$

最后一步把 $x^2=(1+x^2)-1$ 拆开：

$$\int\frac{x^2}{(1+x^2)^{n+1}}\mathrm{d}x=\int\frac{(1+x^2)-1}{(1+x^2)^{n+1}}\mathrm{d}x=K_n-K_{n+1}.$$

移项解出 $K_{n+1}$：

$$K_{n+1}=\frac{2n-1}{2n}K_n+\frac x{2n(1+x^2)^n}.$$

$n=1$ 时得 $\int\frac{\mathrm{d}x}{(1+x^2)^2}=\frac x{2(1+x^2)}+\frac12\arctan x+C$。

**例 38**　求 $\int_0^1\frac{\mathrm{d}x}{(x+1)(x^2+1)}$。

和例 37 相比，只是换成定积分，分解的办法不变。

设 $\frac1{(x+1)(x^2+1)}=\frac A{x+1}+\frac{Bx+C}{x^2+1}$，$A=\frac12$（遮住 $x+1$，$x=-1$ 代入 $\frac1{x^2+1}$），比较 $x^2$ 系数 $B=-\frac12$，常数项 $A+C=1$，$C=\frac12$：

$$\int_0^1\Big[\frac{1/2}{x+1}+\frac{-x+1}{2(x^2+1)}\Big]\mathrm{d}x=\frac12\ln2-\frac14\ln2+\frac12\cdot\frac\pi4=\frac{\ln2}4+\frac\pi8.$$

中间一步：$\int_0^1\frac{-x}{x^2+1}\mathrm{d}x=-\frac12\ln2$，$\int_0^1\frac{1}{x^2+1}\mathrm{d}x=\frac\pi4$，各乘 $\frac12$。

部分分式只管 $x$ 的多项式之比。$\frac1{1+\sin x+\cos x}$ 这样由三角函数拼成的分式不是有理函数，能不能换一个变量把它变成有理函数，再交给这套程序？这是下一节的问题。

合上书，写出有理函数积分的五步程序，并说出重根和不可约二次因式各对应怎样的分解形式。

### 8. 三角函数的分式和简单根式，怎样化成有理函数来积？

碰到由 $\sin x$、$\cos x$ 拼成的分式，自然的想法是换一个变量，把它变成新变量的有理函数，再用第 7 节的程序。

以 $\int\frac{\mathrm{d}x}{1+\sin x+\cos x}$ 为例。令 $u=\sin x$ 不行，$\cos x=\pm\sqrt{1-u^2}$ 带着根号；令 $u=\cos x$ 也一样。需要一个变量，让 $\sin x$、$\cos x$ 和 $\mathrm{d}x$ 都是它的有理式。

令 $t=\tan\frac x2$（$-\pi<x<\pi$）。用二倍角公式，并把分母的 1 写成 $\cos^2\frac x2+\sin^2\frac x2$，分子分母同除以 $\cos^2\frac x2$：

$$\sin x=\frac{2\sin\frac x2\cos\frac x2}{\cos^2\frac x2+\sin^2\frac x2}=\frac{2t}{1+t^2},\qquad \cos x=\frac{\cos^2\frac x2-\sin^2\frac x2}{\cos^2\frac x2+\sin^2\frac x2}=\frac{1-t^2}{1+t^2}.$$

由 $x=2\arctan t$ 得 $\mathrm{d}x=\frac{2}{1+t^2}\mathrm{d}t$。三样都是 $t$ 的有理式。校验：$t=1$ 即 $x=\frac\pi2$，公式给出 $\sin x=\frac22=1$，$\cos x=0$。

为什么偏偏是半角？先在图中的上半圆 $0<x<\pi$ 看它的几何来源：单位圆上取 $A(-1,0)$、$B(1,0)$ 和 $P(\cos x,\sin x)$，$\angle BOP=x$。三角形 $AOP$ 中 $OA=OP=1$，两个底角相等，而外角 $\angle BOP$ 等于这两个底角之和，所以 $\angle OAP=\frac x2$，它正是直线 $AP$ 与 $x$ 轴的夹角，斜率是 $\tan\frac x2=t$。反过来，过 $A$、斜率为 $t$ 的直线与圆的另一个交点，解一个二次方程就得到上面两个分式。其他允许的 $x$ 仍由前面的三角恒等式得到这两个分式。

![图示 $0<x<\pi$：$OA=OP$，所以 $\angle OAP=\frac12\angle BOP=\frac x2$；过 $A(-1,0)$、斜率 $t=\tan\frac x2$ 的直线与单位圆的另一个交点是 $\big(\frac{1-t^2}{1+t^2},\frac{2t}{1+t^2}\big)$，所以 $\cos x$、$\sin x$ 都是 $t$ 的有理式](fig/C11-n6.pdf){width=55%}

**方法 8（化为有理函数）**

1. 被积函数由 $\sin x$、$\cos x$ 和常数经四则运算组成：先看 $u=\sin x$、$\cos x$ 或 $\tan x$ 能不能用（见例 39 后的对比），都不行再令 $t=\tan\frac x2$，用上面三个公式化成 $t$ 的有理函数，再用部分分式积分。
2. 被积函数含 $\sqrt[n]{ax+b}$：令整个根式为 $t$。若几个根式都是同一个整体 $ax+b$ 的不同次根，令 $t=(ax+b)^{1/k}$，$k$ 取这些根指数的最小公倍数，并按原函数的定义域选择代换的范围。
3. 被积函数是 $\mathrm{e}^x$ 的有理式：令 $t=\mathrm{e}^x$，$\mathrm{d}x=\frac{\mathrm{d}t}t$。
4. 定积分同时换上下限。$\tan\frac x2$ 在 $x=(2k+1)\pi$（$k$ 为整数）处没有定义；积分区间跨过这些点时，须分段或另选代换，不能把整段直接一次换过去。

**例 39**　求 $\int_0^{\pi/2}\frac{\mathrm{d}x}{1+\sin x+\cos x}$。

和例 3 相比，那里 $\mathrm{d}x$ 配合分母凑出 $\arctan$，这里分母是 $\sin x$ 与 $\cos x$ 的和，没有整体可凑。

上下限跟着换：$x=0$ 时 $t=0$，$x=\frac\pi2$ 时 $t=\tan\frac\pi4=1$。先把分母通分：

$$1+\frac{2t}{1+t^2}+\frac{1-t^2}{1+t^2}=\frac{1+t^2+2t+1-t^2}{1+t^2}=\frac{2(1+t)}{1+t^2}.$$

被积式变成 $\frac{1+t^2}{2(1+t)}\cdot\frac{2\,\mathrm{d}t}{1+t^2}=\frac{\mathrm{d}t}{1+t}$，$1+t^2$ 恰好约掉，所以

$$\int_0^{\pi/2}\frac{\mathrm{d}x}{1+\sin x+\cos x}=\int_0^1\frac{\mathrm{d}t}{1+t}=\ln2.$$

> 求 $\int_0^{\pi/2}\frac{\mathrm{d}x}{2+\cos x}$。
>
> 答案：$2+\cos x=\frac{3+t^2}{1+t^2}$，被积式化为 $\frac{2\,\mathrm{d}t}{3+t^2}$，原式 $=\frac2{\sqrt3}\arctan\frac t{\sqrt3}\Big|_0^1=\frac{\sqrt3\,\pi}9$。

#### 万能代换一定最省事吗？

万能代换在区间不跨过 $x=(2k+1)\pi$ 时总能化成有理函数，但不一定省事。比较 $\int\frac{\mathrm{d}x}{1+\sin^2x}$ 的两种做法。

用 $t=\tan\frac x2$：分母成了 $t$ 的四次多项式，

$$\int\frac{\mathrm{d}x}{1+\sin^2x}=\int\frac{2(1+t^2)}{t^4+6t^2+1}\,\mathrm{d}t .$$

改用 $u=\tan x$：因为 $\sin^2x=\frac{\tan^2x}{1+\tan^2x}=\frac{u^2}{1+u^2}$，$\mathrm{d}x=\frac{\mathrm{d}u}{1+u^2}$，积分变成

$$\int\frac{\mathrm{d}u}{1+2u^2}=\frac1{\sqrt2}\arctan(\sqrt2\tan x)+C .$$

差别在于：只出现 $\sin^2x$、$\cos^2x$、$\sin x\cos x$ 时，它们已经是 $\tan x$ 的有理式，不必取半角，次数也低一半。

用 $u=\tan x$ 时，积分区间不能跨过 $\frac\pi2+k\pi$，跨过就分段。

**例 40**　求 $\int\frac{\mathrm{d}x}{\sqrt x+\sqrt[3]x}$。

和例 39 相比，被积函数里是根式而不是三角函数，想法相同：换变量，把它变成有理函数。

两个根指数是 2 和 3，最小公倍数是 6，令 $t=x^{1/6}$，两个根式都成了整数次幂：$x=t^6$，$\mathrm{d}x=6t^5\mathrm{d}t$，$\sqrt x=t^3$，$\sqrt[3]x=t^2$。

$$\int\frac{6t^5}{t^3+t^2}\mathrm{d}t=\int\frac{6t^3}{t+1}\mathrm{d}t .$$

这是假分式，先做除法：$t^3=(t+1)(t^2-t+1)-1$，所以被积式是 $6\big(t^2-t+1-\frac1{t+1}\big)$。积分得 $2t^3-3t^2+6t-6\ln(1+t)+C$（$t>0$），回代 $t=x^{1/6}$：

$$\int\frac{\mathrm{d}x}{\sqrt x+\sqrt[3]x}=2\sqrt x-3\sqrt[3]x+6\sqrt[6]x-6\ln\big(1+\sqrt[6]x\big)+C .$$

**例 41**　求 $\int\frac{\mathrm{d}x}{\mathrm{e}^x+1}$。

和例 40 相比，换元的对象是 $\mathrm{e}^x$，换完以后仍是有理函数。

被积函数是 $\mathrm{e}^x$ 的有理式，令 $t=\mathrm{e}^x$，$x=\ln t$，$\mathrm{d}x=\frac{\mathrm{d}t}t$：

$$\int\frac{\mathrm{d}t}{t(t+1)}=\int\Big(\frac1t-\frac1{t+1}\Big)\mathrm{d}t=\ln\frac t{t+1}+C=x-\ln(\mathrm{e}^x+1)+C.$$

中间一步是第 7 节的遮盖法。

到这里，换元、分部、部分分式、万能代换都有了。面对一个具体的积分该先试哪一个？还有，只要方法用对，是不是每个积分都能求出来？这是下一节的问题。

合上书，推出 $\sin x$、$\cos x$、$\mathrm{d}x$ 用 $t=\tan\frac x2$ 表示的三个公式，再说出什么时候改用 $u=\tan x$。

### 9. 拿到一个积分先试哪种方法？哪些积分根本写不成初等函数？

先看几个外观相近的积分：$\int x\mathrm{e}^{x^2}\mathrm{d}x$ 凑微分，$\int x\mathrm{e}^x\mathrm{d}x$ 分部（第 5 节末），而 $\int x^3\mathrm{e}^{x^2}\mathrm{d}x$ 既有 $x^2$ 又有高次幂，该选哪个？这一节不讲新技巧，讲已有技巧的试用顺序；最后回答另一个问题：有没有积分，怎么试都不行？

**方法 9（选积分方法的顺序）**　从省事的往费事的试：

1. 先变形（拆项、约分、三角恒等式），看能否直接查基本积分表；
2. 找「复合函数乘内层的导数」，能凑微分就凑（第 1 节）；
3. 有去不掉的根号，用三角代换或根式代换（第 2 节）；
4. 两类不同的函数相乘，如多项式乘指数、对数或三角函数，用分部积分（第 5 节）；
5. 有理函数用部分分式（第 7 节）；三角函数的有理式，别的办法都不行时才用万能代换（第 8 节），分段后它一定能做，但最费事。

**例 42**　求 $\int x^3\mathrm{e}^{x^2}\,\mathrm{d}x$。

它和例 1 的 $x\mathrm{e}^{x^2}$、例 25 的 $x\mathrm{e}^x$ 外观都相近，只是 $x$ 的次数变成了 3，要先判断是该分部还是该凑微分。

多项式乘指数，像是第 4 步的分部积分。但若照「幂在指数前」取 $u=x^3$，$\mathrm{d}v=\mathrm{e}^{x^2}\mathrm{d}x$，就得先积出 $\mathrm{e}^{x^2}$，而它的原函数写不成初等函数（本节后面解释），这样拆不行。办法是留一个 $x$ 给指数，所以先走第 2 步：$x^3\,\mathrm{d}x=\frac12x^2\cdot2x\,\mathrm{d}x=\frac12x^2\,\mathrm{d}(x^2)$，令 $u=x^2$，之后才是分部积分：

$$\int x^3\mathrm{e}^{x^2}\,\mathrm{d}x=\frac12\int u\,\mathrm{e}^u\,\mathrm{d}u=\frac12(u-1)\mathrm{e}^u+C=\frac12(x^2-1)\mathrm{e}^{x^2}+C .$$

> 求 $\int x^5\mathrm{e}^{x^3}\,\mathrm{d}x$。
>
> 答案：$x^5\,\mathrm{d}x=\frac13x^3\,\mathrm{d}(x^3)$，令 $u=x^3$，原式 $=\frac13\int u\mathrm{e}^u\,\mathrm{d}u=\frac13(x^3-1)\mathrm{e}^{x^3}+C$。

软件会帮我们做这件事。用 SymPy，一行命令就能验算例 42：

```python
from sympy import symbols, exp, sin, integrate
x = symbols('x')
integrate(x**3 * exp(x**2), x)   # (x**2 - 1)*exp(x**2)/2
```

软件的输出和手算只差一个常数项，因为它省略了 $+C$。查积分表是同样的用法：表里列的是常见形式的结果，要先把手里的积分变形成表里的样子。手算的价值在于：知道该写什么命令，也看得懂输出和自己的结果是不是一回事。

#### 哪些积分根本写不成初等函数？

有些连续函数有原函数，却没有初等原函数。$\mathrm{e}^{\pm x^2}$、$\frac{\sin x}{x}$、$\frac{1}{\ln x}$ 在各自不含奇点的区间上连续，由原函数存在定理（C.10.3），原函数确实存在。但它们的原函数不能由基本初等函数经有限次四则运算和复合写出，称为**没有初等原函数**。把同样的积分交给软件：

```python
integrate(exp(-x**2), x)         # sqrt(pi)*erf(x)/2
integrate(sin(x)/x, x)           # Si(x)
```

$\operatorname{erf}(x)$（误差函数）和 $\operatorname{Si}(x)$（正弦积分）只是给这两个积分起的新名字，并没有把它们写成初等函数。

没有初等原函数的函数常常藏在变限积分里，办法是用分部积分让它去求导。

**例 43**　设 $F(x)=\int_x^1\mathrm{e}^{-t^2}\,\mathrm{d}t$，求 $\int_0^1F(x)\,\mathrm{d}x$。

和例 42 相比，这里的 $F$ 已由变限积分定义，但不能写成初等函数，只能让它求导。

它的导数容易求出：由变限积分求导（C.10.1），$F'(x)=-\mathrm{e}^{-x^2}$。因此在分部积分中让 $F$ 求导，把 $\mathrm{d}x$ 积成 $x$：

$$\int_0^1F(x)\,\mathrm{d}x=\Big[xF(x)\Big]_0^1-\int_0^1xF'(x)\,\mathrm{d}x .$$

$F(1)=0$，下限处 $x=0$，所以第一项为 0。第二项代入 $F'(x)$ 后凑微分：

$$\int_0^1F(x)\,\mathrm{d}x=\int_0^1x\mathrm{e}^{-x^2}\,\mathrm{d}x=\Big[-\frac12\mathrm{e}^{-x^2}\Big]_0^1=\frac12\left(1-\mathrm{e}^{-1}\right).$$

分部积分送来的这个 $x$，正好让 $\mathrm{e}^{-x^2}$ 能凑微分。

前面都是已知被积函数、求积分。反过来，遇到一个和式的极限，能不能把它认成某个函数的积分，再交给本章的方法？这是最后一节。

合上书，说出选积分方法的顺序，并解释例 43 为什么要让 $F$ 去求导。

### 10. 一个和式的极限，怎样认出它其实是定积分？

C.9 里定积分是黎曼和的极限。这个定义也可以反着用：看到一个和式的极限，如果它恰好是某个函数的黎曼和，就可以直接写成定积分，再用牛顿–莱布尼茨公式算出来。

拿老朋友 $x^2$ 看。把 $[0,1]$ 等分成 $n$ 份，在每份右端点 $\frac in$ 取函数值 $\big(\frac in\big)^2$ 作矩形的高，每份宽 $\frac1n$，右端点和是

$$S_n=\sum_{i=1}^n\Big(\frac in\Big)^2\cdot\frac1n=\frac1n\sum_{i=1}^n\Big(\frac in\Big)^2.$$

| $n$ | 4 | 10 | 100 | 1000 |
|---|---|---|---|---|
| $S_n$ | 0.46875 | 0.385 | 0.33835 | 0.33383 |

先猜一猜：$n$ 取得越大，这个和会靠近哪个数？表里的数逐渐逼近 $\frac13=\int_0^1x^2\,\mathrm{d}x$。

![左：$n=4$，四个右端点矩形的高分别是 $(\frac14)^2$、$(\frac24)^2$、$(\frac34)^2$、$1$，面积和 0.46875，多出几块；右：$n=10$，矩形更细，面积和 0.385，更贴近曲线 $y=x^2$ 下方的区域（面积 $\frac13$）](fig/C11-n7.pdf){width=85%}

$f$ 在 $[0,1]$ 上连续（所以可积，C.9.3）时，只要分割后最长的小区间长度趋于 0，无论各小区间内选哪个点作取值点，黎曼和都收敛到积分。这里采用等分，每份宽 $\frac1n$，这个条件自动满足：

$$\lim_{n\to\infty}\frac1n\sum_{i=1}^nf\Big(\frac in\Big)=\int_0^1f(x)\,\mathrm{d}x.$$

一般区间 $[a,b]$ 上，分成 $n$ 份，每份宽 $\frac{b-a}n$，右端点 $a+\frac{b-a}ni$。

**方法 10（和式极限化为定积分）**

1. 提出一个 $\frac1n$（它是小区间的宽度），把每一项的其余部分写成 $\frac in$ 的函数 $f\big(\frac in\big)$。
2. 看 $\frac in$ 的范围：$i$ 从 1 到 $n$，$\frac in$ 在 $(0,1]$ 里，对应区间 $[0,1]$；$i$ 从 $n+1$ 到 $2n$ 则对应 $[1,2]$（令 $i=n+j$，$j=1,\dots,n$，则 $\frac in=1+\frac jn$）。
3. 写成 $\int f(x)\,\mathrm{d}x$，用本章的方法积分。

**例 44**　求 $\displaystyle\lim_{n\to\infty}\sum_{i=1}^n\frac1{n+i}$ 和 $\displaystyle\lim_{n\to\infty}\sum_{i=1}^n\frac n{n^2+i^2}$。

和第 10 节开头的 $\sum(i/n)^2\cdot\frac1n$ 相比，这两个和式里没有现成的 $\frac1n$，要自己提。

第一个，分子分母同除以 $n$：

$$\frac1{n+i}=\frac1n\cdot\frac1{1+\frac in},\qquad \sum_{i=1}^n\frac1{n+i}=\frac1n\sum_{i=1}^n\frac1{1+\frac in}\to\int_0^1\frac{\mathrm{d}x}{1+x}=\ln2.$$

第二个，分子分母同除以 $n^2$：

$$\frac n{n^2+i^2}=\frac1n\cdot\frac1{1+(\frac in)^2},\qquad \sum_{i=1}^n\frac n{n^2+i^2}\to\int_0^1\frac{\mathrm{d}x}{1+x^2}=\frac\pi4.$$

数值可以验证：$n=1000$ 时两个和分别是 0.69290 和 0.78515，与 $\ln2=0.69315$、$\frac\pi4=0.78540$ 吻合。

> 求 $\displaystyle\lim_{n\to\infty}\frac1n\sum_{i=1}^n\sin\frac{i\pi}n$。
>
> 答案：$f(x)=\sin(\pi x)$，极限 $=\int_0^1\sin(\pi x)\,\mathrm{d}x=\Big[-\frac{\cos\pi x}\pi\Big]_0^1=\frac2\pi$。

**例 45**　求 $\displaystyle\lim_{n\to\infty}\sum_{i=1}^n\frac n{n^2+i}$。

外观和例 44 相似，结构却不同：分母里是 $i$ 而不是 $i^2$。每一项是 $\frac1n\cdot\frac1{1+i/n^2}$，括号里是 $\frac i{n^2}$，不是 $\frac in$ 的函数，所以不是定积分的形式。这一题用夹逼：$i$ 在 $1$ 到 $n$ 之间，$n^2+1\le n^2+i\le n^2+n$，每一项夹在 $\frac n{n^2+n}$ 与 $\frac n{n^2+1}$ 之间，共 $n$ 项：

$$\frac{n^2}{n^2+n}\le\sum_{i=1}^n\frac n{n^2+i}\le\frac{n^2}{n^2+1}.$$

两边的极限都是 1，所以原极限是 1。认出定积分之前，先问：每一项里的 $i$ 是不是只通过 $\frac in$ 出现。

**例 46**　求 $\displaystyle\lim_{n\to\infty}\Big[\prod_{i=1}^n\Big(1+\frac in\Big)\Big]^{1/n}$。

$\prod$ 读作「连乘」：$\prod_{i=1}^na_i=a_1a_2\cdots a_n$，例如 $\prod_{i=1}^3\big(1+\frac i3\big)=\big(1+\frac13\big)\big(1+\frac23\big)\big(1+\frac33\big)$。和例 44 相比，这里是乘积，不是和式；先取对数，让乘积变成和。

乘积的 $n$ 次方根不是和式，先取对数，用 $\ln(ab)=\ln a+\ln b$ 把乘积变成和：

$$\ln\Big[\prod_{i=1}^n\Big(1+\frac in\Big)\Big]^{1/n}=\frac1n\sum_{i=1}^n\ln\Big(1+\frac in\Big)\to\int_0^1\ln(1+x)\,\mathrm{d}x.$$

积分用分部（例 26 的办法，$u=\ln(1+x)$，$\mathrm{d}v=\mathrm{d}x$）：

$$\int_0^1\ln(1+x)\,\mathrm{d}x=\Big[x\ln(1+x)\Big]_0^1-\int_0^1\frac{x}{1+x}\,\mathrm{d}x .$$

把 $\frac x{1+x}=1-\frac1{1+x}$，第二项是 $\int_0^1\big(1-\frac1{1+x}\big)\mathrm{d}x=1-\ln2$，所以

$$\int_0^1\ln(1+x)\,\mathrm{d}x=\ln2-(1-\ln2)=2\ln2-1 .$$

因为 $\mathrm{e}^x$ 连续，对数的极限是 $2\ln2-1$，原极限就是 $\mathrm{e}^{2\ln2-1}=\frac4{\mathrm{e}}\approx1.4715$。$n=1000$ 时数值是 1.4720。

> 求 $\displaystyle\lim_{n\to\infty}\frac1n\sum_{i=1}^n\frac in\mathrm{e}^{i/n}$。
>
> 答案：$f(x)=x\mathrm{e}^x$，由例 25 的分部积分，极限 $=\int_0^1x\mathrm{e}^x\,\mathrm{d}x=[(x-1)\mathrm{e}^x]_0^1=1$。

合上书，写出和式极限化为定积分的三步，并用 $\sum\frac n{n^2+i}$ 说明什么时候不能这样化。

回到开头的问题。十天累计新增多少用户：被积式 $\frac{200t}{1+t^2}$ 的分子是分母导数的倍数，凑微分得 $N(T)=100\ln(1+T^2)$，$T=10$ 时约 462 人（例 8）。边际成本求总成本是同一件事，把被积函数换成边际成本函数就行。表里没有的 $\int x\mathrm{e}^{x^2}\mathrm{d}x$ 也有了答案：凑微分一行，$\frac12\mathrm{e}^{x^2}+C$（例 1）。而 $\int\mathrm{e}^{x^2}\mathrm{d}x$ 这一类，方法再多也写不成初等函数（第 9 节），只能用定积分表示或求近似值。

### 本章小结

| 方法 | 什么时候用 | 对应题号 |
|---|---|---|
| 方法 1（凑微分） | 被积函数是「内层的函数」乘「内层的导数」；变形后才露出整体；三角函数的幂；构造辅助函数 | C11-10 |
| 方法 2（第二类换元） | 去不掉的根号：三角代换、根式代换、倒代换 | C11-13 |
| 方法 3（定积分换元） | 定积分里换元，换限不回代；积分号里含 $x$ 时让它跑到积分限上 | C11-01、C11-06、C11-12 |
| 方法 4（对称性） | 对称区间上的奇偶函数；整数个周期；区间再现 $x\to a+b-x$ | C11-05、C11-16 |
| 方法 5（分部积分） | 两类函数相乘；$\ln x$、反三角函数；循环型 | C11-02、C11-07、C11-11、C11-14 |
| 方法 6（华里士公式） | $\int_0^{\pi/2}\sin^nx\,\mathrm{d}x$、$\cos^n$；换元后化成它 | C11-08 |
| 方法 7（部分分式） | 有理函数：先除、再分解、求系数、逐项积分 | C11-04 |
| 方法 8（化为有理函数） | $\sin x$、$\cos x$ 的有理式；简单根式；$\mathrm{e}^x$ 的有理式 | C11-09 |
| 方法 9（选方法的顺序） | 拿到一个积分先试哪种；没有初等原函数的积分 | C11-03 |
| 方法 10（和式极限化定积分） | 提出 $\frac1n$，其余是 $\frac in$ 的函数 | C11-11、C11-17 |

章末混合练习 C11-12、C11-13、C11-14、C11-15、C11-16、C11-17 混入前面各章的内容，要先认出该用哪一种方法。

本章在主线上的位置：C.10 的基本定理说，只要找到一个原函数，定积分就能算出来；本章把求导的两条主要规则（链式法则、乘积法则）倒过来，让「找原函数」从查表变成有章可循的技术，并且看到这条路并非总是通的。

**谁推出谁**（沿用 C.9、C.10 的关系图，标出本章新增）：

$$\text{连续}\Rightarrow\text{可积（C.9）},\qquad \text{连续}\Rightarrow\text{有原函数（C.10）},\qquad \text{有原函数}\ \overset{\text{本章新增}}{\not\Rightarrow}\ \text{原函数是初等函数}.$$

最后一个箭头不成立的标准反例是 $\mathrm{e}^{-x^2}$、$\frac{\sin x}x$：它们连续，原函数存在，却写不成初等函数（第 9 节）。有理函数则相反，原函数总是初等函数（第 7 节），这是它有固定程序的原因。
