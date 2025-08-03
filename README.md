# WatchTower AI — Bootstrap

## Stack
Django/DRF + Celery + Redis + Postgres + MinIO + FastAPI (Inference) + React/Vite

## Setup
1. Copie `.env.example` para `.env` e ajuste se necessário.
2. `make up`
3. `make migrate`
4. `make createsuperuser`

## Testes rápidos
- API: `curl http://localhost:8000/api/health`
- Docs: `http://localhost:8000/api/docs/`
- JWT: `POST http://localhost:8000/api/auth/token/`
- Inference: `curl http://localhost:8500/health`
- Frontend: `http://localhost:5173`
