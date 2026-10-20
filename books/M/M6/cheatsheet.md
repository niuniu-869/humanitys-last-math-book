## M.6 · 拉格朗日对偶与 SVM（速记）

| 提示 | 内容 |
|---|---|
| 点到超平面的距离 | $\dfrac{\lvert\boldsymbol w^{\mathsf T}\boldsymbol x+b\rvert}{\lVert\boldsymbol w\rVert}$（$\boldsymbol w\ne\boldsymbol0$）；分对时 $y_i(\boldsymbol w^{\mathsf T}\boldsymbol x_i+b)>0$，标签用 $\pm1$；间隔 = 最小的距离 |
| 缩放自由度 | $(\boldsymbol w,b)\to(c\boldsymbol w,cb)$（$c>0$）直线不变；对已分对的数据除以 $\gamma=\min_iy_i(\boldsymbol w^{\mathsf T}\boldsymbol x_i+b)$，最小得分为 1，间隔 $=1/\lVert\boldsymbol w\rVert$ |
| 硬间隔原问题 | 两类可分时 $\min\tfrac12\lVert\boldsymbol w\rVert^2$，约束 $y_i(\boldsymbol w^{\mathsf T}\boldsymbol x_i+b)\ge1$（边界上或正确一侧的带外）；凸二次目标 + 一次约束 |
| 不等式约束的拉格朗日函数 | $\min J$，$g_i\le0$：$L=J+\sum\alpha_ig_i$，$\alpha_i\ge0$；符号错了就不是 KKT |
| KKT 四条 | $\nabla_{\boldsymbol x}L=\boldsymbol0$；$g_i\le0$；$\alpha_i\ge0$；互补松弛 $\alpha_ig_i=0$。适用：目标可微、约束一次；目标为凸时四条充分（$J=-x^2$ 在 $x=0$ 满足四条却是最大点） |
| 解 KKT 的套路 | 每条约束分「不起作用（$\alpha=0$）/ 起作用（$g=0$）」讨论，解出后检查可行性与 $\alpha\ge0$ |
| 为什么 $\alpha\ge0$ | 单条约束起作用时 $\alpha<0$，则下降方向指向可行一侧，沿它走既可行又让 $J$ 下降；多条约束时 $-\nabla J$ 是各 $\nabla g_i$ 的非负组合 |
| 弱对偶与对偶函数 | $d(\boldsymbol\alpha)=\min_{\boldsymbol w,b}L\le p^*$；$\sum\alpha_iy_i\ne0$ 时 $d=-\infty$；两类可分的硬间隔问题中 $d^*=p^*$ |
| SVM 对偶 | $\max\sum\alpha_i-\tfrac12\sum\alpha_i\alpha_jy_iy_j\boldsymbol x_i^{\mathsf T}\boldsymbol x_j$；$\alpha_i\ge0$，$\sum\alpha_iy_i=0$；$\boldsymbol w=\sum\alpha_iy_i\boldsymbol x_i$ |
| 支持向量（硬间隔） | $\alpha_i>0\Rightarrow y_i(\boldsymbol w^{\mathsf T}\boldsymbol x_i+b)=1$；$b=y_s-\boldsymbol w^{\mathsf T}\boldsymbol x_s$；边界上的点乘子也可为 0；正确一侧带外的点删去不影响解 |
| 软间隔 | $\min\tfrac12\lVert\boldsymbol w\rVert^2+C\sum\xi_i$，$\xi_i=\max(0,1-y_if(\boldsymbol x_i))$（合页损失）；对偶多 $0\le\alpha_i\le C$；$0<\alpha<C$ 的点恰在边界，取 $b$ 用这类点 |
| 合页 vs 逻辑损失 | $z=yf>1$ 时合页为 0、$\alpha=0$；$z=1$ 时损失也是 0 但可以是支持向量；逻辑损失永不为 0；SVM 得分不直接表示概率 |
| 核技巧 | 对偶与预测里数据只以内积出现，换成 $K(\boldsymbol x,\boldsymbol x')=\boldsymbol\varphi(\boldsymbol x)^{\mathsf T}\boldsymbol\varphi(\boldsymbol x')$；$(\boldsymbol x^{\mathsf T}\boldsymbol x')^2$ 对应 $(x_1^2,\sqrt2x_1x_2,x_2^2)$；核矩阵半正定（$\boldsymbol c^{\mathsf T}K\boldsymbol c=\lVert\sum c_i\boldsymbol\varphi(\boldsymbol x_i)\rVert^2$）；$K(\boldsymbol x,\boldsymbol x)<0$ 的函数（如 $-\boldsymbol x^{\mathsf T}\boldsymbol x'$）不是核；直接保存全部核值要 $n\times n$ 个数 |
