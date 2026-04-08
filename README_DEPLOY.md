# Production Deployment (Docker)

This guide deploys the full stack using Docker Compose over a public IPv4 only:
- PostgreSQL
- Django + Gunicorn
- Nginx (serves Vue build, static, and media)

## Prerequisites
- Docker + Docker Compose installed on your server
- Server public IPv4: `72.56.70.71`

## 1) Clone and configure

```bash
git clone <your-repo-url> beauty_service
cd beauty_service
```

Copy the example env and fill in values:

```bash
cp .env.example .env
```

Key variables:
- `DJANGO_SECRET_KEY` (required)
- `DJANGO_ALLOWED_HOSTS` (must include `72.56.70.71`)
- `POSTGRES_*` values
- `OPENAI_API_KEY` (if you use AI assistant)
- `CORS_ALLOWED_ORIGINS` / `CSRF_TRUSTED_ORIGINS` (use the IPv4)
- `DJANGO_SECURE_COOKIES` should stay `false` for HTTP-only deployment

## 2) Start the stack

```bash
docker compose up -d --build
```

Create a Django superuser:

```bash
docker compose exec backend python manage.py createsuperuser
```

## 3) Access

- Frontend: `http://72.56.70.71/`
- API: `http://72.56.70.71/api/`
- Staff panel (SPA): `http://72.56.70.71/admin/`
- Django admin: `http://72.56.70.71/django-admin/`

Quick checks:

```bash
curl -I http://72.56.70.71/
curl http://72.56.70.71/api/health/
```

## 4) Updating

```bash
git pull
docker compose up -d --build
```

## 5) Troubleshooting

- Logs:
  ```bash
  docker compose logs -f backend
  docker compose logs -f nginx
  docker compose logs -f db
  ```
- Common issues:
  - `ALLOWED_HOSTS` missing `72.56.70.71`
  - `CSRF_TRUSTED_ORIGINS` missing `http://72.56.70.71`
  - Wrong DB credentials in `.env`
  - Static or media permissions: ensure volumes are mounted and writable

## Development (optional)

Run the dev stack with Vite + Django runserver:

```bash
docker compose -f docker-compose.dev.yml up --build
```

Frontend: `http://localhost:5173`  
Backend: `http://localhost:8000`
