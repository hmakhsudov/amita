from django.urls import path

from .ai_views import AiChatView

urlpatterns = [
    path("ai/chat/", AiChatView.as_view(), name="ai-chat"),
]
