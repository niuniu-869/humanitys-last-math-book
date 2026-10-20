## L.15 · 奇异值分解

一张 $1000\times1000$ 像素的灰度照片就是一张数表，存下来要一百万个数。本章会把任何一张数表拆成一层一层的「一列乘一行」，并按重要程度排好队。只留最重要的 50 层，大约十万个数，照片往往看不出多大差别。做这种分层的工具叫奇异值分解。

L.13 的正交对角化只对对称矩阵有效，可大多数矩阵不对称，甚至不是方阵。1873 年，贝尔特拉米研究双线性型 $\boldsymbol x^{\mathsf T}A\boldsymbol y$，它两边是不同的变量，可以各做各的正交换元。他发现分别转动 $\boldsymbol x$、$\boldsymbol y$ 的坐标轴，总能化成只剩 $\sigma_1\xi_1\eta_1+\sigma_2\xi_2\eta_2+\cdots$，而且 $A$ 不必对称。第二年若尔当独立得到同样的结果。1936 年，埃卡特和扬在一篇心理测量学的论文里回答了另一个问题：用一张「简单」的表近似一张大数表，怎样误差最小？答案是按奇异值从大到小截断。

本章的顺序：几何（第 1 节）、算法（第 2 节）、外积展开（第 3 节）、伪逆（第 4 节）、截断（第 5 节）、主成分（第 6 节）。

### 1. 任意一个矩阵，能不能找到「垂直进、垂直出」的方向？

先拿老朋友②剪切 $\begin{pmatrix}1&1\\0&1\end{pmatrix}$ 试一试。它只有一条特征方向 $(1,0)^{\mathsf T}$，不能对角化，「只伸缩、不转向的方向」这条路走不通。

但它把单位圆变成什么是看得见的：点 $(\cos t,\sin t)^{\mathsf T}$ 被送到 $(\cos t+\sin t,\ \sin t)^{\mathsf T}$，画出来是一个斜放的椭圆（图 L15-n3 最右一幅），长轴和短轴互相垂直。

长轴端点是单位圆上某个点 $\boldsymbol v_1$ 的像，短轴端点是另一个点 $\boldsymbol v_2$ 的像。第 2 节会说明：$\boldsymbol v_1$ 和 $\boldsymbol v_2$ 也互相垂直。两个像的长度是 $\frac{\sqrt5+1}2\approx1.618$ 和 $\frac{\sqrt5-1}2\approx0.618$，例 2 后的小题会把它们算出来。

所以放宽要求，只要求**垂直进、垂直出**：互相垂直的输入方向，像仍然垂直。第 2 节会证明，任何矩阵都做得到。

#### 把它写成矩阵等式

设 $A$ 是 $m\times n$ 实矩阵，$\mathbb R^n$ 中两两垂直的单位向量 $\boldsymbol v_1,\dots,\boldsymbol v_n$ 使 $A\boldsymbol v_1,\dots,A\boldsymbol v_n$ 也两两垂直。把 $A\boldsymbol v_i$ 的长度记作 $\sigma_i$，编号时从大到小排。设前 $r$ 个大于 0，其余为 0，对前 $r$ 个把 $A\boldsymbol v_i$ 的方向记作单位向量 $\boldsymbol u_i$：

$$A\boldsymbol v_i=\sigma_i\boldsymbol u_i\quad(i\le r),\qquad A\boldsymbol v_i=\boldsymbol 0\quad(i>r).$$

下面分三步把这 $n$ 个等式拼成一个矩阵等式。

第一步，拼 $V$。把 $\boldsymbol v_1,\dots,\boldsymbol v_n$ 排成 $n$ 阶方阵 $V$ 的各列，它是正交矩阵（L.10.4），$VV^{\mathsf T}=E$。按列分块（L.3.7），$AV$ 的第 $i$ 列是 $A\boldsymbol v_i$。

第二步，拼 $U$。$\boldsymbol u_1,\dots,\boldsymbol u_r$ 两两垂直，而 $\mathbb R^m$ 里至多有 $m$ 个两两垂直的非零向量，所以 $r\le m$。$r<m$ 时再补 $m-r$ 个单位向量 $\boldsymbol u_{r+1},\dots,\boldsymbol u_m$，让全部两两垂直，排成 $m$ 阶正交矩阵 $U$。总能补出来：设 $\boldsymbol y\in\mathbb R^m$，与 $\boldsymbol u_i$ 垂直就是线性方程 $\boldsymbol u_i^{\mathsf T}\boldsymbol y=0$；这 $r$ 个方程的系数行线性无关，解空间是 $m-r$ 维的（L.8.4），把它的一组基施密特正交化（L.10.5）即可。

第三步，拼 $\Sigma$。$\Sigma$ 和 $A$ 同为 $m\times n$，对角位置 $(1,1),(2,2),\dots$ 一直到第 $\min(m,n)$ 个，依次放 $\sigma_1,\sigma_2,\dots$，其余全是 0（例 3 有 $3\times2$ 的例子）。于是 $U\Sigma$ 的第 $i$ 列是 $\sigma_i\boldsymbol u_i$，$\sigma_i=0$ 时是 $\boldsymbol 0$。

逐列比较，$AV$ 与 $U\Sigma$ 每一列都相同，所以 $AV=U\Sigma$。两边右乘 $V^{\mathsf T}$：

$$A=U\Sigma V^{\mathsf T}.$$

这叫 $A$ 的**奇异值分解**（SVD）。$\sigma_i$ 叫**奇异值**，$\boldsymbol v_i$、$\boldsymbol u_i$ 分别叫**右奇异向量**、**左奇异向量**。

#### 转一下，沿坐标轴伸缩，再转一下

从右往左读 $A\boldsymbol x=U\big(\Sigma(V^{\mathsf T}\boldsymbol x)\big)$，是三个动作接连做：

1. $V^{\mathsf T}\boldsymbol x$ 的第 $i$ 个分量是 $\boldsymbol v_i^{\mathsf T}\boldsymbol x$，即 $\boldsymbol x$ 在 $\boldsymbol v_i$ 方向上的坐标（L.10.3），因为 $V^{\mathsf T}\boldsymbol v_i=\boldsymbol e_i$，几何上这一步把 $\boldsymbol v_1,\boldsymbol v_2,\dots$ 转到坐标轴上；
2. $\Sigma$ 把第 $i$ 个坐标乘 $\sigma_i$，单位圆变成一个摆正的椭圆；
3. $U$ 把第 $i$ 根坐标轴转到 $\boldsymbol u_i$。

抓手是：**任何矩阵都是「转一下，沿坐标轴伸缩，再转一下」**。单位圆（球）变成以 $\boldsymbol u_i$ 为轴、半轴长 $\sigma_i$ 的椭圆（椭球），$\sigma_i=0$ 的方向被压扁。要补两句：正交矩阵的行列式可能是 $-1$，「转」里可能带一次翻面；$m\ne n$ 时 $\Sigma$ 还改变维数。

![剪切拆成三步：$V^{\mathsf T}$ 把 $\boldsymbol v_1,\boldsymbol v_2$ 转到坐标轴上，$\Sigma$ 把单位圆拉成摆正的椭圆，$U$ 再把半轴转到 $\boldsymbol u_1,\boldsymbol u_2$，结果正是剪切作用出的斜椭圆（浅虚线是单位圆）](fig/L15-n3.pdf){width=95%}

和 L.12 的对角化 $A=P\Lambda P^{-1}$ 比一比：想法相同，都是换尺子后只剩沿轴伸缩；但对角化输入输出用同一组一般不垂直的基，不一定存在（剪切），SVD 用两组各自正交的基，总存在，$\sigma_i\ge0$。

**方法 1（各列正交时直接读出 SVD）**

$A$ 的各列两两正交时，$\boldsymbol e_j$ 本身就是「垂直进、垂直出」的方向，因为 $A\boldsymbol e_j$ 就是第 $j$ 列。

1. 各列的长度就是奇异值，从大到小排；
2. 对应的 $\boldsymbol v$ 取那一列位置上的 $\boldsymbol e_j$；
3. 非零列对应的 $\boldsymbol u$ 取那一列除以它的长度；
4. 零列给出 $\sigma=0$，$\boldsymbol u$ 不够 $m$ 个时另行补齐。

**例 1**　写出 $A=\begin{pmatrix}0&-3\\2&0\end{pmatrix}$ 的奇异值分解。

两列 $(0,2)^{\mathsf T}$、$(-3,0)^{\mathsf T}$ 的点积是 0，用方法 1。

第一步，列长是 2 和 3，从大到小排：$\sigma_1=3$ 来自第二列，$\sigma_2=2$ 来自第一列。

第二步，$\boldsymbol v_1=\boldsymbol e_2$，$\boldsymbol u_1=\frac13(-3,0)^{\mathsf T}=(-1,0)^{\mathsf T}$；$\boldsymbol v_2=\boldsymbol e_1$，$\boldsymbol u_2=(0,1)^{\mathsf T}$。

第三步，按列排好：

$$A=\begin{pmatrix}-1&0\\0&1\end{pmatrix}\begin{pmatrix}3&0\\0&2\end{pmatrix}\begin{pmatrix}0&1\\1&0\end{pmatrix}^{\mathsf T}.$$

这个矩阵没有实特征值（$\lambda^2+6=0$），奇异值却照样存在。

> 写出 $A=\begin{pmatrix}2&-1\\2&1\end{pmatrix}$ 的奇异值分解。
>
> 答案：两列点积 $-2+2=0$，长度 $2\sqrt2$、$\sqrt2$。$\sigma_1=2\sqrt2$，$\boldsymbol v_1=\boldsymbol e_1$，$\boldsymbol u_1=\frac1{\sqrt2}(1,1)^{\mathsf T}$；$\sigma_2=\sqrt2$，$\boldsymbol v_2=\boldsymbol e_2$，$\boldsymbol u_2=\frac1{\sqrt2}(-1,1)^{\mathsf T}$。

合上书，说出 $A=U\Sigma V^{\mathsf T}$ 里三个矩阵各做了什么。这一节还欠一个证明：「垂直进、垂直出」的方向为什么总存在？

### 2. 奇异值和奇异向量怎样算？

列不正交时要另找 $\boldsymbol v_i$。例如 $A=\begin{pmatrix}3&0\\4&5\end{pmatrix}$ 把 $\boldsymbol e_1,\boldsymbol e_2$ 送到 $(3,4)^{\mathsf T}$、$(0,5)^{\mathsf T}$，点积 $20\ne0$。

先把要求写成式子。用 $(AB)^{\mathsf T}=B^{\mathsf T}A^{\mathsf T}$（L.3.6），两个像的点积是

$$(A\boldsymbol v_i)^{\mathsf T}(A\boldsymbol v_j)=\boldsymbol v_i^{\mathsf T}(A^{\mathsf T}A)\boldsymbol v_j .$$

$A$ 只通过 $A^{\mathsf T}A$ 出现。$A^{\mathsf T}A$ 是 $n$ 阶对称矩阵，又是半正定的，因为 $\boldsymbol x^{\mathsf T}A^{\mathsf T}A\boldsymbol x=\lVert A\boldsymbol x\rVert^2\ge0$（$\lVert\cdot\rVert$ 是 L.2 的向量长度；L.14.5）。直接用 $A$ 的特征向量不行：它们一般不垂直，$A$ 不是方阵时更没有特征值。

由谱定理（L.13.3），$A^{\mathsf T}A$ 有两两垂直的单位特征向量 $\boldsymbol v_1,\dots,\boldsymbol v_n$，特征值 $\lambda_1\ge\cdots\ge\lambda_n\ge0$。代进去，用 $A^{\mathsf T}A\boldsymbol v_j=\lambda_j\boldsymbol v_j$：

$$\boldsymbol v_i^{\mathsf T}(A^{\mathsf T}A)\boldsymbol v_j=\lambda_j\,\boldsymbol v_i^{\mathsf T}\boldsymbol v_j=\begin{cases}0,&i\ne j,\\ \lambda_i,&i=j.\end{cases}$$

$i\ne j$ 时为 0，正是「垂直出」；$i=j$ 时得 $\lVert A\boldsymbol v_i\rVert^2=\lambda_i$。所以

$$\sigma_i=\sqrt{\lambda_i},\qquad \boldsymbol u_i=\frac{A\boldsymbol v_i}{\sigma_i}\quad(\sigma_i>0).$$

第 1 节欠的证明补上了。奇异值唯一；$U$、$V$ 不唯一，例如 $\boldsymbol v_i$、$\boldsymbol u_i$ 可以同时变号。

**方法 2（由 $A^{\mathsf T}A$ 构造 SVD）**

1. 求 $A^{\mathsf T}A$ 的特征值，从大到小排，$\sigma_i=\sqrt{\lambda_i}$；
2. 求两两垂直的单位特征向量（重根时在特征子空间内正交化，L.13.4），排成 $V$；
3. 对每个 $\sigma_i>0$，算 $\boldsymbol u_i=A\boldsymbol v_i/\sigma_i$；
4. 不够 $m$ 个时，解 $\boldsymbol u_1^{\mathsf T}\boldsymbol y=\cdots=\boldsymbol u_r^{\mathsf T}\boldsymbol y=0$，正交化、单位化后补齐 $U$。

第 3 步不能换成「另求 $AA^{\mathsf T}$ 的特征向量当 $U$」：特征向量可差一个负号，两边各选各的，会配错。例如例 1 中 $(1,0)^{\mathsf T}$ 也是 $AA^{\mathsf T}=\operatorname{diag}(9,4)$ 的单位特征向量，当 $\boldsymbol u_1$ 配上 $\boldsymbol v_1=\boldsymbol e_2$，乘回去得 $\begin{pmatrix}0&3\\2&0\end{pmatrix}\ne A$。

$m<n$ 时可以先对较小的 $AA^{\mathsf T}$ 求特征值 $\sigma_i^2$ 和 $\boldsymbol u_i$，再用 $\boldsymbol v_i=A^{\mathsf T}\boldsymbol u_i/\sigma_i$。其余的 $\boldsymbol v$ 取 $A$ 的零空间 $N(A)$ 的规范正交基：它们满足 $A\boldsymbol v=\boldsymbol 0$，对应 $\sigma=0$，又自动与前面的 $\boldsymbol v_i$ 垂直（后者在行空间里，L.8.5）。

**例 2**　求 $A=\begin{pmatrix}3&0\\4&5\end{pmatrix}$ 的奇异值分解。

第一步，求 $A^{\mathsf T}A$ 的特征值：

$$A^{\mathsf T}A=\begin{pmatrix}25&20\\20&25\end{pmatrix},\qquad \lambda^2-50\lambda+225=(\lambda-45)(\lambda-5)=0 .$$

所以 $\sigma_1=\sqrt{45}=3\sqrt5$，$\sigma_2=\sqrt5$。

第二步，$\lambda=45$ 时 $A^{\mathsf T}A-45E=\begin{pmatrix}-20&20\\20&-20\end{pmatrix}$，得 $\boldsymbol v_1=\frac1{\sqrt2}(1,1)^{\mathsf T}$；$\lambda=5$ 的特征向量与它垂直（L.13.2），取 $\boldsymbol v_2=\frac1{\sqrt2}(-1,1)^{\mathsf T}$。

第三步，算 $\boldsymbol u_i$：

$$\boldsymbol u_1=\frac{1}{3\sqrt5}\cdot\frac1{\sqrt2}\begin{pmatrix}3\\9\end{pmatrix}=\frac1{\sqrt{10}}\begin{pmatrix}1\\3\end{pmatrix},\qquad \boldsymbol u_2=\frac{1}{\sqrt5}\cdot\frac1{\sqrt2}\begin{pmatrix}-3\\1\end{pmatrix}=\frac1{\sqrt{10}}\begin{pmatrix}-3\\1\end{pmatrix}.$$

于是

$$A=\frac1{\sqrt{10}}\begin{pmatrix}1&-3\\3&1\end{pmatrix}\begin{pmatrix}3\sqrt5&0\\0&\sqrt5\end{pmatrix}\frac1{\sqrt2}\begin{pmatrix}1&-1\\1&1\end{pmatrix}^{\mathsf T}.$$

![垂直的 $\boldsymbol v_1,\boldsymbol v_2$（实线）被送到椭圆的两条半轴，仍然垂直；$\boldsymbol e_1,\boldsymbol e_2$（虚线）的像不垂直](fig/L15-n1.pdf){width=80%}

> 求剪切 $\begin{pmatrix}1&1\\0&1\end{pmatrix}$ 的奇异值，核对第 1 节的两个数。提示：$\big(\frac{1\pm\sqrt5}2\big)^2=\frac{3\pm\sqrt5}2$。
>
> 答案：$A^{\mathsf T}A=\begin{pmatrix}1&1\\1&2\end{pmatrix}$，特征方程 $\lambda^2-3\lambda+1=0$，$\lambda=\frac{3\pm\sqrt5}2$。开方得 $\sigma_1=\frac{\sqrt5+1}2\approx1.618$，$\sigma_2=\frac{\sqrt5-1}2\approx0.618$。

**例 3**　求 $A=\begin{pmatrix}1&1\\0&1\\1&0\end{pmatrix}$ 的奇异值分解。

和例 2 不同，$A$ 是 $3\times2$ 的，$U$ 的第 3 列要按第 4 步补。

第一步，$A^{\mathsf T}A=\begin{pmatrix}2&1\\1&2\end{pmatrix}$ 正是老朋友①：特征值 3、1，$\sigma_1=\sqrt3$，$\sigma_2=1$；特征向量单位化得 $\boldsymbol v_1=\frac1{\sqrt2}(1,1)^{\mathsf T}$，$\boldsymbol v_2=\frac1{\sqrt2}(-1,1)^{\mathsf T}$。

第二步，

$$\boldsymbol u_1=\frac{A\boldsymbol v_1}{\sqrt3}=\frac1{\sqrt6}\begin{pmatrix}2\\1\\1\end{pmatrix},\qquad \boldsymbol u_2=\frac{A\boldsymbol v_2}{1}=\frac1{\sqrt2}\begin{pmatrix}0\\1\\-1\end{pmatrix}.$$

第三步，补 $\boldsymbol u_3$。与 $\boldsymbol u_1,\boldsymbol u_2$ 都垂直：

$$2y_1+y_2+y_3=0,\qquad y_2-y_3=0 .$$

由第二式 $y_2=y_3$，代入第一式得 $y_1=-y_2$，单位化得 $\boldsymbol u_3=\frac1{\sqrt3}(-1,1,1)^{\mathsf T}$。$\Sigma=\begin{pmatrix}\sqrt3&0\\0&1\\0&0\end{pmatrix}$ 的第三行全是 0：$A$ 的输出永远没有 $\boldsymbol u_3$ 方向的分量。

#### 老朋友的奇异值

把四个二阶老朋友的特征值和奇异值并排，先自己看哪里相同：

| 老朋友 | 特征值 | 奇异值 |
|---|---|---|
| ① 对称伸缩 | 3，1 | 3，1 |
| ② 剪切 | 1，1 | 1.618，0.618 |
| ③ 转 90° | 没有实特征值 | 1，1 |
| ④ 投影 | 1，0 | 1，0 |

①④对称半正定，$A^{\mathsf T}A=A^2$ 的特征值是 $\lambda^2$，开方正好是 $\lambda$，两列相同。②③不对称，就对不上：**奇异值一般不等于特征值**，这是本章最常见的错误。

奇异值只由 $A^{\mathsf T}A$ 决定，所以 $Q$ 正交时 $QA$ 与 $A$ 的奇异值相同，因为 $(QA)^{\mathsf T}(QA)=A^{\mathsf T}Q^{\mathsf T}QA=A^{\mathsf T}A$。

合上书，从「$A\boldsymbol v_i$ 两两垂直」推出 $\boldsymbol v_i$ 是 $A^{\mathsf T}A$ 的特征向量、$\sigma_i=\sqrt{\lambda_i}$。

### 3. SVD 把一个矩阵拆成了什么？

三个矩阵相乘不好想，能不能写成几个简单矩阵相加？用「列乘行再相加」（L.3.7）：$M$ 的各列为 $\boldsymbol p_1,\dots,\boldsymbol p_k$、$N$ 的各行为 $\boldsymbol q_1^{\mathsf T},\dots,\boldsymbol q_k^{\mathsf T}$ 时，$MN=\sum\boldsymbol p_i\boldsymbol q_i^{\mathsf T}$。取 $M=U\Sigma$（第 $i$ 列 $\sigma_i\boldsymbol u_i$），$N=V^{\mathsf T}$（第 $i$ 行 $\boldsymbol v_i^{\mathsf T}$）：

$$A=\sigma_1\boldsymbol u_1\boldsymbol v_1^{\mathsf T}+\sigma_2\boldsymbol u_2\boldsymbol v_2^{\mathsf T}+\cdots+\sigma_r\boldsymbol u_r\boldsymbol v_r^{\mathsf T}.$$

这叫**外积展开**。$\boldsymbol u_i\boldsymbol v_i^{\mathsf T}$ 的每一列都是 $\boldsymbol u_i$ 的倍数，每一行都是 $\boldsymbol v_i^{\mathsf T}$ 的倍数，秩为 1，像一张只有一种花纹的图案。把 $\sigma_i\boldsymbol u_i\boldsymbol v_i^{\mathsf T}$ 叫第 $i$ **层**，$A$ 就是 $r$ 层按权重从大到小叠起来的。一层作用在 $\boldsymbol x$ 上是 $\sigma_i(\boldsymbol v_i^{\mathsf T}\boldsymbol x)\boldsymbol u_i$：量出 $\boldsymbol x$ 在 $\boldsymbol v_i$ 上的分量，乘 $\sigma_i$，沿 $\boldsymbol u_i$ 输出。

#### 秩

$U$、$V$ 可逆，乘可逆矩阵不改变秩（L.7.7），所以 $r(A)=r(\Sigma)=r$：**秩等于非零奇异值的个数**。对 $n$ 阶方阵，可逆大定理添上一行：$A$ 可逆 $\iff$ $n$ 个奇异值全都大于 0。

#### 四个子空间

把 $\boldsymbol x$ 按规范正交基 $\boldsymbol v_1,\dots,\boldsymbol v_n$ 展开，坐标就是点积（L.10.3）：$\boldsymbol x=\sum_{i=1}^n(\boldsymbol v_i^{\mathsf T}\boldsymbol x)\boldsymbol v_i$。两边左乘 $A$，用 $A\boldsymbol v_i=\sigma_i\boldsymbol u_i$（$i\le r$）、$A\boldsymbol v_i=\boldsymbol 0$（$i>r$）：

$$A\boldsymbol x=\sum_{i=1}^{r}\sigma_i(\boldsymbol v_i^{\mathsf T}\boldsymbol x)\,\boldsymbol u_i .$$

由它逐个读出 L.8.5 的四个子空间：

- 列空间 $C(A)=\operatorname{span}(\boldsymbol u_1,\dots,\boldsymbol u_r)$：每个 $A\boldsymbol x$ 都是这些 $\boldsymbol u_i$ 的组合，反过来 $\boldsymbol u_i=A(\boldsymbol v_i/\sigma_i)$ 在列空间里。
- 零空间 $N(A)=\operatorname{span}(\boldsymbol v_{r+1},\dots,\boldsymbol v_n)$：$\boldsymbol u_1,\dots,\boldsymbol u_r$ 线性无关，$A\boldsymbol x=\boldsymbol 0$ 当且仅当 $\boldsymbol x$ 在 $\boldsymbol v_1,\dots,\boldsymbol v_r$ 上的坐标全为 0。
- 行空间 $C(A^{\mathsf T})=\operatorname{span}(\boldsymbol v_1,\dots,\boldsymbol v_r)$：对 $A^{\mathsf T}=\sum_{i\le r}\sigma_i\boldsymbol v_i\boldsymbol u_i^{\mathsf T}$ 重复第一条，$\boldsymbol u$、$\boldsymbol v$ 互换角色。
- 左零空间 $N(A^{\mathsf T})=\operatorname{span}(\boldsymbol u_{r+1},\dots,\boldsymbol u_m)$：同样重复第二条。

SVD 一次给出四个子空间的规范正交基，也讲清了 $A$ 怎样搬运：**行空间里的 $\boldsymbol v_i$ 被送到列空间里的 $\sigma_i\boldsymbol u_i$，零空间被压成 $\boldsymbol 0$**。

**方法 3（外积展开读秩和子空间）**

1. 写出外积展开 $A=\sum_{i\le r}\sigma_i\boldsymbol u_i\boldsymbol v_i^{\mathsf T}$；
2. 秩是非零奇异值的个数，四个子空间按上面的清单读出；
3. 秩 1 矩阵 $A=\boldsymbol a\boldsymbol b^{\mathsf T}$（$\boldsymbol a,\boldsymbol b\ne\boldsymbol 0$）直接把长度提出来：$\sigma_1=\lVert\boldsymbol a\rVert\lVert\boldsymbol b\rVert$，$\boldsymbol u_1=\boldsymbol a/\lVert\boldsymbol a\rVert$，$\boldsymbol v_1=\boldsymbol b/\lVert\boldsymbol b\rVert$。

**例 4**　写出 $A=\begin{pmatrix}1&1&1\\2&2&2\end{pmatrix}$ 的外积展开，并给出四个子空间的规范正交基。

和例 2、例 3 不同，这里不用算 $A^{\mathsf T}A$：两行都是 $(1,1,1)$ 的倍数，用第 3 步。

第一步，$A=\boldsymbol a\boldsymbol b^{\mathsf T}$，$\boldsymbol a=(1,2)^{\mathsf T}$，$\boldsymbol b=(1,1,1)^{\mathsf T}$，长度 $\sqrt5$、$\sqrt3$：

$$A=\sqrt{15}\,\boldsymbol u_1\boldsymbol v_1^{\mathsf T},\qquad \boldsymbol u_1=\tfrac1{\sqrt5}(1,2)^{\mathsf T},\quad \boldsymbol v_1=\tfrac1{\sqrt3}(1,1,1)^{\mathsf T}.$$

第二步，列空间由 $\boldsymbol u_1$ 张成，左零空间由与它垂直的 $\boldsymbol u_2=\frac1{\sqrt5}(2,-1)^{\mathsf T}$ 张成；行空间由 $\boldsymbol v_1$ 张成。

第三步，零空间是平面 $x_1+x_2+x_3=0$，要在里面找两个互相垂直的单位向量。一次找一个：先取任意一个解 $\boldsymbol w_1=(1,-1,0)^{\mathsf T}$；第二个既在平面上又与 $\boldsymbol w_1$ 垂直，就再加一个方程：

$$x_1+x_2+x_3=0,\qquad x_1-x_2=0 .$$

得 $x_1=x_2$，$x_3=-2x_1$，取 $\boldsymbol w_2=(1,1,-2)^{\mathsf T}$。单位化：$\boldsymbol v_2=\frac1{\sqrt2}(1,-1,0)^{\mathsf T}$，$\boldsymbol v_3=\frac1{\sqrt6}(1,1,-2)^{\mathsf T}$。

> 写出 $A=\begin{pmatrix}3&4\\-3&-4\end{pmatrix}$ 的奇异值和零空间。
>
> 答案：$A=(1,-1)^{\mathsf T}(3,4)$，$\sigma_1=\sqrt2\cdot5=5\sqrt2$，$\sigma_2=0$；零空间由与 $\boldsymbol v_1=\frac15(3,4)^{\mathsf T}$ 垂直的 $\frac15(4,-3)^{\mathsf T}$ 张成。

合上书，从 $A=U\Sigma V^{\mathsf T}$ 推出外积展开，再说出四个子空间各由哪些奇异向量张成。

### 4. 方程组既无解、解又不唯一时，取哪一个解？

先看 $A=\begin{pmatrix}1&1\\1&1\end{pmatrix}$，$\boldsymbol b=(1,3)^{\mathsf T}$。记 $s=x_1+x_2$，则 $A\boldsymbol x=(s,s)^{\mathsf T}$，方程组要 $s=1$ 且 $s=3$，无解。

退而求最小二乘解（L.10.1）：让 $\lVert A\boldsymbol x-\boldsymbol b\rVert^2=(s-1)^2+(s-3)^2$ 最小，得 $s=2$。可满足 $x_1+x_2=2$ 的 $\boldsymbol x$ 有一整条直线；$A^{\mathsf T}A$ 不可逆，L.10.2 的公式也用不了。自然的选法是取最短的那个，见图 L15-n4。

![粗实线 $x_1+x_2=2$ 上的点都是最小二乘解，它平行于零空间方向（虚线）；从原点作垂线（点线）得到最短的解 $\boldsymbol x^+=(1,1)^{\mathsf T}$（实心点），它在行空间里，其他解如 $(2,0)^{\mathsf T}$（空心点）都更长](fig/L15-n4.pdf){width=60%}

图里有两件事：$\boldsymbol b$ 有一部分 $A$ 到不了；沿零空间方向加一点，$\boldsymbol x$ 只会变长，所以最短的解是垂足。

#### 用 SVD 把两件事分开

令 $\boldsymbol y=V^{\mathsf T}\boldsymbol x$，$\boldsymbol c=U^{\mathsf T}\boldsymbol b$，则 $\boldsymbol x=V\boldsymbol y$，$\boldsymbol b=U\boldsymbol c$。用 $V^{\mathsf T}V=E$ 和正交矩阵保长度（L.10.4）：

$$\lVert A\boldsymbol x-\boldsymbol b\rVert=\lVert U(\Sigma\boldsymbol y-\boldsymbol c)\rVert=\lVert\Sigma\boldsymbol y-\boldsymbol c\rVert,\qquad \lVert\boldsymbol x\rVert=\lVert\boldsymbol y\rVert .$$

$\Sigma\boldsymbol y$ 的前 $r$ 个分量是 $\sigma_iy_i$，其余是 0，所以

$$\lVert\Sigma\boldsymbol y-\boldsymbol c\rVert^2=\sum_{i=1}^r(\sigma_iy_i-c_i)^2+\sum_{i=r+1}^m c_i^2 .$$

这个式子把图里的两件事分开了：

- 第二个和与 $\boldsymbol y$ 无关，是 $\boldsymbol b$ 在左零空间方向上的分量，消不掉；
- 第一个和在 $y_i=c_i/\sigma_i$（$i\le r$）时为 0；
- $y_{r+1},\dots,y_n$ 根本不出现，这就是解不唯一的来源，它们是 $\boldsymbol x$ 在零空间方向上的坐标。要 $\lVert\boldsymbol y\rVert$ 最小，就让它们取 0。

所以长度最小的最小二乘解是

$$\boldsymbol x^+=\sum_{i=1}^r\frac{\boldsymbol u_i^{\mathsf T}\boldsymbol b}{\sigma_i}\,\boldsymbol v_i=A^+\boldsymbol b,\qquad A^+=\sum_{i=1}^r\frac1{\sigma_i}\boldsymbol v_i\boldsymbol u_i^{\mathsf T}=V\Sigma^+U^{\mathsf T},$$

第二个等号把每项写成 $\frac1{\sigma_i}(\boldsymbol v_i\boldsymbol u_i^{\mathsf T})\boldsymbol b$。$\Sigma^+$ 是 $n\times m$ 矩阵，对角线上是 $1/\sigma_1,\dots,1/\sigma_r$，其余为 0。$A^+$ 叫**伪逆**。

伪逆只撤销能撤销的部分：$A$ 把 $\boldsymbol v_i$ 送到 $\sigma_i\boldsymbol u_i$，$A^+$ 把 $\boldsymbol u_i$ 送回 $\boldsymbol v_i/\sigma_i$；被 $A$ 压扁的零空间方向，$A^+$ 不去猜，一律取 0；$\boldsymbol b$ 中到不了的部分直接丢掉。所以一般 $A^+A\ne E$。

$A$ 可逆时 $A^+=A^{-1}$；$A$ 列满秩时，$A^{\mathsf T}A=V\Sigma^{\mathsf T}\Sigma V^{\mathsf T}$ 可逆，代入 L.10.2 的公式，$V^{\mathsf T}V=E$ 消掉：

$$(A^{\mathsf T}A)^{-1}A^{\mathsf T}=V(\Sigma^{\mathsf T}\Sigma)^{-1}V^{\mathsf T}\cdot V\Sigma^{\mathsf T}U^{\mathsf T}=V\big((\Sigma^{\mathsf T}\Sigma)^{-1}\Sigma^{\mathsf T}\big)U^{\mathsf T},$$

中间矩阵的对角元是 $\frac{\sigma_i}{\sigma_i^2}=\frac1{\sigma_i}$，正是 $\Sigma^+$。

**方法 4（用 SVD 求伪逆和最短的最小二乘解）**

1. 求出前 $r$ 层的 $\sigma_i$、$\boldsymbol u_i$、$\boldsymbol v_i$；
2. 写出 $A^+=\sum_{i\le r}\frac1{\sigma_i}\boldsymbol v_i\boldsymbol u_i^{\mathsf T}$，算 $\boldsymbol x^+=A^+\boldsymbol b$；

**例 5**　求 $A=\begin{pmatrix}1&1&1\\2&2&2\end{pmatrix}$ 的伪逆，以及 $\boldsymbol b=(1,1)^{\mathsf T}$ 时长度最小的最小二乘解。

第一步，由例 4，$r=1$，$\sigma_1=\sqrt{15}$，$\boldsymbol u_1$、$\boldsymbol v_1$ 见那里。

第二步，因为 $\sqrt{15}\cdot\sqrt3\cdot\sqrt5=15$，

$$A^+=\frac1{\sqrt{15}}\boldsymbol v_1\boldsymbol u_1^{\mathsf T}=\frac1{15}\begin{pmatrix}1&2\\1&2\\1&2\end{pmatrix},\qquad \boldsymbol x^+=A^+\boldsymbol b=\Big(\frac15,\frac15,\frac15\Big)^{\mathsf T}.$$

第三步，检验：分量和 $\frac35$ 正是让 $(s-1)^2+(2s-1)^2$ 最小的 $s=x_1+x_2+x_3$。

> 设 $A=\begin{pmatrix}1&2\\2&4\end{pmatrix}$，$\boldsymbol b=(3,1)^{\mathsf T}$，求 $A^+$ 和 $\boldsymbol x^+$。
>
> 答案：$A=(1,2)^{\mathsf T}(1,2)$，$\sigma_1=5$，$\boldsymbol u_1=\boldsymbol v_1=\frac1{\sqrt5}(1,2)^{\mathsf T}$，$A^+=\frac1{25}\begin{pmatrix}1&2\\2&4\end{pmatrix}$，$\boldsymbol x^+=\big(\frac15,\frac25\big)^{\mathsf T}$。

合上书，用「正交矩阵保长度」推出最短的最小二乘解，说出残差里哪一部分消不掉、解里哪一部分可以随便取。

### 5. 只保留最大的几层，会损失多少？

照片压缩就是只留前 $k$ 层（$k<r$）：

$$A_k=\sigma_1\boldsymbol u_1\boldsymbol v_1^{\mathsf T}+\cdots+\sigma_k\boldsymbol u_k\boldsymbol v_k^{\mathsf T}.$$

它的秩是 $k$，只需存 $k(m+n+1)$ 个数；开头的照片 $k=50$ 时是 100050 个。LoRA 微调是同一种账：$4096\times4096$ 权重矩阵的修正量只取秩 8，训练 $2\times4096\times8=65536$ 个数，约为全部的 $\frac1{256}$（M.13.6）。

#### 两种量法

**弗罗贝尼乌斯范数**把元素排成一长串求长度：$\lVert A\rVert_F=\sqrt{\sum_{i,j}a_{ij}^2}$。$A^{\mathsf T}A$ 的第 $j$ 个对角元是第 $j$ 列元素的平方和，所以全部元素的平方和是 $A^{\mathsf T}A$ 的迹，而迹是特征值之和（L.11.3）：

$$\lVert A\rVert_F^2=\sigma_1^2+\cdots+\sigma_r^2 .$$

**谱范数**看 $A$ 最多把向量拉长几倍：$\lVert A\rVert_2=\max_{\boldsymbol x\ne\boldsymbol 0}\lVert A\boldsymbol x\rVert/\lVert\boldsymbol x\rVert$。比值的平方 $\frac{\boldsymbol x^{\mathsf T}(A^{\mathsf T}A)\boldsymbol x}{\boldsymbol x^{\mathsf T}\boldsymbol x}$ 是 $A^{\mathsf T}A$ 的瑞利商，由 L.14.7，最大值是 $\sigma_1^2$，在 $\boldsymbol v_1$ 处取到。所以 $\lVert A\rVert_2=\sigma_1$，即椭圆最长的半轴。

误差 $A-A_k=\sum_{i=k+1}^r\sigma_i\boldsymbol u_i\boldsymbol v_i^{\mathsf T}$ 里的 $\boldsymbol u_i$、$\boldsymbol v_i$ 仍各自是两两垂直的单位向量，所以它就是 $A-A_k$ 的 SVD 的外积展开，奇异值是 $\sigma_{k+1},\dots,\sigma_r$：

$$\lVert A-A_k\rVert_2=\sigma_{k+1},\qquad \lVert A-A_k\rVert_F=\sqrt{\sigma_{k+1}^2+\cdots+\sigma_r^2}.$$

**方法 5（截断 SVD 与两种范数）**

1. $\lVert A\rVert_2=\sigma_1$，$\lVert A\rVert_F=\sqrt{\sum\sigma_i^2}$（也等于元素平方和开方）；
2. 最佳秩 $k$ 近似是前 $k$ 层 $A_k$，误差按上面的公式算。

**例 6**　对例 2 的矩阵 $A$，求 $\lVert A\rVert_2$、$\lVert A\rVert_F$、最佳秩 1 近似及其误差。

第一步，$\lVert A\rVert_2=3\sqrt5$；$\lVert A\rVert_F=\sqrt{45+5}=\sqrt{50}$，与元素平方和 $9+16+25=50$ 一致。

第二步，最佳秩 1 近似是第一层：

$$A_1=3\sqrt5\cdot\frac1{\sqrt{10}}\begin{pmatrix}1\\3\end{pmatrix}\cdot\frac1{\sqrt2}(1,1)=\begin{pmatrix}1.5&1.5\\4.5&4.5\end{pmatrix}.$$

第三步，$A-A_1=\begin{pmatrix}1.5&-1.5\\-0.5&0.5\end{pmatrix}$，元素平方和 5，所以 $\lVert A-A_1\rVert_F=\sqrt5=\sigma_2$；第一层保留了平方和的 $90\%$。

#### 为什么前 $k$ 层最好

**埃卡特–扬定理**　设 $0\le k<r$，$B$ 是任一秩不超过 $k$ 的 $m\times n$ 矩阵，则 $\lVert A-B\rVert_2\ge\sigma_{k+1}$，$\lVert A-B\rVert_F\ge\sqrt{\sigma_{k+1}^2+\cdots+\sigma_r^2}$。$A_k$ 取到等号，所以它最好。

先看 $2\times2$、$k=1$：$B$ 秩不超过 1，有单位向量 $\boldsymbol x$ 使 $B\boldsymbol x=\boldsymbol 0$，于是 $\lVert A-B\rVert_2\ge\lVert(A-B)\boldsymbol x\rVert=\lVert A\boldsymbol x\rVert\ge\sigma_2$，因为椭圆上的点离原点至少 $\sigma_2$。抓手是：**找一个被 $B$ 压扁、却被 $A$ 拉长的方向**。

第一步，由秩–零化度定理（L.8.4），$\dim N(B)\ge n-k$。

第二步，$N(B)$ 与 $S=\operatorname{span}(\boldsymbol v_1,\dots,\boldsymbol v_{k+1})$ 有公共的非零向量 $\boldsymbol x$（再缩放成单位向量）。理由：设 $\boldsymbol w_1,\dots,\boldsymbol w_p$ 是 $N(B)$ 的基（$p\ge n-k$），它们连同 $\boldsymbol v_1,\dots,\boldsymbol v_{k+1}$ 至少 $n+1$ 个 $n$ 维向量，必线性相关（L.7）：

$$\underbrace{c_1\boldsymbol v_1+\cdots+c_{k+1}\boldsymbol v_{k+1}}_{\boldsymbol x}=-(a_1\boldsymbol w_1+\cdots+a_p\boldsymbol w_p),$$

系数不全为 0。左边看，$\boldsymbol x\in S$；右边看，$\boldsymbol x\in N(B)$。若 $\boldsymbol x=\boldsymbol 0$，两组向量各自线性无关，系数会全为 0，矛盾。

第三步，写 $\boldsymbol x=\sum_{i\le k+1}c_i\boldsymbol v_i$，$\sum c_i^2=1$。$A\boldsymbol x=\sum c_i\sigma_i\boldsymbol u_i$，各 $\boldsymbol u_i$ 两两垂直，由勾股定理

$$\lVert(A-B)\boldsymbol x\rVert^2=\lVert A\boldsymbol x\rVert^2=\sum_{i=1}^{k+1}\sigma_i^2c_i^2\ge\sigma_{k+1}^2 ,$$

因为 $i\le k+1$ 时 $\sigma_i\ge\sigma_{k+1}$。所以 $\lVert A-B\rVert_2\ge\sigma_{k+1}$。

弗罗贝尼乌斯范数的部分思路相同。$B$ 的各列落在某个 $k$ 维子空间 $W$ 里，$A$ 的每一列到 $W$ 的距离不超过到 $B$ 对应列的距离（垂足最近，L.10.1），逐列用勾股定理得 $\lVert A-B\rVert_F^2\ge\lVert A\rVert_F^2-(A\text{ 的各列投到 }W\text{ 上的平方和})$，只需说明这个平方和不超过 $\sigma_1^2+\cdots+\sigma_k^2$。取 $W$ 的规范正交基 $\boldsymbol p_1,\dots,\boldsymbol p_k$，第 $j$ 列 $\boldsymbol a_j$ 投影的长度平方是 $\sum_l(\boldsymbol p_l^{\mathsf T}\boldsymbol a_j)^2$，对 $j$ 求和得 $\sum_l\lVert A^{\mathsf T}\boldsymbol p_l\rVert^2$。再由 $A^{\mathsf T}\boldsymbol p_l=\sum_i\sigma_i(\boldsymbol u_i^{\mathsf T}\boldsymbol p_l)\boldsymbol v_i$ 和勾股定理，它等于 $\sum_i\sigma_i^2w_i$，其中 $w_i=\sum_l(\boldsymbol u_i^{\mathsf T}\boldsymbol p_l)^2$ 是 $\boldsymbol u_i$ 投到 $W$ 上的长度平方，所以 $w_i\le1$；每个 $\boldsymbol p_l$ 在规范正交基 $\boldsymbol u_1,\dots,\boldsymbol u_m$ 下的坐标平方和是 1，所以全部 $w_i$ 之和是 $k$。$k$ 份权重分给各个 $\sigma_i^2$，每个最多拿一份，最多也就拿到最大的 $k$ 个。

合上书，用「找一个被 $B$ 压扁、被 $A$ 拉长的方向」复述谱范数情形的证明。

### 6. 把一张数据表压成少数几个主方向，是在做什么？

数据表每行一个样本，每列一个指标。指标太多时，想用少数几个综合指标概括每个样本，丢掉的信息尽量少。先把每列减去平均值（**中心化**），这样只需考虑过原点的直线。中心化后的表记作 $X$（$N\times d$，第 $i$ 行是 $\boldsymbol x_i^{\mathsf T}$）。

用一个数概括每个样本，就是选一条方向为单位向量 $\boldsymbol w$ 的直线，把每个点换成投影 $(\boldsymbol x_i^{\mathsf T}\boldsymbol w)\boldsymbol w$（L.2.3），那个数就是 $\boldsymbol x_i^{\mathsf T}\boldsymbol w$，丢掉的是点到直线的距离 $d_i$。由勾股定理 $\lVert\boldsymbol x_i\rVert^2=(\boldsymbol x_i^{\mathsf T}\boldsymbol w)^2+d_i^2$，对所有点求和，并注意 $X\boldsymbol w$ 的第 $i$ 个分量就是 $\boldsymbol x_i^{\mathsf T}\boldsymbol w$：

$$\sum_i d_i^2=\lVert X\rVert_F^2-\lVert X\boldsymbol w\rVert^2 .$$

$\lVert X\rVert_F^2$ 是定数，所以**离直线最近，就是投影最长**：要让 $\lVert X\boldsymbol w\rVert^2=\boldsymbol w^{\mathsf T}X^{\mathsf T}X\boldsymbol w$ 最大。由上一节，最大值是 $\sigma_1^2$，在 $\boldsymbol w=\boldsymbol v_1$ 取到。于是：

- 最好的方向是 $X$ 的第一个右奇异向量 $\boldsymbol v_1$，叫第一**主成分方向**；
- 各样本的综合指标排成列向量是 $X\boldsymbol v_1=\sigma_1\boldsymbol u_1$；
- 投影后的表就是最佳秩 1 近似 $X_1$。

第三条多说一句：投影后第 $i$ 行是「$X\boldsymbol v_1$ 的第 $i$ 个分量乘 $\boldsymbol v_1^{\mathsf T}$」，这恰是列乘行 $(X\boldsymbol v_1)\boldsymbol v_1^{\mathsf T}$ 的第 $i$ 行，所以各行叠起来是

$$(X\boldsymbol v_1)\boldsymbol v_1^{\mathsf T}=\sigma_1\boldsymbol u_1\boldsymbol v_1^{\mathsf T}=X_1 ,$$

丢掉的平方和是 $\sigma_2^2+\cdots+\sigma_r^2$。留 $k$ 个综合指标就取 $\boldsymbol v_1,\dots,\boldsymbol v_k$，投影后的表是 $X_k$。这就是主成分分析（PCA），它的统计含义在 M.5 讲。

**方法 6（用 SVD 求主成分）**

1. 每列减去平均值得 $X$，由 $X^{\mathsf T}X$ 求 $\sigma_i^2$ 和主方向 $\boldsymbol v_i$；
2. 综合指标是 $X\boldsymbol v_i$，保留比例是 $\frac{\sigma_1^2+\cdots+\sigma_k^2}{\sum\sigma_i^2}$（$k\le r$）；$\sigma_1=\sigma_2$ 时主方向不唯一。

**例 7**　四名同学两次测验的成绩，各减去该次平均分后是 $(2,1)$、$(1,2)$、$(-1,-2)$、$(-2,-1)$。求第一主成分方向、每人的综合指标和保留的比例。

第一步，数据已中心化：

$$X=\begin{pmatrix}2&1\\1&2\\-1&-2\\-2&-1\end{pmatrix},\qquad X^{\mathsf T}X=\begin{pmatrix}10&8\\8&10\end{pmatrix}.$$

第二步，特征值 $10\pm8$，即 18、2，$\sigma_1=3\sqrt2$，$\sigma_2=\sqrt2$，$\boldsymbol v_1=\frac1{\sqrt2}(1,1)^{\mathsf T}$。

第三步，综合指标 $X\boldsymbol v_1=\frac1{\sqrt2}(3,3,-3,-3)^{\mathsf T}$：前两人同样高，后两人同样低：两次测验一起高、一起低。

第四步，保留比例 $\frac{18}{20}=90\%$，丢掉的 $\sigma_2^2=2$ 正是四个点到直线 $y=x$ 的距离平方和。

![四个点（实心）到直线 $y=x$（方向 $\boldsymbol v_1$）的垂线段（虚线）平方和是 $2=\sigma_2^2$，在所有过原点的直线里最小；垂足（空心）是 $X_1$ 的各行](fig/L15-n2.pdf){width=55%}

合上书，用勾股定理说明「离直线最近」就是「投影最长」，以及答案为什么是 $\boldsymbol v_1$。

### 本章小结

| 方法 | 什么时候用 | 对应题号 |
|---|---|---|
| 方法 1（各列正交时直接读出 SVD） | 列两两正交 | L15-01 |
| 方法 2（由 $A^{\mathsf T}A$ 构造 SVD） | 一般矩阵求 SVD | L15-02、03、06、07、08 |
| 方法 3（外积展开读秩和子空间） | 秩、四个子空间、秩 1 矩阵 | L15-04、11、14、15 |
| 方法 4（用 SVD 求伪逆和最短的最小二乘解） | 最小二乘解不唯一 | L15-09、11、14、15 |
| 方法 5（截断 SVD 与两种范数） | 范数、最佳低秩近似 | L15-05、07、12、13 |
| 方法 6（用 SVD 求主成分） | 数据表的主方向 | L15-10 |

可逆大定理（$A$ 为 $n$ 阶方阵，各条互相等价）：

| 来自 | 条件 |
|---|---|
| L.4 | 消元后有 $n$ 个主元；$A\boldsymbol x=\boldsymbol b$ 对每个 $\boldsymbol b$ 都有唯一解；$A\boldsymbol x=\boldsymbol 0$ 只有零解 |
| L.5 | $A$ 可逆；存在 $B$ 使 $AB=E$ |
| L.6 | $\lvert A\rvert\ne0$ |
| L.7 | 列（行）向量组线性无关；$r(A)=n$ |
| L.8 | 列向量构成 $\mathbb R^n$ 的一组基；零空间只有零向量 |
| L.11 | 0 不是 $A$ 的特征值 |
| L.14 | $A^{\mathsf T}A$ 正定 |
| L.15（本章新增） | 奇异值全都大于 0 |
