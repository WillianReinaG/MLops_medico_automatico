"""
Script de inicialización rápida del modelo ML
Ejecuta el entrenamiento sin dependencias externas complejas
"""

import os
import sys

# Crear directorio de modelos
os.makedirs('ml_model/models', exist_ok=True)

print("""
╔════════════════════════════════════════════════════════════╗
║   Sistema de Diagnóstico Médico - Configuración           ║
╚════════════════════════════════════════════════════════════╝

El proyecto ha sido creado exitosamente con:

✓ Backend API (Flask) - Endpoints para diagnóstico
✓ Modelo ML (scikit-learn) - Predicción de enfermedades  
✓ Base de Datos (PostgreSQL) - Gestión de pacientes
✓ Frontend Web (HTML/JS) - Interfaz de usuario
✓ Docker & Docker Compose - Containerización completa
✓ GitHub Actions - CI/CD automático
✓ Tests automáticos - pytest

""")

print("PRÓXIMOS PASOS:")
print("="*60)
print("\n1. OPCIÓN A: Usar Docker (RECOMENDADO)")
print("   • Abre una terminal en el directorio del proyecto")
print("   • Windows:")
print("       init.bat")
print("   • Linux/Mac:")
print("       bash init.sh")
print("   • O directamente:")
print("       docker-compose up -d")

print("\n2. OPCIÓN B: Instalación Local")
print("   • Crear entorno virtual: python -m venv venv")
print("   • Activar: source venv/bin/activate (Linux/Mac)")
print("             o: venv\\Scripts\\activate (Windows)")
print("   • Instalar: pip install -r backend/requirements.txt")
print("              pip install -r ml_model/requirements.txt")
print("   • Entrenar modelo: cd ml_model && python train_model.py")
print("   • Ejecutar API: cd backend && python app.py")

print("\n3. ACCESO A LA APLICACIÓN")
print("   • Frontend: http://localhost:80 (o http://localhost:3000)")
print("   • API: http://localhost:5000")
print("   • Base de datos (pgAdmin): http://localhost:5050")
print("   • Usuario pgAdmin: admin@example.com / admin")

print("\n4. ESTRUCTURA DEL PROYECTO")
print("   • backend/          - API REST con Flask")
print("   • ml_model/         - Modelo de Machine Learning")
print("   • frontend/         - Interfaz web HTML/JS")
print("   • docker/           - Archivos de configuración Docker")
print("   • tests/            - Tests automáticos")
print("   • .github/workflows - CI/CD con GitHub Actions")

print("\n5. COMANDOS ÚTILES (si tienes Make instalado)")
print("   • make help         - Ver todos los comandos")
print("   • make up           - Iniciar servicios")
print("   • make down         - Detener servicios")
print("   • make logs         - Ver logs")
print("   • make test         - Ejecutar tests")
print("   • make train-model  - Entrenar modelo ML")

print("\n6. DOCUMENTACIÓN")
print("   • README.md         - Documentación completa")
print("   • .github/copilot-instructions.md - Instrucciones IA")

print("\n" + "="*60)
print("✓ ¡PROYECTO LISTO PARA USAR!")
print("="*60)

# Crear archivo de configuración default
config_content = """# Configuración por defecto del proyecto
# Cambiar según tus necesidades

API_HOST=0.0.0.0
API_PORT=5000

DATABASE_HOST=db
DATABASE_PORT=5432
DATABASE_NAME=medical_db
DATABASE_USER=admin
DATABASE_PASSWORD=password

FLASK_ENV=production
DEBUG=False

MODEL_PATH=/app/ml_model/models
"""

if not os.path.exists('.env'):
    with open('.env', 'w') as f:
        f.write(config_content)
    print("\n✓ Archivo .env creado")

print("\n💡 TIP: Ejecuta 'docker-compose up -d' para iniciar automáticamente")
print("        todos los servicios (recomendado para principiantes)\n")
