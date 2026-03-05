@echo off
REM Setup script for Hand Gesture Recognition application (Windows)

echo.
echo ==========================================
echo Hand Gesture Recognition - Setup Script
echo ==========================================
echo.

REM Check Python version
echo Checking Python version...
python --version

echo.
echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo ==========================================
echo Setup complete!
echo ==========================================
echo.
echo To start the application, run:
echo   venv\Scripts\activate.bat (if not already activated)
echo   python app.py
echo.
echo Then open your browser and go to:
echo   http://localhost:5000
echo.
echo ==========================================
echo.
pause
