@echo off
title Clinica Estetica - Servidor Local
echo =========================================
echo    Iniciando Clinica Estetica v1...
echo =========================================
echo.

echo Ativando ambiente virtual...
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
) else (
    echo [AVISO] Ambiente virtual (.venv) nao encontrado no diretorio atual.
    echo O sistema tentara rodar com o Python global.
)

echo.
echo Abrindo o navegador principal...
start http://127.0.0.1:8000/

echo.
echo Iniciando o servidor Django...
:: Executando atraves do executavel local do .venv para garantir modulos
.\.venv\Scripts\python.exe manage.py runserver

echo.
pause
