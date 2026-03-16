# Patch V1.3.3.2 — Correção NoReverseMatch (namespace agenda) no menu

## Problema
Após o patch do menu "Administração", apareceu:
NoReverseMatch: 'agenda' is not a registered namespace

Isso ocorre porque o projeto atual não usa namespace (ex: agenda:agenda) nas URLs.

## Solução
Este patch ajusta o `templates/base.html` para usar URLs seguras (paths diretos)
sem namespace, mantendo o dropdown **Administração** (Usuários + Serviços).

## Como aplicar
1) Extraia o zip na raiz do projeto (mesmo nível do manage.py), sobrescrevendo.
2) Reinicie:
   python manage.py runserver
