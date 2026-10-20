| 提示 | 内容 |
|---|---|
| SVD 的样子 | $A=U\Sigma V^{\mathsf T}$：$A\boldsymbol v_i=\sigma_i\boldsymbol u_i$，$U$、$V$ 正交，$\Sigma$ 与 $A$ 同形状，对角线 $\sigma_1\ge\sigma_2\ge\cdots\ge0$ |
| 几何 | 转一下（$V^{\mathsf T}$），沿坐标轴伸缩（$\Sigma$），再转一下（$U$）；单位圆变成半轴为 $\sigma_i$、轴方向为 $\boldsymbol u_i$ 的椭圆 |
| 怎样算 | $A^{\mathsf T}A$ 的特征值 $\lambda_i$ → $\sigma_i=\sqrt{\lambda_i}$；单位正交特征向量 → $\boldsymbol v_i$；$\boldsymbol u_i=A\boldsymbol v_i/\sigma_i$ |
| 补 $U$ | $r<m$ 时解 $\boldsymbol u_1^{\mathsf T}\boldsymbol y=\cdots=\boldsymbol u_r^{\mathsf T}\boldsymbol y=0$，正交化、单位化 |
| 易错：配对 | $\boldsymbol u_i$ 必须由 $\boldsymbol v_i$ 算出；分别求 $AA^{\mathsf T}$、$A^{\mathsf T}A$ 的特征向量会配错符号 |
| 易错：特征值 | 奇异值一般不等于特征值；对称半正定时相等；剪切特征值 1、1，奇异值 1.618、0.618 |
| 列正交 | 奇异值就是列长，$\boldsymbol v=\boldsymbol e_j$，$\boldsymbol u=$ 列 / 列长 |
| 秩 1 矩阵 | $\boldsymbol a\boldsymbol b^{\mathsf T}$：$\sigma_1=\lVert\boldsymbol a\rVert\lVert\boldsymbol b\rVert$，$\boldsymbol u_1=\boldsymbol a/\lVert\boldsymbol a\rVert$，$\boldsymbol v_1=\boldsymbol b/\lVert\boldsymbol b\rVert$ |
| 外积展开与秩 | $A=\sum_{i\le r}\sigma_i\boldsymbol u_i\boldsymbol v_i^{\mathsf T}$；$r(A)=$ 非零奇异值个数；方阵可逆 $\iff$ 奇异值全大于 0 |
| 四个子空间 | $C(A)$：$\boldsymbol u_{1..r}$；$N(A^{\mathsf T})$：$\boldsymbol u_{r+1..m}$；$C(A^{\mathsf T})$：$\boldsymbol v_{1..r}$；$N(A)$：$\boldsymbol v_{r+1..n}$ |
| 伪逆 | $A^+=\sum_{i\le r}\frac1{\sigma_i}\boldsymbol v_i\boldsymbol u_i^{\mathsf T}$；$\boldsymbol x^+=A^+\boldsymbol b$ 是长度最小的最小二乘解，在行空间里；一般 $A^+A\ne E$ |
| 两种范数 | $\lVert A\rVert_2=\sigma_1$（$A^{\mathsf T}A$ 的瑞利商）；$\lVert A\rVert_F^2=\sum a_{ij}^2=\operatorname{tr}(A^{\mathsf T}A)=\sum\sigma_i^2$ |
| 截断 | 最佳秩 $k$ 近似是前 $k$ 层 $A_k$；$\lVert A-A_k\rVert_2=\sigma_{k+1}$，$\lVert A-A_k\rVert_F^2=\sigma_{k+1}^2+\cdots+\sigma_r^2$ |
| 正交左乘 | $Q$ 正交时 $QA$ 与 $A$ 奇异值相同：$(QA)^{\mathsf T}QA=A^{\mathsf T}A$ |
| 主成分 | 中心化得 $X$；主方向是 $X$ 的右奇异向量 $\boldsymbol v_i$；综合指标 $X\boldsymbol v_i$；保留比例 $\sum_{i\le k}\sigma_i^2/\sum\sigma_i^2$ |
