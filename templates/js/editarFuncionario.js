window.API_URL = window.API_URL || "http://localhost:8000/api/v1";

document.addEventListener("DOMContentLoaded", async () => {
  if (!localStorage.getItem("token")) {
    window.location.href = "../index.html";
    return;
  }

  const urlParams = new URLSearchParams(window.location.search);
  const id = urlParams.get("id");
  if (!id) {
    alert("ID do funcionário não especificado");
    window.location.href = "../funcionarios/listar.html";
    return;
  }

  const form = document.getElementById("editarForm");
  const btnDesativar = document.getElementById("btnDesativar");
  const idField = document.getElementById("funcionario_id");

  // Criação dos campos de beneficiários (sem data de nascimento)
  function createBeneficiarioFields(beneficiario = {}) {
    const container = document.createElement("div");
    container.className = "form-row beneficiario-row";
    container.style.marginBottom = "10px";

    container.innerHTML = `
      <input type="text" class="beneficiario-nome" placeholder="Nome" value="${
        beneficiario.nome || ""
      }" />
      <input type="text" class="beneficiario-parentesco" placeholder="Parentesco" value="${
        beneficiario.parentesco || ""
      }" style="margin-left: 10px;" />
      <button type="button" class="btn-remove-beneficiario" style="margin-left: 10px;">Remover</button>
    `;

    container
      .querySelector(".btn-remove-beneficiario")
      .addEventListener("click", () => {
        container.remove();
      });

    document.getElementById("beneficiariosContainer").appendChild(container);
  }

  document
    .getElementById("btnAddBeneficiario")
    .addEventListener("click", () => {
      createBeneficiarioFields();
    });

  try {
    const response = await fetch(`${API_URL}/funcionarios/${id}`, {
      headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
    });

    if (!response.ok) throw new Error("Erro ao carregar dados do funcionário");

    const funcionario = await response.json();

    const setValue = (id, val) => {
      const el = document.getElementById(id);
      if (el) {
        if (el.type === "date" && val) {
          el.value = val.split("T")[0];
        } else {
          el.value = val ?? "";
        }
      }
    };

    idField.value = id;
    setValue("nome", funcionario.nome);
    setValue("data_nascimento", funcionario.data_nascimento);
    setValue("cpf", funcionario.cpf);
    setValue("rg_numero", funcionario.rg_numero);
    setValue("nome_mae", funcionario.nome_mae);
    setValue("nome_pai", funcionario.nome_pai);
    setValue("municipio_nascimento", funcionario.municipio_nascimento);
    setValue("uf_nascimento", funcionario.uf_nascimento);
    setValue("nacionalidade", funcionario.nacionalidade);
    setValue("estado_civil", funcionario.estado_civil);
    setValue("rg_data_emissao", funcionario.rg_data_emissao);
    setValue("rg_orgao_emissor", funcionario.rg_orgao_emissor);
    setValue("ctps_numero", funcionario.ctps_numero);
    setValue("ctps_serie", funcionario.ctps_serie);
    setValue("ctps_uf", funcionario.ctps_uf);
    setValue("ctps_data_emissao", funcionario.ctps_data_emissao);
    setValue("titulo_eleitor", funcionario.titulo_eleitor);
    setValue("titulo_zona", funcionario.titulo_zona);
    setValue("titulo_secao", funcionario.titulo_secao);
    setValue("pis", funcionario.pis);
    setValue("pis_data_cadastro", funcionario.pis_data_cadastro);
    setValue("cargo", funcionario.cargo);
    setValue("funcao", funcionario.funcao);
    setValue("departamento", funcionario.departamento);
    setValue("data_admissao", funcionario.data_admissao);
    setValue("data_demissao", funcionario.data_demissao);
    setValue("tipo_desligamento", funcionario.tipo_desligamento);
    setValue("tipo_pagamento", funcionario.tipo_pagamento);
    setValue("salario", funcionario.salario);
    setValue("horas_mensais", funcionario.horas_mensais);
    setValue("tipo_contrato", funcionario.tipo_contrato);
    setValue("adicional_periculosidade", funcionario.adicional_periculosidade);
    setValue("adicional_insalubridade", funcionario.adicional_insalubridade);
    setValue("grau_instrucao", funcionario.grau_instrucao);
    setValue("fgts_data_opcao", funcionario.fgts_data_opcao);
    setValue("fgts_banco", funcionario.fgts_banco);
    setValue("observacoes", funcionario.observacoes);

    const ativoEl = document.getElementById("ativo");
    if (ativoEl) ativoEl.value = funcionario.ativo ? "true" : "false";

    if (Array.isArray(funcionario.beneficiarios)) {
      funcionario.beneficiarios.forEach((b) => {
        const { nome, parentesco } = b;
        createBeneficiarioFields({ nome, parentesco });
      });
    }

    // Atualização
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      try {
        const getVal = (id, type = "text") => {
          const el = document.getElementById(id);
          if (!el) return null;
          if (type === "number") return el.value ? parseFloat(el.value) : null;
          if (type === "int") return el.value ? parseInt(el.value) : null;
          if (type === "bool") return el.value === "true";
          return el.value || null;
        };

        const beneficiarios = [];
        document.querySelectorAll(".beneficiario-row").forEach((row, index) => {
          const nome = row.querySelector(".beneficiario-nome")?.value.trim();
          const parentesco = row
            .querySelector(".beneficiario-parentesco")
            ?.value.trim();

          if (!nome && !parentesco) return;

          if (!nome || !parentesco) {
            alert(
              `Preencha nome e parentesco do beneficiário ${
                index + 1
              } ou deixe todos em branco.`
            );
            throw new Error("Beneficiário com campos incompletos");
          }

          beneficiarios.push({
            nome,
            parentesco,
            data_nascimento: null,
          });
        });

        const formData = {
          nome: getVal("nome"),
          data_nascimento: getVal("data_nascimento"),
          cpf: getVal("cpf"),
          rg_numero: getVal("rg_numero"),
          nome_mae: getVal("nome_mae"),
          nome_pai: getVal("nome_pai"),
          municipio_nascimento: getVal("municipio_nascimento"),
          uf_nascimento: getVal("uf_nascimento"),
          nacionalidade: getVal("nacionalidade"),
          estado_civil: getVal("estado_civil"),
          rg_data_emissao: getVal("rg_data_emissao"),
          rg_orgao_emissor: getVal("rg_orgao_emissor"),
          ctps_numero: getVal("ctps_numero"),
          ctps_serie: getVal("ctps_serie"),
          ctps_uf: getVal("ctps_uf"),
          ctps_data_emissao: getVal("ctps_data_emissao"),
          titulo_eleitor: getVal("titulo_eleitor"),
          titulo_zona: getVal("titulo_zona"),
          titulo_secao: getVal("titulo_secao"),
          pis: getVal("pis"),
          pis_data_cadastro: getVal("pis_data_cadastro"),
          cargo: getVal("cargo"),
          funcao: getVal("funcao"),
          departamento: getVal("departamento"),
          data_admissao: getVal("data_admissao"),
          data_demissao: getVal("data_demissao"),
          tipo_desligamento: getVal("tipo_desligamento"),
          tipo_pagamento: getVal("tipo_pagamento"),
          salario: getVal("salario", "number"),
          horas_mensais: getVal("horas_mensais", "int"),
          tipo_contrato: getVal("tipo_contrato"),
          adicional_periculosidade: getVal(
            "adicional_periculosidade",
            "number"
          ),
          adicional_insalubridade: getVal("adicional_insalubridade", "number"),
          grau_instrucao: getVal("grau_instrucao"),
          fgts_data_opcao: getVal("fgts_data_opcao"),
          fgts_banco: getVal("fgts_banco"),
          observacoes: getVal("observacoes"),
          ativo: getVal("ativo", "bool"),
          beneficiarios: beneficiarios,
        };

        const updateResponse = await fetch(`${API_URL}/funcionarios/${id}`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
          body: JSON.stringify(formData),
        });

        if (!updateResponse.ok) {
          const errorData = await updateResponse.json().catch(() => ({}));
          console.error("Erro detalhado:", errorData);
          throw new Error(JSON.stringify(errorData));
        }

        alert("Alterações salvas com sucesso!");
        sessionStorage.setItem("shouldReload", "true");
        window.location.href = "../funcionarios/listar.html";
      } catch (error) {
        console.error("Erro:", error);
        alert(error.message);
      }
    });

    // Desativação
    btnDesativar.addEventListener("click", async () => {
      if (!confirm("Tem certeza que deseja desativar este funcionário?"))
        return;
      try {
        const deleteResponse = await fetch(`${API_URL}/funcionarios/${id}`, {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        });

        if (!deleteResponse.ok)
          throw new Error("Erro ao desativar funcionário");

        alert("Funcionário desativado com sucesso!");
        sessionStorage.setItem("shouldReload", "true");
        window.location.href = "../funcionarios/listar.html";
      } catch (error) {
        console.error("Erro:", error);
        alert(error.message);
      }
    });
  } catch (error) {
    console.error("Erro:", error);
    alert("Não foi possível carregar os dados do funcionário");
    window.location.href = "../funcionarios/listar.html";
  }
});
