## M.11 · 注意力：QKV 全程手算、为什么除以 √d_k、掩码（速记）

| 提示 | 内容 |
|---|---|
| 单个查询的注意力 | 分数 $s_j=\boldsymbol q\cdot\boldsymbol k_j$ → softmax 得权重 $\alpha_j$（非负、和为 1）→ 对值加权平均 $\sum\alpha_j\boldsymbol v_j$；每个分量落在各个值对应分量的最小值与最大值之间 |
| Q、K、V | $Q=XW_Q$，$K=XW_K$，$V=XW_V$；$X\in\mathbb R^{n\times d}$，$Q,K\in\mathbb R^{n\times d_k}$，$V\in\mathbb R^{n\times d_v}$；查询与键必须同维，值的维数可以不同 |
| 三个角色 | 查询：我要找什么；键：我能被怎样找到；值：被找到后我给出什么；同一个词的 $\boldsymbol q,\boldsymbol k,\boldsymbol v$ 一般互不相同 |
| 矩阵形式 | $\mathrm{softmax}(QK^{\mathsf T}/\sqrt{d_k})V$；原始分数 $U=QK^{\mathsf T}$，缩放分数 $S=U/\sqrt{d_k}$，都是 $n\times n$；对 $S$ 逐行 softmax，输出 $n\times d_v$ |
| 计算量 | $QK^{\mathsf T}$ 约 $2n^2d_k$ 次乘加，$AV$ 约 $2n^2d_v$ 次；序列长度翻倍，计算量变 4 倍；但同一层输入给定后各位置可以并行 |
| 老朋友③ | $QK^{\mathsf T}=\begin{pmatrix}1&0&1\\2&1&3\\3&1&4\end{pmatrix}$；$A$ 第 1 行 $(0.4011,0.1978,0.4011)$；输出第 3 行 $(0.9257,0.6943)$ |
| 为什么除以 $\sqrt{d_k}$ | 全部分量相互独立、零均值、单位方差时 $\mathrm{Var}(\boldsymbol q\cdot\boldsymbol k)=d_k$（每项方差 1，$d_k$ 项相加）；除以标准差 $\sqrt{d_k}$ 让方差回到 1；均值非零则方差变大（均值 1 时是 $3d_k$），不独立也不成立（$\boldsymbol k=\boldsymbol q$ 取 $\pm1$ 时方差为 0） |
| softmax 饱和 | $\partial p_i/\partial z_j=p_i(\delta_{ij}-p_j)$；某个 $p_i\approx1$ 其余趋于 0 时 $J=\mathrm{diag}(\boldsymbol p)-\boldsymbol p\boldsymbol p^{\mathsf T}$ 的元素都趋于 0，这一路导数很小；不缩放的 $(16,8,0)$ 给出 $(0.9997,0.0003,0)$ |
| 缩放量选 $\sqrt{d_k}$ | 除以 $d_k$ 会把分数压得太平，权重更容易接近均匀；缩放量应是标准差，不是方差 |
| 因果掩码 | softmax 前把 $S_{ij}$（$j>i$）设成 $-\infty$，权重为 0，行和仍为 1；位置 $i$ 的输出只依赖 $j\le i$；各位置共享参数、可并行，只给 $n$ 个词时有 $n-1$ 个带目标的位置 |
| 先遮还是后遮 | 先 softmax 再置 0，行和小于 1，需再除以行和才与先遮相同；实际做法是先遮再 softmax |
| 交叉注意力 | $Q$ 来自译文（$m$ 个位置），$K,V$ 来自原文（$n$ 个位置）；$S$ 是 $m\times n$，输出 $m\times d_v$；原文各位置都允许读取时不需要因果掩码 |
| 高频易错 | 混淆 $QK^{\mathsf T}$ 与 $K^{\mathsf T}Q$ 的形状；softmax 对列做而不是对行；忘了缩放；把掩码加在 softmax 之后；交叉注意力中 $Q,K$ 的来源写反 |
