#!/usr/bin/env python3
"""
Script Completo de Pruebas de Producción
Sistema de Diagnóstico Médico MLOps

Prueba todos los endpoints y funcionalidades del sistema
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, List, Tuple

# ==================== CONFIGURACIÓN ====================

BASE_URL = "http://localhost:5000"
API_TIMEOUT = 30  # Aumentado de 10 a 30 segundos
MAX_RETRIES = 3   # Reintentos si falla
RETRY_DELAY = 2   # Delay entre reintentos

# Colores para terminal
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    END = '\033[0m'

# ==================== UTILIDADES ====================

def print_header(text: str):
    """Imprimir encabezado"""
    print(f"\n{Colors.BLUE}{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}{Colors.END}\n")

def print_success(text: str):
    """Imprimir mensaje de éxito"""
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")

def print_error(text: str):
    """Imprimir mensaje de error"""
    print(f"{Colors.RED}✗ {text}{Colors.END}")

def print_warning(text: str):
    """Imprimir mensaje de advertencia"""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.END}")

def print_info(text: str):
    """Imprimir información"""
    print(f"{Colors.CYAN}ℹ {text}{Colors.END}")

def print_test_result(test_name: str, passed: bool, details: str = ""):
    """Imprimir resultado de test"""
    status = f"{Colors.GREEN}PASÓ{Colors.END}" if passed else f"{Colors.RED}FALLÓ{Colors.END}"
    print(f"  [{status}] {test_name}")
    if details:
        print(f"       {details}")

# ==================== TESTS ====================

class ProductionTester:
    def __init__(self):
        self.results = {
            'total': 0,
            'passed': 0,
            'failed': 0,
            'tests': []
        }
        # Usar una cédula con timestamp para evitar conflictos entre ejecuciones
        import time
        self.patient_cedula = str(int(time.time() % 10000000000))  # Cédula basada en timestamp
        self.diagnosis_id = None
        self.session = requests.Session()
        self.session.timeout = API_TIMEOUT

    def hacer_request(self, metodo, url, **kwargs):
        """
        Hacer request con reintentos automáticos
        
        Args:
            metodo: 'GET', 'POST', etc.
            url: URL completa
            **kwargs: argumentos para requests
            
        Returns:
            response o None si falla después de reintentos
        """
        for intento in range(MAX_RETRIES):
            try:
                if metodo.upper() == 'GET':
                    return self.session.get(url, timeout=API_TIMEOUT, **kwargs)
                elif metodo.upper() == 'POST':
                    return self.session.post(url, timeout=API_TIMEOUT, **kwargs)
                elif metodo.upper() == 'PUT':
                    return self.session.put(url, timeout=API_TIMEOUT, **kwargs)
                else:
                    return None
            except (requests.Timeout, requests.ConnectionError) as e:
                if intento < MAX_RETRIES - 1:
                    print_warning(f"Timeout/Error - Reintentando ({intento+1}/{MAX_RETRIES})...")
                    time.sleep(RETRY_DELAY)
                else:
                    print_error(f"Falló después de {MAX_RETRIES} intentos: {str(e)}")
                    return None
            except Exception as e:
                print_error(f"Error inesperado: {str(e)}")
                return None
        return None

    def run_all_tests(self):
        """Ejecutar todas las pruebas"""
        print_header("PRUEBAS DE PRODUCCIÓN - SISTEMA MÉDICO MLOPS")
        
        try:
            # Pruebas básicas
            self.test_health_check()
            
            # Pruebas de pacientes
            self.test_create_patient()
            self.test_get_patient()
            self.test_list_patients()
            
            # Pruebas de diagnóstico
            self.test_diagnose()
            self.test_get_diagnoses()
            
            # Pruebas de reportes
            self.test_generate_report()
            
            # Pruebas de exámenes
            self.test_create_exam()
            self.test_get_exams()
            
            # Resumen
            self.print_summary()
            
        except Exception as e:
            print_error(f"Error crítico: {str(e)}")

    # -------- TEST: Health Check --------
    def test_health_check(self):
        """Test 1: Verificar que la API esté saludable"""
        print_header("Test 1: Health Check")
        
        try:
            response = self.hacer_request('GET', f"{BASE_URL}/api/health")
            if response is None:
                print_test_result("API Health Check", False, "No hay respuesta del servidor")
                self.add_result("Health Check", False)
                return
                
            passed = response.status_code == 200
            data = response.json() if response.status_code == 200 else {}
            
            print_test_result(
                "API Health Check",
                passed,
                f"Status: {data.get('status')}, Model: {data.get('model_loaded')}"
            )
            self.add_result("Health Check", passed)
            
        except Exception as e:
            print_test_result("API Health Check", False, str(e))
            self.add_result("Health Check", False)

    # -------- TEST: Crear Paciente --------
    def test_create_patient(self):
        """Test 2: Crear un paciente nuevo"""
        print_header("Test 2: Crear Paciente")
        
        patient_data = {
            "cedula": self.patient_cedula,
            "name": "Paciente Test Producción",
            "age": 45,
            "gender": "M",
            "email": f"test{self.patient_cedula}@produccion.com",  # Email único
            "phone": "555-9999",
            "weight": 78.5,
            "height": 175,
            "blood_pressure_systolic": 128,
            "blood_pressure_diastolic": 82,
            "temperature": 37.1,
            "previous_diseases": "Diabetes tipo 2",
            "surgeries": "Apendicitis 2010",
            "allergies": "Penicilina",
            "medications": "Metformina 500mg",
            "parents_health": "Padre hipertensión",
            "diet": "Balanceada baja en sodio",
            "exercise": "Moderado",
            "smokes": False,
            "alcohol_consumption": "Ocasional"
        }
        
        try:
            response = self.hacer_request(
                'POST',
                f"{BASE_URL}/api/patients",
                json=patient_data
            )
            if response is None:
                print_test_result("Crear paciente", False, "No hay respuesta del servidor")
                self.add_result("Crear Paciente", False)
                return
            
            passed = response.status_code == 201
            data = response.json() if response.status_code in [200, 201] else {}
            
            print_test_result(
                "Crear paciente",
                passed,
                f"Cédula: {data.get('cedula', self.patient_cedula)}, Status: {response.status_code}"
            )
            self.add_result("Crear Paciente", passed)
            
        except Exception as e:
            print_test_result("Crear paciente", False, str(e))
            self.add_result("Crear Paciente", False)

    # -------- TEST: Obtener Paciente --------
    def test_get_patient(self):
        """Test 3: Obtener información del paciente"""
        print_header("Test 3: Obtener Paciente")
        
        try:
            response = self.hacer_request(
                'GET',
                f"{BASE_URL}/api/patients/{self.patient_cedula}"
            )
            if response is None:
                print_test_result("Obtener paciente", False, "No hay respuesta del servidor")
                self.add_result("Obtener Paciente", False)
                return
            
            passed = response.status_code == 200
            data = response.json()
            
            print_test_result(
                "Obtener paciente",
                passed,
                f"Nombre: {data.get('name', 'N/A')}"
            )
            self.add_result("Obtener Paciente", passed)
            
        except Exception as e:
            print_test_result("Obtener paciente", False, str(e))
            self.add_result("Obtener Paciente", False)

    # -------- TEST: Listar Pacientes --------
    def test_list_patients(self):
        """Test 4: Listar todos los pacientes"""
        print_header("Test 4: Listar Pacientes")
        
        try:
            response = self.hacer_request(
                'GET',
                f"{BASE_URL}/api/patients"
            )
            if response is None:
                print_test_result("Listar pacientes", False, "No hay respuesta del servidor")
                self.add_result("Listar Pacientes", False)
                return
            
            passed = response.status_code == 200
            data = response.json()
            count = len(data) if isinstance(data, list) else data.get('total', 0)
            
            print_test_result(
                "Listar pacientes",
                passed,
                f"Total: {count} pacientes"
            )
            self.add_result("Listar Pacientes", passed)
            
        except Exception as e:
            print_test_result("Listar pacientes", False, str(e))
            self.add_result("Listar Pacientes", False)

    # -------- TEST: Diagnóstico --------
    def test_diagnose(self):
        """Test 5: Realizar diagnóstico"""
        print_header("Test 5: Realizar Diagnóstico")
        
        diagnosis_data = {
            "patient_cedula": self.patient_cedula,
            "symptoms": "Fiebre, tos seca, cansancio, dificultad para respirar",
            "symptoms_detail": [
                {"symptom": "Fiebre", "intensity": "Moderada", "days": 4},
                {"symptom": "Tos seca", "intensity": "Severa", "days": 5},
                {"symptom": "Cansancio", "intensity": "Moderada", "days": 3},
                {"symptom": "Dificultad para respirar", "intensity": "Leve", "days": 2}
            ]
        }
        
        try:
            response = self.hacer_request(
                'POST',
                f"{BASE_URL}/api/diagnose",
                json=diagnosis_data
            )
            if response is None:
                print_test_result("Realizar diagnóstico", False, "No hay respuesta del servidor")
                self.add_result("Diagnóstico", False)
                return
            
            passed = response.status_code == 200
            data = response.json()
            
            if passed:
                self.diagnosis_id = data.get('diagnosis_id')
            
            print_test_result(
                "Realizar diagnóstico",
                passed,
                f"Enfermedad: {data.get('predicted_disease', 'N/A')}, Confianza: {data.get('confidence', 'N/A')}%"
            )
            self.add_result("Diagnóstico", passed)
            
        except Exception as e:
            print_test_result("Realizar diagnóstico", False, str(e))
            self.add_result("Diagnóstico", False)

    # -------- TEST: Obtener Diagnósticos --------
    def test_get_diagnoses(self):
        """Test 6: Obtener historial de diagnósticos"""
        print_header("Test 6: Obtener Diagnósticos")
        
        try:
            response = self.hacer_request(
                'GET',
                f"{BASE_URL}/api/patients/{self.patient_cedula}/diagnoses"
            )
            if response is None:
                print_test_result("Obtener diagnósticos", False, "No hay respuesta del servidor")
                self.add_result("Obtener Diagnósticos", False)
                return
            
            passed = response.status_code == 200
            data = response.json()
            count = len(data) if isinstance(data, list) else 0
            
            print_test_result(
                "Obtener diagnósticos",
                passed,
                f"Total: {count} diagnósticos"
            )
            self.add_result("Obtener Diagnósticos", passed)
            
        except Exception as e:
            print_test_result("Obtener diagnósticos", False, str(e))
            self.add_result("Obtener Diagnósticos", False)

    # -------- TEST: Generar Reporte PDF --------
    def test_generate_report(self):
        """Test 7: Generar reporte PDF"""
        print_header("Test 7: Generar Reporte PDF")
        
        if not self.diagnosis_id:
            print_warning("Se saltó el test - No hay diagnosis_id disponible")
            self.add_result("Generar Reporte", False)
            return
        
        try:
            response = self.hacer_request(
                'GET',
                f"{BASE_URL}/api/diagnoses/{self.diagnosis_id}/report"
            )
            if response is None:
                print_test_result("Generar reporte PDF", False, "No hay respuesta del servidor")
                self.add_result("Generar Reporte", False)
                return
            
            # Verificar que sea PDF (status 200 y contenido binario)
            passed = response.status_code == 200 and len(response.content) > 0
            size = len(response.content) if passed else 0
            
            print_test_result(
                "Generar reporte PDF",
                passed,
                f"Tamaño: {size} bytes"
            )
            self.add_result("Generar Reporte", passed)
            
        except Exception as e:
            print_test_result("Generar reporte PDF", False, str(e))
            self.add_result("Generar Reporte", False)

    # -------- TEST: Crear Examen --------
    def test_create_exam(self):
        """Test 8: Crear orden de examen"""
        print_header("Test 8: Crear Examen")
        
        exam_data = {
            "patient_cedula": self.patient_cedula,
            "exam_type": "Hemograma completo",
            "notes": "Prueba de producción"
        }
        
        try:
            response = self.hacer_request(
                'POST',
                f"{BASE_URL}/api/exams",
                json=exam_data
            )
            if response is None:
                print_test_result("Crear examen", False, "No hay respuesta del servidor")
                self.add_result("Crear Examen", False)
                return
            
            passed = response.status_code == 201
            data = response.json()
            
            print_test_result(
                "Crear examen",
                passed,
                f"ID: {data.get('exam_id', 'N/A')}"
            )
            self.add_result("Crear Examen", passed)
            
        except Exception as e:
            print_test_result("Crear examen", False, str(e))
            self.add_result("Crear Examen", False)

    # -------- TEST: Obtener Exámenes --------
    def test_get_exams(self):
        """Test 9: Obtener exámenes del paciente"""
        print_header("Test 9: Obtener Exámenes")
        
        try:
            response = self.hacer_request(
                'GET',
                f"{BASE_URL}/api/patients/{self.patient_cedula}/exams"
            )
            if response is None:
                print_test_result("Obtener exámenes", False, "No hay respuesta del servidor")
                self.add_result("Obtener Exámenes", False)
                return
            
            passed = response.status_code == 200
            data = response.json()
            count = len(data) if isinstance(data, list) else 0
            
            print_test_result(
                "Obtener exámenes",
                passed,
                f"Total: {count} exámenes"
            )
            self.add_result("Obtener Exámenes", passed)
            
        except Exception as e:
            print_test_result("Obtener exámenes", False, str(e))
            self.add_result("Obtener Exámenes", False)

    # -------- UTILIDADES --------
    def add_result(self, test_name: str, passed: bool):
        """Agregar resultado de test"""
        self.results['total'] += 1
        self.results['tests'].append({'name': test_name, 'passed': passed})
        if passed:
            self.results['passed'] += 1
        else:
            self.results['failed'] += 1

    def print_summary(self):
        """Imprimir resumen de resultados"""
        print_header("RESUMEN DE PRUEBAS")
        
        total = self.results['total']
        passed = self.results['passed']
        failed = self.results['failed']
        percentage = (passed / total * 100) if total > 0 else 0
        
        print(f"Total de pruebas:  {total}")
        print(f"{Colors.GREEN}Pasadas:         {passed}{Colors.END}")
        print(f"{Colors.RED}Fallidas:        {failed}{Colors.END}")
        print(f"Porcentaje éxito: {percentage:.1f}%\n")
        
        if percentage == 100:
            print_success("¡TODAS LAS PRUEBAS PASARON! Sistema listo para producción.")
        elif percentage >= 80:
            print_warning("La mayoría de pruebas pasaron. Revisar las fallidas.")
        else:
            print_error("Hay problemas. Revisar todos los fallos antes de producción.")
        
        print(f"\n{Colors.BLUE}Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.END}")

# ==================== MAIN ====================

def main():
    """Función principal"""
    print_header("PREPARACIÓN DE PRUEBAS EN PRODUCCIÓN")
    print_info("Verificando conectividad...")
    
    # Intentar conectar a la API
    try:
        response = requests.get(f"{BASE_URL}/api/health", timeout=5)
        print_success(f"API accesible en {BASE_URL}")
    except Exception as e:
        print_error(f"No se puede conectar a la API: {str(e)}")
        print_info("Asegúrate de que: docker-compose está corriendo y API está en puerto 5000")
        return
    
    # Ejecutar pruebas
    tester = ProductionTester()
    tester.run_all_tests()
    
    # Instrucciones finales
    print_header("PRÓXIMOS PASOS")
    print_info("1. Revisar todos los resultados arriba")
    print_info("2. Si todas las pruebas pasaron:")
    print_info("   - El sistema está listo para producción")
    print_info("   - Acceder a: http://localhost")
    print_info("   - API disponible en: http://localhost:5000")
    print_info("3. Si hay fallos:")
    print_info("   - Revisar logs: docker logs medical_api")
    print_info("   - Reiniciar servicios: docker-compose restart")
    print_info("   - Volver a ejecutar este script")

if __name__ == "__main__":
    main()
