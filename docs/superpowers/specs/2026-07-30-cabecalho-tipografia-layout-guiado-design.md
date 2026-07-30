# Cabeçalho contextual, tipografia e layout guiado

## Objetivo

Melhorar a organização e a leitura do sistema para a equipe da clínica, evitando informações repetidas e tornando cada operação guiada mais clara para pessoas com pouca familiaridade com informática.

## Identidade e cabeçalho

- A barra lateral exibirá somente o logo Elisângela Barbosa Estética.
- O cabeçalho superior deixará de repetir o nome da clínica.
- Cada template fornecerá um título contextual por meio do bloco `header_title`.
- Exemplos: “Visão geral”, “Nova venda”, “Clientes”, “Novo cliente”, “Agenda” e “Novo serviço”.
- O título da aba do navegador continuará identificando a tela e a clínica.

## Tipografia

- Títulos de página e de etapa usarão uma família serifada elegante, com alternativas locais seguras.
- Textos, menus, campos e botões usarão uma família sem serifa de alta legibilidade.
- O sistema não dependerá de uma fonte remota para funcionar ou manter sua organização.
- Tamanhos, pesos e espaçamento serão ampliados onde necessário para leitura rápida.

## Assistentes guiados

- Vendas e cadastros de clientes, produtos, serviços e usuários adotarão o mesmo componente visual.
- Em telas largas, as etapas ficarão em um painel verde-oliva à esquerda e o formulário à direita.
- A etapa atual terá destaque; etapas anteriores terão indicação de conclusão.
- Cada etapa mostrará poucos campos, uma explicação curta e ações previsíveis.
- “Voltar” ficará à esquerda e “Continuar” ou a ação final ficará à direita.
- Campos terão rótulos acima, largura coerente, altura confortável e foco visível.
- Na venda, a primeira etapa organizará claramente cliente existente e novo cliente.

## Responsividade e acessibilidade

- Em telas pequenas, o painel lateral se transformará em uma faixa horizontal de progresso.
- Os botões permanecerão grandes e fáceis de tocar.
- A ordem visual seguirá a ordem de navegação por teclado.
- Sem JavaScript, todas as etapas continuarão disponíveis em sequência no mesmo formulário.
- Mensagens de erro permanecerão próximas ao campo correspondente.

## Implementação

- `base.html` será a fonte do cabeçalho contextual.
- `guided-workflows.css` concentrará tipografia, painel de etapas, campos e responsividade.
- `guided-workflows.js` continuará controlando navegação e progresso, adicionando indicação de etapas concluídas.
- Os cinco templates guiados fornecerão seus títulos e usarão a estrutura comum.
- Nenhum modelo, banco de dados ou regra comercial será alterado.

## Testes e publicação

- Testes verificarão o título contextual nas principais telas.
- Testes verificarão a estrutura guiada nos cinco fluxos.
- A suíte Django completa deverá passar.
- Os arquivos estáticos serão coletados e validados.
- Após aprovação, as alterações serão enviadas ao GitHub, publicadas no Render e verificadas pela URL pública.
