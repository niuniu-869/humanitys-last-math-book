## C.21 · 多元复合函数与隐函数的求导

训练一个神经网络时，损失要经过几十层运算才依赖到某一个参数。想知道「把这个参数调大一点，损失会变多少」，就得把这几十层的变化率一层一层接起来。这件事用的就是本章的链式法则：反向传播算法把链式法则放在一张计算图上系统地执行一遍，1986 年由鲁梅尔哈特、辛顿和威廉斯推广开。

另一类问题里，函数根本没有写出来。经济学问「每件商品多征一点税，均衡价格变多少」，均衡价格只是被一个方程隐含地确定着：方程有了，函数的表达式却求不出来。能不能直接从方程算出导数，什么时候方程真的确定了一个函数，这是隐函数定理回答的问题。这个定理的幂级数情形来自柯西，一般的实函数情形在 19 世纪后半叶由迪尼等人讲清楚。

两类问题用同一个办法：C.20 讲过，可微就是「放大了看是一张平面」，函数的改变量可以用一个线性式代替。复合以后的函数放大了看，仍是线性的，只不过系数要沿着复合的路径一层层乘起来。本章按下面的顺序展开。第 1 节处理中间变量只有一个自变量的情形，并证明链式法则；第 2 节处理好几个自变量，用树形图一项不漏；第 3 节说明全微分的写法与谁是中间变量无关；第 4 节求抽象函数的二阶偏导；第 5、6 节讲方程确定的隐函数；第 7 节处理两个方程确定两个函数。

### 1. $x$ 和 $y$ 都随时间变化时，$z=f(x,y)$ 随时间变得多快？

C.20 的碗 $z=x^2+y^2$ 上，放一个小球，让它的位置随时间 $t$ 变化：$x=t$，$y=t^2$。小球的高度 $z$ 就成了 $t$ 的函数，可以直接算。把 $x$、$y$ 代入：

$$z=t^2+(t^2)^2=t^2+t^4,\qquad \frac{\mathrm dz}{\mathrm dt}=2t+4t^3 .$$

现在换一种算法，不先代入。$z=f(x,y)$ 的偏导数是 $f_x=2x$、$f_y=2y$，位置的变化率是 $x'(t)=1$、$y'(t)=2t$。把「$x$ 方向每走一步 $z$ 变多少，乘上 $x$ 走了多少」与「$y$ 方向」的对应量加起来：

$$f_x\,x'+f_y\,y'=2x\cdot1+2y\cdot2t=2t+2t^2\cdot2t=2t+4t^3 .$$

两种算法一致。这不是巧合，它就是下面的定理。

![小球的位置 $(t,t^2)$ 在 $xy$ 平面里走一条抛物线（粗实线），虚线圆是碗 $z=x^2+y^2$ 的等高线；从 $P=(0.5,0.25)$ 走到 $Q=(0.6,0.36)$，位移是 $\Delta x=0.1$、$\Delta y=0.11$，高度的实际改变量 $\Delta z=0.1771$，线性部分 $f_x\Delta x+f_y\Delta y=0.155$](fig/C21-n3.pdf){width=55%}

**定理（链式法则，中间变量只有一个自变量）**　设 $z=f(x,y)$ 在点 $(x_0,y_0)$ 可微，$x=x(t)$、$y=y(t)$ 在 $t_0$ 可导，并且 $x(t_0)=x_0$、$y(t_0)=y_0$。那么复合函数 $z=f(x(t),y(t))$ 在 $t_0$ 可导，并且

$$\frac{\mathrm dz}{\mathrm dt}=\frac{\partial f}{\partial x}\frac{\mathrm dx}{\mathrm dt}+\frac{\partial f}{\partial y}\frac{\mathrm dy}{\mathrm dt}.$$

这个 $\dfrac{\mathrm dz}{\mathrm dt}$ 叫作 $z$ 对 $t$ 的**全导数**。写 $\mathrm d$ 不写 $\partial$，是因为 $z$ 经过 $x$、$y$ 最终只依赖 $t$ 这一个变量。

证明的想法是：可微说明 $z$ 的改变量等于一个线性部分加上一个很小的余项，把这个式子的两边都除以 $\Delta t$，再让 $\Delta t\to0$。

1. 当 $t$ 从 $t_0$ 改变 $\Delta t$ 时，$x$、$y$ 分别改变 $\Delta x$、$\Delta y$，$z$ 改变 $\Delta z$。记 $\rho=\sqrt{\Delta x^2+\Delta y^2}$。$f$ 在 $(x_0,y_0)$ 可微（C.20.5），即

$$\Delta z=f_x\Delta x+f_y\Delta y+\varepsilon\,\rho ,$$

其中 $\varepsilon=\varepsilon(\Delta x,\Delta y)$，当 $(\Delta x,\Delta y)\to(0,0)$ 时 $\varepsilon\to0$；$\rho=0$ 时规定 $\varepsilon=0$。这就是「余项比 $\rho$ 高阶」的写法。

2. 两边除以 $\Delta t$：

$$\frac{\Delta z}{\Delta t}=f_x\frac{\Delta x}{\Delta t}+f_y\frac{\Delta y}{\Delta t}+\varepsilon\cdot\frac{\rho}{\Delta t}.$$

3. 令 $\Delta t\to0$。因为 $x(t)$、$y(t)$ 可导，所以 $\frac{\Delta x}{\Delta t}\to x'(t_0)$，$\frac{\Delta y}{\Delta t}\to y'(t_0)$。可导必连续（C.4），所以 $\Delta x$、$\Delta y\to0$，$\rho\to0$，于是 $\varepsilon\to0$。又

$$\left|\frac{\rho}{\Delta t}\right|=\sqrt{\Big(\frac{\Delta x}{\Delta t}\Big)^2+\Big(\frac{\Delta y}{\Delta t}\Big)^2}\to\sqrt{x'(t_0)^2+y'(t_0)^2},$$

这个量有界，所以最后一项趋于 0。前两项趋于 $f_xx'+f_yy'$，定理得证。

证明里用了两次条件：$f$ 可微，才有第 1 步的展开；$x$、$y$ 可导，才有第 3 步。两个条件各去掉一个，看会怎样。先去掉第一个。

取 $f(x,y)=\dfrac{x^2y}{x^2+y^2}$，$f(0,0)=0$。沿坐标轴 $f$ 恒为 0，所以 $f_x(0,0)=f_y(0,0)=0$。让 $x=t$、$y=t$，则 $f(t,t)=\dfrac t2$，全导数是 $\dfrac12$。可是公式给出的是 $0\cdot1+0\cdot1=0$。两者不一样。如果 $f$ 在原点可微，定理就会保证公式成立，给出 $0$，而直接算出的是 $\frac12$，矛盾；所以这个 $f$ 在原点不可微。偏导数存在，不足以用链式法则。

再去掉第二个：$f=x+y$ 处处可微，取 $x=y=|t|$，则 $z=2|t|$ 在 $t=0$ 不可导，公式里的 $x'(0)$、$y'(0)$ 本来就不存在。

**方法 1（全导数）**

1. 认出谁是中间变量，谁是唯一的自变量：$z$ 经过 $x$、$y$ 依赖 $t$。
2. 分别求 $f_x$、$f_y$ 和 $x'(t)$、$y'(t)$。
3. 套公式 $\dfrac{\mathrm dz}{\mathrm dt}=f_xx'+f_yy'$，中间变量不论几个，每个贡献一项。
4. 要某个 $t$ 的值时，最后再代 $t$。

**例 1**　和小球的例子相比，这道题只换了碗和路径：碗换成 $z=x^2y$，路径换成 $x=\sin t$、$y=\cos t$，求 $\dfrac{\mathrm dz}{\mathrm dt}$。

思路：$z$ 经过 $x$、$y$ 依赖 $t$，直接用方法 1。

第一步，$f_x=2xy$，$f_y=x^2$，$x'=\cos t$，$y'=-\sin t$。

第二步，套公式：

$$\frac{\mathrm dz}{\mathrm dt}=2xy\cos t+x^2(-\sin t)=2\sin t\cos^2t-\sin^3t .$$

第三步，算 $t=\frac\pi4$ 的值：$2\cdot\frac{\sqrt2}2\cdot\frac12-\big(\frac{\sqrt2}2\big)^3=\frac{\sqrt2}2-\frac{\sqrt2}4=\frac{\sqrt2}4$。

> 设 $z=xy^2$，$x=t^2$，$y=\mathrm e^t$，求 $\dfrac{\mathrm dz}{\mathrm dt}$。
>
> 答案：$f_x=y^2$，$f_y=2xy$，$x'=2t$，$y'=\mathrm e^t$。$\dfrac{\mathrm dz}{\mathrm dt}=y^2\cdot2t+2xy\cdot\mathrm e^t=2t\,\mathrm e^{2t}+2t^2\mathrm e^{2t}=2t(t+1)\mathrm e^{2t}$。

**例 2**　和例 1 相比，这次中间变量从两个变成三个：$u=xyz$，$x=t$，$y=t^2$，$z=t^3$，求 $\dfrac{\mathrm du}{\mathrm dt}$。

每个中间变量贡献一项，所以有三项：

$$\frac{\mathrm du}{\mathrm dt}=yz\cdot1+xz\cdot2t+xy\cdot3t^2=t^5+2t^5+3t^5=6t^5 .$$

直接代入核对：$u=t\cdot t^2\cdot t^3=t^6$，导数 $6t^5$，与上式相同。这道题说明项数就是中间变量的个数，不多不少。

例 2 里每个中间变量只经过一条路径到达 $t$。下面的例子里，同一个量沿着两条路径影响结果，这是反向传播里最常见的情形，也是它的最小模型。背景只需要两句话：训练神经网络，就是调整参数 $w$，让「损失」（模型的出错程度，越小越好）变小，损失对 $w$ 的导数告诉我们 $w$ 该往哪边调；把计算的先后顺序画成一张图（计算图，箭头表示「由谁算出」），求导就是沿着图上的路径走。

**例 3**　和例 2 相比，这次同一个参数 $w$ 出现了两次，所以损失到 $w$ 有两条路径（$w\to a\to p$ 和 $w\to b\to p$）。设有一个只含一个参数 $w$ 的小模型：对两个输入 $1$ 和 $2$，先算 $a=1\cdot w$ 和 $b=2\cdot w$，输出 $p=ab$。目标值 $10$，损失 $L=(p-10)^2$。求 $w=3$ 时 $\dfrac{\mathrm dL}{\mathrm dw}$。

思路：$L$ 先依赖 $p$，$p$ 依赖 $a$ 和 $b$，$a$、$b$ 都依赖 $w$。把 $L$ 看成 $a$、$b$ 的函数 $L=(ab-10)^2$，再用方法 1。

第一步，先沿计算顺序把各量的值算出来（前向）：$a=3$，$b=6$，$p=18$，$L=64$。

第二步，求局部导数。$\dfrac{\partial L}{\partial a}=2(p-10)\cdot b=2\cdot8\cdot6=96$，$\dfrac{\partial L}{\partial b}=2(p-10)\cdot a=2\cdot8\cdot3=48$，$\dfrac{\mathrm da}{\mathrm dw}=1$，$\dfrac{\mathrm db}{\mathrm dw}=2$。

第三步，两条路径各乘一次，再相加：

$$\frac{\mathrm dL}{\mathrm dw}=96\cdot1+48\cdot2=192 .$$

核对：$L=(2w^2-10)^2$，$\dfrac{\mathrm dL}{\mathrm dw}=2(2w^2-10)\cdot4w$，$w=3$ 时为 $2\cdot8\cdot12=192$。

算出 $192$ 以后，常见的做法是取一个很小的步长（C.22 称为学习率），例如 $0.01$，把 $w$ 改成 $3-0.01\times192=1.08$。往负导数的方向走，是因为导数为正说明 $w$ 增大会让损失变大。为什么沿负导数的方向走最有效，C.22 会讲清楚。

到这里，中间变量都只依赖一个自变量 $t$。可要是 $x$、$y$ 本身又各依赖两个量，$z$ 就要对两个量分别求变化率，$\mathrm d$ 得换成 $\partial$，路径也会变多，怎样才能一项不漏？下一节回答。

合上书，写出全导数公式，并说明证明里为什么需要 $f$ 可微，以及上面的反例为什么说明偏导数存在还不够。

### 2. 中间变量和自变量都有好几个时，怎样一项不漏？

上一节只有一个自变量 $t$。现在让自变量多起来，先看最小的情形：$z=uv$，$u=x+y$，$v=x-y$。直接代入，$z=x^2-y^2$，$z_x=2x$。换一种算法：把 $y$ 固定，$u$、$v$ 就成了只含 $x$ 的一元函数，$u_x=1$，$v_x=1$，上一节的公式马上能用，只是要把 $\mathrm d$ 换成 $\partial$：$z_x=v\cdot1+u\cdot1=(x-y)+(x+y)=2x$，两种算法一致。

一般地，$z=f(u,v)$，而 $u$、$v$ 又各自是 $x$、$y$ 的函数：$u=u(x,y)$，$v=v(x,y)$。这里设 $f$ 有连续偏导数（因而可微），$u$、$v$ 也有连续偏导数，那么

$$\frac{\partial z}{\partial x}=\frac{\partial f}{\partial u}\frac{\partial u}{\partial x}+\frac{\partial f}{\partial v}\frac{\partial v}{\partial x},\qquad
\frac{\partial z}{\partial y}=\frac{\partial f}{\partial u}\frac{\partial u}{\partial y}+\frac{\partial f}{\partial v}\frac{\partial v}{\partial y}.$$

变量一多，容易漏项。办法是画一张**树形图**：最上面是 $z$，往下一层是中间变量 $u$、$v$，再往下是自变量 $x$、$y$，每条边标上对应的偏导数。

![实线边是从 $z$ 走到 $x$ 的两条路径（经过 $u$ 或经过 $v$），末段为虚线的两条路径通向 $y$；每条路径上的偏导相乘，同一个自变量下的各条路径相加](fig/C21-n1.pdf){width=60%}

**方法 2（树形图）**

1. 画出 $z$、中间变量、自变量三层，每条边写上这一层的偏导数（或导数）。
2. 求 $\dfrac{\partial z}{\partial x}$：找出所有从 $z$ 走到 $x$ 的路径，每条路径上的偏导数相乘。
3. 把这些乘积相加。路径有几条就有几项。
4. 一个中间变量如果只依赖一个自变量，这条边写 $\mathrm d$；依赖几个自变量就写 $\partial$。

**例 4**　和例 1 相比，中间变量仍是两个，但自变量也从一个 $t$ 变成了两个 $x$、$y$，所以每个中间变量要对 $x$、$y$ 各求一次偏导，路径也从两条变成四条。设 $z=u^2\ln v$，$u=\dfrac xy$，$v=3x-2y$，求 $\dfrac{\partial z}{\partial x}$、$\dfrac{\partial z}{\partial y}$ 在点 $(2,1)$ 的值。

第一步，画树：$z$ 下面有 $u$、$v$，它们下面都有 $x$ 和 $y$。到 $x$ 有两条路径，到 $y$ 也有两条。

第二步，写出每条边：

$$\frac{\partial z}{\partial u}=2u\ln v,\quad \frac{\partial z}{\partial v}=\frac{u^2}{v},\quad
\frac{\partial u}{\partial x}=\frac1y,\quad\frac{\partial u}{\partial y}=-\frac{x}{y^2},\quad
\frac{\partial v}{\partial x}=3,\quad\frac{\partial v}{\partial y}=-2 .$$

第三步，每条路径相乘，相加：

$$\frac{\partial z}{\partial x}=2u\ln v\cdot\frac1y+\frac{u^2}{v}\cdot3,\qquad
\frac{\partial z}{\partial y}=2u\ln v\cdot\Big(-\frac{x}{y^2}\Big)+\frac{u^2}{v}\cdot(-2).$$

第四步，代入 $(x,y)=(2,1)$，此时 $u=2$，$v=4$：

$$\frac{\partial z}{\partial x}=4\ln4+3,\qquad \frac{\partial z}{\partial y}=-8\ln4-2 .$$

数值上是 $z_x\approx8.545$，$z_y\approx-13.090$。

> 设 $z=\mathrm e^{u}\sin v$，$u=xy$，$v=x+y$，求 $z_x$、$z_y$。
>
> 答案：$z_x=\mathrm e^u\sin v\cdot y+\mathrm e^u\cos v\cdot1=\mathrm e^{xy}\big(y\sin(x+y)+\cos(x+y)\big)$；$z_y=\mathrm e^{xy}\big(x\sin(x+y)+\cos(x+y)\big)$。

很多时候函数 $f$ 没有具体表达式，题目只说「$f$ 有连续偏导数」。这时用位置给偏导数起名：$f$ 的第一个位置的偏导数记作 $f'_1$，第二个位置的记作 $f'_2$（有的书写成 $f_u$、$f_v$，意思相同）。这样就不必引入 $u$、$v$ 两个字母。

**例 5**　和例 4 的区别是 $f$ 没有表达式，只能用 $f'_1$、$f'_2$ 表示答案。设 $z=f\big(x^2-y^2,\ \mathrm e^{xy}\big)$，$f$ 有连续偏导数，求 $z_x$、$z_y$。

第一个位置放的是 $x^2-y^2$，第二个位置放的是 $\mathrm e^{xy}$。按树形图，到 $x$ 有两条路径：

$$z_x=f'_1\cdot2x+f'_2\cdot y\,\mathrm e^{xy},\qquad z_y=f'_1\cdot(-2y)+f'_2\cdot x\,\mathrm e^{xy}.$$

答案里的 $f'_1$、$f'_2$ 都是在点 $\big(x^2-y^2,\ \mathrm e^{xy}\big)$ 取的值。

> 设 $z=f\big(xy,\ \dfrac xy\big)$（$y\ne0$，$f$ 有连续偏导数），求 $z_x$、$z_y$。
>
> 答案：$z_x=y\,f'_1+\dfrac1y\,f'_2$，$z_y=x\,f'_1-\dfrac{x}{y^2}\,f'_2$。

最容易错的是一个变量既当中间变量，又当自变量。

**例 6**　和例 5 的区别是：$x$ 在 $f$ 的第一个位置直接出现，同时又藏在第二个位置的 $xy$ 里。设 $z=f(x,\ xy)$，$f$ 有连续偏导数，求 $z_x$。

路径有两条：一条直接走 $z\to x$，另一条走 $z\to xy\to x$。所以

$$z_x=f'_1\cdot1+f'_2\cdot y .$$

这里要分清两个量：$\dfrac{\partial z}{\partial x}$ 是 $z$ 作为 $x$、$y$ 的函数对 $x$ 求导，包括两条路径；而 $f'_1=\dfrac{\partial f}{\partial(\text{第一个位置})}$ 只是 $f$ 自己对第一个位置求导，不含另一条路径。写 $\dfrac{\partial f}{\partial x}$ 时容易把两者混在一起，所以有这种情形时一律用 $f'_1$、$f'_2$。

用具体函数核对：取 $f(s,t)=s^2t$，则 $z=x^2\cdot xy=x^3y$，$z_x=3x^2y$。公式给出 $2s t\cdot1+s^2\cdot y=2x\cdot xy+x^2y=3x^2y$，一致。

有时中间变量依赖的自变量个数不同，例如 $z=f(u,v)$，$u=\varphi(x)$，$v=\psi(x,y)$。树形图仍然成立：到 $x$ 有两条路径，$z_x=f'_1\varphi'(x)+f'_2\psi_x$；到 $y$ 只有一条，$z_y=f'_2\psi_y$。该用几条路径，由图决定，不靠记公式。

树形图不会漏项，可是每道题都要画一棵树，路径一多画图本身就费事。有没有一种写法，不画树也不漏？下一节从全微分入手。

合上书，画出 $z=f(u,v)$、$u=u(x,y)$、$v=v(x,y)$ 的树形图，写出 $z_x$、$z_y$，并说出例 6 里 $z_x$ 与 $f'_1$ 的区别。

### 3. 不管谁是中间变量，$\mathrm dz$ 的写法都一样吗？

C.20.6 的全微分是 $\mathrm dz=z_x\,\mathrm dx+z_y\,\mathrm dy$。如果 $z=f(u,v)$，而 $u$、$v$ 是自变量，则 $\mathrm dz=f'_1\,\mathrm du+f'_2\,\mathrm dv$。问题是：当 $u$、$v$ 本身又是 $x$、$y$ 的函数，这个式子还对吗？

在第 2 节的条件下（$f$ 有连续偏导数，$u$、$v$ 有连续偏导数）答案是对。把第 2 节的两个公式代入 $\mathrm dz=z_x\mathrm dx+z_y\mathrm dy$，整理：

$$\mathrm dz=\big(f'_1u_x+f'_2v_x\big)\mathrm dx+\big(f'_1u_y+f'_2v_y\big)\mathrm dy
=f'_1\underbrace{(u_x\mathrm dx+u_y\mathrm dy)}_{\mathrm du}+f'_2\underbrace{(v_x\mathrm dx+v_y\mathrm dy)}_{\mathrm dv}
=f'_1\,\mathrm du+f'_2\,\mathrm dv .$$

这叫**全微分形式不变性**：无论 $u$、$v$ 是自变量还是中间变量，$\mathrm dz=f'_1\mathrm du+f'_2\mathrm dv$ 的形状不变。这个性质一元时也有（C.5），那里说的是 $\mathrm dy=f'(u)\,\mathrm du$ 对中间变量 $u$ 同样成立。

它的用处是：不必画树，一次就能写出所有偏导数。做法是只对最外层写微分，再把 $\mathrm du$、$\mathrm dv$ 展开成 $\mathrm dx$、$\mathrm dy$，最后合并同类项，$\mathrm dx$ 的系数就是 $z_x$，$\mathrm dy$ 的系数就是 $z_y$。

**方法 3（微分法求偏导）**

1. 写 $\mathrm dz$，只用最外层的偏导数，对中间变量写 $\mathrm du$、$\mathrm dv$。
2. 把 $\mathrm du$、$\mathrm dv$ 都用 $\mathrm dx$、$\mathrm dy$ 展开。
3. 合并，读出 $\mathrm dx$ 与 $\mathrm dy$ 的系数。

**例 7**　结构和例 4 一样，有两个中间变量 $u=x+y$、$v=xy$，只是外层换成幂函数 $u^v$，两个偏导数各要想一步。这道题当然可以画树，现在换方法 3，看写法有什么好处。设 $z=(x+y)^{xy}$，求在点 $(1,1)$ 处的 $z_x$、$z_y$。

令 $u=x+y$，$v=xy$，则 $z=u^v$。对 $u^v$，$\partial_u=v\,u^{v-1}$，$\partial_v=u^v\ln u$（把 $u^v=\mathrm e^{v\ln u}$ 求导得到）。所以

$$\mathrm dz=v\,u^{v-1}\mathrm du+u^v\ln u\,\mathrm dv .$$

在 $(1,1)$ 处，$u=2$，$v=1$，$\mathrm du=\mathrm dx+\mathrm dy$，$\mathrm dv=y\,\mathrm dx+x\,\mathrm dy=\mathrm dx+\mathrm dy$，代入：

$$\mathrm dz=1\cdot2^0(\mathrm dx+\mathrm dy)+2\ln2\,(\mathrm dx+\mathrm dy)=(1+2\ln2)(\mathrm dx+\mathrm dy).$$

所以 $z_x=z_y=1+2\ln2\approx2.386$。

> 设 $z=\mathrm e^{xy}\sin(x+y)$，用方法 3 求 $\mathrm dz$。
>
> 答案：$\mathrm dz=\mathrm e^{xy}\sin(x+y)\,(y\,\mathrm dx+x\,\mathrm dy)+\mathrm e^{xy}\cos(x+y)\,(\mathrm dx+\mathrm dy)$，合并后 $z_x=\mathrm e^{xy}\big(y\sin(x+y)+\cos(x+y)\big)$，$z_y=\mathrm e^{xy}\big(x\sin(x+y)+\cos(x+y)\big)$。

用方法 3 重做例 5：$\mathrm dz=f'_1\,\mathrm d(x^2-y^2)+f'_2\,\mathrm d(\mathrm e^{xy})=f'_1(2x\,\mathrm dx-2y\,\mathrm dy)+f'_2\,\mathrm e^{xy}(y\,\mathrm dx+x\,\mathrm dy)$，读出系数，结果与例 5 相同，而且一步到位。第 6 节还会用到它。

合上书，把第 2 节的两个链式法则公式代入 $\mathrm dz=z_x\,\mathrm dx+z_y\,\mathrm dy$，独立推出 $\mathrm dz=f'_1\,\mathrm du+f'_2\,\mathrm dv$，说明这个写法对中间变量也成立。

不过到这里求的都是一阶偏导。题目常常要二阶偏导，而 $f'_1$、$f'_2$ 本身又是复合函数，二阶该怎么求才不漏项？下一节回答。

### 4. 抽象复合函数的二阶偏导怎么求才不漏项？

接着第 2 节的例 6，先看一个能手算的小情形：$f(s,t)=s^2t$，$z=f(x,xy)=x^3y$。例 6 已经给出 $z_x=f'_1+y\,f'_2$，其中 $f'_1=2st$、$f'_2=s^2$ 在点 $(x,xy)$ 取值，即 $f'_1=2x^2y$、$f'_2=x^2$。

现在想求 $z_{xx}$，也就是对 $f'_1+y\,f'_2$ 再对 $x$ 求一次导。$f'_1$ 的两个位置放的是 $x$ 和 $xy$，$x$ 一动两个位置都动，所以 $f'_1$ 对 $x$ 的导数是 $f''_{11}\cdot1+f''_{12}\cdot y$。代入 $f''_{11}=2t=2xy$、$f''_{12}=2s=2x$，得 $2xy+2xy=4xy$，与直接对 $f'_1=2x^2y$ 求导的结果一致。

这就是一般情形的做法：$f'_1$、$f'_2$ 仍是 $u$、$v$ 的函数，对 $x$ 或 $y$ 再求偏导时，要对它们再用一次链式法则。漏项几乎都是忘了这一点。

二阶偏导数记号：$f''_{11}$ 是对第一个位置求两次，$f''_{12}$ 是先对第一个位置再对第二个位置，$f''_{22}$ 是对第二个位置求两次。设二阶偏导数连续，则 $f''_{12}=f''_{21}$（C.20.8），所以两个混合偏导的求导次序不用区分，合并时直接写成同一项。

**方法 4（抽象函数的二阶偏导）**

1. 先求一阶偏导，用 $f'_1$、$f'_2$ 写出。
2. 对一阶偏导再求偏导。每一项是「系数」乘「$f'_i$」：乘积法则，系数求导一项，$f'_i$ 求导一项。
3. 对 $f'_i$ 求导时，把它当作和 $f$ 同样的复合函数：$f'_i$ 的两个位置仍是 $u$、$v$，所以 $\dfrac{\partial f'_i}{\partial x}=f''_{i1}\,u_x+f''_{i2}\,v_x$。
4. 合并 $f''_{12}$ 与 $f''_{21}$。

**例 8**　和例 5 相比，仍是 $f(\cdot,\cdot)$ 的复合，但这次要对一阶偏导再求一次偏导，其中 $f'_1$、$f'_2$ 自己也要用链式法则，就是上面小情形里的那一步。设 $z=f(xy,\ x+y)$，求 $\dfrac{\partial^2z}{\partial x\,\partial y}$，$f$ 有连续二阶偏导数。

思路：先求 $z_x$，再对 $y$ 求导。第一个位置是 $xy$，第二个位置是 $x+y$。

第一步，$z_x=f'_1\cdot y+f'_2\cdot1=y\,f'_1+f'_2$。

第二步，对 $y$ 求偏导。第一项 $y\,f'_1$ 是乘积，求导得 $f'_1+y\cdot\dfrac{\partial f'_1}{\partial y}$。其中 $\dfrac{\partial f'_1}{\partial y}$ 是 $f'_1(xy,x+y)$ 对 $y$ 的导数，按链式法则：

$$\frac{\partial f'_1}{\partial y}=f''_{11}\cdot x+f''_{12}\cdot1 .$$

第二项 $f'_2$ 同理：$\dfrac{\partial f'_2}{\partial y}=f''_{21}\cdot x+f''_{22}\cdot1$。

第三步，合并，用 $f''_{12}=f''_{21}$：

$$z_{xy}=f'_1+y\big(x\,f''_{11}+f''_{12}\big)+x\,f''_{12}+f''_{22}=f'_1+xy\,f''_{11}+(x+y)\,f''_{12}+f''_{22}.$$

核对：取 $f(s,t)=s^2t$，则 $f'_1=2st$，$f''_{11}=2t$，$f''_{12}=2s$，$f''_{22}=0$，代入上式得 $2xy(x+y)+xy\cdot2(x+y)+(x+y)\cdot2xy=6xy(x+y)$。而直接算 $z=x^2y^2(x+y)=x^3y^2+x^2y^3$，$z_{xy}=6x^2y+6xy^2=6xy(x+y)$，一致。

> 设 $z=f(x,\ xy)$，求 $z_{xx}$。
>
> 答案：$z_x=f'_1+y\,f'_2$。再对 $x$ 求导：$z_{xx}=\big(f''_{11}+y\,f''_{12}\big)+y\big(f''_{21}+y\,f''_{22}\big)=f''_{11}+2y\,f''_{12}+y^2f''_{22}$。

**例 9**　例 8 有两个中间变量。这次只有一个中间变量，写起来更短。设 $z=f(x^2+y^2)$，$f$ 二阶可导。求 $z_{xx}+z_{yy}$，并验证在 $(x,y)\ne(0,0)$ 的区域内 $z=\ln(x^2+y^2)$ 满足 $z_{xx}+z_{yy}=0$。

第一步，令 $s=x^2+y^2$，则 $z_x=f'(s)\cdot2x$。再对 $x$ 求导，$f'(s)$ 要用链式法则：

$$z_{xx}=2f'(s)+2x\cdot f''(s)\cdot2x=2f'(s)+4x^2f''(s).$$

第二步，$y$ 与 $x$ 的地位对称，$z_{yy}=2f'(s)+4y^2f''(s)$。相加：

$$z_{xx}+z_{yy}=4f'(s)+4(x^2+y^2)f''(s)=4\big(f'(s)+s\,f''(s)\big).$$

第三步，取 $f=\ln s$，则 $f'=\frac1s$，$f''=-\frac1{s^2}$，于是 $f'+sf''=\frac1s-\frac1s=0$。所以在 $(x,y)\ne(0,0)$ 的区域内，$\ln(x^2+y^2)$ 满足 $z_{xx}+z_{yy}=0$。

到这里，函数无论抽象与否，都写成了 $z=\cdots$ 的样子。可有的函数根本写不成这个样子，手里只有一个把变量绑在一起的方程。这样的方程什么时候确定一个函数？下一节回答。

合上书，说明例 8 里为什么对 $f'_1$ 求偏导还要再乘 $x$ 和 $1$，并独立写出 $z=f(x,xy)$ 的 $z_{xx}$。

### 5. 方程 $F(x,y)=0$ 什么时候确定一个函数，它的导数是多少？

前面的函数都有显式表达式。现在看一类「藏在方程里」的函数。单位圆 $x^2+y^2=1$：在点 $(0,1)$ 附近，$y=\sqrt{1-x^2}$，圆的这一小段是一个函数的图像；在点 $(1,0)$ 附近就不行了，对每个 $x$（略小于 1）都有上下两个 $y$，一个 $x$ 对应两个值，不是函数。但在 $(1,0)$ 附近，把 $x$ 写成 $y$ 的函数 $x=\sqrt{1-y^2}$ 是可以的。

所以一个方程能不能「解出」$y$，要看点的位置。记 $F=x^2+y^2-1$，则 $F_y=2y$：在 $(0,1)$ 处 $F_y=2\ne0$，在 $(1,0)$ 处 $F_y=0$，圆在 $(1,0)$ 处的切线是竖直的。

![圆在 $(0,1)$ 附近是 $y=\sqrt{1-x^2}$ 的图像，切线（虚线）水平；在 $(1,0)$ 处切线（虚线）竖直，$x$ 略小于 $1$ 时同一个 $x$ 对应上下两个 $y$](fig/C21-n2.pdf){width=55%}

**定理（隐函数存在定理）**　设 $F(x,y)$ 在点 $(x_0,y_0)$ 的某个邻域内有连续的偏导数，$F(x_0,y_0)=0$，并且 $F_y(x_0,y_0)\ne0$。那么存在 $(x_0,y_0)$ 的一个小矩形，使得对 $x_0$ 附近的每个 $x$，方程 $F(x,y)=0$ 在矩形内恰有一个解 $y=y(x)$。这个函数满足 $y(x_0)=y_0$，有连续的导数，并且

$$\frac{\mathrm dy}{\mathrm dx}=-\frac{F_x}{F_y}.$$

证明分两部分：先说明为什么 $y$ 存在，再求导数。

**存在性。** 想法是：$F_y\ne0$ 说明固定 $x$ 时 $F$ 是 $y$ 的严格单调函数，单调函数穿过 0 恰好一次。

1. $F_y(x_0,y_0)\ne0$，不妨设为正（负的情形把 $F$ 换成 $-F$）。$F_y$ 连续，所以在 $(x_0,y_0)$ 的一个小矩形 $R$ 里 $F_y>0$。于是对固定的 $x$，$F(x,y)$ 关于 $y$ 严格递增：对 $R$ 里的 $y_1<y_2$，一元的拉格朗日中值定理给出 $F(x,y_2)-F(x,y_1)=F_y(x,\xi)(y_2-y_1)>0$，其中 $\xi$ 在 $y_1$、$y_2$ 之间。

2. $F(x_0,y_0)=0$，递增说明取小正数 $\delta$ 后，$F(x_0,y_0-\delta)<0<F(x_0,y_0+\delta)$。$F$ 连续，所以 $x$ 在 $x_0$ 附近时，仍有 $F(x,y_0-\delta)<0<F(x,y_0+\delta)$。

3. 对这样的每个 $x$，$F(x,\cdot)$ 在 $[y_0-\delta,y_0+\delta]$ 上连续，两端异号，由介值定理（C.3）有一个零点；又严格递增，零点只有一个，记作 $y(x)$。

**连续性。** 求导数要用到「$\Delta x\to0$ 时 $\Delta y\to0$」，所以先说明 $y(x)$ 连续。任给更小的 $0<\delta'\le\delta$，按第 2 步同样的理由，$x$ 足够靠近 $x_0$ 时 $F(x,y_0-\delta')<0<F(x,y_0+\delta')$，于是区间 $[y_0-\delta',y_0+\delta']$ 里有 $F(x,\cdot)$ 的零点。矩形内的零点只有一个，所以它就是 $y(x)$，即 $|y(x)-y_0|\le\delta'$。$\delta'$ 可以任意小，这就是 $y$ 在 $x_0$ 连续；邻域里其他点处 $F_y>0$ 仍成立，同样处理。

**求导数。** 设 $x$ 有改变量 $\Delta x$，对应 $y$ 的改变量是 $\Delta y$。两点都满足方程，所以 $F(x+\Delta x,y+\Delta y)-F(x,y)=0$。为了把 $\dfrac{\Delta y}{\Delta x}$ 分离出来，把这个差拆成两段，每段只动一个变量，各用一次一元的中值定理：

$$0=\big[F(x+\Delta x,y+\Delta y)-F(x,y+\Delta y)\big]+\big[F(x,y+\Delta y)-F(x,y)\big]=F_x(P_1)\,\Delta x+F_y(P_2)\,\Delta y ,$$

其中 $P_1$ 在 $(x,y+\Delta y)$ 与 $(x+\Delta x,y+\Delta y)$ 的连线上，$P_2$ 在 $(x,y)$ 与 $(x,y+\Delta y)$ 的连线上。移项得 $\dfrac{\Delta y}{\Delta x}=-\dfrac{F_x(P_1)}{F_y(P_2)}$。$\Delta x\to0$ 时 $\Delta y\to0$（连续性），$P_1$、$P_2$ 都趋于 $(x,y)$，而 $F_x$、$F_y$ 连续、$F_y\ne0$，所以比值趋于 $-\dfrac{F_x}{F_y}$。这说明 $y$ 可导，导数就是 $-\dfrac{F_x}{F_y}$；分子分母都连续，分母不为 $0$，所以导数连续。

实际做题时不必背这个过程。公式的来历还可以更短地看：已知 $y$ 可导并满足方程，则 $F(x,y(x))\equiv0$。恒为 0 的函数导数也恒为 0。用第 1 节的链式法则求导：

$$F_x\cdot1+F_y\cdot y'=0,\qquad\text{所以}\quad y'=-\frac{F_x}{F_y}.$$

定理里的条件各有各的用处。$F_y\ne0$ 保证单调，所以才能解出 $y$：去掉它，$F=x^2-y^2$ 在原点处两条直线交叉，方程在原点附近不是函数。但 $F_y=0$ 时也可能仍有光滑的解，例如 $F=(y-x)^3$ 在原点 $F_y=0$，方程却等价于 $y=x$；所以 $F_y\ne0$ 是充分条件，不是必要条件。条件 $F(x_0,y_0)=0$ 也不能少：取 $F=y-1$，指定点 $(0,0)$，$F_y=1\ne0$，但方程确定的函数是 $y=1$，不可能满足 $y(0)=0$。

**方法 5（隐函数求导）**

1. 把方程整理成 $F(x,y)=0$。
2. 求 $F_x$、$F_y$，检查所求点处 $F_y\ne0$。
3. $\dfrac{\mathrm dy}{\mathrm dx}=-\dfrac{F_x}{F_y}$。点的坐标要在求出偏导以后再代入，$y$ 不需要解出来。
4. 求二阶导数：对 $y'=-\dfrac{F_x}{F_y}$ 再对 $x$ 求导，把 $y$ 看成 $x$ 的函数，遇到 $y'$ 就用步骤 3 的结果代入。

**例 10**　前面的函数都能写成 $z=\cdots$ 的样子，这道题的 $y$ 没有写成 $x$ 的式子，只能用 $F(x,y(x))\equiv0$ 配合第 1 节的链式法则。求笛卡尔叶形线 $x^3+y^3=3xy$ 在点 $\big(\frac32,\frac32\big)$ 处的 $\dfrac{\mathrm dy}{\mathrm dx}$。

第一步，验证点在曲线上：$\frac{27}{8}+\frac{27}{8}=\frac{27}4$，$3\cdot\frac94=\frac{27}4$，成立。

第二步，$F=x^3+y^3-3xy$，$F_x=3x^2-3y$，$F_y=3y^2-3x$。在 $\big(\frac32,\frac32\big)$：$F_x=\frac{27}4-\frac92=\frac94$，$F_y=\frac94\ne0$。

第三步，$\dfrac{\mathrm dy}{\mathrm dx}=-\dfrac{9/4}{9/4}=-1$。

由斜率 $-1$ 得切线 $x+y=3$。这条切线与对称轴 $y=x$ 垂直，和曲线关于 $y=x$ 对称的事实相符。

一个自然的错误做法，是把 $y$ 当常数，只对 $x$ 求偏导，把 $F_x=\frac94$ 当成斜率。这样漏掉了 $y$ 随 $x$ 变化的那一项 $F_y\,y'$：$x$ 走一步，$y$ 也跟着走一步，两部分加起来才是 $0$。

![图中画出第一象限的闭合部分。叶形线 $x^3+y^3=3xy$ 关于虚线 $y=x$ 对称；点 $\big(\frac32,\frac32\big)$ 在对称轴上，那里的切线（实线）斜率为 $-1$，与对称轴垂直](fig/C21-n4.pdf){width=55%}

> 求曲线 $xy+\ln y=1$ 在点 $(1,1)$ 处的 $\dfrac{\mathrm dy}{\mathrm dx}$。
>
> 答案：$F=xy+\ln y-1$，$F_x=y=1$，$F_y=x+\frac1y=2\ne0$，所以 $\dfrac{\mathrm dy}{\mathrm dx}=-\frac12$。

**例 11**　例 10 只要一阶导数。这次要二阶，所以要在 $y'$ 的式子上再对 $x$ 求导，并且每次遇到 $y'$ 都用方法 5 的结果代回。设 $y=y(x)$ 由 $\mathrm e^y+xy=\mathrm e$ 确定，求 $y'(0)$、$y''(0)$。

第一步，$x=0$ 时 $\mathrm e^y=\mathrm e$，所以 $y=1$。

第二步，$F=\mathrm e^y+xy-\mathrm e$，$F_x=y$，$F_y=\mathrm e^y+x$，所以

$$y'=-\frac{y}{\mathrm e^y+x},\qquad y'(0)=-\frac1{\mathrm e}.$$

第三步，对 $y'=-\dfrac{y}{\mathrm e^y+x}$ 用商的求导法则，$y$ 是 $x$ 的函数，$(\mathrm e^y+x)'=\mathrm e^yy'+1$：

$$y''=-\frac{y'(\mathrm e^y+x)-y(\mathrm e^yy'+1)}{(\mathrm e^y+x)^2}.$$

第四步，代入 $x=0$，$y=1$，$y'=-\frac1{\mathrm e}$：分子 $=-\frac1{\mathrm e}\cdot\mathrm e-1\cdot(\mathrm e\cdot(-\tfrac1{\mathrm e})+1)=-1-0=-1$，所以 $y''(0)=-\dfrac{-1}{\mathrm e^2}=\dfrac1{\mathrm e^2}$。

隐函数求导在经济学里的一个标准用法，是无差异曲线的斜率。下面这个例子需要的背景很少：一个人对两种商品的「满意度」是 $U(x,y)$，$x$、$y$ 是两种商品的数量；满意度相同的所有 $(x,y)$ 连成一条曲线，叫无差异曲线（C.20.1）。

**例 12**　和例 10 一样用 $y'=-F_x/F_y$，数据换成一条满意度的等值线，这次要读出斜率的含义。某人对苹果数量 $x$ 与梨的数量 $y$ 的满意度是 $U(x,y)=\sqrt{xy}$。求过点 $(4,9)$ 的无差异曲线在该点的斜率，并解释它的含义。

无差异曲线是 $U(x,y)=6$（$\sqrt{36}=6$）。令 $F=\sqrt{xy}-6$，则 $F_x=\dfrac{y}{2\sqrt{xy}}$，$F_y=\dfrac{x}{2\sqrt{xy}}$。在 $(4,9)$：$F_x=\dfrac9{12}=\dfrac34$，$F_y=\dfrac4{12}=\dfrac13$，所以

$$\frac{\mathrm dy}{\mathrm dx}=-\frac{F_x}{F_y}=-\frac{3/4}{1/3}=-\frac94 .$$

含义：在这一点附近，苹果增加一个很小的量 $\Delta x$，梨可以相应减少约 $\frac94\Delta x$（$\Delta y\approx-\frac94\Delta x$）而满意度几乎不变。这是微小变化的比率，不是说真的多拿 1 单位苹果就恰好少 $\frac94$ 单位梨。这个比值叫边际替代率。

这一节的方程里只有 $x$、$y$ 两个变量，一个方程管一个函数。变量有三个时，比如球面，一个方程能管住一个两元函数 $z(x,y)$ 吗？下一节回答。

合上书，写出隐函数求导公式的推导（对 $F(x,y(x))\equiv0$ 求导），说明 $F_y\ne0$ 在定理里负责什么，并写出例 11 为什么要对 $y'$ 的表达式再求一次导。

### 6. $F(x,y,z)=0$ 确定 $z=z(x,y)$ 时，偏导数怎么求？

先看一个能手算的情形：球面 $x^2+y^2+z^2=4$ 在点 $(0,0,2)$ 附近，$z=\sqrt{4-x^2-y^2}$，所以 $z_x=\dfrac{-x}{\sqrt{4-x^2-y^2}}=-\dfrac xz$。另一方面，记 $F=x^2+y^2+z^2-4$，则 $-\dfrac{F_x}{F_z}=-\dfrac{2x}{2z}=-\dfrac xz$，两者相同。这就是上一节「恒为 $0$ 的函数求导」搬到三个变量的样子。一般的定理如下。

**定理（三个变量的隐函数存在定理）**　设 $F(x,y,z)$ 在点 $P_0=(x_0,y_0,z_0)$ 附近有连续偏导数，$F(P_0)=0$，并且 $F_z(P_0)\ne0$。那么存在 $P_0$ 的一个小长方体，使得对 $(x_0,y_0)$ 附近的每个 $(x,y)$，方程 $F=0$ 在长方体内恰有一个解 $z=z(x,y)$。这个函数满足 $z(x_0,y_0)=z_0$，有连续偏导数。

理由和第 5 节相同：$F_z\ne0$ 且连续（不妨设为正，负的情形把 $F$ 换成 $-F$），所以在 $P_0$ 附近的小长方体里，固定 $(x,y)$ 时 $F$ 关于 $z$ 严格递增；$F(x_0,y_0,z_0\mp\delta)$ 异号，由连续性，$(x,y)$ 在 $(x_0,y_0)$ 附近时仍异号，再用介值定理与单调性，得到唯一的 $z(x,y)$。第 5 节的连续性论证也照样做，只是 $x$ 靠近 $x_0$ 换成点 $(x,y)$ 靠近 $(x_0,y_0)$，这样 $z(x,y)$ 关于 $(x,y)$ 连续，而 $z_x=-F_x/F_z$ 是连续函数的复合，所以偏导数连续。求偏导数时固定 $y$，就剩 $x$、$z$ 两个变量，回到上一节。

求偏导数有两个办法。

**方法 6a（公式法）**　$F(x,y,z(x,y))\equiv0$，对 $x$ 求偏导，$y$ 当常数，用链式法则，$z$ 是中间变量，$x$ 又是自变量（像第 2 节例 6）：

$$F_x\cdot1+F_z\cdot z_x=0,\qquad z_x=-\frac{F_x}{F_z},\qquad\text{同理}\quad z_y=-\frac{F_y}{F_z}.$$

**方法 6b（直接对方程求偏导）**　不引入 $F$，把方程两边对 $x$ 求偏导，$z$ 当作 $x$、$y$ 的函数，然后从得到的方程里解出 $z_x$。需要二阶偏导时，这个办法比套公式更稳。

**例 13**　和上面的球面相比，这次球心移到了 $(0,0,2)$，原点落在球面上。一阶用方法 6a，二阶改用方法 6b，对照两种写法。设 $z=z(x,y)$ 由 $x^2+y^2+z^2=4z$ 在点 $(0,0,0)$ 附近确定，求 $z_x$ 与 $z_{xx}$。

第一步，$F=x^2+y^2+z^2-4z$，$F_x=2x$，$F_z=2z-4$。在 $(0,0,0)$，$F_z=-4\ne0$，可以解出 $z$。公式：

$$z_x=-\frac{2x}{2z-4}=\frac{x}{2-z}.$$

第二步，求 $z_{xx}$，改用方法 6b。方程两边对 $x$ 求偏导，$z$ 是 $x$、$y$ 的函数：

$$2x+2z\,z_x=4z_x .$$

这是 $z_x$ 满足的方程，解出来就是第一步的 $z_x=\dfrac{x}{2-z}$。再对 $x$ 求偏导，左边 $2z\,z_x$ 用乘积法则，其中 $z$ 又对 $x$ 求导：

$$2+2(z_x)^2+2z\,z_{xx}=4z_{xx},\qquad\text{所以}\quad z_{xx}=\frac{1+(z_x)^2}{2-z}.$$

这样不必先把 $z_x$ 化成分式再求商的导数。把 $z_x=\dfrac{x}{2-z}$ 代入，得 $z_{xx}=\dfrac{(2-z)^2+x^2}{(2-z)^3}$。

在 $(0,0,0)$：$z_x=0$，$z_{xx}=\dfrac48=\dfrac12$。

核对：原方程等价于 $x^2+y^2+(z-2)^2=4$，是球心 $(0,0,2)$、半径 2 的球面，原点附近的下半球是 $z=2-\sqrt{4-x^2-y^2}$。令 $y=0$，$z=2-\sqrt{4-x^2}$，$z_{xx}=\dfrac{4}{(4-x^2)^{3/2}}$，在 $x=0$ 为 $\dfrac48=\dfrac12$，一致。

> 设 $z=z(x,y)$ 在满足 $\mathrm e^{z_0}=x_0y_0z_0$ 且 $z_0\ne1$ 的点附近由 $\mathrm e^z=xyz$ 确定，求 $z_x$。
>
> 答案：$F=\mathrm e^z-xyz$，$F_x=-yz$，$F_z=\mathrm e^z-xy$，所以 $z_x=\dfrac{yz}{\mathrm e^z-xy}$。因为 $\mathrm e^z=xyz$，分母 $\mathrm e^z-xy=xyz-xy=xy(z-1)$（$xy\ne0$，否则 $\mathrm e^z=0$ 不可能），所以 $z_{0}\ne1$ 保证分母非零，$z_x=\dfrac{z}{x(z-1)}$。

一个方程里有三个变量时，每个变量都可以做函数，这时偏导数记号里的「谁对谁」就要小心了。设 $F$ 有连续偏导数，点 $P_0$ 满足 $F(P_0)=0$，并且 $F_x$、$F_y$、$F_z$ 在 $P_0$ 都不为零。这时 $F=0$ 在 $P_0$ 附近既能解出 $x=x(y,z)$，也能解出 $y=y(z,x)$ 和 $z=z(x,y)$。三个偏导数是

$$\frac{\partial x}{\partial y}=-\frac{F_y}{F_x},\qquad\frac{\partial y}{\partial z}=-\frac{F_z}{F_y},\qquad\frac{\partial z}{\partial x}=-\frac{F_x}{F_z}.$$

乘起来，分子分母全部约掉，剩下三个负号：

$$\frac{\partial x}{\partial y}\cdot\frac{\partial y}{\partial z}\cdot\frac{\partial z}{\partial x}=-1 .$$

很多人第一次见到会觉得别扭，因为符号长得像分数，似乎应该约成 $+1$。但是每个偏导数里「固定」的变量不同：$\frac{\partial x}{\partial y}$ 固定 $z$，$\frac{\partial y}{\partial z}$ 固定 $x$，$\frac{\partial z}{\partial x}$ 固定 $y$。它们不是同一个除法里的分子分母，不能约。用平面 $x+2y+3z=0$ 验证：$\frac{\partial x}{\partial y}=-2$，$\frac{\partial y}{\partial z}=-\frac32$，$\frac{\partial z}{\partial x}=-\frac13$，乘起来是 $-1$。

**例 14**　和例 13 不同，方程里含有看不见的函数 $F$，求不出偏导数的具体值，只能证明一个关系，要用第 3 节的全微分形式不变性。设 $z=z(x,y)$ 由 $F\big(x+\frac zy,\ y+\frac zx\big)=0$ 确定，$F$ 有连续偏导数，并且 $\dfrac{F_u}{y}+\dfrac{F_v}{x}\ne0$（保证方程确实确定了 $z$，下面第五步会看到它的来历），证明

$$x\,z_x+y\,z_y=z-xy .$$

思路：对方程两边取全微分，用第 3 节的方法 3，不用分别对 $x$、$y$ 求导。

第一步，记 $u=x+\frac zy$，$v=y+\frac zx$，则 $F_u\,\mathrm du+F_v\,\mathrm dv=0$。

第二步，展开 $\mathrm du$、$\mathrm dv$，$z$ 是 $x$、$y$ 的函数，所以 $\mathrm dz=z_x\mathrm dx+z_y\mathrm dy$：

$$\mathrm du=\mathrm dx+\frac{\mathrm dz}{y}-\frac{z}{y^2}\mathrm dy,\qquad \mathrm dv=\mathrm dy+\frac{\mathrm dz}{x}-\frac{z}{x^2}\mathrm dx .$$

第三步，代入后分别读出 $\mathrm dx$、$\mathrm dy$ 的系数，各自等于 0：

$$F_u\Big(1+\frac{z_x}y\Big)+F_v\Big(-\frac z{x^2}+\frac{z_x}x\Big)=0,\qquad
F_u\Big(-\frac z{y^2}+\frac{z_y}y\Big)+F_v\Big(1+\frac{z_y}x\Big)=0 .$$

第四步，要证的式子含 $xz_x+yz_y$，所以把第一式乘 $x$、第二式乘 $y$ 再相加，凑出这个组合。然后把含 $F_u$ 的部分与含 $F_v$ 的部分各自整理：

$$F_u\Big(x+\frac{x z_x+y z_y}{y}-\frac zy\Big)+F_v\Big(y+\frac{xz_x+yz_y}{x}-\frac zx\Big)=0 .$$

提出公因式：含 $F_u$ 的括号等于 $\frac1y\,(xz_x+yz_y-z+xy)$，含 $F_v$ 的括号等于 $\frac1x\,(xz_x+yz_y-z+xy)$，所以

$$\Big(\frac{F_u}{y}+\frac{F_v}{x}\Big)\big(xz_x+yz_y-z+xy\big)=0 .$$

第五步，当 $\dfrac{F_u}y+\dfrac{F_v}x\ne0$ 时（把方程左边记作 $G(x,y,z)=F\big(x+\frac zy,y+\frac zx\big)$，这个量正是 $G_z$，也就是隐函数存在定理要求的 $G_z\ne0$），括号等于 0，所以 $xz_x+yz_y=z-xy$。

这类题的难点是抽象函数 $F$ 看不见，只能靠「恒等于 0 的函数，全微分也是 0」往前推。每步的依据：第一步用方法 3，第二步用 $\mathrm dz$ 的展开，第三步用 $\mathrm dx$、$\mathrm dy$ 互相独立。

这一节的方程仍只有一个，确定的函数也只有一个。要是有两个方程，同时要管两个未知函数呢？下一节从二次方程的两个根入手。

合上书，写出 $F(x,y,z)=0$ 时 $z_x$、$z_y$ 的公式，并解释为什么 $\frac{\partial x}{\partial y}\frac{\partial y}{\partial z}\frac{\partial z}{\partial x}$ 等于 $-1$ 而不是 $1$。

### 7. 两个方程确定两个函数时，怎么求导？

最后一类：未知函数不止一个。二次方程 $t^2-xt+y=0$ 有两个不等的实根 $u>v$，系数 $x$、$y$ 稍微变一变，两个根变得多快？求根公式带着根号。换一个角度，用韦达定理：

$$u+v=x,\qquad uv=y .$$

这是两个方程，四个变量 $x,y,u,v$。给定 $x$、$y$ 就定下了 $u$、$v$，所以 $u$、$v$ 是 $x$、$y$ 的函数 $u(x,y)$、$v(x,y)$。

为了求 $u_x$、$v_x$，把 $y$ 固定，两个方程都对 $x$ 求偏导（第二个方程是乘积，按乘积法则展开）：

$$u_x+v_x=1,\qquad v\,u_x+u\,v_x=0 .$$

未知数 $u_x$、$v_x$ 都只以一次出现，这是一个二元一次方程组。由第一个式子 $v_x=1-u_x$，代入第二个得 $v\,u_x+u-u\,u_x=0$，于是

$$u_x=\frac{u}{u-v},\qquad v_x=\frac{-v}{u-v}.$$

用 $x=3$、$y=2$ 核对：$t^2-3t+2=0$ 的根是 $u=2$、$v=1$，上式给出 $u_x=2$，$v_x=-1$。直接对 $u=\dfrac{x+\sqrt{x^2-4y}}2$ 求导，$u_x=\dfrac12\Big(1+\dfrac{x}{\sqrt{x^2-4y}}\Big)=\dfrac12(1+3)=2$，一致。

分母 $u-v$ 从哪里来？它是方程组左边系数排成的二阶行列式：

$$\begin{vmatrix}1&1\\ v&u\end{vmatrix}=u-v .$$

两根相等时它等于 0，上面的方程组不能唯一解出 $u_x$、$v_x$。这时 $x^2-4y=0$，而在这样的点的任意邻域里都有 $x^2-4y<0$ 的点，那里方程没有实根，所以在整个邻域里得不到两个实根的可微函数。

一般地，方程组 $F(x,y,u,v)=0$、$G(x,y,u,v)=0$ 想确定 $u(x,y)$、$v(x,y)$，关键是行列式

$$J=\frac{\partial(F,G)}{\partial(u,v)}=\begin{vmatrix}F_u&F_v\\ G_u&G_v\end{vmatrix}=F_uG_v-F_vG_u ,$$

读作「$F$、$G$ 对 $u$、$v$ 的雅可比式」。它是把方程组两边求导以后得到的二元一次方程组的系数行列式，所以 $J\ne0$ 时方程组有唯一解（C.19.5 里二阶行列式的记号 $ad-bc$）。

**定理（方程组的隐函数定理）**　设 $F$、$G$ 在点 $P_0=(x_0,y_0,u_0,v_0)$ 附近有连续偏导数，$F(P_0)=G(P_0)=0$，并且 $J(P_0)\ne0$。那么在 $(x_0,y_0)$ 附近，方程组恰好确定一组函数 $u(x,y)$、$v(x,y)$，满足 $u(x_0,y_0)=u_0$、$v(x_0,y_0)=v_0$，并且有连续偏导数。

为什么 $J\ne0$ 就够？思路和解二元一次方程组的代入消元一样，先解出 $v$，再解出 $u$，一共两次「解出」，每次用第 5 节的定理（允许把 $x,y,u$ 一起当自变量，理由见第 6 节）。第一次要 $G_v\ne0$，第二次要 $H_u\ne0$，下面逐一检查。

1. $J\ne0$ 说明 $G_u$、$G_v$ 不全为 0，不妨设 $G_v\ne0$（若 $G_v=0$，则 $G_u\ne0$，把 $u$、$v$ 的角色互换，下面的论证完全对称）。把 $x,y,u$ 当作自变量，由第 5 节的定理，$G=0$ 解出 $v=\varphi(x,y,u)$，并且 $\varphi_u=-\dfrac{G_u}{G_v}$。

2. 把它代入 $F$，得到只含未知数 $u$ 的方程 $H(x,y,u)=F\big(x,y,u,\varphi(x,y,u)\big)=0$。再用一次定理，要检查 $H_u\ne0$。由链式法则：

$$H_u=F_u+F_v\varphi_u=F_u-\frac{F_vG_u}{G_v}=\frac{F_uG_v-F_vG_u}{G_v}=\frac{J}{G_v}\ne0 .$$

3. 所以 $H=0$ 确定 $u(x,y)$，代回 $\varphi$ 得到 $v(x,y)$。

**方法 7（方程组两边求导）**

1. 几个方程确定几个函数，通常题目会指明谁是自变量、谁是函数。
2. 每个方程两边对同一个自变量求导，函数按链式法则带上它的导数。
3. 得到关于这些导数的一次方程组，其系数行列式就是 $J$，$J\ne0$ 时解出。
4. 只要某个点的值时，先把点的坐标代进方程组再解，数字方程组好解得多。

**例 15**　和上面的韦达问题相比，方程换成了几何的（球面与平面），自变量只有一个 $x$，所以每个方程只求一次导。方程组 $x^2+y^2+z^2=6$，$x+y+z=0$ 在点 $(1,-2,1)$ 附近确定 $y=y(x)$、$z=z(x)$，求 $y'(1)$、$z'(1)$。

思路：两个方程，三个变量，所以一个自变量 $x$、两个函数 $y$、$z$。

第一步，两个方程对 $x$ 求导，$y$、$z$ 是 $x$ 的函数，$y^2$ 的导数是 $2yy'$：

$$2x+2yy'+2zz'=0,\qquad 1+y'+z'=0 .$$

第二步，代入 $x=1$，$y=-2$，$z=1$，并把第一个方程除以 2：

$$-2y'+z'=-1,\qquad y'+z'=-1 .$$

第三步，系数行列式 $(-2)\cdot1-1\cdot1=-3\ne0$，可以解。两式相减得 $-3y'=0$，所以

$$y'(1)=0,\qquad z'(1)=-1 .$$

这条曲线是球面与平面相交的圆，C.23 第 3 节还会用到这个结果。

> 极坐标 $x=r\cos\theta$，$y=r\sin\theta$ 在 $r>0$ 的点附近确定 $r(x,y)$、$\theta(x,y)$（$\theta$ 取连续变化的一支）。不反解，求 $r_x$ 与 $\theta_x$。
>
> 答案：两式对 $x$ 求导，得 $1=r_x\cos\theta-r\sin\theta\,\theta_x$，$0=r_x\sin\theta+r\cos\theta\,\theta_x$。系数行列式 $r\cos^2\theta+r\sin^2\theta=r\ne0$。解得 $r_x=\cos\theta$，$\theta_x=-\dfrac{\sin\theta}{r}$。

**回到开头的问题。** 开头问了两件事，现在都能算出来。第一件，例 3 已经算过：损失对 $w$ 的导数是 $192$，由两条路径各乘一次再相加得到，反向传播在每个参数上做的就是这件事。

第二件，用一个小模型：每件商品向买方征税 $t$ 元，卖方到手的价格是 $p$，买方实际付 $p+t$。需求量是 $12-(p+t)$，供给量是 $p^2$，均衡时两者相等，即

$$F(p,t)=p^2+p+t-12=0 .$$

$t=0$ 时 $p=3$。均衡价格 $p$ 由这个方程隐含地确定，用第 5 节的公式，$F_p=2p+1=7$，$F_t=1$，所以

$$\frac{\mathrm dp}{\mathrm dt}=-\frac{F_t}{F_p}=-\frac17 .$$

每件多征 $1$ 元税，卖方到手价约降 $\frac17$ 元，买方实际多付约 $1-\frac17=\frac67$ 元。这里 $p$ 其实能解出来，$p=\frac{-1+\sqrt{49-4t}}2$，求导同样得 $-\frac17$，可以核对公式；但方程再复杂一些就解不出 $p$，公式仍然管用。

合上书，用韦达定理的例子重新推一遍 $u_x$，并说明两根相等时为什么推不下去。

### 本章小结

主线上，C.20 说「曲面放大了看是一张平面」，本章说明复合以后、以及藏在方程里的函数，放大了看仍是线性的：系数沿路径相乘相加（链式法则），或由方程恒为 0 求导解出（隐函数）。下面一章用它们求方向导数和梯度。

「谁推出谁」的关系图在 C.20.7 画过，本章补上与求导有关的两条（本章新增）：

- 偏导连续 $\Rightarrow$ 外层可微，再加内层可导（可微），则链式法则成立。第 1 节的反例 $\dfrac{x^2y}{x^2+y^2}$ 说明只有偏导存在，链式法则可以失效；
- 在 $F$ 偏导数连续、指定点满足 $F=0$ 时，$F_y\ne0$ $\Rightarrow$ 局部有唯一的可导隐函数；反过来不成立，例如 $(y-x)^3=0$ 在原点 $F_y=0$，仍确定 $y=x$。

| 方法 | 什么时候用 | 对应题号 |
|---|---|---|
| 方法 1（全导数） | $z$ 经过 $x,y$ 只依赖一个变量 $t$，$\dfrac{\mathrm dz}{\mathrm dt}=f_xx'+f_yy'$ | 例 1–3；C21-01、06、07、10、12 |
| 方法 2（树形图） | 中间变量、自变量都有好几个，或含抽象函数 $f'_1,f'_2$；一个变量既当中间变量又当自变量时小心路径 | 例 4–6；C21-02、07 |
| 方法 3（微分法） | 一次写出 $\mathrm dz$，读出所有偏导；含抽象函数 $F$ 的证明题 | 例 7、14；C21-03、10 |
| 方法 4（抽象函数的二阶偏导） | 对 $f'_i$ 再用链式法则，合并 $f''_{12}=f''_{21}$ | 例 8、9；C21-08、11 |
| 方法 5（隐函数求导） | $F(x,y)=0$，$F_y\ne0$；$y'=-\dfrac{F_x}{F_y}$；二阶再对 $x$ 求导 | 例 10–12；C21-04、05 |
| 方法 6（三变量隐函数） | $F(x,y,z)=0$，$z_x=-\dfrac{F_x}{F_z}$；二阶用直接求偏导 | 例 13、14；C21-09、10 |
| 方法 7（方程组两边求导） | 两个方程确定两个函数，解关于导数的二元一次方程组，$J\ne0$ | 例 15；C21-12 |
