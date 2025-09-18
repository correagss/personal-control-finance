from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import datetime

# 1. Configurando a conexão com o banco de dados (nossa caixa)
DATABASE_URL = "sqlite:///./financeiro.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# 2. Criando uma sessão para conversar com o banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 3. Desenhando a nossa "tabela" de transações
class Transacao(Base):
    __tablename__ = "transacoes"

    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String, index=True)
    valor = Column(Float)
    tipo = Column(String)  # "entrada" ou "saida"
    data = Column(DateTime, default=datetime.datetime.utcnow)

# 4. Criando a tabela no banco de dados
Base.metadata.create_all(bind=engine)

# Criando nossa aplicação FastAPI
app = FastAPI()

# Dependência para ter a nossa "linha telefônica" com o banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Nossas rotas da API (CRUD Completo) ---

# Rota para adicionar uma nova transação (CRIAR)
@app.post("/transacoes/")
def criar_transacao(descricao: str, valor: float, tipo: str, db: Session = Depends(get_db)):
    nova_transacao = Transacao(descricao=descricao, valor=valor, tipo=tipo)
    db.add(nova_transacao)
    db.commit()
    db.refresh(nova_transacao)
    return nova_transacao

# Rota para ver todas as transações (LER TUDO)
@app.get("/transacoes/")
def ler_transacoes(db: Session = Depends(get_db)):
    transacoes = db.query(Transacao).all()
    return transacoes

# Rota para ver UMA transação específica (LER POR ID)
@app.get("/transacoes/{transacao_id}")
def ler_transacao_por_id(transacao_id: int, db: Session = Depends(get_db)):
    transacao = db.query(Transacao).filter(Transacao.id == transacao_id).first()
    if transacao is None:
        raise HTTPException(status_code=404, detail="Transação não encontrada")
    return transacao

# Rota para atualizar uma transação (ATUALIZAR)
@app.put("/transacoes/{transacao_id}")
def atualizar_transacao(transacao_id: int, descricao: str, valor: float, tipo: str, db: Session = Depends(get_db)):
    db_transacao = db.query(Transacao).filter(Transacao.id == transacao_id).first()
    if db_transacao is None:
        raise HTTPException(status_code=404, detail="Transação não encontrada")

    db_transacao.descricao = descricao
    db_transacao.valor = valor
    db_transacao.tipo = tipo
    db.commit()
    db.refresh(db_transacao)
    return db_transacao

# Rota para deletar uma transação (DELETAR)
@app.delete("/transacoes/{transacao_id}")
def deletar_transacao(transacao_id: int, db: Session = Depends(get_db)):
    db_transacao = db.query(Transacao).filter(Transacao.id == transacao_id).first()
    if db_transacao is None:
        raise HTTPException(status_code=404, detail="Transação não encontrada")
    
    db.delete(db_transacao)
    db.commit()
    return {"mensagem": "Transação deletada com sucesso"}