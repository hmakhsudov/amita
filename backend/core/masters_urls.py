from django.urls import path

from .masters_views import MasterListView

urlpatterns = [
    path("masters/", MasterListView.as_view(), name="masters-list"),
]
