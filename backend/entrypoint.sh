#!/bin/sh
set -e

echo "Starting backend entrypoint..."

if [ -n "$DATABASE_URL" ] || [ -n "$POSTGRES_DB" ]; then
  echo "Waiting for database to be ready..."
  python - <<'PY'
import os
import time
from urllib.parse import urlparse

import psycopg2

def get_conn_params():
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        parsed = urlparse(database_url)
        return dict(
            dbname=parsed.path.lstrip("/"),
            user=parsed.username,
            password=parsed.password,
            host=parsed.hostname,
            port=parsed.port or 5432,
        )
    return dict(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5432"),
    )

params = get_conn_params()
attempts = 0
while True:
    try:
        conn = psycopg2.connect(**params)
        conn.close()
        break
    except Exception as exc:  # pragma: no cover - container startup check
        attempts += 1
        if attempts > 30:
            raise
        time.sleep(1)
PY
fi

python manage.py migrate --noinput
python manage.py collectstatic --noinput

if [ "$#" -gt 0 ]; then
  exec "$@"
fi

exec gunicorn beauty_service.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers ${GUNICORN_WORKERS:-3} \
  --timeout ${GUNICORN_TIMEOUT:-60}
