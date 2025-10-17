# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.database import engine
from .models import models
from .routers import autenticacao, transacoes

# Cria as tabelas no banco de dados (é importante que isso aconteça antes de tudo)
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configuração do CORS
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "http://localhost:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui os routers
app.include_router(autenticacao.router)
app.include_router(transacoes.router)