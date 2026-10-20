## L.7 · 线性相关与秩（速记）

| 提示 | 内容 |
|---|---|
| 定义 | 存在不全为零的 $k_i$ 使 $\sum k_i\boldsymbol\alpha_i=\boldsymbol 0$ 为线性相关；只有全零系数才行为线性无关 |
| 三种说法 | 列相关 ⇔ $A\boldsymbol x=\boldsymbol 0$ 有非零解 ⇔ 有非零方向被压到原点；两个以上向量时 ⇔ 至少一个能由其余表示 |
| 判法 | 排成列消元，主元数 < 向量个数则相关；$n$ 个 $n$ 维向量：相关 ⇔ $\lvert A\rvert=0$ |
| 小情形 | 一个向量相关 ⇔ 零向量；两个相关 ⇔ 共线；含零向量必相关 |
| 定义法证无关 | 设组合为零 → 代入已知无关组、合并 → 各系数为零 → 解出 $k_i$ 全为零 |
| 部分与整体、添分量 | 部分相关 ⇒ 整体相关；无关组添分量仍无关，相关组去分量仍相关（去分量 = 看影子，反方向都不成立） |
| 个数大于维数 | $s>n$ 个 $n$ 维向量必相关 |
| 唯一表示 | $\boldsymbol\alpha_1,\dots,\boldsymbol\alpha_s$ 无关、添 $\boldsymbol\beta$ 后相关 ⇒ $\boldsymbol\beta$ 能由它们唯一表示（前提「无关」不能少） |
| 替换定理 | $B=AK$，$K$ 为 $s\times t$，$t>s$ ⇒ $\boldsymbol\beta$ 相关（以少表多，多的必相关）；$\boldsymbol\alpha$ 无关时 $\boldsymbol\beta$ 无关 ⇔ $K\boldsymbol x=\boldsymbol 0$ 只有零解 |
| 易错：$K$ 的写法 | $\boldsymbol\beta_j$ 的系数写成 $K$ 的第 $j$ 列 |
| 求极大无关组 | 排成列，只做行变换到行最简形；主元列对应的原向量是极大无关组，非主元列的数是表示系数；含参数的主元先问是否为 0 |
| 矩阵的秩 | 行秩 = 列秩 = 主元个数 = 不为零子式的最高阶数 = 变换后还剩几维；$r(A^{\mathsf T})=r(A)$；方阵满秩 ⇔ $\lvert A\rvert\ne0$ |
| 易错：无关与正交 | 两两正交的非零向量必无关，无关不一定正交；两两不共线不等于无关 |
| 等价标准形 | $PAQ=\begin{pmatrix}E_r&O\\O&O\end{pmatrix}$；同型矩阵等价 ⇔ 秩相等；向量组等价只推出秩相等，反之不然 |
| 秩的不等式 | $r(AB)\le\min\{r(A),r(B)\}$；乘可逆矩阵秩不变；$r(A+B)\le r(A)+r(B)$；$r(\boldsymbol u\boldsymbol v^{\mathsf T})=1$（$\boldsymbol u,\boldsymbol v\ne\boldsymbol 0$） |
