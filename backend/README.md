# PawMatch Backend — Deployment & Containerization Guide

This directory contains the production-grade, cloud-agnostic containerized setup for the **PawMatch** Django REST API backend.

---

## 1. Local Development & Docker Setup

### Prerequisites
- [Docker Desktop](https://www.docker.com/) (or Docker Engine 24.0+)
- Docker Compose v2+

### Build Image Locally
```bash
cd backend
docker build -t pawmatch-backend:latest .
```

### Run Containerized Application via Docker Compose
```bash
# Start backend service
docker compose up -d

# View container logs
docker compose logs -f backend

# Stop container services
docker compose down
```

The containerized API will be accessible at `http://localhost:8000`.
Health check probe: `http://localhost:8000/health/`

---

## 2. Render Cloud Deployment (Docker Runtime)

PawMatch is configured for zero-friction deployment on **Render** using Docker runtime.

### Step-by-Step Deployment Instructions
1. **Push Repository**: Ensure your latest changes are pushed to GitHub.
2. **Connect Render Blueprint**:
   - Log in to the [Render Dashboard](https://dashboard.render.com/).
   - Click **New +** ➔ **Blueprint**.
   - Connect your `PawMatch` GitHub repository.
   - Render automatically detects `render.yaml`.
3. **Manual Web Service Creation (Alternative)**:
   - Click **New +** ➔ **Web Service**.
   - Select **Build and deploy from a Git repository**.
   - Choose **Docker** runtime.
   - Set **Context Directory** to `backend`.
   - Set **Dockerfile Path** to `Dockerfile`.
   - Set **Health Check Path** to `/health/`.
4. **Configure Environment Variables**:
   Add the following environment variables in the Render Dashboard:

| Variable | Required | Sample / Value | Description |
| :--- | :---: | :--- | :--- |
| `DJANGO_SETTINGS_MODULE` | Yes | `config.settings.production` | Django settings entry point |
| `SECRET_KEY` | Yes | *[Generated Cryptographic Key]* | Django secret key |
| `DATABASE_URL` | Yes | `postgres://user:pass@ep-neon-123.onrender.com/pawmatch` | Neon / Render Managed PostgreSQL connection string |
| `REDIS_URL` | Optional | `redis://:pass@redis-host:6379/0` | Managed Redis instance for caching/Celery |
| `ALLOWED_HOSTS` | Yes | `.onrender.com,api.pawmatch.com` | Allowed host origins |
| `CORS_ALLOWED_ORIGINS` | Yes | `https://pawmatch.com` | Allowed CORS origins for React frontend |
| `CSRF_TRUSTED_ORIGINS` | Yes | `https://pawmatch.com` | Trusted origins for CSRF validation |
| `SECURE_SSL_REDIRECT` | Yes | `true` | Forces HTTPS redirection |
| `LOG_LEVEL` | No | `INFO` | Logging threshold |

5. **Deploy**: Click **Create Web Service** to launch the deployment pipeline.

---

## 3. OCI & Multi-Cloud Portability

The generated Docker image is 100% OCI-compliant and cloud-agnostic. It can be deployed without modification to:
- **AWS ECS / Fargate / EKS**
- **Kubernetes (K8s)**
- **Google Cloud Run**
- **Azure App Service / AKS**
- **DigitalOcean App Platform**

---

## 4. Verification & Health Probes

- **Health Check Endpoint**: `GET /health/`
  - Returns `{"status": "healthy"}` with HTTP 200.
  - Zero database queries, instantaneous response.
- **Static Asset Verification**: WhiteNoise automatically compresses and serves assets gathered during image build (`python manage.py collectstatic`).
