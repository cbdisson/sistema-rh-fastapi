from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr
from sqlalchemy import Column, Integer, String, Date, Numeric, Boolean, TIMESTAMP, Text, ForeignKey, func
from sqlalchemy.orm import relationship
from database import Base

# ==============================
# MODELO DO BANCO DE DADOS
# ==============================

class BeneficiarioDB(Base):
    __tablename__ = "beneficiarios"
    
    id = Column(Integer, primary_key=True, index=True)
    funcionario_id = Column(Integer, ForeignKey('funcionarios.id', ondelete="CASCADE"), nullable=False)
    nome = Column(String(100), nullable=False)
    data_nascimento = Column(Date, nullable=False)
    parentesco = Column(String(50), nullable=False)

    funcionario = relationship("FuncionarioDB", back_populates="beneficiarios")

class FuncionarioDB(Base):
    __tablename__ = "funcionarios"
    
    id = Column(Integer, primary_key=True, index=True)
    cpf = Column(String(14), unique=True, index=True, nullable=False)
    nome = Column(String(100), nullable=False)
    data_nascimento = Column(Date, nullable=False)
    municipio_nascimento = Column(String(50), nullable=False)
    uf_nascimento = Column(String(2), nullable=False)
    nome_mae = Column(String(100), nullable=False)
    nome_pai = Column(String(100), nullable=False)
    nacionalidade = Column(String(50), nullable=False)
    estado_civil = Column(String(20), nullable=False)
    rg_numero = Column(String(20), nullable=False)
    rg_data_emissao = Column(Date, nullable=False)
    rg_orgao_emissor = Column(String(20), nullable=False)
    ctps_numero = Column(String(20), nullable=False)
    ctps_serie = Column(String(10), nullable=False)
    ctps_uf = Column(String(2), nullable=False)
    ctps_data_emissao = Column(Date, nullable=False)
    titulo_eleitor = Column(String(20), nullable=False)
    titulo_zona = Column(String(10), nullable=False)
    titulo_secao = Column(String(10), nullable=False)
    pis = Column(String(20), nullable=False)
    pis_data_cadastro = Column(Date, nullable=False)
    habilitacao = Column(String(20), nullable=True)
    habilitacao_categoria = Column(String(2), nullable=True)
    documento_militar = Column(String(20), nullable=True)
    cbo = Column(String(10), nullable=False)
    endereco = Column(String(200), nullable=False)
    endereco_numero = Column(String(10), nullable=False)
    endereco_complemento = Column(String(50), nullable=True)
    bairro = Column(String(50), nullable=False)
    municipio = Column(String(50), nullable=False)
    uf = Column(String(2), nullable=False)
    cep = Column(String(10), nullable=False)
    telefone = Column(String(20), nullable=False)
    email = Column(String(100), nullable=False)
    cargo = Column(String(100), nullable=False)
    funcao = Column(String(100), nullable=False)
    departamento = Column(String(100), nullable=False)
    data_admissao = Column(Date, nullable=False)
    data_demissao = Column(Date, nullable=True)
    salario = Column(Numeric(10, 2), nullable=False)
    tipo_pagamento = Column(String(20), nullable=False)
    horas_mensais = Column(Integer, nullable=False)
    tipo_contrato = Column(String(30), nullable=False)
    adicional_periculosidade = Column(Numeric(5, 2), default=0)
    adicional_insalubridade = Column(Numeric(5, 2), default=0)
    grau_instrucao = Column(String(50), nullable=False)
    fgts_data_opcao = Column(Date, nullable=False)
    fgts_banco = Column(String(50), default="Caixa Econômica Federal")
    criado_em = Column(TIMESTAMP, server_default=func.now())
    ativo = Column(Boolean, default=True)
    observacoes = Column(Text, nullable=True)

    beneficiarios = relationship("BeneficiarioDB", back_populates="funcionario", cascade="all, delete")

# ==============================
# MODELOS Pydantic
# ==============================

class BeneficiarioBase(BaseModel):
    nome: str
    data_nascimento: date
    parentesco: str

class FuncionarioBase(BaseModel):
    cpf: str = Field(..., pattern=r'^\d{3}\.\d{3}\.\d{3}-\d{2}$')
    nome: str = Field(..., max_length=100)
    data_nascimento: date
    municipio_nascimento: str
    uf_nascimento: str = Field(..., max_length=2)
    nome_mae: str
    nome_pai: str
    nacionalidade: str
    estado_civil: str
    rg_numero: str
    rg_data_emissao: date
    rg_orgao_emissor: str
    ctps_numero: str
    ctps_serie: str
    ctps_uf: str = Field(..., max_length=2)
    ctps_data_emissao: date
    titulo_eleitor: str
    titulo_zona: str
    titulo_secao: str
    pis: str
    pis_data_cadastro: date
    cargo: str
    funcao: str
    departamento: str
    data_admissao: date
    salario: float = Field(..., gt=0)
    tipo_pagamento: str
    horas_mensais: int = Field(..., gt=0, le=300)
    tipo_contrato: str
    adicional_periculosidade: float = Field(0, ge=0, le=100)
    adicional_insalubridade: float = Field(0, ge=0, le=100)
    grau_instrucao: str
    fgts_data_opcao: date
    fgts_banco: str = "Caixa Econômica Federal"
    beneficiarios: List[BeneficiarioBase] = []

    class Config:
        from_attributes = True

class FuncionarioCreate(FuncionarioBase):
    pass

class FuncionarioUpdate(BaseModel):
    cargo: Optional[str] = None
    funcao: Optional[str] = None
    departamento: Optional[str] = None
    salario: Optional[float] = None
    data_demissao: Optional[date] = None
    tipo_desligamento: Optional[str] = None
    observacoes: Optional[str] = None
    ativo: Optional[bool] = None

class FuncionarioResponse(FuncionarioBase):
    id: int
    criado_em: datetime
    ativo: bool

class UsuarioRH(BaseModel):
    email: EmailStr
    nome: str = Field(..., max_length=100)
    nivel_acesso: str = Field(default="user")

class UsuarioRHCreate(UsuarioRH):
    senha: str = Field(..., min_length=6)

class UsuarioRHLogin(BaseModel):
    email: EmailStr
    senha: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    nivel_acesso: Optional[str] = None
