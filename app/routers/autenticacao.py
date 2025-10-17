# app/routers/autenticacao.py

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..models import models
from ..schemas import schemas
from ..core import security

router = APIRouter()

@router.post("/registrar", response_model=schemas.UserSchema, tags=["Autenticação"])
def registrar_usuario(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
   
    normalized_email = user.email.lower()

    if not (normalized_email.endswith('.com') or normalized_email.endswith('.com.br')):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email domain. Only '.com' and '.com.br' are allowed."
        )

   
    if not security.validate_password(user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The password must have at least 6 characters, one capital letter and one special character (#$%-@&*)."
        )
    
    
    db_user = db.query(models.Usuario).filter(models.Usuario.email == normalized_email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered.")
    
   
    hashed_password = security.hash_password(user.password)
    db_user = models.Usuario(email=normalized_email, hashed_password=hashed_password)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login", response_model=schemas.Token, tags=["Autenticação"])
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    
    
    normalized_email = form_data.username.lower()
    
    user = db.query(models.Usuario).filter(models.Usuario.email == normalized_email).first()
    
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = security.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}