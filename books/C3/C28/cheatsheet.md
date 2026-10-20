## C.28 · 曲面积分、高斯公式与斯托克斯公式（速记）

| 提示 | 内容 |
|---|---|
| 第一类曲面积分 | $\iint_\Sigma f\,\mathrm{d}S=\iint_D f\bigl(x,y,z(x,y)\bigr)\sqrt{1+z_x^2+z_y^2}\,\mathrm{d}\sigma$，$\mathrm{d}S>0$，不分侧 |
| 点在曲面上 | 曲面积分里可以把曲面方程代入被积函数（如球面上 $x^2+y^2+z^2=a^2$）；三重积分里不行 |
| 球面对称 | $\oiint x^2\,\mathrm{d}S=\oiint y^2\,\mathrm{d}S=\oiint z^2\,\mathrm{d}S=\frac13 a^2\cdot4\pi a^2$；关于 $xOy$ 面对称、$f$ 对 $z$ 为奇则积分为 $0$ |
| 第二类曲面积分 | $\iint_\Sigma P\,\mathrm{d}y\mathrm{d}z+Q\,\mathrm{d}z\mathrm{d}x+R\,\mathrm{d}x\mathrm{d}y=\iint_\Sigma\boldsymbol F\cdot\boldsymbol n\,\mathrm{d}S$，换侧变号 |
| 分项投影定号 | $\iint_\Sigma R\,\mathrm{d}x\mathrm{d}y=\pm\iint_D R(x,y,z(x,y))\,\mathrm{d}\sigma$，上侧取 $+$、下侧取 $-$；竖直柱面上这一项为 $0$ |
| 合一投影 | 上侧 $\boldsymbol n\,\mathrm{d}S=(-z_x,-z_y,1)\,\mathrm{d}\sigma$，积分 $=\pm\iint_D(-Pz_x-Qz_y+R)\,\mathrm{d}\sigma$ |
| 高斯公式 | $\oiint_\Sigma\boldsymbol F\cdot\boldsymbol n\,\mathrm{d}S=\iiint_\Omega(P_x+Q_y+R_z)\,\mathrm{d}V$，$\Sigma$ 取外侧，偏导在包含 $\Omega$ 及其边界的开区域内连续 |
| 补面法 | $\iint_\Sigma=\iiint_\Omega\operatorname{div}\boldsymbol F\,\mathrm{d}V-\iint_{\Sigma_1}$，补面的侧与原曲面合成外侧 |
| 有奇点 | 区域内有无定义的点（如 $\frac{(x,y,z)}{(x^2+y^2+z^2)^{3/2}}$ 的原点）时不能直接用高斯公式：内部孤立的无定义点可先挖去小球，再检查剩余区域的条件并计入球面通量。该场散度为 $0$，穿过包住原点的闭曲面的通量却是 $4\pi$ |
| 散度 | $\operatorname{div}\boldsymbol F=P_x+Q_y+R_z$，小球净流出量除以体积、球缩到该点所得的极限，即单位体积的净流出量（正：往外冒） |
| 斯托克斯公式 | $\oint_\Gamma\boldsymbol F\cdot\mathrm{d}\boldsymbol r=\iint_\Sigma\operatorname{rot}\boldsymbol F\cdot\boldsymbol n\,\mathrm{d}S$；平面上的情形就是格林公式 |
| 右手法则 | 沿边界走、头朝所选法向，曲面在左手边；平面片可用四指与拇指定向 |
| 旋度 | $\operatorname{rot}\boldsymbol F=(R_y-Q_z,\ P_z-R_x,\ Q_x-P_y)$，其在单位法向 $\boldsymbol n$ 上的分量，是对应小圆盘的环流量除以面积后的极限 |
| 路径无关 | 曲面单连通区域内：$\operatorname{rot}\boldsymbol F=\boldsymbol 0$ ⇔ 闭曲线积分为 $0$ ⇔ 存在 $u$，积分 $=u(B)-u(A)$；梯度场旋度为零；挖掉 $z$ 轴时 $\frac{(-y,x,0)}{x^2+y^2}$ 旋度为 $\boldsymbol0$ 而环流为 $2\pi$，单连通不能去 |
| 薄壳质心 | $M=\iint_\Sigma\mu\,\mathrm{d}S$，$\bar z=\frac1M\iint_\Sigma z\mu\,\mathrm{d}S$；均匀半球面 $\bar z=\frac a2$ |
