from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import auth_routes, stock_routes, analyse_routes, history_routes

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router)
app.include_router(stock_routes.router)
app.include_router(analyse_routes.router)
app.include_router(history_routes.router)

@app.on_event("startup")
async def startup_event():
    from database import engine
    from models import Base
    Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "OptionFlow backend is running"}