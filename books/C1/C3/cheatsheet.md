## C.3 · 连续（速记）

| 提示 | 内容 |
|---|---|
| 连续的定义 | $f$ 在 $x_0$ 连续 $\iff\lim\limits_{x\to x_0}f(x)=f(x_0)$：有定义、极限存在、两者相等，缺一层就不连续 |
| 三种等价写法 | 极限等于函数值；$\forall\varepsilon\,\exists\delta$：$\lvert x-x_0\rvert<\delta\Rightarrow\lvert f(x)-f(x_0)\rvert<\varepsilon$（不必要求 $x\ne x_0$）；$\Delta x\to0\Rightarrow\Delta y\to0$ |
| 单侧连续 | 连续 $\iff$ 左连续且右连续；闭区间上连续还要求左端点右连续、右端点左连续 |
| 求参数 | 内部分界点令左极限 = 右极限 = 函数值，解参数；闭区间端点只查区间内的一侧 |
| 间断点分类 | 第一类（左右极限都是有限数）：相等为可去，不等为跳跃；第二类（至少一侧不存在）：常见的是趋于 $\pm\infty$（无穷）和来回摆动（振荡） |
| 找候选点 | 初等函数只在无意义点和分段点可能间断；含 $\lvert x\rvert$、$e^{1/x}$、$\arctan\frac1x$ 时分左右算 |
| 连续与间断相加、相乘 | 连续 $+$ 间断 $=$ 间断；连续 $\times$ 间断可能连续（取 $g(0)=0$，$x\cdot\frac{\lvert x\rvert}{x}=\lvert x\rvert$）；$f$ 连续 $\Rightarrow\lvert f\rvert$ 连续，反过来不成立（取 $\pm1$ 的函数） |
| 运算保持连续 | 四则（除式要分母不为 0）、复合、区间上严格单调函数的反函数（在值域上）都连续；初等函数在定义区间内连续（端点单侧）；极限号可以穿过连续的外层函数：$\lim f(\varphi(x))=f(\lim\varphi(x))$，要求 $f$ 在极限点连续 |
| 新增等价无穷小（$x\to0$） | $\ln(1+x)\sim x$，$e^x-1\sim x$，$a^x-1\sim x\ln a$（$a>0,a\ne1$），$(1+x)^\alpha-1\sim\alpha x$（$\alpha\ne0$），$\arcsin x\sim x$，$\arctan x\sim x$ |
| 等价替换的限制 | 乘除因子可换；加减连着的主项抵消时不能换（$\frac{e^x-1-x}{x^2}\to\frac12$，换了得 0） |
| 幂指函数 | $u^v=e^{v\ln u}$；$1^\infty$ 型：$u>0$、$u\to1$、$u\ne1$ 时 $\lim u^v=e^{\lim v(u-1)}$（右边极限要存在） |
| 闭区间上的连续函数 | 有界，并且取得到最大值、最小值；去掉闭或连续都可能不成立（$\frac1x$ 在 $(0,1]$） |
| 零点定理与介值定理 | $f$ 在 $[a,b]$ 连续、$f(a)f(b)<0\Rightarrow\exists\xi\in(a,b)$，$f(\xi)=0$；$C$ 在 $f(a),f(b)$ 之间则 $f(\xi)=C$；$f([a,b])=[m,M]$ |
| 证存在 $\xi$ | 移项造 $g$，查闭区间上连续，端点异号（端点为 0 单独说） |
| 二分法 | 保留两端异号的一半；$n$ 步后区间长 $\frac{b-a}{2^n}$，要小于 $\varepsilon$ 取 $2^n>\frac{b-a}\varepsilon$ |
