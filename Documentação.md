# Documentação do Projeto - Clínica Estética V1

## Visão Geral
Sistema de gestão para clínica de estética contendo os módulos de Agenda, Loja (vendas de produtos), Financeiro e cálculo de Lucro Real. O projeto foi construído utilizando o framework Django (Python).

### Como Iniciar (Ambiente de Desenvolvimento)
No Windows, basta dar dois cliques no arquivo **`Iniciar_Sistema.bat`** (localizado na pasta principal do projeto). 
Este script cuida de:
1. Ativar o ambiente virtual (Python).
2. Abrir a página principal (`http://127.0.0.1:8000/`) no seu navegador padrão.
3. Iniciar o servidor local do Django (`manage.py runserver`).

## Tecnologias e Dependências
- **Linguagem:** Python
- **Framework Web:** Django
- **Banco de Dados:** SQLite (padrão local), configurável via `DATABASE_URL` (dj_database_url).
- **Outros pacotes importantes:** python-dotenv (gerenciamento de variáveis de ambiente), whitenoise (arquivos estáticos).
- **UI/UX & Estilos:** Utilização de Bootstrap 5 combinado com CSS Vanilla Customizado (`estetica_dashboard.css`).
  - O projeto utiliza uma arquitetura visual de *Sidebar + Main Content*, favorecendo painéis responsivos. Padrão de cores focado em tons pastéis (Rose Gold/Mint). As classes específicas de customização (`btn-estetica`, `stat-card`, etc.) substituem o uso de utilitários rígidos do Bootstrap para dar personalidade.

## Estrutura do Projeto (Apps Django)
O sistema é dividido nos seguintes aplicativos independentes:
1. `core`: Configurações e views principais, como a tela de login.
2. `usuarios`: Gerenciamento de profissionais e perfis de usuário.
3. `clientes`: Cadastro (CRUD) de clientes.
4. `agenda`: Controle de agendamentos contendo CRUD e detalhes. Integra com o financeiro ao marcar agendamentos como realizados.
5. `servicos`: Cadastro dos serviços oferecidos pela clínica.
6. `produtos`: Gestão do catálogo e estoque de produtos.
7. `loja`: Módulo de vendas avulsas de produtos (baixa estoque e lança no financeiro).
8. `financeiro`: Lançamentos manuais, filtros e dashboard com lucro real (Entradas - Saídas - Custo dos produtos vendidos).
9. `empresas`: Gestão Multi-empresa (indicado pela presença de `empresas.middleware.EmpresaMiddleware`).
10. `notificacoes`: Módulo de webhooks, especificamente WhatsApp (`/webhooks/whatsapp/`).

## Principais Interações
- **Agendamento -> Financeiro:** Ao marcar um agendamento como `REALIZADO`, é gerada automaticamente uma entrada no financeiro.
- **Agendamento -> Produtos / Estoque:** Ao adicionar produtos usados no detalhe do agendamento, há baixa no estoque e o custo é contabilizado para o lucro real.
- **Venda (Loja) -> Financeiro / Estoque:** A venda avulsa de produtos baixa o estoque correspondente e gera entrada financeira (e custo).

## Páginas e Rotas Principais
- `/`: Dashboard e módulo principal (`core.urls`)
- `/login/`: Autenticação 
- `/admin/`: Painel administrativo do Django
- `/clientes/`: Gestão de Clientes
- `/agenda/`: Gestão da Agenda
- `/loja/`: Módulo de Vendas
- `/financeiro/`: Dashboard Financeiro e lançamentos
- `/usuarios/`: Gestão de Profissionais
- `/servicos/`: Cadastro de Serviços
- `/produtos/`: Gestão de Produtos e Estoque
- `/webhooks/whatsapp/`: Recebimento de notificações do WhatsApp

## Manutenção e Evolução
Este documento é a base para a manutenção arquitetural do projeto. Qualquer nova funcionalidade, alteração no modelo de dados ou na estrutura de dependências deve ser refletida aqui.
> **Importante:** Sempre respeite as responsabilidades de cada app (ex: lógica de estoque fica em `produtos` ou `loja`, lógica de dinheiro em `financeiro`).

## Metodologia Oficial de Revisão & Qualidade
Foi estipulado e documentado no arquivo auxiliar auxiliar estratégico (`Reparos.md`) um **Ciclo de Auditoria e Revisão Sistêmica em 7 Etapas**, que serve como checklist normativo para homologar ou garantir a integridade entre os módulos vitais:
1. Autenticação e Multi-empresas.
2. Cadastros de Clientes/Serviços.
3. Estoque e Insumos.
4. Ciclos da Agenda.
5. Operações de Venda (Loja).
6. Consolidação Financeira.
7. Webhooks/Notificações Externas.

Sempre que refatorações arquiteturais estruturadas se fizerem necessárias, esta trilha deve ser testada para prevenir breaking changes nos fluxos de negócio.
