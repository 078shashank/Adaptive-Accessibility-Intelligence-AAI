#!/bin/bash
# Setup script for AAI Backend
# Run this after installing Python and cloning the repository

set -e  # Exit on first error

echo "🚀 AAI Backend Setup Script"
echo "============================"

# Check Python version
echo "✓ Checking Python installation..."
python --version || (echo "❌ Python not found. Please install Python 3.9+" && exit 1)

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "📥 Upgrading pip..."
pip install --upgrade pip setuptools wheel

# Install requirements
echo "📥 Installing dependencies..."
if [ -f "backend/requirements.txt" ]; then
    pip install -r backend/requirements.txt
else
    echo "Installing default packages..."
    pip install fastapi uvicorn sqlalchemy pydantic python-jose bcrypt python-dotenv pytest pytest-asyncio httpx transformers requests passlib email-validator cryptography slowapi
fi

echo "✓ Dependencies installed"

# Create .env file if it doesn't exist
if [ ! -f "backend/.env" ]; then
    echo "📝 Creating .env file..."
    cp backend/.env.example backend/.env
    echo "✓ .env file created (please update with your values)"
fi

# Initialize database
echo "🗄️  Initializing database..."
cd backend
python -c "from app.database import init_db; init_db(); print('✓ Database initialized')"
cd ..

# Run tests
echo "🧪 Running tests..."
cd backend
pytest app/tests/ -v --tb=short || echo "⚠️  Some tests may have failed"
cd ..

echo ""
echo "✅ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Update backend/.env with your configuration"
echo "2. Start backend server:"
echo "   cd backend && python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000"
echo ""
echo "3. In another terminal, start frontend:"
echo "   cd frontend && npm install && npm start"
echo ""
echo "4. Visit http://localhost:3000 in your browser"
echo ""
echo "📚 Documentation:"
echo "   - API Docs: http://127.0.0.1:8000/docs"
echo "   - README: See README.md in root directory"
