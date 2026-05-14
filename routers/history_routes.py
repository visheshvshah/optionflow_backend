from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from auth import get_current_user, get_db
from models import Analysis, Greeks

router = APIRouter(tags=["history"])


class GreeksPayload(BaseModel):
    delta: float
    gamma: float
    theta: float
    vega: float
    rho: float


class SaveAnalysisRequest(BaseModel):
    ticker: str
    stock_price: float
    strike_K: float
    sigma: float
    rate_r: float
    expiry_T: float
    bs_price: float
    fd_price: float
    mc_price: float
    greeks: GreeksPayload


@router.post("/analyses/save")
def save_analysis(
    payload: SaveAnalysisRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    analysis = Analysis(
        user_id=current_user.id,
        ticker=payload.ticker,
        stock_price=payload.stock_price,
        strike_K=payload.strike_K,
        sigma=payload.sigma,
        rate_r=payload.rate_r,
        expiry_T=payload.expiry_T,
        bs_price=payload.bs_price,
        fd_price=payload.fd_price,
        mc_price=payload.mc_price,
    )
    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    greeks = Greeks(
        analysis_id=analysis.id,
        delta=payload.greeks.delta,
        gamma=payload.greeks.gamma,
        theta=payload.greeks.theta,
        vega=payload.greeks.vega,
        rho=payload.greeks.rho,
    )
    db.add(greeks)
    db.commit()

    return {"message": "Analysis saved", "id": analysis.id}


@router.get("/analyses/history")
def get_history(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    analyses = (
        db.query(Analysis)
        .filter(Analysis.user_id == current_user.id)
        .order_by(Analysis.created_at.desc())
        .all()
    )
    analysis_ids = [analysis.id for analysis in analyses]
    greeks_rows = db.query(Greeks).filter(Greeks.analysis_id.in_(analysis_ids)).all() if analysis_ids else []
    greeks_map = {row.analysis_id: row for row in greeks_rows}

    results = []
    for analysis in analyses:
        greeks = greeks_map.get(analysis.id)
        results.append(
            {
                "id": analysis.id,
                "ticker": analysis.ticker,
                "stock_price": analysis.stock_price,
                "strike_K": analysis.strike_K,
                "sigma": analysis.sigma,
                "rate_r": analysis.rate_r,
                "expiry_T": analysis.expiry_T,
                "bs_price": analysis.bs_price,
                "fd_price": analysis.fd_price,
                "mc_price": analysis.mc_price,
                "created_at": analysis.created_at,
                "greeks": {
                    "delta": greeks.delta,
                    "gamma": greeks.gamma,
                    "theta": greeks.theta,
                    "vega": greeks.vega,
                    "rho": greeks.rho,
                }
                if greeks
                else None,
            }
        )
    return results


@router.delete("/analyses/{analysis_id}")
def delete_analysis(
    analysis_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
    if analysis is None or analysis.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found",
        )
    db.query(Greeks).filter(Greeks.analysis_id == analysis_id).delete()
    db.delete(analysis)
    db.commit()
    return {"message": "Deleted successfully"}
