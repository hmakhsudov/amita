from django.contrib import admin

from .models import (
    AiConversation,
    AiMessage,
    Booking,
    Client,
    Conversation,
    FavoriteService,
    Message,
    Plan,
    PlanItem,
    Service,
    ServiceCategory,
    UserProfile,
)


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "duration_minutes", "price")
    list_filter = ("category",)
    search_fields = ("name",)
    filter_horizontal = ("masters",)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone")
    search_fields = ("name", "email")


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "full_name", "phone", "role")
    list_filter = ("role",)
    search_fields = ("user__email", "full_name", "phone")


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ("user", "updated_at")
    search_fields = ("user__email",)


@admin.register(PlanItem)
class PlanItemAdmin(admin.ModelAdmin):
    list_display = ("plan", "service", "qty", "created_at")
    search_fields = ("plan__user__email", "service__name")


@admin.register(FavoriteService)
class FavoriteServiceAdmin(admin.ModelAdmin):
    list_display = ("user", "service", "created_at")
    search_fields = ("user__email", "service__name")


@admin.register(AiConversation)
class AiConversationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "updated_at")
    search_fields = ("id", "user__email")


@admin.register(AiMessage)
class AiMessageAdmin(admin.ModelAdmin):
    list_display = ("conversation", "role", "created_at")
    search_fields = ("conversation__id", "content")


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ("id", "client", "master", "last_message_at", "updated_at")
    search_fields = ("id", "client__email", "master__email")


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("conversation", "sender", "created_at", "read_at")
    search_fields = ("conversation__id", "sender__email", "body")


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("service", "master", "start_at", "status", "client_name", "client_email")
    list_filter = ("status", "service", "master")
    search_fields = ("client_name", "client_email", "service__name")
