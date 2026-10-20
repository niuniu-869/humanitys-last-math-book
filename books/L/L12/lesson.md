## L.12 · 相似与对角化

一款 App 每月统计一次用户。本月活跃的用户，下月有 80% 仍然活跃、20% 变成沉默用户；沉默用户下月有 30% 被召回、70% 继续沉默。把活跃、沉默两类用户的占比写成向量 $\boldsymbol{x}_n$，下个月的占比就是

$$\boldsymbol{x}_{n+1}=M\boldsymbol{x}_n,\qquad M=\begin{pmatrix}0.8&0.3\\0.2&0.7\end{pmatrix}.$$

想知道一年后、几年后的占比，就要算 $M^{12}\boldsymbol{x}_0$、$M^{100}\boldsymbol{x}_0$。矩阵自乘一百次很费事，对角矩阵的一百次方却只要把对角线上的数各自一百次方。本章的办法就是换一把尺子来量这个变换，让它的矩阵变成对角矩阵。

一个很早的例子是斐波那契数列 $1,1,2,3,5,8,\dots$：每一项是前两项之和，按递推要第 100 项得一项项加下去。直接用 $n$ 写出第 $n$ 项的公式以比内的名字流传（他在 1843 年发表），公式里竟然有 $\sqrt5$：一个整数数列的通项，为什么会冒出无理数？第 6 节会看到，$\sqrt5$ 来自一个二阶矩阵的特征值，这个公式正是把那个矩阵对角化的结果。

第 1 节看换一把尺子以后矩阵怎样变，引出相似；第 2 节问什么样的矩阵能换成对角矩阵；第 3 节给出对角化的步骤；第 4 节用它算 $A^n$；第 5 节处理不能或不必对角化的情形；第 6 节推出斐波那契通项；第 7 节回到 App 求长期占比。

### 1. 同一个变换换一组基来看，矩阵怎样变？

先拿老朋友①对称伸缩来试。记

$$S=\begin{pmatrix}2&1\\1&2\end{pmatrix}.$$

L.11 已经找到它的两个特征方向：$\boldsymbol{p}_1=(1,1)^{\mathsf T}$ 被拉长 3 倍，$\boldsymbol{p}_2=(-1,1)^{\mathsf T}$ 原样不动（特征值 1）。可是在标准坐标下，

$$S\boldsymbol{x}=\begin{pmatrix}2x_1+x_2\\x_1+2x_2\end{pmatrix},$$

新的每个分量都要用到旧的两个分量，两个坐标搅在一起。图 L12-n3 的左幅就是这个样子：单位正方形被拧成一个斜放的平行四边形。

现在换一把尺子。用 $\boldsymbol{p}_1,\boldsymbol{p}_2$ 作基（L.8.3），把向量写成 $\boldsymbol{x}=y_1\boldsymbol{p}_1+y_2\boldsymbol{p}_2$，$(y_1,y_2)^{\mathsf T}$ 就是 $\boldsymbol{x}$ 在新尺子下的坐标。因为线性变换保持加法和数乘，

$$S\boldsymbol{x}=y_1S\boldsymbol{p}_1+y_2S\boldsymbol{p}_2=3y_1\boldsymbol{p}_1+y_2\boldsymbol{p}_2.$$

所以用新尺子量，$S$ 把坐标 $(y_1,y_2)$ 变成 $(3y_1,y_2)$：第一个坐标放大 3 倍，第二个不变，两者互不干扰。这个变换在新尺子下的矩阵是对角矩阵 $\operatorname{diag}(3,1)$。记号 $\operatorname{diag}(d_1,\dots,d_n)$ 表示对角线上依次是 $d_1,\dots,d_n$、其余元素都是 0 的矩阵。

图 L12-n3 的右幅核对了一个点：$\boldsymbol{x}=(2,0)^{\mathsf T}=\boldsymbol{p}_1-\boldsymbol{p}_2$，新坐标 $(1,-1)$；$S\boldsymbol{x}=(4,2)^{\mathsf T}=3\boldsymbol{p}_1-\boldsymbol{p}_2$，新坐标 $(3,-1)$。

![同一个变换 $S$ 用两把尺子量：标准网格里正方形被拧斜，矩阵有非零的非对角元；沿 $\boldsymbol{p}_1,\boldsymbol{p}_2$ 的斜网格里格子只沿 $\boldsymbol{p}_1$ 拉长 3 倍，所以矩阵是 $\operatorname{diag}(3,1)$](fig/L12-n3.pdf){width=85%}

一般地，取一个可逆矩阵 $P$，用它的各列作新尺子。按 L.8.3，旧坐标 $\boldsymbol{x}$ 与新坐标 $\boldsymbol{y}$ 的关系是

$$\boldsymbol{x}=P\boldsymbol{y},\qquad \boldsymbol{y}=P^{-1}\boldsymbol{x}.$$

变换的结果 $A\boldsymbol{x}=AP\boldsymbol{y}$ 是用旧尺子写的，再左乘 $P^{-1}$ 换成新尺子的坐标，得到 $P^{-1}AP\boldsymbol{y}$。所以同一个变换在新尺子下的矩阵是

$$B=P^{-1}AP.$$

这个式子从右往左读：$P$ 把新坐标翻译成旧坐标，$A$ 用旧坐标做变换，$P^{-1}$ 再把结果翻译回新坐标。

本章反复用「两把尺子」来说这件事：$A$ 是用标准尺子记下的变换，$B$ 是用 $P$ 的列这把尺子记下的同一个变换，$P$ 负责翻译。这个说法不保证新矩阵更简单：$P$ 的列不是特征向量时，新尺子下的矩阵照样可以很乱，例 1 就是这样。

设 $A,B$ 都是 $n$ 阶方阵。如果存在可逆矩阵 $P$ 使 $P^{-1}AP=B$，就说 $A$ 与 $B$ **相似**，记作 $A\sim B$。取 $P=E$ 知 $A\sim A$；由 $A=(P^{-1})^{-1}BP^{-1}$ 知 $B\sim A$；若再有 $Q^{-1}BQ=C$，则 $(PQ)^{-1}A(PQ)=C$，相似可以传递。

#### 换尺子时什么不变？

既然是同一个变换，凡是只取决于变换本身、不取决于尺子的量，两个矩阵就应当相同。最重要的是特征多项式。证明的思路是把 $\lambda E$ 也写成「$P^{-1}(\cdots)P$」的样子，再把 $P^{-1}$ 和 $P$ 提到外面：

$$|\lambda E-B|=|P^{-1}(\lambda E)P-P^{-1}AP|=|P^{-1}(\lambda E-A)P|=|P^{-1}|\,|\lambda E-A|\,|P|=|\lambda E-A|.$$

第一个等号用了 $P^{-1}(\lambda E)P=\lambda E$；第二个是分配律，把左右两边的 $P^{-1}$、$P$ 提出来；第三个是乘积公式 $|XY|=|X|\,|Y|$（L.6.4）；最后一个是 $|P^{-1}|\,|P|=|P^{-1}P|=|E|=1$。

特征多项式相同，特征值连同重数都相同，于是特征值之和（迹）与特征值之积（行列式）也相同（L.11.3）。秩也不变，因为乘可逆矩阵不改变秩（L.7.7）。

特征向量却会变。若 $A\boldsymbol{v}=\lambda\boldsymbol{v}$，则

$$B(P^{-1}\boldsymbol{v})=P^{-1}AP\,P^{-1}\boldsymbol{v}=P^{-1}A\boldsymbol{v}=\lambda P^{-1}\boldsymbol{v},$$

所以 $B$ 的特征向量是 $P^{-1}\boldsymbol{v}$。按两把尺子的说法这很自然：箭头还是那支箭头，$P^{-1}\boldsymbol{v}$ 只是它在新尺子下的坐标。

**方法 1（相似不变量）**

1. $A\sim B$ 时，两者的特征多项式、特征值、迹、行列式、秩都相等，可以用来列方程求参数；
2. 判断两个矩阵是否相似时，只要有一项不等，就一定不相似。

**例 1**　$A=\begin{pmatrix}4&1\\2&3\end{pmatrix}$，$P=\begin{pmatrix}1&1\\0&1\end{pmatrix}$。求 $B=P^{-1}AP$，核对不变量，并求 $B$ 属于特征值 5 的特征向量。

这里的 $P$ 正是老朋友②剪切。思路是先算 $AP$，再左乘 $P^{-1}$；特征向量则把 $A$ 的特征向量翻译成新坐标。

由二阶求逆公式（L.5.1），

$$P^{-1}=\begin{pmatrix}1&-1\\0&1\end{pmatrix}.$$

左乘 $P^{-1}$ 的效果是用第一行减去第二行，所以

$$AP=\begin{pmatrix}4&5\\2&5\end{pmatrix},\qquad B=P^{-1}(AP)=\begin{pmatrix}2&0\\2&5\end{pmatrix}.$$

$B$ 是下三角矩阵，特征值就是对角元 2 和 5。$A$ 的特征多项式 $\lambda^2-7\lambda+10=(\lambda-2)(\lambda-5)$，特征值也是 2 和 5。迹和行列式也对得上：$\operatorname{tr}B=7=\operatorname{tr}A$，$|B|=10=|A|$。

$A$ 属于 5 的特征向量可以取 $\boldsymbol{p}_1=(1,1)^{\mathsf T}$，把它翻译成新坐标再验算：

$$P^{-1}\boldsymbol{p}_1=\begin{pmatrix}0\\1\end{pmatrix},\qquad B\begin{pmatrix}0\\1\end{pmatrix}=\begin{pmatrix}0\\5\end{pmatrix}=5\begin{pmatrix}0\\1\end{pmatrix}.$$

> 同一个 $A$，改取 $P=\begin{pmatrix}1&0\\1&1\end{pmatrix}$，求 $P^{-1}AP$ 并核对迹和行列式。
>
> 答案：$P^{-1}=\begin{pmatrix}1&0\\-1&1\end{pmatrix}$，$P^{-1}AP=\begin{pmatrix}5&1\\0&2\end{pmatrix}$，迹 7、行列式 10。

不变量全都相等，能不能断定相似？不能。单位矩阵 $E$ 和剪切 $J=\begin{pmatrix}1&1\\0&1\end{pmatrix}$ 的特征多项式都是 $(\lambda-1)^2$，迹、行列式、秩也都相同。可是对任何可逆 $P$ 都有 $P^{-1}EP=P^{-1}P=E$：「什么都不做」的变换，换哪把尺子写出来都是 $E$。所以和 $E$ 相似的只有 $E$ 自己，而 $J\ne E$。

不变量对不上，一定不相似；全对上了，也可能不相似。缺的信息是特征向量够不够多，这是下一节的问题。

合上书，从 $\boldsymbol{x}=P\boldsymbol{y}$ 出发推出新尺子下的矩阵是 $P^{-1}AP$，再推一遍相似矩阵的特征多项式为什么相同。

### 2. 什么样的矩阵能换成对角矩阵？

第 1 节里，$S$ 用特征向量作尺子就成了对角矩阵。本节问：哪些矩阵有这样一把尺子？分五小步：需要什么，拿老朋友试，有重根时最多凑出几个，几何重数为什么不超过代数重数，合成判据。

#### 对角化需要 $n$ 个线性无关的特征向量

设 $P^{-1}AP=\Lambda=\operatorname{diag}(\lambda_1,\dots,\lambda_n)$（$\Lambda$ 是 $\lambda$ 的大写）。两边左乘 $P$ 得

$$AP=P\Lambda.$$

逐列比较这个等式。左边第 $j$ 列是 $A\boldsymbol{p}_j$；右边第 $j$ 列是 $P$ 乘 $\Lambda$ 的第 $j$ 列 $\lambda_j\boldsymbol{e}_j$，等于 $\lambda_j\boldsymbol{p}_j$。所以

$$A\boldsymbol{p}_j=\lambda_j\boldsymbol{p}_j,\qquad j=1,\dots,n.$$

可逆矩阵没有零列，$\boldsymbol{p}_j\ne\boldsymbol{0}$，所以 $\boldsymbol{p}_j$ 是属于 $\lambda_j$ 的特征向量；$P$ 可逆，这 $n$ 个特征向量线性无关。

倒过来，有 $n$ 个线性无关的特征向量时，把它们排成 $P$，$P$ 可逆（L.7 的可逆大定理），同样逐列计算给出 $AP=P\Lambda$，即 $P^{-1}AP=\Lambda$。

与对角矩阵相似的矩阵叫作**可对角化**的。刚才证明了：**$n$ 阶矩阵 $A$ 可对角化，当且仅当 $A$ 有 $n$ 个线性无关的特征向量。**

#### 拿老朋友试一试

④投影 $H=\frac12\begin{pmatrix}1&1\\1&1\end{pmatrix}$ 的特征值是 1 和 0，特征向量恰好也是 $(1,1)^{\mathsf T}$ 和 $(-1,1)^{\mathsf T}$：直线 $y=x$ 上的向量不动，垂直于它的方向被压到原点。用和 $S$ 同一把尺子 $P=\begin{pmatrix}1&-1\\1&1\end{pmatrix}$，得 $P^{-1}HP=\operatorname{diag}(1,0)$：保留第一个坐标，扔掉第二个坐标，正是垂直地压到直线 $y=x$ 上。

②剪切 $J=\begin{pmatrix}1&1\\0&1\end{pmatrix}$ 就不行了。特征值 1 是二重根，而 $(J-E)\boldsymbol{x}=\boldsymbol{0}$ 只有一个方程 $x_2=0$，特征向量都是 $(1,0)^{\mathsf T}$ 的倍数。图 L12-n4 画出了原因：剪切把每个点水平推动，推的距离等于它的高度，所以只有水平的箭头不转向，其他箭头都被推歪了。

![剪切 $J$ 把每个点水平推动，推的距离等于它的高度：只有水平的箭头方向不变，其他箭头（虚线）的像（实线）都向右歪，所以特征方向只有一条](fig/L12-n4.pdf){width=60%}

找不到第二个特征方向，就凑不出一把由特征向量组成的尺子，$J$ 不能对角化。这也回答了第 1 节的问题：$J$ 若能对角化，只能相似于 $\operatorname{diag}(1,1)=E$，而和 $E$ 相似的只有 $E$。

③转 90° 矩阵 $T=\begin{pmatrix}0&-1\\1&0\end{pmatrix}$ 的毛病不一样。它的特征多项式是 $\lambda^2+1$，没有实根，特征值是 $\pm\mathrm{i}$。设实向量 $\boldsymbol{v}\ne\boldsymbol{0}$ 满足 $T\boldsymbol{v}=\lambda\boldsymbol{v}$。左边是实矩阵乘实向量，每个分量都是实数；右边 $\lambda=\pm\mathrm{i}$，$\boldsymbol{v}$ 的非零分量乘上 $\pm\mathrm{i}$ 是纯虚数，不可能等于实数。所以它没有实的特征向量，用实矩阵 $P$ 不能把它对角化。本章只讨论特征值都是实数的矩阵。

也有好消息。由 L.11.5，属于不同特征值的特征向量线性无关，所以 $n$ 个特征值互不相同时，每个特征值各取一个特征向量，就凑够了 $n$ 个，一定可对角化。麻烦只出在重根上。

#### 有重根时，最多能凑出几个？

设 $A$ 的互不相同的特征值是 $\lambda_1,\dots,\lambda_s$。$\lambda_i$ 作为特征多项式的根的重数叫**代数重数**，记作 $a_i$；特征空间的维数 $g_i=n-r(A-\lambda_iE)$ 叫**几何重数**（L.11.6）。

第一件事：从每个特征空间各取一组基，合起来共 $g_1+\cdots+g_s$ 个向量，它们仍然线性无关。

设它们的某个线性组合等于 $\boldsymbol{0}$。把属于同一个特征值的项归成一组，组的和记作 $\boldsymbol{w}_i$，得 $\boldsymbol{w}_1+\cdots+\boldsymbol{w}_s=\boldsymbol{0}$。每个 $\boldsymbol{w}_i$ 要么是 $\boldsymbol{0}$，要么是属于 $\lambda_i$ 的特征向量。

如果恰有一个 $\boldsymbol{w}_i$ 不为零，等式说它等于零，与它不为零矛盾；如果有几个不为零，就是几个属于不同特征值的特征向量加起来等于零，与 L.11.5 矛盾。所以每个 $\boldsymbol{w}_i=\boldsymbol{0}$。

$\boldsymbol{w}_i=\boldsymbol{0}$ 是第 $i$ 组基的组合，基线性无关，系数只能全为 0。

第二件事：从第 $i$ 个特征空间里最多取出 $g_i$ 个线性无关的向量，这是维数的定义。所以最多能凑出 $g_1+\cdots+g_s$ 个线性无关的特征向量。剩下的问题是 $g_i$ 和 $a_i$ 谁大。

#### 几何重数为什么不超过代数重数？

这一小节单独证明上一小节留下的问题。思路：拿特征向量当新尺子的前几根刻度，新矩阵的左上角就会出现 $\lambda_0E$，特征多项式里就跑出因子 $(\lambda-\lambda_0)^g$。

先在投影 $H$ 上走一遍。取 $\lambda_0=1$ 的特征向量 $\boldsymbol{v}_1=(1,1)^{\mathsf T}$，随便补一个不共线的 $\boldsymbol{v}_2=(0,1)^{\mathsf T}$，令 $P=(\boldsymbol{v}_1,\boldsymbol{v}_2)$。新矩阵的第一列是 $P^{-1}H\boldsymbol{v}_1=P^{-1}\boldsymbol{v}_1=\boldsymbol{e}_1$（因为 $P\boldsymbol{e}_1=\boldsymbol{v}_1$）；算出来 $P^{-1}HP=\begin{pmatrix}1&\frac12\\0&0\end{pmatrix}$，特征多项式 $(\lambda-1)\lambda$ 里的因子 $\lambda-1$ 正来自左上角的 1。

一般情形分四步，考试可能要求写出来。设 $\lambda_0$ 的几何重数是 $g$。

第一步，补成一把尺子。取特征空间的一组基 $\boldsymbol{v}_1,\dots,\boldsymbol{v}_g$，扩充成 $\mathbb{R}^n$ 的基 $\boldsymbol{v}_1,\dots,\boldsymbol{v}_n$（L.8.2），令 $P=(\boldsymbol{v}_1,\dots,\boldsymbol{v}_n)$，$P$ 可逆。

第二步，看新矩阵的前 $g$ 列。由 $P\boldsymbol{e}_i=\boldsymbol{v}_i$ 知 $P^{-1}\boldsymbol{v}_i=\boldsymbol{e}_i$。$i\le g$ 时 $A\boldsymbol{v}_i=\lambda_0\boldsymbol{v}_i$，所以 $P^{-1}AP$ 的第 $i$ 列是 $P^{-1}A\boldsymbol{v}_i=\lambda_0\boldsymbol{e}_i$。于是 $P^{-1}AP$ 是分块上三角的：

$$P^{-1}AP=\begin{pmatrix}\lambda_0E_g&C\\O&D\end{pmatrix},$$

其中 $E_g$ 是 $g$ 阶单位矩阵，$C$、$D$ 是我们不关心的块。

第三步，算它的特征多项式。用 $\lambda E$ 去减它，左上块变成 $(\lambda-\lambda_0)E_g$，右上块变成 $-C$，左下仍是零块：

$$\lambda E-P^{-1}AP=\begin{pmatrix}(\lambda-\lambda_0)E_g&-C\\O&\lambda E-D\end{pmatrix}.$$

分块上三角矩阵的行列式等于两个对角块行列式之积（L.6.3），而 $|(\lambda-\lambda_0)E_g|=(\lambda-\lambda_0)^g$，所以

$$|\lambda E-P^{-1}AP|=(\lambda-\lambda_0)^g\,|\lambda E-D|.$$

第四步，换回 $A$。相似矩阵的特征多项式相同（第 1 节），所以 $|\lambda E-A|$ 也含因子 $(\lambda-\lambda_0)^g$，$\lambda_0$ 的代数重数至少是 $g$。

不等号可以是严格的：剪切 $J$ 的特征值 1，代数重数 2，几何重数 1。

#### 可对角化的充要条件

把两件事接起来。最多能凑出 $g_1+\cdots+g_s$ 个，而

$$g_1+\cdots+g_s\le a_1+\cdots+a_s=n,$$

最后的等号是因为特征多项式是 $n$ 次的，特征值都是实数时，它们的代数重数加起来正好是 $n$。要凑够 $n$ 个，不等号必须取等号；而每一项都有 $g_i\le a_i$，所以必须每一项都相等。这就是**可对角化的充要条件**：每个特征值的几何重数等于代数重数。

可以这样记。代数重数是特征多项式给 $\lambda_i$ 留的名额，几何重数是实际到场的独立特征方向。到场的不会超过名额，名额一共 $n$ 个，所以只有每个特征值的名额都坐满，才凑得齐 $n$ 个方向。单根只有 1 个名额，而每个特征值至少有一个特征向量，所以单根自动坐满，只需检查重根。这个说法到「人数」为止：一个特征空间里有无穷多个特征向量，「到场人数」指的是特征空间的维数。

**方法 2（只查重根）**

1. 求出全部特征值，标出重数；
2. 单根不用查；对每个 $k$ 重根 $\lambda$，算 $r(A-\lambda E)$；
3. 所有重根都满足 $n-r(A-\lambda E)=k$，就可对角化；有一个不满足，就不能。

**例 2**　判断下面两个矩阵能否对角化：

$$A=\begin{pmatrix}2&0&1\\0&1&0\\1&0&2\end{pmatrix},\qquad B=\begin{pmatrix}2&0&1\\1&1&0\\1&0&2\end{pmatrix}.$$

动笔前先比一比：两者只差一个元素。下面会看到它们的特征多项式、迹、行列式全都一样，差别出在哪里？

先求特征值。两个矩阵的第二列都是 $(0,1,0)^{\mathsf T}$，所以 $\lambda E-A$、$\lambda E-B$ 的第二列只有一个非零元 $\lambda-1$。按第二列展开，划掉第二行、第二列后剩下的二阶行列式两者相同：

$$|\lambda E-A|=|\lambda E-B|=(\lambda-1)\big[(\lambda-2)^2-1\big]=(\lambda-1)^2(\lambda-3).$$

特征值是 1（二重）和 3。3 是单根，不用查；只需查 $\lambda=1$：

$$A-E=\begin{pmatrix}1&0&1\\0&0&0\\1&0&1\end{pmatrix},\qquad B-E=\begin{pmatrix}1&0&1\\1&0&0\\1&0&1\end{pmatrix}.$$

$A-E$ 只有一种非零行 $(1,0,1)$，秩 1，几何重数 $3-1=2$，名额坐满，$A$ 可对角化。

$B-E$ 的前两行不成比例，第三行等于第一行，秩 2，几何重数 $3-2=1<2$，$B$ 不能对角化。

所以 $A$ 与 $\operatorname{diag}(1,1,3)$ 相似，$B$ 不相似，$A$ 与 $B$ 也就不相似。差别出在特征空间的维数上，这是第 1 节那几个不变量看不到的。

> 判断 $C=\begin{pmatrix}3&0&0\\1&2&0\\1&0&2\end{pmatrix}$ 能否对角化。
>
> 答案：$C$ 是下三角矩阵，特征值 3、2、2；$C-2E$ 的三行都是 $(1,0,0)$，秩 1，几何重数 $3-1=2$ 等于代数重数，所以能对角化。

合上书，写出「几何重数 ≤ 代数重数」的四步，再说明为什么只需检查重根。

### 3. 具体怎样对角化，又怎样由特征值和特征向量反求 A？

例 2 的 $A$ 能对角化，$P$ 和 $\Lambda$ 具体是什么？第 2 节的证明已经给出了做法：把 $n$ 个线性无关的特征向量排成 $P$。

**方法 3（对角化四步）**

1. 解 $|\lambda E-A|=0$，求出全部特征值；
2. 对每个特征值 $\lambda_i$ 解 $(A-\lambda_iE)\boldsymbol{x}=\boldsymbol{0}$，取一个基础解系（L.9）；
3. 用方法 2 检查一共有没有 $n$ 个，不够就停，$A$ 不能对角化；
4. 把这些向量作为列排成 $P$，$\Lambda$ 的对角元按同样的顺序填上对应的特征值，则 $P^{-1}AP=\Lambda$。

验算不必求 $P^{-1}$，核对 $AP=P\Lambda$，即逐列核对 $A\boldsymbol{p}_j=\lambda_j\boldsymbol{p}_j$。

**例 3**　把例 2 的 $A$ 对角化。

第 1 步已在例 2 完成，特征值 1、1、3。

第 2 步，先做 $\lambda=1$。$A-E$ 化简后只剩一个方程 $x_1+x_3=0$，$x_2,x_3$ 自由。取 $(x_2,x_3)=(1,0)$ 和 $(0,1)$，得

$$\boldsymbol{p}_1=(0,1,0)^{\mathsf T},\qquad \boldsymbol{p}_2=(-1,0,1)^{\mathsf T}.$$

再做 $\lambda=3$。系数矩阵是

$$A-3E=\begin{pmatrix}-1&0&1\\0&-2&0\\1&0&-1\end{pmatrix},$$

第二行给出 $x_2=0$，第一行给出 $x_1=x_3$，取 $\boldsymbol{p}_3=(1,0,1)^{\mathsf T}$。

第 3 步，一共 3 个，够了。第 4 步把它们排成

$$P=\begin{pmatrix}0&-1&1\\1&0&0\\0&1&1\end{pmatrix},\qquad \Lambda=\operatorname{diag}(1,1,3),\qquad P^{-1}AP=\Lambda.$$

验算：$A\boldsymbol{p}_1=\boldsymbol{p}_1$ 一眼可见；$A\boldsymbol{p}_2=(-2+1,\ 0,\ -1+2)^{\mathsf T}=\boldsymbol{p}_2$；$A\boldsymbol{p}_3=(3,0,3)^{\mathsf T}=3\boldsymbol{p}_3$。

$P$ 不唯一。列可以换顺序（$\Lambda$ 跟着换），可以乘非零数，属于 1 的两列可以换成该特征空间的任何一组基。不能变的只有一条：第 $j$ 列必须和 $\Lambda$ 的第 $j$ 个对角元对应。

> 把例 2 后小题里的 $C$ 对角化。
>
> 答案：$\lambda=2$ 时只有方程 $x_1=0$，取 $(0,1,0)^{\mathsf T}$、$(0,0,1)^{\mathsf T}$；$\lambda=3$ 时取 $(1,1,1)^{\mathsf T}$。$P=\begin{pmatrix}0&0&1\\1&0&1\\0&1&1\end{pmatrix}$，$\Lambda=\operatorname{diag}(2,2,3)$。

**例 4**　$A=\begin{pmatrix}a&0&0\\1&2&0\\0&1&3\end{pmatrix}$，$a$ 取何值时 $A$ 可对角化？

和例 2 不同，这里参数决定了哪个特征值是重根，所以要分情况。$A$ 是下三角矩阵，特征值是 $a,2,3$。

$a\ne2$ 且 $a\ne3$ 时，三个特征值互不相同，可对角化。

$a=2$ 时，2 是二重根，

$$A-2E=\begin{pmatrix}0&0&0\\1&0&0\\0&1&1\end{pmatrix},$$

后两行不成比例，秩 2，几何重数 $3-2=1<2$，不能对角化。

$a=3$ 时，3 是二重根，$A-3E$ 的后两行 $(1,-1,0)$、$(0,1,0)$ 不成比例，秩 2，同样不能。

所以 $A$ 可对角化当且仅当 $a\ne2$ 且 $a\ne3$。$a=2$ 时不用查单根 $\lambda=3$。

**例 5**　$A=\begin{pmatrix}2&0&0\\0&3&2\\0&1&x\end{pmatrix}$ 与 $\Lambda=\operatorname{diag}(2,1,y)$ 相似，求 $x,y$。

两个未知数，就用方法 1 的两个不变量列两个方程。迹相等：$2+3+x=2+1+y$。行列式相等：按第一行展开 $|A|=2(3x-2)$，而 $|\Lambda|=2y$，所以 $y=3x-2$。代入第一式，$5+x=3x+1$，解得 $x=2$，$y=4$。

还要回头验证。迹和行列式相等只是相似的必要条件：如果求出的 $A$ 有重根而特征向量又不够，它就不与任何对角矩阵相似，题目也就无解。$x=2$ 时

$$|\lambda E-A|=(\lambda-2)(\lambda^2-5\lambda+4)=(\lambda-2)(\lambda-1)(\lambda-4),$$

特征值 2、1、4 互不相同，$A$ 确实与 $\operatorname{diag}(2,1,4)$ 相似。

反过来，知道全部特征值和特征向量，也能写出 $A$：由 $P^{-1}AP=\Lambda$，两边左乘 $P$、右乘 $P^{-1}$，得 $A=P\Lambda P^{-1}$。

**例 6**　二阶矩阵 $A$ 的特征值为 1、$-2$，对应的特征向量为 $(1,1)^{\mathsf T}$、$(1,2)^{\mathsf T}$，求 $A$。

把特征向量排成 $P$，$|P|=1$，由二阶求逆公式，

$$P=\begin{pmatrix}1&1\\1&2\end{pmatrix},\qquad P^{-1}=\begin{pmatrix}2&-1\\-1&1\end{pmatrix}.$$

$P\Lambda$ 就是把 $P$ 的两列分别乘 1 和 $-2$，再右乘 $P^{-1}$：

$$A=(P\Lambda)P^{-1}=\begin{pmatrix}1&-2\\1&-4\end{pmatrix}\begin{pmatrix}2&-1\\-1&1\end{pmatrix}=\begin{pmatrix}4&-3\\6&-5\end{pmatrix}.$$

验算：$A(1,2)^{\mathsf T}=(4-6,\ 6-10)^{\mathsf T}=-2(1,2)^{\mathsf T}$。

合上书，说明 $P$ 的第 $j$ 列和 $\Lambda$ 的第 $j$ 个对角元为什么必须对应，再说明用不变量求出参数后为什么还要验证。

### 4. $A^{100}$ 怎么算？

拿例 1 的 $A=\begin{pmatrix}4&1\\2&3\end{pmatrix}$ 来说，它的特征值是 5 和 2，特征向量可以取 $\boldsymbol{p}_1=(1,1)^{\mathsf T}$、$\boldsymbol{p}_2=(1,-2)^{\mathsf T}$。可是 $A=P\Lambda P^{-1}$，平方时中间的 $P^{-1}P$ 相消：

$$A^2=P\Lambda P^{-1}P\Lambda P^{-1}=P\Lambda^2P^{-1}.$$

每多乘一个 $A$，就多消掉一对 $P^{-1}P$，所以

$$A^n=P\Lambda^nP^{-1},\qquad \Lambda^n=\operatorname{diag}(\lambda_1^n,\dots,\lambda_n^n),$$

后一式是因为对角矩阵相乘就是对角元相乘。按两把尺子的说法：翻译一次，在新尺子里伸缩 $n$ 次，再翻译回去一次。

**例 7**　求 $A=\begin{pmatrix}4&1\\2&3\end{pmatrix}$ 的 $A^n$。

第一步，写出 $P$、$P^{-1}$ 和 $\Lambda^n$。$|P|=-3$，

$$P=\begin{pmatrix}1&1\\1&-2\end{pmatrix},\qquad P^{-1}=\frac13\begin{pmatrix}2&1\\1&-1\end{pmatrix},\qquad \Lambda^n=\operatorname{diag}(5^n,2^n).$$

第二步，先算 $P\Lambda^n$：两列分别乘 $5^n$、$2^n$。再右乘 $P^{-1}$：

$$A^n=\frac13\begin{pmatrix}5^n&2^n\\5^n&-2\cdot2^n\end{pmatrix}\begin{pmatrix}2&1\\1&-1\end{pmatrix}=\frac13\begin{pmatrix}2\cdot5^n+2^n&5^n-2^n\\2\cdot5^n-2^{n+1}&5^n+2^{n+1}\end{pmatrix}.$$

第三步，验算。代 $n=1$ 得 $\frac13\begin{pmatrix}12&3\\6&9\end{pmatrix}=A$。

> 用例 6 求出的 $P$、$P^{-1}$，写出 $A=\begin{pmatrix}4&-3\\6&-5\end{pmatrix}$ 的 $A^n$。
>
> 答案：$A^n=\begin{pmatrix}2-(-2)^n&(-2)^n-1\\2-2(-2)^n&2(-2)^n-1\end{pmatrix}$。

很多时候只需要 $A^n\boldsymbol{x}$，用不着整个 $A^n$。这时把 $\boldsymbol{x}$ 写成特征向量的组合 $\boldsymbol{x}=c_1\boldsymbol{p}_1+\cdots+c_n\boldsymbol{p}_n$。每作用一次 $A$，每一项各乘自己的特征值，所以

$$A^n\boldsymbol{x}=c_1\lambda_1^n\boldsymbol{p}_1+\cdots+c_n\lambda_n^n\boldsymbol{p}_n.$$

这个式子能看出长期趋势。如果 $|\lambda_1|$ 严格最大并且 $c_1\ne0$，$n$ 很大时其他项和第一项相比可以忽略，$A^n\boldsymbol{x}$ 越来越贴近 $\boldsymbol{p}_1$ 所在的直线（$\lambda_1<0$ 时正负交替）：绝对值最大的特征值最终说了算。

**方法 4（$A^n=P\Lambda^nP^{-1}$）**

1. 先用方法 3 对角化，得到 $P$ 和 $\Lambda$；
2. 要整个 $A^n$：$A^n=P\Lambda^nP^{-1}$，先算 $P\Lambda^n$ 再右乘 $P^{-1}$；
3. 只要 $A^n\boldsymbol{x}$：把 $\boldsymbol{x}$ 分解成特征向量的组合，各项乘 $\lambda_i^n$ 再相加，不必求 $P^{-1}$。

**例 8**　循环神经网络（M.10.4）逐个读入一句话里的词，把读过的内容记在一个状态向量 $\boldsymbol{h}$ 里。每读一个新词，先把旧状态乘上同一个矩阵 $W$，再加进新词的信息（还有一步非线性处理，M.10 再讲）。只看第一个词的状态 $\boldsymbol{h}_0$ 被反复乘 $W$ 留下的部分，第 $t$ 步是 $\boldsymbol{h}_t=W^t\boldsymbol{h}_0$。设

$$W=\begin{pmatrix}0.85&0.35\\0.35&0.85\end{pmatrix},\qquad \boldsymbol{h}_0=(1,0)^{\mathsf T},$$

求 $\boldsymbol{h}_{10}$、$\boldsymbol{h}_{20}$。

先求特征值和特征向量。$\operatorname{tr}W=1.7$，$|W|=0.85^2-0.35^2=0.6$，特征方程 $\lambda^2-1.7\lambda+0.6=(\lambda-1.2)(\lambda-0.5)=0$。验算 $W(1,1)^{\mathsf T}=1.2(1,1)^{\mathsf T}$、$W(1,-1)^{\mathsf T}=0.5(1,-1)^{\mathsf T}$，所以 $(1,1)^{\mathsf T}$ 属于 1.2，$(1,-1)^{\mathsf T}$ 属于 0.5。

然后分解 $\boldsymbol{h}_0=0.5(1,1)^{\mathsf T}+0.5(1,-1)^{\mathsf T}$，由方法 4，

$$\boldsymbol{h}_t=0.5\times1.2^t\begin{pmatrix}1\\1\end{pmatrix}+0.5\times0.5^t\begin{pmatrix}1\\-1\end{pmatrix}.$$

$1.2^{10}\approx6.19$、$0.5^{10}\approx0.001$，所以 $\boldsymbol{h}_{10}\approx(3.10,3.10)^{\mathsf T}$；$1.2^{20}\approx38.3$、$0.5^{20}\approx10^{-6}$，所以 $\boldsymbol{h}_{20}\approx(19.17,19.17)^{\mathsf T}$。

沿 $(1,1)^{\mathsf T}$ 的部分 20 步放大了 38 倍，沿 $(1,-1)^{\mathsf T}$ 的部分缩到百万分之一。特征值的绝对值大于 1 的方向，信号爆炸；小于 1 的方向，信号消失。

合上书，推一遍 $A^n=P\Lambda^nP^{-1}$，再用 $A^n\boldsymbol{x}=\sum c_i\lambda_i^n\boldsymbol{p}_i$ 说明为什么绝对值最大的特征值最终说了算。

### 5. 不能或不必对角化时，Aⁿ 怎样算？

方法 4 要求出全部特征向量，再求一个逆矩阵。有两种情形可以绕开：矩阵简单到不必对角化，或者它根本不能对角化。

#### 秩为 1 的矩阵

**例 9**　求 $A=\begin{pmatrix}2&1&1\\4&2&2\\-2&-1&-1\end{pmatrix}$ 的 $A^n$。

$A$ 的三行分别是 $(2,1,1)$ 的 1、2、$-1$ 倍，秩为 1。记 $\boldsymbol{\alpha}=(1,2,-1)^{\mathsf T}$（各行的倍数），$\boldsymbol{\beta}=(2,1,1)^{\mathsf T}$，第 $i$ 行是 $\alpha_i\boldsymbol{\beta}^{\mathsf T}$，所以 $A=\boldsymbol{\alpha}\boldsymbol{\beta}^{\mathsf T}$（L.3.7 的外积）。

平方时，夹在中间的 $\boldsymbol{\beta}^{\mathsf T}\boldsymbol{\alpha}$ 是一个数，可以提到前面：

$$A^2=\boldsymbol{\alpha}(\boldsymbol{\beta}^{\mathsf T}\boldsymbol{\alpha})\boldsymbol{\beta}^{\mathsf T}=(\boldsymbol{\beta}^{\mathsf T}\boldsymbol{\alpha})A,\qquad \boldsymbol{\beta}^{\mathsf T}\boldsymbol{\alpha}=2+2-1=3.$$

每多乘一个 $A$ 就多一个因子 3，所以对 $n\ge1$ 有 $A^n=3^{n-1}A$。

那个数还可以直接读出来：$\boldsymbol{\beta}^{\mathsf T}\boldsymbol{\alpha}=\sum\alpha_i\beta_i$，而 $\boldsymbol{\alpha}\boldsymbol{\beta}^{\mathsf T}$ 的第 $i$ 个对角元正是 $\alpha_i\beta_i$，所以 $\boldsymbol{\beta}^{\mathsf T}\boldsymbol{\alpha}=\operatorname{tr}A=2+2-1$，不用拆。

**方法 5（秩一矩阵）**

1. $r(A)=1$ 时，取一个非零行作 $\boldsymbol{\beta}^{\mathsf T}$，用 $\boldsymbol{\alpha}$ 记各行是它的几倍，则 $A=\boldsymbol{\alpha}\boldsymbol{\beta}^{\mathsf T}$；
2. $A^2=(\operatorname{tr}A)A$，所以对 $n\ge1$ 有 $A^n=(\operatorname{tr}A)^{n-1}A$。

> 求 $A=\begin{pmatrix}1&2&3\\2&4&6\\-1&-2&-3\end{pmatrix}$ 的 $A^n$。
>
> 答案：各行是 $(1,2,3)$ 的 1、2、$-1$ 倍，秩 1；$\operatorname{tr}A=1+4-3=2$，$A^n=2^{n-1}A$。

#### 不能对角化的二阶矩阵

迹为 0 的秩一矩阵 $N$ 满足 $N^2=(\operatorname{tr}N)N=O$，例如 $N=\begin{pmatrix}1&1\\-1&-1\end{pmatrix}$。它不能对角化：特征值只能是 0（L.11.4），可对角化就只能相似于 $O$，而与 $O$ 相似的只有 $O$。这种 $N$ 正好用来处理不能对角化的矩阵。

先看老朋友②剪切：$J=E+N_0$，$N_0=\begin{pmatrix}0&1\\0&0\end{pmatrix}$，$N_0^2=O$。$E$ 与任何矩阵可交换，可以用二项式定理（L.3.5），含 $N_0^2$ 的项都是零：

$$J^n=(E+N_0)^n=E+nN_0=\begin{pmatrix}1&n\\0&1\end{pmatrix}.$$

剪切做 $n$ 次，就是一次推 $n$ 倍远。

**例 10**　求 $A=\begin{pmatrix}3&1\\-1&1\end{pmatrix}$ 的 $A^n$。

先判断能否对角化。$\operatorname{tr}A=4$，$|A|=4$，特征多项式 $\lambda^2-4\lambda+4=(\lambda-2)^2$。$A-2E=\begin{pmatrix}1&1\\-1&-1\end{pmatrix}$ 秩 1，几何重数 1，$A$ 不能对角化，方法 4 用不了。

模仿剪切，把 $A$ 拆成 $A=2E+N$，$N=A-2E$ 正是上面那个迹为 0 的秩一矩阵，$N^2=O$。$2E$ 与 $N$ 可交换，用二项式定理，$k\ge2$ 的项都含 $N^2=O$：

$$A^n=(2E+N)^n=2^nE+n\,2^{n-1}N=2^{n-1}\begin{pmatrix}n+2&n\\-n&2-n\end{pmatrix}.$$

这个拆法对只有二重实特征值、又不能对角化的二阶矩阵都适用。二重特征值 $\lambda_0$ 的几何重数为 1 时，$N=A-\lambda_0E$ 的秩为 1；它的迹是 $\operatorname{tr}A-2\lambda_0=0$，因为两个特征值之和是 $2\lambda_0$。所以 $N^2=(\operatorname{tr}N)N=O$。

**方法 6（拆成 $\lambda_0E+N$）**

1. 二阶矩阵只有二重特征值 $\lambda_0$、并且不能对角化时，令 $N=A-\lambda_0E$，则 $N^2=O$；
2. 对 $n\ge1$，$A^n=\lambda_0^nE+n\lambda_0^{n-1}N$，而 $A^0=E$。

#### 哈密顿–凯莱定理

下面换一条思路：不求特征向量，只用特征多项式来降次、求逆。线索在例 10 里。特征多项式是 $f(\lambda)=(\lambda-2)^2$，而把 $A$ 代进去，$f(A)=(A-2E)^2=N^2=O$：矩阵代入自己的特征多项式，得到零矩阵。这对一切方阵成立，叫作**哈密顿–凯莱定理**：若 $f(\lambda)=|\lambda E-A|$，则 $f(A)=O$。

可对角化时，证明分两步。

第一步，把 $f(A)$ 写成 $Pf(\Lambda)P^{-1}$。由第 4 节，$A^k=P\Lambda^kP^{-1}$，又 $E=PEP^{-1}$，所以多项式的每一项都能写成 $P(\cdots)P^{-1}$ 的形式，提出公共的 $P$ 和 $P^{-1}$，合起来就是 $f(A)=Pf(\Lambda)P^{-1}$。

第二步，$f(\Lambda)=\operatorname{diag}(f(\lambda_1),\dots,f(\lambda_n))$，而每个 $\lambda_i$ 都是 $f$ 的根，所以 $f(\Lambda)=O$，于是 $f(A)=O$。

二阶矩阵不论能否对角化，都可以直接验证：把 $A^2-(a+d)A+(ad-bc)E$ 乘开，四个元素都是 0。一般 $n$ 阶矩阵的证明要先在复数范围内把矩阵化成三角形，思路相同。

有了 $f(A)=O$，$A$ 的高次幂就能降下来。用 $\lambda^m$ 除以 $f(\lambda)$，得 $\lambda^m=q(\lambda)f(\lambda)+r(\lambda)$。代入 $A$ 时 $q(A)f(A)=O$，只剩 $A^m=r(A)$，而余式 $r$ 的次数低于 $f$ 的次数，也就是低于矩阵的阶数。

**方法 7（用特征多项式降次）**

1. 写出 $f(\lambda)=|\lambda E-A|$，由哈密顿–凯莱定理 $f(A)=O$；
2. 把高次幂逐次换成低次幂，或把 $g(\lambda)$ 除以 $f(\lambda)$ 取余式 $r(\lambda)$，则 $g(A)=r(A)$；
3. $f(A)=O$ 本身是 $A$ 的一个多项式关系式，常数项不为 0 时移项成 $A\cdot(\cdots)=E$，就解出 $A^{-1}$。

**例 11**　对例 10 的 $A$，用哈密顿–凯莱定理求 $A^{-1}$，并把 $A^4$ 写成 $aA+bE$。

由哈密顿–凯莱定理，$f(A)=A^2-4A+4E=O$。移项得 $A(4E-A)=4E$，所以

$$A^{-1}=E-\frac14A=\frac14\begin{pmatrix}1&-1\\1&3\end{pmatrix}.$$

高次幂则反复把 $A^2$ 换成 $4A-4E$，每换一次降一次：

$$A^3=4A^2-4A=12A-16E,\qquad A^4=4A^3-4A^2=4(12A-16E)-4(4A-4E)=32A-48E.$$

和例 10 的公式 $2^4E+4\cdot2^3N$ 一致。

合上书，说明 $(\boldsymbol{\alpha}\boldsymbol{\beta}^{\mathsf T})^2$ 为什么等于 $(\boldsymbol{\beta}^{\mathsf T}\boldsymbol{\alpha})\boldsymbol{\alpha}\boldsymbol{\beta}^{\mathsf T}$，再对可对角化的矩阵推一遍 $f(A)=O$。

### 6. 斐波那契数列的通项公式是从哪里来的？

斐波那契数列 $F_0=0$，$F_1=1$，$F_{n+2}=F_{n+1}+F_n$，依次是 $0,1,1,2,3,5,8,13,\dots$。递推每一步要用前面两项，不能直接写成「下一项等于矩阵乘这一项」。办法是把相邻两项捆成一个向量 $\boldsymbol{x}_n=(F_{n+1},F_n)^{\mathsf T}$，下一个向量是

$$\boldsymbol{x}_{n+1}=\begin{pmatrix}F_{n+2}\\F_{n+1}\end{pmatrix}=\begin{pmatrix}F_{n+1}+F_n\\F_{n+1}\end{pmatrix}=\begin{pmatrix}1&1\\1&0\end{pmatrix}\begin{pmatrix}F_{n+1}\\F_n\end{pmatrix}=A\boldsymbol{x}_n.$$

于是 $\boldsymbol{x}_n=A^n\boldsymbol{x}_0$，$\boldsymbol{x}_0=(1,0)^{\mathsf T}$。两步的递推变成了一步的矩阵递推，求通项就是用方法 4 算 $A^n\boldsymbol{x}_0$。

**例 12**　求 $F_n$ 的通项。

第一步，求特征值。特征方程

$$|\lambda E-A|=(\lambda-1)\lambda-1=\lambda^2-\lambda-1=0,$$

两根 $\varphi=\frac{1+\sqrt5}2\approx1.618$，$\psi=\frac{1-\sqrt5}2\approx-0.618$，互不相同，所以 $A$ 可对角化。

第二步，求特征向量。$(A-\lambda E)\boldsymbol{v}=\boldsymbol{0}$ 的第二行是 $v_1-\lambda v_2=0$，取 $\boldsymbol{v}=(\lambda,1)^{\mathsf T}$，即 $(\varphi,1)^{\mathsf T}$ 和 $(\psi,1)^{\mathsf T}$。

第三步，分解 $\boldsymbol{x}_0=c_1(\varphi,1)^{\mathsf T}+c_2(\psi,1)^{\mathsf T}$。比较第二个分量得 $c_1+c_2=0$；比较第一个分量得 $c_1\varphi+c_2\psi=1$，即 $c_1(\varphi-\psi)=1$。因为 $\varphi-\psi=\sqrt5$，所以 $c_1=\frac1{\sqrt5}$，$c_2=-\frac1{\sqrt5}$。

第四步，代入方法 4 的公式：

$$\boldsymbol{x}_n=\frac1{\sqrt5}\left[\varphi^n\begin{pmatrix}\varphi\\1\end{pmatrix}-\psi^n\begin{pmatrix}\psi\\1\end{pmatrix}\right],$$

取第二个分量，

$$F_n=\frac{\varphi^n-\psi^n}{\sqrt5}.$$

代 $n=2$ 验算：$\frac{\varphi^2-\psi^2}{\sqrt5}=\frac{(\varphi+\psi)(\varphi-\psi)}{\sqrt5}=1=F_2$。

章首的问题有了答案：$\sqrt5$ 来自特征值，两个带 $\sqrt5$ 的项相减时，无理部分恰好抵消。又因为 $|\psi|<1$，$\frac{\psi^n}{\sqrt5}$ 的绝对值小于 $\frac12$ 并且趋于 0，所以 $F_n$ 就是离 $\frac{\varphi^n}{\sqrt5}$ 最近的整数，例如 $\frac{\varphi^{10}}{\sqrt5}\approx55.004$，$F_{10}=55$。

一般的 $a_{n+2}=pa_{n+1}+qa_n$ 照样做。把 $\boldsymbol{x}_n=(a_{n+1},a_n)^{\mathsf T}$ 捆成向量，第一行用递推式、第二行抄下 $a_{n+1}$，矩阵就是 $A=\begin{pmatrix}p&q\\1&0\end{pmatrix}$，特征方程是 $\lambda^2-p\lambda-q=0$，相当于把 $a_n=\lambda^n$ 代入递推再约去 $\lambda^n$。

两根 $r_1\ne r_2$ 时，特征向量是 $(r_i,1)^{\mathsf T}$，$\boldsymbol{x}_n$ 的第二个分量是 $c_1r_1^n+c_2r_2^n$。

二重根 $r\ne0$ 时，$A-rE=\begin{pmatrix}p-r&q\\1&-r\end{pmatrix}$ 的第二行不为零，秩至少为 1；$r$ 是特征值，$|A-rE|=0$，秩小于 2，所以秩为 1，$A$ 不能对角化。用方法 6，$A^n=r^nE+nr^{n-1}N$，所以 $A^n\boldsymbol{x}_0$ 的分量都是 $(C_1+C_2n)r^n$ 的形式。

**方法 8（二阶线性递推的通项）**

1. 对 $a_{n+2}=pa_{n+1}+qa_n$，解特征方程 $\lambda^2=p\lambda+q$；
2. 两个不同的实根时，设 $a_n=C_1r_1^n+C_2r_2^n$；二重根 $r\ne0$ 时，设 $a_n=(C_1+C_2n)r^n$（$r=0$ 即 $p=q=0$，从 $a_2$ 起全为 0）；
3. 由 $a_0,a_1$ 定出 $C_1,C_2$。

> 用方法 8 求 $a_0=0$、$a_1=1$、$a_{n+2}=a_{n+1}+2a_n$ 的通项。
>
> 答案：$\lambda^2=\lambda+2$ 的根是 2 和 $-1$，设 $a_n=C_12^n+C_2(-1)^n$，由 $n=0,1$ 得 $C_1+C_2=0$、$2C_1-C_2=1$，解出 $C_1=\frac13$、$C_2=-\frac13$，所以 $a_n=\frac{2^n-(-1)^n}3$。

**例 13**　$a_0=1$，$a_1=4$，$a_{n+2}=4a_{n+1}-4a_n$，求 $a_n$。

和上一题不同，特征方程 $\lambda^2=4\lambda-4$ 即 $(\lambda-2)^2=0$，2 是二重根，$A$ 不能对角化，通项取 $(C_1+C_2n)2^n$ 的形式。

$n=0$ 给出 $C_1=1$；$n=1$ 给出 $2(C_1+C_2)=4$，即 $C_2=1$。所以 $a_n=(n+1)2^n$。

合上书，把斐波那契递推写成 $\boldsymbol{x}_{n+1}=A\boldsymbol{x}_n$，推出 $\varphi$、$\psi$ 和系数 $\pm\frac1{\sqrt5}$。

### 7. 用户留存、网页排名：反复转移以后会稳定在哪里？

回到章首的 App。开始时全是活跃用户，$\boldsymbol{x}_0=(1,0)^{\mathsf T}$，接下来 $\boldsymbol{x}_1=(0.8,0.2)^{\mathsf T}$，$\boldsymbol{x}_2=(0.7,0.3)^{\mathsf T}$。活跃占比一直往下走，会停在哪里？

$M$ 的每一列加起来都是 1，因为每类用户下个月的去向比例之和为 1。记 $\boldsymbol{1}=(1,1)^{\mathsf T}$，列和为 1 写成 $\boldsymbol{1}^{\mathsf T}M=\boldsymbol{1}^{\mathsf T}$；转置得 $M^{\mathsf T}\boldsymbol{1}=\boldsymbol{1}$，所以 1 是 $M^{\mathsf T}$ 的特征值。又因为 $|\lambda E-M^{\mathsf T}|=|(\lambda E-M)^{\mathsf T}|=|\lambda E-M|$（L.6.4），$M$ 与 $M^{\mathsf T}$ 的特征值相同，1 也是 $M$ 的特征值。另一个特征值是 $\operatorname{tr}M-1=1.5-1=0.5$。

再求特征向量。解 $(M-E)\boldsymbol{x}=\boldsymbol{0}$，第一行是 $-0.2x_1+0.3x_2=0$，取 $(3,2)^{\mathsf T}$，缩放成分量和为 1 的 $(0.6,0.4)^{\mathsf T}$。属于 0.5 的特征向量是 $(1,-1)^{\mathsf T}$。由方法 4，

$$\boldsymbol{x}_0=\begin{pmatrix}0.6\\0.4\end{pmatrix}+0.4\begin{pmatrix}1\\-1\end{pmatrix},\qquad \boldsymbol{x}_n=\begin{pmatrix}0.6\\0.4\end{pmatrix}+0.4\times0.5^n\begin{pmatrix}1\\-1\end{pmatrix}\to\begin{pmatrix}0.6\\0.4\end{pmatrix}.$$

长期来看 60% 的用户活跃。偏离 $(0.6,0.4)^{\mathsf T}$ 的部分沿 $(1,-1)^{\mathsf T}$ 方向，每个月减半（图 L12-n2）。

![各月的占比 $\boldsymbol{x}_0,\boldsymbol{x}_1,\boldsymbol{x}_2,\dots$ 都在线段 $x_1+x_2=1$ 上，沿 $(1,-1)^{\mathsf T}$ 方向向稳态 $(0.6,0.4)^{\mathsf T}$ 靠拢，每一步距离减半](fig/L12-n2.pdf){width=60%}

#### 转移矩阵的几件事

元素都非负、每列之和都是 1 的方阵叫作**转移矩阵**。刚才的计算里有四件事可以推广。下面假定 $M$ 可对角化，属于 1 的特征方向只有一条，且其上的向量分量和不为 0（元素全为正时后两条总成立，理由见 P.9.7）。记 $\boldsymbol{1}=(1,\dots,1)^{\mathsf T}$，$\boldsymbol{1}^{\mathsf T}\boldsymbol{v}$ 就是 $\boldsymbol{v}$ 的分量之和。

第一，1 是特征值，理由和上面一样。

第二，属于其他特征值 $\lambda\ne1$ 的特征向量 $\boldsymbol{v}$，分量之和为 0。把 $M\boldsymbol{v}$ 的分量和用两种方法算：用列和为 1，$\boldsymbol{1}^{\mathsf T}M\boldsymbol{v}=\boldsymbol{1}^{\mathsf T}\boldsymbol{v}$；用 $M\boldsymbol{v}=\lambda\boldsymbol{v}$，它又等于 $\lambda\boldsymbol{1}^{\mathsf T}\boldsymbol{v}$。两者相等，$(\lambda-1)\boldsymbol{1}^{\mathsf T}\boldsymbol{v}=0$，而 $\lambda\ne1$，所以 $\boldsymbol{1}^{\mathsf T}\boldsymbol{v}=0$。

第三，稳态那一项的系数总是 1。在属于 1 的方向上取分量和为 1 的 $\boldsymbol{\pi}$。把初始占比写成 $\boldsymbol{x}_0=c\boldsymbol{\pi}+(\text{其他特征向量的组合})$，两边求分量和。左边 $\boldsymbol{x}_0$ 是占比，分量和为 1；右边 $c\boldsymbol{\pi}$ 的分量和是 $c$，其他项的分量和都是 0（第二条）。所以 $c=1$，与初始占比无关。

第四，元素全为正时，其他特征值的绝对值都小于 1。$\boldsymbol{v}$ 的分量和为 0，分量有正有负（复数时，不全朝同一方向），$M\boldsymbol{v}$ 的每个分量里各项会部分抵消：$m_{ij}$ 全为正、$v_j$ 又不全同向，三角不等式取不到等号，所以

$$|\lambda v_i|<\sum_jm_{ij}|v_j|.$$

对 $i$ 求和并用列和为 1，得 $|\lambda|\sum_i|v_i|<\sum_j|v_j|$，即 $|\lambda|<1$。

四件事合起来：$\boldsymbol{x}_n=\boldsymbol{\pi}+\sum c_i\lambda_i^n\boldsymbol{v}_i$，其他项乘上 $\lambda_i^n$ 后趋于 0，所以 $\boldsymbol{x}_n\to\boldsymbol{\pi}$。这个 $\boldsymbol{\pi}$ 叫作**稳态**。

**方法 9（求稳态）**

1. 确认 $M$ 的各列之和为 1；
2. 解 $(M-E)\boldsymbol{x}=\boldsymbol{0}$；元素全为正时解只有一个方向，缩放成分量和为 1 就是稳态 $\boldsymbol{\pi}$；
3. 在本节的假定下，从任何初始占比出发都收敛到它；反复乘 $M$（**幂迭代**）也能逼近它，偏离的衰减速度由其余特征值里最大的 $|\lambda|$ 决定。

**例 14**　求 $M=\begin{pmatrix}0.7&0.3&0.3\\0.1&0.6&0.1\\0.2&0.1&0.6\end{pmatrix}$ 的稳态，并从 $(1,0,0)^{\mathsf T}$ 出发做三步幂迭代。

$M$ 的各列和为 1，元素全为正。$(M-E)\boldsymbol{x}=\boldsymbol{0}$ 乘 10 后，前两个方程是

$$-3x_1+3x_2+3x_3=0,\qquad x_1-4x_2+x_3=0.$$

第一个给出 $x_1=x_2+x_3$，代入第二个得 $2x_3=3x_2$。取 $x_2=2$，则 $x_3=3$，$x_1=5$。第三个方程 $2x_1+x_2-4x_3=10+2-12=0$ 也满足。缩放成分量和为 1，得 $\boldsymbol{\pi}=(0.5,0.2,0.3)^{\mathsf T}$。

从 $(1,0,0)^{\mathsf T}$ 出发反复乘 $M$，前三步是

$$\boldsymbol{x}_1=(0.7,0.1,0.2)^{\mathsf T},\quad \boldsymbol{x}_2=(0.58,0.15,0.27)^{\mathsf T},\quad \boldsymbol{x}_3=(0.532,0.175,0.293)^{\mathsf T}.$$

偏离 $\boldsymbol{x}_2-\boldsymbol{\pi}=(0.08,-0.05,-0.03)^{\mathsf T}$，$\boldsymbol{x}_3-\boldsymbol{\pi}=(0.032,-0.025,-0.007)^{\mathsf T}$，分量和都是 0。大致每步减半，因为 $M$ 的另两个特征值是 0.5 和 0.4：由 $\operatorname{tr}M=1.9$、$|M|=0.2$，去掉特征值 1 后另两个之和 0.9、之积 0.2。

#### 行和为 1 的写法

很多书（包括 P.9）把占比写成行向量 $\boldsymbol{\pi}$，转移矩阵 $R$ 的每一行之和为 1，一步转移写成 $\boldsymbol{\pi}_{n+1}=\boldsymbol{\pi}_nR$。

两边转置得 $\boldsymbol{\pi}_{n+1}^{\mathsf T}=R^{\mathsf T}\boldsymbol{\pi}_n^{\mathsf T}$。可见 $R^{\mathsf T}$ 就是本节列和为 1 的 $M$，两种写法互为转置。稳态 $\boldsymbol{\pi}R=\boldsymbol{\pi}$ 转置后是 $R^{\mathsf T}\boldsymbol{\pi}^{\mathsf T}=\boldsymbol{\pi}^{\mathsf T}$，所以对 $R^{\mathsf T}$ 用方法 9 即可。

名字的来历：在 $\boldsymbol{\pi}R=\boldsymbol{\pi}$ 里，$\boldsymbol{\pi}$ 乘在 $R$ 的左边，所以叫作 $R$ 的**左特征向量**；平常 $R\boldsymbol{x}=\lambda\boldsymbol{x}$ 里乘在右边的 $\boldsymbol{x}$ 是右特征向量。

最容易错的是直接解 $(R-E)\boldsymbol{x}=\boldsymbol{0}$：行和为 1 使 $R\boldsymbol{1}=\boldsymbol{1}$，$\boldsymbol{1}$ 总是它的解，但这是右特征向量，不是稳态。

> 行和为 1 的 $R=\begin{pmatrix}0.9&0.1\\0.4&0.6\end{pmatrix}$，求满足 $\boldsymbol{\pi}R=\boldsymbol{\pi}$、分量和为 1 的 $\boldsymbol{\pi}$。
>
> 答案：第一个分量给出 $0.9\pi_1+0.4\pi_2=\pi_1$，即 $\pi_1=4\pi_2$，所以 $\boldsymbol{\pi}=(0.8,0.2)$。

网页排名的分数也是这样一个稳态，网页有几十亿个，通常用幂迭代来算。

合上书，说明转移矩阵为什么有特征值 1、其他特征向量的分量和为什么是 0，并据此说明稳态与初始占比无关。

### 本章小结

| 方法 | 什么时候用 | 对应题号 |
|---|---|---|
| 方法 1（相似不变量） | 判断不相似；由相似求参数（求出后验证） | L12-01、02、06 |
| 方法 2（只查重根） | 判断能否对角化，含参数时分情况 | L12-07、08 |
| 方法 3（对角化四步） | 写出 $P$、$\Lambda$；由特征值和特征向量反求 $A=P\Lambda P^{-1}$ | L12-03、07、13 |
| 方法 4（$A^n=P\Lambda^nP^{-1}$） | 可对角化矩阵的幂；只要 $A^n\boldsymbol{x}$ 时按特征向量分解 | L12-04、13 |
| 方法 5（秩一矩阵） | $r(A)=1$：$A^n=(\operatorname{tr}A)^{n-1}A$ | L12-05 |
| 方法 6（拆成 $\lambda_0E+N$） | 二阶、二重特征值、不能对角化 | L12-10、12、13 |
| 方法 7（用特征多项式降次） | 高次多项式 $g(A)$、用 $f(A)=O$ 求逆 | L12-09、10、12 |
| 方法 8（二阶线性递推的通项） | $a_{n+2}=pa_{n+1}+qa_n$ 求通项 | L12-11 |
| 方法 9（求稳态） | 转移矩阵的长期占比、幂迭代 | L12-14 |

可逆大定理本章没有新增条目，到 L.11 为止的串联是：$A\boldsymbol{x}=\boldsymbol{0}$ 只有零解 $\iff$ $A$ 可逆 $\iff$ $|A|\ne0$ $\iff$ $r(A)=n$ $\iff$ 列向量构成 $\mathbb{R}^n$ 的一组基 $\iff$ 0 不是特征值。本章多了一种用法：相似矩阵的行列式相同，所以 $A\sim B$ 时，两者同时可逆或同时不可逆。
