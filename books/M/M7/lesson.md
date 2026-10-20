## M.7 · 多层网络与反向传播

PyTorch 里写一行 `loss.backward()`（`loss` 是损失，一个数；这一行的意思是「从损失出发，往回算出每个参数的偏导」），就能得到几十亿个参数各自的偏导数，花的时间只是前向计算的几倍。如果用 M.1 的办法，每个参数单独把损失算两遍再相减，几十亿个参数要算几十亿遍，根本做不到。这一行背后的算法，就是本章的反向传播。

它是被一个失败逼出来的。1950 年代末 Rosenblatt 的感知机只有一层，只能用一条直线（一个超平面）分开两类。1969 年 Minsky 与 Papert 指出，它连「异或」都学不会。多层网络当然更强，但当时没人知道怎样训练：每多一层，损失对参数的依赖就多套一层函数。办法其实就是 C.21 的链式法则，只是要把它组织成可以机械执行的步骤。反向模式的自动微分由 Linnainmaa 在 1970 年提出，Werbos 随后想到用它训练神经网络，1986 年 Rumelhart、Hinton 与 Williams 用它训练出带隐藏层的网络，多层网络才真正流行起来。

对照三件套：模型是 M.2 的线性层叠成多层、层与层之间夹一个非线性；损失沿用 M.2.4 的交叉熵；更新规则仍是 M.1 的梯度下降。这一章新的只有一件事：梯度怎么算出来。

本章的顺序：第 1–3 节搭出多层网络，数清它的形状和参数；第 4–7 节把求梯度变成对计算图的两遍扫描，并说明为什么要从后往前扫；第 8–11 节把这个算法写成向量和矩阵的公式，用符号推出两层网络的全部梯度；第 12 节用数值梯度检验推导有没有错。

### 1. 一条直线分不开的数据怎么办？

异或（XOR）问题：输入 $(x_1,x_2)\in\{0,1\}^2$，$(0,0)$ 与 $(1,1)$ 标签为 0，$(0,1)$ 与 $(1,0)$ 标签为 1。M.2.3 的模型在 $\boldsymbol w^{\mathsf T}\boldsymbol x+b>0$ 时判为 1，我们看有没有 $\boldsymbol w,b$ 让四个点都判对。标签为 1 的点要求得分大于 0，标签为 0 的点要求得分不大于 0（得分恰为 0 时 M.2.3 判为 0），四个点各给出一个不等式：

$$b\le0,\qquad w_1+w_2+b\le0,\qquad w_1+b>0,\qquad w_2+b>0 .$$

后两式相加得 $w_1+w_2+2b>0$，即 $w_1+w_2+b>-b$。第一式说 $-b\ge0$，所以 $w_1+w_2+b>0$，和第二式矛盾。因此任何一条直线都分不开异或。

读者很自然会想：多叠几层线性层，总该更强了吧？不会。叠两层得到

$$W_2(W_1\boldsymbol x+\boldsymbol b_1)+\boldsymbol b_2=(W_2W_1)\boldsymbol x+(W_2\boldsymbol b_1+\boldsymbol b_2),$$

仍然是一个矩阵乘 $\boldsymbol x$ 再加一个向量，等价于一层（L.3 里矩阵乘法就是变换的复合，线性变换的复合还是线性变换）。所以层与层之间必须夹一个**非线性**函数 $\varphi$，叫**激活函数**。

形式如下。输入 $\boldsymbol x$，先做线性变换，再逐分量过一遍 $\varphi$，作为**隐藏层**的输出 $\boldsymbol h$；再做一次线性变换，得到输出：

$$\boldsymbol z_1=W_1\boldsymbol x+\boldsymbol b_1,\qquad \boldsymbol h=\varphi(\boldsymbol z_1),\qquad \boldsymbol z_2=W_2\boldsymbol h+\boldsymbol b_2 .$$

这样的网络叫**多层感知机**（MLP）。每一个 $W\boldsymbol x+\boldsymbol b$ 叫**线性层**（全连接层），$\boldsymbol z_1$ 叫它的**预激活**（过 $\varphi$ 之前的值）。

**方法 1（用隐藏层构造/前向计算）**

1. 先逐层算预激活 $\boldsymbol z_1=W_1\boldsymbol x+\boldsymbol b_1$。
2. 逐分量过激活函数得 $\boldsymbol h$。
3. 再算输出 $\boldsymbol z_2$。每一层的输出是下一层的输入。

**例 1**　取 $\varphi=\operatorname{ReLU}$（$\varphi(z)=\max(0,z)$），$W_1=\begin{pmatrix}1&1\\1&1\end{pmatrix}$，$\boldsymbol b_1=(0,-1)^{\mathsf T}$，$W_2=(1,-2)$，$b_2=0$。验证这个网络算出异或。

先不问这组参数是怎么想出来的，把四个输入逐个送进去，看隐藏层怎样把点搬开。

这里 $\boldsymbol z_1=(x_1+x_2,\ x_1+x_2-1)^{\mathsf T}$，$h_1=\operatorname{ReLU}(x_1+x_2)$，$h_2=\operatorname{ReLU}(x_1+x_2-1)$，输出 $z_2=h_1-2h_2$。逐个输入代入：

| $(x_1,x_2)$ | $\boldsymbol z_1$ | $\boldsymbol h$ | $z_2$ |
|---|---|---|---|
| $(0,0)$ | $(0,-1)$ | $(0,0)$ | 0 |
| $(1,0)$ | $(1,0)$ | $(1,0)$ | 1 |
| $(0,1)$ | $(1,0)$ | $(1,0)$ | 1 |
| $(1,1)$ | $(2,1)$ | $(2,1)$ | 0 |

四个输出正好是 $0,1,1,0$。看隐藏层做了什么：它把输入平面上的点搬成 $\boldsymbol h$ 平面上的点，两个标签为 1 的点重合在了 $(1,0)$。搬完以后，标签 0 的点在 $(0,0)$ 和 $(2,1)$，标签 1 的点在 $(1,0)$。网络的输出 $z_2=h_1-2h_2$ 在这四个点上依次是 $0,1,1,0$，再取 $\tfrac12$（0 与 1 的中点）为阈值（$z_2>\tfrac12$ 判为 1），对应 $\boldsymbol h$ 平面上的直线 $h_1-2h_2=\tfrac12$，它把两类分开了。

![左：输入平面上的异或，四个点没有一条直线能分开；右：隐藏层把点搬到 $(h_1,h_2)$ 平面，两个标签为 1 的点（空心圆）重合在 $(1,0)$，实线可以把它们与标签为 0 的点（实心圆）分开](fig/M7-n1.pdf){width=90%}

> 同一个隐藏层，把输出层换成 $W_2=(-1,2)$，$b_2=1$，求四个输出。
>
> 答案：$z_2=1-h_1+2h_2$，依次是 $1,0,0,1$，这是异或的反面（同或）。

这就是 M.6 末尾提到的事：M.6 用核函数手工指定新坐标，这里新坐标由 $W_1,\boldsymbol b_1$ 决定，而它们是可以训练的。后面反复出场的是**老朋友②**：2-2-1 小网络，

$$\boldsymbol x=\begin{pmatrix}1\\2\end{pmatrix},\ y=1,\quad W_1=\begin{pmatrix}0.5&-0.5\\0.25&0.5\end{pmatrix},\ \boldsymbol b_1=\boldsymbol0,\quad \boldsymbol w_2=\begin{pmatrix}1\\-1\end{pmatrix},\ b_2=0,$$

隐藏层和输出层都用 sigmoid，损失是交叉熵，读作输入 2 维、隐藏层 2 个单元、输出 1 个数。

例 1 的 $W_1,\boldsymbol b_1$ 是凑出来的。真正的问题是：给一批数据，怎样让机器自己找到这些参数？这需要损失对 $W_1$ 每个元素的偏导，而 $\varphi$ 选什么会直接影响这些偏导，所以先看激活函数。

合上书，写出为什么线性层叠起来还是线性的，并说明隐藏层在异或问题里做了什么。

### 2. 常用的激活函数各有什么特点？

激活函数既要提供非线性，又要能求导，因为下面所有的梯度都要穿过它。四种最常见的：

- **sigmoid**：$\sigma(z)=\dfrac1{1+e^{-z}}$，值域 $(0,1)$（M.2.3）。
- **tanh**：$\tanh z=\dfrac{e^z-e^{-z}}{e^z+e^{-z}}=2\sigma(2z)-1$，值域 $(-1,1)$。
- **ReLU**：$\max(0,z)$。
- **GELU**：$z\,\Phi(z)$，$\Phi(z)$ 是标准正态变量小于 $z$ 的概率（P 册的分布函数），从 0 单调升到 1。$z$ 很负时 $\Phi\approx0$，输出接近 0；$z$ 很大时 $\Phi\approx1$，输出接近 $z$，所以它像一条平滑的 ReLU，常用在 Transformer 里。

#### 四种函数的导数

它们的导数各有一个好记的形式。

**sigmoid**：$\sigma'(z)=\dfrac{e^{-z}}{(1+e^{-z})^2}=\sigma(z)\cdot\dfrac{e^{-z}}{1+e^{-z}}=\sigma(z)\big(1-\sigma(z)\big)$，最后一步用到 $1-\sigma(z)=\dfrac{e^{-z}}{1+e^{-z}}$。

**tanh**：由 $\tanh z=2\sigma(2z)-1$ 求导（链式法则，里面的 $2z$ 带出一个因子 2）：

$$\tanh'z=4\sigma'(2z)=4\sigma(2z)\big(1-\sigma(2z)\big).$$

再把 $\sigma(2z)=\frac{1+\tanh z}{2}$ 代入，右边变成 $4\cdot\frac{1+\tanh z}2\cdot\frac{1-\tanh z}2$，得 $\tanh'z=1-\tanh^2z$。

**ReLU**：$z>0$ 时导数为 1，$z<0$ 时为 0，$z=0$ 不可导，本书约定取 0。

**GELU**：乘积求导，$(z\Phi(z))'=\Phi(z)+z\,\Phi'(z)$，其中 $\Phi'(z)=\frac1{\sqrt{2\pi}}e^{-z^2/2}$ 是标准正态分布的密度函数。

前两个的导数可以用函数值自己表示。这在反向传播里很有用：前向已经算出 $\sigma(z)$ 并存下来了，求导时直接用，不用再算一遍指数。

| $z$ | $\sigma$ | $\sigma'$ | $\tanh$ | $\tanh'$ | ReLU | ReLU$'$ | GELU | GELU$'$ |
|---|---|---|---|---|---|---|---|---|
| $-2$ | 0.1192 | 0.1050 | $-0.9640$ | 0.0707 | 0 | 0 | $-0.0455$ | $-0.0852$ |
| $0$ | 0.5 | 0.25 | 0 | 1 | 0 | 0（约定） | 0 | 0.5 |
| $2$ | 0.8808 | 0.1050 | 0.9640 | 0.0707 | 2 | 1 | 1.9545 | 1.0852 |

![四种激活函数（上）与导数（下）：sigmoid 实线、tanh 虚线、ReLU 点线、GELU 点划线。sigmoid 与 tanh 的导数在 $\lvert z\rvert$ 大时趋近 0，ReLU 的导数只取 0 和 1](fig/M7-n2.pdf){width=95%}

#### 从表里读出三件事


第一，sigmoid 的导数最大只有 0.25，$|z|$ 一大就接近 0，这叫**饱和**。梯度要连续穿过很多层，每过一层都会乘上这一层的激活导数（还要乘权重矩阵），饱和时这个导数接近 0，连乘以后到第一层可能几乎只剩零头；M.8.2 专门讲这件事。tanh 的最大导数是 1（在 $z=0$ 处），好一些，但同样会饱和。

第二，ReLU 在 $z>0$ 时导数恒为 1，不会饱和，计算也最便宜；代价是 $z<0$ 的单元梯度为 0，如果对所有样本都小于 0，这个单元就再也学不动。

第三，为什么不用最直观的阶跃函数（$z>0$ 取 1，否则取 0）？它的导数几乎处处为 0，梯度下降拿不到任何方向，训练没法进行。

**方法 2（激活函数的导数）** 求 $\varphi'(z)$ 时：sigmoid 用 $\sigma(1-\sigma)$，tanh 用 $1-\tanh^2$，ReLU 看 $z$ 的符号，GELU 用 $\Phi+z\Phi'$。前向时存下 $\varphi(z)$，前两者可以直接复用。

**例 2**　求 $z=-1$ 与 $z=0.5$ 处 sigmoid、tanh、ReLU 的导数。

例 1 的隐藏层用的是 ReLU，现在不算整个网络，只问隐藏层里一个激活函数在某一点的导数。

$z=-1$：$\sigma(-1)=0.2689$，$\sigma'=0.2689\times0.7311=0.1966$；$\tanh(-1)=-0.7616$，$\tanh'=1-0.5800=0.4200$；$z<0$，ReLU 的导数为 0。

$z=0.5$：$\sigma(0.5)=0.6225$，$\sigma'=0.6225\times0.3775=0.2350$；$\tanh(0.5)=0.4621$，$\tanh'=1-0.2135=0.7864$；ReLU 的导数为 1。

老朋友②的隐藏层 $\boldsymbol z_1=(-0.5,1.25)$ 就是这样用上的：$\sigma(\boldsymbol z_1)=(0.3775,0.7773)$，导数 $h(1-h)=(0.2350,0.1731)$。

> 求 $z=2$ 处 sigmoid、tanh、ReLU 的导数。
>
> 答案：$\sigma'=0.8808\times0.1192=0.1050$；$\tanh'=1-0.9640^2=0.0707$；ReLU 的导数为 1。

合上书，写出 sigmoid、tanh、ReLU 的导数，并说明 sigmoid 在 $\lvert z\rvert$ 很大时为什么会让梯度变得很小。

这些导数都只管一个激活函数。要把它们串成整个网络的梯度，先得弄清网络里每个量是数、向量还是矩阵，下一节先做这件事。

### 3. 多层感知机的形状和参数量怎么数？

AI 的公式读不懂，大多是因为不知道每个字母是数、向量还是矩阵。所以先养成习惯：**每个量写出形状**。

一个线性层把 $d$ 维变成 $m$ 维，$W\in\mathbb R^{m\times d}$，$\boldsymbol b\in\mathbb R^m$，参数个数 $md+m$。激活函数没有参数。网络的总参数就是各线性层相加。

老朋友②：$W_1$ 是 $2\times2$（4 个），$\boldsymbol b_1$ 有 2 个，$\boldsymbol w_2^{\mathsf T}$ 是 $1\times2$（2 个），$b_2$ 有 1 个，共 9 个参数。

训练时一次喂进去 $B$ 个样本。习惯上把样本一行一行叠成 $X\in\mathbb R^{B\times d}$（和数据表一致，一行一个样本）。这时单个样本的 $W\boldsymbol x+\boldsymbol b$ 变成

$$Z=XW^{\mathsf T}+\boldsymbol b^{\mathsf T},\qquad X\in\mathbb R^{B\times d},\ W^{\mathsf T}\in\mathbb R^{d\times m},\ Z\in\mathbb R^{B\times m}.$$

第 $b$ 行就是第 $b$ 个样本的 $W\boldsymbol x+\boldsymbol b$（转置之后写成行）。单个样本是 $W\boldsymbol x$，$W$ 是 $m\times d$；样本改成行以后要右乘 $W^{\mathsf T}$，公式里的转置就是这么来的。$\boldsymbol b^{\mathsf T}$ 只有一行，要加到 $Z$ 的每一行上，这叫**广播**。numpy 里一行代码：

```python
Z = X @ W.T + b      # X:(B,d)  W:(m,d)  b:(m,)  ->  Z:(B,m)
```

批量 $B$ 只改变数据的行数，不改变参数的个数。

**方法 3（数形状与参数）**

1. 从输入开始，每过一个线性层，最后一维从 $d$ 变成 $m$，批量维 $B$ 不变。
2. 激活函数不改形状。
3. 参数数 $=\sum(md+m)$。写出每个量的形状，矩阵乘的内侧维数必须相等。

**例 3**　一个 4–6–5–3 的 MLP（输入 4 维，两个隐藏层分别有 6 个和 5 个单元，输出 3 个数），批量 8，求每层输出的形状和总参数。

例 1 只有一个隐藏层，这里换成两个隐藏层并加上批量，也不算输出的值，只数形状和参数。

输出形状依次是 $8\times6$、$8\times5$、$8\times3$（激活函数不改变形状）。三个线性层的参数：

$$4\times6+6=30,\qquad 6\times5+5=35,\qquad 5\times3+3=18,$$

合计 $83$ 个。

> 把批量改成 16，参数个数变不变？第二层的 $W$ 是什么形状？
>
> 答案：不变，仍是 83；第二层 $W\in\mathbb R^{5\times6}$（输出维在前），$XW^{\mathsf T}$ 的形状 $16\times5$。

形状和参数数清了，但还没有回答怎么训练：老朋友②有 9 个参数，就要 9 个偏导，大模型要几十亿个。下一节先看怎样把求偏导变成机械的步骤。

合上书，说出批量 $B$ 为什么不影响参数个数，以及 $Z=XW^{\mathsf T}+\boldsymbol b^{\mathsf T}$ 里 $\boldsymbol b$ 是怎样加到每一行上的。

### 4. 一个有上亿参数的模型，怎样求出损失对每个参数的偏导？

M.2.5 里，逻辑回归的梯度是用链式法则一口气推出来的。网络一深，这样的推导就写不完了。直接的想法是对整个公式一次求导，但式子会随层数成倍变长，同一个中间量还会被反复重算。解决办法是先把整个计算拆成一步一步的基本运算，每一步只涉及一个简单函数（加、乘、$\sigma$、$\ln$），然后让计算机逐步处理。把这些步骤和它们的依赖关系画成图，就是**计算图**：每个节点是一个中间值，箭头从输入指向用到它的节点。

先拿最简单的情形练手，用 M.2 的逻辑回归，只看一个样本 $x=3$，$y=1$，参数 $w=0.5$，$b=-1$。模型是 $p=\sigma(wx+b)$，标签为 1 时交叉熵是 $-\ln p$。拆成四步：

$$u=w\,x,\qquad z=u+b,\qquad p=\sigma(z),\qquad \ell=-\ln p .$$

**前向**就是沿箭头方向把每个节点的值算出来：

$$u=1.5,\qquad z=0.5,\qquad p=\sigma(0.5)=0.6225,\qquad \ell=-\ln0.6225=0.4741 .$$

这些中间值要**记下来**，反向时会用到：$\sigma$ 的导数需要 $p$，乘法的导数需要另一个因子。

![逻辑回归的计算图：方框是节点，上方写前向算出的值；$w$、$b$ 是要求梯度的参数。箭头自左向右，是前向计算的方向](fig/M7-n3.pdf){width=95%}

**方法 4（画计算图并前向）**

1. 把损失的公式拆成基本运算，每个中间量取一个名字。
2. 按依赖的先后顺序（输入在前、损失在最后），逐个算出节点的值。
3. 把所有节点的值都存下来。

**例 4**　$z=w_1x_1+w_2x_2+b$，$a=\operatorname{ReLU}(z)$，$L=(a-t)^2$。取 $\boldsymbol x=(1,-2)$，$\boldsymbol w=(0.5,0.25)$，$b=0.5$，$t=1$，画出计算图并前向。

和上面的逻辑回归图相比，激活换成了 ReLU，损失换成了平方误差，并多了一个求和节点，前向的步骤相同。拆成

$$q_1=w_1x_1,\ \ q_2=w_2x_2,\ \ s=q_1+q_2,\ \ z=s+b,\ \ a=\operatorname{ReLU}(z),\ \ r=a-t,\ \ L=r^2 .$$

依次算：$q_1=0.5$，$q_2=-0.5$，$s=0$，$z=0.5$，$a=0.5$，$r=-0.5$，$L=0.25$。

> 同一个图，取 $b=-1$，其余不变，求 $L$。
>
> 答案：$z=-1$，$a=0$，$r=-1$，$L=1$。

老朋友②的前向也是这样走的：

$$\boldsymbol z_1=W_1\boldsymbol x=(-0.5,\ 1.25),\quad \boldsymbol h=\sigma(\boldsymbol z_1)=(0.3775,\ 0.7773),\quad z_2=\boldsymbol w_2^{\mathsf T}\boldsymbol h+b_2=-0.3998,$$

$$\hat y=\sigma(z_2)=0.4014,\qquad L=-\ln\hat y=0.9129 .$$

合上书，画出逻辑回归的计算图，说明前向为什么要把每个中间值都记下来。

前向只算出了损失的值，比如逻辑回归图里的 $\ell=0.4741$。训练要的是 $\partial\ell/\partial w$ 和 $\partial\ell/\partial b$，也就是 $w$ 动一点，$\ell$ 动多少。下一节顺着箭头反过来走，把它们求出来。

### 5. 沿着计算图往回走，链式法则变成了什么？

第 4 节的图里，$w$ 要经过 $u,z,p$ 三个节点才影响到 $\ell$。损失对 $w$ 的偏导，就是这几段变化率连乘，每一段只涉及一个简单函数。下面把这个想法写成规则。

目标是损失 $L$ 对每个参数的偏导数。记节点 $v$ 的**梯度** $\bar v=\partial L/\partial v$，它表示「这个节点的值动一点，损失动多少」。

最后一个节点是 $L$ 本身，$\bar L=1$。其余节点的梯度，要从后面一个节点的梯度算出来。设节点 $c=f(a)$，$a$ 只被 $c$ 一个节点用到（这个条件不能丢，第 6 节会看到去掉它会漏项）。C.21.1 的链式法则说

$$\frac{\partial L}{\partial a}=\frac{\partial L}{\partial c}\cdot\frac{\partial c}{\partial a},\qquad\text{即}\qquad \bar a=\bar c\cdot f'(a).$$

左边的 $\bar c$ 叫**上游梯度**（从后面传来的），$f'(a)$ 叫**局部导数**（只看这一个小运算）。所以反向传播的规则就一句话：**上游梯度乘局部导数**。每个节点只需知道自己这一步的导数，不用关心整个网络多复杂。

几个基本运算的局部规则：

- 加法 $c=a+b$：局部导数都是 1，所以 $\bar a=\bar b=\bar c$，上游梯度原样分给两边；
- 乘法 $c=ab$：$\bar a=\bar c\,b$，$\bar b=\bar c\,a$，各自乘上另一个因子；
- $c=\sigma(a)$：$\bar a=\bar c\,c(1-c)$；
- $c=\ln a$：$\bar a=\bar c/a$；
- $c=\operatorname{ReLU}(a)$：$a>0$ 时 $\bar a=\bar c$，否则为 0。

**方法 5（沿计算图反向传播）**

1. 在前向存好的值上，从损失出发，令 $\bar L=1$。
2. 沿箭头反方向，逐个节点用「上游梯度 × 局部导数」算出它的输入的梯度。
3. 走到参数节点，得到的 $\bar w$、$\bar b$ 就是损失对它的偏导。

**例 5**　对第 4 节的逻辑回归图做反向传播。

图和数值都沿用第 4 节，前向存下的 $u,z,p$ 现在派上用场：从 $\ell$ 往回走，把存下的值代入每个节点的局部导数。

先写每一步的局部规则，再代入前向的值：

$$\bar\ell=1,\qquad \bar p=\bar\ell\cdot\Big(-\frac1p\Big)=-1.6065,\qquad \bar z=\bar p\cdot p(1-p)=-1.6065\times0.2350=-0.3775 .$$

$\bar z=-0.3775=p-1=p-y$：中间的 $-1/p$ 与 $p(1-p)$ 相乘时，$p$ 约掉了，只剩 $p-1$。这正是 M.2.5 里「交叉熵对分数的梯度是 $p-y$」，现在是自然地走出来的。再往前，$z=u+b$ 是加法，上游梯度原样分给两边：

$$\bar u=\bar z=-0.3775,\qquad \bar b=\bar z=-0.3775,\qquad \bar w=\bar u\cdot x=-0.3775\times3=-1.1326 .$$

与 M.2.5 的公式 $(p-y)x=-0.3775\times3$ 一致。M.2.5 一口气推出的结论，在这里拆成了每步只涉及一个简单导数的小步。

> 同一张图，把输入换成 $x=2$，参数换成 $w=0.5$，$b=-1$（$y=1$ 不变），求 $\bar w$ 与 $\bar b$。
>
> 答案：前向 $u=1$，$z=0$，$p=0.5$，所以 $\bar z=p-1=-0.5$；$\bar b=\bar z=-0.5$，$\bar w=\bar z\cdot x=-1$。

**例 6**　对例 4 的 ReLU 图做反向传播。

和例 5 的区别是，这里有减法、平方和 ReLU，局部规则不同，其余流程相同。

$$\bar L=1,\quad \bar r=2r=-1,\quad \bar a=\bar r=-1\ (\text{减法对 }a\text{ 的导数是 }1),\quad \bar z=\bar a\ (\text{因 }z=0.5>0),$$

接着加法把梯度原样分给 $s$ 和 $b$，再分给 $q_1,q_2$：

$$\bar b=-1,\quad \bar q_1=\bar q_2=-1,\quad \bar w_1=\bar q_1x_1=-1,\quad \bar w_2=\bar q_2x_2=2 .$$

检验：$L=(\operatorname{ReLU}(w_1-2w_2+b)-1)^2$，在 $z>0$ 的区域里 $\partial L/\partial w_1=2(a-1)\cdot1=-1$，$\partial L/\partial w_2=2(a-1)\cdot(-2)=2$，与上面一致。

> 同一个图取 $b=-1$（此时 $z=-1$），求 $\bar w_1,\bar w_2,\bar b$。
>
> 答案：$z<0$，ReLU 的局部导数为 0，$\bar z=0$，往前所有梯度都是 0：$\bar w_1=\bar w_2=\bar b=0$。ReLU 把这条路关上了。

合上书，写出反向的局部规则（上游梯度乘局部导数），并说明 ReLU 在 $z<0$ 时为什么把往前的梯度全部关掉。

到这里每个节点都只被一个节点用到，规则只有一条。一个量被两处用到时，只用这一条会漏项，这是下一节的问题。

### 6. 一个中间量被好几处用到时，梯度怎么算？

到现在每个节点都只被一个节点用到。网络里更常见的是一个量被两处以上用到，例如输入 $x_j$ 同时送进隐藏层的每一个单元，或者一个参数被多个样本共用。这时 $a$ 有两条出路，$L$ 通过 $c_1$ 和 $c_2$ 两条路径依赖于 $a$。C.21.2 的树形图说：沿每条路径把偏导相乘，再把各条路径相加。

$$\frac{\partial L}{\partial a}=\frac{\partial L}{\partial c_1}\frac{\partial c_1}{\partial a}+\frac{\partial L}{\partial c_2}\frac{\partial c_2}{\partial a},\qquad\text{即}\qquad \bar a=\bar c_1\frac{\partial c_1}{\partial a}+\bar c_2\frac{\partial c_2}{\partial a}.$$

只取其中一条路径是不行的，会漏掉另一条路径的贡献，例 7 里漏掉的那一项就有 0.1966，占总梯度的五分之一。

**方法 6（分叉处梯度相加）** 处理节点 $a$ 时，每个用到 $a$ 的节点都给 $\bar a$ 贡献一项，把这些项全部加起来。程序里写成 `a_bar += ...`，不是 `=`。

这要求处理一个节点时，用到它的所有节点都已经处理过。所以必须按前向顺序的**逆序**走。

**例 7**　$L=u\cdot\sigma(u)$，$u=1$，求 $\partial L/\partial u$。

例 5、例 6 里每个量都只被用一次，这道题里 $u$ 被用到两次，两条路径的梯度要加起来。

这里 $u$ 同时进入乘法节点的两个位置：一条直接进入，一条先经过 $\sigma$。设 $s=\sigma(u)$，$L=u\cdot s$。前向：$s=0.7311$，$L=0.7311$。

反向，先处理乘法节点：$\bar s=\bar L\cdot u=1$，$u$ 沿直接那条路收到 $\bar L\cdot s=0.7311$。再处理 $\sigma$ 节点，$u$ 沿第二条路收到

$$\bar s\cdot\sigma'(u)=1\times0.7311\times0.2689=0.1966 .$$

把两项加起来：$\bar u=0.7311+0.1966=0.9277$。

验证：直接求导，$\dfrac{\mathrm{d}}{\mathrm{d}u}\big[u\sigma(u)\big]=\sigma(u)+u\sigma'(u)=0.7311+0.1966$，完全一致。

> $L=u\cdot u$，$u=3$。这时 $u$ 同时进入乘法的两个位置。用方法 6 求 $\bar u$。
>
> 答案：两个位置各贡献一项，$\bar u=u+u=6$，与 $\mathrm{d}(u^2)/\mathrm{d}u=2u$ 相同。

**例 8**　共用的参数。$L=(wx_1-y_1)^2+(wx_2-y_2)^2$，同一个 $w$ 被两个样本用到。取 $w=2$，$(x_1,y_1)=(1,1)$，$(x_2,y_2)=(3,2)$，求 $\partial L/\partial w$。

前面例 7 是一个中间量分叉，这里是一个参数分叉，规则相同。前向：第一项 $(2-1)^2=1$，第二项 $(6-2)^2=16$。每一项是一条路径，各自贡献

$$2(wx_1-y_1)x_1=2,\qquad 2(wx_2-y_2)x_2=2\times4\times3=24,$$

相加得 $\partial L/\partial w=26$。这就是小批量训练的梯度为什么是各个样本梯度的求和（或平均，M.1.6）：参数被每个样本共用，每个样本是一条路径。

![分叉：$u$ 同时进入乘法节点和 $\sigma$ 节点；实线箭头是前向，虚线箭头是反向，两条反向箭头在 $u$ 处汇合，梯度相加得 $0.7311+0.1966$](fig/M7-n4.pdf){width=70%}

合上书，说明一个量被两处用到时梯度为什么要相加，并用小批量的参数梯度举例。

有了这两条规则（上游梯度乘局部导数，分叉处相加），任何计算图的梯度都能算。可是为什么偏偏要从损失往回走？下一节比较两种走法的代价。

### 7. 为什么要从后往前算，而不是从前往后？

读者可能想到另一个办法：链式法则的乘法顺序是可以选的，为什么非要从损失往回走？也可以从某个参数出发，沿着箭头方向，把「它的变化怎样传到每个节点」一路算下去，这叫**前向模式**。我们走的叫**反向模式**。两者算出的结果相同，区别在代价。

前向模式从一个参数 $w_j$ 出发，一遍可以算出**所有节点**对这一个参数的导数，也就是每个节点对 $w_j$ 的偏导。想要损失对全部 $N$ 个参数的偏导，要跑 $N$ 遍。反向模式从损失出发，一遍可以算出损失对**所有节点**的导数，其中就包括全部参数，只需要一遍。

训练里损失只有一个数，参数却有上亿个，所以走反向。老朋友②有 9 个参数，前向模式要 9 遍，反向模式 1 遍。

这个选择取决于输出的个数。如果只有一个输入、却有很多输出，前向模式一遍就够，反向模式反而要跑和输出个数一样多的遍数。训练恰好是多输入、单输出的情形。

#### 两种顺序差多少？

用矩阵乘法可以把代价看得更清楚。设 $\boldsymbol x\to\boldsymbol y_1\to\boldsymbol y_2\to L$，每一步把「输出对输入的全部偏导」排成一张表：$J_1$ 的第 $(i,j)$ 个元素是 $\partial y_{1,i}/\partial x_j$，$J_2$ 的是 $\partial y_{2,i}/\partial y_{1,j}$，这样的表叫雅可比矩阵（第 8 节再讲它的形状约定）；$L$ 是一个数，所以 $J_3$ 只有一行。链式法则给出

$$\Big(\frac{\partial L}{\partial\boldsymbol x}\Big)^{\mathsf T}=J_3\,J_2\,J_1 .$$

这个式子可以由第 8 节的规则看出来：$\bar{\boldsymbol y}_2=J_3^{\mathsf T}$，$\bar{\boldsymbol y}_1=J_2^{\mathsf T}\bar{\boldsymbol y}_2$，$\bar{\boldsymbol x}=J_1^{\mathsf T}\bar{\boldsymbol y}_1=J_1^{\mathsf T}J_2^{\mathsf T}J_3^{\mathsf T}$，整体转置就是上式。左边是转置，因为 $J_3$ 只有一行，乘出来是一个行向量；第 8 节约定梯度写成列向量，转置回去就是它。

矩阵乘法满足结合律，可以先算右边的 $J_2J_1$（前向模式的顺序），也可以先算左边的 $J_3J_2$（反向模式的顺序），结果相同。但一个行向量乘矩阵，比两个矩阵相乘便宜得多。

**例 9**　$\boldsymbol x\in\mathbb R^{10}$，$\boldsymbol y_1\in\mathbb R^{20}$，$\boldsymbol y_2\in\mathbb R^{30}$，$L$ 是数。比较两种乘法顺序的乘法次数。

例 5–8 都在算梯度的值，这道题不算梯度，只数上面两种乘法顺序各要多少次乘法。

$J_1$ 是 $20\times10$，$J_2$ 是 $30\times20$，$J_3$ 是 $1\times30$。一个 $\alpha\times\beta$ 的矩阵乘 $\beta\times\gamma$ 的矩阵需要 $\alpha\beta\gamma$ 次乘法。

先算 $J_2J_1$：$30\times20\times10=6000$ 次，再乘 $J_3$：$1\times30\times10=300$ 次，共 6300。

先算 $J_3J_2$：$1\times30\times20=600$ 次，再乘 $J_1$：$1\times20\times10=200$ 次，共 800。

维数放大到每层 1000，两者分别是约 $10^9$ 和 $2\times10^6$ 次，相差 500 倍。

反向模式的代价是：必须把前向的所有中间值存下来，因为每步的局部导数要用它们。这是训练比推理占用更多显存的一个主要原因。

> $\boldsymbol x\in\mathbb R^{5}$，$\boldsymbol y_1\in\mathbb R^{8}$，$\boldsymbol y_2\in\mathbb R^{4}$，$L$ 是数，两种顺序各多少次乘法？
>
> 答案：$J_1$ 是 $8\times5$，$J_2$ 是 $4\times8$，$J_3$ 是 $1\times4$。先算 $J_2J_1$：$4\cdot8\cdot5+1\cdot4\cdot5=180$；先算 $J_3J_2$：$1\cdot4\cdot8+1\cdot8\cdot5=72$。

合上书，说明为什么训练神经网络用反向模式，以及它要付出什么代价。

### 8. 对向量、矩阵求导，结果是什么形状？

第 5、6 节的节点都是一个数。真正的网络里，节点是向量甚至矩阵：一层 $\boldsymbol y=W\boldsymbol x+\boldsymbol b$ 有 $m$ 个输出、$d$ 个输入，如果每个数都画一个节点，图就太大了。要把「上游梯度乘局部导数」搬到向量上，先定好导数的形状。

对损失 $L$ 求导，**梯度的形状约定与被求导的量相同**：$\boldsymbol x\in\mathbb R^d$ 则 $\partial L/\partial\boldsymbol x\in\mathbb R^d$（列向量，L.14.8），$W\in\mathbb R^{m\times d}$ 则 $\partial L/\partial W\in\mathbb R^{m\times d}$，第 $(i,j)$ 个元素是 $\partial L/\partial W_{ij}$。这样 $W\leftarrow W-\eta\,\partial L/\partial W$ 才能直接做。

对向量值函数 $\boldsymbol y=f(\boldsymbol x)$，$\boldsymbol x\in\mathbb R^d$，$\boldsymbol y\in\mathbb R^m$，**雅可比矩阵** $J\in\mathbb R^{m\times d}$ 的元素是 $J_{ij}=\partial y_i/\partial x_j$：行对应输出，列对应输入。它是一元函数导数的推广，若 $f$ 在该点可微，则在 $\boldsymbol x$ 附近 $\boldsymbol y$ 的变化约为 $J\,\mathrm{d}\boldsymbol x$（C.20.6）。

先看最小的情形：两个输入 $x_1,x_2$，两个输出 $y_1,y_2$。$x_1$ 同时影响 $y_1$ 和 $y_2$，由第 6 节，$\bar x_1=\bar y_1\dfrac{\partial y_1}{\partial x_1}+\bar y_2\dfrac{\partial y_2}{\partial x_1}$，$\bar x_2$ 同理。四个偏导排成的 $2\times2$ 表就是雅可比矩阵，这两个式子合起来正是它的转置乘 $(\bar y_1,\bar y_2)^{\mathsf T}$。

一般情形同理。已知上游梯度 $\bar{\boldsymbol y}=\partial L/\partial\boldsymbol y\in\mathbb R^m$，求 $\bar{\boldsymbol x}$。$L$ 通过每一个 $y_i$ 依赖于 $x_j$，$m$ 条路径相加（第 6 节）：

$$\frac{\partial L}{\partial x_j}=\sum_{i=1}^m\frac{\partial L}{\partial y_i}\frac{\partial y_i}{\partial x_j}=\sum_{i=1}^m J_{ij}\,\bar y_i=(J^{\mathsf T}\bar{\boldsymbol y})_j .$$

所以

$$\boxed{\ \bar{\boldsymbol x}=J^{\mathsf T}\,\bar{\boldsymbol y}\ }$$

这里出现了转置：$J$ 的行对应输出，求和 $\sum_i$ 是沿着行的方向走的，而 $\bar{\boldsymbol x}$ 的下标 $j$ 是列，写成矩阵乘就是 $J^{\mathsf T}$。

形状是最好的检验：$J^{\mathsf T}\in\mathbb R^{d\times m}$，$\bar{\boldsymbol y}\in\mathbb R^m$，乘出 $\mathbb R^d$，与 $\boldsymbol x$ 同形。如果推出的式子形状对不上，一定是错的。反过来，形状对得上并不保证没错：方阵的 $W$ 与 $W^{\mathsf T}$ 形状相同，写反了形状照样对得上，这类错要靠第 12 节的数值检验才能发现。

**方法 7（向量的反向传播与形状核对）**

1. 写出每个量的形状和雅可比矩阵 $J$（行：输出，列：输入）。
2. 反向：$\bar{\boldsymbol x}=J^{\mathsf T}\bar{\boldsymbol y}$。
3. 用「与被求导的量同形」核对结果，对不上就检查转置和乘法顺序。

**例 10**　$\boldsymbol y=(x_1x_2,\ x_1+x_2)^{\mathsf T}$，在 $\boldsymbol x=(2,3)^{\mathsf T}$ 处，上游梯度 $\bar{\boldsymbol y}=(1,-1)^{\mathsf T}$，求 $\bar{\boldsymbol x}$。

例 5–7 的节点都是一个数，这道题的节点是二维向量，局部导数换成了雅可比矩阵。

先写雅可比矩阵：

$$J=\begin{pmatrix}\partial y_1/\partial x_1&\partial y_1/\partial x_2\\ \partial y_2/\partial x_1&\partial y_2/\partial x_2\end{pmatrix}=\begin{pmatrix}x_2&x_1\\1&1\end{pmatrix}=\begin{pmatrix}3&2\\1&1\end{pmatrix}.$$

反向：

$$\bar{\boldsymbol x}=J^{\mathsf T}\bar{\boldsymbol y}=\begin{pmatrix}3&1\\2&1\end{pmatrix}\begin{pmatrix}1\\-1\end{pmatrix}=\begin{pmatrix}2\\1\end{pmatrix}.$$

验证：把 $\bar y_i$ 当常数，取辅助函数 $\widetilde L=\bar y_1y_1+\bar y_2y_2$（只用来检验，不是真实的损失），它对 $y_i$ 的偏导正好是 $\bar y_i$，所以它对 $\boldsymbol x$ 的梯度应该是 $J^{\mathsf T}\bar{\boldsymbol y}$。这里 $\widetilde L=x_1x_2-(x_1+x_2)$，梯度 $(x_2-1,\ x_1-1)=(2,1)$，与上面一致。

> $\boldsymbol y=(x_1^2,\ x_1x_2)^{\mathsf T}$，在 $\boldsymbol x=(1,2)^{\mathsf T}$ 处，$\bar{\boldsymbol y}=(1,1)^{\mathsf T}$，求 $\bar{\boldsymbol x}$。
>
> 答案：$J=\begin{pmatrix}2x_1&0\\x_2&x_1\end{pmatrix}=\begin{pmatrix}2&0\\2&1\end{pmatrix}$，$\bar{\boldsymbol x}=J^{\mathsf T}\bar{\boldsymbol y}=(4,1)^{\mathsf T}$。

合上书，写出向量反向传播的公式 $\bar{\boldsymbol x}=J^{\mathsf T}\bar{\boldsymbol y}$，并说明怎样用「与被求导的量同形」核对结果。

### 9. 一层 $\boldsymbol y=W\boldsymbol x+\boldsymbol b$ 的梯度，怎样一次写出来？

线性层是网络里出现最多的一步，它的反向公式值得单独推一遍，之后直接用。

先看 $2\times3$ 的小情形：$y_1=W_{11}x_1+W_{12}x_2+W_{13}x_3+b_1$，$y_2$ 同理。$W_{12}$ 只出现在 $y_1$ 里，系数是 $x_2$，所以 $\partial L/\partial W_{12}=\bar y_1x_2$；$x_2$ 则同时出现在 $y_1$ 和 $y_2$ 里，系数分别是 $W_{12}$ 和 $W_{22}$。下面把这个观察写成一般形式。

设 $W\in\mathbb R^{m\times d}$，$\boldsymbol y=W\boldsymbol x+\boldsymbol b$，已知上游梯度 $\boldsymbol\delta=\bar{\boldsymbol y}\in\mathbb R^m$。逐分量写出 $y_i=\sum_jW_{ij}x_j+b_i$，从这个式子读出各个偏导数。

对 $W_{ij}$：$W_{ij}$ 只出现在 $y_i$ 里，系数是 $x_j$，所以

$$\frac{\partial L}{\partial W_{ij}}=\frac{\partial L}{\partial y_i}\frac{\partial y_i}{\partial W_{ij}}=\delta_i\,x_j .$$

第 $(i,j)$ 个元素是 $\delta_ix_j$ 的矩阵，正是外积 $\boldsymbol\delta\boldsymbol x^{\mathsf T}$（L.3），形状 $m\times d$，与 $W$ 同形。

对 $b_i$：$\partial y_i/\partial b_i=1$，所以 $\partial L/\partial\boldsymbol b=\boldsymbol\delta$。

对 $x_j$：$x_j$ 出现在每一个 $y_i$ 里，系数是 $W_{ij}$，$m$ 条路径相加（第 6 节）：

$$\frac{\partial L}{\partial x_j}=\sum_i\delta_iW_{ij}=(W^{\mathsf T}\boldsymbol\delta)_j .$$

这与第 8 节的 $J^{\mathsf T}\bar{\boldsymbol y}$ 一致，因为线性层的雅可比矩阵就是 $W$。

**方法 8（线性层的反向）** 已知 $\boldsymbol\delta=\partial L/\partial\boldsymbol y$：

$$\frac{\partial L}{\partial W}=\boldsymbol\delta\,\boldsymbol x^{\mathsf T},\qquad \frac{\partial L}{\partial\boldsymbol b}=\boldsymbol\delta,\qquad \frac{\partial L}{\partial\boldsymbol x}=W^{\mathsf T}\boldsymbol\delta .$$

#### 一批样本怎么办？

训练时一次喂进 $B$ 个样本：样本为行，$X\in\mathbb R^{B\times d}$，$Y=XW^{\mathsf T}+\boldsymbol b^{\mathsf T}$，$\Delta=\partial L/\partial Y\in\mathbb R^{B\times m}$。第 $b$ 个样本的输入是 $X$ 的第 $b$ 行 $\boldsymbol x_b$，上游梯度是 $\Delta$ 的第 $b$ 行 $\boldsymbol\delta_b$。分三步看：

1. $W$ 被所有样本共用（第 6 节），每个样本贡献一项外积，所以对样本求和 $\sum_b\boldsymbol\delta_b\boldsymbol x_b^{\mathsf T}$。它的第 $(i,j)$ 个元素是 $\sum_b\Delta_{bi}X_{bj}$，正好是 $\Delta^{\mathsf T}X$ 的第 $(i,j)$ 个元素，所以 $\partial L/\partial W=\Delta^{\mathsf T}X$。
2. $\boldsymbol b$ 也被共用，每个样本贡献 $\boldsymbol\delta_b$，求和就是把 $\Delta$ 的各行相加，写成 $\Delta^{\mathsf T}\boldsymbol 1$，$\boldsymbol 1$ 是元素全为 1 的 $B$ 维向量。
3. $X$ 的第 $b$ 行只影响第 $b$ 个样本，它的梯度是 $W^{\mathsf T}\boldsymbol\delta_b$ 转成行，叠起来就是 $\Delta W$。

$$\frac{\partial L}{\partial W}=\Delta^{\mathsf T}X,\qquad \frac{\partial L}{\partial\boldsymbol b}=\Delta^{\mathsf T}\boldsymbol 1,\qquad \frac{\partial L}{\partial X}=\Delta\,W .$$

```python
dW = Delta.T @ X          # (m,B)@(B,d) -> (m,d)，与 W 同形
db = Delta.sum(axis=0)    # 对批量维求和 -> (m,)
dX = Delta @ W            # (B,m)@(m,d) -> (B,d)，与 X 同形
```

注意每个公式里内侧维数都对得上，这是检验有没有写反的最快办法。前向有一次矩阵乘，反向有 $\partial W$ 和 $\partial X$ 两次，每次的大小和前向相同，所以一次反向大约是前向的两倍计算量。

**例 11**　$W=\begin{pmatrix}1&0&2\\-1&1&0\end{pmatrix}$，$\boldsymbol x=(1,2,-1)^{\mathsf T}$，上游梯度 $\boldsymbol\delta=(1,-2)^{\mathsf T}$，求 $\partial L/\partial W$、$\partial L/\partial\boldsymbol b$、$\partial L/\partial\boldsymbol x$，再对批量 $B=2$ 做一遍。

和例 10 相比，雅可比矩阵换成了线性层的 $W$，于是结果可以用外积直接写出；这次再加上批量。

形状：$W$ 是 $2\times3$，$\boldsymbol x$ 是 3 维，$\boldsymbol y$ 是 2 维，$\boldsymbol\delta$ 是 2 维，与 $\boldsymbol y$ 同形。

$$\frac{\partial L}{\partial W}=\boldsymbol\delta\boldsymbol x^{\mathsf T}=\begin{pmatrix}1\\-2\end{pmatrix}(1,2,-1)=\begin{pmatrix}1&2&-1\\-2&-4&2\end{pmatrix},\qquad \frac{\partial L}{\partial\boldsymbol b}=\begin{pmatrix}1\\-2\end{pmatrix},$$

$$\frac{\partial L}{\partial\boldsymbol x}=W^{\mathsf T}\boldsymbol\delta=\begin{pmatrix}1&-1\\0&1\\2&0\end{pmatrix}\begin{pmatrix}1\\-2\end{pmatrix}=\begin{pmatrix}3\\-2\\2\end{pmatrix}.$$

批量：再加一个样本 $\boldsymbol x'=(0,1,1)^{\mathsf T}$，其上游梯度 $\boldsymbol\delta'=(0,3)^{\mathsf T}$。叠成 $X=\begin{pmatrix}1&2&-1\\0&1&1\end{pmatrix}$，$\Delta=\begin{pmatrix}1&-2\\0&3\end{pmatrix}$。

$$\Delta^{\mathsf T}X=\begin{pmatrix}1&2&-1\\-2&-1&5\end{pmatrix}\ \Big(=\boldsymbol\delta\boldsymbol x^{\mathsf T}+\boldsymbol\delta'\boldsymbol x'^{\mathsf T}\Big),\quad \Delta^{\mathsf T}\boldsymbol1=\begin{pmatrix}1\\1\end{pmatrix},\quad \Delta W=\begin{pmatrix}3&-2&2\\-3&3&0\end{pmatrix}.$$

最后一个矩阵的第一行就是单样本的 $W^{\mathsf T}\boldsymbol\delta$。

> 把 $W$ 换成 $\begin{pmatrix}2&-1\\0&3\end{pmatrix}$，$\boldsymbol x=(1,-1)^{\mathsf T}$，$\boldsymbol\delta=(1,2)^{\mathsf T}$，求 $\partial L/\partial W$ 和 $\partial L/\partial\boldsymbol x$。
>
> 答案：$\boldsymbol\delta\boldsymbol x^{\mathsf T}=\begin{pmatrix}1&-1\\2&-2\end{pmatrix}$；$W^{\mathsf T}\boldsymbol\delta=\begin{pmatrix}2&0\\-1&3\end{pmatrix}\begin{pmatrix}1\\2\end{pmatrix}=\begin{pmatrix}2\\5\end{pmatrix}$。

合上书，写出 $\partial L/\partial W$、$\partial L/\partial\boldsymbol b$、$\partial L/\partial\boldsymbol x$ 三个式子，并给每个量标上形状。

线性层只是网络的一半，层与层之间还夹着激活函数。下一节看逐元素的函数怎样反向。

### 10. 逐元素作用的函数，梯度为什么是对应相乘？

激活函数是逐分量作用的：$\boldsymbol h=\varphi(\boldsymbol z)$ 的意思是 $h_i=\varphi(z_i)$，每个输出只依赖同下标的输入。它的雅可比矩阵 $J_{ij}=\partial h_i/\partial z_j$：$i\ne j$ 时 $h_i$ 不含 $z_j$，导数为 0；$i=j$ 时为 $\varphi'(z_i)$。所以 $J$ 是对角矩阵：

$$J=\operatorname{diag}\big(\varphi'(z_1),\dots,\varphi'(z_n)\big).$$

老朋友②的隐藏层就是这样：$\boldsymbol z_1=(-0.5,1.25)$，$h_1$ 只由 $z_{1,1}$ 决定，$h_2$ 只由 $z_{1,2}$ 决定，$J=\operatorname{diag}(0.2350,\ 0.1731)$。

代入第 8 节的 $\bar{\boldsymbol z}=J^{\mathsf T}\bar{\boldsymbol h}$。对角矩阵乘向量就是各分量分别相乘，所以

$$\bar z_i=\varphi'(z_i)\,\bar h_i,\qquad\text{即}\qquad \bar{\boldsymbol z}=\bar{\boldsymbol h}\odot\varphi'(\boldsymbol z).$$

$\odot$ 是**哈达玛积**（两个同形的向量或矩阵，对应位置相乘）。实际计算不会真的造出 $n\times n$ 的对角矩阵（它几乎全是 0，白白占 $n^2$ 个位置），只存 $n$ 个导数值，用一次对应相乘代替矩阵乘。

**方法 9（逐元素函数的反向）** $\bar{\boldsymbol z}=\bar{\boldsymbol h}\odot\varphi'(\boldsymbol z)$。sigmoid 用前向存的 $\boldsymbol h$：$\varphi'=\boldsymbol h\odot(1-\boldsymbol h)$；tanh：$1-\boldsymbol h\odot\boldsymbol h$；ReLU：$z>0$ 取 1，否则取 0（一个 0/1 的掩码）。

```python
dz = dh * h * (1 - h)     # sigmoid
dz = dh * (z > 0)         # ReLU
```

**例 12**　tanh 层，前向输出 $\boldsymbol h=(0.5,-0.8)$，上游梯度 $\bar{\boldsymbol h}=(2,-1)$，求 $\bar{\boldsymbol z}$。

例 11 的雅可比矩阵是整块的 $W$，这里是逐元素的激活层，雅可比矩阵是对角的。

$\tanh'=1-h^2$：$(1-0.25,\ 1-0.64)=(0.75,\ 0.36)$。对应相乘：

$$\bar{\boldsymbol z}=(2\times0.75,\ -1\times0.36)=(1.5,\ -0.36).$$

> ReLU 层，$\boldsymbol z=(-1,0.5,2)$，$\bar{\boldsymbol h}=(1,2,-1)$，求 $\bar{\boldsymbol z}$。
>
> 答案：掩码 $(0,1,1)$，$\bar{\boldsymbol z}=(0,2,-1)$。第一个分量的梯度被截断了。

#### softmax 也能对应相乘吗？

不能。softmax 把分数 $\boldsymbol z\in\mathbb R^K$ 变成 $p_i=e^{z_i}/S$，$S=\sum_ke^{z_k}$，$S$ 里含所有分数，每个输出都依赖所有输入，雅可比矩阵不是对角的，上面的公式不能套用。先求它，用商的求导法则：

$$\frac{\partial p_i}{\partial z_j}=\begin{cases}\dfrac{e^{z_i}}S-\dfrac{e^{2z_i}}{S^2}=p_i(1-p_i),&j=i,\\[2mm]-\dfrac{e^{z_i}e^{z_j}}{S^2}=-p_ip_j,&j\ne i,\end{cases}$$

即 $J=\operatorname{diag}(\boldsymbol p)-\boldsymbol p\boldsymbol p^{\mathsf T}$。代入 $\bar z_j=\sum_i\bar p_iJ_{ij}$，得

$$\bar z_j=p_j\big(\bar p_j-\boldsymbol p^{\mathsf T}\bar{\boldsymbol p}\big).$$

再配上交叉熵，结果会化简得很干净。标签是第 $c$ 类时 $L=-\ln p_c$，$\bar{\boldsymbol p}=-\boldsymbol e_c/p_c$（$\boldsymbol e_c$ 是第 $c$ 个分量为 1、其余为 0 的向量），$\boldsymbol p^{\mathsf T}\bar{\boldsymbol p}=-1$，所以 $\bar z_c=p_c(-1/p_c+1)=p_c-1$，$\bar z_j=p_j$（$j\ne c$），合起来就是 M.2.7 的 $\boldsymbol p-\boldsymbol y$。

老朋友④的打分 $(2,1,0)$，$\boldsymbol p=(0.6652,0.2447,0.0900)$，正确类是第一个时，$\bar{\boldsymbol z}=(-0.3348,\ 0.2447,\ 0.0900)$。

合上书，写出逐元素函数的反向式 $\bar{\boldsymbol z}=\bar{\boldsymbol h}\odot\varphi'(\boldsymbol z)$，并说明为什么不必造出对角矩阵。

线性层和逐元素的激活层都有了反向规则，下一节把它们接成一条完整的链。

### 11. 两层网络的全部梯度，怎样只用符号推出来？

老朋友②的反向要依次经过输出层、第 2 个线性层、激活层、第 1 个线性层，每一步正好是前面某一节的一条规则。先用符号把这条链写出来，再代入数值。两层网络：$\boldsymbol x\in\mathbb R^d$，

$$\boldsymbol z_1=W_1\boldsymbol x+\boldsymbol b_1\in\mathbb R^{H},\qquad \boldsymbol h=\varphi(\boldsymbol z_1),\qquad \boldsymbol z_2=W_2\boldsymbol h+\boldsymbol b_2\in\mathbb R^{K},$$

再接损失 $L(\boldsymbol z_2)$。隐藏层有 $H$ 个单元（$H$ 取 hidden 的首字母，避免和隐藏层输出 $\boldsymbol h$ 混淆），$W_1\in\mathbb R^{H\times d}$，$W_2\in\mathbb R^{K\times H}$。

从后往前，每一步套用前面的一条规则。起点是**输出层的误差信号** $\boldsymbol\delta_2=\partial L/\partial\boldsymbol z_2\in\mathbb R^K$，它只取决于损失和输出的形式，是唯一随任务变化的一块。几种常见情形：

- 输出过 sigmoid 配二元交叉熵（$K=1$）：$\delta_2=\hat y-y$（M.2.5）；
- 输出过 softmax 配交叉熵：$\boldsymbol\delta_2=\boldsymbol p-\boldsymbol y$（M.2.7）；
- 输出直接是分数，损失 $\tfrac12\lVert\boldsymbol z_2-\boldsymbol t\rVert^2$：$\boldsymbol\delta_2=\boldsymbol z_2-\boldsymbol t$。

有了 $\boldsymbol\delta_2$：

1. 第 2 个线性层（方法 8）：$\dfrac{\partial L}{\partial W_2}=\boldsymbol\delta_2\boldsymbol h^{\mathsf T}$（$K\times H$），$\dfrac{\partial L}{\partial\boldsymbol b_2}=\boldsymbol\delta_2$，$\bar{\boldsymbol h}=W_2^{\mathsf T}\boldsymbol\delta_2$（$H$ 维）。
2. 激活层（方法 9）：$\boldsymbol\delta_1=\bar{\boldsymbol h}\odot\varphi'(\boldsymbol z_1)=\big(W_2^{\mathsf T}\boldsymbol\delta_2\big)\odot\varphi'(\boldsymbol z_1)$。
3. 第 1 个线性层（方法 8）：$\dfrac{\partial L}{\partial W_1}=\boldsymbol\delta_1\boldsymbol x^{\mathsf T}$（$H\times d$），$\dfrac{\partial L}{\partial\boldsymbol b_1}=\boldsymbol\delta_1$。

每个梯度的形状都和对应参数一样，这是核对。也可以用形状看出为什么传回去的是 $W_2^{\mathsf T}\boldsymbol\delta_2$：$W_2$ 是 $K\times H$，$\boldsymbol\delta_2$ 有 $K$ 个分量，$W_2\boldsymbol\delta_2$ 的形状根本对不上，只有 $W_2^{\mathsf T}\boldsymbol\delta_2$ 才是 $H$ 维。

#### 推广到 $D$ 层

把上面三条写成带层号的形式。设有 $D$ 个线性层（$D$ 取 depth 的首字母，$L$ 留给损失），$\boldsymbol a_0=\boldsymbol x$，第 $l$ 层是 $\boldsymbol z_l=W_l\boldsymbol a_{l-1}+\boldsymbol b_l$；前 $D-1$ 层后面接激活 $\boldsymbol a_l=\varphi(\boldsymbol z_l)$，最后一层 $\boldsymbol z_D$ 直接送进损失（输出层的 sigmoid 或 softmax 已并入损失，$\boldsymbol\delta_D$ 就是上面三种情形之一）。对照两层的情形：上面的 $\boldsymbol z_1,\boldsymbol h$ 对应 $\boldsymbol z_l,\boldsymbol a_l$，$\varphi'$ 仍作用在同一层的 $\boldsymbol z_l$ 上，$W_2^{\mathsf T}\boldsymbol\delta_2$ 来自后一层，所以是 $W_{l+1}^{\mathsf T}\boldsymbol\delta_{l+1}$。误差信号逐层往回递推：

$$\boldsymbol\delta_l=\big(W_{l+1}^{\mathsf T}\boldsymbol\delta_{l+1}\big)\odot\varphi'(\boldsymbol z_l)\quad(l=D-1,\dots,1),$$

每一层的参数梯度是

$$\frac{\partial L}{\partial W_l}=\boldsymbol\delta_l\boldsymbol a_{l-1}^{\mathsf T},\qquad \frac{\partial L}{\partial\boldsymbol b_l}=\boldsymbol\delta_l\qquad(l=D,\dots,1).$$

**方法 10（误差信号的逐层递推）**

1. 前向，存下每层的 $\boldsymbol z_l$ 和 $\boldsymbol a_l$。
2. 求输出层的 $\boldsymbol\delta_D=\partial L/\partial\boldsymbol z_D$。
3. 对 $l=D,D-1,\dots,1$：先写 $\partial W_l=\boldsymbol\delta_l\boldsymbol a_{l-1}^{\mathsf T}$、$\partial\boldsymbol b_l=\boldsymbol\delta_l$；若 $l\ge2$，再用 $\boldsymbol\delta_{l-1}=(W_l^{\mathsf T}\boldsymbol\delta_l)\odot\varphi'(\boldsymbol z_{l-1})$ 把误差信号传到前一层。

**例 13**　老朋友②：求全部梯度。

例 11、例 12 各算了一层，这道题把它们接成一条链：老朋友②的前向第 4 节已经算过，现在从输出层一路算到 $W_1$。

前向的值：$\boldsymbol z_1=(-0.5,1.25)$，$\boldsymbol h=(0.3775,0.7773)$，$z_2=-0.3998$，$\hat y=0.4014$，$L=0.9129$。

输出层（sigmoid 配交叉熵，$y=1$）：

$$\delta_2=\hat y-y=-0.5986 .$$

第 2 个线性层，$W_2=\boldsymbol w_2^{\mathsf T}$ 是 $1\times2$：

$$\frac{\partial L}{\partial\boldsymbol w_2}=\delta_2\boldsymbol h=(-0.2260,\ -0.4653),\qquad \frac{\partial L}{\partial b_2}=-0.5986,\qquad \bar{\boldsymbol h}=\boldsymbol w_2\delta_2=(-0.5986,\ 0.5986).$$

激活层，$\sigma'(\boldsymbol z_1)=\boldsymbol h\odot(1-\boldsymbol h)=(0.2350,\ 0.1731)$：

$$\boldsymbol\delta_1=\bar{\boldsymbol h}\odot\sigma'(\boldsymbol z_1)=(-0.1407,\ 0.1036).$$

第 1 个线性层，$\boldsymbol x=(1,2)^{\mathsf T}$：

$$\frac{\partial L}{\partial W_1}=\boldsymbol\delta_1\boldsymbol x^{\mathsf T}=\begin{pmatrix}-0.1407&-0.2814\\0.1036&0.2073\end{pmatrix},\qquad \frac{\partial L}{\partial\boldsymbol b_1}=\boldsymbol\delta_1 .$$

九个参数的梯度全部算出，只做了一遍反向。符号也说得通：$\partial L/\partial W_1$ 的第一行都是负的，梯度下降会让这一行变大；只动这一行时，$z_{1,1}$ 和 $h_1$ 随之变大，而 $z_2=h_1-h_2$ 里 $h_1$ 的系数是 $+1$，所以 $\hat y$ 向标签 1 靠近（当前只有 0.40）。

![老朋友②的计算图：上方是前向的值，下方是反向的误差信号 $\delta$；每个箭头旁标出用到的局部规则](fig/M7-n5.pdf){width=95%}

> 老朋友②只把标签改成 $y=0$，其余不变，求 $\delta_2$、$\partial L/\partial\boldsymbol w_2$ 和 $\boldsymbol\delta_1$。
>
> 答案：前向不变，$\hat y=0.4014$，$\delta_2=\hat y-0=0.4014$；$\partial L/\partial\boldsymbol w_2=\delta_2\boldsymbol h=(0.1515,\ 0.3120)$；$\bar{\boldsymbol h}=\boldsymbol w_2\delta_2=(0.4014,\ -0.4014)$，$\boldsymbol\delta_1=\bar{\boldsymbol h}\odot(0.2350,\ 0.1731)=(0.0943,\ -0.0695)$。

**例 14**　不带数值的符号推导。两层网络，隐藏层用 tanh，输出是线性的，损失 $L=\tfrac12\lVert\hat{\boldsymbol y}-\boldsymbol t\rVert^2$，$\hat{\boldsymbol y}=\boldsymbol z_2$。用 $\boldsymbol x,\boldsymbol h,W_1,W_2$ 写出全部梯度，并标出形状。

和例 13 的区别只有两处：输出层的 $\boldsymbol\delta_2$ 变成 $\hat{\boldsymbol y}-\boldsymbol t$，激活换成 tanh，导数 $\varphi'(\boldsymbol z_1)=1-\boldsymbol h\odot\boldsymbol h$。其余步骤不变：

$$\boldsymbol\delta_2=\hat{\boldsymbol y}-\boldsymbol t\ (K),\qquad \frac{\partial L}{\partial W_2}=(\hat{\boldsymbol y}-\boldsymbol t)\boldsymbol h^{\mathsf T}\ (K\times H),\qquad \frac{\partial L}{\partial\boldsymbol b_2}=\hat{\boldsymbol y}-\boldsymbol t\ (K),$$

$$\boldsymbol\delta_1=\big(W_2^{\mathsf T}(\hat{\boldsymbol y}-\boldsymbol t)\big)\odot(1-\boldsymbol h\odot\boldsymbol h)\ (H),\qquad \frac{\partial L}{\partial W_1}=\boldsymbol\delta_1\boldsymbol x^{\mathsf T}\ (H\times d),\qquad \frac{\partial L}{\partial\boldsymbol b_1}=\boldsymbol\delta_1\ (H).$$

> 隐藏层 ReLU，输出 $K=3$ 类过 softmax 配交叉熵（标签 one-hot 向量 $\boldsymbol y$，预测 $\boldsymbol p$），写出 $\partial L/\partial W_1$。
>
> 答案：$\boldsymbol\delta_2=\boldsymbol p-\boldsymbol y$，$\boldsymbol\delta_1=\big(W_2^{\mathsf T}(\boldsymbol p-\boldsymbol y)\big)\odot\mathbf 1[\boldsymbol z_1>0]$（逐分量的 0–1 向量：该分量大于 0 取 1，否则取 0），$\partial L/\partial W_1=\boldsymbol\delta_1\boldsymbol x^{\mathsf T}$（$H\times d$）。

梯度推出来了，可是一个转置写反、一个求和漏掉，训练照样能跑，只是学得慢。有没有办法不靠推导，直接检验梯度对不对？

合上书，不看公式，写出两层网络反向传播的五个式子，并给每个量标上形状。

### 12. 推出来的梯度对不对，怎样检验？

例 13 算出了 $\partial L/\partial W_{1,11}=-0.1407$，怎么知道它没有算错？手推的梯度很容易错一个转置或漏一个求和，而且错了以后训练也能跑，只是学得很慢，不报错。检验的办法是用定义算一遍：导数是差商的极限，所以取一个很小的 $\varepsilon$，用两次前向计算近似它。

最直接的是**前向差分** $\dfrac{f(\theta+\varepsilon)-f(\theta)}{\varepsilon}$。把 $f(\theta+\varepsilon)$ 做泰勒展开（C.7.3）：

$$\frac{f(\theta+\varepsilon)-f(\theta)}{\varepsilon}=f'(\theta)+\frac{f''(\theta)}{2}\varepsilon+\cdots,$$

误差与 $\varepsilon$ 同阶。更好的是**中心差分**：对称地取两边。两个展开式

$$f(\theta\pm\varepsilon)=f(\theta)\pm f'(\theta)\varepsilon+\frac{f''(\theta)}{2}\varepsilon^2\pm\frac{f'''(\theta)}{6}\varepsilon^3+\cdots$$

相减，$f$ 和 $\varepsilon^2$ 项抵消：

$$\frac{f(\theta+\varepsilon)-f(\theta-\varepsilon)}{2\varepsilon}=f'(\theta)+\frac{f'''(\theta)}{6}\varepsilon^2+\cdots,$$

误差是 $\varepsilon^2$ 阶，比前向差分高一阶。

**方法 11（数值梯度检验）**

1. 挑一个参数 $\theta_k$，其余固定，算 $L(\theta_k+\varepsilon)$ 与 $L(\theta_k-\varepsilon)$，$\varepsilon$ 取 $10^{-5}$ 左右。
2. 数值梯度 $g_{\text{num}}=\dfrac{L(\theta_k+\varepsilon)-L(\theta_k-\varepsilon)}{2\varepsilon}$。
3. 和反向传播的结果 $g$ 比较，看相对误差 $\dfrac{|g-g_{\text{num}}|}{\max(|g|,|g_{\text{num}}|)}$，双精度下应小于 $10^{-6}$ 左右。

$\varepsilon$ 不能取得太小：太小时两个 $L$ 几乎相等，相减会损失有效数字（舍入误差约 $10^{-16}/\varepsilon$）。$10^{-5}$ 时截断误差约 $10^{-10}$，舍入误差约 $10^{-11}$，两者都很小。

**例 15**　$f(x)=e^x$ 在 $x=0$ 处，$\varepsilon=0.1$，比较两种差分。真值 $f'(0)=1$。

先不碰网络，在真值能心算出来的 $e^x$ 上比较两种差分哪个更准。

前向差分 $(e^{0.1}-1)/0.1=1.0517$，误差 0.0517；中心差分 $(e^{0.1}-e^{-0.1})/0.2=1.0017$，误差 0.0017，小了约 30 倍。

> 用中心差分、$\varepsilon=0.1$ 近似 $\sigma'(0)$。
>
> 答案：$(\sigma(0.1)-\sigma(-0.1))/0.2=(0.52498-0.47502)/0.2=0.2498$，真值 0.25。

**例 16**　检验例 13 中 $\partial L/\partial W_{1,11}=-0.1407$（$W_1$ 的第 1 行第 1 列）。

这次函数换成整个网络，要核对的是例 13 反向传播的结果，检验的是第 11 节的整条推导。

取 $\varepsilon=10^{-5}$，把 $W_{1,11}$ 从 0.5 改成 $0.5\pm10^{-5}$，其余不动，各做一遍前向，得 $L(\theta+\varepsilon)=0.91286968$，$L(\theta-\varepsilon)=0.91287250$，代入公式：

$$g_{\text{num}}=\frac{L(\theta+\varepsilon)-L(\theta-\varepsilon)}{2\times10^{-5}}=-0.1406802,$$

与反向传播的 $-0.1407$ 一致（多保留几位，两者都是 $-0.1406802$），说明从输出层一路传到 $W_1$ 的整条链没有错。

数值梯度每检验一个参数就要多两遍前向（第 7 节的前向模式每个参数一遍，数值差分要两遍，所以更贵），对上亿参数的模型不可能全查，只用来在小网络上调试，抽查几个参数。

![误差随 $\varepsilon$ 的变化（双对数坐标）：前向差分（虚线）的误差与 $\varepsilon$ 成正比，中心差分（实线）与 $\varepsilon^2$ 成正比；$\varepsilon$ 太小时舍入误差上升](fig/M7-n6.pdf){width=70%}

回到开头的问题：按 M.1 的办法，每个参数把损失算两遍再相减，老朋友②的 9 个参数要 18 遍前向。反向传播只要一遍前向加一遍反向，反向约是前向的两倍（第 9 节），合计约 3 遍前向的代价，而且不随参数个数增加。参数有 $10^9$ 个时，前者是 $2\times10^9$ 遍，后者仍是约 3 遍，这就是 `loss.backward()` 能在前向几倍的时间里给出全部偏导的原因。

合上书，写出反向传播的两条规则（上游梯度乘局部导数、分叉处相加），并说明为什么从后往前走只需一遍。

### 本章小结

| 方法 | 什么时候用 | 对应题号 |
|---|---|---|
| 方法 1（隐藏层与前向计算） | 判断数据能否一层分开；算 MLP 的输出 | M7-01、M7-15 |
| 方法 2（激活函数的导数） | 求 $\varphi'(z)$；判断饱和与截断 | M7-02、M7-08 |
| 方法 3（数形状与参数） | 写出每层形状，数参数 | M7-03、M7-14 |
| 方法 4（画计算图并前向） | 把公式拆成基本运算，记下中间值 | M7-05、M7-13 |
| 方法 5（沿计算图反向传播） | 标量图上求每个节点的梯度 | M7-05、M7-13 |
| 方法 6（分叉处梯度相加） | 一个量被多处用到；参数共用 | M7-05 |
| 方法 7（向量的反向与形状核对） | 向量值函数；用形状检查结果 | M7-06、M7-09 |
| 方法 8（线性层的反向） | $\partial W=\boldsymbol\delta\boldsymbol x^{\mathsf T}$，$\partial\boldsymbol x=W^{\mathsf T}\boldsymbol\delta$，含批量 | M7-07、M7-08、M7-14 |
| 方法 9（逐元素函数的反向） | 激活层：对应相乘 | M7-04、M7-08、M7-09、M7-10、M7-11 |
| 方法 10（误差信号的逐层递推） | 两层、多层网络的符号推导和手算 | M7-10、M7-11、M7-12、M7-14 |
| 方法 11（数值梯度检验） | 检查手推的梯度是否正确 | M7-12 |

在全书的主线上，本章把第三件「更新规则」里的 $\nabla L$ 补全了：模型 $f_\theta$ 现在可以是任意深的网络，损失仍是 M.2 的交叉熵或平方误差，梯度由反向传播一遍求出，再交给 M.1 的梯度下降走一步。M.8 会把「前向—反向—更新」连成一次完整的训练，并讨论层数一深以后梯度怎样消失或爆炸。

逐章长大的「损失 ⇐ 概率假设」表，本章没有新增行：输出层的 $\boldsymbol\delta=\hat y-y$ 或 $\boldsymbol p-\boldsymbol y$ 就是 M.2 的两行损失（二元交叉熵、softmax 交叉熵）经过反向传播的结果。

| 损失或做法 | 背后的概率假设 | 出现章 |
|---|---|---|
| 均方误差 | 噪声是高斯分布 | M.2（本章例 4、例 14 用到） |
| 交叉熵（二分类、多分类） | 标签服从伯努利 / 类别分布 | M.2（本章例 5、例 13 用到） |
| L2、L1 正则 | 高斯先验、拉普拉斯先验 | M.3 |
| 本章新增 | 无新增行 | M.7 |
