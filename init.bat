@echo off
REM Script de inicialización para Windows

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║   Inicializador de MLOps Medical Diagnosis System          ║
echo ║   Sistema de Diagnóstico Médico con Machine Learning      ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Crear directorios
echo 📁 Creando directorios...
if not exist "ml_model\models" mkdir ml_model\models
if not exist "logs" mkdir logs
if not exist "data" mkdir data
echo ✓ Directorios creados

REM Crear .env si no existe
if not exist ".env" (
    echo 🔐 Creando archivo .env...
    copy .env.example .env
    echo ✓ Archivo .env creado
) else (
    echo ⚠ .env ya existe
)

echo.
echo ==========================================
echo Opciones de inicialización:
echo ==========================================
echo 1. Docker Compose (recomendado)
echo 2. Instalación local
echo 3. Solo crear estructura
echo.

set /p choice="Selecciona una opción (1-3): "

if "%choice%"=="1" (
    echo 🐳 Iniciando Docker Compose...
    docker-compose up -d
    if %ERRORLEVEL% EQU 0 (
        echo ✓ ¡Servicios iniciados!
        echo.
        echo Accesos:
        echo   • API: http://localhost:5000
        echo   • Frontend: http://localhost:80
        echo   • pgAdmin: http://localhost:5050
        echo.
        echo Ver logs:
        echo   docker-compose logs -f
    )
) else if "%choice%"=="2" (
    echo 🐍 Instalación local...
    python -m venv venv
    call venv\Scripts\activate.bat
    pip install -r backend\requirements.txt
    pip install -r ml_model\requirements.txt
    echo.
    echo Pasos siguientes:
    echo   1. venv\Scripts\activate.bat
    echo   2. cd ml_model && python train_model.py
    echo   3. cd backend && python app.py
) else if "%choice%"=="3" (
    echo ✓ Estructura del proyecto lista
) else (
    echo Opción inválida
    exit /b 1
)

echo.
echo ==========================================
echo ✓ Inicialización completada
echo ==========================================
echo.
echo Documentación: Consulta README.md para más detalles
echo.
