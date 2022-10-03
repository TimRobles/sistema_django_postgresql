from django.db import models
from django.conf import settings


class Transportista(models.Model):
    tipo_documento = models.IntegerField()
    numero_documento = models.CharField('Número de Documento', max_length=15)
    razon_social = models.CharField('Razón Social', max_length=100)
    
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Transportista_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Transportista_updated_by', editable=False)

    class Meta:
        verbose_name = 'Transportista'
        verbose_name_plural = 'Transportistas'

    def __str__(self):
        return str(self.id)
