from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles      # <-- LINHA ADICIONADA
from starlette.responses import FileResponse    # <-- LINHA ADICIONADA
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from typing import List
import datetime

# 1. Configurando a conexão com o banco de dados
DATABASE_URL = "sqlite:///./app/financeiro.db" # Corrigindo o caminho para o DB ficar dentro da pasta app
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# 2. Criando uma sessão para conversar com o banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- Nossas "cestas" Pydantic (Schemas) ---

class TransacaoBase(BaseModel):
    descricao: str
    valor: float
    tipo: str

class TransacaoCreate(TransacaoBase):
    pass

class TransacaoSchema(TransacaoBase):
    id: int
    data: datetime.datetime

    class Config:
        from_attributes = True

# 3. Desenhando a nossa "tabela" de transações (Model do SQLAlchemy)
class Transacao(Base):
    __tablename__ = "transacoes"
    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String, index=True)
    valor = Column(Float)
    tipo = Column(String)
    data = Column(DateTime, default=datetime.datetime.utcnow)

# 4. Criando a tabela no banco de dados
Base.metadata.create_all(bind=engine)

# Criando nossa aplicação FastAPI
app = FastAPI()

# --- MONTAGEM DO FRONTEND ---
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
async def root():
    return FileResponse('app/static/index.html')
# --- FIM DA MONTAGEM DO FRONTEND ---


# --- CONFIGURAÇÃO DO CORS ---
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Dependência para ter a nossa "linha telefônica" com o banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Nossas rotas da API (CRUD Inteligente) ---
# ... (TODAS AS SUAS ROTAS @app.post, @app.get, etc. CONTINUAM AQUI, SEM MUDANÇA) ...
@app.post("/transacoes/", response_model=TransacaoSchema)
def criar_transacao(transacao: TransacaoCreate, db: Session = Depends(get_db)):
    nova_transacao = Transacao(**transacao.dict())
    db.add(nova_transacao)
    db.commit()
    db.refresh(nova_transacao)
    return nova_transacao

@app.get("/transacoes/", response_model=List[TransacaoSchema])
def ler_transacoes(db: Session = Depends(get_db)):
    transacoes = db.query(Transacao).all()
    return transacoes

@app.get("/transacoes/{transacao_id}", response_model=TransacaoSchema)
def ler_transacao_por_id(transacao_id: int, db: Session = Depends(get_db)):
    transacao = db.query(Transacao).filter(Transacao.id == transacao_id).first()
    if transacao is None:
        raise HTTPException(status_code=404, detail="Transação não encontrada")
    return transacao

@app.put("/transacoes/{transacao_id}", response_model=TransacaoSchema)
def atualizar_transacao(transacao_id: int, transacao: TransacaoCreate, db: Session = Depends(get_db)):
    db_transacao = db.query(Transacao).filter(Transacao.id == transacao_id).first()
    if db_transacao is None:
        raise HTTPException(status_code=404, detail="Transação não encontrada")

    for key, value in transacao.dict().items():
        setattr(db_transacao, key, value)
    
    db.commit()
    db.refresh(db_transacao)
    return db_transacao

@app.delete("/transacoes/{transacao_id}")
def deletar_transacao(transacao_id: int, db: Session = Depends(get_db)):
    db_transacao = db.query(Transacao).filter(Transacao.id == transacao_id).first()
    if db_transacao is None:
        raise HTTPException(status_code=404, detail="Transação não encontrada")
    
    db.delete(db_transacao)
    db.commit()
    return {"mensagem": "Transação deletada com sucesso"}

# --- Rotas de Lógica de Negócio ---

@app.get("/saldo/")
def get_saldo(db: Session = Depends(get_db)):
    transacoes = db.query(Transacao).all()
    total_entradas = sum(t.valor for t in transacoes if t.tipo == 'entrada')
    total_saidas = sum(t.valor for t in transacoes if t.tipo == 'saida')
    saldo = total_entradas - total_saidas
    
    return {
        "total_entradas": round(total_entradas, 2),
        "total_saidas": round(total_saidas, 2),
        "saldo": round(saldo, 2)
    }