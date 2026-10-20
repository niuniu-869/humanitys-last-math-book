## L.8 · 向量空间

手机照片的每个像素记着三个数：红、绿、蓝三种光各有多亮。JPEG 保存照片时，通常先用一个线性变换把这三个数换成另外三个数：一个亮度，两个色差（颜色偏离灰色的程度）。像素还是那个像素，只是换了一套坐标来记。人眼对亮度的细节敏感、对色差的细节迟钝，所以换过以后，色差可以存得粗一些，文件小了许多，肉眼却看不出差别。

同一个对象换一组基来描述，是本章的主题之一。抓住一个画面：**基就是一把尺子，坐标是用这把尺子量出的读数；换基就是换一把尺子量同一个箭头。**

「向量空间」这个说法来自一次统一。格拉斯曼 1844 年的书（L.1）写法抽象，早期很少有人读懂；后来，数学家在别处一再碰到同样的结构：两个次数不超过 2 的多项式相加、乘一个数，还是这样的多项式，同型矩阵也一样。1888 年皮亚诺把这些对象共同遵守的运算规则列成一组公理，通常被看作现代定义的起点：满足公理的集合都叫线性空间，从公理推出的结论对它们都成立。统一之后紧接着一个问题：描述同一个平面的向量组可多可少，「维数」以哪一组为准？L.7 的替换定理正好能回答。

本章第 1 节说清什么样的一堆向量算一个「空间」；第 2 节用最少的向量描述它，得到基和维数；第 3 节看换基时坐标怎样变；第 4 节数出 $A\boldsymbol{x}=\boldsymbol{0}$ 的解有几个自由度；第 5 节看一个矩阵自带的四个空间怎样互相垂直；第 6、7 节是支线，把这套语言搬到多项式和矩阵上，并给抽象的线性变换配上矩阵。

### 1. 什么样的一堆向量可以叫作一个「空间」？

前面遇到过好几种向量的集合：L.1 例 3 的张成是平面 $z=x+y$；齐次方程组的解有时是一条直线（L.4）；超平面 $\boldsymbol{a}^{\mathsf T}\boldsymbol{x}=c$ 在 $c\ne0$ 时不过原点（L.2.4）。哪些集合可以像整个 $\mathbb{R}^n$ 那样放心地做加法和数乘，不会「出界」？

拿平面 $z=x+y$ 试一试。在上面任取两点，坐标满足 $z_1=x_1+y_1$、$z_2=x_2+y_2$。两式相加得

$$z_1+z_2=(x_1+x_2)+(y_1+y_2),$$

所以两点之和仍在平面上；第一式两边乘 $k$，可知 $k$ 倍也在平面上。

再看平行的平面 $z=x+y+1$。点 $(0,0,1)^{\mathsf T}$ 在上面，它的 2 倍 $(0,0,2)^{\mathsf T}$ 却不满足 $2=0+0+1$，出界了。毛病出在常数 1 跟着翻了倍（图 L8-n3）。

![实线箭头 $(0,0,1)^{\mathsf T}$ 的终点在上面的平面 $z=x+y+1$ 上，它的 2 倍（虚线箭头）冲出了这张平面；下面过原点的平面 $z=x+y$ 对加法和数乘都不出界](fig/L8-n3.pdf){width=58%}

一般地，设 $V$ 是 $\mathbb{R}^n$ 的一个非空子集。如果

- $V$ 中任意两个向量的和仍在 $V$ 中，
- $V$ 中任意向量的任意实数倍也仍在 $V$ 中，

就说 $V$ **对加法和数乘封闭**，称 $V$ 是 $\mathbb{R}^n$ 的一个**子空间**。两条合起来，就是 $V$ 中向量的任何线性组合仍在 $V$ 中。

任取 $\boldsymbol{v}\in V$ 乘以 0，得 $\boldsymbol{0}\in V$，所以子空间一定含零向量。平面 $z=x+y+1$ 不含原点，一眼就能排除。$\{\boldsymbol{0}\}$ 和 $\mathbb{R}^n$ 是两个极端的子空间。

#### 三类以后天天用的子空间

第一类是张成。$\operatorname{span}(\boldsymbol{a}_1,\dots,\boldsymbol{a}_k)$ 中两个向量 $\sum c_i\boldsymbol{a}_i$ 与 $\sum d_i\boldsymbol{a}_i$ 的和是 $\sum(c_i+d_i)\boldsymbol{a}_i$，$k$ 倍是 $\sum(kc_i)\boldsymbol{a}_i$，仍是这组向量的线性组合。

第二类是矩阵的**列空间**：$m\times n$ 矩阵 $A$ 的各列张成的子空间，记作 $C(A)$，在 $\mathbb{R}^m$ 中。由 L.3.1，$A\boldsymbol{x}$ 是以 $\boldsymbol{x}$ 的分量为系数的各列的组合，所以

$$C(A)=\{A\boldsymbol{x}:\boldsymbol{x}\in\mathbb{R}^n\}.$$

用变换的话说，列空间就是变换 $A$ 的「像」：所有向量被 $A$ 送到的地方。$A\boldsymbol{x}=\boldsymbol{b}$ 有解，就是 $\boldsymbol{b}$ 落在像里。

第三类是**零空间** $N(A)=\{\boldsymbol{x}\in\mathbb{R}^n:A\boldsymbol{x}=\boldsymbol{0}\}$，即齐次方程组的全部解，也就是被 $A$ 压到原点的那些方向。若 $A\boldsymbol{x}=A\boldsymbol{y}=\boldsymbol{0}$，由分配律

$$A(\boldsymbol{x}+\boldsymbol{y})=A\boldsymbol{x}+A\boldsymbol{y}=\boldsymbol{0},\qquad A(k\boldsymbol{x})=kA\boldsymbol{x}=\boldsymbol{0}.$$

拿投影④ $\frac12\begin{pmatrix}1&1\\1&1\end{pmatrix}$ 试一试：它的像是直线 $y=x$，零空间是 $(1,-1)^{\mathsf T}$ 方向的直线（L.7 图 L7-n1），两个都过原点。

反过来，$\boldsymbol{b}\ne\boldsymbol{0}$ 时 $A\boldsymbol{x}=\boldsymbol{b}$ 的解集不是子空间：$A\boldsymbol{0}=\boldsymbol{0}\ne\boldsymbol{b}$，零向量不是解。这和平面 $z=x+y+1$ 是同一件事，它的样子留到 L.9.3 再看。

不妨把子空间想成「过原点的、平直的集合」：过原点对应含零向量，平直对应对线性组合封闭。在 $\mathbb{R}^3$ 里，它们就是原点、过原点的直线、过原点的平面和整个空间（下一节说明为什么只有这几种）。这个画面有两处不灵：$n\ge4$ 时画不出来，仍要回到封闭性；两张过原点的平面合在一起（例如坐标平面 $x_1=0$ 与 $x_2=0$ 的并）也像「平直」的，却不是子空间，下面例 1 的 (4) 会验证。

**方法 1（判断子空间）**

1. 先看零向量在不在集合里，不在就不是子空间。
2. 能写成某组向量的张成或某个矩阵的零空间，就直接断定是。
3. 否则任取集合里的两个向量和一个实数，验证和与倍数仍满足集合的条件。
4. 要否定，举出一组具体的向量，说明它们的和或倍数出界。

**例 1**　判断 $\mathbb{R}^3$ 的下列子集是不是子空间：(1) $V_1=\{\boldsymbol{x}:x_1-2x_2+x_3=0\}$；(2) $V_2=\{\boldsymbol{x}:x_1=x_2=x_3\}$；(3) $V_3=\{\boldsymbol{x}:x_1+x_2+x_3=1\}$；(4) $V_4=\{\boldsymbol{x}:x_1x_2=0\}$。

(1) 是，$V_1$ 就是 $1\times3$ 矩阵 $(1,-2,1)$ 的零空间。

(2) 是，满足条件的向量都是 $t(1,1,1)^{\mathsf T}$，$V_2$ 是 $(1,1,1)^{\mathsf T}$ 张成的直线。

(3) 不是，零向量不满足 $x_1+x_2+x_3=1$。

(4) 零向量在里面，要找反例。$(1,0,0)^{\mathsf T}$ 和 $(0,1,0)^{\mathsf T}$ 都满足 $x_1x_2=0$，它们的和 $(1,1,0)^{\mathsf T}$ 却有 $1\times1\ne0$，所以不是子空间。$V_4$ 是两张坐标平面 $x_1=0$ 与 $x_2=0$ 的并，对数乘封闭，对加法不封闭。两个子空间的并集一般不是子空间。

为什么 (4) 不能靠验证几个向量就说「是」？因为封闭性要求对任意两个向量成立，验证再多也只是特例；否定却只需要一个反例。

> 判断 $W_1=\{\boldsymbol{x}\in\mathbb{R}^3:x_1+x_2=0,\ x_3=2x_1\}$ 与 $W_2=\{\boldsymbol{x}\in\mathbb{R}^3:x_1^2=x_2^2\}$ 是不是子空间。
>
> 答案：$W_1$ 是，它是 $\begin{pmatrix}1&1&0\\2&0&-1\end{pmatrix}$ 的零空间。$W_2$ 不是：$(1,1,0)^{\mathsf T}$ 和 $(1,-1,0)^{\mathsf T}$ 都在里面，和 $(2,0,0)^{\mathsf T}$ 却有 $4\ne0$。

合上书，说出子空间为什么一定含零向量，再说明 $A\boldsymbol{x}=\boldsymbol{0}$ 的解集为什么是子空间、$A\boldsymbol{x}=\boldsymbol{b}\ (\boldsymbol{b}\ne\boldsymbol{0})$ 的解集为什么不是。

### 2. 描述一个空间最少需要几个向量？

平面 $z=x+y$ 可以说成 $\operatorname{span}(\boldsymbol{a}_1,\boldsymbol{a}_2)$，也可以说成 $\operatorname{span}(\boldsymbol{a}_1,\boldsymbol{a}_2,\boldsymbol{a}_1+\boldsymbol{a}_2)$，后者多一个向量，却没多张成任何东西（L.1.3）。描述一个子空间，自然想用一组既不多余、又够用的向量。

设 $V$ 是子空间。如果 $V$ 中的向量 $\boldsymbol{\alpha}_1,\dots,\boldsymbol{\alpha}_r$ 线性无关，并且张成 $V$，就称它们是 $V$ 的一组**基**。张成 $V$ 保证够用；线性无关保证不多余（L.7.1）。

两条合起来还给出表示的唯一性。若 $\boldsymbol{v}=\sum c_i\boldsymbol{\alpha}_i=\sum d_i\boldsymbol{\alpha}_i$，移项得 $\sum(c_i-d_i)\boldsymbol{\alpha}_i=\boldsymbol{0}$，由无关得每个 $c_i=d_i$。

#### 维数与基的选法无关

同一个子空间有许多组基。要用基里向量的个数来定义维数，先得说明不同的基个数相同。

设 $\boldsymbol{\alpha}_1,\dots,\boldsymbol{\alpha}_s$ 与 $\boldsymbol{\beta}_1,\dots,\boldsymbol{\beta}_t$ 都是 $V$ 的基。$\boldsymbol{\beta}$ 组在 $V$ 里，能由张成 $V$ 的 $\boldsymbol{\alpha}$ 组表示。若 $t>s$，由替换定理（L.7.3，以少表多，多的必相关），$\boldsymbol{\beta}$ 组相关，与它是基矛盾，所以 $t\le s$。

两组的地位是对称的：$\boldsymbol{\alpha}$ 组也能由 $\boldsymbol{\beta}$ 组表示，同样的理由给出 $s\le t$。所以 $s=t$。

这个公共的个数叫 $V$ 的**维数**，记作 $\dim V$，并规定 $\dim\{\boldsymbol{0}\}=0$。$\boldsymbol{e}_1,\dots,\boldsymbol{e}_n$ 无关且张成 $\mathbb{R}^n$，所以 $\dim\mathbb{R}^n=n$。

维数就是自由度：在 $V$ 里定位一个向量，恰好要 $\dim V$ 个数。平面 $z=x+y$ 上的点由 $x,y$ 两个数定下，$z$ 随之确定，所以它是 2 维的。

#### 三条常用的事实

设 $\dim V=d$。替换定理还给出三条事实，后面比较维数时要连着用，一条一条看。

第一条，$V$ 中任意 $d+1$ 个向量必相关。因为它们能由一组基（$d$ 个向量）表示，以少表多。

第二条，$V$ 中任意 $d$ 个无关的向量都是基。用反证法：若有 $\boldsymbol{v}\in V$ 不能由它们表示，把 $\boldsymbol{v}$ 添进去仍然无关（L.7.2 的性质 (4)：添进去若相关，$\boldsymbol v$ 就能被表示），$V$ 里就有了 $d+1$ 个无关向量，与第一条矛盾。

第三条，$V$ 中任一无关组都能扩充成基。个数不到 $d$ 时它张不满 $V$（否则它就是一组基，个数却不是 $d$），就在 $V$ 里取一个不能由它表示的向量添进去，仍然无关；一次添一个，添到 $d$ 个为止。

由第二条还得到：若子空间 $W\subseteq V$ 且 $\dim W=\dim V$，则 $W$ 的一组基是 $V$ 里 $d$ 个无关的向量，也就是 $V$ 的基，所以 $W=V$。

L.1.3 留下的问题在这里有了答案：$\mathbb{R}^3$ 的子空间维数只能是 0、1、2、3，依次是原点、过原点的直线、过原点的平面和 $\mathbb{R}^3$ 本身。

子空间由一组向量张成时，L.7.4 的极大无关组就是它的基，所以

$$\dim\operatorname{span}(\boldsymbol{a}_1,\dots,\boldsymbol{a}_k)=r(\boldsymbol{a}_1,\dots,\boldsymbol{a}_k).$$

**方法 2（求张成的基与维数）**

1. 把向量作为列排成矩阵，只用初等行变换化成阶梯形。
2. 主元列对应的**原来的**向量组成一组基，主元个数就是维数（L.7.4）。
3. 要扩充成 $\mathbb{R}^n$ 的基，就添入不在这个子空间里的向量，添到 $n$ 个，用行列式不为零检验。

**例 2**　设 $\boldsymbol{\alpha}_1=(1,1,0,2)^{\mathsf T}$，$\boldsymbol{\alpha}_2=(2,1,1,3)^{\mathsf T}$，$\boldsymbol{\alpha}_3=(0,1,-1,1)^{\mathsf T}$，$\boldsymbol{\alpha}_4=(1,0,1,2)^{\mathsf T}$，$V=\operatorname{span}(\boldsymbol{\alpha}_1,\dots,\boldsymbol{\alpha}_4)$。(1) 求 $V$ 的一组基和维数；(2) 把这组基扩充成 $\mathbb{R}^4$ 的基。

(1) 以四个向量为列。第一步，第 2 行减第 1 行，第 4 行减第 1 行的 2 倍：

$$\begin{pmatrix}1&2&0&1\\1&1&1&0\\0&1&-1&1\\2&3&1&2\end{pmatrix}\to\begin{pmatrix}1&2&0&1\\0&-1&1&-1\\0&1&-1&1\\0&-1&1&0\end{pmatrix}.$$

第二步，第 3 行加第 2 行，第 4 行减第 2 行，再交换后两行：

$$\to\begin{pmatrix}1&2&0&1\\0&-1&1&-1\\0&0&0&1\\0&0&0&0\end{pmatrix}.$$

主元在第 1、2、4 列，所以 $\boldsymbol{\alpha}_1,\boldsymbol{\alpha}_2,\boldsymbol{\alpha}_4$ 是一组基，$\dim V=3$。第 3 列没有主元，$\boldsymbol{\alpha}_3$ 多余（化成行最简形可读出 $\boldsymbol{\alpha}_3=2\boldsymbol{\alpha}_1-\boldsymbol{\alpha}_2$）。

(2) 还差一个向量。$\boldsymbol{e}_4$ 不行，它在 $V$ 里：$\boldsymbol{\alpha}_1-\boldsymbol{\alpha}_2+\boldsymbol{\alpha}_4=\boldsymbol{e}_4$。试 $\boldsymbol{e}_1$，按第 4 列展开：

$$\begin{vmatrix}1&2&1&1\\1&1&0&0\\0&1&1&0\\2&3&2&0\end{vmatrix}=(-1)^{1+4}\begin{vmatrix}1&1&0\\0&1&1\\2&3&2\end{vmatrix}=-1\ne0,$$

所以 $\boldsymbol{\alpha}_1,\boldsymbol{\alpha}_2,\boldsymbol{\alpha}_4,\boldsymbol{e}_1$ 是 $\mathbb{R}^4$ 的基。$\boldsymbol{e}_4$ 的教训是：添向量前要检验它不在原来的张成里。

> 求 $(1,0,1)^{\mathsf T},(0,1,1)^{\mathsf T},(1,1,2)^{\mathsf T},(1,-1,0)^{\mathsf T}$ 张成的子空间的维数和一组基，并扩充成 $\mathbb{R}^3$ 的基。
>
> 答案：主元在前两列，后两个向量是前两个的和与差，维数 2，前两个是一组基，张成的就是平面 $z=x+y$。$\boldsymbol{e}_3$ 不满足 $z=x+y$，添上后行列式为 1，得到 $\mathbb{R}^3$ 的基。

合上书，用替换定理说明同一个子空间的两组基为什么个数相同，再说明 $d$ 维子空间里 $d$ 个无关向量为什么一定是基。

### 3. 换一组基，同一个向量的坐标怎样变？

#### 坐标：用一把尺子量出的读数

照片上相邻两个像素的亮度常常很接近，比如 $\boldsymbol{x}=(200,196)^{\mathsf T}$。换用基 $\boldsymbol{\alpha}_1=(1,1)^{\mathsf T}$、$\boldsymbol{\alpha}_2=(1,-1)^{\mathsf T}$，设 $\boldsymbol{x}=y_1\boldsymbol{\alpha}_1+y_2\boldsymbol{\alpha}_2$，按分量得

$$y_1+y_2=200,\qquad y_1-y_2=196,$$

解得 $y_1=198$、$y_2=2$：平均亮度和半差。相邻像素越接近，半差越小，存的时候可以舍入得更粗。这正是最简单的哈尔（Haar）小波变换的小例子：换一组基，相近的数据就集中到少数几个坐标上。

图 L8-n1 把同一个点放在两张方格纸上读数：箭头没动，换的是尺子。

![同一个点 $(5,3)^{\mathsf T}$ 在标准方格纸上读作 $(5,3)$，在沿 $\boldsymbol{\alpha}_1,\boldsymbol{\alpha}_2$ 画的斜方格纸（虚线）上读作 $(4,1)$，因为 $4\boldsymbol{\alpha}_1+\boldsymbol{\alpha}_2=(5,3)^{\mathsf T}$](fig/L8-n1.pdf){width=60%}

一般地，设 $\boldsymbol{\alpha}_1,\dots,\boldsymbol{\alpha}_n$ 是 $V$ 的一组基。$V$ 中的 $\boldsymbol{v}$ 唯一地写成

$$\boldsymbol{v}=y_1\boldsymbol{\alpha}_1+\cdots+y_n\boldsymbol{\alpha}_n,$$

$\boldsymbol{y}=(y_1,\dots,y_n)^{\mathsf T}$ 叫 $\boldsymbol{v}$ 在这组基下的**坐标**。唯一性保证坐标是确定的。在标准基下，坐标就是分量本身。

为了书写方便，把基向量依次作为列排在一起，记作 $(\boldsymbol{\alpha})=(\boldsymbol{\alpha}_1,\dots,\boldsymbol{\alpha}_n)$。在 $\mathbb{R}^n$ 里它就是一个矩阵，由 L.3.1「矩阵乘向量 = 各列的组合」，上式就是

$$\boldsymbol{v}=(\boldsymbol{\alpha})\boldsymbol{y}.$$

#### 过渡矩阵：两把尺子之间的换算表

现在换基。设旧基是 $(\boldsymbol{\alpha})$，新基是 $(\boldsymbol{\beta})=(\boldsymbol{\beta}_1,\dots,\boldsymbol{\beta}_n)$。把 $\boldsymbol{\beta}_j$ 在旧基下的坐标排成第 $j$ 列，得到 $n$ 阶矩阵 $P$。和 L.7.3 的 $B=AK$ 一样，按列分块，

$$(\boldsymbol{\beta}_1,\dots,\boldsymbol{\beta}_n)=(\boldsymbol{\alpha}_1,\dots,\boldsymbol{\alpha}_n)P,\qquad\text{简写为}\qquad(\boldsymbol{\beta})=(\boldsymbol{\alpha})P.$$

$P$ 叫从旧基到新基的**过渡矩阵**（考研教材的叫法：它把新基写成旧基的组合）。记住它的定义：$P$ 的第 $j$ 列，是第 $j$ 个新基向量用旧尺子量出的读数。

设 $\boldsymbol{v}$ 的旧坐标是 $\boldsymbol{x}$、新坐标是 $\boldsymbol{y}$。把 $(\boldsymbol{\beta})=(\boldsymbol{\alpha})P$ 代进 $\boldsymbol{v}=(\boldsymbol{\beta})\boldsymbol{y}$：

$$\boldsymbol{v}=(\boldsymbol{\beta})\boldsymbol{y}=(\boldsymbol{\alpha})P\boldsymbol{y}.$$

这说明 $P\boldsymbol{y}$ 也是 $\boldsymbol{v}$ 的旧坐标。旧坐标是唯一的，于是得到**坐标变换公式**

$$\boldsymbol{x}=P\boldsymbol{y},\qquad\boldsymbol{y}=P^{-1}\boldsymbol{x}.$$

$P$ 为什么可逆？若 $P\boldsymbol{k}=\boldsymbol{0}$，则 $(\boldsymbol{\beta})\boldsymbol{k}=(\boldsymbol{\alpha})P\boldsymbol{k}=\boldsymbol{0}$，而新基无关，只能 $\boldsymbol{k}=\boldsymbol{0}$，所以 $P$ 可逆（L.5.2）。反过来，$P$ 可逆时 $(\boldsymbol{\alpha})P$ 也是一组基，这正是 L.7.3 的方法 4。

公式里 $P$ 的方向很容易记反。抓住一个画面：$P$ 的每一列是一个新基向量的旧读数，$P\boldsymbol{y}$ 以新坐标为权重把这些列加起来，得到的自然是旧读数。所以 **$P$ 吃进新坐标、吐出旧坐标**。要从旧坐标求新坐标，就解方程组 $P\boldsymbol{y}=\boldsymbol{x}$，不必先求 $P^{-1}$。

把两个式子并排看一次，它们最容易混：

| 式子 | $P$ 乘在哪 | 方向 |
|---|---|---|
| $(\boldsymbol{\beta})=(\boldsymbol{\alpha})P$ | 旧基的右边 | 由旧基算出新基 |
| $\boldsymbol{x}=P\boldsymbol{y}$ | 新坐标的左边 | 由新坐标算出旧坐标 |

从新基到旧基的过渡矩阵则是 $P^{-1}$。

**方法 3（过渡矩阵与坐标变换）**

1. 两组基都给出分量时，以它们为列分别排成矩阵 $A$、$B$。由 $B=AP$ 得 $P=A^{-1}B$，用行变换 $(A\mid B)\to(E\mid P)$ 求出（L.5.4）。
2. 只给出新基用旧基表示的关系时，把 $\boldsymbol{\beta}_j$ 的系数写成 $P$ 的第 $j$ 列。
3. 求新坐标就解 $P\boldsymbol{y}=\boldsymbol{x}$。
4. 判断新的一组向量是不是基，就看 $P$ 是否可逆。

**例 3**　在 $\mathbb{R}^3$ 中，旧基为 $\boldsymbol{\alpha}_1=(1,0,0)^{\mathsf T}$，$\boldsymbol{\alpha}_2=(1,1,0)^{\mathsf T}$，$\boldsymbol{\alpha}_3=(1,1,1)^{\mathsf T}$，新基为 $\boldsymbol{\beta}_1=(2,1,0)^{\mathsf T}$，$\boldsymbol{\beta}_2=(0,1,1)^{\mathsf T}$，$\boldsymbol{\beta}_3=(1,0,1)^{\mathsf T}$。求从旧基到新基的过渡矩阵 $P$。

$A$ 是上三角的，对 $(A\mid B)$ 从下往上消。第一步，第 2 行减第 3 行；第二步，第 1 行减去新的第 2 行和第 3 行：

$$\left(\begin{array}{ccc|ccc}1&1&1&2&0&1\\0&1&1&1&1&0\\0&0&1&0&1&1\end{array}\right)\to\left(\begin{array}{ccc|ccc}1&1&1&2&0&1\\0&1&0&1&0&-1\\0&0&1&0&1&1\end{array}\right)\to\left(\begin{array}{ccc|ccc}1&0&0&1&-1&1\\0&1&0&1&0&-1\\0&0&1&0&1&1\end{array}\right).$$

右半边就是 $P$。验算第 1 列：$\boldsymbol{\alpha}_1+\boldsymbol{\alpha}_2=(2,1,0)^{\mathsf T}=\boldsymbol{\beta}_1$。

> 求从标准基 $\boldsymbol{e}_1,\boldsymbol{e}_2$ 到 $\boldsymbol{\beta}_1=(1,2)^{\mathsf T}$、$\boldsymbol{\beta}_2=(1,3)^{\mathsf T}$ 的过渡矩阵，以及 $(3,7)^{\mathsf T}$ 的新坐标。
>
> 答案：旧基是标准基，$A=E$，$P=B=\begin{pmatrix}1&1\\2&3\end{pmatrix}$。解 $y_1+y_2=3$、$2y_1+3y_2=7$ 得 $y_1=2$、$y_2=1$，即 $(3,7)^{\mathsf T}=2\boldsymbol{\beta}_1+\boldsymbol{\beta}_2$。

**例 4**　设 $\boldsymbol{\alpha}_1,\boldsymbol{\alpha}_2,\boldsymbol{\alpha}_3$ 是 $\mathbb{R}^3$ 的一组基，$\boldsymbol{\beta}_1=\boldsymbol{\alpha}_1+\boldsymbol{\alpha}_2$，$\boldsymbol{\beta}_2=\boldsymbol{\alpha}_2+\boldsymbol{\alpha}_3$，$\boldsymbol{\beta}_3=\boldsymbol{\alpha}_3+\boldsymbol{\alpha}_1$。证明 $\boldsymbol{\beta}_1,\boldsymbol{\beta}_2,\boldsymbol{\beta}_3$ 也是一组基，并求 $\boldsymbol{\xi}=\boldsymbol{\alpha}_1+2\boldsymbol{\alpha}_2+3\boldsymbol{\alpha}_3$ 在新基下的坐标。

和例 3 不同，这里只给关系、不给分量，用方法 3 的第 2 步。三个关系的系数依次写成三列：

$$P=\begin{pmatrix}1&0&1\\1&1&0\\0&1&1\end{pmatrix},\qquad|P|=1\cdot(1-0)-0+1\cdot(1-0)=2\ne0.$$

$P$ 可逆，所以 $\boldsymbol{\beta}$ 组是基（这正是 L.7 例 3）。

$\boldsymbol{\xi}$ 的旧坐标是 $(1,2,3)^{\mathsf T}$，解 $P\boldsymbol{y}=(1,2,3)^{\mathsf T}$：

$$y_1+y_3=1,\qquad y_1+y_2=2,\qquad y_2+y_3=3.$$

三式相加得 $2(y_1+y_2+y_3)=6$，即 $y_1+y_2+y_3=3$。用它分别减去三式：

$$y_2=3-1=2,\qquad y_3=3-2=1,\qquad y_1=3-3=0.$$

新坐标是 $(0,2,1)^{\mathsf T}$。验算：$2\boldsymbol{\beta}_2+\boldsymbol{\beta}_3=\boldsymbol{\alpha}_1+2\boldsymbol{\alpha}_2+3\boldsymbol{\alpha}_3$。

合上书，从 $(\boldsymbol{\beta})=(\boldsymbol{\alpha})P$ 出发重新推出 $\boldsymbol{x}=P\boldsymbol{y}$，并指出哪一步用了坐标的唯一性。

### 4. Ax=0 的解有多少个自由度？

先拿三阶压扁⑤ 试一试。它的行最简形（L.7.4）是

$$\begin{pmatrix}1&2&1\\2&4&3\\3&6&4\end{pmatrix}\to\begin{pmatrix}1&2&0\\0&0&1\\0&0&0\end{pmatrix}.$$

$x_2$ 是自由未知量，$x_1=-2x_2$，$x_3=0$，所以零空间是 $(-2,1,0)^{\mathsf T}$ 张成的直线，1 维；而秩是 2，列空间是平面 $z=x+y$，2 维。$1+2=3$，正好是输入空间的维数。图 L8-n4 画出了这件事：一条直线上的方向被压到原点，剩下的两维铺成了像。

![三阶压扁⑤：左边输入空间里虚线方向 $(-2,1,0)^{\mathsf T}$（零空间，1 维）被压到原点；右边整个空间被压成阴影平面 $z=x+y$（列空间，2 维）；$1+2=3$](fig/L8-n4.pdf){width=85%}

再看一个有两个自由未知量的例子，第 5 节还要用它：

$$A=\begin{pmatrix}1&2&0&1\\2&4&1&3\\3&6&1&4\end{pmatrix}\to\begin{pmatrix}1&2&0&1\\0&0&1&1\\0&0&0&0\end{pmatrix}.$$

（第 2 行减第 1 行的 2 倍；第 3 行减第 1 行的 3 倍，再减新的第 2 行。）主元在第 1、3 列，$r(A)=2$；$x_2,x_4$ 是自由未知量，方程化为 $x_1=-2x_2-x_4$，$x_3=-x_4$。于是每个解都写成

$$\boldsymbol{x}=\begin{pmatrix}-2x_2-x_4\\x_2\\-x_4\\x_4\end{pmatrix}=x_2\begin{pmatrix}-2\\1\\0\\0\end{pmatrix}+x_4\begin{pmatrix}-1\\0\\-1\\1\end{pmatrix}=x_2\boldsymbol{\xi}_1+x_4\boldsymbol{\xi}_2.$$

#### $\boldsymbol\xi_1,\boldsymbol\xi_2$ 为什么是一组基

够用：每个解由自由未知量 $x_2,x_4$ 的取值唯一决定，上面一行说明它就是 $\boldsymbol{\xi}_1,\boldsymbol{\xi}_2$ 的组合，所以 $\boldsymbol{\xi}_1,\boldsymbol{\xi}_2$ 张成 $N(A)$。

不多余：只看第 2、4 个分量，$\boldsymbol{\xi}_1$ 是 $(1,0)$，$\boldsymbol{\xi}_2$ 是 $(0,1)$。若 $c_1\boldsymbol{\xi}_1+c_2\boldsymbol{\xi}_2=\boldsymbol{0}$，这两个位置给出 $c_1=c_2=0$。

所以 $\dim N(A)=2$，恰好是自由未知量的个数。

这个论证对任何矩阵都适用：让自由未知量轮流取 1、其余取 0，得到的解在自由未知量的位置上像 $\boldsymbol{e}_1,\boldsymbol{e}_2,\dots$ 那样排开，所以无关；每个解由自由未知量的值唯一决定，所以够用。自由未知量的个数是未知数个数减去主元个数，主元个数就是秩（L.7.5），于是得到**秩–零化度定理**（零化度就是 $\dim N(A)$）：对 $m\times n$ 矩阵 $A$，

$$\dim N(A)=n-r(A).$$

$\dim C(A)$ 是列秩 $r(A)$，所以 $\dim C(A)+\dim N(A)=n$：输入的 $n$ 维里，$n-r(A)$ 维被压成零向量，像只剩 $r(A)$ 维。

可以这样记：$n$ 个未知数有 $n$ 个自由度，每一条独立的方程锁住一个，剩下 $n-r(A)$ 个。「独立」二字要紧：上面的 $A$ 有 3 个方程，第 3 个是前两个之和，什么也没锁住，所以剩下 $4-2$ 个而不是 $4-3$ 个。

**方法 4（秩–零化度定理）**

1. 已知 $r(A)$ 求解空间的维数，或反过来，都用 $\dim N(A)=n-r(A)$。
2. $n$ 是**列数**（未知数个数），不是行数。
3. 要具体的一组基，就化成行最简形，让自由未知量轮流取 1。

**例 5**　设 $A$ 是 $4\times5$ 矩阵，$N(A)$ 由两个线性无关的向量张成。(1) 求 $r(A)$；(2) $A\boldsymbol{x}=\boldsymbol{b}$ 是否对每个 $\boldsymbol{b}\in\mathbb{R}^4$ 都有解？

(1) $\dim N(A)=2$，未知数个数 $n=5$，由 $2=5-r(A)$ 得 $r(A)=3$。最常见的错误是拿行数 4 去减。

(2) 不是。$A\boldsymbol{x}=\boldsymbol{b}$ 有解当且仅当 $\boldsymbol{b}\in C(A)$（第 1 节），而 $\dim C(A)=r(A)=3$。$C(A)$ 只是 $\mathbb{R}^4$ 里的 3 维子空间，维数不同，不可能是整个 $\mathbb{R}^4$，总有 $\boldsymbol{b}$ 落在它外面。这道题没解方程，只用了维数。

> 设 $B=\begin{pmatrix}1&-1&2&0\\2&-2&4&1\end{pmatrix}$。不解方程先说出 $\dim N(B)$，再求 $N(B)$ 的一组基。
>
> 答案：两行不成比例，$r(B)=2$，$\dim N(B)=4-2=2$。第 2 行减第 1 行的 2 倍得 $(0,0,0,1)$，于是 $x_4=0$，$x_1=x_2-2x_3$，$x_2,x_3$ 自由，基为 $(1,1,0,0)^{\mathsf T}$、$(-2,0,1,0)^{\mathsf T}$。

合上书，用一个具体的行最简形说明自由未知量轮流取 1 得到的解为什么无关、为什么够用，再写出秩–零化度定理。

### 5. 一个矩阵自带哪四个空间，它们怎样互相垂直？

把 $A\boldsymbol{x}=\boldsymbol{0}$ 逐行写开，第 $i$ 个方程说的是 $A$ 的第 $i$ 行与 $\boldsymbol{x}$ 的点积等于 0（L.3.1 的按行看法）。所以 $\boldsymbol{x}\in N(A)$ 就是 $\boldsymbol{x}$ 与每一行都正交（L.2.3）。零空间和「行」有这样的关系，各行张成的子空间也该有个名字。

#### 四个子空间和它们的维数

$A$ 的各行转置成列向量后张成的子空间叫**行空间**。它就是 $A^{\mathsf T}$ 的列空间，记作 $C(A^{\mathsf T})$，在 $\mathbb{R}^n$ 中。

$A^{\mathsf T}$ 的零空间 $N(A^{\mathsf T})$ 在 $\mathbb{R}^m$ 中，叫**左零空间**。这个名字是因为 $A^{\mathsf T}\boldsymbol{y}=\boldsymbol{0}$ 转置后是 $\boldsymbol{y}^{\mathsf T}A=\boldsymbol{0}^{\mathsf T}$，$\boldsymbol{y}^{\mathsf T}$ 从左边乘 $A$ 得零。

设 $r(A)=r$，四个子空间的维数是

$$\dim C(A)=r,\qquad\dim C(A^{\mathsf T})=r,\qquad\dim N(A)=n-r,\qquad\dim N(A^{\mathsf T})=m-r.$$

第二个用了行秩等于列秩（L.7.5）；第四个是对 $A^{\mathsf T}$ 用秩–零化度定理，$A^{\mathsf T}$ 有 $m$ 列、秩为 $r$。

求它们的基时，要分清行变换改变了什么：

- 行变换把每一行换成原来各行的组合，并且可以撤销，所以**行空间不变**，阶梯形的非零行就是行空间的一组基；
- 列空间却会变。三阶压扁⑤ 的第 1 列是 $(1,2,3)^{\mathsf T}$，行最简形的第 1 列 $(1,0,0)^{\mathsf T}$ 却不在平面 $z=x+y$ 上。行变换保住的只是列与列之间的线性关系，所以列空间的基要取**原矩阵**的主元列。

行空间看变换后的行，列空间看变换前的列，两条正好相反，一起记。

#### 行空间与零空间互为正交补

$N(A)$ 中的向量与每一行正交，因而与各行的任何组合正交：

$$\boldsymbol{x}\cdot\sum c_i\boldsymbol{r}_i=\sum c_i(\boldsymbol{x}\cdot\boldsymbol{r}_i)=0.$$

为了把这种关系说完整，定义子空间 $V$ 的**正交补** $V^{\perp}$（读作「$V$ 垂」）为与 $V$ 中每个向量都正交的全体向量。它也是子空间：若 $\boldsymbol{u},\boldsymbol{v}$ 都与 $\boldsymbol{w}$ 正交，则 $(\boldsymbol{u}+\boldsymbol{v})\cdot\boldsymbol{w}=\boldsymbol{u}\cdot\boldsymbol{w}+\boldsymbol{v}\cdot\boldsymbol{w}=0$，数乘同理。

**定理**　行空间与零空间互为正交补：$N(A)=C(A^{\mathsf T})^{\perp}$，$C(A^{\mathsf T})=N(A)^{\perp}$。

思路是先证一个包含，再比维数。

1. 与每一行正交，就是与行空间正交，所以 $N(A)=C(A^{\mathsf T})^{\perp}$。
2. 行空间的向量都与 $N(A)$ 正交，所以 $C(A^{\mathsf T})\subseteq N(A)^{\perp}$。
3. 比维数。把 $N(A)$ 的一组基（$n-r$ 个向量）作为一个新矩阵 $M$ 的行，$M$ 是 $(n-r)\times n$ 矩阵，行空间就是 $N(A)$。对 $M$ 用第 1 步：$N(M)=C(M^{\mathsf T})^{\perp}=N(A)^{\perp}$。再对 $M$ 用秩–零化度定理（第 4 节）：$M$ 有 $n$ 列，行无关所以秩为 $n-r$，于是 $\dim N(A)^{\perp}=\dim N(M)=n-(n-r)=r$，与行空间的维数相同。
4. 一个子空间含在另一个里且维数相同，两者相等（第 2 节）。

把 $A$ 换成 $A^{\mathsf T}$，同样得到 $C(A)$ 与 $N(A^{\mathsf T})$ 在 $\mathbb{R}^m$ 中互为正交补。

#### 每个向量都分成两份

由正交补得到一个分解。

先看公共部分。两者公共的 $\boldsymbol{x}$ 与自己正交，$\lVert\boldsymbol{x}\rVert^2=\boldsymbol{x}\cdot\boldsymbol{x}=0$（$\lVert\boldsymbol{x}\rVert$ 是 L.2 的长度，即高中课本的 $|\boldsymbol{x}|$），所以只有零向量是公共的。

再看合起来。两者的基合起来共 $r+(n-r)=n$ 个向量，它们无关：一个为零的组合里，行空间那部分等于零空间那部分的相反数，是公共向量，只能是零，于是两部分的系数各自全为零。由第 2 节第二条，这 $n$ 个向量是 $\mathbb{R}^n$ 的一组基。于是每个 $\boldsymbol{x}\in\mathbb{R}^n$ 都能唯一地写成

$$\boldsymbol{x}=\boldsymbol{x}_r+\boldsymbol{x}_n,\qquad\boldsymbol{x}_r\in C(A^{\mathsf T}),\quad\boldsymbol{x}_n\in N(A),$$

并且 $A\boldsymbol{x}=A\boldsymbol{x}_r+A\boldsymbol{x}_n=A\boldsymbol{x}_r$。$A$ 只看得见 $\boldsymbol{x}$ 落在行空间里的那一份，零空间里的那一份被它压成了零（图 L8-n2）。L.10 的投影和 L.15 的奇异值分解都建立在这张图上。

![行空间（阴影平面）与零空间（虚线）在原点垂直相交；$\boldsymbol{x}$ 分成平面上的 $\boldsymbol{x}_r$ 和沿虚线方向的 $\boldsymbol{x}_n$，$A$ 把 $\boldsymbol{x}_n$ 压成零，所以 $A\boldsymbol{x}=A\boldsymbol{x}_r$](fig/L8-n2.pdf){width=60%}

把有解的条件用三种说法对齐：

| 方程组 | 列向量 | 变换 |
|---|---|---|
| $A\boldsymbol{x}=\boldsymbol{b}$ 有解 | $\boldsymbol{b}$ 是各列的组合，$\boldsymbol{b}\in C(A)$ | $\boldsymbol{b}$ 落在像里 |
| $A\boldsymbol{x}=\boldsymbol{0}$ 只有零解 | 各列线性无关 | 零空间只有 $\boldsymbol 0$，没有方向被压扁 |

由刚证的 $C(A)=N(A^{\mathsf T})^{\perp}$，第一行还等价于：$\boldsymbol{b}$ 与左零空间的每个向量正交。这个条件只要算几个点积，不用解方程。

#### 计算四个子空间

**方法 5（四个子空间）**

1. 把 $A$ 化成行最简形。
2. 非零行给出行空间的基；原矩阵的主元列给出列空间的基；自由未知量轮流取 1 给出零空间的基。
3. 左零空间：对 $A^{\mathsf T}$ 做同样的事，或者记下消元时化成零行的那个行组合。
4. 维数用 $r$、$r$、$n-r$、$m-r$ 检验。
5. $A\boldsymbol{x}=\boldsymbol{b}$ 有解当且仅当 $\boldsymbol{b}$ 与左零空间的每个向量正交。

**例 6**　对第 4 节的 $A=\begin{pmatrix}1&2&0&1\\2&4&1&3\\3&6&1&4\end{pmatrix}$，求四个子空间的基，并写出 $A\boldsymbol{x}=\boldsymbol{b}$ 有解的条件。

这里 $m=3$，$n=4$，$r=2$，四个维数应是 2、2、2、1。

行空间取行最简形的非零行 $(1,2,0,1)^{\mathsf T}$、$(0,0,1,1)^{\mathsf T}$。主元在第 1、3 列，列空间取原矩阵的 $(1,2,3)^{\mathsf T}$、$(0,1,1)^{\mathsf T}$。零空间是第 4 节的 $\boldsymbol{\xi}_1,\boldsymbol{\xi}_2$，它们与行空间两个基向量的四个点积都是 0，例如 $(0,0,1,1)\cdot\boldsymbol{\xi}_2=-1+1=0$。

左零空间看消元的记录。第 3 行先减去第 1 行的 3 倍，再减去新的第 2 行（即第 2 行减第 1 行的 2 倍），化成了零行，合起来是

$$\boldsymbol{r}_3-3\boldsymbol{r}_1-(\boldsymbol{r}_2-2\boldsymbol{r}_1)=\boldsymbol{r}_3-\boldsymbol{r}_1-\boldsymbol{r}_2=\boldsymbol{0}.$$

所以 $\boldsymbol{y}=(-1,-1,1)^{\mathsf T}$ 满足 $\boldsymbol{y}^{\mathsf T}A=\boldsymbol{0}^{\mathsf T}$；左零空间是 1 维的，它就是一组基。

有解的条件是 $\boldsymbol{b}$ 与 $(-1,-1,1)^{\mathsf T}$ 正交，即 $b_3=b_1+b_2$。用列空间的两个基向量验算：$3=1+2$，$1=0+1$。

> 对 $A=\begin{pmatrix}1&1\\2&2\\3&3\end{pmatrix}$ 求四个子空间的维数和基。
>
> 答案：$r=1$，$m=3$，$n=2$，维数依次是 1、1、1、2。列空间由 $(1,2,3)^{\mathsf T}$ 张成，行空间由 $(1,1)^{\mathsf T}$ 张成，零空间由 $(1,-1)^{\mathsf T}$ 张成；左零空间是 $y_1+2y_2+3y_3=0$ 的解集，基为 $(-2,1,0)^{\mathsf T}$、$(-3,0,1)^{\mathsf T}$。

合上书，说明 $N(A)$ 为什么与行空间正交，再用维数说明两者为什么恰好互为正交补。

### 6. 多项式、矩阵也能当作向量吗？

次数不超过 2 的多项式 $a_0+a_1t+a_2t^2$ 相加，系数对应相加；乘一个数，系数都乘这个数。它的运算和 $(a_0,a_1,a_2)^{\mathsf T}$ 一模一样。前五节的结论能直接搬过来吗？

把能搬的东西抽出来。设非空集合 $V$ 上定义了加法和与实数的数乘，结果仍在 $V$ 中，并且对任意 $\boldsymbol u,\boldsymbol v,\boldsymbol w\in V$ 和实数 $k,l$ 满足八条运算律。加法四条：

1. 交换律 $\boldsymbol{u}+\boldsymbol{v}=\boldsymbol{v}+\boldsymbol{u}$；
2. 结合律 $(\boldsymbol{u}+\boldsymbol{v})+\boldsymbol{w}=\boldsymbol{u}+(\boldsymbol{v}+\boldsymbol{w})$；
3. 有零元 $\boldsymbol{0}$，使 $\boldsymbol{v}+\boldsymbol{0}=\boldsymbol{v}$；
4. 每个 $\boldsymbol{v}$ 有负元 $-\boldsymbol{v}$，使 $\boldsymbol{v}+(-\boldsymbol{v})=\boldsymbol{0}$。

数乘四条：

5. $1\boldsymbol{v}=\boldsymbol{v}$；
6. $k(l\boldsymbol{v})=(kl)\boldsymbol{v}$；
7. $k(\boldsymbol{u}+\boldsymbol{v})=k\boldsymbol{u}+k\boldsymbol{v}$；
8. $(k+l)\boldsymbol{v}=k\boldsymbol{v}+l\boldsymbol{v}$。

这样的 $V$ 叫（实）**线性空间**，也叫向量空间，其中的元素都叫向量。移项要用 3、4 两条，合并同类项要用 7、8 两条，L.1 的计算就是靠这八条做的。线性组合、线性相关、基、维数、坐标的定义只用到加法和数乘，于是原样适用；第 2、3 节关于基、维数、坐标的证明（包括替换定理和三条事实）也只用了这八条，所以那些结论同样成立。第 4、5 节用到矩阵的行和点积，只对 $\mathbb{R}^n$ 来说。

这时「向量」不再一定是箭头，但仍可以当箭头来想：**多项式也是箭头**，只要选好一把尺子，读数就是它的坐标。

#### 几个常见的线性空间

次数不超过 $n$ 的实系数多项式全体记作 $P_n$。$1,t,\dots,t^n$ 是一组基：它们张成 $P_n$，而一个多项式恒为零当且仅当系数全为零，所以它们无关。于是 $\dim P_n=n+1$。

全体 $m\times n$ 实矩阵记作 $\mathbb{R}^{m\times n}$。以 $E_{ij}$ 记第 $i$ 行第 $j$ 列是 1、其余是 0 的矩阵，这 $mn$ 个矩阵是一组基，所以维数是 $mn$。

多项式全体（不限次数）也是线性空间：对任何 $m$，$1,t,\dots,t^m$ 都无关，所以有限个向量张不满它，叫**无穷维**。本书只用有限维的空间。

#### 坐标是翻译器

抽象的向量怎样计算？选定一组基，每个向量对应它的坐标。由表示的唯一性，向量相加时坐标相加，数乘时坐标数乘，所以 $\sum c_i\boldsymbol{v}_i=\boldsymbol 0$ 翻成坐标就是 $\sum c_i\boldsymbol{x}_i=\boldsymbol 0$（$\boldsymbol x_i$ 是 $\boldsymbol v_i$ 的坐标），反过来也一样。于是一组抽象向量无关当且仅当它们的坐标向量无关。坐标像一台翻译器，把多项式、矩阵翻成数组，算完再翻回来。

**方法 6（用坐标计算抽象向量）**

1. 选一组简单的基（$1,t,t^2,\dots$ 或 $E_{ij}$）。
2. 把每个向量写成坐标。
3. 对坐标向量用方法 2、3 判断相关性、求基和维数、求坐标，再翻回去。

**例 7**　(1) 证明 $1,\ 1+t,\ (1+t)^2$ 是 $P_2$ 的一组基；(2) 求 $p(t)=2+3t+t^2$ 在这组基下的坐标。

(1) 由 $(1+t)^2=1+2t+t^2$，三个多项式在基 $1,t,t^2$ 下的坐标是 $(1,0,0)^{\mathsf T}$、$(1,1,0)^{\mathsf T}$、$(1,2,1)^{\mathsf T}$。以它们为列的矩阵是上三角的，行列式等于对角元之积 1，所以三个坐标向量无关，三个多项式也无关。$\dim P_2=3$，由第 2 节第二条，3 个无关向量就是一组基。

(2) 设 $p=c_1\cdot1+c_2(1+t)+c_3(1+t)^2$，比较 $1,t,t^2$ 的系数：

$$c_1+c_2+c_3=2,\qquad c_2+2c_3=3,\qquad c_3=1.$$

从下往上代，$c_2=1$，$c_1=0$，坐标是 $(0,1,1)^{\mathsf T}$，即 $2+3t+t^2=(1+t)+(1+t)^2$。

> 求 2 阶对称矩阵全体 $W=\left\{\begin{pmatrix}a&b\\b&c\end{pmatrix}:a,b,c\in\mathbb{R}\right\}$ 的一组基和维数，并写出 $\begin{pmatrix}1&2\\2&3\end{pmatrix}$ 的坐标。
>
> 答案：$\begin{pmatrix}a&b\\b&c\end{pmatrix}=aE_{11}+b(E_{12}+E_{21})+cE_{22}$，三个矩阵张成 $W$；组合为零矩阵时 $a=b=c=0$，所以无关。$\dim W=3$，所给矩阵的坐标是 $(1,2,3)^{\mathsf T}$。

合上书，说明为什么选定一组基以后，判断几个多项式是否线性无关可以改成判断它们的坐标向量。

### 7. 抽象空间上的线性变换怎样用矩阵记下来？

求导把一个多项式变成另一个：$D(a_0+a_1t+a_2t^2)=a_1+2a_2t$。求导满足 $D(p+q)=Dp+Dq$、$D(kp)=kDp$，按 L.3.3 的定义，它是 $P_2$ 上的线性变换。

L.3.3 里，$\mathbb{R}^n$ 上线性变换的矩阵第 $j$ 列是 $T(\boldsymbol{e}_j)$。$P_2$ 里没有现成的分量，借助坐标就有了。三个基向量的去向是 $D(1)=0$，$D(t)=1$，$D(t^2)=2t$，把它们在基 $1,t,t^2$ 下的坐标依次排成三列：

$$A=\begin{pmatrix}0&1&0\\0&0&2\\0&0&0\end{pmatrix}.$$

检验：$p=2+3t+t^2$ 的坐标是 $(2,3,1)^{\mathsf T}$，

$$A\begin{pmatrix}2\\3\\1\end{pmatrix}=\begin{pmatrix}3\\2\\0\end{pmatrix},$$

翻回多项式是 $3+2t$，正是 $p'(t)$。

道理和 L.3.3 一样：$p=\sum x_j\boldsymbol{\alpha}_j$ 时，由线性，$Dp=\sum x_jD\boldsymbol{\alpha}_j$，它的坐标是 $A$ 的各列以 $x_j$ 为权重的组合，即 $A\boldsymbol{x}$。

一般地，设 $T$ 是 $n$ 维线性空间 $V$ 上的线性变换，$\boldsymbol{\alpha}_1,\dots,\boldsymbol{\alpha}_n$ 是 $V$ 的基，把 $T\boldsymbol{\alpha}_j$ 的坐标排成第 $j$ 列得到 $A$，即

$$(T\boldsymbol{\alpha}_1,\dots,T\boldsymbol{\alpha}_n)=(\boldsymbol{\alpha}_1,\dots,\boldsymbol{\alpha}_n)A,$$

$A$ 叫 $T$ 在这组基下的**矩阵**。向量的坐标是 $\boldsymbol{x}$ 时，像的坐标是 $A\boldsymbol{x}$。

#### 换一把尺子，矩阵怎样变

设新基 $(\boldsymbol{\beta})=(\boldsymbol{\alpha})P$，$T$ 在新基下的矩阵是 $B$。已知 $\boldsymbol{v}$ 的新坐标 $\boldsymbol{y}$，求 $T\boldsymbol{v}$ 的新坐标，可以分三步：

1. 译出：用 $P$ 把 $\boldsymbol{y}$ 译成旧坐标 $P\boldsymbol{y}$（第 3 节）；
2. 作用：用旧矩阵算出像的旧坐标 $AP\boldsymbol{y}$；
3. 译回：用 $P^{-1}$ 译回新坐标 $P^{-1}AP\boldsymbol{y}$。

按定义这个结果又是 $B\boldsymbol{y}$。两者对每个 $\boldsymbol{y}$ 都相等（取 $\boldsymbol{y}=\boldsymbol{e}_j$ 就是第 $j$ 列相等），所以

$$B=P^{-1}AP.$$

$B$ 与 $A$ 记录的是同一个变换，只是尺子不同。L.12 把满足这个关系的两个矩阵叫作相似矩阵，并寻找让 $B$ 成为对角矩阵的尺子。

**方法 7（线性变换的矩阵）**

1. 把基向量的像逐个写成坐标，依次排成列。
2. 换基时用 $B=P^{-1}AP$；或者直接把新基向量的像写成新坐标排成列。两种算法可以互相验算。

**例 8**　$\mathbb{R}^2$ 上的线性变换 $T$ 在标准基下的矩阵是 $A=\begin{pmatrix}3&1\\0&2\end{pmatrix}$，求 $T$ 在基 $\boldsymbol{\beta}_1=(1,0)^{\mathsf T}$、$\boldsymbol{\beta}_2=(1,-1)^{\mathsf T}$ 下的矩阵。

旧基是标准基，$P=(\boldsymbol{\beta}_1,\boldsymbol{\beta}_2)=\begin{pmatrix}1&1\\0&-1\end{pmatrix}$，$|P|=-1$。由二阶求逆公式，$P^{-1}=\frac{1}{-1}\begin{pmatrix}-1&-1\\0&1\end{pmatrix}=P$。于是

$$AP=\begin{pmatrix}3&2\\0&-2\end{pmatrix},\qquad B=P^{-1}AP=\begin{pmatrix}1&1\\0&-1\end{pmatrix}\begin{pmatrix}3&2\\0&-2\end{pmatrix}=\begin{pmatrix}3&0\\0&2\end{pmatrix}.$$

用另一种算法验算：$A\boldsymbol{\beta}_1=(3,0)^{\mathsf T}=3\boldsymbol{\beta}_1$，$A\boldsymbol{\beta}_2=(2,-2)^{\mathsf T}=2\boldsymbol{\beta}_2$，新坐标 $(3,0)^{\mathsf T}$、$(0,2)^{\mathsf T}$ 排成两列正是 $B$。换了这把尺子，$T$ 只是沿两个基向量方向伸缩；这样的尺子怎样找，是 L.11、L.12 的事。

合上书，说出线性变换在一组基下的矩阵第 $j$ 列放的是什么，再用「译出、作用、译回」推出 $B=P^{-1}AP$。

### 本章小结

| 方法 | 什么时候用 | 对应题号 |
|---|---|---|
| 方法 1（判断子空间） | 某个集合是不是子空间 | L8-01、L8-05 |
| 方法 2（求张成的基与维数） | 张成的基、维数，扩充成基 | L8-02 |
| 方法 3（过渡矩阵与坐标变换） | 换基、换坐标，判断新向量组是否为基 | L8-03、L8-06、L8-10 |
| 方法 4（秩–零化度定理） | 秩与解空间维数互推 | L8-04、L8-08、L8-14 |
| 方法 5（四个子空间） | 四个子空间的基，有解条件 | L8-07、L8-09、L8-11、L8-14 |
| 方法 6（用坐标计算抽象向量） | 多项式、矩阵空间的基、维数、坐标 | L8-13 |
| 方法 7（线性变换的矩阵） | 抽象线性变换的矩阵，换基后的 $P^{-1}AP$ | L8-13 |

**可逆大定理**（$n$ 阶方阵 $A$，下面各条互相等价）：

- 消元后有 $n$ 个主元；$A\boldsymbol x=\boldsymbol b$ 对每个 $\boldsymbol b$ 都有唯一解；$A\boldsymbol x=\boldsymbol 0$ 只有零解（L.4）；
- $A$ 可逆；存在 $B$ 使 $AB=E$（L.5）；
- $|A|\ne0$（L.6）；
- 列（行）向量组线性无关；$r(A)=n$（L.7）；
- $A$ 的列向量构成 $\mathbb{R}^n$ 的一组基（本章新增）；
- 零空间 $N(A)$ 只有零向量（本章新增）。

**秩的几种说法**：$r(A)=$ 主元个数 $=$ 列秩 $=$ 行秩 $=$ 不为零子式的最高阶数（L.7）$=\dim C(A)=\dim C(A^{\mathsf T})=n-\dim N(A)$（本章新增）。
