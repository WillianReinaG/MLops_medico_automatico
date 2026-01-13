-- Script de inicialización de base de datos
-- Las tablas se crean automáticamente desde la aplicación Flask

-- Limpiar tablas si existen
DROP TABLE IF EXISTS medical_exams CASCADE;
DROP TABLE IF EXISTS diagnoses CASCADE;
DROP TABLE IF EXISTS patients CASCADE;

-- Crear extensiones útiles para PostgreSQL
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
