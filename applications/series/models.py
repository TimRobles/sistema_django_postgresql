from pyexpat import model
from django.conf import settings
from django.db import models
from django.contrib.contenttypes.models import ContentType

from applications.material.models import Material
from applications.sociedad.models import Sociedad
from applications.variables import ESTADOS


# Create your models here.

class Serie(models.Model):
    """Model definition for Serie."""

    serie_base = models.CharField("Serie_Base",max_length=100)
    serie_secundaria = models.CharField("Serie_Secundaria",max_length=100)
    serie_terciaria = models.CharField("Serie_Terciaria",max_length=100)
    # estado_id = models.IntegerField('Estado', choices=ESTADOS, default=1)
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    id_registro = models.IntegerField()
    # documento_compra_id = models.ForeignKey()
    # documento_venta_id = models.ForeignKey()
    sociedad_id = models.ForeignKey(Sociedad, on_delete=models.PROTECT)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='Encuesta_created_by', editable=False)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='Encuesta_updated_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)


    class Meta:
        """Meta definition for Serie."""

        verbose_name = 'Serie'
        verbose_name_plural = 'Series'

    def __str__(self):
        """Unicode representation of Serie."""
        return self.serie_base
