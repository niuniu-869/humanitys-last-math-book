## L.1 · 向量与线性组合

线性代数研究「一次」的关系：好几个量同时满足的一次方程，以及把一串数按比例伸缩再相加的运算。今天它是处理「一大串数」的通用语言：推荐系统把一个用户写成一串打分，大模型把每个词写成几千个数，模型的每一层几乎都在做「矩阵乘向量」。

它最早是被解方程组逼出来的。《九章算术》的「方程」章把数按位置排成数表，用一组数减去另一组的倍数，逐个消去未知数。19 世纪初，高斯在轨道计算中把逐个消元整理成固定步骤，今天叫高斯消元（L.4）。方程一多，值得研究的就成了那张系数表本身，1858 年凯莱发表了系统研究矩阵运算的论文（L.3）。

另一条线索来自几何。高中的向量是平面或空间里的箭头，最多三个分量。格拉斯曼在 1844 年的《线性扩张论》里换了个角度：箭头相加、伸缩的规则本身并不依赖「只有三个方向」，所以同一套运算可以用在任意多个方向上。本章做最基础的一步：让一串数能相加、伸缩；比较谁和谁像，留给 L.2。

本章先把向量定义成有序的一串数（第 1 节），再只用加法和数乘去「拼」向量，得到线性组合（第 2 节）和张成（第 3 节），最后给系数加上「非负、和为 1」的限制，得到凸组合（第 4 节）。

### 1. 一个用户、一件商品、一个词，怎样写成一串数？

一个视频网站请用户给四部电影打分（1 到 5 分），四部依次是科幻片、动作片、爱情片、文艺片。小林打了 5、4、1、2 分，小周打了 4、5、2、1 分，小吴打了 1、2、5、4 分。网站存下的是这四个数按固定顺序排成的一列，小林是

$$\boldsymbol u=\begin{pmatrix}5\\4\\1\\2\end{pmatrix}.$$

顺序是约定好的，第 1 个数永远是科幻片的分，顺序一换说的就是另一个人。

这一节的内容用一句话就能说完：**向量就是一串有顺序的数，外加两条运算规定**。

#### 对象：一串有顺序的数

$n$ 个实数按顺序排成的一列，叫作一个 **$n$ 维向量**，第 $i$ 个数 $a_i$ 叫它的第 $i$ 个**分量**。「维数」就是这串数有多长，小林的打分是 4 维向量。

全体 $n$ 维向量组成的集合记作 $\mathbb R^n$。高中的平面向量都在 $\mathbb R^2$ 里，空间向量都在 $\mathbb R^3$ 里。

两个向量相等，指维数相同、并且每个分量都相等。分量全是 0 的向量叫零向量，记作 $\boldsymbol 0$。本书用粗体小写字母表示向量，普通字母表示数。

本书的向量默认竖着写，叫**列向量**。竖着写太占地方，正文里常横过来写，再加一个上标：$\boldsymbol u=(5,4,1,2)^{\mathsf T}$。上标 $^{\mathsf T}$ 读作「转置」，它把列变成行、行变成列。横着写的一行数叫**行向量**，所以 $\boldsymbol u^{\mathsf T}=(5,4,1,2)$ 是行向量；再转置一次又回到列，$(\boldsymbol u^{\mathsf T})^{\mathsf T}=\boldsymbol u$。

默认竖着写，是因为到 L.3 要把几个向量并排成一张数表，每个向量正好占一列。

#### 两条规定：加法和数乘

小林和小周一起看电影，要按两人的总分挑片，就把对应位置的分相加。记小周为 $\boldsymbol v=(4,5,2,1)^{\mathsf T}$，

$$\boldsymbol u+\boldsymbol v=(5+4,\ 4+5,\ 1+2,\ 2+1)^{\mathsf T}=(9,9,3,3)^{\mathsf T}.$$

改用 10 分制，每个分数乘 2，小林成了 $2\boldsymbol u=(10,8,2,4)^{\mathsf T}$。

一般地，规定

$$\boldsymbol a+\boldsymbol b=(a_1+b_1,\ \dots,\ a_n+b_n)^{\mathsf T},\qquad k\boldsymbol a=(ka_1,\ \dots,\ ka_n)^{\mathsf T},$$

分别叫向量的**加法**和**数乘**。这里 $k$ 是实数，也叫**标量**。维数不同的向量不能相加。$(-1)\boldsymbol a$ 记作 $-\boldsymbol a$，$\boldsymbol a+(-\boldsymbol b)$ 记作 $\boldsymbol a-\boldsymbol b$，也就是对应分量相减。

#### 运算律：从实数那里继承来

加法和数乘都是一个分量一个分量地做，每个分量上做的就是实数的加法和乘法，所以实数的运算律原样搬过来：

1. 加法的交换律、结合律：$\boldsymbol a+\boldsymbol b=\boldsymbol b+\boldsymbol a$，$(\boldsymbol a+\boldsymbol b)+\boldsymbol c=\boldsymbol a+(\boldsymbol b+\boldsymbol c)$；
2. 两条分配律：$k(\boldsymbol a+\boldsymbol b)=k\boldsymbol a+k\boldsymbol b$，$(k+l)\boldsymbol a=k\boldsymbol a+l\boldsymbol a$；
3. 数乘的结合律：$k(l\boldsymbol a)=(kl)\boldsymbol a$。

这五个等式不用死记，它们都用同一个办法验证：比较等号两边的第 $i$ 个分量。以 $k(\boldsymbol a+\boldsymbol b)=k\boldsymbol a+k\boldsymbol b$ 为例，左边先相加再乘 $k$，右边先各乘 $k$ 再相加，两边的第 $i$ 个分量是

$$k(a_i+b_i)=ka_i+kb_i,$$

中间的等号是实数的乘法分配律。$i$ 是任取的，所以两个向量的每个分量都相等。其余四条，把这里的乘法分配律换成对应的实数运算律就行。

有了这五条，含向量的等式就能像一次方程那样处理。「移项」就是两边同加一个向量，例如同加 $-\boldsymbol a$；「约去系数」就是两边同乘同一个非零数。

#### 两种看法：清单和箭头

一串数还有另一种看法。只看前两部电影，小林是 $(5,4)^{\mathsf T}$，画成从原点指向点 $(5,4)$ 的箭头，就是高中的平面向量：加法是箭头首尾相接，数乘是伸缩，$k<0$ 时掉头。三个分量对应空间里的点，四个分量就画不出来了。

两种看法可以记成「清单」和「箭头」：清单用来计算，箭头用来想象方向和长短。第 $i$ 个数就是箭头终点的第 $i$ 个坐标。

箭头只在 $n\le3$ 时画得出来。好在定义和运算律只用到逐个分量的计算，和能不能画图无关。所以从这里开始，$n$ 维向量的结论都只用定义和运算律来推，图只帮助想象。

**方法 1（逐分量运算与移项）**

1. 加法、数乘逐个分量做；转置不改分量，只改横竖。
2. 含未知向量的一次等式，按运算律移项、合并，再两边同乘一个非零数，把未知向量单独留在一边。
3. 解出后代回原式检查。

**例 1**　设 $\boldsymbol a=(1,-2,0,3)^{\mathsf T}$，$\boldsymbol b=(1,0,2,1)^{\mathsf T}$，求满足 $2\boldsymbol x+\boldsymbol a=3\boldsymbol b$ 的向量 $\boldsymbol x$。

思路和解 $2x+1=3$ 一样：先移项，再除以 2。

第一步，移项。两边同加 $-\boldsymbol a$。左边的 $\boldsymbol a+(-\boldsymbol a)$ 逐个分量是 $a_i-a_i=0$，等于 $\boldsymbol 0$，于是

$$2\boldsymbol x=3\boldsymbol b-\boldsymbol a.$$

第二步，约去系数。两边同乘 $\frac12$，左边由数乘结合律得 $\frac12(2\boldsymbol x)=(\frac12\cdot2)\boldsymbol x=\boldsymbol x$：

$$\boldsymbol x=\tfrac12(3\boldsymbol b-\boldsymbol a).$$

第三步，逐个分量算出来：

$$3\boldsymbol b-\boldsymbol a=(3,0,6,3)^{\mathsf T}-(1,-2,0,3)^{\mathsf T}=(2,2,6,0)^{\mathsf T},\qquad \boldsymbol x=(1,1,3,0)^{\mathsf T}.$$

代回检查：$2\boldsymbol x+\boldsymbol a=(2,2,6,0)^{\mathsf T}+(1,-2,0,3)^{\mathsf T}=(3,0,6,3)^{\mathsf T}=3\boldsymbol b$。

> 设 $\boldsymbol c=(2,1,-1,0)^{\mathsf T}$，$\boldsymbol d=(1,2,4,3)^{\mathsf T}$。求 $\boldsymbol c+\boldsymbol d$，再求满足 $3\boldsymbol x-\boldsymbol d=\boldsymbol c$ 的 $\boldsymbol x$。
>
> 答案：$\boldsymbol c+\boldsymbol d=(3,3,3,3)^{\mathsf T}$。两边同加 $\boldsymbol d$ 得 $3\boldsymbol x=\boldsymbol c+\boldsymbol d$，再同乘 $\frac13$，$\boldsymbol x=(1,1,1,1)^{\mathsf T}$。

合上书，写出加法和数乘的定义，再只用定义说明 $k(\boldsymbol a+\boldsymbol b)=k\boldsymbol a+k\boldsymbol b$ 为什么对任意维数都成立。

### 2. 只许伸缩和相加，能拼出哪些向量？

有了加法和数乘，自然要问：只用这两种运算，手上的几个向量能造出哪些新向量？

平面上给定 $\boldsymbol a_1=(1,2)^{\mathsf T}$、$\boldsymbol a_2=(3,1)^{\mathsf T}$，只许把它们各自伸缩、再相加，能不能得到 $\boldsymbol b=(5,5)^{\mathsf T}$？问题就是：有没有两个数 $c_1,c_2$，使

$$c_1\begin{pmatrix}1\\2\end{pmatrix}+c_2\begin{pmatrix}3\\1\end{pmatrix}=\begin{pmatrix}5\\5\end{pmatrix}?$$

左边按定义算出来是 $(c_1+3c_2,\ 2c_1+c_2)^{\mathsf T}$。两个向量相等就是每个分量相等，于是一个向量等式变成了两个普通方程：

$$c_1+3c_2=5,\qquad 2c_1+c_2=5.$$

由第二式 $c_2=5-2c_1$，代入第一式：

$$c_1+3(5-2c_1)=5,\qquad -5c_1=-10,\qquad c_1=2,$$

再得 $c_2=1$。检查：$2(1,2)^{\mathsf T}+(3,1)^{\mathsf T}=(5,5)^{\mathsf T}$。

在图 LA1-1 里，两族斜线分别平行于 $\boldsymbol a_1$、$\boldsymbol a_2$，铺成一张斜方格纸。

![沿 $\boldsymbol a_1$ 走 2 步、再沿 $\boldsymbol a_2$ 走 1 步到达 $\boldsymbol b$，这条折线就是 $\boldsymbol b=2\boldsymbol a_1+\boldsymbol a_2$](fig/LA1-1.pdf){width=60%}

这张斜方格纸在 L.3 还会出现：把普通方格纸的 $\boldsymbol e_1=(1,0)^{\mathsf T}$、$\boldsymbol e_2=(0,1)^{\mathsf T}$ 换成 $\boldsymbol a_1$、$\boldsymbol a_2$，方格纸就被推歪成图里的样子，这个推歪就是一个矩阵。

#### 线性组合

「伸缩再相加」贯穿整个线性代数，给它一个名字。设 $\boldsymbol a_1,\dots,\boldsymbol a_k$ 是维数相同的向量，$c_1,\dots,c_k$ 是实数，和式

$$c_1\boldsymbol a_1+c_2\boldsymbol a_2+\cdots+c_k\boldsymbol a_k$$

叫作这组向量的一个**线性组合**，$c_i$ 叫**组合系数**。如果向量 $\boldsymbol b$ 能写成这种形式，就说 $\boldsymbol b$ 能由这组向量**线性表示**。

系数允许取任何实数：负系数是掉头再伸缩，小数是只取一部分。

**方法 2（按分量列方程求组合系数）**

1. 设 $\boldsymbol b=c_1\boldsymbol a_1+\cdots+c_k\boldsymbol a_k$，把系数 $c_1,\dots,c_k$ 当作未知数。
2. 两边逐个分量写出来，得到 $n$ 个方程、$k$ 个未知数。
3. 解方程组：有解，解就是组合系数；方程之间矛盾，$\boldsymbol b$ 就不能表示。

依据只有一条：两个向量相等，当且仅当每个分量都相等。

方法 2 把「能不能拼出来」翻译成了「方程组有没有解」。同一件事有了两种说法；L.3 还会给出第三种，L.4 再把三种说法排成一张表对齐。

**例 2**　记 $\boldsymbol 1=(1,1,1,1)^{\mathsf T}$ 为每个分量都是 1 的向量。$\boldsymbol w=(1,2,5,4)^{\mathsf T}$ 能不能由 $\boldsymbol u=(5,4,1,2)^{\mathsf T}$ 和 $\boldsymbol 1$ 线性表示？

和开头的问题不同，这里有 4 个方程、只有 2 个未知数。思路是先用两个方程定出系数，剩下的方程用来检验。

第一步，列方程。设 $\boldsymbol w=c_1\boldsymbol u+c_2\boldsymbol 1$，左边是 $(5c_1+c_2,\ 4c_1+c_2,\ c_1+c_2,\ 2c_1+c_2)^{\mathsf T}$，与 $(1,2,5,4)^{\mathsf T}$ 逐个分量比较：

$$5c_1+c_2=1,\qquad 4c_1+c_2=2,\qquad c_1+c_2=5,\qquad 2c_1+c_2=4.$$

第二步，用前两式定系数。两式相减得 $c_1=-1$，代回第二式得 $c_2=6$。

第三步，用后两式检验：$-1+6=5$，$-2+6=4$，都成立。

所以 $\boldsymbol w=6\cdot\boldsymbol 1-\boldsymbol u$。

为什么后两式对不上，就能断定不能表示？因为前两个方程已经把 $c_1,c_2$ 唯一定了下来，别无选择。这组唯一的系数若不满足后面的方程，就没有任何系数能满足全部方程。

> 判断 $\boldsymbol v=(4,5,2,1)^{\mathsf T}$ 能否由 $\boldsymbol u$ 和 $\boldsymbol 1$ 线性表示。
>
> 答案：不能。由 $5c_1+c_2=4$、$4c_1+c_2=5$ 得 $c_1=-1$、$c_2=9$；第三个分量要求 $c_1+c_2=2$，而 $-1+9=8$，矛盾。

这个「先唯一定出、再检验」的论证有个前提：前几个方程确实把系数唯一定了下来。如果参与组合的两个向量方向相同，它们只能拼出一条直线：直线上的目标有无穷多组系数，直线外的目标一组也没有，这时不能拿某一组解下结论。第 3 节专门讲这种情形。

最简单的一组向量是：记 $\boldsymbol e_i$ 为第 $i$ 个分量是 1、其余是 0 的 $n$ 维向量。它们各管一个坐标方向，所以任何向量都能由它们表示，系数就是分量本身：

$$\boldsymbol b=b_1\boldsymbol e_1+b_2\boldsymbol e_2+\cdots+b_n\boldsymbol e_n.$$

合上书，把开头拼出 $(5,5)^{\mathsf T}$ 的问题从头做一遍：写出向量等式，说明它为什么等价于两个普通方程。

### 3. 所有线性组合合在一起是什么形状？

$\boldsymbol a_1,\boldsymbol a_2$ 能拼出 $(5,5)^{\mathsf T}$，换成 $(2,9)^{\mathsf T}$ 呢？一个一个目标去试太慢，不如一次看清：所有能拼出的向量，合在一起是什么样子？

一组向量的全部线性组合组成的集合，叫作它们的**张成**，记作

$$\operatorname{span}(\boldsymbol a_1,\dots,\boldsymbol a_k)=\{c_1\boldsymbol a_1+\cdots+c_k\boldsymbol a_k:\ c_1,\dots,c_k\in\mathbb R\}.$$

「$\boldsymbol b$ 能由它们线性表示」和「$\boldsymbol b$ 属于它们的张成」是同一句话，仍用方法 2 判断。系数全取 0 得 $\boldsymbol 0$，所以张成总过原点。

#### 一个向量张成一条直线

只有一个非零向量 $\boldsymbol a$ 时，线性组合就是 $c\boldsymbol a$。$c$ 取遍实数，箭头沿 $\boldsymbol a$ 的方向伸长、缩短、掉头，终点画出一条过原点的直线。如果 $\boldsymbol a=\boldsymbol 0$，张成只有原点一个点。

#### 两个向量：先分清共线还是不共线

再加一个向量，要回答三件事：共线时张成是什么，不共线时张成是什么，不共线时系数唯不唯一。先给出一个词：两个向量中有一个是另一个的倍数，就说它们**共线**。零向量是任何向量的 0 倍，所以和任何向量都共线。

第一种情形，共线。设 $\boldsymbol a_1\ne\boldsymbol 0$，$\boldsymbol a_2=k\boldsymbol a_1$。把它代进任意一个组合，按分配律合并：

$$c_1\boldsymbol a_1+c_2\boldsymbol a_2=c_1\boldsymbol a_1+c_2k\boldsymbol a_1=(c_1+kc_2)\boldsymbol a_1.$$

从这个式子读出两件事。其一，拼来拼去还是 $\boldsymbol a_1$ 的倍数，张成仍是那条直线，新加的 $\boldsymbol a_2$ 什么也没添。其二，只要 $c_1+kc_2$ 取对，$c_1,c_2$ 就有无穷多种取法，系数不唯一。图 L1-n2 画的是 $k=2$ 的情形：$3\boldsymbol a_1$ 既等于 $3\boldsymbol a_1+0\cdot\boldsymbol a_2$，也等于 $\boldsymbol a_1+\boldsymbol a_2$。

![$\boldsymbol a_2=2\boldsymbol a_1$ 时，两种走法都停在同一点 $3\boldsymbol a_1$，所以系数不唯一；而无论怎样组合都离不开这条直线，直线外的 $\boldsymbol b$ 拼不出来](fig/L1-n2.pdf){width=55%}

第二种情形，不共线。在平面 $\mathbb R^2$ 里，它们能拼出所有向量，这是高中的平面向量基本定理：在图 LA1-1 上，过任一点 $\boldsymbol b$ 作 $\boldsymbol a_2$ 的平行线交 $\boldsymbol a_1$ 所在直线，就把 $\boldsymbol b$ 拆成了 $c_1\boldsymbol a_1$、$c_2\boldsymbol a_2$ 两段。

#### 平面上怎样判断共线

平面上两个向量能不能拼出整个平面，全看共不共线。下面的式子一步就能判断：平面上两个向量 $(p,q)^{\mathsf T}$、$(r,s)^{\mathsf T}$ 共线，当且仅当

$$ps-qr=0.$$

若 $(r,s)=k(p,q)$，即 $r=kp$、$s=kq$，代入得

$$ps-qr=p\cdot kq-q\cdot kp=0;$$

$(p,q)$ 是 $(r,s)$ 的倍数时同样。反过来，设 $ps=qr$，分三种情况找倍数：

- $p\ne0$：取 $k=\frac rp$，则 $kp=r$，并且 $kq=\frac{rq}p=\frac{ps}p=s$；
- $p=0$、$q\ne0$：这时 $qr=ps=0$，所以 $r=0$，取 $k=\frac sq$；
- $p=q=0$：$(p,q)$ 是零向量，和谁都共线。

前两种情况都得到 $(r,s)=k(p,q)$。

开头的 $\boldsymbol a_1=(1,2)^{\mathsf T}$、$\boldsymbol a_2=(3,1)^{\mathsf T}$ 有 $1\times1-2\times3=-5\ne0$，不共线，所以平面上任何目标都拼得出来。$(2,9)^{\mathsf T}$ 也不例外。式子 $ps-qr$ 到 L.6 会有名字，叫二阶行列式。

#### 不共线时系数唯一

不共线的两个向量，组合系数是唯一的，这在任何维数都成立。思路是：假设同一个向量有两套系数，证明这两套其实一样。

假如 $c_1\boldsymbol a_1+c_2\boldsymbol a_2=d_1\boldsymbol a_1+d_2\boldsymbol a_2$。移项、合并同类项，得

$$(c_1-d_1)\boldsymbol a_1=(d_2-c_2)\boldsymbol a_2.$$

第一步，证 $c_1=d_1$。若 $c_1\ne d_1$，两边同乘 $\frac1{c_1-d_1}$，$\boldsymbol a_1$ 就成了 $\boldsymbol a_2$ 的倍数，与不共线矛盾。

第二步，证 $c_2=d_2$。这时 $(d_2-c_2)\boldsymbol a_2=\boldsymbol 0$。零向量和谁都共线，而 $\boldsymbol a_2$ 与 $\boldsymbol a_1$ 不共线，所以 $\boldsymbol a_2\ne\boldsymbol 0$，它有某个分量 $a_{2j}\ne0$。看这个分量：$(d_2-c_2)a_{2j}=0$，只能 $d_2=c_2$。

所以两个不共线向量的组合可以「比较系数」：两个组合相等，对应系数就相等。

#### 到了空间，两个向量不够了

在 $\mathbb R^3$ 里，两个不共线的向量只张成一个平面，拼不出全部向量。

**例 3**　设 $\boldsymbol a_1=(1,0,1)^{\mathsf T}$，$\boldsymbol a_2=(0,1,1)^{\mathsf T}$。(1) 说明它们的张成恰好由满足 $z=x+y$ 的 $(x,y,z)^{\mathsf T}$ 组成，并判断 $\boldsymbol b=(2,3,4)^{\mathsf T}$、$\boldsymbol b'=(2,3,5)^{\mathsf T}$ 在不在里面；(2) 加入 $\boldsymbol a_3=(1,1,2)^{\mathsf T}$，张成变不变？改加 $\boldsymbol e_3=(0,0,1)^{\mathsf T}$ 呢？

(1) 要说明两个集合相同，两个方向各说一遍。

一方面，任一组合 $c_1\boldsymbol a_1+c_2\boldsymbol a_2=(c_1,\ c_2,\ c_1+c_2)^{\mathsf T}$，第三个分量正好是前两个之和。

另一方面，任给满足 $z=x+y$ 的 $(x,y,z)^{\mathsf T}$，取 $c_1=x$、$c_2=y$，组合就是 $(x,y,x+y)^{\mathsf T}=(x,y,z)^{\mathsf T}$。

所以张成恰好是平面 $\{(x,y,z)^{\mathsf T}:z=x+y\}$。$\boldsymbol b$ 的第三个分量 $4\ne2+3$，不在里面；$\boldsymbol b'$ 满足 $5=2+3$，$\boldsymbol b'=2\boldsymbol a_1+3\boldsymbol a_2$。

![全部组合铺成过原点的平面 $z=x+y$：$\boldsymbol b'$ 在平面上，$\boldsymbol b$ 在它正下方，拼不出来](fig/LA1-2.pdf){width=56%}

(2) 先看 $\boldsymbol a_3$。它等于 $\boldsymbol a_1+\boldsymbol a_2$，本来就在张成里。任取三个向量的一个组合，把 $\boldsymbol a_3$ 换成 $\boldsymbol a_1+\boldsymbol a_2$ 再合并同类项：

$$c_1\boldsymbol a_1+c_2\boldsymbol a_2+c_3\boldsymbol a_3=(c_1+c_3)\boldsymbol a_1+(c_2+c_3)\boldsymbol a_2,$$

它仍是 $\boldsymbol a_1,\boldsymbol a_2$ 的组合，所以张成还是那张平面。

再看 $\boldsymbol e_3$。它的第三个分量 $1\ne0+0$，不在平面上。加入它以后，任给 $(x,y,z)^{\mathsf T}$ 都有

$$x\boldsymbol a_1+y\boldsymbol a_2+(z-x-y)\boldsymbol e_3=(x,\ y,\ x+y+z-x-y)^{\mathsf T}=(x,y,z)^{\mathsf T},$$

三个向量拼出了整个 $\mathbb R^3$。系数 $z-x-y$ 是这样想到的：前两个分量只有 $\boldsymbol a_1$、$\boldsymbol a_2$ 能提供，系数只能取 $x$ 和 $y$；这时第三个分量是 $x+y$，离目标还差 $z-x-y$，由 $\boldsymbol e_3$ 补上。

易错点：$\boldsymbol a_1,\boldsymbol a_2,\boldsymbol a_3$ 两两不共线，却只张成平面。有没有多余的向量，要看它能不能由其余的线性表示。

> 设 $\boldsymbol a_1=(1,2,0)^{\mathsf T}$，$\boldsymbol a_2=(0,1,1)^{\mathsf T}$。写出 $(x,y,z)^{\mathsf T}$ 属于它们的张成的条件，并判断 $(2,5,1)^{\mathsf T}$ 在不在里面。
>
> 答案：组合是 $(c_1,\ 2c_1+c_2,\ c_2)^{\mathsf T}$，第一、三个分量定出 $c_1=x$、$c_2=z$，条件是 $y=2x+z$。$(2,5,1)^{\mathsf T}$ 满足 $5=4+1$，它等于 $2\boldsymbol a_1+\boldsymbol a_2$。

**方法 3（看新向量添没添东西）**

往一组向量里加一个新向量时：

1. 用方法 2 判断新向量能不能由原来的向量线性表示；
2. 能，张成不变，新向量是多余的；
3. 不能，张成严格变大，因为新向量在新张成里、不在旧张成里。在 $\mathbb R^3$ 里依次是点、直线、平面、整个空间；为什么每次恰好大一档，L.8 讲维数时说明。

张成可以想成「只许沿这几个方向走能到达的地点」：系数是沿各方向走多远，可以倒着走；能用别的方向走出来的方向，加进来也不会多到一处。这个说法到「走」为止：走路有先后，向量加法可以交换次序。

这种「多余的箭头」到 L.7 会有正式的名字，叫线性相关。

合上书，说出一个非零向量、两个不共线向量在 $\mathbb R^3$ 里各张成什么，再解释加入 $\boldsymbol a_1+\boldsymbol a_2$ 为什么不改变张成。

### 4. 几种原料或几种资产按比例混合，结果落在哪里？

两种饲料原料每 100 克含蛋白质、脂肪的克数分别是 $\boldsymbol p_1=(40,10)^{\mathsf T}$、$\boldsymbol p_2=(10,40)^{\mathsf T}$。按 $\frac23$ 和 $\frac13$ 的比例混合，得到

$$\tfrac23\boldsymbol p_1+\tfrac13\boldsymbol p_2=(30,20)^{\mathsf T}.$$

混合物的成分是原料的线性组合，但系数受两条限制：非负，因为原料不能用负数克；和为 1，因为各原料的占比加起来是全部。

#### 两种原料：一条线段

两种原料能配出哪些成分？设原料 2 占比例 $t$，原料 1 占 $1-t$，$0\le t\le1$。按分配律把 $(1-t)\boldsymbol p_1$ 拆成 $\boldsymbol p_1-t\boldsymbol p_1$，再把含 $t$ 的两项合并：

$$(1-t)\boldsymbol p_1+t\boldsymbol p_2=\boldsymbol p_1+t(\boldsymbol p_2-\boldsymbol p_1).$$

右边读作：从 $\boldsymbol p_1$ 出发，沿指向 $\boldsymbol p_2$ 的箭头 $\boldsymbol p_2-\boldsymbol p_1$ 走它的 $t$ 倍。$t$ 从 0 变到 1，点从 $\boldsymbol p_1$ 走到 $\boldsymbol p_2$，$t=\frac13$ 时到 $(30,20)^{\mathsf T}$。

所以两种原料能配出的，恰好是线段 $\boldsymbol p_1\boldsymbol p_2$ 上的点。$t<0$ 或 $t>1$ 的点在线段两头的延长线上，要用负数克的原料，配不出来。

#### 凸组合的定义

一般地，系数都非负、并且和为 1 的线性组合

$$c_1\boldsymbol a_1+\cdots+c_k\boldsymbol a_k,\qquad c_i\ge0,\quad c_1+\cdots+c_k=1$$

叫作这组向量的**凸组合**。它就是加权平均：两个向量的平均 $\frac12\boldsymbol a+\frac12\boldsymbol b$ 是凸组合，几只基金按比例组合、不卖空时的收益率也是。

两条限制各管一件事，把三种情形并排放在一起就看清了：

| 对系数的限制 | $\boldsymbol p_1,\boldsymbol p_2$ 的全部组合 |
|---|---|
| 没有限制（线性组合） | 张成，这里是整个平面 |
| 只要求和为 1 | 过 $\boldsymbol p_1$、$\boldsymbol p_2$ 的整条直线 |
| 和为 1 并且非负（凸组合） | 线段 $\boldsymbol p_1\boldsymbol p_2$ |

和为 1 把组合收到直线上，非负再把直线截成线段。

#### 三种原料：一个三角形

再加一种原料 $\boldsymbol p_3=(10,10)^{\mathsf T}$。三种原料的凸组合可以分两步混出来：先把原料 2 和原料 3 按 $c_2:c_3$ 混成中间料 $\boldsymbol d$，再把原料 1 和中间料按 $c_1:(c_2+c_3)$ 混合。

下面先说明凸组合都在三角形里，再说明三角形里的点都是凸组合。$c_1=1$ 时另两个权重都是 0，组合就是顶点 $\boldsymbol p_1$，所以只需看 $c_1<1$。

第一步，写出这个拆法。$c_1<1$ 时 $c_2+c_3=1-c_1>0$，令

$$\boldsymbol d=\frac{c_2}{1-c_1}\boldsymbol p_2+\frac{c_3}{1-c_1}\boldsymbol p_3,$$

则 $c_1\boldsymbol p_1+(1-c_1)\boldsymbol d$ 乘开正好是 $c_1\boldsymbol p_1+c_2\boldsymbol p_2+c_3\boldsymbol p_3$。

第二步，看 $\boldsymbol d$ 在哪。它的两个权重非负、和为 $\frac{c_2+c_3}{1-c_1}=1$，是 $\boldsymbol p_2,\boldsymbol p_3$ 的凸组合，所以落在边 $\boldsymbol p_2\boldsymbol p_3$ 上。

第三步，外面一层是 $\boldsymbol p_1$ 和 $\boldsymbol d$ 的凸组合，落在线段 $\boldsymbol p_1\boldsymbol d$ 上。这条线段在三角形里，所以三种原料的凸组合都落在三角形 $\boldsymbol p_1\boldsymbol p_2\boldsymbol p_3$ 里，含边界。

反过来，三角形里的点都配得出来。$\boldsymbol b=\boldsymbol p_1$ 时取权重 $1,0,0$。否则从 $\boldsymbol p_1$ 经过 $\boldsymbol b$ 的射线继续往前，总要在某条边上离开三角形。边 $\boldsymbol p_1\boldsymbol p_2$、$\boldsymbol p_1\boldsymbol p_3$ 所在直线都过 $\boldsymbol p_1$，射线和它们只在 $\boldsymbol p_1$ 相交，除非射线就沿着其中一条边，那时 $\boldsymbol b$ 在这条边上，已是两端点的凸组合。所以离开处 $\boldsymbol d$ 在对边上，$\boldsymbol d=t\boldsymbol p_2+(1-t)\boldsymbol p_3$，$0\le t\le1$。$\boldsymbol d$ 和 $\boldsymbol b$ 在同一条射线上且更远，所以 $\boldsymbol b$ 在线段 $\boldsymbol p_1\boldsymbol d$ 上，$\boldsymbol b=(1-s)\boldsymbol p_1+s\boldsymbol d$，$0\le s\le1$。代入得权重 $1-s$、$st$、$s(1-t)$，都非负，和为 1。

![两种原料配出线段；三种原料先混出边上的 $\boldsymbol d$ 再与 $\boldsymbol p_1$ 混合，凸组合落在三角形里；$(20,20)^{\mathsf T}$ 在内，$(30,30)^{\mathsf T}$ 在外](fig/L1-n1.pdf){width=60%}

线段、三角形里任取两点，连线都留在图形里，没有凹进去的地方，这样的图形叫凸的，「凸组合」由此得名。

#### 一个不用画图的检验

凸组合的每个分量，都夹在各原料这个分量的最小值和最大值之间。以蛋白质为例，三种原料中最高是 40，

$$40c_1+10c_2+10c_3\le40c_1+40c_2+40c_3=40(c_1+c_2+c_3)=40.$$

不等号那一步把每一项放大，用了 $c_i\ge0$；最后一步用了权重和为 1。把 40 换成最小值 10，不等号反过来，同样两步给出下界 10。对任意一个分量、任意多个向量，论证都一样。

**方法 4（解权重，再查符号）**

1. 按方法 2 设系数、按分量列方程，再补上方程 $c_1+\cdots+c_k=1$。
2. 解出权重，检查每个是否非负。
3. 权重唯一时，有一个是负数，$\boldsymbol b$ 就不是凸组合。
4. 权重不唯一时，一组带负数的解说明不了问题。例如平面上四个点配一个目标，三个方程四个权重，留一个参数 $s$，把其余权重写成 $s$ 的式子，再找使它们都 $\ge0$ 的 $s$。

**例 4**　设 $\boldsymbol p_1=(40,10)^{\mathsf T}$，$\boldsymbol p_2=(10,40)^{\mathsf T}$，$\boldsymbol p_3=(10,10)^{\mathsf T}$。(1) $(20,20)^{\mathsf T}$；(2) $(30,30)^{\mathsf T}$ 是不是它们的凸组合？是的话求出权重。

第一步，列方程。设权重 $c_1,c_2,c_3$，目标为 $(x,y)^{\mathsf T}$：

$$40c_1+10c_2+10c_3=x,\qquad 10c_1+40c_2+10c_3=y,\qquad c_1+c_2+c_3=1.$$

第二步，用第三式化简前两式。想让 $c_1+c_2+c_3=1$ 派上用场，就在第一式里凑出它：$40c_1$ 拆成 $30c_1+10c_1$，三项各留一个 10，提出公因数：

$$40c_1+10c_2+10c_3=30c_1+10(c_1+c_2+c_3)=30c_1+10,\qquad c_1=\frac{x-10}{30};$$

第二式同样拆成 $30c_2+10$，所以 $c_2=\frac{y-10}{30}$；最后 $c_3=1-c_1-c_2$。

第三步，代入目标、查符号。

(1) $(x,y)=(20,20)$：$c_1=c_2=c_3=\frac13$，都非负，是凸组合。

(2) $(x,y)=(30,30)$：$c_1=c_2=\frac23$，$c_3=1-\frac43=-\frac13<0$。权重由方程唯一定出，所以不是凸组合；在图 L1-n1 里它落在边 $\boldsymbol p_1\boldsymbol p_2$ 外侧。

它的两个分量都在 10 到 40 之间，却不是凸组合，可见夹逼检验只是必要条件：不满足就一定不是，满足了还要解权重。

> $(25,15)^{\mathsf T}$ 是不是 $\boldsymbol p_1,\boldsymbol p_2,\boldsymbol p_3$ 的凸组合？
>
> 答案：是。$c_1=\frac{25-10}{30}=\frac12$，$c_2=\frac{15-10}{30}=\frac16$，$c_3=1-\frac12-\frac16=\frac13$，都非负。

#### 大模型里的加权平均

大模型把每个词记成一个向量。读到某个词时，模型要让它「看一看」上下文：给参与加权的每个向量一个权重，权重非负、和为 1，再按权重加权平均，得到这个词读过上下文之后的新向量。这一步叫注意力，它的输出正是凸组合。

例 5 是二维的简化模型。真实模型里，参与平均的向量要先由词向量变换出来，权重也要先算出来，这些留到 M.11。

**例 5**　一句话里三个词的向量是 $\boldsymbol h_1=(1,0)^{\mathsf T}$、$\boldsymbol h_2=(3,2)^{\mathsf T}$、$\boldsymbol h_3=(0,4)^{\mathsf T}$。(1) 三个词的权重依次为 $0.5,0.3,0.2$ 时，求注意力的输出；(2) $(2,3)^{\mathsf T}$ 可能是这三个词的注意力输出吗？

(1) 直接按权重加权平均：

$$0.5\boldsymbol h_1+0.3\boldsymbol h_2+0.2\boldsymbol h_3=(0.5+0.9+0,\ 0+0.6+0.8)^{\mathsf T}=(1.4,1.4)^{\mathsf T}.$$

(2) 用方法 4，三个方程是

$$c_1+3c_2=2,\qquad 2c_2+4c_3=3,\qquad c_1+c_2+c_3=1.$$

由第一、三式得 $c_1=2-3c_2$，$c_3=1-c_1-c_2=2c_2-1$。代入第二式：

$$2c_2+4(2c_2-1)=3,\qquad c_2=0.7,\qquad c_3=0.4,\qquad c_1=-0.1.$$

权重唯一而 $c_1<0$，所以不可能。

不论权重怎样取，注意力的输出都落在这几个词向量围成的三角形里，只能在已有的向量之间调和。

合上书，用「两步混合」说明三种原料的凸组合为什么落在三角形里。

### 本章小结

| 方法 | 什么时候用 | 对应题号 |
|---|---|---|
| 方法 1（逐分量运算与移项） | 解含未知向量的一次等式 | L1-01 |
| 方法 2（按分量列方程求组合系数） | 能否拼出、求系数、比较系数 | L1-02、L1-04、L1-08–L1-13 |
| 方法 3（看新向量添没添东西） | 张成的形状、能否张成全空间、哪个向量多余 | L1-03、L1-04、L1-06、L1-07、L1-09、L1-10、L1-12 |
| 方法 4（解权重，再查符号） | 按比例混合、点在不在线段或三角形里 | L1-05、L1-08、L1-11、L1-13、L1-14 |
