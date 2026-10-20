## L.2 · 点积、长度、夹角与投影（速记）

| 提示 | 内容 |
|---|---|
| 点积 | $\boldsymbol{a}\cdot\boldsymbol{b}=\boldsymbol{a}^{\mathsf T}\boldsymbol{b}=a_1b_1+\cdots+a_nb_n$，结果是数；可交换、可分配、数乘可提出；$\boldsymbol{a}\cdot\boldsymbol{a}\ge0$，等号只在 $\boldsymbol{a}=\boldsymbol{0}$ |
| 易错：不能搬的习惯 | 没有结合律：$(\boldsymbol{a}\cdot\boldsymbol{b})\boldsymbol{c}$ 与 $\boldsymbol{a}(\boldsymbol{b}\cdot\boldsymbol{c})$ 一般不等，$\boldsymbol{a}\cdot\boldsymbol{b}\cdot\boldsymbol{c}$ 有歧义；$\boldsymbol{a}\cdot\boldsymbol{b}=\boldsymbol{a}\cdot\boldsymbol{c}$ 不能约去 $\boldsymbol{a}$，只说明 $\boldsymbol{a}\perp(\boldsymbol{b}-\boldsymbol{c})$ |
| 长度、距离 | $\lVert\boldsymbol{a}\rVert=\sqrt{\boldsymbol{a}\cdot\boldsymbol{a}}$（即高中的 $|\boldsymbol{a}|$，双竖线与绝对值区分），$\lVert k\boldsymbol{a}\rVert=|k|\,\lVert\boldsymbol{a}\rVert$；两点距离 $\lVert\boldsymbol{a}-\boldsymbol{b}\rVert$；单位化：除以自己的长度 |
| 展开式 | $\lVert\boldsymbol{a}\pm\boldsymbol{b}\rVert^2=\lVert\boldsymbol{a}\rVert^2\pm2\,\boldsymbol{a}\cdot\boldsymbol{b}+\lVert\boldsymbol{b}\rVert^2$；没有分量、只给长度时，先平方再展开 |
| 夹角 | $\cos\theta=\frac{\boldsymbol{a}\cdot\boldsymbol{b}}{\lVert\boldsymbol{a}\rVert\lVert\boldsymbol{b}\rVert}$，$\theta\in[0,\pi]$，两个向量都要非零；二维、三维里由余弦定理推出 |
| 锐角、钝角 | 点积为 0 是直角；点积为正且不同向才是锐角，点积为负且不反向才是钝角 |
| 柯西–施瓦茨 | $|\boldsymbol{a}\cdot\boldsymbol{b}|\le\lVert\boldsymbol{a}\rVert\lVert\boldsymbol{b}\rVert$，等号 ⇔ 共线（零向量与任何向量共线），共线包括反向；证法：$\lVert\boldsymbol{a}+t\boldsymbol{b}\rVert^2\ge0$ 对一切 $t$ 成立，判别式 $\le0$ |
| 方法 3 | 一次式写成 $\boldsymbol{c}\cdot\boldsymbol{x}$ 得到界，等号点 $\boldsymbol{x}=t\boldsymbol{c}$ 满足全部条件时界才是最值 |
| 三角不等式 | $\lVert\boldsymbol{a}+\boldsymbol{b}\rVert\le\lVert\boldsymbol{a}\rVert+\lVert\boldsymbol{b}\rVert$（两边平方，用柯西–施瓦茨）；等号 ⇔ 同向（一个是另一个的非负倍数），求「距离之和最小」靠它定点 |
| 正交与勾股 | $\boldsymbol{a}\perp\boldsymbol{b}$ ⇔ $\boldsymbol{a}\cdot\boldsymbol{b}=0$ ⇔ $\lVert\boldsymbol{a}+\boldsymbol{b}\rVert^2=\lVert\boldsymbol{a}\rVert^2+\lVert\boldsymbol{b}\rVert^2$；零向量与任何向量正交 |
| 投影 | $t=\frac{\boldsymbol{a}\cdot\boldsymbol{b}}{\boldsymbol{a}\cdot\boldsymbol{a}}$，$\boldsymbol{p}=t\boldsymbol{a}$，$\boldsymbol{e}=\boldsymbol{b}-\boldsymbol{p}\perp\boldsymbol{a}$；垂足是直线上最近的点，距离 $\lVert\boldsymbol{e}\rVert$；投影到全 1 方向，$t$ 是平均数 |
| 易错：投影三个量 | 系数 $t$、带符号长度 $\frac{\boldsymbol{a}\cdot\boldsymbol{b}}{\lVert\boldsymbol{a}\rVert}$、投影向量 $\boldsymbol{p}$ 不是一回事；$\boldsymbol{a}$ 换成 $k\boldsymbol{a}$，$t$ 变成 $\frac tk$，$\boldsymbol{p}$、$\boldsymbol{e}$ 不变，带符号长度在 $k<0$ 时变号 |
| 超平面 | $\boldsymbol{a}^{\mathsf T}\boldsymbol{x}=c$（$\boldsymbol{a}\ne\boldsymbol{0}$）⇔ $\boldsymbol{a}\cdot(\boldsymbol{x}-\boldsymbol{x}_0)=0$；系数向量是法向量；$c\ne0$ 时不过原点 |
| 方法 5 | $t=\frac{\boldsymbol{a}\cdot\boldsymbol{y}-c}{\boldsymbol{a}\cdot\boldsymbol{a}}$，垂足 $\boldsymbol{y}-t\boldsymbol{a}$，距离 $\frac{|\boldsymbol{a}\cdot\boldsymbol{y}-c|}{\lVert\boldsymbol{a}\rVert}$；直线不过原点时别漏了减 $c$；$\boldsymbol{a}\cdot\boldsymbol{y}-c$ 的符号说明在哪一侧，同侧两点求距离和最小先反射 |
| 余弦相似度 | 比方向不比长度；打分先减各自平均分（去掉在 $\boldsymbol{1}$ 上的投影）再算余弦；去均值后为零向量就没有余弦；嵌入向量（检索）直接算余弦 |
