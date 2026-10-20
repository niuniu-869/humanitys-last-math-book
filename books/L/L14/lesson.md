## L.14 · 二次型与正定

几只股票按比例组合，组合收益的方差是各个比例两两相乘再加权求和：没有一次项，没有常数项，而且不会是负数。训练模型时，损失函数（衡量模型错得多厉害的函数）在最低点附近也近似于这样一个二次式，画出来像一只碗。碗口朝上，最低点才真是最低点；碗又窄又长，梯度下降就会在两壁之间来回弹，走得很慢。碗朝不朝上、圆不圆，都由一个对称矩阵决定。

这类式子最早出现在数论里：整系数的 $ax^2+bxy+cy^2$ 能取到哪些整数？拉格朗日和高斯发现，作行列式为 $\pm1$ 的整系数换元（能用整系数换回来），式子变了样，能取到的整数却不变，于是问题变成「换元以后什么不变」。对实系数的二次型，西尔维斯特在 1852 年证明：不管用哪种可逆换元化成平方和，正项和负项的个数都不变，这就是惯性定理。另一条线来自微积分：判断多元函数的极值，要看二阶导数组成的二次式在各个方向上的符号。

第 1 节把二次式写成 $\boldsymbol x^{\mathsf T}A\boldsymbol x$；第 2 节转动坐标轴消去交叉项；第 3 节改用配方；第 4 节看各种化法下什么不变；第 5 节定义「碗口朝上」，即正定；第 6 节不求特征值判断正定；第 7 节求球面上的最值；第 8 节把 $n$ 元函数的导数写成向量和矩阵；第 9 节用它们判断极值。

### 1. 多元二次函数怎样用一个矩阵记下来？

C.24 判断二元函数的极值时，关键是驻点附近的二次项，例如

$$f(x,y)=2x^2+4xy+5y^2.$$

它对所有 $(x,y)\ne(0,0)$ 都是正的吗？交叉项 $4xy$ 可正可负，一眼看不出。变量一多，式子更长，先要找一个整齐的记法。

把交叉项拆成两半，$4xy=2xy+2yx$，四项的系数恰好排成一张对称的表：

$$f=\begin{pmatrix}x&y\end{pmatrix}\begin{pmatrix}2&2\\2&5\end{pmatrix}\begin{pmatrix}x\\y\end{pmatrix}.$$

从右往左乘来核对：矩阵乘列向量得 $(2x+2y,\ 2x+5y)^{\mathsf T}$，再左乘 $(x,y)$ 得 $x(2x+2y)+y(2x+5y)=2x^2+4xy+5y^2$。

一般地，记 $\boldsymbol x=(x_1,\dots,x_n)^{\mathsf T}$。$A\boldsymbol x$ 的第 $i$ 个分量是 $\sum_ja_{ij}x_j$（L.3.1），$\boldsymbol x^{\mathsf T}$ 乘它，就是

$$\boldsymbol x^{\mathsf T}A\boldsymbol x=\sum_{i=1}^n\sum_{j=1}^na_{ij}x_ix_j.$$

这个双重和里有 $n^2$ 项。$n=2$ 时把四项全写出来：

$$a_{11}x_1^2+a_{12}x_1x_2+a_{21}x_2x_1+a_{22}x_2^2.$$

中间两项乘出来是同一个单项式 $x_1x_2$，合并成 $(a_{12}+a_{21})x_1x_2$；$A$ 对称时就是 $2a_{12}x_1x_2$。$n$ 元时也一样：$i=j$ 的项给出平方项 $a_{ii}x_i^2$；$i\ne j$ 时，$(i,j)$ 和 $(j,i)$ 两项合并成 $2a_{ij}x_ix_j$。开头的 $4xy=2xy+2yx$ 就是这样来的。

每一项都恰好是两个变量相乘的多项式，叫作 $n$ 元**二次型**；写成 $\boldsymbol x^{\mathsf T}A\boldsymbol x$、$A$ 对称时，$A$ 叫作它的矩阵，$A$ 的秩叫作二次型的**秩**。

为什么非要对称？只要 $a_{12}+a_{21}=4$，比如 $\begin{pmatrix}2&4\\0&5\end{pmatrix}$，给出的都是同一个 $f$。规定对称以后，矩阵由 $f$ 唯一确定，还能用 L.13 的正交对角化。给了不对称的 $B$，$\boldsymbol x^{\mathsf T}B\boldsymbol x$ 的矩阵是 $\frac12(B+B^{\mathsf T})$：一个数的转置是它自己，所以 $\boldsymbol x^{\mathsf T}B\boldsymbol x=(\boldsymbol x^{\mathsf T}B\boldsymbol x)^{\mathsf T}=\boldsymbol x^{\mathsf T}B^{\mathsf T}\boldsymbol x$，两式平均即得。

拿 L.3 的老朋友试一试：

| 矩阵 | 二次型 $\boldsymbol x^{\mathsf T}M\boldsymbol x$（$\boldsymbol x=(x,y)^{\mathsf T}$） | 说明 |
|---|---|---|
| ① 对称伸缩 $\begin{pmatrix}2&1\\1&2\end{pmatrix}$ | $2x^2+2xy+2y^2$ | 对称，直接读 |
| ② 剪切 $\begin{pmatrix}1&1\\0&1\end{pmatrix}$ | $x^2+xy+y^2$ | 不对称，它的矩阵是 $\begin{pmatrix}1&\frac12\\\frac12&1\end{pmatrix}$ |
| ③ 转 90° $\begin{pmatrix}0&-1\\1&0\end{pmatrix}$ | $-xy+yx=0$ | 矩阵的秩是 2，二次型的秩却是 0 |
| ④ 投影 $\frac12\begin{pmatrix}1&1\\1&1\end{pmatrix}$ | $\frac12(x+y)^2$ | 秩 1：两个变量只通过 $x+y$ 出现 |

③ 这一行是常见的坑：二次型的秩要按对称化以后的矩阵算，③ 对称化后是零矩阵。

**方法 1（写出二次型的矩阵）**

1. 平方项 $x_i^2$ 的系数放在对角线第 $i$ 个位置；
2. 交叉项 $x_ix_j$ 的系数对半分，放在 $(i,j)$ 和 $(j,i)$ 两处；
3. 没有出现的项填 0；
4. 给的是不对称的 $B$ 时，先换成 $\frac12(B+B^{\mathsf T})$，二次型的秩按这个对称矩阵算。

**例 1**　写出 $f(x_1,x_2,x_3)=x_1^2+3x_2^2+4x_1x_2-2x_1x_3+2x_2x_3$ 的矩阵，并求它的秩。

平方项给出对角线 $1,3,0$（没有 $x_3^2$ 项）。$4x_1x_2$ 在 $(1,2)$、$(2,1)$ 两处各放 2，$-2x_1x_3$ 各放 $-1$，$2x_2x_3$ 各放 1：

$$A=\begin{pmatrix}1&2&-1\\2&3&1\\-1&1&0\end{pmatrix}.$$

按第一行展开，$|A|=1\cdot(0-1)-2\cdot(0+1)+(-1)\cdot(2+3)=-8\ne0$，所以秩为 3。

> 写出 $g=x_1^2+x_2^2+x_3^2+2x_1x_2+2x_1x_3+2x_2x_3$ 的矩阵和秩。
>
> 答案：矩阵的 9 个元素都是 1，秩为 1。事实上 $g=(x_1+x_2+x_3)^2$，三个变量只通过一个组合出现。

合上书，用 $n=2$ 的四项说明 $\boldsymbol x^{\mathsf T}A\boldsymbol x$ 里交叉项 $x_ix_j$ 的系数为什么是 $2a_{ij}$。

### 2. 怎样转动坐标轴，消去交叉项？

曲线 $2x^2+4xy+5y^2=6$ 是什么形状？如果方程是 $y_1^2+6y_2^2=6$，立刻知道是半轴长 $\sqrt6$ 和 1 的椭圆。有交叉项，说明坐标轴没有对准图形的对称轴，那就把坐标轴转过去对准它。

转动坐标轴用正交矩阵描述。设 $Q$ 是正交矩阵（$Q^{\mathsf T}Q=E$，L.10.4），列为 $\boldsymbol q_1,\dots,\boldsymbol q_n$，作换元

$$\boldsymbol x=Q\boldsymbol y=y_1\boldsymbol q_1+\cdots+y_n\boldsymbol q_n.$$

$y_i=\boldsymbol q_i^{\mathsf T}\boldsymbol x$ 是同一个点在以 $\boldsymbol q_1,\dots,\boldsymbol q_n$ 为坐标轴的新坐标系里的坐标（L.10.3）。正交矩阵保长度、保夹角，所以图形本身没有动，只是换了一副坐标轴去看。代进二次型，用 $(Q\boldsymbol y)^{\mathsf T}=\boldsymbol y^{\mathsf T}Q^{\mathsf T}$ 和结合律：

$$\boldsymbol x^{\mathsf T}A\boldsymbol x=(Q\boldsymbol y)^{\mathsf T}A(Q\boldsymbol y)=\boldsymbol y^{\mathsf T}(Q^{\mathsf T}AQ)\boldsymbol y.$$

要新二次型没有交叉项，就要 $Q^{\mathsf T}AQ$ 是对角矩阵。$A$ 对称，L.13.3 的谱定理正好保证有这样的 $Q$：它的列是 $A$ 的两两正交的单位特征向量，$Q^{\mathsf T}AQ=\Lambda=\operatorname{diag}(\lambda_1,\dots,\lambda_n)$，即对角线依次为 $\lambda_1,\dots,\lambda_n$、其余为 0 的对角矩阵。于是

$$f=\lambda_1y_1^2+\lambda_2y_2^2+\cdots+\lambda_ny_n^2.$$

只含平方项的二次型叫**标准形**。用正交变换化出的标准形，系数就是 $A$ 的特征值；新坐标轴 $\boldsymbol q_i$ 是对应的特征向量方向，叫作**主轴**。$Q$ 不唯一，但系数总是那组特征值。

回到开头。$A=\begin{pmatrix}2&2\\2&5\end{pmatrix}$ 的迹是 7、行列式是 6，特征值是 $t^2-7t+6=0$ 的根 1 和 6。解 $(A-E)\boldsymbol x=\boldsymbol0$ 得特征向量 $(2,-1)^{\mathsf T}$，解 $(A-6E)\boldsymbol x=\boldsymbol0$ 得 $(1,2)^{\mathsf T}$。单位化得 $\boldsymbol q_1=\frac1{\sqrt5}(2,-1)^{\mathsf T}$、$\boldsymbol q_2=\frac1{\sqrt5}(1,2)^{\mathsf T}$，于是 $f=y_1^2+6y_2^2$。曲线 $f=6$ 是沿 $\boldsymbol q_1$ 半轴长 $\sqrt6$、沿 $\boldsymbol q_2$ 半轴长 1 的椭圆。

![椭圆 $2x^2+4xy+5y^2=6$ 在虚线主轴的坐标下是 $y_1^2+6y_2^2=6$：沿 $\boldsymbol q_1$ 半轴 $\sqrt6$，沿 $\boldsymbol q_2$ 半轴 1](fig/L14-n1.pdf){width=58%}

L.13 开头的问题也有了答案。① 的二次型 $2x^2+2xy+2y^2$，特征值 3、1，主轴沿 $(1,1)^{\mathsf T}$ 和 $(1,-1)^{\mathsf T}$，所以椭圆 $2x^2+2xy+2y^2=1$ 化成 $3y_1^2+y_2^2=1$：沿 $(1,1)^{\mathsf T}$ 的半轴是 $\frac1{\sqrt3}$，沿 $(1,-1)^{\mathsf T}$ 的半轴是 1。

**方法 2（正交变换化标准形）**

1. 写出矩阵 $A$；
2. 求特征值；
3. 求特征向量，重特征值的特征空间里先施密特正交化，再全部单位化（L.13.4）；
4. 以它们为列排成 $Q$，令 $\boldsymbol x=Q\boldsymbol y$，得 $f=\sum\lambda_iy_i^2$，$\lambda_i$ 的次序与 $Q$ 的列一一对应。

**例 2**　用正交变换把 $f=x_1^2+2x_2^2+3x_3^2-4x_1x_2-4x_2x_3$ 化成标准形，并说明 $f=1$ 是什么曲面。

第一步，矩阵是 $A=\begin{pmatrix}1&-2&0\\-2&2&-2\\0&-2&3\end{pmatrix}$。

第二步，$\lambda E-A=\begin{pmatrix}\lambda-1&2&0\\2&\lambda-2&2\\0&2&\lambda-3\end{pmatrix}$，按第一行展开，再把两项分别乘开：

$$(\lambda-1)\big[(\lambda-2)(\lambda-3)-4\big]-2\cdot2(\lambda-3)=(\lambda^3-6\lambda^2+7\lambda-2)-(4\lambda-12)=\lambda^3-6\lambda^2+3\lambda+10.$$

试根 $\lambda=-1$ 得 0，除掉因式 $\lambda+1$ 后剩 $\lambda^2-7\lambda+10=(\lambda-2)(\lambda-5)$，特征值是 $-1,2,5$。

第三步，逐个解 $(A-\lambda E)\boldsymbol x=\boldsymbol0$：

- $\lambda=-1$：由第一、三行得 $x_1=x_2$、$x_2=2x_3$，取 $(2,2,1)^{\mathsf T}$；
- $\lambda=2$：得 $x_1=-2x_2$、$x_3=2x_2$，取 $(-2,1,2)^{\mathsf T}$；
- $\lambda=5$：得 $x_2=-2x_1$、$x_3=2x_1$，取 $(1,-2,2)^{\mathsf T}$。

三个特征值互不相同，特征向量已经两两正交（L.13.2），长度都是 3。

第四步，

$$Q=\frac13\begin{pmatrix}2&-2&1\\2&1&-2\\1&2&2\end{pmatrix},\qquad \boldsymbol x=Q\boldsymbol y,\qquad f=-y_1^2+2y_2^2+5y_3^2.$$

$f=1$ 在新坐标里是 $-y_1^2+2y_2^2+5y_3^2=1$，两正一负，是单叶双曲面（C.19.13）。正交变换不改变形状，原来的曲面也是单叶双曲面。

> 用正交变换化 $g=3x^2+2xy+3y^2$ 为标准形。
>
> 答案：矩阵 $\begin{pmatrix}3&1\\1&3\end{pmatrix}$，特征值 2、4，单位特征向量 $\frac1{\sqrt2}(1,-1)^{\mathsf T}$、$\frac1{\sqrt2}(1,1)^{\mathsf T}$，令 $\boldsymbol x=Q\boldsymbol y$ 得 $g=2y_1^2+4y_2^2$。

合上书，从 $\boldsymbol x=Q\boldsymbol y$ 出发，推一遍标准形的系数为什么是特征值。

### 3. 不要求转动、只要求换元可逆时，有没有更快的化法？

三阶矩阵求特征值要解三次方程，常常没有整数根。如果只关心二次型的正负（碗还是马鞍），不必坚持转动，任何能换回去的换元都可以。最老的办法是配方。

**例 3**　用配方法把 $f=x_1^2+2x_2^2+5x_3^2+2x_1x_2+2x_1x_3+6x_2x_3$ 化成标准形，写出所用的换元。

思路：一次收拾一个变量，把含它的项全部收进一个完全平方。

先收拾 $x_1$。$x_1^2+2x_1(x_2+x_3)$ 补上 $(x_2+x_3)^2$ 就是 $(x_1+x_2+x_3)^2$，补的部分再减回去：

$$f=(x_1+x_2+x_3)^2-(x_2+x_3)^2+2x_2^2+5x_3^2+6x_2x_3=(x_1+x_2+x_3)^2+x_2^2+4x_2x_3+4x_3^2.$$

剩下的部分不再含 $x_1$。对 $x_2$ 重复一次：$x_2^2+4x_2x_3+4x_3^2=(x_2+2x_3)^2$。令

$$y_1=x_1+x_2+x_3,\qquad y_2=x_2+2x_3,\qquad y_3=x_3,$$

得 $f=y_1^2+y_2^2$。

配方只产生两个平方，第三个新变量为什么取 $x_3$？要凑够三个新变量，换元才能换回去，$x_3$ 是最简单的选择。从下往上解出 $x_3=y_3$，$x_2=y_2-2y_3$，$x_1=y_1-x_2-x_3=y_1-y_2+y_3$，即

$$\boldsymbol x=C\boldsymbol y,\qquad C=\begin{pmatrix}1&-1&1\\0&1&-2\\0&0&1\end{pmatrix},\qquad |C|=1\ne0.$$

一般地，作可逆换元 $\boldsymbol x=C\boldsymbol y$，和上一节一样的计算给出 $\boldsymbol x^{\mathsf T}A\boldsymbol x=\boldsymbol y^{\mathsf T}(C^{\mathsf T}AC)\boldsymbol y$。$C$ 可逆时，称 $B=C^{\mathsf T}AC$ 与 $A$ **合同**。

合同保持对称，因为 $(C^{\mathsf T}AC)^{\mathsf T}=C^{\mathsf T}A^{\mathsf T}C$；也保持秩，因为乘可逆矩阵不改变秩（L.7.7）。注意这里的 $C$ 是「用 $\boldsymbol y$ 表示 $\boldsymbol x$」的那个矩阵，不是它的逆：例 3 中 $A=\begin{pmatrix}1&1&1\\1&2&3\\1&3&5\end{pmatrix}$，用上面的 $C$ 乘出来正是 $C^{\mathsf T}AC=\operatorname{diag}(1,1,0)$。

只有交叉项、没有平方项时，配方无从下手，比如 $f=2x_1x_2$。这时先造出平方项。平方差公式 $(y_1+y_2)(y_1-y_2)=y_1^2-y_2^2$ 把一个乘积变成了两个平方，所以令 $x_1=y_1+y_2$、$x_2=y_1-y_2$，就有 $2x_1x_2=2y_1^2-2y_2^2$。这个换元的矩阵 $\begin{pmatrix}1&1\\1&-1\end{pmatrix}$ 行列式是 $-2\ne0$，可以换回去。

**方法 3（配方法）**

1. 取一个有平方项的变量，把含它的项全部收进一个完全平方，补上的部分减回去；
2. 剩下的式子少了一个变量，重复第 1 步；
3. 只有交叉项 $x_ix_j$、没有平方项时，先令 $x_i=y_i+y_j$、$x_j=y_i-y_j$ 造出平方项，再照常配方；
4. 新变量凑够 $n$ 个，写出 $\boldsymbol x=C\boldsymbol y$，检查 $|C|\ne0$。

> 用配方法化 $g=x_1^2-4x_1x_2+3x_2^2$ 为标准形。
>
> 答案：$g=(x_1-2x_2)^2-4x_2^2+3x_2^2=(x_1-2x_2)^2-x_2^2$，令 $y_1=x_1-2x_2$、$y_2=x_2$，得 $y_1^2-y_2^2$。

合上书，把例 3 的两次配方重做一遍，写出换元矩阵 $C$。

### 4. 不同化法得到的标准形不一样，什么是不变的？

例 3 的矩阵如果用正交变换来化，直接算 $|\lambda E-A|=\lambda(\lambda^2-8\lambda+6)$，特征值是 $0$ 和 $4\pm\sqrt{10}$，标准形是 $(4+\sqrt{10})z_1^2+(4-\sqrt{10})z_2^2$；配方法给的是 $y_1^2+y_2^2$。系数完全不同，但正系数都是 2 个，负系数都是 0 个。

用碗的图景看这件事：换元就是换一副坐标去看同一张曲面 $z=f(\boldsymbol x)$。坐标可以斜着、可以把刻度拉长，所以系数会变；但曲面在几个方向上朝上弯、几个方向上朝下弯，是曲面自己的事，不随坐标改变。

**惯性定理**　二次型经任何可逆换元化成标准形，正系数的个数 $p$ 和负系数的个数 $q$ 都是确定的，并且 $p+q$ 等于二次型的秩（其余系数是 0）。$p$、$q$ 分别叫**正惯性指数**和**负惯性指数**。

为什么成立？只证正项个数，负项同理。思路是：如果两种写法的正项个数不同，就能找到一个非零的 $\boldsymbol x$，在一种写法下 $f>0$，在另一种写法下 $f\le0$，矛盾。

设两个可逆换元 $\boldsymbol x=C_1\boldsymbol y$、$\boldsymbol x=C_2\boldsymbol z$ 把 $f$ 化成两个标准形，各自把正系数排在前面：

$$f=d_1y_1^2+\cdots+d_ny_n^2,\qquad f=e_1z_1^2+\cdots+e_nz_n^2,$$

其中 $d_1,\dots,d_p>0$、其余 $d_i\le0$，$e_1,\dots,e_s>0$、其余 $e_i\le0$。假设 $s<p$。

1. 新变量是 $\boldsymbol x$ 的线性组合：$\boldsymbol y=C_1^{-1}\boldsymbol x$，$\boldsymbol z=C_2^{-1}\boldsymbol x$。
2. 要求 $z_1=\cdots=z_s=0$（去掉第二种写法的全部正项）和 $y_{p+1}=\cdots=y_n=0$（第一种写法只留正项），这是关于 $\boldsymbol x$ 的 $s+(n-p)$ 个齐次方程。因为 $s<p$，方程个数少于未知数个数 $n$，有非零解 $\boldsymbol x$（L.4.3）。
3. 在这个 $\boldsymbol x$ 上看第二种写法：只剩系数 $\le0$ 的项，所以 $f\le0$。
4. 再看第一种写法：$\boldsymbol x\ne\boldsymbol0$，而 $C_1^{-1}$ 可逆，所以 $\boldsymbol y\ne\boldsymbol0$；$y_{p+1},\dots,y_n$ 已经是 0，所以 $y_1,\dots,y_p$ 不全为 0，$f=d_1y_1^2+\cdots+d_py_p^2>0$。

第 3、4 步矛盾，所以 $s\ge p$；两种写法对调，又得 $p\ge s$。

用正交变换时系数是特征值，所以 $p$、$q$ 就是正、负特征值的个数（按重数算）。对标准形 $\sum d_iy_i^2$，对 $d_i\ne0$ 令 $w_i=\sqrt{|d_i|}\,y_i$，把系数的绝对值吸收进变量（$d_i=0$ 的变量原样保留，换元仍可逆），正项排在前面，就变成

$$w_1^2+\cdots+w_p^2-w_{p+1}^2-\cdots-w_{p+q}^2,$$

叫**规范形**。约定正项在前、负项在后，由惯性定理它是唯一的。两个同阶实对称矩阵合同，当且仅当 $p$、$q$ 都相同：相同时两者都合同于同一个规范形的矩阵，而合同可以传递。

#### 三种关系：等价、相似、合同

到这里，矩阵之间有了三种关系：等价（L.7.6）、相似（L.12.1）、合同。它们有一个共同点：都是在 $A$ 的左右各乘一个可逆矩阵。区别只在左右两个矩阵之间的联系：等价时互不相干，相似时互为逆矩阵，合同时互为转置。再看表。

| 关系 | 定义 | 不变的量 | 实对称矩阵怎样判断 |
|---|---|---|---|
| 等价 | $PAQ=B$，$P,Q$ 可逆 | 秩 | 同型且秩相等 |
| 相似 | $P^{-1}AP=B$ | 特征值、迹、行列式、秩 | 特征值相同 |
| 合同 | $C^{\mathsf T}AC=B$，$C$ 可逆 | 秩、正负惯性指数 | $p$、$q$ 都相同 |

相似、合同都推出等价。对实对称矩阵，相似推出合同：特征值相同，正负个数自然相同。反过来不成立：$E$ 与 $2E$ 合同（取 $C=\sqrt2E$），特征值不同，不相似。

**方法 4（用惯性指数判断合同）**

1. 读出两个实对称矩阵的 $p$、$q$：数特征值的正负个数，或者看任何一种标准形的系数符号；
2. $p$、$q$ 都相同就合同，否则不合同；
3. 判断相似要比特征值本身，判断等价只比秩。

**例 4**　在 $A_1=\begin{pmatrix}0&1\\1&0\end{pmatrix}$、$A_2=\begin{pmatrix}1&0\\0&-1\end{pmatrix}$、$A_3=\begin{pmatrix}2&0\\0&-3\end{pmatrix}$、$A_4=E$ 中，哪些相似，哪些合同？

$A_1$ 的特征值由 $t^2-1=0$ 得 $\pm1$，和 $A_2$ 相同。两者都实对称，都正交相似于同一个对角矩阵 $\operatorname{diag}(1,-1)$（L.13.3），所以相似。$A_3$ 的特征值 $2,-3$ 与它们不同，不相似；但 $p=q=1$，所以 $A_1,A_2,A_3$ 两两合同。$A_4$ 的 $p=2$，与前三个既不合同也不相似。四个矩阵秩都是 2，两两等价。

> 例 2 的二次型特征值为 $-1,2,5$，写出它的规范形和正、负惯性指数。
>
> 答案：$p=2$，$q=1$，规范形 $w_1^2+w_2^2-w_3^2$。

合上书，用「解一个齐次方程组」的办法说明正项个数为什么不随化法改变。

### 5. 什么样的二次型像一只开口朝上的碗？

开头的 $f=2x^2+4xy+5y^2$ 化成了 $y_1^2+6y_2^2$。只要 $(x,y)\ne(0,0)$，$\boldsymbol y=Q^{\mathsf T}\boldsymbol x$ 就不是零向量，$f>0$，曲面 $z=f(x,y)$ 是开口朝上的碗，最低点在原点。换成 $g=x^2+4xy+y^2$：在 $(1,0)$ 处 $g=1$，在 $(1,-1)$ 处 $g=-2$，它是马鞍面（C.20.1）。投影 ④ 的二次型 $\frac12(x+y)^2$ 又是第三种样子：沿 $(1,-1)^{\mathsf T}$ 方向一直是 0，像一道水槽。

![三种二次型的曲面和等高线：碗 $x^2+y^2$（等高线是圆，处处朝上）、马鞍 $x^2-y^2$（等高线是双曲线，一个方向朝上一个方向朝下）、槽 $x^2$（等高线是平行直线，沿 $y$ 方向是平的）](fig/L14-n4.pdf){width=85%}

设 $A$ 是实对称矩阵。如果对一切 $\boldsymbol x\ne\boldsymbol0$ 都有 $\boldsymbol x^{\mathsf T}A\boldsymbol x>0$，就说二次型 $f$ **正定**，$A$ 是**正定矩阵**；只要求 $\ge0$ 时叫**半正定**。$-f$ 正定时 $f$ **负定**；正值、负值都取得到时 $f$ **不定**。碗是正定，槽是半正定，马鞍是不定。条件 $\boldsymbol x\ne\boldsymbol0$ 不能少，因为任何二次型在 $\boldsymbol0$ 处都等于 0。

**定理**　实对称矩阵 $A$ 正定 $\iff$ $A$ 的特征值全为正。考试常要求写这个证明，两个方向都要能默写。

「$\Rightarrow$」的骨架：

1. 设 $\lambda$ 是 $A$ 的特征值，$\boldsymbol v\ne\boldsymbol0$ 是对应的实特征向量（L.13.1）。
2. $\boldsymbol v^{\mathsf T}A\boldsymbol v=\boldsymbol v^{\mathsf T}(\lambda\boldsymbol v)=\lambda\lVert\boldsymbol v\rVert^2$，这里 $\lVert\boldsymbol v\rVert$ 是向量的长度（高中写作 $|\boldsymbol v|$），$\boldsymbol v^{\mathsf T}\boldsymbol v=\lVert\boldsymbol v\rVert^2$。
3. 由正定，左边 $>0$；又 $\lVert\boldsymbol v\rVert^2>0$，所以 $\lambda>0$。

「$\Leftarrow$」的骨架：

1. 由谱定理，有正交矩阵 $Q$ 使 $Q^{\mathsf T}AQ=\Lambda$。
2. 任取 $\boldsymbol x\ne\boldsymbol0$，令 $\boldsymbol y=Q^{\mathsf T}\boldsymbol x$；$Q^{\mathsf T}$ 可逆，所以 $\boldsymbol y\ne\boldsymbol0$。
3. $\boldsymbol x^{\mathsf T}A\boldsymbol x=\boldsymbol y^{\mathsf T}\Lambda\boldsymbol y=\lambda_1y_1^2+\cdots+\lambda_ny_n^2$。
4. 每个 $\lambda_i>0$，$y_i$ 不全为 0，所以和 $>0$。

把 $>0$ 换成 $\ge0$，同样几步给出：$A$ 半正定 $\iff$ 特征值全 $\ge0$。

#### 正定的几种等价说法

由第 4 节还有几种等价说法：正定 $\iff$ $p=n$ $\iff$ $A$ 与 $E$ 合同 $\iff$ 存在可逆矩阵 $C$ 使 $A=C^{\mathsf T}C$。最后一条可以直接看出。一方面，$A=C^{\mathsf T}C$ 时 $\boldsymbol x^{\mathsf T}A\boldsymbol x=(C\boldsymbol x)^{\mathsf T}(C\boldsymbol x)=\lVert C\boldsymbol x\rVert^2$，$\boldsymbol x\ne\boldsymbol0$ 时 $C\boldsymbol x\ne\boldsymbol0$，所以 $>0$。另一方面，由 $A=Q\Lambda Q^{\mathsf T}$，取 $C=\operatorname{diag}(\sqrt{\lambda_1},\dots,\sqrt{\lambda_n})\,Q^{\mathsf T}$，乘出来就是 $A$。

于是可以把正定矩阵看成正数的推广：正数 $a$ 能写成 $c^2$（$c\ne0$），正定矩阵能写成 $C^{\mathsf T}C$（$C$ 可逆）；正数的「大于 0」对应 $\boldsymbol x^{\mathsf T}A\boldsymbol x>0$。这个类比到乘法就不灵了：两个正定矩阵的乘积连对称都不一定。

保持正定的运算有下面几种，每一条都可以用定义或特征值验证：

- $A$、$B$ 都正定时，$A+B$ 正定：$\boldsymbol x^{\mathsf T}(A+B)\boldsymbol x=\boldsymbol x^{\mathsf T}A\boldsymbol x+\boldsymbol x^{\mathsf T}B\boldsymbol x>0$；
- $k>0$ 时 $kA$ 正定；$C$ 可逆时 $C^{\mathsf T}AC$ 正定（$\boldsymbol x\ne\boldsymbol0$ 时 $C\boldsymbol x\ne\boldsymbol0$）；
- $A^{-1}$、$A^k$（$k$ 为正整数）和伴随矩阵 $A^*=|A|A^{-1}$（L.6.8）都正定，因为它们的特征值 $1/\lambda_i$、$\lambda_i^k$、$|A|/\lambda_i$ 仍为正（L.11.4）。

正定还给出两个快速的必要条件。记 $\boldsymbol e_i$ 为第 $i$ 个分量是 1、其余是 0 的向量（L.1.2）。$A\boldsymbol e_i$ 是 $A$ 的第 $i$ 列，再左乘 $\boldsymbol e_i^{\mathsf T}$ 取出它的第 $i$ 个分量，所以 $\boldsymbol e_i^{\mathsf T}A\boldsymbol e_i=a_{ii}$，正定时 $a_{ii}>0$。又 $|A|=\lambda_1\cdots\lambda_n>0$（L.11.3）。对角线上出现一个 $\le0$ 的数，立刻不正定。

#### 两类常见的半正定矩阵

任意 $m\times n$ 矩阵 $A$，$A^{\mathsf T}A$ 对称，并且

$$\boldsymbol x^{\mathsf T}A^{\mathsf T}A\boldsymbol x=\lVert A\boldsymbol x\rVert^2\ge0,$$

等号当且仅当 $A\boldsymbol x=\boldsymbol0$。$A$ 列满秩（秩 $r(A)=n$）时 $A\boldsymbol x=\boldsymbol0$ 只有零解，$A^{\mathsf T}A$ 正定，这就是 L.10.2 的正规方程在列满秩时有唯一解的原因。$A$ 是方阵时，这给可逆大定理添了一条：$A$ 可逆 $\iff$ $A^{\mathsf T}A$ 正定。另一类是 $\boldsymbol a\boldsymbol a^{\mathsf T}$：$\boldsymbol x^{\mathsf T}\boldsymbol a\boldsymbol a^{\mathsf T}\boldsymbol x=(\boldsymbol a^{\mathsf T}\boldsymbol x)^2\ge0$，半正定；$n\ge2$ 时它的秩不超过 1，有零特征值，不正定。

**方法 5（用定义或特征值证正定）**

1. 先说明 $A$ 对称；
2. 抽象矩阵：把 $\boldsymbol x^{\mathsf T}A\boldsymbol x$ 写成长度的平方，或几个正的、非负的式子之和；
3. $A$ 满足一个多项式关系时：用 L.11.4 求出特征值只能取哪些值，看是否全正。

**例 5**　设实对称矩阵 $A$ 满足 $A^2-3A+2E=O$（$O$ 是零矩阵），证明 $A$ 正定。

$A$ 已经对称，走第 3 步。设 $\lambda$ 是特征值，$A\boldsymbol v=\lambda\boldsymbol v$，$\boldsymbol v\ne\boldsymbol0$。由 L.11.4，

$$(A^2-3A+2E)\boldsymbol v=(\lambda^2-3\lambda+2)\boldsymbol v.$$

左边是 $O\boldsymbol v=\boldsymbol0$，而 $\boldsymbol v\ne\boldsymbol0$，所以 $\lambda^2-3\lambda+2=0$，$\lambda=1$ 或 2。特征值全为正，$A$ 正定。

> $n$ 阶实对称矩阵 $A$ 满足 $A^2=2A$ 且 $r(A)=n$，$A$ 正定吗？
>
> 答案：正定。特征值满足 $\lambda^2=2\lambda$，只能是 0 或 2；$r(A)=n$ 说明 $|A|\ne0$，而 $|A|$ 是特征值之积，所以没有 0，特征值全是 2（其实 $A=2E$）。

下一道例题不知道特征值，改走第 2 步。

**例 6**　设 $A$ 是 $m\times n$ 实矩阵，$k>0$，$E$ 是 $n$ 阶单位矩阵，证明 $kE+A^{\mathsf T}A$ 正定。

先说对称：$(kE+A^{\mathsf T}A)^{\mathsf T}=kE+A^{\mathsf T}A$。任取 $\boldsymbol x\ne\boldsymbol0$，

$$\boldsymbol x^{\mathsf T}(kE+A^{\mathsf T}A)\boldsymbol x=k\lVert\boldsymbol x\rVert^2+\lVert A\boldsymbol x\rVert^2>0,$$

第一项 $>0$，第二项 $\ge0$。$A$ 不必列满秩，加上 $kE$ 总能补成正定。

合上书，默写「正定 $\iff$ 特征值全正」两个方向的骨架。

### 6. 不求特征值，能判断正定吗？

$f=x_1^2+x_2^2+5x_3^2+2tx_1x_2-2x_1x_3+4x_2x_3$，$t$ 取什么值时正定？特征多项式里带着 $t$，三次方程解不出来。上一节的必要条件给了启发：取 $\boldsymbol x=\boldsymbol e_1$ 得到 $a_{11}>0$；只让前两个分量非零，能得到左上角 $2\times2$ 块的条件。

记 $A_k$ 为 $A$ 左上角的 $k$ 阶子矩阵，$D_k=|A_k|$ 叫 $A$ 的 $k$ 阶**顺序主子式**。

**定理（顺序主子式判别法）**　实对称矩阵 $A$ 正定 $\iff$ $D_1>0,\ D_2>0,\ \dots,\ D_n>0$。

必要性的骨架：

1. 任取非零的 $\boldsymbol z\in\mathbb R^k$，在后面补 $n-k$ 个 0，得到 $\boldsymbol x=(\boldsymbol z^{\mathsf T},\boldsymbol0^{\mathsf T})^{\mathsf T}\ne\boldsymbol0$。
2. 按分块乘法（L.3.7），$\boldsymbol x^{\mathsf T}A\boldsymbol x=\boldsymbol z^{\mathsf T}A_k\boldsymbol z$：补上的 0 把 $A$ 的其余部分都乘掉了。
3. 左边 $>0$，所以 $A_k$ 正定，特征值全正。
4. $D_k=|A_k|$ 是 $A_k$ 的特征值之积（L.11.3），所以 $D_k>0$。

充分性只讲思路，关键是看出「配方」和「消元」是同一件事。先在 L.4 的老朋友三阶好矩阵 ⑥ $\begin{pmatrix}2&1&0\\1&2&1\\0&1&2\end{pmatrix}$ 上看。它的二次型是

$$f=2x_1^2+2x_2^2+2x_3^2+2x_1x_2+2x_2x_3.$$

配方：先收拾 $x_1$，再收拾 $x_2$，

$$f=2\Big(x_1+\tfrac12x_2\Big)^2+\tfrac32x_2^2+2x_2x_3+2x_3^2=2\Big(x_1+\tfrac12x_2\Big)^2+\tfrac32\Big(x_2+\tfrac23x_3\Big)^2+\tfrac43x_3^2.$$

再对 ⑥ 做消元，只用「上面某行的倍数加到下面」：第 2 行减去第 1 行的 $\frac12$ 倍，第 3 行减去新第 2 行的 $\frac23$ 倍，

$$\begin{pmatrix}2&1&0\\1&2&1\\0&1&2\end{pmatrix}\to\begin{pmatrix}2&1&0\\0&\frac32&1\\0&1&2\end{pmatrix}\to\begin{pmatrix}2&1&0\\0&\frac32&1\\0&0&\frac43\end{pmatrix}.$$

主元 $2,\frac32,\frac43$ 正是配方得到的三个系数，用的倍数 $\frac12$、$\frac23$ 也正是配方括号里的系数。这不是巧合：配方收拾 $x_1$ 时，剩下的二次型的矩阵第 $(i,j)$ 个元素是 $a_{ij}-\frac{a_{i1}a_{1j}}{a_{11}}$；消元时把第 1 行的 $\frac{a_{i1}}{a_{11}}$ 倍从第 $i$ 行减去，第 $(i,j)$ 个位置得到的也是这个数。

主元又和顺序主子式挂钩。倍加变换不改变行列式（L.6.2），而且左上角每个 $k$ 阶块里做的也只是倍加，所以 $D_k$ 等于消完后左上角块的行列式，即前 $k$ 个主元之积：

$$D_1=2,\qquad D_2=2\cdot\tfrac32=3,\qquad D_3=2\cdot\tfrac32\cdot\tfrac43=4.$$

这正是 ⑥ 档案里的 2、3、4，第 $k$ 个主元 $d_k=D_k/D_{k-1}$（$D_0=1$）。

一般情形对变量个数归纳：设 $n-1$ 元时「顺序主子式全正 $\Rightarrow$ 正定」已成立。

1. $D_1=a_{11}>0$，先收拾 $x_1$：$f=a_{11}(x_1+\cdots)^2+g$，$g$ 只含 $x_2,\dots,x_n$，它的矩阵 $S$ 的元素就是上面的 $a_{ij}-\frac{a_{i1}a_{1j}}{a_{11}}$。
2. 对 $A$ 做同样的消元。倍加不改变行列式，左上角 $k+1$ 阶块里做的也只是倍加，所以消元后这个块的行列式仍是 $D_{k+1}$；它的形状是 $\begin{pmatrix}a_{11}&*\\\boldsymbol0&S_k\end{pmatrix}$（$S_k$ 是 $S$ 左上角的 $k$ 阶块），按第一列展开得 $D_{k+1}=a_{11}|S_k|$。所以 $S$ 的顺序主子式 $D_2/D_1,\dots,D_n/D_1$ 全正。
3. 由归纳假设，$g$ 正定。$\boldsymbol x\ne\boldsymbol0$ 时，若 $x_2,\dots,x_n$ 不全为 0，则 $g>0$；若全为 0，则 $x_1\ne0$，第一项 $a_{11}x_1^2>0$。两种情况都有 $f>0$。

二元时看得最清楚：

$$ax^2+2bxy+cy^2=a\Big(x+\frac bay\Big)^2+\frac{ac-b^2}{a}\,y^2,$$

两个系数是 $D_1=a$ 和 $D_2/D_1=(ac-b^2)/a$。

负定的判别由此得到：$A$ 负定 $\iff$ $-A$ 正定 $\iff$ $|-A_k|=(-1)^kD_k>0$，即奇数阶顺序主子式 $<0$、偶数阶 $>0$。

把「$>0$」改成「$\ge0$」，判别法对半正定就不成立了。$A=\begin{pmatrix}0&0\\0&-1\end{pmatrix}$ 的 $D_1=0$、$D_2=0$，都 $\ge0$，可是 $\boldsymbol e_2^{\mathsf T}A\boldsymbol e_2=-1<0$。毛病出在 $D_1=0$：第一个主元是 0，配方配不下去，左上角根本看不到右下角的 $-1$。判断半正定要用特征值。

**方法 6（顺序主子式）**

1. 写出 $A$，依次算 $D_1,D_2,\dots,D_n$；
2. 全正就正定；负、正交替（$D_1<0$ 开始）就负定；
3. 带参数时，把各个不等式的解取交集；
4. 不能用来判断半正定。

**例 7**　上面的 $f$，$t$ 取何值时正定？

按方法 1，$2tx_1x_2$ 对半分，$-2x_1x_3$、$4x_2x_3$ 同样：

$$A=\begin{pmatrix}1&t&-1\\t&1&2\\-1&2&5\end{pmatrix}.$$

$D_1=1>0$。$D_2=1-t^2>0$ 给出 $-1<t<1$。$D_3$ 按第一行展开，三个二阶余子式分别是 $5-4$、$5t+2$、$2t+1$：

$$D_3=1\cdot(5-4)-t\,(5t+2)+(-1)(2t+1)=-5t^2-4t=-t(5t+4).$$

$D_3>0$ 即 $t(5t+4)<0$，$-\frac45<t<0$。与 $D_2$ 的条件取交集，得 $-\frac45<t<0$。

> $g=2x_1^2+x_2^2+x_3^2+2x_1x_2+tx_2x_3$，$t$ 取何值时正定？
>
> 答案：交叉项 $tx_2x_3$ 分成两个 $\frac t2$，$A=\begin{pmatrix}2&1&0\\1&1&t/2\\0&t/2&1\end{pmatrix}$，$D_1=2$，$D_2=1$，$D_3=2\big(1-\frac{t^2}4\big)-1=1-\frac{t^2}2>0$，所以 $-\sqrt2<t<\sqrt2$。

**例 8**　判断 $f=-5x_1^2-6x_2^2-4x_3^2+4x_1x_2+4x_1x_3$ 是否正定或负定。

和例 7 不同，对角线全是负数，正定已经不可能，要查的是负定。$A=\begin{pmatrix}-5&2&2\\2&-6&0\\2&0&-4\end{pmatrix}$，

$$D_1=-5<0,\qquad D_2=30-4=26>0,\qquad D_3=-5\cdot24-2\cdot(-8)+2\cdot12=-80<0.$$

符号负、正、负交替，$f$ 负定。

合上书，写出必要性的四步，用 ⑥ 说明主元和顺序主子式的关系，再举出「顺序主子式都非负却不半正定」的例子。

### 7. 二次型在单位球面上最大、最小能到多少？

$f=2x^2+4xy+5y^2$ 在单位圆 $x^2+y^2=1$ 上最大是多少、最小是多少？C.24.7 的拉格朗日乘数法能做，换到主轴坐标更快。$\boldsymbol x=Q\boldsymbol y$ 保长度，所以 $y_1^2+y_2^2=x^2+y^2=1$，而

$$f=y_1^2+6y_2^2=1+5y_2^2.$$

$y_2^2$ 在 $[0,1]$ 里变，$f$ 就在 $[1,6]$ 里变：最小值 1 在 $\pm\boldsymbol q_1$ 取到，最大值 6 在 $\pm\boldsymbol q_2$ 取到，恰好是最小、最大特征值和对应的单位特征向量。

![单位圆（实线）夹在椭圆 $f=1$（点线）与 $f=6$（虚线）之间，分别在 $\pm\boldsymbol q_1$、$\pm\boldsymbol q_2$ 处相切](fig/L14-n2.pdf){width=55%}

一般地，对 $\boldsymbol x\ne\boldsymbol0$，比值

$$R(\boldsymbol x)=\frac{\boldsymbol x^{\mathsf T}A\boldsymbol x}{\boldsymbol x^{\mathsf T}\boldsymbol x}$$

叫**瑞利商**。分子、分母都是二次的，$R(k\boldsymbol x)=R(\boldsymbol x)$，所以 $R$ 在单位球面上的取值就是它的全部取值。

**定理**　$A$ 为实对称矩阵时，$\lambda_{\min}\le R(\boldsymbol x)\le\lambda_{\max}$，在对应的特征向量处取等号。

证明：令 $\boldsymbol x=Q\boldsymbol y$，则 $\boldsymbol x^{\mathsf T}\boldsymbol x=\boldsymbol y^{\mathsf T}Q^{\mathsf T}Q\boldsymbol y=\boldsymbol y^{\mathsf T}\boldsymbol y$，而

$$\boldsymbol x^{\mathsf T}A\boldsymbol x=\sum_i\lambda_iy_i^2\le\lambda_{\max}\sum_iy_i^2=\lambda_{\max}\,\boldsymbol x^{\mathsf T}\boldsymbol x.$$

不等号是把每个 $\lambda_i$ 放大成 $\lambda_{\max}$，$y_i^2\ge0$ 保证不等号方向不变。下界同理。取 $\boldsymbol x$ 为 $\lambda_{\max}$ 的特征向量，$\boldsymbol x^{\mathsf T}A\boldsymbol x=\lambda_{\max}\boldsymbol x^{\mathsf T}\boldsymbol x$，等号成立。

常用的写法是 $\lambda_{\min}\lVert\boldsymbol x\rVert^2\le\boldsymbol x^{\mathsf T}A\boldsymbol x\le\lambda_{\max}\lVert\boldsymbol x\rVert^2$。$A$ 正定时，两端之比 $\kappa=\lambda_{\max}/\lambda_{\min}$ 叫 $A$ 的**条件数**，它量的是碗有多扁：等高线 $f=c$ 在主轴方向的半轴是 $\sqrt{c/\lambda_i}$，最长与最短半轴之比是 $\sqrt\kappa$。$\kappa=1$ 时等高线是圆；$\kappa$ 很大时等高线又细又长，碗成了一道窄长的山谷。

**方法 7（瑞利商求球面上的最值）**

$A$ 实对称时，$\boldsymbol x^{\mathsf T}A\boldsymbol x$ 在球面 $\lVert\boldsymbol x\rVert=r$ 上：

1. 求出 $\lambda_{\max}$、$\lambda_{\min}$ 和对应的单位特征向量；
2. 最大值是 $\lambda_{\max}r^2$，最小值是 $\lambda_{\min}r^2$；
3. 取到的点是对应单位特征向量乘 $\pm r$。

**例 9**　求 $f=x_1^2+2x_2^2+3x_3^2-4x_1x_2-4x_2x_3$ 在球面 $x_1^2+x_2^2+x_3^2=4$ 上的最大值、最小值，以及取到的点。

例 2 已经求出特征值 $-1,2,5$ 和单位特征向量。球面上 $\lVert\boldsymbol x\rVert^2=4$，所以 $-4\le f\le20$。最大值 20 在 $\boldsymbol x=\pm\frac23(1,-2,2)^{\mathsf T}$ 取到，最小值 $-4$ 在 $\boldsymbol x=\pm\frac23(2,2,1)^{\mathsf T}$ 取到。注意半径是 2：最值乘的是 $r^2=4$，单位特征向量乘的是 $r=2$。

> 求 $3x^2+2xy+3y^2$ 在单位圆上的最大值和取到的点。
>
> 答案：特征值 2、4（第 2 节小题），最大值 4，在 $\pm\frac1{\sqrt2}(1,1)^{\mathsf T}$ 取到。

合上书，用主轴坐标证明 $R(\boldsymbol x)\le\lambda_{\max}$，并说出条件数和等高线形状的关系。

### 8. n 元函数的一阶、二阶导数怎样写成向量和矩阵？

二元函数的梯度 $\nabla f=(f_x,f_y)^{\mathsf T}$（C.22.3）和二阶泰勒公式里由二阶偏导排成的数表（C.24.2）已经出现过，下面推广到 $n$ 元。

设 $f(\boldsymbol x)=f(x_1,\dots,x_n)$，定义

$$\nabla f=\Big(\frac{\partial f}{\partial x_1},\dots,\frac{\partial f}{\partial x_n}\Big)^{\mathsf T},\qquad H=\Big(\frac{\partial^2f}{\partial x_i\,\partial x_j}\Big)_{n\times n},$$

分别叫**梯度**和 **Hessian 矩阵**（黑塞矩阵）。二阶偏导数连续时，混合偏导数与求导次序无关（C.20.8），$H$ 是对称矩阵。

**泰勒公式**　固定点 $\boldsymbol x$ 和方向 $\boldsymbol h$，像 C.24.2 那样沿直线看一元函数 $\varphi(t)=f(\boldsymbol x+t\boldsymbol h)$。由链式法则（C.21.2），

$$\varphi'(t)=\sum_i\frac{\partial f}{\partial x_i}(\boldsymbol x+t\boldsymbol h)\,h_i=\nabla f(\boldsymbol x+t\boldsymbol h)^{\mathsf T}\boldsymbol h.$$

对每个 $\frac{\partial f}{\partial x_i}(\boldsymbol x+t\boldsymbol h)$ 再用一次链式法则，

$$\varphi''(t)=\sum_i\sum_j\frac{\partial^2f}{\partial x_i\,\partial x_j}(\boldsymbol x+t\boldsymbol h)\,h_ih_j=\boldsymbol h^{\mathsf T}H(\boldsymbol x+t\boldsymbol h)\,\boldsymbol h,$$

最后一个等号就是第 1 节的 $\sum\sum a_{ij}x_ix_j=\boldsymbol x^{\mathsf T}A\boldsymbol x$。对 $\varphi$ 在 $[0,1]$ 上用带拉格朗日余项的泰勒公式（C.7.6），$\varphi(1)=\varphi(0)+\varphi'(0)+\frac12\varphi''(\theta)$，$0<\theta<1$，换回 $f$：

$$f(\boldsymbol x+\boldsymbol h)=f(\boldsymbol x)+\nabla f(\boldsymbol x)^{\mathsf T}\boldsymbol h+\tfrac12\,\boldsymbol h^{\mathsf T}H(\boldsymbol x+\theta\boldsymbol h)\,\boldsymbol h.$$

**两个常用梯度**，逐个分量求偏导就能得到。

第一个，$\boldsymbol a^{\mathsf T}\boldsymbol x=\sum_ia_ix_i$ 对 $x_k$ 求偏导只剩 $a_k$，所以 $\nabla(\boldsymbol a^{\mathsf T}\boldsymbol x)=\boldsymbol a$。

第二个，$\boldsymbol x^{\mathsf T}A\boldsymbol x=\sum_i\sum_ja_{ij}x_ix_j$ 对 $x_k$ 求偏导。按乘积法则，每一项 $a_{ij}x_ix_j$ 的贡献分两种：

- 第一个因子是 $x_k$（$i=k$）时，贡献 $a_{kj}x_j$，对 $j$ 求和得 $\sum_ja_{kj}x_j$；
- 第二个因子是 $x_k$（$j=k$）时，贡献 $a_{ik}x_i$，对 $i$ 求和得 $\sum_ia_{ik}x_i$。

$i=j=k$ 的那一项两种都算一次，合起来正是 $a_{kk}x_k^2$ 的导数 $2a_{kk}x_k$。所以

$$\frac{\partial}{\partial x_k}\big(\boldsymbol x^{\mathsf T}A\boldsymbol x\big)=\sum_ja_{kj}x_j+\sum_ia_{ik}x_i=(A\boldsymbol x)_k+(A^{\mathsf T}\boldsymbol x)_k,\qquad \nabla(\boldsymbol x^{\mathsf T}A\boldsymbol x)=(A+A^{\mathsf T})\boldsymbol x.$$

$A$ 对称时是 $2A\boldsymbol x$，可以和一元的 $(ax^2)'=2ax$ 对照着记；不对称时是 $A+A^{\mathsf T}$，不要套 $2A$。再对 $(A+A^{\mathsf T})\boldsymbol x$ 求一次偏导，得 $\boldsymbol x^{\mathsf T}A\boldsymbol x$ 的 Hessian 是 $A+A^{\mathsf T}$，$A$ 对称时就是 $2A$。所以对称矩阵 $A$ 的二次函数

$$q(\boldsymbol x)=\tfrac12\boldsymbol x^{\mathsf T}A\boldsymbol x-\boldsymbol b^{\mathsf T}\boldsymbol x$$

的梯度是 $A\boldsymbol x-\boldsymbol b$，Hessian 是 $A$，前面的 $\frac12$ 就是为了约掉求导出来的 2。驻点满足 $A\boldsymbol x=\boldsymbol b$：求二次函数的驻点就是解线性方程组。

**方法 8（用矩阵形式求梯度）**

1. 把函数展开成 $\boldsymbol x^{\mathsf T}M\boldsymbol x$、$\boldsymbol c^{\mathsf T}\boldsymbol x$ 和常数之和；$\boldsymbol x^{\mathsf T}\boldsymbol c$ 与 $\boldsymbol c^{\mathsf T}\boldsymbol x$ 是同一个数，可以合并；
2. 用 $\nabla(\boldsymbol c^{\mathsf T}\boldsymbol x)=\boldsymbol c$、$\nabla(\boldsymbol x^{\mathsf T}M\boldsymbol x)=(M+M^{\mathsf T})\boldsymbol x$；
3. Hessian 是 $M+M^{\mathsf T}$。

**例 10**　设 $A$ 是 $m\times n$ 矩阵，$\boldsymbol b\in\mathbb R^m$。求 $F(\boldsymbol x)=\lVert A\boldsymbol x-\boldsymbol b\rVert^2$ 的梯度和 Hessian，以及驻点满足的方程。

长度的平方是向量和自己的点积，展开成方法 8 的三种项：

$$F=(A\boldsymbol x-\boldsymbol b)^{\mathsf T}(A\boldsymbol x-\boldsymbol b)=\boldsymbol x^{\mathsf T}A^{\mathsf T}A\boldsymbol x-\boldsymbol x^{\mathsf T}A^{\mathsf T}\boldsymbol b-\boldsymbol b^{\mathsf T}A\boldsymbol x+\boldsymbol b^{\mathsf T}\boldsymbol b.$$

中间两项是同一个数（$(\boldsymbol x^{\mathsf T}A^{\mathsf T}\boldsymbol b)^{\mathsf T}=\boldsymbol b^{\mathsf T}A\boldsymbol x$），合并成 $-2(A^{\mathsf T}\boldsymbol b)^{\mathsf T}\boldsymbol x$。$A^{\mathsf T}A$ 对称，于是

$$\nabla F=2A^{\mathsf T}A\boldsymbol x-2A^{\mathsf T}\boldsymbol b=2A^{\mathsf T}(A\boldsymbol x-\boldsymbol b),\qquad H=2A^{\mathsf T}A.$$

驻点满足 $A^{\mathsf T}A\boldsymbol x=A^{\mathsf T}\boldsymbol b$，这正是 L.10.2 用投影推出的正规方程。$H=2A^{\mathsf T}A$ 半正定，$A$ 列满秩时正定（第 5 节），下一节说明这保证驻点是最小值点。

> 设 $B=\begin{pmatrix}1&2\\0&3\end{pmatrix}$，求 $g(\boldsymbol x)=\boldsymbol x^{\mathsf T}B\boldsymbol x$ 的梯度，并展开核对。
>
> 答案：$(B+B^{\mathsf T})\boldsymbol x=\begin{pmatrix}2&2\\2&6\end{pmatrix}\boldsymbol x=(2x_1+2x_2,\ 2x_1+6x_2)^{\mathsf T}$。展开 $g=x_1^2+2x_1x_2+3x_2^2$，直接求偏导结果相同；误用 $2B\boldsymbol x$ 会得到 $(2x_1+4x_2,\ 6x_2)^{\mathsf T}$。

合上书，用逐个分量求偏导的办法推出 $\nabla(\boldsymbol x^{\mathsf T}A\boldsymbol x)=(A+A^{\mathsf T})\boldsymbol x$。

### 9. n 元函数的驻点是极大、极小还是鞍点？

在驻点 $\boldsymbol x_0$，$\nabla f(\boldsymbol x_0)=\boldsymbol0$，泰勒公式的一次项消失：

$$f(\boldsymbol x_0+\boldsymbol h)-f(\boldsymbol x_0)=\tfrac12\,\boldsymbol h^{\mathsf T}H(\boldsymbol x_0+\theta\boldsymbol h)\,\boldsymbol h.$$

函数值比 $f(\boldsymbol x_0)$ 大还是小，就看这个二次型的符号：驻点附近的曲面，就是第 5 节的碗、马鞍或槽。

设 $f$ 的二阶偏导数连续，$\nabla f(\boldsymbol x_0)=\boldsymbol0$，$H(\boldsymbol x_0)$ 正定。右边的矩阵却是 $H(\boldsymbol x_0+\theta\boldsymbol h)$，它为什么也正定？用第 6 节：$H(\boldsymbol x_0)$ 的各阶顺序主子式都 $>0$，它们是二阶偏导数的多项式，随点连续变化，所以在 $\boldsymbol x_0$ 附近仍然 $>0$。于是 $\lVert\boldsymbol h\rVert$ 足够小时 $H(\boldsymbol x_0+\theta\boldsymbol h)$ 正定，$\boldsymbol h\ne\boldsymbol0$ 时右边 $>0$，$\boldsymbol x_0$ 是严格极小值点。负定时同理是严格极大值点。

$H(\boldsymbol x_0)$ 不定时，取一个使 $\boldsymbol h^{\mathsf T}H(\boldsymbol x_0)\boldsymbol h>0$ 的方向，沿它看 $\varphi(t)=f(\boldsymbol x_0+t\boldsymbol h)$：$\varphi'(0)=\nabla f(\boldsymbol x_0)^{\mathsf T}\boldsymbol h=0$，$\varphi''(0)=\boldsymbol h^{\mathsf T}H(\boldsymbol x_0)\boldsymbol h>0$，由一元的第二充分条件（C.8.2），沿这个方向函数往两边上升；沿使二次型 $<0$ 的方向同理下降。有升有降，$\boldsymbol x_0$ 不是极值点，叫**鞍点**。

$H(\boldsymbol x_0)$ 半正定而不正定（有零特征值）时，二次项在某些方向上是 0，要看更高阶的项，这个办法判断不了。$x^4+y^2$ 和 $x^3+y^2$ 在原点的 Hessian 都是 $\operatorname{diag}(0,2)$，前者原点是极小值点，后者沿 $x$ 轴有正有负，不是极值点。二元时 $H$ 正定 $\iff$ $f_{xx}>0$ 且 $f_{xx}f_{yy}-f_{xy}^2>0$，正是 C.24.3 的判别法。

**方法 9（用 Hessian 判别极值）**

1. 解 $\nabla f=\boldsymbol0$，求出全部驻点；
2. 在每个驻点算 $H$；
3. 正定是极小，负定是极大（用方法 6）；
4. 顺序主子式既不全正也不负正交替时，$H$ 可能不定也可能半定：直接找一个使 $\boldsymbol h^{\mathsf T}H\boldsymbol h>0$ 和一个使它 $<0$ 的方向，找到就是鞍点；
5. 半定而奇异时此法失效。

**例 11**　求 $f(x,y,z)=x^3+y^2+z^2+12xy+2z$ 的极值。

第一步，令 $f_x=3x^2+12y=0$，$f_y=2y+12x=0$，$f_z=2z+2=0$。由第三式 $z=-1$，由第二式 $y=-6x$，代入第一式得 $3x^2-72x=0$，$x=0$ 或 24。驻点是 $P_1(0,0,-1)$ 和 $P_2(24,-144,-1)$。

第二步，

$$H=\begin{pmatrix}6x&12&0\\12&2&0\\0&0&2\end{pmatrix}.$$

第三步，在 $P_2$，$D_1=144$，$D_2=288-144=144$，$D_3=2D_2=288$，都正，$P_2$ 是极小值点，极小值 $f(P_2)=24^3+144^2+1+12\cdot24\cdot(-144)-2=-6913$。

第四步，在 $P_1$，$D_1=0$，不满足正定要的 $D_1>0$，也不满足负定要的 $D_1<0$。可这只说明不是正定或负定，还没排除半定，所以要直接找两个方向。取 $\boldsymbol h=(1,-1,0)^{\mathsf T}$，$\boldsymbol h^{\mathsf T}H\boldsymbol h=0-24+2=-22<0$；取 $\boldsymbol h=\boldsymbol e_3$，得 $2>0$。$H$ 不定，$P_1$ 是鞍点。

> 求 $g(x,y,z)=x^2+2y^2+z^3-2xy-3z$ 的极值。
>
> 答案：由 $g_x=2x-2y=0$、$g_y=4y-2x=0$ 得 $x=y=0$，由 $g_z=3z^2-3=0$ 得 $z=\pm1$。$H=\begin{pmatrix}2&-2&0\\-2&4&0\\0&0&6z\end{pmatrix}$，$D_1=2$，$D_2=4$，$D_3=24z$。$z=1$ 时正定，极小值 $g(0,0,1)=-2$；$z=-1$ 时 $\boldsymbol e_1$ 方向给出 $2>0$、$\boldsymbol e_3$ 方向给出 $-6<0$，是鞍点。

最后看模型训练。训练就是调整参数，让损失函数尽量小；把全部参数排成向量 $\boldsymbol w$。梯度下降每一步把参数沿负梯度方向挪一点（C.22.5）：$\boldsymbol w\leftarrow\boldsymbol w-\eta\nabla L(\boldsymbol w)$，$\eta>0$ 叫学习率。由泰勒公式，最小值点附近的损失近似于一个二次型。下面手算一个二元的例子。

**例 12**　一个有两个参数的模型，把最小值点平移到原点、减去最小值后，损失在附近是

$$L(\boldsymbol w)=\tfrac12\boldsymbol w^{\mathsf T}H\boldsymbol w,\qquad H=\begin{pmatrix}5.5&4.5\\4.5&5.5\end{pmatrix}.$$

(1) 说明原点是极小值点，求条件数；(2) 从 $\boldsymbol w_0=(2,0)^{\mathsf T}$ 出发，取 $\eta=0.18$ 走两步，并解释轨迹；(3) $\eta$ 最大能取多少才不发散？

(1) $H$ 的迹是 11，行列式是 $5.5^2-4.5^2=10$，特征值是 10 和 1，单位特征向量 $\boldsymbol q_1=\frac1{\sqrt2}(1,1)^{\mathsf T}$、$\boldsymbol q_2=\frac1{\sqrt2}(1,-1)^{\mathsf T}$。$H$ 正定，原点是极小值点。条件数 $\kappa=10$，等高线是长短半轴之比 $\sqrt{10}\approx3.2$ 的椭圆：沿 $\boldsymbol q_1$ 陡，沿 $\boldsymbol q_2$ 平。

(2) 由第 8 节，$\nabla L=H\boldsymbol w$，一步更新是 $\boldsymbol w\leftarrow(E-\eta H)\boldsymbol w$。

$$H\boldsymbol w_0=(11,9)^{\mathsf T},\qquad \boldsymbol w_1=(2,0)^{\mathsf T}-0.18\,(11,9)^{\mathsf T}=(0.02,-1.62)^{\mathsf T}.$$

第二步同样代公式：

$$H\boldsymbol w_1=(5.5\cdot0.02-4.5\cdot1.62,\ 4.5\cdot0.02-5.5\cdot1.62)^{\mathsf T}=(-7.18,-8.82)^{\mathsf T},$$

$$\boldsymbol w_2=\boldsymbol w_1-0.18\,H\boldsymbol w_1=(0.02+1.2924,\ -1.62+1.5876)^{\mathsf T}=(1.3124,-0.0324)^{\mathsf T}.$$

轨迹在山谷两壁之间来回跳。为了看清原因，换到主轴坐标 $\boldsymbol y=Q^{\mathsf T}\boldsymbol w$：

$$\boldsymbol y_{k+1}=Q^{\mathsf T}(E-\eta H)Q\,\boldsymbol y_k=(E-\eta\Lambda)\,\boldsymbol y_k,$$

也就是 $y_1\leftarrow(1-10\eta)y_1=-0.8\,y_1$，$y_2\leftarrow(1-\eta)y_2=0.82\,y_2$。陡的方向每步乘 $-0.8$，符号来回变，所以在两壁之间弹；平的方向每步只缩小 18%，10 步后还剩 $0.82^{10}\approx0.14$。

![等高线是以虚线为主轴的椭圆；梯度下降沿陡的 $\boldsymbol q_1$ 方向来回跳，沿平的 $\boldsymbol q_2$ 方向慢慢靠近原点](fig/L14-n3.pdf){width=58%}

(3) 两个方向都要收缩，需要 $|1-10\eta|<1$ 且 $|1-\eta|<1$，即 $0<\eta<0.2=2/\lambda_{\max}$。学习率被陡的方向卡住，平的方向每步的倍数 $1-\eta\lambda_{\min}$ 就大于 $1-2\lambda_{\min}/\lambda_{\max}=1-2/\kappa=0.8$。条件数越大，梯度下降越慢（M.1.3 接着讲）。

合上书，说明 Hessian 正定的驻点为什么是极小值点，以及条件数大为什么让梯度下降变慢。

### 本章小结

| 方法 | 什么时候用 | 对应题号 |
|---|---|---|
| 方法 1（写出二次型的矩阵） | 由式子写对称矩阵、求二次型的秩；给的矩阵不对称时 | L14-01、L14-14 |
| 方法 2（正交变换化标准形） | 要求正交变换、主轴方向、判断二次曲面类型 | L14-02、L14-10 |
| 方法 3（配方法） | 只要可逆换元、特征值难求时 | L14-03 |
| 方法 4（用惯性指数判断合同） | 判断合同、相似、等价；求规范形 | L14-09 |
| 方法 5（用定义或特征值证正定） | 抽象矩阵、$A^{\mathsf T}A$ 型、满足多项式关系的矩阵 | L14-04、L14-05 |
| 方法 6（顺序主子式） | 带参数判断正定、负定 | L14-06 |
| 方法 7（瑞利商求球面上的最值） | 二次型在球面上的最值、条件数 | L14-07、L14-10、L14-12 |
| 方法 8（用矩阵形式求梯度） | $\boldsymbol a^{\mathsf T}\boldsymbol x$、$\boldsymbol x^{\mathsf T}A\boldsymbol x$、$\lVert A\boldsymbol x-\boldsymbol b\rVert^2$ 的梯度和 Hessian | L14-08、L14-13、L14-14 |
| 方法 9（用 Hessian 判别极值） | $n$ 元函数的驻点分类 | L14-11、L14-12、L14-13、L14-15 |

可逆大定理：$n$ 阶方阵 $A$ 可逆，等价于下面每一条。

| 条件 | 出处 |
|---|---|
| 消元后有 $n$ 个主元；$A\boldsymbol x=\boldsymbol0$ 只有零解；$A\boldsymbol x=\boldsymbol b$ 对每个 $\boldsymbol b$ 有唯一解 | L.4 |
| 存在 $B$ 使 $AB=E$ | L.5 |
| $\lvert A\rvert\ne0$ | L.6 |
| 列（行）向量组线性无关；$r(A)=n$ | L.7 |
| 列向量构成 $\mathbb R^n$ 的基；零空间只有零向量 | L.8 |
| 0 不是 $A$ 的特征值 | L.11 |
| $A^{\mathsf T}A$ 正定（本章新增） | L.14 |
