# app/schemas/schemas.py

from pydantic import BaseModel
import datetime

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