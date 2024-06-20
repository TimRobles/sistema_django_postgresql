from django.db import models
from django.conf import settings

from applications.variables import CONDICION_SUNAT, ESTADO_SUNAT, TIPO_DOCUMENTO_SUNAT


class Transportista(models.Model):
    tipo_documento = models.CharField('Tipo de Documento', max_length=1, choices=TIPO_DOCUMENTO_SUNAT)
    numero_documento = models.CharField('Número de Documento', max_length=15)
    razon_social = models.CharField('Razón Social', max_length=100)
    estado_sunat = models.IntegerField('Estado SUNAT', choices=ESTADO_SUNAT, default=1)
    condicion_sunat = models.IntegerField('Condición SUNAT', choices=CONDICION_SUNAT, default=1)
    
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Transportista_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Transportista_updated_by', editable=False)

    class Meta:
        verbose_name = 'Transportista'
        verbose_name_plural = 'Transportistas'

        ordering = [
            'razon_social',
            ]
        

    def __str__(self):
        return str(self.razon_social)
