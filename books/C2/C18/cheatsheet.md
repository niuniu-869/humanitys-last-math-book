| 提示 | 内容 |
|---|---|
| 缺 $y$：$y''=f(x,y')$ | 令 $v=y'$，$y''=\frac{\mathrm{d}v}{\mathrm{d}x}$，化成关于 $v(x)$ 的一阶方程 |
| 缺 $x$：$y''=f(y,y')$ | 令 $v=y'$ 看成 $y$ 的函数，$y''=v\frac{\mathrm{d}v}{\mathrm{d}y}$（在 $y'\ne0$ 的一段上，常值解另查） |
| 降阶时的初值 | 每积分一次就用初值定常数；开方时按初值选符号 |
| 叠加原理 | $L[C_1y_1+C_2y_2]=C_1L[y_1]+C_2L[y_2]$；非齐次解之差是齐次解 |
| 线性方程通解结构 | 齐次：$C_1y_1+C_2y_2$（$y_1/y_2$ 不是常数）；非齐次：再加一个特解 $y^*$ |
| 特征方程 | $y''+py'+qy=0$ 把 $y'',y',y$ 换成 $r^2,r,1$：$r^2+pr+q=0$ |
| 三种根 | 不等实根 $C_1e^{r_1x}+C_2e^{r_2x}$；重根 $(C_1+C_2x)e^{rx}$；$\alpha\pm i\beta$：$e^{\alpha x}(C_1\cos\beta x+C_2\sin\beta x)$ |
| 高阶 | $k$ 重根贡献 $e^{rx}$ 乘 $1,x,\dots,x^{k-1}$；$n$ 阶通解有 $n$ 个常数 |
| 关键恒等式 $(\star)$ | $y=ue^{rx}$ 时 $y''+py'+qy=[u''+(2r+p)u'+(r^2+pr+q)u]e^{rx}$ |
| 右边 $G_m(x)e^{\lambda x}$ | 设 $y^*=x^kW_m(x)e^{\lambda x}$，$k$ = $\lambda$ 是特征根的重数（0、1、2） |
| 右边 $e^{\alpha x}(P\cos\beta x+\tilde P\sin\beta x)$ | 设 $x^ke^{\alpha x}(R_m\cos\beta x+S_m\sin\beta x)$，$\alpha+i\beta$ 是根则 $k=1$；只有 cos 也要两项都设 |
| $x''+cx'+ax=0$（$a,c>0$） | $0<c<2\sqrt a$ 非零解振荡衰减；$c=2\sqrt a$ 时最慢部分的指数衰减率最大；从 $x(0)>0,x'(0)=0$ 出发，$c\ge2\sqrt a$ 的解不越过 0 |
| 欧拉方程 $x^2y''+pxy'+qy=f$ | 令 $x=e^t$：$xy'=\frac{\mathrm{d}y}{\mathrm{d}t}$，$x^2y''=\frac{\mathrm{d}^2y}{\mathrm{d}t^2}-\frac{\mathrm{d}y}{\mathrm{d}t}$ |
| 方程组消元 | 由一式解出 $y$ 代入另一式；$y$ 用回代式求出，不另加常数 |
