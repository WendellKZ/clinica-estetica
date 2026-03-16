/**
 * VENDA PREMIUM
 * - Ao selecionar produto cadastrado, busca preco/custo do backend e preenche os campos.
 * - Trava Preço/Custo quando produto selecionado (evita erro humano).
 * - Se "nenhum produto", libera campos e mantém modo manual.
 *
 * Endpoint usado: /loja/produtos/<id>/json/
 */
(function () {
  function $(sel) { return document.querySelector(sel); }

  function setReadonly(el, ro) {
    if (!el) return;
    el.readOnly = ro;
    el.style.background = ro ? "rgba(240,240,250,.6)" : "";
  }

  async function fillFromProduto(produtoId) {
    const resp = await fetch(`/loja/produtos/${produtoId}/json/`, {
      headers: { "X-Requested-With": "XMLHttpRequest" }
    });
    if (!resp.ok) throw new Error("Falha ao buscar produto");
    return await resp.json();
  }

  document.addEventListener("DOMContentLoaded", () => {
    const selProduto = $("#id_produto");
    const inpPreco = $("#id_preco_unitario");
    const inpCusto = $("#id_custo_unitario");
    const inpNome = $("#id_item_nome");

    if (!selProduto) return;

    async function apply() {
      const val = (selProduto.value || "").trim();
      if (!val) {
        // modo manual
        setReadonly(inpPreco, false);
        setReadonly(inpCusto, false);
        if (inpNome) inpNome.readOnly = false;
        return;
      }

      // modo produto cadastrado
      try {
        const p = await fillFromProduto(val);
        if (inpPreco) inpPreco.value = Number(p.preco_venda || 0).toFixed(2);
        if (inpCusto) inpCusto.value = Number(p.custo || 0).toFixed(2);

        setReadonly(inpPreco, true);
        setReadonly(inpCusto, true);

        // nome manual fica opcional (deixa livre, mas ajudamos o usuário)
        if (inpNome) {
          inpNome.value = "";
          inpNome.placeholder = `Produto selecionado: ${p.nome || ""}`;
        }
      } catch (e) {
        console.warn("Autofill produto falhou:", e);
      }
    }

    selProduto.addEventListener("change", apply);
    apply();
  });
})();
