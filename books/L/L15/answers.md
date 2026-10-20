## L.15 · 奇异值分解（答案）

**L15-01**
**答案：** 奇异值为 $2,\sqrt2$。可取
$$U=\begin{pmatrix}0&1/\sqrt2&1/\sqrt2\\0&1/\sqrt2&-1/\sqrt2\\1&0&0\end{pmatrix},\quad\Sigma=\begin{pmatrix}2&0\\0&\sqrt2\\0&0\end{pmatrix},\quad V=\begin{pmatrix}0&1\\1&0\end{pmatrix}.$$
因为第二列长度为 $2$，第一列长度为 $\sqrt2$，而两列互相垂直，所以直接按长度排序即可。

区分点：要把奇异值按从大到小重排，同时记得 $U$ 是 $3\times3$。

**L15-02**
**答案：** $A^{\mathsf T}A=\begin{pmatrix}5&4\\4&5\end{pmatrix}$ 的特征值为 $9,1$，故 $\sigma_1=3,\sigma_2=1$。可取 $\boldsymbol v_1=\boldsymbol u_1=(1,1)^{\mathsf T}/\sqrt2$，$\boldsymbol v_2=(1,-1)^{\mathsf T}/\sqrt2$，$\boldsymbol u_2=(-1,1)^{\mathsf T}/\sqrt2$。

区分点：奇异值取非负平方根，左向量由 $A\boldsymbol v_i/\sigma_i$ 配出。

**L15-03**
**答案：** (B)。$A^{\mathsf T}A=\operatorname{diag}(1,4)$，所以奇异值为 $2,1$；(A) 的 $\Sigma$ 形状错，(C) 忽略左右向量的配对，(D) 把行数误当成正奇异值个数。

区分点：先看矩阵形状和秩，再谈奇异值。

**L15-04**
**答案：** 两个外积因子的长度为 $\sqrt5$、$3$，所以非零奇异值为 $3\sqrt5$，秩为 $1$。列空间基为 $(1,2)^{\mathsf T}/\sqrt5$，左零空间基为 $(2,-1)^{\mathsf T}/\sqrt5$；行空间基为 $(2,-2,1)^{\mathsf T}/3$，零空间基可取 $(1,1,0)^{\mathsf T}/\sqrt2$ 与 $(1,-1,-4)^{\mathsf T}/(3\sqrt2)$。

区分点：秩 1 外积要把两个因子的长度都乘进奇异值。

**L15-05**
**答案：** (C)。$\lVert A\rVert_2=4$，$\lVert A\rVert_F=\sqrt{21}$，最佳秩 1 的弗罗贝尼乌斯误差为 $\sqrt{2^2+1^2}=\sqrt5$，最佳秩 2 的谱范数误差为 $1$。

区分点：谱范数读最大奇异值，截断误差从被舍弃的第一层读。

**L15-06**
**答案：** $AA^{\mathsf T}=2E_2$，两个奇异值都是 $\sqrt2$。重复特征值对应整个 $\mathbb R^2$，可协调取 $U=E_2$，于是 $\boldsymbol v_1=A^{\mathsf T}\boldsymbol u_1/\sqrt2=(1,1,0)^{\mathsf T}/\sqrt2$，$\boldsymbol v_2=(1,-1,0)^{\mathsf T}/\sqrt2$，再在 $N(A)$ 中取 $\boldsymbol v_3=(0,0,1)^{\mathsf T}$。因此
$$U=E_2,\quad\Sigma=\begin{pmatrix}\sqrt2&0&0\\0&\sqrt2&0\end{pmatrix},\quad V=\begin{pmatrix}1/\sqrt2&1/\sqrt2&0\\1/\sqrt2&-1/\sqrt2&0\\0&0&1\end{pmatrix}.$$
重复奇异值时，左右基都可在对应子空间内旋转，但必须保持 $A\boldsymbol v_i=\sigma_i\boldsymbol u_i$。

区分点：先用 $AA^{\mathsf T}$ 找左基，再补右零空间，不能只写出两个正奇异向量。

**L15-07**
**答案：** (B)。$A^{\mathsf T}A=5E$，所以两个奇异值都是 $\sqrt5$；其余选项分别混淆了特征值、谱范数和 SVD 的存在条件。

区分点：一般矩阵的特征值不能直接当奇异值。

**L15-08**
**答案：** $(QA)^{\mathsf T}(QA)=A^{\mathsf T}Q^{\mathsf T}QA=A^{\mathsf T}A$，所以两者的 Gram 矩阵相同，特征值相同，奇异值也相同。

区分点：比较 $A^{\mathsf T}A$，不能比较 $QA$ 和 $A$ 的元素。

**L15-09**
**答案：** (A)。$A$ 满行秩，所以 $AA^+=E_2$；又由 SVD，$A^+A$ 是到行空间的正交投影。直接算得
$$A^+A=\frac13\begin{pmatrix}2&-1&1\\-1&2&1\\1&1&2\end{pmatrix}.$$
(B) 把 $3\times3$ 的投影误当成单位矩阵；(C) 阶数写反；(D) 满行秩时应使用 $A^+=A^{\mathsf T}(AA^{\mathsf T})^{-1}$。

区分点：$AA^+$ 投影到列空间，$A^+A$ 投影到行空间。

**L15-10**
**答案：** 三列两两正交，平方长度为 $36,16,4$，所以第一、第二方向可取 $\boldsymbol v_1=(1,0,0)^{\mathsf T}$、$\boldsymbol v_2=(0,1,0)^{\mathsf T}$。保留两个方向时只丢掉第三列，误差平方和为 $4$。任一主方向整体变号只会使对应得分变号，投影后的表和误差不变。

区分点：第二主方向来自第二大奇异值，不能只求第一方向。

**L15-11**
**答案：** 直接最小化
$$f(x_1,x_2,x_3)=(x_1-1)^2+x_2^2+(x_1+x_2)^2$$
得 $x_1=2/3,x_2=-1/3$，而 $x_3$ 任意。因为 $N(A)=\operatorname{span}\{(0,0,1)^{\mathsf T}\}$，长度最小者取 $x_3=0$，即 $\boldsymbol x^+=(2/3,-1/3,0)^{\mathsf T}$。

区分点：不相容时先求投影意义下的最小二乘解，再沿零空间取最短者。

**L15-12**
**答案：** 取 $u_1=v_1=(1,1,0)^{\mathsf T}/\sqrt2$，奇异值为 $4,2,0$，所以
$$A_1=4u_1v_1^{\mathsf T}=\begin{pmatrix}2&2&0\\2&2&0\\0&0&0\end{pmatrix}.$$
误差矩阵的奇异值为 $2,0$，故 $\lVert A-A_1\rVert_2=2$、$\lVert A-A_1\rVert_F=2$。对任意 $\operatorname{rank}(B)\le1$，埃卡特–扬下界给出 $\lVert A-B\rVert_2\ge\sigma_2=2$；取 $B=A_1$ 时等号成立，所以这个下界最佳。

区分点：非对角矩阵先找正交方向，再按奇异值截断。

**L15-13**
**答案：** $A^{\mathsf T}A$ 的最大特征值为 $9$，所以最大值为 $3$。取等号的单位向量为 $\pm(1,1)^{\mathsf T}/\sqrt2$。

区分点：最大值来自最大奇异值，取等号方向来自对应特征空间。

**L15-14**
**答案：** $A^{\mathsf T}A=\begin{pmatrix}2&1\\1&2\end{pmatrix}$，其逆为 $\frac13\begin{pmatrix}2&-1\\-1&2\end{pmatrix}$。因此
$$A(A^{\mathsf T}A)^{-1}A^{\mathsf T}\boldsymbol b=\frac13\begin{pmatrix}2&-1&1\\-1&2&1\\1&1&2\end{pmatrix}\begin{pmatrix}1\\2\\0\end{pmatrix}=\begin{pmatrix}0\\1\\1\end{pmatrix}.$$
该向量在 $C(A)$ 中，它就是第二列 $(0,1,1)^{\mathsf T}$；残差 $\boldsymbol b-\boldsymbol p=(1,1,-1)^{\mathsf T}$ 与两列 $(1,0,1)^{\mathsf T}$、$(0,1,1)^{\mathsf T}$ 的点积都是 0，所以它是列空间上的正交投影。

区分点：满列秩时用 $A(A^{\mathsf T}A)^{-1}A^{\mathsf T}$，并检查残差正交。

**L15-15**
**答案：** $A=\boldsymbol a\boldsymbol c^{\mathsf T}$，其中 $\boldsymbol a=(1,2)^{\mathsf T}$、$\boldsymbol c=(1,1,0)^{\mathsf T}$。取 $u_1=\boldsymbol a/\sqrt5$、$v_1=\boldsymbol c/\sqrt2$、$\sigma_1=\sqrt{10}$，则
$$A^+=\frac1{\sigma_1}v_1u_1^{\mathsf T}=\frac1{10}\begin{pmatrix}1&2\\1&2\\0&0\end{pmatrix}.$$
对 $\boldsymbol b=(1,0)^{\mathsf T}$，$\boldsymbol x^+=A^+\boldsymbol b=(1/10,1/10,0)^{\mathsf T}$。零空间由 $(1,-1,0)^{\mathsf T}$、$(0,0,1)^{\mathsf T}$ 张成，$\boldsymbol x^+$ 与它们都正交，因此是最短的最小二乘解。

区分点：先写 SVD 数据，再由 $A^+=\sigma_1^{-1}v_1u_1^{\mathsf T}$ 求伪逆。
