@echo off

if not exist venv (
    python -m venv venv
    if %errorlevel% neq 0 (
        echo Failed to create virtual environment.
        exit /b 1
    )
    call .\venv\Scripts\activate
    if %errorlevel% neq 0 (
        echo Failed to activate virtual environment.
        exit /b 1
    )
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo Failed to install packages.
        exit /b 1
    )
) else (
    call .\venv\Scripts\activate
    if %errorlevel% neq 0 (
        echo Failed to activate virtual environment.
        exit /b 1
    )
)

python -m main
