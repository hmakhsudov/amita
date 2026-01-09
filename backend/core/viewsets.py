from rest_framework import viewsets

from .models import Service, ServiceCategory
from .permissions import IsAdminRoleOrReadOnly, IsServiceMasterOrAdmin
from .serializers import CategorySerializer, ServiceSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = ServiceCategory.objects.all().order_by("name")
    serializer_class = CategorySerializer
    permission_classes = [IsAdminRoleOrReadOnly]


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = (
        Service.objects.select_related("category")
        .prefetch_related("masters", "masters__profile")
        .all()
        .order_by("name")
    )
    serializer_class = ServiceSerializer
    permission_classes = [IsServiceMasterOrAdmin]

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.request.query_params.get("category")
        master_id = self.request.query_params.get("master")
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        if master_id:
            queryset = queryset.filter(masters__id=master_id)
        return queryset.distinct()
