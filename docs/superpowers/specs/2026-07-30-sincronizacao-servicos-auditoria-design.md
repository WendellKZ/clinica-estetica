# Sincronização de serviços e auditoria dos fluxos críticos

## Diagnóstico

O painel administrativo grava serviços em `servicos.Servico`, enquanto os agendamentos possuem chave estrangeira para `agenda.Servico`. O sinal de sincronização existente tenta copiar campos que não existem no modelo da agenda. A exceção é capturada silenciosamente, portanto o cadastro aparenta sucesso, mas o serviço não entra na lista da agenda.

## Correção

- Manter os dois modelos nesta entrega para evitar uma migração arriscada das relações já existentes.
- Criar uma função explícita e testável de sincronização.
- Mapear:
  - `servicos.Servico.nome` → `agenda.Servico.nome`
  - `servicos.Servico.preco_padrao` → `agenda.Servico.preco`
  - `servicos.Servico.duracao_min` → `agenda.Servico.duracao_minutos`
- Novos serviços e edições serão sincronizados pelo sinal `post_save`.
- O sinal não ocultará erros de programação ou campos incompatíveis.
- Serviços inativos serão excluídos das opções para novos agendamentos sem apagar agendamentos históricos.
- Uma migração de dados idempotente copiará os serviços já cadastrados para a agenda durante o deploy.
- Registros serão conciliados pelo nome, preservando as referências existentes.

## Segurança dos dados

- Nenhum agendamento, atendimento, cliente, venda ou lançamento financeiro será apagado.
- A sincronização poderá ser executada repetidamente sem duplicar serviços.
- Serviços históricos já vinculados continuarão válidos.
- A futura unificação dos modelos ficará fora desta entrega.

## Auditoria automatizada

Serão cobertos:

- cadastro e edição de serviço;
- serviço ativo disponível no novo agendamento;
- serviço desativado indisponível para novos agendamentos;
- agendamento completo e bloqueio de horário retroativo;
- conclusão de atendimento e lançamento financeiro idempotente;
- cadastro e edição de clientes;
- criação, itens e finalização idempotente de venda;
- baixa e devolução de estoque;
- páginas autenticadas e permissões administrativas;
- saúde da aplicação, arquivos estáticos e comandos de implantação.

“Testar 100%” será tratado como cobertura integral dos fluxos críticos conhecidos, além da suíte existente. Não representa garantia matemática de que nenhum defeito futuro possa ocorrer.

## Publicação

- Executar testes direcionados e suíte completa.
- Executar verificações do Django, migrações e coleta de estáticos.
- Publicar no GitHub e Render.
- Confirmar migração concluída, serviço saudável e presença dos serviços ativos no ambiente online.
