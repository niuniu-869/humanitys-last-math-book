## L.12 · 相似与对角化（速记）

| 提示 | 内容 |
|---|---|
| 相似（两把尺子） | $P^{-1}AP=B$（$P$ 可逆）：同一个变换用两把尺子（两组基）记下的矩阵；从右往左读：$P$ 把新坐标翻译成旧坐标，$A$ 做变换，$P^{-1}$ 翻译回来 |
| 相似不变量 | 特征多项式、特征值（含重数）、迹、行列式、秩都相同；特征向量会变：$A$ 的 $\boldsymbol{v}$ 对应 $B$ 的 $P^{-1}\boldsymbol{v}$ |
| 易错：不变量只是必要条件 | $E$ 与剪切 $J=\begin{pmatrix}1&1\\0&1\end{pmatrix}$ 不变量全同却不相似（$J$ 只有一条特征方向）；用迹、行列式求出参数后要回头验证能否对角化 |
| 可对角化 | $\Leftrightarrow$ 有 $n$ 个线性无关的特征向量 $\Leftrightarrow$ 每个特征值的几何重数 = 代数重数；$n$ 个特征值互不相同 $\Rightarrow$ 可对角化 |
| 几何重数 ≤ 代数重数 | 特征空间的基扩充成 $P$ → $P^{-1}AP=\begin{pmatrix}\lambda_0E_g&C\\O&D\end{pmatrix}$ → 特征多项式含 $(\lambda-\lambda_0)^g$ → 相似不改变特征多项式 |
| 方法 2（只查重根） | 单根自动满足；$k$ 重根 $\lambda$ 要求 $n-r(A-\lambda E)=k$；含参数时先看参数让哪个特征值变成重根 |
| 对角化与反求 | 特征向量按列排成 $P$，$\Lambda$ 的对角元按同样顺序填特征值；验算 $AP=P\Lambda$；反求 $A=P\Lambda P^{-1}$ |
| 方法 4 | $A^n=P\Lambda^nP^{-1}$；只要 $A^n\boldsymbol{x}$ 时写 $\boldsymbol{x}=\sum c_i\boldsymbol{p}_i$，$A^n\boldsymbol{x}=\sum c_i\lambda_i^n\boldsymbol{p}_i$，绝对值最大的特征值最终说了算 |
| 秩一矩阵 | $A=\boldsymbol{\alpha}\boldsymbol{\beta}^{\mathsf T}$，$\boldsymbol{\beta}^{\mathsf T}\boldsymbol{\alpha}=\operatorname{tr}A$，$A^n=(\operatorname{tr}A)^{n-1}A$；$\operatorname{tr}A=0$ 时 $A^2=O$，不能对角化 |
| 方法 6（$\lambda_0E+N$） | 二阶、二重特征值 $\lambda_0$、不能对角化：$N=A-\lambda_0E$ 满足 $N^2=O$，$A^n=\lambda_0^nE+n\lambda_0^{n-1}N$ |
| 哈密顿–凯莱 | $f(\lambda)=\lvert\lambda E-A\rvert\Rightarrow f(A)=O$；二阶：$A^2-(\operatorname{tr}A)A+\lvert A\rvert E=O$；用来降次、求 $A^{-1}$ |
| 二阶线性递推 | $\boldsymbol{x}_n=(a_{n+1},a_n)^{\mathsf T}$，$A=\begin{pmatrix}p&q\\1&0\end{pmatrix}$；$\lambda^2=p\lambda+q$ 两根不同：$C_1r_1^n+C_2r_2^n$；二重根 $r\ne0$：$(C_1+C_2n)r^n$；斐波那契 $F_n=\frac{\varphi^n-\psi^n}{\sqrt5}$ |
| 转移矩阵 | 元素非负、列和为 1；1 是特征值；其他特征向量分量和为 0；元素全正时其他 $\lvert\lambda\rvert<1$，稳态与初始占比无关 |
| 方法 9（稳态） | 解 $(M-E)\boldsymbol{x}=\boldsymbol{0}$，缩放成分量和为 1；幂迭代的偏离按其余特征值中最大的 $\lvert\lambda\rvert^n$ 衰减 |
| 易错：行和为 1 | $\boldsymbol{\pi}R=\boldsymbol{\pi}\Leftrightarrow R^{\mathsf T}\boldsymbol{\pi}^{\mathsf T}=\boldsymbol{\pi}^{\mathsf T}$（左特征向量）；直接解 $(R-E)\boldsymbol{x}=\boldsymbol{0}$ 得到的 $(1,\dots,1)^{\mathsf T}$ 是右特征向量，不是稳态 |
