# OptionFlow

**Full-Stack Options Pricing & Analysis Platform**

A quantitative finance web application that fetches live stock prices and prices European call options using three mathematical methods — Black-Scholes analytical solution, Crank-Nicolson finite difference PDE solver, and Monte Carlo simulation.

Built on top of my MC211 PDE coursework (Black-Scholes Option Pricing) at DAU Gandhinagar.

---

## Live Demo

> Frontend: [optionflow.vercel.app](https://optionflow.vercel.app)  
> Backend API: [optionflow-api.railway.app/docs](https://optionflow-api.railway.app/docs)

---

## What It Does

1. User searches any NSE stock (RELIANCE, TCS, INFY, HDFCBANK...)
2. App fetches the last closing price automatically via Yahoo Finance
3. User adjusts option parameters — Strike Price K, Volatility σ, Risk-free Rate r, Time to Expiry T
4. Backend runs three pricing models simultaneously
5. Results displayed — prices, Greeks dashboard, convergence comparison
6. User can save analyses to their account and view history

---

## Pricing Methods

### 1. Black-Scholes Analytical Solution
Closed-form solution to the Black-Scholes PDE derived using delta hedging and the no-arbitrage condition.

```
V = S·N(d₁) - K·e^(-rT)·N(d₂)
```

where d₁ = [ln(S/K) + (r + σ²/2)T] / σ√T and d₂ = d₁ - σ√T

### 2. Finite Difference — Crank-Nicolson Scheme
Numerical solution to the Black-Scholes PDE by discretising the equation on an M×N grid and solving a tridiagonal system at each time step. Unconditionally stable, second-order accurate.

```
∂V/∂t + ½σ²S²∂²V/∂S² + rS∂V/∂S - rV = 0
```

### 3. Monte Carlo Simulation
Simulates 10,000 GBM stock price paths and averages the discounted payoff. Converges to the Black-Scholes price as paths increase.

```
dS = μS dt + σS dW
Payoff = max(S_T - K, 0)
V = e^(-rT) · E[Payoff]
```

### Validation
For S=2500, K=2500, σ=0.25, r=0.07, T=0.25:
- Black-Scholes: ₹146.40
- Finite Difference: ₹144.78  
- Monte Carlo: ₹146.36

All three methods converge confirming mathematical consistency.

---

## The Greeks

| Greek | Formula | Meaning |
|-------|---------|---------|
| Delta (Δ) | N(d₁) | Option price change per ₹1 stock move |
| Gamma (Γ) | N'(d₁) / Sσ√T | Rate of change of Delta |
| Theta (Θ) | -(SN'(d₁)σ/2√T) - rKe^(-rT)N(d₂) | Daily time decay |
| Vega (V) | S√T·N'(d₁) | Change per 1% volatility increase |
| Rho (ρ) | KTe^(-rT)N(d₂) | Change per 1% interest rate increase |

---

## Tech Stack

### Frontend
- React (Vite) + React Router
- Chart.js + react-chartjs-2
- Axios for API calls
- Terminal/Bloomberg-style dark UI

### Backend
- FastAPI (Python)
- SQLAlchemy ORM
- yfinance for live stock data
- NumPy + SciPy for mathematical computations
- JWT authentication via python-jose + passlib

### Database
- PostgreSQL (Supabase) in production
- SQLite for local development

### Deployment
- Frontend: Vercel
- Backend: Railway
- Database: Supabase

---

## System Architecture

```
User → React Frontend (Vercel)
          ↓ HTTP REST API
       FastAPI Backend (Railway)
          ↓                ↓
     PostgreSQL        Yahoo Finance
     (Supabase)         (yfinance)
          ↓
    quant/ module
    ├── black_scholes.py
    ├── finite_difference.py
    └── monte_carlo.py
```

**Request flow:**
1. React sends POST /analyse with parameters + JWT token
2. FastAPI verifies token
3. FastAPI fetches live price via yfinance
4. Math module runs BS + FD + MC simultaneously
5. Results returned as JSON
6. React renders charts and Greeks dashboard

---

## API Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | /auth/signup | Create account | No |
| POST | /auth/login | Login, get JWT | No |
| GET | /stock/price?ticker= | Fetch live price | Yes |
| POST | /analyse | Run all 3 models | Yes |
| POST | /analyses/save | Save to database | Yes |
| GET | /analyses/history | Get user history | Yes |
| DELETE | /analyses/{id} | Delete analysis | Yes |

---

## Database Schema

```
users
├── id (PK)
├── email (unique)
├── hashed_password
└── created_at

analyses
├── id (PK)
├── user_id (FK → users)
├── ticker, stock_price
├── strike_K, sigma, rate_r, expiry_T
├── bs_price, fd_price, mc_price
└── created_at

greeks
├── id (PK)
├── analysis_id (FK → analyses)
└── delta, gamma, theta, vega, rho
```

---

## Local Setup

### Backend
```bash
cd optionflow-backend
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Frontend
```bash
cd optionflow-frontend
npm install
npm run dev
```

### Environment Variables (backend .env)
```
SECRET_KEY=your_secret_key
DATABASE_URL=sqlite:///./optionflow.db
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
```

---

## Mathematical Background

This project implements the Black-Scholes framework derived in my PDE coursework:

- **GBM Model:** Stock prices follow dS = μS dt + σS dW
- **Delta Hedging:** Risk-free portfolio by holding -Δ shares per option eliminates the stochastic term
- **No-Arbitrage:** Risk-free portfolio must earn risk-free rate r
- **PDE Derivation:** Applying Itô's Lemma + no-arbitrage yields the BS PDE
- **Heat Equation Connection:** BS PDE is mathematically equivalent to the heat diffusion equation

---

## Author

**Vishesh Shah**