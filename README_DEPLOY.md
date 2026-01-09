# Production Deployment (Docker)

This guide deploys the full stack using Docker Compose:
- PostgreSQL
- Django + Gunicorn
- Nginx (serves Vue build, static, and media)

## Prerequisites
- Docker + Docker Compose installed on your server
- A domain pointing to your server IP (optional but recommended)

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
- `DJANGO_ALLOWED_HOSTS` (comma-separated)
- `POSTGRES_*` values
- `OPENAI_API_KEY` (if you use AI assistant)
- `CORS_ALLOWED_ORIGINS` / `CSRF_TRUSTED_ORIGINS` (your domain)

## 2) Start the stack

```bash
docker compose up -d --build
```

Create a Django superuser:

```bash
docker compose exec backend python manage.py createsuperuser
```

## 3) Access

- Frontend: `http://YOUR_DOMAIN/`
- API: `http://YOUR_DOMAIN/api/`
- Admin: `http://YOUR_DOMAIN/admin/`

## 4) HTTPS with Let’s Encrypt (recommended)

One simple approach is to use Certbot on the host:

```bash
sudo apt-get update
sudo apt-get install certbot
sudo certbot certonly --standalone -d your-domain.com
```

Then edit `nginx/default.conf` and enable the HTTPS block (paths are in the file).
Restart:

```bash
docker compose restart nginx
```

## 5) Updating

```bash
git pull
docker compose up -d --build
```

## 6) Troubleshooting

- Logs:
  ```bash
  docker compose logs -f backend
  docker compose logs -f nginx
  docker compose logs -f db
  ```
- Common issues:
  - `ALLOWED_HOSTS` missing your domain
  - `CSRF_TRUSTED_ORIGINS` missing `https://your-domain.com`
  - Wrong DB credentials in `.env`
  - Static or media permissions: ensure volumes are mounted and writable

## Development (optional)

Run the dev stack with Vite + Django runserver:

```bash
docker compose -f docker-compose.dev.yml up --build
```

Frontend: `http://localhost:5173`  
Backend: `http://localhost:8000`
