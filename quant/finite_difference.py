import numpy as np
from numpy.linalg import solve


def crank_nicolson_call(S: float, K: float, r: float, sigma: float, T: float, S_max: float = None, M: int = 100, N: int = 1000) -> float:
    if S_max is None:
        S_max = 4 * K

    S_grid = np.linspace(0, S_max, M + 1)
    dt = T / N
    V = np.maximum(S_grid - K, 0.0)

    size = M - 1
    i = np.arange(1, M)
    sigma2 = sigma ** 2
    a = 0.25 * dt * (sigma2 * i ** 2 - r * i)
    b = -0.5 * dt * (sigma2 * i ** 2 + r)
    c = 0.25 * dt * (sigma2 * i ** 2 + r * i)

    A = np.zeros((size, size))
    B = np.zeros((size, size))
    for idx in range(size):
        A[idx, idx] = 1.0 - b[idx]
        B[idx, idx] = 1.0 + b[idx]
        if idx > 0:
            A[idx, idx - 1] = -a[idx]
            B[idx, idx - 1] = a[idx]
        if idx < size - 1:
            A[idx, idx + 1] = -c[idx]
            B[idx, idx + 1] = c[idx]

    for n in range(N):
        t_curr = T - n * dt
        V_right = S_max - K * np.exp(-r * (T - t_curr))

        V_inner = V[1:-1]
        rhs = B.dot(V_inner)
        rhs[0] += a[0] * 0.0
        rhs[-1] += c[-1] * V_right

        V_inner = solve(A, rhs)
        t_prev = T - (n + 1) * dt
        V_right_prev = S_max - K * np.exp(-r * (T - t_prev))
        V = np.concatenate(([0.0], V_inner, [V_right_prev]))

    return float(np.interp(S, S_grid, V))
