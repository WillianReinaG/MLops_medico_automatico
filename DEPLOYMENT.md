# DEPLOYMENT.md - Guía de Despliegue

## 🚀 Despliegue del Sistema de Diagnóstico Médico

Esta guía cubre todas las opciones de despliegue del sistema MLOps Medical desde Docker hasta la nube.

## 1️⃣ Despliegue Local (Desarrollo)

### Requisitos
- Docker y Docker Compose instalados
- Git
- 4GB RAM mínimo

### Pasos

```bash
# Clonar repositorio
git clone https://github.com/tu-usuario/MLops_medico_automatico.git
cd MLops_medico_automatico

# Crear archivo .env
cp .env.example .env

# Iniciar servicios
docker-compose up -d

# Ver logs
docker-compose logs -f backend
```

### Verificar que todo funciona
```bash
# Health check API
curl http://localhost:5000/health

# Acceder a frontend
# Abrir en navegador: http://localhost:80
```

---

## 2️⃣ Despliegue en Servidor Linux

### Requisitos
- Ubuntu/Debian 20.04+
- Docker CE
- Docker Compose
- 8GB RAM mínimo
- 20GB espacio en disco

### Instalación de Docker

```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Agregar usuario actual al grupo docker
sudo usermod -aG docker $USER
newgrp docker
```

### Desplegar aplicación

```bash
# Clonar repositorio
git clone https://github.com/tu-usuario/MLops_medico_automatico.git
cd MLops_medico_automatico

# Crear archivo .env con configuración segura
cp .env.example .env
nano .env  # Editar y asegurar contraseñas

# Crear directorios persistentes
sudo mkdir -p /data/medical-db
sudo mkdir -p /data/medical-logs
sudo chown -R $USER:$USER /data/

# Iniciar servicios en background
docker-compose up -d

# Verificar estado
docker-compose ps
```

### Configurar dominio y SSL

```bash
# Editar nginx.conf para dominio
sudo nano docker/nginx.conf

# Agregar certificados SSL (ejemplo con Let's Encrypt)
sudo apt install certbot python3-certbot-nginx
sudo certbot certonly --standalone -d tudominio.com
```

### Hacer persistentes los datos

```yaml
# Actualizar docker-compose.yml
volumes:
  postgres_data:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /data/medical-db
```

---

## 3️⃣ Despliegue en AWS (EC2 + RDS)

### Arquitectura Recomendada
- EC2 (t3.medium) - Backend + Frontend + ML
- RDS (PostgreSQL) - Base de datos
- S3 - Almacenamiento de modelos
- CloudWatch - Logs y monitoreo

### Pasos

1. **Crear instancia EC2**
```bash
# AMI: Ubuntu 20.04 LTS
# Tipo: t3.medium
# Security Group: Permitir puertos 22, 80, 443
```

2. **Instalar Docker**
```bash
#!/bin/bash
sudo apt update
sudo apt install -y docker.io docker-compose git

# Descargar proyecto
cd /home/ubuntu
git clone https://github.com/tu-usuario/MLops_medico_automatico.git
cd MLops_medico_automatico

# Crear archivo .env con RDS endpoint
cat > .env << EOF
DATABASE_URL=postgresql://admin:password@medical-db.xxxxx.rds.amazonaws.com:5432/medical_db
FLASK_ENV=production
EOF

docker-compose up -d
```

3. **Crear RDS PostgreSQL**
```bash
# Via AWS Console o CLI
aws rds create-db-instance \
  --db-instance-identifier medical-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --master-username admin \
  --master-user-password <secure-password> \
  --allocated-storage 20
```

4. **Configurar Load Balancer** (opcional)
```bash
# Usar Application Load Balancer (ALB)
# Apuntar a puerto 80 de EC2
# Configurar health check: /health
```

---

## 4️⃣ Despliegue en Google Cloud (Compute Engine + Cloud SQL)

### Pasos

```bash
# 1. Crear instancia
gcloud compute instances create medical-api \
  --image-family ubuntu-2004-lts \
  --image-project ubuntu-os-cloud \
  --machine-type e2-medium \
  --zone us-central1-a

# 2. SSH a la instancia
gcloud compute ssh medical-api --zone us-central1-a

# 3. Instalar Docker (mismo que AWS)
curl -fsSL https://get.docker.com | sh
sudo apt-get install -y docker-compose

# 4. Crear Cloud SQL
gcloud sql instances create medical-db \
  --database-version POSTGRES_13 \
  --tier db-f1-micro \
  --region us-central1

# 5. Obtener conexión string
gcloud sql instances describe medical-db
```

---

## 5️⃣ Despliegue en Azure (App Service + Database for PostgreSQL)

### Via Portal Azure

1. **Crear App Service**
   - Resource Group: medical-rg
   - Runtime: Docker
   - Publish: Docker Container

2. **Crear Database**
   - Database for PostgreSQL Single Server
   - Pricing tier: Basic

3. **Configurar variables de entorno**
   - DATABASE_URL=postgresql://...
   - FLASK_ENV=production

---

## 6️⃣ Despliegue en Kubernetes (K8s)

### Requisitos
- Kubectl instalado
- Cluster K8s (Minikube, EKS, GKE, AKS)

### Manifiestos

```bash
# Crear namespace
kubectl create namespace medical

# Aplicar manifiestos
kubectl apply -f k8s/backend-deployment.yaml -n medical
kubectl apply -f k8s/db-deployment.yaml -n medical
kubectl apply -f k8s/ingress.yaml -n medical

# Ver estado
kubectl get pods -n medical
```

---

## 7️⃣ Despliegue en Heroku

```bash
# 1. Instalar Heroku CLI
curl https://cli.heroku.com/install.sh | sh

# 2. Login
heroku login

# 3. Crear aplicación
heroku create medical-diagnosis-api

# 4. Agregar PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# 5. Configurar variables
heroku config:set FLASK_ENV=production

# 6. Deploy
git push heroku main

# 7. Ver logs
heroku logs --tail
```

---

## 8️⃣ Monitoreo en Producción

### Logging
```bash
# Centralizar logs en ELK Stack
docker-compose -f docker-compose.prod.yml up -d

# O usar servicios cloud:
# - AWS CloudWatch
# - Google Cloud Logging
# - Azure Monitor
```

### Alertas
```bash
# Configurar alertas para:
# - CPU > 80%
# - Memoria > 85%
# - Disco > 90%
# - API latency > 1s
# - Errores 5xx > 1%
```

### Backups
```bash
# Backup automático de BD cada 24h
# Retener últimas 7 versiones
# Testear restore mensualmente
```

---

## 9️⃣ Optimizaciones de Producción

### Seguridad
```bash
# 1. HTTPS obligatorio
# 2. WAF (Web Application Firewall)
# 3. DDoS Protection
# 4. VPN/Bastion Host
# 5. Secretos en Vault (HashiCorp, AWS Secrets Manager)
```

### Performance
```bash
# 1. CDN para assets estáticos
# 2. Cache Redis
# 3. Database replication
# 4. Load balancing
# 5. Auto-scaling
```

### Costo
```bash
# 1. Reserved instances (-40% vs on-demand)
# 2. Spot instances para training del modelo
# 3. Auto-scaling para evitar overprovisioning
# 4. Monitorear costos con CloudMonitor
```

---

## 🔟 Troubleshooting

### API no responde
```bash
docker-compose logs backend
# Verificar que variables de entorno están correctas
# Verificar conexión a BD
```

### Base de datos no conecta
```bash
docker-compose logs db
# Verificar volúmenes
docker volume ls
# Reiniciar servicio
docker-compose restart db
```

### Bajo rendimiento
```bash
# Aumentar recursos
docker-compose.prod.yml con limits

# Revisar logs de error
docker-compose logs --tail=100 backend

# Monitorear BD
docker-compose exec db psql -U admin -d medical_db
\dt  # Ver tablas
```

---

## 📋 Checklist Pre-Producción

- [ ] Configurar variables de entorno seguras
- [ ] Cambiar contraseñas por defecto
- [ ] Configurar HTTPS/SSL
- [ ] Configurar backups automáticos
- [ ] Configurar logs centralizados
- [ ] Configurar alertas
- [ ] Realizar load testing
- [ ] Documentar procedimiento de rollback
- [ ] Configurar disaster recovery
- [ ] Plan de capacitación para ops

---

## 📞 Soporte

- Issues: GitHub Issues
- Email: ops@example.com
- Slack: #medical-ops

---

**Última actualización**: 12 de enero de 2026
