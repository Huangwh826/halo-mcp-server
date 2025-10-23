@echo off
chcp 65001 >nul
echo ========================================
echo Halo MCP Server - Windows Setup Script
echo ========================================
echo.

REM Check Python version
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found! Please install Python 3.10 or higher.
    pause
    exit /b 1
)

echo [1/5] Checking Python version...
python -c "import sys; exit(0 if sys.version_info >= (3, 10) else 1)"
if errorlevel 1 (
    echo [ERROR] Python 3.10+ required. Please upgrade Python.
    pause
    exit /b 1
)
echo [OK] Python version check passed

echo.
echo [2/5] Creating virtual environment...
if exist venv (
    echo [INFO] Virtual environment already exists
) else (
    python -m venv venv
    echo [OK] Virtual environment created
)

echo.
echo [3/5] Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo [4/5] Installing dependencies...
pip install --upgrade pip
pip install -e .
if errorlevel 1 (
    echo [ERROR] Installation failed
    pause
    exit /b 1
)
echo [OK] Dependencies installed

echo.
echo [5/5] Setting up configuration...
if exist .env (
    echo [INFO] .env file already exists
) else (
    copy .env.example .env
    echo [OK] Created .env file
    echo.
    echo [IMPORTANT] Please edit .env file and add your Halo configuration:
    echo - HALO_BASE_URL
    echo - HALO_TOKEN
)

echo.
echo ========================================
echo Setup completed successfully!
echo ========================================
echo.
echo Next steps:
echo 1. Edit .env file and add your Halo Token
echo 2. Configure Claude Desktop (see QUICKSTART.md)
echo 3. Run: python -m halo-mcp-server
echo.
echo For detailed instructions, see QUICKSTART.md
echo.
pause
