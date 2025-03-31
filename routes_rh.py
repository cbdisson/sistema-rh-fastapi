from fastapi import APIRouter, HTTPException, status
from models import UsuarioRHCreate, UsuarioRHLogin, Token
from auth import (
    criar_hash_senha,
    verificar_senha,
    criar_access_token,
    get_usuario_atual
)
from database import get_db
import sqlite3

router = APIRouter()

@router.post("/rh/cadastrar", status_code=status.HTTP_201_CREATED)
def cadastrar_usuario_rh(usuario: UsuarioRHCreate):
    """Cadastra um novo usuário do RH"""
    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO usuarios_rh (email, nome, senha_hash, nivel_acesso) VALUES (?, ?, ?, ?)",
            (
                usuario.email,
                usuario.nome,
                criar_hash_senha(usuario.senha),
                usuario.nivel_acesso
            )
        )
        conn.commit()
        return {"mensagem": "Usuário RH cadastrado com sucesso"}
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado"
        )
    finally:
        conn.close()

@router.post("/rh/login", response_model=Token)
def login_rh(credenciais: UsuarioRHLogin):
    """Rota de login que retorna um token JWT"""
    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios_rh WHERE email = ?", (credenciais.email,))
        usuario = cursor.fetchone()
        
        if not usuario or not verificar_senha(credenciais.senha, usuario["senha_hash"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ou senha incorretos"
            )
        
        access_token = criar_access_token(
            data={"sub": usuario["email"], "nivel": usuario["nivel_acesso"]}
        )
        
        return {"access_token": access_token, "token_type": "bearer"}
    finally:
        conn.close()