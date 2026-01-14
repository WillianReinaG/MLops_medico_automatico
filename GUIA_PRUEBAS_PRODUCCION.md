# 🚀 GUÍA COMPLETA: PRUEBAS EN PRODUCCIÓN

## Estado Actual del Sistema

```
✓ Base de datos (PostgreSQL 15) corriendo
✓ API REST (Flask + Gunicorn) corriendo  
✓ Frontend (Nginx) corriendo
✓ ML Model cargado y funcionando
✓ Todos los endpoints implementados
```

---

## OPCIÓN 1: Pruebas Automáticas (Recomendado)

### Paso 1: Ejecutar el Script de Pruebas

```bash
# Navegar al directorio
cd C:\Users\bebes\MLops_medico_automatico

# Ejecutar pruebas automáticas
python test_produccion.py
```

**Qué hace este script:**
- ✓ Verifica que la API esté saludable
- ✓ Crea un paciente de prueba
- ✓ Obtiene información del paciente
- ✓ Lista todos los pacientes
- ✓ Realiza un diagnóstico completo
- ✓ Obtiene historial de diagnósticos
- ✓ Genera reporte PDF
- ✓ Crea órdenes de examen
- ✓ Obtiene exámenes del paciente
- ✓ Proporciona resumen de resultados

**Resultado esperado:**
```
[✓ PASÓ] API Health Check
[✓ PASÓ] Crear paciente
[✓ PASÓ] Obtener paciente
[✓ PASÓ] Listar pacientes
[✓ PASÓ] Realizar diagnóstico
[✓ PASÓ] Obtener diagnósticos
[✓ PASÓ] Generar reporte PDF
[✓ PASÓ] Crear examen
[✓ PASÓ] Obtener exámenes

Porcentaje éxito: 100.0%
✓ ¡TODAS LAS PRUEBAS PASARON!
```

---

## OPCIÓN 2: Pruebas Manuales (Paso a Paso)

### 2.1 - Verificar que la API está activa

```bash
# Opción A: Curl
curl http://localhost:5000/api/health

# Opción B: PowerShell
Invoke-WebRequest http://localhost:5000/api/health
```

**Respuesta esperada:**
```json
{
  "status": "healthy",
  "timestamp": "2026-01-13T05:56:34.463842",
  "model_loaded": true
}
```

### 2.2 - Crear un paciente de prueba

```bash
curl -X POST http://localhost:5000/api/patients \
  -H "Content-Type: application/json" \
  -d '{
    "cedula": "1234567890",
    "name": "Juan Test",
    "age": 35,
    "gender": "M",
    "email": "juan@test.com",
    "phone": "555-1234",
    "weight": 75.0,
    "height": 180,
    "blood_pressure_systolic": 120,
    "blood_pressure_diastolic": 80,
    "temperature": 37.0,
    "previous_diseases": "Ninguna",
    "surgeries": "Ninguna",
    "allergies": "Ninguna",
    "medications": "Ninguno",
    "parents_health": "Sin problemas",
    "diet": "Balanceada",
    "exercise": "Moderado",
    "smokes": false,
    "alcohol_consumption": "Ocasional"
  }'
```

**Respuesta esperada:**
```json
{
  "status": "success",
  "cedula": "1234567890",
  "name": "Juan Test",
  "message": "Paciente creado exitosamente"
}
```

### 2.3 - Realizar un diagnóstico

```bash
curl -X POST http://localhost:5000/api/diagnose \
  -H "Content-Type: application/json" \
  -d '{
    "patient_cedula": "1234567890",
    "symptoms": "Fiebre, tos, cansancio",
    "symptoms_detail": [
      {"symptom": "Fiebre", "intensity": "Moderada", "days": 3},
      {"symptom": "Tos", "intensity": "Moderada", "days": 3},
      {"symptom": "Cansancio", "intensity": "Leve", "days": 2}
    ]
  }'
```

**Respuesta esperada:**
```json
{
  "diagnosis_id": 1,
  "patient_cedula": "1234567890",
  "predicted_disease": "Bronquitis aguda",
  "confidence": 85.5,
  "severity": "Moderada",
  "medications": ["Antibióticos", "Expectorantes"],
  "message": "Diagnóstico completado"
}
```

### 2.4 - Descargar reporte PDF

```bash
# Usar el diagnosis_id de la respuesta anterior
curl -X GET http://localhost:5000/api/diagnoses/1/report \
  -o "reporte_medico.pdf"
```

**Resultado:** Se descargará un archivo PDF profesional con toda la información.

### 2.5 - Obtener historial de diagnósticos

```bash
curl http://localhost:5000/api/patients/1234567890/diagnoses
```

**Respuesta esperada:**
```json
[
  {
    "diagnosis_id": 1,
    "patient_cedula": "1234567890",
    "predicted_disease": "Bronquitis aguda",
    "confidence": 85.5,
    "severity": "Moderada",
    "created_at": "2026-01-13T10:30:00"
  }
]
```

---

## OPCIÓN 3: Pruebas desde el Frontend Web

### Paso 1: Abrir la interfaz web

```
http://localhost
```

### Paso 2: Realizar flujo completo

1. **Seleccionar "Nuevo Paciente"**
   - Llenar todos los campos (información personal, vitales, historial médico, estilos de vida)
   - Hacer click en "Siguiente"

2. **Ingresar síntomas**
   - Agregar múltiples síntomas
   - Indicar intensidad y duración
   - Hacer click en "Solicitar Diagnóstico"

3. **Ver resultado**
   - Sistema muestra diagnóstico con confiabilidad
   - Si confiabilidad < 84%: muestra pruebas recomendadas
   - Hacer click en "Descargar Reporte PDF"

4. **Recargar diagnóstico**
   - Ir a pestaña "Historial"
   - Ingresar cédula
   - Buscar diagnóstico anterior
   - Hacer click en "Recargar Detalles" o "Descargar Reporte"

---

## VERIFICACIÓN DE SALUD DEL SISTEMA

### 1. Ver estado de servicios Docker

```bash
docker ps
```

**Resultado esperado:**
```
NAMES           STATUS         PORTS
medical_nginx   Up 21 hours    0.0.0.0:80->80/tcp, 0.0.0.0:443->443/tcp
medical_api     Up 21 hours    0.0.0.0:5000->5000/tcp
medical_db      Up 21 hours    0.0.0.0:5432->5432/tcp
```

### 2. Ver logs de la API

```bash
# Últimos 50 líneas
docker logs medical_api | tail -50

# O en PowerShell:
docker logs medical_api | Select-Object -Last 50
```

**Qué buscar:**
- ✓ "Modelo ML cargado exitosamente"
- ✓ "Tablas de BD creadas"
- ✓ "Gunicorn listening at http://0.0.0.0:5000"
- ✗ "Error" o "Exception"

### 3. Ver logs de base de datos

```bash
docker logs medical_db | tail -20
```

**Qué buscar:**
- ✓ "database system is ready to accept connections"
- ✓ Sin errores de conexión

---

## MÉTRICAS DE PERFORMANCE

### Pruebas de carga

```bash
# Instalar herramienta de pruebas (si no la tienes)
pip install locust

# Crear archivo locustfile.py (ver ejemplo abajo)
# Ejecutar prueba
locust -f locustfile.py --host=http://localhost:5000
```

### Comprobar tiempo de respuesta

```python
import requests
import time

start = time.time()
response = requests.get("http://localhost:5000/api/health")
elapsed = time.time() - start

print(f"Tiempo de respuesta: {elapsed*1000:.2f}ms")
# Resultado esperado: < 100ms
```

---

## CHECKLIST PRE-PRODUCCIÓN

### Base de Datos
- [ ] PostgreSQL está corriendo
- [ ] Conexión a BD funciona
- [ ] Todas las tablas creadas
- [ ] Datos persisten correctamente
- [ ] Backups configurados (si aplica)

### API
- [ ] Todos los endpoints responden
- [ ] Validación de entrada funciona
- [ ] Manejo de errores correcto
- [ ] Timeouts configurados
- [ ] Rate limiting implementado (si aplica)

### Frontend
- [ ] Formularios funcionan correctamente
- [ ] Validación de entrada en cliente
- [ ] PDFs se descargan correctamente
- [ ] Historial carga correctamente
- [ ] Responsive design funciona

### Machine Learning
- [ ] Modelo cargado correctamente
- [ ] Predicciones tienen sentido
- [ ] Confiabilidad se calcula correctamente
- [ ] Pruebas recomendadas cuando < 84%

### Seguridad
- [ ] No hay credenciales en código
- [ ] Variables de entorno configuradas
- [ ] CORS habilitado solo para dominios permitidos
- [ ] HTTPS configurado (si aplica)

### Documentación
- [ ] README actualizado
- [ ] Endpoints documentados
- [ ] Estructura de BD documentada
- [ ] Instrucciones de deployment claras

---

## SOLUCIÓN DE PROBLEMAS

### Problema: API no responde

**Solución:**
```bash
# 1. Verificar que Docker está corriendo
docker ps

# 2. Reiniciar API
docker restart medical_api

# 3. Ver logs de error
docker logs medical_api

# 4. Si sigue fallando, reconstruir
docker-compose down -v
docker-compose up -d --build
```

### Problema: Base de datos no conecta

**Solución:**
```bash
# 1. Verificar BD está activa
docker ps | grep medical_db

# 2. Verificar conexión
docker exec medical_db psql -U postgres -c "SELECT 1"

# 3. Si no funciona, restaurar volumen
docker-compose down -v
docker-compose up -d
```

### Problema: PDF no se descarga

**Solución:**
```bash
# 1. Verificar endpoint
curl -X GET http://localhost:5000/api/diagnoses/1/report

# 2. Verificar content-type en respuesta (debe ser application/pdf)

# 3. Ver logs
docker logs medical_api | grep "PDF"

# 4. Reiniciar API si necesario
docker restart medical_api
```

### Problema: Diagnóstico no tiene confiabilidad < 84%

**Solución:**
```
1. Esto es normal - depende del modelo ML
2. El sistema está diseñado para ambas situaciones
3. Prueba con síntomas diferentes para obtener otro resultado
```

---

## FLUJO DE PRUEBA RECOMENDADO

### Semana 1: Pruebas Básicas
1. Ejecutar `test_produccion.py`
2. Verificar que todos los tests pasen
3. Revisar logs para errores

### Semana 2: Pruebas Funcionales
1. Crear múltiples pacientes
2. Realizar diagnósticos variados
3. Verificar PDFs se generan correctamente
4. Probar historial y recarga de diagnósticos

### Semana 3: Pruebas de Carga
1. Realizar 100 diagnósticos simultáneamente
2. Verificar performance del sistema
3. Monitorear uso de recursos (CPU, memoria)

### Semana 4: Pruebas de Seguridad
1. Intentar inyección SQL (debería fallar)
2. Verificar validación de entrada
3. Probar límites de permisos

---

## REFERENCIAS

| Componente | URL | Descripción |
|-----------|-----|------------|
| Frontend | http://localhost | Interfaz web de usuario |
| API | http://localhost:5000 | Servidor REST |
| Health Check | http://localhost:5000/api/health | Estado del sistema |
| pgAdmin | http://localhost:5050 | Administración BD (usuario: admin@admin.com) |

## Comandos Útiles

```bash
# Ver estado
docker ps

# Ver logs en vivo
docker logs -f medical_api

# Entrar en contenedor
docker exec -it medical_api bash

# Conectar a BD
docker exec -it medical_db psql -U postgres

# Reiniciar todo
docker-compose restart

# Limpiar y reconstruir
docker-compose down -v && docker-compose up -d --build
```

---

## ✅ Sistema Listo para Producción

Cuando todos los tests pasen y hayas completado el checklist, el sistema estará **100% listo para producción**.

**Estado actual: 🟢 LISTO**

