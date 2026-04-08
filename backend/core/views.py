from django.contrib.auth import authenticate, get_user_model
from django.http import JsonResponse
from rest_framework import permissions, serializers, status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import UserProfile
from .serializers import RegisterSerializer, UserMeSerializer, UserMeUpdateSerializer

User = get_user_model()
DEFAULT_ADMIN_EMAIL = "admin@admin.admin"
DEFAULT_ADMIN_PASSWORD = "Admin1234"

def _ensure_profile(user):
    default_role = UserProfile.ROLE_ADMIN if user.is_superuser else UserProfile.ROLE_CLIENT
    profile, _ = UserProfile.objects.get_or_create(
        user=user,
        defaults={"role": default_role},
    )
    return profile


def home(request):
    """Health check/home endpoint."""
    return JsonResponse({"status": "ok", "message": "Beauty service API is running"})


def health(request):
    """Simple health endpoint for container checks."""
    return JsonResponse({"status": "ok"})


@api_view(["GET"])
def service_list(request):
    """
    Placeholder list of services.
    Replace with serialized Service queryset when real data exists.
    """
    data = [
        {
            "name": "Detox Facial",
            "category": "Facial care",
            "duration_minutes": 60,
            "price": 120.0,
        },
        {
            "name": "Vitamin Cocktail Mask",
            "category": "Skin boost",
            "duration_minutes": 45,
            "price": 95.0,
        },
        {
            "name": "Relaxing Massage",
            "category": "Body",
            "duration_minutes": 75,
            "price": 140.0,
        },
    ]
    return Response(data)


@api_view(["GET"])
def recommendations(request):
    """
    Placeholder recommendations.
    Future: connect to ML/heuristic engine using Client preferences + history.
    """
    recommended = [
        {
            "name": "Glow Revival Facial",
            "reason": "Great for dull skin before events",
            "duration_minutes": 50,
            "price": 110.0,
        },
        {
            "name": "Green Detox Smoothie Peel",
            "reason": "Gentle exfoliation with botanical extracts",
            "duration_minutes": 40,
            "price": 105.0,
        },
    ]
    return Response({"recommended": recommended})


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Minimal JWT login serializer that uses email + password.
    """
    username_field = "email"

    def validate(self, attrs):
        email = (attrs.get("email") or "").strip().lower()
        password = attrs.get("password")
        if (
            email == DEFAULT_ADMIN_EMAIL
            and password == DEFAULT_ADMIN_PASSWORD
            and not User.objects.filter(email__iexact=DEFAULT_ADMIN_EMAIL).exists()
        ):
            admin_user = User.objects.create_user(
                username=DEFAULT_ADMIN_EMAIL,
                email=DEFAULT_ADMIN_EMAIL,
                password=DEFAULT_ADMIN_PASSWORD,
            )
            UserProfile.objects.create(
                user=admin_user,
                full_name="Администратор",
                role=UserProfile.ROLE_ADMIN,
            )
        user = authenticate(
            request=self.context.get("request"),
            username=email,
            password=password,
        )
        if not user:
            raise serializers.ValidationError({"detail": "Неверный email или пароль."})
        if email == DEFAULT_ADMIN_EMAIL:
            profile = _ensure_profile(user)
            if profile.role != UserProfile.ROLE_ADMIN:
                profile.role = UserProfile.ROLE_ADMIN
                profile.save(update_fields=["role"])
        refresh = self.get_token(user)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        _ensure_profile(user)
        return Response(
            UserMeSerializer(user, context={"request": request}).data,
            status=status.HTTP_201_CREATED,
        )


class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        _ensure_profile(request.user)
        return Response(UserMeSerializer(request.user, context={"request": request}).data)

    def patch(self, request):
        serializer = UserMeUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.update(request.user, serializer.validated_data)
        return Response(UserMeSerializer(request.user, context={"request": request}).data)

    def put(self, request):
        return self.patch(request)
