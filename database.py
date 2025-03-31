import sqlite3
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_db():
    conn = sqlite3.connect('funcionarios.db')
    conn.row_factory = sqlite3.Row  # Retorna linhas como dicionários
    return conn

def criar_tabelas():
    conn = get_db()
    try:
        # Tabela de Funcionários
        conn.execute('''
        CREATE TABLE IF NOT EXISTS funcionarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cpf TEXT UNIQUE NOT NULL,
            nome TEXT NOT NULL,
            data_nascimento TEXT,
            cargo TEXT,
            salario REAL,
            departamento TEXT,
            criado_em TEXT DEFAULT CURRENT_TIMESTAMP
        )
        ''')

        # Tabela de Usuários do RH
        conn.execute('''
        CREATE TABLE IF NOT EXISTS usuarios_rh (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            nome TEXT NOT NULL,
            senha_hash TEXT NOT NULL,
            nivel_acesso TEXT NOT NULL,
            criado_em TEXT DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        conn.commit()
        logger.info("Tabelas criadas com sucesso!")
    except Exception as e:
        logger.error(f"Erro ao criar tabelas: {e}")
        raise
    finally:
        conn.close()