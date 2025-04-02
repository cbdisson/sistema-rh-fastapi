from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os
from database import criar_tabelas, engine
from sqlalchemy import inspect

# 🔄 Gerenciamento do ciclo de vida do app (Startup & Shutdown)
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        os.makedirs("templates", exist_ok=True)  # Garante que a pasta exista
        criar_tabelas()  # Criando tabelas se não existirem
        print("✅ Banco de dados inicializado com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao inicializar o banco de dados: {e}")
    yield

# 🚀 Função para criar a aplicação FastAPI
def create_app() -> FastAPI:
    app = FastAPI(
        title="API de Gestão de RH",
        description="Sistema completo para administração de funcionários e recursos humanos.\n\n"
                    "📌 **Acesse `/docs` para explorar a API interativamente.**\n\n"
                    "📌 **Acesse `/redoc` para visualizar a documentação detalhada.**",
        version="1.0.0",
        lifespan=lifespan
    )

    # 🔥 Middleware CORS (permite acesso de outros domínios)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # ⚠️ Em produção, restrinja para domínios específicos!
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["Content-Disposition"]
    )

    # 🔗 Servindo arquivos estáticos se a pasta existir
    if os.path.exists("templates"):
        app.mount("/static", StaticFiles(directory="templates", html=True), name="static")

    # 🔄 Importação de rotas
    from routes_funcionarios import router as funcionarios_router
    from routes_rh import router as rh_router
    
    app.include_router(funcionarios_router, prefix="/api/v1", tags=["Funcionários"])
    app.include_router(rh_router, prefix="/api/v1", tags=["Recursos Humanos"])

    # 🏠 Rota principal
    @app.get("/", tags=["Root"])
    async def root():
        return {"message": "👋 Bem-vindo à API de Gestão de RH! Acesse `/docs` para mais informações."}

    # ✅ Health Check (para monitoramento)
    @app.get("/health", include_in_schema=False)
    async def health_check():
        return {"status": "healthy"}

    # 🔍 Verificação da estrutura da tabela funcionários (para debug)
    @app.get("/debug/check-funcionarios-structure", tags=["Debug"])
    async def check_structure():
        try:
            inspector = inspect(engine)
            tables = inspector.get_table_names()
            if "funcionarios" not in tables:
                return {"error": "❌ Tabela 'funcionarios' não encontrada no banco de dados."}

            columns = inspector.get_columns("funcionarios")
            return {
                "status": "✅ Estrutura da tabela 'funcionarios' verificada com sucesso!",
                "colunas": [{"nome": c["name"], "tipo": str(c["type"])} for c in columns]
            }
        except Exception as e:
            return {"error": f"Erro ao verificar estrutura da tabela: {e}"}

    return app

# 🚀 Inicializando o app
app = create_app()
