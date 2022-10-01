from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from applications.almacenes.models import Almacen
from applications.movimiento_almacen.managers import MovimientoAlmacenManager
from applications.sociedad.models import Sociedad

# Create your models here.
class TipoStock(models.Model):
    codigo = models.IntegerField('Código', blank=True, null=True, unique=True)
    descripcion = models.CharField('Descripción del movimiento', max_length=50, unique=True)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='TipoStock_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='TipoStock_updated_by', editable=False)

    class Meta:
        verbose_name = 'Tipo de Stock'
        verbose_name_plural = 'Tipos de Stocks'

    def __str__(self):
        return "%s - %s" % (self.codigo, self.descripcion)


class TipoMovimiento(models.Model):
    codigo = models.IntegerField('Código', blank=True, null=True, unique=True)
    descripcion = models.CharField('Descripción del movimiento', max_length=50, unique=True)
    tipo_stock_inicial = models.ForeignKey(TipoStock, on_delete=models.CASCADE, blank=True, null=True, related_name='TipoMovimiento_tipo_stock_inicial')
    tipo_stock_final = models.ForeignKey(TipoStock, on_delete=models.CASCADE, blank=True, null=True, related_name='TipoMovimiento_tipo_stock_final')

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='TipoMovimiento_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='TipoMovimiento_updated_by', editable=False)
    
    class Meta:
        verbose_name = 'Tipo de Movimiento'
        verbose_name_plural = 'Tipos de Movimientos'

    def __str__(self):
        return "%s - %s" % (self.codigo, self.descripcion)


class MovimientosAlmacen(models.Model):
    SIGNOS = (
        (1, '+1'),
        (0, '0'),
        (-1, '-1'),
    )
    content_type_producto = models.ForeignKey(ContentType, on_delete=models.PROTECT, related_name='MovimientosAlmacen_content_type_producto')
    id_registro_producto = models.IntegerField()
    cantidad = models.DecimalField('Cantidad', max_digits=22, decimal_places=10)
    tipo_movimiento = models.ForeignKey(TipoMovimiento, on_delete=models.PROTECT)
    tipo_stock = models.ForeignKey(TipoStock, on_delete=models.CASCADE)
    signo_factor_multiplicador = models.IntegerField('Signo Factor Multiplicador', choices=SIGNOS)
    content_type_documento_proceso = models.ForeignKey(ContentType, on_delete=models.PROTECT, related_name='MovimientosAlmacen_content_type_documento_proceso')
    id_registro_documento_proceso = models.IntegerField()
    almacen = models.ForeignKey(Almacen, on_delete=models.PROTECT, blank=True, null=True)
    sociedad = models.ForeignKey(Sociedad, on_delete=models.PROTECT, blank=True, null=True)
    movimiento_anterior = models.ForeignKey('self', on_delete=models.PROTECT, blank=True, null=True, related_name='MovimientosAlmacen_movimiento_anterior')
    movimiento_reversion = models.BooleanField(default=False)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='MovimientosAlmacen_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='MovimientosAlmacen_updated_by', editable=False)

    objects = MovimientoAlmacenManager()

    class Meta:
        verbose_name = 'Movimiento de Almacen'
        verbose_name_plural = 'Movimientos de Almacenes'

    @property
    def documento_proceso(self):
        return self.content_type_documento_proceso.model_class().objects.get(id=self.id_registro_documento_proceso)

    def valor(self):
        return self.cantidad * self.signo_factor_multiplicador

    def __str__(self):
        return str(self.id)
