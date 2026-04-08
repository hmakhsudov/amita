from datetime import datetime

from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Conversation, Message, UserProfile
from .serializers import ConversationListSerializer, MessageSerializer

User = get_user_model()


def _get_role(user):
    profile = getattr(user, "profile", None)
    return profile.role if profile else ""


def _is_master(user):
    return _get_role(user) == UserProfile.ROLE_MASTER


def _is_client(user):
    return _get_role(user) == UserProfile.ROLE_CLIENT


def _user_display(user, request):
    profile = getattr(user, "profile", None)
    name = ""
    if profile and profile.full_name:
        name = profile.full_name
    elif user.get_full_name():
        name = user.get_full_name()
    else:
        name = user.email
    avatar_url = ""
    if profile and profile.avatar:
        url = profile.avatar.url
        avatar_url = request.build_absolute_uri(url) if request else url
    return {
        "id": user.id,
        "name": name,
        "role": profile.role if profile else "",
        "avatar_url": avatar_url,
    }


def _get_conversation_for_user(user, conversation_id):
    qs = Conversation.objects.filter(Q(client=user) | Q(master=user))
    return get_object_or_404(qs, id=conversation_id)


class ConversationListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        conversations = (
            Conversation.objects.select_related(
                "client",
                "client__profile",
                "master",
                "master__profile",
            )
            .filter(Q(client=request.user) | Q(master=request.user))
            .order_by("-last_message_at", "-updated_at")
        )
        items = []
        for conv in conversations:
            counterpart = conv.master if conv.client_id == request.user.id else conv.client
            last_message = conv.messages.order_by("-created_at").first()
            unread_count = conv.messages.filter(
                read_at__isnull=True
            ).exclude(sender=request.user).count()
            items.append(
                {
                    "id": conv.id,
                    "counterpart": _user_display(counterpart, request),
                    "last_message_preview": last_message.body[:120] if last_message else "",
                    "last_message_at": conv.last_message_at,
                    "unread_count": unread_count,
                }
            )
        serializer = ConversationListSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request):
        counterpart_id = request.data.get("counterpart_user_id")
        if not counterpart_id:
            return Response(
                {"detail": "counterpart_user_id обязателен."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        counterpart = get_object_or_404(User, id=counterpart_id)
        if _is_client(request.user) and _is_master(counterpart):
            client = request.user
            master = counterpart
        elif _is_master(request.user) and _is_client(counterpart):
            client = counterpart
            master = request.user
        else:
            return Response(
                {"detail": "Можно общаться только между клиентом и мастером."},
                status=status.HTTP_403_FORBIDDEN,
            )
        conversation, _ = Conversation.objects.get_or_create(client=client, master=master)
        counterpart_user = master if conversation.client_id == request.user.id else client
        last_message = conversation.messages.order_by("-created_at").first()
        unread_count = conversation.messages.filter(
            read_at__isnull=True
        ).exclude(sender=request.user).count()
        payload = {
            "id": conversation.id,
            "counterpart": _user_display(counterpart_user, request),
            "last_message_preview": last_message.body[:120] if last_message else "",
            "last_message_at": conversation.last_message_at,
            "unread_count": unread_count,
        }
        serializer = ConversationListSerializer(payload)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ConversationMessagesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        conversation = _get_conversation_for_user(request.user, pk)
        limit = int(request.query_params.get("limit", 50))
        limit = max(1, min(limit, 100))
        before = request.query_params.get("before")
        qs = conversation.messages.all()
        if before:
            try:
                before_dt = datetime.fromisoformat(before)
                if timezone.is_naive(before_dt):
                    before_dt = timezone.make_aware(before_dt, timezone.get_current_timezone())
                qs = qs.filter(created_at__lt=before_dt)
            except ValueError:
                return Response(
                    {"detail": "Неверный формат даты before."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        messages = list(qs.order_by("-created_at")[:limit])
        messages.reverse()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        conversation = _get_conversation_for_user(request.user, pk)
        body = (request.data.get("body") or "").strip()
        if not body:
            return Response(
                {"detail": "Сообщение не может быть пустым."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if request.user.id not in [conversation.client_id, conversation.master_id]:
            return Response({"detail": "Недостаточно прав."}, status=status.HTTP_403_FORBIDDEN)
        message = Message.objects.create(
            conversation=conversation,
            sender=request.user,
            body=body,
        )
        conversation.last_message_at = message.created_at
        conversation.save(update_fields=["last_message_at", "updated_at"])
        return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)


class ConversationReadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        conversation = _get_conversation_for_user(request.user, pk)
        updated = conversation.messages.filter(
            read_at__isnull=True
        ).exclude(sender=request.user).update(read_at=timezone.now())
        return Response({"ok": True, "updated": updated})


class ConversationUnreadCountView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        conversations = Conversation.objects.filter(
            Q(client=request.user) | Q(master=request.user)
        )
        count = Message.objects.filter(
            conversation__in=conversations,
            read_at__isnull=True,
        ).exclude(sender=request.user).count()
        return Response({"unread_count": count})
