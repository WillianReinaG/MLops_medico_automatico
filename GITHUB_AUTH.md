🔐 AUTENTICACIÓN EN GITHUB
═════════════════════════════════════════════════════════════════

PROBLEMA: GitHub ya no permite contraseña en git push. Necesitas un Personal Access Token.

SOLUCIÓN:

PASO 1: Crear Personal Access Token en GitHub
──────────────────────────────────────────────

1. Ve a: https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Dale un nombre: "git-push-token"
4. Selecciona los permisos:
   ✓ repo (acceso completo a repositorios)
   ✓ user (información de usuario)
5. Click "Generate token"
6. COPIA el token (es una cadena larga)
   ⚠️ Solo se muestra UNA VEZ, cópialo ya

PASO 2: Usa el token para hacer push
────────────────────────────────────

Cuando git te pida contraseña:
- Usuario: WillianReinaG
- Contraseña: (pega el token aquí)

O directamente:

git push https://WillianReinaG:TOKEN@github.com/WillianReinaG/MLops_medico_automatico.git main

Reemplaza TOKEN con el token que copiaste.

PASO 3: Configurar credenciales (opcional pero recomendado)
──────────────────────────────────────────────────────────

Para que no tengas que pegar el token cada vez:

git config --global credential.helper store

Luego en el próximo push, ingresa:
- Usuario: WillianReinaG
- Token: (pega el token)

Git lo guardará para futuros pushes.

═════════════════════════════════════════════════════════════════

ALTERNATIVA CON SSH (Más seguro)
────────────────────────────────

1. Genera clave SSH:
   ssh-keygen -t ed25519 -C "bebedowi@gmail.com"
   (presiona Enter 3 veces)

2. Ve a: https://github.com/settings/ssh/new

3. Pega tu clave pública:
   cat ~/.ssh/id_ed25519.pub

4. Cambia la URL del remote:
   git remote set-url origin git@github.com:WillianReinaG/MLops_medico_automatico.git

5. Haz push:
   git push -u origin main

═════════════════════════════════════════════════════════════════

¿CUÁL PREFIERES?

Opción A: Personal Access Token (Más simple)
Opción B: SSH (Más seguro para futuro)

Dime cuál quieres y te ayudo.
