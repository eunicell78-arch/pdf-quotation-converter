@echo off
REM PDF Quotation Converter - GUI Launcher
REM Double-click this file to run the converter

echo =====================================
echo    PDF 견적서 변환기 시작 중...
echo =====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [오류] Python이 설치되어 있지 않습니다.
    echo Python 3.7 이상을 설치해주세요: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

REM Check if required packages are installed
python -c "import pdfplumber, pandas, tkinter" >nul 2>&1
if errorlevel 1 (
    echo [알림] 필요한 패키지를 설치합니다...
    echo.
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [오류] 패키지 설치에 실패했습니다.
        echo 수동으로 설치해주세요: pip install -r requirements.txt
        echo.
        pause
        exit /b 1
    )
)

REM Run the GUI application
python converter_gui.py

if errorlevel 1 (
    echo.
    echo [오류] 프로그램 실행 중 오류가 발생했습니다.
    pause
)
