📤 INSTRUCCIONES PARA SUBIR A GITHUB
═════════════════════════════════════════════════════════════════

El proyecto ha sido inicializado con Git y tiene el commit inicial listo.

PASO 1: Crear repositorio en GitHub
───────────────────────────────────

1. Abre https://github.com/new
2. Completa lo siguiente:
   
   Repository name: MLops_medico_automatico
   Description: Sistema automático de diagnóstico médico basado en ML con predicción de enfermedades, solicitud de exámenes y generación de reportes médicos.
   
   Visibility: Public (para que otros puedan verlo)
   
   ✗ NO inicialices con README (ya lo tenemos)
   ✗ NO agreges .gitignore (ya lo tenemos)
   ✗ NO agregues licencia (agrégala después)
   
3. Click en "Create repository"

PASO 2: Conectar repositorio local con GitHub
──────────────────────────────────────────────

En la terminal, ejecuta:

git remote add origin https://github.com/Willian-Reina-G/MLops_medico_automatico.git

⚠️ IMPORTANTE: Reemplaza "Willian-Reina-G" con tu usuario exacto de GitHub


PASO 3: Renombrar rama main (si es necesario)
──────────────────────────────────────────────

git branch -M main


PASO 4: Subir el proyecto
─────────────────────────

git push -u origin main


PASO 5: Verificar en GitHub
───────────────────────────

1. Abre https://github.com/Willian-Reina-G/MLops_medico_automatico
2. Verifica que todos los archivos están

═════════════════════════════════════════════════════════════════

COMANDOS RÁPIDOS (copiar y pegar en terminal):

# Configurar origen (UNA SOLA VEZ)
git remote add origin https://github.com/Willian-Reina-G/MLops_medico_automatico.git

# Cambiar rama a main
git branch -M main

# Subir proyecto
git push -u origin main

═════════════════════════════════════════════════════════════════

PARA FUTUROS CAMBIOS:

Después de hacer cambios:

git add .
git commit -m "Descripción del cambio"
git push

═════════════════════════════════════════════════════════════════

CONFIGURAR GITHUB ACTIONS (Opcional):

El pipeline CI/CD en .github/workflows/ci-cd.yml se ejecutará 
automáticamente cuando hagas push:

✓ Ejecuta tests automáticos
✓ Analiza seguridad
✓ Construye imágenes Docker
✓ Genera reportes de cobertura

═════════════════════════════════════════════════════════════════

PROTEGER RAMA MAIN (Recomendado):

1. Ve a Settings → Branches
2. Click en "Add rule"
3. Pattern: main
4. Activa:
   ✓ Require pull request reviews before merging
   ✓ Require status checks to pass before merging

═════════════════════════════════════════════════════════════════

AGREGAR COLABORADORES:

1. Ve a Settings → Collaborators
2. Click "Add people"
3. Busca por usuario de GitHub
4. Selecciona rol (Write/Admin)

═════════════════════════════════════════════════════════════════

ISSUES Y PULL REQUESTS:

En GitHub puedes:
- Reportar bugs
- Sugerir features
- Hacer pull requests
- Discutir cambios

═════════════════════════════════════════════════════════════════

BADGES Y DOCUMENTACIÓN:

Puedes agregar al README.md:

[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)]
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)]
[![Docker](https://img.shields.io/badge/docker-ready-brightgreen.svg)]

═════════════════════════════════════════════════════════════════

¡Tu proyecto está listo para GitHub! 🚀

Créate en ser un developer profesional con MLOps y buenas prácticas.
