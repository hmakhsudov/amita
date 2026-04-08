from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db.models import Count, Sum
from django.utils import timezone
from rest_framework import permissions, serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Booking, UserProfile
from .permissions import IsAdminOnly
from .serializers import AdminUserSerializer, BookingSerializer

User = get_user_model()


class AdminDashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdminOnly]

    def get(self, request):
        today = timezone.localdate()
        total_revenue = (
            Booking.objects.filter(status=Booking.STATUS_COMPLETED).aggregate(
                total=Sum("service__price")
            )["total"]
            or Decimal("0")
        )
        popular_services = (
            Booking.objects.values("service_id", "service__name")
            .annotate(bookings_count=Count("id"))
            .order_by("-bookings_count", "service__name")[:5]
        )
        payload = {
            "total_users": User.objects.count(),
            "total_bookings": Booking.objects.count(),
            "today_bookings": Booking.objects.filter(start_at__date=today).count(),
            "total_revenue": float(total_revenue),
            "popular_services": [
                {
                    "service_id": item["service_id"],
                    "name": item["service__name"],
                    "bookings_count": item["bookings_count"],
                }
                for item in popular_services
            ],
        }
        return Response(payload)


class AdminBookingListView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdminOnly]

    def get(self, request):
        queryset = (
            Booking.objects.select_related(
                "service",
                "service__category",
                "master",
                "master__profile",
                "user",
                "user__profile",
            )
            .all()
            .order_by("-start_at")
        )
        return Response(
            BookingSerializer(queryset, many=True, context={"request": request}).data
        )


class AdminBookingStatusView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdminOnly]

    def patch(self, request, pk):
        booking = Booking.objects.filter(pk=pk).first()
        if not booking:
            return Response({"detail": "Запись не найдена."}, status=status.HTTP_404_NOT_FOUND)
        status_value = request.data.get("status")
        allowed = {
            Booking.STATUS_SCHEDULED,
            Booking.STATUS_CANCELLED,
            Booking.STATUS_COMPLETED,
        }
        if status_value not in allowed:
            return Response(
                {"detail": "Некорректный статус."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        booking.status = status_value
        booking.save(update_fields=["status", "updated_at"])
        booking = Booking.objects.select_related(
            "service",
            "service__category",
            "master",
            "master__profile",
        ).get(pk=pk)
        return Response(BookingSerializer(booking, context={"request": request}).data)


class AdminUserListView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdminOnly]

    def get(self, request):
        queryset = (
            User.objects.select_related("profile")
            .all()
            .order_by("-date_joined")
        )
        serializer = AdminUserSerializer(
            queryset,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)

    def post(self, request):
        email = (request.data.get("email") or "").strip().lower()
        password = request.data.get("password") or ""
        name = (request.data.get("name") or "").strip()
        phone = (request.data.get("phone") or "").strip()

        if not email:
            raise serializers.ValidationError({"email": "Email обязателен."})
        if User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError({"email": "Пользователь уже существует."})
        if len(password) < 8:
            raise serializers.ValidationError(
                {"password": "Пароль должен быть не короче 8 символов."}
            )

        user = User.objects.create_user(username=email, email=email, password=password)
        UserProfile.objects.create(
            user=user,
            full_name=name,
            phone=phone,
            role=UserProfile.ROLE_MASTER,
        )
        serialized = AdminUserSerializer(user, context={"request": request})
        return Response(serialized.data, status=status.HTTP_201_CREATED)
