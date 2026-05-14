from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class AnalysisBase(BaseModel):
    ticker: str
    stock_price: float
    strike_K: float
    sigma: float
    rate_r: float
    expiry_T: float

class AnalysisCreate(AnalysisBase):
    pass

class Analysis(AnalysisBase):
    id: int
    user_id: int
    bs_price: Optional[float]
    fd_price: Optional[float]
    mc_price: Optional[float]
    created_at: datetime

    class Config:
        from_attributes = True

class GreeksBase(BaseModel):
    delta: float
    gamma: float
    theta: float
    vega: float
    rho: float

class GreeksCreate(GreeksBase):
    pass

class Greeks(GreeksBase):
    id: int
    analysis_id: int

    class Config:
        from_attributes = True