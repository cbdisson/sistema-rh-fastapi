let isLoading = false;

const elements = {
    tableBody: document.querySelector('#funcionariosTable tbody'),
    departamentoFilter: document.getElementById('departamentoFilter'),
    loadingIndicator: document.getElementById('loadingIndicator') || { style: {} },
    filterButton: document.getElementById('filterButton')
};

function showLoading(show) {
    if (elements.loadingIndicator) elements.loadingIndicator.style.display = show ? 'inline-block' : 'none';
    if (elements.filterButton) elements.filterButton.disabled = show;
}

function showError(message) {
    elements.tableBody.innerHTML = `<tr><td colspan="4" class="error-message">${message}</td></tr>`;
}

function renderizarFuncionarios(funcionarios) {
    if (!funcionarios || funcionarios.length === 0) {
        elements.tableBody.innerHTML = `<tr><td colspan="4" class="no-data">Nenhum funcionário encontrado</td></tr>`;
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

async function carregarFuncionarios(departamento = '', status = '') {
    if (sessionStorage.getItem('shouldReload')) {
        sessionStorage.removeItem('shouldReload');
        departamento = '';
        status = '';
    }

    if (isLoading) return;
    try {
        isLoading = true;
        showLoading(true);
        const url = new URL(`${API_URL}/funcionarios`);
        if (departamento) url.searchParams.append('departamento', departamento);
        if (status !== '') url.searchParams.append('ativo', status === 'true');
        url.searchParams.append('_', Date.now());

        const response = await fetch(url, {
            headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
        });

        if (!response.ok) throw new Error('Erro ao carregar funcionários');
        renderizarFuncionarios(await response.json());
    } catch (error) {
        showError('Erro ao carregar funcionários. Tente novamente.');
    } finally {
        isLoading = false;
        showLoading(false);
    }
}

async function carregarDepartamentos() {
    const token = localStorage.getItem("token");
    try {
        const response = await fetch(`${API_URL}/departamentos`, {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        if (!response.ok) {
            throw new Error("Erro ao carregar departamentos");
        }

        const departamentos = await response.json();
        const select = document.getElementById("departamentoFilter");

        departamentos.forEach(dep => {
            const option = document.createElement("option");
            option.value = dep;
            option.textContent = dep;
            select.appendChild(option);
        });
    } catch (error) {
        console.error("Erro ao carregar departamentos:", error);
    }
}

function editarFuncionario(id) {
    window.location.href = `../funcionarios/editar.html?id=${id}`;
}

window.editarFuncionario = function(id) {
    window.location.href = `editar.html?id=${id}`;
}

window.desativarFuncionario = async function(id) {
    if (!confirm('Tem certeza que deseja desativar este funcionário?')) return;
    try {
        showLoading(true);
        const response = await fetch(`${API_URL}/funcionarios/${id}`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
        });
        if (!response.ok) throw new Error('Erro ao desativar funcionário');
        sessionStorage.setItem('shouldReload', 'true');
        await carregarFuncionarios();
        alert('Funcionário desativado com sucesso!');
    } catch (error) {
        alert(error.message || 'Erro ao desativar funcionário');
    } finally {
        showLoading(false);
    }
}

function filtrarFuncionarios() {
    const departamento = elements.departamentoFilter.value;
    const status = document.getElementById("ativoFilter").value;
    carregarFuncionarios(departamento, status);
}

if (document.getElementById('cadastroForm')) {
    document.getElementById('cadastroForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        try {
            const formData = new FormData(e.target);
            const funcionario = Object.fromEntries(formData.entries());
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

            if (!response.ok) throw new Error('Erro ao cadastrar funcionário');
            alert('Funcionário cadastrado com sucesso!');
            window.location.href = '../dashboard.html';
        } catch (error) {
            alert(error.message || 'Erro ao cadastrar funcionário');
        }
    });
}

async function inicializarPagina() {
    try {
        showLoading(true);
        await carregarDepartamentos();
        await carregarFuncionarios();
    } catch (error) {
        showError('Erro ao carregar dados. Tente recarregar a página.');
    } finally {
        showLoading(false);
    }
}

// Ao carregar a página
window.onload = () => {
    inicializarPagina();
    if (elements.departamentoFilter && elements.filterButton) {
        elements.departamentoFilter.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') filtrarFuncionarios();
        });
    }
}
