# Validação e publicação do Clínica Estética

## Objetivo

Validar o sistema Django recebido em um ambiente limpo, corrigir defeitos reproduzíveis, preparar a aplicação para produção e publicar a versão resultante no repositório `WendellKZ/clinica-estetica` e no serviço Render `estetica-clinica`.

## Escopo

A validação cobre:

- inicialização do Django, migrações e integridade dos modelos;
- login, logout, proteção de rotas e permissões por perfil;
- clientes, serviços e usuários;
- agenda, criação e conclusão de atendimentos;
- produtos, vendas, estoque e cálculo dos totais;
- lançamentos financeiros e reflexos das operações;
- templates, arquivos estáticos e rotas principais;
- configurações de segurança e execução equivalentes ao Render;
- endpoint de saúde e comportamento básico do serviço publicado;
- ausência de segredos, banco local, ambiente virtual e artefatos de desenvolvimento no commit.

Não fazem parte deste ciclo integrações reais pagas ou externas, como o envio efetivo de WhatsApp. Essas integrações serão validadas até o limite seguro de configuração, filas e tratamento de erros, sem disparar mensagens para terceiros.

## Estratégia de testes

O trabalho começa pela suíte existente e adiciona testes automatizados de comportamento para os fluxos críticos e seus principais casos de erro. Defeitos encontrados serão tratados com TDD:

1. criar um teste mínimo que reproduza a falha;
2. confirmar que o teste falha pelo motivo esperado;
3. aplicar a correção mínima;
4. confirmar o teste e toda a suíte;
5. refatorar somente quando necessário, mantendo a suíte verde.

Também serão executados:

- `manage.py check`;
- `manage.py test`;
- verificação de migrações pendentes;
- `manage.py check --deploy`;
- coleta de arquivos estáticos com configuração de produção;
- inicialização via Gunicorn em ambiente compatível;
- smoke tests HTTP das páginas públicas e autenticadas;
- teste final da URL pública após o deploy.

## Tratamento das alterações recebidas

O ZIP já contém alterações locais não commitadas. Elas serão preservadas, revisadas e testadas como parte do programa entregue. Arquivos gerados durante testes, caches, banco SQLite local e o ambiente virtual empacotado não serão publicados.

Se uma alteração existente não puder ser validada ou causar regressão, ela será ajustada apenas dentro do escopo necessário para deixar o comportamento consistente e testado.

## Produção e segurança

A configuração do Render continuará baseada no `render.yaml` e em variáveis de ambiente. A aplicação terá uma rota de saúde dedicada, sem depender da tela de login. Serão revisados hosts permitidos, origens CSRF, proxy HTTPS, redirecionamento SSL, HSTS e armazenamento de arquivos estáticos.

Nenhuma chave, senha, token, banco de dados local ou valor sensível será adicionado ao Git. Configurações locais serão documentadas apenas com valores de exemplo.

## Publicação

Após todas as verificações passarem:

1. revisar o diff e o estado do repositório;
2. criar um commit intencional contendo somente arquivos do projeto;
3. enviar a branch principal ao remoto existente;
4. acompanhar o deploy automático do Render;
5. validar a rota de saúde, login e páginas principais na URL pública;
6. entregar um relatório curto com testes executados, correções, commit e endereço publicado.

Caso GitHub ou Render exijam autenticação interativa, a publicação será pausada apenas no ponto exato dessa autorização, sem descartar o trabalho já validado.

## Critérios de conclusão

O trabalho estará concluído quando:

- todos os testes automatizados estiverem passando;
- não houver migrações de modelo pendentes;
- a coleta de estáticos e a inicialização de produção funcionarem;
- alertas de segurança aplicáveis ao Render estiverem resolvidos ou explicitamente justificados;
- o repositório remoto contiver o commit validado;
- o deploy estiver saudável e os smoke tests públicos passarem;
- limitações externas remanescentes estiverem claramente registradas.
