# Patch V1.2.9.1 - Fix Agenda (NoReverseMatch)

## Problema
O template novo referenciava a URL name `agenda_semana`, mas no seu projeto essa rota não está registrada com esse nome.

## Correção
Removi os botões "Semana anterior/Hoje/Próxima semana" que dependiam de `agenda_semana`, mantendo:
- Cabeçalho
- Botão "Novo agendamento"
- Layout responsivo (mobile/tablet) com `dias`

## Aplicar
1) Pare o servidor
2) Extraia o ZIP na raiz (sobrescrevendo)
3) Rode: python manage.py runserver
4) Ctrl+F5 no navegador

## Próximo passo (opcional)
Se você quiser a navegação semanal, eu preparo um patch para registrar a rota `agenda_semana` no `agenda/urls.py`.
