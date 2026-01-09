from django.urls import path

from .plan_views import PlanClearView, PlanDetailView, PlanItemCreateView, PlanItemDetailView

urlpatterns = [
    path("", PlanDetailView.as_view(), name="plan-detail"),
    path("items/", PlanItemCreateView.as_view(), name="plan-item-create"),
    path("items/<int:pk>/", PlanItemDetailView.as_view(), name="plan-item-detail"),
    path("clear/", PlanClearView.as_view(), name="plan-clear"),
]
