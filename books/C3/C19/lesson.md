## C.19 · 空间向量与解析几何

玩 3D 游戏时，画面里的物体都由成千上万个小三角形拼成。引擎在每一帧要判断：每个小三角形朝向屏幕还是背对屏幕，该画得多亮。做法是给它配一个垂直于它的箭头（法向量），再和从它指向摄像机的箭头算一个数，用正负判断摄像机在它的哪一侧。搜索和推荐系统比较两段文字像不像，也是把每段文字变成一串数，再算两串数夹角的余弦。这些运算的共同语言，就是本章的空间坐标和向量。

笛卡儿等人用坐标把几何问题变成代数问题：给平面上的点两个数，曲线就成了方程。但坐标只说一个点在哪里，说不出一段位移朝向哪边，也说不出两个方向有多一致。向量补上了这一环。哈密顿在尝试把复数推广到三维时发展了四元数；后来，吉布斯等人把计算中常用的运算单独整理出来：**数量积**回答「两个方向有多一致」，**向量积**回答「同时垂直于两个方向的方向是哪一个」。

本章的次序是：第 1–3 节建立坐标、向量和长度；第 4、5、6 节依次讲数量积、向量积和混合积，第 7 节用它们写出平面的方程；第 8–10 节写直线，判断位置关系，算点到直线的距离；第 11–13 节看一个方程画出什么曲面；第 14、15 节写空间曲线和它的投影。后面画二元函数的图像、写切平面，都在这套语言里进行。

本章的老朋友：三个点 $A(1,0,0)$、$B(0,2,0)$、$C(0,0,3)$，各落在一条坐标轴上，围成一个三角形；两个向量 $\boldsymbol a=(1,2,2)$、$\boldsymbol b=(3,0,4)$，长度恰好是 3 和 5。每学一种新运算，都先拿它们试一试，最后汇成一张表。

### 1. 空间里的一个位置，怎样用三个数记下来？

选房间的一个墙角作原点 $O$，沿两条墙脚线和竖直的墙角线各画一条数轴，叫 $x$ 轴、$y$ 轴、$z$ 轴。三条轴两两垂直，并约定**右手法则**：右手四指从 $x$ 轴正向弯向 $y$ 轴正向时，拇指指向 $z$ 轴正向。这样得到的叫**空间直角坐标系**。

给定一点 $P$，过 $P$ 作三个平面，分别垂直于 $x$ 轴、$y$ 轴、$z$ 轴。它们与各自那条轴的交点的读数依次是 $x$、$y$、$z$，记作 $P(x,y,z)$。反过来，三个数也确定唯一的点。三条轴两两确定三个**坐标面**：$xOy$ 面（$z=0$）、$yOz$ 面（$x=0$）、$zOx$ 面（$y=0$）。

下一个问题是两点相距多远：平面上的距离公式来自勾股定理，空间里再用一次。

设 $P_1(x_1,y_1,z_1)$、$P_2(x_2,y_2,z_2)$。以线段 $P_1P_2$ 为对角线，作各棱平行于坐标轴的长方体，三条棱长是 $|x_2-x_1|$、$|y_2-y_1|$、$|z_2-z_1|$（这里的 $|\cdot|$ 是数的绝对值；用 $d(P_1,P_2)$ 记两点的距离，是为了把竖线留给绝对值）。

![以 $P_1P_2$ 为体对角线的长方体：底面对角线 $P_1Q$（虚线）的平方是前两条棱的平方和，它与竖直的棱垂直，再用一次勾股定理。图中取 $P_1$ 为原点，$3,2,4$ 只是一组示例，一般情形平移即可](fig/C19-n1.pdf){width=62%}

第一步，设 $Q(x_2,y_2,z_1)$，它是底面上与 $P_1$ 相对的顶点，底面的对角线 $P_1Q$ 是底面直角三角形的斜边：

$$d(P_1,Q)^2=(x_2-x_1)^2+(y_2-y_1)^2.$$

第二步，$P_1Q$ 在底面上，竖直的棱 $QP_2$ 垂直于底面，所以 $\triangle P_1QP_2$ 是直角三角形，$P_1P_2$ 是斜边：

$$d(P_1,P_2)=\sqrt{(x_2-x_1)^2+(y_2-y_1)^2+(z_2-z_1)^2}.$$

**方法 1（坐标与距离）**

1. 位置一律写成坐标；
2. 与距离有关的条件，代入距离公式，两边平方去掉根号再列方程；
3. 点在某条坐标轴或坐标面上时，先把为 0 的坐标写进去。

**例 1**　老朋友 $A(1,0,0)$、$B(0,2,0)$、$C(0,0,3)$，求三角形 $ABC$ 的三边长。

先在三个老朋友点上用一次距离公式，看这个三角形的三条边各有多长。

三个点各落在一条坐标轴上，坐标差里总有 0：

$$d(A,B)^2=1+4+0=5,\qquad d(B,C)^2=0+4+9=13,\qquad d(A,C)^2=1+0+9=10.$$

三边长是 $\sqrt5$、$\sqrt{13}$、$\sqrt{10}$，最长边的平方 13 不等于另两边的平方和 $5+10=15$，所以不是直角三角形。

> 求 $A(1,2,3)$ 与 $B(4,-2,15)$ 的距离。
>
> 答案：坐标差是 $(3,-4,12)$，$d(A,B)=\sqrt{9+16+144}=13$。

**例 2**　在 $z$ 轴上求一点 $P$，使它到 $M(1,0,2)$ 和 $N(0,1,-1)$ 的距离相等。

和例 1 不同，这次有一个点是未知的，但它在 $z$ 轴上，横、纵坐标都是 0，所以设 $P(0,0,z)$。距离相等就是距离的平方相等：

$$1+(z-2)^2=1+(z+1)^2 ,\qquad -4z+4=2z+1 ,$$

解得 $z=\frac12$，$P\left(0,0,\frac12\right)$。

合上书，用长方体和两次勾股定理推出空间两点的距离公式。

距离只给出一个数。角色从 $A$ 走到 $B$，除了走多远，还要知道往哪个方向走，这是距离公式回答不了的。

### 2. 「从这里到那里」的位移怎样记录，怎样相加、伸缩？

上一节留下的问题是方向。一个角色从位置 $A$ 走到位置 $B$，要记的是整个位移：走多远、朝哪个方向。既有大小又有方向的量叫**向量**，用一支带箭头的线段画出来：箭尾是起点，箭头是终点。两个向量大小相同、方向相同，就算同一个向量，所以向量可以随意平移。向量用粗体字母 $\boldsymbol a$ 表示，从 $A$ 到 $B$ 的位移记作 $\overrightarrow{AB}$。

位移有两种自然的运算。

先走 $\boldsymbol a$、再走 $\boldsymbol b$，总的位移是 $\boldsymbol a+\boldsymbol b$：把 $\boldsymbol b$ 的箭尾接到 $\boldsymbol a$ 的箭头上，从 $\boldsymbol a$ 的箭尾连到 $\boldsymbol b$ 的箭头。也可以把两个向量放在同一个起点，以它们为邻边作平行四边形，从起点出发的对角线就是 $\boldsymbol a+\boldsymbol b$。

把位移伸长或缩短：$k\boldsymbol a$ 的长度是 $\boldsymbol a$ 的 $|k|$ 倍，$k>0$ 时方向相同，$k<0$ 时方向相反。$(-1)\boldsymbol a$ 记作 $-\boldsymbol a$，$\boldsymbol a-\boldsymbol b$ 理解成 $\boldsymbol a+(-\boldsymbol b)$。长度为零的向量叫零向量，记作 $\boldsymbol 0=(0,0,0)$，它没有确定的方向，$0\boldsymbol a=\boldsymbol 0$。

几何定义清楚，算起来要用坐标。把起点放在原点，终点的坐标就是向量的坐标。沿三条轴正方向的单位长度的向量记作 $\boldsymbol i=(1,0,0)$、$\boldsymbol j=(0,1,0)$、$\boldsymbol k=(0,0,1)$，任何向量都可以写成

$$\boldsymbol a=a_x\boldsymbol i+a_y\boldsymbol j+a_z\boldsymbol k=(a_x,a_y,a_z).$$

按平行四边形法则相加时，每条轴方向上的分量各自相加，所以加法和数乘**逐个坐标**进行。

$$(a_x,a_y,a_z)+(b_x,b_y,b_z)=(a_x+b_x,\ a_y+b_y,\ a_z+b_z),\qquad k(a_x,a_y,a_z)=(ka_x,ka_y,ka_z).$$

一般的位移怎么办？从 $A(x_1,y_1,z_1)$ 到 $B(x_2,y_2,z_2)$：先从 $A$ 退回原点，再从原点走到 $B$，即 $\overrightarrow{AB}=\overrightarrow{OB}-\overrightarrow{OA}$，所以

$$\overrightarrow{AB}=(x_2-x_1,\ y_2-y_1,\ z_2-z_1),$$

**终点减起点**。

最后是平行。两个非零向量方向相同或相反，叫作平行（也叫共线），并约定零向量与任何向量平行。$\boldsymbol b\ne\boldsymbol 0$ 时，$\boldsymbol a\parallel\boldsymbol b$ 当且仅当有一个数 $\lambda$ 使 $\boldsymbol a=\lambda\boldsymbol b$，写成坐标就是

$$a_x=\lambda b_x,\qquad a_y=\lambda b_y,\qquad a_z=\lambda b_z.$$

说成「坐标成比例」时要小心：这三个等式用的是**同一个** $\lambda$，而且某个 $b$ 的坐标为 0 时，对应的 $a$ 的坐标也必须为 0。要求 $\boldsymbol b\ne\boldsymbol 0$，是因为 $\boldsymbol b=\boldsymbol 0$ 时 $\lambda\boldsymbol b$ 永远是零向量，凑不出非零的 $\boldsymbol a$。

**方法 2（向量的坐标运算）**

1. 位移 = 终点坐标减起点坐标；
2. 加、减、数乘逐个坐标做；
3. 判断平行：看能不能找到同一个 $\lambda$ 使 $\boldsymbol a=\lambda\boldsymbol b$；
4. 三点 $A,B,C$ 共线，等价于 $\overrightarrow{AB}\parallel\overrightarrow{AC}$（两个位移有公共起点）。

**例 3**　已知 $A(1,-1,2)$、$B(3,1,1)$，求 $\overrightarrow{AB}$，并判断 $C(7,5,-1)$ 在不在直线 $AB$ 上。

例 1、例 2 求的是距离，这一节的新问题是位移和共线：用终点减起点，再比较坐标。这里换了新的点，因为老朋友的三个点不在一条直线上，没有共线可判断。

第一步，终点减起点：$\overrightarrow{AB}=(2,2,-1)$。

第二步，$\overrightarrow{AC}=(6,6,-3)$。三个坐标都是 $\overrightarrow{AB}$ 的 3 倍，是同一个 $\lambda=3$，所以 $\overrightarrow{AC}=3\overrightarrow{AB}$。

第三步，两个位移平行且同起点，所以 $C$ 在直线 $AB$ 上。

> 设 $\boldsymbol a=(2,m,-4)$ 与 $\boldsymbol b=(-1,3,n)$ 平行，求 $m,n$。
>
> 答案：$\boldsymbol b$ 的第一个坐标不为 0，先由它定 $\lambda$：$2=\lambda\cdot(-1)$，$\lambda=-2$，即 $\boldsymbol a=-2\boldsymbol b$，所以 $m=-6$，$-4=-2n$，$n=2$。

合上书，说明三点共线为什么能化成两个有公共起点的位移平行，并写出「$\boldsymbol a$ 与 $\boldsymbol b$ 平行」的坐标条件。

位移能相加、能判断平行了，可是还说不出一个位移到底有多长、朝向哪边。

### 3. 一个向量有多长，指向哪个方向？

上一节留下的问题是：一个位移到底有多长，朝向哪边？先看老朋友 $\boldsymbol a=(1,2,2)$。它是从原点走到点 $(1,2,2)$ 的位移，长度就是原点到这个点的距离，由第 1 节的公式是 $\sqrt{1+4+4}=3$。

一般地，向量 $\boldsymbol a$ 的长度是原点到点 $(a_x,a_y,a_z)$ 的距离，由第 1 节的距离公式，

$$\lVert\boldsymbol a\rVert=\sqrt{a_x^2+a_y^2+a_z^2}.$$

$\lVert\boldsymbol a\rVert$ 也叫 $\boldsymbol a$ 的**模**，有的书写成 $|\boldsymbol a|$。这里用双竖线，是为了和数的绝对值 $|x|$ 分开，数学和 AI 论文里都这样写，本书以后统一用双竖线。

长度为 1 的向量叫**单位向量**。$\boldsymbol a\ne\boldsymbol 0$ 时，$\boldsymbol a$ 乘以 $\frac1{\lVert\boldsymbol a\rVert}$ 得到同方向、长度为 1 的向量（记作 $\boldsymbol a^{0}$，读作 a 零）

$$\boldsymbol a^{0}=\frac{\boldsymbol a}{\lVert\boldsymbol a\rVert},$$

方向本身怎样用数记？对非零向量 $\boldsymbol a$，它与三条坐标轴正方向的夹角 $\alpha,\beta,\gamma$（都在 $0$ 到 $\pi$ 之间）叫它的**方向角**，它们的余弦叫**方向余弦**。过 $\boldsymbol a$ 的终点向 $x$ 轴作垂线，得到直角三角形，斜边是 $\lVert\boldsymbol a\rVert$。$a_x>0$ 时邻边长为 $a_x$；$a_x<0$ 时邻边长为 $|a_x|$，夹角是钝角，余弦带负号；$a_x=0$ 时余弦为零。三种情况都有 $\cos\alpha=\frac{a_x}{\lVert\boldsymbol a\rVert}$。三个方向余弦正好是单位向量的三个坐标：

$$\boldsymbol a^{0}=(\cos\alpha,\cos\beta,\cos\gamma),\qquad \cos^2\alpha+\cos^2\beta+\cos^2\gamma=1,$$

后一个等式就是 $\lVert\boldsymbol a^0\rVert=1$。

**方法 3（长度、单位化与方向）**

1. 长度：三个坐标的平方和开方；
2. 同方向的单位向量：除以长度；
3. 方向余弦：就是单位向量的坐标；
4. 反过来，已知长度和方向余弦，各坐标 $=$ 长度 $\times$ 对应的余弦；
5. 只给两个方向角时，先由平方和为 1 求第三个余弦的平方 $\cos^2\gamma$，分三种情形：
   - $\cos^2\gamma>0$：$\cos\gamma$ 有正负两个值，有两个可能方向；
   - $\cos^2\gamma=0$：只有一个可能方向；
   - $\cos^2\gamma<0$：不存在。

   只有另外给定正的长度，才能分别确定两个或一个向量。

**例 4**　老朋友 $\boldsymbol a=(1,2,2)$，求长度、同方向的单位向量和方向余弦。

和例 3 只求位移不同，这里要说出老朋友 $\boldsymbol a$ 多长、朝哪里，长度在本节开头已经算出是 3。

长度 $\lVert\boldsymbol a\rVert=\sqrt{1+4+4}=3$，所以单位向量是 $\left(\frac13,\frac23,\frac23\right)$，三个方向余弦就是 $\frac13,\frac23,\frac23$。验算平方和：$\frac19+\frac49+\frac49=1$。

> 一个向量的长度是 6，它与 $x$ 轴、$y$ 轴的夹角分别是 $\frac\pi3$ 和 $\frac{2\pi}3$，求这个向量。
>
> 答案：$\cos\alpha=\frac12$，$\cos\beta=-\frac12$，由约束 $\cos^2\gamma=\frac12$，$\cos\gamma=\pm\frac{\sqrt2}2$，两个符号都能取。长度乘余弦，得 $(3,-3,3\sqrt2)$ 和 $(3,-3,-3\sqrt2)$，只给两个方向角时向量不唯一。

合上书，写出长度公式和方向余弦的约束，并说明为什么方向余弦就是单位向量的坐标。

每个向量有了长度和方向，可是两个向量的方向有多接近，还没有办法比较。

### 4. 两个方向有多一致？

上一节留下的问题是：两个向量的方向有多接近？最自然的量是夹角，可是夹角要靠量角器，我们希望直接从坐标算出来。先在平面上试两个小例子。

$\boldsymbol u=(1,0)$、$\boldsymbol v=(1,1)$ 的夹角是 $45^\circ$，$\lVert\boldsymbol u\rVert\lVert\boldsymbol v\rVert\cos45^\circ=1\cdot\sqrt2\cdot\frac{\sqrt2}2=1$，而对应坐标相乘再相加是 $1\cdot1+0\cdot1=1$。再看 $\boldsymbol u=(1,1)$、$\boldsymbol v=(-1,1)$，夹角是 $90^\circ$，$\lVert\boldsymbol u\rVert\lVert\boldsymbol v\rVert\cos90^\circ=0$，对应坐标相乘再相加是 $-1+1=0$。两次都对上了，这是巧合吗？下面在空间里说明它不是。

把两个非零向量 $\boldsymbol a$、$\boldsymbol b$ 平移到同一个起点，它们之间不超过 $\pi$ 的那个角 $\theta$ 叫**夹角**。定义**数量积**（也叫点积）：

$$\boldsymbol a\cdot\boldsymbol b=\lVert\boldsymbol a\rVert\,\lVert\boldsymbol b\rVert\cos\theta ,$$

结果是一个数；有零向量时规定为 0。

定义里有夹角，直接用很不方便。下面用余弦定理把它变成坐标的式子。余弦定理说，三角形两边长为 $p,q$，夹角为 $\theta$，第三边的平方是 $p^2+q^2-2pq\cos\theta$。在以 $\boldsymbol a$、$\boldsymbol b$ 为两边的三角形里，第三边是 $\boldsymbol a-\boldsymbol b$（图 C19-n2），所以

$$\lVert\boldsymbol a-\boldsymbol b\rVert^2=\lVert\boldsymbol a\rVert^2+\lVert\boldsymbol b\rVert^2-2\,\boldsymbol a\cdot\boldsymbol b .$$

![把 $\boldsymbol a$、$\boldsymbol b$ 放在同一起点，第三边是 $\boldsymbol a-\boldsymbol b$；$\boldsymbol b$ 沿 $\boldsymbol a$ 方向的带符号投影为 $\lVert\boldsymbol b\rVert\cos\theta$，粗线段的长度是它的绝对值，钝角时投影落在反方向](fig/C19-n2.pdf){width=62%}

另一方面，左边按坐标展开：

$$\lVert\boldsymbol a-\boldsymbol b\rVert^2=(a_x-b_x)^2+(a_y-b_y)^2+(a_z-b_z)^2=\lVert\boldsymbol a\rVert^2+\lVert\boldsymbol b\rVert^2-2(a_xb_x+a_yb_y+a_zb_z).$$

两种写法的左边相同，消去 $\lVert\boldsymbol a\rVert^2$ 和 $\lVert\boldsymbol b\rVert^2$，再除以 $-2$：

$$\boldsymbol a\cdot\boldsymbol b=a_xb_x+a_yb_y+a_zb_z .$$

两向量共线时三角形退化，但夹角为 $0$ 或 $\pi$，代入同样得到上面的等式；有零向量时两边都为零。此后算数量积只用这个式子。

这个式子的每一项都是 $\boldsymbol a$ 与 $\boldsymbol b$ 的同一个坐标相乘，数的乘法可交换、对加法可分配，所以 $\boldsymbol a\cdot\boldsymbol b=\boldsymbol b\cdot\boldsymbol a$，对加法可以分配，$(k\boldsymbol a)\cdot\boldsymbol b=k(\boldsymbol a\cdot\boldsymbol b)$，且 $\boldsymbol a\cdot\boldsymbol a=\lVert\boldsymbol a\rVert^2$。它有三个用处：

- 夹角：$\cos\theta=\dfrac{\boldsymbol a\cdot\boldsymbol b}{\lVert\boldsymbol a\rVert\,\lVert\boldsymbol b\rVert}$；
- 垂直：两个非零向量垂直当且仅当 $\boldsymbol a\cdot\boldsymbol b=0$（因为 $\cos\theta=0$；零向量与任何向量的数量积都是 0，却没有夹角可言，所以要两个都非零）；
- 投影：$\boldsymbol b$ 在 $\boldsymbol a$ 方向上的（带符号的）投影长是 $\lVert\boldsymbol b\rVert\cos\theta=\dfrac{\boldsymbol a\cdot\boldsymbol b}{\lVert\boldsymbol a\rVert}$。夹角是钝角时它是负数，表示 $\boldsymbol b$ 的影子落在 $\boldsymbol a$ 的反方向上。

**方法 4（数量积求夹角、垂直和投影）**

1. 用坐标算 $\boldsymbol a\cdot\boldsymbol b$ 和两个长度；
2. 夹角、投影代公式；
3. 垂直写成 $\boldsymbol a\cdot\boldsymbol b=0$，含参数时解方程；
4. 求长度的平方时，用 $\lVert\boldsymbol a\pm\boldsymbol b\rVert^2=\lVert\boldsymbol a\rVert^2\pm2\,\boldsymbol a\cdot\boldsymbol b+\lVert\boldsymbol b\rVert^2$，像展开 $(p\pm q)^2$ 一样。例如 $\lVert\boldsymbol a\rVert=3$，$\lVert\boldsymbol b\rVert=4$，夹角 $\frac\pi3$ 时 $\boldsymbol a\cdot\boldsymbol b=6$，$\lVert\boldsymbol a+\boldsymbol b\rVert^2=9+12+16=37$。

**例 5**　老朋友 $\boldsymbol a=(1,2,2)$、$\boldsymbol b=(3,0,4)$，求夹角的余弦，以及 $\boldsymbol b$ 在 $\boldsymbol a$ 方向上的投影。

例 4 求出了 $\boldsymbol a$ 的长度，现在把第二个老朋友 $\boldsymbol b$ 放进来，看两个方向有多一致。

第一步，$\boldsymbol a\cdot\boldsymbol b=3+0+8=11$，$\lVert\boldsymbol a\rVert=3$，$\lVert\boldsymbol b\rVert=5$。

第二步，

$$\cos\theta=\frac{11}{3\cdot5}=\frac{11}{15},\qquad \text{投影}=\frac{11}{\lVert\boldsymbol a\rVert}=\frac{11}3 .$$

> 求 $k$，使 $(1,k,2)\perp(3,-1,k)$。
>
> 答案：数量积 $3-k+2k=3+k=0$，所以 $k=-3$。

**例 6**　文章的向量。假设用三个特征（体育、财经、科技的相关度）描述一篇文章，一篇检索文章 $\boldsymbol q=(2,1,0)$，两篇候选文章 $\boldsymbol d_1=(4,3,0)$、$\boldsymbol d_2=(20,0,20)$。哪篇和 $\boldsymbol q$ 更像？

和例 5 相比，向量不再是几何箭头，而是文章的特征；算的仍是夹角的余弦，只是多了一个问题：该比数量积，还是比余弦？

先凭眼睛猜一猜：$\boldsymbol d_1=(4,3,0)$ 和 $\boldsymbol d_2=(20,0,20)$，哪一个的三个特征的比例更接近 $\boldsymbol q=(2,1,0)$？再看数量积给出的答案是否和你的猜测一致。

这里约定：用三个特征的相对比例是否接近，来衡量两篇文章像不像，也就是看两串数的方向一不一致。数量积同时受长度和夹角影响：本题两个数量积都是正的，把候选向量伸长，数量积就变大。为了只比较方向，把数量积除以两个长度，得到的 $\cos\theta$ 叫**余弦相似度**。这里只用三个特征做简化演示，文本怎样变成向量，M.9 会讲。

第一步，数量积：$\boldsymbol q\cdot\boldsymbol d_1=8+3=11$，$\boldsymbol q\cdot\boldsymbol d_2=40$。光看数量积，$\boldsymbol d_2$ 大得多。

第二步，长度：$\lVert\boldsymbol q\rVert=\sqrt5$，$\lVert\boldsymbol d_1\rVert=5$，$\lVert\boldsymbol d_2\rVert=20\sqrt2$。

第三步，余弦相似度：

$$\cos\theta_1=\frac{11}{5\sqrt5}\approx0.984,\qquad \cos\theta_2=\frac{40}{\sqrt5\cdot20\sqrt2}=\frac{2}{\sqrt{10}}\approx0.632 .$$

$\boldsymbol d_1$ 的方向与 $\boldsymbol q$ 几乎一致，$\boldsymbol d_2$ 只是长，方向偏向了第三个特征。数量积被长度带偏了，余弦相似度没有。

合上书，用余弦定理推出数量积的坐标公式，并说出投影为什么可能是负数。

数量积只回答两个方向有多一致。要造出一个同时垂直于两个方向的方向，它只能事后检验，不能直接造出来。

### 5. 怎样造出一个同时垂直于两个方向的方向？

写一个平面方程需要它的朝向，也就是一个垂直于平面的向量。平面里有两个不平行的方向 $\boldsymbol a$、$\boldsymbol b$，所以要的是一个**同时垂直于两者**的向量 $\boldsymbol n$。

先用数量积硬解一次。取老朋友三角形的两条边 $\overrightarrow{AB}=(-1,2,0)$、$\overrightarrow{AC}=(-1,0,3)$，要 $\boldsymbol n=(p,q,r)$ 同时垂直于两者：

$$-p+2q=0,\qquad -p+3r=0 .$$

三个未知数、两个方程，令 $p=6$ 得 $q=3$，$r=2$，所以 $\boldsymbol n=(6,3,2)$，乘任何非零数也行。每换一对边就要解一遍，很麻烦；向量积把这个解法写成了现成的公式。

先引入一个记号。四个数排成两行两列，规定

$$\begin{vmatrix}p&q\\r&s\end{vmatrix}=ps-qr ,$$

叫**二阶行列式**（竖线在这里是排列的记号，不是绝对值）。线性代数册会把它推广到 $n$ 阶。

把 $\boldsymbol a$ 写在上一行、$\boldsymbol b$ 写在下一行，依次遮住第 1、2、3 列，各取剩下的二阶行列式，中间一项加负号，得到**向量积**（也叫叉积）：

$$\boldsymbol a\times\boldsymbol b=\left(\begin{vmatrix}a_y&a_z\\b_y&b_z\end{vmatrix},\ -\begin{vmatrix}a_x&a_z\\b_x&b_z\end{vmatrix},\ \begin{vmatrix}a_x&a_y\\b_x&b_y\end{vmatrix}\right)=(a_yb_z-a_zb_y,\ a_zb_x-a_xb_z,\ a_xb_y-a_yb_x).$$

中间那个负号不是随手加的，它保证了结果同时垂直于两个向量。下面验证三件事。

**它垂直于 $\boldsymbol a$ 和 $\boldsymbol b$ 吗？** 把 $\boldsymbol a\times\boldsymbol b$ 与 $\boldsymbol a$ 作数量积，展开成六项：

$$a_xa_yb_z-a_xa_zb_y+a_ya_zb_x-a_xa_yb_z+a_xa_zb_y-a_ya_zb_x ,$$

含 $a_xa_yb_z$ 的两项符号相反，含 $a_xa_zb_y$ 的两项符号相反，含 $a_ya_zb_x$ 的两项符号相反，所以和为 0。把 $\boldsymbol a$ 换成 $\boldsymbol b$ 同样展开：

$$a_yb_xb_z-a_zb_xb_y+a_zb_yb_x-a_xb_yb_z+a_xb_zb_y-a_yb_zb_x=0 ,$$

也是三对相反项抵消。若 $\boldsymbol a\parallel\boldsymbol b$，数量积仍为 0，但此时向量积本身是 $\boldsymbol 0$，没有方向可言。

**它有多长？** 把 $\lVert\boldsymbol a\rVert^2\lVert\boldsymbol b\rVert^2-(\boldsymbol a\cdot\boldsymbol b)^2$ 按坐标展开。前一项有九个乘积项，后一项有三个平方项和三个交叉项。三个平方项 $a_x^2b_x^2,a_y^2b_y^2,a_z^2b_z^2$ 两边各有一份，相减后抵消；剩下六个乘积项和三个交叉项，每三个凑成一个完全平方，例如

$$a_x^2b_y^2+a_y^2b_x^2-2a_xb_xa_yb_y=(a_xb_y-a_yb_x)^2 ,$$

另外两对 $a_x^2b_z^2+a_z^2b_x^2-2a_xb_xa_zb_z$ 和 $a_y^2b_z^2+a_z^2b_y^2-2a_yb_ya_zb_z$ 同样凑成 $(a_xb_z-a_zb_x)^2$ 和 $(a_yb_z-a_zb_y)^2$，三个平方恰好是 $\boldsymbol a\times\boldsymbol b$ 三个坐标的平方，即 $\lVert\boldsymbol a\rVert^2\lVert\boldsymbol b\rVert^2-(\boldsymbol a\cdot\boldsymbol b)^2=\lVert\boldsymbol a\times\boldsymbol b\rVert^2$。代入 $\boldsymbol a\cdot\boldsymbol b=\lVert\boldsymbol a\rVert\lVert\boldsymbol b\rVert\cos\theta$：

$$\lVert\boldsymbol a\times\boldsymbol b\rVert^2=\lVert\boldsymbol a\rVert^2\lVert\boldsymbol b\rVert^2(1-\cos^2\theta)=\lVert\boldsymbol a\rVert^2\lVert\boldsymbol b\rVert^2\sin^2\theta .$$

$\theta\in[0,\pi]$，$\sin\theta\ge0$，开方得

$$\lVert\boldsymbol a\times\boldsymbol b\rVert=\lVert\boldsymbol a\rVert\,\lVert\boldsymbol b\rVert\sin\theta .$$

右边正是以 $\boldsymbol a$、$\boldsymbol b$ 为邻边的平行四边形的面积：底 $\lVert\boldsymbol a\rVert$，高 $\lVert\boldsymbol b\rVert\sin\theta$（图 C19-n3）。

**公式取了两个相反方向里的哪一个？** 垂直于两者的方向有相反的两个。先看一组：$\boldsymbol i\times\boldsymbol j=(0,0,1)=\boldsymbol k$，与坐标系的右手法则一致。再让 $\boldsymbol a,\boldsymbol b$ 连续地改变长度和夹角，并转动到任意位置，只要始终不平行。这时公式给出的 $\boldsymbol a\times\boldsymbol b$ 连续变化、始终非零、始终垂直于两者，所以只能停在「右手法则所选的一侧」或「相反的一侧」（一个连续变化的量如果只能取两个相隔的值，就只能恒取其中一个），不能中途跳换；右手法则选出的一侧也连续变化。起初二者一致，因此始终一致：对所有不平行的 $\boldsymbol a,\boldsymbol b$，右手四指从 $\boldsymbol a$ 弯向 $\boldsymbol b$，拇指都指向 $\boldsymbol a\times\boldsymbol b$。

![底 $\lVert\boldsymbol a\rVert$ 乘高 $\lVert\boldsymbol b\rVert\sin\theta$ 就是 $\lVert\boldsymbol a\times\boldsymbol b\rVert$；$\boldsymbol a\times\boldsymbol b$ 垂直于平行四边形所在的平面，按右手法则定向](fig/C19-n3.pdf){width=60%}

交换 $\boldsymbol a$、$\boldsymbol b$，相当于交换两行，每个二阶行列式变号，所以 $\boldsymbol b\times\boldsymbol a=-\boldsymbol a\times\boldsymbol b$；特别地 $\boldsymbol a\times\boldsymbol a=\boldsymbol 0$。$\boldsymbol a\parallel\boldsymbol b$ 时 $\sin\theta=0$，向量积为 $\boldsymbol 0$；反过来，向量积为 $\boldsymbol 0$ 就是 $\boldsymbol a\parallel\boldsymbol b$（含零向量）。

两种乘积易混，并排看一遍。先自己找出它们的异同：

| | 数量积 $\boldsymbol a\cdot\boldsymbol b$ | 向量积 $\boldsymbol a\times\boldsymbol b$ |
|---|---|---|
| 结果 | 一个数 | 一个向量 |
| 量的是 | $\cos\theta$：有多一致 | $\sin\theta$：有多「错开」，大小是平行四边形面积 |
| 为 0 当且仅当 | 垂直（两个向量都非零时） | 平行 |
| 交换次序 | 不变 | 变号 |

**方法 5（向量积求公垂向量和面积）**

1. 按遮列法算 $\boldsymbol a\times\boldsymbol b$，用 $\boldsymbol a\cdot(\boldsymbol a\times\boldsymbol b)=0$ 验算；
2. 平行四边形面积 $=\lVert\boldsymbol a\times\boldsymbol b\rVert$，三角形面积是它的一半；
3. 需要一个同时垂直于两个**不平行**方向的非零向量时，取它们的向量积；两个方向平行时向量积为零（例如 $(1,2,3)\times(2,4,6)=\boldsymbol 0$），不能用来确定法向量。

**例 7**　老朋友 $A$、$B$、$C$，求一个同时垂直于 $\overrightarrow{AB}$、$\overrightarrow{AC}$ 的向量和三角形 $ABC$ 的面积。

例 5 用数量积量「沿着」，这一次换向量积量「错开」，对象仍是老朋友，不过换成三角形 $ABC$ 的两条边。

第一步，$\overrightarrow{AB}=(-1,2,0)$，$\overrightarrow{AC}=(-1,0,3)$。

第二步，遮列。遮第 1 列：$2\cdot3-0\cdot0=6$。遮第 2 列：$(-1)\cdot3-0\cdot(-1)=-3$，加负号得 $3$。遮第 3 列：$(-1)\cdot0-2\cdot(-1)=2$。所以

$$\overrightarrow{AB}\times\overrightarrow{AC}=(6,3,2),$$

验算：与 $\overrightarrow{AB}$ 的数量积 $-6+6+0=0$，与 $\overrightarrow{AC}$ 的数量积 $-6+0+6=0$。这正是本节开头硬解出的 $(6,3,2)$。

第三步，长度 $\sqrt{36+9+4}=7$，三角形面积是 $\frac72$。另一对老朋友也这样算：$\boldsymbol a\times\boldsymbol b=(8,2,-6)$，小结的表里会用到。

> 求 $(1,2,-1)\times(2,0,1)$，以及以这两个向量为邻边的平行四边形的面积。
>
> 答案：$(2\cdot1-(-1)\cdot0,\ -(1\cdot1-(-1)\cdot2),\ 1\cdot0-2\cdot2)=(2,-3,-4)$，面积 $\sqrt{4+9+16}=\sqrt{29}$。

**例 8**　三维游戏中的朝向判断。一个三角形面片的三个顶点按逆时针（从外侧看）排列为 $P_1(0,0,0)$、$P_2(2,0,0)$、$P_3(0,2,0)$，摄像机在 $E(1,1,5)$ 处，判断它看到的是正面还是背面。

和例 7 相比，向量积不再用来求面积，而是用它的方向判断面朝哪里。

约定：顶点从外侧看按逆时针排列时，两条边的向量积（右手法则）指向外侧，记作法向量 $\boldsymbol n$。从面片指向摄像机的向量与 $\boldsymbol n$ 的数量积为正，说明摄像机在正面一侧；为负，在背面一侧。若采用只画正面的规则，背面就跳过。

第一步，$\overrightarrow{P_1P_2}=(2,0,0)$，$\overrightarrow{P_1P_3}=(0,2,0)$，法向量

$$\boldsymbol n=\overrightarrow{P_1P_2}\times\overrightarrow{P_1P_3}=(0\cdot0-0\cdot2,\ -(2\cdot0-0\cdot0),\ 2\cdot2-0\cdot0)=(0,0,4).$$

第二步，视线向量 $\overrightarrow{P_1E}=(1,1,5)$，$\boldsymbol n\cdot\overrightarrow{P_1E}=20>0$，是正面。

合上书，写出遮列法，并说明 $\lVert\boldsymbol a\times\boldsymbol b\rVert$ 为什么是平行四边形的面积。

向量积一次只处理两个向量。再加进第三个向量，它会不会正好躺在前两个所在的平面里？不在的话，三个向量围出多大的体积？

### 6. 三个向量在不在同一个平面里，围出多大体积？

两个不平行的向量决定一个平面，第三个向量要么躺在这个平面里，要么翘出去。翘出去时，三个向量围出一个**平行六面体**，我们想知道它的体积。

先定义。**混合积**是先作向量积、再作数量积：

$$[\boldsymbol a,\boldsymbol b,\boldsymbol c]=(\boldsymbol a\times\boldsymbol b)\cdot\boldsymbol c ,$$

结果是一个数。

先看最简单的情形：$\boldsymbol a=(2,0,0)$、$\boldsymbol b=(0,3,0)$、$\boldsymbol c=(0,0,4)$ 两两垂直，围成长方体，体积是 $2\cdot3\cdot4=24$。这时 $\boldsymbol a\times\boldsymbol b=(0,0,6)$，长度 6 是底面积，方向沿 $z$ 轴、垂直于底面，而 $(\boldsymbol a\times\boldsymbol b)\cdot\boldsymbol c=24$ 恰好是体积。下面说明这不是巧合。

一般情形看几何。以 $\boldsymbol a$、$\boldsymbol b$ 为邻边的平行四边形是底，面积 $\lVert\boldsymbol a\times\boldsymbol b\rVert$，$\boldsymbol a\times\boldsymbol b$ 垂直于这个底。先设 $\boldsymbol a,\boldsymbol b$ 不平行、$\boldsymbol c\ne\boldsymbol 0$，用 $\varphi$ 表示 $\boldsymbol c$ 与 $\boldsymbol a\times\boldsymbol b$ 的夹角。$\boldsymbol c$ 沿这个垂直方向的投影长取绝对值，就是平行六面体的高 $h$：

$$|(\boldsymbol a\times\boldsymbol b)\cdot\boldsymbol c|=\lVert\boldsymbol a\times\boldsymbol b\rVert\cdot\big(\lVert\boldsymbol c\rVert\,|\cos\varphi|\big)=\text{底面积}\times\text{高}=\text{体积}.$$

![以 $\boldsymbol a,\boldsymbol b,\boldsymbol c$ 为棱的平行六面体：底是 $\boldsymbol a,\boldsymbol b$ 张成的平行四边形（阴影），$\boldsymbol a\times\boldsymbol b$ 垂直于底，高是 $\boldsymbol c$ 沿 $\boldsymbol a\times\boldsymbol b$ 方向的带符号投影的绝对值（点线）](fig/C19-n4.pdf){width=58%}

所以混合积的绝对值是体积；符号说明 $\boldsymbol c$ 在 $\boldsymbol a\times\boldsymbol b$ 指的一侧（正）还是另一侧（负）。三个向量共面时没有高，混合积为 0，反过来也成立。若 $\boldsymbol a\parallel\boldsymbol b$，它们与任意第三个向量都共面，叉积及混合积都是 0；若 $\boldsymbol a,\boldsymbol b$ 不平行，叉积是非零的法向量，混合积为 0 正好表示 $\boldsymbol c$ 躺在底面所在的平面里；$\boldsymbol c=\boldsymbol 0$ 时结论同样成立。于是

$$\boldsymbol a,\boldsymbol b,\boldsymbol c\ \text{共面}\iff[\boldsymbol a,\boldsymbol b,\boldsymbol c]=0 .$$

体积和三条棱的叫法次序无关，所以绝对值不随次序变；符号看右手系的朝向，三个向量依次轮换时朝向不变，所以 $[\boldsymbol a,\boldsymbol b,\boldsymbol c]=[\boldsymbol b,\boldsymbol c,\boldsymbol a]=[\boldsymbol c,\boldsymbol a,\boldsymbol b]$。交换 $\boldsymbol a,\boldsymbol b$ 时 $\boldsymbol b\times\boldsymbol a=-\boldsymbol a\times\boldsymbol b$（第 5 节），符号变反；任意交换两个向量，都等于一次轮换加上这样一次交换，符号都变反。

怎么用坐标算？把向量积的坐标式代入数量积，得到

$$[\boldsymbol a,\boldsymbol b,\boldsymbol c]=c_x\begin{vmatrix}a_y&a_z\\b_y&b_z\end{vmatrix}-c_y\begin{vmatrix}a_x&a_z\\b_x&b_z\end{vmatrix}+c_z\begin{vmatrix}a_x&a_y\\b_x&b_y\end{vmatrix}.$$

这个式子很整齐，值得有一个专门的记号。三行排成方阵，规定**三阶行列式**按第一行展开：第一行的每个元素，乘上遮住它所在的行和列后剩下的二阶行列式，符号依次为 $+,-,+$。展开式的三个系数正好是 $\boldsymbol c$ 的三个分量，所以 $[\boldsymbol a,\boldsymbol b,\boldsymbol c]$ 等于第一行为 $\boldsymbol c$、后两行为 $\boldsymbol a,\boldsymbol b$ 的三阶行列式。如果三行改按 $\boldsymbol a,\boldsymbol b,\boldsymbol c$ 排，同样按第一行展开，得到 $\boldsymbol a\cdot(\boldsymbol b\times\boldsymbol c)=[\boldsymbol b,\boldsymbol c,\boldsymbol a]$，由轮换不变仍等于 $[\boldsymbol a,\boldsymbol b,\boldsymbol c]$，所以

$$[\boldsymbol a,\boldsymbol b,\boldsymbol c]=\begin{vmatrix}a_x&a_y&a_z\\b_x&b_y&b_z\\c_x&c_y&c_z\end{vmatrix}.$$

向量积也可以这样记：把第一行换成 $\boldsymbol i,\boldsymbol j,\boldsymbol k$，按第一行展开，得到的就是遮列法的结果。这只是借用了展开的格式，第一行放的是向量而不是数。

**方法 6（用混合积判断共面、求体积）**

1. 把三个向量按行排成三阶行列式，展开；
2. 等于 0：共面；不等于 0：体积 $=$ 绝对值，四面体体积是它的 $\frac16$（同样的三条棱，三角形底面积是平行四边形的一半，棱锥体积再乘 $\frac13$，所以是 $\frac12\times\frac13=\frac16$）；
3. 判断四个点 $A,B,C,D$ 是否共面，取 $\overrightarrow{AB},\overrightarrow{AC},\overrightarrow{AD}$。

**例 9**　老朋友 $A,B,C$ 再加一个点 $D(1,1,1)$，判断四点是否共面，并求四面体 $ABCD$ 的体积。

例 7 用两条边 $\overrightarrow{AB}$、$\overrightarrow{AC}$ 围出平面里的面积；再添一个不在平面里的点 $D$，三个位移就围出一个体积。

第一步，取从 $A$ 出发的三个位移：$\overrightarrow{AB}=(-1,2,0)$，$\overrightarrow{AC}=(-1,0,3)$，$\overrightarrow{AD}=(0,1,1)$。

第二步，按第一行展开：

$$\begin{vmatrix}-1&2&0\\-1&0&3\\0&1&1\end{vmatrix}=-1\cdot(0\cdot1-3\cdot1)-2\cdot((-1)\cdot1-3\cdot0)+0=3+2=5 .$$

第三步，不为 0，所以四点不共面；平行六面体体积为 5，四面体是它的 $\frac16$，体积 $\frac56$。

用例 7 的结果检查：$(6,3,2)\cdot(0,1,1)=5$，一致。

> 求以 $O$、$A(1,0,0)$、$B(1,2,0)$、$C(1,2,3)$ 为顶点的四面体的体积。
>
> 答案：$\begin{vmatrix}1&0&0\\1&2&0\\1&2&3\end{vmatrix}=1\cdot(6-0)=6$，体积 $\frac66=1$。

合上书，说明混合积的绝对值为什么是体积，并说出共面的判据。

共面和体积有了判据，可是我们最早要的是平面本身：怎样用一个方程，把平面上所有的点一次写出来？

### 7. 怎样用一个方程写出一个平面？

回到第 5 节开头的问题：有了法向量，怎样写出平面的方程？

先看最简单的平面，$xOy$ 面。它过原点，法向量是 $\boldsymbol k=(0,0,1)$。点 $(x,y,z)$ 在这个面上，当且仅当从原点到它的位移 $(x,y,z)$ 与 $\boldsymbol k$ 垂直，即 $(x,y,z)\cdot(0,0,1)=z=0$。把原点换成任意一点、$\boldsymbol k$ 换成任意法向量，就是一般的做法。

平面的朝向由一个垂直于它的非零向量记录，叫**法向量**。过一点、垂直于给定方向的平面只有一个，所以「一个点加一个法向量」就确定了一个平面。

设平面过 $M_0(x_0,y_0,z_0)$，法向量 $\boldsymbol n=(A,B,C)\ne\boldsymbol 0$。点 $M(x,y,z)$ 在平面上，当且仅当 $\overrightarrow{M_0M}$ 躺在平面里，即 $\overrightarrow{M_0M}\perp\boldsymbol n$，也就是 $\boldsymbol n\cdot\overrightarrow{M_0M}=0$。写成坐标：

$$A(x-x_0)+B(y-y_0)+C(z-z_0)=0 ,$$

这是平面的**点法式方程**。展开得**一般式** $Ax+By+Cz+D=0$（这里的 $A,B,C,D$ 是方程的系数，与点 $A,B,C$ 及例 9 的点 $D$ 无关），其中 $D=-(Ax_0+By_0+Cz_0)$。反过来，一般式里 $x,y,z$ 的系数（不全为 0）就是一个法向量。

不含 $z$ 的 $Ax+By+D=0$（$(A,B)\ne(0,0)$），法向量 $(A,B,0)$ 垂直于 $z$ 轴，平面包含平行于 $z$ 轴的方向：$D\ne0$ 时与 $z$ 轴平行，$D=0$ 时包含 $z$ 轴。平面在三条轴上的截距 $a,b,c$ 都不为 0 时，方程还能写成**截距式** $\frac xa+\frac yb+\frac zc=1$。

**方法 7（写平面方程）**

1. 找一个点和一个法向量；
2. 法向量不直接给时，取平面内两个不平行方向的向量积；三点定平面时先确认三点不共线，再取 $\overrightarrow{M_1M_2}\times\overrightarrow{M_1M_3}$；
3. 代入点法式，再整理成一般式。

**例 10**　老朋友 $A,B,C$ 三点，求过它们的平面方程。

例 7 求出了垂直于平面里两条边的向量 $(6,3,2)$，现在拿它做法向量写平面方程。

三点定一个平面，法向量要同时垂直于平面里的两个方向 $\overrightarrow{AB}$、$\overrightarrow{AC}$，正好是例 7 求出的 $(6,3,2)$。用点 $A$ 写点法式：

$$6(x-1)+3y+2z=0 ,\qquad 6x+3y+2z=6 .$$

两边除以 6 得截距式 $\frac x1+\frac y2+\frac z3=1$，三个截距正是 $A,B,C$ 的坐标，对得上。

> 求过 $P(1,1,0)$、$Q(0,1,1)$、$R(1,0,1)$ 的平面方程。
>
> 答案：$\overrightarrow{PQ}=(-1,0,1)$，$\overrightarrow{PR}=(0,-1,1)$，向量积是 $(0\cdot1-1\cdot(-1),\ -((-1)\cdot1-1\cdot0),\ (-1)(-1)-0\cdot(-1))=(1,1,1)$，用点 $P$：$(x-1)+(y-1)+z=0$，即 $x+y+z=2$。

**一个点离平面有多远？** 设点为 $P_1(x_1,y_1,z_1)$。从平面上任取一点 $M_0$，把 $\overrightarrow{M_0P_1}$ 分成两部分：平行于 $\boldsymbol n$ 的部分和躺在平面里的部分。$P_1$ 到平面的垂线平行于 $\boldsymbol n$，所以距离就是第一部分的长度，即 $\overrightarrow{M_0P_1}$ 沿 $\boldsymbol n$ 方向的投影的绝对值（图 C19-n5）。由第 4 节的投影公式，

$$d=\frac{|\boldsymbol n\cdot\overrightarrow{M_0P_1}|}{\lVert\boldsymbol n\rVert}.$$

分子里的数量积，用「终点减起点」写成坐标：

$$\boldsymbol n\cdot\overrightarrow{M_0P_1}=A(x_1-x_0)+B(y_1-y_0)+C(z_1-z_0)=Ax_1+By_1+Cz_1-(Ax_0+By_0+Cz_0).$$

$M_0$ 在平面上，所以 $Ax_0+By_0+Cz_0=-D$，右边就是 $Ax_1+By_1+Cz_1+D$。于是 $M_0$ 取哪一点结果都一样：

$$d=\frac{|Ax_1+By_1+Cz_1+D|}{\sqrt{A^2+B^2+C^2}} .$$

![$P_1$ 到平面的垂线平行于 $\boldsymbol n$，所以距离 $d$ 是 $\overrightarrow{M_0P_1}$ 沿法向方向的投影的绝对值；粗实线标出法向方向上的投影，点线 $P_1H$ 标出垂直距离，浅灰带是平面的侧视图](fig/C19-n5.pdf){width=58%}

**例 11**　例 9 的点 $D(1,1,1)$ 到例 10 的平面 $6x+3y+2z-6=0$ 的距离，并用例 9 的体积核对。

和例 9 对照：例 9 用混合积算四面体体积，这里改用「底面积 $\times$ 高 $\div3$」，高是点到平面的距离。

距离：

$$d=\frac{|6+3+2-6|}{\sqrt{36+9+4}}=\frac57 .$$

核对：四面体 $ABCD$ 以三角形 $ABC$ 为底，面积 $\frac72$，高就是 $d$，体积 $\frac13\cdot\frac72\cdot\frac57=\frac56$，与例 9 一致。

> 求点 $P(1,2,3)$ 到平面 $2x-y+2z+1=0$ 的距离。
>
> 答案：$d=\frac{|2-2+6+1|}{\sqrt{4+1+4}}=\frac73$。

**例 12**　线性分类器与间隔。一个线性分类器给样本 $\boldsymbol x=(x_1,x_2,x_3)$（三个特征）打分 $s=\boldsymbol w\cdot\boldsymbol x+\beta$，$s>0$ 判为甲类，$s<0$ 判为乙类。设 $\boldsymbol w=(1,2,2)$，$\beta=-3$，求分界面，以及 $\boldsymbol p_1=(3,0,1)$ 和 $\boldsymbol p_2=(0,0,0)$ 各被判为哪一类、离分界面多远。

和例 11 相比，对象从几何里的点换成了样本的特征向量；算的仍是点到平面的距离，只是平面的名字换成了「分界面」。

$\boldsymbol w$ 的三个坐标是给三个特征的系数，$\beta$ 是加在总分上的常数。分界面是 $s=0$，即 $x_1+2x_2+2x_3-3=0$。用本节的说法，它是以 $\boldsymbol w$ 为法向量的平面：$\boldsymbol w$ 决定朝向；固定 $\boldsymbol w$ 后，改变 $\beta$ 会平移分界面，原点到分界面的距离是 $\frac{|\beta|}{\lVert\boldsymbol w\rVert}$。分数恰为 0 时样本落在分界面上，本例暂不把它分到任何一侧。

$\lVert\boldsymbol w\rVert=3$。先看 $\boldsymbol p_1$：分数 $s=3+0+2-3=2>0$，判为甲类，距离 $\frac{|s|}{\lVert\boldsymbol w\rVert}=\frac23$。

再看 $\boldsymbol p_2$：分数 $s=-3<0$，判为乙类，距离 $\frac33=1$。

如果两类样本能被一个平面完全分开，可以在把两类样本都放对一侧的前提下，让最近的样本也尽量远离分界面；这个最近距离（本章就把它叫间隔）是支持向量机的一种基本想法，真实模型更复杂，细节留到 M.6。

合上书，从 $\overrightarrow{M_0M}\perp\boldsymbol n$ 写出点法式，再用投影推出点到平面的距离公式。

平面有了方程。直线是两个平面的交线，也是最简单的曲线，它的方程该怎么写？

### 8. 怎样用方程写出一条直线？

平面由「一个点加一个法向量」确定，直线同样简单：过一个点、沿一个方向，就只有一条。先看最简单的一条，$x$ 轴：过原点、沿 $\boldsymbol i$，它上面的点是 $(t,0,0)$，即 $t\boldsymbol i$，$t$ 取遍全体实数。一般的直线只是把原点换成任意一点、$\boldsymbol i$ 换成任意方向。

和直线平行的非零向量叫它的**方向向量**，记作 $\boldsymbol s=(m,n,p)$。

设直线过 $M_0(x_0,y_0,z_0)$。点 $M(x,y,z)$ 在直线上，当且仅当 $\overrightarrow{M_0M}\parallel\boldsymbol s$，即有一个数 $t$ 使 $\overrightarrow{M_0M}=t\boldsymbol s$。按坐标写开：

$$x=x_0+mt,\qquad y=y_0+nt,\qquad z=z_0+pt,$$

这是直线的**参数方程**，$t$ 取遍全体实数，点就走遍整条直线。三个式子都解出 $t$，令它们相等，得到**点向式**（也叫对称式）：

$$\frac{x-x_0}{m}=\frac{y-y_0}{n}=\frac{z-z_0}{p}.$$

$m,n,p$ 叫方向数。某个分母为 0 时，约定对应的分子也为 0。例如 $\frac{x-1}{0}=\frac{y-2}{3}=\frac{z}{1}$ 表示 $x=1$ 且 $\frac{y-2}{3}=\frac z1$：方向向量的 $x$ 分量为 0，点沿直线走时 $x$ 不变。

两个不平行的平面相交成一条直线，所以直线也可以写成方程组，叫**一般式**：

$$\begin{cases}A_1x+B_1y+C_1z+D_1=0,\\ A_2x+B_2y+C_2z+D_2=0.\end{cases}$$

一般式不直接告诉方向，做题时常要化成点向式。直线躺在两个平面里，所以它的方向同时垂直于两个法向量，第 5 节的向量积正好造出这样的方向：$\boldsymbol s=\boldsymbol n_1\times\boldsymbol n_2$。

**方法 8（写直线方程）**

1. 已知两点：方向取它们的位移，用其中一点；
2. 已知一般式：方向取 $\boldsymbol n_1\times\boldsymbol n_2$；点取令某个变量为一个方便值（常取 0）后解出的解。这个变量要选 $\boldsymbol s$ 里分量不为 0 的：例如 $s_z\ne0$，直线会穿过每一个水平面，令 $z=0$ 一定有唯一的交点；若 $s_z=0$，直线躺在一个水平面里，可能根本碰不到 $z=0$；
3. 写成点向式或参数方程，代回两个平面方程检查一次。

**例 13**　把直线 $\begin{cases}x+y+z=1,\\2x-y+3z=4\end{cases}$ 写成点向式和参数方程。

例 10 用向量积造出平面的法向量；这一道换成直线，已知的是两个平面的交线，要的方向向量同时垂直于两个法向量，用的还是向量积。

第一步，两个法向量是 $\boldsymbol n_1=(1,1,1)$、$\boldsymbol n_2=(2,-1,3)$，按遮列法：

$$\boldsymbol n_1\times\boldsymbol n_2=\big(1\cdot3-1\cdot(-1),\ -(1\cdot3-1\cdot2),\ 1\cdot(-1)-1\cdot2\big)=(4,-1,-3).$$

直线在两个平面里，方向同时垂直于 $\boldsymbol n_1,\boldsymbol n_2$，所以取 $\boldsymbol s=(4,-1,-3)$。

第二步，找一点。令 $z=0$ 会得到分数，改令 $y=0$：$x+z=1$，$2x+3z=4$，解得 $z=2$，$x=-1$。代回两个方程检查：$-1+0+2=1$，$-2-0+6=4$，都成立。

第三步，

$$\frac{x+1}{4}=\frac{y}{-1}=\frac{z-2}{-3},\qquad x=-1+4t,\ y=-t,\ z=2-3t .$$

点可以换，方向向量也可以乘非零数，所以点向式不唯一。

> 求过 $A(1,0,-2)$、$B(3,1,1)$ 两点的直线的点向式方程。
>
> 答案：方向向量取 $\overrightarrow{AB}=(2,1,3)$，用点 $A$：$\frac{x-1}{2}=\frac y1=\frac{z+2}{3}$。

**例 14**　过 $P(1,2,3)$ 作平面 $2x-y+2z+1=0$ 的垂线，求垂足。

沿用第 7 节随堂小题的点 $P(1,2,3)$ 和平面 $2x-y+2z+1=0$：那里求出了距离，现在求垂足。这次直线的方向由平面给出，垂线垂直于平面，所以它的方向向量就是平面的法向量 $\boldsymbol n=(2,-1,2)$，参数方程是 $x=1+2t$，$y=2-t$，$z=3+2t$。

垂足是垂线与平面的交点，把参数方程代入平面方程：

$$2(1+2t)-(2-t)+2(3+2t)+1=7+9t=0 ,\qquad t=-\frac79 ,$$

垂足 $\left(-\frac59,\ \frac{25}9,\ \frac{13}9\right)$。垂足到 $P$ 的距离是 $|t|\lVert\boldsymbol n\rVert=\frac79\cdot3=\frac73$，与第 7 节随堂小题求出的距离 $\frac73$ 一致。

合上书，从 $\overrightarrow{M_0M}=t\boldsymbol s$ 写出参数方程和点向式，再说明一般式的方向为什么取 $\boldsymbol n_1\times\boldsymbol n_2$。

平面和直线都有了方程。它们之间是平行、垂直还是相交，夹角多大？

### 9. 两个平面、两条直线、直线和平面之间是什么位置关系？

有了方程，就能问两个对象的相对位置。先看两个坐标面 $z=0$ 与 $x=0$：它们的法向量是 $\boldsymbol k$ 与 $\boldsymbol i$，数量积为 0，所以两个面垂直。一般的办法同样是先用代表向量判断方向关系，再用点的位置区分平行、重合和包含：平面看法向量 $\boldsymbol n$，直线看方向向量 $\boldsymbol s$，两条直线的夹角同样用 $\boldsymbol s_1,\boldsymbol s_2$，都用数量积算。

两个平面的夹角，规定为两个法向量的夹角里不超过 $\frac\pi2$ 的那个，所以要加绝对值：

$$\cos\varphi=\frac{|\boldsymbol n_1\cdot\boldsymbol n_2|}{\lVert\boldsymbol n_1\rVert\lVert\boldsymbol n_2\rVert}.$$

直线和平面的夹角不同。它指直线和它在平面上的投影之间的夹角 $\varphi$（直线垂直于平面时规定 $\varphi=\frac\pi2$）。看图 C19-n6，先选直线方向 $\boldsymbol s$，使 $\boldsymbol s\cdot\boldsymbol n\ge0$。法向量垂直于平面，在这个取向下 $\boldsymbol s$ 与 $\boldsymbol n$ 的夹角是 $\frac\pi2-\varphi$，余弦变成正弦。改取相反方向只会改变数量积的符号，所以一般公式在分子取绝对值：

$$\sin\varphi=\frac{|\boldsymbol s\cdot\boldsymbol n|}{\lVert\boldsymbol s\rVert\lVert\boldsymbol n\rVert}.$$

![直线 $L$ 与它在平面上的投影（虚线）夹角为 $\varphi$；法向量 $\boldsymbol n$ 垂直于平面，图中选择 $\boldsymbol s\cdot\boldsymbol n\ge0$ 的取向，$\boldsymbol s$ 与 $\boldsymbol n$ 的夹角是 $\frac\pi2-\varphi$，所以用 $\sin\varphi$ 而不是 $\cos\varphi$](fig/C19-n6.pdf){width=55%}

平行和垂直由此读出。先自己想一想直线和平面的两种情形，再对照：

| 关系 | 平面与平面 | 直线与直线 | 直线与平面 |
|---|---|---|---|
| 平行（含重合、包含） | $\boldsymbol n_1\parallel\boldsymbol n_2$；再代一点，区分平行与重合 | $\boldsymbol s_1\parallel\boldsymbol s_2$；再代一点，区分平行与重合 | $\boldsymbol s\cdot\boldsymbol n=0$；再代一点，区分平行与包含 |
| 垂直 | $\boldsymbol n_1\cdot\boldsymbol n_2=0$ | $\boldsymbol s_1\cdot\boldsymbol s_2=0$ | $\boldsymbol s\parallel\boldsymbol n$ |

最后一列最容易弄反：直线平行于平面时，方向向量和法向量**垂直**；直线垂直于平面时，两个向量反而**平行**，因为 $\boldsymbol n$ 本身就垂直于平面。

**方法 9（判断位置关系、求夹角）**

1. 写出每个对象的代表向量：平面取 $\boldsymbol n$，直线取 $\boldsymbol s$；
2. 平面与平面、直线与直线的夹角用 $\cos\varphi$，直线与平面用 $\sin\varphi$，都加绝对值；
3. 平行、垂直查上表；方向平行时再代一点，区分平行、重合和包含。

**例 15**　求直线 $L:\frac{x-1}{1}=\frac{y-2}{0}=\frac{z+1}{1}$ 与平面 $\pi:x+y-5=0$ 的夹角和交点。

例 13 写出了直线的方程；这一道让直线和平面相遇，问它们的夹角和交点。

夹角用 $\sin\varphi$；交点把参数方程代入平面方程，只剩一个未知数。

第一步，$\boldsymbol s=(1,0,1)$，$\boldsymbol n=(1,1,0)$：

$$\sin\varphi=\frac{|1+0+0|}{\sqrt2\cdot\sqrt2}=\frac12,\qquad\varphi=\frac\pi6.$$

第二步，参数方程 $x=1+t$，$y=2$，$z=-1+t$（分母为 0，$y$ 不变）。代入 $\pi$：$(1+t)+2-5=0$，$t=2$，交点 $(3,2,1)$。

> 求平面 $x+y-5=0$ 与平面 $x+z-1=0$ 的夹角。
>
> 答案：法向量 $(1,1,0)$、$(1,0,1)$，$\cos\varphi=\frac{|1|}{\sqrt2\cdot\sqrt2}=\frac12$，$\varphi=\frac\pi3$。

**两条直线是相交还是异面？** 平面上两条直线不平行就一定相交，空间里却不一定，还可能既不平行也不相交，叫**异面**。设 $L_1$ 过 $M_1$、方向 $\boldsymbol s_1$，$L_2$ 过 $M_2$、方向 $\boldsymbol s_2$，两个方向不平行。

**共面 $\Rightarrow$ 混合积为 0。** 若两条直线共面于 $\pi$，则 $\pi$ 的法向量可取 $\boldsymbol s_1\times\boldsymbol s_2$，$M_1$、$M_2$ 都在 $\pi$ 上，所以 $\overrightarrow{M_1M_2}$ 垂直于它。

**混合积为 0 $\Rightarrow$ 共面。** 若 $\overrightarrow{M_1M_2}\perp\boldsymbol s_1\times\boldsymbol s_2$，过 $M_1$、以 $\boldsymbol s_1\times\boldsymbol s_2$ 为法向量的平面包含 $L_1$，也包含 $M_2$ 和方向 $\boldsymbol s_2$，于是包含 $L_2$。所以

$$L_1,L_2\ \text{共面}\iff(\boldsymbol s_1\times\boldsymbol s_2)\cdot\overrightarrow{M_1M_2}=0 ,$$

右边的 $(\boldsymbol s_1\times\boldsymbol s_2)\cdot\overrightarrow{M_1M_2}$ 是混合积（第 6 节）。两直线方向不平行时，混合积为 0 表示共面，从而相交；不为 0 则异面。方向平行时 $\boldsymbol s_1\times\boldsymbol s_2=\boldsymbol 0$，混合积一定是 0，可两条平行线并不相交，所以这个判据要先确认方向不平行。

**例 16**　判断 $L_1:\frac{x}{1}=\frac{y-1}{2}=\frac{z}{1}$ 与 $L_2:\frac{x-2}{2}=\frac{y}{1}=\frac{z-1}{0}$ 的位置关系。

例 15 里直线与平面相交于一点；两条直线却可能既不平行也不相交，这就要用到第 6 节的混合积。

第一步，方向不平行（$(1,2,1)$ 与 $(2,1,0)$ 坐标不成比例），不是平行线。

第二步，取 $M_1(0,1,0)$、$M_2(2,0,1)$，$\overrightarrow{M_1M_2}=(2,-1,1)$，算混合积：

$$\begin{vmatrix}1&2&1\\2&1&0\\2&-1&1\end{vmatrix}=1\cdot(1-0)-2\cdot(2-0)+1\cdot(-2-2)=1-4-4=-7\ne0 .$$

不共面，所以两条直线异面。

合上书，画出直线与平面的夹角，说明公式里为什么是 $\sin$ 而不是 $\cos$，再说明混合积为 0 为什么等价于两条直线共面。

直线与平面、直线与直线的位置都能判断了，可一个点离一条直线有多远，还没有办法。

### 10. 一个点离一条直线有多远？

第 7 节用沿法向方向的投影算点到平面的距离，因为一个平面的所有非零法向量都互相平行。直线的垂直方向却有无穷多个，所以这里改用面积除以底。

先看最简单的一条直线，$x$ 轴，和点 $M_1(3,4,0)$：垂足是 $(3,0,0)$，距离是 4。用向量来算：取 $M_0=O$，$\boldsymbol s=\boldsymbol i$，$\overrightarrow{M_0M_1}\times\boldsymbol s=(3,4,0)\times(1,0,0)=(0,0,-4)$，长度 4，除以 $\lVert\boldsymbol i\rVert=1$，还是 4。一般的直线照这个办法做。

设直线过 $M_0$、方向为 $\boldsymbol s$，点 $M_1$ 在直线外。以 $\overrightarrow{M_0M_1}$ 和 $\boldsymbol s$ 为邻边作平行四边形（沿用图 C19-n3 的画法）。它的底是 $\lVert\boldsymbol s\rVert$，高正是 $M_1$ 到直线的距离 $d$；它的面积又等于向量积的长度。于是 $\lVert\overrightarrow{M_0M_1}\times\boldsymbol s\rVert=\lVert\boldsymbol s\rVert\,d$，即

$$d=\frac{\lVert\overrightarrow{M_0M_1}\times\boldsymbol s\rVert}{\lVert\boldsymbol s\rVert}.$$

**方法 10（点到直线的距离）**

1. 从直线方程读出一点 $M_0$ 和方向 $\boldsymbol s$；
2. 算 $\overrightarrow{M_0M_1}\times\boldsymbol s$ 的长度，再除以 $\lVert\boldsymbol s\rVert$；
3. 题目还要垂足时，设垂足 $M=M_0+t\boldsymbol s$，由 $\overrightarrow{MM_1}\cdot\boldsymbol s=0$ 解出 $t$。

**例 17**　求点 $M_1(3,2,1)$ 到直线 $L:\frac{x-1}{2}=\frac{y+1}{-1}=\frac z2$ 的距离和垂足。

例 14 求点到平面的垂足，这一道求点到直线的距离，并求垂足；直线用点向式给出。第一步，$M_0(1,-1,0)$，$\boldsymbol s=(2,-1,2)$，$\lVert\boldsymbol s\rVert=3$，$\overrightarrow{M_0M_1}=(2,3,1)$。

第二步，遮列法：

$$\overrightarrow{M_0M_1}\times\boldsymbol s=(3\cdot2-1\cdot(-1),\ -(2\cdot2-1\cdot2),\ 2\cdot(-1)-3\cdot2)=(7,-2,-8),$$

长度 $\sqrt{49+4+64}=3\sqrt{13}$，所以 $d=\sqrt{13}$。

第三步，垂足 $M=(1+2t,\,-1-t,\,2t)$，$\overrightarrow{MM_1}=(2-2t,\,3+t,\,1-2t)$。为什么条件是数量积为 0？垂足是直线上离 $M_1$ 最近的点，连线必须垂直于直线。于是

$$2(2-2t)-(3+t)+2(1-2t)=3-9t=0,\qquad t=\frac13 ,$$

垂足 $\left(\frac53,-\frac43,\frac23\right)$。验算：$\overrightarrow{MM_1}=\left(\frac43,\frac{10}3,\frac13\right)$，长度 $\frac{\sqrt{117}}3=\sqrt{13}$，与第二步一致。

> 求点 $(1,1,1)$ 到直线 $\frac x1=\frac y0=\frac z1$ 的距离。
>
> 答案：$M_0=(0,0,0)$，$\boldsymbol s=(1,0,1)$，$(1,1,1)\times(1,0,1)=(1,0,-1)$，长度 $\sqrt2$，除以 $\lVert\boldsymbol s\rVert=\sqrt2$，距离为 1。

合上书，画出平行四边形，说出距离公式里分子、分母各是什么。

到这里，点、直线、平面的位置和距离都能算了。接下来换一个问题：一个方程在空间里画出什么，会是整张曲面吗？

### 11. 一个方程在空间里画出什么？

平面上，一个方程 $F(x,y)=0$ 一般画出一条曲线。到了空间，满足 $F(x,y,z)=0$ 的点一般组成一张**曲面**，这个方程叫曲面的方程。

**球面**直接来自距离公式。到定点 $(a,b,c)$ 距离为 $R$ 的点满足

$$(x-a)^2+(y-b)^2+(z-c)^2=R^2 .$$

反过来，三个平方项系数相同、没有 $xy$ 这类交叉项的二次方程，配方后就能看出是不是球面。例如 $x^2+y^2+z^2-2x+4z=0$ 配方得 $(x-1)^2+y^2+(z+2)^2=5$，球心 $(1,0,-2)$，半径 $\sqrt5$。

再看缺一个变量的方程，例如 $x^2+y^2=1$。在平面上它是单位圆。在空间里，方程对 $z$ 没有任何要求：点 $(x,y)$ 只要在圆上，$z$ 取什么都行。圆上每一点都长出一条平行于 $z$ 轴的竖直线，这些竖线合起来是圆柱面。

一般地，若不含 $z$ 的方程 $F(x,y)=0$ 在 $xOy$ 面上表示一条曲线（叫准线），那么它在空间里表示**柱面**：由平行于 $z$ 轴的直线（叫母线）沿着这条曲线平移而成。缺 $x$ 的方程母线平行于 $x$ 轴，缺 $y$ 的平行于 $y$ 轴。所以 $y=x^2$ 在空间里是抛物柱面，$x^2+z^2=4$ 是以 $y$ 轴为轴的圆柱面。

**方法 11（认球面与柱面）**

1. 三个平方项系数相同、没有交叉项：配方，看出球心和半径（右边为 0 是一点，为负则没有点）；
2. 方程缺哪个变量，先看另外两个变量的方程在它们的坐标面上表示什么；若是曲线，就沿缺失变量对应的轴平移得到柱面，母线平行于那个轴。

**例 18**　说出 $x^2+y^2+z^2+4y=0$ 和 $z=1-x^2$ 在空间里各是什么曲面。

平面是一次方程，这一道看二次方程：第一个配方认球面，第二个缺一个变量，认柱面。

前者配方得 $x^2+(y+2)^2+z^2=4$，球心 $(0,-2,0)$、半径 2 的球面。后者缺 $y$，是母线平行于 $y$ 轴的抛物柱面，准线是 $zOx$ 面上的抛物线 $z=1-x^2$。

> 说出 $y^2+z^2=9$ 在空间里是什么曲面，点 $(5,3,0)$ 在不在上面。
>
> 答案：缺 $x$，是以 $x$ 轴为轴、半径 3 的圆柱面。$9+0=9$，点 $(5,3,0)$ 在上面，横坐标取什么都行。

合上书，解释 $x^2+y^2=1$ 在空间里为什么是圆柱面，而不是一个圆。

球面和柱面的方程是直接看出来的。花瓶、碗这类形状是一条曲线绕轴转出来的，它们的方程该怎么写？

### 12. 一条曲线绕轴转一圈，扫出的曲面怎么写？

花瓶、碗、冷却塔都是一条曲线绕轴转出来的，叫**旋转曲面**。

先看一个小情形：$yOz$ 面上的抛物线 $z=y^2$ 绕 $z$ 轴转。曲线上高度 $z_1$ 处的点离轴 $\sqrt{z_1}$，转一圈走出半径 $\sqrt{z_1}$ 的水平圆，所以空间里的点 $(x,y,z)$ 在曲面上，当且仅当它离轴的距离 $\sqrt{x^2+y^2}$ 等于 $\sqrt z$，即 $z=x^2+y^2$，这是一只碗。一般的曲线照此办理。

设 $yOz$ 面上有曲线 $f(y,z)=0$，绕 $z$ 轴旋转。曲线上一点 $M_1(0,y_1,z_1)$ 转起来，走出一个水平的圆（图 C19-n7）。转动时有两样东西不变：高度 $z_1$，以及到 $z$ 轴的距离 $|y_1|$。所以点 $M(x,y,z)$ 在旋转曲面上，当且仅当

$$z=z_1,\qquad \sqrt{x^2+y^2}=|y_1| .$$

把 $y_1=\pm\sqrt{x^2+y^2}$、$z_1=z$ 代入 $f(y_1,z_1)=0$，得旋转曲面的方程

$$f\big(\pm\sqrt{x^2+y^2},\,z\big)=0,$$

其中 $\pm$ 表示两个符号各给一个方程，即 $f(\sqrt{x^2+y^2},z)=0$ 与 $f(-\sqrt{x^2+y^2},z)=0$，满足其中一个的点都在曲面上。

![曲线上的点 $M_1$ 绕 $z$ 轴转一圈，画出虚线圆；转动时高度 $z$ 不变，到轴的距离 $\sqrt{x^2+y^2}$ 也不变，等于 $|y_1|$](fig/C19-n7.pdf){width=55%}

记法是：**绕哪个轴转，哪个坐标不动；另一个坐标换成「到这根轴的距离」，即另外两个坐标平方和的正负平方根。**例如上面的抛物线得到碗；直线 $z=y$ 绕 $z$ 轴，得 $z=\pm\sqrt{x^2+y^2}$，即 $z^2=x^2+y^2$，是圆锥面。

**方法 12（写旋转曲面）**

1. 认出旋转轴，它对应的坐标保持不动；
2. 曲线方程里另一个坐标换成 $\pm\sqrt{\text{另外两个坐标的平方和}}$；
3. 方程里只出现这个坐标的平方时，直接换成平方和，不必写 $\pm$；
4. 原曲线的坐标范围要一并保留，平方后再检查有没有多出另一支。例如 $yOz$ 面上只取 $y\ge0$ 的半条直线 $z=y$，绕 $z$ 轴旋转后只有 $z=\sqrt{x^2+y^2}$，即 $z^2=x^2+y^2$ 且 $z\ge0$。

**例 19**　$zOx$ 面上的双曲线 $\frac{x^2}{4}-\frac{z^2}{9}=1$ 分别绕 $z$ 轴、$x$ 轴旋转，写出旋转曲面的方程。

例 18 是缺变量的柱面与球面；这一节让曲线转起来，对象换成旋转曲面。

绕 $z$ 轴：$z$ 不动，$x$ 换成 $\pm\sqrt{x^2+y^2}$，平方后

$$\frac{x^2+y^2}{4}-\frac{z^2}{9}=1 .$$

绕 $x$ 轴：这次 $x$ 不动，$z$ 换成 $\pm\sqrt{y^2+z^2}$，

$$\frac{x^2}{4}-\frac{y^2+z^2}{9}=1 .$$

绕的轴不同，曲面完全不同：前一个连成一片，像冷却塔；后一个分成两片，下一节用截痕法看清。

> $xOy$ 面上的椭圆 $\frac{x^2}{4}+y^2=1$ 分别绕 $x$ 轴、$y$ 轴旋转，写出旋转曲面的方程。
>
> 答案：绕 $x$ 轴，$x$ 不动，$y^2$ 换成 $y^2+z^2$：$\frac{x^2}{4}+y^2+z^2=1$。绕 $y$ 轴，$y$ 不动，$x^2$ 换成 $x^2+z^2$：$\frac{x^2+z^2}{4}+y^2=1$。两个都是旋转椭球面，前者沿 $x$ 轴拉长，后者被压扁。

合上书，用「高度不变、到轴的距离不变」推出 $f(\pm\sqrt{x^2+y^2},z)=0$。

例 19 里同一条双曲线绕不同的轴，得到连成一片和分成两片的曲面。除了这样转出来的，二次方程还能画出哪些曲面？

### 13. 二次方程能画出哪几种曲面？

没有交叉项的二次方程，配方后化成的标准形式只有少数几种。空间曲面画不准，但可以像 3D 打印机那样一层层切开看：用平行于坐标面的平面 $z=k$（或 $x=k$、$y=k$）去截曲面，看截出的曲线（叫**截痕**）怎样随 $k$ 变化，再拼出整体形状。这个办法叫**截痕法**。

以 $\frac{x^2}{a^2}+\frac{y^2}{b^2}-\frac{z^2}{c^2}=1$ 为例。用 $z=k$ 去截，得 $\frac{x^2}{a^2}+\frac{y^2}{b^2}=1+\frac{k^2}{c^2}$，右边总是正的，所以每一层都是椭圆，$k=0$ 时最小，$|k|$ 越大越大。用 $x=0$ 去截，得 $yOz$ 面上的双曲线 $\frac{y^2}{b^2}-\frac{z^2}{c^2}=1$。椭圆一层层往上下放大，侧面是双曲线，整个曲面连成一片，叫**单叶双曲面**。$a=b$ 时得到绕 $z$ 轴旋转的单叶双曲面，取 $a=b=2$、$c=3$ 就是例 19 的第一个方程。

把右边的 $1$ 改成 $-1$，曲面还会连成一片吗？先猜一猜，再看截痕，它变成 $\frac{x^2}{a^2}+\frac{y^2}{b^2}=\frac{k^2}{c^2}-1$。$|k|<c$ 时右边为负，这一层没有点；$|k|=c$ 时是一点；$|k|>c$ 才是椭圆。曲面在 $-c<z<c$ 之间断开，分成上下两片，叫**双叶双曲面**。右边的 $1$ 和 $-1$ 只差一个符号，曲面却从一片变成两片，原因就在截痕方程右边能不能为负。

其余几种同样截出来，汇总如下（以下 $a,b,c$ 都是正数，图 C19-n8），每一行都可以代 $z=k$ 自己推出。

| 名称 | 标准方程 | 截痕 $z=k$ | 截痕 $x=0$ |
|---|---|---|---|
| 椭球面 | $\frac{x^2}{a^2}+\frac{y^2}{b^2}+\frac{z^2}{c^2}=1$ | $\lvert k\rvert<c$ 时为椭圆，$=c$ 时为一点 | 椭圆 |
| 单叶双曲面 | $\frac{x^2}{a^2}+\frac{y^2}{b^2}-\frac{z^2}{c^2}=1$ | 椭圆 | 双曲线 |
| 双叶双曲面 | $\frac{x^2}{a^2}+\frac{y^2}{b^2}-\frac{z^2}{c^2}=-1$ | $\lvert k\rvert>c$ 时为椭圆 | 双曲线 |
| 椭圆锥面 | $\frac{x^2}{a^2}+\frac{y^2}{b^2}=\frac{z^2}{c^2}$ | 椭圆，$k=0$ 时缩成一点 | 两条相交直线 |
| 椭圆抛物面 | $z=\frac{x^2}{a^2}+\frac{y^2}{b^2}$ | $k>0$ 时为椭圆，$k=0$ 时为一点 | 开口向上的抛物线 |
| 马鞍面（双曲抛物面） | $z=\frac{x^2}{a^2}-\frac{y^2}{b^2}$ | 双曲线，$k=0$ 时为两条直线 | 开口向下的抛物线 |

![六种二次曲面。前五个曲面上加粗的环线是截痕 $z=k$，马鞍面上加粗的两条抛物线是截痕（粗实线 $y=0$，粗虚线 $x=0$）；双叶双曲面在 $-c<z<c$ 之间没有点，所以分成上下两片](fig/C19-n8.pdf){width=88%}

最后两行是后面反复要用的基本图形：$z=x^2+y^2$ 是碗，$z=x^2-y^2$ 是马鞍，C.20 会用等高线再画一遍。

**方法 13（截痕法与认曲面）**

1. 先配方成标准形式；
2. 若一个变量只出现一次方，先解出它。另两个变量都有非零平方项时，同号给出椭圆抛物面，异号给出马鞍面；缺少一个平方项时，先检查是不是柱面；
3. 若三个变量都有平方项，先整理到三个平方项系数全为正，或恰有一个为负。全为正时，右边为正、零、负分别得到椭球面、一个点、空集。恰有一个负号时，右边为零得到椭圆锥面；右边归一化成 $1$ 或 $-1$ 后，分别得到单叶或双叶双曲面。用垂直于负号对应坐标轴的平面去截，可以检查这个判断；

配方不能省：$x^2+y^2-z^2=2z+1$ 里有一次项 $2z$，但 $z$ 也有平方项，配方得 $x^2+y^2=(z+1)^2$，是顶点在 $(0,0,-1)$ 的圆锥面。


**例 20**　用截痕法判断 $x^2-4y^2+z^2=-4$ 是什么曲面。

和例 19 对照：例 19 从曲线出发写曲面，这一道反过来，从方程出发判断是哪一种曲面。

和表里的单叶、双叶双曲面对照，这里负号落在 $y^2$ 上，所以改用 $y=k$ 去截（截面要垂直于带负号那个变量的轴）：

$$x^2+z^2=4k^2-4 .$$

$|k|<1$ 时右边为负，没有点；$|k|=1$ 时是一点；$|k|>1$ 时是圆，$|k|$ 越大圆越大。曲面在 $-1<y<1$ 之间断开，是双叶双曲面，两片分别朝 $y$ 轴正、负方向伸出去。

> 判断 $-x^2+y^2+z^2=1$ 是什么曲面。
>
> 答案：负号落在 $x^2$ 上，用 $x=k$ 去截：$y^2+z^2=1+k^2$，右边总是正的，每一层都是圆，$|k|$ 越大圆越大，曲面连成一片，是以 $x$ 轴为轴的单叶双曲面。

合上书，用截痕说明右边的 $1$ 换成 $-1$ 时，单叶为什么变成双叶。

曲面认识了。再往前一步，两个曲面相交出的一条线怎么写？

### 14. 空间里的一条曲线怎么写？

空间曲线常用两个曲面的交线来表示，也可以用一个参数描述。第 8 节已经见过直线的两种写法（参数方程和一般式），空间曲线也是这两种。

**一般方程**：把曲线看成两个曲面的交线，写成方程组 $\begin{cases}F(x,y,z)=0,\\G(x,y,z)=0.\end{cases}$ 例如球面 $x^2+y^2+z^2=4$ 和平面 $z=1$ 的交线，把 $z=1$ 代入得 $x^2+y^2=3$，是高度为 1、半径 $\sqrt3$ 的圆。

**参数方程**：让三个坐标都随一个参数变化，$x=x(t)$，$y=y(t)$，$z=z(t)$。例如

$$x=\cos t,\qquad y=\sin t,\qquad z=\frac{t}{2\pi} .$$

$(x,y)$ 在单位圆上转，$t$ 每增加 $2\pi$ 转一圈，同时 $z$ 升高 1。这条曲线绕在圆柱面 $x^2+y^2=1$ 上，叫螺旋线。

两种写法常要互化。由一般方程求参数方程，思路是先消去一个坐标得到一条平面曲线，把它参数化（圆、椭圆用 $\cos t$、$\sin t$），再由另一个方程解出被消去的坐标。

**方法 14（由交线求参数方程）**

1. 从两个方程里消去一个坐标，或者取其中一个柱面方程，得到只含两个坐标的方程；
2. 把这条平面曲线参数化；
3. 把参数代入另一个方程，解出第三个坐标；若有两个实数分支，两个都要保留，按原条件限制参数范围，并检查所得参数式是否覆盖整条曲线。

**例 21**　把圆柱面 $x^2+y^2=1$ 与平面 $x+y+z=2$ 的交线写成参数方程。

前面的交线都只写成方程组，这一道要把交线写成参数方程。

第一步，圆柱面上的点可以写成 $x=\cos t$，$y=\sin t$，因为 $\cos^2t+\sin^2t=1$ 自动满足第一个方程。

第二步，代入平面方程解出 $z$：$z=2-\cos t-\sin t$。交线是

$$x=\cos t,\qquad y=\sin t,\qquad z=2-\cos t-\sin t,\qquad 0\le t<2\pi .$$

> 把球面 $x^2+y^2+z^2=9$ 与平面 $z=x$ 的交线写成参数方程。
>
> 答案：代入得 $2x^2+y^2=9$，即 $\frac{x^2}{9/2}+\frac{y^2}{9}=1$。令 $x=\frac3{\sqrt2}\cos t$，$y=3\sin t$，则 $z=x=\frac3{\sqrt2}\cos t$，$0\le t<2\pi$。

合上书，说出参数方程和一般方程各怎样描述一条曲线，以及由一般方程求参数方程的步骤。

曲线有了方程。从正上方看下去，它的影子是什么？

### 15. 曲线和立体在坐标面上的影子是什么？

后面算三重积分，要先知道一个立体投到 $xOy$ 面上占哪块区域。先看曲线。

从曲线 $C$ 上每一点作平行于 $z$ 轴的直线，这些直线合起来构成 $C$ 对 $xOy$ 面的**投影柱面**；它与 $z=0$ 的交集就是 $C$ 在 $xOy$ 面上的**投影曲线**，也就是 $C$ 从正上方照下来的影子。

一般不能直接把 $z=0$ 代进两个方程：那样得到的是曲线与 $xOy$ 面的交点；只有曲线本身就在 $xOy$ 面内时，交点才是影子。影子上的点 $(x,y,0)$ 只要求曲线上有某个点 $(x,y,z)$ 在它的正上方或正下方。

计算时设 $C$ 由 $\begin{cases}F(x,y,z)=0,\\G(x,y,z)=0\end{cases}$ 给出。先从两个方程里消去 $z$，得到只含 $x,y$ 的关系，例如 $H(x,y)=0$。它缺 $z$，是一个母线平行于 $z$ 轴的柱面（第 11 节），$C$ 上的点都满足它，所以它只给出投影必须满足的条件。还要检查：每个保留的 $(x,y)$ 是否都能配上满足原方程组的实数 $z$。加上这个限制，再令第三个坐标为 0，才得到完整的投影：

$$\begin{cases}H(x,y)=0,\\ z=0 .\end{cases}$$

投到 $yOz$ 面或 $zOx$ 面，就改为消去 $x$ 或 $y$。

**方法 15（求投影曲线与投影区域）**

1. 投到哪个坐标面，就从方程组里消去垂直于它的那个变量，得到必要的坐标关系；
2. 检查被消去的变量对保留的点是否存在符合原条件的实数解，保留相应范围，再把垂直于该面的坐标设为 0；
3. 立体在 $xOy$ 面上的投影区域，就是找出哪些 $(x,y)$ 能配上至少一个符合原条件的实数 $z$。若立体写成 $f(x,y)\le z\le g(x,y)$，先取两个函数的共同定义域，再保留满足 $f(x,y)\le g(x,y)$ 的点。

**例 22**　求球面 $x^2+y^2+z^2=4$ 与平面 $x+z=2$ 的交线在 $xOy$ 面上的投影曲线。

和例 21 相反，这次要把交线压到坐标面上。

第一步，由平面得 $z=2-x$，代入球面，消去 $z$：

$$x^2+y^2+(2-x)^2=4,\qquad 2x^2-4x+y^2=0 .$$

第二步，配方：$2(x-1)^2+y^2=2$，即 $(x-1)^2+\frac{y^2}{2}=1$。投影曲线是

$$\begin{cases}(x-1)^2+\dfrac{y^2}{2}=1,\\ z=0,\end{cases}$$

一个中心在 $(1,0)$ 的椭圆。交线本身是斜平面上的圆，从正上方看被压扁成了椭圆。

> 求球面 $x^2+y^2+z^2=4$ 与平面 $y+z=2$ 的交线在 $xOy$ 面上的投影曲线。
>
> 答案：由平面得 $z=2-y$，代入球面消去 $z$：$x^2+y^2+(2-y)^2=4$，即 $x^2+2(y-1)^2=2$，$\frac{x^2}2+(y-1)^2=1$。投影曲线是该椭圆，写成 $\begin{cases}\frac{x^2}2+(y-1)^2=1,\\ z=0,\end{cases}$ 中心在 $(0,1)$。

**例 23**　立体 $\Omega$ 的下界是圆锥面的上半部分 $z=\sqrt{x^2+y^2}$，上界是上半球面 $z=\sqrt{2-x^2-y^2}$，求它在 $xOy$ 面上的投影区域。

和例 22 不同，这次要的是一块区域，按方法 15 第 3 步找哪些 $(x,y)$ 配得上 $z$。

第一步，令 $r=\sqrt{x^2+y^2}$，即点到 $z$ 轴的距离。上半球面要求 $2-r^2\ge0$，即 $0\le r\le\sqrt2$。

第二步，在这个范围内，下界不超过上界当且仅当 $r\le\sqrt{2-r^2}$。两边都非负，平方后得 $r^2\le1$，即 $r\le1$。（交线正是 $r=1$、$z=1$ 的单位圆，它给出了边界。）

所以投影区域是 $D=\{(x,y)\mid x^2+y^2\le1\}$：花括号内的竖线读作「满足」，即取所有满足右侧不等式的 $(x,y)$。

合上书，说明消去 $z$ 得到的方程为什么表示一个包含曲线的柱面。

### 本章小结

回到开头的问题。游戏里的小三角形朝向哪边：例 8 的面片法向量 $(0,0,4)$ 与视线向量 $(1,1,5)$ 的数量积是 $20>0$，摄像机在正面一侧。两段文字像不像：例 6 的 $\cos\theta_1\approx0.984$ 远大于 $\cos\theta_2\approx0.632$，$\boldsymbol d_1$ 更像 $\boldsymbol q$，而数量积 11 和 40 给出的却是相反的答案。

本册的主线是「放大了看都是直线，切细了再加起来」。后面研究二元函数时，会问它的图像在一点附近能否用平面近似。要描述这样的平面，先得有空间里点、直线、平面的语言：本章就是这套语言，它为 C.20 的切平面和 C.22 的方向变化准备好了坐标、向量和法向量。

老朋友的表，到这里长成了下面的样子（粗体是本章新增的对象）：

| 运算 | 老朋友上的结果 | 回答的问题 |
|---|---|---|
| 距离、长度 | $d(A,B)=\sqrt5$；$\lVert\boldsymbol a\rVert=3$，$\lVert\boldsymbol b\rVert=5$ | 多远、多长 |
| 数量积 | $\boldsymbol a\cdot\boldsymbol b=11$，$\cos\theta=\frac{11}{15}$ | 方向有多一致 |
| 向量积 | $\boldsymbol a\times\boldsymbol b=(8,2,-6)$；$\overrightarrow{AB}\times\overrightarrow{AC}=(6,3,2)$，三角形面积 $\frac72$ | 垂直方向，面积 |
| 混合积 | $[\overrightarrow{AB},\overrightarrow{AC},\overrightarrow{AD}]=5$，四面体体积 $\frac56$ | 共面，体积 |
| **平面** | $6x+3y+2z=6$，$D$ 到它的距离 $\frac57$ | 一个点加一个法向量 |
| **直线** | 一般式 $\to$ 点向式，方向 $(4,-1,-3)$ | 一个点加一个方向向量 |
| **曲面** | 球面、柱面、旋转曲面、二次曲面 | 方程画出什么 |

| 方法 | 什么时候用 | 对应题号 |
|---|---|---|
| 方法 1（坐标与距离） | 两点距离、按距离条件求点 | C19-01 |
| 方法 2（向量的坐标运算） | 位移、平行与共线 | C19-01 |
| 方法 3（长度、单位化与方向） | 单位向量、方向余弦 | C19-02 |
| 方法 4（数量积） | 夹角、垂直、投影、长度的平方 | C19-03、04、06、07 |
| 方法 5（向量积） | 公垂向量与面积 | C19-03、09 |
| 方法 6（混合积） | 共面与体积 | C19-08、11 |
| 方法 7（写平面方程） | 三点定面、点加法向量、点面距离 | C19-09、11 |
| 方法 8（写直线方程） | 两点、一般式化点向式 | C19-09 |
| 方法 9（位置关系与夹角） | 线面夹角用 $\sin$，其余用 $\cos$；异面用混合积 | C19-05、11 |
| 方法 10（点到直线的距离） | 面积除以底；垂足用数量积为 0 | C19-11、15 |
| 方法 11（认球面与柱面） | 配方；缺一个变量就是柱面 | C19-13 |
| 方法 12（旋转曲面） | 绕谁转谁不动，另一个换成平方和的根 | C19-10 |
| 方法 13（截痕法） | 认二次曲面 | C19-10 |
| 方法 14（由交线求参数方程） | 先参数化柱面，再解第三个坐标 | C19-12 |
| 方法 15（投影） | 消元得投影柱面，联立坐标面 | C19-12、14 |
