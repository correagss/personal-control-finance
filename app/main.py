# =======================================================================
# 1. IMPORTAÇÕES (TUDO JUNTO AQUI)
# =======================================================================
import datetime
from datetime import timedelta
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy import (Column, DateTime, Float, Integer, String,
                        create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from starlette.responses import FileResponse

# =======================================================================
# 2. CONFIGURAÇÕES GLOBAIS
# =======================================================================
# --- CONFIGURAÇÃO DO TOKEN JWT ---
SECRET_KEY = "Microsatelite_Em_Orbita"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

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

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

# Cria as tabelas no banco de dados
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

# =======================================================================
# 6. INICIALIZAÇÃO DO APP FASTAPI
# =======================================================================
app = FastAPI()

# =======================================================================
# 7. MONTAGEM DO FRONTEND E CORS
# =======================================================================
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/", include_in_schema=False)
async def root():
    return FileResponse('app/static/index.html')

origins = ["http://localhost", "http://localhost:8080", "http://127.0.0.1:8080"]
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
    db_user = db.query(Usuario).filter(Usuario.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="E-mail já registrado")
    hashed_password = hash_password(user.password)
    db_user = Usuario(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/login", response_model=Token, tags=["Autenticação"])
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.query(Usuario).filter(Usuario.email == form_data.username).first()
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
def criar_transacao(transacao: TransacaoCreate, db: Session = Depends(get_db)):
    nova_transacao = Transacao(**transacao.dict())
    db.add(nova_transacao)
    db.commit()
    db.refresh(nova_transacao)
    return nova_transacao

@app.get("/transacoes/", response_model=List[TransacaoSchema], tags=["Transações"])
def ler_transacoes(db: Session = Depends(get_db)):
    transacoes = db.query(Transacao).all()
    return transacoes

# ... (o resto das suas rotas de transações e saldo continuam aqui)
# (Eu adicionei 'tags' para organizar melhor seus docs!)
# ...