## L.10 · 正交与最小二乘（速记）

| 提示 | 内容 |
|---|---|
| 最近点判据 | $\boldsymbol p\in S$ 离 $\boldsymbol b$ 最近 ⇔ 残差 $\boldsymbol e=\boldsymbol b-\boldsymbol p$ 与 $S$ 的每个生成向量正交；最近点唯一（勾股：$\lVert\boldsymbol b-\boldsymbol q\rVert^2=\lVert\boldsymbol e\rVert^2+\lVert\boldsymbol p-\boldsymbol q\rVert^2$） |
| 易错：分别投影再相加 | 生成向量不两两正交时，$\boldsymbol b$ 在各个向量上的投影之和不是在子空间上的投影；先正交化或解正规方程 |
| 正规方程 | $A^{\mathsf T}(\boldsymbol b-A\hat{\boldsymbol x})=\boldsymbol 0$，即 $A^{\mathsf T}A\hat{\boldsymbol x}=A^{\mathsf T}\boldsymbol b$；$A^{\mathsf T}A$ 的元是两列的点积，残差 $\boldsymbol e\in N(A^{\mathsf T})$ |
| 何时唯一 | $r(A^{\mathsf T}A)=r(A)$，所以列满秩 ⇔ $A^{\mathsf T}A$ 可逆 ⇔ $\hat{\boldsymbol x}=(A^{\mathsf T}A)^{-1}A^{\mathsf T}\boldsymbol b$ 唯一 |
| 正规方程必有解 | $r(A^{\mathsf T}A)\le r(A^{\mathsf T}A\mid A^{\mathsf T}\boldsymbol b)=r\big(A^{\mathsf T}(A\mid\boldsymbol b)\big)\le r(A^{\mathsf T})=r(A)=r(A^{\mathsf T}A)$；解不唯一时 $\boldsymbol p=A\hat{\boldsymbol x}$ 仍唯一 |
| 投影矩阵 | $P=A(A^{\mathsf T}A)^{-1}A^{\mathsf T}$（列满秩），$P^2=P$，$P^{\mathsf T}=P$；一列时 $P=\frac{\boldsymbol a\boldsymbol a^{\mathsf T}}{\boldsymbol a^{\mathsf T}\boldsymbol a}$，$\boldsymbol a=(1,1)^{\mathsf T}$ 时就是老朋友④；$A$ 不是方阵时不能拆成 $A^{-1}(A^{\mathsf T})^{-1}$ |
| 规范正交组 | $\boldsymbol q_i\cdot\boldsymbol q_j=0\,(i\ne j)$，$=1\,(i=j)$；两两正交的非零向量必线性无关，反之不然（$(1,0),(1,1)$） |
| 正交基下的坐标与投影 | 坐标 $x_j=\boldsymbol q_j\cdot\boldsymbol b$；投影 $\boldsymbol p=\sum(\boldsymbol q_i\cdot\boldsymbol b)\boldsymbol q_i$，$P=QQ^{\mathsf T}$；只正交不单位时系数是 $\frac{\boldsymbol a_i\cdot\boldsymbol b}{\boldsymbol a_i\cdot\boldsymbol a_i}$ |
| 正交矩阵 | 方阵 $Q^{\mathsf T}Q=E$ ⇔ 各列（各行）规范正交；$Q^{-1}=Q^{\mathsf T}$，$\lVert Q\boldsymbol x\rVert=\lVert\boldsymbol x\rVert$，$(Q\boldsymbol x)\cdot(Q\boldsymbol y)=\boldsymbol x\cdot\boldsymbol y$，乘积仍正交 |
| 易错：行列式 | 正交 ⇒ $|Q|=\pm1$，反之不成立（老朋友②剪切 $\begin{pmatrix}1&1\\0&1\end{pmatrix}$）；长度条件只定绝对值，符号要靠两两正交定 |
| 行列式技巧 | 含正交矩阵 $A$ 的行列式，把 $E$ 换成 $A^{\mathsf T}A$ 提出 $A$；$|A|=-1$ ⇒ $|E+A|=0$ |
| 施密特正交化 | $\boldsymbol b_j=\boldsymbol a_j-\sum_{i<j}\frac{\boldsymbol a_j\cdot\boldsymbol b_i}{\boldsymbol b_i\cdot\boldsymbol b_i}\boldsymbol b_i$，减的是在已正交化的 $\boldsymbol b_i$ 上的投影；可随时去分母，最后单位化；张成不变 |
| QR | $A=QR$，$R$ 上三角，$r_{ij}=\boldsymbol q_i\cdot\boldsymbol a_j$，对角元 $\lVert\boldsymbol b_j\rVert>0$；最小二乘化为 $R\hat{\boldsymbol x}=Q^{\mathsf T}\boldsymbol b$ |
| 拟合直线 | 设计矩阵行 $(1,t_i)$；$D=\frac{\sum(t_i-\bar t)(y_i-\bar y)}{\sum(t_i-\bar t)^2}$，$C=\bar y-D\bar t$，直线过 $(\bar t,\bar y)$；残差是竖直方向的差，和为 0，$\sum t_ie_i=0$ |
| 梯度下降 | $f=\lVert\boldsymbol b-A\boldsymbol x\rVert^2$，$\nabla f=-2A^{\mathsf T}\boldsymbol e$（$\boldsymbol e=\boldsymbol b-A\boldsymbol x$），一步 $\boldsymbol x\leftarrow\boldsymbol x+2\eta A^{\mathsf T}\boldsymbol e$；停住处即正规方程的解，$\eta$ 太大会发散 |
