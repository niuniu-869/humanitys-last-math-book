## M.16 · 生成模型：隐变量、ELBO、VAE 与 GAN

M.14 里的语言模型一个词一个词地往外写，因为文字天然有先后。图像也可以先规定像素的次序再逐个生成，不过一张图里几十万个像素互相牵连，这不是唯一的办法。本章走另一条路：先随机抽一个较短的向量，再让一个网络把它变成整张图。

这个办法今天处处可见。一些文生图工具先把图像转换成较小的表示，在这个小表示上做主要的生成计算，最后解码回图像，这个转换用的就是本章的 VAE。例如把 $512\times512\times3$ 个数转换成 $64\times64\times4$ 个数，元素数量变成原来的 $1/48$。这只说明尺寸怎样缩小，真实模型更复杂；逐步加噪去噪的生成计算留到 M.17。人脸合成、老照片修复里也有它的影子。

问题出在训练上。早期的自编码器能把图压缩再还原，却不会生成：它不知道该往解码器里送什么。2013 年底，Kingma 与 Welling 解决的正是这件事：隐变量的后验算不出来时怎样训练。他们用 Jensen 不等式得到一个可以优化的下界，再用"重参数化"让梯度穿过随机抽样，结果叫 VAE（变分自编码器）。几乎同时，Goodfellow 等人在 2014 年走了另一条路：干脆不写出概率，让生成器和一个判别器对抗，这就是生成对抗网络（GAN）。采用简单高斯解码器的 VAE 常常生成偏平滑的图，GAN 能生成清晰的样本，对抗训练却可能不稳定。这是常见的现象，不是两类模型在所有设置下的保证；这两个缺点也给了下一章的扩散模型机会。

按主线的三件套来填：VAE 的 $f$ 是"编码器 + 解码器"，$L$ 是负的 ELBO（本章第 3 节得到），更新规则仍是梯度下降。GAN 的两个网络各自优化自己的损失，原始形式可以合写成一个极小极大目标。

本章按这个顺序拆开：第 1 节说明隐变量模型和它为什么难算；第 2 节学 Jensen 不等式；第 3 节推出 ELBO；第 4 节看 ELBO 怎样给出 EM 算法；第 5 节解决"梯度怎样穿过随机抽样"；第 6 节把它们合成 VAE 的损失；第 7、8 节讲 GAN 的目标和它实际在优化什么；第 9 节解释 GAN 的毛病。

### 1. 怎样让模型凭空生成一张新图？

本章先研究一种常用的隐变量模型，分两步生成。先从标准正态分布抽一个 $d_z$ 维向量 $\boldsymbol z$（"隐"，是因为数据里看不见它），再让解码器网络 $g_\theta$ 把 $\boldsymbol z$ 变成一张图的均值：

$$p(\boldsymbol z)=N(\boldsymbol 0,I),\qquad p_\theta(\boldsymbol x\mid\boldsymbol z)=N\big(\boldsymbol x;\ g_\theta(\boldsymbol z),\ \sigma_x^2I\big).$$

$I$ 是相应维数的单位矩阵，$\theta$ 表示解码器的参数；$N(\boldsymbol x;\boldsymbol m,\Sigma)$ 表示均值为 $\boldsymbol m$、协方差为 $\Sigma$ 的正态密度在 $\boldsymbol x$ 处的值，这里每个像素的条件方差都固定为 $\sigma_x^2>0$。

$g_\theta:\mathbb R^{d_z}\to\mathbb R^{d_x}$ 是一个神经网络，$d_x$ 是像素总数，$d_z$ 远小于 $d_x$。一张图有几十万个像素，却能由一个短向量决定，是因为自然图像里的像素高度相关：同一张脸，真正在变的只有表情、角度、光照这几个自由度，所以短向量可以当作压缩的编码。两步合起来，$(\boldsymbol x,\boldsymbol z)$ 的联合分布是 $p(\boldsymbol z)\,p_\theta(\boldsymbol x\mid\boldsymbol z)$。$p_\theta(\boldsymbol x\mid\boldsymbol z)$ 和 $p_\theta(\boldsymbol x)$ 都是概率密度。模型在一张图 $\boldsymbol x$ 处的密度，是把 $\boldsymbol z$ 的所有可能取值积掉（P.6.3 的边缘分布）：

$$p_\theta(\boldsymbol x)=\int p_\theta(\boldsymbol x\mid\boldsymbol z)\,p(\boldsymbol z)\,\mathrm d\boldsymbol z .$$

以上是模型本身的假设。训练就是 P.11.3 的最大似然：让 $\sum_i\log p_\theta(\boldsymbol x_i)$ 最大。麻烦在这个积分：对一般的非线性网络解码器，它通常没有方便的闭式表达式。直接从先验抽样仍可以估计它，但 $\boldsymbol z$ 有几十维时，能解释 $\boldsymbol x_i$ 的 $\boldsymbol z$ 只占整个空间里很小的一块，随手抽中的概率很小，往往要抽很多样本才能得到稳定的估计。

要看清结构，先看一个能手算的最小例子：$\boldsymbol z$ 不取连续值，只取两个编号，积分换成求和。这就是高斯混合模型。

**方法 1（隐变量模型的边缘与后验）**

1. 写出联合：$p(x,z)=p(z)\,p(x\mid z)$。
2. 求边缘：对 $z$ 求和（连续时求积分），$p(x)=\sum_z p(x,z)$。
3. 求后验（贝叶斯公式）：$p(z\mid x)=p(x,z)/p(x)$，它回答"这个 $x$ 最可能是由哪个 $z$ 生成的"。

**例 1**　先从隐变量只取两个值的情形算起，这样积分变成求和。设 $z\in\{1,2\}$，$P(z=1)=0.4$，$P(z=2)=0.6$；$x\mid z=1\sim N(-1,1)$，$x\mid z=2\sim N(2,1)$。求边缘密度在 $x=0$ 处的值 $p(0)$、$\log p(0)$ 和后验概率 $P(z\mid x=0)$。

记 $\nu(t)=e^{-t^2/2}/\sqrt{2\pi}$ 为标准正态密度（本章 $\log$ 都指自然对数）。$\nu(1)\approx0.2420$，$\nu(2)\approx0.0540$。$x=0$ 到两个中心的距离分别是 1 和 2。

先写联合，两项分别是

$$p(0,z{=}1)=0.4\times0.2420=0.0968,\qquad p(0,z{=}2)=0.6\times0.0540=0.0324 .$$

再求边缘，把两项相加：$p(0)\approx0.1292$，$\log p(0)\approx-2.0465$。

最后求后验，各项除以 $p(0)$：

$$P(z{=}1\mid x{=}0)\approx0.7492,\qquad P(z{=}2\mid x{=}0)\approx0.2508 .$$

先验里 $z=2$ 的概率更大（0.6），但 $x=0$ 离第一个中心近得多，所以后验反过来偏向 $z=1$。

![混合密度是两个加权成分之和：实线是 $p(x)$，虚线是 $0.4\,N(-1,1)$（成分 1），点划线是 $0.6\,N(2,1)$（成分 2），竖线标出 $x=0$；该处虚线较高，后验就是两条曲线在 $x=0$ 处的高度占总高度的比例](fig/M16-n1.pdf){width=70%}

> 设 $P(z{=}1)=P(z{=}2)=0.5$，$x\mid z=1\sim N(0,1)$，$x\mid z=2\sim N(3,1)$。求 $p(1)$ 和 $P(z=1\mid x=1)$。
>
> 答案：联合两项为 $0.5\nu(1)=0.1210$ 和 $0.5\nu(2)=0.0270$，$p(1)\approx0.1480$，后验 $P(z=1\mid x=1)\approx0.8176$。

连续的 $\boldsymbol z$ 把求和换成积分。线性高斯等特殊情形还能算出边缘和后验；一般的非线性解码器通常难以直接计算。例 1 里的 $\log p(0)=\log(0.0968+0.0324)$ 是一个和的对数，对数套在求和（连续时是积分）外面，既不能拆开，也没法逐项求导。下一节先解决这个形状上的麻烦。

合上书，写出隐变量模型的联合、边缘和后验三个式子，并说明为什么一般的非线性解码器会让边缘难算。

### 2. 对数里面套着一个期望，怎样把它拿到外面？

先回到例 1 的数。$x=0$ 处，两个成分给出的密度是 $0.2420$ 和 $0.0540$，先验权重是 $0.4$ 和 $0.6$，所以 $p(0)$ 是这两个数按权重取的平均，也就是先验下的期望 $p(0)=E_{p(z)}[p(0\mid z)]\approx0.1292$，取对数得 $-2.0465$。

如果把 $\log$ 先挪进去，再取平均，得到 $0.4\log0.2420+0.6\log0.0540\approx-2.3189$。这两个数不相等，后者小。一般的隐变量模型里，$\log$ 在期望外面时没法逐项处理，挪进里面就容易了，代价是等号变成不等号。本节先证明这个不等式，第 3 节再引入可以选择的分布 $q$，得到便于训练的下界。

先说一个叫法，沿用 C.8 和 M.1.5 的约定：二阶可导的函数，$f''\ge0$ 叫凸函数，$f''\le0$ 叫凹函数。$\log x$ 的二阶导数是 $-1/x^2<0$，曲线向下弯，弦在曲线下方，所以对数是凹函数。

凹函数的弦在曲线下方，把它写成两点的式子：对 $a,b>0$ 和 $0\le\lambda\le1$，

$$\log\big(\lambda a+(1-\lambda)b\big)\ \ge\ \lambda\log a+(1-\lambda)\log b .$$

左边是"先平均再取对数"，右边是"先取对数再平均"。这是两点的情形，把权重 $\lambda,1-\lambda$ 看成一个取两个值的随机变量的概率，它就是下面定理的特例。

**定理（Jensen 不等式，对数的情形）** 设 $X>0$ 是随机变量，$E[X]$ 与 $E[|\log X|]$ 都有限，则

$$\log E[X]\ \ge\ E[\log X],$$

等号当且仅当 $X$ 几乎处处等于常数（几乎处处，指以概率 1 成立；只在概率为 0 的地方取别的值，不影响期望）。

*思路*：在均值处作切线。凹函数的图像总在切线下方，两边取期望，切线的一次项恰好消掉。

*证明*：

1. 记 $\mu=E[X]>0$。$\log$ 在 $x=\mu$ 处的切线是 $y=\log\mu+\frac{1}{\mu}(x-\mu)$，斜率 $1/\mu$ 来自 $(\log x)'=1/x$。
2. 因为 $\log$ 是凹函数，图像在切线下方：对一切 $x>0$，$\log x\le\log\mu+\frac{x-\mu}{\mu}$。这也可以直接验证：令 $t=x/\mu$，它就是 P.14.4 里用过的 $\ln t\le t-1$。
3. 把 $x$ 换成随机变量 $X$，两边取期望（期望保持不等号，P.7 的单调性）：
$$E[\log X]\le\log\mu+\frac{E[X]-\mu}{\mu}=\log\mu+0=\log E[X].$$
4. 等号：第 2 步里切线与曲线之差 $\log\mu+\frac{X-\mu}{\mu}-\log X$ 恒非负，它的期望为 0，只能是这个差以概率 1 为 0；而 $\ln t\le t-1$ 只在 $t=1$ 取等号，所以必须 $X=\mu$ 几乎处处成立。 $\square$

三个条件各有用处。$X>0$ 保证 $\log X$ 有意义，$X$ 取到负值时 $\log X$ 就没有定义；$E[X]$ 与 $E[|\log X|]$ 有限保证两边都是有限的数；凹性决定不等号的方向，拿凸函数 $x^2$ 来做，不等号就反过来：$E[X^2]\ge(E[X])^2$，这正是方差非负。

![对数是凹函数：弦（虚线）在曲线下方，$X$ 取 1 和 4 各一半时，$\log E[X]=\log2.5$ 在曲线上，$E[\log X]=\tfrac12\log4$ 在弦上，弦上的点比曲线上的低](fig/M16-n2.pdf){width=60%}

**方法 2（Jensen 放缩）**

1. 把要处理的量写成 $\log E_q[\,\cdot\,]$ 的形式。
2. 确认里面的量为正、相关期望有限，并且外面的函数是凹的。
3. 把 $\log$ 挪进期望，得到下界 $E_q[\log\,\cdot\,]$，等号当且仅当里面的量在 $q$ 下以概率 1 等于同一个常数。

**例 2**　先在最简单的随机变量上看差距有多大。设 $X$ 取 1 和 4，概率各为 $\tfrac12$，求 $\log E[X]$ 与 $E[\log X]$，并说明差距。

$E[X]=\tfrac12(1+4)=2.5$，所以 $\log E[X]=\log2.5\approx0.9163$。

另一边 $E[\log X]=\tfrac12\log1+\tfrac12\log4=\log2\approx0.6931$。

于是 $0.6931\le0.9163$，差距约 0.2231。两个取值不同，所以严格不等号成立；$X$ 取常数时差距为 0。把 $\log$ 和期望随手互换是很自然的错误，这一题说明两者不等，互换后的值总是偏小。

> 设 $X$ 取 1 和 9，概率各为 $\tfrac12$，求两者的差距。
>
> 答案：$\log5\approx1.6094$，$E[\log X]=\tfrac12\log9\approx1.0986$，差距约 0.5108。

合上书，写出 Jensen 不等式的切线证明的四步，并说明为什么等号只在 $X$ 是常数时成立。

### 3. 似然算不出来，能不能改为最大化它的一个下界？

上一节在例 1 的数上做的，其实是用先验 $p(z)$ 当权重：$\log p(0)=-2.0465$，挪进去的值 $-2.3189$ 是它的一个下界，差了 $0.2724$。这个差很大，原因是先验给 $z=2$ 的权重 0.6 太高，而 $x=0$ 更可能来自 $z=1$（后验 $0.7492$）。换一个权重，也就是自己选一个更合适的分布 $q$，下界应该会更紧。

一般地，回到 $\log p(\boldsymbol x)=\log\int p(\boldsymbol x,\boldsymbol z)\,\mathrm d\boldsymbol z$。固定一个观测 $\boldsymbol x$，满足 $0<p(\boldsymbol x)<\infty$。再选一个我们自己的分布 $q(\boldsymbol z)$：它能抽样、能算密度（之后由编码器给出）。本节只讨论 $q(\boldsymbol z)$ 与 $p(\boldsymbol x,\boldsymbol z)$ 取正值的范围相同，并且下面各项期望都有限的情形，这样乘除 $q$ 时分母不会为零。在被积函数上乘一次除一次：

$$\log p(\boldsymbol x)=\log\int q(\boldsymbol z)\,\frac{p(\boldsymbol x,\boldsymbol z)}{q(\boldsymbol z)}\,\mathrm d\boldsymbol z=\log E_{q}\!\left[\frac{p(\boldsymbol x,\boldsymbol z)}{q(\boldsymbol z)}\right].$$

乘除 $q$ 的目的是把积分写成 $q$ 下的期望，这样才能用方法 2。里面的量 $p(\boldsymbol x,\boldsymbol z)/q(\boldsymbol z)$ 为正，对数是凹的，Jensen 不等式给出

$$\log p(\boldsymbol x)\ \ge\ E_{q}\!\left[\log\frac{p(\boldsymbol x,\boldsymbol z)}{q(\boldsymbol z)}\right]=:\mathrm{ELBO}(q).$$

ELBO 是 evidence lower bound（证据下界）的缩写。$p(\boldsymbol x)$ 在统计里叫证据，$\log p(\boldsymbol x)$ 是对数证据，这里的下界针对后者。

把联合拆成 $p(\boldsymbol x\mid\boldsymbol z)\,p(\boldsymbol z)$，里面的对数就拆成两项：

$$E_q\Big[\log\frac{p(\boldsymbol x\mid\boldsymbol z)\,p(\boldsymbol z)}{q(\boldsymbol z)}\Big]=E_q\big[\log p(\boldsymbol x\mid\boldsymbol z)\big]+E_q\Big[\log\frac{p(\boldsymbol z)}{q(\boldsymbol z)}\Big].$$

第二项的相反数正是 $\mathrm{KL}(q\Vert p(\boldsymbol z))$。所以 ELBO 拆成两项：

$$\mathrm{ELBO}=\underbrace{E_{q}\big[\log p(\boldsymbol x\mid\boldsymbol z)\big]}_{\text{重建项}}\ -\ \underbrace{\mathrm{KL}\big(q(\boldsymbol z)\,\Vert\,p(\boldsymbol z)\big)}_{\text{先验项}} .$$

第一项问：从 $q$ 里抽出的 $\boldsymbol z$，解码器能不能把 $\boldsymbol x$ 画回来。第二项问：$q$ 离标准正态先验有多远（P.14.4 的 KL 散度）。这是一个拉锯：只追求重建，$q$ 会把每张图编码到各不相同的角落，离先验很远；只追求贴近先验，$q$ 就不带任何关于 $\boldsymbol x$ 的信息。

下界和真值差多少？这个差正好是一个 KL。把 $p(\boldsymbol x,\boldsymbol z)=p(\boldsymbol z\mid\boldsymbol x)\,p(\boldsymbol x)$ 代进 ELBO：

$$\mathrm{ELBO}=E_q\!\left[\log\frac{p(\boldsymbol z\mid\boldsymbol x)\,p(\boldsymbol x)}{q(\boldsymbol z)}\right]=\log p(\boldsymbol x)\ -\ E_q\!\left[\log\frac{q(\boldsymbol z)}{p(\boldsymbol z\mid\boldsymbol x)}\right].$$

这里 $\log p(\boldsymbol x)$ 不含 $\boldsymbol z$，期望里直接提出来。于是

$$\log p(\boldsymbol x)-\mathrm{ELBO}(q)=\mathrm{KL}\big(q(\boldsymbol z)\,\Vert\,p(\boldsymbol z\mid\boldsymbol x)\big)\ \ge0 .$$

这给出了 ELBO 的第二个证明（KL 非负，P.14.4），并且比 Jensen 多说了两件事：差距恰好是 $q$ 与真实后验的 KL；当且仅当 $q$ 与 $p(\boldsymbol z\mid\boldsymbol x)$ 以概率 1 相同时下界贴紧。

这对训练意味着什么？固定模型参数时，$\log p_\theta(\boldsymbol x)$ 不变，增大 ELBO 就是在缩小 $q$ 与当前真实后验的 KL。

模型参数也要改，这时真实似然和这个差距都在变，不能保证每次提高 ELBO 都会提高真实似然，第 4 节的 EM 靠特定的两步交替来保证。好处是计算 ELBO 不必求出后验，只需要能算联合密度和 $q$ 的密度，并能从 $q$ 抽样。

**方法 3（ELBO 的拆分与差距）**

1. 写出 $\mathrm{ELBO}(q)=E_q[\log p(x,z)]-E_q[\log q(z)]$，按需拆成"重建项 − 先验项"。
2. 差距 $=\log p(x)-\mathrm{ELBO}(q)=\mathrm{KL}(q\Vert p(z\mid x))$。
3. 等号条件：$q$ 与 $p(z\mid x)$ 相同（有限离散情形就是两个概率向量相等）。

**例 3**　数据沿用例 1，$x=0$，现在只多了一个自己选的 $q$。取 $q=(0.5,0.5)$（即 $q(z{=}1)=q(z{=}2)=0.5$），算 ELBO、两种拆分和差距。

联合 $p(0,z{=}1)=0.0968$，$p(0,z{=}2)=0.0324$ 已在例 1 求出。直接按定义：

$$\mathrm{ELBO}=0.5\log\frac{0.0968}{0.5}+0.5\log\frac{0.0324}{0.5}\approx-2.1893 .$$

用"重建 − 先验"拆开核对。重建项 $E_q[\log p(0\mid z)]=0.5(-1.4189)+0.5(-2.9189)=-2.1689$，其中 $\log\nu(1)=-1.4189$，$\log\nu(2)=-2.9189$。先验项 $\mathrm{KL}(q\Vert p(z))=0.5\log\frac{0.5}{0.4}+0.5\log\frac{0.5}{0.6}=0.0204$。两者相减 $-2.1689-0.0204=-2.1893$，一致。

差距：$\log p(0)-\mathrm{ELBO}=-2.0465+2.1893=0.1428$。这应当等于 $\mathrm{KL}(q\Vert\text{后验})$，后验是例 1 的 $(0.7492,0.2508)$：

$$0.5\log\frac{0.5}{0.7492}+0.5\log\frac{0.5}{0.2508}\approx0.1428 .$$

三种算法一致。把三个 $q$ 排在一起：取先验 $(0.4,0.6)$ 就是上一节的 $-2.3189$，取 $(0.5,0.5)$ 是 $-2.1893$，取后验 $(0.7492,0.2508)$ 时 ELBO 等于 $\log p(0)=-2.0465$，差距 0。越靠近后验，下界越紧。

![把 $q(z{=}1)=s$ 当自变量：实线是 ELBO，水平虚线是 $\log p(0)=-2.0465$；ELBO 处处在虚线下方，只在 $s=0.7492$（后验）处与虚线相切，竖直方向的间隔就是 $q$ 与后验的 KL](fig/M16-n3.pdf){width=70%}

> 仍用例 1 的模型，取 $q=(0.2,0.8)$，求 ELBO 和差距。
>
> 答案：ELBO $=0.2\log\frac{0.0968}{0.2}+0.8\log\frac{0.0324}{0.8}\approx-2.7105$，差距 $\approx0.664$。$q$ 偏离后验越远，下界越松。

合上书，写出 ELBO 的定义、"重建 − 先验"的拆法，并推出"差距恰好是 $q$ 与后验的 KL"。

还剩两件事。$q$ 取后验时下界最紧，混合模型里后验只是一次贝叶斯公式，下一节就用它估参数。神经网络解码器的后验算不出来，那就要把 $q$ 也交给网络，而这立刻带来第 5 节的问题。

### 4. 高斯混合的参数怎样估？

这一节讲一个独立的经典算法，不读不影响后面。例 1 假定了两个成分的中心和权重，现实中它们要由数据估计，可是估计时又需要知道每个点属于哪个成分。ELBO 的两个"抬高"可以交替做，得到的就是期望最大化（EM）算法（Dempster 等，1977）：E 步求期望（取后验），M 步最大化。

设混合模型的参数 $\theta$ 是各成分的均值和权重，数据是 $x_1,\dots,x_n$，每个 $x_i$ 有自己的隐变量 $z_i$。第 3 节说，固定 $\theta$ 时取 $q=p(z\mid x;\theta)$ 能让下界贴紧；固定 $q$ 时对 $\theta$ 最大化 ELBO 能把下界抬高（这里假定 E 步精确取到后验，M 步精确求出最大点）。后一步的目标是 $\mathrm{ELBO}(q,\theta)=E_q[\log p_\theta(x,z)]+H(q)$，其中 $H(q)=-E_q[\log q(z)]$ 与 $\theta$ 无关，所以只需最大化 $E_q[\log p_\theta(x,z)]$。交替做这两步：

**方法 4（EM 的一轮）**

1. E 步：对每个点算后验 $r_{ik}=P(z_i=k\mid x_i;\theta)$，叫第 $k$ 个成分对点 $i$ 的"责任"。
2. M 步：最大化 $\sum_i\sum_k r_{ik}\log p(x_i,z_i{=}k;\theta)$。成分方差固定为 1 时，这等价于每个成分取"责任加权平均"：$\mu_k=\sum_i r_{ik}x_i\big/\sum_i r_{ik}$，$\pi_k=\sum_i r_{ik}/n$。
3. 重复到对数似然不再上升。

M 步里的两个更新是怎么来的？先看均值。目标里含 $\mu_k$ 的部分是 $\sum_i r_{ik}\big(-\tfrac12(x_i-\mu_k)^2\big)$，对 $\mu_k$ 求导令其为 0：

$$\sum_i r_{ik}(x_i-\mu_k)=0\ \Longrightarrow\ \mu_k=\frac{\sum_i r_{ik}x_i}{\sum_i r_{ik}} .$$

再看权重。记 $N_k=\sum_i r_{ik}$，含 $\pi_k$ 的部分是 $\sum_k N_k\log\pi_k$，约束是 $\sum_k\pi_k=1$。用拉格朗日乘子（C.22）：$N_k/\pi_k=\lambda$，所以 $\pi_k=N_k/\lambda$；对 $k$ 求和并用 $\sum_k\pi_k=1$ 得 $\lambda=\sum_kN_k=n$，于是 $\pi_k=N_k/n$。每个 $\pi_k$ 的二阶导数 $-N_k/\pi_k^2<0$，这是最大点。

**例 4**　例 1 里成分的中心是已知的，后验直接可算；这里中心要由数据估计，后验只是第一步。五个点 $x=(-2,-1,0,3,4)$，两个方差为 1 的高斯成分，初值 $\mu=(-1,1)$，$\pi=(0.5,0.5)$，做一轮 EM。

E 步。先算第一个点 $x_1=-2$：它到两个中心 $-1$ 和 $1$ 的距离分别是 1 和 3，权重相等，所以

$$r_{11}=\frac{\nu(1)}{\nu(1)+\nu(3)}\approx0.982 .$$

五个点对第一个成分的责任依次约为 $(0.982,0.881,0.5,0.0025,0.0003)$：靠左的点几乎全归第一个成分，$x=0$ 到两个中心等距，各占一半，靠右的两个点几乎全归第二个。第二个成分的责任是 $1-r_{i1}$。责任之和为 $N_1=2.366$，$N_2=2.634$。

M 步：

$$\mu_1=\frac{\sum_i r_{i1}x_i}{N_1}\approx-1.199,\quad\mu_2\approx2.595,\quad\pi=\Big(\frac{N_1}{5},\frac{N_2}{5}\Big)\approx(0.473,0.527).$$

对数似然从 $-14.719$ 升到 $-10.172$；再做一轮升到 $-9.225$，$\mu$ 变成 $(-1.025,3.373)$。

> 两个点 $x=(0,2)$，两个方差为 1 的成分，初值 $\mu=(0,2)$，$\pi=(0.5,0.5)$，做一轮 EM。
>
> 答案：点 $x=0$ 对第一个成分的责任是 $\frac{\nu(0)}{\nu(0)+\nu(2)}\approx0.8808$，$x=2$ 对第一个成分的责任是 $0.1192$；$N_1=N_2=1$，所以 $\pi$ 不变，$\mu_1=0.1192\times2=0.2384$，$\mu_2=2-0.2384=1.7616$。两个中心互相靠拢，因为每个点都有一部分归给了对方。

似然单调不降，理由就是第 3 节的两句话。设 $\theta_{\text{旧}}$ 为当前参数，E 步取出 $q$，下面三步先对单个 $x$ 写；对数据集，把各点的 ELBO 相加，每个 $x_i$ 的不等式都成立，求和后仍成立，M 步最大化的正是这个和。三步用的是同一个 $q$：

1. E 步让下界贴紧：$\log p(x;\theta_{\text{旧}})=\mathrm{ELBO}(q,\theta_{\text{旧}})$。
2. M 步把 $\theta$ 换成使 ELBO 更大的 $\theta_{\text{新}}$：$\mathrm{ELBO}(q,\theta_{\text{新}})\ge\mathrm{ELBO}(q,\theta_{\text{旧}})$。
3. ELBO 永远不超过似然：$\log p(x;\theta_{\text{新}})\ge\mathrm{ELBO}(q,\theta_{\text{新}})$。

连起来是 $\log p(x;\theta_{\text{新}})\ge\mathrm{ELBO}(q,\theta_{\text{新}})\ge\mathrm{ELBO}(q,\theta_{\text{旧}})=\log p(x;\theta_{\text{旧}})$，似然没有下降。

合上书，写出 EM 的一轮：E 步算后验责任 $r_{ik}$，M 步推出均值和权重的更新，并说明为什么每轮迭代后似然不降。

如果各成分的权重固定相等、方差固定相同，并把每个点硬分配给最近的中心（责任取 0 或 1），再把中心更新为组内平均，就得到 M.4.7 的 k-means 的两步。一般的混合模型里，最大后验的分配还受权重和方差影响，不能只看离哪个中心最近。VAE 的神经网络后验没有闭式解，E 步做不了，所以第 5 节要换一个办法同时优化两边。

### 5. 期望里面有随机抽样，梯度怎样穿过去？

VAE 把 $q$ 也写成带参数的分布 $q_\phi(\boldsymbol z\mid\boldsymbol x)$，取对角高斯（各分量独立的正态分布），由编码器给出它的均值 $\boldsymbol\mu_\phi(\boldsymbol x)$ 和标准差 $\boldsymbol\sigma_\phi(\boldsymbol x)$（都是 $d_z$ 维，标准差取正值；网络常输出 $\ell_j=\log\sigma_j^2$，再由 $\sigma_j=e^{\ell_j/2}$ 得到正的标准差）。ELBO 的重建项是 $E_{\boldsymbol z\sim q_\phi}[f(\boldsymbol z)]$，其中 $f(\boldsymbol z)=\log p_\theta(\boldsymbol x\mid\boldsymbol z)$。要对 $\phi$ 求梯度，但 $\phi$ 出现在"从哪个分布抽"里，不在被积函数里。

直接做法是把梯度符号挪进期望，写成 $E_q[\nabla_\phi f(\boldsymbol z)]$。这个等号不成立。拿一维的 $f(z)=z^2$、$q=N(\mu,\sigma^2)$ 试：$f(z)$ 里没有 $\mu$，挪进去以后右边恒为 0；而 $E_q[z^2]=\mu^2+\sigma^2$，对 $\mu$ 的导数是 $2\mu$，一般不为 0。$\mu$ 藏在抽样的分布 $q_\phi$ 里，$\boldsymbol z$ 一旦抽出来，梯度就断在这里。

办法是把随机性挪走。抽 $\varepsilon\sim N(\boldsymbol 0,I)$（它的分布与 $\phi$ 无关），再令

$$\boldsymbol z=\boldsymbol\mu+\boldsymbol\sigma\odot\boldsymbol\varepsilon .$$

$\odot$ 是逐分量相乘。由 P.5.3 的线性变换，$\boldsymbol z$ 的分布就是 $N(\boldsymbol\mu,\mathrm{diag}(\boldsymbol\sigma^2))$，其中 $\mathrm{diag}(\boldsymbol\sigma^2)$ 是把各个 $\sigma_j^2$ 放在对角线上、其余位置为零的矩阵。这与直接从 $q_\phi$ 抽没有区别。但现在 $\boldsymbol z$ 是 $\phi$ 的确定函数，加上一个与 $\phi$ 无关的噪声：

$$E_{\boldsymbol z\sim q_\phi}[f(\boldsymbol z)]=E_{\boldsymbol\varepsilon}\big[f(\boldsymbol\mu+\boldsymbol\sigma\odot\boldsymbol\varepsilon)\big],\qquad \nabla_\phi E=E_{\boldsymbol\varepsilon}\big[\nabla_\phi f(\boldsymbol\mu+\boldsymbol\sigma\odot\boldsymbol\varepsilon)\big].$$

第二个等号现在可以成立：分布不再依赖 $\phi$，先沿着确定的运算过程求导，里面是普通的链式法则（M.7.5）。求导和期望能交换，需要导数不会大到让期望失控，本章的多项式和高斯例子都满足。每个分量上：

$$\frac{\partial f}{\partial\mu_j}=\frac{\partial f}{\partial z_j},\qquad \frac{\partial f}{\partial\sigma_j}=\frac{\partial f}{\partial z_j}\,\varepsilon_j .$$

形状账本：$\boldsymbol\mu,\boldsymbol\sigma,\boldsymbol\varepsilon,\boldsymbol z\in\mathbb R^{d_z}$，两个梯度与 $\boldsymbol\mu,\boldsymbol\sigma$ 同形。代码对照只有两行：

```
eps = np.random.randn(d_z)     # 与参数无关的噪声
z = mu + sigma * eps           # 梯度从 z 流回 mu, sigma
```

**方法 5（重参数化求梯度）**

1. 把 $z\sim N(\mu,\sigma^2)$ 改写成 $z=\mu+\sigma\varepsilon$，$\varepsilon\sim N(0,1)$。
2. 抽一个（或几个）$\varepsilon$，算 $z$ 和 $f(z)$（$f$ 要对 $z$ 可导）。
3. 链式法则：$\partial f/\partial\mu=f'(z)$，$\partial f/\partial\sigma=f'(z)\,\varepsilon$。

**例 5**　先在最简单的 $f$ 上把重参数化走通，第 6 节的重建项就是这类期望。设 $f(z)=z^2$，$q=N(\mu,\sigma^2)$，$\mu=1$，$\sigma=0.5$。先用公式求精确梯度，再用抽到的 $\varepsilon=0.8$ 做一次重参数化估计。

精确值：$E[z^2]=\mu^2+\sigma^2$（方差公式），所以 $\partial/\partial\mu=2\mu=2$，$\partial/\partial\sigma=2\sigma=1$。

估计：$z=1+0.5\times0.8=1.4$，$f'(z)=2z=2.8$。于是 $\partial f/\partial\mu=2.8$，$\partial f/\partial\sigma=2.8\times0.8=2.24$。

单次估计和精确值不同，但在 $\varepsilon$ 上平均，$E[2(1+0.5\varepsilon)]=2$，$E[2(1+0.5\varepsilon)\varepsilon]=2\times0.5=1$，恰是精确值。

> 设 $f(z)=(z-2)^2$，$\mu=1$，$\sigma=0.5$，抽到 $\varepsilon=-0.4$，求 $\partial f/\partial\mu$ 和 $\partial f/\partial\sigma$ 的一次估计，并给出精确值。
>
> 答案：$z=0.8$，$f'(z)=2(z-2)=-2.4$，估计为 $-2.4$ 和 $0.96$。精确：$E f=(\mu-2)^2+\sigma^2$，梯度 $2(\mu-2)=-2$ 和 $2\sigma=1$。

M.15.4 的对数导数技巧也能处理这个问题，两种做法值得并排看。先猜一下：在例 5 里，对 $\mu$ 的单次估计，哪一种的方差更小？

| | 重参数化 | 对数导数技巧 |
|---|---|---|
| 公式 | $\nabla_\phi E[f]=E_\varepsilon[\nabla_\phi f(g_\phi(\varepsilon))]$ | $\nabla_\phi E[f]=E_q[f(z)\,\nabla_\phi\log q_\phi(z)]$ |
| 要求 | $f(g_\phi(\varepsilon))$ 对参数可导，且求导与期望可交换 | 分布对参数可导，求导与求和或积分可交换；$f$ 只需能算值，离散的也行 |
| 例 5 中对 $\mu$ 的单次估计的方差 | $4\sigma^2=1$ | $21.75$ |

后者对 $\mu$ 的一次估计是 $f(z)\cdot\frac{z-\mu}{\sigma^2}=z^2\frac{z-\mu}{\sigma^2}$，精确期望也是 2。方差 21.75 是这样来的：代入 $z=1+0.5\varepsilon$，估计量是 $T=2\varepsilon+2\varepsilon^2+\tfrac12\varepsilon^3$。标准正态的奇数阶矩为 0，二、四、六阶矩分别是 1、3、15，所以 $E[T]=2$，$E[T^2]=4+12+\tfrac{15}4+6=\tfrac{103}4$，方差 $\tfrac{103}4-4=21.75$。

在这个例子里，重参数化的方差小得多，差了 20 多倍。这就是需要把采样出的词当离散动作、对期望奖励求梯度时（如 M.15）用对数导数，而 VAE 的连续隐变量常用重参数化的原因。两种估计的方差大小取决于函数和分布，不能保证总是同一种更小。

合上书，说明为什么"把梯度符号挪进期望"在 $q_\phi$ 里直接做不成，以及重参数化把随机性放到了哪里。

梯度现在能穿过抽样了。下一节把编码器、重参数化和解码器接成一个整体，看它的损失是什么形状。

### 6. VAE 的损失为什么是"重建误差 + KL"？

现在把零件合起来。编码器网络 $\boldsymbol x\mapsto(\boldsymbol\mu_\phi,\log\boldsymbol\sigma^2_\phi)$ 给出 $q_\phi(\boldsymbol z\mid\boldsymbol x)$，解码器 $g_\theta$ 给出 $p_\theta(\boldsymbol x\mid\boldsymbol z)$。对一张图 $\boldsymbol x$，要最大化第 3 节的 ELBO，也就是最小化 $-\mathrm{ELBO}$。两项分别处理。以下固定观测方差 $\sigma_x^2>0$，不把它当作待优化的参数。$\lVert\boldsymbol a\rVert$ 表示向量的长度（有的书写作 $|\boldsymbol a|$，用双竖线是为了和数的绝对值区分）。

**重建项。** 解码器是 $N(g_\theta(\boldsymbol z),\sigma_x^2I)$，取对数：

$$\log p_\theta(\boldsymbol x\mid\boldsymbol z)=-\frac{\lVert\boldsymbol x-g_\theta(\boldsymbol z)\rVert^2}{2\sigma_x^2}-\frac{d_x}2\log(2\pi\sigma_x^2).$$

后一项与 $\theta,\phi$ 无关。这是 M.2.1 的老结论：高斯噪声下的最大似然就是均方误差。期望用一次重参数化抽样近似（训练的每一步抽一次，许多步平均下来逼近期望，和 M.1.6 的随机梯度是同一个道理）：抽 $\boldsymbol\varepsilon$，令 $\boldsymbol z=\boldsymbol\mu+\boldsymbol\sigma\odot\boldsymbol\varepsilon$，重建误差就是 $\lVert\boldsymbol x-g_\theta(\boldsymbol z)\rVert^2/(2\sigma_x^2)$（省去的常数项见下）。

**先验项。** $q_\phi$ 和先验 $N(0,I)$ 都是对角高斯。先算一维。设 $q=N(\mu,\sigma^2)$，$p=N(0,1)$：

$$\mathrm{KL}(q\Vert p)=E_q\!\left[\log q(z)-\log p(z)\right]=E_q\!\left[-\tfrac12\log(2\pi\sigma^2)-\frac{(z-\mu)^2}{2\sigma^2}+\tfrac12\log(2\pi)+\frac{z^2}{2}\right].$$

逐项取期望：$E_q[(z-\mu)^2]=\sigma^2$，所以第二项是 $-\frac12$；$E_q[z^2]=\mu^2+\sigma^2$，所以最后一项是 $\frac12(\mu^2+\sigma^2)$。第一项和第三项的常数部分合起来，是 $-\frac12\log\sigma^2$。合并：

$$\mathrm{KL}\big(N(\mu,\sigma^2)\,\Vert\,N(0,1)\big)=\tfrac12\big(\mu^2+\sigma^2-1-\log\sigma^2\big).$$

多维时，两个分布的每个分量独立，对数比是各分量之和，期望的和等于和的期望，所以 KL 就是各分量相加：

$$\mathrm{KL}=\frac12\sum_{j=1}^{d_z}\big(\mu_j^2+\sigma_j^2-1-\log\sigma_j^2\big).$$

核对：$\mu=0,\sigma=1$ 时每项为 $0$，$q$ 与先验相同；这个式子每项 $\ge0$（因为 $\sigma^2-1-\log\sigma^2\ge0$，即 $\ln t\le t-1$），与 KL 非负一致。

两项合起来。对一个观测样本，用一次噪声抽样估计重建期望，并省去固定的常数，得到这次训练使用的损失 $\widehat L$：

$$\widehat L(\theta,\phi;\boldsymbol x,\boldsymbol\varepsilon)=\underbrace{\frac{\lVert\boldsymbol x-g_\theta(\boldsymbol\mu+\boldsymbol\sigma\odot\boldsymbol\varepsilon)\rVert^2}{2\sigma_x^2}}_{\text{重建误差}}+\underbrace{\tfrac12\sum_j(\mu_j^2+\sigma_j^2-1-\log\sigma_j^2)}_{\text{KL}} .$$

这就是 VAE。对 $\boldsymbol\varepsilon$ 取期望再加回常数，正是完整的负 ELBO：

$$E_{\boldsymbol\varepsilon}\big[\widehat L\big]+\frac{d_x}2\log(2\pi\sigma_x^2)=-\mathrm{ELBO}.$$

单次损失和它的梯度会偏离这个期望值，训练利用的是反复抽样后的平均效果。$\sigma_x^2$ 是两项之间的调节旋钮：它越小，重建项权重越大。对 $\theta$ 和 $\phi$ 同时用梯度下降（也可以用 M.1 的 Adam）训练，$\phi$ 的梯度靠第 5 节的重参数化穿过抽样。

**方法 6（VAE 的单样本损失）**

1. 编码器给出 $\boldsymbol\mu,\boldsymbol\sigma$。
2. 抽 $\boldsymbol\varepsilon$，令 $\boldsymbol z=\boldsymbol\mu+\boldsymbol\sigma\odot\boldsymbol\varepsilon$。
3. 解码器给出 $g(\boldsymbol z)$，算重建误差。
4. 用闭式公式算 KL，两项相加，得到这一次抽样的损失。

**例 6**　先单独练 VAE 损失里的 KL，暂不含解码器。取老朋友⑥，也就是例 5 的同一个 $q=N(1,0.5^2)$，先验 $N(0,1)$，求 KL；再求二维情形 $\boldsymbol\mu=(1,0)$，$\boldsymbol\sigma=(0.5,2)$ 的 KL。

一维：$\mu=1,\sigma^2=0.25$，$\log\sigma^2=-1.3863$。

$$\mathrm{KL}=\tfrac12(1+0.25-1+1.3863)=\tfrac12(1.6363)\approx0.8181 .$$

二维按分量相加：第一个分量就是上面的 0.8181；第二个分量 $\mu=0$，$\sigma^2=4$，$\tfrac12(0+4-1-1.3863)=0.8069$。合计 $1.625$。

注意第二个分量方差比先验大，同样会被罚，只是罚的方式不同：方差太大由 $\sigma^2$ 项罚，太小由 $-\log\sigma^2$ 项罚。KL 惩罚的是"和先验不同"，不是"方差小"。

> 求 $q=N(2,1)$ 与先验 $N(0,1)$ 的 KL。
>
> 答案：$\tfrac12(4+1-1-0)=2$。

**例 7**　把例 5 的抽样 $\varepsilon=0.8$、例 6 的 KL 接上一个解码器，就是一步完整的训练，只是把 $f(z)=z^2$ 换成了真正的重建误差。一个玩具 VAE，数据 $x$ 是一维的，$z$ 也是一维的，解码器 $g(z)=2z$，$\sigma_x^2=1$。训练样本 $x=3$，编码器给出 $\mu=1$，$\sigma=0.5$（就是例 6 的 $q$），抽到 $\varepsilon=0.8$。求这一步的损失，以及损失对 $\mu,\sigma$ 的梯度。

第一步，抽样：$z=1+0.5\times0.8=1.4$。

第二步，解码并算重建误差：$g(z)=2.8$，重建误差 $\tfrac12(3-2.8)^2=0.02$。

第三步，KL 取例 6 的 $0.8181$。总损失 $L=0.02+0.8181=0.8381$。

第四步，梯度。重建项通过 $z$ 回传，$\partial z/\partial\mu=1$，$\partial z/\partial\sigma=\varepsilon$（第 5 节），且 $\partial(\text{重建})/\partial z=(g(z)-x)g'(z)=(2.8-3)\times2=-0.4$。KL 为 $\frac12(\mu^2+\sigma^2-1-2\log\sigma)$，对 $\mu$ 的偏导是 $\mu=1$，对 $\sigma$ 的偏导是 $\sigma-1/\sigma=-1.5$。

$$\frac{\partial L}{\partial\mu}=-0.4+1=0.6,\qquad\frac{\partial L}{\partial\sigma}=-0.4\times0.8-1.5=-1.82 .$$

读法：梯度下降走负梯度方向。重建项想把 $\mu$ 调大（让 $2z$ 更接近 3），对应梯度 $-0.4$；KL 项想把它拉回 0，对应梯度 $+1$；合起来 $\partial L/\partial\mu=0.6>0$，所以 $\mu$ 这一步会变小。$\sigma$ 的梯度为负，所以 $\sigma$ 会变大，主要因为 KL 想让 $\sigma$ 靠近 1。

> 同一个模型，同一个 $x=3$、$\mu=1$、$\sigma=0.5$，但抽到 $\varepsilon=-0.4$，求这一步的损失和对 $\mu,\sigma$ 的梯度。
>
> 答案：$z=0.8$，$g(z)=1.6$，重建误差 $\frac12(3-1.6)^2=0.98$，加上 KL $0.8181$，损失 $\approx1.7981$。重建项对 $z$ 的偏导是 $(1.6-3)\times2=-2.8$，所以 $\partial L/\partial\mu=-2.8+1=-1.8$，$\partial L/\partial\sigma=-2.8\times(-0.4)-1.5=-0.38$。

回到章首的问题：自编码器不知道该往解码器里送什么。现在有了答案。训练好以后生成新图，不再用编码器：先从 $N(0,I)$ 抽 $\boldsymbol z$，再由解码器给出均值 $g_\theta(\boldsymbol z)$。若严格按本章的高斯模型抽样，还要独立抽 $\boldsymbol\xi\sim N(\boldsymbol 0,I_{d_x})$，令 $\boldsymbol x=g_\theta(\boldsymbol z)+\sigma_x\boldsymbol\xi$；直接显示均值也可以，但与完整抽样不同。KL 项鼓励每张图的 $q$ 接近标准正态，有助于缩小训练时的 $\boldsymbol z$ 与生成时从先验抽的 $\boldsymbol z$ 之间的差异，这是自编码器没有的约束，但并不保证每个先验样本都能生成好图。

合上书，写出 VAE 的单样本损失，并说明两项各来自 ELBO 的哪一部分。

![VAE 的一次前向：编码器给出 $\boldsymbol\mu,\boldsymbol\sigma$，噪声 $\boldsymbol\varepsilon$（方框）从旁边进入，$\boldsymbol z=\boldsymbol\mu+\boldsymbol\sigma\odot\boldsymbol\varepsilon$ 是确定的运算，编码器给出均值与标准差，固定噪声后由 $\boldsymbol z=\boldsymbol\mu+\boldsymbol\sigma\odot\boldsymbol\varepsilon$ 送入解码器。重建项沿下排粗实线回传，KL 项另有直接通向均值和标准差的支路（点线），两部分相加后更新编码器；虚线连接 KL 项与重建误差各自比较的两端](fig/M16-n4.pdf){width=85%}

### 7. 不写出似然，能不能直接让生成的图以假乱真？

VAE 要写出 $p_\theta(\boldsymbol x\mid\boldsymbol z)$ 的形式，采用高斯解码器时训练的是平均意义下的平方误差，生成的图常常偏平滑。GAN 绕开似然：生成器 $G$ 直接把噪声 $\boldsymbol z\sim N(0,I)$ 变成图 $G(\boldsymbol z)$，它的输出分布记作 $p_g$（它是一个确定的分布，但我们算不出 $p_g(\boldsymbol x)$ 的值，只能从中抽样；下一节是数学推导，把 $p_g$ 当作有密度的分布来写积分，训练时并不去算这个密度，只用样本和 $D$ 的输出）。再请一个判别器 $D$ 当裁判，$D(\boldsymbol x)\in(0,1)$ 是它认为 $\boldsymbol x$ 是真图的概率。

判别器做的是二分类（M.2.4）：真图标签 1，生成的图标签 0。二元交叉熵的相反数是

$$V(D,G)=E_{\boldsymbol x\sim p_{\text{data}}}\big[\log D(\boldsymbol x)\big]+E_{\boldsymbol z}\big[\log\big(1-D(G(\boldsymbol z))\big)\big].$$

判别器想让 $V$ 尽量大，因为这等于分类得准。生成器想骗过判别器，所以想让 $V$ 尽量小，只有第二项含 $G$。合起来是一个极小极大问题：

$$\min_G\max_D V(D,G).$$

训练时两个网络交替做梯度步：先固定 $G$，用真图和生成图更新 $D$；再固定 $D$，更新 $G$ 让 $D$ 判错。各自的损失就是上面 $V$ 的相应部分，合写起来是一个极小极大目标。

生成器这一步有个常用的小改动。设 $D=\sigma(s)$（这里 $\sigma$ 是 sigmoid 函数，与编码器的标准差无关），$s$ 是判别器的分数。训练刚开始 $G$ 很差，$D(G(z))\approx0$，目标 $\log(1-\sigma(s))$ 对 $s$ 的导数是 $-\sigma(s)\approx0$，生成器几乎收不到信号。改成最小化 $-\log D(G(z))$，导数是 $-(1-\sigma(s))\approx-1$，信号很强。两种写法的理想终点都是 $p_g=p_{\text{data}}$，原论文也建议用后一种；改用它以后，损失就不再能直接写成下一节的 JS 等式。

两个网络的目标相反，这和前面所有"一个网络、一个损失"的训练都不一样。GAN 的难处也来自这里，第 9 节再说。

合上书，从二分类交叉熵写出 GAN 的极小极大目标，并说明生成器为什么改用 $-\log D(G(z))$。

这个极小极大目标到底在让 $p_g$ 靠近 $p_{\text{data}}$ 的什么量？VAE 有 ELBO 可以说清，GAN 没写似然，要先看判别器练到最好的情形。

### 8. 判别器练到最好时，生成器实际在优化什么？

固定 $G$，也就是固定 $p_g$。下面先在两个分布都有密度的情形下推导（只有有限个点时，把积分换成求和）；$p_{\text{data}}$ 表示真实数据的分布。计算的是不受网络形式限制的理想判别器，允许它在每个位置自由取值；实际的判别器只能逼近它。把 $V$ 的两个期望都写成对 $\boldsymbol x$ 的积分（第二项把 $G(\boldsymbol z)$ 的分布换成 $p_g$）：

$$V(D,G)=\int\Big[p_{\text{data}}(\boldsymbol x)\log D(\boldsymbol x)+p_g(\boldsymbol x)\log\big(1-D(\boldsymbol x)\big)\Big]\mathrm d\boldsymbol x .$$

最大化它，只要对每个 $\boldsymbol x$ 单独最大化被积函数：$D$ 在不同的 $\boldsymbol x$ 上可以独立取值，积分又是各点被积函数的累加，每个点上取最大，累加起来就最大。记 $a=p_{\text{data}}(\boldsymbol x)$，$b=p_g(\boldsymbol x)$，$y=D(\boldsymbol x)$，问题是 $a\log y+b\log(1-y)$ 在 $y\in[0,1]$ 上的最大值。先看 $a,b>0$ 的情形。

求导：$\frac ay-\frac b{1-y}=0$，解得 $y=\frac a{a+b}$。二阶导数 $-\frac a{y^2}-\frac b{(1-y)^2}<0$，所以这是最大点：

$$D^*(\boldsymbol x)=\frac{p_{\text{data}}(\boldsymbol x)}{p_{\text{data}}(\boldsymbol x)+p_g(\boldsymbol x)} .$$

直观上这很合理：某张图在真图里出现得多、在假图里出现得少，裁判就更相信它是真的。边界情形：$a>0,b=0$ 时最优输出为 1，$a=0,b>0$ 时为 0，两者都为 0 的位置不影响目标。上面的公式只在分母 $a+b>0$ 的位置使用。

把 $D^*$ 代回，看生成器此时面对的目标。$1-D^*=\frac{p_g}{p_{\text{data}}+p_g}$。引入混合分布 $m=\tfrac12(p_{\text{data}}+p_g)$，则 $p_{\text{data}}+p_g=2m$：

$$V(D^*,G)=E_{p_{\text{data}}}\Big[\log\frac{p_{\text{data}}}{2m}\Big]+E_{p_g}\Big[\log\frac{p_g}{2m}\Big]=\mathrm{KL}(p_{\text{data}}\Vert m)+\mathrm{KL}(p_g\Vert m)-2\log2 .$$

两个 $\log\frac12$ 提出来各是 $-\log2$。定义 **JS 散度**（Jensen–Shannon）：

$$\mathrm{JS}(p\Vert q)=\tfrac12\mathrm{KL}(p\Vert m)+\tfrac12\mathrm{KL}(q\Vert m),\qquad m=\tfrac12(p+q).$$

合起来就是

$$\boxed{\ V(D^*,G)=2\,\mathrm{JS}(p_{\text{data}}\Vert p_g)-\log4\ }.$$

JS 有三条性质：对称（KL 不对称）；$\mathrm{JS}\ge0$，只在 $p=q$ 时为 0（两项 KL 都非负，和为零就要求两项都为零，所以 $p=m=q$，P.14.4）；上界 $\log2$（因为 $m\ge p/2$，所以 $\mathrm{KL}(p\Vert m)=E_p[\log\frac pm]\le\log2$，$q$ 同理）。上界在两个分布的支撑（密度大于 0 的地方）不重叠时取到：此时 $m$ 在 $p$ 的支撑上恰是 $p/2$，$\mathrm{KL}(p\Vert m)=\log2$，$q$ 同理，所以 $\mathrm{JS}=\log2$。

所以在判别器每次都达到理想最优时，第 7 节最初写出的极小极大目标，对生成器就是在最小化 $p_{\text{data}}$ 与 $p_g$ 的 JS 散度，最优点是 $p_g=p_{\text{data}}$：两个分布相同时，在密度为正的位置 $D^*=\frac12$（裁判只能瞎猜），$V=-\log4$。这回答了开头的问题。若生成器改用 $-\log D(G(z))$，损失就不能直接写成这个 JS 公式。

**方法 7（最优判别器与 JS）**

1. 对每个分母大于零的 $\boldsymbol x$，$D^*=p_{\text{data}}/(p_{\text{data}}+p_g)$。
2. 代回得 $V^*=\mathrm{KL}(p_{\text{data}}\Vert m)+\mathrm{KL}(p_g\Vert m)-2\log2=2\mathrm{JS}-\log4$。
3. 真假完全一样时 $D^*\equiv\frac12$，$V^*=-\log4\approx-1.3863$。

**例 8**　从这里转到 GAN。为了能手算，把空间缩小到两个点。给定两点空间上的概率向量 $p=(0.6,0.4)$ 与 $q=(0.2,0.8)$，令 $F(y_1,y_2)=\sum_{i=1}^{2}\big[p_i\log y_i+q_i\log(1-y_i)\big]$，$0<y_1,y_2<1$。求最大点 $y^*$ 和最大值，并验证最大值等于 $2\mathrm{JS}(p\Vert q)-\log4$（这里 $p$ 是 $p_{\text{data}}$，$q$ 是 $p_g$，$y$ 是判别器在两点上的取值）。

最大点：每个 $y_i$ 单独最大化，$y_1^*=\frac{0.6}{0.8}=0.75$，$y_2^*=\frac{0.4}{1.2}=\frac13$。

最大值把两点的项相加：

$$F^*=0.6\log0.75+0.2\log0.25+0.4\log\tfrac13+0.8\log\tfrac23\approx-1.2137 .$$

验证：$m=(0.4,0.6)$，$\mathrm{KL}(p_{\text{data}}\Vert m)=0.6\log\frac{0.6}{0.4}+0.4\log\frac{0.4}{0.6}=0.0811$，$\mathrm{KL}(p_g\Vert m)=0.2\log\frac{0.2}{0.4}+0.8\log\frac{0.8}{0.6}=0.0915$，$\mathrm{JS}=\tfrac12(0.0811+0.0915)=0.0863$，$2\mathrm{JS}-\log4=0.1726-1.3863=-1.2137$，一致。

作为对照，取 $y_1=y_2=\frac12$，则 $F=2\log\frac12=-\log4\approx-1.3863$，比最大值小，说明 $y^*$ 确实让 $F$ 更大。

> 设 $p=(0.5,0.5)$，$q=(0.25,0.75)$，求 $y^*$ 和最大值 $F^*$。
>
> 答案：$y^*=(\frac23,\ 0.4)$，$F^*=0.5\log\frac23+0.25\log\frac13+0.5\log0.4+0.75\log0.6\approx-1.3187$，比 $-\log4$ 高 $0.0676$，也就是 $2\mathrm{JS}$（$\mathrm{JS}\approx0.0338$）。

![一维情形：真图分布（实线）、生成图分布（虚线）和最优判别器 $D^*$（点线，对应右侧纵轴）。$D^*$ 在真图多、假图少的地方接近 1，在假图多的地方接近 0，两条曲线相交处等于 $\tfrac12$](fig/M16-n5.pdf){width=70%}

合上书，推出最优判别器 $D^*$，写出代回后与 JS 散度的关系。

这个结论假定判别器每次都练到最优、$p_g$ 有密度，实际训练能不能做到，是下一节的问题。

### 9. GAN 为什么常常只会画几种样子？

这一节可以单独读，不读不影响全章结论。第 8 节的结论看上去很漂亮，实际训练却常出三种毛病。

第一种叫**模式坍塌**：真图有好几类（模式），生成器只画其中一两类。原因在于生成器只需要骗过**当前**的判别器，不需要覆盖全部真图。

用例 8 的两点空间看一下。设真图是 $a,b$ 各一半，生成器把全部概率放在 $a$ 上：$p_g=(1,0)$。这时 $m=(0.75,0.25)$，

$$\mathrm{JS}=\tfrac12\Big[0.5\log\tfrac{0.5}{0.75}+0.5\log\tfrac{0.5}{0.25}\Big]+\tfrac12\log\tfrac1{0.75}\approx0.2158 .$$

这个值远小于上界 $\log2\approx0.6931$：有限的 JS 值仍可能对应缺了一个模式，要判断是否覆盖了全部模式，还得看生成概率怎样分配。此时最优判别器 $D^*(a)=\frac{0.5}{1.5}=\frac13$，$D^*(b)=1$（$b$ 处 $p_g=0$，属于上面的边界情形）：它认为 $a$ 大多是假的，但 $b$ 完全是真的。若生成器每次把全部概率转移到当前判别器更相信的位置，就会在 $a$ 和 $b$ 之间来回跳。这依赖具体的更新方式，不能由 $D^*$ 的两个数值断定；允许逐步调整两点的概率时，目标仍在 $p_g=(\tfrac12,\tfrac12)$ 处最小。

第二种是**训练不稳定**。极小极大问题不是求一个函数的最小值，两个网络各自沿梯度走，可能绕圈而不收敛。先猜：下面这个最简单的对抗问题，两个变量各自朝对自己有利的方向走，会不会收敛到平衡点？$\min_x\max_y\,xy$ 的平衡点（鞍点）是 $(0,0)$，注意 $y$ 能取任意实数时内层的最大值对 $x\neq0$ 是无穷，不存在有限的"最优值"。同时更新 $x\leftarrow x-\eta y$，$y\leftarrow y+\eta x$（两式右边都用旧值），从 $(1,0)$ 出发，$\eta=0.1$：一步后 $(1,0.1)$，距离平方从 1 变成 $1.01$；每一步距离平方乘以 $1+\eta^2$，越转越远，猜"会收敛"是错的。真实 GAN 的两个网络也有类似的相互追逐。

第三种是**梯度消失**，来自第 8 节的上界：如果在参数的一段变化范围内，真图与假图取正值的位置始终不重叠，这段范围内 JS 恒等于 $\log2$，理想目标不能提供变好的方向。这是这种目标可能遇到的困难，并不意味着实际训练里的真假分布都不重叠。

这些毛病催生了后面的很多改进（比如换成别的距离），也让人转向另一条路：不对抗，而是一步一步地加噪去噪，也就是下一章的扩散模型。

**例 9**　和例 8 相比，把 $p$ 换成 $(\tfrac12,\tfrac12)$ 以便手算，并把生成分布在第二个位置的概率设为 0，这正是第 8 节说的边界情形。取 $p=(\tfrac12,\tfrac12)$，$q=(1,0)$，求 JS 散度，并求 $F(y_1,y_2)=\tfrac12\log y_1+\log(1-y_1)+\tfrac12\log y_2$ 在 $0<y_1<1$，$0<y_2\le1$ 上的最大点和最大值（第二个位置里 $q_2=0$，所以没有 $\log(1-y_2)$ 项）。

$y_1^*=\frac{1/2}{3/2}=\frac13$。第二项只有 $\tfrac12\log y_2$，$y_2$ 越大越好，在边界取 $y_2^*=1$。所以最大点是 $y^*=(\tfrac13,1)$。

最大值 $F^*=\tfrac12\log\tfrac13+\log\tfrac23+0\approx-0.9548$，与上面的 JS 一致：$2\times0.2158-1.3863\approx-0.9548$。

对照完全拟合的 $-1.3863$，这里高约 0.4315。

合上书，说明模式坍塌的原因，并举出梯度步会绕圈的最小例子。

### 本章小结

| 方法 | 什么时候用 | 对应题号 |
|---|---|---|
| 方法 1（隐变量模型的边缘与后验） | 写联合、算 $p(x)$、算后验 | M16-01、M16-12 |
| 方法 2（Jensen 放缩） | 对数套着期望，要把对数挪进期望，得到 $E[\log X]$ | M16-02 |
| 方法 3（ELBO 的拆分与差距） | 算 ELBO；求 $q$ 与真实后验的 KL | M16-03、M16-06、M16-11 |
| 方法 4（EM 的一轮） | 混合模型的参数估计 | M16-07、M16-11 |
| 方法 5（重参数化求梯度） | 梯度要穿过 $z\sim q_\phi$ 的抽样 | M16-05、M16-08、M16-10 |
| 方法 6（VAE 的单样本损失） | 算 VAE 的损失和梯度；算对角高斯的 KL | M16-04、M16-10、M16-12 |
| 方法 7（最优判别器与 JS） | GAN 的目标、$D^*$、$V^*$、JS 散度 | M16-09 |

章首提出的两个问题都有了回答。VAE 靠 KL 项让编码贴近标准正态，所以从 $N(0,I)$ 抽 $\boldsymbol z$ 送进解码器就可以按这个流程生成（不保证每个先验样本都好）；GAN 不写似然，在判别器最优时目标等于 $2\mathrm{JS}-\log4$，它的毛病也由此而来。

在主线的三件套上，本章把「损失从概率来」接到了隐变量模型：模型 $f$ 变成「编码器 + 解码器」或「生成器 + 判别器」，损失是负 ELBO（或极小极大目标），更新规则仍是梯度下降，新的难点，VAE 是梯度怎样穿过随机抽样，GAN 是两个网络的对抗。损失与概率假设的表在本章新增最后一行：

| 损失或做法 | 背后的概率假设 | 出现章 |
|---|---|---|
| 均方误差 | 噪声是高斯分布 | M.2 |
| 交叉熵（二分类） | 标签服从伯努利分布 | M.2 |
| L2、L1 正则 | 参数的先验是高斯、拉普拉斯分布 | M.3 |
| 语言模型的交叉熵 | 下一个词服从类别分布 | M.10 |
| 奖励减 KL | 偏好服从 Bradley–Terry 模型 | M.15 |
| **ELBO（本章新增）** | 隐变量模型的对数似然下界 | M.16 |

