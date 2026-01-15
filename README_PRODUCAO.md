# Produção (Render) — Passo a passo

## 1) Variáveis de ambiente (Render)
Em **Environment → Environment Variables**, adicione:

- `SECRET_KEY` = uma chave grande (segura)
- `DEBUG` = `0`
- `ALLOWED_HOSTS` = `seuapp.onrender.com,seu-dominio.com`
- `CSRF_TRUSTED_ORIGINS` = `https://seuapp.onrender.com,https://seu-dominio.com`
- `DATABASE_URL` = (Render Postgres cria automaticamente ao conectar o DB)
- `SECURE_PROXY_SSL_HEADER` = `1`

## 2) Build e Start (Render)
**Build Command**
```
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
```

**Start Command**
```
gunicorn estetica.wsgi:application --bind 0.0.0.0:$PORT
```

## 3) Criar usuário admin
No Render → Shell:
```
python manage.py createsuperuser
```

## 4) Local (dev)
Crie `.env` copiando de `.env.example` e rode:
```
python manage.py migrate
python manage.py runserver
```

## Static
O `whitenoise` serve os arquivos estáticos em produção (sem S3).
