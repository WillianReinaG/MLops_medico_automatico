"""
Script para inicializar y gestionar la base de datos
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool

# Agregar path
sys.path.insert(0, os.path.dirname(__file__))

from app import db, app, Patient, Diagnosis, MedicalExam

def create_database():
    """Crear base de datos y tablas"""
    with app.app_context():
        print("Creando tablas de base de datos...")
        db.create_all()
        print("✓ Tablas creadas exitosamente")

def drop_database():
    """Eliminar todas las tablas"""
    with app.app_context():
        print("Eliminando todas las tablas...")
        db.drop_all()
        print("✓ Tablas eliminadas")

def seed_database():
    """Llenar BD con datos de prueba"""
    from datetime import datetime, timedelta
    
    with app.app_context():
        # Crear pacientes de prueba
        test_patients = [
            Patient(
                name='Juan Pérez García',
                age=35,
                gender='M',
                email='juan.perez@example.com',
                phone='+34 912345678'
            ),
            Patient(
                name='María López Rodríguez',
                age=28,
                gender='F',
                email='maria.lopez@example.com',
                phone='+34 923456789'
            ),
            Patient(
                name='Carlos González López',
                age=42,
                gender='M',
                email='carlos.gonzalez@example.com',
                phone='+34 934567890'
            )
        ]
        
        for patient in test_patients:
            db.session.add(patient)
        
        db.session.commit()
        print("✓ Pacientes de prueba creados")

def reset_database():
    """Resetear BD completamente"""
    drop_database()
    create_database()
    seed_database()
    print("✓ Base de datos reseteada")

if __name__ == '__main__':
    command = sys.argv[1] if len(sys.argv) > 1 else 'create'
    
    if command == 'create':
        create_database()
    elif command == 'drop':
        drop_database()
    elif command == 'seed':
        seed_database()
    elif command == 'reset':
        reset_database()
    else:
        print("Uso: python manage_db.py [create|drop|seed|reset]")
