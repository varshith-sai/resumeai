@echo off
echo ==========================================
echo    ResumeAI — Windows Setup Script
echo ==========================================

echo.
echo Checking Python version...
python --version
if %errorlevel% neq 0 (
  echo ERROR: Python not found. Install from https://www.python.org/downloads/
  pause
  exit /b 1
)

echo.
echo Checking Node.js version...
node --version
if %errorlevel% neq 0 (
  echo ERROR: Node.js not found. Install from https://nodejs.org/
  pause
  exit /b 1
)

echo.
echo Creating Python virtual environment...
python -m venv venv
call venv\Scripts\activate

echo.
echo Installing Python dependencies...
pip install --upgrade pip
pip install -r requirements.txt

if %errorlevel% neq 0 (
  echo ERROR: Failed to install Python dependencies
  pause
  exit /b 1
)
echo Python dependencies installed successfully

echo.
echo Installing frontend dependencies...
cd frontend
npm install
if %errorlevel% neq 0 (
  echo ERROR: Failed to install frontend dependencies
  pause
  exit /b 1
)
echo Frontend dependencies installed successfully
cd ..

echo.
if not exist config.yaml (
  copy config.example.yaml config.yaml
  echo config.yaml created — edit it with your personal details
) else (
  echo config.yaml already exists
)

if not exist .env (
  copy .env.example .env
  echo .env created — add your API tokens
) else (
  echo .env already exists
)

mkdir data 2>nul
mkdir output 2>nul

echo.
echo ==========================================
echo Setup complete!
echo.
echo Next steps:
echo 1. Edit .env and add your HF_API_TOKEN and GITHUB_TOKEN
echo 2. Edit config.yaml with your personal details
echo 3. Add your resume text to data\master_resume.txt
echo.
echo To run the app:
echo   Terminal 1: venv\Scripts\activate then uvicorn backend.main:app --reload
echo   Terminal 2: cd frontend then npm run dev
echo   Open: http://localhost:5173
echo ==========================================
pause