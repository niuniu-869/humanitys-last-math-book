## C.11 · 积分的计算方法（速记）

| 提示 | 内容 |
|---|---|
| 凑微分（方法 1） | $\int f(u(x))u'(x)\,\mathrm{d}x=\int f(u)\,\mathrm{d}u$；找整体 $u$，剩下的是 $u'$ 的常数倍；在 $f$ 可导且不为 0 的区间上 $\int\frac{f'}f\mathrm{d}x=\ln\lvert f\rvert+C$ |
| 常用凑法 | $x\,\mathrm{d}x=\frac12\mathrm{d}x^2$，$\frac{\mathrm{d}x}x=\mathrm{d}\ln\lvert x\rvert$（$x\ne0$），$\frac{\mathrm{d}x}{\sqrt x}=2\mathrm{d}\sqrt x$（$x>0$），$\mathrm{e}^x\mathrm{d}x=\mathrm{d}\mathrm{e}^x$，$\sin x\,\mathrm{d}x=-\mathrm{d}\cos x$；$\int\frac{\mathrm{d}x}{a^2+x^2}=\frac1a\arctan\frac xa$，$\int\frac{\mathrm{d}x}{\sqrt{a^2-x^2}}=\arcsin\frac xa$ |
| 三角函数的幂 | 有奇次幂：拆一个出来凑微分；全是偶次幂：用 $\frac{1\pm\cos2x}2$ 降次；$\int\sec x\,\mathrm{d}x=\ln\lvert\sec x+\tan x\rvert+C$ |
| 第二类换元（方法 2） | $\sqrt{a^2-x^2}$ 用 $x=a\sin t$，$\sqrt{a^2+x^2}$ 用 $a\tan t$，$\sqrt{x^2-a^2}$ 用 $a\sec t$（设 $a>0$，取使 $\cos t$、$\sec t$、$\tan t$ 为正的一支）；根式 $\sqrt[n]{ax+b}$ 令其为 $t$；分母次数高用 $x=\frac1t$；换回靠直角三角形 |
| 定积分换元（方法 3） | 换元必换限，不回代；要检查 $\varphi$ 满足定理条件（$x=\frac1t$ 不能跨过 0）；$\int_0^1f(xt)\,\mathrm{d}t=\frac1x\int_0^xf$，让 $x$ 跑到积分限上再求导 |
| 对称性（方法 4） | 奇函数在 $[-a,a]$ 上积分为 0，偶函数为 $2\int_0^a$（区间必须关于原点对称，周期性要整数个周期）；$\int_{-a}^af=\int_0^a[f(x)+f(-x)]$；周期 $T$：$\int_a^{a+T}f=\int_0^Tf$ |
| 区间再现 | $\int_a^bf(x)\,\mathrm{d}x=\int_a^bf(a+b-x)\,\mathrm{d}x$；翻转后得到伙伴 $J$（$I+J$ 好算）或得到「好算部分 $-I$」或「常数 $-I$」，列方程解 $I$ |
| 分部积分（方法 5） | $\int u\,\mathrm{d}v=uv-\int v\,\mathrm{d}u$；$u$ 按反对幂指三选（经验次序，$\int\frac{\ln x}x$ 这类能凑微分的先凑）；$\ln x$、$\arctan x$ 把 $\mathrm{d}x$ 当 $\mathrm{d}v$；循环型两次同角色分部后解方程 |
| 华里士公式（方法 6） | $n$ 为正整数，$\int_0^{\pi/2}\sin^nx=\int_0^{\pi/2}\cos^nx=\frac{n-1}n I_{n-2}$（$I_0=\frac\pi2$）：偶数 $\frac{(n-1)!!}{n!!}\frac\pi2$，奇数 $\frac{(n-1)!!}{n!!}$；边界项为 0 是因为端点各让一个因子为零 |
| 部分分式（方法 7） | 假分式先除；$(x-a)^k$ 对应 $k$ 项 $\frac{A_i}{(x-a)^i}$；$(x^2+px+q)^k$（$p^2-4q<0$）对应 $\frac{B_ix+C_i}{(\cdot)^i}$；单根用遮盖法；二次项拆成 $\ln$ 与 $\arctan$ |
| 化为有理函数（方法 8） | $t=\tan\frac x2$（$x=(2k+1)\pi$ 处无定义，跨过要分段）：$\sin x=\frac{2t}{1+t^2}$，$\cos x=\frac{1-t^2}{1+t^2}$，$\mathrm{d}x=\frac{2\mathrm{d}t}{1+t^2}$；只含 $\sin^2,\cos^2,\sin\cos$ 时用 $u=\tan x$；$\mathrm{e}^x$ 的有理式令 $t=\mathrm{e}^x$ |
| 选方法的顺序（方法 9） | 变形查表 → 凑微分 → 三角或根式代换 → 分部 → 部分分式 → 万能代换；$\mathrm{e}^{\pm x^2}$、$\frac{\sin x}x$、$\frac1{\ln x}$ 没有初等原函数（但原函数存在），藏在变限积分里时让它求导 |
| 和式极限（方法 10） | $\lim\frac1n\sum f\big(\frac in\big)=\int_0^1f$；先看每项里的 $i$ 是否只通过 $\frac in$ 出现，$\sum\frac n{n^2+i}$ 这类要夹逼 |
