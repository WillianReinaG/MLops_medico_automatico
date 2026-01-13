"""
Script de inicialización del proyecto
Ejecutar una sola vez después de clonar el repositorio
"""

import os
import sys
import subprocess

def run_command(command, description):
    """Ejecutar comando y reportar resultado"""
    print(f"\n{'='*50}")
    print(f"→ {description}")
    print(f"{'='*50}")
    try:
        result = subprocess.run(command, shell=True, check=True)
        print(f"✓ {description} - OK")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} - ERROR: {e}")
        return False

def main():
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║   Inicializador de MLOps Medical Diagnosis System          ║
    ║   Sistema de Diagnóstico Médico con Machine Learning      ║
    ╚════════════════════════════════════════════════════════════╝
    """)

    # Crear directorios necesarios
    print("\n📁 Creando directorios...")
    os.makedirs('ml_model/models', exist_ok=True)
    os.makedirs('logs', exist_ok=True)
    os.makedirs('data', exist_ok=True)
    print("✓ Directorios creados")

    # Copiar archivo .env
    if not os.path.exists('.env'):
        print("\n🔐 Creando archivo .env...")
        if os.path.exists('.env.example'):
            with open('.env.example', 'r') as src, open('.env', 'w') as dst:
                dst.write(src.read())
            print("✓ Archivo .env creado (basado en .env.example)")
        else:
            print("⚠ No se encontró .env.example")
    else:
        print("⚠ .env ya existe, saltando...")

    # Dar opción de iniciar con Docker
    print("\n" + "="*50)
    print("Opciones de inicialización:")
    print("="*50)
    print("1. Docker Compose (recomendado)")
    print("2. Instalación local")
    print("3. Solo crear estructura")
    
    try:
        choice = input("\nSelecciona una opción (1-3): ").strip()
    except:
        choice = '3'

    if choice == '1':
        if run_command('docker-compose up -d', 'Iniciando Docker Compose'):
            print("\n✓ ¡Servicios iniciados!")
            print("\nAccesos:")
            print("  • API: http://localhost:5000")
            print("  • Frontend: http://localhost:80")
            print("  • pgAdmin: http://localhost:5050 (admin@example.com / admin)")
            print("\nVer logs:")
            print("  docker-compose logs -f")

    elif choice == '2':
        print("\n🐍 Instalación local...")
        run_command(f'{sys.executable} -m pip install -r backend/requirements.txt', 'Instalar dependencias backend')
        run_command(f'{sys.executable} -m pip install -r ml_model/requirements.txt', 'Instalar dependencias ML')
        print("\nPasos siguientes:")
        print("  1. cd ml_model && python train_model.py")
        print("  2. cd backend && python app.py")

    else:
        print("\n✓ Estructura del proyecto lista")

    print("\n" + "="*50)
    print("✓ Inicialización completada")
    print("="*50)
    print("\nDocumentación: Consulta README.md para más detalles")

if __name__ == '__main__':
    main()
