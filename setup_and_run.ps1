# Setup and Run Script for Windows PowerShell
# Email Productivity Agent

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "Email Productivity Agent - Setup & Run" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Check Python version
Write-Host "[1/6] Checking Python version..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] Python found: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "[ERROR] Python not found! Please install Python 3.9 or higher" -ForegroundColor Red
    exit 1
}

# Create virtual environment if it doesn't exist
Write-Host ""
Write-Host "[2/6] Setting up virtual environment..." -ForegroundColor Yellow
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Gray
    python -m venv venv
    Write-Host "[OK] Virtual environment created" -ForegroundColor Green
} else {
    Write-Host "[OK] Virtual environment already exists" -ForegroundColor Green
}

# Activate virtual environment
Write-Host ""
Write-Host "[3/6] Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"
if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] Virtual environment activated" -ForegroundColor Green
} else {
    Write-Host "[WARNING] Could not activate virtual environment" -ForegroundColor Yellow
    Write-Host "You may need to run: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser" -ForegroundColor Yellow
}

# Install dependencies
Write-Host ""
Write-Host "[4/6] Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt --quiet
if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] Dependencies installed" -ForegroundColor Green
} else {
    Write-Host "[ERROR] Failed to install dependencies" -ForegroundColor Red
    exit 1
}

# Check for .env file
Write-Host ""
Write-Host "[5/6] Checking configuration..." -ForegroundColor Yellow
if (-not (Test-Path ".env")) {
    Write-Host "[WARNING] .env file not found!" -ForegroundColor Yellow
    Write-Host "Creating .env from .env.example..." -ForegroundColor Gray
    Copy-Item ".env.example" ".env"
    Write-Host ""
    Write-Host "[WARNING] IMPORTANT: Edit .env file and add your API key!" -ForegroundColor Red
    Write-Host "  1. Open .env in a text editor" -ForegroundColor Yellow
    Write-Host "  2. Get FREE Gemini API key from: https://aistudio.google.com/app/apikey" -ForegroundColor Yellow
    Write-Host "  3. Add to .env: GEMINI_API_KEY=AIza..." -ForegroundColor Yellow
    Write-Host "  4. Set: LLM_PROVIDER=gemini" -ForegroundColor Yellow
    Write-Host "  5. Save the file" -ForegroundColor Yellow
    Write-Host ""
    $response = Read-Host "Have you added your API key? (y/n)"
    if ($response -ne "y") {
        Write-Host "Please add your API key and run this script again" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "[OK] .env file found" -ForegroundColor Green
}

# Create data directory if needed
if (-not (Test-Path "data")) {
    New-Item -ItemType Directory -Path "data" | Out-Null
}

# Run tests (optional)
Write-Host ""
Write-Host "[6/6] Running tests..." -ForegroundColor Yellow
$runTests = Read-Host "Run basic tests before starting? (y/n)"
if ($runTests -eq "y") {
    python tests/test_basic.py
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[WARNING] Some tests failed, but you can continue" -ForegroundColor Yellow
    }
}

# Ready to launch
Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "[OK] Setup Complete!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Starting Email Productivity Agent..." -ForegroundColor Cyan
Write-Host "The app will open in your browser at http://localhost:8501" -ForegroundColor Gray
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Launch Streamlit
streamlit run frontend/app.py
