import warnings
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from models import TokenData
from database import get_db
import sqlite3

# Configurações JWT
SECRET_KEY = "sua-chave-secreta-super-segura-aqui"  # Em produção, use uma chave segura!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Ignorar warnings do passlib
warnings.filterwarnings("ignore", category=UserWarning, module="passlib")

# Configuração do CryptContext
pwd_context = CryptContext(
    schemes=["bcrypt"],
    bcrypt__rounds=12,
    deprecated="auto"
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/rh/login")

def criar_hash_senha(senha: str) -> str:
    """Cria um hash seguro da senha usando bcrypt"""
    return pwd_context.hash(senha)

def verificar_senha(senha: str, hash_senha: str) -> bool:
    """Verifica se a senha corresponde ao hash"""
    try:
        return pwd_context.verify(senha, hash_senha)
    except Exception as e:
        print(f"Erro ao verificar senha: {str(e)}")
        return False

def criar_access_token(data: dict) -> str:
    """Cria um token JWT com os dados do usuário"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_usuario_atual(token: str = Depends(oauth2_scheme)):
    """Obtém o usuário atual baseado no token JWT"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios_rh WHERE email = ?", (token_data.email,))
        usuario = cursor.fetchone()
        
        if usuario is None:
            raise credentials_exception
            
        return usuario
    except Exception as e:
        print(f"Erro ao buscar usuário: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao processar a requisição"
        )
    finally:
        if conn:
            conn.close()

async def get_usuario_admin(usuario_atual: dict = Depends(get_usuario_atual)):
    """Verifica se o usuário atual é admin"""
    if usuario_atual["nivel_acesso"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso restrito a administradores"
        )
    return usuario_atual