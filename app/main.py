
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.database import engine
from .models import models
from .routers import autenticacao, transacoes


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "http://localhost:5173",
    "https://personal-finance-app-8tkn.onrender.com",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(autenticacao.router)
app.include_router(transacoes.router)