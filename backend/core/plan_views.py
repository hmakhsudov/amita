from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Plan, PlanItem
from .serializers import PlanItemCreateSerializer, PlanItemUpdateSerializer, PlanSerializer


def _get_plan_with_items(user):
    plan, _ = Plan.objects.get_or_create(user=user)
    return (
        Plan.objects.prefetch_related("items__service__category")
        .select_related("user")
        .get(pk=plan.pk)
    )


class PlanDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        plan = _get_plan_with_items(request.user)
        return Response(PlanSerializer(plan).data)


class PlanItemCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = PlanItemCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        plan, _ = Plan.objects.get_or_create(user=request.user)
        service = serializer.validated_data["service"]
        qty = serializer.validated_data.get("qty", 1)

        item, created = PlanItem.objects.get_or_create(
            plan=plan,
            service=service,
            defaults={"qty": qty},
        )
        if not created:
            item.qty += qty
            item.save(update_fields=["qty"])

        plan = _get_plan_with_items(request.user)
        return Response(PlanSerializer(plan).data, status=status.HTTP_201_CREATED)


class PlanItemDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        serializer = PlanItemUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        item = get_object_or_404(
            PlanItem.objects.select_related("plan"),
            pk=pk,
            plan__user=request.user,
        )
        item.qty = serializer.validated_data["qty"]
        item.save(update_fields=["qty"])
        plan = _get_plan_with_items(request.user)
        return Response(PlanSerializer(plan).data)

    def delete(self, request, pk):
        item = get_object_or_404(
            PlanItem.objects.select_related("plan"),
            pk=pk,
            plan__user=request.user,
        )
        item.delete()
        plan = _get_plan_with_items(request.user)
        return Response(PlanSerializer(plan).data)


class PlanClearView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        plan, _ = Plan.objects.get_or_create(user=request.user)
        plan.items.all().delete()
        plan = _get_plan_with_items(request.user)
        return Response(PlanSerializer(plan).data)
