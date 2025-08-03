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

## Fluxo de Ingestão

1. Crie os cadastros básicos usando um token JWT:

```bash
# Site
curl -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"name":"Obra Alpha","address":"Rua X"}' \
  http://localhost:8000/api/sites/

# Area
curl -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"site":1,"name":"Galpao 1"}' \
  http://localhost:8000/api/areas/

# Camera
curl -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"area":1,"name":"Cam 1","rtsp_url":""}' \
  http://localhost:8000/api/cameras/
```

2. Ingestão de um frame gera um `DetectionEvent`:

```bash
curl -H "Authorization: Bearer $TOKEN" \
  -F "camera_id=1" \
  -F "image=@/caminho/frame.jpg" \
  http://localhost:8000/api/events/ingest
```

3. Filtre eventos:

```bash
curl -H "Authorization: Bearer $TOKEN" \
  "http://localhost:8000/api/events/?site=1&violation=true"
```
