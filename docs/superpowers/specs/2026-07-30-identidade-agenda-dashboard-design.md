# Identidade visual e agenda semanal no Dashboard

## Objetivo

Aplicar a identidade “Elisângela Barbosa Estética” à autenticação e à navegação principal, substituindo o texto genérico “Sistema Clínica”, e apresentar no Dashboard uma prévia útil da agenda da semana.

## Identidade visual

A imagem fornecida será adicionada aos arquivos estáticos do projeto sem substituir ou alterar o arquivo original.

Na tela de login:

- a imagem completa será usada como painel de identidade visual;
- em telas largas, painel visual e formulário ficarão lado a lado;
- em telas pequenas, a composição será empilhada;
- o formulário continuará acessível, legível e funcional;
- textos e título da página usarão “Elisângela Barbosa Estética”.

Na navegação:

- a marca do menu lateral substituirá o ícone e o texto “Sistema Clínica”;
- a barra mobile exibirá a mesma identidade;
- o recorte será feito por CSS sobre a região central da imagem, evitando gerar uma segunda imagem derivada;
- títulos genéricos do sistema serão substituídos pela marca da clínica.

## Prévia da agenda semanal

O Dashboard exibirá uma seção “Agenda da semana” abaixo dos indicadores financeiros e antes do bloco de acesso rápido.

A consulta abrangerá a semana corrente, de segunda-feira a domingo, e respeitará a empresa ativa quando o modelo possuir vínculo com empresa. Somente dias que contenham agendamentos serão renderizados.

Cada dia será apresentado em um card responsivo. Cada agendamento mostrará:

- horário inicial;
- cliente;
- serviço;
- profissional;
- status.

Os itens serão ordenados cronologicamente. Quando não houver agendamentos na semana, a seção exibirá uma mensagem amigável e um atalho para criar um novo agendamento.

## Responsividade e estilo

Os componentes reutilizarão a linguagem visual existente, com cores suaves, bordas e espaçamentos consistentes. A agenda será organizada em cards que se adaptam a uma coluna no celular e múltiplas colunas em telas maiores.

A imagem não será esticada. No login será preservada a proporção original; no menu será usada uma janela de recorte com `object-fit: cover` e posicionamento central.

## Testes

A implementação seguirá TDD:

1. teste da consulta da semana corrente;
2. teste de exclusão de dias sem agendamentos;
3. teste da filtragem por empresa;
4. teste do estado vazio;
5. teste de presença da nova identidade nos templates;
6. suíte completa, migrações, coleta de estáticos e smoke tests.

## Publicação

Após todos os testes:

1. revisar o diff e confirmar que a imagem está versionada;
2. executar a suíte completa e a coleta de estáticos;
3. criar commit e enviar à branch `main`;
4. acionar e acompanhar o deploy do Render;
5. validar login, Dashboard, imagem e arquivos estáticos na URL pública.

## Critérios de conclusão

- a marca aparece corretamente no login, menu desktop e barra mobile;
- “Sistema Clínica” não aparece mais nas áreas substituídas;
- o Dashboard mostra somente dias da semana corrente que possuem agendamentos;
- cada item contém as informações definidas;
- o estado vazio é claro e possui atalho de criação;
- layout desktop e mobile permanecem utilizáveis;
- testes locais e smoke tests públicos passam.
