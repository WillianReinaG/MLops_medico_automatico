# USAGE.md - Guía de Uso del Sistema

## 📋 Tabla de Contenidos
1. [Inicio Rápido](#inicio-rápido)
2. [Para Usuarios](#para-usuarios)
3. [Para Desarrolladores](#para-desarrolladores)
4. [Para Administradores](#para-administradores)
5. [Ejemplos de Uso](#ejemplos-de-uso)

---

## Inicio Rápido

### 1. Iniciando la Aplicación

#### Con Docker (Recomendado)
```bash
docker-compose up -d
```

#### Sin Docker
```bash
# Terminal 1: Base de datos (requiere PostgreSQL instalado)
# O usar versión local

# Terminal 2: Entrenar modelo
cd ml_model
python train_model.py

# Terminal 3: Ejecutar API
cd backend
python app.py

# Terminal 4: Servir frontend
# Abrir frontend/index.html en navegador
```

### 2. Verificar que todo funciona
```bash
# Revisar servicios
docker-compose ps

# Verificar API
curl http://localhost:5000/health

# Acceder a frontend
# Navegador: http://localhost:80
```

---

## Para Usuarios

### Acceder a la Aplicación

1. **Abrir navegador**: http://localhost:80
2. **Ver interfaz moderna y responsiva**
3. **Seleccionar tipo de usuario**

### Flujo de Nuevo Paciente

```
1. Seleccionar "Nuevo Paciente"
2. Completar datos:
   - Nombre completo
   - Edad
   - Género
   - Email
   - Teléfono (opcional)
   - Historial médico (opcional)
3. Describir síntomas
4. Clic en "Solicitar Diagnóstico"
```

### Interpretar Resultados

#### Diagnóstico Claro
```
✓ Confianza: >85%
✓ Se genera automáticamente:
  - Dicta médica
  - Medicamentos recomendados
  - Instrucciones de seguimiento
```

#### Diagnóstico Requiere Confirmación
```
⚠ Confianza: 60-85%
⚠ Requiere:
  - Solicitud de examen médico
  - Cita con médico
  - Tests adicionales
```

### Ver Historial Médico

```
1. Tab: "Historial de Paciente"
2. Ingresar ID de paciente
3. Clic: "Cargar Historial"
4. Ver lista de diagnósticos previos con:
   - Fecha
   - Enfermedad
   - Confianza
   - Severidad
```

### Ver Exámenes Solicitados

```
1. Tab: "Mis Exámenes"
2. Ingresar ID de paciente
3. Ver estado de exámenes:
   - Pendiente (azul)
   - Programado (naranja)
   - Completado (verde)
4. Programar cita si es necesario
```

---

## Para Desarrolladores

### Configuración del Entorno Local

```bash
# 1. Clonar repo
git clone https://github.com/tu-usuario/MLops_medico_automatico.git

# 2. Crear venv
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate  # Windows

# 3. Instalar dependencias
pip install -r backend/requirements.txt
pip install -r ml_model/requirements.txt
pip install pytest pytest-cov

# 4. Entrenar modelo
cd ml_model && python train_model.py && cd ..

# 5. Correr API
cd backend && python app.py
```

### Estructura de Carpetas Importante

```
backend/
├── app.py              # Aplicación principal (Flask)
├── config.py          # Configuraciones
├── manage_db.py       # Gestión de BD
├── utils.py           # Funciones auxiliares
└── requirements.txt   # Dependencias

ml_model/
├── train_model.py     # Script de entrenamiento
├── models/            # Modelos guardados
└── requirements.txt

tests/
├── test_api.py        # Tests de API
└── test_ml_model.py   # Tests de modelo
```

### Agregar Nueva Enfermedad

1. **Editar train_model.py**
```python
SYMPTOM_DISEASE_DATA = {
    'symptoms': [
        # ... síntomas existentes
        'nuevo síntoma 1 nuevo síntoma 2'  # Agregar aquí
    ],
    'disease': [
        # ... enfermedades existentes
        'Nueva Enfermedad'  # Agregar aquí
    ],
    'exam_needed': [
        # ...
        True  # o False
    ],
    'severity': [
        # ...
        'Leve|Moderada|Alta'
    ]
}

# Agregar medicamentos
MEDICATIONS['Nueva Enfermedad'] = [
    'Medicamento 1 dosis',
    'Medicamento 2 dosis'
]
```

2. **Reentrenar modelo**
```bash
cd ml_model
python train_model.py
```

3. **Reiniciar API**
```bash
docker-compose restart backend
# o
Ctrl+C en terminal y ejecutar python app.py
```

### Crear Nuevo Endpoint

```python
# En backend/app.py

@app.route('/api/mi-endpoint', methods=['POST'])
@require_patient_id  # Opcional: validar patient_id
def mi_endpoint():
    """Descripción del endpoint"""
    try:
        data = request.json
        
        # Lógica aquí
        
        return jsonify({
            'status': 'success',
            'data': resultado
        }), 200
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500
```

### Ejecutar Tests

```bash
# Todos los tests
pytest tests/ -v

# Solo tests de modelo
pytest tests/test_ml_model.py -v

# Solo tests de API
pytest tests/test_api.py -v

# Con cobertura
pytest tests/ --cov=backend --cov=ml_model

# Generar reporte HTML
pytest tests/ --cov=backend --cov-report=html
```

### Debugging

```bash
# Ver logs en tiempo real
docker-compose logs -f

# Logs de servicio específico
docker-compose logs -f backend

# Acceder a shell
docker-compose exec backend /bin/bash

# Ejecutar comando en contenedor
docker-compose exec backend python manage_db.py seed

# Conectar a BD
docker-compose exec db psql -U admin -d medical_db
```

### Commits y Pull Requests

```bash
# Crear rama para feature
git checkout -b feature/nueva-caracteristica

# Hacer cambios, tests, commits
git add .
git commit -m "Agregar nueva caracteristica"

# Push y crear PR
git push origin feature/nueva-caracteristica
```

---

## Para Administradores

### Gestión de Base de Datos

```bash
# Crear tablas
docker-compose exec backend python manage_db.py create

# Cargar datos de prueba
docker-compose exec backend python manage_db.py seed

# Resetear BD completamente
docker-compose exec backend python manage_db.py reset

# Conectar a BD directamente
docker-compose exec db psql -U admin -d medical_db

# Queries útiles en psql
\dt                          # Ver tablas
SELECT COUNT(*) FROM patients; # Contar pacientes
```

### Monitoreo de Servicios

```bash
# Ver estado de todos
docker-compose ps

# Ver recursos usados
docker stats

# Ver logs completos
docker-compose logs

# Ver logs desde hace X minutos
docker-compose logs --since 10m

# Logs con timestamps
docker-compose logs -t
```

### Mantenimiento

```bash
# Actualizar imágenes base
docker-compose pull

# Limpiar espacios sin usar
docker system prune -a

# Reconstruir imágenes
docker-compose build --no-cache

# Backup de BD
docker-compose exec db pg_dump -U admin medical_db > backup.sql

# Restaurar BD
docker-compose exec -T db psql -U admin medical_db < backup.sql
```

### Seguridad

```bash
# Cambiar contraseña de BD
# Editar .env y docker-compose.yml

# Generar nuevo SECRET_KEY
python -c "import secrets; print(secrets.token_hex(32))"

# Ver variables de entorno
docker-compose exec backend env | grep -E "DATABASE|FLASK"
```

### Escalabilidad

```bash
# Aumentar recursos en docker-compose.yml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '1'
          memory: 512M

# Aplicar cambios
docker-compose up -d
```

---

## Ejemplos de Uso

### Ejemplo 1: Crear Paciente e Iniciar Diagnóstico

```bash
# 1. Crear paciente
curl -X POST http://localhost:5000/api/patients \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Juan Pérez",
    "age": 35,
    "gender": "M",
    "email": "juan@example.com",
    "phone": "+34912345678"
  }'

# Respuesta:
# {"id": 1, "name": "Juan Pérez", ...}

# 2. Realizar diagnóstico
curl -X POST http://localhost:5000/api/diagnose \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": 1,
    "symptoms": "fiebre dolor cabeza cuerpo malestar general"
  }'

# 3. Obtener reporte
curl http://localhost:5000/api/diagnoses/1/report

# 4. Solicitar examen si es necesario
curl -X POST http://localhost:5000/api/exams \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": 1,
    "exam_type": "Análisis de sangre",
    "description": "Análisis completo solicitado"
  }'

# 5. Programar cita
curl -X PUT http://localhost:5000/api/exams/1/schedule \
  -H "Content-Type: application/json" \
  -d '{
    "appointment_date": "2026-01-20T10:30:00"
  }'
```

### Ejemplo 2: Consultar Historial Completo de Paciente

```bash
# Obtener info del paciente
curl http://localhost:5000/api/patients/1

# Historial de diagnósticos
curl http://localhost:5000/api/patients/1/diagnoses

# Exámenes solicitados
curl http://localhost:5000/api/patients/1/exams
```

### Ejemplo 3: Integración con Sistemas Externos

```python
# Python
import requests

API_URL = "http://localhost:5000"

# Crear paciente
patient_data = {
    "name": "María García",
    "age": 28,
    "email": "maria@example.com"
}
response = requests.post(f"{API_URL}/api/patients", json=patient_data)
patient_id = response.json()['id']

# Realizar diagnóstico
diag_data = {
    "patient_id": patient_id,
    "symptoms": "fiebre dolor garganta"
}
response = requests.post(f"{API_URL}/api/diagnose", json=diag_data)
diagnosis = response.json()

print(f"Diagnóstico: {diagnosis['predicted_disease']}")
print(f"Confianza: {diagnosis['confidence']}%")
print(f"Requiere examen: {diagnosis['requires_exam']}")
```

---

## 🔗 Enlaces Útiles

- [API Documentation](#) - Especificación OpenAPI
- [GitHub Repo](https://github.com) - Código fuente
- [Issues](https://github.com/issues) - Reportar problemas
- [Discussions](https://github.com/discussions) - Preguntas y sugerencias

---

## 📞 Soporte

- 💬 Issues de GitHub
- 📧 Email: support@example.com
- 💁 Documentación: README.md
- 🚀 Deployment: DEPLOYMENT.md

---

**Última actualización**: 12 de enero de 2026
