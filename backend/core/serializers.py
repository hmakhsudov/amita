from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import (
    Booking,
    FavoriteService,
    Message,
    Plan,
    PlanItem,
    Service,
    ServiceCategory,
    UserProfile,
)

User = get_user_model()


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    name = serializers.CharField()
    phone = serializers.CharField(required=False, allow_blank=True)
    role = serializers.ChoiceField(
        choices=UserProfile.ROLE_CHOICES,
        required=False,
        default=UserProfile.ROLE_CLIENT,
    )

    def validate_email(self, value: str) -> str:
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Пользователь с таким email уже существует.")
        return value

    def validate_role(self, value: str) -> str:
        if value != UserProfile.ROLE_CLIENT:
            raise serializers.ValidationError("Регистрация администраторов отключена.")
        return value

    def create(self, validated_data):
        email = validated_data["email"].lower()
        user = User.objects.create_user(
            username=email,
            email=email,
            password=validated_data["password"],
        )
        UserProfile.objects.create(
            user=user,
            full_name=validated_data.get("name", ""),
            phone=validated_data.get("phone", ""),
            role=UserProfile.ROLE_CLIENT,
        )
        return user


class UserMeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    email = serializers.EmailField()
    name = serializers.CharField(source="profile.full_name", allow_blank=True)
    phone = serializers.CharField(source="profile.phone", allow_blank=True)
    role = serializers.CharField(source="profile.role")
    avatar_url = serializers.SerializerMethodField()

    def get_avatar_url(self, obj):
        profile = getattr(obj, "profile", None)
        if not profile or not profile.avatar:
            return ""
        request = self.context.get("request")
        url = profile.avatar.url
        return request.build_absolute_uri(url) if request else url


class UserMeUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(required=False, allow_blank=True)
    phone = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False)
    avatar = serializers.ImageField(required=False, allow_null=True)

    def update(self, instance, validated_data):
        profile = getattr(instance, "profile", None)
        if not profile:
            default_role = (
                UserProfile.ROLE_ADMIN if instance.is_superuser else UserProfile.ROLE_CLIENT
            )
            profile = UserProfile.objects.create(user=instance, role=default_role)

        if "name" in validated_data:
            profile.full_name = validated_data.get("name", "")
        if "phone" in validated_data:
            profile.phone = validated_data.get("phone", "")
        if "avatar" in validated_data:
            profile.avatar = validated_data.get("avatar")
        profile.save()

        if "email" in validated_data:
            instance.email = validated_data["email"]
            instance.username = validated_data["email"]
            instance.save(update_fields=["email", "username"])

        return instance


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = ["id", "name", "description"]


class MasterSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    avatar_url = serializers.SerializerMethodField()
    phone = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "name", "avatar_url", "phone"]

    def get_name(self, obj):
        profile = getattr(obj, "profile", None)
        return (
            (profile.full_name if profile else "")
            or obj.get_full_name()
            or obj.email
        )

    def get_avatar_url(self, obj):
        profile = getattr(obj, "profile", None)
        if not profile or not profile.avatar:
            return ""
        request = self.context.get("request")
        url = profile.avatar.url
        return request.build_absolute_uri(url) if request else url

    def get_phone(self, obj):
        profile = getattr(obj, "profile", None)
        return profile.phone if profile else ""


class ServiceSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=ServiceCategory.objects.all(),
        source="category",
        write_only=True,
    )
    masters = MasterSerializer(many=True, read_only=True)
    masters_ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(profile__role=UserProfile.ROLE_MASTER),
        source="masters",
        many=True,
        write_only=True,
        required=False,
    )

    class Meta:
        model = Service
        fields = [
            "id",
            "name",
            "description",
            "price",
            "duration_minutes",
            "category",
            "category_id",
            "masters",
            "masters_ids",
        ]
        extra_kwargs = {
            "duration_minutes": {"required": False},
        }


class FavoriteServiceItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Service
        fields = ["id", "name", "description", "price", "category"]


class FavoriteServiceSerializer(serializers.ModelSerializer):
    service = FavoriteServiceItemSerializer(read_only=True)

    class Meta:
        model = FavoriteService
        fields = ["id", "service", "created_at"]


class FavoriteServiceCreateSerializer(serializers.Serializer):
    service_id = serializers.PrimaryKeyRelatedField(
        queryset=Service.objects.all(),
        source="service",
    )


class PlanServiceSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Service
        fields = ["id", "name", "price", "category"]


class PlanItemSerializer(serializers.ModelSerializer):
    service = PlanServiceSerializer(read_only=True)

    class Meta:
        model = PlanItem
        fields = ["id", "qty", "service"]


class PlanSerializer(serializers.ModelSerializer):
    items = PlanItemSerializer(many=True, read_only=True)
    total_count = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Plan
        fields = ["items", "total_count", "total_price"]

    def get_total_count(self, obj):
        return sum(item.qty for item in obj.items.all())

    def get_total_price(self, obj):
        total = 0
        for item in obj.items.all():
            total += item.service.price * item.qty
        return total


class PlanItemCreateSerializer(serializers.Serializer):
    service_id = serializers.PrimaryKeyRelatedField(
        queryset=Service.objects.all(),
        source="service",
    )
    qty = serializers.IntegerField(min_value=1, default=1)


class PlanItemUpdateSerializer(serializers.Serializer):
    qty = serializers.IntegerField(min_value=1)


class BookingServiceSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Service
        fields = ["id", "name", "price", "duration_minutes", "category"]


class BookingSerializer(serializers.ModelSerializer):
    service = BookingServiceSerializer(read_only=True)
    master = MasterSerializer(read_only=True)
    client_id = serializers.IntegerField(source="user_id", read_only=True)

    class Meta:
        model = Booking
        fields = [
            "id",
            "service",
            "master",
            "client_id",
            "start_at",
            "end_at",
            "status",
            "comment",
            "client_name",
            "client_phone",
            "client_email",
            "created_at",
        ]


class BookingCreateSerializer(serializers.Serializer):
    service_id = serializers.PrimaryKeyRelatedField(
        queryset=Service.objects.all(),
        source="service",
    )
    master_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(profile__role=UserProfile.ROLE_MASTER),
        source="master",
    )
    start_at = serializers.DateTimeField()
    comment = serializers.CharField(required=False, allow_blank=True)
    client_name = serializers.CharField(required=False, allow_blank=True)
    client_phone = serializers.CharField(required=False, allow_blank=True)
    client_email = serializers.EmailField(required=False, allow_blank=True)


class UserCompactSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    role = serializers.CharField()
    avatar_url = serializers.CharField()


class ConversationListSerializer(serializers.Serializer):
    counterpart = UserCompactSerializer(read_only=True)
    last_message_preview = serializers.CharField(read_only=True)
    unread_count = serializers.IntegerField(read_only=True)
    id = serializers.UUIDField()
    last_message_at = serializers.DateTimeField(allow_null=True)


class MessageSerializer(serializers.ModelSerializer):
    sender_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Message
        fields = ["id", "sender_id", "body", "created_at", "read_at"]


class AdminUserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    phone = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "name",
            "phone",
            "role",
            "avatar_url",
            "is_active",
            "date_joined",
        ]

    def get_name(self, obj):
        profile = getattr(obj, "profile", None)
        if profile and profile.full_name:
            return profile.full_name
        return obj.get_full_name() or obj.email

    def get_phone(self, obj):
        profile = getattr(obj, "profile", None)
        return profile.phone if profile else ""

    def get_role(self, obj):
        profile = getattr(obj, "profile", None)
        return profile.role if profile else ""

    def get_avatar_url(self, obj):
        profile = getattr(obj, "profile", None)
        if not profile or not profile.avatar:
            return ""
        request = self.context.get("request")
        url = profile.avatar.url
        return request.build_absolute_uri(url) if request else url
