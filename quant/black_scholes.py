import numpy as np
from scipy.stats import norm


def calculate_d1(S: float, K: float, r: float, sigma: float, T: float) -> float:
    return (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))


def calculate_d2(d1: float, sigma: float, T: float) -> float:
    return d1 - sigma * np.sqrt(T)


def black_scholes_call(S: float, K: float, r: float, sigma: float, T: float) -> float:
    d1 = calculate_d1(S, K, r, sigma, T)
    d2 = calculate_d2(d1, sigma, T)
    return float(S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2))


def calculate_greeks(S: float, K: float, r: float, sigma: float, T: float) -> dict:
    d1 = calculate_d1(S, K, r, sigma, T)
    d2 = calculate_d2(d1, sigma, T)
    pdf_d1 = norm.pdf(d1)
    delta = float(norm.cdf(d1))
    gamma = float(pdf_d1 / (S * sigma * np.sqrt(T)))
    theta = float((-(S * pdf_d1 * sigma) / (2 * np.sqrt(T)) - r * K * np.exp(-r * T) * norm.cdf(d2)) / 365)
    vega = float(S * np.sqrt(T) * pdf_d1 / 100)
    rho = float(K * T * np.exp(-r * T) * norm.cdf(d2) / 100)
    return {
        "delta": delta,
        "gamma": gamma,
        "theta": theta,
        "vega": vega,
        "rho": rho,
    }
