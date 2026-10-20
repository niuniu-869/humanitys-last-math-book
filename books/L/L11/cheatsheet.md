## L.11 · 特征值与特征向量（速记）

| 提示 | 内容 |
|---|---|
| 定义 | $A\boldsymbol v=\lambda\boldsymbol v$，$\boldsymbol v\ne\boldsymbol 0$；特征向量是变换下不转向的方向（可掉头），$\lambda$ 是伸缩倍数；$\boldsymbol v$ 的非零倍数仍是特征向量 |
| 求法 | 特征方程 $|\lambda E-A|=0$ 求 $\lambda$；对每个 $\lambda_i$ 解 $(\lambda_iE-A)\boldsymbol x=\boldsymbol 0$，基础解系不全为零的组合是全部特征向量 |
| 易错：零向量 | 特征向量必须非零；特征子空间 $N(\lambda_iE-A)$ 比全体特征向量多一个零向量；写通解时注明系数不全为 0 |
| 三阶分解 | 先用行列式性质提公因式（各行和相等时把各列加到第一列；某两行相减出现公因式）；否则展开后在常数项的因数里试根，再带余除法 |
| 复特征值 | 旋转 $\begin{pmatrix}0&-1\\1&0\end{pmatrix}$ 的特征多项式 $\lambda^2+1$，特征值 $\pm\mathrm i$；$n$ 阶方阵在复数范围内恰有 $n$ 个特征值（计重数） |
| 迹与行列式 | $\lambda_1+\cdots+\lambda_n=\operatorname{tr}A$，$\lambda_1\cdots\lambda_n=|A|$；二阶特征多项式 $\lambda^2-(\operatorname{tr}A)\lambda+|A|$；$A$ 可逆 ⇔ 0 不是特征值 |
| 迹的性质 | $\operatorname{tr}(AB)=\operatorname{tr}(BA)$，$\operatorname{tr}(\boldsymbol\alpha\boldsymbol\beta^{\mathsf T})=\boldsymbol\beta^{\mathsf T}\boldsymbol\alpha$；$\operatorname{tr}(AB)\ne\operatorname{tr}A\operatorname{tr}B$ |
| 相关矩阵的特征值 | $A^k\to\lambda^k$，$f(A)\to f(\lambda)$，$A^{-1}\to\frac1\lambda$，$A^*\to\frac{|A|}\lambda$，特征向量不变；$A^{\mathsf T}$ 特征值相同、特征向量一般不同 |
| 行列式 | $|f(A)|=f(\lambda_1)\cdots f(\lambda_n)$；含 $A^*$、$A^{-1}$ 时可先乘 $A$ 化成多项式 |
| 易错：和的特征值 | $A+B$ 的特征值一般不是各自特征值相加（特征向量不同），只有同一个 $A$ 的多项式才能代入 |
| 矩阵等式定候选 | $A^2=A$ ⇒ $\lambda\in\{0,1\}$；$A^2=E$ ⇒ $\pm1$；$A^2=O$ ⇒ 全为 0 但 $A$ 未必为 $O$；只是候选，不一定都出现 |
| 不同特征值 | 属于不同特征值的特征向量线性无关（作用 $A$ 再减 $\lambda_k$ 倍，归纳）；各特征子空间的无关组合并仍无关 |
| 和是不是特征向量 | 不同特征值：$\boldsymbol v_1+\boldsymbol v_2$ 一定不是；同一特征值：和非零时仍是；对 $f(A)$ 要看 $f(\lambda_1)$ 是否等于 $f(\lambda_2)$ |
| 两种重数 | 代数重数＝根的重数；几何重数 $=n-r(\lambda_iE-A)$；$1\le$ 几何 $\le$ 代数，单根几何重数必为 1；老朋友②剪切 $\begin{pmatrix}1&1\\0&1\end{pmatrix}$ 代数 2、几何 1 |
