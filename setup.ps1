# Setup script for AAI Backend on Windows (PowerShell version)
# Run: powershell -ExecutionPolicy Bypass -File setup.ps1

Write-Host "🚀 AAI Backend Setup Script" -ForegroundColor Green
Write-Host "============================" -ForegroundColor Green
Write-Host ""

# Check Python installation
Write-Host "✓ Checking Python installation..." -ForegroundColor Cyan
try {
    $pythonVersion = python --version 2>&1
    Write-Host "  Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found. Please install Python 3.9+ from https://www.python.org/" -ForegroundColor Red
    exit 1
}

# Create virtual environment
if (-not (Test-Path "venv")) {
    Write-Host "📦 Creating Python virtual environment..." -ForegroundColor Cyan
    python -m venv venv
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
} else {
    Write-Host "✓ Virtual environment already exists" -ForegroundColor Green
}

# Activate virtual environment
Write-Host "🔧 Activating virtual environment..." -ForegroundColor Cyan
& ".\venv\Scripts\Activate.ps1"

# Upgrade pip
Write-Host "📥 Upgrading pip..." -ForegroundColor Cyan
python -m pip install --upgrade pip setuptools wheel | Out-Null

# Install requirements
Write-Host "📥 Installing dependencies..." -ForegroundColor Cyan
if (Test-Path "backend\requirements.txt") {
    pip install -r backend\requirements.txt
} else {
    Write-Host "Installing default packages..." -ForegroundColor Yellow
    pip install fastapi uvicorn sqlalchemy pydantic python-jose bcrypt python-dotenv pytest pytest-asyncio httpx transformers requests passlib email-validator cryptography slowapi
}
Write-Host "✓ Dependencies installed" -ForegroundColor Green
Write-Host ""

# Create .env file
if (-not (Test-Path "backend\.env")) {
    Write-Host "📝 Creating .env file..." -ForegroundColor Cyan
    Copy-Item "backend\.env.example" "backend\.env"
    Write-Host "✓ .env file created (please update with your values)" -ForegroundColor Green
} else {
    Write-Host "✓ .env file already exists" -ForegroundColor Green
}

# Initialize database
Write-Host "🗄️  Initializing database..." -ForegroundColor Cyan
Push-Location "backend"
python -c "from app.database import init_db; init_db(); print('✓ Database initialized')"
Pop-Location

# Run tests
Write-Host "🧪 Running tests..." -ForegroundColor Cyan
Push-Location "backend"
pytest app/tests/ -v --tb=short
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  Some tests may have failed - check output above" -ForegroundColor Yellow
}
Pop-Location

Write-Host ""
Write-Host "✅ Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Next steps:" -ForegroundColor Yellow
Write-Host "1. Update backend\.env with your configuration"
Write-Host "2. Start backend server in one PowerShell window:"
Write-Host "   cd backend; python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000"
Write-Host ""
Write-Host "3. In another PowerShell window, start frontend:"
Write-Host "   cd frontend; npm install; npm start"
Write-Host ""
Write-Host "4. Visit http://localhost:3000 in your browser"
Write-Host ""
Write-Host "📚 Documentation:" -ForegroundColor Yellow
Write-Host "   - API Docs: http://127.0.0.1:8000/docs"
Write-Host "   - README: See README.md in root directory"
Write-Host ""
