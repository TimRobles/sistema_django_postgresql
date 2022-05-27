from applications.variables import ESTADOS
from django.db import models
from django.conf import settings
from applications.sede.models import Sede



class Almacen(models.Model):
    nombre = models.CharField('Almacén', max_length=100)
    sede = models.ForeignKey(Sede, on_delete=models.CASCADE)
    estado_alta_baja = models.IntegerField('Estado', choices=ESTADOS, default=1)
    
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Almacen_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Almacen_updated_by', editable=False)


    class Meta:
        verbose_name = 'Almacen'
        verbose_name_plural = 'Almacenes'

    def __str__(self):
        return self.nombre
