## L.5 · 逆矩阵

国家统计局定期编制全国的投入产出表，记下每个部门生产 1 元产品要消耗其他各部门多少元的产品。拿着这张表可以回答一个很实际的问题：如果居民和出口对汽车的需求增加 1 亿元，钢铁、电力、化工等部门总共要多生产多少？难处在于连锁反应：造汽车要钢，炼钢要电，发电又要钢。

20 世纪 30 年代，列昂惕夫用美国的经济统计编制投入产出表，把这个问题写成线性方程组：已知各部门的最终需求，反求各部门的总产出。这正是把一个线性变换倒过来，从结果找原因。他因发展投入产出方法及其经济应用，获得 1973 年的诺贝尔经济学奖。

L.3 里有的变换能倒过来：老朋友③把平面逆时针转了 90°，顺时针转回去就行。有的不能：老朋友④把平面压到直线 $y=x$ 上，不同的点被压到同一处，从结果分不出原来是哪个。本章回答三个问题：怎样描述「倒过来」，怎样判断能不能倒过来，怎样把倒过来的矩阵算出来。

第 1 节定义逆矩阵和它的运算律；第 2 节给出可逆的充要条件；第 3 节用消元求逆；第 4 节解以矩阵为未知量的方程；第 5 节回到投入产出模型。

### 1. 怎样撤销一个变换？

先拿老朋友试。③ $=\begin{pmatrix}0&-1\\1&0\end{pmatrix}$ 逆时针转 90°，撤销它就是顺时针转 90°，矩阵是 $\begin{pmatrix}0&1\\-1&0\end{pmatrix}$（它把 $\boldsymbol{e}_1$ 送到 $(0,-1)^{\mathsf T}$，$\boldsymbol{e}_2$ 送到 $(1,0)^{\mathsf T}$）。先转过去再转回来，或者先转回来再转过去，都回到原样。按行乘列验证，两个次序的乘积都是 $E$。顺便留意，撤销③的矩阵恰好是把③的行和列对调，也就是③的转置；只转动、不变形的变换都有这个性质，L.10 讲正交矩阵时再回来。

②剪切 $\begin{pmatrix}1&1\\0&1\end{pmatrix}$ 把高度为 $y$ 的水平线向右推 $y$，撤销它就是向左推 $y$，矩阵是 $\begin{pmatrix}1&-1\\0&1\end{pmatrix}$。L.4.4 已经算过，两者相乘得 $E$。

再看①$=\begin{pmatrix}2&1\\1&2\end{pmatrix}$（L.3 的对称伸缩）：它把 $\boldsymbol{e}_1$、$\boldsymbol{e}_2$ 送到 $(2,1)^{\mathsf T}$、$(1,2)^{\mathsf T}$，单位正方形被拉成以这两个向量为邻边的平行四边形。撤销它，就是把这个平行四边形原样拉回正方形，见下图；撤销①的矩阵在例 1 算出。

![①把单位正方形（虚线）变成斜放的平行四边形（实线，阴影）；①的逆把它原样变回单位正方形。两个方向的箭头分别标 ① 和 $\text{①}^{-1}$](fig/L5-n2.pdf){width=80%}

把「撤销」写成定义。设 $A$ 是 $n$ 阶方阵，如果有 $n$ 阶方阵 $B$ 使

$$AB=BA=E,$$

这里的 $E$ 是 $n$ 阶单位矩阵 $E_n$，阶数不言自明时省去下标。这时称 $A$ **可逆**，$B$ 叫 $A$ 的**逆矩阵**，记作 $A^{-1}$，读作「$A$ 逆」。不可逆的方阵也叫**奇异矩阵**，可逆的叫非奇异矩阵。定义里要求两个次序都得 $E$：先做 $A$ 再做 $B$ 回到原样，先做 $B$ 再做 $A$ 也回到原样。

#### 为什么只对方阵谈逆

你也许会问：$2\times3$ 的矩阵 $A$ 能不能找到 $3\times2$ 的 $B$，让 $AB$ 和 $BA$ 都是单位矩阵？先把阶数理清：

- $A$ 是 2 行 3 列，把 3 维向量送进 2 维；
- $B$ 是 3 行 2 列，把 2 维向量送回 3 维；
- $AB$ 是 $2\times2$，要和 $E_2$ 比；$BA$ 是 $3\times3$，要和 $E_3$ 比。

答案是不能同时做到，理由用 L.4.3 就够。$A\boldsymbol{x}=\boldsymbol{0}$ 是 2 个方程、3 个未知数的齐次方程组，未知数多于方程，一定有非零解 $\boldsymbol{x}_0$。于是

$$(BA)\boldsymbol{x}_0=B(A\boldsymbol{x}_0)=B\boldsymbol{0}=\boldsymbol{0}\ne\boldsymbol{x}_0,$$

所以 $BA$ 不可能是 $E_3$。从变换看，三维空间进了二维，一定有一个方向被压到原点，这个方向再也找不回来。$AB=E_2$ 倒是可能的，例如

$$A=\begin{pmatrix}1&0&0\\0&1&0\end{pmatrix},\quad B=\begin{pmatrix}1&0\\0&1\\0&0\end{pmatrix},\quad AB=E_2,\quad BA=\begin{pmatrix}1&0&0\\0&1&0\\0&0&0\end{pmatrix}\ne E_3 .$$

$A$ 扔掉了第三个坐标，$B$ 补不回来。

反过来，$A$ 是 $3\times2$、$B$ 是 $2\times3$ 时，轮到 $B\boldsymbol{x}=\boldsymbol{0}$ 有非零解，同样的推理说明 $AB$ 不可能是 $E_3$。所以非方阵的两个乘积总有一个不是单位矩阵，逆矩阵只对方阵定义。

#### 逆矩阵只有一个，它能「约分」

逆矩阵如果存在，只有一个。设 $B$、$C$ 都是 $A$ 的逆矩阵，利用结合律在中间插入 $E=AC$：

$$B=BE=B(AC)=(BA)C=EC=C .$$

有了逆矩阵，L.3 里失效的「约分」对可逆矩阵恢复了：从 $AB=AC$ 两边左乘 $A^{-1}$，得 $B=C$。方程组 $A\boldsymbol{x}=\boldsymbol{b}$ 两边左乘 $A^{-1}$，得唯一解

$$\boldsymbol{x}=A^{-1}\boldsymbol{b};$$

反过来它确实是解，因为 $A(A^{-1}\boldsymbol{b})=\boldsymbol{b}$。用变换的话说：要找哪个点被送到 $\boldsymbol{b}$，就把 $\boldsymbol{b}$ 用撤销变换送回去。

#### 二阶矩阵的逆

设 $A=\begin{pmatrix}a&b\\c&d\end{pmatrix}$，先设 $ad-bc\ne0$。如果逆存在，由 $AA^{-1}=E$ 按列看，$A$ 乘 $A^{-1}$ 的第 1 列得 $E$ 的第 1 列 $\boldsymbol{e}_1$。所以 $A^{-1}$ 的第 1 列是被 $A$ 送到 $\boldsymbol{e}_1$ 的那个向量，即方程组 $ax_1+bx_2=1$、$cx_1+dx_2=0$ 的解。

用加减消元解。第一式乘 $d$ 减去第二式乘 $b$，$x_2$ 消掉：

$$d(ax_1+bx_2)-b(cx_1+dx_2)=(ad-bc)x_1,\qquad d\cdot1-b\cdot0=d,$$

所以 $(ad-bc)x_1=d$。同样，第一式乘 $c$ 减去第二式乘 $a$，$x_1$ 消掉，得 $(bc-ad)x_2=c$。所以

$$x_1=\frac{d}{ad-bc},\qquad x_2=\frac{-c}{ad-bc}.$$

同样，第 2 列是 $A\boldsymbol{x}=\boldsymbol{e}_2$ 的解 $\frac{1}{ad-bc}(-b,a)^{\mathsf T}$。下面的公式就是这样来的。

把两个主对角元对调、两个副对角元变号，记作 $A^*=\begin{pmatrix}d&-b\\-c&a\end{pmatrix}$，叫作 $A$ 的**伴随矩阵**。三阶以上也有伴随矩阵，L.6.8 用行列式定义它，记号不变；本章只在二阶用。按行乘列，

$$AA^*=\begin{pmatrix}ad-bc&0\\0&ad-bc\end{pmatrix}=(ad-bc)E,$$

换个次序相乘也得 $(ad-bc)E$。所以 $ad-bc\ne0$ 时两边除以它：

$$A^{-1}=\frac{1}{ad-bc}\begin{pmatrix}d&-b\\-c&a\end{pmatrix}.$$

再看 $ad-bc=0$ 的情形，这时 $A$ 不可逆。由 L.1.3，这时两列共线，$A$ 把整个平面压到一条直线上（或原点）。④就是这样：$\frac12\cdot\frac12-\frac12\cdot\frac12=0$。

用式子说明：这时 $AA^*=O$；假如 $A$ 可逆，左乘 $A^{-1}$ 得 $A^*=O$，于是 $a=b=c=d=0$，$A=O$，可 $O$ 乘任何矩阵都是 $O$，得不到 $E$，矛盾。

**方法 1（二阶公式）**

1. 先算 $ad-bc$。为 0 则不可逆，停。
2. 不为 0，就把主对角元对调、副对角元变号。
3. 再除以 $ad-bc$。
4. 用 $AA^{-1}=E$ 检验。

**例 1**　求①$=\begin{pmatrix}2&1\\1&2\end{pmatrix}$ 的逆矩阵，并解方程组 $2x+y=3$，$x+2y=0$。

第一步，$ad-bc=4-1=3\ne0$，可逆。

第二步，对调、变号、除以 3：

$$\text{①}^{-1}=\frac13\begin{pmatrix}2&-1\\-1&2\end{pmatrix}.$$

检验：$\begin{pmatrix}2&1\\1&2\end{pmatrix}\begin{pmatrix}2&-1\\-1&2\end{pmatrix}=\begin{pmatrix}3&0\\0&3\end{pmatrix}$，再乘 $\frac13$ 得 $E$。

第三步，方程组就是①$\boldsymbol{x}=(3,0)^{\mathsf T}$，所以

$$\boldsymbol{x}=\frac13\begin{pmatrix}2&-1\\-1&2\end{pmatrix}\begin{pmatrix}3\\0\end{pmatrix}=\begin{pmatrix}2\\-1\end{pmatrix}.$$

代回：$4-1=3$，$2-2=0$。

这道题的新东西在第三步：解方程组不再消元，而是把 $\boldsymbol{b}$ 用撤销变换送回去。同一个①配不同的 $\boldsymbol{b}$，逆只要求一次，每个 $\boldsymbol{b}$ 乘一下就得到解。

> 求 $\begin{pmatrix}2&1\\5&3\end{pmatrix}$ 的逆矩阵。
>
> 答案：$ad-bc=6-5=1$，逆矩阵是 $\begin{pmatrix}3&-1\\-5&2\end{pmatrix}$。检验第一行：$(2,1)$ 乘两列得 $6-5=1$、$-2+2=0$。

#### 运算律

逆矩阵的运算律都用同一个办法证：猜出逆矩阵，验证它和原矩阵相乘得 $E$，再由唯一性下结论。最常用、也最容易记错的是乘积的逆：

$$(AB)^{-1}=B^{-1}A^{-1}.$$

验证时用结合律重新加括号：

$$(AB)(B^{-1}A^{-1})=A(BB^{-1})A^{-1}=AA^{-1}=E,$$

另一个次序 $(B^{-1}A^{-1})(AB)=B^{-1}(A^{-1}A)B=E$ 同样算出。

次序为什么要反过来？早上先穿袜子再穿鞋，晚上要先脱鞋再脱袜子。$AB$ 是先做 $B$ 再做 $A$，撤销时要先撤销最后做的 $A$，所以 $A^{-1}$ 写在右边、先作用。

![先转（③）再剪切（②），撤销时先撤销剪切、再转回来：上排箭头是 $\text{②}\,\text{③}$，下排箭头依次是 $\text{②}^{-1}$、$\text{③}^{-1}$](fig/L5-n4.pdf){width=85%}

这个说法也提醒另一件事：$(A+B)^{-1}$ 和 $A^{-1}+B^{-1}$ 没有关系。例如 $A=B=E$ 时，前者是 $\frac12E$，后者是 $2E$。

其余几条，每条一句理由，用到时再回来查：

- $(A^{-1})^{-1}=A$：把 $AA^{-1}=A^{-1}A=E$ 倒过来读，$A$ 正是 $A^{-1}$ 的逆。
- $(kA)^{-1}=\frac1kA^{-1}$（$k\ne0$）：$(kA)(\frac1kA^{-1})=AA^{-1}=E$。
- $(A^{\mathsf T})^{-1}=(A^{-1})^{\mathsf T}$：由 L.3.6 的 $(AB)^{\mathsf T}=B^{\mathsf T}A^{\mathsf T}$，$A^{\mathsf T}(A^{-1})^{\mathsf T}=(A^{-1}A)^{\mathsf T}=E^{\mathsf T}=E$，另一侧 $(A^{-1})^{\mathsf T}A^{\mathsf T}=(AA^{-1})^{\mathsf T}=E$。
- 初等矩阵的逆是同类的初等矩阵：$E(i,j)^{-1}=E(i,j)$，$E(i(k))^{-1}=E(i(\frac1k))$，$E(i,j(k))^{-1}=E(i,j(-k))$，L.4.4 已经验算过。

**例 2**　设②$=\begin{pmatrix}1&1\\0&1\end{pmatrix}$，$B=\begin{pmatrix}1&0\\2&1\end{pmatrix}$。用运算律求 $(\text{②}B)^{-1}$，并与 $\text{②}^{-1}B^{-1}$ 比较。

和例 1 不同，这里不先乘出 $\text{②}B$，而是用 $(\text{②}B)^{-1}=B^{-1}\text{②}^{-1}$。由二阶公式，$\text{②}^{-1}=\begin{pmatrix}1&-1\\0&1\end{pmatrix}$，$B^{-1}=\begin{pmatrix}1&0\\-2&1\end{pmatrix}$，

$$(\text{②}B)^{-1}=B^{-1}\text{②}^{-1}=\begin{pmatrix}1&-1\\-2&3\end{pmatrix},\qquad \text{②}^{-1}B^{-1}=\begin{pmatrix}3&-1\\-2&1\end{pmatrix}.$$

两者不同。核对：$\text{②}B=\begin{pmatrix}3&1\\2&1\end{pmatrix}$，$ad-bc=1$，按二阶公式它的逆正是 $\begin{pmatrix}1&-1\\-2&3\end{pmatrix}$。

这一节定义了「撤销」并会算二阶的逆，但还留着一个问题：一个三阶、四阶的矩阵，怎么知道它能不能撤销？下一节回答。

合上书，证明逆矩阵唯一，再用「穿袜子、穿鞋」说明 $(AB)^{-1}$ 的次序。

### 2. 什么样的变换撤销不了？

$2\times2$ 矩阵看 $ad-bc$ 就知道能不能撤销。$n$ 阶方阵呢？L.6 会给出一个类似 $ad-bc$ 的数，这里先用已有的工具：消元和数主元。

先看④为什么撤销不了。它把 $(1,0)^{\mathsf T}$ 和 $(0,1)^{\mathsf T}$ 都送到 $(\frac12,\frac12)^{\mathsf T}$；把非零向量 $(-1,1)^{\mathsf T}$ 送到 $\boldsymbol{0}$，而 $\boldsymbol{0}$ 也被送到 $\boldsymbol{0}$。两个不同的点撞到了一起，任何「撤销」都没法把同一个点同时送回两个地方。

![④把平面垂直地压到直线 $y=x$ 上：实心点 $(1,0)$ 和空心点 $(0,1)$ 沿虚线落到同一点 $(\frac12,\frac12)$；方向 $(-1,1)$ 整条被压到原点。撞在一起的点分不开，所以撤销不了](fig/L5-n3.pdf){width=60%}

所以可逆的变换不能把非零向量压成 $\boldsymbol{0}$，也就是 $A\boldsymbol{x}=\boldsymbol{0}$ 只能有零解。反过来，只要 $A\boldsymbol{x}=\boldsymbol{0}$ 只有零解，L.4.3 告诉我们 $A$ 有 $n$ 个主元，能消成 $E$，而消元的每一步都能用初等矩阵撤销。每一步能撤销，整串是否也能撤销？下面证明的第 3 步把 $A$ 写成这些撤销矩阵的乘积，第 4 步再说明这样的乘积可逆。串起来就是下面的定理。

#### 可逆的四个等价条件

**可逆的充要条件**　对 $n$ 阶方阵 $A$，下面四条互相等价：

(a) $A$ 可逆；
(b) $A\boldsymbol{x}=\boldsymbol{0}$ 只有零解；
(c) $A$ 有 $n$ 个主元，即行最简形是 $E$；
(d) $A$ 是若干个初等矩阵的乘积。

证明按 (a)→(b)→(c)→(d)→(a) 转一圈，这是考试会要求写的骨架：

1. (a)→(b)：若 $A\boldsymbol{x}=\boldsymbol{0}$，两边左乘 $A^{-1}$，得 $\boldsymbol{x}=A^{-1}\boldsymbol{0}=\boldsymbol{0}$。
2. (b)→(c)：若主元少于 $n$ 个，就有自由未知量，$A\boldsymbol{x}=\boldsymbol{0}$ 有非零解（L.4.3），与 (b) 矛盾。所以有 $n$ 个主元；它们落在 $n$ 行 $n$ 列里，每行每列各一个，只能排在对角线上，化成行最简形就是 $E$（L.4.2）。
3. (c)→(d)：消元写成 $E_s\cdots E_2E_1A=E$。两边从左边依次乘 $E_s^{-1},\dots,E_1^{-1}$，得 $A=E_1^{-1}E_2^{-1}\cdots E_s^{-1}$，每个因子都是初等矩阵。
4. (d)→(a)：每个初等矩阵可逆，由 $(AB)^{-1}=B^{-1}A^{-1}$，可逆矩阵的乘积仍可逆。

第 3 步在 $2\times2$ 上走一遍就不抽象了。L.4.4 的例子里 $E(2,1(-3))\begin{pmatrix}1&2\\3&4\end{pmatrix}=\begin{pmatrix}1&2\\0&-2\end{pmatrix}$；再做 $-\frac12r_2$、$r_1-2r_2$ 就到 $E$。三步依次是 $E(2,1(-3))$、$E(2(-\frac12))$、$E(1,2(-2))$，所以

$$E(1,2(-2))\,E\big(2(-\tfrac12)\big)\,E(2,1(-3))\begin{pmatrix}1&2\\3&4\end{pmatrix}=E.$$

从左边依次乘各个因子的逆，就得到

$$\begin{pmatrix}1&2\\3&4\end{pmatrix}=E(2,1(3))\,E(2(-2))\,E(1,2(2)),$$

右边按行乘列乘出来，确实是原矩阵。注意右边各因子的次序和消元的次序正好相反，这又是「穿袜子、穿鞋」。

#### 可逆与不可逆的对照

把可逆和不可逆并排放，先自己找找每一行的区别：

| | 可逆（如⑥、③） | 不可逆（如⑤、④） |
|---|---|---|
| $A\boldsymbol{x}=\boldsymbol{0}$ | 只有零解 | 有非零解，如④$(-1,1)^{\mathsf T}=\boldsymbol{0}$ |
| 主元个数 | $n$ | 少于 $n$ |
| $A\boldsymbol{x}=\boldsymbol{b}$ | 对每个 $\boldsymbol{b}$ 恰有一个解 | 有的 $\boldsymbol{b}$ 无解，有解时有无穷多个 |
| 几何上 | 不同的点去不同的地方，能还原 | 压扁了，不同的点撞在一起 |

背后只有一件事：变换有没有丢信息。⑤就是不可逆的一侧：L.4 对它消元只得到两个主元，$(-2,1,0)^{\mathsf T}$ 被它压到原点。丢了多少，L.7 用秩来量。

#### 方阵只要验证一边

定理给出一个很实用的推论：设 $A,B$ 是 $n$ 阶方阵，$AB=E$，那么 $BA=E$，从而 $B=A^{-1}$。理由分两步。

第一步，$B$ 可逆。若 $B\boldsymbol{x}=\boldsymbol{0}$，把 $E$ 换成 $AB$，再按结合律重新加括号：$\boldsymbol{x}=E\boldsymbol{x}=(AB)\boldsymbol{x}=A(B\boldsymbol{x})=A\boldsymbol{0}=\boldsymbol{0}$。这里没有用到 $A$ 可逆。所以 $B$ 满足 (b)，由定理 $B$ 可逆。

第二步，在 $AB=E$ 两边右乘 $B^{-1}$，得 $A=B^{-1}$，于是 $BA=BB^{-1}=E$。

以后验证逆矩阵，乘一边得 $E$ 就够了。注意「方阵」不能少：上一节的 $2\times3$ 例子里 $AB=E_2$，$BA$ 却不是 $E_3$。

**方法 2（判断可逆）**

1. 对 $A$ 消元，数主元。
2. 有 $n$ 个就可逆；少于 $n$ 个就不可逆，并从行最简形写出 $A\boldsymbol{x}=\boldsymbol{0}$ 的一个非零解作为证据。
3. 抽象条件下，设法凑出 $AB=E$（只验一边），或者找出 $A\boldsymbol{x}=\boldsymbol{0}$ 的非零解。

**例 3**　判断 $A=\begin{pmatrix}1&2&1\\2&3&1\\1&1&0\end{pmatrix}$ 是否可逆；不可逆时找一个非零的 $\boldsymbol{x}$ 使 $A\boldsymbol{x}=\boldsymbol{0}$。

第一步，消元：

$$\begin{pmatrix}1&2&1\\2&3&1\\1&1&0\end{pmatrix}\xrightarrow[r_3-r_1]{r_2-2r_1}\begin{pmatrix}1&2&1\\0&-1&-1\\0&-1&-1\end{pmatrix}\xrightarrow{r_3-r_2}\begin{pmatrix}1&2&1\\0&-1&-1\\0&0&0\end{pmatrix}.$$

只有两个主元，$A$ 不可逆。

第二步，找证据。剩下的方程是 $x_1+2x_2+x_3=0$、$-x_2-x_3=0$。取自由未知量 $x_3=1$，得 $x_2=-1$，$x_1=1$。检验：

$$A\begin{pmatrix}1\\-1\\1\end{pmatrix}=\begin{pmatrix}1-2+1\\2-3+1\\1-1+0\end{pmatrix}=\boldsymbol{0},$$

即第一列减第二列加第三列等于 $\boldsymbol{0}$，方向 $(1,-1,1)^{\mathsf T}$ 被压到了原点。

> 判断 $\begin{pmatrix}1&0&2\\0&1&1\\1&1&2\end{pmatrix}$ 是否可逆。
>
> 答案：$r_3-r_1$ 得 $(0,1,0)$，$r_3-r_2$ 得 $(0,0,-1)$，三个主元，可逆。

**例 4**　设 $n$ 阶方阵 $A$ 满足 $A^k=O$（$k$ 是某个正整数）。证明 $E-A$ 可逆，且 $(E-A)^{-1}=E+A+A^2+\cdots+A^{k-1}$；并对 $A=\begin{pmatrix}0&1&2\\0&0&3\\0&0&0\end{pmatrix}$ 求 $(E-A)^{-1}$。

和例 3 不同，这里没有具体的数，不能消元，只能凑「乘起来得 $E$」。为什么猜这个式子？数的情形有恒等式

$$(1-a)(1+a+\cdots+a^{k-1})=1-a^k,$$

$a^k=0$ 时右边恰好是 1。矩阵照搬，验证一边就够：

$$(E-A)(E+A+\cdots+A^{k-1})=(E+A+\cdots+A^{k-1})-(A+A^2+\cdots+A^k)=E-A^k=E .$$

中间一步按分配律展开，两串相同的项相互抵消，只剩首项 $E$ 和末项 $A^k$。这一步能照搬数的恒等式，依据的是什么？依据 $E$ 和 $A$ 的各次幂相乘可以交换次序（L.3.5）。

对给定的 $A$，$A^2=\begin{pmatrix}0&0&3\\0&0&0\\0&0&0\end{pmatrix}$，$A^3=O$，所以

$$(E-A)^{-1}=E+A+A^2=\begin{pmatrix}1&1&5\\0&1&3\\0&0&1\end{pmatrix}.$$

第 5 节的投入产出模型会再遇到这个和。

会判断了，下一步是把逆矩阵算出来。证明里的第 3 步其实已经藏着算法。

合上书，按 (a)→(b)→(c)→(d)→(a) 写出可逆充要条件的四步证明，再说明为什么方阵 $AB=E$ 就推出 $BA=E$。

### 3. 逆矩阵怎样算出来？

第 2 节证明的第 3 步其实已经给出了算法。消元得到 $E_s\cdots E_2E_1A=E$，两边右乘 $A^{-1}$，得

$$E_s\cdots E_2E_1=A^{-1}.$$

也就是说，把 $A$ 化成 $E$ 的那一串行变换，如果作用在 $E$ 上，得到的正是 $A^{-1}$。所以不必记下每个初等矩阵，只要让 $A$ 和 $E$ 并排，接受同样的行变换。用 L.3.7 的分块乘法看，记 $P=E_s\cdots E_1$，

$$P(A\mid E)=(PA\mid PE)=(E\mid A^{-1}).$$

左半边变成 $E$ 的同时，右半边就成了 $A^{-1}$。如果消元途中左半边出现全 0 的行，$A$ 的主元少于 $n$ 个，由第 2 节它不可逆，停下即可。

**方法 3（初等行变换求逆）**

1. 写出 $n\times2n$ 矩阵 $(A\mid E)$。
2. 只用行变换，先把左半边化成行阶梯形；出现零行就不可逆，停。
3. 再从下往上把左半边化成 $E$，右半边就是 $A^{-1}$。
4. 验证 $AA^{-1}=E$，只需一边。

全程只用行变换，不能混入列变换：列变换要右乘，等式 $P(A\mid E)=(PA\mid PE)$ 就不成立了。

只想解一个方程组 $A\boldsymbol{x}=\boldsymbol{b}$ 时，不必先求逆再乘 $\boldsymbol{b}$，直接对 $(A\mid\boldsymbol{b})$ 消元更省事。计算软件也是这样做的：几乎从不显式求逆，而是消元解方程。逆矩阵更多用在推理里，比如下一节的矩阵方程。

**例 5**　求⑥$=\begin{pmatrix}2&1&0\\1&2&1\\0&1&2\end{pmatrix}$ 的逆矩阵。

第一步，化左半边为行阶梯形。为了让主元是 1，先交换第 1、2 行，消第 1 列；再交换第 2、3 行，用 1 去消 $-3$：

$$\left(\begin{array}{rrr|rrr}2&1&0&1&0&0\\1&2&1&0&1&0\\0&1&2&0&0&1\end{array}\right)\xrightarrow{r_1\leftrightarrow r_2}\left(\begin{array}{rrr|rrr}1&2&1&0&1&0\\2&1&0&1&0&0\\0&1&2&0&0&1\end{array}\right)\xrightarrow{r_2-2r_1}\left(\begin{array}{rrr|rrr}1&2&1&0&1&0\\0&-3&-2&1&-2&0\\0&1&2&0&0&1\end{array}\right),$$

$$\xrightarrow{r_2\leftrightarrow r_3}\left(\begin{array}{rrr|rrr}1&2&1&0&1&0\\0&1&2&0&0&1\\0&-3&-2&1&-2&0\end{array}\right)\xrightarrow{r_3+3r_2}\left(\begin{array}{rrr|rrr}1&2&1&0&1&0\\0&1&2&0&0&1\\0&0&4&1&-2&3\end{array}\right).$$

左边三个主元，可逆，和 L.4 对⑥消元的结论一致。

第二步，从下往上化成 $E$。先 $\frac14r_3$，把第 3 个主元变成 1：

$$\xrightarrow{\frac14r_3}\left(\begin{array}{rrr|rrr}1&2&1&0&1&0\\0&1&2&0&0&1\\0&0&1&\frac14&-\frac12&\frac34\end{array}\right).$$

再用第 3 行消掉第 3 列上方的数（$r_2-2r_3$、$r_1-r_3$），得到下面左边的矩阵；最后 $r_1-2r_2$：

$$\left(\begin{array}{rrr|rrr}1&2&0&-\frac14&\frac32&-\frac34\\0&1&0&-\frac12&1&-\frac12\\0&0&1&\frac14&-\frac12&\frac34\end{array}\right)\xrightarrow{r_1-2r_2}\left(\begin{array}{rrr|rrr}1&0&0&\frac34&-\frac12&\frac14\\0&1&0&-\frac12&1&-\frac12\\0&0&1&\frac14&-\frac12&\frac34\end{array}\right).$$

所以

$$\text{⑥}^{-1}=\frac14\begin{pmatrix}3&-2&1\\-2&4&-2\\1&-2&3\end{pmatrix}.$$

第三步，验证一边。⑥的第一行 $(2,1,0)$ 乘 $\begin{pmatrix}3&-2&1\\-2&4&-2\\1&-2&3\end{pmatrix}$ 的三列，得 $6-2=4$、$-4+4=0$、$2-2=0$，除以 4 得 $(1,0,0)$；其余两行同样得到 $E$ 的对应行。⑥是对称矩阵，它的逆也是对称的，这不是巧合：由 $(A^{\mathsf T})^{-1}=(A^{-1})^{\mathsf T}$，$A^{\mathsf T}=A$ 时 $A^{-1}$ 等于自己的转置。

> 求 $\begin{pmatrix}1&1&1\\0&1&1\\0&0&1\end{pmatrix}$ 的逆矩阵。
>
> 答案：左半边已是阶梯形，直接从下往上：$r_2-r_3$、$r_1-r_3$，再 $r_1-r_2$，右半边成为 $\begin{pmatrix}1&-1&0\\0&1&-1\\0&0&1\end{pmatrix}$。

#### 有成块的零时，按块求逆

这一小节和例 5 无关，可以单独读。矩阵大了，消元的工作量也大。如果矩阵里有成块的零，可以按 L.3.7 分块，把求逆拆成求几个小块的逆。

先看最简单的分块对角矩阵 $\begin{pmatrix}A_1&O\\O&A_2\end{pmatrix}$，$A_1$、$A_2$ 是可逆方阵（阶数可以不同）。两块互不干扰，各自撤销就行：按分块乘法，

$$\begin{pmatrix}A_1&O\\O&A_2\end{pmatrix}\begin{pmatrix}A_1^{-1}&O\\O&A_2^{-1}\end{pmatrix}=\begin{pmatrix}E_{n_1}&O\\O&E_{n_2}\end{pmatrix},$$

$n_1$、$n_2$ 是两块的阶数，右边就是单位矩阵。由第 2 节验一边就够。例如 $\begin{pmatrix}3&0&0\\0&2&1\\0&5&3\end{pmatrix}$ 分成 $(3)$ 和第 1 节小题的 $\begin{pmatrix}2&1\\5&3\end{pmatrix}$，逆矩阵是 $\begin{pmatrix}\frac13&0&0\\0&3&-1\\0&-5&2\end{pmatrix}$。

右上角不是零块时，$M=\begin{pmatrix}A_1&C\\O&A_2\end{pmatrix}$ 仍可以按块求。仿照二阶上三角矩阵的逆，猜 $M^{-1}=\begin{pmatrix}A_1^{-1}&Y\\O&A_2^{-1}\end{pmatrix}$，按分块乘法，

$$\begin{pmatrix}A_1&C\\O&A_2\end{pmatrix}\begin{pmatrix}A_1^{-1}&Y\\O&A_2^{-1}\end{pmatrix}=\begin{pmatrix}E_{n_1}&A_1Y+CA_2^{-1}\\O&E_{n_2}\end{pmatrix}.$$

要让右上角是 $O$，即 $A_1Y+CA_2^{-1}=O$。把 $CA_2^{-1}$ 移到右边得 $A_1Y=-CA_2^{-1}$；$A_1$ 在 $Y$ 的左边，所以两边左乘 $A_1^{-1}$，得 $Y=-A_1^{-1}CA_2^{-1}$。所以

$$\begin{pmatrix}A_1&C\\O&A_2\end{pmatrix}^{-1}=\begin{pmatrix}A_1^{-1}&-A_1^{-1}CA_2^{-1}\\O&A_2^{-1}\end{pmatrix}.$$

分块的前提是对角线上的块是方阵，并且都可逆。

会求逆了，下一节把它用到以矩阵为未知量的方程上。

合上书，从 $E_s\cdots E_1A=E$ 出发说明 $(A\mid E)$ 为什么会变成 $(E\mid A^{-1})$，再用分块乘法推出分块上三角矩阵的逆。

### 4. $AX=B$、$XA=B$ 怎么解？

已知平面上的线性变换 $T$ 把 $(1,1)^{\mathsf T}$ 送到 $(3,1)^{\mathsf T}$，把 $(1,-1)^{\mathsf T}$ 送到 $(1,-1)^{\mathsf T}$，求 $T$ 的矩阵 $X$。两个条件是 $X(1,1)^{\mathsf T}=(3,1)^{\mathsf T}$ 和 $X(1,-1)^{\mathsf T}=(1,-1)^{\mathsf T}$。把它们并排摆：左边把两个原像拼成矩阵的两列，右边把两个像拼成两列。按列分块乘法，$X$ 乘这个矩阵就是分别乘它的每一列，所以两个条件合成一个等式

$$X\begin{pmatrix}1&1\\1&-1\end{pmatrix}=\begin{pmatrix}3&1\\1&-1\end{pmatrix}.$$

未知数是整个矩阵 $X$。这类以矩阵为未知量的方程叫**矩阵方程**。

$A$ 可逆时，$AX=B$ 两边**左乘** $A^{-1}$，得 $X=A^{-1}B$；$XA=B$ 两边**右乘** $A^{-1}$，得 $X=BA^{-1}$。乘法不能交换，所以 $A^{-1}$ 从哪边乘进去，就留在哪边。上面的 $T$：$\begin{pmatrix}1&1\\1&-1\end{pmatrix}^{-1}=\frac12\begin{pmatrix}1&1\\1&-1\end{pmatrix}$，右乘得

$$X=\begin{pmatrix}3&1\\1&-1\end{pmatrix}\cdot\frac12\begin{pmatrix}1&1\\1&-1\end{pmatrix}=\begin{pmatrix}2&1\\0&1\end{pmatrix}.$$

核对：$X(1,1)^{\mathsf T}=(3,1)^{\mathsf T}$，$X(1,-1)^{\mathsf T}=(1,-1)^{\mathsf T}$。

$X=A^{-1}B$ 也不必先求 $A^{-1}$ 再相乘。和第 3 节同样的道理，把 $A$ 化成 $E$ 的那串行变换（合起来就是 $A^{-1}$）作用在 $(A\mid B)$ 上，得 $(E\mid A^{-1}B)$。$XA=B$ 可以先转置成 $A^{\mathsf T}X^{\mathsf T}=B^{\mathsf T}$，变成前一种。

**方法 4（解矩阵方程）**

1. 移项：含 $X$ 的项移到等号一边，例如 $AX=2X+B$ 变成 $AX-2X=B$。
2. 改写数乘：$2X$ 写成 $2EX$（$X$ 在右侧时）或 $X\cdot2E$（$X$ 在左侧时）。
3. 从同一侧提出 $X$：$AX-2EX=(A-2E)X$，得到 $AX=B$ 或 $XA=B$ 的样子。
4. $AX=B$：用 $(A\mid B)\to(E\mid A^{-1}B)$。$XA=B$：用 $X=BA^{-1}$，或先转置。
5. $A$ 不可逆时不能这样做：$AX=B$ 按列拆成 $A\boldsymbol{x}_j=\boldsymbol{b}_j$；$XA=B$ 先转置成 $A^{\mathsf T}X^{\mathsf T}=B^{\mathsf T}$，再按列拆；这相当于 $X$ 的每一行各自满足一个方程组。

**例 6**　解 $AX=B$，其中 $A=\begin{pmatrix}2&1\\5&3\end{pmatrix}$，$B=\begin{pmatrix}1&0&2\\2&1&1\end{pmatrix}$。

思路是对 $(A\mid B)$ 做行变换，把左半边化成 $E$。

第一步，造一个主元 1。直接用 2 去消 5 会出分数，所以先 $r_2-2r_1$，在第 1 列造出一个 1，再换到上面：

$$\left(\begin{array}{rr|rrr}2&1&1&0&2\\5&3&2&1&1\end{array}\right)\xrightarrow{r_2-2r_1}\left(\begin{array}{rr|rrr}2&1&1&0&2\\1&1&0&1&-3\end{array}\right)\xrightarrow{r_1\leftrightarrow r_2}\left(\begin{array}{rr|rrr}1&1&0&1&-3\\2&1&1&0&2\end{array}\right).$$

第二步，消元并化成 $E$：

$$\xrightarrow{r_2-2r_1}\left(\begin{array}{rr|rrr}1&1&0&1&-3\\0&-1&1&-2&8\end{array}\right)\xrightarrow{-r_2}\left(\begin{array}{rr|rrr}1&1&0&1&-3\\0&1&-1&2&-8\end{array}\right)\xrightarrow{r_1-r_2}\left(\begin{array}{rr|rrr}1&0&1&-1&5\\0&1&-1&2&-8\end{array}\right).$$

左半边成了 $E$，所以

$$X=\begin{pmatrix}1&-1&5\\-1&2&-8\end{pmatrix}.$$

用第 1 节小题的 $A^{-1}$ 核对：$A^{-1}B=\begin{pmatrix}3&-1\\-5&2\end{pmatrix}B$，第一行是 $(3-2,\ -1,\ 6-1)=(1,-1,5)$，一致。

> 解 $XA=C$，其中 $A=\begin{pmatrix}2&1\\5&3\end{pmatrix}$，$C=\begin{pmatrix}1&1\\0&1\end{pmatrix}$。
>
> 答案：两边右乘 $A^{-1}$，$X=CA^{-1}=\begin{pmatrix}1&1\\0&1\end{pmatrix}\begin{pmatrix}3&-1\\-5&2\end{pmatrix}=\begin{pmatrix}-2&1\\-5&2\end{pmatrix}$。

第 5 步值得多说一句。$A$ 不可逆时 $A^{-1}$ 不存在，但方程未必无解。把 $X$ 和 $B$ 按列拆开，$AX=B$ 就是几个方程组 $A\boldsymbol{x}_j=\boldsymbol{b}_j$，用 L.4 的方法 3 逐个解：只要有一个无解，矩阵方程就无解；都有解时，往往有无穷多个 $X$。

有时题目不给矩阵，只给一个关系式。这时设法把它写成「$A\cdot(\text{某个矩阵})=E$」，由第 2 节，一边就够。

**例 7**　方阵 $A$ 满足 $A^2-A-2E=O$。证明 $A$ 与 $A+2E$ 都可逆，并求它们的逆。

关系式里只有 $A$ 的多项式，可以像数一样移项、提公因式（L.3.5）。

先看 $A$。由 $A^2-A=2E$，左边提出 $A$：$A(A-E)=2E$，即

$$A\cdot\tfrac12(A-E)=E,$$

所以 $A$ 可逆，$A^{-1}=\frac12(A-E)$。

再看 $A+2E$，要凑出因式 $A+2E$。数的恒等式能照搬进矩阵，和例 4 同理：$A$ 与 $E$ 的各次幂相乘可以交换。为什么想到多项式除法？关系式是 $x^2-x-2$ 在 $A$ 处的值，用 $x+2$ 去除它，商和余数会告诉我们还差多少：

$$x^2-x-2=(x+2)(x-3)+4.$$

把 $x$ 换成 $A$、常数乘 $E$，由 $A^2-A-2E=O$ 得

$$(A+2E)(A-3E)+4E=O,\qquad\text{即}\qquad(A+2E)\cdot\Big(-\tfrac14(A-3E)\Big)=E .$$

所以 $A+2E$ 可逆，$(A+2E)^{-1}=-\frac14(A-3E)$。直接展开 $(A+2E)(A-3E)=A^2-A-6E=-4E$ 也能核对。

矩阵方程是逆矩阵在考试里最常见的用法：先整理，再看清从哪边乘。下一节回到开头的问题，看逆矩阵在经济计划里算的是什么。

合上书，说出 $AX=B$ 和 $XA=B$ 的解为什么不一样，再用多项式除法重新求一遍例 7 中 $(A+2E)^{-1}$。

### 5. 一个部门多生产一块钱的产品，整个经济要多生产多少？

设经济只有两个部门：农业（部门 1）和工业（部门 2）。生产 1 元农产品要消耗 0.2 元农产品和 0.4 元工业品；生产 1 元工业品要消耗 0.4 元农产品和 0.3 元工业品。把它们排成**直接消耗系数矩阵**

$$A=\begin{pmatrix}0.2&0.4\\0.4&0.3\end{pmatrix}.$$

第 $j$ 列是部门 $j$ 生产 1 元产品对各部门产品的消耗；元素 $a_{ij}$ 是部门 $j$ 每生产 1 元要用掉部门 $i$ 的多少元。

设两部门的总产出是 $\boldsymbol{x}=(x_1,x_2)^{\mathsf T}$（亿元）。按列看法，生产它们要消耗 $A\boldsymbol{x}$，剩下的才能交给居民、政府和出口，叫**最终需求** $\boldsymbol{d}$。所以

$$\boldsymbol{x}-A\boldsymbol{x}=\boldsymbol{d},\qquad\text{即}\qquad(E-A)\boldsymbol{x}=\boldsymbol{d}.$$

当 $E-A$ 可逆时，解唯一，$\boldsymbol{x}=(E-A)^{-1}\boldsymbol{d}$，$(E-A)^{-1}$ 叫**列昂惕夫逆矩阵**。它的第 $j$ 列是 $(E-A)^{-1}\boldsymbol{e}_j$，也就是部门 $j$ 的最终需求多 1 元、其他不变时，各部门总共要多生产多少。这就回答了本节的问题。

**例 8**　对上面的 $A$，求列昂惕夫逆矩阵；若最终需求是农业 100 亿元、工业 200 亿元，两部门各应生产多少？

第一步，求逆。$E-A=\begin{pmatrix}0.8&-0.4\\-0.4&0.7\end{pmatrix}$，$ad-bc=0.56-0.16=0.4$，按二阶公式

$$(E-A)^{-1}=\frac1{0.4}\begin{pmatrix}0.7&0.4\\0.4&0.8\end{pmatrix}=\begin{pmatrix}1.75&1\\1&2\end{pmatrix}.$$

第二步，求总产出：

$$\boldsymbol{x}=\begin{pmatrix}1.75&1\\1&2\end{pmatrix}\begin{pmatrix}100\\200\end{pmatrix}=\begin{pmatrix}375\\500\end{pmatrix}.$$

第三步，检验。农业被消耗 $0.2\times375+0.4\times500=275$，剩 $375-275=100$；工业被消耗 $0.4\times375+0.3\times500=300$，剩 $500-300=200$。

第 2 列 $(1,2)^{\mathsf T}$ 说：工业品的最终需求多 1 元，工业自己要多生产 2 元，农业要多生产 1 元，远多于直接消耗的 0.3 元和 0.4 元。

> 若最终需求变成农业 200 亿元、工业 100 亿元，两部门各应生产多少？
>
> 答案：$\boldsymbol{x}=\begin{pmatrix}1.75&1\\1&2\end{pmatrix}\begin{pmatrix}200\\100\end{pmatrix}=\begin{pmatrix}450\\400\end{pmatrix}$；检验：农业剩 $450-(90+160)=200$，工业剩 $400-(180+120)=100$。

#### 多出来的部分从哪里来？

把连锁反应一轮一轮地算。取工业多 1 元需求，$\boldsymbol{d}=\boldsymbol{e}_2=(0,1)^{\mathsf T}$。

第 0 轮，先生产这 1 元工业品，累计 $(0,1)$。

第 1 轮，生产它消耗了 $A\boldsymbol{e}_2=(0.4,0.3)^{\mathsf T}$，也就是 $A$ 的第 2 列，得补上，累计 $(0.4,1.3)$。

第 2 轮，补这些又消耗 $A^2\boldsymbol{e}_2$，累计 $(0.6,1.55)$；第 3 轮累计 $(0.74,1.705)$。如此下去，一步步逼近列昂惕夫逆矩阵的第 2 列 $(1,2)$。

![工业最终需求多 1 元时，两部门累计总产出随轮数增加：实线是工业，虚线是农业，分别逼近点线 2 和 1，即列昂惕夫逆矩阵的第 2 列](fig/L5-n1.pdf){width=64%}

为什么会逼近这个答案？算到第 $k$ 轮，累计产出是 $(E+A+\cdots+A^k)\boldsymbol{d}$。由例 4 的抵消，

$$(E-A)(E+A+\cdots+A^k)=E-A^{k+1}.$$

两边左乘 $(E-A)^{-1}$，得 $E+A+\cdots+A^k=(E-A)^{-1}-(E-A)^{-1}A^{k+1}$。再右乘 $\boldsymbol{d}$，并把第一项移到左边（两边同减 $(E-A)^{-1}\boldsymbol{d}$ 再变号），得

$$(E-A)^{-1}\boldsymbol{d}-(E+A+\cdots+A^k)\boldsymbol{d}=(E-A)^{-1}A^{k+1}\boldsymbol{d}.$$

左边是答案和累计产出的差。所以只要 $k$ 越来越大时 $A^{k+1}\boldsymbol{d}\to\boldsymbol{0}$，右边就跟着趋于 $\boldsymbol{0}$：固定矩阵 $(E-A)^{-1}$ 乘一个向量，结果的每个分量都是这个向量各分量的固定倍数之和，各分量趋于 0，和也趋于 0。于是累计产出就越来越接近答案。

本例的新增量为什么越来越小？$A$ 的元素都非负，两列之和是 0.6 和 0.7。设某一轮新增的是非负向量 $(y_1,y_2)^{\mathsf T}$，下一轮新增的两个分量之和是

$$0.6y_1+0.7y_2\le0.7(y_1+y_2),$$

至多是上一轮总和的 0.7 倍。一轮轮乘下去，第 $k+1$ 轮新增量的分量和不超过 $0.7^{k+1}$，所以 $A^{k+1}\boldsymbol{d}\to\boldsymbol{0}$。

列和小于 1 的经济含义是：每个部门生产 1 元，消耗的投入不到 1 元。这只是本例用到的一个充分条件；「越来越接近」的严格含义在 C.14 讲级数时说明。

合上书，从「总产出 = 中间消耗 + 最终需求」推出 $\boldsymbol{x}=(E-A)^{-1}\boldsymbol{d}$，并说明 $(E-A)^{-1}$ 第 $j$ 列的含义。

### 本章小结

| 方法 | 什么时候用 | 对应题号 |
|---|---|---|
| 方法 1（二阶公式） | $2\times2$ 求逆、判断可逆 | L5-01、L5-02 |
| 方法 2（判断可逆） | 数主元判断可逆；证明 $B=A^{-1}$ 只验一边；由 $A^k=O$ 等条件证可逆 | L5-03、L5-05、L5-06 |
| 方法 3（初等行变换求逆） | $n$ 阶具体矩阵求逆；分块对角、分块上三角按块求逆 | L5-07、L5-10 |
| 方法 4（解矩阵方程） | $AX=B$、$XA=B$；由关系式求逆；投入产出 | L5-04、L5-08、L5-09、L5-11–L5-13 |

可逆大定理长到了这样。$n$ 阶方阵 $A$ 的下列条件互相等价：

| 条件 | 出处 |
|---|---|
| 消元后有 $n$ 个主元（行最简形是 $E$） | L.4 |
| 对每个 $\boldsymbol{b}$，$A\boldsymbol{x}=\boldsymbol{b}$ 都有唯一解 | L.4 |
| $A\boldsymbol{x}=\boldsymbol{0}$ 只有零解 | L.4 |
| $A$ 可逆 | 本章新增 |
| 存在 $B$ 使 $AB=E$（只验一边） | 本章新增 |
| $A$ 是初等矩阵的乘积 | 本章新增 |

用变换的话说，这几行都是同一件事：$A$ 没有把任何方向压扁，所以能撤销。⑥、①、②、③满足，④、⑤不满足。
