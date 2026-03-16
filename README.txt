PATCH v1.3.8.3 - Corrige NoReverseMatch: Reverse for 'agenda' not found

O erro acontece porque algum template está chamando {% url 'agenda' %},
mas no projeto a rota da agenda semanal está registrada com outro name
(ex: 'agenda_lista').

O que este patch faz:
- Procura e substitui referências a "{% url 'agenda' %}" / "{% url "agenda" %}"
  por "{% url 'agenda_lista' %}" em templates da pasta templates/agenda/.

Como aplicar:
1) Extraia este .zip dentro da pasta do projeto (mesma pasta do manage.py).
2) Rode:
   python apply_patch.py
3) Reinicie o servidor:
   python manage.py runserver

Obs:
- O script faz backup dos arquivos alterados com extensão .bak
