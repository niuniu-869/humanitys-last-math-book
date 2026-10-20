## L.14 · 二次型与正定（速记）

| 提示 | 内容 |
|---|---|
| 图景 | 正定 = 开口朝上的碗（等高线是椭圆），不定 = 马鞍，半正定而不正定 = 槽；条件数大 = 窄长的山谷 |
| 二次型的矩阵 | $f=\boldsymbol{x}^{\mathsf T}A\boldsymbol{x}$，$A$ 对称：平方项系数放对角线，交叉项 $x_ix_j$ 的系数对半分到 $(i,j)$、$(j,i)$；给的 $B$ 不对称时换成 $\frac12(B+B^{\mathsf T})$，二次型的秩按它算 |
| 正交变换化标准形 | $\boldsymbol{x}=Q\boldsymbol{y}$ 得 $f=\boldsymbol{y}^{\mathsf T}(Q^{\mathsf T}AQ)\boldsymbol{y}=\sum\lambda_iy_i^2$；系数是特征值，$Q$ 的列是单位正交特征向量（主轴），次序一一对应 |
| 合同 | 可逆换元 $\boldsymbol{x}=C\boldsymbol{y}$ 把 $A$ 变成 $C^{\mathsf T}AC$；合同保持对称和秩；配方法给出的也是一种标准形 |
| 惯性定理 | 正、负系数个数 $p$、$q$ 不随化法改变，$p+q=$ 秩；$p$、$q$ 就是正、负特征值的个数；规范形 $w_1^2+\cdots+w_p^2-w_{p+1}^2-\cdots-w_{p+q}^2$ |
| 等价、相似、合同 | 等价看秩；实对称时相似看特征值、合同看 $p,q$；实对称矩阵相似 ⇒ 合同 ⇒ 等价；合同推不出相似（$E$ 与 $2E$） |
| 正定的等价条件 | $\boldsymbol{x}^{\mathsf T}A\boldsymbol{x}>0\ (\boldsymbol{x}\ne\boldsymbol{0})$ ⇔ 特征值全正 ⇔ $p=n$ ⇔ $A=C^{\mathsf T}C$（$C$ 可逆）⇔ 顺序主子式全正（负定：$(-1)^kD_k>0$）；主元 $d_k=D_k/D_{k-1}$ 就是配方系数 |
| 正定的必要条件 | $a_{ii}>0$，$\lvert A\rvert>0$；对角线上有一个 $\le0$ 的数就不正定 |
| 保持正定的运算 | $A+B$、$kA\ (k>0)$、$A^{-1}$、$A^k\ (k\in\mathbb{N}^*)$、伴随矩阵 $A^*$、$C^{\mathsf T}AC\ (C$ 可逆$)$；$AB$ 不一定 |
| 半正定 | ⇔ 特征值全 $\ge0$；$A^{\mathsf T}A$、$\boldsymbol{a}\boldsymbol{a}^{\mathsf T}$ 总半正定；$A$ 列满秩时 $A^{\mathsf T}A$ 正定；$kE+A^{\mathsf T}A\ (k>0)$ 总正定 |
| 易错：半正定 | 顺序主子式全 $\ge0$ 推不出半正定，反例 $\operatorname{diag}(0,-1)$；判半正定用特征值 |
| 瑞利商 | $\lambda_{\min}\lVert\boldsymbol{x}\rVert^2\le\boldsymbol{x}^{\mathsf T}A\boldsymbol{x}\le\lambda_{\max}\lVert\boldsymbol{x}\rVert^2$；球面 $\lVert\boldsymbol{x}\rVert=r$ 上最值是 $\lambda r^2$；条件数 $\kappa=\lambda_{\max}/\lambda_{\min}$ |
| 梯度公式 | $\nabla(\boldsymbol{a}^{\mathsf T}\boldsymbol{x})=\boldsymbol{a}$，$\nabla(\boldsymbol{x}^{\mathsf T}A\boldsymbol{x})=(A+A^{\mathsf T})\boldsymbol{x}$；$\frac12\boldsymbol{x}^{\mathsf T}A\boldsymbol{x}-\boldsymbol{b}^{\mathsf T}\boldsymbol{x}$ 的梯度 $A\boldsymbol{x}-\boldsymbol{b}$、Hessian $A$；$\nabla\lVert A\boldsymbol{x}-\boldsymbol{b}\rVert^2=2A^{\mathsf T}(A\boldsymbol{x}-\boldsymbol{b})$ |
| $n$ 元泰勒公式 | $f(\boldsymbol{x}+\boldsymbol{h})=f(\boldsymbol{x})+\nabla f(\boldsymbol{x})^{\mathsf T}\boldsymbol{h}+\frac12\boldsymbol{h}^{\mathsf T}H(\boldsymbol{x}+\theta\boldsymbol{h})\boldsymbol{h}$ |
| 极值判别 | 驻点处 $H$ 正定 → 极小，负定 → 极大，不定 → 鞍点（找一正一负两个方向），半定且奇异 → 此法失效 |
