# FreshGuard AI — Production Deployment Guide

**Application:** FreshGuard AI  
**Deployment Model:** Containerized Microservices (Docker / FastAPI / PostgreSQL)  

---

## 1. System Requirements

- **Python:** 3.11+ (tested on Python 3.14)
- **Database:** PostgreSQL 15+ (Production) / SQLite (Local Development)
- **System Memory:** 2GB RAM minimum (4GB recommended for Vision AI inference)
- **Container Runtime:** Docker Engine 20.10+ & Docker Compose 2.0+

---

## 2. Docker & Containerized Deployment

### A. Environment Configuration
Copy `.env.example` to `.env` in the project root:

```bash
cp .env.example .env
```

Ensure production values are supplied:
```env
APP_NAME=FreshGuard AI
APP_ENV=production
SECRET_KEY=your_random_production_jwt_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=4320
DATABASE_URL=postgresql://freshguard:freshguard_pass@db:5432/freshguard_db
CORS_ORIGINS=https://app.freshguard.ai,http://localhost:8000
```

### B. Launching Container Stack
Execute Docker Compose to bring up PostgreSQL and FastAPI Backend:

```bash
docker-compose up -d --build
```

Verify service status:
```bash
docker-compose ps
```

---

## 3. Production Health Probes & Verification

Configure container orchestra (Kubernetes / AWS ECS / Render) health check probes:

- **Liveness Probe:**
  - Endpoint: `GET /health`
  - Protocol: HTTP
  - Expected Status: `200 OK`
  - Response: `{"status": "READY", "process_alive": true}`
- **Readiness Probe:**
  - Endpoint: `GET /api/v1/health`
  - Interval: 10s
  - Timeout: 2s

---

## 4. Environment Checklist

- [x] Production `SECRET_KEY` configured via environment variable.
- [x] Production `DATABASE_URL` pointing to isolated PostgreSQL instance.
- [x] CORS origins restricted to approved web domains via `CORS_ORIGINS`.
- [x] Automated SHA-256 model integrity verification enabled on startup (`python scripts/verify_model_integrity.py`).
- [x] HTTPS enforced via reverse proxy (Nginx / Cloudflare / AWS ALB).
