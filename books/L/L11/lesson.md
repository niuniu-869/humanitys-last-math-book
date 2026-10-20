## L.11 · 特征值与特征向量

搜索引擎要给几十亿个网页排先后。谷歌早年的 PageRank 用的想法是：被重要网页链接的网页也重要。这句话在绕圈子，每个网页的分数要用别的网页的分数来定义。但「分数等于收到的份额之和」对每个网页列一个一次方程，把份额系数排成矩阵 $M$，方程组就写成 $\boldsymbol x=M\boldsymbol x$：一个矩阵乘分数向量，结果还是这个向量。解出来就是本章的特征向量（例 5）。主成分分析从几十个指标里找出数据散得最开的方向（M.5），算的也是某个矩阵的特征向量。

L.3 把矩阵看成变换：大多数向量经过变换后方向会转动。本章找的是那些方向不变、只被拉伸的特殊方向。这个问题最直观的来源是几何：椭圆、椭球这类图形的方程里有 $xy$ 这样的交叉项时，看不出图形朝哪个方向斜放，要把坐标轴转到合适的位置（叫主轴）让交叉项消失（L.14）。1829 年，柯西把找主轴的问题归结为一个关于 $\lambda$ 的行列式方程。「本征」译自德语 eigen，意思是「自己的、固有的」；希尔伯特在 1904 年前后研究积分方程时用开了这个词，中文多译作「特征」。

第 1 节定义特征值和特征向量，拿老朋友试一试；第 2 节用行列式和解方程组把它们求出来；第 3 节不解方程，由迹和行列式得到特征值的和与积；第 4 节由 $A$ 的特征值得到 $A^k$、$A^{-1}$ 等矩阵的特征值；第 5 节证明不同特征值的特征向量线性无关；第 6 节看重根时特征向量够不够。

### 1. 有没有方向只被拉伸、不被转向？

拿老朋友①（对称伸缩）$A=\begin{pmatrix}2&1\\1&2\end{pmatrix}$ 来看它把几个向量变成什么：

$$A\begin{pmatrix}1\\0\end{pmatrix}=\begin{pmatrix}2\\1\end{pmatrix},\qquad A\begin{pmatrix}1\\1\end{pmatrix}=\begin{pmatrix}3\\3\end{pmatrix}=3\begin{pmatrix}1\\1\end{pmatrix},\qquad A\begin{pmatrix}-1\\1\end{pmatrix}=\begin{pmatrix}-1\\1\end{pmatrix}.$$

$(1,0)^{\mathsf T}$ 的方向转了；$(1,1)^{\mathsf T}$ 方向没变，长度变成 3 倍；$(-1,1)^{\mathsf T}$ 原样不动。在图里，单位圆上的向量被变到椭圆上，几乎都转了一个角度，只有两条直线上的向量留在原来的直线上。

![单位圆（虚线）被老朋友①变成椭圆（实线）；$\boldsymbol e_1$ 变成 $(2,1)^{\mathsf T}$，方向转了；$\boldsymbol u$、$\boldsymbol w$ 是沿 $(1,1)^{\mathsf T}$、$(-1,1)^{\mathsf T}$ 的单位向量，$\boldsymbol u$ 伸长 3 倍，$\boldsymbol w$ 不变，都留在原来的直线（点线）上](fig/L11-n1.pdf){width=60%}

设 $A$ 是 $n$ 阶方阵。如果有数 $\lambda$ 和**非零**向量 $\boldsymbol v$ 使

$$A\boldsymbol v=\lambda\boldsymbol v ,$$

就称 $\lambda$ 是 $A$ 的**特征值**，$\boldsymbol v$ 是 $A$ 的属于 $\lambda$ 的**特征向量**。上例中 3 和 1 是特征值，$(1,1)^{\mathsf T}$ 属于 3，$(-1,1)^{\mathsf T}$ 属于 1。

定义里有三处要留意。

第一，要求 $\boldsymbol v\ne\boldsymbol 0$，因为 $A\boldsymbol 0=\lambda\boldsymbol 0$ 对任何 $\lambda$ 都成立，零向量说明不了什么。

第二，特征值可以是 0，这时 $A\boldsymbol v=\boldsymbol 0$，这个方向被压成了原点；也可以是负数，这时方向掉头。

第三，由 $A(c\boldsymbol v)=cA\boldsymbol v=\lambda(c\boldsymbol v)$，特征向量的非零倍数仍是属于同一特征值的特征向量。真正确定的是一条过原点的直线，也就是一个方向。

所以可以这样记：**特征向量是变换下不转向的方向，特征值是沿这个方向的伸缩倍数**。用它把其他老朋友过一遍，图里画出了它们各自的不转向的方向。

- 老朋友②（剪切）$\begin{pmatrix}1&1\\0&1\end{pmatrix}$：$x$ 轴上的向量不动（特征值 1），其他方向都被斜推了。只有一条特征方向。
- 老朋友③（转 $90^\circ$）$\begin{pmatrix}0&-1\\1&0\end{pmatrix}$：每个方向都被转了直角，找不到实的特征向量。
- 老朋友④（投影）$\frac12\begin{pmatrix}1&1\\1&1\end{pmatrix}$：直线 $y=x$ 上的向量不动（特征值 1），与它垂直的 $(-1,1)^{\mathsf T}$ 被压成零（特征值 0）。

![实线箭头是原向量，虚线箭头是像。左：剪切只让 $x$ 轴方向不转；中：转 $90^\circ$ 让每个方向都转了；右：投影让 $y=x$ 方向不动，$(-1,1)^{\mathsf T}$ 方向压成原点](fig/L11-n2.pdf){width=90%}

这个「不转向的方向」的说法在旋转处失灵：下一节会看到，旋转的特征值是复数，对应的特征向量分量也是复数，不是实平面上能画出的箭头。

**方法 1（验证特征向量）**

1. 算出 $A\boldsymbol v$（$\boldsymbol v\ne\boldsymbol 0$），看它是不是 $\boldsymbol v$ 的倍数；倍数就是特征值。
2. 含参数时，令 $A\boldsymbol v=\lambda\boldsymbol v$ 的各个分量相等，解出参数和 $\lambda$。

**例 1**　设 $A=\begin{pmatrix}2&1&1\\1&2&1\\1&1&2\end{pmatrix}$，$\boldsymbol\alpha=(1,k,1)^{\mathsf T}$ 是 $A$ 的特征向量，求 $k$ 和对应的特征值。

思路：按方法 1 第 2 步，比较 $A\boldsymbol\alpha$ 与 $\lambda\boldsymbol\alpha$ 的各个分量。

第一步，算 $A\boldsymbol\alpha=(k+3,\ 2k+2,\ k+3)^{\mathsf T}$，它要等于 $\lambda(1,k,1)^{\mathsf T}$。

第二步，比较第一个分量得 $\lambda=k+3$，代入第二个分量：

$$2k+2=k(k+3),\qquad\text{即}\quad k^2+k-2=0,$$

所以 $k=1$ 或 $k=-2$。第三个分量与第一个相同，不再给出新条件。

第三步，回代。$k=1$ 时 $\lambda=4$，验算 $A(1,1,1)^{\mathsf T}=(4,4,4)^{\mathsf T}$；$k=-2$ 时 $\lambda=1$，验算 $A(1,-2,1)^{\mathsf T}=(1,-2,1)^{\mathsf T}$。

> 设 $A=\begin{pmatrix}3&2\\2&0\end{pmatrix}$，判断 $(2,1)^{\mathsf T}$、$(1,-2)^{\mathsf T}$、$(1,1)^{\mathsf T}$ 是不是 $A$ 的特征向量。
>
> 答案：$A(2,1)^{\mathsf T}=(8,4)^{\mathsf T}=4(2,1)^{\mathsf T}$，是，特征值 4；$A(1,-2)^{\mathsf T}=(-1,2)^{\mathsf T}=-(1,-2)^{\mathsf T}$，是，特征值 $-1$；$A(1,1)^{\mathsf T}=(5,2)^{\mathsf T}$ 不是 $(1,1)^{\mathsf T}$ 的倍数，不是。

合上书，写出特征值和特征向量的定义，说明为什么要求 $\boldsymbol v\ne\boldsymbol 0$，并说出四个老朋友各有几条不转向的方向。

### 2. 特征值和特征向量怎样求？

方法 1 要先有候选向量。直接找的办法是把 $A\boldsymbol v=\lambda\boldsymbol v$ 改写成方程组。$\lambda\boldsymbol v=\lambda E\boldsymbol v$（$E$ 是与 $A$ 同阶的单位矩阵），移项得

$$(\lambda E-A)\boldsymbol v=\boldsymbol 0 .$$

对固定的 $\lambda$，这是齐次方程组，特征向量就是它的非零解。用变换的话说：$\lambda E-A$ 要把某个非零方向压成原点，也就是把空间压扁。方阵的齐次方程组有非零解当且仅当系数行列式为 0（L.6.3），所以 $\lambda$ 是特征值当且仅当

$$|\lambda E-A|=0 .$$

它叫 $A$ 的**特征方程**。左边是 $\lambda$ 的 $n$ 次多项式，首项系数是 1（第 3 节说明），叫**特征多项式**。写成 $\lambda E-A$ 而不是 $A-\lambda E$，就是为了首项系数为 1，两者的根相同。

求出特征值 $\lambda_i$ 后，解 $(\lambda_iE-A)\boldsymbol x=\boldsymbol 0$，求出基础解系 $\boldsymbol\xi_1,\dots,\boldsymbol\xi_s$（L.9.2）。属于 $\lambda_i$ 的全部特征向量就是 $k_1\boldsymbol\xi_1+\cdots+k_s\boldsymbol\xi_s$（$k_j$ 不全为 0）。解空间 $N(\lambda_iE-A)$ 叫属于 $\lambda_i$ 的**特征子空间**，它比全体特征向量多一个零向量。

**方法 2（求特征值和特征向量）**

1. 展开 $|\lambda E-A|$ 并分解因式，得到全部特征值。
2. 对每个 $\lambda_i$，把 $\lambda_iE-A$ 消元，写出基础解系；特征向量是它们不全为零的组合。
3. 验算 $A\boldsymbol\xi=\lambda_i\boldsymbol\xi$。

**例 2**　求 $A=\begin{pmatrix}4&-2\\1&1\end{pmatrix}$ 的特征值和特征向量。

第一步，特征多项式：

$$|\lambda E-A|=\begin{vmatrix}\lambda-4&2\\-1&\lambda-1\end{vmatrix}=(\lambda-4)(\lambda-1)+2=\lambda^2-5\lambda+6=(\lambda-2)(\lambda-3),$$

特征值是 2 和 3。

第二步，$\lambda=2$ 时 $2E-A=\begin{pmatrix}-2&2\\-1&1\end{pmatrix}$，两行成比例，方程化为 $x_1=x_2$，基础解系 $(1,1)^{\mathsf T}$，特征向量是 $k(1,1)^{\mathsf T}$（$k\ne0$）。

第三步，$\lambda=3$ 时 $3E-A=\begin{pmatrix}-1&2\\-1&2\end{pmatrix}$，方程化为 $x_1=2x_2$，特征向量是 $k(2,1)^{\mathsf T}$（$k\ne0$）。验算：$A(2,1)^{\mathsf T}=(6,3)^{\mathsf T}=3(2,1)^{\mathsf T}$。

> 求 $A=\begin{pmatrix}5&-1\\3&1\end{pmatrix}$ 的特征值和特征向量。
>
> 答案：$|\lambda E-A|=(\lambda-5)(\lambda-1)+3=(\lambda-2)(\lambda-4)$。$\lambda=2$：$-3x_1+x_2=0$，特征向量 $k(1,3)^{\mathsf T}$；$\lambda=4$：$x_1=x_2$，特征向量 $k(1,1)^{\mathsf T}$，$k\ne0$。

三阶矩阵的难点在分解特征多项式。有两条路，下面各用一道例题示范。

第一条路：展开以前先用行列式的性质提出公因式。最常见的信号是各行元素之和都相等，这时把后几列都加到第一列。

**例 3**　求例 1 中 $A$ 的特征值和特征向量。

第一步，提公因式。$\lambda E-A$ 每行元素之和都是 $\lambda-4$。把第二、三列加到第一列，第一列变成三个 $\lambda-4$，提出来；再用第二、三行减去第一行，化成三角形：

$$|\lambda E-A|=(\lambda-4)\begin{vmatrix}1&-1&-1\\1&\lambda-2&-1\\1&-1&\lambda-2\end{vmatrix}=(\lambda-4)\begin{vmatrix}1&-1&-1\\0&\lambda-1&0\\0&0&\lambda-1\end{vmatrix}=(\lambda-4)(\lambda-1)^2 .$$

特征值是 4 和 1（二重）。

第二步，$\lambda=4$。$4E-A=\begin{pmatrix}2&-1&-1\\-1&2&-1\\-1&-1&2\end{pmatrix}$，每行之和为 0，所以 $(1,1,1)^{\mathsf T}$ 是解；前两行不成比例，秩是 2，解空间是 1 维，基础解系就是 $(1,1,1)^{\mathsf T}$。

第三步，$\lambda=1$。$E-A$ 的三行都是 $(-1,-1,-1)$，方程只剩 $x_1+x_2+x_3=0$，取 $x_2,x_3$ 为自由未知量，基础解系 $\boldsymbol\xi_2=(-1,1,0)^{\mathsf T}$、$\boldsymbol\xi_3=(-1,0,1)^{\mathsf T}$，特征向量是 $k_2\boldsymbol\xi_2+k_3\boldsymbol\xi_3$（$k_2,k_3$ 不全为 0）。例 1 的 $(1,-2,1)^{\mathsf T}=-2\boldsymbol\xi_2+\boldsymbol\xi_3$ 就在其中。

第二条路：展开成三次多项式再试根。$A$ 的元都是整数时，特征多项式 $\lambda^3+b\lambda^2+c\lambda+d$ 首项系数为 1、其余系数都是整数。如果整数 $r$ 是根，由 $r^3+br^2+cr+d=0$ 得 $d=-r(r^2+br+c)$，括号里是整数，所以 $r$ 整除常数项 $d$。于是只需在 $d$ 的因数里试（$d=0$ 时 0 本身就是根）。试出 $r$ 后，由因式定理，$\lambda-r$ 是因式，再用带余除法（C.11.7）降成二次。

**例 4**　求 $A=\begin{pmatrix}2&-1&-2\\1&3&1\\-1&1&3\end{pmatrix}$ 的特征值和特征向量。

和例 3 不同，这里各行之和不相等，看不出公因式，就直接展开。

第一步，按第一行展开，并用 $(\lambda-3)^2-1=(\lambda-2)(\lambda-4)$：

$$|\lambda E-A|=\begin{vmatrix}\lambda-2&1&2\\-1&\lambda-3&-1\\1&-1&\lambda-3\end{vmatrix}=(\lambda-2)^2(\lambda-4)+(\lambda-4)-2(\lambda-4)=\lambda^3-8\lambda^2+19\lambda-12 .$$

第二步，试根。常数项 $-12$ 的因数里先试 $\lambda=1$：$1-8+19-12=0$。所以 $\lambda-1$ 是因式，带余除法得

$$\lambda^3-8\lambda^2+19\lambda-12=(\lambda-1)(\lambda^2-7\lambda+12)=(\lambda-1)(\lambda-3)(\lambda-4).$$

（细心的话，第一步的三项都含 $\lambda-4$，本可以直接提出来。）

第三步，$\lambda=4$。$4E-A=\begin{pmatrix}2&1&2\\-1&1&-1\\1&-1&1\end{pmatrix}$，第一行加第二行的 2 倍得 $(0,3,0)$，所以 $x_2=0$；第三行给出 $x_1+x_3=0$。特征向量 $k(1,0,-1)^{\mathsf T}$，验算 $A(1,0,-1)^{\mathsf T}=(4,0,-4)^{\mathsf T}$。

第四步，$\lambda=1$。$E-A=\begin{pmatrix}-1&1&2\\-1&-2&-1\\1&-1&-2\end{pmatrix}$，第三行是第一行的 $-1$ 倍；第二行减第一行得 $(0,-3,-3)$，所以 $x_2=-x_3$，代回第一行 $-x_1+x_2+2x_3=0$ 得 $x_1=x_3$。特征向量 $k(1,-1,1)^{\mathsf T}$。

第五步，$\lambda=3$。$3E-A=\begin{pmatrix}1&1&2\\-1&0&-1\\1&-1&0\end{pmatrix}$，第二行给出 $x_1=-x_3$，第三行给出 $x_2=x_1$，特征向量 $k(1,1,-1)^{\mathsf T}$（以上 $k\ne0$）。验算 $A(1,1,-1)^{\mathsf T}=(3,3,-3)^{\mathsf T}$。

回到章首的 PageRank，看特征值 1 的特征向量怎样给网页打分。

**例 5**　三个网页：网页 1 链接到网页 2 和 3，网页 2 链接到网页 3，网页 3 链接到网页 1。按 PageRank 的规则，每个网页把自己的分数平均分给它链接到的网页，一个网页的分数等于它收到的份额之和。求各网页的分数（分数之和为 1）。

![三个网页的链接：箭头上的数是分出去的比例；网页 1 把分数对半分给 2 和 3，网页 2、3 各把分数全给唯一的链接对象](fig/L11-n3.pdf){width=45%}

第一步，列方程。记分数向量 $\boldsymbol x=(x_1,x_2,x_3)^{\mathsf T}$。网页 1 只收到网页 3 的全部分数，网页 2 收到网页 1 的一半，网页 3 收到网页 1 的一半和网页 2 的全部：

$$x_1=x_3,\qquad x_2=\tfrac12x_1,\qquad x_3=\tfrac12x_1+x_2,\qquad\text{即}\quad \boldsymbol x=M\boldsymbol x,\quad M=\begin{pmatrix}0&0&1\\ \frac12&0&0\\ \frac12&1&0\end{pmatrix}.$$

$M$ 的第 $j$ 列记录网页 $j$ 的分数怎样分出去，每列之和为 1。$\boldsymbol x=M\boldsymbol x$ 说的正是：$\boldsymbol x$ 是 $M$ 属于特征值 1 的特征向量。

第二步，解 $(E-M)\boldsymbol x=\boldsymbol 0$。由前两式 $x_3=x_1$、$x_2=\frac12x_1$，第三式自动成立，基础解系是 $(2,1,2)^{\mathsf T}$；按分数之和为 1 缩放，得 $(0.4,0.2,0.4)^{\mathsf T}$。

网页 1 只被一个网页链接，分数却和网页 3 一样高，因为链接它的网页 3 分数高，并且把分数全给了它。为什么 1 一定是这种矩阵的特征值，实际中怎样用反复相乘求这个向量，见 L.12.7。

#### 特征方程没有实根时

上面几道例题的特征方程都有实根。但特征方程也可能没有实根。老朋友③的特征多项式是 $\begin{vmatrix}\lambda&1\\-1&\lambda\end{vmatrix}=\lambda^2+1$，在实数里无解，和「每个方向都被转动」一致；在复数里它有两个根 $\pm\mathrm i$。

一般地，**代数基本定理**说：$n$ 次多项式在复数范围内按重数计恰有 $n$ 个根。

为什么一定有根？可以这样想。让 $\lambda$ 沿复平面上一个很大的圆走一圈，这时 $\lambda^n$ 远远压过其余各项，多项式的值近似于 $\lambda^n$，它绕原点转 $n$ 圈。把圆连续地缩小到原点附近，多项式的值接近常数项，几乎不动，不再绕圈。这里的圈数指多项式的值绕原点转了几圈，它只能是整数，不能从 $n$ 一点点连续地变到 0；圈数要变，只能在曲线经过原点的那一刻发生，那一刻多项式等于 0。找到一个根 $r$ 以后，除以 $\lambda-r$ 降一次，再找下一个，一共 $n$ 个。把这个想法写严格要仔细处理「连续变化」，高斯 1799 年的博士论文给出了早期的一个证明。

用到特征多项式上：$n$ 阶方阵按重数计恰有 $n$ 个复特征值；不同的特征值可能少于 $n$ 个（例 3），实特征值也可能一个都没有（老朋友③）。考研题里求特征向量都在实数范围内进行。

合上书，从 $A\boldsymbol v=\lambda\boldsymbol v$ 推出特征方程，说明特征向量是哪个方程组的什么解，再说出分解三阶特征多项式的两条路。

### 3. 不解特征方程，能知道特征值的和与积吗？

例 3 的特征值 4、1、1 之和是 6，正好是对角元之和 $2+2+2$；之积是 4，而 $|A|=4$。例 4 的 $1+3+4=8=2+3+3$，$1\cdot3\cdot4=12=|A|$，也是这样。方阵对角元之和叫**迹**，记作 $\operatorname{tr}A$。下面说明这两个关系对任何方阵都成立。

先看二阶。直接展开，

$$\begin{vmatrix}\lambda-a&-b\\-c&\lambda-d\end{vmatrix}=\lambda^2-(a+d)\lambda+(ad-bc),$$

而它又等于 $(\lambda-\lambda_1)(\lambda-\lambda_2)=\lambda^2-(\lambda_1+\lambda_2)\lambda+\lambda_1\lambda_2$。比较系数，$\lambda_1+\lambda_2=a+d$，$\lambda_1\lambda_2=ad-bc$。

$n$ 阶时同样比较两种写法的系数。由代数基本定理，$f(\lambda)=|\lambda E-A|=(\lambda-\lambda_1)\cdots(\lambda-\lambda_n)$（特征值按重数列出）。右边 $\lambda^{n-1}$ 的系数是 $-(\lambda_1+\cdots+\lambda_n)$，常数项是 $(-1)^n\lambda_1\cdots\lambda_n$。左边分两件事看。

常数项：令 $\lambda=0$，$f(0)=|-A|=(-1)^n|A|$。

$\lambda^{n-1}$ 项：在完全展开式（L.6.5）里，每一项从每行每列各取一个元。只要有一个元不在对角线上，比如取了第 $i$ 行第 $j$ 列（$i\ne j$），第 $i$ 行和第 $j$ 列的对角元就都取不到了，而 $\lambda$ 只出现在对角元 $\lambda-a_{ii}$ 里，非对角元都是常数，所以这一项至多含 $n-2$ 个 $\lambda$。所以 $\lambda^n$、$\lambda^{n-1}$ 只来自对角线乘积 $(\lambda-a_{11})\cdots(\lambda-a_{nn})$，首项系数是 1，$\lambda^{n-1}$ 的系数是 $-(a_{11}+\cdots+a_{nn})$。比较得

$$\lambda_1+\cdots+\lambda_n=\operatorname{tr}A,\qquad \lambda_1\lambda_2\cdots\lambda_n=|A| .$$

由第二式，$A$ 可逆当且仅当 0 不是特征值。这和第 1 节一致：特征值 0 表示有方向被压成原点，被压扁的变换撤销不了。可逆大定理由此添了一条。

迹还有一条常用性质：$A$ 是 $m\times n$、$B$ 是 $n\times m$ 矩阵时，$\operatorname{tr}(AB)=\operatorname{tr}(BA)$。理由是 $AB$ 的第 $i$ 个对角元是 $\sum_ja_{ij}b_{ji}$，所以 $\operatorname{tr}(AB)=\sum_i\sum_ja_{ij}b_{ji}$；而 $\operatorname{tr}(BA)=\sum_j\sum_ib_{ji}a_{ij}$，是同一批乘积换了求和顺序。例如对列向量 $\boldsymbol\alpha,\boldsymbol\beta$，$\operatorname{tr}(\boldsymbol\alpha\boldsymbol\beta^{\mathsf T})=\boldsymbol\beta^{\mathsf T}\boldsymbol\alpha$，$n$ 阶矩阵 $\boldsymbol\alpha\boldsymbol\beta^{\mathsf T}$ 的特征值之和就是一个数。

**方法 3（用迹和行列式）**

1. 已知部分特征值时，用「和等于迹、积等于行列式」求其余的。
2. 矩阵含参数时，列出这两个方程解参数。
3. 二阶矩阵的特征多项式直接写成 $\lambda^2-(\operatorname{tr}A)\lambda+|A|$。

**例 6**　设 $A=\begin{pmatrix}1&-1&1\\2&4&-2\\-3&-3&a\end{pmatrix}$ 以 2 为二重特征值，求 $a$ 和另一个特征值 $\lambda_3$。

思路：两个未知数，用两个关系各列一个方程。

第一步，迹：$1+4+a=2+2+\lambda_3$，所以 $\lambda_3=a+1$。

第二步，行列式按第一行展开：

$$|A|=1\cdot(4a-6)+1\cdot(2a-6)+1\cdot(-6+12)=6a-6,$$

它等于 $2\cdot2\cdot\lambda_3=4(a+1)$，解得 $a=5$，$\lambda_3=6$。

第三步，检验：$a=5$ 时 $|A|=24=2\cdot2\cdot6$，迹 $10=2+2+6$。

> 已知 $A=\begin{pmatrix}a&2\\2&1\end{pmatrix}$ 的一个特征值是 5，求 $a$ 和另一个特征值。
>
> 答案：设另一个为 $\mu$，则 $a+1=5+\mu$，$a-4=5\mu$。两式相减得 $5=5-4\mu$，所以 $\mu=0$，$a=4$。

合上书，用二阶矩阵说明「和等于迹、积等于行列式」，再说明 $n$ 阶时常数项和 $\lambda^{n-1}$ 的系数各从哪里来。

### 4. $A^k$、$f(A)$、$A^{-1}$、$A^*$ 的特征值是什么？

设 $A\boldsymbol v=\lambda\boldsymbol v$。两边再左乘 $A$：

$$A^2\boldsymbol v=A(\lambda\boldsymbol v)=\lambda A\boldsymbol v=\lambda^2\boldsymbol v .$$

照这样一次次乘下去，对整数 $k\ge0$ 有 $A^k\boldsymbol v=\lambda^k\boldsymbol v$：同一个方向被拉伸 $k$ 次。对多项式 $f(x)=a_0+a_1x+\cdots+a_mx^m$，记 $f(A)=a_0E+a_1A+\cdots+a_mA^m$（L.3.5），逐项相加得

$$f(A)\boldsymbol v=f(\lambda)\boldsymbol v .$$

所以 $\boldsymbol v$ 也是 $f(A)$ 的特征向量，特征值是 $f(\lambda)$。

反过来，$f(A)$ 的特征向量不一定是 $A$ 的特征向量。拿老朋友③试：转两次直角就是掉头，$A^2=-E$，每个非零向量都是 $A^2$ 的特征向量（特征值 $-1$），而 $A$ 本身一个实特征向量也没有。

#### 逆矩阵、伴随矩阵和转置

再看 $A^{-1}$。$A$ 可逆时特征值都不为 0（第 3 节）。在 $A\boldsymbol v=\lambda\boldsymbol v$ 两边左乘 $A^{-1}$ 得 $\boldsymbol v=\lambda A^{-1}\boldsymbol v$，所以 $A^{-1}\boldsymbol v=\frac1\lambda\boldsymbol v$：撤销变换，伸缩倍数取倒数。伴随矩阵（本书 $A^*$ 专指伴随矩阵）满足 $A^*=|A|A^{-1}$（L.6.8，$A$ 可逆），所以 $A^*\boldsymbol v=\frac{|A|}{\lambda}\boldsymbol v$。

$A^{\mathsf T}$ 和这些不一样。转置不改变行列式，$|\lambda E-A^{\mathsf T}|=|(\lambda E-A)^{\mathsf T}|=|\lambda E-A|$，所以 $A^{\mathsf T}$ 与 $A$ 的特征值相同。但特征向量一般不同，因为 $A\boldsymbol v=\lambda\boldsymbol v$ 推不出关于 $A^{\mathsf T}\boldsymbol v$ 的任何等式。例如 $A=\begin{pmatrix}2&1\\0&3\end{pmatrix}$ 属于 2 的特征向量是 $(1,0)^{\mathsf T}$，而 $A^{\mathsf T}(1,0)^{\mathsf T}=(2,1)^{\mathsf T}$ 不是它的倍数；$A^{\mathsf T}$ 属于 2 的特征向量是 $(-1,1)^{\mathsf T}$。

到这里，可以把「哪个能换、哪个不能换」列成一张表（设 $A\boldsymbol v=\lambda\boldsymbol v$）：

| 矩阵 | 特征值 | $\boldsymbol v$ 还是它的特征向量吗 |
|---|---|---|
| $A^k$、$f(A)$ | $\lambda^k$、$f(\lambda)$ | 是 |
| $A^{-1}$（$A$ 可逆） | $\frac1\lambda$ | 是 |
| $A^*$（$A$ 可逆） | $\frac{\lvert A\rvert}{\lambda}$ | 是 |
| $A^{\mathsf T}$ | $\lambda$（特征值相同） | 一般不是 |

#### $|f(A)|$ 为什么等于 $f(\lambda_i)$ 之积

算行列式 $|f(A)|$ 时，还要知道 $f(A)$ 的 $n$ 个特征值恰好是 $f(\lambda_1),\dots,f(\lambda_n)$，连重数也对得上。直接算行列式，分三步。

1. 在复数范围内分解 $f(x)=c(x-r_1)\cdots(x-r_m)$。$A$ 的多项式相乘和普通多项式一样，所以 $f(A)=c(A-r_1E)\cdots(A-r_mE)$。
2. 每个因子的行列式：由特征多项式的分解，$|A-rE|=(-1)^n|rE-A|=(\lambda_1-r)\cdots(\lambda_n-r)$。
3. 用乘积公式把 $m$ 个行列式乘起来，再把因子按 $\lambda_i$ 重新分组：

$$|f(A)|=c^n\prod_{j}|A-r_jE|=\prod_{i=1}^{n}\Big(c\prod_j(\lambda_i-r_j)\Big)=f(\lambda_1)f(\lambda_2)\cdots f(\lambda_n).$$

把这个式子用在 $f(x)-\mu$ 上，得 $|f(A)-\mu E|=\prod_i\big(f(\lambda_i)-\mu\big)$，所以 $f(A)$ 的特征值按重数恰好是 $f(\lambda_i)$。

#### 一个要防住的直觉

$A$、$B$ 各有特征值，$A+B$ 的特征值一般不是它们相加，因为两者的特征向量不同。例如 $\begin{pmatrix}0&1\\0&0\end{pmatrix}$ 和 $\begin{pmatrix}0&0\\1&0\end{pmatrix}$ 的特征值都只有 0，它们的和 $\begin{pmatrix}0&1\\1&0\end{pmatrix}$ 的特征值却是 $\pm1$。上面的规则只对同一个 $A$ 的多项式成立。

**方法 4（由 A 的特征值求相关矩阵的特征值）**

1. 把表达式里的 $A$ 换成 $\lambda$：$A^k\to\lambda^k$，$f(A)\to f(\lambda)$，$A^{-1}\to\frac1\lambda$，$A^*\to\frac{|A|}{\lambda}$。
2. $A$ 的特征向量仍是这些矩阵的特征向量，但它们可能多出特征向量。
3. $|f(A)|$ 等于各个 $f(\lambda_i)$ 之积，其中有一个为 0 就不可逆。

**例 7**　三阶矩阵 $A$ 的特征值为 $1,-1,2$，求 $|A^*+3A-2E|$。

第一步，$|A|=1\cdot(-1)\cdot2=-2$。

第二步，对属于 $\lambda$ 的特征向量 $\boldsymbol v$，

$$(A^*+3A-2E)\boldsymbol v=\Big(\frac{-2}{\lambda}+3\lambda-2\Big)\boldsymbol v ,$$

三个特征值依次是 $-2+3-2=-1$，$2-3-2=-3$，$-1+6-2=3$，所以所求行列式是 $(-1)(-3)\cdot3=9$。

这里要多想一步。上面算出的三个数确实都是 $A^*+3A-2E$ 的特征值，因为各有特征向量；但「行列式等于它们之积」要求它们恰好是全部特征值、重数也对得上，而三步公式只对多项式 $f(A)$ 证过，$A^*=|A|A^{-1}$ 里有逆矩阵。（这道题的三个特征值互不相同，这样直接算其实是对的，理由要用第 5 节和 L.12 的对角化。）稳妥的做法是先乘一个 $A$，化成多项式：$(A^*+3A-2E)A=|A|E+3A^2-2A$，它的行列式是 $\prod(3\lambda_i^2-2\lambda_i-2)=(-1)\cdot3\cdot6=-18$，除以 $|A|=-2$ 也得 9。

> 三阶矩阵 $A$ 的特征值为 $1,2,3$，求 $|A^2-2A+3E|$ 和 $A^{-1}$ 的特征值。
>
> 答案：$\lambda^2-2\lambda+3$ 在 $1,2,3$ 处的值是 $2,3,6$，行列式为 36；$A^{-1}$ 的特征值是 $1,\frac12,\frac13$。

**例 8**　设 $A^2=A$，证明 $A$ 的特征值只能是 0 或 1。

和例 7 方向相反：这里不知道特征值，只知道一个矩阵等式，要从等式反推特征值。

设 $A\boldsymbol v=\lambda\boldsymbol v$，$\boldsymbol v\ne\boldsymbol 0$。一方面 $A^2\boldsymbol v=\lambda^2\boldsymbol v$，另一方面 $A^2\boldsymbol v=A\boldsymbol v=\lambda\boldsymbol v$。相减得 $(\lambda^2-\lambda)\boldsymbol v=\boldsymbol 0$；$\boldsymbol v\ne\boldsymbol 0$，所以 $\lambda^2-\lambda=0$，$\lambda=0$ 或 1。

老朋友④满足 $P^2=P$（L.10.2），两个值都取到了：直线 $y=x$ 上的向量属于 1，与它垂直的方向属于 0。但这样得到的只是候选值：$E^2=E$，而 $E$ 没有特征值 0。同理 $A^2=O$ 时特征值全是 0，可 $A$ 不一定是零矩阵，例如 $\begin{pmatrix}0&1\\0&0\end{pmatrix}$。

合上书，从 $A\boldsymbol v=\lambda\boldsymbol v$ 推出 $f(A)\boldsymbol v=f(\lambda)\boldsymbol v$ 和 $A^{-1}$、$A^*$ 的特征值，再说出例 8 为什么只得到候选值。

### 5. 属于不同特征值的特征向量为什么线性无关？

例 4 的三个特征值互不相同，三个特征向量 $(1,-1,1)^{\mathsf T}$、$(1,1,-1)^{\mathsf T}$、$(1,0,-1)^{\mathsf T}$ 排成的行列式是 $-2\ne0$，所以线性无关。这不是巧合。

**定理**　设 $\lambda_1,\dots,\lambda_k$ 互不相同，$\boldsymbol v_i$ 是属于 $\lambda_i$ 的特征向量，则 $\boldsymbol v_1,\dots,\boldsymbol v_k$ 线性无关。

思路：从一个线性关系出发，用 $A$ 作用一次，再减去适当的倍数，消掉一个向量，关系就落到更少的向量上，而那里已经知道无关。先看 $k=2$：设 $c_1\boldsymbol v_1+c_2\boldsymbol v_2=\boldsymbol 0$，用 $A$ 作用得 $c_1\lambda_1\boldsymbol v_1+c_2\lambda_2\boldsymbol v_2=\boldsymbol 0$，减去原式的 $\lambda_2$ 倍得 $c_1(\lambda_1-\lambda_2)\boldsymbol v_1=\boldsymbol 0$，所以 $c_1=0$，再得 $c_2=0$。一般情形对个数 $k$ 归纳：

1. $k=1$ 时，特征向量非零，一个非零向量线性无关。
2. 设 $k-1$ 个时结论成立，从 $c_1\boldsymbol v_1+\cdots+c_k\boldsymbol v_k=\boldsymbol 0$（记作 ①）出发。
3. 用 $A$ 作用于 ①，得 $c_1\lambda_1\boldsymbol v_1+\cdots+c_k\lambda_k\boldsymbol v_k=\boldsymbol 0$；减去 ① 的 $\lambda_k$ 倍，$\boldsymbol v_k$ 被消掉：$c_1(\lambda_1-\lambda_k)\boldsymbol v_1+\cdots+c_{k-1}(\lambda_{k-1}-\lambda_k)\boldsymbol v_{k-1}=\boldsymbol 0$。
4. 由归纳假设，每个 $c_i(\lambda_i-\lambda_k)=0$；特征值互不相同，$\lambda_i-\lambda_k\ne0$，所以 $c_1=\cdots=c_{k-1}=0$。
5. 代回 ① 得 $c_k\boldsymbol v_k=\boldsymbol 0$，而 $\boldsymbol v_k\ne\boldsymbol 0$，所以 $c_k=0$。

「互不相同」只在第 4 步用到。推论：$n$ 阶矩阵有 $n$ 个不同的特征值时，必有 $n$ 个线性无关的特征向量，L.12 的对角化要用它。更进一步，从每个特征子空间里各取一组线性无关的向量，合在一起仍线性无关。理由分两层。设合起来的组合为零，把属于同一个 $\lambda_i$ 的项加在一起记作 $\boldsymbol w_i$，它要么是零，要么是属于 $\lambda_i$ 的特征向量。第一层：如果有几个 $\boldsymbol w_i$ 不为零，它们之和为零，与定理矛盾，所以每个 $\boldsymbol w_i=\boldsymbol 0$。第二层：$\boldsymbol w_i$ 是第 $i$ 组向量的组合，这组本身线性无关，所以组内系数全为 0。

**方法 5（用「作用一次再相减」处理特征向量的组合）**

1. 要证几个特征向量的组合有什么性质（无关、不是特征向量），先写出组合满足的等式。
2. 用 $A$ 作用一次，与原式的倍数相减，或者直接比较。
3. 用「不同特征值的特征向量线性无关」比较系数。

**例 9**　设 $\lambda_1\ne\lambda_2$ 是 $A$ 的特征值，$\boldsymbol v_1,\boldsymbol v_2$ 是对应的特征向量，证明 $\boldsymbol v_1+\boldsymbol v_2$ 不是 $A$ 的特征向量。

用反证法。假设 $A(\boldsymbol v_1+\boldsymbol v_2)=\mu(\boldsymbol v_1+\boldsymbol v_2)$，左边等于 $\lambda_1\boldsymbol v_1+\lambda_2\boldsymbol v_2$，移项得

$$(\lambda_1-\mu)\boldsymbol v_1+(\lambda_2-\mu)\boldsymbol v_2=\boldsymbol 0 .$$

由定理 $\boldsymbol v_1,\boldsymbol v_2$ 线性无关，两个系数都为 0，于是 $\lambda_1=\mu=\lambda_2$，与 $\lambda_1\ne\lambda_2$ 矛盾。

把它和同一个特征值的情形并排看。$\boldsymbol v_1,\boldsymbol v_2$ 都属于 $\lambda$ 时，$A(\boldsymbol v_1+\boldsymbol v_2)=\lambda(\boldsymbol v_1+\boldsymbol v_2)$，和只要不是零向量就仍是特征向量，因为特征子空间对加法封闭。属于不同特征值时，和永远不是特征向量。差别在于相加的两部分伸缩倍数是否一致：倍数不同，合起来的箭头就会被拉歪。

> 设 $A\boldsymbol v_1=\boldsymbol v_1$，$A\boldsymbol v_2=2\boldsymbol v_2$（$\boldsymbol v_1,\boldsymbol v_2$ 非零），判断 $\boldsymbol v_1-2\boldsymbol v_2$ 是不是 $A$ 的特征向量，是不是 $A^2-3A$ 的特征向量。
>
> 答案：不是 $A$ 的特征向量，理由和例 9 相同。$A^2-3A$ 对应 $f(\lambda)=\lambda^2-3\lambda$，$f(1)=f(2)=-2$，所以 $\boldsymbol v_1,\boldsymbol v_2$ 都属于 $A^2-3A$ 的同一个特征值 $-2$，$\boldsymbol v_1-2\boldsymbol v_2\ne\boldsymbol 0$ 是它的特征向量。

合上书，默写定理证明的五步，说清楚「作用一次再相减」是为了消掉什么。

### 6. 特征值是重根时，特征向量够不够用？

例 3 中 1 是二重根，解出了两个线性无关的特征向量。老朋友②（剪切）的特征多项式是 $(\lambda-1)^2$，1 也是二重根，可

$$E-\begin{pmatrix}1&1\\0&1\end{pmatrix}=\begin{pmatrix}0&-1\\0&0\end{pmatrix}$$

的秩是 1，方程只给出 $x_2=0$，特征向量只有 $k(1,0)^{\mathsf T}$ 一个方向。这和第 1 节的图一致：剪切把 $x$ 轴以外的方向都斜推了。可见重根不保证有同样多的特征向量。

特征值 $\lambda_i$ 作为特征多项式的根的重数，叫它的**代数重数**；特征子空间 $N(\lambda_iE-A)$ 的维数，即属于 $\lambda_i$ 的线性无关特征向量的最多个数，叫它的**几何重数**。由 L.8.4，

$$\text{几何重数}=n-r(\lambda_iE-A).$$

两者的关系是

$$1\le\text{几何重数}\le\text{代数重数}.$$

左边成立，因为 $\lambda_i$ 是特征值，至少有一个特征向量。右边的证明要用换基，放在 L.12.2；直观地说，有 $g$ 个独立的方向都被拉伸 $\lambda_i$ 倍，特征多项式里就至少有 $g$ 个因式 $\lambda-\lambda_i$。所以单根的几何重数一定是 1，只有重根需要检查。剪切的 1 代数重数 2、几何重数 1；例 3 的 1 两者都是 2。L.12 会看到，特征多项式能完全分解时，两种重数处处相等正是矩阵能对角化的条件。

**方法 6（判断重根的几何重数）**

1. 先求出特征值和代数重数。
2. 对每个重根 $\lambda_i$ 求 $r(\lambda_iE-A)$，几何重数是 $n-r(\lambda_iE-A)$，与代数重数比较。
3. 单根不必检查。

**例 10**　设 $A=\begin{pmatrix}1&2&-3\\-1&4&-3\\1&a&5\end{pmatrix}$ 的特征多项式有重根，求 $a$，并求重根的几何重数。

第一步，提公因式。$\lambda E-A$ 的第一行减去第二行，得 $(\lambda-2,\ 2-\lambda,\ 0)=(\lambda-2)(1,-1,0)$；提出 $\lambda-2$ 后，再把第一列加到第二列，第一行变成 $(1,0,0)$：

$$|\lambda E-A|=(\lambda-2)\begin{vmatrix}1&-1&0\\1&\lambda-4&3\\-1&-a&\lambda-5\end{vmatrix}=(\lambda-2)\begin{vmatrix}\lambda-3&3\\-a-1&\lambda-5\end{vmatrix}=(\lambda-2)(\lambda^2-8\lambda+18+3a).$$

重根有两种来源，分别讨论。

第二步，若 2 是二次式的根，则 $4-16+18+3a=0$，$a=-2$，二次式为 $(\lambda-2)(\lambda-6)$，特征值 $2,2,6$。这时 $2E-A=\begin{pmatrix}1&-2&3\\1&-2&3\\-1&2&-3\end{pmatrix}$ 的秩为 1，几何重数 $3-1=2$，等于代数重数。

第三步，若二次式本身有重根，则判别式 $64-4(18+3a)=0$，$a=-\frac23$，重根 $\lambda=4$，特征值 $2,4,4$。这时 $4E-A=\begin{pmatrix}3&-2&3\\1&0&3\\-1&\frac23&-1\end{pmatrix}$，第三行是第一行的 $-\frac13$ 倍，前两行不成比例，秩为 2，几何重数 $3-2=1$，小于代数重数 2。

> 求 $A=\begin{pmatrix}2&1&0\\0&2&0\\0&0&3\end{pmatrix}$ 各特征值的代数重数和几何重数。
>
> 答案：三角矩阵的特征值是对角元，2 是二重根，3 是单根。$2E-A=\begin{pmatrix}0&-1&0\\0&0&0\\0&0&-1\end{pmatrix}$ 的秩是 2，2 的几何重数为 1；3 是单根，几何重数为 1。

合上书，说出代数重数和几何重数的定义，用剪切说明两者可以不等，再写出几何重数的计算公式。

### 本章小结

| 方法 | 什么时候用 | 对应题号 |
|---|---|---|
| 方法 1（验证特征向量） | 判断给定向量是否特征向量；含参数的特征向量反求参数 | L11-01 |
| 方法 2（求特征值和特征向量） | 由特征方程求特征值，解齐次方程组求特征向量；三阶时提公因式或试根 | L11-02、L11-06 |
| 方法 3（用迹和行列式） | 已知部分特征值求其余；含参数矩阵定参数 | L11-03、L11-07、L11-13、L11-14、L11-15 |
| 方法 4（由 A 的特征值求相关矩阵的特征值） | $A^k$、$f(A)$、$A^{-1}$、$A^*$ 的特征值，$\lvert f(A)\rvert$，可逆性；由矩阵等式定特征值的候选 | L11-04、L11-05、L11-08、L11-11、L11-13、L11-14、L11-15 |
| 方法 5（作用一次再相减） | 证明特征向量线性无关、某个组合不是特征向量 | L11-09 |
| 方法 6（判断重根的几何重数） | 重根时数线性无关的特征向量，为对角化做准备 | L11-10、L11-12 |

$n$ 阶方阵 $A$ 可逆的等价条件到这里是：

| 等价条件 | 出处 |
|---|---|
| 消元后有 $n$ 个主元；$A\boldsymbol x=\boldsymbol 0$ 只有零解 | L.4 |
| 存在 $B$ 使 $AB=E$ | L.5 |
| $\lvert A\rvert\ne0$ | L.6 |
| 列向量组线性无关；$r(A)=n$ | L.7 |
| 列向量构成 $\mathbb R^n$ 的一组基 | L.8 |
| 0 不是 $A$ 的特征值（本章新增） | L.11 |
