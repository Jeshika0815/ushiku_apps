@echo off

REM confirm python3 exist
python3 --version > nul 2>&1
if %errorlevel% neq 0 (
    echo "python3 は見つかりませんでした。"
    echo "ただいまから、インストールを実行します。"
    winget install -e --id Python.Python
    exit /b 1
)

REM confirm Django exist
python3 -m django --version > nul 2>&1
if %errorlevel% neq 0 (
    echo "Django は見つかりませんでした。　インストールを実行します。"
    pip install Django
    if %errorlevel% neq 0 (
        echo "Django のインストールに失敗しました。"
        exit /b 1
    )
)

REM run server
python3 manage.py runserver