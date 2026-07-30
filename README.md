# PawMatch — Pet Adoption & Health Ecosystem

PawMatch is an end-to-end pet adoption and health ecosystem powered by a React 19 SPA client and a modular Django 5 REST Framework backend.

---

## Technical Documentation & Architecture

- **Root Technical Specs**: See [`docs/`](file:///home/spidy/Desktop/projects/PawMatch/docs/)
- **Backend Architecture & Guidelines**: See [`backend/filestructure.md`](file:///home/spidy/Desktop/projects/PawMatch/backend/filestructure.md)
- **Deployment & Containerization Guide**: See [`backend/README.md`](file:///home/spidy/Desktop/projects/PawMatch/backend/README.md)

---

## Quick Start (Backend Containerized)

### Local Docker Build
```bash
cd backend
docker build -t pawmatch-backend .
```

### Local Docker Compose
```bash
cd backend
docker compose up -d
```

Access the health check endpoint: `http://localhost:8000/health/`
