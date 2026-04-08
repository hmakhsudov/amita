import json
import logging
import os
from typing import Dict, List

from django.utils import timezone
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

from .models import AiConversation, AiMessage, Booking, Plan, Service, UserProfile

logger = logging.getLogger(__name__)

MODEL_DEFAULT = "gpt-4.1-mini"
MAX_HISTORY_MESSAGES = 10

SEVERE_KEYWORDS = [
    "кров",
    "кровотеч",
    "сильн",
    "нестерп",
    "гной",
    "инфекц",
    "температур",
    "жар",
    "аллерг",
    "отек",
    "опух",
    "ожог",
    "язв",
    "сыпь",
    "боль",
]


def _get_openai_client():
    if OpenAI is None:
        return None
    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key:
        return None
    return OpenAI(api_key=api_key)


def _build_catalog(services: List[Service]) -> str:
    lines = ["SERVICES CATALOG (only these can be recommended):"]
    for service in services:
        category = service.category.name if service.category else "Без категории"
        description = (service.description or "").strip()
        if len(description) > 160:
            description = f"{description[:157]}..."
        master_names = []
        for master in service.masters.all()[:3]:
            profile = getattr(master, "profile", None)
            master_names.append(profile.full_name if profile and profile.full_name else master.email)
        masters_line = f"Мастера: {', '.join(master_names)}" if master_names else "Мастера: нет"
        lines.append(
            f"[id={service.id}] {service.name} — категория: {category}; цена: {service.price} €; "
            f"длительность: {service.duration_minutes} мин; {masters_line}. "
            f"Описание: {description or '—'}"
        )
    return "\n".join(lines)


def _build_client_context(user) -> str:
    profile = getattr(user, "profile", None)
    if not profile or profile.role != UserProfile.ROLE_CLIENT:
        return ""
    plan_items = []
    plan = Plan.objects.filter(user=user).prefetch_related("items__service").first()
    if plan:
        for item in plan.items.all():
            plan_items.append(f"{item.service.name} x{item.qty}")
    history_items = (
        Booking.objects.filter(user=user, status=Booking.STATUS_COMPLETED)
        .select_related("service")
        .order_by("-start_at")[:5]
    )
    history_list = [f"{item.service.name} ({item.start_at:%Y-%m-%d})" for item in history_items]
    plan_text = ", ".join(plan_items) if plan_items else "пусто"
    history_text = ", ".join(history_list) if history_list else "пусто"
    return f"CLIENT CONTEXT: plan=[{plan_text}], completed_visits=[{history_text}]"


def _build_messages(
    conversation: AiConversation,
    user_message: str,
    system_context: str,
    json_mode: bool = False,
) -> List[Dict]:
    json_instruction = (
        "Отвечай строго валидным JSON без пояснений, без Markdown и без оберток."
        if json_mode
        else ""
    )
    messages = [
        {
            "role": "system",
            "content": (
                "Ты — профессиональный косметолог и специалист по здоровому образу жизни. "
                "Отвечай по-русски, дружелюбно и бережно. Не ставь диагнозов и не обещай лечение. "
                "Рекомендуй ТОЛЬКО услуги из каталога ниже. Всегда добавляй короткую дисклеймер-заметку "
                "о том, что это не медицинская консультация. "
                "Поле follow_up_questions заполняй как короткие варианты ответа клиента (утверждения), "
                "а не вопросы."
            ),
        },
        *( [{"role": "system", "content": json_instruction}] if json_instruction else [] ),
        {
            "role": "system",
            "content": system_context,
        },
    ]
    history = (
        AiMessage.objects.filter(conversation=conversation)
        .order_by("-created_at")[:MAX_HISTORY_MESSAGES]
    )
    for msg in reversed(list(history)):
        messages.append({"role": msg.role, "content": msg.content})
    messages.append({"role": "user", "content": user_message})
    return messages


def _severe_symptoms(message: str) -> bool:
    lowered = message.lower()
    return any(keyword in lowered for keyword in SEVERE_KEYWORDS)


class AiChatView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        message = (request.data.get("message") or "").strip()
        if not message:
            return Response(
                {"detail": "Сообщение не может быть пустым."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        conversation_id = request.data.get("conversation_id") or ""
        conversation = None
        if conversation_id:
            try:
                conversation = AiConversation.objects.get(id=conversation_id)
            except (AiConversation.DoesNotExist, ValueError, TypeError):
                conversation = None

        if conversation and conversation.user:
            if not request.user.is_authenticated or conversation.user_id != request.user.id:
                conversation = None

        if conversation is None:
            conversation = AiConversation.objects.create(
                user=request.user if request.user.is_authenticated else None
            )
        elif request.user.is_authenticated and conversation.user is None:
            conversation.user = request.user
            conversation.save(update_fields=["user", "updated_at"])

        AiMessage.objects.create(
            conversation=conversation,
            role=AiMessage.ROLE_USER,
            content=message,
        )

        services = (
            Service.objects.select_related("category")
            .prefetch_related("masters", "masters__profile")
            .all()
        )
        if not services:
            return Response(
                {
                    "conversation_id": str(conversation.id),
                    "assistant_message": "Каталог услуг пуст. Добавьте услуги в базе, чтобы я мог рекомендовать.",
                    "recommended_services": [],
                    "follow_up_questions": [
                        "Какая цель для вас сейчас важнее всего?",
                        "Есть ли ограничения по времени или бюджету?",
                    ],
                    "safety_note": "Это не медицинская консультация. При симптомах обратитесь к врачу.",
                }
            )
        catalog = _build_catalog(list(services))
        client_context = ""
        if request.user.is_authenticated:
            client_context = _build_client_context(request.user)

        context_payload = request.data.get("context") or {}
        context_lines = []
        if context_payload.get("preferred_master_id"):
            context_lines.append(
                f"Preferred master id: {context_payload.get('preferred_master_id')}"
            )
        if context_payload.get("budget"):
            context_lines.append(f"Budget: {context_payload.get('budget')}")
        if context_payload.get("time_window"):
            context_lines.append(f"Time window: {context_payload.get('time_window')}")

        system_context = "\n".join(
            line for line in [catalog, client_context, *context_lines] if line
        )

        schema = {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "assistant_message": {"type": "string"},
                "recommended_services": {
                    "type": "array",
                    "maxItems": 5,
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "service_id": {"type": "integer"},
                            "reason": {"type": "string"},
                        },
                        "required": ["service_id", "reason"],
                    },
                },
                "follow_up_questions": {
                    "type": "array",
                    "maxItems": 5,
                    "items": {"type": "string"},
                },
                "safety_note": {"type": "string"},
            },
            "required": [
                "assistant_message",
                "recommended_services",
                "follow_up_questions",
                "safety_note",
            ],
        }

        client = _get_openai_client()
        if not client:
            return Response(
                {"detail": "AI не настроен. Укажите OPENAI_API_KEY."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        model = os.getenv("OPENAI_MODEL", MODEL_DEFAULT)

        logger.info(
            "Using Responses structured outputs: text.format json_schema name=bizu_ai_response"
        )
        try:
            response = client.responses.create(
                model=model,
                input=_build_messages(conversation, message, system_context),
                temperature=0.4,
                store=False,
                text={
                    "format": {
                        "type": "json_schema",
                        "name": "bizu_ai_response",
                        "strict": True,
                        "schema": schema,
                    }
                },
            )
        except Exception as exc:
            error_text = str(exc)
            if "text.format.name" in error_text or "missing required parameter" in error_text:
                logger.exception(
                    "AI chat request shape error: model=%s conversation=%s user=%s",
                    model,
                    conversation.id,
                    request.user.id if request.user.is_authenticated else "anon",
                )
                return Response(
                    {
                        "detail": (
                            "Ошибка конфигурации AI (text.format.name). "
                            "Проверьте обновлённую схему запроса."
                        )
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
            if "json_schema" in error_text and "not supported" in error_text:
                logger.warning(
                    "Structured outputs not supported by model, falling back to json_object."
                )
                try:
                    response = client.responses.create(
                        model=model,
                        input=_build_messages(
                            conversation, message, system_context, json_mode=True
                        ),
                        temperature=0.3,
                        store=False,
                        text={"format": {"type": "json_object"}},
                    )
                except Exception as inner_exc:
                    logger.exception(
                        "AI chat error: model=%s conversation=%s user=%s",
                        model,
                        conversation.id,
                        request.user.id if request.user.is_authenticated else "anon",
                    )
                    return Response(
                        {
                            "detail": (
                                "Не удалось получить ответ от AI. Проверьте ключ и модель. "
                                f"Ошибка: {inner_exc.__class__.__name__}."
                            )
                        },
                        status=status.HTTP_502_BAD_GATEWAY,
                    )
            else:
                logger.exception(
                    "AI chat error: model=%s conversation=%s user=%s",
                    model,
                    conversation.id,
                    request.user.id if request.user.is_authenticated else "anon",
                )
                return Response(
                    {
                        "detail": (
                            "Не удалось получить ответ от AI. Проверьте ключ и модель. "
                            f"Ошибка: {exc.__class__.__name__}."
                        )
                    },
                    status=status.HTTP_502_BAD_GATEWAY,
                )
            logger.exception(
                "AI chat error: model=%s conversation=%s user=%s",
                model,
                conversation.id,
                request.user.id if request.user.is_authenticated else "anon",
            )
            return Response(
                {
                    "detail": (
                        "Не удалось получить ответ от AI. Проверьте ключ и модель. "
                        f"Ошибка: {exc.__class__.__name__}."
                    )
                },
                status=status.HTTP_502_BAD_GATEWAY,
            )

        raw_text = getattr(response, "output_text", None)
        if not raw_text:
            try:
                raw_text = response.output[0].content[0].text
            except Exception:
                raw_text = ""

        try:
            payload = json.loads(raw_text) if raw_text else {}
        except json.JSONDecodeError:
            payload = {}

        assistant_message = payload.get(
            "assistant_message",
            "Спасибо за запрос. Уточните, пожалуйста, ваши цели и ограничения.",
        )
        follow_up = payload.get("follow_up_questions", []) or []
        if not isinstance(follow_up, list):
            follow_up = []
        follow_up = [str(item) for item in follow_up if item]
        safety_note = payload.get(
            "safety_note",
            "Это не медицинская консультация. При симптомах обратитесь к врачу.",
        )

        if _severe_symptoms(message):
            safety_note = (
                f"{safety_note} При выраженных симптомах обратитесь к врачу."
            )

        service_index = {service.id: service for service in services}
        recommended_services = []
        for rec in payload.get("recommended_services", []) or []:
            service_id = rec.get("service_id")
            try:
                service_id = int(service_id)
            except (TypeError, ValueError):
                continue
            service = service_index.get(service_id)
            if not service:
                continue
            recommended_services.append(
                {
                    "service_id": service.id,
                    "name": service.name,
                    "category": service.category.name if service.category else "Без категории",
                    "price": service.price,
                    "duration_minutes": service.duration_minutes,
                    "reason": rec.get("reason", ""),
                }
            )

        if not recommended_services:
            follow_up = follow_up or [
                "Какая у вас цель: расслабление, кожа лица, тело?",
                "Есть ли предпочтения по времени или бюджету?",
            ]
            assistant_message = (
                assistant_message
                or "Пока не вижу подходящих услуг. Давайте уточним ваши потребности."
            )

        AiMessage.objects.create(
            conversation=conversation,
            role=AiMessage.ROLE_ASSISTANT,
            content=assistant_message,
        )
        conversation.updated_at = timezone.now()
        conversation.save(update_fields=["updated_at"])

        return Response(
            {
                "conversation_id": str(conversation.id),
                "assistant_message": assistant_message,
                "recommended_services": recommended_services,
                "follow_up_questions": follow_up,
                "safety_note": safety_note,
            }
        )
