## M.1 · 优化：梯度下降、学习率与收敛、凸性、动量、Adam

今天的大模型有几十亿个参数，每一个都是训练出来的：先随便给一组初值，让模型在训练数据上算一遍，看错了多少，再把每个参数往“错得少一点”的方向挪一小步，如此重复几十万次。这个“挪一小步”的规则，在大模型训练的设置里常常写成这样一行：AdamW，$\beta_1=0.9$，$\beta_2=0.95$，预热之后余弦衰减。读完本章，你能看懂其中的 Adam、两个 $\beta$、预热和余弦衰减各是什么；AdamW 里“W”（权重衰减）留到 M.3。

这套办法有一段很长的来历。1847 年，柯西为了求解天文计算中的联立方程，提出每一步沿着函数下降最快的方向走。1951 年，Robbins 与 Monro 问的是：每次只能拿到带噪声的估计，还能不能迭代到正确的答案？到了深度学习，数据成亿条，损失曲面又窄又崎岖。让迭代带上惯性的动量更早（Polyak 在 1964 年提出“重球法”），这时成了标配，再加上给每个参数各配一个步长的 Adam（Kingma 与 Ba，2014）。本章的每一节，都是从上一节解决不了的问题长出来的。

第四部分里的每个模型都由三件东西组成：一个带参数的**模型**，一个衡量错多少的**损失**，一条根据损失调参数的**更新规则**。本章讲的是第三件，而且讲的是所有模型共用的那一件。以后每一章开头，我们先填这三格，看这一章新在哪里。

本章按下面的问题链往下走：训练在解什么数学问题（第 1 节）；沿哪个方向走一步（第 2 节）；一步走多远才不会走散（第 3、4 节）；停下来的地方是不是最低点（第 5 节）；数据太多怎么办（第 6 节）；山谷窄而长怎么办（第 7 节）；每个参数能不能有自己的步长（第 8 节）；步长要不要随时间变（第 9 节）。

本章的“老朋友”是 5 个点：$x=(1,2,3,4,5)$，标签 $y=(2,3,5,6,9)$，用直线 $\hat y=wx+b$ 去拟合。

### 1. 训练一个模型，到底是在解什么数学问题？

先看最小的一个模型：直线 $\hat y=wx+b$。参数是 $\theta=(w,b)$，输入 $x$，输出预测 $\hat y$。对 5 个点中的第 $i$ 个，预测错多少用平方误差 $(wx_i+b-y_i)^2$ 来量。把 5 个点的平方误差取平均，就得到整个训练集上的损失：

$$L(w,b)=\frac15\sum_{i=1}^{5}(wx_i+b-y_i)^2 .$$

这是一个以参数为变量的函数：每给一组 $(w,b)$，就得到一个数，表示这条直线整体错得有多少。训练的全部含义就是找一组参数，让这个数尽量小。

一般地，训练集有 $n$ 个样本 $(\boldsymbol x_i,y_i)$，模型是 $f_\theta$，单个样本的损失是 $\ell(f_\theta(\boldsymbol x_i),y_i)$，则

$$L(\theta)=\frac1n\sum_{i=1}^{n}\ell\big(f_\theta(\boldsymbol x_i),\,y_i\big),\qquad \theta^*=\arg\min_\theta L(\theta).$$

$\arg\min$ 读作“使 $L$ 最小的那个 $\theta$”。这个在训练集上平均的损失也叫**经验风险**。我们真正关心的是模型在没见过的新数据上错多少，但手里只有这 $n$ 个样本，只能拿它当替身；替身好不好，留到 M.3 讲。本章只做一件事：给定 $L$，怎样找到它的最小点。

**方法 1（写出训练的损失）**

1. 认出参数 $\theta$ 是什么，模型对每个输入给出什么输出；
2. 选一个单样本损失 $\ell$，量“这一个样本错多少”；
3. 对全体样本取平均，得到 $L(\theta)$。

**例 1**　对 5 个点，求直线 $(w,b)=(0,0)$、$(1,0)$、$(1.7,-0.1)$ 的损失。

先代入 $(0,0)$：预测全是 0，误差就是标签本身，

$$L(0,0)=\frac{2^2+3^2+5^2+6^2+9^2}{5}=\frac{155}{5}=31 .$$

再代入 $(1,0)$：预测是 $1,2,3,4,5$，误差 $-1,-1,-2,-2,-4$，

$$L(1,0)=\frac{1+1+4+4+16}{5}=5.2 .$$

最后 $(1.7,-0.1)$：预测 $1.6,\,3.3,\,5.0,\,6.7,\,8.4$，误差 $-0.4,\,0.3,\,0,\,0.7,\,-0.6$，平方和 $0.16+0.09+0+0.49+0.36=1.1$，

$$L(1.7,-0.1)=\frac{1.1}{5}=0.22 .$$

三个数 $31,\,5.2,\,0.22$ 说明了一件事：直线的竖直残差越小，$L$ 越小。$(1.7,-0.1)$ 就是 L.10 里求出的最小二乘解，它是这个 $L$ 的最小点。

> 自己试一试：求 $(w,b)=(2,0)$ 的损失。
>
> 答案：预测 $2,4,6,8,10$，误差 $0,1,1,2,1$，平方和 7，所以 $L(2,0)=1.4$。

合上书，写出经验风险 $L(\theta)$ 的定义，并说出训练为什么是求 $\arg\min_\theta L(\theta)$。

对直线，最小点有现成的公式；对几十亿参数的网络没有，只能一步步走过去。下一节问的就是怎么走。

### 2. 沿哪个方向走一小步，损失降得最快？

回到例 1 的起点 $(w,b)=(0,0)$，这里 $L=31$。试着把参数朝四个方向各挪 0.1，看 $L$ 变成多少：

| 挪法 | $(0.1,\,0)$ | $(0,\,0.1)$ | $(-0.1,\,0)$ | $(0,\,-0.1)$ |
|---|---|---|---|---|
| 新的 $L$ | 27.43 | 30.01 | 34.79 | 32.01 |

增大 $w$ 降了 3.57，增大 $b$ 只降了 0.99，反方向都变大；同时增大两个，$(0.1,0.1)$ 处是 26.50，降得比单独走任何一个方向都多。降的幅度因方向而异，那么所有方向里哪一个降得最多？

一般地，站在某一组参数 $\theta$ 上，想挪一个小向量 $\Delta$，让 $L$ 尽量降。C.22 讲过，$L$ 在 $\theta$ 附近可以用一阶近似，其中 $\nabla L$ 是梯度，即把 $L$ 对每个参数的偏导排成的向量：

$$L(\theta+\Delta)\approx L(\theta)+\nabla L(\theta)\cdot\Delta .$$

右边第二项是梯度与 $\Delta$ 的点积。固定挪动的长度 $\lVert\Delta\rVert=r$（$\lVert\Delta\rVert$ 是向量 $\Delta$ 的长度），由点积的几何意义（L.2），

$$\nabla L\cdot\Delta=\lVert\nabla L\rVert\,r\cos\varphi ,$$

其中 $\varphi$ 是两个向量的夹角。$\cos\varphi$ 最小是 $-1$，在 $\varphi=\pi$ 时取到，即 $\Delta$ 正好与梯度反向。所以在同样的挪动长度下，沿负梯度方向，$L$ 的一阶预估下降得最多。

把方向取定为 $-\nabla L$，长度交给一个正数 $\eta$ 去调：

$$\boxed{\theta\leftarrow\theta-\eta\,\nabla L(\theta)}$$

这就是**梯度下降**。$\eta$ 叫**学习率**（步长）。反复做这一步，得到序列 $\theta_0,\theta_1,\theta_2,\dots$，每一次都用当前位置的梯度。

这里的步长是 $\eta\lVert\nabla L\rVert$：梯度大的地方（陡）走得多，梯度小的地方（快到谷底、变平）走得少，相当于自带刹车。

表里的 3.57 和 0.99 已经接近 $36.8\times0.1$ 和 $10\times0.1$，这正是下面例 2 要算出的梯度分量。这个公式用的是一阶近似，只在 $\Delta$ 很小时可靠：$\eta$ 太大时近似不准，下降的预估可能落空。下一节专门讲这件事。

**方法 2（梯度下降一步）**

1. 在当前 $\theta$ 处算梯度 $\nabla L(\theta)$；
2. 乘上学习率 $\eta$；
3. 从 $\theta$ 里减去它，得到新的 $\theta$。

**例 2**　接着例 1 的起点：5 个点，从 $(w,b)=(0,0)$ 出发，$\eta=0.02$，走一步。

先写出梯度。对 $L=\frac15\sum(wx_i+b-y_i)^2$，用链式法则（C.21），

$$\frac{\partial L}{\partial w}=\frac25\sum_i(wx_i+b-y_i)\,x_i,\qquad \frac{\partial L}{\partial b}=\frac25\sum_i(wx_i+b-y_i).$$

在 $(0,0)$ 处 $wx_i+b-y_i=-y_i$，所以

$$\frac{\partial L}{\partial w}=-\frac25(2+6+15+24+45)=-36.8,\qquad \frac{\partial L}{\partial b}=-\frac25(2+3+5+6+9)=-10 .$$

梯度是 $(-36.8,\,-10)$，两个分量都是负的，意思是增大 $w$ 和 $b$ 都会让 $L$ 下降，和上面的表一致。更新：

$$\begin{pmatrix}w\\b\end{pmatrix}\leftarrow\begin{pmatrix}0\\0\end{pmatrix}-0.02\begin{pmatrix}-36.8\\-10\end{pmatrix}=\begin{pmatrix}0.736\\0.2\end{pmatrix}.$$

损失从 31 降到了 $L(0.736,0.2)\approx8.797$。

注意一阶近似预测的下降量是 $\eta\lVert\nabla L\rVert^2=0.02\times1454.24\approx29.08$，也就是预测降到 $1.92$；实际降到 8.80，没有预测的那么多。这是因为 $L$ 在这一步里弯了，一阶近似没把弯曲算进去。

> 自己试一试：从 $(1,0)$ 出发，$\eta=0.05$，走一步，求新参数和新损失。
>
> 答案：在 $(1,0)$ 处误差是 $-1,-1,-2,-2,-4$，$\partial L/\partial w=\frac25(-1-2-6-8-20)=-14.8$，$\partial L/\partial b=\frac25(-10)=-4$。更新得 $(1+0.74,\ 0+0.2)=(1.74,\,0.2)$，$L(1.74,0.2)=0.3996$（由 5.2 降下来）。

**例 3**　接着例 2 往下走：同样的 $\eta=0.02$，多走几步，看损失怎样变。

把第 1 步得到的 $(0.736,0.2)$ 当作新起点，再算梯度、再更新，依次得到

| 步数 | $w$ | $b$ | $L$ | 梯度 |
|---|---|---|---|---|
| 0 | 0 | 0 | 31 | $(-36.8,\,-10)$ |
| 1 | 0.736 | 0.2 | 8.797 | $(-19.41,\,-5.18)$ |
| 2 | 1.124 | 0.304 | 2.636 | $(-10.25,\,-2.65)$ |
| 3 | 1.329 | 0.357 | 0.926 | $(-5.42,\,-1.31)$ |
| 4 | 1.437 | 0.383 | 0.451 | $(-2.88,\,-0.61)$ |

损失单调下降，梯度越来越小，步子也越来越小。参数在向 $(1.7,-0.1)$ 靠近，但 $b$ 还在 $0.38$ 附近，离 $-0.1$ 很远。这个“$w$ 先到位、$b$ 慢吞吞”的现象，下一节解释。

合上书，由一阶近似和点积推出同样长度下负梯度方向下降最快，并写出更新式 $\theta\leftarrow\theta-\eta\nabla L$。

走了几步看得出方法有效，但没有回答：$\eta$ 取多大合适？若取成 0.1 会怎样？

### 3. 学习率取多大，迭代才会收敛？

把例 3 的 $\eta$ 换成 0.1，从 $(0,0)$ 出发，前几步是 $(0,0)\to(3.68,1)\to(-1.336,-0.408)\to(5.528,1.475)\to\cdots$，损失依次是 $31,\,57.6,\,107.3,\,200.1,\dots$，越走越大。$\eta=0.02$ 好好地降，$\eta=0.1$ 却炸了，分界线在哪里？

要回答这个问题，先看最简单的情形：一个参数，$L(\theta)=\frac12\lambda\theta^2$，最小点在 0，$\lambda>0$ 表示曲线弯得多厉害（二阶导数）。此时 $\nabla L=\lambda\theta$，更新

$$\theta\leftarrow\theta-\eta\lambda\theta=(1-\eta\lambda)\,\theta .$$

每一步乘上同一个数 $1-\eta\lambda$，所以 $\theta_t=(1-\eta\lambda)^t\theta_0$。收敛的条件是 $|1-\eta\lambda|<1$，即

$$0<\eta<\frac{2}{\lambda}.$$

当 $\eta\lambda=1$ 时因子为 0，一步就落在最低点；当 $\eta\lambda=2$ 时因子为 $-1$，在 $\pm\theta_0$ 之间来回跳。除这两个边界外，还有三种情形：$0<\eta\lambda<1$ 时因子在 $(0,1)$，单调地靠近 0；$1<\eta\lambda<2$ 时因子在 $(-1,0)$，每步跨过最低点又折回来，一左一右但越摆越小；$\eta\lambda>2$ 时因子小于 $-1$，一步比一步摆得远。

![一维抛物线上三种学习率：单调靠近、来回摆动着靠近、来回摆动着发散](fig/M1-n1.pdf){width=70%}

**例 4**　例 3 里有两个参数，先缩成一个参数，把三种走法看清。$L(\theta)=\theta^2$（即 $\lambda=2$），$\theta_0=1$，分别取 $\eta=0.25$、$0.75$、$1$、$1.1$。

$\lambda=2$，因子 $1-2\eta$ 分别是 $0.5$、$-0.5$、$-1$、$-1.2$。

$\eta=0.25$：$\theta_t=1,\ 0.5,\ 0.25,\ 0.125,\dots$，单调趋于 0。

$\eta=0.75$：$\theta_t=1,\ -0.5,\ 0.25,\ -0.125,\dots$，正负交替但绝对值减半，仍然收敛。

$\eta=1$：$\theta_t=1,\ -1,\ 1,\ -1,\dots$，永远在两点之间跳，不收敛。

$\eta=1.1$：$\theta_t=1,\ -1.2,\ 1.44,\ -1.728,\dots$，发散。

阈值 $2/\lambda=1$：小于 1 收敛，等于 1 在两点间来回跳而不收敛，大于 1 发散。

> 自己试一试：$L(\theta)=5\theta^2$（$\lambda=10$），$\eta=0.15$ 和 $\eta=0.25$ 各是什么情形？
>
> 答案：阈值 $2/\lambda=0.2$。$\eta=0.15$ 时因子 $1-1.5=-0.5$，来回摆着收敛；$\eta=0.25$ 时因子 $1-2.5=-1.5$，发散。

参数不止一个时，还有这样干净的结论吗？$L$ 在最小点 $\theta^*$ 附近可以用泰勒公式展开到二阶（二阶项的系数矩阵是 L.14 的 Hessian $H$）。因为 $\theta^*$ 是最小点，$\nabla L(\theta^*)=\boldsymbol 0$，一阶项消失，剩下

$$L(\theta)\approx L(\theta^*)+\frac12(\theta-\theta^*)^{\mathsf T}H(\theta-\theta^*).$$

对右边求梯度：把 $\frac12\boldsymbol v^{\mathsf T}H\boldsymbol v$ 展开成 $\frac12\sum_{i,j}H_{ij}v_iv_j$，对 $v_k$ 求偏导，含 $v_k$ 的项有两类（$i=k$ 与 $j=k$），由 $H$ 对称合成 $\sum_jH_{kj}v_j$，也就是 $H\boldsymbol v$ 的第 $k$ 个分量。于是

$$\nabla L(\theta)=H(\theta-\theta^*).$$

所以在谷底附近，光滑损失的行为由二次函数的分析给出（前提是 $H$ 正定，下面的定理就是这种情形）。下面这个证明分三步，是本章最值得自己能写出来的一个。

**定理**　设 $L(\theta)=L(\theta^*)+\frac12(\theta-\theta^*)^{\mathsf T}H(\theta-\theta^*)$ 是精确的二次函数，$H$ 对称正定，特征值 $\lambda_1,\dots,\lambda_d$，最大的记 $\lambda_{\max}$。则梯度下降 $\theta\leftarrow\theta-\eta\nabla L$ 对**任意**起点都收敛到 $\theta^*$，当且仅当 $0<\eta<2/\lambda_{\max}$。

对一般的光滑损失，这个定理只说明它在最小点附近的局部行为（二次近似是近似，不是等号）；全局的保证见下一节。

先说思路：把误差向量沿 $H$ 的特征方向拆开，每个方向独立地被乘上一个数，然后每个方向都变成上面一维的情形。

**证明**

第一步，写出误差的递推。记 $\boldsymbol e_t=\theta_t-\theta^*$，则

$$\boldsymbol e_{t+1}=\boldsymbol e_t-\eta H\boldsymbol e_t=(I-\eta H)\,\boldsymbol e_t .$$

第二步，对角化。$H$ 对称，由 L.13，$H=Q\Lambda Q^{\mathsf T}$，$Q$ 的列是单位正交的特征向量，$\Lambda=\mathrm{diag}(\lambda_1,\dots,\lambda_d)$。令 $\boldsymbol u_t=Q^{\mathsf T}\boldsymbol e_t$，也就是把误差换到特征向量的坐标系里。递推式两边左乘 $Q^{\mathsf T}$，并在 $\boldsymbol e_t$ 前面插入 $QQ^{\mathsf T}=I$：

$$Q^{\mathsf T}\boldsymbol e_{t+1}=Q^{\mathsf T}(I-\eta H)Q\,\big(Q^{\mathsf T}\boldsymbol e_t\big).$$

因为 $Q^{\mathsf T}Q=I$，有 $Q^{\mathsf T}(I-\eta H)Q=I-\eta Q^{\mathsf T}HQ=I-\eta\Lambda$，于是

$$\boldsymbol u_{t+1}=(I-\eta\Lambda)\,\boldsymbol u_t,\qquad u_{i,t}=(1-\eta\lambda_i)^t\,u_{i,0}.$$

每个分量各自独立，就是一维的情形。

第三步，判断收敛。$Q$ 是正交矩阵，不改变向量的长度，$\lVert\boldsymbol e_t\rVert=\lVert\boldsymbol u_t\rVert$，所以 $\boldsymbol e_t\to0$ 当且仅当每个 $u_{i,t}\to0$，当且仅当每个 $|1-\eta\lambda_i|<1$，即对每个 $i$ 有 $\eta<2/\lambda_i$（$\lambda_i>0$，$\eta>0$）。等号取不到：$\eta=2/\lambda_i$ 时因子是 $-1$，来回跳而不收敛。最苛刻的是最大的 $\lambda_{\max}$，所以条件就是 $\eta<2/\lambda_{\max}$。$\blacksquare$

去掉“正定”这个条件会怎样？取 $L=-\frac12\theta^2$（$\lambda=-1$，谷底变成山脊），更新是 $\theta\leftarrow(1+\eta)\theta$，$\eta$ 再小也越走越远。取 $L=\frac12\theta_1^2$（$H=\mathrm{diag}(1,0)$，只是半正定），第二个分量原地不动，迭代收敛到 $(0,\theta_{2,0})$，最小点不止一个，到不了事先指定的那个 $\theta^*$。

**收敛有多快？** 每个方向的衰减因子是 $|1-\eta\lambda_i|$，整体的速度由最慢的那个方向决定：$\max_i|1-\eta\lambda_i|$。$\lambda_{\max}$ 限制了 $\eta$ 的上限；$\eta$ 被压在 $2/\lambda_{\max}$ 以下以后，$\lambda_{\min}$ 方向的因子 $1-\eta\lambda_{\min}$ 就贴近 1，$\kappa$ 越大、$\lambda_{\min}$ 越小越贴近，那个方向就走得越慢。

$\eta$ 取多大时整体最快？最慢的因子 $\max\{|1-\eta\lambda_{\min}|,\,|1-\eta\lambda_{\max}|\}$ 随 $\eta$ 增大先降后升：$\eta$ 小时由 $\lambda_{\min}$ 一端决定且在降，$\eta$ 大时由 $\lambda_{\max}$ 一端决定且在升，在 $0<\eta<2/\lambda_{\max}$ 内，$|1-\eta\lambda_{\min}|$ 随 $\eta$ 递减，$|1-\eta\lambda_{\max}|$ 先递减到 0、再递增，两条曲线的较大者在它们相交处最小。相交处前者为正、后者为负（$\eta$ 已过了 $1/\lambda_{\max}$），所以是$1-\eta\lambda_{\min}=-(1-\eta\lambda_{\max})$，解得

$$\eta^*=\frac{2}{\lambda_{\max}+\lambda_{\min}},\qquad \text{因子}=\frac{\kappa-1}{\kappa+1},\quad \kappa=\frac{\lambda_{\max}}{\lambda_{\min}}.$$

$\kappa$ 叫 $H$ 的**条件数**（L.14）。$\kappa$ 接近 1，因子接近 0，几步就到；$\kappa$ 很大，因子接近 1，即使取最优学习率也走得很慢。

这里有一个很自然的想法：慢的是 $\lambda_{\min}$ 方向，那把 $\eta$ 直接调到 $1/\lambda_{\min}$ 不就快了？不行。$\eta$ 一超过 $2/\lambda_{\max}$，$\lambda_{\max}$ 方向的因子绝对值就大于 1，那个方向先炸掉。例 5 里 $1/\lambda_{\min}\approx2.96$，而 $2/\lambda_{\max}\approx0.0845$，差了 35 倍。

**方法 3（用特征值判断学习率）**

1. 在谷底附近算 Hessian $H$ 的特征值，找出 $\lambda_{\max}$ 和 $\lambda_{\min}$；
2. $\eta<2/\lambda_{\max}$ 才能收敛，实际取值通常在 $1/\lambda_{\max}$ 附近；
3. 收敛的快慢看 $\kappa=\lambda_{\max}/\lambda_{\min}$，最优学习率下每步的因子是 $(\kappa-1)/(\kappa+1)$。

**例 5**　回到本节开头的问题：5 个点的损失为什么 $\eta=0.02$ 好使、$\eta=0.1$ 就炸。用例 3 同一个 $L$，只是现在去看它的 Hessian。

先求 Hessian。$L$ 对 $w$、$b$ 的二阶偏导（对上面的一阶导再求一次）：

$$H=\frac25\begin{pmatrix}\sum x_i^2&\sum x_i\\ \sum x_i&5\end{pmatrix}=\frac25\begin{pmatrix}55&15\\15&5\end{pmatrix}=\begin{pmatrix}22&6\\6&2\end{pmatrix}.$$

特征方程 $\lambda^2-24\lambda+8=0$（迹为 24，行列式 $44-36=8$），解得

$$\lambda=12\pm\sqrt{136}\ \approx\ 23.662,\ \ 0.338 .$$

于是阈值 $2/\lambda_{\max}\approx0.0845$。$\eta=0.02$ 小于它，$\eta=0.1$ 大于它，对上了。具体看两个方向的因子：

$\eta=0.02$ 时，$1-0.02\times23.662\approx0.527$，$1-0.02\times0.338\approx0.9932$；

$\eta=0.1$ 时，$1-0.1\times23.662\approx-1.366$，绝对值大于 1，发散。

再看条件数 $\kappa=23.662/0.338\approx70$，最优学习率 $\eta^*=2/24=1/12\approx0.0833$，每步因子 $(70-1)/(70+1)\approx0.972$。即使取最优学习率，误差每步也只缩小 2.8%。从原点出发，用几行程序数一数 $\lVert\theta_t-\theta^*\rVert$ 缩到 0.001 以内要走几步：$\eta=0.02$ 要 931 步，$\eta^*$ 要 261 步。程序大致是（$H$、`theta_star` 是上面的矩阵和 $(1.7,-0.1)$）：

```python
theta = np.zeros(2); k = 0
while np.linalg.norm(theta - theta_star) >= 1e-3:
    theta = theta - eta * H @ (theta - theta_star); k += 1
```

前一个数可以用最慢方向的因子 $0.9932$ 粗略检验：$0.9932^{1000}\approx0.001$，量级对得上。

这就是例 3 里 $b$ 慢吞吞的原因：最慢的那个特征方向上 $\lambda_{\min}=0.338$ 太小，$\eta=0.02$ 时每步只缩小 0.7%。

> 自己试一试：某损失的 Hessian 是 $\begin{pmatrix}5&2\\2&2\end{pmatrix}$，求学习率上限、条件数和最优学习率下的每步因子。
>
> 答案：迹 7，行列式 6，特征值 $6$ 和 $1$。上限 $2/6=1/3$；$\kappa=6$；最优 $\eta^*=2/7$，因子 $(6-1)/(6+1)=5/7$。

那怎么办？除了调 $\eta$，也可以改变问题本身。

**例 6**　和例 5 比，这次不动 $\eta$，只改数据：5 个点的 $x$ 值减去平均数 3，改用 $x'=x-3=(-2,-1,0,1,2)$，直线写成 $\hat y=w'x'+b'$。条件数怎么变？此时 $\sum x'_i=0$，$\sum x'^2_i=10$，

$$H'=\frac25\begin{pmatrix}10&0\\0&5\end{pmatrix}=\begin{pmatrix}4&0\\0&2\end{pmatrix},\qquad \kappa=2 .$$

条件数从 70 降到 2，最优学习率 $2/(4+2)=1/3$，每步因子 $(2-1)/(2+1)=1/3$，几步就够了。训练中先把特征减均值、除标准差，就是在改善条件数，这是最便宜的办法之一。

![5 个点的损失等高线（椭圆）上，$\eta=0.02$ 与 $\eta=0.08$ 的梯度下降轨迹（$\eta=0.08$ 仍在阈值 $0.0845$ 之内）](fig/M1-n2.pdf){width=70%}

图里的椭圆又窄又长，$\eta=0.08$ 的轨迹在窄的方向上来回折，$\eta=0.02$ 的不折，但沿长轴爬得很慢。

合上书，把误差沿 $H$ 的特征方向拆开，推出收敛条件 $0<\eta<2/\lambda_{\max}$，并指出等号为什么取不到。

这一节的结论都建立在损失是二次函数上，下一节要问，一般的光滑函数上有没有类似的保证。

### 4. 一般的光滑函数上，步长多小能保证每一步都下降？

二次函数的 Hessian 处处相同，所以有一个统一的 $\lambda_{\max}$。一般函数里曲率随位置变。比如 $L(\theta)=\theta^4$，二阶导数 $12\theta^2$ 在 $\theta=1$ 附近是 12，在 $\theta=10$ 附近就是 1200。只看 $|\theta|\le1$，曲率不超过 12，有一个上界可用；放在整条数轴上，就找不到对所有位置都适用的 $\eta$。所以我们要先有一个整个区域都适用的曲率上界，这就是 **$L$-光滑**：存在常数 $L_s>0$，使得对任意两点 $\boldsymbol a,\boldsymbol b$，

$$\lVert\nabla L(\boldsymbol a)-\nabla L(\boldsymbol b)\rVert\le L_s\lVert\boldsymbol a-\boldsymbol b\rVert .$$

意思是梯度变化得不会比位置变化快 $L_s$ 倍。对二阶可导的 $L$，梯度差等于 Hessian 沿线段的积分，由此可以推出它与“Hessian 的特征值的绝对值处处不超过 $L_s$”一致；本节只用上面的梯度形式。对 Hessian 半正定的二次函数，$L_s=\lambda_{\max}$；一般地 $L_s=\max_i|\lambda_i|$。

由此可以推出**下降引理**：沿梯度方向走一步 $\eta\le1/L_s$，损失至少降 $\frac\eta2\lVert\nabla L\rVert^2$。证明只需两步。

第一步，把函数夹在一个抛物线下面，分三小步。其一，沿线段从 $\theta$ 走到 $\theta+\Delta$，由微积分基本定理，

$$L(\theta+\Delta)-L(\theta)-\nabla L(\theta)\cdot\Delta=\int_0^1\big(\nabla L(\theta+s\Delta)-\nabla L(\theta)\big)\cdot\Delta\,\mathrm ds .$$

其二，用柯西不等式 $|\boldsymbol a\cdot\boldsymbol b|\le\lVert\boldsymbol a\rVert\lVert\boldsymbol b\rVert$ 把被积函数的绝对值放大成 $\lVert\nabla L(\theta+s\Delta)-\nabla L(\theta)\rVert\lVert\Delta\rVert$；再用光滑性，两点相距 $s\lVert\Delta\rVert$，所以它不超过 $L_s s\lVert\Delta\rVert^2$。其三，$\int_0^1s\,\mathrm ds=\frac12$，积分得 $\frac{L_s}{2}\lVert\Delta\rVert^2$，所以

$$L(\theta+\Delta)\le L(\theta)+\nabla L\cdot\Delta+\frac{L_s}{2}\lVert\Delta\rVert^2 .$$

第二步，代入 $\Delta=-\eta\nabla L$，

$$L(\theta-\eta\nabla L)\le L(\theta)-\eta\lVert\nabla L\rVert^2+\frac{L_s\eta^2}{2}\lVert\nabla L\rVert^2=L(\theta)-\eta\Big(1-\frac{L_s\eta}{2}\Big)\lVert\nabla L\rVert^2 .$$

$\eta\le1/L_s$ 时括号里至少是 $\frac12$，得到结论。若 $\eta<2/L_s$，括号仍为正，也保证下降，与上一节的阈值一致。

**例 7**　起点和梯度都和例 2 一样，只把 $\eta$ 从 0.02 换成 $1/L_s$，检查下降引理保证的下降量。5 个点的 $L_s=\lambda_{\max}\approx23.662$（例 5，Hessian 处处相同）。取 $\eta=1/L_s\approx0.04226$，从 $(0,0)$ 走一步。

梯度平方范数 $\lVert\nabla L\rVert^2=1454.24$，引理保证至少降 $\frac\eta2\lVert\nabla L\rVert^2=\frac{0.04226}{2}\times1454.24\approx30.73$，所以新损失不超过 $31-30.73\approx0.270$。

实际走一步得 $(1.555,\,0.423)$，$L\approx0.2697$，刚好在保证值之下。在二次函数上这个界几乎是紧的。

在实际训练里，一般不去算 $L_s$，学习率靠试：从一个值开始，往大往小各试几倍，挑损失下降得又快又稳的那个。本节的作用是告诉你，试的时候合理范围的量级由曲率决定。

合上书，写出 $L$-光滑的定义，并用抛物线界说明为什么 $\eta\le1/L_s$ 时每步都下降。

下降引理保证每一步都降，却没有说降到最后停在哪里：梯度为零的点，是不是最低点？

### 5. 停下来的地方，是不是全局最低点？

梯度下降停下来的位置是梯度为零的点。先看一个会出问题的函数：$f(x)=x^4-2x^2+0.5x$，$f'(x)=4x^3-4x+0.5$ 有三个零点。$x\approx-1.057$ 是左坑底，$f\approx-1.515$；$x\approx0.930$ 是右坑底，$f\approx-0.517$，左坑更深；$x\approx0.127$ 是两坑之间的小山顶。梯度下降从 $x_0=1.5$ 出发停在右坑底，从 $-1.5$ 出发停在左坑底。梯度为零的点，可能是全局最低点，也可能只是小坑的底，甚至是山顶。什么样的函数可以放心？答案是**凸函数**。

先说一个叫法上的约定。C.8.4 里把 $f''\ge0$、图像向上弯的函数叫“凹函数”；优化和机器学习领域的叫法正相反，称它为**凸函数**。本书从第四部分起统一采用优化的叫法：图像向上弯、$f''\ge0$ 的函数就叫凸函数。

**定义**　函数 $f$ 称为凸函数，如果对任意两点 $\boldsymbol x,\boldsymbol y$ 和任意 $\alpha\in[0,1]$，

$$f\big(\alpha\boldsymbol x+(1-\alpha)\boldsymbol y\big)\le\alpha f(\boldsymbol x)+(1-\alpha)f(\boldsymbol y).$$

左边是两点之间某处的函数值，右边是同一处弦（连接两点函数值的线段）的高度。所以意思是：弦永远在图像上方。

![凸函数的弦在曲线上方，非凸函数的弦会穿到曲线下面](fig/M1-n3.pdf){width=70%}

**定理**　凸函数的局部最小点就是全局最小点。

思路：假设有一个局部最小点 $\boldsymbol x$，又有更低的点 $\boldsymbol y$，则沿弦走，附近的点会比 $\boldsymbol x$ 更低，与“局部最小”矛盾。

**证明**

设 $\boldsymbol x$ 是局部最小点，即存在 $\delta>0$，在 $\lVert\boldsymbol z-\boldsymbol x\rVert<\delta$ 内总有 $f(\boldsymbol z)\ge f(\boldsymbol x)$。若存在 $\boldsymbol y$ 使 $f(\boldsymbol y)<f(\boldsymbol x)$，考虑弦上的点 $\boldsymbol z=\alpha\boldsymbol x+(1-\alpha)\boldsymbol y$，它到 $\boldsymbol x$ 的距离是 $(1-\alpha)\lVert\boldsymbol y-\boldsymbol x\rVert$，$\alpha\to1$ 时 $\boldsymbol z=\alpha\boldsymbol x+(1-\alpha)\boldsymbol y\to\boldsymbol x$，所以取 $\alpha$ 足够靠近 1，可以使 $\boldsymbol z$ 落进 $\boldsymbol x$ 的那个小邻域内。凸性给出

$$f(\boldsymbol z)\le\alpha f(\boldsymbol x)+(1-\alpha)f(\boldsymbol y)<\alpha f(\boldsymbol x)+(1-\alpha)f(\boldsymbol x)=f(\boldsymbol x),$$

第二个不等号用了 $f(\boldsymbol y)<f(\boldsymbol x)$ 和 $1-\alpha>0$。这说明邻域里有比 $\boldsymbol x$ 更低的点，和“局部最小”矛盾。$\blacksquare$

去掉凸性，结论马上失效：开头那个 $f$ 的右坑底就是局部最小而不是全局最小。梯度下降找到的是梯度为零的点，所以还要补一句：对可导的凸函数，梯度为零的点必是全局最小。设 $\nabla f(\boldsymbol x)=\boldsymbol 0$，任取 $\boldsymbol y$，在凸性不等式里取 $\alpha=1-s$（$0<s<1$），

$$f\big(\boldsymbol x+s(\boldsymbol y-\boldsymbol x)\big)\le f(\boldsymbol x)+s\big(f(\boldsymbol y)-f(\boldsymbol x)\big).$$

移项后两边除以 $s$，让 $s\to0^+$，左边趋于方向导数 $\nabla f(\boldsymbol x)\cdot(\boldsymbol y-\boldsymbol x)=0$，于是 $0\le f(\boldsymbol y)-f(\boldsymbol x)$。神经网络的损失一般不是凸的，却照样用梯度下降训练，这一点留到 M.8 再谈。

这里的函数都定义在整个空间（或某个凸的区域）上，这样两点之间的线段才在定义域内。怎么检验一个函数是不是凸函数？对二阶连续可导的函数，用二阶条件。理由：沿任意方向 $\boldsymbol d$ 把 $f$ 限制成一元函数 $g(s)=f(\boldsymbol x+s\boldsymbol d)$，则 $g''(s)=\boldsymbol d^{\mathsf T}H\boldsymbol d$；一元函数 $g''\ge0$ 时图像向上弯（C.8.4）。弦只涉及一条直线上的两点，所以逐条直线检查就够了：每个方向上 $g''\ge0$，等价于对每个 $\boldsymbol d$ 有 $\boldsymbol d^{\mathsf T}H\boldsymbol d\ge0$，这就是 $H$ 半正定。

$$f\ \text{是凸函数}\iff\text{每一点的 Hessian }H\text{ 都是半正定矩阵（即特征值全}\ge0,\ \text{L.14.5）}.$$

一元时就是 $f''\ge0$。

**方法 4（用 Hessian 判断凸性）**

1. 算出 Hessian 矩阵；
2. 看它是否在所有点都半正定：特征值全 $\ge0$，或者对二阶实对称矩阵看迹 $\ge0$ 且行列式 $\ge0$（两个特征值之和与积都不为负，才能同时不为负）；
3. 若某点有负特征值，则不是凸函数（那个方向上是向下弯的）。

**例 8**　例 5 里的 Hessian 是现成的，特征值恰好都为正。这次换两个具体函数，从头算出 Hessian 再判断：$f(x,y)=x^2+xy+y^2$ 和 $g(x,y)=x^2+3xy+y^2$ 是否为凸函数。

$f$ 的 Hessian：$f_{xx}=2$，$f_{xy}=1$，$f_{yy}=2$，

$$H_f=\begin{pmatrix}2&1\\1&2\end{pmatrix},\quad \text{迹 }4,\ \text{行列式 }3 .$$

迹和行列式都为正，所以两个特征值都为正（它们的和与积都是正数），$H_f$ 正定，$f$ 是凸函数，且唯一的最小点在原点。

$g$ 的 Hessian：

$$H_g=\begin{pmatrix}2&3\\3&2\end{pmatrix},\quad \text{行列式 }4-9=-5<0 .$$

行列式为负，两个特征值一正一负，$g$ 在原点是鞍点，不是凸函数。沿 $y=-x$ 方向 $g=-x^2$，向下弯。

> 自己试一试：判断 $h(x,y)=x^2+2xy+y^2$ 是否为凸函数，最小点是否唯一。
>
> 答案：$H_h=\begin{pmatrix}2&2\\2&2\end{pmatrix}$，迹 4，行列式 0，特征值 $4,0$，半正定，所以 $h$ 是凸函数；因为 $h=(x+y)^2$，沿 $y=-x$ 的整条线都是最小点，最小点不唯一。

**例 9**　和例 8 相比，这次对一整类损失做判断，函数没有给出具体式子：5 个点的损失为什么是凸函数？这里 Hessian 是 $H=\frac25X^{\mathsf T}X$，$X$ 是 $5\times2$ 的数据矩阵（每行 $(x_i,1)$，这里的“特征”指输入的分量，和 L.13 的特征值无关）。

对任意向量 $\boldsymbol v$，

$$\boldsymbol v^{\mathsf T}H\boldsymbol v=\frac25\,\boldsymbol v^{\mathsf T}X^{\mathsf T}X\boldsymbol v=\frac25\lVert X\boldsymbol v\rVert^2\ \ge0 ,$$

所以 $H$ 半正定，$L$ 是凸函数。这个论证对任何线性模型的均方误差都成立，M.2 会再用到。实际上例 5 里 $H$ 的特征值 23.66 和 0.338 都为正，是正定的，所以最小点唯一。

合上书，写出凸函数的定义，并用弦上的点说明局部最小点为什么一定是全局最小点。

到这里，“往哪走、走多远、停在哪”都有了回答。但每一步的代价还没有算：损失是全体数据的平均。

### 6. 数据有上亿条，每一步都要用全部数据算梯度吗？

$L$ 是 $n$ 个样本的平均，所以梯度也是 $n$ 个单样本梯度的平均：

$$\nabla L(\theta)=\frac1n\sum_{i=1}^n\nabla\ell_i(\theta).$$

$n$ 是上亿时，走一步就要把全体数据过一遍。观察一下 5 个点在 $(0,0)$ 处每个样本的梯度 $\nabla\ell_i=2(wx_i+b-y_i)(x_i,1)$：

$$(-4,-4),\ (-12,-6),\ (-30,-10),\ (-48,-12),\ (-90,-18).$$

平均是 $(-36.8,-10)$，恰好是例 2 的梯度。这些单样本梯度虽然大小不同，但大多方向一致。既然如此，每次不用全部，只随机抽几条，用它们的平均当作梯度的估计，是不是也能朝大致正确的方向走？

抽出的 $B$ 个样本叫一个**小批量**，$B$ 叫批量大小。**小批量梯度**是

$$\boldsymbol g_B=\frac1B\sum_{j=1}^{B}\nabla\ell_{i_j}(\theta),$$

其中 $i_1,\dots,i_B$ 是独立地、等可能地从 $1,\dots,n$ 中抽出的下标。用它代替全梯度，就是**随机梯度下降**（SGD）：$\theta\leftarrow\theta-\eta\boldsymbol g_B$。

这里 $E$ 表示期望（P.7），也就是对“抽到哪几个样本”这件事取平均。这个估计有两条好性质，都由 P.7、P.8 的期望和方差性质推出。

**无偏**：抽出任意一条的下标 $I$，$E[\nabla\ell_I]=\sum_i\frac1n\nabla\ell_i=\nabla L$（每个样本以概率 $1/n$ 被抽中）。对 $B$ 个取平均，期望的线性性给出 $E[\boldsymbol g_B]=\nabla L$。也就是说，平均来看，小批量梯度指向正确的方向。

**方差按 $1/B$ 缩小**：$B$ 个抽样独立，设单条梯度某个分量在 $n$ 个样本上的方差为 $\sigma^2$，则平均的方差为 $\sigma^2/B$（P.8：独立变量和的方差等于方差的和，平均时除以 $B^2$）。批量大一倍，噪声的方差减半。

![5 个点上全梯度与小批量梯度的轨迹：小批量在同一方向附近抖动](fig/M1-n4.pdf){width=70%}

**方法 5（小批量梯度）**

1. 随机抽 $B$ 个样本；
2. 算出这 $B$ 个样本各自的梯度并取平均，当作梯度；
3. 照常更新。每步成本是全梯度的 $B/n$，噪声方差是单条的 $1/B$。

**例 10**　还是例 2 的 $(0,0)$ 处，用上面的 5 个单样本梯度，批量取第 2、4 号样本，求 $\boldsymbol g_B$，并与全梯度比较。

$$\boldsymbol g_B=\frac12\Big[(-12,-6)+(-48,-12)\Big]=(-30,\,-9).$$

全梯度是 $(-36.8,-10)$，两者的方向接近，大小有偏差。再看无偏性：有放回地抽 2 个，共 $5\times5=25$ 种有序取法，每种等可能。第一个位置上每个样本恰好出现 5 次，第二个位置也一样，所以 25 个小批量梯度的平均是 $\frac1{25}\cdot\frac12\big(5\sum_i\nabla\ell_i+5\sum_i\nabla\ell_i\big)=\frac15\sum_i\nabla\ell_i$，正好是全梯度。

先猜一猜：批量从 2 增大到 5，噪声的方差会变成原来的几分之几？用方差公式算。5 个样本在 $w$ 方向的单样本梯度 $(-4,-12,-30,-48,-90)$ 的方差是 $938.56$，所以 $B=2$ 时（有放回抽样）方差约为 $469.3$，$B=5$ 时约为 $187.7$，是原来的 $2/5$，不多不少，正是 $1/B$ 的比例。

> 自己试一试：批量取第 1、5 号样本，求 $\boldsymbol g_B$。
>
> 答案：$\boldsymbol g_B=\frac12[(-4,-4)+(-90,-18)]=(-47,-11)$。比全梯度偏大，这次抽样碰巧抽到了梯度最大的样本。

SGD 的轨迹带噪声，到谷底附近也不停下来，总在最小点附近抖动，$\eta$ 越大抖得越厉害（在二次函数上，抖动的方差大致和 $\eta$ 成正比）。想让它真正落进谷底，学习率得随训练逐步减小，这是第 9 节学习率调度的由来之一，也是 Robbins 与 Monro 当年的结论：学习率要衰减到 0，但不能衰减得太快（$\sum\eta_t=\infty$，$\sum\eta_t^2<\infty$）。

合上书，解释小批量梯度为什么无偏，以及它的方差为什么按 $1/B$ 缩小。

小批量解决了每步代价的问题，但没有解决弯曲山谷里的来回摆动。

### 7. 山谷又窄又长、梯度来回打转时怎么办？

回到第 3 节的图：椭圆很窄，学习率较大（$\eta\lambda_{\max}>1$，如图里的 $\eta=0.08$）时，梯度下降的轨迹在窄方向来回折，沿长方向却进展缓慢。此时窄方向的梯度符号每步都反；$\eta$ 小（如 $\eta=0.02$）时窄方向单调靠近，不再变号，但长方向的梯度每步都同号却很小，照样慢。

想一想怎么利用这一点：如果把最近几步的梯度**加在一起**，反复变号的分量会互相抵消，始终同号的分量会累积。这就是**动量**：不直接用当前梯度，而是用梯度的指数加权和（差一个常数因子，就是滑动平均，见本节末尾）。

定义速度向量 $\boldsymbol v$，初值为 $\boldsymbol 0$，每一步

$$\boldsymbol v\leftarrow\beta\boldsymbol v+\nabla L(\theta),\qquad \theta\leftarrow\theta-\eta\boldsymbol v,$$

$\beta\in[0,1)$ 叫动量系数，常取 0.9。展开一下就看得出为什么叫滑动平均：

$$\boldsymbol v_t=\nabla L(\theta_t)+\beta\nabla L(\theta_{t-1})+\beta^2\nabla L(\theta_{t-2})+\cdots$$

越久以前的梯度权重 $\beta^k$ 越小。若每一步梯度都相同（始终同号的分量），$\boldsymbol v\to\boldsymbol g(1+\beta+\beta^2+\cdots)=\boldsymbol g/(1-\beta)$，$\beta=0.9$ 时放大 10 倍；若梯度正负交替（$g,-g,g,\dots$），$\boldsymbol v\to g(1-\beta+\beta^2-\cdots)=g/(1+\beta)$，$\beta=0.9$ 时约是 $0.53g$，比同号时的 $10g$ 小得多。

这个算法常被叫作“惯性”或“重球”：$\boldsymbol v$ 对应球的速度，$\beta$ 对应速度保留多少，$1-\beta$ 对应每步损失多少。这个说法有一点能直接拿来判断：$\beta$ 越大，冲过谷底后折回来越慢。

**方法 6（动量）**

1. 保存速度 $\boldsymbol v$，初值 $\boldsymbol 0$；
2. 每步 $\boldsymbol v\leftarrow\beta\boldsymbol v+\nabla L(\theta)$；
3. 用 $\boldsymbol v$ 代替梯度更新：$\theta\leftarrow\theta-\eta\boldsymbol v$。

**例 11**　和例 3 同样的 5 个点、同样的起点和 $\eta=0.02$，只加上动量 $\beta=0.9$，走 3 步，与例 3 对比。先猜一猜：动量既然更快，损失会不会每一步都降？

第 1 步：$\boldsymbol v_1=\nabla L(0,0)=(-36.8,-10)$，$\theta_1=(0.736,0.2)$，和普通梯度下降一样（因为 $\boldsymbol v_0=\boldsymbol 0$）。

第 2 步：$\nabla L(\theta_1)=(-19.408,-5.184)$，

$$\boldsymbol v_2=0.9(-36.8,-10)+(-19.408,-5.184)=(-52.528,\,-14.184),\quad \theta_2=(1.787,\,0.484).$$

第 3 步：$\nabla L(\theta_2)=(5.406,\,1.687)$，梯度已经变号，说明 $\theta_2$ 的 $w$ 已经越过了谷底；但速度里还带着前面的 $-52.5$，

$$\boldsymbol v_3=0.9(-52.528,-14.184)+(5.406,1.687)\approx(-41.87,\,-11.08),\quad \theta_3\approx(2.624,\,0.705).$$

普通梯度下降第 3 步在 $(1.329,0.357)$，动量走到了 $(2.624,0.705)$，已经冲过了 $w=1.7$。答案是不会。损失依次是 $31\to8.80\to0.946\to14.7$，先降后升：第 3 步冲过了最低点，之后几步会折回来（第 4、5 步的损失分别是 22.2、10.9，第 6 步回到 0.45）。

动量法下损失不一定单调（这是惯性的代价），但整体收敛得更快：达到 $\lVert\theta_t-\theta^*\rVert<0.001$，普通梯度下降 $\eta=0.02$ 需要 931 步，加上 $\beta=0.9$ 只要 124 步。

> 自己试一试：$\beta=0.5$，$\eta=0.02$，从 $(0,0)$ 走 2 步，求 $\theta_2$。
>
> 答案：$\boldsymbol v_1=(-36.8,-10)$，$\theta_1=(0.736,0.2)$；$\boldsymbol v_2=0.5(-36.8,-10)+(-19.408,-5.184)=(-37.808,-10.184)$，$\theta_2=(0.736+0.7562,\ 0.2+0.2037)=(1.4922,\ 0.4037)$。

为什么加动量会快这么多？看第 3 节的二次函数，沿某个特征方向（特征值 $\lambda$）的误差记作 $e_t$，该方向的梯度是 $\lambda e_t$。于是

$$v_t=\beta v_{t-1}+\lambda e_t,\qquad e_{t+1}=e_t-\eta v_t .$$

要消去 $v$：由第二式 $\eta v_{t-1}=e_{t-1}-e_t$，把第一式乘 $\eta$ 再代入，

$$e_{t+1}=e_t-\beta(e_{t-1}-e_t)-\eta\lambda e_t=(1+\beta-\eta\lambda)\,e_t-\beta\,e_{t-1}.$$

这是一个二阶递推，它的特征方程

$$r^2-(1+\beta-\eta\lambda)r+\beta=0$$

的两个根决定衰减的快慢。

判别式小于零，即 $(1+\beta-\eta\lambda)^2<4\beta$，等价于 $|1+\beta-\eta\lambda|<2\sqrt\beta$，也就是

$$(1-\sqrt\beta)^2<\eta\lambda<(1+\sqrt\beta)^2 .$$

此时两根是共轭复数 $r_1,r_2$。由根与系数的关系 $r_1r_2=\beta$，共轭复数的模相等，所以

$$|r_1|=|r_2|=\sqrt\beta .$$

这个模里没有 $\lambda$。于是只要所有特征值都落在上面的范围里，每个方向的误差都按同一个 $\sqrt\beta$ 衰减，**与 $\lambda$ 无关**：特征值差得再远，也不拖慢最慢的方向。

对 5 个点，$\beta=0.9$，$\sqrt\beta\approx0.949$，范围是 $(0.0026,\ 3.80)$。$\eta=0.02$ 时 $\eta\lambda_{\max}=0.473$ 和 $\eta\lambda_{\min}=0.0068$ 都在里面。于是误差带着振荡，振幅的包络每步按 0.949 衰减。（收敛还要求两根的模都小于 1。对 $r^2+ar+\beta$ 这等价于 $|\beta|<1$，且多项式在 $r=1$ 与 $r=-1$ 处的值都为正：前者是 $\eta\lambda>0$，后者是 $2(1+\beta)-\eta\lambda>0$，合起来 $0<\eta\lambda<2(1+\beta)$，本例满足。）不带动量，最好的每步因子也只有 0.972（条件数 70 的代价）。大致的规律是：动量把条件数 $\kappa$ 对速度的影响，从 $\kappa$ 降到 $\sqrt\kappa$ 的量级。

另外要留心两种写法的区别：这里写的是 $\boldsymbol v\leftarrow\beta\boldsymbol v+\boldsymbol g$（许多库的 SGD 动量采用），而下一节的 Adam 用的是 $\boldsymbol m\leftarrow\beta\boldsymbol m+(1-\beta)\boldsymbol g$。后者是真正的“平均”，前者比它大 $1/(1-\beta)$ 倍，所以若把累加量直接当更新方向，同一个 $\eta$ 的步长差 $1/(1-\beta)=10$ 倍（$\beta=0.9$）；Adam 还要除以 $\sqrt{\hat{\boldsymbol s}}$，$\eta$ 的含义不同，见下一节。

![同一个窄山谷中（$\eta=0.02$），普通梯度下降沿长轴爬得很慢，加动量后沿长轴前进快得多，途中带有摆动](fig/M1-n5.pdf){width=70%}

合上书，从动量的二阶递推推出判别式小于零时 $|r|=\sqrt{\beta}$，并说明收敛速度为什么不再依赖 $\lambda$。

动量治的是方向上的问题：反复变号的分量被抵消。还有一个问题它没碰：不同参数的梯度大小可能差几个数量级，共用一个 $\eta$ 照顾不到每一个。

### 8. 每个参数能不能有自己的步长？

在 5 个点上，$w$ 的梯度（$-36.8$）比 $b$ 的梯度（$-10$）大三倍多，原因是 $x$ 的值比常数 1 大。大模型里不同层的梯度可以差到几个数量级。共用一个 $\eta$，要么梯度大的参数炸掉，要么梯度小的参数几乎不动。

想法是：把每个参数的步长按它自己梯度的“典型大小”缩放。典型大小用梯度平方的滑动平均来量。这就是 **Adam**（Adaptive Moment Estimation）。每一步，对每个参数（逐坐标）维护两个量：

$$\boldsymbol m\leftarrow\beta_1\boldsymbol m+(1-\beta_1)\boldsymbol g,\qquad \boldsymbol s\leftarrow\beta_2\boldsymbol s+(1-\beta_2)\,\boldsymbol g\odot\boldsymbol g .$$

$\boldsymbol g=\nabla L$ 是当前梯度，$\odot$ 表示逐坐标相乘（所以 $\boldsymbol g\odot\boldsymbol g$ 是各坐标的平方）。$\boldsymbol m$ 是梯度本身的滑动平均，叫**一阶矩**，起一阶动量的作用；$\boldsymbol s$ 是梯度平方的滑动平均，叫**二阶矩**，量梯度的大小。（注意：Adam 论文里二阶矩写作 $v$，这里为避免与上一节动量的速度 $\boldsymbol v$ 撞名改写为 $\boldsymbol s$；从这里起 $\boldsymbol s$ 只指二阶矩。）常取 $\beta_1=0.9$，$\beta_2=0.999$（大模型训练里也见到 $\beta_2=0.95$ 这样更小的取值）。$\boldsymbol m$、$\boldsymbol s$ 初值为 $\boldsymbol 0$。

更新时除以 $\sqrt{\boldsymbol s}$，使每个坐标的步长与自己的梯度大小无关：

$$\theta\leftarrow\theta-\eta\,\frac{\hat{\boldsymbol m}}{\sqrt{\hat{\boldsymbol s}}+\epsilon},\qquad \hat{\boldsymbol m}=\frac{\boldsymbol m}{1-\beta_1^t},\quad \hat{\boldsymbol s}=\frac{\boldsymbol s}{1-\beta_2^t}.$$

除法和开方都是逐坐标做的。$\epsilon$ 是个很小的数（如 $10^{-8}$），防止分母为 0。$t$ 是已走的步数。

这里有一个读者最容易感到别扭的地方：$\hat{\boldsymbol m}$ 和 $\hat{\boldsymbol s}$ 为什么要除以 $1-\beta^t$？

**偏差修正的来由。** $\boldsymbol m$ 从 $\boldsymbol 0$ 起步。假设每步梯度都是同一个值 $g$。第 1 步 $m_1=(1-\beta_1)g=0.1g$；第 2 步 $m_2=0.9\times0.1g+0.1g=0.19g$；一般地，

$$m_t=(1-\beta_1)\,g\,(1+\beta_1+\cdots+\beta_1^{t-1})=(1-\beta_1^t)\,g .$$

最后一步用了等比数列求和。可见 $m_t$ 比真实的 $g$ 偏小，偏小的比例正好是 $1-\beta_1^t$；除以它就还原了。$t$ 大了，$\beta_1^t\to0$，修正自然消失。$\boldsymbol s$ 同理，且 $\beta_2=0.999$ 偏得更久（前几百步都明显偏小）。

![从零起步的滑动平均偏小，除以修正因子后回到真实值](fig/M1-n6.pdf){width=70%}

再看除以 $\sqrt{\hat s}$ 的效果。若某坐标的梯度基本恒定为 $g$，则 $\hat m\approx g$，$\sqrt{\hat s}\approx|g|$，更新量约是 $\eta\,g/|g|=\pm\eta$（这里忽略 $\epsilon$）：**梯度稳定时，步长约是 $\eta$，与梯度大小无关**，只剩下符号。这就是“逐坐标缩放”的含义，$\eta$ 在 Adam 里直接标出了每个参数每步走多远的量级。

**方法 7（Adam 一步）**

1. 算梯度 $\boldsymbol g$；
2. 更新 $\boldsymbol m$、$\boldsymbol s$（两个滑动平均）；
3. 做偏差修正，得 $\hat{\boldsymbol m}$、$\hat{\boldsymbol s}$；
4. 逐坐标更新 $\theta\leftarrow\theta-\eta\hat{\boldsymbol m}/(\sqrt{\hat{\boldsymbol s}}+\epsilon)$。

**例 12**　把例 11 的动量换成 Adam，仍是同样的 5 个点和起点。Adam 每步大约走 $\eta$，所以不再用 0.02，改取 $\eta=0.1$，$\beta_1=0.9$，$\beta_2=0.999$，走 3 步。

第 1 步：$\boldsymbol g=(-36.8,-10)$。$\boldsymbol m=0.1\boldsymbol g=(-3.68,-1)$，$\boldsymbol s=0.001\,\boldsymbol g\odot\boldsymbol g=(1.354,\,0.1)$。修正因子 $1-0.9=0.1$、$1-0.999=0.001$，所以 $\hat{\boldsymbol m}=\boldsymbol g$，$\hat{\boldsymbol s}=\boldsymbol g\odot\boldsymbol g$，

$$\theta_1=\theta_0-0.1\,\mathrm{sign}(\boldsymbol g)=(0.1,\ 0.1)\qquad(\text{忽略 }\epsilon).$$

两个坐标各走了 0.1，虽然梯度差了 3.7 倍。

第 2 步：梯度 $(-34.0,-9.2)$，修正后 $\hat{\boldsymbol m}\approx(-35.33,-9.58)$，$\sqrt{\hat{\boldsymbol s}}\approx(35.43,\,9.61)$，每个坐标的比值都接近 $-1$，得 $\theta_2\approx(0.1997,\ 0.1997)$。

第 3 步：同理得 $\theta_3\approx(0.2989,\ 0.2988)$。

每步两个坐标几乎同步地走 $\eta=0.1$。目标是 $(1.7,-0.1)$，$w$ 要走 1.7、$b$ 只要走 $-0.1$，两个坐标却以同样的步长前进。继续算下去（用程序），第 20 步在 $\theta\approx(1.54,\,1.49)$，$b$ 被带得离目标远了一大截，之后才折回来。梯度方向稳定时，Adam 每步约走 $\eta$，不会像梯度下降那样随梯度变小而自动缩小，所以后期要靠第 9 节把步长降下来。

> 自己试一试：用 $\eta=0.01$ 重算第 1 步，$\theta_1$ 是多少？
>
> 答案：第一步的更新量总是 $\eta\cdot\mathrm{sign}(\boldsymbol g)$（因为 $\hat m=g$，$\sqrt{\hat s}=|g|$），所以 $\theta_1=(0.01,\ 0.01)$。

**例 13**　例 12 里两个坐标的梯度只差 3.7 倍。大模型里同一层的参数可以差得悬殊得多：设两个参数的梯度一直约为 $1000$ 和 $0.001$（差 $10^6$ 倍）。分别用 SGD（$\eta=10^{-3}$）和 Adam（$\eta=10^{-3}$）走一步，比较各自的步长。

SGD：步长 $\eta g$，两个参数分别移动 $10^{-3}\times1000=1$ 和 $10^{-3}\times0.001=10^{-6}$。第一个一步就跳到 1 那么远（可能冲出去），第二个几乎没动，几乎训练不到。

Adam：两个参数在稳定梯度下步长都是 $\eta=10^{-3}$，同量级地前进。

这是大模型训练里常用 Adam 一类方法的一个原因：不同层的梯度尺度本来就没法统一。

合上书，说明 Adam 为何要做偏差修正，以及梯度稳定时除以 $\sqrt{\hat{\boldsymbol s}}$ 后步长为什么约为 $\eta$。

AdamW 的 W 指**权重衰减**，它与梯度更新分开做：更新式后面再减去 $\eta\lambda_{\mathrm{wd}}\theta$（$\lambda_{\mathrm{wd}}$ 是一个小系数），它与 L2 正则的关系在 M.3 讲。章首那一行里只剩“预热之后余弦衰减”没有讲，是下一节。

### 9. 训练过程中学习率该怎样变化？

例 12 留下了两个现象。一头是后半段：Adam 到了谷底附近，每步仍约走 $\eta$，$\eta$ 不降，参数就在最小点附近晃。另一头是第一步：$\hat{\boldsymbol s}$ 只由一个梯度算出，却已经让每个坐标走满 $\eta$，这个步长其实没有多少依据。前面的 $\eta$ 都是常数，实践里它随时间变，对应两头各有一个做法。

**预热**：训练开头的几百到几千步，$\eta$ 从接近 0 线性升到目标值。理由就是上面的第二个现象：开头 $\hat{\boldsymbol m}$ 和 $\hat{\boldsymbol s}$ 只由很少的几个梯度估计，不可靠，步长不能放开。

**衰减**：训练后期把 $\eta$ 逐渐调小。第 6 节说过，SGD 在谷底附近 $\eta$ 越大抖得越厉害，$\eta$ 变小，抖动变小，参数才能落进更深的谷底。

这是一种常用的调度方案，不是所有训练都必须这样做，也有不预热或用别的衰减形状的做法。

常用的是**余弦衰减**：设预热 $T_w$ 步，总共 $T$ 步，$t\ge T_w$ 时

$$\eta_t=\eta_{\min}+\frac12(\eta_{\max}-\eta_{\min})\Big(1+\cos\frac{\pi(t-T_w)}{T-T_w}\Big).$$

$t=T_w$ 时括号里是 $1+1=2$，$\eta_t=\eta_{\max}$；$t=T$ 时是 $1+(-1)=0$，$\eta_t=\eta_{\min}$；中间走一条平滑的余弦曲线，学习率下降的速度先慢后快再慢。

![预热阶段线性上升，之后沿余弦曲线下降到最小值](fig/M1-n7.pdf){width=70%}

**例 14**　把上面的公式代入具体的超参数。某次训练设 $\eta_{\max}=3\times10^{-4}$，$\eta_{\min}=3\times10^{-5}$，预热 $T_w=100$ 步，总步数 $T=1100$。求 $t=50$、$600$、$1100$ 时的学习率。

$t=50$ 在预热阶段，线性上升：$3\times10^{-4}\times50/100=1.5\times10^{-4}$。

$t=600$：$(t-T_w)/(T-T_w)=500/1000=0.5$，$\cos(\pi/2)=0$，

$$\eta=3\times10^{-5}+\tfrac12(2.7\times10^{-4})(1+0)=1.65\times10^{-4}.$$

$t=1100$：比值为 1，$\cos\pi=-1$，$\eta=\eta_{\min}=3\times10^{-5}$。

> 自己试一试：同样的设置，求 $t=300$ 时的学习率。
>
> 答案：$(300-100)/1000=0.2$，$\cos(0.2\pi)\approx0.809$，$\eta=3\times10^{-5}+\frac12(2.7\times10^{-4})(1.809)\approx2.74\times10^{-4}$。

合上书，写出预热加余弦衰减的学习率公式，并说明开头为什么要预热、后期为什么要衰减。

**回到开头的问题。** 章首那一行是“AdamW，$\beta_1=0.9$，$\beta_2=0.95$，预热后余弦衰减”，现在每个词都有了意思。Adam 是第 8 节的更新，每个坐标步长约 $\eta$。$\beta_1=0.9$ 表示 $\boldsymbol m$ 大致平均最近 $1/(1-\beta_1)=10$ 步的梯度，$\beta_2=0.95$ 表示 $\boldsymbol s$ 大致平均最近 20 步的梯度平方（常见的 0.999 是 1000 步，0.95 对梯度大小的变化反应快得多）。预热是开头把 $\eta$ 线性升到 $\eta_{\max}$，余弦衰减是之后按例 14 的公式降到 $\eta_{\min}$。W 留到 M.3。

回到三件套，本章讲的是第三格（更新规则）从最朴素的梯度下降长到 AdamW 的全过程，模型和损失两格留给后面各章。合上书，试着自己写出：（1）二次函数上梯度下降收敛的证明三步；（2）Adam 为什么要除以 $1-\beta^t$；（3）小批量梯度为什么无偏。

### 本章小结

| 方法 | 什么时候用 | 对应题号 |
|---|---|---|
| 方法 1（写出训练的损失） | 把“训练一个模型”翻成最小化一个函数 | M1-01 |
| 方法 2（梯度下降一步） | 已知损失与起点，走一步或几步 | M1-02 |
| 方法 3（用特征值判断学习率） | 问学习率上限、收敛快慢、条件数 | M1-03、M1-05、M1-10 |
| 方法 4（用 Hessian 判断凸性） | 问停下来的点是不是全局最小 | M1-04、M1-10 |
| 方法 5（小批量梯度） | 数据多，估计梯度，问无偏与方差 | M1-06 |
| 方法 6（动量） | 山谷窄长，梯度反复变号 | M1-07、M1-11 |
| 方法 7（Adam 一步） | 参数梯度尺度差异大 | M1-08 |
| 预热与余弦衰减（读值） | 已知超参数，求某一步的学习率 | M1-09 |

训练技巧一栏，本章先填四行（以后各章继续补）：

| 技巧 | 它治的是什么病 | 为什么能治 |
|---|---|---|
| 小批量 | 每步要扫全部数据，太贵 | 无偏估计，方差按 $1/B$ 缩小 |
| 动量 | 窄谷里反复折返 | 滑动平均抵消变号分量，累积同号分量 |
| Adam | 各参数梯度尺度悬殊 | 除以梯度的滑动均方根，每个坐标步长约为 $\eta$ |
| 预热加余弦衰减 | 开头统计量不可靠，后期抖动 | 先小步升上去，再逐渐降下来 |
