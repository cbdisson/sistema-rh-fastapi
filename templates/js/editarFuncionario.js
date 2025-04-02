document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("editarForm");
    const funcionarioId = new URLSearchParams(window.location.search).get("id");

    if (funcionarioId) {
        fetch(`http://127.0.0.1:8000/api/funcionarios/${funcionarioId}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error("Funcionário não encontrado");
                }
                return response.json();
            })
            .then(data => preencherFormulario(data))
            .catch(error => {
                console.error("Erro ao carregar funcionário:", error);
                alert("Erro ao carregar os dados do funcionário.");
            });
    }

    function formatarData(data) {
        if (!data) return "";
        return data.split("T")[0];
    }

    function preencherFormulario(funcionario) {
        document.getElementById("funcionario_id").value = funcionario.id;
        document.getElementById("nome").value = funcionario.nome || "";
        document.getElementById("data_nascimento").value = formatarData(funcionario.data_nascimento);
        document.getElementById("cpf").value = funcionario.cpf || "";
        document.getElementById("rg_numero").value = funcionario.rg_numero || "";
        document.getElementById("nome_mae").value = funcionario.nome_mae || "";
        document.getElementById("nome_pai").value = funcionario.nome_pai || "";
        document.getElementById("cargo").value = funcionario.cargo || "";
        document.getElementById("departamento").value = funcionario.departamento || "";
        document.getElementById("data_admissao").value = formatarData(funcionario.data_admissao);
        document.getElementById("salario").value = funcionario.salario || 0;
        document.getElementById("ativo").value = funcionario.ativo ? "true" : "false";
    }

    form.addEventListener("submit", function (event) {
        event.preventDefault();

        const funcionarioAtualizado = {
            id: funcionarioId,
            nome: document.getElementById("nome").value,
            data_nascimento: document.getElementById("data_nascimento").value,
            cpf: document.getElementById("cpf").value,
            rg_numero: document.getElementById("rg_numero").value,
            nome_mae: document.getElementById("nome_mae").value,
            nome_pai: document.getElementById("nome_pai").value,
            cargo: document.getElementById("cargo").value,
            departamento: document.getElementById("departamento").value,
            data_admissao: document.getElementById("data_admissao").value,
            salario: parseFloat(document.getElementById("salario").value),
            ativo: document.getElementById("ativo").value === "true"
        };

        fetch(`http://127.0.0.1:8000/api/funcionarios/${funcionarioId}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(funcionarioAtualizado)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error("Erro ao atualizar funcionário");
            }
            return response.json();
        })
        .then(() => {
            alert("Funcionário atualizado com sucesso!");
            window.location.href = "listar.html";
        })
        .catch(error => {
            console.error("Erro:", error);
            alert("Erro ao atualizar funcionário.");
        });
    });

    document.getElementById("btnDesativar").addEventListener("click", function () {
        if (confirm("Tem certeza que deseja desativar este funcionário?")) {
            fetch(`http://127.0.0.1:8000/api/funcionarios/${funcionarioId}`, {
                method: "PATCH", // Altere para PATCH se apenas desativar
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ ativo: false })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error("Erro ao desativar funcionário");
                }
                return response.json();
            })
            .then(() => {
                alert("Funcionário desativado com sucesso!");
                window.location.href = "listar.html";
            })
            .catch(error => {
                console.error("Erro:", error);
                alert("Erro ao desativar funcionário.");
            });
        }
    });
});