## L.13 · 实对称矩阵（速记）

| 提示 | 内容 |
|---|---|
| 图景 | 对称矩阵 = 沿几条互相垂直的方向各自伸缩；$A=Q\Lambda Q^{\mathsf T}$：转过去，沿坐标轴伸缩，再转回来 |
| 特征值是实数（四步） | ① 取共轭 $A\bar{\boldsymbol v}=\bar\lambda\bar{\boldsymbol v}$ ② 右算 $\bar{\boldsymbol v}^{\mathsf T}A\boldsymbol v=\lambda\bar{\boldsymbol v}^{\mathsf T}\boldsymbol v$ ③ 用 $A^{\mathsf T}=A$ 左算得 $\bar\lambda\bar{\boldsymbol v}^{\mathsf T}\boldsymbol v$ ④ 相减，$\bar{\boldsymbol v}^{\mathsf T}\boldsymbol v=\sum\lvert v_i\rvert^2>0$ |
| 方法 1 的变式 | 反对称 $A^{\mathsf T}=-A$：特征值 0 或纯虚数；正交 $Q^{\mathsf T}Q=E$：$\lvert\lambda\rvert=1$；复向量不能用 $\boldsymbol v^{\mathsf T}\boldsymbol v$（可能为 0） |
| 搬家恒等式 | $(A\boldsymbol x)\cdot\boldsymbol y=\boldsymbol x\cdot(A^{\mathsf T}\boldsymbol y)$；对称时可自由搬家 |
| 不同特征值的特征向量正交 | $\lambda_1(\boldsymbol x\cdot\boldsymbol y)=(A\boldsymbol x)\cdot\boldsymbol y=\boldsymbol x\cdot(A\boldsymbol y)=\lambda_2(\boldsymbol x\cdot\boldsymbol y)$；同一特征值的不一定正交 |
| 方法 2 | 缺一个单根的特征向量：解「与已知特征向量都正交」的方程组，不必知道 $A$；重根特征空间 = 其余特征向量的正交补 |
| 谱定理 | 对称 $\Leftrightarrow$ 存在正交 $Q$ 使 $Q^{\mathsf T}AQ=\Lambda$；证明思路：取单位特征向量，与它垂直的子空间被送回自己，一次剥掉一个方向 |
| 推论 | 对称矩阵几何重数 = 代数重数；两个对称矩阵特征值（含重数）相同 $\Rightarrow$ 相似 |
| 方法 3（判相似） | 都对称只比特征值；一对称一不对称：不对称的不能对角化就不相似 |
| 方法 4（五步） | 特征值 → 基础解系 → 重根在特征空间内施密特正交化 → 全部单位化 → 排成 $Q$，$\Lambda$ 同顺序 |
| 易错 | 重根的基不正交化、或忘了单位化，$Q$ 不是正交矩阵，不能用 $Q^{\mathsf T}$ 代 $Q^{-1}$ |
| 谱分解 | $A=\sum\lambda_i\boldsymbol q_i\boldsymbol q_i^{\mathsf T}$，$\boldsymbol q_i\boldsymbol q_i^{\mathsf T}\boldsymbol x=(\boldsymbol q_i\cdot\boldsymbol x)\boldsymbol q_i$ 是投影；拆、乘、加；$A^k=\sum\lambda_i^k\boldsymbol q_i\boldsymbol q_i^{\mathsf T}$；未单位化时除以 $\lVert\boldsymbol v\rVert^2$ |
| 方法 5（两个特征值） | $\mu$ 单根、单位特征向量 $\boldsymbol q$，其余是 $\lambda$：$A=\lambda E+(\mu-\lambda)\boldsymbol q\boldsymbol q^{\mathsf T}$ |
| 协方差与主方向 | $C=\frac1m\sum\boldsymbol x_k\boldsymbol x_k^{\mathsf T}$（中心化）；沿单位 $\boldsymbol u$ 的方差 $\boldsymbol u^{\mathsf T}C\boldsymbol u=\sum\lambda_i(\boldsymbol q_i\cdot\boldsymbol u)^2$，最大值是最大特征值 |
