## L.9 · 线性方程组解的结构（速记）

| 提示 | 内容 |
|---|---|
| 有没有解 | $A\boldsymbol x=\boldsymbol b$ 有解 $\iff r(A)=r(A\mid\boldsymbol b)\iff\boldsymbol b\in C(A)$（$\boldsymbol b$ 在像里） |
| 三种结局 | $r(A)<r(A\mid\boldsymbol b)$ 无解；$r(A)=r(A\mid\boldsymbol b)=n$ 唯一；$=r<n$ 无穷多，$n-r$ 个自由未知量（$n$ 是未知数个数） |
| 齐次方程组 | 有非零解 $\iff r(A)<n$；$m<n$ 必有；方阵时 $\iff\lvert A\rvert=0$ |
| 单向推断 | 齐次只有零解 ⇏ 非齐次有解；齐次有非零解 ⇏ 非齐次无穷多解；非齐次无穷多解 ⇒ 齐次有非零解；$r(A)=m$ ⇒ 总有解 |
| 基础解系 | $N(A)$ 的一组基：都是解、线性无关、个数 $=n-r$（三条查齐，「能表示全部解」不必另验） |
| 求基础解系 | 行最简形 → 主元用自由未知量表示 → 自由未知量轮流取 1（有分数就取分母的倍数） |
| 非齐次通解 | $\boldsymbol\eta^*+k_1\boldsymbol\xi_1+\cdots+k_{n-r}\boldsymbol\xi_{n-r}$：一个落脚点加上零空间；解集是平移过的子空间，不过原点 |
| 解的组合 | $\sum c_i\boldsymbol\eta_i$ 是 $A\boldsymbol x=\boldsymbol b$ 的解 $\iff\sum c_i=1$；是 $A\boldsymbol x=\boldsymbol 0$ 的解 $\iff\sum c_i=0$ |
| 含参数 | 方阵先解 $\lvert A\rvert=0$ 找特殊值，其余唯一解；两个参数或非方阵就带参数消元；不能除以可能为零的含参式 |
| $AB=O$ | $B$ 的列掉进 $N(A)$：$r(A)+r(B)\le n$（$n$ 是 $A$ 的列数） |
| $r(A^{\mathsf T}A)=r(A)$ | 两者零空间相同；关键一步 $\lVert A\boldsymbol x\rVert^2=0\Rightarrow A\boldsymbol x=\boldsymbol 0$，只在实数里成立；列无关时 $A^{\mathsf T}A$ 可逆 |
| 伴随矩阵的秩 | $r(A)=n,\,n-1,\,<n-1$ 时 $r(A^*)=n,\,1,\,0$；$r(A)=n-1$ 时 $A^*$ 的非零列就是基础解系 |
| 公共解与同解 | 公共解：上下拼起来解；同解 $\iff r(A)=r(B)=r\begin{pmatrix}A\\B\end{pmatrix}$ |
