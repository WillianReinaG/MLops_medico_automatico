.PHONY: help install build up down logs test clean train-model init

help:
	@echo "╔════════════════════════════════════════════════════════════╗"
	@echo "║   MLOps Medical Diagnosis System - Comandos Disponibles    ║"
	@echo "╚════════════════════════════════════════════════════════════╝"
	@echo ""
	@echo "Instalación:"
	@echo "  make init          - Inicializar proyecto"
	@echo "  make install       - Instalar dependencias locales"
	@echo ""
	@echo "Docker:"
	@echo "  make build         - Construir imágenes Docker"
	@echo "  make up            - Iniciar servicios (Docker Compose)"
	@echo "  make down          - Detener servicios"
	@echo "  make logs          - Ver logs en tiempo real"
	@echo "  make logs-backend  - Ver logs del backend"
	@echo "  make logs-db       - Ver logs de la base de datos"
	@echo ""
	@echo "Base de Datos:"
	@echo "  make db-create     - Crear tablas"
	@echo "  make db-drop       - Eliminar tablas"
	@echo "  make db-seed       - Cargar datos de prueba"
	@echo "  make db-reset      - Resetear BD completamente"
	@echo ""
	@echo "ML Model:"
	@echo "  make train-model   - Entrenar modelo ML"
	@echo "  make train-docker  - Entrenar modelo en Docker"
	@echo ""
	@echo "Testing:"
	@echo "  make test          - Ejecutar tests"
	@echo "  make test-ml       - Tests del modelo ML"
	@echo "  make test-api      - Tests de la API"
	@echo "  make coverage      - Generar reporte de cobertura"
	@echo ""
	@echo "Desarrollo:"
	@echo "  make shell         - Acceder a shell del backend"
	@echo "  make shell-db      - Acceder a psql de la BD"
	@echo "  make clean         - Limpiar archivos temporales"
	@echo "  make lint          - Ejecutar linter"
	@echo ""

init:
	@echo "Inicializando proyecto..."
	@python init.py

install:
	@echo "Instalando dependencias..."
	pip install -r backend/requirements.txt
	pip install -r ml_model/requirements.txt
	pip install pytest pytest-cov pytest-flask

build:
	@echo "Construyendo imágenes Docker..."
	docker-compose build --no-cache

up:
	@echo "Iniciando servicios..."
	docker-compose up -d
	@echo ""
	@echo "✓ Servicios iniciados:"
	@echo "  • API: http://localhost:5000"
	@echo "  • Frontend: http://localhost:80"
	@echo "  • pgAdmin: http://localhost:5050"
	@echo "  • Base de datos: localhost:5432"

down:
	@echo "Deteniendo servicios..."
	docker-compose down

restart:
	@echo "Reiniciando servicios..."
	docker-compose restart

logs:
	docker-compose logs -f

logs-backend:
	docker-compose logs -f backend

logs-db:
	docker-compose logs -f db

logs-nginx:
	docker-compose logs -f nginx

db-create:
	docker-compose exec backend python manage_db.py create

db-drop:
	docker-compose exec backend python manage_db.py drop

db-seed:
	docker-compose exec backend python manage_db.py seed

db-reset:
	docker-compose exec backend python manage_db.py reset

train-model:
	@echo "Entrenando modelo ML..."
	cd ml_model && python train_model.py

train-docker:
	@echo "Entrenando modelo en Docker..."
	docker-compose up ml_trainer

test:
	@echo "Ejecutando tests..."
	pytest tests/ -v --cov=backend --cov=ml_model

test-ml:
	@echo "Ejecutando tests del modelo..."
	pytest tests/test_ml_model.py -v

test-api:
	@echo "Ejecutando tests de la API..."
	pytest tests/test_api.py -v

coverage:
	@echo "Generando reporte de cobertura..."
	pytest tests/ --cov=backend --cov=ml_model --cov-report=html
	@echo "Reporte disponible en htmlcov/index.html"

shell:
	docker-compose exec backend /bin/bash

shell-db:
	docker-compose exec db psql -U admin -d medical_db

lint:
	@echo "Ejecutando linter..."
	pylint backend/*.py ml_model/*.py tests/*.py 2>/dev/null || true

format:
	@echo "Formateando código..."
	black backend/ ml_model/ tests/ --line-length 100

clean:
	@echo "Limpiando archivos temporales..."
	find . -type d -name __pycache__ -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.log" -delete
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
	@echo "✓ Limpieza completada"

status:
	@echo "Estado de los servicios:"
	docker-compose ps

pull:
	@echo "Actualizando imágenes base..."
	docker-compose pull

ps:
	docker-compose ps

# Variables por defecto
.DEFAULT_GOAL := help
