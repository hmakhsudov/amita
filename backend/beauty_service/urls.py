"""
Root URL configuration for beauty_service.

Routes:
- /admin/: Django admin for managing services/clients.
- /api/health/: health check endpoint for container monitoring.
- /api/services/: CRUD services (GET public, write for admins).
- /api/categories/: CRUD categories (GET public, write for admins).
- /api/plan/: authenticated user plan endpoints.
- /api/bookings/: booking endpoints.
- /api/availability/: availability slots endpoint.
- /api/masters/: list of masters.
- /api/recommendations/: placeholder recommendations response.
- /: simple health check text response.
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from core import views as core_views

urlpatterns = [
    path("admin/", admin.site.urls),
    # API routes for the Vue frontend to consume
    path("api/health/", core_views.health, name="health"),
    path("api/recommendations/", core_views.recommendations, name="recommendations"),
    path("api/", include("core.api_urls")),
    path("api/plan/", include("core.plan_urls")),
    path("api/", include("core.booking_urls")),
    path("api/", include("core.masters_urls")),
    path("api/", include("core.favorites_urls")),
    path("api/", include("core.ai_urls")),
    path("api/", include("core.chat_urls")),
    # Auth routes (SimpleJWT + registration)
    path("api/auth/", include("core.urls")),
    # Health/home endpoint
    path("", core_views.home, name="home"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
