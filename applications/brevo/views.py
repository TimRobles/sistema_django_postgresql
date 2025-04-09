import json
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_datetime
from django.shortcuts import render, get_object_or_404
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


def event_list(request):
    # Recuperar filtros desde parámetros GET
    recipient_filter = request.GET.get('recipient', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')

    qs = BrevoWebhookEvent.objects.all()
    if recipient_filter:
        qs = qs.filter(email__icontains=recipient_filter)
    if date_from:
        qs = qs.filter(date__gte=date_from)
    if date_to:
        qs = qs.filter(date__lte=date_to)

    qs = qs.order_by('date')
    
    # Agrupar por 'message_id'. Si message_id es None, usamos un identificador temporal.
    grouped = {}
    for event in qs:
        key = event.message_id or f'no_id_{event.pk}'
        if key not in grouped:
            grouped[key] = {
                'message_id': key,
                'recipient': event.email,
                'sender': event.sender_email,
                'subject': event.subject,
                'date': event.date,
                'open_count': 0,
                'status': event.event,  # estado inicial
                'events': [],
            }
        grouped[key]['events'].append(event)
        if event.event in ('opened', 'unique_opened'):
            grouped[key]['open_count'] += 1

        # Actualizar el estatus según una jerarquía definida (se puede ajustar)
        # Definimos los niveles de cada tipo de evento (mayor número = peor estado)
        hierarchy = {
            'error': 6,
            'hard_bounce': 5,
            'soft_bounce': 5,
            'blocked': 5,
            'complaint': 4,
            'unsubscribed': 4,
            'deferred': 3,
            'delivered': 2,
            'click': 2,
            'opened': 1,
            'unique_opened': 1,
            'request': 0,
            'proxy_open': 1,
        }
        current_status = grouped[key]['status']
        if hierarchy.get(event.event, 0) > hierarchy.get(current_status, 0):
            grouped[key]['status'] = event.event

    events_list = list(grouped.values())

    context = {
        'events_list': events_list,
        'recipient_filter': recipient_filter,
        'date_from': date_from,
        'date_to': date_to,
    }
    return render(request, 'brevo/event_list.html', context)


def event_detail(request, message_id):
    # Recupera todos los eventos asociados a un message_id dado
    events = BrevoWebhookEvent.objects.filter(message_id=message_id).order_by('date')
    context = {
        'message_id': message_id,
        'events': events,
    }
    return render(request, 'brevo/event_detail.html', context)
