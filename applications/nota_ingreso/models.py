from decimal import Decimal
from email.policy import default
from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from applications.almacenes.models import Almacen
from applications.comprobante_compra.models import ComprobanteCompraPI, ComprobanteCompraPIDetalle
from applications.funciones import numeroXn
from applications.nota_ingreso.managers import NotaIngresoManager, NotaStockInicialManager
from applications.proveedores.models import Proveedor

from applications.recepcion_compra.models import RecepcionCompra
from applications.sociedad.models import Sociedad
from applications.variables import ESTADO_NOTA_INGRESO
from django.db.models.signals import pre_save, post_save, post_delete

# Create your models here.
class NotaIngreso(models.Model):
    nro_nota_ingreso = models.IntegerField('Número de Nota de Ingreso', help_text='Correlativo', blank=True, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT) #RecepcionCompra / NotaStockInicial
    id_registro = models.IntegerField()
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
    
    @property
    def recepcion_compra(self):
        return self.content_type.get_object_for_this_type(id = self.id_registro)

    def __str__(self):
        return "NOTA DE INGRESO %s - %s" % (numeroXn(self.nro_nota_ingreso, 6), self.recepcion_compra)


class NotaIngresoDetalle(models.Model):
    item = models.IntegerField(blank=True, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT) #ComprobanteCompraPIDetalle / NotaStockInicialDetalle
    id_registro = models.IntegerField()
    cantidad_conteo = models.DecimalField('Cantidad del conteo', max_digits=22, decimal_places=10, blank=True, null=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, blank=True, null=True)
    almacen = models.ForeignKey(Almacen, on_delete=models.PROTECT, blank=True, null=True)
    nota_ingreso = models.ForeignKey(NotaIngreso, on_delete=models.PROTECT, related_name='NotaIngresoDetalle_nota_ingreso')

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='NotaIngresoDetalle_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='NotaIngresoDetalle_updated_by', editable=False)

    class Meta:
        verbose_name = 'Nota de Ingreso Detalle'
        verbose_name_plural = 'Notas de Ingreso Detalles'
        ordering = [
            'nota_ingreso',
            'item',
            ]

    @property
    def comprobante_compra_detalle(self):
        return self.content_type.get_object_for_this_type(id = self.id_registro)

    def __str__(self):
        return "%s" % (self.comprobante_compra_detalle)

def nota_ingreso_detalle_post_save(*args, **kwargs):
    if kwargs['created']:
        obj = kwargs['instance']
        try:
            obj.proveedor = obj.comprobante_compra_detalle.proveedor
            obj.proveedor.save()
        except Exception as e:
            pass
            
post_save.connect(nota_ingreso_detalle_post_save, sender=NotaIngresoDetalle)


class NotaStockInicial(models.Model):
    nro_nota_stock_inicial = models.IntegerField('Número de Nota de Stock Inicial', help_text='Correlativo', blank=True, null=True)
    sociedad = models.ForeignKey(Sociedad, on_delete=models.PROTECT)
    fecha_ingreso = models.DateField('Fecha de Ingreso', auto_now=False, auto_now_add=False)
    observaciones = models.TextField(blank=True, null=True)
    motivo_anulacion = models.TextField('Motivo de Anulación', blank=True, null=True)
    estado = models.IntegerField('Estado', choices=ESTADO_NOTA_INGRESO, default=1)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='NotaStockInicial_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='NotaStockInicial_updated_by', editable=False)

    objects = NotaStockInicialManager()

    class Meta:
        verbose_name = 'Nota de Stock Inicial'
        verbose_name_plural = 'Notas de Stock Inicial'

    @property
    def fecha(self):
        return self.fecha_ingreso
    
    @property
    def documento(self):
        return self
    
    @property
    def detalle(self):
        return self.NotaStockInicialDetalle_nota_stock_inicial.all()

    def __str__(self):
        return "NOTA DE STOCK INICIAL %s" % (numeroXn(self.nro_nota_stock_inicial, 6))


class NotaStockInicialDetalle(models.Model):
    item = models.IntegerField(blank=True, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT) #Material
    id_registro = models.IntegerField()
    cantidad_total = models.DecimalField('Cantidad total', max_digits=22, decimal_places=10, default=Decimal('0.00'))
    nota_stock_inicial = models.ForeignKey(NotaStockInicial, on_delete=models.PROTECT, related_name='NotaStockInicialDetalle_nota_stock_inicial')

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='NotaStockInicialDetalle_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='NotaStockInicialDetalle_updated_by', editable=False)

    class Meta:
        verbose_name = 'Nota de Stock Inicial Detalle'
        verbose_name_plural = 'Notas de Stock Inicial Detalles'
        ordering = [
            'nota_stock_inicial',
            'item',
            ]

    @property
    def producto(self):
        return self.content_type.get_object_for_this_type(id=self.id_registro)

    @property
    def cantidad(self):
        return self.cantidad_total
    
    @property
    def orden_compra_detalle(self):
        return self

    @property
    def cantidad_contada(self):
        nota_ingreso_detalle = NotaIngresoDetalle.objects.filter(
            content_type=ContentType.objects.get_for_model(self),
            id_registro=self.id,
        )
        if nota_ingreso_detalle:
            return nota_ingreso_detalle.aggregate(models.Sum('cantidad_conteo'))['cantidad_conteo__sum']
        return Decimal('0.00')

    @property
    def pendiente(self):
        return self.cantidad - self.cantidad_contada

    def __str__(self):
        return "%s - %s" % (self.item, self.producto)
