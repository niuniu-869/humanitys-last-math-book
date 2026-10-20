## C.16 · 傅里叶级数（速记）

| 提示 | 内容 |
|---|---|
| 三角级数 | $\frac{a_0}{2}+\sum_{n=1}^\infty(a_n\cos nx+b_n\sin nx)$；常数项写 $\frac{a_0}2$ 是为了 $a_0$ 与 $a_n$ 共用一个公式 |
| 正交性 | 在 $[-\pi,\pi]$ 上，$m\ne n$ 时 $\int\cos mx\cos nx=\int\sin mx\sin nx=0$；$m=n\ge1$ 时为 $\pi$；$\int\sin mx\cos nx=0$ 总成立 |
| 系数公式 | $a_n=\frac1\pi\int_{-\pi}^{\pi}f\cos nx\,\mathrm dx$（$n\ge0$），$b_n=\frac1\pi\int_{-\pi}^{\pi}f\sin nx\,\mathrm dx$（$n\ge1$）；「乘 $\cos kx$ 再积分，只剩自己」 |
| 奇偶先看 | 奇函数 $a_n=0$，$b_n=\frac2\pi\int_0^\pi f\sin nx$；偶函数 $b_n=0$，$a_n=\frac2\pi\int_0^\pi f\cos nx$ |
| 端点值 | $\sin n\pi=0$，$\cos n\pi=(-1)^n$；$a_0$ 单独算，通项里的 $\frac1n$ 在 $n=0$ 时不能用 |
| 记号 $\sim$ | 傅里叶级数先写 $f\sim\cdots$，收不收敛、收敛到什么由狄利克雷定理回答 |
| 狄利克雷定理 | 一个周期上连续或只有有限个第一类间断点（左右极限有限），且能分成有限个单调段（允许常值段） ⇒ 级数处处收敛到 $\frac{f(x^-)+f(x^+)}{2}$，连续点处等于 $f(x)$ |
| 易错：$x=\pm\pi$ | 先周期延拓；$f(-\pi^+)\ne f(\pi^-)$ 时 $\pm\pi$ 是跳跃点，$S(\pi)=\frac{f(\pi^-)+f(-\pi^+)}2$，不是 $f(\pi)$ |
| 求数项级数的和 | 展开后代入使 $\cos nx$ 成为 $\pm1$ 的点（$0$ 或 $\pi$），先确认该点和函数的值：$\sum\frac1{n^2}=\frac{\pi^2}6$，$\sum\frac{(-1)^{n+1}}{n^2}=\frac{\pi^2}{12}$，$\sum\frac1{(2k-1)^2}=\frac{\pi^2}8$ |
| 正弦/余弦级数 | 只给 $[0,\pi]$：要正弦级数奇延拓，要余弦级数偶延拓；系数 $\frac2\pi\int_0^\pi$ |
| 周期前提 | 级数以 $2\pi$ 为周期；$f$ 本身不周期时，只在给定的那一个周期内与 $f$ 一致（$x$ 在 $[-\pi,\pi)$ 的级数，在 $\pi+0.5$ 处的和是 $-\pi+0.5$） |
| 端点处的和 | 正弦级数在 $x=0,\pi$ 处为 0；满足本章收敛条件时，余弦级数在端点等于 $f(0^+)$、$f(\pi^-)$ |
| 周期 $2l$ | 令 $t=\frac{\pi x}{l}$：$a_n=\frac1l\int_{-l}^{l}f\cos\frac{n\pi x}{l}\,\mathrm dx$，$b_n$ 同理；$[0,l]$ 上的正弦/余弦级数系数为 $\frac2l\int_0^l$ |
| 易错：周期 $2l$ 的分部积分 | $\cos\frac{n\pi x}{l}$ 的原函数是 $\frac{l}{n\pi}\sin\frac{n\pi x}{l}$，系数 $\frac{l}{n\pi}$ 最容易漏 |
