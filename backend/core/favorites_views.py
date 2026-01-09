from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import FavoriteService
from .permissions import IsClientRole
from .serializers import FavoriteServiceCreateSerializer, FavoriteServiceSerializer


def _get_favorites_qs(user):
    return FavoriteService.objects.select_related(
        "service",
        "service__category",
    ).filter(user=user)


class FavoriteListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsClientRole]

    def get(self, request):
        favorites = _get_favorites_qs(request.user).order_by("-created_at")
        return Response(FavoriteServiceSerializer(favorites, many=True).data)

    def post(self, request):
        serializer = FavoriteServiceCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = serializer.validated_data["service"]
        favorite, _ = FavoriteService.objects.get_or_create(
            user=request.user,
            service=service,
        )
        favorite = _get_favorites_qs(request.user).get(pk=favorite.pk)
        return Response(
            FavoriteServiceSerializer(favorite).data,
            status=status.HTTP_201_CREATED,
        )


class FavoriteDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsClientRole]

    def delete(self, request, pk):
        favorite = get_object_or_404(FavoriteService, pk=pk, user=request.user)
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
