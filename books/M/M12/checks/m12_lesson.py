"""Recompute all nine lesson examples from their inputs.

Example 8 distinguishes the matrix subtotal from the total including
normalization scales; verify both against the author's corrected lesson.
"""

from pathlib import Path
import sys

import numpy as np
import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
FAILURES = 0


def close(actual, expected, atol=0.000051, rtol=0):
    assert np.allclose(actual, expected, atol=atol, rtol=rtol), (actual, expected)


def softmax(x):
    e = np.exp(x - np.max(x, axis=-1, keepdims=True))
    return e / e.sum(axis=-1, keepdims=True)


def norm(x, eps=0, center=True, axis=-1):
    x = np.asarray(x, dtype=float)
    z = x - x.mean(axis=axis, keepdims=True) if center else x
    return z / np.sqrt((z*z).mean(axis=axis, keepdims=True) + eps)


def rotation(x):
    return np.array([[np.cos(x), -np.sin(x)], [np.sin(x), np.cos(x)]])


def example1():
    # Head 1's original projection matrices are specified in M.11, section 2.
    x = np.array([[1., 0.], [0., 1.], [1., 1.]])
    q1 = x @ np.array([[1, 0], [1, 1]])
    k1 = x @ np.array([[1, 1], [0, 1]])
    a1 = softmax(q1@k1.T / np.sqrt(q1.shape[1]))
    o1 = a1 @ x
    q2 = k2 = x
    v2 = np.array([[1, -1], [0, 2], [1, 1]])
    s2 = q2@k2.T / np.sqrt(q2.shape[1])
    a2 = softmax(s2)
    o2 = a2 @ v2
    wo = np.array([[1, 0, 0, 1], [0, 1, 1, 0], [1, 0, 1, 0], [0, 1, 0, 1]])
    close(o1[2], [0.9257, 0.6943])
    close(s2[2], [0.7071, 0.7071, 1.4142])
    close(np.exp(s2[2]), [2.028, 2.028, 4.113], atol=0.00051)
    close(np.exp(s2[2]).sum(), 8.170, atol=0.001)
    close(a2[2], [0.2483, 0.2483, 0.5035])
    close(o2[2], [0.7517, 0.7517])
    close((np.concatenate([o1, o2], axis=1)@wo)[2], [1.6774, 1.4460, 1.4460, 1.6774])
    close(a1[1], [0.2840, 0.1400, 0.5760])
    close(a2[1], [0.1978, 0.4011, 0.4011])
    assert 512//8 == 64 and 4*512**2 == 1048576
    # Also verify the unmasked permutation calculation in section 4.
    p = np.eye(3)[::-1]
    swapped = softmax((p@q1)@(p@k1).T/np.sqrt(2)) @ (p@x)
    close(swapped, p@o1, atol=1e-12)
    close(swapped, [[0.9257, 0.6943], [0.8600, 0.7160], [0.8022, 0.5989]])


def example2():
    w1 = sp.Matrix([[1, -1, 0, 1], [0, 1, 1, -1]])
    w2 = sp.Matrix([[1, 0], [0, 1], [1, 1], [-1, 0]])
    b = sp.Matrix([[0, 0, -1, 0]])
    for x, pre_expected, hidden_expected, out_expected in [
        ([1, 2], [1, 1, 1, -1], [1, 1, 1, 0], [2, 2]),
        ([0, 1], [0, 1, 0, -1], [0, 1, 0, 0], [0, 1]),
        ([2, 0], [2, -2, -1, 2], [2, 0, 0, 2], [0, 0]),
    ]:
        pre = sp.Matrix([x])*w1+b
        hidden = pre.applyfunc(lambda z: sp.Max(z, 0))
        assert pre == sp.Matrix([pre_expected])
        assert hidden == sp.Matrix([hidden_expected])
        assert hidden*w2 == sp.Matrix([out_expected])


def example3():
    x = np.array([1., 2., 3., 6.])
    assert x.mean() == 3 and x.var() == 3.5
    close(np.sqrt(x.var()), 1.8708)
    y = norm(x)
    close(y, [-1.0690, -0.5345, 0, 1.6036])
    close(y.sum(), 0, atol=1e-12)
    close(y.var(), 1, atol=1e-12)
    assert np.mean(x*x) == 12.5
    close(np.sqrt(np.mean(x*x)), 3.5355)
    close(norm(x, center=False), [0.2828, 0.5657, 0.8485, 1.6971])
    assert not np.isclose(norm(x, center=False).sum(), 0)
    close(norm(10*x), y, atol=1e-12)
    close(norm(x+100), y, atol=1e-12)
    batch = np.array([[1., 2., 3.], [3., 6., 9.]])
    close(norm(batch, axis=0), [[-1]*3, [1]*3], atol=1e-12)
    # A positive epsilon is necessary for the zero-variance BN example.
    duplicate = np.vstack([batch[0], batch[0]])
    close(norm(duplicate, eps=1e-5, axis=0), np.zeros((2, 3)), atol=1e-12)
    close(norm(batch), [[-1.2247, 0, 1.2247]]*2)
    close(norm(duplicate), norm(batch), atol=1e-12)
    close(norm([2, 4, 6]), [-1.2247, 0, 1.2247])
    # Section 3 opening: LN of example 1's output vector.
    o = np.array([1.6774, 1.4460, 1.4460, 1.6774])
    close(o.mean(), 1.5617); close(o - o.mean(), [0.1157, -0.1157, -0.1157, 0.1157])
    close(norm(o), [1, -1, -1, 1], atol=1e-3)
    close(norm(-10*x), -norm(x), atol=1e-12)
    assert not np.allclose(norm(x+100, center=False), norm(x, center=False))


def example4():
    position = lambda p, d: np.array([
        f(p * 10000**(-2*i/d)) for i in range(d//2) for f in (np.sin, np.cos)
    ])
    close(position(2, 2), [0.9093, -0.4161])
    close(position(2, 2)+[1, 0], [1.9093, -0.4161])
    close(position(5, 2), [-0.9589, 0.2837])
    close(position(5, 2)+[1, 0], [0.0411, 0.2837])
    table = [[0, 1, 0, 1], [0.8415, 0.5403, 0.0100, 1.0000],
             [0.9093, -0.4161, 0.0200, 0.9998], [0.1411, -0.9900, 0.0300, 0.9996]]
    for p, expected in enumerate(table):
        close(position(p, 4), expected)
    p, k, w = sp.symbols("p k w", real=True)
    rhs = sp.Matrix([[sp.cos(w*k), sp.sin(w*k)], [-sp.sin(w*k), sp.cos(w*k)]])
    delta = sp.Matrix([sp.sin(w*(p+k)), sp.cos(w*(p+k))])-rhs*sp.Matrix([sp.sin(w*p), sp.cos(w*p)])
    assert all(sp.trigsimp(sp.expand_trig(v)) == 0 for v in delta)


def example5():
    q, k = np.array([2., 1.]), np.array([1., 1.])
    close(rotation(1)@k, [-0.3012, 1.3818])
    close(q@(rotation(1)@k), 0.7794)
    for m, n, qr_expected, kr_expected in [
        (1, 3, [1.2757, 1.8364], [-0.9268, 1.0682]),
        (4, 6, [-1.7416, 1.4024], [-1.1311, -0.8489]),
    ]:
        qr, kr = rotation(m*0.5)@q, rotation(n*0.5)@k
        close(qr, qr_expected)
        close(kr, kr_expected)
        close(qr@kr, 0.7794)
        close(qr@kr, q@(rotation((n-m)*0.5)@k), atol=1e-12)
    close((rotation(2)@q)@(rotation(2)@k), 3, atol=1e-12)
    close(rotation(-0.5)@k, [1.3570, 0.3982])
    close(q@(rotation(-0.5)@k), 3.1122, atol=0.0001)


def example6():
    n, d, h, dff = 3, 4, 2, 16
    x = np.arange(n*d, dtype=float).reshape(n, d)
    z = norm(x)
    q = z @ np.zeros((d, d))
    heads = np.split(q, h, axis=1)
    weights = np.stack([softmax(head@head.T/np.sqrt(d//h)) for head in heads])
    outputs = [weights[a]@heads[a] for a in range(h)]
    concatenated = np.concatenate(outputs, axis=1)
    attention = concatenated@np.zeros((d, d))
    xp = x+attention
    hidden = np.maximum(norm(xp)@np.zeros((d, dff)), 0)
    y = xp+hidden@np.zeros((dff, d))
    assert z.shape == q.shape == concatenated.shape == xp.shape == y.shape == (3, 4)
    assert heads[0].shape == outputs[0].shape == (3, 2)
    assert weights.shape == (2, 3, 3) and hidden.shape == (3, 16)
    attention_count = sum(np.zeros((d, d//h)).size for _ in range(3*h))+d*d
    ffn_count = np.zeros((d, dff)).size+np.zeros((dff, d)).size
    assert (attention_count, ffn_count, attention_count+ffn_count) == (64, 128, 192)
    close(y, x, atol=1e-12)
    assert np.zeros((2, 5, 5)).size == 50


def example7():
    e = np.array([[1, 0], [0, 1], [-1, -1]])
    u = np.array([2, 1])
    z = u@e.T
    close(z, [2, 1, -3], atol=1e-12)
    close(np.exp(z), [7.389, 2.718, 0.0498], atol=0.0005)
    close(np.exp(z).sum(), 10.157, atol=0.0005)
    p = softmax(z)
    close(p, [0.7275, 0.2676, 0.0049])
    close(-np.log(p[:2]), [0.3182, 1.3182])
    assert 50000*2048 == 102400000


def example8():
    layers, d, dff, vocab, tokens = 32, 4096, 11008, 32000, 2*10**12
    attn = sum(rows*cols for rows, cols in [(d, d)]*4)
    ffn = sum(rows*cols for rows, cols in [(d, dff)]*2+[(dff, d)])
    block = attn+ffn
    embeddings = 2*vocab*d
    matrix_total = layers*block+embeddings
    assert (attn, ffn, block, layers*block, embeddings, matrix_total) == (
        67108864, 135266304, 202375168, 6476005376, 262144000, 6738149376)
    approximate = 12*layers*d*d+vocab*d
    close(approximate, 6.57e9, atol=5e6)
    close((matrix_total-approximate)/matrix_total, 0.025, atol=0.001)
    # Section 3 gives one scale vector per RMSNorm; sections 6-7 give
    # two norms per block and one final norm.
    norm_parameters = sum(d for _ in range(2*layers+1))
    full_total = matrix_total+norm_parameters
    assert norm_parameters == 266240
    assert full_total == 6738415616 and full_total != matrix_total
    lesson = (ROOT / "lesson.md").read_text(encoding="utf-8")
    assert all(str(value) in lesson for value in (matrix_total, norm_parameters, full_total))
    c = 6*matrix_total*tokens
    close(c, 8.1e22, rtol=0.005)
    # Hardware numbers are supplied assumptions, not current hardware facts.
    rate = 3.12e14*0.4
    seconds = c/rate
    close(rate, 1.25e14, rtol=0.003)
    close(seconds, 6.5e8, rtol=0.005)
    close(seconds/3600, 1.8e5, rtol=0.005)
    close(seconds/86400, 7500, rtol=0.005)
    close(2048/(6*4096), 0.08, atol=0.005)
    close(32768/(6*4096), 1.33, atol=0.005)
    # GPT-3 arithmetic in the same section, under the stated approximation.
    close(12*96*12288**2, 1.739e11, rtol=0.001)
    close(50257*12288, 0.62e9, rtol=0.005)
    close(12*96*12288**2+50257*12288, 1.746e11, rtol=0.001)


def example9():
    blocks = 12*24*2048**2
    embedding = 50000*2048
    n = blocks+embedding
    close(blocks, 1.208e9, atol=5e5)
    close(embedding, 1.02e8, atol=5e5)
    close(n, 1.31e9, atol=5e6)
    close(6*n*10**11, 7.9e20, atol=5e18)
    gpt_blocks, gpt_embedding = 12*12*768**2, 50257*768
    close(gpt_blocks, 8.49e7, atol=5e4)
    close(gpt_embedding, 3.86e7, atol=5e4)
    close(gpt_blocks+gpt_embedding, 1.24e8, atol=5e5)
    assert 4*64**2 == 16384 and 3*64*172 == 33024 and 4*64**2+3*64*172 == 49408


if __name__ == "__main__":
    for number in range(1, 10):
        try:
            globals()[f"example{number}"]()
        except Exception as error:
            FAILURES += 1
            print(f"FAIL 例{number} {type(error).__name__}: {error}")
        else:
            note = " (矩阵小计与含归一化参数的总量均已核对)" if number == 8 else ""
            print(f"PASS 例{number}{note}")
    sys.exit(bool(FAILURES))
