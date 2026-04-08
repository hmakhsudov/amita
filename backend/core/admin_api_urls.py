from django.urls import path

from .admin_api_views import (
    AdminBookingListView,
    AdminBookingStatusView,
    AdminDashboardView,
    AdminUserListView,
)

urlpatterns = [
    path("dashboard/", AdminDashboardView.as_view(), name="admin-dashboard"),
    path("bookings/", AdminBookingListView.as_view(), name="admin-bookings"),
    path(
        "bookings/<int:pk>/status/",
        AdminBookingStatusView.as_view(),
        name="admin-booking-status",
    ),
    path("users/", AdminUserListView.as_view(), name="admin-users"),
]
