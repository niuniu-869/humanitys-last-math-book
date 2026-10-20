| 提示 | 内容 |
|---|---|
| 行列式是什么 | 有向体积的放大倍数：绝对值是面积（体积）放大几倍，负号表示翻面，0 表示压扁 |
| 二阶、三阶 | $ad-bc$；三阶对角线法则六项三正三负。四阶以上不能用对角线法则 |
| 三条规则 | 按行线性；两行相同则为 0；$\lvert E\rvert=1$ |
| 行变换怎样改值 | 换行变号；某行乘 $k$ 值乘 $k$；倍加不变。算行列式用等号，换行添负号、公因子提到外面 |
| 三角形与分块三角形 | 三角形 = 对角元之积；$\begin{vmatrix}A&C\\O&B\end{vmatrix}=\lvert A\rvert\lvert B\rvert$ |
| 可逆判据 | $A$ 可逆 $\iff\lvert A\rvert\ne0\iff$ 有 $n$ 个主元 $\iff A\boldsymbol x=\boldsymbol 0$ 只有零解 |
| 乘积公式 | $\lvert AB\rvert=\lvert A\rvert\lvert B\rvert$，$\lvert A^{\mathsf T}\rvert=\lvert A\rvert$，$\lvert A^{-1}\rvert=1/\lvert A\rvert$，$\lvert kA\rvert=k^n\lvert A\rvert$ |
| 高频易错 | $\lvert A+B\rvert\ne\lvert A\rvert+\lvert B\rvert$；$\lvert kA\rvert$ 不是 $k\lvert A\rvert$；遇到和先化成积（如 $A+E=(E+A^{\mathsf T})A$） |
| 完全展开式 | $n!$ 项，每项每行每列各取一个；行号排好后，列号排列逆序数偶正奇负 |
| 展开定理 | $\lvert A\rvert=\sum_j a_{ij}A_{ij}$，$A_{ij}=(-1)^{i+j}M_{ij}$；异乘变零 $\sum_j a_{kj}A_{ij}=0\ (k\ne i)$ |
| 代数余子式的组合 | $\sum_j b_jA_{ij}$ = 把第 $i$ 行换成 $(b_1,\dots,b_n)$ 后的行列式 |
| 特殊形状的第一步 | 行和相等：各列加到第一列；爪形：用对角元消第一列；三对角：按第一行展开得递推；范德蒙德：$\prod_{i<j}(x_j-x_i)$，后减前 |
| 伴随矩阵 | $A^*$ 的第 $i$ 列是第 $i$ 行的代数余子式；$AA^*=A^*A=\lvert A\rvert E$，$A^{-1}=A^*/\lvert A\rvert$；二阶：主对角互换，副对角变号 |
| 伴随的性质 | $\lvert A^*\rvert=\lvert A\rvert^{n-1}$，$(A^*)^{-1}=(A^{-1})^*=A/\lvert A\rvert$，$(kA)^*=k^{n-1}A^*$，$(AB)^*=B^*A^*$；含 $A^*$ 的式子先换成 $\lvert A\rvert A^{-1}$ |
| 克拉默法则 | $n$ 元 $n$ 个方程且 $D\ne0$：$x_j=D_j/D$；$D=0$ 时不能用，回到消元 |
