from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from auth import get_usuario_atual
from models import FuncionarioCreate, FuncionarioResponse, FuncionarioUpdate
from database import get_db
import sqlite3
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/funcionarios", response_model=List[FuncionarioResponse])
def listar_funcionarios(
    usuario_atual: dict = Depends(get_usuario_atual),
    departamento: Optional[str] = None
):
    """Lista todos os funcionários, com filtro opcional por departamento"""
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        if departamento:
            cursor.execute("SELECT * FROM funcionarios WHERE departamento = ?", (departamento,))
        else:
            cursor.execute("SELECT * FROM funcionarios")
            
        return [dict(row) for row in cursor.fetchall()]
    except Exception as e:
        logger.error(f"Erro ao listar funcionários: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao recuperar funcionários"
        )
    finally:
        if conn:
            conn.close()

@router.get("/funcionarios/{id}", response_model=FuncionarioResponse)
def buscar_funcionario(
    id: int, 
    usuario_atual: dict = Depends(get_usuario_atual)
):
    """Busca um funcionário específico pelo ID"""
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM funcionarios WHERE id = ?", (id,))
        funcionario = cursor.fetchone()
        
        if not funcionario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Funcionário não encontrado"
            )
            
        return dict(funcionario)
    except Exception as e:
        logger.error(f"Erro ao buscar funcionário: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao buscar funcionário"
        )
    finally:
        if conn:
            conn.close()

@router.post("/funcionarios", response_model=FuncionarioResponse, status_code=status.HTTP_201_CREATED)
def criar_funcionario(
    funcionario: FuncionarioCreate,
    usuario_atual: dict = Depends(get_usuario_atual)
):
    """Cria um novo funcionário"""
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute(
            """INSERT INTO funcionarios 
            (cpf, nome, data_nascimento, cargo, salario, departamento) 
            VALUES (?, ?, ?, ?, ?, ?)""",
            (
                funcionario.cpf,
                funcionario.nome,
                funcionario.data_nascimento.isoformat() if funcionario.data_nascimento else None,
                funcionario.cargo,
                funcionario.salario,
                funcionario.departamento
            )
        )
        conn.commit()
        
        cursor.execute("SELECT * FROM funcionarios WHERE id = last_insert_rowid()")
        return dict(cursor.fetchone())
        
    except sqlite3.IntegrityError as e:
        logger.error(f"Erro de integridade: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="CPF já cadastrado no sistema"
        )
    except Exception as e:
        logger.error(f"Erro inesperado: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao processar o cadastro"
        )
    finally:
        if conn:
            conn.close()

@router.put("/funcionarios/{id}", response_model=FuncionarioResponse)
def atualizar_funcionario(
    id: int,
    funcionario: FuncionarioUpdate,
    usuario_atual: dict = Depends(get_usuario_atual)
):
    """Atualiza os dados de um funcionário"""
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Verifica se o funcionário existe
        cursor.execute("SELECT id FROM funcionarios WHERE id = ?", (id,))
        if not cursor.fetchone():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Funcionário não encontrado"
            )
        
        # Atualiza os campos fornecidos
        campos_para_atualizar = []
        valores = []
        
        if funcionario.nome:
            campos_para_atualizar.append("nome = ?")
            valores.append(funcionario.nome)
        if funcionario.cargo:
            campos_para_atualizar.append("cargo = ?")
            valores.append(funcionario.cargo)
        if funcionario.salario:
            campos_para_atualizar.append("salario = ?")
            valores.append(funcionario.salario)
        if funcionario.departamento:
            campos_para_atualizar.append("departamento = ?")
            valores.append(funcionario.departamento)
        
        if not campos_para_atualizar:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Nenhum dado fornecido para atualização"
            )
        
        valores.append(id)
        query = f"UPDATE funcionarios SET {', '.join(campos_para_atualizar)} WHERE id = ?"
        cursor.execute(query, valores)
        conn.commit()
        
        cursor.execute("SELECT * FROM funcionarios WHERE id = ?", (id,))
        return dict(cursor.fetchone())
        
    except Exception as e:
        logger.error(f"Erro ao atualizar funcionário: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao atualizar funcionário"
        )
    finally:
        if conn:
            conn.close()

@router.delete("/funcionarios/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_funcionario(
    id: int,
    usuario_atual: dict = Depends(get_usuario_atual)
):
    """Remove um funcionário do sistema"""
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM funcionarios WHERE id = ?", (id,))
        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Funcionário não encontrado"
            )
            
        conn.commit()
        return None
    except Exception as e:
        logger.error(f"Erro ao deletar funcionário: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao remover funcionário"
        )
    finally:
        if conn:
            conn.close()