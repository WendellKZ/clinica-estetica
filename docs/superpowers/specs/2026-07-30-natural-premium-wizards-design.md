# Tema natural premium e assistentes guiados

## Objetivo

Tornar o sistema mais bonito, contrastado e simples para pessoas com pouca familiaridade com informática, aplicando uma identidade natural premium e convertendo vendas e todos os cadastros principais em fluxos guiados.

## Público e princípios

O sistema será utilizado diariamente por profissionais da clínica que podem ter baixo domínio de informática. A interface deve:

- usar frases curtas e linguagem cotidiana;
- mostrar uma ação principal por vez;
- evitar termos técnicos;
- manter botões grandes e áreas clicáveis amplas;
- deixar obrigatoriedade, erros e próximos passos evidentes;
- impedir perda acidental de dados;
- funcionar bem em computador, tablet e celular;
- preservar o funcionamento quando JavaScript não estiver disponível.

## Identidade natural premium

A nova paleta usará:

- terracota como cor de ação principal;
- verde oliva para sucesso, confirmação e indicadores positivos;
- bege quente nos fundos;
- creme nos cartões e campos;
- marrom profundo nos textos;
- vermelho terroso somente para erros e ações destrutivas.

O contraste seguirá critérios de legibilidade. Cartões terão bordas mais definidas, sombras discretas e hierarquia visual mais clara. Tipografia, espaçamentos, estados de foco e botões serão padronizados em todo o sistema.

## Arquitetura dos assistentes

Os formulários Django e suas regras de validação continuarão sendo a fonte de verdade. Uma camada progressiva de HTML, CSS e JavaScript organizará os campos em etapas sem alterar o formato final enviado ao servidor.

Cada assistente terá:

- título que descreve o objetivo;
- indicador textual de progresso;
- nomes simples para as etapas;
- poucos campos visíveis por vez;
- ajuda curta e exemplos;
- botões “Voltar” e “Continuar”;
- resumo para conferência;
- botão final específico, como “Salvar cliente”;
- foco automático no primeiro erro;
- retorno à etapa que contém um campo inválido.

Sem JavaScript, todas as etapas permanecerão visíveis como seções normais e o formulário continuará utilizável.

## Fluxos

### Venda

1. Cliente e forma de pagamento.
2. Produtos, quantidades e itens avulsos.
3. Conferência de itens, estoque e valores.
4. Finalização e confirmação.

O fluxo respeitará o modelo atual, no qual a venda é criada antes da inclusão de itens, mas apresentará as páginas como uma sequência contínua e orientada.

### Cliente

1. Identificação.
2. Contato.
3. Observações.
4. Conferência e salvamento.

### Produto

1. Identificação.
2. Preço de custo e venda.
3. Estoque e disponibilidade.
4. Conferência e salvamento.

### Serviço

1. Nome e duração.
2. Preço.
3. Conferência e salvamento.

### Usuário

1. Identificação e contato.
2. Nível de acesso e função.
3. Senha.
4. Conferência e salvamento.

O assistente explicará de forma simples a diferença entre administrador e profissional.

## Demais telas

Dashboard, agenda, financeiro, listas e navegação receberão a nova paleta e componentes padronizados. Tabelas terão cabeçalhos mais legíveis, linhas com maior espaçamento, ações identificadas por texto e estados vazios com orientação.

Ações destrutivas ficarão visualmente separadas e exigirão confirmação clara. Mensagens de sucesso informarão o que foi salvo e qual é o próximo passo possível.

## Acessibilidade e facilidade de uso

- contraste suficiente entre texto, fundo e controles;
- foco de teclado visível;
- labels permanentes, sem depender apenas de placeholders;
- ícones sempre acompanhados por texto;
- alvos de toque com tamanho confortável;
- erros associados aos campos;
- mensagens compatíveis com leitores de tela;
- respeito à preferência de movimento reduzido;
- ordem de tabulação previsível.

## Testes

A implementação seguirá TDD e cobrirá:

- renderização das etapas e progresso;
- navegação Voltar/Continuar;
- ausência de bloqueio quando JavaScript estiver desativado;
- envio dos formulários com os mesmos campos atuais;
- retorno automático à etapa que contém erro;
- criação e edição de clientes, produtos, serviços e usuários;
- criação, inclusão de itens e finalização de vendas;
- validação de estoque e prevenção de finalização duplicada;
- responsividade em desktop e celular;
- contraste e presença dos novos componentes;
- suíte completa, migrações, estáticos e smoke tests públicos.

## Estratégia de entrega

A implementação será feita em componentes reutilizáveis para evitar comportamentos diferentes entre formulários:

1. tokens de cor e componentes globais;
2. estrutura comum do assistente;
3. cadastros simples;
4. usuários e permissões;
5. fluxo de venda;
6. listas e telas complementares;
7. validação visual e funcional;
8. deploy e smoke tests online.

## Critérios de conclusão

- tema natural premium aplicado de forma consistente;
- contraste e legibilidade superiores ao tema anterior;
- venda e todos os cadastros definidos funcionam como assistentes;
- linguagem e ações são compreensíveis para usuários iniciantes;
- funcionamento do backend e integridade dos dados são preservados;
- experiência desktop e mobile é validada;
- testes automatizados e públicos passam;
- deploy do Render fica saudável.
