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

MODEL_DEFAULT = "mistralai/mistral-7b-instruct:free"
MODEL_FALLBACK = "openrouter/free"
MAX_HISTORY_MESSAGES = 10
MAX_RETRIES = 2
OPENROUTER_TIMEOUT_SECONDS = float(os.getenv("OPENROUTER_TIMEOUT_SECONDS", "18"))

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


def _get_openrouter_client():
    if OpenAI is None:
        return None
    api_key = os.getenv("OPENROUTER_API_KEY", "")
    if not api_key:
        return None
    return OpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
        timeout=OPENROUTER_TIMEOUT_SECONDS,
        max_retries=0,
    )


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
) -> List[Dict]:
    output_contract = (
        "Верни только JSON-объект без Markdown и пояснений. "
        "Структура JSON:\n"
        "{\n"
        "  \"assistant_message\": \"string\",\n"
        "  \"recommended_services\": [\n"
        "    {\"service_id\": number, \"reason\": \"string\"}\n"
        "  ],\n"
        "  \"follow_up_questions\": [\"string\"],\n"
        "  \"safety_note\": \"string\"\n"
        "}\n"
        "recommended_services: максимум 5 элементов. "
        "Рекомендуй ТОЛЬКО service_id из SERVICES CATALOG. "
        "Если не уверен — верни пустой массив recommended_services и уточняющие follow_up_questions."
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
        {"role": "system", "content": output_contract},
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


def _chat_completion_with_retry(client, model: str, messages: List[Dict]):
    last_exception = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            logger.info(
                "OpenRouter AI request: model=%s attempt=%s/%s",
                model,
                attempt,
                MAX_RETRIES,
            )
            return client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.4,
            )
        except Exception as exc:
            last_exception = exc
            logger.exception(
                "OpenRouter chat completion error (attempt %s/%s): model=%s",
                attempt,
                MAX_RETRIES,
                model,
            )
    raise last_exception


def _build_model_candidates() -> List[str]:
    primary_model = (os.getenv("OPENROUTER_MODEL", MODEL_DEFAULT) or "").strip() or MODEL_DEFAULT
    candidates = [primary_model]
    if primary_model != MODEL_FALLBACK:
        candidates.append(MODEL_FALLBACK)
    return candidates


def _model_error_detail(exc: Exception) -> str:
    error_text = str(exc)
    lowered = error_text.lower()
    if (
        "no endpoints found" in lowered
        or "404" in lowered
        or "model not found" in lowered
        or "does not exist" in lowered
    ):
        return (
            "Модель OpenRouter недоступна. "
            "Проверьте OPENROUTER_MODEL или используйте openrouter/free."
        )
    return (
        "Не удалось получить ответ от AI. "
        "Проверьте OPENROUTER_API_KEY, выбранную модель и лимиты OpenRouter."
    )


def _is_model_unavailable_error(exc: Exception) -> bool:
    lowered = str(exc).lower()
    return (
        "no endpoints found" in lowered
        or "404" in lowered
        or "model not found" in lowered
        or "does not exist" in lowered
    )


def _extract_response_text(response) -> str:
    try:
        content = response.choices[0].message.content
    except Exception:
        return ""

    if isinstance(content, str):
        return content.strip()

    if isinstance(content, list):
        chunks = []
        for item in content:
            if isinstance(item, str):
                chunks.append(item)
            elif isinstance(item, dict):
                text = item.get("text") or item.get("content")
                if text:
                    chunks.append(str(text))
        return "\n".join(chunks).strip()

    return ""


def _parse_payload(raw_text: str) -> Dict:
    if not raw_text:
        return {}

    text = raw_text.strip()
    candidates = [text]

    if text.startswith("```"):
        cleaned = text.strip("`")
        cleaned = cleaned.replace("json", "", 1).strip()
        candidates.append(cleaned)

    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        candidates.append(text[start : end + 1])

    for candidate in candidates:
        try:
            data = json.loads(candidate)
            if isinstance(data, dict):
                return data
        except json.JSONDecodeError:
            continue

    return {}


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

        services_qs = (
            Service.objects.select_related("category")
            .prefetch_related("masters", "masters__profile")
            .all()
        )
        services = list(services_qs)

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

        catalog = _build_catalog(services)
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

        client = _get_openrouter_client()
        if not client:
            return Response(
                {"detail": "AI не настроен. Укажите OPENROUTER_API_KEY."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        model_candidates = _build_model_candidates()
        response = None
        last_error = None

        messages = _build_messages(conversation, message, system_context)
        for idx, model in enumerate(model_candidates):
            try:
                response = _chat_completion_with_retry(
                    client=client,
                    model=model,
                    messages=messages,
                )
                logger.info(
                    "OpenRouter AI request successful: model=%s conversation=%s user=%s",
                    model,
                    conversation.id,
                    request.user.id if request.user.is_authenticated else "anon",
                )
                break
            except Exception as exc:
                last_error = exc
                logger.warning(
                    "OpenRouter model failed: model=%s conversation=%s user=%s error=%s",
                    model,
                    conversation.id,
                    request.user.id if request.user.is_authenticated else "anon",
                    exc,
                )
                if idx == 0 and _is_model_unavailable_error(exc) and len(model_candidates) > 1:
                    logger.info(
                        "Primary model is unavailable, switching to fallback model=%s",
                        model_candidates[1],
                    )
                    continue
                break

        if response is None:
            detail = _model_error_detail(last_error or Exception("unknown_error"))
            logger.exception(
                "AI chat error via OpenRouter after fallbacks: models=%s conversation=%s user=%s",
                ",".join(model_candidates),
                conversation.id,
                request.user.id if request.user.is_authenticated else "anon",
            )
            return Response(
                {"detail": f"{detail} Ошибка: {(last_error or Exception()).__class__.__name__}."},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        raw_text = _extract_response_text(response)
        payload = _parse_payload(raw_text)

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
            if not isinstance(rec, dict):
                continue
            service_id = rec.get("service_id")
            try:
                service_id = int(service_id)
            except (TypeError, ValueError):
                continue
            service = service_index.get(service_id)
            if not service:
                logger.warning(
                    "AI recommended unknown service_id=%s conversation=%s",
                    service_id,
                    conversation.id,
                )
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
