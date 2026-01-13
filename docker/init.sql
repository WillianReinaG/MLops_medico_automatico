"""
Script de inicialización de base de datos
"""

-- Crear extensiones
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Crear índices para mejorar rendimiento
CREATE INDEX IF NOT EXISTS idx_patient_email ON patients(email);
CREATE INDEX IF NOT EXISTS idx_diagnosis_patient ON diagnoses(patient_id);
CREATE INDEX IF NOT EXISTS idx_exam_patient ON medical_exams(patient_id);
CREATE INDEX IF NOT EXISTS idx_diagnosis_created ON diagnoses(created_at);
