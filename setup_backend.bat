@echo off
echo ========================================
echo Setting up Backend Virtual Environment
echo ========================================

cd backend

echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing dependencies...
pip install -r requirements.txt

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To activate the environment, run:
echo   cd backend
echo   venv\Scripts\activate
echo.
echo Then run the backend:
echo   python app.py
echo.
pause
