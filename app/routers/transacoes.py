# app/routers/transacoes.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..models import models
from ..schemas import schemas
from ..core.security import get_current_user

router = APIRouter()

@router.post("/transacoes/", response_model=schemas.TransacaoSchema, tags=["Transações"])
def criar_transacao(transacao: schemas.TransacaoCreate, db: Session = Depends(get_db), current_user: models.Usuario = Depends(get_current_user)):
    nova_transacao = models.Transacao(**transacao.dict(), owner_id=current_user.id)
    db.add(nova_transacao)
    db.commit()
    db.refresh(nova_transacao)
    return nova_transacao

@router.get("/transacoes/", response_model=List[schemas.TransacaoSchema], tags=["Transações"])
def ler_transacoes(db: Session = Depends(get_db), current_user: models.Usuario = Depends(get_current_user)):
    transacoes = db.query(models.Transacao).filter(models.Transacao.owner_id == current_user.id).all()
    return transacoes

@router.get("/transacoes/{transacao_id}", response_model=schemas.TransacaoSchema, tags=["Transações"])
def ler_transacao_por_id(transacao_id: int, db: Session = Depends(get_db), current_user: models.Usuario = Depends(get_current_user)):
    transacao = db.query(models.Transacao).filter(models.Transacao.id == transacao_id, models.Transacao.owner_id == current_user.id).first()
    if transacao is None:
        raise HTTPException(status_code=404, detail="Transação não encontrada")
    return transacao

@router.put("/transacoes/{transacao_id}", response_model=schemas.TransacaoSchema, tags=["Transações"])
def atualizar_transacao(transacao_id: int, transacao: schemas.TransacaoCreate, db: Session = Depends(get_db), current_user: models.Usuario = Depends(get_current_user)):
    db_transacao = db.query(models.Transacao).filter(models.Transacao.id == transacao_id, models.Transacao.owner_id == current_user.id).first()
    if db_transacao is None:
        raise HTTPException(status_code=404, detail="Transação não encontrada")

    for key, value in transacao.dict().items():
        setattr(db_transacao, key, value)
    
    db.commit()
    db.refresh(db_transacao)
    return db_transacao

@router.delete("/transacoes/{transacao_id}", tags=["Transações"])
def deletar_transacao(transacao_id: int, db: Session = Depends(get_db), current_user: models.Usuario = Depends(get_current_user)):
    db_transacao = db.query(models.Transacao).filter(models.Transacao.id == transacao_id, models.Transacao.owner_id == current_user.id).first()
    if db_transacao is None:
        raise HTTPException(status_code=404, detail="Transação não encontrada")
    
    db.delete(db_transacao)
    db.commit()
    return {"mensagem": "Transação deletada com sucesso"}


@router.get("/saldo", tags=["Transações"]) 
def get_saldo(db: Session = Depends(get_db), current_user: models.Usuario = Depends(get_current_user)):
    transacoes = db.query(models.Transacao).filter(models.Transacao.owner_id == current_user.id).all()
    total_entradas = sum(t.valor for t in transacoes if t.tipo == 'entrada')
    total_saidas = sum(t.valor for t in transacoes if t.tipo == 'saida')
    saldo = total_entradas - total_saidas
    
    return {
        "total_entradas": round(total_entradas, 2),
        "total_saidas": round(total_saidas, 2),
        "saldo": round(saldo, 2)
    }