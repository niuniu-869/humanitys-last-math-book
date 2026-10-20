import math
import numpy as np


def passed(label, ok):
    print(f"{'PASS' if ok else 'FAIL'} {label}")


# 例 1: cosine attention, RMSNorm, and temperature effect.
cos_scores = np.array([1 / math.sqrt(2), 0.0, 1 / math.sqrt(5)]) / 0.5
weights = np.exp(cos_scores - cos_scores.max())
weights /= weights.sum()
tau1 = np.array([1 / math.sqrt(2), 0.0, 1 / math.sqrt(5)])
w1 = np.exp(tau1 - tau1.max())
w1 /= w1.sum()
tau01 = np.array([1 / math.sqrt(2), 0.0, 1 / math.sqrt(5)]) / 0.1
w01 = np.exp(tau01 - tau01.max())
w01 /= w01.sum()
rms = math.sqrt((3**2 + 4**2) / 2)
rms_y = np.array([3, 4]) / rms
passed("例1", np.allclose(weights, [0.5441, 0.1323, 0.3236], atol=5e-4)
       and np.allclose(w1, [0.4417, 0.2178, 0.3406], atol=5e-4)
       and np.allclose(w01, [0.930, 0.0008, 0.0692], atol=8e-4)
       and np.allclose(rms_y, [0.8485, 1.1314], atol=5e-4))

# 例 2: the diffusion objective is a scalar expectation of a squared norm.
x0 = np.zeros((2, 2, 1))
noise = np.ones_like(x0)
alpha_bar = 0.6
xt = math.sqrt(alpha_bar) * x0 + math.sqrt(1 - alpha_bar) * noise
prediction = np.zeros_like(xt)
loss_sample = np.linalg.norm(noise - prediction) ** 2
passed("例2", xt.shape == x0.shape == noise.shape and np.isscalar(loss_sample) and loss_sample == 4.0)

# 例 3: sinusoidal positional encodings at d_model=4.
def pe(pos, d=4):
    out = []
    for j in range(d):
        i = j // 2
        den = 10000 ** (2 * i / d)
        out.append(math.sin(pos / den) if j % 2 == 0 else math.cos(pos / den))
    return np.array(out)


passed("例3", np.allclose(pe(1), [0.8415, 0.5403, 0.0100, 1.0000], atol=5e-4)
       and np.allclose(pe(2), [0.9093, -0.4161, 0.0200, 0.9998], atol=5e-4))

# 例 4: parameter counts for the paper's base model.
d, h, dk, dv, dff = 512, 8, 64, 64, 2048
attn = 3 * h * d * dk + h * dv * d
ffn = d * dff + dff * d
enc = attn + ffn
dec = enc + attn
all_layers = 6 * enc + 6 * dec
alt = 12 * 1024**2
passed("例4", (attn, ffn, enc, dec, all_layers, alt) == (1048576, 2097152, 3145728, 4194304, 44040192, 12582912))

# 例 5: operation counts.
d = 512
small = (50**2 * d, 50 * d**2)
large = (1000**2 * d, 1000 * d**2)
passed("例5", small == (1280000, 13107200) and large == (512000000, 262144000))

# 例 6: warmup learning-rate values and the extra peak example.
def lr(model_d, step, warmup):
    return model_d**-0.5 * min(step**-0.5, step * warmup**-1.5)


vals = [lr(512, 1, 4000), lr(512, 4000, 4000), lr(512, 10000, 4000)]
peak_extra = lr(256, 1000, 1000)
passed("例6", np.allclose(vals, [1.747e-7, 6.99e-4, 4.419e-4], rtol=3e-3)
       and abs(peak_extra - 1.976e-3) < 2e-5)

# 例 7: residual output, derivative, and ten-layer products.
residual_y = 1 + 0.1 * 1
residual_grad = 1 + 0.1
plain_ten = 0.1**10
residual_ten = 1.1**10
passed("例7", residual_y == 1.1 and residual_grad == 1.1
       and abs(plain_ten - 1e-10) < 1e-20 and abs(residual_ten - 2.59374246) < 1e-6)

# 编辑稿新增：位置 0 的编码；Pre-LN / Post-LN 的一数示例。
pe0 = pe(0) if callable(pe) else None
pre_layer, post_layer = 1 + 0.1 * 0.8, 0.8 * (1 + 0.1)
passed("编辑-PE0与LN示例", np.allclose(pe0, [0, 1, 0, 1])
       and abs(pre_layer - 1.08) < 1e-12 and abs(post_layer - 0.88) < 1e-12
       and abs(pre_layer**10 - 2.16) < 5e-3 and abs(post_layer**10 - 0.28) < 5e-3)
