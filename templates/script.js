let token = null;
let currentUser = null;

// Funções de Autenticação
async function login() {
    const email = document.getElementById('login-email').value;
    const senha = document.getElementById('login-senha').value;

    try {
        const response = await fetch('http://localhost:8000/api/v1/rh/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email: email,
                senha: senha
            })
        });

        const data = await response.json();
        
        if (response.ok) {
            token = data.access_token;
            currentUser = { email: email };
            
            document.getElementById('login-form').style.display = 'none';
            document.getElementById('user-info').style.display = 'block';
            document.getElementById('user-name').textContent = email;
            document.getElementById('funcionarios-section').style.display = 'block';
            
            listarFuncionarios();
        } else {
            alert('Login falhou: ' + (data.detail || 'Credenciais inválidas'));
        }
    } catch (error) {
        console.error('Erro ao fazer login:', error);
        alert('Erro ao conectar com o servidor');
    }
}

function logout() {
    token = null;
    currentUser = null;
    document.getElementById('login-form').style.display = 'block';
    document.getElementById('user-info').style.display = 'none';
    document.getElementById('funcionarios-section').style.display = 'none';
    document.getElementById('funcionarios-list').innerHTML = '';
}

// Funções de Funcionários
document.getElementById('form-funcionario').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const funcionario = {
        cpf: document.getElementById('cpf').value,
        nome: document.getElementById('nome').value,
        data_nascimento: document.getElementById('data-nascimento').value || null,
        cargo: document.getElementById('cargo').value,
        salario: parseFloat(document.getElementById('salario').value),
        departamento: document.getElementById('departamento').value
    };

    try {
        const response = await fetch('http://localhost:8000/api/v1/funcionarios', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(funcionario)
        });

        if (response.ok) {
            alert('Funcionário cadastrado com sucesso!');
            document.getElementById('form-funcionario').reset();
            listarFuncionarios();
        } else {
            const error = await response.json();
            alert('Erro: ' + (error.detail || 'Falha ao cadastrar'));
        }
    } catch (error) {
        console.error('Erro:', error);
        alert('Erro ao conectar com o servidor');
    }
});

async function listarFuncionarios() {
    const departamento = document.getElementById('filter-departamento').value;
    let url = 'http://localhost:8000/api/v1/funcionarios';
    
    if (departamento) {
        url += `?departamento=${encodeURIComponent(departamento)}`;
    }

    try {
        const response = await fetch(url, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (response.ok) {
            const funcionarios = await response.json();
            renderizarFuncionarios(funcionarios);
        } else {
            const error = await response.json();
            alert('Erro: ' + (error.detail || 'Falha ao listar'));
        }
    } catch (error) {
        console.error('Erro:', error);
        alert('Erro ao conectar com o servidor');
    }
}

function renderizarFuncionarios(funcionarios) {
    const container = document.getElementById('funcionarios-list');
    container.innerHTML = '';

    funcionarios.forEach(func => {
        const card = document.createElement('div');
        card.className = 'funcionario-card';
        card.innerHTML = `
            <h3>${func.nome}</h3>
            <p><strong>CPF:</strong> ${func.cpf}</p>
            <p><strong>Cargo:</strong> ${func.cargo}</p>
            <p><strong>Salário:</strong> R$ ${func.salario.toFixed(2)}</p>
            <p><strong>Departamento:</strong> ${func.departamento}</p>
            <div class="funcionario-actions">
                <button class="edit-btn" onclick="editarFuncionario(${func.id})">Editar</button>
                <button class="delete-btn" onclick="deletarFuncionario(${func.id})">Excluir</button>
            </div>
        `;
        container.appendChild(card);
    });
}

async function deletarFuncionario(id) {
    if (!confirm('Tem certeza que deseja excluir este funcionário?')) return;

    try {
        const response = await fetch(`http://localhost:8000/api/v1/funcionarios/${id}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (response.ok) {
            alert('Funcionário excluído com sucesso!');
            listarFuncionarios();
        } else {
            const error = await response.json();
            alert('Erro: ' + (error.detail || 'Falha ao excluir'));
        }
    } catch (error) {
        console.error('Erro:', error);
        alert('Erro ao conectar com o servidor');
    }
}

async function editarFuncionario(id) {
    // Implementação básica - poderia abrir um modal com o formulário preenchido
    const novoSalario = prompt("Digite o novo salário:");
    if (novoSalario && !isNaN(novoSalario)) {
        try {
            const response = await fetch(`http://localhost:8000/api/v1/funcionarios/${id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    salario: parseFloat(novoSalario)
                })
            });

            if (response.ok) {
                alert('Funcionário atualizado com sucesso!');
                listarFuncionarios();
            } else {
                const error = await response.json();
                alert('Erro: ' + (error.detail || 'Falha ao atualizar'));
            }
        } catch (error) {
            console.error('Erro:', error);
            alert('Erro ao conectar com o servidor');
        }
    }
}