# Configuración del Copilot

Este archivo proporciona instrucciones personalizadas para el GitHub Copilot y otros asistentes de IA en este proyecto de MLOps Medical.

## Contexto del Proyecto

Este es un sistema de diagnóstico médico basado en ML que incluye:
- API REST con Flask para predicción de enfermedades
- Modelo RandomForest entrenado con síntomas
- Base de datos PostgreSQL para gestión de pacientes
- Docker para deployment
- Tests automáticos con GitHub Actions
- Frontend HTML/JS para interfaz de usuario

## Convenciones de Código

### Python
- PEP 8 compliant
- Type hints cuando sea posible
- Docstrings en todas las funciones
- Tests para cada módulo nuevo

### Estructura de Respuestas API
```json
{
  "status": "success",
  "data": {},
  "message": "Descripción",
  "timestamp": "ISO 8601"
}
```

### Nombres de Funciones
- Nombres descriptivos en inglés para funciones internas
- Nombres en español para mensajes y textos de usuario
- Prefijo `test_` para funciones de testing

## Patrones Comunes

### Manejo de Errores
- Siempre retornar status HTTP apropiado
- Incluir mensaje de error descriptivo
- Loguear errores en nivel WARNING o ERROR

### Autenticación (futuro)
- Usar JWT tokens
- Incluir en header `Authorization: Bearer {token}`

### Validación de Entrada
- Validar tipo de dato
- Validar rango de valores
- Sanitizar strings

## Dependencias del Proyecto

### Backend
- Flask 3.0.0
- SQLAlchemy para ORM
- scikit-learn para ML
- psycopg2 para PostgreSQL

### Frontend
- HTML5 vanilla (sin frameworks)
- Fetch API para llamadas HTTP
- CSS Grid para layouts

## Estructura de Base de Datos

- `patients`: Información de pacientes
- `diagnoses`: Diagnósticos realizados
- `medical_exams`: Exámenes solicitados

## Archivos Importantes

- `backend/app.py`: Aplicación principal Flask
- `ml_model/train_model.py`: Entrenamiento del modelo
- `frontend/index.html`: Interfaz de usuario
- `docker-compose.yml`: Orquestación de servicios
- `.github/workflows/ci-cd.yml`: Pipeline de CI/CD

## Notas para Asistentes de IA

- Los modelos se guardan en `ml_model/models/`
- La BD se resetea cada vez que se ejecuta docker-compose down/up
- Usar variables de entorno para configuración sensible
- Los logs están disponibles con `docker-compose logs`
- El frontend está servido por Nginx en el puerto 80

---

Última actualización: 12 de enero de 2026
