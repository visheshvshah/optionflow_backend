from fastapi import APIRouter, Depends
from pydantic import BaseModel

from auth import get_current_user
from quant.black_scholes import black_scholes_call, calculate_greeks
from quant.finite_difference import crank_nicolson_call
from quant.monte_carlo import monte_carlo_call

router = APIRouter(tags=["analyse"])


class AnalyseRequest(BaseModel):
    ticker: str
    stock_price: float
    strike_K: float
    sigma: float
    rate_r: float
    expiry_T: float


@router.post("/analyse")
def analyse(request: AnalyseRequest, current_user=Depends(get_current_user)):
    bs_price = black_scholes_call(
        request.stock_price,
        request.strike_K,
        request.rate_r,
        request.sigma,
        request.expiry_T,
    )
    fd_price = crank_nicolson_call(
        request.stock_price,
        request.strike_K,
        request.rate_r,
        request.sigma,
        request.expiry_T,
    )
    mc_price = monte_carlo_call(
        request.stock_price,
        request.strike_K,
        request.rate_r,
        request.sigma,
        request.expiry_T,
    )
    greeks = calculate_greeks(
        request.stock_price,
        request.strike_K,
        request.rate_r,
        request.sigma,
        request.expiry_T,
    )
    return {
        "ticker": request.ticker,
        "stock_price": request.stock_price,
        "strike_K": request.strike_K,
        "sigma": request.sigma,
        "rate_r": request.rate_r,
        "expiry_T": request.expiry_T,
        "bs_price": round(bs_price, 2),
        "fd_price": round(fd_price, 2),
        "mc_price": round(mc_price, 2),
        "greeks": {
            "delta": round(greeks["delta"], 4),
            "gamma": round(greeks["gamma"], 6),
            "theta": round(greeks["theta"], 4),
            "vega": round(greeks["vega"], 4),
            "rho": round(greeks["rho"], 4),
        },
    }
