## L.13 · 实对称矩阵（答案）

### A 基础

**L13-01**
**答案：** 取共轭得 $A\bar{\boldsymbol v}=\bar\lambda\bar{\boldsymbol v}$。同一数从右、左分别计算为 $\lambda\bar{\boldsymbol v}^{\mathsf T}\boldsymbol v$ 与 $-\bar\lambda\bar{\boldsymbol v}^{\mathsf T}\boldsymbol v$。因后面的因子是正实数，所以 $\lambda=-\bar\lambda$，即 $\operatorname{Re}\lambda=0$。给定矩阵的特征方程是 $\lambda^2+4=0$，故特征值为 $\pm2i$。

区分点：左算时必须把 $A^{\mathsf T}=-A$ 用进去。

**L13-02**
**答案：** 设 $\boldsymbol x=(x_1,x_2,x_3)^{\mathsf T}$ 属于 $5$。由正交性，$x_1+x_2=0$，$x_1-x_2+2x_3=0$，所以 $x_2=-x_1,x_3=-x_1$。全部特征向量为 $t(1,-1,-1)^{\mathsf T}$，其中 $t\ne0$。

区分点：先把正交性转成两个点积方程。

**L13-03**
**答案：** (A)、(B)。谱定理给出 (A)，能正交对角化的矩阵写成 $Q\Lambda Q^{\mathsf T}$，所以
$$A^{\mathsf T}=Q\Lambda^{\mathsf T}Q^{\mathsf T}=Q\Lambda Q^{\mathsf T}=A,$$
从而 (B) 正确。(C) 的具体反例是
$$\begin{pmatrix}1&1\\0&2\end{pmatrix},$$
它的特征值全为实数但不对称，不能正交对角化。(D) 的具体反例是单位矩阵 $E$：$(1,0)^{\mathsf T}$ 与 $(1,1)^{\mathsf T}$ 都属于特征值 $1$ 的特征空间，但点积为 $1$，不正交。

区分点：正交可对角化与对称性是充要条件，只有实特征值还不够。

**L13-04**
**答案：** 直接计算得
$$Q^{\mathsf T}A_tQ=\operatorname{diag}(2+t,2-t).$$
当 $t>2$ 时，$2+t>0$ 且 $2-t<0$；按从大到小排列为 $2+t,2-t$。

区分点：参数改变特征值，但给定的两个方向始终是正交单位特征向量。

**L13-05**
**答案：** 写成 $A=2E+\boldsymbol1\boldsymbol1^{\mathsf T}$，其中 $\boldsymbol1=(1,1,1)^{\mathsf T}$。若 $\boldsymbol x\in\boldsymbol q^\perp$，则 $x_1+x_2+x_3=0$，所以
$$\boldsymbol1\boldsymbol1^{\mathsf T}\boldsymbol x=\boldsymbol0,\qquad A\boldsymbol x=2\boldsymbol x.$$
因此正交补上的特征值为 $2$。因为 $(1,-1,0)^{\mathsf T}$ 属于该正交补，
$$A(1,-1,0)^{\mathsf T}=2(1,-1,0)^{\mathsf T}.$$

区分点：先识别矩阵为 $2E+\boldsymbol1\boldsymbol1^{\mathsf T}$，再看正交补上的外积项为零。

### B 进阶

**L13-06**
**答案：** 正交矩阵保持长度，所以
$$\lVert Q\boldsymbol v\rVert^2=\boldsymbol v^{\mathsf T}Q^{\mathsf T}Q\boldsymbol v=\lVert\boldsymbol v\rVert^2.$$
又 $Q\boldsymbol v=\lambda\boldsymbol v$，且 $\boldsymbol v$ 为实向量，所以 $\lambda^2\lVert\boldsymbol v\rVert^2=\lVert\boldsymbol v\rVert^2$，从而 $\lambda^2=1$，即 $\lambda=\pm1$。对旋转矩阵，特征方程为 $\lambda^2+1=0$，没有实根，所以没有非零实特征向量。

区分点：实特征值时可直接用长度平方，旋转矩阵则在第一步就出现复根。

**L13-07**
**答案：** $(1,0)^{\mathsf T}$ 的正交补由 $(0,1)^{\mathsf T}$ 张成，而
$$B_t(0,1)^{\mathsf T}=(t,2)^{\mathsf T}.$$
它仍在该正交补中当且仅当 $t=0$。此时另一个特征值为 $2$。

区分点：正交补自动是不变方向是对称矩阵的结论，参数题要直接检查像是否仍在这条直线上。

**L13-08**
**答案：** 两矩阵都是上三角或对角矩阵，特征多项式都是 $(\lambda-1)^2(\lambda-2)$。但 $A$ 的特征值 $1$ 的特征空间是二维，$B$ 的特征空间只有 $\operatorname{span}\{(1,0,0)^{\mathsf T}\}$，几何重数不同，所以 $A,B$ 不相似。

区分点：特征多项式相同只给出代数重数，还要比较几何重数。

**L13-09**
**答案：** 取基 $\boldsymbol\alpha_1=(1,-1,0)^{\mathsf T}$、$\boldsymbol\alpha_2=(1,0,-1)^{\mathsf T}$。施密特正交化得 $\boldsymbol\beta_1=\boldsymbol\alpha_1$、$\boldsymbol\beta_2=(1,1,-2)^{\mathsf T}$。补上的正交方向是 $(1,1,1)^{\mathsf T}$。单位化后可取
$$Q=\left(\frac{(1,-1,0)^{\mathsf T}}{\sqrt2},\frac{(1,1,-2)^{\mathsf T}}{\sqrt6},\frac{(1,1,1)^{\mathsf T}}{\sqrt3}\right),\quad\Lambda=\operatorname{diag}(2,2,5).$$

区分点：先由方程找出整个特征空间，再在这个空间内正交化。

**L13-10**
**答案：** $A$ 在 $\boldsymbol q$ 方向的特征值为 $5$，在正交补上的特征值为 $2$，所以 $p(A)$ 在这两个方向上的特征值分别为 $p(5)=11$、$p(2)=-1$。令 $\boldsymbol b=(1,2,0)^{\mathsf T}$，则
$$\boldsymbol b_{\parallel}=(-1/3,1/3,-1/3)^{\mathsf T},\quad \boldsymbol b_\perp=(4/3,5/3,1/3)^{\mathsf T},$$
从而 $p(A)\boldsymbol b=11\boldsymbol b_{\parallel}-\boldsymbol b_\perp=(-5,2,-4)^{\mathsf T}$。

区分点：先对输入向量按特征方向分解，再把多项式作用到特征值上。

**L13-11**
**答案：** 均值为 $\boldsymbol\mu=(2,4/3)^{\mathsf T}$，中心化后的三点为 $(-1,-1/3)^{\mathsf T},(1,5/3)^{\mathsf T},(0,-4/3)^{\mathsf T}$。因此
$$C=\frac13\sum(\boldsymbol x_k-\boldsymbol\mu)(\boldsymbol x_k-\boldsymbol\mu)^{\mathsf T}=\begin{pmatrix}2/3&2/3\\2/3&14/9\end{pmatrix}.$$
其特征值为 $\frac{10+2\sqrt{13}}9$ 与 $\frac{10-2\sqrt{13}}9$，所以单位方向上的最大方差为 $\frac{10+2\sqrt{13}}9$。

区分点：必须先减去均值，再按本章的 $1/m$ 约定平均。

### C 提高

**L13-12**
**答案：** 因为 $\mu$ 是单根，$\boldsymbol q$ 张成 $\mu$ 的特征空间；谱定理写成
$$A=\lambda(E-\boldsymbol q\boldsymbol q^{\mathsf T})+\mu\boldsymbol q\boldsymbol q^{\mathsf T}=\lambda E+(\mu-\lambda)P,$$
其中 $P=\boldsymbol q\boldsymbol q^{\mathsf T}$，且 $P^2=P$。因此 $A$ 在 $\boldsymbol q$ 方向乘 $\mu$，在正交补上乘 $\lambda$；连续作用 $k$ 次后得到
$$A^k=\lambda^kE+(\mu^k-\lambda^k)\boldsymbol q\boldsymbol q^{\mathsf T}.$$
严格地说，对 $k=1$ 公式成立。若对某个 $k\ge1$ 成立，右乘 $A$，并用 $P^2=P$、$P(E-P)=0$，得
$$A^{k+1}=\bigl(\lambda^k(E-P)+\mu^kP\bigr)\bigl(\lambda(E-P)+\mu P\bigr)=\lambda^{k+1}(E-P)+\mu^{k+1}P,$$
这正是所需公式，所以由归纳法对所有正整数 $k$ 成立。

区分点：幂作用在特征值上，而不是把外积矩阵当成普通标量。

**L13-13**
**答案：** 若 $A\boldsymbol x=\lambda\boldsymbol x$ 且 $\boldsymbol x\ne0$，则 $A^2\boldsymbol x=\lambda^2\boldsymbol x$；由 $A^2=A$ 得 $\lambda=0$ 或 $1$。由谱定理正交对角化后，秩等于非零对角元的个数，所以秩为 $2$ 表明特征值 $1$ 的重数为 $2$，从而
$$Q^{\mathsf T}AQ=\operatorname{diag}(1,1,0),\qquad |A+E|=4.$$
谱分解说明 $A$ 保留 $1$ 特征空间的分量并消去其正交补分量，所以它是到一个二维子空间的正交投影。

区分点：秩与特征值重数之间要通过正交对角化连接。

**L13-14**
**答案：** $R$ 的特征方程为 $\lambda^2+1=0$，复特征值为 $i,-i$。本章的正交性定理要求矩阵是实对称矩阵，并讨论实特征向量；$R^{\mathsf T}=-R\ne R$，所以条件不满足。由于特征值不是实数，$R$ 没有非零实特征向量。

区分点：先检查定理的条件，不能只因为矩阵是正交矩阵就套用本章结论。

### 章末混合练习

**L13-15**
**答案：** $(1,-1)^{\mathsf T}$ 和 $(1,1)^{\mathsf T}$ 分别属于特征值 $1,3$，所以
$$A^6(1,-1)^{\mathsf T}=(1,-1)^{\mathsf T},\qquad A^6(1,1)^{\mathsf T}=729(1,1)^{\mathsf T}.$$

区分点：先认出输入向量是特征向量，再取幂。

**L13-16**
**答案：** $P=\frac15\begin{pmatrix}1&2\\2&4\end{pmatrix}$。因为 $\boldsymbol q^{\mathsf T}\boldsymbol q=1$，所以 $P^2=P$，并且
$$P(3,4)^{\mathsf T}=\frac15(11,22)^{\mathsf T}.$$

区分点：幂等性来自单位向量的内积为 $1$。

**L13-17**
**答案：** 单根方向为 $\boldsymbol q$，所以
$$A=2(E-\boldsymbol q\boldsymbol q^{\mathsf T})=\frac23\begin{pmatrix}2&-1&-1\\-1&2&-1\\-1&-1&2\end{pmatrix}.$$
由谱分解，$\operatorname{Im}A$ 是非零特征空间，也就是 $\boldsymbol q^\perp$；等价地，对称矩阵满足 $\operatorname{Im}A=(\ker A)^\perp$。右端与 $\boldsymbol q$ 的内积为 $2/\sqrt3\ne0$，所以不在像空间内，方程无解。

区分点：判断线性方程组要检查右端是否属于像空间。

**L13-18**
**答案：** 因为 $Q^{\mathsf T}Q=E$ 且 $\Lambda^{\mathsf T}=\Lambda$，
$$A^{\mathsf T}=(Q\Lambda Q^{\mathsf T})^{\mathsf T}=Q\Lambda^{\mathsf T}Q^{\mathsf T}=Q\Lambda Q^{\mathsf T}=A.$$
按对角元展开迹，或使用循环不变性，得
$$\operatorname{tr}A=\operatorname{tr}(Q\Lambda Q^{\mathsf T})=\operatorname{tr}(\Lambda Q^{\mathsf T}Q)=\operatorname{tr}\Lambda=\lambda_1+\lambda_2+\lambda_3.$$

区分点：转置时反转乘积顺序，迹的化简还要用 $Q^{\mathsf T}Q=E$。
