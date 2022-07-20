from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from applications.almacenes.models import Almacen
from applications.sociedad.models import Sociedad

# Create your models here.
class TipoMovimiento(models.Model):
    SIGNOS = (
        (1, '+1'),
        (0, '0'),
        (-1, '-1'),
    )
    codigo = models.IntegerField('Código SAP', blank=True, null=True)
    descripcion = models.CharField('Descripción del movimiento', max_length=50)
    signo_factor_multiplicador = models.IntegerField('Signo Factor Multiplicador', choices=SIGNOS)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='TipoMovimiento_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='TipoMovimiento_updated_by', editable=False)
    
    class Meta:
        verbose_name = 'Tipo de Movimiento'
        verbose_name_plural = 'Tipos de Movimientos'

    def __str__(self):
        return "%i - %s (%i)" % (self.codigo, self.descripcion, self.signo_factor_multiplicador)



class MovimientosAlmacen(models.Model):
    content_type_producto = models.ForeignKey(ContentType, on_delete=models.PROTECT, related_name='MovimientosAlmacen_content_type_producto')
    id_registro_producto = models.IntegerField()
    cantidad = models.DecimalField('Cantidad', max_digits=22, decimal_places=10)
    tipo_movimiento = models.ForeignKey(TipoMovimiento, on_delete=models.PROTECT)
    content_type_documento_proceso = models.ForeignKey(ContentType, on_delete=models.PROTECT, related_name='MovimientosAlmacen_content_type_documento_proceso')
    id_registro_documento_proceso = models.IntegerField()
    almacen = models.ForeignKey(Almacen, on_delete=models.PROTECT, blank=True, null=True)
    sociedad = models.ForeignKey(Sociedad, on_delete=models.PROTECT, blank=True, null=True)
    movimiento_anterior = models.ForeignKey('self', on_delete=models.PROTECT)
    movimiento_reversion = models.BooleanField(default=False)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='MovimientosAlmacen_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='MovimientosAlmacen_updated_by', editable=False)

    class Meta:
        verbose_name = 'Movimiento de Almacen'
        verbose_name_plural = 'Movimientos de Almacenes'

    def __str__(self):
        return str(self.id)
