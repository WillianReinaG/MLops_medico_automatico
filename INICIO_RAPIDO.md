# ⚡ INICIO RÁPIDO: PRUEBAS EN PRODUCCIÓN

## Opción Más Rápida (5 minutos)

### 1. Abrir Navegador
```
http://localhost
```

### 2. Llenar Formulario
- Click en "Nuevo Paciente"
- Completar datos personales, vitales, historial
- Agregar síntomas (click "Agregar síntoma" múltiples veces)
- Click "Solicitar Diagnóstico"

### 3. Ver Resultado
- Sistema muestra diagnóstico con confiabilidad
- Si < 84%: Ver pruebas recomendadas
- Click "Descargar Reporte PDF"

### 4. Verificar Historial
- Click en pestaña "Historial"
- Ingresar cédula
- Click "Cargar Historial"
- Ver diagósticos previos con opciones de descarga y recarga

---

## Opción Automática (3 minutos)

### 1. Abrir Terminal PowerShell

### 2. Ejecutar Pruebas
```powershell
cd C:\Users\bebes\MLops_medico_automatico
python test_produccion.py
```

### 3. Ver Resultado
El script mostrará:
- ✓ Tests que pasaron
- ✗ Tests que fallaron
- Porcentaje de éxito final

**Resultado esperado: > 80% de éxito**

---

## Opción Manual con Curl (10 minutos)

### 1. Verificar API está activa
```powershell
curl http://localhost:5000/api/health
```

### 2. Crear Paciente
```powershell
$body = @{
    cedula = "1111111111"
    name = "Test Usuario"
    age = 40
    gender = "M"
    email = "test@ejemplo.com"
    phone = "555-1234"
    weight = 75.0
    height = 180
    blood_pressure_systolic = 120
    blood_pressure_diastolic = 80
    temperature = 37.0
    previous_diseases = "Ninguna"
    surgeries = "Ninguna"
    allergies = "Ninguna"
    medications = "Ninguno"
    parents_health = "Sanos"
    diet = "Balanceada"
    exercise = "Moderado"
    smokes = $false
    alcohol_consumption = "Ocasional"
} | ConvertTo-Json

curl -X POST http://localhost:5000/api/patients `
  -H "Content-Type: application/json" `
  -d $body
```

### 3. Realizar Diagnóstico
```powershell
$diagBody = @{
    patient_cedula = "1111111111"
    symptoms = "Fiebre y tos"
    symptoms_detail = @(
        @{symptom = "Fiebre"; intensity = "Moderada"; days = 3},
        @{symptom = "Tos"; intensity = "Moderada"; days = 3}
    )
} | ConvertTo-Json

curl -X POST http://localhost:5000/api/diagnose `
  -H "Content-Type: application/json" `
  -d $diagBody
```

### 4. Descargar PDF
```powershell
# Usar el diagnosis_id de la respuesta anterior
curl -X GET http://localhost:5000/api/diagnoses/1/report `
  -o "reporte.pdf"
```

---

## Estado Actual del Sistema

✓ **API**: http://localhost:5000 (funcionando)  
✓ **Frontend**: http://localhost (funcionando)  
✓ **Base de Datos**: PostgreSQL (funcionando)  
✓ **Modelo ML**: Cargado y funcionando  
✓ **PDFs**: Generándose correctamente  

---

## Próximos Pasos

1. **Elige una opción arriba** (Web es más rápido)
2. **Ejecuta las pruebas**
3. **Verifica los resultados**
4. **Si todo OK**: Sistema listo para producción ✅

---

## Documentación Completa

Para guía detallada:
📖 [Ver GUIA_PRUEBAS_PRODUCCION.md](GUIA_PRUEBAS_PRODUCCION.md)

Para ver estado del sistema:
📊 [Ver PROYECTO_COMPLETO.md](PROYECTO_COMPLETO.md)

---

## ¿Necesitas Ayuda?

### Problema: API no responde
```powershell
docker restart medical_api
docker logs medical_api
```

### Problema: Base de datos no conecta
```powershell
docker restart medical_db
```

### Problema: PDFs no se descargan
```powershell
docker logs medical_api | findstr "PDF"
```

### Limpiar todo y empezar de nuevo
```powershell
docker-compose down -v
docker-compose up -d
```

---

**¡Listo! Ahora puedes hacer pruebas en producción. Elige tu opción favorita arriba y comienza. 🚀**

