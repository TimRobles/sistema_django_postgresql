import json
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_datetime

from applications.brevo.models import BrevoWebhookEvent

logger = logging.getLogger("django")

@csrf_exempt
def brevo_webhook_view(request):
    if request.method == "POST":
        try:
            payload = json.loads(request.body)
            logger.info("BREVO WEBHOOK PAYLOAD: %s", json.dumps(payload))

            BrevoWebhookEvent.objects.create(
                event=payload.get("event"),
                email=payload.get("email"),
                sender_email=payload.get("sender_email"),
                subject=payload.get("subject"),
                date=parse_datetime(payload.get("date")) if payload.get("date") else None,
                ts=payload.get("ts"),
                ts_event=payload.get("ts_event"),
                ts_epoch=payload.get("ts_epoch"),
                message_id=payload.get("message-id"),
                sending_ip=payload.get("sending_ip"),
                reason=payload.get("reason"),
                mirror_link=payload.get("mirror_link"),
                tag=payload.get("tag"),
                tags=payload.get("tags"),
                user_agent=payload.get("user_agent"),
                device_used=payload.get("device_used"),
                link=payload.get("link"),
            )

            return JsonResponse({"status": "received"}, status=200)

        except Exception as e:
            logger.error(f"ERROR: {str(e)}\n")
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
    else:
        return JsonResponse({"message": "Only POST method allowed"}, status=405)
