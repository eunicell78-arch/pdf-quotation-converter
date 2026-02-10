@echo off
REM Build EXE file using PyInstaller
REM This creates a standalone executable that doesn't require Python installation

echo =====================================
echo    EXE 파일 빌드 시작
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

REM Check if PyInstaller is installed
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo [알림] PyInstaller를 설치합니다...
    echo.
    pip install pyinstaller
    if errorlevel 1 (
        echo [오류] PyInstaller 설치에 실패했습니다.
        echo.
        pause
        exit /b 1
    )
)

REM Clean previous build
if exist "dist" (
    echo 이전 빌드 삭제 중...
    rmdir /s /q dist
)
if exist "build" (
    rmdir /s /q build
)
REM Remove old .spec file for clean build
REM Note: You can keep the .spec file if you want to customize PyInstaller settings
if exist "견적서변환기.spec" (
    del "견적서변환기.spec"
)

echo.
echo EXE 파일 생성 중... (시간이 걸릴 수 있습니다)
echo.

REM Build the EXE
pyinstaller --onefile --windowed --name="견적서변환기" converter_gui.py

if errorlevel 1 (
    echo.
    echo [오류] EXE 빌드에 실패했습니다.
    pause
    exit /b 1
)

echo.
echo =====================================
echo    빌드 완료!
echo =====================================
echo.
echo 생성된 EXE 파일: dist\견적서변환기.exe
echo.
echo 이 파일을 바탕화면에 복사하여 사용하세요!
echo.
pause
