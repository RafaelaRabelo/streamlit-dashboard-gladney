@echo off
echo Iniciando Streamlit com Chrome...

:: Caminho até a pasta onde está seu projeto
cd "C:\Users\rafae\Downloads\Projeto_Gladney_Dashboard"

:: Executa o Streamlit sem abrir aba automaticamente
start "" streamlit run test_looker.py --server.headless true

:: Aguarda alguns segundos para garantir que o servidor subiu
timeout /t 5 > nul

:: Abre manualmente no Chrome
start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" http://localhost:8080

pause
