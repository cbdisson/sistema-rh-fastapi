from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente do .env
load_dotenv()

# Criar URL do banco de dados com valores padrão para evitar erros
DATABASE_URL = f"postgresql://{os.getenv('POSTGRES_USER', 'user')}:{os.getenv('POSTGRES_PASSWORD', 'password')}" \
               f"@{os.getenv('POSTGRES_HOST', 'localhost')}:{os.getenv('POSTGRES_PORT', '5432')}/{os.getenv('POSTGRES_DB', 'database')}"

# Criar o motor do SQLAlchemy (com echo=True para depuração)
engine = create_engine(DATABASE_URL, echo=True)

# Criar sessão do banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Criar base declarativa
Base = declarative_base()

# Função para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        print(f"Erro na sessão do banco de dados: {e}")
        db.rollback()
        raise
    finally:
        db.close()

# Criar tabelas no banco de dados
def criar_tabelas():
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Tabelas criadas com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao criar tabelas: {e}")

# Modelo de Usuário RH
class UsuarioRH(Base):
    __tablename__ = "usuarios_rh"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True, nullable=False)
    nome = Column(String(100), nullable=False)
    senha_hash = Column(String(255), nullable=False)
    nivel_acesso = Column(String(20), default="user", nullable=False)
