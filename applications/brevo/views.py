import json
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import make_aware
from datetime import datetime

logger = logging.getLogger("django")

@csrf_exempt
def brevo_webhook_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            print("BREVO WEBHOOK PAYLOAD:", data)  # 👈 Muestra en consola
            logger.info("BREVO WEBHOOK PAYLOAD: %s", json.dumps(data))  # 👈 Guarda en el log

            # Si deseas, aquí podrías agregar validaciones antes de guardar

            return JsonResponse({"status": "received"}, status=200)

        except json.JSONDecodeError:
            logger.error("Invalid JSON received")
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    else:
        return JsonResponse({"message": "Only POST method allowed"}, status=405)
