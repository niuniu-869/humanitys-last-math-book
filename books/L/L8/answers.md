## L.8 · 向量空间（答案）

### A 基础

**L8-01**
**答案：** (C)。(A) 不含零向量；(B) 中 $(1,0,0)^{\mathsf T}$ 与 $(0,1,0)^{\mathsf T}$ 的和不在集合中；(D) 也不含零向量。 (C) 中向量都是 $t(1,1,1)^{\mathsf T}$，对加法和数乘封闭。

区分点：先查零向量能立刻排除仿射平面和球面，再检查并集型条件的加法封闭性。

**L8-02**
**答案：** $\{\boldsymbol v_1,\boldsymbol v_2,\boldsymbol v_4\}$ 是一组基，$\dim V=3$；添上 $\boldsymbol e_1$ 得到 $\mathbb R^4$ 的基。

以四向量为列作矩阵，主元列为第 1、2、4 列，且 $\boldsymbol v_3=\boldsymbol v_1+\boldsymbol v_2$。再算
$\det(\boldsymbol v_1,\boldsymbol v_2,\boldsymbol v_4,\boldsymbol e_1)=1\ne0$，所以添入 $\boldsymbol e_1$ 后无关且张成 $\mathbb R^4$。

区分点：行变换只用来找主元位置，基向量仍取原矩阵的对应列；添 $\boldsymbol e_1$ 还要检验它确实不在原张成中。

**L8-03**
**答案：**
$$P=\begin{pmatrix}1&1&0\\1&-1&0\\0&0&1\end{pmatrix},\qquad \boldsymbol y=P^{-1}\boldsymbol x=(2,1,2)^{\mathsf T}.$$

三列分别是 $\boldsymbol\beta_j$ 的旧坐标。由坐标变换 $\boldsymbol x=P\boldsymbol y$，解
$y_1+y_2=3$、$y_1-y_2=1$、$y_3=2$，得所写坐标。

区分点：$P$ 的列是新基用旧坐标表示的系数，因此是旧坐标等于 $P$ 乘新坐标，方向不能倒写。

**L8-04**
**答案：** 取 $A=(1,-1,0)$。因为 $A(a,a,b)^{\mathsf T}=0$，所以 $N(A)=N$；矩阵只有一行且非零，故 $r(A)=1$，由秩–零化度定理 $\dim N(A)=3-1=2$。

区分点：先把零空间中的关系读成约束 $x_1-x_2=0$，再用秩核对维数。

### B 进阶

**L8-05**
**答案：** 任取 $\boldsymbol u,\boldsymbol v\in W_1\cap W_2$ 与 $c\in\mathbb R$，因为两者分别在 $W_1,W_2$ 中，而它们都是子空间，所以 $\boldsymbol u+\boldsymbol v$ 与 $c\boldsymbol u$ 仍同时属于两者；零向量也同时属于两者，故交集是子空间。

若 $W_1\subseteq W_2$ 或 $W_2\subseteq W_1$，并集就等于较大的子空间，因而是子空间。反过来，若并集是子空间且两者互不包含，取 $\boldsymbol u\in W_1\setminus W_2$、$\boldsymbol v\in W_2\setminus W_1$。则 $\boldsymbol u+\boldsymbol v\in W_1\cup W_2$；若在 $W_1$ 中，则 $\boldsymbol v=(\boldsymbol u+\boldsymbol v)-\boldsymbol u\in W_1$，矛盾，落在 $W_2$ 中同理矛盾。因此必有一个包含另一个。

区分点：交集要验证同一个向量同时满足两套封闭性；并集的反向证明必须选取分别只属于一边的两个向量。

**L8-06**
**答案：** 复合过渡矩阵为
$$R=PQ=\begin{pmatrix}3&1\\1&-1\end{pmatrix}.$$ 
因为旧坐标 $\boldsymbol x=R\boldsymbol z$，所以对 $\boldsymbol x=(5,-1)^{\mathsf T}$ 解得 $\boldsymbol z=(1,2)^{\mathsf T}$。

区分点：连续换两次基时，先后的过渡矩阵按 $PQ$ 相乘，坐标变换仍由“新坐标送回旧坐标”的方程确定。

**L8-07**
**答案：** 四个空间的维数依次为
$$\dim C(A)=2,\quad \dim C(A^{\mathsf T})=2,\quad \dim N(A)=4-2=2,\quad \dim N(A^{\mathsf T})=1.$$ 
由 $\boldsymbol b\in C(A)$ 当且仅当它与左零空间正交，方程有解当且仅当 $b_1+b_2-b_3=0$。

区分点：已知秩和左零空间时，四个维数由公式得到，可解条件由正交关系得到。

**L8-08**
**答案：** $t=1$。第三行与前两行的和相比只差最后一个分量，因此 $t=1$ 时秩为 $2$，$\dim N(A_t)=4-2=2$；此时
$$N(A_1)=\operatorname{span}\{(-1,0,1,0)^{\mathsf T},(0,-1,0,1)^{\mathsf T}\}.$$
当 $t\ne1$ 时三行无关，秩为 $3$，零空间维数只有 $1$。

区分点：参数先改变秩，再由列数减秩求零化度；不能看到三行三列就直接把秩当成 3。

**L8-09**
**答案：** 行最简形为
$$R=\begin{pmatrix}1&0&-2&-1\\0&1&1&1\\0&0&0&0\end{pmatrix}.$$ 
所以主元列为第 1、2 列，列空间的一组基要取原矩阵的
$(1,0,1)^{\mathsf T},(2,1,3)^{\mathsf T}$。行空间的一组基可取 $R$ 的两行；零空间由 $x_1=2x_3+x_4$、$x_2=-x_3-x_4$ 得基 $(2,-1,1,0)^{\mathsf T},(1,-1,0,1)^{\mathsf T}$；左零空间为 $\operatorname{span}\{(1,1,-1)^{\mathsf T}\}$。这是因为行变换保留列之间的线性关系，却不保留列向量本身。

区分点：列空间取原矩阵的主元列，行空间取行最简形的非零行，两者不能都从行最简形直接读。

### C 提高

**L8-10**
**答案：** 令旧坐标、新坐标都为 $\boldsymbol y$，则需满足 $P\boldsymbol y=\boldsymbol y$，即
$$(P-E)\boldsymbol y=0.$$
解得 $\boldsymbol y=s(-1,1,0)^{\mathsf T}$。当 $s\ne0$ 时得到全部非零向量；因为两套坐标相同，它们的旧坐标也是
$s(-1,1,0)^{\mathsf T}$。

区分点：不能把“坐标相同”误读成向量等于零，而要解 $(P-E)\boldsymbol y=\boldsymbol 0$，再去掉零解。

**L8-11**
**答案：** 取
$$A=\begin{pmatrix}1&-1&0&0\\0&0&1&-1\end{pmatrix}.$$
它的两行都正交于给定的两个生成向量，且秩为 $2$，所以 $\dim N(A)=4-2=2$，从而 $N(A)=N$。四个子空间的基可取
$$C(A):\ (1,0)^{\mathsf T},(0,1)^{\mathsf T};\quad C(A^{\mathsf T}):\ (1,-1,0,0)^{\mathsf T},(0,0,1,-1)^{\mathsf T};$$
$$N(A):\ (1,1,0,0)^{\mathsf T},(0,0,1,1)^{\mathsf T};\quad N(A^{\mathsf T})=\{0\},\quad \text{其基为 }\varnothing，\dim N(A^{\mathsf T})=0.$$
这里给出的是一种可行构造，其他取自 $N^\perp$ 的行基也可以。由于 $C(A)=\mathbb R^2$，$A\boldsymbol x=\boldsymbol b$ 对每个 $\boldsymbol b\in\mathbb R^2$ 都有解。两行是正交补的一组基，且少于两行不可能得到秩 $2$，所以行数最少。

区分点：由零空间反造矩阵要取其正交补作行空间，还要用零化度核对没有遗漏约束。

### 章末混合练习

**L8-12**
**答案：** 任取 $\boldsymbol w=s(1,0,1)^{\mathsf T}+t(0,1,1)^{\mathsf T}=(s,t,s+t)^{\mathsf T}$。交集还需满足 $s-t=0$，所以
$$W\cap U=\operatorname{span}\{(1,1,2)^{\mathsf T}\},\qquad \dim(W\cap U)=1.$$
这里先用 $W$ 的两个生成向量写出一般元素，再施加 $U$ 的方程，因此始终只在 $W$ 内求解，没有把 $W$ 当成整个 $\mathbb R^3$。

（用到方法 1、2，以及线性方程组的参数表示。）

区分点：交集要求同时满足“属于 $W$”和“满足 $U$ 的方程”，漏掉任一条件都会得到过大的集合。

**L8-13**
**答案：** 在 $(1,t,t^2)$ 下，$T(1)=t$、$T(t)=1$、$T(t^2)=2t$，所以
$$A=\begin{pmatrix}0&1&0\\1&0&2\\0&0&0\end{pmatrix}.$$
新基相对旧基的矩阵为
$P=\begin{pmatrix}1&1&0\\1&-1&0\\0&0&1\end{pmatrix}$。它的行列式为 $-2\ne0$，所以 $(1+t,1-t,t^2)$ 确实是一组基；故
$$B=P^{-1}AP=\begin{pmatrix}1&0&1\\0&-1&-1\\0&0&0\end{pmatrix}.$$

（用到方法 6、7。）

区分点：先把抽象多项式的像翻成旧基坐标，再用 $P^{-1}AP$ 译回新坐标；直接在多项式式子上排系数容易把换基方向写反。

**L8-14**
**答案：** 消元得 $x_1-x_3=-1$、$x_2+x_3=1$，故全部解为
$$\boldsymbol x=(-1+s,1-s,s)^{\mathsf T},\quad s\in\mathbb R.$$
一般右端的第二行是第一行的 2 倍，所以有解当且仅当 $b_2=2b_1$。此外
$$N(A)=\operatorname{span}\{(1,-1,1)^{\mathsf T}\},\qquad N(A^{\mathsf T})=\operatorname{span}\{(-2,1,0)^{\mathsf T}\}.$$

（用到方法 4、5，以及线性方程组。）

区分点：先分离一致性条件再写参数解；左零空间检验的是右端 $\boldsymbol b$，不能拿零空间的向量去检验。

