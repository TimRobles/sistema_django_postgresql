from django.db import models
from django.conf import settings

# Create your models here.
class Excepcion(models.Model):
    texto = models.TextField()
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Excepcion_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Excepcion_updated_by', editable=False)

    class Meta:
        verbose_name = 'Excepcion'
        verbose_name_plural = 'Excepciones'

    def __str__(self):
        return self.texto
