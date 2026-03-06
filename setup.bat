@echo off
REM Setup script for AAI Backend on Windows
REM Run this after installing Python and cloning the repository

echo.
echo 🚀 AAI Backend Setup Script
echo ============================
echo.

REM Check Python version
echo ✓ Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found. Please install Python 3.9+ from https://www.python.org/
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 📦 Creating Python virtual environment...
    python -m venv venv
    echo ✓ Virtual environment created
) else (
    echo ✓ Virtual environment already exists
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo 📥 Upgrading pip...
python -m pip install --upgrade pip setuptools wheel

REM Install requirements
echo 📥 Installing dependencies...
if exist "backend\requirements.txt" (
    pip install -r backend\requirements.txt
) else (
    echo Installing default packages...
    pip install fastapi uvicorn sqlalchemy pydantic python-jose bcrypt python-dotenv pytest pytest-asyncio httpx transformers requests passlib email-validator cryptography slowapi
)

echo ✓ Dependencies installed
echo.

REM Create .env file if it doesn't exist
if not exist "backend\.env" (
    echo 📝 Creating .env file...
    copy backend\.env.example backend\.env
    echo ✓ .env file created (please update with your values)
) else (
    echo ✓ .env file already exists
)

REM Initialize database
echo 🗄️  Initializing database...
cd backend
python -c "from app.database import init_db; init_db(); print('✓ Database initialized')"
cd ..

REM Run tests
echo 🧪 Running tests...
cd backend
pytest app/tests/ -v --tb=short
if %errorlevel% neq 0 (
    echo ⚠️  Some tests may have failed - check output above
)
cd ..

echo.
echo ✅ Setup complete!
echo.
echo 📋 Next steps:
echo 1. Update backend\.env with your configuration
echo 2. Start backend server in one terminal:
echo    cmd /k "cd backend && python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000"
echo.
echo 3. In another terminal, start frontend:
echo    cmd /k "cd frontend && npm install && npm start"
echo.
echo 4. Visit http://localhost:3000 in your browser
echo.
echo 📚 Documentation:
echo    - API Docs: http://127.0.0.1:8000/docs
echo    - README: See README.md in root directory
echo.
pause
