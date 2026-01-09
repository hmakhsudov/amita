from django.urls import path

from .booking_views import (
    AvailabilityView,
    BookingCancelView,
    BookingDetailView,
    BookingHistoryView,
    BookingListCreateView,
    MasterBookingListView,
    MasterBookingStatusView,
)

urlpatterns = [
    path("bookings/", BookingListCreateView.as_view(), name="booking-list-create"),
    path("bookings/history/", BookingHistoryView.as_view(), name="booking-history"),
    path("bookings/<int:pk>/", BookingDetailView.as_view(), name="booking-detail"),
    path("bookings/<int:pk>/cancel/", BookingCancelView.as_view(), name="booking-cancel"),
    path("availability/", AvailabilityView.as_view(), name="availability"),
    path("master/bookings/", MasterBookingListView.as_view(), name="master-bookings"),
    path("master/bookings/<int:pk>/status/", MasterBookingStatusView.as_view(), name="master-booking-status"),
]
