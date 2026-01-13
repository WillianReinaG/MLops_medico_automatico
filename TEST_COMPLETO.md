# Prueba Completa del Sistema Médico MLOps

## Estado del Sistema ✅

### Servicios Activos
- ✅ PostgreSQL 15 (puerto 5432)
- ✅ Flask API (puerto 5000)
- ✅ Nginx (puerto 80/443)
- ✅ ML Trainer (modelo cargado)

### Características Implementadas
- ✅ Gestión completa de pacientes con cédula como ID
- ✅ Recopilación extensiva de datos médicos:
  - Datos vitales (peso, altura, presión arterial, temperatura)
  - Historial médico (enfermedades, cirugías, alergias, medicamentos)
  - Salud familiar
  - Estilos de vida (dieta, ejercicio, consumo de alcohol, tabaco)
- ✅ Diagnóstico automático con confiabilidad en porcentaje
- ✅ Lógica inteligente: Si confiabilidad < 84%:
  - Crear recomendaciones de pruebas (Análisis de sangre, Radiografía, Ecografía)
  - Programar cita de seguimiento en 7 días
  - Mostrar pruebas recomendadas al paciente
- ✅ Generación de reportes PDF con:
  - Información completa del paciente
  - Datos vitales
  - Diagnóstico con confiabilidad
  - Medicamentos recomendados
  - Pruebas de apoyo recomendadas
  - Antecedentes médicos
- ✅ Descarga automática de PDF al agendar pruebas

## Flujo de Prueba Recomendado

### 1. Crear Nuevo Paciente
```bash
curl -X POST http://localhost:5000/api/patients \
  -H "Content-Type: application/json" \
  -d '{
    "cedula": "1234567890",
    "name": "Juan Pérez",
    "age": 35,
    "gender": "M",
    "email": "juan@example.com",
    "phone": "1234567890",
    "weight": 75.5,
    "height": 180,
    "blood_pressure_systolic": 130,
    "blood_pressure_diastolic": 85,
    "temperature": 37.2,
    "previous_diseases": "Hipertensión",
    "surgeries": "Ninguna",
    "allergies": "Penicilina",
    "medications": "Enalapril",
    "parents_health": "Padre diabético",
    "diet": "Balanceada",
    "exercise": "Moderado",
    "smokes": false,
    "alcohol_consumption": "Ocasional"
  }'
```

### 2. Realizar Diagnóstico con Síntomas
```bash
curl -X POST http://localhost:5000/api/patients/1234567890/diagnose \
  -H "Content-Type: application/json" \
  -d '{
    "symptoms": "Dolor de cabeza, fiebre",
    "symptoms_detail": [
      {
        "symptom": "Dolor de cabeza",
        "intensity": "Moderado",
        "days": 3
      },
      {
        "symptom": "Fiebre",
        "intensity": "Leve",
        "days": 2
      }
    ]
  }'
```

### 3. Si Confiabilidad < 84%:
- Sistema automáticamente crea pruebas recomendadas
- Sistema automáticamente programa cita en 7 días
- Respuesta incluye `recommended_tests` y `appointment_scheduled`

### 4. Descargar Reporte PDF
```bash
curl -X GET http://localhost:5000/api/diagnoses/{diagnosis_id}/report \
  -H "Accept: application/pdf" \
  -o "reporte_medico.pdf"
```

## Prueba en Interfaz Web

1. Abrir http://localhost
2. Llenar formulario "Registro de Nuevo Paciente":
   - Información Personal
   - Signos Vitales
   - Historial Médico
   - Salud Familiar
   - Estilos de Vida
3. Agregar síntomas dinámicamente con intensidad y duración
4. Ver diagnóstico
5. Si hay recomendaciones de pruebas: Click "Agendar Pruebas"
6. Descargar PDF automáticamente

## Base de Datos

### Tablas Creadas
- `patient` - Información del paciente (20+ campos)
- `diagnosis` - Diagnósticos realizados
- `medical_test` - Pruebas recomendadas
- `appointment` - Citas de seguimiento
- `medical_exam` - Exámenes históricos

## Archivos Principales

| Archivo | Cambios |
|---------|---------|
| [backend/app.py](backend/app.py) | +200 líneas: Modelos extendidos, lógica de confianza, PDF generation |
| [frontend/index.html](frontend/index.html) | +100 líneas: Formulario multi-sección, campos dinámicos |
| [backend/requirements.txt](backend/requirements.txt) | Agregado: reportlab, pypdf |
| [docker-compose.yml](docker-compose.yml) | Sin cambios (compatible) |

## Próximos Pasos Opcionales

- [ ] Implementar autenticación JWT
- [ ] Agregar generación de certificado de incapacidad
- [ ] Dashboard de estadísticas de diagnósticos
- [ ] Notificaciones por email para citas
- [ ] Integración con servicios de laboratorio

## Notas Técnicas

- Base de datos se resetea al hacer `docker-compose down -v`
- Los logs están disponibles con `docker logs medical_api`
- El modelo ML se entrena automáticamente al iniciar el contenedor ml_trainer
- Reportlab genera PDFs profesionales con tablas y estilos
- Frontend usa HTML5 vanilla sin dependencias externas

