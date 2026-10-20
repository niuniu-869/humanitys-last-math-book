## M.17 · 扩散模型的前向过程：高斯噪声的叠加与闭式解

今天的文生图和视频生成工具，比如 Stable Diffusion、Midjourney，核心都是扩散模型。它的想法很朴素：一张清晰的图，每次只加一点点噪声，加上千次以后就变成一团没有内容的噪点；反过来，如果能学会"把噪点去掉一点点"这一步，从一团纯噪声出发，一步步去噪，就能得到一张新图。这里有两件事要弄清：加噪这一半能不能用一个公式直接算出来，去噪这一步到底要学什么。

M.16 里的 VAE 和 GAN 都想一步到位：从噪声直接变出图。VAE 的解码器负担太重，图偏模糊；GAN 画质好，训练却不稳定。2015 年，Sohl-Dickstein 等人提出把这一步拆成很多小步：前向每步加一点高斯噪声，反向学着每步去掉一点。这条路当时没有引起太多注意，直到 2020 年，Ho、Jain 与 Abbeel 的 DDPM 把训练目标化简成"预测加进去的噪声"，图像质量才追上了 GAN。

这件事和上一章是同一个框架。把整条链 $\boldsymbol x_1,\dots,\boldsymbol x_T$ 看成隐变量，加噪这一半（编码器）是固定的，不用学，只有去噪这一半（解码器）有参数。训练目标出自 M.16.3 的 ELBO：ELBO 拆成逐步的 KL 项和一个重建项，每个 KL 项可以化成预测噪声的均方误差，去掉 KL 项的系数并把重建项单独处理，得到一个简单的均方误差（第 7 节推导）。按全书的三件套（模型、损失、更新规则）来填：$f$ 是预测噪声的网络 $\varepsilon_\theta(\boldsymbol x_t,t)$，$L$ 是预测噪声的均方误差，更新规则是 Adam。本章在损失表里新增：预测噪声的均方误差，对应的概率假设是"前向过程是高斯分布"。

本章主要讲前向，也就是怎样加噪，以及最后得到的那个很好用的公式。前向只需要正态分布、线性变换和方差，用到的都是 P.4–P.7（第 5 节的终点估计还用 C.8 的对数不等式）。第 1 节说清整体框架；第 2 节看单步加噪；第 3 节学两份独立高斯噪声怎么合成一份；第 4 节由它得到"一步跳到第 $t$ 步"的闭式解；第 5 节看噪声表怎么定、为什么最后是纯噪声；第 6 节得到训练目标；第 7、8 节讲反向一步的分布（并接回 ELBO）和生成时的采样。

### 1. 怎样从一团噪声里"变"出一张图？

先看一个像素。设它的值是 $x_0=2$（图 1 里为了画出两个峰，假设 $x_0$ 取 $\pm2$ 两个值；例 1 只走 $x_0=2$ 这一条路径），每一步让它缩小一点点，再加一点高斯噪声。第 2 节的例 1 会具体算出，三步以后它依次变成 $2.06,\ 1.63,\ 1.61$，在 2 附近晃动，每步只变一点。一张图有几十万个像素，每个都这样处理，上千步以后，每个像素都被噪声淹没。整个流程可以画出来：设 $\boldsymbol x_0$ 是一张真图，$T$ 是总步数（常取 1000）。

**前向过程**（加噪，固定，不含参数）：从 $\boldsymbol x_0$ 出发，每一步在上一步的结果上加一点高斯噪声，得到 $\boldsymbol x_1,\boldsymbol x_2,\dots,\boldsymbol x_T$。每一步只依赖前一步，所以是一条链。到 $\boldsymbol x_T$ 时，图里的信息基本被噪声淹没，在常用的噪声表下（第 5 节给出条件 $\bar\alpha_T\approx0$），它的分布近似标准正态 $N(\boldsymbol 0,I)$（$I$ 是单位矩阵）。

**反向过程**（去噪，要学）：从 $\boldsymbol x_T\sim N(\boldsymbol 0,I)$（$\bar\alpha_T\approx0$ 时的近似）开始，一个网络每一步根据 $\boldsymbol x_t$ 给出 $\boldsymbol x_{t-1}$ 应有的分布，一步步走回 $\boldsymbol x_0$。

为什么要拆成这么多小步？VAE 的解码器要一步从纯噪声变出整张图，负担太重。拆成小步以后，每步只需要从 $\boldsymbol x_t$ 退回 $\boldsymbol x_{t-1}$，而退得很短时，这个反向的条件分布近似是高斯分布，理由如下。

由贝叶斯公式，$q(\boldsymbol x_{t-1}\mid\boldsymbol x_t)\propto q(\boldsymbol x_t\mid\boldsymbol x_{t-1})\,q(\boldsymbol x_{t-1})$。第一个因子把 $\boldsymbol x_t$ 固定，看成 $\boldsymbol x_{t-1}$ 的函数，是一个很窄的高斯，宽度只有 $\sqrt{\beta_t}$ 的量级；在这么窄的范围里，第二个因子（数据在第 $t-1$ 步的分布）几乎不变，窄高斯乘上一个变化很慢的因子，仍然近似是高斯（第 7 节会看到两个高斯相乘的精确规则）。这是近似，不是恒等式，每步越小越准。反过来，如果一步退得很远，反向分布就是数据分布本身，比如图 1 里 $x_0$ 取 $\pm2$ 两个值时有两个峰（本节后面的图），不再是高斯。所以网络只需要学这个高斯的均值，难度小得多。

要分清两个分布：这里的 $q(\boldsymbol x_{t-1}\mid\boldsymbol x_t)$ 不含 $\boldsymbol x_0$，是生成时真正需要的；第 7 节算的 $q(\boldsymbol x_{t-1}\mid\boldsymbol x_t,\boldsymbol x_0)$ 要已知 $\boldsymbol x_0$，只在训练时可算，是网络去逼近的参照。

两章的对应关系如下：

| | VAE（M.16） | 扩散模型 |
|---|---|---|
| 隐变量 | 一个 $\boldsymbol z$ | 一串 $\boldsymbol x_1,\dots,\boldsymbol x_T$ |
| 编码器 $q$ | 网络给出 $N(\boldsymbol\mu,\boldsymbol\sigma^2)$，要学 | 固定的加噪，不用学 |
| 解码器 | 一步，$p_\theta(\boldsymbol x\mid\boldsymbol z)$ | $T$ 步，$p_\theta(\boldsymbol x_{t-1}\mid\boldsymbol x_t)$ |
| 训练目标 | ELBO | 同一个 ELBO，化简后是均方误差 |

图像 $\boldsymbol x_0\in\mathbb R^{H\times W\times C}$（高、宽、通道数）有几十万个分量，噪声对每个分量独立地加，所以下面的推导先在一个分量（一个数）上做，结论对整张图逐分量成立，最后再把标量换成"每个分量各自一份"。

![一维数据在逐步加噪中的变化：每格是一个时刻 $t$ 的 $\boldsymbol x_t$ 的密度。$t=0$ 时箭头表示 $x=\pm2$ 处的点质量，$t>0$ 的实线是当前密度，随 $t$ 增大两峰变宽、靠近，$t=30$ 已接近 $N(0,1)$（点线作参照），继续增大趋于它](fig/M17-n1.pdf){width=95%}

框架有了，可是还没有一个能动手算的东西：加噪这一半具体怎么写？下一节从最小的一步开始。

合上书，说出前向过程和反向过程各自要不要学参数，以及为什么拆成小步比一步到位容易。

### 2. 加一步噪声，数据的分布怎么变？

单步加噪取这样的形式，其中 $\beta_t\in(0,1)$ 是第 $t$ 步的噪声强度（一个很小的数），$\varepsilon_t\sim N(\boldsymbol 0,I)$：

$$\boldsymbol x_t=\sqrt{1-\beta_t}\,\boldsymbol x_{t-1}+\sqrt{\beta_t}\,\varepsilon_t .$$

读法：先把上一步的值乘 $\sqrt{1-\beta_t}$ 缩小一点，再加上 $\sqrt{\beta_t}$ 倍的标准正态噪声。以后写 $\alpha_t=1-\beta_t$，式子就是 $\boldsymbol x_t=\sqrt{\alpha_t}\boldsymbol x_{t-1}+\sqrt{1-\alpha_t}\,\varepsilon_t$。

已知 $\boldsymbol x_{t-1}$ 时，$\boldsymbol x_t$ 是 $\varepsilon_t$ 的线性函数。由 P.5.3，正态的线性变换仍是正态，均值是 $\sqrt{\alpha_t}\boldsymbol x_{t-1}$，方差是 $\beta_t$（噪声乘以 $\sqrt{\beta_t}$，方差乘以 $\beta_t$）：

$$q(\boldsymbol x_t\mid\boldsymbol x_{t-1})=N\big(\sqrt{1-\beta_t}\,\boldsymbol x_{t-1},\ \beta_tI\big).$$

**方法 1（单步加噪）**

1. 抽 $\varepsilon_t\sim N(0,1)$（整张图逐分量各抽一个）。
2. $x_t=\sqrt{1-\beta_t}\,x_{t-1}+\sqrt{\beta_t}\,\varepsilon_t$。
3. 条件分布 $N(\sqrt{1-\beta_t}\,x_{t-1},\beta_t)$。

$I$ 表示相应维数的单位矩阵，$\propto$ 读作"正比于"，$\lVert\cdot\rVert$ 表示向量的长度。

**例 1**　沿用前面的设定：$\beta_t=0.1$ 不变，$x_0=2$（就是第 1 节开头的那个像素）。设三步抽到的噪声是 $\varepsilon_1=0.5$，$\varepsilon_2=-1.0$，$\varepsilon_3=0.2$，写出 $x_1,x_2,x_3$。

$\sqrt{1-\beta}=\sqrt{0.9}\approx0.9487$，$\sqrt\beta=\sqrt{0.1}\approx0.3162$。

$$x_1=0.9487\times2+0.3162\times0.5\approx2.0555,\qquad x_2=0.9487\times2.0555+0.3162\times(-1.0)\approx1.6338,$$

$$x_3=0.9487\times1.6338+0.3162\times0.2\approx1.6132 .$$

数值在 2 附近晃动，每步变一点。这是一条具体的路径；换一组 $\varepsilon$ 会得到另一条。

> 同样的 $\beta=0.1$，$x_0=-1$，$\varepsilon_1=1$，求 $x_1$ 的值和 $x_1$ 的分布。
>
> 答案：$x_1=-0.9487+0.3162=-0.6325$；分布 $N(-0.9487,0.1)$。

为什么要先缩小再加噪，而不是直接 $x_t=x_{t-1}+\sqrt{\beta_t}\varepsilon_t$？看方差。设 $x_{t-1}$ 均值为 0、方差为 $s$，与新噪声独立，则

$$\mathrm{Var}(x_t)=(\sqrt{1-\beta_t})^2s+(\sqrt{\beta_t})^2=(1-\beta_t)s+\beta_t .$$

独立变量的方差相加（P.7）。这个式子有一个不动点 $s=1$：如果 $s=1$，则 $\mathrm{Var}(x_t)=1-\beta_t+\beta_t=1$，方差不变。而不缩小的话，方差是 $s+\beta_t$，每步增加，几百步以后越来越大，网络的输入尺度也在不断变化。先缩再加，是为了把方差拉向 1 并保持在 1 附近，让整条链的数值保持在同一量级。

**例 2**　仍用单步公式，这次不关心具体抽到什么噪声，只看方差怎样变。设 $x_{t-1}$ 均值 0、方差 4，$\beta_t=0.1$，求 $x_t$ 的方差；若不缩小，方差是多少？

按 $\mathrm{Var}(x_t)=(1-\beta_t)s+\beta_t$：$0.9\times4+0.1=3.7$，比 4 更接近 1。不缩小则是 $4+0.1=4.1$，离 1 更远。

> $s=0.25$，$\beta_t=0.1$，求 $\mathrm{Var}(x_t)$。
>
> 答案：$0.9\times0.25+0.1=0.325$，向 1 靠近。

例 1 的三步是抽了具体噪声才算出来的，换一组噪声又是另一条路径。真正想知道的是 $x_t$ 服从什么分布；如果每次都从 $x_1$ 一步步算到 $x_t$，$t=1000$ 就要算一千次。能不能把两步合成一步？下一节先看走两步。

合上书，写出单步加噪的式子和条件分布，并用方差说明为什么要乘 $\sqrt{1-\beta_t}$。

### 3. 两份独立的高斯噪声叠在一起，能写成一份吗？

先用例 1 的数看一眼。取 $\beta=0.1$，把 $x_1=\sqrt{0.9}\,x_0+\sqrt{0.1}\,\varepsilon_1$ 代进 $x_2=\sqrt{0.9}\,x_1+\sqrt{0.1}\,\varepsilon_2$：

$$x_2=0.9\,x_0+\sqrt{0.09}\,\varepsilon_1+\sqrt{0.1}\,\varepsilon_2=1.8+0.3\,\varepsilon_1+0.3162\,\varepsilon_2 .$$

两份噪声的系数分别是 0.3 和 0.3162，$\varepsilon_1,\varepsilon_2$ 是独立抽的两个标准正态。它们加在一起，波动有多大？先猜一猜：是两个系数直接相加的 0.6162，还是比这小？用计算机抽 10 万组 $(\varepsilon_1,\varepsilon_2)$，算 $0.3\varepsilon_1+0.3162\varepsilon_2$ 的样本标准差，约为 0.437，比 0.6162 小得多，却和 $\sqrt{0.09+0.1}=\sqrt{0.19}=0.4359$ 很接近。也就是说，方差相加，标准差不能直接相加，而且合起来还是一个高斯。为什么，下面对一般的 $\alpha_1,\alpha_2$ 推。

对一般的 $\alpha_1,\alpha_2$ 同样代入：

$$x_2=\sqrt{\alpha_2}\,x_1+\sqrt{\beta_2}\,\varepsilon_2=\sqrt{\alpha_2}\big(\sqrt{\alpha_1}x_0+\sqrt{\beta_1}\varepsilon_1\big)+\sqrt{\beta_2}\,\varepsilon_2=\sqrt{\alpha_1\alpha_2}\,x_0+\underbrace{\sqrt{\alpha_2\beta_1}\,\varepsilon_1+\sqrt{\beta_2}\,\varepsilon_2}_{\text{两份独立的高斯噪声}}.$$

括号里是两份独立的、均值为 0 的高斯噪声之和（约定：$x_0$ 与各步噪声 $\varepsilon_1,\varepsilon_2,\dots$ 相互独立，图像的各个分量也各抽各的噪声）。需要一个结论说明它仍是一份高斯噪声。

**定理** 设 $a,b>0$，$X\sim N(0,a)$，$Y\sim N(0,b)$ 相互独立，则 $X+Y\sim N(0,a+b)$。

*思路*：独立的正态变量组成的向量是二元正态，$X+Y$ 是它的线性函数。线性函数不改变"正态"，只需要算均值和方差。

*证明*：

1. 独立时 $(X,Y)$ 的联合密度是两个正态密度的乘积，指数里是 $-\frac{x^2}{2a}-\frac{y^2}{2b}$，正是二元正态 $N(\boldsymbol 0,\mathrm{diag}(a,b))$（P.7.12）。
2. $X+Y=(1,1)\binom XY$ 是它的线性变换，由 P.7.12，线性变换后仍是正态。
3. 均值 $E[X+Y]=0$；独立所以方差相加，$\mathrm{Var}(X+Y)=a+b$。正态由均值和方差决定，所以是 $N(0,a+b)$。 $\square$

"独立"这个条件不能去：$Y=-X$ 时（$b=a$）$X+Y\equiv0$，方差是 0 而不是 $2a$。

扩散里这个条件对应"每一步都重新抽一份噪声"。如果两步共用同一个 $\varepsilon$，上面的和就是 $(0.3+0.3162)\varepsilon$，标准差 0.6162 而不是 0.4359，这正是前面猜测里那个直接相加的错误结果。

用这个结论，括号里的噪声方差是 $\alpha_2\beta_1+\beta_2$。代入 $\beta_1=1-\alpha_1$，$\beta_2=1-\alpha_2$：

$$\alpha_2(1-\alpha_1)+(1-\alpha_2)=1-\alpha_1\alpha_2 .$$

于是两份噪声合成了一份，方差正好是 $1-\alpha_1\alpha_2$：

$$x_2=\sqrt{\alpha_1\alpha_2}\,x_0+\sqrt{1-\alpha_1\alpha_2}\;\bar\varepsilon,\qquad\bar\varepsilon\sim N(0,1) .$$

这里的 $\bar\varepsilon$ 是新的标准正态，既不是 $\varepsilon_1$ 也不是 $\varepsilon_2$。看到系数的平方：信号的系数平方 $\alpha_1\alpha_2$ 加噪声的系数平方 $1-\alpha_1\alpha_2$ 等于 1，这个关系每一步都保持。

图上看，两份噪声的标准差 $\sqrt{\alpha_2\beta_1}$ 和 $\sqrt{\beta_2}$ 是直角三角形的两条直角边，合成后的标准差 $\sqrt{1-\alpha_1\alpha_2}$ 是斜边：标准差按"勾股"合成，方差按加法合成。

![两份独立噪声合成一份：两条直角边（实线）是 $\sqrt{\alpha_2\beta_1}$ 和 $\sqrt{\beta_2}$（取 $\beta=0.1$ 时为 $0.3$ 与 $0.3162$），斜边（虚线）是合成噪声的标准差 $\sqrt{1-\alpha_1\alpha_2}=0.4359$；直角三角形的斜边平方等于两直角边平方之和，就是方差相加](fig/M17-n2.pdf){width=55%}

**方法 2（合并独立高斯噪声）**

1. 写出每份噪声的系数，算每份的方差（系数的平方）。
2. 独立的高斯噪声方差相加，总噪声是一份新的 $N(0,\text{总方差})$。
3. 用 $\beta_t=1-\alpha_t$ 化简，核对"信号系数² + 噪声系数² = 1"。

**例 3**　$\beta=0.1$，$x_0=2$ 不变，不再抽具体噪声，直接求 $x_2$ 的分布，并与"先求 $x_1$ 的分布、再由单步公式推 $x_2$"核对。

合并：$\alpha_1\alpha_2=0.81$，均值 $\sqrt{0.81}\times2=1.8$，方差 $1-0.81=0.19$，所以 $x_2\sim N(1.8,0.19)$。

核对：$x_1\sim N(\sqrt{0.9}\times2,0.1)=N(1.8974,0.1)$。再走一步，$x_2=\sqrt{0.9}x_1+\sqrt{0.1}\varepsilon_2$，均值 $\sqrt{0.9}\times1.8974=1.8$，方差 $0.9\times0.1+0.1=0.19$（方法 2：独立噪声方差相加）。两种算法一致。

> 如果 $\beta_1=0.2$，$\beta_2=0.1$，$x_0=2$，求 $x_2$ 的分布。
>
> 答案：$\alpha_1=0.8$，$\alpha_2=0.9$，$\alpha_1\alpha_2=0.72$。均值 $\sqrt{0.72}\times2\approx1.697$，方差 $0.28$。核对 $\alpha_2\beta_1+\beta_2=0.18+0.1=0.28$。

两步合成了一份，可我们要的是 $t=1000$。能不能把"合成一份再走一步"这件事一次写成通式？下一节就做这个。

合上书，写出两份独立高斯噪声合并的结论和三步证明，并说明合并后的噪声为什么是一份新的 $\bar\varepsilon$。

### 4. 从原图能不能一步跳到第 $t$ 步？

两步能合成一份，三步呢？仍取 $\beta=0.1$，把上面 $x_2$ 的表达式代进 $x_3=\sqrt{0.9}\,x_2+\sqrt{0.1}\,\varepsilon_3$：

$$x_3=0.9^{3/2}x_0+\sqrt{0.9^2\times0.1}\,\varepsilon_1+\sqrt{0.9\times0.1}\,\varepsilon_2+\sqrt{0.1}\,\varepsilon_3 .$$

三份独立噪声的方差是 $0.081+0.09+0.1=0.271=1-0.729$，而信号系数的平方是 $0.9^3=0.729$。规律是：信号系数每步多乘一个 $\sqrt{\alpha}$，噪声的总方差始终等于 1 减去信号系数的平方。一般的 $t$ 步也是如此。为了写通式，记

$$\alpha_t=1-\beta_t,\qquad \bar\alpha_t=\alpha_1\alpha_2\cdots\alpha_t=\prod_{s=1}^t\alpha_s .$$

$\bar\alpha_t$ 读作"阿尔法 bar"，是前 $t$ 步 $\alpha_s=1-\beta_s$ 的连乘；每步信号乘 $\sqrt{\alpha_s}$，连乘 $t$ 步后信号系数是 $\sqrt{\bar\alpha_t}$，$\bar\alpha_t$ 是这个系数的平方。

**定理（前向过程的闭式解）** 对任意 $t\ge1$，

$$x_t=\sqrt{\bar\alpha_t}\,x_0+\sqrt{1-\bar\alpha_t}\,\varepsilon,\quad\varepsilon\sim N(0,1),\qquad\text{即}\qquad q(x_t\mid x_0)=N\big(\sqrt{\bar\alpha_t}\,x_0,\ (1-\bar\alpha_t)\big).$$

*思路*：对 $t$ 做数学归纳。$t=1$ 就是单步公式；从 $t-1$ 到 $t$ 时，再走一步，把新噪声和旧的合并，方法同第 3 节。

*证明*：

1. $t=1$：$\bar\alpha_1=\alpha_1$，式子就是 $x_1=\sqrt{\alpha_1}x_0+\sqrt{1-\alpha_1}\varepsilon_1$。
2. 假设 $x_{t-1}=\sqrt{\bar\alpha_{t-1}}\,x_0+\sqrt{1-\bar\alpha_{t-1}}\,\bar\varepsilon$，这里 $\bar\varepsilon$ 是把 $\varepsilon_1,\dots,\varepsilon_{t-1}$ 按第 3 节的办法合成的那一份标准正态。代进 $x_t=\sqrt{\alpha_t}x_{t-1}+\sqrt{1-\alpha_t}\,\varepsilon_t$：
$$x_t=\sqrt{\alpha_t\bar\alpha_{t-1}}\,x_0+\underbrace{\sqrt{\alpha_t(1-\bar\alpha_{t-1})}\,\bar\varepsilon+\sqrt{1-\alpha_t}\,\varepsilon_t}_{\text{两份独立噪声}} .$$
3. $\bar\varepsilon$ 只由 $\varepsilon_1,\dots,\varepsilon_{t-1}$ 合成，$\varepsilon_t$ 是第 $t$ 步新抽的，两者独立。方差相加：
$$\alpha_t(1-\bar\alpha_{t-1})+(1-\alpha_t)=1-\alpha_t\bar\alpha_{t-1}=1-\bar\alpha_t .$$
4. 信号系数 $\sqrt{\alpha_t\bar\alpha_{t-1}}=\sqrt{\bar\alpha_t}$。均值为 0、方差为 $v$ 的高斯变量可以写成 $\sqrt v$ 乘一个标准正态，所以两份噪声合成一份 $\sqrt{1-\bar\alpha_t}\,\varepsilon$。 $\square$

图像是向量，每个分量独立地套这个结论，写成向量形式 $q(\boldsymbol x_t\mid\boldsymbol x_0)=N(\sqrt{\bar\alpha_t}\,\boldsymbol x_0,\ (1-\bar\alpha_t)I)$。形状账本：$\boldsymbol x_0,\boldsymbol x_t,\varepsilon\in\mathbb R^{H\times W\times C}$，$\bar\alpha_t$ 是标量，对所有像素用同一个。代码对照：

```
abar = np.cumprod(1 - betas)                       # shape (T,)，abar[t-1] 就是 ᾱ_t
xt = np.sqrt(abar[t-1]) * x0 + np.sqrt(1 - abar[t-1]) * np.random.randn(*x0.shape)
```

这个公式带来两个好处。第一，训练时不用真的走 $t$ 步：随机取一个 $t$，一行就能得到 $\boldsymbol x_t$。第二，$\boldsymbol x_t$ 被写成"信号 + 噪声"的组合，系数平方和为 1，噪声部分 $\varepsilon$ 就是我们要网络去预测的东西（第 6 节）。

逐步走和一步跳产生的 $x_t$ 的分布相同吗？用例 1 的设置（$\beta=0.1$，$x_0=2$）试一试：逐步走三步重复 10 万次，样本均值 1.710、方差 0.270；直接用一步跳的公式抽 10 万次，样本均值 1.708、方差 0.271；公式给出 1.7076 和 0.271。分布相同，但这两种做法不是同一条路径：逐步走会留下中间的 $x_1,\dots,x_{t-1}$，一步跳不产生它们。训练只需要 $x_t$ 的分布，所以一步跳够用。

**方法 3（一步跳到第 $t$ 步）**

1. 算 $\bar\alpha_t=\prod_{s\le t}(1-\beta_s)$。
2. $x_t=\sqrt{\bar\alpha_t}\,x_0+\sqrt{1-\bar\alpha_t}\,\varepsilon$，$\varepsilon\sim N(0,I)$。
3. 分布是 $N(\sqrt{\bar\alpha_t}\,x_0,(1-\bar\alpha_t)I)$。

**例 4**　就是上面三步展开的数，沿用 $\beta_t=0.1$，$x_0=2$，$t=3$，用闭式解一步跳到 $x_3$。

$\bar\alpha_3=0.9^3=0.729$。均值 $\sqrt{0.729}\times2\approx0.8538\times2=1.7076$，方差 $1-0.729=0.271$。所以

$$x_3\sim N(1.7076,\ 0.271),\qquad\text{标准差}\approx0.5206 .$$

与例 1 比较：逐步走得到的一个样本 $x_3=1.6132$ 落在 $1.7076\pm0.52$ 里，没有矛盾。

> 同样的 $\beta=0.1$，求 $x_0=-1$ 时 $x_2$ 的分布。
>
> 答案：$\bar\alpha_2=0.81$，$N(-0.9,0.19)$。

**例 5**　例 4 的 $\beta$ 是常数，真实训练用的噪声表让 $\beta_t$ 逐步增大，公式不变，只是 $\bar\alpha_t$ 要用数组连乘算。取 $T=1000$，$\beta_t$ 从 $10^{-4}$ 到 $0.02$ 等差增加（DDPM 的线性表）。某个像素归一化后的值是 $x_0=0.8$，训练时抽到 $t=500$，求 $x_{500}$ 的分布。

先查表（用数组连乘算出）：$\bar\alpha_{500}\approx0.0786$。所以信号系数 $\sqrt{0.0786}\approx0.2803$，噪声系数 $\sqrt{1-0.0786}\approx0.9599$。

$$x_{500}\sim N(0.2803\times0.8,\ 0.9599^2)=N(0.2243,\ 0.9214).$$

此时噪声的标准差约 0.96，远大于信号 0.22，就这一个像素的均值和波动比较，信号已经被噪声压过。如果逐步走，需要做 500 次加噪；一步跳是 1 次。这就是训练可以对 $t$ 随机取值的原因。

闭式解对任意 $t$ 成立，但 $t=T$ 时它是不是真的把图变成了纯噪声，要看 $\beta_t$ 怎么取。这是下一节的事。

合上书，写出闭式解及它的归纳证明，并说明 $\bar\alpha_t$ 是什么。

### 5. 加到最后为什么是纯噪声？噪声表怎么定？

例 4 走到 $t=3$，信号系数 $\sqrt{0.729}=0.85$，还几乎完整；常数表 $\beta=0.1$ 下走到 $t=10$，$\bar\alpha_{10}=0.9^{10}\approx0.349$，信号系数降到 0.59。继续走下去会怎样？闭式解里，$t$ 越大 $\bar\alpha_t$ 越小，信号系数 $\sqrt{\bar\alpha_t}$ 越小，噪声系数 $\sqrt{1-\bar\alpha_t}$ 越接近 1。到 $t=T$ 时要求 $\bar\alpha_T\approx0$，这样 $x_T\approx\varepsilon\sim N(0,I)$，近似与原图无关（有限步时仍有很小的残余，数据已归一化到单位量级时它可以忽略），生成时才能从标准正态出发。

$\bar\alpha_T\approx0$ 靠什么保证？取对数。$\ln\bar\alpha_T=\sum_t\ln(1-\beta_t)$，而 $\ln(1-\beta)\le-\beta$（C.8 的不等式 $\ln(1+u)\le u$），所以

$$\bar\alpha_T\le e^{-\sum_t\beta_t} .$$

只要噪声强度加起来足够大，$\bar\alpha_T$ 就足够小。DDPM 的线性表 $\beta_t:10^{-4}\to0.02$，$T=1000$，$\sum\beta_t=10.05$，上界 $e^{-10.05}\approx4.3\times10^{-5}$，实际算出 $\bar\alpha_{1000}\approx4.0\times10^{-5}$，相当于 $\sqrt{\bar\alpha_T}\approx0.006$，对单位量级的数据，残余的信号只有 0.6% 左右。

还可以用信号和噪声的比来衡量：

$$\mathrm{SNR}_t=\frac{\bar\alpha_t}{1-\bar\alpha_t}.$$

信噪比就是信号系数平方与噪声系数平方之比，$\bar\alpha_t$ 算出来后直接代入。线性表下几个时刻的值如下（数组连乘算出）：

| $t$ | $\bar\alpha_t$ | $\mathrm{SNR}_t$ |
|---|---|---|
| 100 | 0.897 | 8.7 |
| 250 | 0.524 | 1.10 |
| 500 | 0.0786 | 0.085 |
| 1000 | $4.0\times10^{-5}$ | $4.0\times10^{-5}$ |

例如 $t=250$：$0.524/(1-0.524)=1.10$。SNR 越过 1 的位置在 $t=259$ 与 $t=260$ 之间：$\mathrm{SNR}_{259}=1.0010>1>\mathrm{SNR}_{260}=0.9905$。信号和噪声的交接发生在前四分之一多一点的位置，此后大约四分之三的步数里噪声都压过信号。

![线性噪声表下的信号系数 $\sqrt{\bar\alpha_t}$（实线）和噪声系数 $\sqrt{1-\bar\alpha_t}$（虚线）随 $t$ 的变化：两条线在 $t\approx260$（第 259、260 步之间）相交（SNR = 1），$t=1000$ 时信号系数几乎为 0；任一时刻两者的平方和等于 1](fig/M17-n3.pdf){width=70%}

噪声表怎么选，影响的是各个时刻"难度"的分布：早期 $\beta$ 很小，$x_t$ 几乎等于原图，去噪的任务很轻；若信号太早被淹没，后面大量的步数浪费在纯噪声上。

**方法 4（用噪声表算信号和噪声的比例）**

1. 算 $\bar\alpha_t=\prod(1-\beta_s)$（数组连乘）。
2. 信号系数 $\sqrt{\bar\alpha_t}$，噪声系数 $\sqrt{1-\bar\alpha_t}$，信噪比 $\bar\alpha_t/(1-\bar\alpha_t)$。
3. 检查终点：$\bar\alpha_T\le e^{-\sum\beta_t}$ 要足够小。

**例 6**　用常数表 $\beta_t=0.1$，把例 4 倒过来问：例 4 走 3 步时信号系数还有 0.85，至少走多少步，才能使 $\bar\alpha_t<0.01$（信号系数 $<0.1$）？

$\bar\alpha_t=0.9^t<0.01$，取对数：$t\ln0.9<\ln0.01$。两边除以 $\ln0.9<0$，不等号反向：

$$t>\frac{\ln0.01}{\ln0.9}\approx43.7 .$$

所以至少 $t=44$。验算：$0.9^{43}=0.01078>0.01$，$0.9^{44}=0.00970<0.01$。常数表几十步就能淹没信号，但每步的 $\beta=0.1$ 不算小，第 1 节说的"退一小步近似高斯"就不那么可靠。所以常用的表让 $\beta_t$ 从很小的值开始、慢慢增大，并取较大的总步数，每一步只加一点点，信号仍然在终点前被淹没。

> 常数表 $\beta_t=0.05$，至少走多少步才能使 $\bar\alpha_t<0.01$？
>
> 答案：$t>\ln0.01/\ln0.95\approx89.8$，至少 $t=90$。

到这里前向过程完全确定，没有任何参数。网络该根据什么来学？

合上书，说明 $\bar\alpha_T\approx0$ 靠什么保证，并说出信噪比为 1 的时刻在线性表的哪里。

### 6. 神经网络到底在学什么？

前向过程固定，没有参数。要学的是反向：给一个有噪声的 $\boldsymbol x_t$，网络要告诉我们怎样去噪。

先看一个像素。例 4 里 $x_3=1.7076+0.5206\,\varepsilon$。如果知道 $x_0=2$，看到 $x_3=1.9679$ 就能反推 $\varepsilon=(1.9679-1.7076)/0.5206=0.5$。可网络拿到的只有 $x_3$，不知道 $x_0$，只能凭 $x_3$ 去猜这个 $\varepsilon$。训练时 $x_t$ 是我们自己造的，手里有真正的 $\varepsilon$，正好拿来当答案。一般的写法如下。

闭式解给出一个现成的监督信号。把 $\boldsymbol x_t=\sqrt{\bar\alpha_t}\boldsymbol x_0+\sqrt{1-\bar\alpha_t}\,\varepsilon$ 解出 $\boldsymbol x_0$：

$$\boldsymbol x_0=\frac{\boldsymbol x_t-\sqrt{1-\bar\alpha_t}\,\varepsilon}{\sqrt{\bar\alpha_t}} .$$

给定 $\boldsymbol x_t$ 和 $t$，知道 $\varepsilon$ 就等于知道 $\boldsymbol x_0$，反之亦然。所以让网络预测哪一个都可以。DDPM 选了预测 $\varepsilon$，一个原因是它的分布固定为标准正态，每个 $t$ 上的目标尺度相同；哪一种更好学取决于数据分布和训练设置。

训练目标是预测值与真实噪声的均方误差，网络的输入是 $(\boldsymbol x_t,t)$：

$$L=E_{t,\boldsymbol x_0,\varepsilon}\Big[\big\lVert\varepsilon-\varepsilon_\theta\big(\sqrt{\bar\alpha_t}\boldsymbol x_0+\sqrt{1-\bar\alpha_t}\,\varepsilon,\ t\big)\big\rVert^2\Big].$$

形状账本：$\varepsilon$、$\boldsymbol x_t$ 和网络输出 $\varepsilon_\theta$ 都是 $H\times W\times C$ 的张量；$t$ 是标量，作为额外输入告诉网络现在在哪一步。

**方法 5（噪声预测的一步训练）**

1. 取一张真图 $\boldsymbol x_0$，随机抽 $t\in\{1,\dots,T\}$ 和 $\varepsilon\sim N(0,I)$。
2. 一步跳到 $\boldsymbol x_t=\sqrt{\bar\alpha_t}\boldsymbol x_0+\sqrt{1-\bar\alpha_t}\,\varepsilon$。
3. 损失 $\lVert\varepsilon-\varepsilon_\theta(\boldsymbol x_t,t)\rVert^2$，对 $\theta$ 做梯度步（用小批量，Adam）。

随机抽 $t$、抽 $\varepsilon$、抽 $\boldsymbol x_0$，是在对期望做抽样，所以这是 M.1.6 的随机梯度下降：小批量损失是 $L$ 的无偏估计。

为什么均方误差就够了？这和 M.2.1 的最小二乘是同一个道理：均方误差的最优预测是条件均值。

**命题** 对任意（二阶矩有限的）预测函数 $f(\boldsymbol x_t)$，$E\lVert\varepsilon-f\rVert^2$ 最小的 $f$ 是 $E[\varepsilon\mid\boldsymbol x_t]$。

*证明*：记 $g=E[\varepsilon\mid\boldsymbol x_t]$，把 $\varepsilon-f$ 写成 $(\varepsilon-g)+(g-f)$，平方展开：

$$E\lVert\varepsilon-f\rVert^2=E\lVert\varepsilon-g\rVert^2+E\lVert g-f\rVert^2+2E\big[(\varepsilon-g)^{\mathsf T}(g-f)\big] .$$

交叉项 $E\big[(\varepsilon-g)^{\mathsf T}(g-f)\big]$ 为 0，分两步看。第一步，总期望等于条件期望的期望：$E[\,\cdot\,]=E\big[E[\,\cdot\mid\boldsymbol x_t]\big]$，先算内层。第二步，给定 $\boldsymbol x_t$ 时，$g$ 和 $f$ 都只依赖 $\boldsymbol x_t$，是已知的常数，可以提到条件期望外面，内层变成 $\big(E[\varepsilon\mid\boldsymbol x_t]-g\big)^{\mathsf T}(g-f)=0$，因为 $g$ 的定义就是 $E[\varepsilon\mid\boldsymbol x_t]$。外层对 0 取期望还是 0。于是 $E\lVert\varepsilon-f\rVert^2\ge E\lVert\varepsilon-g\rVert^2$，等号当且仅当 $f=g$（几乎处处）。 $\square$

条件是 $f$ 只能看到 $\boldsymbol x_t$。如果还允许 $f$ 用 $\boldsymbol x_0$，它可以直接算出 $\varepsilon$，损失为 0，可是生成时没有 $\boldsymbol x_0$，这样的预测用不上。

所以训练好的网络近似 $E[\varepsilon\mid\boldsymbol x_t]$：在 $\boldsymbol x_t$ 这一点上，所有可能产生它的 $(\boldsymbol x_0,\varepsilon)$ 里，噪声的平均。

**例 7**　例 4 里 $x_0=2$ 是固定的数，这里让 $x_0$ 也随机，看最优预测是什么。设数据 $x_0\sim N(0,1)$（一维），$t=3$，$\beta=0.1$，求最优预测 $E[\varepsilon\mid x_t]$ 和对应的最小损失。

$x_3=\sqrt{0.729}\,x_0+\sqrt{0.271}\,\varepsilon$，$x_0,\varepsilon$ 独立，所以 $x_3\sim N(0,1)$（方差 $0.729+0.271=1$）。$(\varepsilon,x_3)$ 联合正态，协方差 $\mathrm{Cov}(\varepsilon,x_3)=\sqrt{0.271}\,\mathrm{Var}(\varepsilon)=\sqrt{0.271}$。

联合正态的条件期望（P.7.12 的回归直线）：

$$E[\varepsilon\mid x_3]=\frac{\mathrm{Cov}(\varepsilon,x_3)}{\mathrm{Var}(x_3)}\,x_3=0.5206\,x_3 .$$

最小损失是剩下的方差：$\mathrm{Var}(\varepsilon)-\frac{\mathrm{Cov}^2}{\mathrm{Var}(x_3)}=1-0.271=0.729$，也就是 $\bar\alpha_3$。

读法：这个数据分布下 $x_0$ 本身也是正态噪声，在 $x_3$ 里没法和 $\varepsilon$ 分开，所以损失降不到 0；最小损失正是 $\bar\alpha_t$，所以在这个分布下 $t$ 越小损失越大。再对比单点数据 $x_0\equiv c$：此时 $\varepsilon=(x_t-\sqrt{\bar\alpha_t}c)/\sqrt{1-\bar\alpha_t}$ 可以精确算出，损失可以降到 0。哪种情形更接近真实图片，要看数据的分布，不能凭这两个极端判断。

> 同样的 $\beta=0.1$，$x_0\sim N(0,1)$，改成 $t=1$，求最优预测和最小损失。
>
> 答案：$x_1=\sqrt{0.9}\,x_0+\sqrt{0.1}\,\varepsilon$，$\mathrm{Cov}(\varepsilon,x_1)=\sqrt{0.1}$，$\mathrm{Var}(x_1)=1$，所以 $E[\varepsilon\mid x_1]=0.3162\,x_1$，最小损失 $1-0.1=0.9=\bar\alpha_1$。

**例 8**　接着例 4 的数据，走完整的一步训练：$x_0=2$，$\beta=0.1$，抽到 $t=3$，$\varepsilon=0.5$。网络（尚未训练好）输出 $\varepsilon_\theta(x_3,3)=0.2$，求损失以及它对网络输出的梯度。

第一步，一步跳：$x_3=\sqrt{0.729}\times2+\sqrt{0.271}\times0.5=1.7076+0.2603\approx1.9679$。

第二步，网络收到 $(1.9679,3)$，输出 0.2。

第三步，损失 $(0.5-0.2)^2=0.09$，对输出 $\varepsilon_\theta$ 的导数 $-2(0.5-0.2)=-0.6$。梯度为负，梯度下降会把输出调大，朝 0.5 靠近。

网络内部的参数怎样随这个梯度更新，就是 M.7 的反向传播，不在本章展开。

> $\beta=0.1$，$x_0=-1$，$t=2$，$\varepsilon=1$，网络输出 $\varepsilon_\theta=0.4$，求 $x_2$、损失及其对输出的梯度。
>
> 答案：$x_2=0.9\times(-1)+\sqrt{0.19}\times1\approx-0.4641$；损失 $(1-0.4)^2=0.36$；梯度 $-2(1-0.4)=-1.2$。

简单损失是直接写出来的。它和上一章的 ELBO 是什么关系？没有这层联系，我们只知道它"合理"，不知道它"从哪来"。下一节把这条线补上。

合上书，写出噪声预测的损失，说明最优预测是什么，并说明训练时为什么随机抽 $t$ 就够了。

### 7. 已知原图时，往回退一步是什么分布？

这一节解释上面的简单损失和 ELBO 是什么关系：它是 ELBO 去掉各项权重以后的版本。

先看一个具体的问题。训练时手里既有 $x_0=2$，又有 $x_3=1.9679$（例 8），那 $x_2$ 应该在哪里？

从 $x_0$ 一侧看，例 3 说 $x_2\sim N(1.8,0.19)$。从 $x_3$ 一侧看，$x_3=\sqrt{0.9}\,x_2+\sqrt{0.1}\,\varepsilon_3$，把它看成 $x_2$ 的函数，是一个以 $x_3/\sqrt{0.9}=2.0744$ 为中心、方差 $0.1/0.9=0.1111$ 的高斯形状。两个来源各给了一个高斯，$x_2$ 要同时满足两者，也就是把两个形状相乘。一般的 $t$ 同样处理，这个分布叫前向后验 $q(\boldsymbol x_{t-1}\mid\boldsymbol x_t,\boldsymbol x_0)$（本节取 $t\ge2$，并记 $\bar\alpha_0=1$；$t=1$ 时 $\boldsymbol x_0$ 是已知常数，没有随机性，那一项在 ELBO 里单独作为重建项）。

**怎样写出这个乘积？** 由贝叶斯公式（P.2），$q(x_{t-1}\mid x_t,x_0)\propto q(x_t\mid x_{t-1},x_0)\,q(x_{t-1}\mid x_0)$。这条链里 $x_t$ 只依赖 $x_{t-1}$（马尔可夫性），已知 $x_{t-1}$ 以后 $x_0$ 不再提供信息，$q(x_t\mid x_{t-1},x_0)=q(x_t\mid x_{t-1})$，于是

$$q(x_{t-1}\mid x_t,x_0)\ \propto\ q(x_t\mid x_{t-1})\;q(x_{t-1}\mid x_0).$$

右边是关于 $x_{t-1}$ 的两个高斯：第二个是第 4 节的 $N(\sqrt{\bar\alpha_{t-1}}x_0,\ 1-\bar\alpha_{t-1})$；第一个把 $x_t$ 固定，看成 $x_{t-1}$ 的函数，指数里是 $-\frac{(x_t-\sqrt{\alpha_t}x_{t-1})^2}{2\beta_t}=-\frac{\alpha_t}{2\beta_t}\big(x_{t-1}-x_t/\sqrt{\alpha_t}\big)^2$，也就是以 $x_t/\sqrt{\alpha_t}$ 为中心、方差 $\beta_t/\alpha_t$ 的高斯形状。

**两个高斯形状相乘会得到什么？** 需要一个引理。

**引理** $N(a,u)$ 与 $N(b,v)$ 的密度（关于同一个变量 $x$）相乘，正比于一个高斯，其精度（方差的倒数）是两个精度之和，均值是按精度加权的平均：

$$\frac1w=\frac1u+\frac1v,\qquad m=w\Big(\frac au+\frac bv\Big).$$

*证明*：指数相加，$-\frac{(x-a)^2}{2u}-\frac{(x-b)^2}{2v}=-\frac12\Big[\big(\tfrac1u+\tfrac1v\big)x^2-2\big(\tfrac au+\tfrac bv\big)x\Big]+\text{常数}$。对 $x$ 配方：与 $-\frac1{2w}(x-m)^2=-\frac1{2w}x^2+\frac mw x+\text{常数}$ 对比，$x^2$ 的系数给出 $\frac1w=\frac1u+\frac1v$，一次项的系数给出 $\frac mw=\frac au+\frac bv$，即 $m=w\big(\frac au+\frac bv\big)$。 $\square$

**代入以后是什么？** 用引理（$a=x_t/\sqrt{\alpha_t}$，$u=\beta_t/\alpha_t$；$b=\sqrt{\bar\alpha_{t-1}}x_0$，$v=1-\bar\alpha_{t-1}$），精度之和是

$$\frac{\alpha_t}{\beta_t}+\frac1{1-\bar\alpha_{t-1}}=\frac{\alpha_t(1-\bar\alpha_{t-1})+\beta_t}{\beta_t(1-\bar\alpha_{t-1})}=\frac{1-\bar\alpha_t}{\beta_t(1-\bar\alpha_{t-1})},$$

最后一步用了 $\alpha_t(1-\bar\alpha_{t-1})+\beta_t=\alpha_t-\bar\alpha_t+1-\alpha_t=1-\bar\alpha_t$。所以

$$q(x_{t-1}\mid x_t,x_0)=N\big(\tilde\mu_t,\ \tilde\beta_t\big),\quad \tilde\beta_t=\frac{1-\bar\alpha_{t-1}}{1-\bar\alpha_t}\beta_t,\quad\tilde\mu_t=\frac{\sqrt{\bar\alpha_{t-1}}\,\beta_t}{1-\bar\alpha_t}\,x_0+\frac{\sqrt{\alpha_t}\,(1-\bar\alpha_{t-1})}{1-\bar\alpha_t}\,x_t .$$

均值是 $x_0$ 和 $x_t$ 的线性组合。

**方法 6（前向后验）**

1. 写出两个关于 $x_{t-1}$ 的高斯：$N(x_t/\sqrt{\alpha_t},\ \beta_t/\alpha_t)$ 和 $N(\sqrt{\bar\alpha_{t-1}}x_0,\ 1-\bar\alpha_{t-1})$。
2. 精度相加，均值按精度加权。
3. 得 $\tilde\beta_t$ 和 $\tilde\mu_t$。

**例 9**　就是上面开头那个问题，沿用 $\beta=0.1$，$x_0=2$，$t=3$，用例 8 的 $x_3=1.9679$，求 $q(x_2\mid x_3,x_0)$。

两个形状在上面已经列出：$N(1.8,0.19)$ 和 $N(2.0744,0.1111)$。精度分别是 $1/0.19=5.263$ 和 $0.9/0.1=9$。

精度之和 $14.263$，方差 $\tilde\beta_3=0.0701$（公式核对：$\frac{0.19}{0.271}\times0.1=0.0701$）。均值是加权平均：

$$\tilde\mu_3=\frac{5.263\times1.8+9\times2.0744}{14.263}\approx1.9731 .$$

比 $x_3=1.9679$ 略大，朝着 $x_0=2$ 靠了一点，方差只有 $0.0701$，比只知道 $x_0$ 时 $x_2$ 的方差 $0.19$ 小得多：两头都知道以后，退一步的位置很确定。

> 同样的 $\beta=0.1$，$x_0=2$，$t=2$，$x_2=1.8$，求 $\tilde\beta_2$ 和 $\tilde\mu_2$。
>
> 答案：$\bar\alpha_1=0.9$，$\bar\alpha_2=0.81$。$\tilde\beta_2=\frac{0.1}{0.19}\times0.1=0.0526$；$\tilde\mu_2=\frac{\sqrt{0.9}\times0.1}{0.19}\times2+\frac{\sqrt{0.9}\times0.1}{0.19}\times1.8$，两个系数相同都是 $0.4993$，$\tilde\mu_2=0.4993\times3.8=1.897$。

![退一步的分布是两个高斯形状的乘积：点线是由 $x_3$ 得到的形状 $N(2.0744,0.1111)$，虚线是 $q(x_2\mid x_0)=N(1.8,0.19)$，实线是它们的乘积归一化后的 $N(1.9731,0.0701)$，比两者都窄，均值落在两者之间、更靠近精度大（更窄）的点线](fig/M17-n4.pdf){width=70%}

**这个前向后验怎样接到 ELBO 上？** M.16.3 的 ELBO 是 $\log p(x_0)\ge E_q\big[\log\frac{p_\theta(x_{0:T})}{q(x_{1:T}\mid x_0)}\big]$，其中 $x_{1:T}$ 是隐变量，$q$ 是固定的前向过程，$p_\theta(x_{0:T})=p(x_T)\prod_{t=1}^{T}p_\theta(x_{t-1}\mid x_t)$，$p(x_T)=N(0,I)$。关键是把分母 $q(x_{1:T}\mid x_0)=\prod_{t=1}^{T}q(x_t\mid x_{t-1})$ 改写成"反向"的乘积。对 $t\ge2$，用贝叶斯公式和马尔可夫性：

$$q(x_t\mid x_{t-1})=\frac{q(x_{t-1}\mid x_t,x_0)\,q(x_t\mid x_0)}{q(x_{t-1}\mid x_0)} .$$

把 $t=2,\dots,T$ 的这些式子连乘，各项 $\dfrac{q(x_t\mid x_0)}{q(x_{t-1}\mid x_0)}$ 逐个约去，只剩 $\dfrac{q(x_T\mid x_0)}{q(x_1\mid x_0)}$；再乘上 $t=1$ 的因子 $q(x_1\mid x_0)$，分母的 $q(x_1\mid x_0)$ 恰好被约掉：

$$q(x_{1:T}\mid x_0)=q(x_T\mid x_0)\prod_{t=2}^{T}q(x_{t-1}\mid x_t,x_0).$$

代回 ELBO，取负号并取期望。$t\ge2$ 的 $q(x_{t-1}\mid x_t,x_0)$ 与 $p_\theta(x_{t-1}\mid x_t)$ 配成 KL，$q(x_T\mid x_0)$ 与 $p(x_T)$ 配成一项，$t=1$ 的 $\log p_\theta(x_0\mid x_1)$ 没有对手，单独留下：

$$-\mathrm{ELBO}=\mathrm{KL}\big(q(x_T\mid x_0)\Vert p(x_T)\big)+\sum_{t=2}^{T}E\,\mathrm{KL}\big(q(x_{t-1}\mid x_t,x_0)\,\Vert\,p_\theta(x_{t-1}\mid x_t)\big)-E\log p_\theta(x_0\mid x_1).$$

第一项没有参数（$\bar\alpha_T\approx0$ 时接近 0）。

**中间的每个 KL 里，哪一部分含 $\theta$？** 每一项都是两个高斯的 KL。让 $p_\theta(x_{t-1}\mid x_t)=N(\mu_\theta(x_t,t),\sigma_t^2)$，方差 $\sigma_t^2$ 取成 $\tilde\beta_t$ 或 $\beta_t$ 这样不含参数的值。两个一维高斯的 KL 是

$$\mathrm{KL}\big(N(m_1,s_1^2)\Vert N(m_2,s_2^2)\big)=\log\frac{s_2}{s_1}+\frac{s_1^2+(m_1-m_2)^2}{2s_2^2}-\frac12 .$$

这里 $m_1=\tilde\mu_t$，$s_1^2=\tilde\beta_t$，$m_2=\mu_\theta$，$s_2^2=\sigma_t^2$。$s_1,s_2$ 不含 $\theta$ 时，只有 $\frac{(\tilde\mu_t-\mu_\theta)^2}{2\sigma_t^2}$ 含 $\theta$，其余是常数。取 $\sigma_t^2=\tilde\beta_t$ 时 $s_1=s_2$，常数是 $0+\frac12-\frac12=0$。

**把均值写成噪声的形式会怎样？** 把 $x_0=(x_t-\sqrt{1-\bar\alpha_t}\,\varepsilon)/\sqrt{\bar\alpha_t}$ 代进 $\tilde\mu_t$，化简得到

$$\tilde\mu_t=\frac1{\sqrt{\alpha_t}}\Big(x_t-\frac{\beta_t}{\sqrt{1-\bar\alpha_t}}\,\varepsilon\Big).$$

（$x_t$ 的系数：$\frac{\sqrt{\bar\alpha_{t-1}}\beta_t}{(1-\bar\alpha_t)\sqrt{\bar\alpha_t}}+\frac{\sqrt{\alpha_t}(1-\bar\alpha_{t-1})}{1-\bar\alpha_t}$，用 $\sqrt{\bar\alpha_{t-1}}/\sqrt{\bar\alpha_t}=1/\sqrt{\alpha_t}$，通分后分子 $\beta_t+\alpha_t(1-\bar\alpha_{t-1})=1-\bar\alpha_t$ 与分母约去，得 $1/\sqrt{\alpha_t}$。）例 9 的数验算：$\varepsilon=0.5$，$\tilde\mu_3=\frac1{\sqrt{0.9}}\big(1.9679-\frac{0.1}{\sqrt{0.271}}\times0.5\big)=1.9731$，与上面一致。

让网络的均值也取同样形式，$\mu_\theta=\frac1{\sqrt{\alpha_t}}(x_t-\frac{\beta_t}{\sqrt{1-\bar\alpha_t}}\varepsilon_\theta)$，则均值差为 $\frac{\beta_t}{\sqrt{\alpha_t}\sqrt{1-\bar\alpha_t}}(\varepsilon-\varepsilon_\theta)$，KL 变成

$$\frac{\beta_t^2}{2\sigma_t^2\alpha_t(1-\bar\alpha_t)}\,\lVert\varepsilon-\varepsilon_\theta\rVert^2 .$$

各个 $t$ 的 KL 都是预测噪声的均方误差，只差一个依赖 $t$ 的系数。

**去掉系数的代价是什么？** DDPM 把 KL 项的这些系数全部去掉，换成 1，重建项也不再单独计较（$t=1$ 作为一般的 $t$ 处理），就得到第 6 节的简单损失。这回答了 ELBO 与简单损失的关系：简单损失是 ELBO 的一个重新加权的版本，它不再是 ELBO 本身。代价是各个 $t$ 的权重变了，不再对应对数似然的下界；DDPM 的做法是把它当作一个更好训练的目标，实际样本质量也更好。

到这里训练目标的来历清楚了。可是网络训练好以后，怎样用它真的生成一张图？这是最后一节。

合上书，写出前向后验的均值与方差，并说明每个 KL 项为什么变成噪声预测的均方误差。

### 8. 生成时怎样一步步去噪？

网络训练好以后，生成一张新图：先抽 $\boldsymbol x_T\sim N(\boldsymbol 0,I)$，再从 $t=T$ 走到 $t=1$。每一步根据第 7 节的均值公式，把 $\varepsilon$ 换成网络的预测，再补上一点随机性。

**方法 7（DDPM 采样的一步）**

1. 网络预测 $\varepsilon_\theta(\boldsymbol x_t,t)$。
2. 均值 $\boldsymbol\mu_\theta=\frac1{\sqrt{\alpha_t}}\Big(\boldsymbol x_t-\frac{\beta_t}{\sqrt{1-\bar\alpha_t}}\varepsilon_\theta\Big)$。
3. $\boldsymbol x_{t-1}=\boldsymbol\mu_\theta+\sigma_t\boldsymbol z$，$\boldsymbol z\sim N(\boldsymbol 0,I)$，$\sigma_t^2=\beta_t$（或 $\tilde\beta_t$）；最后一步 $t=1$ 不加噪声。这是采样的约定：最后一步的 $p_\theta(x_0\mid x_1)$ 取均值，输出的就是最终的图，再加噪声只会在图上留下杂点；前面各步都按分布抽样。

为什么每一步还要补噪声？反向的条件分布是 $N(\mu_\theta,\sigma_t^2)$，不是一个点，生成要从这个分布里抽样，补噪声就是在实现这个抽样，它让同一个 $\boldsymbol x_T$ 也可能走出不同的路径。如果每一步都只取均值，得到的是一条"均值路径"，不是模型分布的样本。

**例 10**　沿用例 8、9 的数据，把例 9 的退一步连着走三次。数据只有一个点 $x_0=2$，所以"完美网络"能精确给出 $\varepsilon^*(x_t)=(x_t-\sqrt{\bar\alpha_t}\cdot2)/\sqrt{1-\bar\alpha_t}$。常数 $\beta=0.1$，从 $x_3=1.9679$ 出发，为看清均值的走向，各步取 $\boldsymbol z=0$，走到 $x_0$。

$t=3$：$\varepsilon^*=(1.9679-0.8538\times2)/0.5206=0.5$（就是例 8 的 $\varepsilon$），$x_2=\mu=1.9731$。

$t=2$：$\bar\alpha_2=0.81$，$\varepsilon^*=(1.9731-0.9\times2)/\sqrt{0.19}\approx0.3972$，$x_1=\frac1{\sqrt{0.9}}\big(1.9731-\frac{0.1}{\sqrt{0.19}}\times0.3972\big)\approx1.9838$。

$t=1$：$\bar\alpha_1=0.9$，$\varepsilon^*=(1.9838-0.9487\times2)/0.3162\approx0.2734$，$x_0=\frac1{\sqrt{0.9}}\big(1.9838-\frac{0.1}{0.3162}\times0.2734\big)=2.0000$。

三步下来精确回到 $x_0=2$，此时网络给出的是真的噪声。真实数据有很多个点，网络预测的是 $E[\varepsilon\mid\boldsymbol x_t]$（第 6 节），均值走向的是所有可能原图的"加权方向"，不是某一张具体的训练图。

回到开头的问题：怎样从一团噪声变出一张图？加噪这一半不用学，而且有闭式解，所以训练时一步就能造出 $(\boldsymbol x_t,\varepsilon)$ 的配对，让网络学预测 $\varepsilon$（第 4、6 节）；生成时从 $\boldsymbol x_T\sim N(\boldsymbol 0,I)$ 出发，按方法 7 走 $T$ 步，每步的均值由网络的预测给出。例 10 在只有一个数据点的情形里把这条路完整走了一遍，从 $x_3=1.9679$ 回到 $x_0=2$。代价是采样要跑网络 $T$ 次（如 1000 次），比 VAE 和 GAN 的一次前向慢得多。

合上书，写出 DDPM 采样的一步，并说明 $t=1$ 一步为什么不加噪声。

### 本章小结

| 方法 | 什么时候用 | 对应题号 |
|---|---|---|
| 方法 1（单步加噪） | 写单步条件分布；方差递推 | M17-01、M17-07、M17-11 |
| 方法 2（合并独立高斯噪声） | 两步或多步噪声合成一份；方差相加 | M17-02、M17-05、M17-06、M17-09 |
| 方法 3（一步跳到第 $t$ 步） | 求 $x_t$ 的分布；构造训练样本 | M17-03、M17-04、M17-06、M17-07、M17-09、M17-10、M17-11 |
| 方法 4（用噪声表算信号和噪声的比例） | 算 $\bar\alpha_t$、信噪比、找终点 | M17-03、M17-08 |
| 方法 5（噪声预测的一步训练） | 写损失；最优预测和最小损失 | M17-04、M17-10、M17-12 |
| 方法 6（前向后验） | 已知 $x_0$ 时退一步的分布；接到 ELBO | M17-15 |
| 方法 7（DDPM 采样的一步） | 生成时的一步；完美网络下的轨迹 | — |

在主线的三件套上，本章把 M.16 的隐变量框架推进到一串隐变量：模型 $f$ 是预测噪声的网络，损失是预测噪声的均方误差（ELBO 重新加权的结果），更新规则是随机梯度加 Adam；新的东西只有前向加噪这一半，它没有参数，闭式解让训练一步就能造出任意 $t$ 的样本。损失与概率假设的表本章再增一行：

| 损失或做法 | 背后的概率假设 | 出现章 |
|---|---|---|
| 均方误差 | 噪声是高斯分布 | M.2 |
| 奖励减 KL | 偏好服从 Bradley–Terry 模型 | M.15 |
| ELBO | 隐变量模型的对数似然下界 | M.16 |
| **预测噪声的均方误差（本章新增）** | 前向过程是高斯分布 | M.17 |
