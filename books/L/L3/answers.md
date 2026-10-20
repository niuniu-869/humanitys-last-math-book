## L.3 · 矩阵是线性变换（答案）

### A 基础

**L3-01**

**答案：** 有定义，$A$ 是 $2\times3$ 矩阵而 $\boldsymbol{x}$ 有 3 个分量；结果为 $(4,6)^{\mathsf T}$。

按行得 $1\cdot2+(-2)(-1)=4$，$2\cdot2-1+3=6$。按列写成
$$2(1,2)^{\mathsf T}+(-1)(-2,1)^{\mathsf T}+1(0,3)^{\mathsf T}=(4,6)^{\mathsf T}.$$

区分点：先查 $A$ 的列数 3 等于 $\boldsymbol x$ 的分量数 3 才能乘；按列写时，系数是 $\boldsymbol x$ 的分量，配的是 $A$ 的各列。

**L3-02**

**答案：** (A)。矩阵的两列分别是 $A\boldsymbol e_1=(0,1)^{\mathsf T}$ 与 $A\boldsymbol e_2=(-1,0)^{\mathsf T}$，所以这是逆时针旋转 $90^\circ$，单位正方形仍是保持边长的正方形。

区分点：第 $j$ 列才是 $\boldsymbol e_j$ 的像。(B) 把第一行当成像，转向读反了；(C) 只看对角元，丢了非对角元；(D) 把两列垂直误当成压扁，其实两列垂直且等长，正方形只是转了 $90^\circ$。

**L3-03**

**答案：** (B)。两个分量都是输入分量的常数倍之和，所以满足可加性和齐次性；其余各项分别含常数、乘积或绝对值。

区分点：(B) 的每个分量都是常数倍之和。(A) 有常数项，$T(\boldsymbol0)\ne\boldsymbol0$；(C) 的乘积 $xy$ 使 $T(2,2)=(4,2)\ne2T(1,1)=(2,2)$；(D) 的绝对值使 $T(-1,0)=(1,0)\ne-T(1,0)$。

**L3-04**

**答案：** 只有 $AP$ 有定义，因为 $A$ 是 $2\times3$、$P$ 是 $3\times3$，所以 $AP$ 是 $2\times3$；$PA$ 要求 $P$ 的列数 3 等于 $A$ 的行数 2，不成立。直接计算
$$AP=\begin{pmatrix}\frac12&\frac12&0\\\frac12&\frac12&0\end{pmatrix}.$$
因此两个次序不能都当作复合矩阵，次序必须先检查维数。

区分点：$AP$ 是 $(2\times3)(3\times3)$，内侧相等；$PA$ 是 $(3\times3)(2\times3)$，内侧不等、无定义。$AP$ 表示先做 $P$ 再做 $A$。

**L3-05**

**答案：** (C)，输出为 $(0,2)^{\mathsf T}$。矩阵部分给出 $(-1,4)^{\mathsf T}$，加上偏置得到 $(0,2)^{\mathsf T}$；又因 $T(\boldsymbol0)=(1,-2)^{\mathsf T}\ne\boldsymbol0$，所以 $T$ 不线性。

区分点：输出 $(-1,4)^{\mathsf T}+(1,-2)^{\mathsf T}=(0,2)^{\mathsf T}$，选 (C)。(A) 漏看常数项；(B) 漏加常数项，算错输出；(D) 把常数项当输出。带常数项的 $W\boldsymbol x+\boldsymbol b$ 把原点送到 $\boldsymbol b\ne\boldsymbol0$，不是线性变换。

### B 进阶

**L3-06**

**答案：** 取
$$C=\begin{pmatrix}0&1\\0&0\end{pmatrix}\ne O,$$
则
$$CA=\begin{pmatrix}0&0\\0&0\end{pmatrix}=O.$$
题设中的 $A,B$ 都非零而 $AB=O$，所以不能从 $AB=O$ 约去 $A$ 得到 $B=O$；矩阵乘法存在非零零因子。

区分点：$CA$ 的第 1 列是 $C$ 的第 1 列、第 2 列是零，所以只要 $C$ 的第 1 列为零，例如 $C=\begin{pmatrix}0&1\\0&0\end{pmatrix}$；$A$ 把 $\boldsymbol e_2$ 方向压到原点、丢了信息，所以不能约去。

**L3-07**

**答案：** 只有 (A) 成立。分配律总给出
$$(A+B)^2=A^2+AB+BA+B^2.$$
本题 $AB\ne BA$，所以 $AB+BA$ 不能写成 $2AB$，(B) 不成立。直接展开
$$(A-B)(A+B)=A^2+AB-BA-B^2,$$
$$(A+B)(A-B)=A^2-AB+BA-B^2,$$
两式都不等于 $A^2-B^2$，所以 (C)、(D) 都不成立。

区分点：展开时保持次序，只有 (A) 对任意方阵成立；(B)、(C)、(D) 都要把 $BA$ 换成 $AB$，暗中用了可交换。

**L3-08**

**答案：** 由 $A^2=4A-3E$，先得
$$A^3=4A^2-3A=13A-12E,$$
$$A^4=13A^2-12A=40A-39E.$$
再降一次：
$$A^5=40A^2-39A=40(4A-3E)-39A=121A-120E.$$

区分点：每次左乘 $A$ 后立刻把 $A^2$ 换成 $4A-3E$：$A^3=13A-12E$，$A^4=40A-39E$，$A^5=121A-120E$，全程不需要知道 $A$ 本身。

**L3-09**

**答案：** 对 $i>j$，因为 $A,B$ 上三角，$a_{ik}$ 只有在 $k\ge i$ 时可能非零，$b_{kj}$ 只有在 $k\le j$ 时可能非零；而 $i>j$ 时不存在同时满足 $i\le k\le j$ 的 $k$，所以
$$(AB)_{ij}=\sum_{k=1}^n a_{ik}b_{kj}=0.$$
因此 $AB$ 仍是上三角矩阵。对角元取 $i=j$ 时，只有 $k=i$ 可能非零，所以
$$(AB)_{ii}=a_{ii}b_{ii}.$$

区分点：要说清下标范围：$a_{ik}$ 只在 $k\ge i$、$b_{kj}$ 只在 $k\le j$ 时可能非零，$i>j$ 时这样的 $k$ 不存在。

**L3-10**

**答案：**
$$A=\begin{pmatrix}2&0&1\\4&0&2\\-2&0&-1\end{pmatrix}.$$
外积的第 $j$ 列等于 $\beta_j\boldsymbol\alpha$（读列：$A\boldsymbol e_j=\boldsymbol\alpha(\boldsymbol\beta^{\mathsf T}\boldsymbol e_j)$），所以每一列都是 $\boldsymbol\alpha$ 的倍数，第 2 列是 $\beta_2\boldsymbol\alpha=\boldsymbol 0$。又
$$\boldsymbol\beta^{\mathsf T}\boldsymbol\alpha=2\cdot1+0\cdot2+1\cdot(-1)=1,$$
所以 $A^2=A$，从而 $A^4=A$。

区分点：外积的第 $j$ 列是 $\beta_j\boldsymbol\alpha$；$\boldsymbol\beta^{\mathsf T}\boldsymbol\alpha=1$ 是一个数，所以 $A^n=A$，把它当矩阵或漏掉 $n-1$ 次方都会错。

### C 提高

**L3-11**

**答案：**
$$RX=\begin{pmatrix}-c&-d\\a&b\end{pmatrix},\qquad XR=\begin{pmatrix}b&-a\\d&-c\end{pmatrix}.$$
比较对应元素得 $c=-b$、$d=a$，因此全部解为
$$X=\begin{pmatrix}a&b\\-b&a\end{pmatrix}.$$
其中 $X^{\mathsf T}=X$ 当且仅当 $b=0$，所以对称的只有 $aE$。

区分点：比较 $RX$ 与 $XR$ 的四个元素得 $c=-b$、$d=a$；再要求对称，$b=-b$ 迫使 $b=0$，只剩数量矩阵 $aE$。

**L3-12**

**答案：** 分块对角矩阵的幂逐块计算。旋转块满足
$$R^n=\begin{pmatrix}\cos(n\pi/2)&-\sin(n\pi/2)\\\sin(n\pi/2)&\cos(n\pi/2)\end{pmatrix}.$$
又 $J=-E+N$，$-E$ 与 $N$ 可交换且 $N^2=O$，二项式展开只剩两项，所以
$$J^n=\begin{pmatrix}(-1)^n&2n(-1)^{n-1}\\0&(-1)^n\end{pmatrix}.$$
于是
$$M^n=\begin{pmatrix}R^n&O\\O&J^n\end{pmatrix}.$$
特别地，$R^4=E$，故
$$M^4=\begin{pmatrix}1&0&0&0\\0&1&0&0\\0&0&1&-8\\0&0&0&1\end{pmatrix}.$$

区分点：分块对角的幂逐块算；旋转块用几何得 $R^4=E$，幂零块用 $-E+N$ 展开只剩两项，$M^4$ 右下角的 $-8=2\cdot4\cdot(-1)^3$。

### 章末混合练习

**L3-13**

**答案：** 令 $\boldsymbol a=(1,3)^{\mathsf T}$，则
$$P=\frac{\boldsymbol a\boldsymbol a^{\mathsf T}}{\boldsymbol a^{\mathsf T}\boldsymbol a}.$$
于是 $P\boldsymbol x=\dfrac{\boldsymbol a^{\mathsf T}\boldsymbol x}{\boldsymbol a^{\mathsf T}\boldsymbol a}\boldsymbol a$ 正是 L.2 的投影公式。$P\boldsymbol x=\boldsymbol x$ 当且仅当 $\boldsymbol x$ 是 $\boldsymbol a$ 的倍数（右边总是 $\boldsymbol a$ 的倍数；反过来 $P\boldsymbol a=\boldsymbol a$），即直线 $y=3x$ 上的向量保持不动；$P\boldsymbol x=\boldsymbol 0$ 当且仅当 $\boldsymbol a^{\mathsf T}\boldsymbol x=0$，即直线 $x+3y=0$ 上的向量被送到原点。所以 $P$ 是垂直投影到 $y=3x$ 的矩阵。并且
$$P(2,1)^{\mathsf T}=\frac1{10}(1\cdot2+3\cdot1,\ 3\cdot2+9\cdot1)^{\mathsf T}=\frac1{10}(5,15)^{\mathsf T}=\left(\frac12,\frac32\right)^{\mathsf T}.$$

区分点：先认出 $P=\dfrac{\boldsymbol a\boldsymbol a^{\mathsf T}}{\boldsymbol a^{\mathsf T}\boldsymbol a}$ 是投影，再分别解 $P\boldsymbol x=\boldsymbol x$ 与 $P\boldsymbol x=\boldsymbol0$；算 $P(2,1)^{\mathsf T}$ 要两列都用上。

**L3-14**

**答案：** 以 $u,v,w$ 为列组成的矩阵为
$$Q=\begin{pmatrix}1&0&1\\0&1&1\\1&1&0\end{pmatrix}.$$
先用 $u,v,w$ 拼出 $(2,3,4)^{\mathsf T}$：解 $Q\boldsymbol c=(2,3,4)^{\mathsf T}$（三个方程相加得 $c_1+c_2+c_3=\frac92$，再逐个相减），得唯一解
$$ (2,3,4)^{\mathsf T}=\frac32u+\frac52v+\frac12w.$$
由线性性，
$$T(2,3,4)^{\mathsf T}=\frac32(1,0,0)^{\mathsf T}+\frac52(0,1,0)^{\mathsf T}+\frac12(0,0,1)^{\mathsf T}=\left(\frac32,\frac52,\frac12\right)^{\mathsf T}.$$

区分点：先用 $u,v,w$ 拼出 $(2,3,4)^{\mathsf T}$，再用线性逐项送进 $T$；把 $2,3,4$ 直接当作 $T(u),T(v),T(w)$ 的系数会错。

**L3-15**

**答案：** 令 $\boldsymbol a=(2,-1)^{\mathsf T}$，则
$$P=\frac15\begin{pmatrix}4&-2\\-2&1\end{pmatrix},\qquad F=2P-E=\begin{pmatrix}\frac35&-\frac45\\-\frac45&-\frac35\end{pmatrix}.$$
对 $\boldsymbol y=(1,3)^{\mathsf T}$，有
$$F\boldsymbol y=\left(-\frac95,-\frac{13}5\right)^{\mathsf T}.$$
由 $P^2=P$，
$$F^2=(2P-E)^2=4P^2-4P+E=E.$$
因此连续镜像两次恢复原向量，也就是回到原来的点。

区分点：镜像矩阵 $F=2P-E$ 来自「镜像点 = 2×垂足 − 原点」；验证 $F^2=4P^2-4P+E=E$ 用的是 $P^2=P$，不必逐个元素硬算。
