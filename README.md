# Beauty Salon Automation & Recommendation Starter

Mono-repo for a premium **Beauty & Healthy Bar** experience. Django powers the API; Vue 3 + Vite powers the frontend with a fresh lime + deep green palette.

## Project layout
- `backend/` — Django project `beauty_service` with app `core`.
- `frontend/` — Vite + Vue 3 app with router, components, and assets.

## Backend (Django)
```bash
cd backend
python3 -m venv .venv              # create a virtualenv (optional but recommended)
source .venv/bin/activate          # activate it
pip install -r requirements.txt    # install Django + DRF + CORS headers

python manage.py migrate           # create the SQLite db
python manage.py createsuperuser   # optional: access the admin
python manage.py runserver         # start API on http://localhost:8000
```

### Environment
Set these for the AI assistant endpoint in the project root `.env`:
- `OPENAI_API_KEY` — required to call the OpenAI API.
- `OPENAI_MODEL` — optional, defaults to `gpt-4.1-mini`.

### Endpoints
- `/` — Health check JSON: “Beauty service API is running”.
- `/admin/` — manage services, categories, clients.
- `/api/services/` — placeholder services list (replace with DB + serializers).
- `/api/recommendations/` — placeholder recommendations (future ML hook).
- `/api/ai/chat/` — AI cosmetologist assistant (OpenAI required).

### CORS
`CORS_ALLOWED_ORIGINS` is set for `http://localhost:5173` (Vite dev server). Add production origins when deploying.

## Frontend (Vue 3 + Vite)
```bash
cd frontend
npm install        # install deps
npm run dev        # start Vite dev server on http://localhost:5173
```

Pages:
- `/` Landing page with hero, highlights, gallery, and recommendation teaser (uses API if available).
- `/services` Service cards with filters and “Add to plan” placeholder action.
- `/about` Brand story, contacts, and team section.

## Development notes
- Replace placeholder assets in `frontend/src/assets/` (`logo-bizu.svg`, `salon-*.jpg`, `hero-bg-pattern.svg`) with real client files.
- Extend recommendation logic in `backend/core/views.py` and swap placeholder data with serializers tied to models.
- Booking/auth flows can live in new Django apps + Vue pages; keep CORS origins aligned.
- Tailwind or additional UI libraries can be added later if desired; current styles use handcrafted CSS with the specified palette.

Happy building!
