# Patch v1.3.8.6 — Fix `agenda_dia` missing (AttributeError)

## Problema
Ao subir o servidor, ocorre:
`AttributeError: module 'agenda.views' has no attribute 'agenda_dia'`

Isso acontece porque o `agenda/urls.py` aponta para `views.agenda_dia`, mas essa função não existe no `agenda/views.py`.

## Solução
Criar um *alias* `agenda_dia` que reaproveita a view existente (`agenda_lista`).

## Como aplicar
1. Extraia o ZIP na raiz do projeto (onde existe a pasta `agenda/`).
2. Confirme/mescle a alteração no arquivo `agenda/views.py` conforme abaixo.
3. Reinicie o servidor.

> Se você já tiver customizações em `agenda/views.py`, **não substitua** o arquivo inteiro — apenas cole a função `agenda_dia` no final (ou próximo das outras views).
