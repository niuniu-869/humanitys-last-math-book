## L.3 · 矩阵是线性变换

手机修图时，把照片放大、转个角度、往一边拉斜，软件对每个像素的坐标做的是同一类运算：新坐标的每个分量，都是旧坐标各分量乘上固定的数再相加。神经网络里的全连接层也是这样：输入一串数，输出一串数，每个输出都是全部输入的加权和。这类「把一个向量变成另一个向量」的规则，用一张数表就能完全记下来，这张数表叫作矩阵。

矩阵是从换元里长出来的。18、19 世纪的数学家研究二次式和坐标变换时，常要把旧变量换成新变量，例如 $x=ax'+by'$，$y=cx'+dy'$，而且常要连做两次。把第二次的式子代进第一次，展开、合并，得到的还是一次这样的换元，只是系数变了。

1850 年，西尔维斯特把长方形的数表叫作 matrix。凯莱在 1858 年的《矩阵理论备忘录》里把换元的系数表本身当作运算对象，规定两张表的乘积就是连做两次换元得到的那张表。这样定出的乘法有一个当时让人意外的性质：两次换元先做哪一次，结果可能不同。

本章先把矩阵看成一个动作：把平面里的每个箭头搬到新位置，每条运算规则都从这个动作推出来。第 1–3 节讲矩阵乘向量和线性变换，四个「老朋友」在第 2 节登场，后面每学一个新概念都先拿它们试一试；第 4、5 节由连做两个变换得到乘法和幂；第 6、7 节讲转置和分块。

### 1. 一张数表怎样把一个向量变成另一个向量？

回到 L.1 的礼盒。A 盒装 1 斤苹果、2 斤梨，B 盒装 3 斤苹果、1 斤梨，记作 $\boldsymbol{a}_1=(1,2)^{\mathsf T}$、$\boldsymbol{a}_2=(3,1)^{\mathsf T}$。买 $x_1$ 盒 A、$x_2$ 盒 B，得到的水果是 $x_1\boldsymbol{a}_1+x_2\boldsymbol{a}_2$。

把两个盒子并排成一张表 $A$，买法写成 $\boldsymbol{x}=(x_1,x_2)^{\mathsf T}$，规定「表乘向量」就是以 $\boldsymbol{x}$ 的分量为系数的组合：

$$A=\begin{pmatrix}1&3\\2&1\end{pmatrix},\qquad A\boldsymbol{x}=x_1\begin{pmatrix}1\\2\end{pmatrix}+x_2\begin{pmatrix}3\\1\end{pmatrix}=\begin{pmatrix}x_1+3x_2\\2x_1+x_2\end{pmatrix}.$$

例如 $A(2,1)^{\mathsf T}=(5,5)^{\mathsf T}$，就是买 2 盒 A、1 盒 B 得到的水果。

$m$ 行 $n$ 列的数表叫作 **$m\times n$ 矩阵**。第 $i$ 行第 $j$ 列的数记作 $a_{ij}$，整个矩阵记作 $A=(a_{ij})_{m\times n}$。第 $j$ 列是 $m$ 维向量 $\boldsymbol{a}_j$，所以也写成 $A=(\boldsymbol{a}_1,\dots,\boldsymbol{a}_n)$。行数等于列数时叫 **$n$ 阶方阵**。

对 $\boldsymbol{x}\in\mathbb{R}^n$，规定

$$A\boldsymbol{x}=x_1\boldsymbol{a}_1+x_2\boldsymbol{a}_2+\cdots+x_n\boldsymbol{a}_n .$$

$\boldsymbol{x}$ 的每个分量配 $A$ 的一列，所以 $A$ 的列数必须等于 $\boldsymbol{x}$ 的分量个数。结果是 $m$ 维向量的组合，所以 $A\boldsymbol{x}\in\mathbb{R}^m$。

#### 按行看：点积

礼盒里 $A\boldsymbol{x}$ 的第 2 个分量 $2x_1+x_2$，也可以看成 $A$ 的第 2 行 $(2,1)$ 与 $\boldsymbol{x}$ 的点积（L.2）。一般地，第 $i$ 个分量 $a_{i1}x_1+\cdots+a_{in}x_n$ 就是 $A$ 的第 $i$ 行与 $\boldsymbol{x}$ 的点积。

两种看法算的是同一批乘积 $a_{ij}x_j$，只是一个先竖着加、一个先横着加。记成一句话：**列看组合，行看点积**。

#### 方程组就是 $A\boldsymbol{x}=\boldsymbol{b}$

方程组 $a_{i1}x_1+\cdots+a_{in}x_n=b_i$（$i=1,\dots,m$）的第 $i$ 个左边，正是 $A$ 的第 $i$ 行与 $\boldsymbol{x}$ 的点积，所以整个方程组写成 $A\boldsymbol{x}=\boldsymbol{b}$，$A$ 叫**系数矩阵**。

按列看，它问的是能不能用 $A$ 的各列拼出 $\boldsymbol{b}$：

$$A\boldsymbol{x}=\boldsymbol{b}\ \text{有解}\iff\boldsymbol{b}\ \text{在}\ A\ \text{的各列的张成里},$$

解就是拼法的系数。按行看是找几条直线（平面）的公共点，按列看是问 $\boldsymbol{b}$ 在不在各列张成的直线或平面上，L.4 起会反复对照。

**方法 1（矩阵乘向量）**

1. 先查形状：$A$ 是 $m\times n$，$\boldsymbol{x}$ 必须有 $n$ 个分量，结果有 $m$ 个分量。
2. 计算时按行：第 $i$ 个分量是第 $i$ 行与 $\boldsymbol{x}$ 的点积。
3. 讨论能得到哪些向量、方程组有没有解时按列。

**例 1**　设 $A=\begin{pmatrix}1&2&0\\-1&1&3\end{pmatrix}$，$\boldsymbol{x}=(3,1,-1)^{\mathsf T}$，用两种看法求 $A\boldsymbol{x}$。

先查形状：$A$ 是 $2\times3$，$\boldsymbol{x}$ 有 3 个分量，可以乘，结果有 2 个分量。

按行，两行分别与 $\boldsymbol{x}$ 作点积：

$$1\cdot3+2\cdot1+0\cdot(-1)=5,\qquad (-1)\cdot3+1\cdot1+3\cdot(-1)=-5.$$

按列，三列分别乘 $3,1,-1$ 再相加：

$$3\begin{pmatrix}1\\-1\end{pmatrix}+\begin{pmatrix}2\\1\end{pmatrix}-\begin{pmatrix}0\\3\end{pmatrix}=\begin{pmatrix}5\\-5\end{pmatrix}.$$

两者一致。

> 设 $A=\begin{pmatrix}2&0&1\\1&-1&0\end{pmatrix}$，求 $A(1,2,-1)^{\mathsf T}$。
>
> 答案：按行，$2+0-1=1$，$1-2+0=-1$，结果是 $(1,-1)^{\mathsf T}$。

合上书，写出 $A\boldsymbol{x}$ 按列的定义，再说明它的第 $i$ 个分量为什么是第 $i$ 行与 $\boldsymbol{x}$ 的点积。

### 2. 一个 $2\times2$ 矩阵会把平面上的图形变成什么样？

现在让输入和输出都是平面上的箭头：取 $2\times2$ 矩阵 $A$，把每个点 $\boldsymbol{x}$ 送到 $A\boldsymbol{x}$。整个平面会被怎样搬动？拿第一个老朋友来试：

$$A=\begin{pmatrix}2&1\\1&2\end{pmatrix}.$$

#### 两个基本箭头去了哪里

每个点都能写成 $\boldsymbol{x}=x_1\boldsymbol{e}_1+x_2\boldsymbol{e}_2$，$\boldsymbol{e}_1=(1,0)^{\mathsf T}$，$\boldsymbol{e}_2=(0,1)^{\mathsf T}$（L.1.2），所以先看这两个箭头。按列的定义，$A\boldsymbol{e}_1=1\cdot\boldsymbol{a}_1+0\cdot\boldsymbol{a}_2=\boldsymbol{a}_1$，同样 $A\boldsymbol{e}_2=\boldsymbol{a}_2$。这对任何矩阵都成立：

$$A\boldsymbol{e}_j=A\ \text{的第}\ j\ \text{列}.$$

#### 其余的点跟着走

点 $\boldsymbol{x}=(2,1)^{\mathsf T}=2\boldsymbol{e}_1+\boldsymbol{e}_2$ 是从原点沿 $\boldsymbol{e}_1$ 走两格、再沿 $\boldsymbol{e}_2$ 走一格。按定义，

$$A\boldsymbol{x}=2\boldsymbol{a}_1+\boldsymbol{a}_2=2\begin{pmatrix}2\\1\end{pmatrix}+\begin{pmatrix}1\\2\end{pmatrix}=\begin{pmatrix}5\\4\end{pmatrix},$$

也就是沿第 1 列走两格、再沿第 2 列走一格。步数没变，只是两种步子换成了两列。

所以整张方格纸被一起搬走：正方形网格变成以两列为步子的平行四边形网格，原点不动，单位正方形变成以两列为邻边的平行四边形。

![网格跟着两列走：空心圆 $2\boldsymbol e_1+\boldsymbol e_2$ 被送到实心圆 $2\boldsymbol a_1+\boldsymbol a_2$；点线是走法，阴影是单位正方形和它的像，虚线圆被拉成虚线椭圆](fig/L3-n3.pdf){width=92%}

网格线变完为什么还是等距的平行直线？把系数拆开再合并同类项，得到两条性质：

$$A(\boldsymbol{x}+\boldsymbol{y})=A\boldsymbol{x}+A\boldsymbol{y},\qquad A(k\boldsymbol{x})=k\,A\boldsymbol{x}.$$

于是直线 $\boldsymbol{p}+t\boldsymbol{v}$ 变成 $A\boldsymbol{p}+tA\boldsymbol{v}$：$A\boldsymbol{v}\ne\boldsymbol{0}$ 时仍是直线，方向为 $A\boldsymbol{v}$，$t$ 每增加 1 像就前进一个 $A\boldsymbol{v}$。所以同方向的网格线变完仍同方向、等距排开；只有像下面 ④ 那样把平面压扁时，网格线才会挤到一起。

**方法 2（读列）**

1. 看 $2\times2$ 矩阵把平面怎样变，只看两列：第 1 列是 $\boldsymbol{e}_1$ 的去处，第 2 列是 $\boldsymbol{e}_2$ 的去处。
2. 单位正方形变成以两列为邻边的平行四边形，网格跟着变。
3. 反过来，知道 $\boldsymbol{e}_1,\boldsymbol{e}_2$ 各去哪里，把两个像依次排成列，就得到矩阵。

$3\times3$ 同理，单位正方体变成以三列为棱的平行六面体。

#### 四个老朋友

**① 对称伸缩** $\begin{pmatrix}2&1\\1&2\end{pmatrix}$，就是上面的 $A$，它把单位圆拉成斜放的椭圆。有两个方向值得单独看：

$$A\begin{pmatrix}1\\1\end{pmatrix}=\begin{pmatrix}3\\3\end{pmatrix},\qquad A\begin{pmatrix}-1\\1\end{pmatrix}=\begin{pmatrix}-1\\1\end{pmatrix}.$$

$(1,1)^{\mathsf T}$ 方向不变、长度变成 3 倍，$(-1,1)^{\mathsf T}$ 原地不动，其他方向都被转了一点。这两个「只伸缩、不转向」的方向正是椭圆的两条轴：两方向互相垂直，记单位向量为 $\boldsymbol u_1,\boldsymbol u_2$，单位圆上的点 $\cos t\,\boldsymbol u_1+\sin t\,\boldsymbol u_2$ 被送到 $3\cos t\,\boldsymbol u_1+\sin t\,\boldsymbol u_2$，正是半轴为 3 和 1 的椭圆。L.11 会叫它们特征方向。

**② 剪切** $\begin{pmatrix}1&1\\0&1\end{pmatrix}$。第 1 列说 $\boldsymbol{e}_1$ 不动，第 2 列说 $\boldsymbol{e}_2$ 被推到右边一格。写成坐标是 $(x,y)\mapsto(x+y,\ y)$：高为 $y$ 的水平线整体横移 $y$（$y<0$ 时向左），像推一摞扑克牌，底下一张不动，越往上推得越远。正方形变成同底同高的平行四边形，面积不变，L.6 会用到这一点。

**③ 转 $90^\circ$** $\begin{pmatrix}0&-1\\1&0\end{pmatrix}$。两列说 $\boldsymbol{e}_1$ 转到正上方、$\boldsymbol{e}_2$ 转到正左方：整个平面绕原点逆时针转直角，形状大小不变。和 ① 不同，这里没有一个方向保持不变。

**④ 投影** $\frac12\begin{pmatrix}1&1\\1&1\end{pmatrix}$。两列都是 $(\tfrac12,\tfrac12)^{\mathsf T}$，在直线 $y=x$ 上，两列的任何组合也在这条线上：整个平面被压到直线 $y=x$ 上。

为什么说是垂直地压？看 $\boldsymbol{e}_1$ 和它的像 $(\tfrac12,\tfrac12)^{\mathsf T}$：两者之差 $(\tfrac12,-\tfrac12)^{\mathsf T}$ 与直线方向 $(1,1)^{\mathsf T}$ 的点积是 0，即从 $\boldsymbol{e}_1$ 到像的那一步垂直于直线，所以像是垂足，也就是 L.2 投影公式给出的 $\frac{\boldsymbol{a}\cdot\boldsymbol{e}_1}{\boldsymbol{a}\cdot\boldsymbol{a}}\boldsymbol{a}$（$\boldsymbol{a}=(1,1)^{\mathsf T}$）。$\boldsymbol{e}_2$ 同理。

直线上的 $(1,1)^{\mathsf T}$ 不动，与它垂直的 $(-1,1)^{\mathsf T}$ 被压到原点。不同的点被压到同一处，只看像分不出原来是谁，所以这个变换撤销不了，L.5 会回到这一点。

![读两列就知道平面怎样变：剪切推成平行四边形，转 $90^\circ$ 转过直角，投影压到 $y=x$ 上；虚线是原来的网格和正方形，阴影（投影时是粗线段）是正方形的像，空心圆变到实心圆](fig/L3-n4.pdf){width=95%}

> 仿照 ④，求把平面垂直投影到直线 $\{s(1,2)^{\mathsf T}\}$ 上的矩阵 $H$。
>
> 答案：$\boldsymbol{a}\cdot\boldsymbol{a}=5$，$\boldsymbol{a}\cdot\boldsymbol{e}_1=1$，$\boldsymbol{a}\cdot\boldsymbol{e}_2=2$，两列是 $\frac15(1,2)^{\mathsf T}$、$\frac25(1,2)^{\mathsf T}$，$H=\frac15\begin{pmatrix}1&2\\2&4\end{pmatrix}$。

#### 几种特殊的方阵

还有几种方阵读列一眼就能看懂，后面常用它们的名字。

方阵从左上到右下的线叫**主对角线**，线上的 $a_{ii}$ 叫对角元。主对角线以外全是 0 的方阵叫**对角矩阵** $\operatorname{diag}(\lambda_1,\dots,\lambda_n)$：第 $i$ 列是 $\lambda_i\boldsymbol{e}_i$，所以它把第 $i$ 个坐标方向伸缩 $\lambda_i$ 倍。

对角元全相等时，各方向伸缩同样的倍数，叫**数量矩阵** $kE$；全是 1 时什么都不做，叫**单位矩阵** $E$（也写作 $I$），$E\boldsymbol{x}=\boldsymbol{x}$。

读列还能看出两个反射：$\begin{pmatrix}1&0\\0&-1\end{pmatrix}$ 把 $\boldsymbol{e}_2$ 翻到下方，关于 $x$ 轴；$\begin{pmatrix}0&1\\1&0\end{pmatrix}$ 对调 $\boldsymbol{e}_1,\boldsymbol{e}_2$，关于直线 $y=x$。

**例 2**　求把平面绕原点逆时针旋转 $\theta$ 的矩阵 $R_\theta$，并求 $(2,1)^{\mathsf T}$ 旋转 $90^\circ$ 后的位置。

按方法 2，只要知道 $\boldsymbol{e}_1,\boldsymbol{e}_2$ 转到哪里。

第 1 列：$\boldsymbol{e}_1$ 是单位圆上角度为 0 的点，转到角度 $\theta$ 处，即 $(\cos\theta,\sin\theta)$。

第 2 列：$\boldsymbol{e}_2$ 在角度 $90^\circ$ 处，转到 $\theta+90^\circ$ 处，由诱导公式是 $(-\sin\theta,\cos\theta)$。

排成列：

$$R_\theta=\begin{pmatrix}\cos\theta&-\sin\theta\\\sin\theta&\cos\theta\end{pmatrix},\qquad R_{90^\circ}\begin{pmatrix}2\\1\end{pmatrix}=\begin{pmatrix}0&-1\\1&0\end{pmatrix}\begin{pmatrix}2\\1\end{pmatrix}=\begin{pmatrix}-1\\2\end{pmatrix}.$$

$R_{90^\circ}$ 正是老朋友 ③。检验：$(2,1)\cdot(-1,2)=0$，两者垂直；长度 $\lVert\cdot\rVert$（即高中的 $|\boldsymbol{a}|$）都是 $\sqrt5$。

合上书，说明 $A\boldsymbol{e}_j$ 为什么是第 $j$ 列，再凭读列默写四个老朋友，各说一句它把平面怎样变。

### 3. 哪些变换能写成 $A\boldsymbol{x}$？

随便一种「搬点」的规则都能写成矩阵吗？不能。把每个点右移 1，$T(\boldsymbol{x})=\boldsymbol{x}+(1,0)^{\mathsf T}$，就写不成 $A\boldsymbol{x}$：任何矩阵都有 $A\boldsymbol{0}=\boldsymbol{0}$，而 $T(\boldsymbol{0})\ne\boldsymbol{0}$。能写成 $A\boldsymbol{x}$ 的变换有什么共同点？

#### 线性变换

对每个 $\boldsymbol{x}\in\mathbb{R}^n$ 给出唯一一个 $T(\boldsymbol{x})\in\mathbb{R}^m$ 的规则，叫作**变换** $T:\mathbb{R}^n\to\mathbb{R}^m$，即输入、输出都是向量的函数。如果对任意 $\boldsymbol{x},\boldsymbol{y}$ 和实数 $k$ 都有

$$T(\boldsymbol{x}+\boldsymbol{y})=T(\boldsymbol{x})+T(\boldsymbol{y}),\qquad T(k\boldsymbol{x})=kT(\boldsymbol{x}),$$

就称 $T$ 是**线性变换**，两条分别叫可加性、齐次性。第 2 节验证过 $A\boldsymbol{x}$ 满足这两条，所以每个矩阵都给出一个线性变换。

#### 每个线性变换都是一个矩阵

反过来也对，而且矩阵是现成的。思路是把 $\boldsymbol{x}$ 拆成 $\boldsymbol{e}_j$ 的组合，再用线性把 $T$ 逐项送进去。设 $\boldsymbol{x}=x_1\boldsymbol{e}_1+\cdots+x_n\boldsymbol{e}_n$：

$$T(\boldsymbol{x})\overset{\text{可加}}{=}T(x_1\boldsymbol{e}_1)+\cdots+T(x_n\boldsymbol{e}_n)\overset{\text{齐次}}{=}x_1T(\boldsymbol{e}_1)+\cdots+x_nT(\boldsymbol{e}_n).$$

最后一式是以 $x_1,\dots,x_n$ 为系数组合 $n$ 个向量，按第 1 节的列定义，正是把这些向量排成矩阵再乘 $\boldsymbol{x}$。所以 $T$ 的矩阵是

$$A=\big(T(\boldsymbol{e}_1),\ T(\boldsymbol{e}_2),\ \dots,\ T(\boldsymbol{e}_n)\big),$$

它是 $m\times n$ 的：列数是输入的维数，行数是输出的维数。

取 $\boldsymbol{x}=\boldsymbol{e}_j$ 可知这个矩阵唯一。所以「线性变换」和「矩阵」是一回事，以后两种说法混用。

#### 怎样判断是不是线性的

取 $k=0$ 得 $T(\boldsymbol{0})=\boldsymbol{0}$，所以 $T(\boldsymbol{0})\ne\boldsymbol{0}$ 的一定不是线性的；但只有 $T(\boldsymbol{0})=\boldsymbol{0}$ 还不够。

实际判断时，看每个输出分量能不能写成「输入分量的常数倍之和」：能，就直接写出矩阵；不能（如含常数项、乘积、平方），就按定义检验，找一组具体的数做反例。分段定义的也要按定义验。

**方法 3（写出线性变换的矩阵）**

1. 先确认 $T$ 是线性的。
2. 算出 $T(\boldsymbol{e}_1),\dots,T(\boldsymbol{e}_n)$，依次排成列。
3. 只知道 $T$ 在另外几个向量上的值时，先把每个 $\boldsymbol{e}_j$ 写成这几个向量的组合（设出系数，比较分量解小方程组），再用线性算 $T(\boldsymbol{e}_j)$。这要求它们拼得出每个 $\boldsymbol{e}_j$，在 $\mathbb{R}^2$ 里两个不共线的向量就行（L.1.3）。

**例 3**　$T(x_1,x_2,x_3)=(x_1+2x_2,\ 3x_3-x_1)$。判断它是否线性，并写出矩阵。

两个输出分量都是输入分量的常数倍之和，$T$ 是线性的。三个基本向量的像是

$$T(\boldsymbol{e}_1)=(1,-1),\qquad T(\boldsymbol{e}_2)=(2,0),\qquad T(\boldsymbol{e}_3)=(0,3).$$

排成列，$A=\begin{pmatrix}1&2&0\\-1&0&3\end{pmatrix}$。输入 3 维、输出 2 维，所以是 $2\times3$；把像排成行会得到 $3\times2$，一查形状就知道错了。

> 判断下列变换是否线性，是的写出矩阵：$S(x,y)=(y,\ x-y,\ 2x)$；$U(x,y)=(x+y,\ y+1)$；$V(x,y)=(x^2,\ y)$。
>
> 答案：$S$ 线性，矩阵是 $\begin{pmatrix}0&1\\1&-1\\2&0\end{pmatrix}$。$U(0,0)=(0,1)$，不是。$V$ 保持原点，但 $V(2,0)=(4,0)$，而 $2V(1,0)=(2,0)$，不是。

**例 4**　线性变换 $T:\mathbb{R}^2\to\mathbb{R}^2$ 满足 $T(1,1)=(3,3)$，$T(-1,1)=(-1,1)$。求 $T$ 的矩阵和 $T(2,5)$。

和例 3 不同，这里要先用两个已知向量（不共线）拼出 $\boldsymbol{e}_1,\boldsymbol{e}_2$。

第一步，设 $\boldsymbol{e}_1=c_1(1,1)+c_2(-1,1)$，比较两个分量得 $c_1-c_2=1$，$c_1+c_2=0$，解出 $c_1=\frac12$，$c_2=-\frac12$；$\boldsymbol{e}_2$ 同样解。

$$\boldsymbol{e}_1=\tfrac12(1,1)-\tfrac12(-1,1),\qquad \boldsymbol{e}_2=\tfrac12(1,1)+\tfrac12(-1,1).$$

第二步，用线性把 $T$ 送进去：

$$T(\boldsymbol{e}_1)=\tfrac12(3,3)-\tfrac12(-1,1)=(2,1),\qquad T(\boldsymbol{e}_2)=\tfrac12(3,3)+\tfrac12(-1,1)=(1,2).$$

第三步，排成列得 $\begin{pmatrix}2&1\\1&2\end{pmatrix}$，正是老朋友 ①，$T(2,5)=(9,12)$。

#### 变换的加法和数乘

设 $S,T:\mathbb{R}^n\to\mathbb{R}^m$ 的矩阵是 $A,B$。$(S+T)(\boldsymbol{x})=S(\boldsymbol{x})+T(\boldsymbol{x})$ 仍是线性的，第 $j$ 列是 $\boldsymbol{a}_j+\boldsymbol{b}_j$，所以 $A+B$ 就是同形矩阵对应元素相加；同理 $kA$ 是每个元素乘 $k$。元素全为 0 的矩阵叫**零矩阵** $O$。

合上书，证明「线性变换的矩阵第 $j$ 列是 $T(\boldsymbol{e}_j)$」，指出哪一步用了可加性、哪一步用了齐次性。

### 4. 先做一个变换再做另一个，合起来是哪个矩阵？

把两个老朋友接起来：先转 $90^\circ$（③，记作 $R$），再剪切（②，记作 $S$）。合起来是什么变换，矩阵是什么？

#### 从「连做两次」推出乘法规则

合起来的变换 $\boldsymbol{x}\mapsto S(R\boldsymbol{x})$ 仍是线性的（依次用 $R$、$S$ 的线性），按第 3 节，它的第 $j$ 列是 $\boldsymbol{e}_j$ 最后的去处：

- $\boldsymbol{e}_1$：转后到 $(0,1)^{\mathsf T}$，再剪切 $(x,y)\mapsto(x+y,y)$，到 $(1,1)^{\mathsf T}$；
- $\boldsymbol{e}_2$：转后到 $(-1,0)^{\mathsf T}$，再剪切，仍是 $(-1,0)^{\mathsf T}$。

所以「先转再剪切」的矩阵是 $\begin{pmatrix}1&-1\\1&0\end{pmatrix}$，它的每一列是 $S$ 乘 $R$ 的对应列。

一般地，设 $A=(\boldsymbol{a}_1,\dots,\boldsymbol{a}_n)$ 是 $p\times n$，$B$ 是 $m\times p$。先做 $A$（$\mathbb{R}^n\to\mathbb{R}^p$）再做 $B$（$\mathbb{R}^p\to\mathbb{R}^m$），合起来的矩阵叫作**乘积** $BA$。$\boldsymbol{e}_j$ 先到 $\boldsymbol{a}_j$，再到 $B\boldsymbol{a}_j$，所以

$$BA=(B\boldsymbol{a}_1,\ B\boldsymbol{a}_2,\ \dots,\ B\boldsymbol{a}_n),\qquad (BA)\boldsymbol{x}=B(A\boldsymbol{x}).$$

第一，$BA$ **从右往左读**：先做 $A$ 再做 $B$，和 $f(g(x))$ 先算 $g$ 一样。「先转再剪切」因此记作 $SR$。

第二，形状。$B$ 要接收 $A$ 输出的 $p$ 维向量，写成 $(m\times p)(p\times n)$：内侧两数相等才能乘，外侧两数是结果的形状。

#### 行乘列

$BA$ 的 $(i,j)$ 元是第 $j$ 列 $B\boldsymbol{a}_j$ 的第 $i$ 个分量，按「行看点积」，它是 $B$ 的第 $i$ 行与 $\boldsymbol{a}_j$ 的点积（一行 $p$ 个数和一列 $p$ 个数对应相乘再相加，横写竖写不影响结果）：

$$(BA)_{ij}=b_{i1}a_{1j}+b_{i2}a_{2j}+\cdots+b_{ip}a_{pj}.$$

单看这个「左行乘右列」的公式很随意，其实它是从连做两次变换推出来的。

两种看法也搬到了乘积上：按列，$BA$ 的第 $j$ 列是 $B$ 的各列的组合；按行，$BA$ 的第 $i$ 行是 $B$ 的第 $i$ 行乘 $A$，即 $A$ 的各行以 $b_{i1},\dots,b_{ip}$ 为系数的组合。L.4 用后一种看法记录消元。

**方法 4（矩阵乘法）**

1. 先查形状：左边的列数等于右边的行数才能乘；结果的行数取左边，列数取右边。
2. 逐个元素算：$(i,j)$ 元是左边第 $i$ 行与右边第 $j$ 列的点积。
3. 次序不能随手交换；「先 $A$ 后 $B$」写成 $BA$。

**例 5**　$A=\begin{pmatrix}1&2\\0&1\\-1&3\end{pmatrix}$，$B=\begin{pmatrix}2&0&1\\1&-1&0\end{pmatrix}$，求 $AB$ 与 $BA$。

先查形状：$AB$ 是 $(3\times2)(2\times3)$，结果 $3\times3$；$BA$ 是 $(2\times3)(3\times2)$，结果 $2\times2$。

再逐个元素算，例如 $AB$ 的 $(1,1)$ 元是 $(1,2)$ 与 $(2,1)^{\mathsf T}$ 的点积 4。全部算完：

$$AB=\begin{pmatrix}4&-2&1\\1&-1&0\\1&-3&-1\end{pmatrix},\qquad BA=\begin{pmatrix}1&7\\1&1\end{pmatrix}.$$

> 设 $A=\begin{pmatrix}1&2\\3&4\end{pmatrix}$，$W=\begin{pmatrix}0&1\\1&0\end{pmatrix}$，求 $AW$ 和 $WA$，说出右乘、左乘 $W$ 各起什么作用。
>
> 答案：$AW=\begin{pmatrix}2&1\\4&3\end{pmatrix}$，$WA=\begin{pmatrix}3&4\\1&2\end{pmatrix}$。右乘 $W$ 交换两列，左乘 $W$ 交换两行。

#### 乘法不能交换

换个次序，先剪切再转，即 $RS$：

- $\boldsymbol{e}_1$：剪切后不动，再转到 $(0,1)^{\mathsf T}$；
- $\boldsymbol{e}_2$：剪切后到 $(1,1)^{\mathsf T}$，再转 $(x,y)\mapsto(-y,x)$，到 $(-1,1)^{\mathsf T}$。

所以

$$RS=\begin{pmatrix}0&-1\\1&1\end{pmatrix}\ne\begin{pmatrix}1&-1\\1&0\end{pmatrix}=SR.$$

读到这里多半会觉得别扭：乘法怎么能不交换？因为矩阵乘法记录的是两个动作的先后。剪切只沿水平方向推，转之前推和转之后推，推的是图形上不同的方向。下图用一面不对称的小旗看得最清楚。

![同一面旗，先转 $90^\circ$ 再剪切（上排）旗杆倒在 $x$ 轴上，先剪切再转（下排）旗杆斜向左上，所以 $SR\ne RS$；虚线是原来那面旗的位置](fig/L3-n5.pdf){width=85%}

所以矩阵乘法一般**不能交换**：$AB$ 和 $BA$ 可能一个有定义、一个没有，可能形状不同（例 5），同为方阵也可能不等。$AB=BA$ 时称 $A,B$ **可交换**。

哪些矩阵和剪切可交换？把未知矩阵的元素设成未知数，比较两个乘积。设 $X=\begin{pmatrix}a&b\\c&d\end{pmatrix}$，

$$SX=\begin{pmatrix}a+c&b+d\\c&d\end{pmatrix},\qquad XS=\begin{pmatrix}a&a+b\\c&c+d\end{pmatrix}.$$

令四个位置分别相等：$a+c=a$，$b+d=a+b$，$c=c$，$d=c+d$。第 1、4 个给出 $c=0$，第 2 个给出 $d=a$，第 3 个恒成立。所以与剪切可交换的矩阵恰好是 $\begin{pmatrix}a&b\\0&a\end{pmatrix}$。

#### 结合律和分配律还在

交换律没有了，其余运算律都在。

最重要的是**结合律** $(CB)A=C(BA)$：两边都是「先 $A$，再 $B$，再 $C$」，只是分组不同。让两边作用在同一个 $\boldsymbol{x}$ 上，每一步只用定义 $(BA)\boldsymbol{x}=B(A\boldsymbol{x})$：

$$\big((CB)A\big)\boldsymbol{x}=(CB)(A\boldsymbol{x})=C\big(B(A\boldsymbol{x})\big),\qquad \big(C(BA)\big)\boldsymbol{x}=C\big((BA)\boldsymbol{x}\big)=C\big(B(A\boldsymbol{x})\big).$$

取 $\boldsymbol{x}=\boldsymbol{e}_j$ 知两边各列相同，所以相等。以后连乘不写括号，先算哪两个都行，只要不改变左右次序。

**分配律** $B(A_1+A_2)=BA_1+BA_2$、$(B_1+B_2)A=B_1A+B_2A$ 以及 $k(BA)=(kB)A=B(kA)$，按行乘列逐个元素展开即可验证，因为每个元素都是实数乘积之和，实数的分配律逐项成立。

单位矩阵什么都不做，所以 $EA=AE=A$。

#### 两个非零矩阵相乘可以得零

老朋友 ④ 记作 $H_1$；同样的办法，垂直压到直线 $y=-x$ 上的矩阵是 $H_2=\frac12\begin{pmatrix}1&-1\\-1&1\end{pmatrix}$。先做 $H_2$，点都落到 $y=-x$ 上，这条线与 $y=x$ 垂直，再做 $H_1$ 就全压到原点：

$$H_1H_2=\frac14\begin{pmatrix}1-1&-1+1\\1-1&-1+1\end{pmatrix}=O.$$

两个非零矩阵，乘积却是 $O$。和实数对照：

| 规律 | 实数 | 矩阵 |
|---|---|---|
| $ab=ba$ | 成立 | 一般不成立（$SR\ne RS$） |
| $ab=0\Rightarrow a=0$ 或 $b=0$ | 成立 | 不成立（$H_1H_2=O$） |
| $ab=ac$，$a\ne0\Rightarrow b=c$ | 成立 | 不成立（$H_1H_2=H_1O$，但 $H_2\ne O$） |

$H_1$ 不能从两边「约掉」，因为它把不同的向量压到同一处，丢了信息。哪些矩阵能约掉，L.5 的逆矩阵来回答。

**例 6**　神经网络的**全连接层**把每个输出算成全部输入的加权和再加常数，即 $\boldsymbol{y}=W\boldsymbol{x}+\boldsymbol{b}$。设常数为 $\boldsymbol{0}$，第一层 $W_1=\begin{pmatrix}1&0&-1\\2&1&0\end{pmatrix}$，第二层 $W_2=\begin{pmatrix}1&1\\1&-1\end{pmatrix}$。求输入 $\boldsymbol{x}=(1,2,3)^{\mathsf T}$ 的输出，并说明两层合起来等于一层。

第一步，逐层算：

$$W_1\boldsymbol{x}=\begin{pmatrix}1-3\\2+2\end{pmatrix}=\begin{pmatrix}-2\\4\end{pmatrix},\qquad W_2\begin{pmatrix}-2\\4\end{pmatrix}=\begin{pmatrix}2\\-6\end{pmatrix}.$$

第二步，由结合律 $W_2(W_1\boldsymbol{x})=(W_2W_1)\boldsymbol{x}$，先把两层乘成一个矩阵：

$$W_2W_1=\begin{pmatrix}3&1&-1\\-1&-1&-1\end{pmatrix},\qquad (W_2W_1)\boldsymbol{x}=\begin{pmatrix}3+2-3\\-1-2-3\end{pmatrix}=\begin{pmatrix}2\\-6\end{pmatrix}.$$

结果一样，两层只等于一个 $2\times3$ 的层；有常数时，由分配律合起来也只是「一个矩阵乘 $\boldsymbol{x}$ 再加常数」。叠一百层也只等于一层，所以真实网络在层与层之间对每个分量做一次非线性加工（例如把负数换成 0），M.7 再讲。

合上书，从「$BA$ 的第 $j$ 列是 $B\boldsymbol{a}_j$」推出行乘列，再用剪切和转 $90^\circ$ 说明 $AB$ 为什么可以不等于 $BA$。

### 5. 同一个变换连做 $k$ 次是什么？

老朋友 ③ 连转 4 次回到原位，即 $R$ 自乘 4 次等于 $E$。剪切连做 $k$ 次、投影连做两次又是什么？能不能不硬乘就看出来？

#### 方阵的幂

输出要能当下一次的输入，所以只有方阵能连做。设 $A$ 是 $n$ 阶方阵，规定 $A^k=AA\cdots A$（$k$ 个），$A^0=E$。由结合律，对非负整数 $k,l$ 有 $A^kA^l=A^{k+l}$，$(A^k)^l=A^{kl}$。

但 $(AB)^k=A^kB^k$ 一般不成立：$(AB)^2=ABAB$，要变成 $AABB$，得把中间的 $BA$ 换成 $AB$，这需要可交换。

#### 三种求幂的办法

第一种看几何。转 $\theta$ 连做 $k$ 次就是转 $k\theta$，$R_\theta^k=R_{k\theta}$；投影一次后点已在直线上，再投影不动，所以投影的平方等于它自己；剪切把高为 $y$ 的水平线横移 $y$，连做 $k$ 次横移 $ky$，所以

$$\begin{pmatrix}1&1\\0&1\end{pmatrix}^k=\begin{pmatrix}1&k\\0&1\end{pmatrix}.$$

第二种是猜规律再用归纳法（Z.4.5）证明。第三种用二项式定理，但要先弄清什么时候能用。

#### 二项式定理什么时候能用

按分配律展开并保持次序：

$$(A+B)^2=A^2+AB+BA+B^2.$$

只有 $AB=BA$ 时中间两项才能合并成 $2AB$。

不可交换时确实会错：取 $A=\begin{pmatrix}1&0\\0&0\end{pmatrix}$，$B=\begin{pmatrix}0&1\\0&0\end{pmatrix}$，算得 $A^2=A$，$B^2=O$，$AB=B$，$BA=O$，于是 $(A+B)^2=A+B$，而 $A^2+2AB+B^2=A+2B$。

$A,B$ 可交换时，把展开式每一项里的 $B$ 用 $AB=BA$ 逐个与左边的 $A$ 交换，含 $k$ 个 $B$ 的 $\mathrm{C}_n^k$ 项就都等于 $A^{n-k}B^k$，二项式定理（Z.5.6，$\mathrm{C}_n^k$ 是组合数）照样成立：

$$(A+B)^n=\sum_{k=0}^{n}\mathrm{C}_n^k\,A^{n-k}B^k\qquad(AB=BA).$$

#### 拆成 $\lambda E+N$

什么拆法一定可交换？$\lambda E$ 和任何同阶方阵都可交换，因为 $(\lambda E)X=\lambda X=X(\lambda E)$。所以对角元全是 $\lambda$ 的上三角矩阵可以拆成 $\lambda E+N$，$N$ 的主对角线及其下方全是 0，叫**严格上三角矩阵**。

这样拆的好处是 $N$ 自乘几次就变成 $O$。读列：$N\boldsymbol{e}_j$ 是 $\boldsymbol{e}_1,\dots,\boldsymbol{e}_{j-1}$ 的组合，每乘一次 $N$ 下标至少降 1，$n$ 阶时降 $n$ 次必然降没了：

$$N^n=O\qquad(N\ \text{是}\ n\ \text{阶严格上三角矩阵}).$$

**方法 5（拆成 $\lambda E+N$ 用二项式定理）**

1. 写成 $A=\lambda E+N$：$\lambda$ 取对角元，$N=A-\lambda E$。只适用于对角元全相等的三角矩阵，一般方阵的幂见 L.12。
2. 依次算 $N^2,N^3,\dots$，算到第一次出现 $O$ 为止（$n$ 阶时最多到 $N^n$）。
3. 按二项式定理展开，只保留 $N$ 的非零幂；依据是 $\lambda E$ 与 $N$ 可交换。

**例 7**　$A=\begin{pmatrix}2&1&0\\0&2&1\\0&0&2\end{pmatrix}$，求 $A^n$（整数 $n\ge2$）。

第一步，拆成 $A=2E+N$，$N=\begin{pmatrix}0&1&0\\0&0&1\\0&0&0\end{pmatrix}$。

第二步，读列：$N\boldsymbol{e}_1=\boldsymbol{0}$，$N\boldsymbol{e}_2=\boldsymbol{e}_1$，$N\boldsymbol{e}_3=\boldsymbol{e}_2$，每乘一次下标降 1。

连乘两次：$\boldsymbol{e}_3\to\boldsymbol{e}_2\to\boldsymbol{e}_1$，另外两个都到了 $\boldsymbol{0}$；再乘一次全是 $\boldsymbol{0}$。所以

$$N^2=\begin{pmatrix}0&0&1\\0&0&0\\0&0&0\end{pmatrix},\qquad N^3=O.$$

第三步，$2E$ 与 $N$ 可交换，按二项式定理展开，$N^3$ 及以后的项都是 $O$：

$$A^n=2^nE+\mathrm{C}_n^1\,2^{n-1}N+\mathrm{C}_n^2\,2^{n-2}N^2=\begin{pmatrix}2^n&n2^{n-1}&n(n-1)2^{n-3}\\0&2^n&n2^{n-1}\\0&0&2^n\end{pmatrix},$$

其中 $\mathrm{C}_n^2\,2^{n-2}=\frac{n(n-1)}2\,2^{n-2}=n(n-1)2^{n-3}$。

> 求 $\begin{pmatrix}-1&2\\0&-1\end{pmatrix}^n$。
>
> 答案：写成 $-E+N$，$N=\begin{pmatrix}0&2\\0&0\end{pmatrix}$，$N^2=O$，结果是 $(-1)^nE+n(-1)^{n-1}N=\begin{pmatrix}(-1)^n&2n(-1)^{n-1}\\0&(-1)^n\end{pmatrix}$。

#### 矩阵多项式

$f(x)=a_mx^m+\cdots+a_1x+a_0$ 时，规定**矩阵多项式** $f(A)=a_mA^m+\cdots+a_1A+a_0E$。常数项要乘 $E$，否则数没法和矩阵相加。

同一个 $A$ 的各次幂彼此可交换，所以数的多项式恒等式对 $f(A)$ 照样成立，例如 $A^2-3A+2E=(A-E)(A-2E)$。两个不同的矩阵就不行：$(A+B)(A-B)$ 展开多出 $BA-AB$。

**例 8**　$A=\begin{pmatrix}1&-1\\2&4\end{pmatrix}$。(1) 求 $A^2-5A+6E$；(2) 把 $A^3$ 写成 $aA+bE$ 的形式。

(1) 按行乘列，

$$A^2=\begin{pmatrix}1-2&-1-4\\2+8&-2+16\end{pmatrix}=\begin{pmatrix}-1&-5\\10&14\end{pmatrix},\qquad A^2-5A+6E=\begin{pmatrix}-1-5+6&-5+5\\10-10&14-20+6\end{pmatrix}=O.$$

(2) 和例 7 不同，$A$ 不是三角矩阵，改用 (1) 的关系降次。由 $A^2=5A-6E$，两边左乘 $A$，再把出现的 $A^2$ 换掉：

$$A^3=5A^2-6A=5(5A-6E)-6A=19A-30E=\begin{pmatrix}-11&-19\\38&46\end{pmatrix}.$$

$A$ 为什么满足这个二次式，L.11 讲特征多项式时说明。

合上书，说出 $(A+B)^2$ 为什么一般不等于 $A^2+2AB+B^2$，再说明 $2E+N$ 为什么能用二项式定理，$N$ 最多自乘几次变成 $O$。

### 6. 把矩阵的行和列对调，乘法规则怎么变？

#### 转置

$m\times n$ 矩阵 $A$ 的**转置** $A^{\mathsf T}$ 是 $n\times m$ 矩阵，$(A^{\mathsf T})_{ij}=a_{ji}$：$A$ 的第 $i$ 行变成 $A^{\mathsf T}$ 的第 $i$ 列。例如

$$\begin{pmatrix}1&2&3\\4&5&6\end{pmatrix}^{\mathsf T}=\begin{pmatrix}1&4\\2&5\\3&6\end{pmatrix}.$$

逐个元素看，$(A^{\mathsf T})^{\mathsf T}=A$，$(A+B)^{\mathsf T}=A^{\mathsf T}+B^{\mathsf T}$，$(kA)^{\mathsf T}=kA^{\mathsf T}$。

#### 乘积的转置

自然的猜测是 $A^{\mathsf T}B^{\mathsf T}$。拿老朋友试：$(SR)^{\mathsf T}=\begin{pmatrix}1&1\\-1&0\end{pmatrix}$，而

$$S^{\mathsf T}R^{\mathsf T}=\begin{pmatrix}1&0\\1&1\end{pmatrix}\begin{pmatrix}0&1\\-1&0\end{pmatrix}=\begin{pmatrix}0&1\\-1&1\end{pmatrix},\qquad R^{\mathsf T}S^{\mathsf T}=\begin{pmatrix}0&1\\-1&0\end{pmatrix}\begin{pmatrix}1&0\\1&1\end{pmatrix}=\begin{pmatrix}1&1\\-1&0\end{pmatrix}.$$

猜错了，对的是倒过来的 $R^{\mathsf T}S^{\mathsf T}$。一般地

$$(AB)^{\mathsf T}=B^{\mathsf T}A^{\mathsf T}.$$

证明的思路是把两边的 $(i,j)$ 元化成同一个点积。

左边：$(AB)^{\mathsf T}$ 的 $(i,j)$ 元是 $AB$ 的 $(j,i)$ 元，即 $A$ 的第 $j$ 行与 $B$ 的第 $i$ 列的点积。

右边：$B^{\mathsf T}A^{\mathsf T}$ 的 $(i,j)$ 元是 $B^{\mathsf T}$ 的第 $i$ 行与 $A^{\mathsf T}$ 的第 $j$ 列的点积；由转置的定义，前者就是 $B$ 的第 $i$ 列（横过来写），后者就是 $A$ 的第 $j$ 行（竖过来写）。

点积与次序无关，两边相等。三个矩阵时把 $AB$ 看成整体：$(ABC)^{\mathsf T}=C^{\mathsf T}(AB)^{\mathsf T}=C^{\mathsf T}B^{\mathsf T}A^{\mathsf T}$。转置穿过乘积，次序整个倒过来。

#### 对称矩阵与反对称矩阵

$A^{\mathsf T}=A$ 的方阵叫**对称矩阵**，$a_{ij}=a_{ji}$。老朋友 ① 和 ④ 是对称的，② 不是。L.13 会说明，实对称矩阵总是沿几条互相垂直的方向伸缩（倍数为负时反向），① 的两个特殊方向正好垂直。

$A^{\mathsf T}=-A$ 的方阵叫**反对称矩阵**。由 $a_{ii}=-a_{ii}$ 得对角元全是 0。老朋友 ③ 就是一个：它的转置 $\begin{pmatrix}0&1\\-1&0\end{pmatrix}$ 正好是它的相反数。

**方法 6（用转置的运算律判断对称）**

1. 要证 $M$ 对称，就算 $M^{\mathsf T}$。
2. 用 $(AB)^{\mathsf T}=B^{\mathsf T}A^{\mathsf T}$ 等运算律一层层拆开，再代入已知条件（如 $A^{\mathsf T}=A$）。
3. 看能否回到 $M$；证反对称，就看能否得到 $-M$。

**例 9**　(1) 证明对任意 $m\times n$ 矩阵 $A$，$A^{\mathsf T}A$ 对称；(2) 设 $A,B$ 是同阶对称矩阵，证明 $AB$ 对称当且仅当 $AB=BA$。

(1) 先用乘积的转置倒序，再用 $(A^{\mathsf T})^{\mathsf T}=A$：

$$(A^{\mathsf T}A)^{\mathsf T}=A^{\mathsf T}(A^{\mathsf T})^{\mathsf T}=A^{\mathsf T}A.$$

(2) 这次要用已知条件 $A^{\mathsf T}=A$，$B^{\mathsf T}=B$：

$$(AB)^{\mathsf T}=B^{\mathsf T}A^{\mathsf T}=BA.$$

于是「$AB$ 对称」即 $(AB)^{\mathsf T}=AB$，也就是 $BA=AB$。两个说法是同一个等式，两个方向一起得证。

> 把 $A=\begin{pmatrix}1&4\\2&3\end{pmatrix}$ 写成一个对称矩阵与一个反对称矩阵之和。
>
> 答案：设 $A=K_1+K_2$，转置得 $A^{\mathsf T}=K_1-K_2$，所以 $K_1=\frac12(A+A^{\mathsf T})=\begin{pmatrix}1&3\\3&3\end{pmatrix}$，$K_2=\frac12(A-A^{\mathsf T})=\begin{pmatrix}0&1\\-1&0\end{pmatrix}$。

#### 三角矩阵的乘积

主对角线下方全是 0 的方阵叫**上三角矩阵**，上方全是 0 的叫**下三角矩阵**。两个同阶上三角矩阵相乘，结果仍是上三角的，对角元是对应对角元之积。

看下标。$(AB)_{ij}=\sum_k a_{ik}b_{kj}$ 中，$a_{ik}$ 只在 $k\ge i$ 时可能非零，$b_{kj}$ 只在 $k\le j$ 时可能非零，所以非零项要求 $i\le k\le j$。$i>j$ 时这样的 $k$ 不存在，$(AB)_{ij}=0$；$i=j$ 时只有 $k=i$，得 $a_{ii}b_{ii}$。下三角的情形转置一下就化成上三角。

合上书，逐个元素推出 $(AB)^{\mathsf T}=B^{\mathsf T}A^{\mathsf T}$，再用 $S,R$ 说明 $A^{\mathsf T}B^{\mathsf T}$ 为什么不对。

### 7. 大矩阵怎样切成小块来乘？

求 $M=\begin{pmatrix}1&1&0&0\\0&1&0&0\\0&0&2&0\\0&0&1&2\end{pmatrix}$ 的 $n$ 次幂。$M$ 的右上、左下两块全是 0，读列可知前两个坐标和后两个坐标各管各的，像两个 $2\times2$ 的变换并排放着。能不能当成两个小矩阵来算？

#### 分块乘法

用横线和竖线把矩阵切开，每一块叫**子块**，切好的矩阵叫**分块矩阵**。把 $M$ 在第 2 行、第 2 列之后切开：

$$M=\begin{pmatrix}A_1&O\\O&A_2\end{pmatrix},\qquad A_1=\begin{pmatrix}1&1\\0&1\end{pmatrix},\quad A_2=\begin{pmatrix}2&0\\1&2\end{pmatrix}.$$

**分块乘法**是把子块当作元素照行乘列相乘，条件是左边的列在哪里切，右边的行就在同样的位置切，这样对应子块的形状对得上；子块是矩阵，次序不能换。

为什么成立？看最简单的切法：$A$（$m\times p$）竖着切成 $(C_1\ \ C_2)$，$C_1$ 是前 $s$ 列；$B$（$p\times n$）横着切成 $\begin{pmatrix}D_1\\D_2\end{pmatrix}$，$D_1$ 是前 $s$ 行。行乘列的和按 $k\le s$ 与 $k>s$ 分成两段：

$$(AB)_{ij}=\underbrace{\sum_{k=1}^{s}a_{ik}b_{kj}}_{C_1D_1\ \text{的}\ (i,j)\ \text{元}}+\underbrace{\sum_{k=s+1}^{p}a_{ik}b_{kj}}_{C_2D_2\ \text{的}\ (i,j)\ \text{元}},$$

因为前一段只用到 $A$ 的前 $s$ 列和 $B$ 的前 $s$ 行。所以 $(C_1\ \ C_2)\begin{pmatrix}D_1\\D_2\end{pmatrix}=C_1D_1+C_2D_2$。切更多刀时，和式按同样的位置分成更多段，每段是一对子块的乘积。

最常用的是**分块对角矩阵**。按分块乘法，非对角位置都是含 $O$ 的乘积之和，两块互不干扰：

$$\begin{pmatrix}A_1&O\\O&A_2\end{pmatrix}\begin{pmatrix}B_1&O\\O&B_2\end{pmatrix}=\begin{pmatrix}A_1B_1&O\\O&A_2B_2\end{pmatrix},\qquad M^n=\begin{pmatrix}A_1^n&O\\O&A_2^n\end{pmatrix}.$$

$A_1$ 是老朋友 ② 剪切，第 5 节已得 $A_1^n=\begin{pmatrix}1&n\\0&1\end{pmatrix}$。$A_2=2E+N$，$N=\begin{pmatrix}0&0\\1&0\end{pmatrix}$，读列知 $N^2=O$；方法 5 只用到 $2E$ 与 $N$ 可交换，$N$ 在下三角也照样能用：$A_2^n=2^nE+n2^{n-1}N=\begin{pmatrix}2^n&0\\n2^{n-1}&2^n\end{pmatrix}$。

#### 外积

分块的一种极端是左边切成一列一列、右边切成一行一行。先看最小的情形：列向量 $\boldsymbol{a}$（$m\times1$）乘行向量 $\boldsymbol{b}^{\mathsf T}$（$1\times n$），内侧维数都是 1，得到 $m\times n$ 矩阵 $\boldsymbol{a}\boldsymbol{b}^{\mathsf T}$，$(i,j)$ 元是 $a_ib_j$，叫作**外积**。例如

$$\begin{pmatrix}1\\2\\3\end{pmatrix}(1,\ -1,\ 1)=\begin{pmatrix}1&-1&1\\2&-2&2\\3&-3&3\end{pmatrix},$$

每一行都是 $(1,-1,1)$ 的倍数，倍数依次是 $\boldsymbol{a}$ 的分量。和点积并排对照：

| | 点积 $\boldsymbol{a}^{\mathsf T}\boldsymbol{b}$ | 外积 $\boldsymbol{a}\boldsymbol{b}^{\mathsf T}$ |
|---|---|---|
| 形状 | $(1\times m)(m\times1)$，要求同维 | $(m\times1)(1\times n)$，不要求同维 |
| 结果 | 一个数 $\sum_i a_ib_i$ | 一张 $m\times n$ 的表，$(i,j)$ 元 $a_ib_j$ |

两者只差转置号的位置，先看清它在左还是在右。

**方法 7（分块与外积）**

1. 有成块的 0 时按块切开，把子块当元素来乘；先核对左边列的切法与右边行的切法一致。
2. 每一行都是同一行的倍数时，写成外积 $\boldsymbol{\alpha}\boldsymbol{\beta}^{\mathsf T}$。
3. 求幂时用结合律，把中间的 $\boldsymbol{\beta}^{\mathsf T}\boldsymbol{\alpha}$ 先算成一个数。

**例 10**　$A=\begin{pmatrix}1&-1&1\\2&-2&2\\3&-3&3\end{pmatrix}$，求 $A^n$。

$A$ 没有成块的 0，但三行依次是 $(1,-1,1)$ 的 1、2、3 倍，正是上面那个外积：$A=\boldsymbol{\alpha}\boldsymbol{\beta}^{\mathsf T}$，$\boldsymbol{\alpha}=(1,2,3)^{\mathsf T}$，$\boldsymbol{\beta}=(1,-1,1)^{\mathsf T}$。

由结合律，先把中间两个乘起来：

$$A^2=\boldsymbol{\alpha}(\boldsymbol{\beta}^{\mathsf T}\boldsymbol{\alpha})\boldsymbol{\beta}^{\mathsf T}=2\,\boldsymbol{\alpha}\boldsymbol{\beta}^{\mathsf T}=2A.$$

中间的 $\boldsymbol{\beta}^{\mathsf T}\boldsymbol{\alpha}=1-2+3=2$ 是 $1\times1$ 的，就是一个数，数乘放在哪里都一样，所以能挪到最前面。每多乘一个 $A$ 就多出一个 2，所以

$$A^n=2^{n-1}A.$$

这个数 $\sum_i\alpha_i\beta_i$ 正好是 $A$ 的对角元之和，可以直接读出。

> 求 $\begin{pmatrix}1&2\\3&6\end{pmatrix}^n$。
>
> 答案：第二行是第一行的 3 倍，$A=(1,3)^{\mathsf T}(1,2)$，$\boldsymbol{\beta}^{\mathsf T}\boldsymbol{\alpha}=1+6=7$，所以 $A^n=7^{n-1}A$。

#### 乘积是外积之和

一般的乘积是几个外积之和。把 $A$（$m\times p$）按列切成 $\boldsymbol{a}_1,\dots,\boldsymbol{a}_p$，$B$（$p\times n$）按行切成 $\boldsymbol{b}_1^{\mathsf T},\dots,\boldsymbol{b}_p^{\mathsf T}$。

这是 $C_1D_1+C_2D_2$ 切到最细：和式每段只有一个 $k$，于是

$$AB=\boldsymbol{a}_1\boldsymbol{b}_1^{\mathsf T}+\boldsymbol{a}_2\boldsymbol{b}_2^{\mathsf T}+\cdots+\boldsymbol{a}_p\boldsymbol{b}_p^{\mathsf T}.$$

核对一个元素：$\boldsymbol{a}_k\boldsymbol{b}_k^{\mathsf T}$ 的 $(i,j)$ 元是 $a_{ik}b_{kj}$，对 $k$ 求和正是行乘列。

合上书，写出外积展开并用一个元素验证，再说明例 10 哪一步用了结合律。

### 本章小结

| 方法 | 什么时候用 | 对应题号 |
|---|---|---|
| 方法 1（矩阵乘向量） | 算 $A\boldsymbol{x}$；判断方程组有没有解 | L3-01 |
| 方法 2（读列） | 看平面怎样变；由 $\boldsymbol{e}_j$ 的去处写矩阵 | L3-02、L3-12、L3-13、L3-15 |
| 方法 3（写出线性变换的矩阵） | 判断线性；由几个向量的像求矩阵 | L3-03、L3-05、L3-14 |
| 方法 4（矩阵乘法） | 复合变换；可交换与零因子 | L3-04、L3-06、L3-11 |
| 方法 5（拆成 $\lambda E+N$ 用二项式定理） | 求方阵的幂；矩阵多项式与降次 | L3-07、L3-08、L3-12 |
| 方法 6（用转置的运算律判断对称） | 对称与反对称、三角矩阵 | L3-09、L3-11、L3-13、L3-15 |
| 方法 7（分块与外积） | 分块对角、每行成比例时求幂 | L3-10、L3-12 |
