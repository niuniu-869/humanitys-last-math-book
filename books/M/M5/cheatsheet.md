| 提示 | 内容 |
|---|---|
| 中心化与协方差矩阵 | $X_c$ 每列减列平均；$S=\frac1{n-1}X_c^{\mathsf T}X_c\in\mathbb R^{d\times d}$，对称、半正定；对角线是方差，其余是协方差；改除以 $n$ 只差一个常数倍 |
| 投影方差 | 单位向量 $\boldsymbol w$ 上的得分 $\boldsymbol t=X_c\boldsymbol w$，平均 0，方差 $\boldsymbol w^{\mathsf T}S\boldsymbol w$ |
| 拉格朗日推导 | 最大化 $\boldsymbol w^{\mathsf T}S\boldsymbol w$，约束 $\boldsymbol w^{\mathsf T}\boldsymbol w=1$：$\nabla f=2S\boldsymbol w$，$\nabla g=2\boldsymbol w$，得 $S\boldsymbol w=\lambda\boldsymbol w$，函数值 $=\lambda$ |
| 第一主成分 | 方向 $=$ 最大特征值 $\lambda_1$ 的单位特征向量，该方向方差 $=\lambda_1$；也可由 $\sum\lambda_ic_i^2\le\lambda_1$ 验证 |
| 第二主成分 | 加约束 $\boldsymbol w_1^{\mathsf T}\boldsymbol w=0$，乘子 $\mu=0$，仍是特征向量，取第二大特征值；各主成分得分两两不相关 |
| 特征值重复 | 重特征值的特征子空间里任一组正交方向都行，主成分方向不唯一 |
| 贡献率 | $\mathrm{tr}\,S=\sum\lambda_j$（$\mathrm{tr}(Q\Lambda Q^{\mathsf T})=\mathrm{tr}\Lambda$，要求 $\mathrm{tr}\,S>0$）；第 $j$ 个贡献率 $\lambda_j/\sum\lambda_i$，累计贡献率 85%–95% 是常用参考线，不是定理 |
| 重建误差 | 点到过中心、方向 $\boldsymbol w$ 的直线距离平方 $=\lVert\boldsymbol x_c\rVert^2-(\boldsymbol w^{\mathsf T}\boldsymbol x_c)^2$；总误差 $=(n-1)(\mathrm{tr}\,S-\boldsymbol w^{\mathsf T}S\boldsymbol w)$，所以最小误差等价于最大方差；留 $k$ 个时误差 $=(n-1)\times$ 丢掉的特征值之和 |
| PCA 与回归直线 | 回归量竖直距离，$x$ 为输入；PCA 量垂直距离，两指标对等；斜率一般不同（老朋友①：1.7 与 1.748） |
| 标准化 | 指标单位不同或方差悬殊时（标准差为 0 的列先删去），先 $z=(x-\bar x)/s$，在相关矩阵 $R$ 上做 PCA；二阶 $R$ 的特征值 $1\pm r$，方向 $(1,\pm1)/\sqrt2$；同一尺度的指标（如像素）不必标准化 |
| 用 SVD 求 PCA | $X_c=U\Sigma V^{\mathsf T}$：$V$ 的列是主成分方向，$\lambda_j=\sigma_j^2/(n-1)$，得分矩阵 $X_cV=U\Sigma$；比先算 $S$ 稳定（列满秩时 $X_c^{\mathsf T}X_c$ 的条件数是 $X_c$ 的平方）、省空间；$n<d$ 时 $S$ 的秩至多 $n-1$ |
| 手算全流程 | 中心化 → $S$ → 特征值与单位特征向量 → 贡献率定 $k$ → 得分 $X_c\boldsymbol w_j$ → 重建误差；综合指标的权重就是第一主成分方向的各分量（随单位变，单位不同先标准化） |
| 易错点 | 忘了中心化；$S$ 要对称才有 $\nabla=2S\boldsymbol w$（反例 $A=\begin{pmatrix}0&2\\0&0\end{pmatrix}$：$f$ 最大值 1，特征值全 0）；特征向量忘了单位化；方差大不等于对预测有用（PCA 不看标签） |
