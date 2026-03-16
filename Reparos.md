# Documento de Reparos - Clínica Estética

Durante a revisão de código, foram encontrados os seguintes bugs e inconsistências arquiteturais focados no Clean Code e na estabilidade do framework Django. Abaixo estão listadas as ações necessárias para suas respectivas correções.

## Lista de Problemas Encontrados

### 1. [CORRIGIDO] Falta de CSRF Token no formulário de Login (`core/views.py`)
- **Problema:** A visualização de fallback da view `login_view` (usada caso o template não exista) retorna um HTML hardcoded sem o campo input necessário para o CSRF Token. Quando submetido, o Django recusa a requisição com **HTTP 403 Forbidden**.
- **Ação Necessária:** O ideal é garantir que o arquivo de template exista, mas, como medida de robustez, o HTML da view deve incluir o token csrf via context processor manualmente ou ser transformado em um `Template().render(Context(...))` que suporte o token.

### 2. [CORRIGIDO] Sobrescrita da `class Meta` em Modelo (`produtos/models.py`)
- **Problema:** A classe `LegacyProduto` tem dois escopos `class Meta:` declarados seguidos. Em Python, a segunda declaração sobrescreve a primeira. O resultado é que a regra `app_label = 'produtos'` da primeira declaração é totalmente ignorada.
- **Ação Necessária:** Unificar os dois blocos `Meta` em um único bloco.

### 3. [CORRIGIDO] Falha Crítica de Transação no Controle de Estoque (`loja/views.py`)
- **Problema:** A função `venda_finalizar` possui o decorador `@transaction.atomic`. No loop que verifica o estoque (`if p.estoque_atual < item.quantidade:`), se falta estoque ela interrompe o decorrer chamando um `redirect()`. Contudo, como não há Exception sendo levantada e o HTTP flow segue normal, o Django **comita a transação**. Os produtos iterados *antes* da falha no mesmo loop terão seus estoques subtraídos parcialmente da base de dados sem gerar uma Venda concluída.
- **Ação Necessária:** A verificação de estoque (`p.estoque_atual < item.quantidade`) deve ser feita integralmente para todos os produtos em um _loop de validação_ inicial, antes de qualquer alteração nos registros de banco de dados e execução do `p.save()`.

### 4. [CORRIGIDO] Propriedade de Preço Incorreta na API (`loja/views.py`)
- **Problema:** A função `produto_json` (linha 163) tenta ler o preço através de `getattr(obj, 'preco', None)`. Ocorre que o modelo `Produto` importado de loja (e o proxy `ProdutoCatalogo`) guardam o preço de venda no campo `preco_venda`, resultando em um preenchimento em branco ou falho (None ou 0) na funcionalidade autofill de vendas.
- **Ação Necessária:** Substituir a busca `getattr(obj, 'preco', None)` por `getattr(obj, 'preco_venda', getattr(obj, 'preco', None))` para retrocompatibilidade ou acesso direto a `preco_venda`.

### 5. [CORRIGIDO] Estoque não sendo debitado no Agendamento (`agenda/models.py`)
- **Problema:** A `Documentação.md` afirma na seção de Integrações: _"Agendamento -> Produtos / Estoque: Ao adicionar produtos usados no detalhe do agendamento, há baixa no estoque"_. A entidade responsável (`AtendimentoProduto`) contabiliza o `custo_total` mas **não diminui** a contagem de `estoque_atual` daquele produto na Loja.
- **Ação Necessária:** Implementar o débito da variável `estoque_atual` (e a possível devolução ao deletar) dentro do `.save()` de `AtendimentoProduto`, além de considerar o recálculo via `post_save` e `post_delete` Signals para respeitar o Clean Code e não inflar a modelagem além do necessário.

---

**Observação:**
Nenhuma ação de correção foi executada no código. O presente documento foi gerado a título de planejamento da refatoração e documentação anterior a qualquer implementação.

---

## Metodologia de Revisão Completa do Sistema (Auditoria em 7 Etapas)

Para atestar o pleno e irrestrito funcionamento da plataforma, suas interações e integrações modulares (Clean Code), foi desenvolvido este plano de ação em 7 etapas verificáveis:

### Etapa 1: Autenticação, Usuários e Multi-tenant (Empresas) [CONCLUÍDA]
- **Objetivo:** Garantir a segurança e separação de dados.
- **Testes Requeridos:**
  - Login, permissões e restrições de rotas (`@login_required` e acessos `superuser` x profissionais comuns).
  - Validação do `EmpresaMiddleware` para cenários single-tenant vs multi-tenant (vazamento de dados entre empresas `request.empresa`).

### Etapa 2: Clientes e Serviços (Cadastros Base) [CONCLUÍDA]
- **Objetivo:** Auditar fluxos vitais do funcionamento estético.
- **Testes Requeridos:**
  - Fluxo CRUD em `clientes` e `servicos`.
  - Tratamento de cadastros atrelados à exclusão (Proteção contra deleção em cascata não proposital em vendas/agendamentos atrelados a um cliente inativo).

### Etapa 3: Gestão de Produtos e Estoque (Core de Insumos) [CONCLUÍDA]
- **Objetivo:** Assegurar a integridade do inventário dinâmico.
- **Testes Requeridos:**
  - Validação da estrutura `Produto` / `ProdutoCatalogo` (`produtos/models.py`).
  - Prevenção contra estoque negativo.
  - Testes nas saídas e estornos (CRUD do estoque).

### Etapa 4: Módulo de Agenda (Coração Operacional) [CONCLUÍDA]
- **Objetivo:** Revisar estabilidade e ciclo de vida do agendamento.
- **Testes Requeridos:**
  - Lógica de transição de status (`Pendente` -> `Realizado` / `Cancelado`).
  - **Integrações Críticas:** Verificar se os produtos utilizados do "Carrinho do Agendamento" (`AtendimentoProduto`) estão disparando Signals apropriados de baixa de estoque e contabilização de custos.

### Etapa 5: Vendas Avulsas (Módulo Loja) [CONCLUÍDA]
- **Objetivo:** Verificar a solidez das transações financeiras.
- **Testes Requeridos:**
  - Finalização de Vendas Diretas com `@transaction.atomic` efetivo (falha reversível sem side-effects no estoque).
  - **Integração:** Debitar o estoque corretamente e despachar os registros de entradas pro pipeline financeiro sem dupla-contagem.

### Etapa 6: Hub Financeiro & Dashboard Central [CONCLUÍDA]
- **Objetivo:** Confrontar cálculos e métricas de desempenho.
- **Testes Requeridos:**
  - Validação da recepção automática de lançamentos vindos da Agenda (`serviço realizado`) e da Loja (`venda concluída`).
  - Testes do log (Entradas vs Saídas) para garantir precisão no cálculo de `Lucro Real` no dashboard customizado.

### Etapa 7: Webhooks e Notificações (APIs Externas) [CONCLUÍDA]
- **Objetivo:** Confirmar robustez nas integrações Assíncronas.
- **Testes Requeridos:**
  - Validação das rotas expostas em `notificacoes/urls.py` (Ex: endpoints nativos para WhatsApp).
  - Testes para confirmações de presença autônomas da agenda.
  - Segurança de Webhooks (Token/Assinaturas).
