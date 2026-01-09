from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import MasterSerializer

User = get_user_model()


class MasterListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        masters = User.objects.filter(profile__role="admin").select_related("profile")
        return Response(MasterSerializer(masters, many=True, context={"request": request}).data)
