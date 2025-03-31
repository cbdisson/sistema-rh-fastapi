from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import criar_tabelas

def create_app():
    app = FastAPI(
        title="API de Gestão de RH",
        description="Sistema para administração de funcionários e usuários do RH",
        version="1.0.0"
    )

    # Configuração CORS (Adicione este bloco)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Em produção, substitua por seus domínios
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Importações de rotas dentro da função para evitar circular imports
    from routes_funcionarios import router as funcionarios_router
    from routes_rh import router as rh_router

    # Registra as rotas
    app.include_router(funcionarios_router, prefix="/api/v1")
    app.include_router(rh_router, prefix="/api/v1")

    return app

app = create_app()

@app.on_event("startup")
async def startup():
    criar_tabelas()
    print("✅ Tabelas verificadas/criadas com sucesso!")