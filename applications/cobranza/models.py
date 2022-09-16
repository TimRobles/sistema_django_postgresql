from django.db import models
from applications.clientes.models import Cliente
from applications.datos_globales.models import Moneda
from applications.variables import ESTADOS
from django.conf import settings

from django.db.models.signals import pre_save, post_save, pre_delete, post_delete


class LineaCredito(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='LineaCredito_cliente', blank=True, null=True)
    monto = models.DecimalField('Monto', max_digits=7, decimal_places=2)
    moneda = models.ForeignKey(Moneda, on_delete=models.PROTECT)
    condiciones_pago = models.CharField('Condiciones de pago', max_length=250)
    estado = models.IntegerField('Estado', choices=ESTADOS, default=1)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='LineaCredito_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='LineaCredito_updated_by', editable=False)


    class Meta:
        verbose_name = 'Linea de Credito'
        verbose_name_plural = 'Lineas de Credito'

    def __str__(self):
        return str(self.id)

def linea_credito_post_save(*args, **kwargs):
    if kwargs['created']:
        obj = kwargs['instance']
        lineas = LineaCredito.objects.filter(
                cliente=obj.cliente,
                estado=1,
            ).exclude(id=obj.id)
        for linea in lineas:
            linea.estado = 2
            linea.save()

post_save.connect(linea_credito_post_save, sender=LineaCredito)