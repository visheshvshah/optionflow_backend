from fastapi import APIRouter, Depends, HTTPException, status
import yfinance as yf

from auth import get_current_user

router = APIRouter(prefix="/stock", tags=["stock"])


def get_reliable_price(ticker: str):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="5d")
        if not hist.empty:
            price = float(hist['Close'].iloc[-1])
            return price, "LAST_CLOSE_PRICE"
    except Exception as e:
        print(f"yfinance error: {e}")
    return None, None


@router.get("/price")
def get_stock_price(ticker: str, current_user=Depends(get_current_user)):
    ticker = ticker.strip().upper()
    if "." not in ticker:
        ticker += ".NS"
    price, note = get_reliable_price(ticker)
    if price is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Could not fetch price for {ticker}. Market may be closed or ticker invalid. Try again or enter price manually.",
        )
    return {"ticker": ticker, "price": price, "note": note or "LIVE_PRICE"}
