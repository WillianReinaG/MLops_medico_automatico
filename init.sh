#!/bin/bash

# Script de inicialización para sistemas Unix/Linux/Mac

echo "╔════════════════════════════════════════════════════════════╗"
echo "║   Inicializador de MLOps Medical Diagnosis System          ║"
echo "║   Sistema de Diagnóstico Médico con Machine Learning      ║"
echo "╚════════════════════════════════════════════════════════════╝"

# Crear directorios
echo "📁 Creando directorios..."
mkdir -p ml_model/models
mkdir -p logs
mkdir -p data
echo "✓ Directorios creados"

# Crear .env si no existe
if [ ! -f .env ]; then
    echo "🔐 Creando archivo .env..."
    cp .env.example .env
    echo "✓ Archivo .env creado"
else
    echo "⚠ .env ya existe"
fi

# Preguntar sobre método de instalación
echo ""
echo "=========================================="
echo "Opciones de inicialización:"
echo "=========================================="
echo "1. Docker Compose (recomendado)"
echo "2. Instalación local"
echo "3. Solo crear estructura"
echo ""

read -p "Selecciona una opción (1-3): " choice

case $choice in
    1)
        echo "🐳 Iniciando Docker Compose..."
        docker-compose up -d
        if [ $? -eq 0 ]; then
            echo "✓ ¡Servicios iniciados!"
            echo ""
            echo "Accesos:"
            echo "  • API: http://localhost:5000"
            echo "  • Frontend: http://localhost:80"
            echo "  • pgAdmin: http://localhost:5050"
            echo ""
            echo "Ver logs:"
            echo "  docker-compose logs -f"
        fi
        ;;
    2)
        echo "🐍 Instalación local..."
        python3 -m venv venv
        source venv/bin/activate
        pip install -r backend/requirements.txt
        pip install -r ml_model/requirements.txt
        echo ""
        echo "Pasos siguientes:"
        echo "  1. source venv/bin/activate"
        echo "  2. cd ml_model && python train_model.py"
        echo "  3. cd backend && python app.py"
        ;;
    3)
        echo "✓ Estructura del proyecto lista"
        ;;
    *)
        echo "Opción inválida"
        exit 1
        ;;
esac

echo ""
echo "=========================================="
echo "✓ Inicialización completada"
echo "=========================================="
echo ""
echo "Documentación: Consulta README.md para más detalles"
