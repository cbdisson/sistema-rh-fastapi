from datetime import datetime, timedelta
import os
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from models import TokenData
from database import get_db, UsuarioRH as UsuarioRHDB
from sqlalchemy.orm import Session

# 🔐 Carregando Configurações Seguras do .env
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

if not SECRET_KEY:
    raise ValueError("SECRET_KEY não está definida no .env!")

# 🔒 Configuração de Criptografia de Senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 🔑 Configuração do OAuth2 para autenticação via Swagger
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/rh/login", scheme_name="Bearer")

# 🔑 Função para criar hash de senha
def criar_hash_senha(senha: str) -> str:
    """Gera um hash seguro para a senha."""
    return pwd_context.hash(senha)

# 🔍 Função para verificar senha
def verificar_senha(senha: str, hash_senha: str) -> bool:
    """Verifica se a senha fornecida corresponde ao hash armazenado."""
    return pwd_context.verify(senha, hash_senha)

# 🏷️ Função para criar token JWT
def criar_access_token(data: dict) -> str:
    """
    Cria um token JWT para autenticação.
    :param data: Dados a serem codificados no token.
    :return: Token JWT como string.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# 🔓 Função para obter usuário atual com base no token JWT
async def get_usuario_atual(
    token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_db)
) -> Optional[UsuarioRHDB]:
    """
    Obtém o usuário autenticado com base no token JWT.
    :param token: Token JWT do usuário.
    :param db: Sessão do banco de dados.
    :return: Usuário autenticado.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido ou expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decodifica o token JWT
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: Optional[str] = payload.get("sub")
        nivel_acesso: Optional[str] = payload.get("nivel")

        if not email or not nivel_acesso:
            raise credentials_exception

        token_data = TokenData(email=email, nivel_acesso=nivel_acesso)

    except JWTError as e:
        print(f"[ERRO JWT] {str(e)}")  # Log de erro
        raise credentials_exception
    
    # Verifica se o usuário existe no banco de dados
    usuario = db.query(UsuarioRHDB).filter(UsuarioRHDB.email == token_data.email).first()
    
    if not usuario:
        print(f"[ERRO] Usuário não encontrado: {token_data.email}")  # Log para debug
        raise credentials_exception
        
    return usuario

# 🔐 Função para verificar se o usuário é administrador
async def get_usuario_admin(usuario_atual: UsuarioRHDB = Depends(get_usuario_atual)) -> UsuarioRHDB:
    """
    Verifica se o usuário autenticado tem permissão de administrador.
    :param usuario_atual: Usuário autenticado.
    :return: Usuário se for admin.
    """
    if usuario_atual.nivel_acesso != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso restrito a administradores"
        )
    return usuario_atual
