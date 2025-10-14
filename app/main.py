# =======================================================================
# 1. IMPORTAÇÕES
# =======================================================================
import re
import datetime
from datetime import timedelta
from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy import (Column, DateTime, Float, ForeignKey, Integer, String,
                        create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

# =======================================================================
# 2. CONFIGURAÇÕES GLOBAIS
# =======================================================================
# --- CONFIGURAÇÃO DO TOKEN JWT ---
SECRET_KEY = "Microsatelite_Em_Orbita"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# --- CONFIGURAÇÃO DE SENHAS ---
pwd_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")

# --- CONFIGURAÇÃO DO BANCO DE DADOS ---
DATABASE_URL = "sqlite:///./app/financeiro.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# =======================================================================
# 3. MODELOS DO BANCO DE DADOS (SQLAlchemy)
# =======================================================================
class Transacao(Base):
    __tablename__ = "transacoes"
    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String, index=True)
    valor = Column(Float)
    tipo = Column(String)
    data = Column(DateTime, default=datetime.datetime.utcnow)
    owner_id = Column(Integer, ForeignKey("usuarios.id"))

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

Base.metadata.create_all(bind=engine)

# =======================================================================
# 4. SCHEMAS DE DADOS (Pydantic)
# =======================================================================
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

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class UserSchema(UserBase):
    id: int
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

# =======================================================================
# 5. FUNÇÕES DE UTILIDADE E DEPENDÊNCIAS
# =======================================================================
def validate_password(password: str):
    if len(password) < 6:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[-!@#$%^&*(),.?\":{}|<>]", password):
        return False
    return True

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(Usuario).filter(Usuario.email == email).first()
    if user is None:
        raise credentials_exception
    return user

# =======================================================================
# 6. INICIALIZAÇÃO DO APP FASTAPI
# =======================================================================
app = FastAPI()

# =======================================================================
# 7. CONFIGURAÇÃO DO CORS
# =======================================================================
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

# =======================================================================
# 8. ROTAS DA API
# =======================================================================

# --- ROTAS DE AUTENTICAÇÃO ---
@app.post("/registrar", response_model=UserSchema, tags=["Autenticação"])
def registrar_usuario(user: UserCreate, db: Session = Depends(get_db)):
    if not validate_password(user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A senha deve ter no mínimo 6 caracteres, uma letra maiúscula e um caractere especial(#$%-@&*)."
        )
    
    normalized_email = user.email.lower()
    db_user = db.query(Usuario).filter(Usuario.email == normalized_email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="E-mail já registrado")
    
    hashed_password = hash_password(user.password)
    db_user = Usuario(email=normalized_email, hashed_password=hashed_password)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/login", response_model=Token, tags=["Autenticação"])
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    normalized_email = form_data.username.lower()
    user = db.query(Usuario).filter(Usuario.email == normalized_email).first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="E-mail ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# --- ROTAS DE TRANSAÇÕES ---
@app.post("/transacoes/", response_model=TransacaoSchema, tags=["Transações"])
def criar_transacao(transacao: TransacaoCreate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    nova_transacao = Transacao(**transacao.dict(), owner_id=current_user.id)
    db.add(nova_transacao)
    db.commit()
    db.refresh(nova_transacao)
    return nova_transacao

@app.get("/transacoes/", response_model=List[TransacaoSchema], tags=["Transações"])
def ler_transacoes(db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    transacoes = db.query(Transacao).filter(Transacao.owner_id == current_user.id).all()
    return transacoes

@app.get("/transacoes/{transacao_id}", response_model=TransacaoSchema, tags=["Transações"])
def ler_transacao_por_id(transacao_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    transacao = db.query(Transacao).filter(Transacao.id == transacao_id, Transacao.owner_id == current_user.id).first()
    if transacao is None:
        raise HTTPException(status_code=404, detail="Transação não encontrada")
    return transacao

@app.put("/transacoes/{transacao_id}", response_model=TransacaoSchema, tags=["Transações"])
def atualizar_transacao(transacao_id: int, transacao: TransacaoCreate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    db_transacao = db.query(Transacao).filter(Transacao.id == transacao_id, Transacao.owner_id == current_user.id).first()
    if db_transacao is None:
        raise HTTPException(status_code=404, detail="Transação não encontrada")

    for key, value in transacao.dict().items():
        setattr(db_transacao, key, value)
    
    db.commit()
    db.refresh(db_transacao)
    return db_transacao

@app.delete("/transacoes/{transacao_id}", tags=["Transações"])
def deletar_transacao(transacao_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    db_transacao = db.query(Transacao).filter(Transacao.id == transacao_id, Transacao.owner_id == current_user.id).first()
    if db_transacao is None:
        raise HTTPException(status_code=404, detail="Transação não encontrada")
    
    db.delete(db_transacao)
    db.commit()
    return {"mensagem": "Transação deletada com sucesso"}

@app.get("/saldo/", tags=["Transações"])
def get_saldo(db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    transacoes = db.query(Transacao).filter(Transacao.owner_id == current_user.id).all()
    total_entradas = sum(t.valor for t in transacoes if t.tipo == 'entrada')
    total_saidas = sum(t.valor for t in transacoes if t.tipo == 'saida')
    saldo = total_entradas - total_saidas
    
    return {
        "total_entradas": round(total_entradas, 2),
        "total_saidas": round(total_saidas, 2),
        "saldo": round(saldo, 2)
    }