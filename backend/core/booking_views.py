from datetime import datetime, time, timedelta

from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Booking, Service, UserProfile
from .permissions import IsBookingOwnerOrMaster, IsClientRole
from .serializers import BookingCreateSerializer, BookingSerializer


def _ensure_aware(value):
    if timezone.is_naive(value):
        return timezone.make_aware(value, timezone.get_current_timezone())
    return value


def _is_master(user) -> bool:
    profile = getattr(user, "profile", None)
    return bool(profile and profile.role == UserProfile.ROLE_MASTER)


class BookingListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        qs = Booking.objects.select_related(
            "service",
            "service__category",
            "master",
            "master__profile",
        ).filter(user=request.user)
        qs = qs.order_by("-start_at")
        return Response(BookingSerializer(qs, many=True, context={"request": request}).data)

    def post(self, request):
        serializer = BookingCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = serializer.validated_data["service"]
        master = serializer.validated_data["master"]
        start_at = _ensure_aware(serializer.validated_data["start_at"])
        now = timezone.now()
        if start_at < now:
            return Response(
                {"detail": "Нельзя создать запись в прошлом."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        duration = service.duration_minutes or 60
        end_at = start_at + timedelta(minutes=duration)

        overlaps = Booking.objects.filter(
            status=Booking.STATUS_SCHEDULED,
            master=master,
            start_at__lt=end_at,
            end_at__gt=start_at,
        ).exists()
        if overlaps:
            return Response(
                {"detail": "Это время уже занято, выберите другое."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not getattr(master, "profile", None) or master.profile.role != UserProfile.ROLE_MASTER:
            return Response(
                {"detail": "Выберите корректного мастера."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not service.masters.filter(id=master.id).exists():
            return Response(
                {"detail": "Выбранный мастер не оказывает эту услугу."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        profile = getattr(request.user, "profile", None)
        client_name = (
            serializer.validated_data.get("client_name")
            or (profile.full_name if profile else "")
            or request.user.get_full_name()
            or request.user.email
        )
        client_phone = serializer.validated_data.get("client_phone") or (
            profile.phone if profile else ""
        )
        client_email = (
            serializer.validated_data.get("client_email") or request.user.email or ""
        )

        booking = Booking.objects.create(
            user=request.user,
            service=service,
            master=master,
            start_at=start_at,
            end_at=end_at,
            status=Booking.STATUS_SCHEDULED,
            client_name=client_name,
            client_phone=client_phone,
            client_email=client_email,
            comment=serializer.validated_data.get("comment", ""),
        )
        booking = Booking.objects.select_related(
            "service",
            "service__category",
            "master",
            "master__profile",
        ).get(pk=booking.pk)
        return Response(
            BookingSerializer(booking, context={"request": request}).data,
            status=status.HTTP_201_CREATED,
        )


class BookingHistoryView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsClientRole]

    def get(self, request):
        qs = (
            Booking.objects.select_related(
                "service",
                "service__category",
                "master",
                "master__profile",
            )
            .filter(user=request.user, status=Booking.STATUS_COMPLETED)
            .order_by("-start_at")
        )
        return Response(BookingSerializer(qs, many=True, context={"request": request}).data)


class BookingDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsBookingOwnerOrMaster]

    def get_object(self, request, pk):
        booking = get_object_or_404(
            Booking.objects.select_related(
                "service",
                "service__category",
                "master",
                "master__profile",
            ),
            pk=pk,
        )
        self.check_object_permissions(request, booking)
        return booking

    def get(self, request, pk):
        booking = self.get_object(request, pk)
        return Response(BookingSerializer(booking, context={"request": request}).data)


class BookingCancelView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsBookingOwnerOrMaster]

    def post(self, request, pk):
        booking = get_object_or_404(Booking, pk=pk)
        self.check_object_permissions(request, booking)
        if booking.status == Booking.STATUS_COMPLETED:
            return Response(
                {"detail": "Нельзя отменить завершённую запись."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if booking.status == Booking.STATUS_CANCELLED:
            return Response(
                {"detail": "Запись уже отменена."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        booking.status = Booking.STATUS_CANCELLED
        booking.save(update_fields=["status", "updated_at"])
        booking = Booking.objects.select_related(
            "service",
            "service__category",
            "master",
            "master__profile",
        ).get(pk=pk)
        return Response(BookingSerializer(booking, context={"request": request}).data)


class AvailabilityView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        date_str = request.query_params.get("date")
        service_id = request.query_params.get("service_id")
        master_id = request.query_params.get("master_id")
        if not date_str or not service_id or not master_id:
            return Response(
                {"detail": "Необходимо указать date, service_id и master_id."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return Response(
                {"detail": "Неверный формат даты. Используйте YYYY-MM-DD."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        service = get_object_or_404(Service, pk=service_id)
        master = get_object_or_404(service.masters.select_related("profile"), pk=master_id)
        if not getattr(master, "profile", None) or master.profile.role != UserProfile.ROLE_MASTER:
            return Response(
                {"detail": "Неверный мастер."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        duration = service.duration_minutes or 60

        tz = timezone.get_current_timezone()
        day_start = timezone.make_aware(datetime.combine(selected_date, time(10, 0)), tz)
        day_end = timezone.make_aware(datetime.combine(selected_date, time(20, 0)), tz)

        existing = list(
            Booking.objects.filter(
                status=Booking.STATUS_SCHEDULED,
                master=master,
                start_at__lt=day_end,
                end_at__gt=day_start,
            ).only("start_at", "end_at")
        )

        slot_step = timedelta(minutes=30)
        slots = []
        cursor = day_start
        now = timezone.now()
        while cursor + timedelta(minutes=duration) <= day_end:
            slot_end = cursor + timedelta(minutes=duration)
            if cursor >= now:
                conflict = any(
                    booking.start_at < slot_end and booking.end_at > cursor for booking in existing
                )
                if not conflict:
                    slots.append(cursor.isoformat())
            cursor += slot_step

        return Response({"slots": slots})


class MasterBookingListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if not _is_master(request.user):
            return Response({"detail": "Недостаточно прав."}, status=status.HTTP_403_FORBIDDEN)
        qs = Booking.objects.select_related(
            "service",
            "service__category",
            "master",
            "master__profile",
        ).filter(master=request.user)
        return Response(
            BookingSerializer(qs.order_by("-start_at"), many=True, context={"request": request}).data
        )


class MasterBookingStatusView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        if not _is_master(request.user):
            return Response({"detail": "Недостаточно прав."}, status=status.HTTP_403_FORBIDDEN)
        booking = get_object_or_404(Booking, pk=pk, master=request.user)
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
        if booking.status == Booking.STATUS_COMPLETED and status_value != Booking.STATUS_COMPLETED:
            return Response(
                {"detail": "Нельзя изменить завершённую запись."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        booking.status = status_value
        booking.save(update_fields=["status", "updated_at"])
        booking = Booking.objects.select_related(
            "service",
            "service__category",
            "master",
            "master__profile",
        ).get(pk=booking.pk)
        return Response(BookingSerializer(booking, context={"request": request}).data)
