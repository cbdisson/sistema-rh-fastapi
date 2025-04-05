from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from sqlalchemy.orm import Session
from models import FuncionarioCreate, FuncionarioResponse, FuncionarioUpdate, FuncionarioDB
from database import get_db
from auth import get_usuario_atual
from database import UsuarioRH
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/funcionarios", response_model=List[FuncionarioResponse])
def listar_funcionarios(
    db: Session = Depends(get_db),
    departamento: Optional[str] = None,
    ativo: Optional[bool] = Query(True, description="Filtrar funcionários ativos ou inativos"),
    current_user: UsuarioRH = Depends(get_usuario_atual)
):
    query = db.query(FuncionarioDB)
    if departamento:
        query = query.filter(FuncionarioDB.departamento == departamento)
    if ativo is not None:
        query = query.filter(FuncionarioDB.ativo == ativo)
    return query.all()

@router.get("/funcionarios/{id}", response_model=FuncionarioResponse)
def buscar_funcionario(
    id: int,
    db: Session = Depends(get_db),
    current_user: UsuarioRH = Depends(get_usuario_atual)
):
    funcionario = db.query(FuncionarioDB).get(id)
    if not funcionario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Funcionário não encontrado")
    return funcionario

@router.post("/funcionarios", response_model=FuncionarioResponse, status_code=status.HTTP_201_CREATED)
def criar_funcionario(
    funcionario: FuncionarioCreate,
    db: Session = Depends(get_db),
    current_user: UsuarioRH = Depends(get_usuario_atual)
):
    try:
        db_funcionario = FuncionarioDB(**funcionario.dict())
        db.add(db_funcionario)
        db.commit()
        db.refresh(db_funcionario)
        return db_funcionario
    except Exception as e:
        db.rollback()
        logger.error(f"Erro ao criar funcionário: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Erro ao criar funcionário")

@router.put("/funcionarios/{id}", response_model=FuncionarioResponse)
def atualizar_funcionario(
    id: int,
    funcionario: FuncionarioUpdate,
    db: Session = Depends(get_db),
    current_user: UsuarioRH = Depends(get_usuario_atual)
):
    try:
        db_funcionario = db.query(FuncionarioDB).filter(FuncionarioDB.id == id).with_for_update().one()
        
        update_data = funcionario.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_funcionario, key, value)
        
        db.commit()
        db.refresh(db_funcionario)
        return db_funcionario
    except Exception as e:
        db.rollback()
        logger.error(f"Erro ao atualizar funcionário {id}: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Erro ao atualizar funcionário")

@router.delete("/funcionarios/{id}", status_code=status.HTTP_200_OK)
def deletar_funcionario(
    id: int,
    db: Session = Depends(get_db),
    current_user: UsuarioRH = Depends(get_usuario_atual)
):
    try:
        funcionario = db.query(FuncionarioDB).get(id)
        if not funcionario:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Funcionário não encontrado")
        
        funcionario.ativo = False
        db.commit()
        return {"mensagem": "Funcionário desativado com sucesso"}
    except Exception as e:
        db.rollback()
        logger.error(f"Erro ao desativar funcionário {id}: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Erro ao desativar funcionário")

@router.get("/departamentos", response_model=List[str])
def listar_departamentos(
    db: Session = Depends(get_db),
    current_user: UsuarioRH = Depends(get_usuario_atual)
):
    return [d[0] for d in db.query(FuncionarioDB.departamento).distinct().all() if d[0]]