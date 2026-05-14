import numpy as np


def monte_carlo_call(S: float, K: float, r: float, sigma: float, T: float, num_paths: int = 10000) -> float:
    np.random.seed(42)
    Z = np.random.randn(num_paths)
    S_final = S * np.exp((r - 0.5 * sigma ** 2) * T + sigma * np.sqrt(T) * Z)
    payoffs = np.maximum(S_final - K, 0)
    return float(np.mean(payoffs) * np.exp(-r * T))
