from pydantic import BaseModel, Field, EmailStr
from datetime import date
from typing import Optional

# --- Modelos de Funcionário ---
class FuncionarioBase(BaseModel):
    cpf: str = Field(..., pattern=r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', example="123.456.789-09")
    nome: str = Field(..., max_length=100, example="João Silva")
    data_nascimento: Optional[date] = None
    cargo: str = Field(..., example="Analista de RH")
    salario: float = Field(..., gt=0, example=5000.00)
    departamento: str = Field(..., example="Recursos Humanos")

class FuncionarioCreate(FuncionarioBase):
    pass

class FuncionarioUpdate(BaseModel):
    nome: Optional[str] = Field(None, max_length=100)
    cargo: Optional[str] = None
    salario: Optional[float] = Field(None, gt=0)
    departamento: Optional[str] = None

class FuncionarioResponse(FuncionarioBase):
    id: int
    criado_em: str

# --- Modelos de Autenticação ---
class UsuarioRHBase(BaseModel):
    email: EmailStr = Field(..., example="admin@empresa.com")
    nome: str = Field(..., example="Admin do RH")
    nivel_acesso: str = Field(..., pattern="^(admin|gerente|assistente)$", example="admin")

class UsuarioRHCreate(UsuarioRHBase):
    senha: str = Field(..., min_length=8, example="senhaSegura123")

class UsuarioRHLogin(BaseModel):
    email: EmailStr
    senha: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """Modelo para dados contidos no token JWT"""
    email: str | None = None
    nivel_acesso: str | None = None

class Token(BaseModel):
    """Modelo para resposta de login"""
    access_token: str
    token_type: str