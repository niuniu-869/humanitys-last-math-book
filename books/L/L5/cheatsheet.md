## L.5 · 逆矩阵（速记）

| 提示 | 内容 |
|---|---|
| 定义 | 方阵 $A$，若有 $B$ 使 $AB=BA=E$，则 $A$ 可逆，$A^{-1}=B$；逆矩阵唯一 |
| 只验一边 | 方阵 $AB=E\Rightarrow BA=E$，所以 $B=A^{-1}$ |
| 二阶公式 | $\begin{pmatrix}a&b\\c&d\end{pmatrix}^{-1}=\frac1{ad-bc}\begin{pmatrix}d&-b\\-c&a\end{pmatrix}$；$ad-bc=0$ 时不可逆 |
| 运算律 | $(A^{-1})^{-1}=A$，$(kA)^{-1}=\frac1kA^{-1}$，$(AB)^{-1}=B^{-1}A^{-1}$（先脱鞋再脱袜子），$(A^{\mathsf T})^{-1}=(A^{-1})^{\mathsf T}$ |
| 易错 | $(A+B)^{-1}\ne A^{-1}+B^{-1}$；$(AB)^{-1}\ne A^{-1}B^{-1}$；非方阵没有逆（总有一个乘积不是 $E$） |
| 初等矩阵的逆 | $E(i,j)^{-1}=E(i,j)$，$E(i(k))^{-1}=E(i(\frac1k))$，$E(i,j(k))^{-1}=E(i,j(-k))$ |
| 可逆充要条件 | 可逆 ⇔ $A\boldsymbol{x}=\boldsymbol{0}$ 只有零解 ⇔ $n$ 个主元（行最简形为 $E$）⇔ 初等矩阵之积 |
| 不可逆的证据 | 找到 $\boldsymbol{x}\ne\boldsymbol{0}$ 使 $A\boldsymbol{x}=\boldsymbol{0}$：这个方向被压扁，两点撞在一起（如④、⑤） |
| 消去律 | $A$ 可逆时 $AB=AC\Rightarrow B=C$；$A\boldsymbol{x}=\boldsymbol{b}$ 有唯一解 $A^{-1}\boldsymbol{b}$ |
| 求逆 | $(A\mid E)\xrightarrow{\text{只用行变换}}(E\mid A^{-1})$；左边出现零行则不可逆 |
| 矩阵方程 | $AX=B\Rightarrow X=A^{-1}B$（$(A\mid B)\to(E\mid A^{-1}B)$）；$XA=B\Rightarrow X=BA^{-1}$ |
| 由关系式求逆 | 把关系式改写成 $A\cdot(\cdots)=E$；求 $(A+cE)^{-1}$ 时用多项式除以 $x+c$，余数给出常数 |
| 幂零 | $A^k=O\Rightarrow(E-A)^{-1}=E+A+\cdots+A^{k-1}$ |
| 分块上三角 | $\begin{pmatrix}A_1&C\\O&A_2\end{pmatrix}^{-1}=\begin{pmatrix}A_1^{-1}&-A_1^{-1}CA_2^{-1}\\O&A_2^{-1}\end{pmatrix}$，$C=O$ 时各块分别求逆 |
| 投入产出 | $\boldsymbol{x}=A\boldsymbol{x}+\boldsymbol{d}\Rightarrow\boldsymbol{x}=(E-A)^{-1}\boldsymbol{d}$；第 $j$ 列 = 部门 $j$ 最终需求多 1 元时各部门的总增产 |
