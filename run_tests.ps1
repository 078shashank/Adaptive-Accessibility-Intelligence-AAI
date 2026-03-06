# Test Runner Script
cd "C:\Users\s.shashank.kumar\OneDrive - Accenture\Desktop\Project\backend"

# Activate virtual environment
& .\venv\Scripts\Activate.ps1

# Install requirements if needed
python -m pip install -q fastapi uvicorn sqlalchemy pydantic pytest httpx python-multipart

# Run tests
echo "=== Running Backend Tests ==="
python -m pytest app/tests -v --tb=short

# Show summary
echo ""
echo "=== Test Summary ==="
python -m pytest app/tests --co -q
