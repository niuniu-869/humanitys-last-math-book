## L.7 · 线性相关与秩

一张销售表里同时存了「不含税价」和「含税价」。税率 13% 时，含税价总是不含税价的 1.13 倍，第二列没有带来新信息。用它们去预测销量（回归）时，给不含税价的权重加 1.13、同时给含税价的权重减 1，每一行的预测值都不变，参数解就不唯一。表一大，多余的列往往是好几列的组合，一眼看不出来。本章给出判断哪些列多余、真正独立的有几列的通用办法，并把答案浓缩成一个数，叫作**秩**。

这个问题最早出现在解方程组里：如果第三个方程等于前两个相加，看起来有三个方程，实际只有两个。L.6 的行列式能判断方阵会不会把空间压扁，却说不出压成了几维，而且只对方阵有定义。弗罗贝尼乌斯用从矩阵里取出的小行列式（第 5 节的「子式」）刻画了真正独立的方程个数，把它叫作秩（德文 Rang）。今天的教材从「一组向量里有没有多余的」讲起，再证明它和子式的说法一致。

用变换的语言说，秩回答的是 L.6 留下的问题：**变换把空间压扁以后，还剩几维。**平面被压成一条线，秩就是 1。

本章第 1 节定义线性相关；第 2 节看增减向量、增减分量时相关性怎样变；第 3 节看一组向量由另一组表示时个数的限制；第 4 节定义极大无关组和向量组的秩；第 5 节说明行秩、列秩和子式给出同一个数；第 6 节用秩给矩阵分类（支线）；第 7 节估计乘积与和的秩。

### 1. 一组向量里有没有多余的？

L.1 例 3 里，三个向量

$$(1,0,1)^{\mathsf T},\qquad (0,1,1)^{\mathsf T},\qquad (1,1,2)^{\mathsf T}$$

只张成一个平面，因为第三个等于前两个之和，它是多余的。

可多余的到底是哪一个？同一个等式移项以后，第一个也等于第三个减第二个，说第一个多余也行。为了不必先挑出「哪一个」，把关系写成对称的形式：

$$1\cdot\begin{pmatrix}1\\0\\1\end{pmatrix}+1\cdot\begin{pmatrix}0\\1\\1\end{pmatrix}-1\cdot\begin{pmatrix}1\\1\\2\end{pmatrix}=\boldsymbol 0.$$

三个向量配上一组不全为零的系数，组合出了零向量，在图上就是走一圈回到原点（图 L7-n3）。这就是「有多余的」的对称说法。

![三个向量都在阴影平面 $z=x+y$ 里；走 $\boldsymbol\alpha_1$、再走 $\boldsymbol\alpha_2$、再沿虚线逆着 $\boldsymbol\alpha_3$ 走，回到原点](fig/L7-n3.pdf){width=55%}

#### 定义

本章按考研的习惯，把一组向量记作 $\boldsymbol\alpha_1,\dots,\boldsymbol\alpha_s$，叫作**向量组**。

对向量组 $\boldsymbol\alpha_1,\dots,\boldsymbol\alpha_s$，如果存在**不全为零**的数 $k_1,\dots,k_s$，使

$$k_1\boldsymbol\alpha_1+k_2\boldsymbol\alpha_2+\cdots+k_s\boldsymbol\alpha_s=\boldsymbol 0,$$

就说它们**线性相关**；如果只有 $k_1=\cdots=k_s=0$ 才能使上式成立，就说它们**线性无关**。

系数全取 0 总能得到零向量，这不说明任何事。线性相关说的是「除了全取 0，还有别的办法」。

从这里开始，判断相关、无关只用这个定义。它和「有多余的」确实是一回事，下面说清楚。

#### 「有多余的」和定义是同一件事

「某个向量能由其余向量表示」要有「其余向量」可用，所以先设向量组至少有两个向量。

一方面，若定义里的某个 $k_j\ne0$，两边除以 $k_j$ 再移项，$\boldsymbol\alpha_j$ 就写成了其余向量的线性组合。

另一方面，若 $\boldsymbol\alpha_j$ 等于其余向量的某个组合，把它移到等号另一边，$\boldsymbol\alpha_j$ 的系数是 $-1\ne0$，这组系数不全为零，所以向量组相关。

于是，对两个以上的向量，线性相关 $\iff$ 至少有一个向量能由其余向量线性表示。

注意是「至少有一个」，不是「每一个」。$(1,0)^{\mathsf T},(2,0)^{\mathsf T},(0,1)^{\mathsf T}$ 线性相关（第二个是第一个的 2 倍），但 $(0,1)^{\mathsf T}$ 不能由前两个表示。

向量少的时候可以直接看：

- 一个向量相关当且仅当它是零向量：没有「其余」可言，直接用定义，$k\boldsymbol\alpha=\boldsymbol 0$ 且 $k\ne0$，除以 $k$ 得 $\boldsymbol\alpha=\boldsymbol 0$。
- 两个向量相关当且仅当一个是另一个的倍数，也就是共线（L.1.3）。
- 含零向量的向量组一定相关：给零向量配系数 1，其余配 0。

#### 排成矩阵，用消元判断

向量多了，就把它们排成矩阵的列，$A=(\boldsymbol\alpha_1,\dots,\boldsymbol\alpha_s)$。由 L.3.1 的按列看法，$k_1\boldsymbol\alpha_1+\cdots+k_s\boldsymbol\alpha_s=A\boldsymbol k$，其中 $\boldsymbol k=(k_1,\dots,k_s)^{\mathsf T}$。所以「有不全为零的 $k_i$ 组合出 $\boldsymbol 0$」就是「$A\boldsymbol x=\boldsymbol 0$ 有非零解 $\boldsymbol x=\boldsymbol k$」。

用变换的眼光看，这句话有一个画面。投影④ $\frac12\begin{pmatrix}1&1\\1&1\end{pmatrix}$ 的两列都是 $(\frac12,\frac12)^{\mathsf T}$，所以

$$1\cdot\text{第 1 列}-1\cdot\text{第 2 列}=\boldsymbol 0,\qquad\text{也就是}\qquad \frac12\begin{pmatrix}1&1\\1&1\end{pmatrix}\begin{pmatrix}1\\-1\end{pmatrix}=\begin{pmatrix}0\\0\end{pmatrix}.$$

相关关系的系数 $(1,-1)^{\mathsf T}$，正好是一个被压到原点的方向（图 L7-n1）。

![投影④把 $\boldsymbol e_1$、$\boldsymbol e_2$ 送到同一点，所以虚线方向 $\boldsymbol e_1-\boldsymbol e_2=(1,-1)^{\mathsf T}$ 被送到原点；系数 $1,-1$ 就是两列的相关关系](fig/L7-n1.pdf){width=78%}

同一件事有三种说法，把它们对齐：

| 方程组 | 列向量 | 变换 |
|---|---|---|
| $A\boldsymbol x=\boldsymbol 0$ 有非零解 | 列线性相关 | 有一个非零方向被压到原点 |
| $A\boldsymbol x=\boldsymbol 0$ 只有零解 | 列线性无关 | 没有方向被压到原点 |

由 L.4.3，对 $A$ 消元以后，主元个数等于未知数个数 $s$ 时没有自由未知量，只有零解；主元少于 $s$ 时有自由未知量，就有非零解。$A$ 是方阵时，由 L.6.3，只有零解等价于 $|A|\ne0$。

**方法 1（排成列，数主元）**

1. 把向量排成矩阵的列，用初等行变换化成阶梯形。
2. 主元个数等于向量个数，则线性无关；少于向量个数，则线性相关。
3. 相关时，解出 $A\boldsymbol x=\boldsymbol 0$ 的一个非零解，它的分量就是一组相关系数。
4. $n$ 个 $n$ 维向量可以直接算行列式：$|A|=0$ 相关，$|A|\ne0$ 无关。

**例 1**　判断 $\boldsymbol\alpha_1=(1,2,-1,0)^{\mathsf T}$，$\boldsymbol\alpha_2=(2,1,0,1)^{\mathsf T}$，$\boldsymbol\alpha_3=(0,3,-2,-1)^{\mathsf T}$ 是否线性相关；若相关，写出一个相关关系。

第一步，第二行减去第一行的 2 倍，第三行加上第一行，消去第一列：

$$\begin{pmatrix}1&2&0\\2&1&3\\-1&0&-2\\0&1&-1\end{pmatrix}\to\begin{pmatrix}1&2&0\\0&-3&3\\0&2&-2\\0&1&-1\end{pmatrix}.$$

第二步，第四行的 1 当主元不用分数，所以交换第二、四行：

$$\to\begin{pmatrix}1&2&0\\0&1&-1\\0&2&-2\\0&-3&3\end{pmatrix}.$$

第三步，第三行减去新第二行的 2 倍，第四行加上它的 3 倍，两行都成为零行：

$$\to\begin{pmatrix}1&2&0\\0&1&-1\\0&0&0\\0&0&0\end{pmatrix}.$$

只有 2 个主元，少于 3 个向量，所以线性相关。

第四步，求相关关系。第三个未知数是自由的，取 $x_3=1$；由第二行 $x_2-x_3=0$ 得 $x_2=1$；由第一行 $x_1+2x_2=0$ 得 $x_1=-2$。所以

$$-2\boldsymbol\alpha_1+\boldsymbol\alpha_2+\boldsymbol\alpha_3=\boldsymbol 0,\qquad\text{即}\qquad\boldsymbol\alpha_3=2\boldsymbol\alpha_1-\boldsymbol\alpha_2.$$

> 判断 $(1,0,1,1)^{\mathsf T}$、$(1,1,0,1)^{\mathsf T}$、$(0,1,1,1)^{\mathsf T}$ 是否线性相关。
>
> 答案：排成列，第三、四行减去第一行得 $(0,-1,1)$、$(0,0,1)$；第三行再加第二行得 $(0,0,2)$，第四行减去它的 $\frac12$ 成零行。三列都有主元，无关。

**例 2**　$t$ 取何值时，$\boldsymbol\alpha_1=(1,1,1)^{\mathsf T}$，$\boldsymbol\alpha_2=(1,2,3)^{\mathsf T}$，$\boldsymbol\alpha_3=(1,3,t)^{\mathsf T}$ 线性相关？这时写出相关关系。

和例 1 不同，这里矩阵是方阵，可以用方法 1 的第 4 步算行列式。第二、三行各减去第一行，再按第一列展开：

$$\begin{vmatrix}1&1&1\\1&2&3\\1&3&t\end{vmatrix}=\begin{vmatrix}1&1&1\\0&1&2\\0&2&t-1\end{vmatrix}=1\cdot\big[(t-1)-4\big]=t-5.$$

所以 $t=5$ 时线性相关，$t\ne5$ 时无关。

$t=5$ 时回到第 3 步解 $A\boldsymbol x=\boldsymbol 0$：上面消元得到的两行 $(0,1,2)$、$(0,2,4)$ 成比例，取 $x_3=1$，得 $x_2=-2$、$x_1=1$：

$$\boldsymbol\alpha_1-2\boldsymbol\alpha_2+\boldsymbol\alpha_3=\boldsymbol 0.$$

#### 只给关系、不给分量时：回到定义

向量不给分量、只给它们之间的关系时，没法排成数字矩阵，要回到定义。

**方法 2（定义法证无关）**

1. 设 $k_1\boldsymbol\beta_1+\cdots+k_s\boldsymbol\beta_s=\boldsymbol 0$。
2. 把各 $\boldsymbol\beta_i$ 用已知线性无关的 $\boldsymbol\alpha_j$ 代入，按 $\boldsymbol\alpha_j$ 合并同类项。
3. 因为 $\boldsymbol\alpha_j$ 无关，每个 $\boldsymbol\alpha_j$ 的系数都是 0，得到关于 $k_i$ 的齐次方程组。
4. 它只有零解，$\boldsymbol\beta_i$ 就无关；有非零解，就相关，非零解就是相关系数。

**例 3**　已知 $\boldsymbol\alpha_1,\boldsymbol\alpha_2,\boldsymbol\alpha_3$ 线性无关，$\boldsymbol\beta_1=\boldsymbol\alpha_1+\boldsymbol\alpha_2$，$\boldsymbol\beta_2=\boldsymbol\alpha_2+\boldsymbol\alpha_3$，$\boldsymbol\beta_3=\boldsymbol\alpha_3+\boldsymbol\alpha_1$。证明 $\boldsymbol\beta_1,\boldsymbol\beta_2,\boldsymbol\beta_3$ 线性无关。

第一步，设 $k_1\boldsymbol\beta_1+k_2\boldsymbol\beta_2+k_3\boldsymbol\beta_3=\boldsymbol 0$。

第二步，代入 $\boldsymbol\beta$ 的表达式，按 $\boldsymbol\alpha$ 合并：

$$(k_1+k_3)\boldsymbol\alpha_1+(k_1+k_2)\boldsymbol\alpha_2+(k_2+k_3)\boldsymbol\alpha_3=\boldsymbol 0.$$

第三步，$\boldsymbol\alpha_1,\boldsymbol\alpha_2,\boldsymbol\alpha_3$ 无关，所以三个系数都是 0：

$$k_1+k_3=0,\qquad k_1+k_2=0,\qquad k_2+k_3=0.$$

第四步，三式相加得 $k_1+k_2+k_3=0$，再分别减去三个方程，得 $k_1=k_2=k_3=0$。所以 $\boldsymbol\beta_1,\boldsymbol\beta_2,\boldsymbol\beta_3$ 线性无关。

把三个加号都改成减号（$\boldsymbol\beta_1=\boldsymbol\alpha_1-\boldsymbol\alpha_2$ 等），三者相加等于 $\boldsymbol 0$，结论就反过来：相关。

> 已知 $\boldsymbol\alpha_1,\boldsymbol\alpha_2$ 线性无关，判断 $\boldsymbol\alpha_1+2\boldsymbol\alpha_2$ 与 $2\boldsymbol\alpha_1+\boldsymbol\alpha_2$ 是否线性无关。
>
> 答案：合并得 $(k_1+2k_2)\boldsymbol\alpha_1+(2k_1+k_2)\boldsymbol\alpha_2=\boldsymbol 0$，所以 $k_1+2k_2=0$，$2k_1+k_2=0$，系数行列式 $-3\ne0$，只有零解，线性无关。

合上书，写出线性相关的定义，说明它为什么等价于「$A\boldsymbol x=\boldsymbol 0$ 有非零解」，在变换的图上又对应什么。

### 2. 加一个向量、去掉一个、给每个向量添几个分量，相关性怎样变？

下面四条性质都从定义直接推出，做选择题时最常用。

**(1) 部分相关，则整体相关；整体无关，则部分无关。**

设部分向量有不全为零的系数组合出 $\boldsymbol 0$，给其余向量都配系数 0，整个组的系数仍不全为零，组合仍是 $\boldsymbol 0$。后半句是前半句的逆否命题。

反方向不成立：$(1,0)^{\mathsf T},(0,1)^{\mathsf T},(1,1)^{\mathsf T}$ 相关，前两个却无关。

**(2) 无关组添分量后仍无关；相关组去掉分量后仍相关。**

记号：给每个 $\boldsymbol\alpha_i$ 在相同的位置添上几个分量，添好的向量记作 $\boldsymbol\alpha_i'$，例如 $(1,0)^{\mathsf T}$ 末尾添上 3 成为 $(1,0,3)^{\mathsf T}$。

写出 $k_1\boldsymbol\alpha_1'+\cdots+k_s\boldsymbol\alpha_s'=\boldsymbol 0$ 逐个分量的方程：原来的方程一个不少，又多了新分量的方程。原来只有零解，加了方程更只有零解，所以添分量后仍无关。反过来，长向量的非零系数也满足其中原来那些方程，所以去掉分量后仍相关。

两个方向可以这样记：添分量，保住的是无关；去分量，保住的是相关。方向不能倒过来。去掉第三个分量，就是看箭头在地面（$xy$ 平面）上的影子（图 L7-n2）：两根不共线的箭头 $(1,0,0)^{\mathsf T}$、$(2,0,1)^{\mathsf T}$，影子 $(1,0)^{\mathsf T}$、$(2,0)^{\mathsf T}$ 却共线。所以箭头无关推不出影子无关。

![去掉第三个分量就是看地面上的影子：两根实线箭头不共线（无关），影子 $(1,0)$ 和虚线的影子 $(2,0)$ 却在同一条直线上（相关）](fig/L7-n2.pdf){width=62%}

**(3) 向量个数大于维数时必相关。**特别地，$n+1$ 个 $n$ 维向量一定相关。

理由：$A\boldsymbol x=\boldsymbol 0$ 有 $n$ 个方程、$s>n$ 个未知数，主元最多 $n$ 个，由 L.4.3 有非零解。

**(4) $\boldsymbol\alpha_1,\dots,\boldsymbol\alpha_s$ 无关，添上 $\boldsymbol\beta$ 后相关，则 $\boldsymbol\beta$ 能由 $\boldsymbol\alpha_1,\dots,\boldsymbol\alpha_s$ 线性表示，并且表示法唯一。**

这条是后面几节的工具，考试也常要求写证明。思路：相关给出一个组合，再说明 $\boldsymbol\beta$ 的系数不可能是 0。

- 第一步，由相关，有不全为零的 $k_1,\dots,k_s,k$ 使 $k_1\boldsymbol\alpha_1+\cdots+k_s\boldsymbol\alpha_s+k\boldsymbol\beta=\boldsymbol 0$。
- 第二步，$k\ne0$。否则式子只剩 $k_1\boldsymbol\alpha_1+\cdots+k_s\boldsymbol\alpha_s=\boldsymbol 0$，而 $k_i$ 不全为零，说明 $\boldsymbol\alpha_i$ 相关，矛盾。
- 第三步，两边除以 $k$ 再移项，$\boldsymbol\beta$ 就表示出来了。
- 第四步，唯一性。若 $\boldsymbol\beta=\sum c_i\boldsymbol\alpha_i=\sum d_i\boldsymbol\alpha_i$，两式相减得 $\sum(c_i-d_i)\boldsymbol\alpha_i=\boldsymbol 0$，由无关得每个 $c_i=d_i$。

「$\boldsymbol\alpha$ 无关」这个前提不能少。$(1,0)^{\mathsf T},(2,0)^{\mathsf T}$ 本身相关，添上 $(0,1)^{\mathsf T}$ 后相关，但 $(0,1)^{\mathsf T}$ 不能由前两个表示。

**方法 3（用性质推相关性）**

1. 从已知无关（或相关）的组出发，用性质 (1) 传到它的部分（或整体）。
2. 「无关组加一个向量变相关」用性质 (4) 转成「这个向量能被唯一表示」。
3. 要证「不能表示」，用反证法：假设能表示，推出某个已知无关的组相关。

**例 4**　已知 $\boldsymbol\alpha_1,\boldsymbol\alpha_2,\boldsymbol\alpha_3$ 线性相关，$\boldsymbol\alpha_2,\boldsymbol\alpha_3,\boldsymbol\alpha_4$ 线性无关。证明：(1) $\boldsymbol\alpha_1$ 能由 $\boldsymbol\alpha_2,\boldsymbol\alpha_3$ 线性表示；(2) $\boldsymbol\alpha_4$ 不能由 $\boldsymbol\alpha_1,\boldsymbol\alpha_2,\boldsymbol\alpha_3$ 线性表示。

(1) $\boldsymbol\alpha_2,\boldsymbol\alpha_3$ 是无关组 $\boldsymbol\alpha_2,\boldsymbol\alpha_3,\boldsymbol\alpha_4$ 的一部分，由性质 (1) 也无关。添上 $\boldsymbol\alpha_1$ 以后相关，由性质 (4)，

$$\boldsymbol\alpha_1=l_2\boldsymbol\alpha_2+l_3\boldsymbol\alpha_3.$$

(2) 用反证法。假设 $\boldsymbol\alpha_4=k_1\boldsymbol\alpha_1+k_2\boldsymbol\alpha_2+k_3\boldsymbol\alpha_3$，把 (1) 的结果代进去：

$$\boldsymbol\alpha_4=(k_1l_2+k_2)\boldsymbol\alpha_2+(k_1l_3+k_3)\boldsymbol\alpha_3.$$

$\boldsymbol\alpha_4$ 能由 $\boldsymbol\alpha_2,\boldsymbol\alpha_3$ 表示，于是 $\boldsymbol\alpha_2,\boldsymbol\alpha_3,\boldsymbol\alpha_4$ 相关，与已知矛盾。

> 判断真假：(a) 若 $\boldsymbol\alpha_1,\boldsymbol\alpha_2$ 无关，$\boldsymbol\alpha_1,\boldsymbol\alpha_2,\boldsymbol\beta$ 相关，则 $\boldsymbol\beta$ 能由 $\boldsymbol\alpha_1,\boldsymbol\alpha_2$ 表示；(b) 若 $\boldsymbol\alpha_1,\boldsymbol\alpha_2,\boldsymbol\alpha_3$ 相关，则 $\boldsymbol\alpha_3$ 能由 $\boldsymbol\alpha_1,\boldsymbol\alpha_2$ 表示。
>
> 答案：(a) 真，就是性质 (4)。(b) 假，缺了「$\boldsymbol\alpha_1,\boldsymbol\alpha_2$ 无关」这个前提，反例是 $(1,0)^{\mathsf T},(2,0)^{\mathsf T},(0,1)^{\mathsf T}$。

#### 无关、正交、两两不共线，并排看

先自己判断：哪组线性无关？哪组两两正交？

$$\text{甲：}(1,0)^{\mathsf T},(0,1)^{\mathsf T};\qquad\text{乙：}(1,0)^{\mathsf T},(1,1)^{\mathsf T};\qquad\text{丙：}(1,0,1)^{\mathsf T},(0,1,1)^{\mathsf T},(1,1,2)^{\mathsf T}.$$

甲既无关又正交；乙无关，但夹角 $45^\circ$；丙两两不共线，却线性相关（本章开头那三个）。

原理是：**两两正交的非零向量一定线性无关**，反过来不成立。在 $\sum k_i\boldsymbol\alpha_i=\boldsymbol 0$ 两边和 $\boldsymbol\alpha_j$ 作点积，其余各项因为正交都是 0，剩下 $k_j\lVert\boldsymbol\alpha_j\rVert^2=0$（$\lVert\cdot\rVert$ 是 L.2 的长度，即高中的 $|\cdot|$），而 $\boldsymbol\alpha_j\ne\boldsymbol 0$，所以 $k_j=0$。无关只要求「谁也不能由别人拼出来」，比垂直弱得多；「两两不共线」看不到三个一起的关系，比无关还弱。

合上书，默写性质 (4) 的四步证明，并用影子的画面说明「添分量」为什么不能反过来用。

### 3. 一组向量能由另一组表示时，个数有什么限制？

例 3 的 $\boldsymbol\beta_1,\boldsymbol\beta_2,\boldsymbol\beta_3$ 每一个都能由 $\boldsymbol\alpha_1,\boldsymbol\alpha_2,\boldsymbol\alpha_3$ 线性表示，这叫**向量组 $\boldsymbol\beta$ 能由向量组 $\boldsymbol\alpha$ 线性表示**。

由 L.3.7 的按列分块，$(\boldsymbol\alpha_1,\boldsymbol\alpha_2,\boldsymbol\alpha_3)K$ 的第 $j$ 列是各 $\boldsymbol\alpha$ 以 $K$ 的第 $j$ 列为系数的组合。所以把 $\boldsymbol\beta_j$ 的系数放进 $K$ 的第 $j$ 列，三个表示式就并成一个矩阵等式：

$$(\boldsymbol\beta_1,\boldsymbol\beta_2,\boldsymbol\beta_3)=(\boldsymbol\alpha_1,\boldsymbol\alpha_2,\boldsymbol\alpha_3)\begin{pmatrix}1&0&1\\1&1&0\\0&1&1\end{pmatrix}.$$

一般地，以两组向量为列分别排成 $A$、$B$，「$\boldsymbol\beta_1,\dots,\boldsymbol\beta_t$ 能由 $\boldsymbol\alpha_1,\dots,\boldsymbol\alpha_s$ 表示」就是存在 $s\times t$ 矩阵 $K$ 使 $B=AK$。

#### 以少表多，多的必相关

先看一个具体的情形。设 $\boldsymbol\beta_1=\boldsymbol\alpha_1+\boldsymbol\alpha_2$，$\boldsymbol\beta_2=\boldsymbol\alpha_1-\boldsymbol\alpha_2$，$\boldsymbol\beta_3=2\boldsymbol\alpha_1+\boldsymbol\alpha_2$。三个 $\boldsymbol\beta$ 由两个 $\boldsymbol\alpha$ 表示，$K$ 是 $2\times3$ 矩阵：

$$(\boldsymbol\beta_1,\boldsymbol\beta_2,\boldsymbol\beta_3)=(\boldsymbol\alpha_1,\boldsymbol\alpha_2)\begin{pmatrix}1&1&2\\1&-1&1\end{pmatrix}.$$

$K\boldsymbol x=\boldsymbol 0$ 只有 2 个方程、3 个未知数，一定有非零解，例如 $\boldsymbol x=(3,1,-2)^{\mathsf T}$。于是 $3\boldsymbol\beta_1+\boldsymbol\beta_2-2\boldsymbol\beta_3=(\boldsymbol\alpha_1,\boldsymbol\alpha_2)K\boldsymbol x=\boldsymbol 0$。

不管 $\boldsymbol\alpha_1,\boldsymbol\alpha_2$ 是什么，三个 $\boldsymbol\beta$ 都相关：它们都躺在 $\boldsymbol\alpha_1,\boldsymbol\alpha_2$ 张成的平面（或直线）里，平面挤不下三个互不多余的方向。这个论证对一般情形原样成立。

**替换定理**　若 $\boldsymbol\beta_1,\dots,\boldsymbol\beta_t$ 能由 $\boldsymbol\alpha_1,\dots,\boldsymbol\alpha_s$ 线性表示，并且 $t>s$，则 $\boldsymbol\beta_1,\dots,\boldsymbol\beta_t$ 线性相关。

证明：写成 $B=AK$，$K$ 是 $s\times t$ 矩阵。$K\boldsymbol x=\boldsymbol 0$ 的未知数比方程多，由 L.4.3 有非零解 $\boldsymbol x$，于是 $B\boldsymbol x=A(K\boldsymbol x)=\boldsymbol 0$，$\boldsymbol\beta$ 们相关。记成一句话：**以少表多，多的必相关。**

它的逆否形式更常用：若 $\boldsymbol\beta_1,\dots,\boldsymbol\beta_t$ 线性无关，又能由 $\boldsymbol\alpha_1,\dots,\boldsymbol\alpha_s$ 表示，则 $t\le s$。上一节的性质 (3) 是它的特例，因为任何 $n$ 维向量都能由 $\boldsymbol e_1,\dots,\boldsymbol e_n$ 这 $n$ 个向量表示。

两组向量能互相线性表示时，称它们**等价**。两个等价的线性无关组，互相用逆否形式，个数 $t\le s$ 且 $s\le t$，所以个数相等。

#### 新组无关不无关，只看 $K$

$\boldsymbol\alpha$ 无关时，$A\boldsymbol y=\boldsymbol 0$ 只有零解，于是

$$B\boldsymbol x=A(K\boldsymbol x)=\boldsymbol 0\iff K\boldsymbol x=\boldsymbol 0,$$

$\boldsymbol\beta$ 是否无关完全由 $K$ 决定。

**方法 4（$B=AK$，看 $K$）**

1. 把每个 $\boldsymbol\beta_j$ 的系数写成 $K$ 的第 $j$ 列（按列写，不要写成行）。
2. $\boldsymbol\alpha$ 线性无关时，$\boldsymbol\beta$ 线性无关 $\iff$ $K\boldsymbol x=\boldsymbol 0$ 只有零解；$K$ 是方阵时 $\iff|K|\ne0$。
3. 相关时，$K\boldsymbol x=\boldsymbol 0$ 的非零解就是 $\boldsymbol\beta$ 之间的相关系数。

例 3 的 $K$ 行列式是 2，所以无关。方法 4 把方法 2 的四步压成了一个行列式。

**例 5**　$\boldsymbol\alpha_1,\boldsymbol\alpha_2,\boldsymbol\alpha_3$ 线性无关，$\boldsymbol\beta_1=\boldsymbol\alpha_1+2\boldsymbol\alpha_2$，$\boldsymbol\beta_2=\boldsymbol\alpha_2+t\boldsymbol\alpha_3$，$\boldsymbol\beta_3=\boldsymbol\alpha_1+2\boldsymbol\alpha_3$。$t$ 取何值时 $\boldsymbol\beta_1,\boldsymbol\beta_2,\boldsymbol\beta_3$ 线性相关？写出此时的相关关系。

第一步，写 $K$。三列依次是三个 $\boldsymbol\beta$ 的系数 $(1,2,0)^{\mathsf T}$、$(0,1,t)^{\mathsf T}$、$(1,0,2)^{\mathsf T}$。

第二步，按第一行展开：

$$|K|=\begin{vmatrix}1&0&1\\2&1&0\\0&t&2\end{vmatrix}=1\cdot(2-0)-0+1\cdot(2t-0)=2t+2.$$

所以 $t=-1$ 时相关。

第三步，$t=-1$ 时解 $K\boldsymbol x=\boldsymbol 0$。取 $x_3=1$：第一行 $x_1+x_3=0$ 给出 $x_1=-1$，第二行 $2x_1+x_2=0$ 给出 $x_2=2$，第三行 $-x_2+2x_3=0$ 也成立。所以

$$-\boldsymbol\beta_1+2\boldsymbol\beta_2+\boldsymbol\beta_3=\boldsymbol 0.$$

> $\boldsymbol\alpha_1,\boldsymbol\alpha_2,\boldsymbol\alpha_3$ 线性无关，$\boldsymbol\beta_1=\boldsymbol\alpha_1+\boldsymbol\alpha_2+\boldsymbol\alpha_3$，$\boldsymbol\beta_2=\boldsymbol\alpha_1+2\boldsymbol\alpha_2+3\boldsymbol\alpha_3$，$\boldsymbol\beta_3=\boldsymbol\alpha_1+3\boldsymbol\alpha_2+t\boldsymbol\alpha_3$。$t$ 取何值时 $\boldsymbol\beta$ 们相关？
>
> 答案：$K$ 的三列正是例 2 的三个向量，$|K|=t-5$。所以 $t=5$ 时相关，由例 2 的解，$\boldsymbol\beta_1-2\boldsymbol\beta_2+\boldsymbol\beta_3=\boldsymbol 0$。

合上书，用 $B=AK$ 写出替换定理的证明。

### 4. 一组向量里最多能挑出几个互不多余的？

一组向量相关时，去掉多余的向量，能拼出的东西不变（L.1.3）。去到不能再去，剩下的就是「骨架」。

设向量组 $T$ 中有一部分 $\boldsymbol\alpha_{i_1},\dots,\boldsymbol\alpha_{i_r}$ 线性无关，而从 $T$ 中任取一个别的向量添进来都相关，这一部分就叫 $T$ 的一个**极大线性无关组**，简称极大无关组。由第 2 节的性质 (4)，「添进来都相关」等价于「$T$ 中每个向量都能由它表示」。

极大无关组一般不唯一。例如 $(1,0)^{\mathsf T},(0,1)^{\mathsf T},(1,1)^{\mathsf T}$ 中任意两个都是极大无关组。

但个数总相同。两个极大无关组都能表示整个 $T$，当然能互相表示，是等价的线性无关组；由上一节，个数相等。这个公共的个数叫向量组的**秩**，记作 $r(\boldsymbol\alpha_1,\dots,\boldsymbol\alpha_s)$。只含零向量的向量组挑不出线性无关的向量，规定它的秩为 0。由定义，向量组线性无关 $\iff$ 秩等于向量个数。

秩还能比较：若向量组 $\boldsymbol\beta$ 能由向量组 $\boldsymbol\alpha$ 表示，则 $r(\boldsymbol\beta)\le r(\boldsymbol\alpha)$。因为 $\boldsymbol\beta$ 的极大无关组能由 $\boldsymbol\alpha$ 表示，从而能由 $\boldsymbol\alpha$ 的极大无关组表示；由替换定理的逆否形式，它的个数不超过后者。所以等价的向量组秩相等。

#### 行变换不改变列之间的关系

怎样找出极大无关组？先拿三阶压扁⑤ 来试，它的三列是

$$\boldsymbol a_1=(1,2,3)^{\mathsf T},\qquad\boldsymbol a_2=(2,4,6)^{\mathsf T},\qquad\boldsymbol a_3=(1,3,4)^{\mathsf T}.$$

它的行最简形（L.4.2）是

$$\begin{pmatrix}1&2&1\\2&4&3\\3&6&4\end{pmatrix}\to\begin{pmatrix}1&2&0\\0&0&1\\0&0&0\end{pmatrix}.$$

行最简形里，列之间的关系一眼看得出：第 2 列是第 1 列的 2 倍；第 1、3 列是 $\boldsymbol e_1$、$\boldsymbol e_2$，无关。回到原来的列，确实 $\boldsymbol a_2=2\boldsymbol a_1$，而 $\boldsymbol a_1,\boldsymbol a_3$ 不共线。

这不是巧合：**初等行变换不改变各列之间的线性关系。**理由是一串行变换相当于左乘一个可逆矩阵 $P$（L.4.4、L.5.2），而

$$A\boldsymbol x=\boldsymbol 0\iff PA\boldsymbol x=\boldsymbol 0.$$

左推右是两边左乘 $P$，右推左是两边左乘 $P^{-1}$。所以 $A$ 的各列满足的每一个关系 $x_1\boldsymbol a_1+\cdots+x_n\boldsymbol a_n=\boldsymbol 0$，$PA$ 的各列也满足，反过来也一样。

剩下的问题是在行最简形里怎样读关系。设主元列依次是 $\boldsymbol e_1,\dots,\boldsymbol e_r$，它们无关。一个非主元列的形状是 $(c_1,\dots,c_r,0,\dots,0)^{\mathsf T}$（阶梯形里主元行下面全是 0），它正好等于

$$c_1\boldsymbol e_1+c_2\boldsymbol e_2+\cdots+c_r\boldsymbol e_r.$$

所以非主元列里的数，就是它用主元列表示的系数，这些关系原样搬回原来的列。

为什么不能做列变换？列变换把列本身换掉了。对⑤ 做「第 2 列减去第 1 列的 2 倍」，第 2 列成了零向量，可原来的 $\boldsymbol a_2$ 并不是零向量。用式子说，列变换是右乘可逆矩阵 $Q$，$AQ\boldsymbol y=\boldsymbol 0$ 说的是 $A(Q\boldsymbol y)=\boldsymbol 0$，系数被 $Q$ 搅在了一起。

**方法 5（行变换找极大无关组）**

1. 把向量排成列，只用初等行变换化成行最简形。
2. 主元所在的列，对应的**原向量**是一个极大无关组；主元个数是秩。
3. 非主元列里的数，就是对应的原向量用极大无关组表示时的系数。
4. 全程不做列变换。
5. 含参数时，含参数的数要当主元，先问它是否为 0：为 0 时主元变少，秩和极大无关组都跟着变，要分情况写。

**例 6**　求向量组 $\boldsymbol\alpha_1=(1,-1,2,4)^{\mathsf T}$，$\boldsymbol\alpha_2=(0,3,1,2)^{\mathsf T}$，$\boldsymbol\alpha_3=(3,0,7,14)^{\mathsf T}$，$\boldsymbol\alpha_4=(1,-2,2,0)^{\mathsf T}$，$\boldsymbol\alpha_5=(2,1,5,10)^{\mathsf T}$ 的秩和一个极大无关组，并把其余向量用它表示。

第一步，用第一行消第一列：第二行加第一行，第三行减第一行的 2 倍，第四行减第一行的 4 倍。

$$\begin{pmatrix}1&0&3&1&2\\-1&3&0&-2&1\\2&1&7&2&5\\4&2&14&0&10\end{pmatrix}\to\begin{pmatrix}1&0&3&1&2\\0&3&3&-1&3\\0&1&1&0&1\\0&2&2&-4&2\end{pmatrix}.$$

第二步，交换第二、三行，让第二列的主元是 1；再用它消去下面两行的第二列（第三行减它的 3 倍，第四行减它的 2 倍）。

$$\to\begin{pmatrix}1&0&3&1&2\\0&1&1&0&1\\0&0&0&-1&0\\0&0&0&-4&0\end{pmatrix}.$$

第三步，第四行减去第三行的 4 倍成为零行；第三行乘 $-1$；第一行减去新第三行，消掉第四列的 1。

$$\to\begin{pmatrix}1&0&3&0&2\\0&1&1&0&1\\0&0&0&1&0\\0&0&0&0&0\end{pmatrix}.$$

主元在第 1、2、4 列，所以秩是 3，$\boldsymbol\alpha_1,\boldsymbol\alpha_2,\boldsymbol\alpha_4$ 是一个极大无关组。第 3 列是 $(3,1,0,0)^{\mathsf T}$，第 5 列是 $(2,1,0,0)^{\mathsf T}$，所以

$$\boldsymbol\alpha_3=3\boldsymbol\alpha_1+\boldsymbol\alpha_2,\qquad\boldsymbol\alpha_5=2\boldsymbol\alpha_1+\boldsymbol\alpha_2.$$

> 求 $\boldsymbol\alpha_1=(1,2,1,3)^{\mathsf T}$，$\boldsymbol\alpha_2=(2,4,2,6)^{\mathsf T}$，$\boldsymbol\alpha_3=(1,1,0,1)^{\mathsf T}$，$\boldsymbol\alpha_4=(3,5,2,7)^{\mathsf T}$，$\boldsymbol\alpha_5=(0,1,2,1)^{\mathsf T}$ 的秩和一个极大无关组，并表示其余向量。
>
> 答案：主元在第 1、3、5 列，秩为 3，极大无关组是 $\boldsymbol\alpha_1,\boldsymbol\alpha_3,\boldsymbol\alpha_5$；$\boldsymbol\alpha_2=2\boldsymbol\alpha_1$，$\boldsymbol\alpha_4=2\boldsymbol\alpha_1+\boldsymbol\alpha_3$。

合上书，说明为什么行变换不改变列之间的线性关系，以及为什么极大无关组的个数与挑法无关。

### 5. 一个矩阵的秩到底是什么？

一个 $m\times n$ 矩阵 $A$ 有两组向量：$n$ 个列和 $m$ 个行。列向量组的秩叫**列秩**，行向量组的秩叫**行秩**。

还是看三阶压扁⑤。上一节算出它的列秩是 2。它的第三行 $(3,6,4)$ 等于前两行之和，前两行不成比例，所以行秩也是 2。列和行是两组毫不相干的向量，两个秩却总是相等。

#### 行秩等于列秩

思路：两个数都等于阶梯形的主元个数。

第一步，列秩等于主元个数。这是上一节的方法 5：行变换不改变列之间的关系，主元列构成极大无关组。

第二步，行变换不改变行秩。变换后的每一行都是原来各行的组合；三种行变换都能撤销，所以原来的每一行也是变换后各行的组合。两组行向量等价，由第 4 节，秩相等。

第三步，阶梯形的非零行线性无关。设它们的组合等于零。看第一行主元所在的列：下面各行在这一列都是 0，所以第一行的系数乘主元等于 0，系数为 0。再看第二行主元所在的列，第二行的系数也为 0。依次下去，系数全为 0。

把三步连起来：

$$\text{行秩}=\text{阶梯形的非零行数}=\text{主元个数}=\text{列秩}.$$

这个公共的数叫矩阵的**秩**，记作 $r(A)$。

#### 秩就是压扁后还剩几维

由 L.3.1，$A\boldsymbol x$ 是 $A$ 的列的组合，所以变换 $A$ 把整个空间送进列的张成。列秩是 $r$，这个张成就由 $r$ 个互不多余的方向撑起：$r=1$ 是直线，$r=2$ 是平面。这里的「几维」先按 L.1.3 的直观理解（直线 1 维、平面 2 维），定义见 L.8.2。所以**秩就是变换之后还剩几维**。

拿老朋友试一试：①②③ 两列不共线，秩 2，平面还是平面；投影④ 秩 1，平面压成直线；零矩阵秩 0。三阶的⑤ 秩 2，把空间压成平面 $z=x+y$；⑥ 行列式为 4，秩 3。

![单位正方形在三个矩阵下的像：对称伸缩①下是平行四边形（还剩 2 维，秩 2），投影④下是直线 $y=x$ 上的线段（秩 1），零矩阵下是原点（秩 0）](fig/L7-n4.pdf){width=85%}

#### 第三种说法：子式

弗罗贝尼乌斯当年的定义用的是行列式。在 $A$ 中任取 $k$ 行、$k$ 列，交叉处的元素按原来的顺序组成的 $k$ 阶行列式，叫 $A$ 的一个 **$k$ 阶子式**。

先在⑤ 上看。它的三阶子式只有一个，就是 $|A|=0$。取第 1、2 行与第 1、3 列，二阶子式 $\begin{vmatrix}1&1\\2&3\end{vmatrix}=1\ne0$。不为零的子式最高是 2 阶，正好等于秩。

**结论**　若 $A\ne O$，则 $r(A)$ 等于 $A$ 中不为零子式的最高阶数。

证明分两半，设 $r(A)=r\ge1$。

一方面，存在不为零的 $r$ 阶子式。分三步找出它：

- 先挑列：原矩阵 $A$ 中主元所在的 $r$ 列（原来的列）线性无关（第 4 节），组成一个 $m\times r$ 子矩阵 $S$，列秩为 $r$。
- 再挑行：对 $S$ 用「行秩 = 列秩」，$S$ 的行秩也是 $r$，能挑出 $r$ 个无关的行。
- 这 $r$ 行组成 $r$ 阶方阵，行秩为 $r$，再用一次「行秩 = 列秩」，列也无关，由方法 1 第 4 步，行列式非零。

另一方面，不为零的子式不超过 $r$ 阶。若有一个 $k$ 阶子式不为 0，由方法 1 第 4 步，组成它的 $k$ 个短列（每列只有 $k$ 个分量）线性无关。给这些短列添回其余各行的分量，就是 $A$ 的 $k$ 列，由第 2 节性质 (2) 仍无关，所以 $k\le$ 列秩 $=r$。

$A=O$ 时没有不为零的子式，按约定 $r(O)=0$。

注意是「最高阶」：$r(A)=r$ 不意味着每个 $r$ 阶子式都不为零。⑤ 左上角的二阶子式 $\begin{vmatrix}1&2\\2&4\end{vmatrix}=0$，秩照样是 2。

#### 基本事实

把秩的基本事实列在一起：

- $0\le r(A)\le\min\{m,n\}$，且 $r(A)=0\iff A=O$；
- $r(A^{\mathsf T})=r(A)$，因为转置把行秩和列秩对调；
- 初等行变换、初等列变换都不改变秩（列变换就是对 $A^{\mathsf T}$ 做行变换）；
- 对 $n$ 阶方阵，$r(A)=n$ 叫**满秩**；由子式的说法，满秩 $\iff|A|\ne0\iff A$ 可逆。

#### 怎样求秩

**方法 6（求矩阵的秩）**

1. 数字矩阵：化成阶梯形，数非零行。
2. 含参数的方阵：先算行列式，行列式不为零的参数值下满秩；再把使行列式为零的值逐个代回，化阶梯形。
3. 要说明「秩至少是 $k$」，找一个不为零的 $k$ 阶子式最快。

**例 7**　求 $A=\begin{pmatrix}1&2&0&3\\2&4&1&7\\1&2&1&4\end{pmatrix}$ 的秩。

第二行减去第一行的 2 倍，第三行减去第一行，两行都成为 $(0,0,1,1)$；第三行再减去第二行，成为零行：

$$A\to\begin{pmatrix}1&2&0&3\\0&0&1&1\\0&0&1&1\end{pmatrix}\to\begin{pmatrix}1&2&0&3\\0&0&1&1\\0&0&0&0\end{pmatrix}.$$

非零行有 2 行，$r(A)=2$。

用子式核对：第 1、2 行与第 1、3 列交叉处的二阶子式 $\begin{vmatrix}1&0\\2&1\end{vmatrix}=1\ne0$，所以秩至少是 2。

> 求 $\begin{pmatrix}1&-1&2\\2&-2&4\\3&0&1\end{pmatrix}$ 的秩。
>
> 答案：第二行是第一行的 2 倍，消去后剩两行 $(1,-1,2)$、$(0,3,-5)$，秩为 2。也可以看子式：行列式为 0（两行成比例），而二阶子式 $\begin{vmatrix}1&-1\\3&0\end{vmatrix}=3\ne0$。

**例 8**　讨论 $A=\begin{pmatrix}a&1&1\\1&a&1\\1&1&a\end{pmatrix}$ 的秩随 $a$ 的变化。

和例 7 不同，这次有参数。$A$ 是方阵，按方法 6 第 2 步先算行列式，把要单独讨论的参数值一次找全。

第一步，各行元素之和都是 $a+2$（L.6.7），把第二、三列加到第一列，提出公因子，再让第二、三行减去第一行：

$$|A|=(a+2)\begin{vmatrix}1&1&1\\1&a&1\\1&1&a\end{vmatrix}=(a+2)\begin{vmatrix}1&1&1\\0&a-1&0\\0&0&a-1\end{vmatrix}=(a+2)(a-1)^2.$$

第二步，$a\ne1$ 且 $a\ne-2$ 时 $|A|\ne0$，$r(A)=3$。

第三步，逐个代回。$a=1$ 时三行都是 $(1,1,1)$，$r(A)=1$。$a=-2$ 时 $|A|=0$，秩小于 3；而左上角二阶子式 $\begin{vmatrix}-2&1\\1&-2\end{vmatrix}=3\ne0$，所以 $r(A)=2$。

如果一上来就消元，会遇到用 $a-1$ 作除数，每次都要分情况（方法 5 第 5 步）；先算行列式，要单独讨论的值一次找全。

合上书，说明行秩为什么等于列秩，以及秩为什么等于不为零的子式的最高阶数。

### 6. 只看秩的话，两个矩阵能有多「一样」？

行、列变换一起用，能把矩阵化到多简单？做法分三步：行变换化成行最简形；用每个主元 1 做列的倍加，消去它所在行的其余元素（非主元列于是成为零列）；交换列，把主元挪到左上角。以例 7 的 $A$ 为例：

$$A\to\begin{pmatrix}1&2&0&3\\0&0&1&1\\0&0&0&0\end{pmatrix}\to\begin{pmatrix}1&0&0&0\\0&0&1&0\\0&0&0&0\end{pmatrix}\to\begin{pmatrix}1&0&0&0\\0&1&0&0\\0&0&0&0\end{pmatrix}.$$

一般地，任何秩为 $r$ 的 $m\times n$ 矩阵都能这样化成

$$F=\begin{pmatrix}E_r&O\\O&O\end{pmatrix},$$

叫 $A$ 的**等价标准形**。行变换是左乘可逆矩阵，列变换是右乘可逆矩阵（L.4.4），所以存在可逆矩阵 $P,Q$ 使 $PAQ=F$。

$A$ 经过有限次初等行、列变换变成 $B$（即存在可逆的 $P,Q$ 使 $B=PAQ$），称 $A$ 与 $B$ **等价**。

**结论**　同型矩阵等价 $\iff$ 秩相等。

一个方向：初等变换不改变秩。另一个方向：秩相等的两个矩阵能化成同一个 $F$，每一步都能撤销，于是从 $A$ 化到 $F$，再倒着走回 $B$。所以秩相等是同型矩阵等价的充要条件。

这里有一对容易混的概念。矩阵等价只看秩：同型且秩相等就等价。向量组等价却不只看秩：$\{(1,0)^{\mathsf T}\}$ 与 $\{(0,1)^{\mathsf T}\}$ 的秩都是 1，但谁也表示不了谁，不等价。向量组等价能推出秩相等，反过来不行。

**方法 7（等价标准形）**

1. 先求秩 $r$。
2. 标准形就是左上角为 $E_r$、其余为 0 的同型矩阵。
3. 判断同型矩阵是否等价，只比较秩。

> 说明 $\begin{pmatrix}1&2\\2&4\end{pmatrix}$ 与 $\begin{pmatrix}0&3\\0&0\end{pmatrix}$ 等价，写出它们共同的等价标准形。
>
> 答案：两者的秩都是 1，所以等价，标准形是 $\begin{pmatrix}1&0\\0&0\end{pmatrix}$。

合上书，说明为什么秩相等的两个同型矩阵一定等价。

### 7. 矩阵相乘、相加以后，秩最多是多少？

#### 乘积的秩

设 $A$ 是 $m\times n$ 矩阵，$B$ 是 $n\times p$ 矩阵。

按列看：由 L.3.7，$AB=(A\boldsymbol b_1,\dots,A\boldsymbol b_p)$，每一列 $A\boldsymbol b_j$ 都是 $A$ 的列的组合。所以 $AB$ 的列向量组能由 $A$ 的列向量组表示，由第 4 节的比较性质，$r(AB)\le r(A)$。

按行看：$AB$ 的每一行是 $B$ 的各行的组合，同理 $r(AB)\le r(B)$。

合起来：

$$r(AB)\le\min\{r(A),r(B)\}.$$

用变换的话说，变换只会把方向压掉，不会凭空造出新方向，接连做两次，剩下的维数只减不增。

等号不一定成立。先投影到直线 $y=-x$ 上，再投影到 $y=x$ 上，乘积 $\frac12\begin{pmatrix}1&1\\1&1\end{pmatrix}\cdot\frac12\begin{pmatrix}1&-1\\-1&1\end{pmatrix}$ 是零矩阵：两个因子的秩都是 1，第一步留下的直线恰好被第二步压到原点。这种情形 L.9.5 还会再讲。

#### 可逆因子和相加

乘可逆矩阵不改变秩：$P$ 可逆时，$r(PA)\le r(A)$；又 $A=P^{-1}(PA)$，所以 $r(A)\le r(PA)$。右乘同理。

和的秩：设 $A,B$ 同型。$A+B$ 的第 $j$ 列是 $\boldsymbol a_j+\boldsymbol b_j$，能由 $A$、$B$ 的全部列合在一起表示；这些列又能由两个极大无关组合起来表示，一共最多 $r(A)+r(B)$ 个向量。所以

$$r(A+B)\le r(A)+r(B).$$

常用的特例是外积：$\boldsymbol u,\boldsymbol v$ 是非零列向量时，$\boldsymbol u\boldsymbol v^{\mathsf T}$ 的第 $j$ 列是 $v_j\boldsymbol u$，每一列都是 $\boldsymbol u$ 的倍数，而 $\boldsymbol v$ 有非零分量，所以它不是零矩阵，秩恰好是 1。两个这样的矩阵相加，秩不超过 2。

**方法 8（秩的不等式）**

1. 乘积的秩不超过每个因子的秩。
2. 乘可逆矩阵秩不变：求乘积的秩时，先看有没有可逆因子可以直接去掉。
3. 和的秩不超过秩的和；外积 $\boldsymbol u\boldsymbol v^{\mathsf T}$（$\boldsymbol u,\boldsymbol v\ne\boldsymbol 0$）的秩是 1。

**例 9**　$A$ 是 $4\times3$ 矩阵，$r(A)=2$，$B=\begin{pmatrix}1&0&1\\0&2&0\\-1&0&3\end{pmatrix}$，求 $r(AB)$。

不知道 $A$ 的元素，只能借不等式。先看 $B$ 是否可逆，按第一行展开：

$$|B|=1\cdot(6-0)-0+1\cdot(0+2)=8\ne0.$$

$B$ 可逆，右乘可逆矩阵不改变秩，所以 $r(AB)=r(A)=2$。如果 $B$ 不可逆，就只能得到 $r(AB)\le\min\{2,r(B)\}$。

> $A$ 是 $3\times4$ 矩阵，$r(A)=2$，$C=\begin{pmatrix}1&1&0\\0&1&1\\0&0&1\end{pmatrix}$，求 $r(CA)$。
>
> 答案：$C$ 是上三角矩阵，$|C|=1\ne0$，可逆；左乘可逆矩阵不改变秩，$r(CA)=2$。

最后看一个 AI 里真实的例子。大模型里有大量「线性层」，做的就是矩阵乘向量 $W\boldsymbol x$，$W$ 是 $d\times d$ 矩阵，它的 $d^2$ 个元素叫**参数**，是训练出来的。让训练好的模型适应新任务（**微调**），就是把 $W$ 改成 $W+\Delta W$。$d$ 常有几千，$\Delta W$ 有上千万个数要学。

2021 年胡等人提出的 LoRA（低秩适配）规定，改动量必须写成乘积

$$\Delta W=BA,\qquad B\ \text{是}\ d\times \ell\ \text{矩阵},\quad A\ \text{是}\ \ell\times d\ \text{矩阵},$$

$\ell$ 远小于 $d$（用 $\ell$ 免得和秩 $r(\cdot)$ 混淆），只需学 $B$ 和 $A$ 的 $2d\ell$ 个数。

**例 10**　(1) 说明 LoRA 的改动量满足 $r(\Delta W)\le\ell$；(2) 取 $d=4$，$\ell=2$，$B=\begin{pmatrix}1&0\\0&1\\1&1\\2&-1\end{pmatrix}$，$A=\begin{pmatrix}1&0&2&0\\0&1&0&-1\end{pmatrix}$，算出 $\Delta W$ 并求它的秩；(3) 对 $d=4096$、$\ell=8$，比较 LoRA 要学的参数个数和 $d^2$。

(1) 由乘积的秩不等式，$r(\Delta W)\le\min\{r(B),r(A)\}$。$B$ 只有 $\ell$ 列，$r(B)\le\ell$，所以 $r(\Delta W)\le\ell$。

(2) $\Delta W$ 的第 $i$ 行，是以 $B$ 的第 $i$ 行为系数、$A$ 的两行的组合。记 $A$ 的两行为 $\boldsymbol p=(1,0,2,0)$、$\boldsymbol q=(0,1,0,-1)$，四行依次是 $\boldsymbol p$、$\boldsymbol q$、$\boldsymbol p+\boldsymbol q$、$2\boldsymbol p-\boldsymbol q$：

$$\Delta W=\begin{pmatrix}1&0&2&0\\0&1&0&-1\\1&1&2&-1\\2&-1&4&1\end{pmatrix}.$$

后两行能由前两行表示，前两行不成比例，所以 $r(\Delta W)=2$，恰好达到上界。

(3) LoRA 要学 $2d\ell=2\times4096\times8=65536$ 个数，而 $d^2=16777216$，只有它的 $\frac1{256}$。

这样限制仍然管用，依据是实验观察：微调所需的改动大致集中在少数几个方向上。「集中在 $\ell$ 个方向上」是说 $\Delta W$ 的各列都落在 $\ell$ 个向量张成的子空间里，即列秩不超过 $\ell$，这正是 $BA$ 的样子（$B$ 的 $\ell$ 列就是这些方向）。怎样用更少的方向近似一个矩阵，留到 L.15。

合上书，按列、按行各说一遍 $r(AB)\le\min\{r(A),r(B)\}$ 的理由，再举一个等号不成立的例子。

### 本章小结

| 方法 | 什么时候用 | 对应题号 |
|---|---|---|
| 方法 1（排成列，数主元） | 给出分量的向量组判相关、找相关关系 | L7-01、L7-17 |
| 方法 2（定义法证无关） | 由已知无关组构造的新向量组；证明题 | L7-05、L7-14 |
| 方法 3（用性质推相关性） | 部分与整体、添分量、唯一表示等抽象判断 | L7-03 |
| 方法 4（$B=AK$，看 $K$） | 新向量组由无关组表示，判断相关性或求参数 | L7-06、L7-14 |
| 方法 5（行变换找极大无关组） | 求向量组的秩、极大无关组，并表示其余向量 | L7-07、L7-08、L7-11 |
| 方法 6（求矩阵的秩） | 数字矩阵、含参数方阵、子式估下界 | L7-02、L7-09、L7-11、L7-12、L7-15 |
| 方法 7（等价标准形） | 写标准形，判断两个矩阵是否等价 | L7-10 |
| 方法 8（秩的不等式） | 乘积与和的秩、可逆因子、外积 | L7-04、L7-12、L7-13、L7-16 |

**可逆大定理**（$n$ 阶方阵 $A$，下面各条互相等价）：

- 消元后有 $n$ 个主元；$A\boldsymbol x=\boldsymbol b$ 对每个 $\boldsymbol b$ 都有唯一解；$A\boldsymbol x=\boldsymbol 0$ 只有零解（L.4）；
- $A$ 可逆；存在 $B$ 使 $AB=E$（L.5）；
- $|A|\ne0$（L.6）；
- $A$ 的列向量组线性无关，行向量组线性无关（本章新增）；
- $r(A)=n$（本章新增）。

**秩的几种说法**：$r(A)=$ 主元个数 $=$ 列秩 $=$ 行秩 $=$ 不为零子式的最高阶数。
