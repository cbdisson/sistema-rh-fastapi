// Estado global para controle de carregamento
let isLoading = false;

// Elementos do DOM
const elements = {
    tableBody: document.querySelector('#funcionariosTable tbody'),
    departamentoFilter: document.getElementById('departamentoFilter'),
    loadingIndicator: document.getElementById('loadingIndicator') || { style: {} },
    filterButton: document.getElementById('filterButton')
};

// Função para mostrar/ocultar loading
function showLoading(show) {
    if (elements.loadingIndicator) {
        elements.loadingIndicator.style.display = show ? 'inline-block' : 'none';
    }
    if (elements.filterButton) {
        elements.filterButton.disabled = show;
    }
}

// Função para mostrar erros
function showError(message) {
    elements.tableBody.innerHTML = `
        <tr>
            <td colspan="4" class="error-message">${message}</td>
        </tr>
    `;
}

// Função para renderizar funcionários na tabela
function renderizarFuncionarios(funcionarios) {
    if (!funcionarios || funcionarios.length === 0) {
        elements.tableBody.innerHTML = `
            <tr>
                <td colspan="4" class="no-data">Nenhum funcionário encontrado</td>
            </tr>
        `;
        return;
    }

    elements.tableBody.innerHTML = '';
    
    funcionarios.forEach(func => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${func.nome || '--'}</td>
            <td>${func.departamento || '--'}</td>
            <td>${func.cargo || '--'}</td>
            <td>
                <button onclick="editarFuncionario(${func.id})">Editar</button>
                <button class="btn-danger" onclick="desativarFuncionario(${func.id})">Desativar</button>
            </td>
        `;
        elements.tableBody.appendChild(row);
    });
}

// Listagem de Funcionários
async function carregarFuncionarios(departamento = '') {
    if (isLoading) return;
    
    try {
        isLoading = true;
        showLoading(true);
        
        const url = new URL(`${API_URL}/funcionarios`);
        if (departamento) url.searchParams.append('departamento', departamento);
        url.searchParams.append('ativo', 'true');
        url.searchParams.append('_', Date.now()); // Evitar cache

        const response = await fetch(url, {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });
        
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.message || 'Erro ao carregar funcionários');
        }
        
        const funcionarios = await response.json();
        renderizarFuncionarios(funcionarios);
        
    } catch (error) {
        console.error('Erro:', error);
        showError('Erro ao carregar funcionários. Tente novamente.');
    } finally {
        isLoading = false;
        showLoading(false);
    }
}

// Carregar departamentos para o filtro
async function carregarDepartamentos() {
    try {
        showLoading(true);
        
        const response = await fetch(`${API_URL}/departamentos`, {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });
        
        if (!response.ok) throw new Error('Erro ao carregar departamentos');
        
        const departamentos = await response.json();
        
        elements.departamentoFilter.innerHTML = '<option value="">Todos</option>';
        departamentos.forEach(depto => {
            const option = document.createElement("option");
            option.value = depto.nome;
            option.textContent = depto.nome;
            elements.departamentoFilter.appendChild(option);
        });
        
    } catch (error) {
        console.error("Erro ao carregar departamentos:", error);
        // Fallback para departamentos padrão se a API falhar
        elements.departamentoFilter.innerHTML = `
            <option value="">Todos</option>
            <option value="TI">TI</option>
            <option value="RH">RH</option>
            <option value="Financeiro">Financeiro</option>
            <option value="Vendas">Vendas</option>
        `;
    } finally {
        showLoading(false);
    }
}

// Filtro de funcionários
function filtrarFuncionarios() {
    const departamento = elements.departamentoFilter.value;
    carregarFuncionarios(departamento);
}

// Cadastro de Funcionário
if (document.getElementById('cadastroForm')) {
    document.getElementById('cadastroForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        try {
            const formData = new FormData(e.target);
            const funcionario = Object.fromEntries(formData.entries());
            
            // Converter tipos numéricos
            funcionario.salario = parseFloat(funcionario.salario);
            funcionario.horas_mensais = parseInt(funcionario.horas_mensais);
            funcionario.adicional_periculosidade = parseFloat(funcionario.adicional_periculosidade) || 0;
            funcionario.adicional_insalubridade = parseFloat(funcionario.adicional_insalubridade) || 0;
            
            const response = await fetch(`${API_URL}/funcionarios`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                },
                body: JSON.stringify(funcionario)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Erro ao cadastrar funcionário');
            }

            alert('Funcionário cadastrado com sucesso!');
            window.location.href = '../dashboard.html';
            
        } catch (error) {
            console.error('Erro detalhado:', error);
            alert(error.message || 'Erro ao cadastrar funcionário');
        }
    });
}

// Funções globais para edição e desativação
window.editarFuncionario = function(id) {
    window.location.href = `editar.html?id=${id}`;
}

window.desativarFuncionario = async function(id) {
    if (!confirm('Tem certeza que deseja desativar este funcionário?')) return;
    
    try {
        showLoading(true);
        
        const response = await fetch(`${API_URL}/funcionarios/${id}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });
        
        if (!response.ok) throw new Error('Erro ao desativar funcionário');
        
        await carregarFuncionarios();
        alert('Funcionário desativado com sucesso!');
        
    } catch (error) {
        console.error('Erro detalhado:', error);
        alert(error.message || 'Erro ao desativar funcionário');
    } finally {
        showLoading(false);
    }
}

// Inicialização
async function inicializarPagina() {
    try {
        showLoading(true);
        await carregarDepartamentos();
        await carregarFuncionarios();
    } catch (error) {
        console.error('Erro na inicialização:', error);
        showError('Erro ao carregar dados. Tente recarregar a página.');
    } finally {
        showLoading(false);
    }
}

// Configurar event listeners
if (window.location.pathname.includes('listar.html')) {
    document.addEventListener('DOMContentLoaded', inicializarPagina);
    
    // Adicionar event listener para o filtro
    if (elements.departamentoFilter && elements.filterButton) {
        elements.departamentoFilter.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') filtrarFuncionarios();
        });
    }
}