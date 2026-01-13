"""
Tests para la API
"""

import pytest
import sys
import os
from datetime import datetime, timedelta

# Agregar rutas
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from backend.app import app, db, Patient, Diagnosis, MedicalExam

@pytest.fixture
def client():
    """Fixture para cliente de prueba"""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()

@pytest.fixture
def sample_patient(client):
    """Fixture para paciente de prueba"""
    with app.app_context():
        patient = Patient(
            name='Juan Pérez',
            age=35,
            gender='M',
            email='juan@example.com',
            phone='123456789'
        )
        db.session.add(patient)
        db.session.commit()
        return patient

def test_health_check(client):
    """Test de verificación de salud"""
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'

def test_create_patient(client):
    """Test de creación de paciente"""
    response = client.post('/api/patients', json={
        'name': 'María García',
        'age': 28,
        'gender': 'F',
        'email': 'maria@example.com',
        'phone': '987654321'
    })
    
    assert response.status_code == 201
    data = response.get_json()
    assert data['name'] == 'María García'
    assert data['email'] == 'maria@example.com'

def test_create_duplicate_patient(client):
    """Test de paciente duplicado"""
    email = 'duplicate@example.com'
    
    client.post('/api/patients', json={
        'name': 'Patient 1',
        'age': 30,
        'email': email
    })
    
    response = client.post('/api/patients', json={
        'name': 'Patient 2',
        'age': 40,
        'email': email
    })
    
    assert response.status_code == 400

def test_get_patient(client, sample_patient):
    """Test de obtención de paciente"""
    response = client.get(f'/api/patients/{sample_patient.id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == 'Juan Pérez'

def test_list_patients(client, sample_patient):
    """Test de listado de pacientes"""
    response = client.get('/api/patients')
    assert response.status_code == 200
    data = response.get_json()
    assert 'patients' in data
    assert len(data['patients']) > 0

def test_diagnose_without_model(client, sample_patient):
    """Test de diagnóstico sin modelo cargado"""
    response = client.post('/api/diagnose', json={
        'patient_id': sample_patient.id,
        'symptoms': 'fiebre dolor cabeza'
    })
    
    # Sin modelo, puede fallar o procesar
    assert response.status_code in [200, 503]

def test_create_exam(client, sample_patient):
    """Test de creación de examen"""
    response = client.post('/api/exams', json={
        'patient_id': sample_patient.id,
        'exam_type': 'Radiografía',
        'description': 'Radiografía de pecho'
    })
    
    assert response.status_code == 201
    data = response.get_json()
    assert data['exam_type'] == 'Radiografía'

def test_schedule_exam(client, sample_patient):
    """Test de programación de examen"""
    # Crear examen
    exam_response = client.post('/api/exams', json={
        'patient_id': sample_patient.id,
        'exam_type': 'Sangre',
        'description': 'Análisis de sangre'
    })
    
    exam_id = exam_response.get_json()['id']
    
    # Programar
    appointment_date = (datetime.utcnow() + timedelta(days=7)).isoformat()
    response = client.put(f'/api/exams/{exam_id}/schedule', json={
        'appointment_date': appointment_date
    })
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['exam']['status'] == 'scheduled'

def test_get_patient_exams(client, sample_patient):
    """Test de obtención de exámenes del paciente"""
    # Crear exámenes
    client.post('/api/exams', json={
        'patient_id': sample_patient.id,
        'exam_type': 'Tipo 1',
        'description': 'Descripción 1'
    })
    
    response = client.get(f'/api/patients/{sample_patient.id}/exams')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) > 0

def test_invalid_patient_id(client):
    """Test con ID de paciente inválido"""
    response = client.get('/api/patients/999')
    assert response.status_code == 404
