from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from applications.almacenes.models import Almacen
from applications.comprobante_compra.models import ComprobanteCompraPI, ComprobanteCompraPIDetalle
from applications.funciones import numeroXn
from applications.nota_ingreso.managers import NotaIngresoManager

from applications.recepcion_compra.models import RecepcionCompra
from applications.sociedad.models import Sociedad
from applications.variables import ESTADO_NOTA_INGRESO

# Create your models here.
class NotaIngreso(models.Model):
    nro_nota_ingreso = models.IntegerField('Número de Nota de Ingreso', help_text='Correlativo', blank=True, null=True)
    recepcion_compra = models.ForeignKey(RecepcionCompra, on_delete=models.PROTECT)
    sociedad = models.ForeignKey(Sociedad, on_delete=models.PROTECT)
    fecha_ingreso = models.DateField('Fecha de Ingreso', auto_now=False, auto_now_add=False)
    observaciones = models.TextField(blank=True, null=True)
    motivo_anulacion = models.TextField('Motivo de Anulación', blank=True, null=True)
    estado = models.IntegerField('Estado', choices=ESTADO_NOTA_INGRESO, default=1)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='NotaIngreso_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='NotaIngreso_updated_by', editable=False)

    objects = NotaIngresoManager()

    class Meta:
        verbose_name = 'Nota de Ingreso'
        verbose_name_plural = 'Notas de Ingreso'

    @property
    def fecha(self):
        return self.fecha_ingreso

    def __str__(self):
        return "%s" % (numeroXn(self.nro_nota_ingreso, 6))


class NotaIngresoDetalle(models.Model):
    item = models.IntegerField(blank=True, null=True)
    comprobante_compra_detalle = models.ForeignKey(ComprobanteCompraPIDetalle, on_delete=models.PROTECT, related_name='NotaIngresoDetalle_comprobante_compra_detalle')
    cantidad_conteo = models.DecimalField('Cantidad del conteo', max_digits=22, decimal_places=10, blank=True, null=True)
    almacen = models.ForeignKey(Almacen, on_delete=models.PROTECT)
    nota_ingreso = models.ForeignKey(NotaIngreso, on_delete=models.PROTECT, related_name='NotaIngresoDetalle_nota_ingreso')

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='NotaIngresoDetalle_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='NotaIngresoDetalle_updated_by', editable=False)

    class Meta:
        verbose_name = 'Nota de Ingreso Detalle'
        verbose_name_plural = 'Notas de Ingreso Detalles'
        ordering = [
            'item',
            ]

    def __str__(self):
        return "%s" % (self.comprobante_compra_detalle)
