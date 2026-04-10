@echo off
cd /d "%~dp0"

echo Starting Streamlit...
start "" python -m streamlit run app.py

timeout /t 5 >nul

echo Opening app...
start "" http://localhost:8501

exit