# MLOps Medical Diagnosis System

Sistema automático de diagnóstico médico basado en inteligencia artificial, con capacidad de predicción de enfermedades, solicitud de exámenes y generación de reportes médicos.

## 🎯 Características Principales

- **Diagnóstico Inteligente**: Modelo ML basado en RandomForest que predice enfermedades a partir de síntomas
- **API REST**: Backend Flask con endpoints para gestión de pacientes, diagnósticos y exámenes
- **Base de Datos**: PostgreSQL para almacenamiento persistente de historiales médicos
- **Docker**: Containerización completa para deployment en cualquier entorno
- **Frontend Web**: Interfaz intuitiva para pacientes y médicos
- **CI/CD**: GitHub Actions para testing automático y deployment
- **Escalabilidad**: Diseño preparado para múltiples instancias y load balancing

## 🏗️ Arquitectura del Proyecto

```
MLops_medico_automatico/
├── backend/                  # API REST con Flask
│   ├── app.py               # Aplicación principal
│   └── requirements.txt      # Dependencias Python
├── ml_model/                # Modelos de Machine Learning
│   ├── train_model.py       # Script de entrenamiento
│   ├── models/              # Modelos guardados
│   └── requirements.txt      # Dependencias ML
├── frontend/                # Interfaz web
│   └── index.html           # Aplicación web HTML/JS
├── docker/                  # Configuración Docker
│   ├── Dockerfile.backend   # Imagen del backend
│   ├── Dockerfile.ml        # Imagen del modelo ML
│   └── init.sql             # Script inicialización BD
├── tests/                   # Tests automáticos
│   ├── test_api.py          # Tests de API
│   └── test_ml_model.py     # Tests del modelo
├── .github/workflows/       # GitHub Actions
│   └── ci-cd.yml            # Pipeline CI/CD
└── docker-compose.yml       # Orquestación de servicios
```

## 🚀 Inicio Rápido

### Requisitos Previos
- Docker y Docker Compose instalados
- Git
- 4GB RAM mínimo
- Puertos disponibles: 5000 (API), 5432 (BD), 5050 (pgAdmin)

### Instalación Local

1. **Clonar el repositorio**
```bash
git clone https://github.com/tu-usuario/MLops_medico_automatico.git
cd MLops_medico_automatico
```

2. **Configurar variables de entorno**
```bash
cp .env.example .env
# Editar .env si es necesario
```

3. **Iniciar con Docker Compose**
```bash
docker-compose up -d
```

4. **Acceder a la aplicación**
- Frontend: http://localhost:3000 (si está configurado)
- API: http://localhost:5000
- pgAdmin: http://localhost:5050

### Configuración Manual (sin Docker)

1. **Crear entorno virtual**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

2. **Instalar dependencias**
```bash
pip install -r backend/requirements.txt
pip install -r ml_model/requirements.txt
```

3. **Entrenar el modelo**
```bash
cd ml_model
python train_model.py
cd ..
```

4. **Ejecutar API**
```bash
cd backend
python app.py
```

## 📊 Endpoints de la API

### Pacientes
- `POST /api/patients` - Crear nuevo paciente
- `GET /api/patients` - Listar pacientes
- `GET /api/patients/{id}` - Obtener paciente específico

### Diagnósticos
- `POST /api/diagnose` - Realizar diagnóstico basado en síntomas
- `GET /api/patients/{id}/diagnoses` - Historial de diagnósticos
- `GET /api/diagnoses/{id}/report` - Generar reporte médico

### Exámenes
- `POST /api/exams` - Solicitar examen médico
- `GET /api/exams/{id}` - Obtener detalles del examen
- `PUT /api/exams/{id}/schedule` - Programar cita
- `GET /api/patients/{id}/exams` - Exámenes del paciente

### Salud
- `GET /health` - Verificar estado de la API

## 🧬 Modelo de Machine Learning

### Algoritmo
- **Tipo**: RandomForest Classifier
- **Vectorización**: TF-IDF para procesamiento de texto
- **Dataset**: 15 enfermedades comunes con síntomas asociados
- **Características**: 
  - Predicción de enfermedad
  - Cálculo de confianza
  - Recomendación de exámenes
  - Severidad de enfermedad

### Enfermedades Soportadas
1. Gripe/Influenza
2. Bronquitis
3. Neumonía
4. Faringitis
5. Gastroenteritis
6. Mareos/Vértigo
7. Hipertensión
8. Hipotensión
9. Dermatitis/Alergia
10. Artritis
11. Infección Viral
12. Resfriado Común
13. Asma
14. Otitis
15. Conjuntivitis

## 🐳 Comandos Docker Útiles

```bash
# Ver logs de todos los servicios
docker-compose logs -f

# Ver logs de un servicio específico
docker-compose logs -f backend

# Detener servicios
docker-compose down

# Reconstruir imágenes
docker-compose build --no-cache

# Ejecutar comando en contenedor
docker-compose exec backend python -c "..."

# Reiniciar un servicio
docker-compose restart backend
```

## 🧪 Testing

### Ejecutar tests locales
```bash
# Tests del modelo ML
pytest tests/test_ml_model.py -v

# Tests de la API
pytest tests/test_api.py -v

# Todos los tests con cobertura
pytest tests/ --cov=backend --cov=ml_model
```

### Tests automáticos en CI/CD
Los tests se ejecutan automáticamente en GitHub Actions cuando:
- Se realiza push a `main` o `develop`
- Se crea un Pull Request

## 📝 Ejemplo de Uso

### 1. Crear nuevo paciente
```bash
curl -X POST http://localhost:5000/api/patients \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Juan Pérez",
    "age": 35,
    "gender": "M",
    "email": "juan@example.com",
    "phone": "+34912345678"
  }'
```

### 2. Realizar diagnóstico
```bash
curl -X POST http://localhost:5000/api/diagnose \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": 1,
    "symptoms": "fiebre dolor cabeza cuerpo malestar"
  }'
```

### 3. Solicitar examen médico
```bash
curl -X POST http://localhost:5000/api/exams \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": 1,
    "exam_type": "Radiografía",
    "description": "Radiografía de pecho"
  }'
```

### 4. Programar cita
```bash
curl -X PUT http://localhost:5000/api/exams/1/schedule \
  -H "Content-Type: application/json" \
  -d '{
    "appointment_date": "2026-01-20T10:30:00"
  }'
```

## 🔐 Seguridad

- ✅ CORS configurado para acceso seguro
- ✅ Validación de entrada en todos los endpoints
- ✅ Base de datos con autenticación
- ✅ Variables sensibles en .env
- ✅ HTTPS listo (requiere certificados en producción)

### Recomendaciones para Producción
1. Cambiar credenciales de base de datos
2. Usar variables de entorno seguros
3. Activar HTTPS con certificados válidos
4. Implementar autenticación (JWT, OAuth)
5. Configurar WAF (Web Application Firewall)
6. Usar secretos de GitHub para CI/CD
7. Implementar rate limiting
8. Configurar backups automáticos

## 📈 Monitoreo y Logs

- Logs disponibles en `docker-compose logs`
- Healthcheck en `/health` para cada servicio
- Métricas de base de datos en pgAdmin (puerto 5050)

## 🛠️ Desarrollo

### Variables de entorno local
```bash
FLASK_ENV=development
FLASK_DEBUG=True
DATABASE_URL=postgresql://admin:password@localhost:5432/medical_db
```

### Agregar nuevas enfermedades

Editar `ml_model/train_model.py`:
```python
SYMPTOM_DISEASE_DATA = {
    'symptoms': [
        '...',
        'nuevos síntomas aquí'
    ],
    'disease': [
        '...',
        'Nueva Enfermedad'
    ],
    # ...
}
```

## 📦 Deployment

### Opciones de Deploy

1. **Docker Compose (Local/Servidor)**
```bash
docker-compose up -d
```

2. **Kubernetes**
```bash
kubectl apply -f k8s/
```

3. **Cloud (AWS/GCP/Azure)**
- Usar ECR/GCR/ACR para imágenes
- RDS/Cloud SQL para base de datos
- Lambda/Cloud Functions para escalabilidad

## 🤝 Contribuir

1. Fork el repositorio
2. Crear rama: `git checkout -b feature/nueva-feature`
3. Commit: `git commit -am 'Agregar nueva feature'`
4. Push: `git push origin feature/nueva-feature`
5. Pull Request

## 📄 Licencia

MIT License - Ver [LICENSE](LICENSE)

## 👥 Autor

- GitHub: [@tu-usuario](https://github.com/tu-usuario)

## 📞 Soporte

- Issues: [GitHub Issues](https://github.com/tu-usuario/MLops_medico_automatico/issues)
- Email: soporte@example.com

## 📚 Recursos Adicionales

- [Documentación Flask](https://flask.palletsprojects.com/)
- [Documentación scikit-learn](https://scikit-learn.org/)
- [Documentación PostgreSQL](https://www.postgresql.org/docs/)
- [Docker Documentation](https://docs.docker.com/)
- [GitHub Actions](https://docs.github.com/en/actions)

---

**Última actualización**: 12 de enero de 2026
