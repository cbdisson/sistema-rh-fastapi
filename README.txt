Sistema RH - FastAPI





Um sistema de gerenciamento de funcionários desenvolvido com FastAPI e SQLite, proporcionando um backend rápido e eficiente para controle de registros de funcionários.

📌 Funcionalidades

📋 Cadastro, edição e remoção de funcionários.

🔍 Listagem e busca de funcionários.

🔑 Autenticação de usuários.

📊 Dashboard para visualização de dados.

🚀 Tecnologias Utilizadas

Backend: Python (FastAPI)

Banco de Dados: SQLite

Frontend: HTML, CSS, JavaScript

Migrações: Alembic (opcional)

🛠 Instalação e Configuração

1️⃣ Clonar o repositório

 git clone https://github.com/cbdisson/sistema-rh-fastapi.git
 cd sistema-rh-fastapi

2️⃣ Criar e ativar um ambiente virtual (recomendado)

python -m venv venv  # Criar ambiente virtual
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate  # Windows

3️⃣ Instalar dependências

pip install -r requirements.txt

4️⃣ Configurar variáveis de ambiente

Crie um arquivo .env na raiz do projeto e configure as credenciais necessárias:

DATABASE_URL=sqlite:///./database.db
SECRET_KEY=sua_chave_secreta_aqui

5️⃣ Rodar a aplicação

uvicorn main:app --reload

A API estará disponível em: http://127.0.0.1:8000

📂 Estrutura do Projeto

📁 sistema-rh-fastapi/
│-- 📂 templates/        # Arquivos HTML e CSS
│-- 📂 static/js/        # Scripts JavaScript
│-- 📂 alembic/          # Migrações do banco de dados
│-- 📄 main.py           # Ponto de entrada do FastAPI
│-- 📄 models.py         # Definição dos modelos de dados
│-- 📄 routes.py         # Rotas da API
│-- 📄 requirements.txt  # Dependências do projeto
│-- 📄 .env              # Configurações sensíveis (não versionado)

📌 Endpoints Principais

Método

Rota

Descrição

GET

/funcionarios/

Lista todos os funcionários

POST

/funcionarios/

Adiciona um novo funcionário

GET

/funcionarios/{id}

Obtém detalhes de um funcionário

PUT

/funcionarios/{id}

Atualiza informações de um funcionário

DELETE

/funcionarios/{id}

Remove um funcionário

📜 Licença

Este projeto é open-source e está disponível sob a licença MIT.