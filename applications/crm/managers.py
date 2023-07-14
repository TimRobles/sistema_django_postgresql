from decimal import Decimal
from django.db import models
from django.db.models import Sum

class RespuestaDetalleCRMManager(models.Manager):
    def ver_respuestas(self, respuesta_crm):
        respuestas_detalle_crm = self.filter(respuesta_crm = respuesta_crm)
        consulta = {}
        for respuesta in respuestas_detalle_crm:
            if respuesta.pregunta_crm.tipo_pregunta == 1:
                consulta[respuesta.pregunta_crm] = [respuesta.alternativa_crm,]
            elif respuesta.pregunta_crm.tipo_pregunta == 2:
                if not respuesta.pregunta_crm in consulta:
                    consulta[respuesta.pregunta_crm] = []
                consulta[respuesta.pregunta_crm] = consulta[respuesta.pregunta_crm] + [respuesta.alternativa_crm,]
            elif respuesta.pregunta_crm.tipo_pregunta == 3:
                consulta[respuesta.pregunta_crm] = [respuesta.texto,]
        
        return consulta