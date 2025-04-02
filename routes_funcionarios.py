from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from sqlalchemy.orm import Session
from models import FuncionarioCreate, FuncionarioResponse, FuncionarioUpdate, FuncionarioDB
from database import get_db
from auth import get_usuario_atual
from database import UsuarioRH

router = APIRouter()

@router.get("/funcionarios", response_model=List[FuncionarioResponse])
def listar_funcionarios(
    db: Session = Depends(get_db),
    departamento: Optional[str] = None,
    ativo: Optional[bool] = True,
    current_user: UsuarioRH = Depends(get_usuario_atual)
):
    """Lista todos os funcionários com filtros opcionais"""
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
    """Busca um funcionário pelo ID"""
    funcionario = db.query(FuncionarioDB).filter(FuncionarioDB.id == id).first()
    if not funcionario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Funcionário não encontrado"
        )
    return funcionario

@router.post("/funcionarios", response_model=FuncionarioResponse, status_code=status.HTTP_201_CREATED)
def criar_funcionario(
    funcionario: FuncionarioCreate,
    db: Session = Depends(get_db),
    current_user: UsuarioRH = Depends(get_usuario_atual)
):
    """Cria um novo funcionário"""
    try:
        db_funcionario = FuncionarioDB(**funcionario.dict())
        db.add(db_funcionario)
        db.commit()
        db.refresh(db_funcionario)
        return db_funcionario
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao criar funcionário: {str(e)}"
        )

@router.put("/funcionarios/{id}", response_model=FuncionarioResponse)
def atualizar_funcionario(
    id: int,
    funcionario: FuncionarioUpdate,
    db: Session = Depends(get_db),
    current_user: UsuarioRH = Depends(get_usuario_atual)
):
    """Atualiza os dados de um funcionário"""
    try:
        db_funcionario = db.query(FuncionarioDB).filter(FuncionarioDB.id == id).first()
        if not db_funcionario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Funcionário não encontrado"
            )
        
        update_data = funcionario.dict(exclude_unset=True)
        
        # Atualiza apenas campos fornecidos
        for field, value in update_data.items():
            setattr(db_funcionario, field, value)
        
        db.add(db_funcionario)
        db.commit()
        db.refresh(db_funcionario)
        
        return db_funcionario
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao atualizar funcionário: {str(e)}"
        )

@router.delete("/funcionarios/{id}", status_code=status.HTTP_200_OK)
def deletar_funcionario(
    id: int,
    db: Session = Depends(get_db),
    current_user: UsuarioRH = Depends(get_usuario_atual)
):
    """Desativa um funcionário (deleção lógica)"""
    try:
        funcionario = db.query(FuncionarioDB).filter(FuncionarioDB.id == id).first()
        if not funcionario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Funcionário não encontrado"
            )
        
        funcionario.ativo = False
        db.add(funcionario)
        db.commit()
        
        return {"mensagem": "Funcionário desativado com sucesso"}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao desativar funcionário: {str(e)}"
        )

@router.get("/departamentos", response_model=List[str])
def listar_departamentos(
    db: Session = Depends(get_db),
    current_user: UsuarioRH = Depends(get_usuario_atual)
):
    """Lista todos os departamentos distintos"""
    departamentos = db.query(FuncionarioDB.departamento).distinct().all()
    return [d[0] for d in departamentos if d[0]]