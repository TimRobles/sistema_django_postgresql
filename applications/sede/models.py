from django.db import models
from django.conf import settings
from applications import datos_globales
from applications.variables import ESTADOS
from applications.sociedad.models import Sociedad
from applications.datos_globales.models import Distrito

class Sede(models.Model):

    sociedad = models.ManyToManyField(Sociedad)
    nombre = models.CharField('Nombre', max_length=100)
    usuario_responsable = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='Usuario_Responsable')
    direccion = models.CharField('Dirección', max_length=254)
    ubigeo = models.CharField('Ubigeo', max_length=6)
    distrito = models.ForeignKey(Distrito, on_delete=models.PROTECT, blank=True, null=True)
    estado = models.IntegerField('Estado', choices=ESTADOS, default=1)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='Sede_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='Sede_updated_by', editable=False)
    
    class Meta:

        verbose_name = 'Sede'
        verbose_name_plural = 'Sedes'

    def save(self, *args, **kwargs):
        if self.ubigeo:
            self.distrito = datos_globales.models.Distrito.objects.get(codigo = self.ubigeo)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre

