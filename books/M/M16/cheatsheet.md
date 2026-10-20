## M.16 · 生成模型：隐变量、ELBO、VAE 与 GAN（速记）

| 提示 | 内容 |
|---|---|
| 隐变量模型 | $p(z)=N(0,I)$，$p_\theta(x\mid z)=N(g_\theta(z),\sigma_x^2I)$，$p_\theta(x)=\int p_\theta(x\mid z)p(z)\,\mathrm dz$ 一般算不出；后验 $p(z\mid x)=p(x,z)/p(x)$ |
| Jensen（对数） | $\log E[X]\ge E[\log X]$（$X>0$，$E[X]$、$E[|\log X|]$ 有限），等号当且仅当 $X$ 以概率 1 为常数；证明：均值处的切线；按 C.8、M.1 的约定 $\log$ 是凹函数 |
| ELBO | $\log p(x)\ge E_q[\log\frac{p(x,z)}{q(z)}]=E_q[\log p(x\mid z)]-\mathrm{KL}(q(z)\Vert p(z))$（重建项 − 先验项）；$q$ 取先验就是直接对先验用 Jensen，得到一个较松的下界（例 1：$-2.3189$ 对 $-2.0465$） |
| ELBO 的差距 | $\log p(x)-\mathrm{ELBO}=\mathrm{KL}(q(z)\Vert p(z\mid x))\ge0$；$q=$ 后验时贴紧；固定模型参数时增大 ELBO 就是缩小这个 KL，改变参数时不保证似然上升 |
| EM | E 步：$q=$ 后验（责任 $r_{ik}$）；M 步：$\mu_k=\sum r_{ik}x_i/\sum r_{ik}$，$\pi_k=\sum_i r_{ik}/n$；似然单调不降；权重、方差固定相同并硬分配给最近中心时就是 k-means |
| 重参数化 | $z=\mu+\sigma\odot\varepsilon$，$\varepsilon\sim N(0,I)$；$\partial f/\partial\mu=f'(z)$，$\partial f/\partial\sigma=f'(z)\varepsilon$；固定噪声，沿 $z$ 对均值和标准差求导（要求 $f$ 可导、求导与期望可交换） |
| 与对数导数技巧对照 | 重参数化要 $f$ 可导；对数导数 $E[f\nabla\log q]$ 离散也能用；两者方差大小取决于函数和分布（例 5 对 $\mu$：1 对 21.75） |
| VAE 损失 | 固定 $\sigma_x^2$ 时，一次抽样的损失 $\frac{\lVert x-g(z)\rVert^2}{2\sigma_x^2}+\mathrm{KL}$，$z=\mu+\sigma\odot\varepsilon$；对 $\varepsilon$ 取期望加回常数才是负 ELBO；高斯解码器的重建项是均方误差 |
| 对角高斯的 KL | $\mathrm{KL}(N(\mu,\sigma^2)\Vert N(0,1))=\frac12(\mu^2+\sigma^2-1-\log\sigma^2)$，多维按分量相加；$N(1,0.5^2)$ 对 $N(0,1)$：$\approx0.8181$（例 6） |
| 生成新图 | 训练后不用编码器，$z\sim N(0,I)$ 送进解码器得均值（完整抽样再加 $\sigma_x\xi$）；KL 项鼓励编码接近先验，不保证每个先验样本都好 |
| GAN 目标 | $\min_G\max_D E_{p_{\text{data}}}\log D(x)+E_z\log(1-D(G(z)))$；$D$ 是真假二分类；常用 $-\log D(G(z))$ 代替以免初期梯度消失 |
| 最优判别器 | 分母大于零处 $D^*=p_{\text{data}}/(p_{\text{data}}+p_g)$（$p_g=0$ 处取 1，$p_{\text{data}}=0$ 处取 0）；代回得 $V^*=2\,\mathrm{JS}-\log4$（对原始极小极大目标）；$p_g=p_{\text{data}}$ 时 $D^*=\frac12$，$V^*=-\log4$ |
| JS 散度 | $\frac12\mathrm{KL}(p\Vert m)+\frac12\mathrm{KL}(q\Vert m)$，$m=\frac12(p+q)$；对称，$0\le\mathrm{JS}\le\log2$；支撑不重叠时恒为 $\log2$ |
| GAN 的毛病 | 模式坍塌（只需骗过当前判别器）；极小极大的梯度步可能绕圈（$\min_x\max_y xy$，同时更新）；真假分布始终不重叠时 JS 恒为 $\log2$，目标无方向信息 |
