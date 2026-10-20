## L.13 · 实对称矩阵

推荐系统把每两位用户的余弦相似度（L.2.5）填成一张表，这张表一定对称：$i$ 和 $j$ 多像，$j$ 和 $i$ 就多像。数据分析里的协方差矩阵（本章第 5 节）、二阶偏导连续的多元函数的 Hessian 矩阵（L.14.8）也都是对称矩阵。它们有一件 L.12 里得不到保证的好事：总能找到几个互相垂直的方向，矩阵在每个方向上只做伸缩。PCA（M.5）找的就是协方差矩阵的这几个方向。

它来自一个几何问题。斜放的椭圆 $2x^2+2xy+2y^2=1$，对称轴在哪、多长？18 世纪的数学家把它化成解方程，根（就是特征值 $\lambda$）决定半轴长 $1/\sqrt\lambda$，椭球要解三次方程；而三次方程可能有复数根，轴长却不能是复数。柯西在 1829 年对任意多个变量证明了它们都是实数，并且相应的轴总能取成两两垂直。后来希尔伯特研究积分方程时把变换的全部特征值叫作「谱」，核心定理因此叫谱定理。

对称伸缩 ① $\begin{pmatrix}2&1\\1&2\end{pmatrix}$ 把单位圆拉成斜放的椭圆（图 L13-n1）：沿 $(1,1)^{\mathsf T}$ 拉长到 3 倍，沿 $(1,-1)^{\mathsf T}$ 长度不变。这两个方向互相垂直，恰好是椭圆的两条轴。注意这是单位圆的像，半轴是 $\lambda$ 本身（3 和 1），和上一段的椭圆方向相同、长度不同。本章要说明：**每个实对称矩阵都只是沿几条互相垂直的方向各自伸缩。**

![① 把单位圆变成椭圆（阴影）：$\boldsymbol q_1$ 方向被拉到 3 倍，$\boldsymbol q_2$ 方向不变，两条特征方向垂直，就是椭圆的轴；不在特征方向上的 $\boldsymbol e_1$ 被转了方向](fig/L13-n1.pdf){width=58%}

第 1 节说明特征值是实数；第 2 节说明不同特征值的特征方向垂直；第 3 节合成谱定理；第 4 节给出正交对角化的步骤；第 5 节把对称矩阵拆成投影矩阵之和。本章的「对称矩阵」都指实对称矩阵：元素都是实数，并且 $A^{\mathsf T}=A$（L.3.6）。

### 1. 对称矩阵的特征值为什么一定是实数？

转 90° 的 ③ 的特征值 $\pm\mathrm i$ 不是实数（L.11.2）：每个方向都被转走了。对称矩阵会不会也这样？二阶时 $\begin{pmatrix}a&b\\b&c\end{pmatrix}$ 特征方程的判别式是 $(a-c)^2+4b^2\ge0$，根总是实数；$n$ 阶没有判别式可用，需要一个和阶数无关的论证。思路是：先允许 $\lambda$ 是复数，把同一个数用两种办法算出来，一次得到 $\lambda$ 乘某个正数，一次得到 $\bar\lambda$ 乘同一个正数，于是 $\lambda=\bar\lambda$。

#### 准备：复数分量的向量

证明要用三件工具，先逐个备好。

第一件，共轭。复数 $z=a+b\mathrm i$ 的共轭是 $\bar z=a-b\mathrm i$，$z\bar z=a^2+b^2=|z|^2\ge0$，等号只在 $z=0$ 时成立；共轭和加法、乘法可以交换次序。复数是实数，当且仅当它等于自己的共轭。

第二件，一个正数。把复向量 $\boldsymbol v$ 的每个分量取共轭，得到 $\bar{\boldsymbol v}$。一行乘一列得到 $1\times1$ 矩阵，就当作一个数：

$$\bar{\boldsymbol v}^{\mathsf T}\boldsymbol v=\bar v_1v_1+\cdots+\bar v_nv_n=|v_1|^2+\cdots+|v_n|^2.$$

每一项都非负，所以 $\boldsymbol v\ne\boldsymbol0$ 时它是正实数，证明最后要约去它。不能改用 $\boldsymbol v^{\mathsf T}\boldsymbol v$：$\boldsymbol v=(1,\mathrm i)^{\mathsf T}$ 时它是 $1+\mathrm i^2=0$。

第三件，$A$ 是实矩阵时 $\overline{A\boldsymbol v}=A\bar{\boldsymbol v}$，因为取共轭时实数 $a_{ij}$ 不变。

#### 把同一个数算两遍

先在 ① 上看「算两遍」。取 $\boldsymbol v=(1,\mathrm i)^{\mathsf T}$，一次先让 $A$ 作用在 $\boldsymbol v$ 上，一次先让 $A$ 作用在 $\bar{\boldsymbol v}$ 上：

$$\bar{\boldsymbol v}^{\mathsf T}(A\boldsymbol v)=(1,-\mathrm i)\begin{pmatrix}2+\mathrm i\\1+2\mathrm i\end{pmatrix}=4,\qquad (A\bar{\boldsymbol v})^{\mathsf T}\boldsymbol v=(2-\mathrm i,\ 1-2\mathrm i)\begin{pmatrix}1\\\mathrm i\end{pmatrix}=4.$$

结果相同不是巧合：由 $(XY)^{\mathsf T}=Y^{\mathsf T}X^{\mathsf T}$（L.3.6），$(A\bar{\boldsymbol v})^{\mathsf T}\boldsymbol v=\bar{\boldsymbol v}^{\mathsf T}A^{\mathsf T}\boldsymbol v$，而 $A^{\mathsf T}=A$。把 $\boldsymbol v$ 换成特征向量，右边算出 $\lambda$ 乘 $\bar{\boldsymbol v}^{\mathsf T}\boldsymbol v$，左边算出 $\bar\lambda$ 乘同一个数。下面写成考试可以默写的四步。

**定理（对称矩阵的特征值是实数）**　设 $A$ 是实对称矩阵，$A\boldsymbol v=\lambda\boldsymbol v$，$\boldsymbol v\ne\boldsymbol0$（$\lambda$、$\boldsymbol v$ 先允许是复的）。

1. 取共轭：$A$ 是实矩阵，所以 $A\bar{\boldsymbol v}=\bar\lambda\bar{\boldsymbol v}$。
2. 从右边算：$\bar{\boldsymbol v}^{\mathsf T}A\boldsymbol v=\bar{\boldsymbol v}^{\mathsf T}(\lambda\boldsymbol v)=\lambda\,\bar{\boldsymbol v}^{\mathsf T}\boldsymbol v$。
3. 从左边算，先用 $A=A^{\mathsf T}$，再用 $\bar{\boldsymbol v}^{\mathsf T}A^{\mathsf T}=(A\bar{\boldsymbol v})^{\mathsf T}$ 和第 1 步：
$$\bar{\boldsymbol v}^{\mathsf T}A\boldsymbol v=\bar{\boldsymbol v}^{\mathsf T}A^{\mathsf T}\boldsymbol v=(A\bar{\boldsymbol v})^{\mathsf T}\boldsymbol v=\bar\lambda\,\bar{\boldsymbol v}^{\mathsf T}\boldsymbol v.$$
4. 两式相减，$(\lambda-\bar\lambda)\bar{\boldsymbol v}^{\mathsf T}\boldsymbol v=0$；$\bar{\boldsymbol v}^{\mathsf T}\boldsymbol v>0$，所以 $\lambda=\bar\lambda$，$\lambda$ 是实数。

对称性只在第 3 步用了一次。$\lambda$ 是实数以后，$(A-\lambda E)\boldsymbol x=\boldsymbol0$ 用实数消元就有非零解，所以本章从这里开始只用实特征向量。

**方法 1（把 $\bar{\boldsymbol v}^{\mathsf T}A\boldsymbol v$ 算两遍）**

已知 $A^{\mathsf T}=\pm A$、$A^{\mathsf T}A=E$ 这类转置关系，推特征值的性质：

1. 设 $A\boldsymbol v=\lambda\boldsymbol v$，$\boldsymbol v\ne\boldsymbol0$，取共轭得 $A\bar{\boldsymbol v}=\bar\lambda\bar{\boldsymbol v}$；
2. 一次让 $A$ 作用在 $\boldsymbol v$ 上，一次用转置关系把 $A$ 挪到左边作用在 $\bar{\boldsymbol v}$ 上；
3. 令两个结果相等，约去正数 $\bar{\boldsymbol v}^{\mathsf T}\boldsymbol v$。

**例 1**　实矩阵 $A$ 满足 $A^{\mathsf T}=-A$（反对称矩阵）。证明 $A$ 的特征值只能是 0 或纯虚数。

和定理只差第 3 步。第 1、2 步照旧，得 $\bar{\boldsymbol v}^{\mathsf T}A\boldsymbol v=\lambda\,\bar{\boldsymbol v}^{\mathsf T}\boldsymbol v$。第 3 步这次把 $A$ 换成 $-A^{\mathsf T}$：

$$\bar{\boldsymbol v}^{\mathsf T}A\boldsymbol v=-\bar{\boldsymbol v}^{\mathsf T}A^{\mathsf T}\boldsymbol v=-(A\bar{\boldsymbol v})^{\mathsf T}\boldsymbol v=-\bar\lambda\,\bar{\boldsymbol v}^{\mathsf T}\boldsymbol v.$$

两式相等，约去正数得 $\lambda=-\bar\lambda$。写 $\lambda=a+b\mathrm i$，就是 $a+b\mathrm i=-a+b\mathrm i$，所以实部 $a=0$。

> 实矩阵 $Q$ 满足 $Q^{\mathsf T}Q=E$（正交矩阵，L.10.4），$Q\boldsymbol v=\lambda\boldsymbol v$，$\boldsymbol v\ne\boldsymbol0$。把 $\bar{\boldsymbol v}^{\mathsf T}Q^{\mathsf T}Q\boldsymbol v$ 算两遍，证明 $|\lambda|=1$。
>
> 答案：一方面它等于 $\bar{\boldsymbol v}^{\mathsf T}E\boldsymbol v=\bar{\boldsymbol v}^{\mathsf T}\boldsymbol v$；另一方面 $\bar{\boldsymbol v}^{\mathsf T}Q^{\mathsf T}=(Q\bar{\boldsymbol v})^{\mathsf T}=\bar\lambda\bar{\boldsymbol v}^{\mathsf T}$，它等于 $\bar\lambda\lambda\,\bar{\boldsymbol v}^{\mathsf T}\boldsymbol v=|\lambda|^2\bar{\boldsymbol v}^{\mathsf T}\boldsymbol v$。约去正数得 $|\lambda|^2=1$。

合上书，写出四步，指出第 3 步哪里用了 $A^{\mathsf T}=A$。

### 2. 对称矩阵的特征向量为什么互相垂直？

有了实的特征方向，再看它们之间的夹角。不对称的 $N=\begin{pmatrix}4&1\\2&3\end{pmatrix}$ 的特征值是 5 和 2，特征向量 $(1,1)^{\mathsf T}$、$(1,-2)^{\mathsf T}$ 的点积是 $-1$，两条特征方向斜交。① 属于 3 和 1 的特征向量 $(1,1)^{\mathsf T}$、$(1,-1)^{\mathsf T}$ 的点积是 0，互相垂直。差别来自一个点积恒等式。

点积可以写成矩阵乘法 $\boldsymbol a\cdot\boldsymbol b=\boldsymbol a^{\mathsf T}\boldsymbol b$（L.2.1），于是对任意方阵

$$(A\boldsymbol x)\cdot\boldsymbol y=(A\boldsymbol x)^{\mathsf T}\boldsymbol y=\boldsymbol x^{\mathsf T}A^{\mathsf T}\boldsymbol y=\boldsymbol x\cdot(A^{\mathsf T}\boldsymbol y).$$

第二个等号用了 $(A\boldsymbol x)^{\mathsf T}=\boldsymbol x^{\mathsf T}A^{\mathsf T}$，第三个把 $\boldsymbol x^{\mathsf T}(A^{\mathsf T}\boldsymbol y)$ 读回点积。记成一句话：**矩阵从点积的一边搬到另一边，要换成转置。**对称矩阵的转置就是自己，所以能自由搬家：$(A\boldsymbol x)\cdot\boldsymbol y=\boldsymbol x\cdot(A\boldsymbol y)$。

设 $A$ 对称，$A\boldsymbol x=\lambda_1\boldsymbol x$，$A\boldsymbol y=\lambda_2\boldsymbol y$，$\lambda_1\ne\lambda_2$。从 $(A\boldsymbol x)\cdot\boldsymbol y$ 出发，一边让 $A$ 作用在 $\boldsymbol x$ 上，一边先搬家再作用在 $\boldsymbol y$ 上：

$$\lambda_1(\boldsymbol x\cdot\boldsymbol y)=(A\boldsymbol x)\cdot\boldsymbol y=\boldsymbol x\cdot(A\boldsymbol y)=\lambda_2(\boldsymbol x\cdot\boldsymbol y).$$

移项得 $(\lambda_1-\lambda_2)(\boldsymbol x\cdot\boldsymbol y)=0$，而 $\lambda_1\ne\lambda_2$，只能 $\boldsymbol x\cdot\boldsymbol y=0$。

**定理**　实对称矩阵属于不同特征值的特征向量互相正交。

「不同特征值」不能少：$E$ 的特征值只有 1，$(1,0)^{\mathsf T}$ 和 $(1,1)^{\mathsf T}$ 都是它的特征向量，却不垂直。同一个特征值的特征向量怎样挑成垂直的，留给第 4 节。

它的直接用处：缺一个特征向量时靠「垂直」补出来。

**方法 2（用正交性补特征向量）**

全部特征值已知，缺的那个是单根；其余特征值的线性无关特征向量都已给出，个数等于它们的重数之和 $n-1$。这时：

1. 设所缺的特征向量为 $\boldsymbol x$；
2. 它和已知的每个特征向量都正交，逐个写出「点积为 0」，得到齐次方程组；
3. 解出的非零解就是所缺的特征向量。

**例 2**　三阶实对称矩阵 $A$ 的特征值为 2、3、6，属于 2、3 的特征向量分别是 $\boldsymbol v_1=(1,1,0)^{\mathsf T}$、$\boldsymbol v_2=(1,-1,1)^{\mathsf T}$。求属于 6 的全部特征向量。

6 和 2、3 都不同，所以属于 6 的特征向量 $\boldsymbol x$ 和 $\boldsymbol v_1$、$\boldsymbol v_2$ 都正交：

$$x_1+x_2=0,\qquad x_1-x_2+x_3=0.$$

由第一式 $x_2=-x_1$，代入第二式得 $x_3=-2x_1$，所以 $\boldsymbol x=x_1(1,-1,-2)^{\mathsf T}$。

6 是特征值，至少有一个特征向量，它只能在这条直线上，而特征向量的非零倍数仍是特征向量。所以属于 6 的全部特征向量是 $k(1,-1,-2)^{\mathsf T}$，$k\ne0$。

> 三阶实对称矩阵的特征值为 $-1$、0、2，属于 $-1$、0 的特征向量分别是 $(1,0,1)^{\mathsf T}$、$(0,1,0)^{\mathsf T}$。求属于 2 的全部特征向量。
>
> 答案：由 $x_1+x_3=0$、$x_2=0$ 得 $k(1,0,-1)^{\mathsf T}$，$k\ne0$。

合上书，推一遍搬家恒等式，再用它证明不同特征值的特征向量正交。

### 3. 对称矩阵为什么总能用正交矩阵对角化？

还剩两个问题：有重根时特征向量够不够 $n$ 个？能不能全挑成两两垂直的单位向量？答案都是能。两两垂直的单位向量排成的 $Q$ 是正交矩阵（L.10.4），只转动或翻面，$Q^{-1}=Q^{\mathsf T}$。

**谱定理**　对 $n$ 阶实对称矩阵 $A$，一定存在正交矩阵 $Q$，使

$$Q^{\mathsf T}AQ=Q^{-1}AQ=\Lambda=\operatorname{diag}(\lambda_1,\dots,\lambda_n),$$

$Q$ 的第 $i$ 列 $\boldsymbol q_i$ 是属于 $\lambda_i$ 的单位特征向量，$\Lambda$ 是把 $\lambda_i$ 按同样顺序排在对角线上的对角矩阵。这叫 $A$ 可以**正交对角化**。

写成 $A=Q\Lambda Q^{\mathsf T}$，从右往左读 $A\boldsymbol x$：$Q^{\mathsf T}\boldsymbol x=(\boldsymbol q_1\cdot\boldsymbol x,\dots,\boldsymbol q_n\cdot\boldsymbol x)^{\mathsf T}$ 是 $\boldsymbol x$ 在「特征方向这把尺子」上的坐标（L.10.3），$\Lambda$ 把第 $i$ 个坐标乘 $\lambda_i$，$Q$ 再用新坐标把各个 $\boldsymbol q_i$ 拼回去。$Q^{\mathsf T}$、$Q$ 都只转动或翻面，所以对称矩阵就是：**转过去，沿坐标轴伸缩，再转回来。**

#### 一次剥掉一个方向

证明的思路是一次剥掉一个方向。先在三阶好矩阵 ⑥ $A=\begin{pmatrix}2&1&0\\1&2&1\\0&1&2\end{pmatrix}$ 上走一遍。

第一步，找一个特征方向。$A(-1,0,1)^{\mathsf T}=(-2,0,2)^{\mathsf T}$，所以 2 是特征值，取 $\boldsymbol q_1=\frac1{\sqrt2}(-1,0,1)^{\mathsf T}$。

第二步，和 $\boldsymbol q_1$ 垂直的向量满足 $x_1=x_3$，组成平面 $W$，形如 $(a,b,a)^{\mathsf T}$。$A$ 把 $W$ 送回它自己：

$$A(a,b,a)^{\mathsf T}=(2a+b,\ 2a+2b,\ 2a+b)^{\mathsf T},$$

第一、三个分量仍相等（图 L13-n3）。由搬家恒等式，若 $\boldsymbol u\cdot\boldsymbol q_1=0$，则 $(A\boldsymbol u)\cdot\boldsymbol q_1=\boldsymbol u\cdot(A\boldsymbol q_1)=2(\boldsymbol u\cdot\boldsymbol q_1)=0$。

![⑥ 的特征方向 $\boldsymbol q_1$（实线）和与它垂直的平面 $W$（阴影）：$W$ 里的 $\boldsymbol u$ 被送到 $A\boldsymbol u$，仍在 $W$ 里，所以剥掉 $\boldsymbol q_1$ 以后，剩下的问题只在平面 $W$ 里](fig/L13-n3.pdf){width=58%}

第三步，在 $W$ 里重做同一个问题。取 $W$ 里互相垂直的单位向量 $\boldsymbol f_1=\frac1{\sqrt2}(1,0,1)^{\mathsf T}$、$\boldsymbol f_2=(0,1,0)^{\mathsf T}$ 当尺子，直接计算

$$A\boldsymbol f_1=\tfrac1{\sqrt2}(2,2,2)^{\mathsf T}=2\boldsymbol f_1+\sqrt2\,\boldsymbol f_2,\qquad A\boldsymbol f_2=(1,2,1)^{\mathsf T}=\sqrt2\,\boldsymbol f_1+2\boldsymbol f_2.$$

在 $W$ 里用 $\boldsymbol f_1,\boldsymbol f_2$ 读坐标，$A$ 的作用就是 $A_1=\begin{pmatrix}2&\sqrt2\\\sqrt2&2\end{pmatrix}$。它又对称，和 ① 同样子，特征方向是坐标 $(1,\pm1)$，特征值 $2\pm\sqrt2$；翻回三维是 $\boldsymbol f_1\pm\boldsymbol f_2=\frac1{\sqrt2}(1,\pm\sqrt2,1)^{\mathsf T}$，正是 ⑥ 另外两个特征方向。

一般情形照同样三步写：

1. 找一个方向。特征多项式在复数范围内有根（L.11.2），由第 1 节它是实数 $\lambda_1$，取单位实特征向量 $\boldsymbol q_1$。
2. 剥掉它。把 $\boldsymbol q_1$ 扩充成规范正交基（L.10.5），排成正交矩阵 $Q_1$。先看第一列：它是 $Q_1^{\mathsf T}AQ_1\boldsymbol e_1=Q_1^{\mathsf T}A\boldsymbol q_1=\lambda_1Q_1^{\mathsf T}\boldsymbol q_1$，而 $Q_1^{\mathsf T}\boldsymbol q_1$ 的分量是 $Q_1$ 各列与 $\boldsymbol q_1$ 的点积，只有第一个是 1，所以第一列是 $\lambda_1\boldsymbol e_1$。再看第一行：$(Q_1^{\mathsf T}AQ_1)^{\mathsf T}=Q_1^{\mathsf T}A^{\mathsf T}Q_1=Q_1^{\mathsf T}AQ_1$，矩阵对称，第一行等于第一列：
$$Q_1^{\mathsf T}AQ_1=\begin{pmatrix}\lambda_1&\boldsymbol0^{\mathsf T}\\\boldsymbol0&A_1\end{pmatrix},\qquad A_1\ \text{是}\ n-1\ \text{阶对称矩阵}.$$
3. 重复。设已有 $n-1$ 阶正交矩阵 $P_1$ 使 $P_1^{\mathsf T}A_1P_1$ 对角，令 $Q_2=\begin{pmatrix}1&\boldsymbol0^{\mathsf T}\\\boldsymbol0&P_1\end{pmatrix}$，分块相乘得 $(Q_1Q_2)^{\mathsf T}A(Q_1Q_2)=Q_2^{\mathsf T}(Q_1^{\mathsf T}AQ_1)Q_2=\begin{pmatrix}\lambda_1&\boldsymbol0^{\mathsf T}\\\boldsymbol0&P_1^{\mathsf T}A_1P_1\end{pmatrix}$，是对角矩阵；$Q=Q_1Q_2$ 正交，因为 $Q^{\mathsf T}Q=Q_2^{\mathsf T}Q_1^{\mathsf T}Q_1Q_2=E$。$P_1$ 由同样的办法对 $n-1$ 阶得到，一直退到一阶（一阶矩阵本来就是对角的）。

对称性用在第 2 步，让第一行跟着第一列变干净。

谱定理有三个推论：

1. 对称矩阵一定可对角化，所以每个特征值的几何重数都等于代数重数（L.12.2）。
2. 两个同阶对称矩阵的特征值（连同重数）相同，它们就相似。特征值按同样顺序排，有 $Q_1^{\mathsf T}AQ_1=\Lambda=Q_2^{\mathsf T}BQ_2$，由右式 $B=Q_2\Lambda Q_2^{\mathsf T}$，再代入左式：
$$B=Q_2Q_1^{\mathsf T}AQ_1Q_2^{\mathsf T}=R^{-1}AR,\qquad R=Q_1Q_2^{\mathsf T},\ R^{-1}=R^{\mathsf T}.$$
3. 能正交对角化的矩阵一定对称：$A=Q\Lambda Q^{\mathsf T}$ 时 $A^{\mathsf T}=Q\Lambda^{\mathsf T}Q^{\mathsf T}=A$。所以「对称」和「能正交对角化」是同一件事。

先想想它和 L.12 的对角化差在哪，再看下表。

| | 对角化（L.12） | 正交对角化（本章） |
|---|---|---|
| 对谁能做 | 有 $n$ 个线性无关特征向量的矩阵 | 恰好是对称矩阵 |
| 换基矩阵 | $P$，列是特征向量 | $Q$，列是两两垂直的单位特征向量 |
| 逆矩阵 | 要算 $P^{-1}$ | $Q^{-1}=Q^{\mathsf T}$ |
| 特征值相同时 | 不一定相似（② 与 $E$） | 都对称就一定相似 |

**方法 3（对称矩阵只比特征值）**

判断两个矩阵是否相似：

1. 先比特征值（连同重数），不同就不相似；
2. 两者都对称，特征值相同就相似；
3. 特征值相同、一个对称一个不对称时，查不对称的能否对角化：不能就不相似，能就相似。

**例 3**　判断 $A=\begin{pmatrix}1&1&0\\1&1&0\\0&0&2\end{pmatrix}$，$B=\begin{pmatrix}2&1&0\\0&2&0\\0&0&0\end{pmatrix}$，$C=\operatorname{diag}(2,2,0)$ 中哪两个相似。

$A$ 左上角二阶块的迹是 2、行列式是 0，特征值 2、0，再加右下角的 2，$A$ 的特征值是 2、2、0。$B$ 是上三角矩阵，特征值是对角元 2、2、0。三者特征值相同。

$A$、$C$ 都对称，所以相似。$B$ 不对称，查重根 2：$B-2E=\begin{pmatrix}0&1&0\\0&0&0\\0&0&-2\end{pmatrix}$ 的秩是 2，几何重数 $3-2=1<2$，$B$ 不能对角化，和 $C$、$A$ 都不相似。答案：只有 $A$ 与 $C$ 相似。

合上书，用 ⑥ 说一遍「剥掉一个方向」。

### 4. 正交对角化具体怎么做？

下面把 $Q$ 造出来，比 L.12.3 多了正交化和单位化。

**方法 4（正交对角化五步）**

1. 解 $|\lambda E-A|=0$，求全部特征值；
2. 对每个特征值，求 $(A-\lambda E)\boldsymbol x=\boldsymbol0$ 的基础解系；
3. 单根的向量已经和别的特征值的向量垂直，不用处理；重根的几个向量，在本特征空间内部做施密特正交化（L.10.5）；
4. 全部单位化；
5. 排成 $Q$，$\Lambda$ 按同样顺序填特征值，$Q^{\mathsf T}AQ=\Lambda$。

第 3 步为什么只在特征空间内部做？施密特正交化得到的是原向量的组合，同一个特征值的特征向量组合起来仍是这个特征值的特征向量；不同特征值的向量本来就垂直。

**例 4**　把 $A=\begin{pmatrix}0&1&1\\1&0&1\\1&1&0\end{pmatrix}$ 正交对角化。

第 1 步。$\lambda E-A$ 每行之和都是 $\lambda-2$：把后两列加到第一列，提出 $\lambda-2$，再用第一行消去下面两行的第一个元素（L.6.7）：

$$|\lambda E-A|=(\lambda-2)\begin{vmatrix}1&-1&-1\\1&\lambda&-1\\1&-1&\lambda\end{vmatrix}=(\lambda-2)\begin{vmatrix}1&-1&-1\\0&\lambda+1&0\\0&0&\lambda+1\end{vmatrix}=(\lambda-2)(\lambda+1)^2.$$

第 2 步。$\lambda=2$：方程是 $-2x_1+x_2+x_3=0$、$x_1-2x_2+x_3=0$、$x_1+x_2-2x_3=0$，前两式相减得 $x_1=x_2$，后两式相减得 $x_2=x_3$，解是 $(1,1,1)^{\mathsf T}$ 的倍数。$\lambda=-1$：$A+E$ 三行都是 $(1,1,1)$，方程只有

$$x_1+x_2+x_3=0,$$

基础解系取 $\boldsymbol\alpha_1=(1,-1,0)^{\mathsf T}$、$\boldsymbol\alpha_2=(1,0,-1)^{\mathsf T}$。这个特征空间是图 L13-n4 里的阴影平面，$(1,1,1)^{\mathsf T}$ 是它的法向量。

第 3 步。$\boldsymbol\alpha_1\cdot\boldsymbol\alpha_2=1\ne0$，要正交化。保留 $\boldsymbol\beta_1=\boldsymbol\alpha_1$，从 $\boldsymbol\alpha_2$ 里减去它在 $\boldsymbol\beta_1$ 上的投影：

$$\boldsymbol\beta_2=\boldsymbol\alpha_2-\frac{\boldsymbol\alpha_2\cdot\boldsymbol\beta_1}{\boldsymbol\beta_1\cdot\boldsymbol\beta_1}\boldsymbol\beta_1=(1,0,-1)^{\mathsf T}-\tfrac12(1,-1,0)^{\mathsf T}=\tfrac12(1,1,-2)^{\mathsf T}.$$

取 $\boldsymbol\beta_2=(1,1,-2)^{\mathsf T}$。它还属于 $-1$ 吗？代进 $x_1+x_2+x_3=0$：$1+1-2=0$，还在那个平面里。

![正对特征值 $-1$ 的特征空间（阴影平面）看，法向量 $(1,1,1)^{\mathsf T}$ 垂直于纸面；$\boldsymbol\alpha_2$ 减去它在 $\boldsymbol\alpha_1$ 上的投影（点线），得到平面内垂直于 $\boldsymbol\alpha_1$ 的 $\boldsymbol\beta_2$（虚线）](fig/L13-n4.pdf){width=58%}

第 4、5 步。三个向量的长度是 $\sqrt3$、$\sqrt2$、$\sqrt6$，单位化后排成

$$Q=\begin{pmatrix}\frac1{\sqrt3}&\frac1{\sqrt2}&\frac1{\sqrt6}\\\frac1{\sqrt3}&-\frac1{\sqrt2}&\frac1{\sqrt6}\\\frac1{\sqrt3}&0&-\frac2{\sqrt6}\end{pmatrix},\qquad Q^{\mathsf T}AQ=\operatorname{diag}(2,-1,-1).$$

验算：$A(1,1,-2)^{\mathsf T}=(-1,-1,2)^{\mathsf T}$。重根的向量不正交化、或忘了单位化，$Q$ 就不是正交矩阵。

> 把 $\begin{pmatrix}1&-2&2\\-2&4&-4\\2&-4&4\end{pmatrix}=\boldsymbol v\boldsymbol v^{\mathsf T}$（$\boldsymbol v=(1,-2,2)^{\mathsf T}$）正交对角化。
>
> 答案：$\boldsymbol v\boldsymbol v^{\mathsf T}\boldsymbol v=9\boldsymbol v$；秩为 1，0 是二重特征值，特征空间 $x_1-2x_2+2x_3=0$，取 $(2,1,0)^{\mathsf T}$、$(-2,0,1)^{\mathsf T}$ 再正交化。$Q$ 的三列依次为 $\frac13(1,-2,2)^{\mathsf T}$、$\frac1{\sqrt5}(2,1,0)^{\mathsf T}$、$\frac1{3\sqrt5}(-2,4,5)^{\mathsf T}$，$\Lambda=\operatorname{diag}(9,0,0)$。

下一道和例 4 不同：$A$ 没给出来，只知道特征值和一个特征向量。

**例 5**　三阶实对称矩阵 $A$ 的特征值为 1、1、4，属于 4 的特征向量为 $(1,-1,1)^{\mathsf T}$。求正交矩阵 $Q$，使 $Q^{\mathsf T}AQ$ 为对角矩阵。

先定出重根 1 的特征空间。属于 1 的特征向量都和 $(1,-1,1)^{\mathsf T}$ 垂直，都在平面 $x_1-x_2+x_3=0$ 上；由推论 1，这个特征空间是二维的。二维的空间装在一个平面里，只能是整个平面。

再在平面里直接挑两个垂直的向量：先取满足方程的 $\boldsymbol\beta_1=(1,0,-1)^{\mathsf T}$；第二个既在平面里、又垂直于 $\boldsymbol\beta_1$，解

$$x_1-x_2+x_3=0,\qquad x_1-x_3=0,$$

得 $\boldsymbol\beta_2=(1,2,1)^{\mathsf T}$。三个向量的长度分别是 $\sqrt3$、$\sqrt2$、$\sqrt6$，

$$Q=\begin{pmatrix}\frac1{\sqrt3}&\frac1{\sqrt2}&\frac1{\sqrt6}\\-\frac1{\sqrt3}&0&\frac2{\sqrt6}\\\frac1{\sqrt3}&-\frac1{\sqrt2}&\frac1{\sqrt6}\end{pmatrix},\qquad Q^{\mathsf T}AQ=\operatorname{diag}(4,1,1).$$

这道题学到的是：对称矩阵的重根特征空间，就是其余特征向量的正交补。

合上书，说出五步，再解释施密特正交化为什么不会把特征向量变成非特征向量。

### 5. 对称矩阵能拆成哪些简单矩阵的和？

把 $A=Q\Lambda Q^{\mathsf T}$ 乘开。右乘对角矩阵是把各列伸缩，$Q\Lambda=(\lambda_1\boldsymbol q_1,\dots,\lambda_n\boldsymbol q_n)$；再按「列乘行」展开成外积之和（L.3.7）：

$$A=\lambda_1\boldsymbol q_1\boldsymbol q_1^{\mathsf T}+\lambda_2\boldsymbol q_2\boldsymbol q_2^{\mathsf T}+\cdots+\lambda_n\boldsymbol q_n\boldsymbol q_n^{\mathsf T}.$$

这叫**谱分解**。每一项里的 $\boldsymbol q_i\boldsymbol q_i^{\mathsf T}$ 作用在 $\boldsymbol x$ 上，先算 $\boldsymbol q_i^{\mathsf T}\boldsymbol x$ 这个数：

$$\boldsymbol q_i\boldsymbol q_i^{\mathsf T}\boldsymbol x=(\boldsymbol q_i\cdot\boldsymbol x)\,\boldsymbol q_i,$$

正是 $\boldsymbol x$ 在单位向量 $\boldsymbol q_i$ 方向上的投影（L.2.3），所以 $\boldsymbol q_i\boldsymbol q_i^{\mathsf T}$ 是投影矩阵。在 ① 上，$\boldsymbol q_1\boldsymbol q_1^{\mathsf T}=\frac12\begin{pmatrix}1&1\\1&1\end{pmatrix}$ 就是老朋友投影 ④，于是

$$\begin{pmatrix}2&1\\1&2\end{pmatrix}=3\cdot\tfrac12\begin{pmatrix}1&1\\1&1\end{pmatrix}+1\cdot\tfrac12\begin{pmatrix}1&-1\\-1&1\end{pmatrix}.$$

谱分解作用在 $\boldsymbol x$ 上的读法是**拆、乘、加**：把 $\boldsymbol x$ 拆成沿各垂直方向的分量，每个分量乘自己的 $\lambda_i$，再加回去。取 $\boldsymbol x=(2,0)^{\mathsf T}$：沿 $\boldsymbol q_1$、$\boldsymbol q_2$ 的分量是 $(1,1)^{\mathsf T}$、$(1,-1)^{\mathsf T}$，乘 3 和 1 再相加得 $(4,2)^{\mathsf T}$，正是 ① 乘 $\boldsymbol x$。

![把 $\boldsymbol x=(2,0)^{\mathsf T}$ 拆成两个垂直分量，各乘特征值 3、1 再相加：$A\boldsymbol x=3(1,1)^{\mathsf T}+(1,-1)^{\mathsf T}=(4,2)^{\mathsf T}$](fig/L13-n2.pdf){width=58%}

各个投影加起来是 $E$：$\sum\boldsymbol q_i\boldsymbol q_i^{\mathsf T}=QQ^{\mathsf T}=E$，分量加回去就是 $\boldsymbol x$ 本身。两个投影相乘时，$(\boldsymbol q_i\boldsymbol q_i^{\mathsf T})(\boldsymbol q_j\boldsymbol q_j^{\mathsf T})=\boldsymbol q_i(\boldsymbol q_i^{\mathsf T}\boldsymbol q_j)\boldsymbol q_j^{\mathsf T}$，中间的数在 $i\ne j$ 时是 0、$i=j$ 时是 1。所以若 $A^k=\sum\lambda_i^k\boldsymbol q_i\boldsymbol q_i^{\mathsf T}$，再右乘 $A=\sum\lambda_j\boldsymbol q_j\boldsymbol q_j^{\mathsf T}$，交叉项全部消失，只剩 $\sum\lambda_i^{k+1}\boldsymbol q_i\boldsymbol q_i^{\mathsf T}$。$k=1$ 时就是谱分解本身，由归纳，

$$A^k=\lambda_1^k\boldsymbol q_1\boldsymbol q_1^{\mathsf T}+\cdots+\lambda_n^k\boldsymbol q_n\boldsymbol q_n^{\mathsf T}.$$

拆、乘、加照样适用，只是每个分量乘的是 $\lambda_i^k$。

**方法 5（谱分解反求 $A$）**

已知全部特征值和两两正交的特征向量 $\boldsymbol v_i$ 时：

1. 单位化：$\boldsymbol q_i\boldsymbol q_i^{\mathsf T}=\boldsymbol v_i\boldsymbol v_i^{\mathsf T}/\lVert\boldsymbol v_i\rVert^2$，$\lVert\boldsymbol v\rVert$ 是长度，即高中的 $|\boldsymbol v|$，双竖线和数的绝对值区分开；
2. 写出 $A=\sum\lambda_i\boldsymbol q_i\boldsymbol q_i^{\mathsf T}$，不用求 $P^{-1}$；
3. 只有两个不同的特征值 $\lambda$、$\mu$，$\mu$ 是单根、单位特征向量为 $\boldsymbol q$ 时，属于 $\lambda$ 的投影之和是 $E-\boldsymbol q\boldsymbol q^{\mathsf T}$，所以
$$A=\lambda E+(\mu-\lambda)\boldsymbol q\boldsymbol q^{\mathsf T}.$$

**例 6**　求例 5 中的矩阵 $A$。

用方法 5 第 3 步，$\boldsymbol q=\frac1{\sqrt3}(1,-1,1)^{\mathsf T}$，$\lambda=1$，$\mu=4$：

$$A=E+3\boldsymbol q\boldsymbol q^{\mathsf T}=E+\begin{pmatrix}1&-1&1\\-1&1&-1\\1&-1&1\end{pmatrix}=\begin{pmatrix}2&-1&1\\-1&2&-1\\1&-1&2\end{pmatrix}.$$

为什么属于 1 的两项之和是 $E-\boldsymbol q\boldsymbol q^{\mathsf T}$？三个投影之和是 $E$，减去属于 4 的那一项就是另外两项之和，和那两个向量怎么挑无关。

#### 数据最分散的方向

下面换个场景，看谱分解在数据分析里的用法。$m$ 个二维数据点 $\boldsymbol x_k$ 已经各自减去了平均值（中心化）。沿单位向量 $\boldsymbol u$ 看，点 $\boldsymbol x_k$ 的坐标是 $\boldsymbol u\cdot\boldsymbol x_k$，这些坐标的平均值是 0，所以按高中方差的定义，沿 $\boldsymbol u$ 的方差是 $\frac1m\sum(\boldsymbol u\cdot\boldsymbol x_k)^2$。

为了把 $\boldsymbol u$ 提出求和号，先用 $\boldsymbol u\cdot\boldsymbol x_k=\boldsymbol u^{\mathsf T}\boldsymbol x_k=\boldsymbol x_k^{\mathsf T}\boldsymbol u$（数的转置是自己）写出两个因子，再用矩阵乘法的结合律重新加括号：

$$(\boldsymbol u\cdot\boldsymbol x_k)^2=(\boldsymbol u^{\mathsf T}\boldsymbol x_k)(\boldsymbol x_k^{\mathsf T}\boldsymbol u)=\boldsymbol u^{\mathsf T}(\boldsymbol x_k\boldsymbol x_k^{\mathsf T})\boldsymbol u.$$

每一项左边都是 $\boldsymbol u^{\mathsf T}$、右边都是 $\boldsymbol u$，提到求和号外，于是

$$\text{沿 }\boldsymbol u\text{ 的方差}=\boldsymbol u^{\mathsf T}C\boldsymbol u,\qquad C=\frac1m\sum_{k=1}^m\boldsymbol x_k\boldsymbol x_k^{\mathsf T}.$$

$C$ 叫**协方差矩阵**（本章除以 $m$；统计里常除以 $m-1$，不影响方向），它是对称矩阵。

**例 7**　四个中心化的数据点 $(2,2)$、$(-2,-2)$、$(1,-1)$、$(-1,1)$。求协方差矩阵，说明数据沿哪个方向最分散。

前两个点的外积都是 $\begin{pmatrix}4&4\\4&4\end{pmatrix}$，后两个都是 $\begin{pmatrix}1&-1\\-1&1\end{pmatrix}$，相加除以 4 得 $C=\begin{pmatrix}2.5&1.5\\1.5&2.5\end{pmatrix}$，特征值 4、1，单位特征向量就是 ① 的 $\boldsymbol q_1$、$\boldsymbol q_2$。由谱分解，对单位向量 $\boldsymbol u$，

$$\boldsymbol u^{\mathsf T}C\boldsymbol u=4(\boldsymbol q_1\cdot\boldsymbol u)^2+1\cdot(\boldsymbol q_2\cdot\boldsymbol u)^2.$$

两个权重非负，和为 $\lVert\boldsymbol u\rVert^2=1$（$\boldsymbol u$ 在规范正交基下坐标的平方和，L.10.3），所以沿任何方向的方差都是 4 和 1 的加权平均：最大是 4，在 $\boldsymbol u=\boldsymbol q_1$ 时取到。

最大特征值的特征向量就是数据最分散的方向，叫第一主成分（M.5）。

合上书，由 $A=Q\Lambda Q^{\mathsf T}$ 推出谱分解，说明每一项为什么是投影，再推一遍 $A=\lambda E+(\mu-\lambda)\boldsymbol q\boldsymbol q^{\mathsf T}$。

### 本章小结

| 方法 | 什么时候用 | 对应题号 |
|---|---|---|
| 方法 1（把 $\bar{\boldsymbol v}^{\mathsf T}A\boldsymbol v$ 算两遍） | 由转置关系推特征值的性质 | L13-01、06、14 |
| 方法 2（用正交性补特征向量） | 补特征向量；重根特征空间是正交补 | L13-02、07、09、14 |
| 方法 3（对称矩阵只比特征值） | 判断相似 | L13-03、08 |
| 方法 4（正交对角化五步） | 求正交矩阵 $Q$ | L13-04、09 |
| 方法 5（谱分解反求 $A$） | 由特征信息写出 $A$、$A^k$ | L13-05、10–13、15–17 |

可逆大定理本章没有新增条目，表见 L.12 的小结。
