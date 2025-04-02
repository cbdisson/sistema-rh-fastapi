from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from database import UsuarioRH, get_db
from models import UsuarioRHCreate, Token, UsuarioRH as UsuarioRHModel
from auth import (
    criar_hash_senha,
    verificar_senha,
    criar_access_token,
    get_usuario_admin
)

router = APIRouter()

@router.post("/rh/cadastrar", status_code=status.HTTP_201_CREATED)
def cadastrar_usuario_rh(
    usuario: UsuarioRHCreate,
    db: Session = Depends(get_db)
):
    """Cadastro de usuários no RH"""
    
    db_usuario = UsuarioRH(
        email=usuario.email,
        nome=usuario.nome,
        senha_hash=criar_hash_senha(usuario.senha),
        nivel_acesso=usuario.nivel_acesso
    )
    db.add(db_usuario)
    try:
        db.commit()
        return {"mensagem": "Usuário RH cadastrado com sucesso"}
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado"
        )

@router.post("/rh/login", response_model=Token)
def login_rh(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Autenticação de usuário e geração do token JWT"""
    
    usuario = db.query(UsuarioRH).filter(UsuarioRH.email == form_data.username).first()
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não encontrado"
        )

    if not verificar_senha(form_data.password, usuario.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Senha incorreta"
        )
    
    access_token = criar_access_token(
        data={"sub": usuario.email, "nivel": usuario.nivel_acesso}
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/rh/usuarios", response_model=List[UsuarioRHModel])
def listar_usuarios_rh(
    db: Session = Depends(get_db),
    current_user: UsuarioRH = Depends(get_usuario_admin)
):
    """Listagem de usuários RH (apenas para administradores)"""
    
    usuarios = db.query(UsuarioRH).all()
    return usuarios
