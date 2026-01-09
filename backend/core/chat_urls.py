from django.urls import path

from .chat_views import (
    ConversationListView,
    ConversationMessagesView,
    ConversationReadView,
    ConversationUnreadCountView,
)

urlpatterns = [
    path("conversations/", ConversationListView.as_view(), name="conversation-list"),
    path(
        "conversations/unread_count/",
        ConversationUnreadCountView.as_view(),
        name="conversation-unread-count",
    ),
    path(
        "conversations/<uuid:pk>/messages/",
        ConversationMessagesView.as_view(),
        name="conversation-messages",
    ),
    path(
        "conversations/<uuid:pk>/read/",
        ConversationReadView.as_view(),
        name="conversation-read",
    ),
]
