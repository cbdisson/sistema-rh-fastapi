@echo off
cd C:\Users\ed_di\OneDrive\Área de Trabalho\P.I RH
call .\venv\Scripts\activate
uvicorn main:app --reload
pause