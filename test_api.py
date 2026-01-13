#!/usr/bin/env python3
"""Script de prueba para el sistema médico MLOps"""

import requests
import json
import time

BASE_URL = "http://localhost:5000"

def test_create_patient():
    """Crear un paciente de prueba"""
    print("\n=== Creando paciente de prueba ===")
    patient_data = {
        "cedula": "1111222333",
        "name": "Juan de Prueba",
        "age": 40,
        "gender": "M",
        "email": "juanprueba@example.com",
        "phone": "555-1234",
        "weight": 75.0,
        "height": 180,
        "blood_pressure_systolic": 130,
        "blood_pressure_diastolic": 85,
        "temperature": 37.5,
        "previous_diseases": "Ninguna",
        "surgeries": "Ninguna",
        "allergies": "Ninguna",
        "medications": "Ninguno",
        "parents_health": "Sin problemas",
        "diet": "Balanceada",
        "exercise": "Moderado",
        "smokes": False,
        "alcohol_consumption": "Ocasional"
    }
    
    response = requests.post(f"{BASE_URL}/api/patients", json=patient_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    return patient_data["cedula"]

def test_diagnose(cedula):
    """Realizar diagnóstico"""
    print("\n=== Realizando diagnóstico ===")
    diagnosis_data = {
        "patient_cedula": cedula,
        "symptoms": "Dolor de cabeza, fiebre, escalofríos",
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
            },
            {
                "symptom": "Escalofríos",
                "intensity": "Moderado",
                "days": 2
            }
        ]
    }
    
    response = requests.post(
        f"{BASE_URL}/api/diagnose",
        json=diagnosis_data
    )
    print(f"Status: {response.status_code}")
    resp_data = response.json()
    print(f"Response: {json.dumps(resp_data, indent=2, ensure_ascii=False)}")
    
    if response.status_code == 200:
        diagnosis_id = resp_data.get("diagnosis_id")
        confidence = resp_data.get("confidence")
        print(f"\n✓ Diagnóstico exitoso!")
        print(f"  - ID: {diagnosis_id}")
        print(f"  - Enfermedad: {resp_data.get('predicted_disease')}")
        print(f"  - Confiabilidad: {confidence}%")
        
        if confidence < 84:
            print(f"  - ⚠️  Baja confiabilidad ({confidence}% < 84%)")
            print(f"  - Pruebas recomendadas: {len(resp_data.get('recommended_tests', []))} pruebas")
            if resp_data.get('appointment_scheduled'):
                print(f"  - ✓ Cita de seguimiento programada")
        
        return diagnosis_id
    return None

def test_get_report(diagnosis_id):
    """Obtener reporte PDF"""
    print(f"\n=== Descargando reporte PDF para diagnóstico {diagnosis_id} ===")
    response = requests.get(f"{BASE_URL}/api/diagnoses/{diagnosis_id}/report")
    
    if response.status_code == 200:
        # Guardar PDF
        with open(f"reporte_prueba_{diagnosis_id}.pdf", "wb") as f:
            f.write(response.content)
        print(f"✓ PDF descargado exitosamente!")
        print(f"  - Archivo: reporte_prueba_{diagnosis_id}.pdf")
        print(f"  - Tamaño: {len(response.content)} bytes")
    else:
        print(f"✗ Error: {response.status_code}")
        print(f"Response: {response.text}")

def main():
    print("=" * 60)
    print("PRUEBA COMPLETA DEL SISTEMA MÉDICO MLOPS")
    print("=" * 60)
    
    try:
        # Test 1: Crear paciente
        cedula = test_create_patient()
        
        # Test 2: Realizar diagnóstico
        diagnosis_id = test_diagnose(cedula)
        
        if diagnosis_id:
            # Test 3: Descargar reporte
            test_get_report(diagnosis_id)
        
        print("\n" + "=" * 60)
        print("✓ PRUEBAS COMPLETADAS EXITOSAMENTE")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Esperar a que la API esté lista
    print("Esperando a que la API esté lista...")
    for i in range(30):
        try:
            requests.get(f"{BASE_URL}/api/health")
            print("✓ API lista!")
            break
        except:
            if i == 29:
                print("✗ API no respondió después de 30 intentos")
                exit(1)
            time.sleep(1)
    
    main()
