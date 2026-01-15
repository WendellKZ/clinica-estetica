# Clínica Estética - V1 (Agenda + Loja + Financeiro + Lucro Real)

## O que tem pronto
- Login
- Clientes (CRUD)
- Agenda do dia (CRUD + detalhe)
- Marcar agendamento como REALIZADO (gera entrada no financeiro)
- Produtos (CRUD)
- Venda avulsa (criar venda, adicionar itens, finalizar -> baixa estoque + gera entrada no financeiro)
- Financeiro (lançamentos manuais + filtros)
- Dashboard com **lucro real** (Entradas - Saídas - Custo dos produtos vendidos)

## Como rodar localmente (Windows / Linux / Mac)
1) Crie e ative um venv
   - Windows (PowerShell):
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
   - Linux/Mac:
     python3 -m venv .venv
     source .venv/bin/activate

2) Instale dependências
   pip install -r requirements.txt

3) Migrações
   python manage.py migrate

4) Crie um usuário admin
   python manage.py createsuperuser

5) Suba o servidor
   python manage.py runserver

Abra:
- http://127.0.0.1:8000/login/
- Admin: http://127.0.0.1:8000/admin/

## Primeiro uso (para testar rápido)
1) Admin -> crie alguns usuários (profissionais), clientes, serviços e produtos (com estoque, custo e preço).
2) Faça um agendamento e marque como REALIZADO (vai gerar entrada).
3) No detalhe do agendamento, adicione produtos usados (baixa estoque e entra no custo do lucro real).
4) Faça uma venda avulsa em /loja/vendas/nova/, adicione itens e finalize.
5) Veja o Dashboard e o Financeiro para conferir o lucro real.

## Observações do V1
- Agenda é uma lista por dia (mais simples). Evolução (V2): calendário semanal/mensal.
- Estoque é simples: baixa ao vender e ao usar no atendimento.
- Lucro real considera custos dos produtos vendidos/usados.


## V1.1 - Melhorias
- Venda: permite cadastrar item na hora (nome + preço; custo opcional para manter lucro real)
- Agendamento e Venda: permite cadastrar cliente na hora
