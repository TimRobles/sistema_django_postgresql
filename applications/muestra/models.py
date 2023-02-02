from decimal import Decimal
from django.db import models
from django.conf import settings

from django.contrib.contenttypes.models import ContentType
from applications.almacenes.models import Almacen
from applications.calidad.models import FallaMaterial, Serie
from applications.clientes.models import Cliente, InterlocutorCliente
from applications.funciones import numeroXn
from applications.muestra.managers import DevolucionMuestraManager, NotaIngresoMuestraManager
from applications.nota_ingreso.models import NotaIngresoDetalle
from applications.proveedores.models import Proveedor
from applications.sede.models import Sede
from applications.sociedad.models import Sociedad
from applications.variables import ESTADO_NOTA_INGRESO

# Create your models here.

class NotaIngresoMuestra(models.Model):
    nro_nota_ingreso_muestra = models.IntegerField('Número de Nota de Ingreso de Muestra', help_text='Correlativo', blank=True, null=True)
    sociedad = models.ForeignKey(Sociedad, on_delete=models.PROTECT)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    fecha_ingreso = models.DateField('Fecha de Ingreso', auto_now=False, auto_now_add=False)
    observaciones = models.TextField(blank=True, null=True)
    motivo_anulacion = models.TextField('Motivo de Anulación', blank=True, null=True)
    estado = models.IntegerField('Estado', choices=ESTADO_NOTA_INGRESO, default=1)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='NotaIngresoMuestra_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='NotaIngresoMuestra_updated_by', editable=False)

    objects = NotaIngresoMuestraManager()

    class Meta:
        verbose_name = 'Nota de Ingreso de Muestra'
        verbose_name_plural = 'Notas de Ingreso de Muestra'

    @property
    def fecha(self):
        return self.fecha_ingreso
    
    @property
    def documento(self):
        return self
    
    @property
    def detalle(self):
        return self.NotaIngresoMuestraDetalle_nota_ingreso_muestra.all()

    def __str__(self):
        return "NOTA DE INGRESO DE MUESTRA %s" % (numeroXn(self.nro_nota_ingreso_muestra, 6))


class NotaIngresoMuestraDetalle(models.Model):
    item = models.IntegerField(blank=True, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT) #Material
    id_registro = models.IntegerField()
    cantidad_total = models.DecimalField('Cantidad total', max_digits=22, decimal_places=10, default=Decimal('0.00'))
    nota_ingreso_muestra = models.ForeignKey(NotaIngresoMuestra, on_delete=models.PROTECT, related_name='NotaIngresoMuestraDetalle_nota_ingreso_muestra')

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='NotaIngresoMuestraDetalle_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='NotaIngresoMuestraDetalle_updated_by', editable=False)

    class Meta:
        verbose_name = 'Nota de Ingreso de Muestra Detalle'
        verbose_name_plural = 'Notas de Ingreso de Muestra Detalles'
        ordering = [
            'nota_ingreso_muestra',
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
    def sociedad(self):
        return self.nota_ingreso_muestra.sociedad

    def __str__(self):
        return "%s - %s" % (self.item, self.producto)


class DevolucionMuestra(models.Model):
    ESTADOS_DEVOLUCION_MATERIALES = (
        (1, 'EN PROCESO'),
        (2, 'FINALIZADO'),
        (3, 'ANULADO'),
    )
    numero_devolucion = models.IntegerField('Número Devolución', blank=True, null=True)
    sociedad = models.ForeignKey(Sociedad, on_delete=models.CASCADE)
    sede = models.ForeignKey(Sede, on_delete=models.CASCADE)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    fecha_devolucion = models.DateField('Fecha Devolución', auto_now=False, auto_now_add=False)
    observaciones = models.TextField(blank=True, null=True)
    motivo_anulacion = models.TextField('Motivo Anulación', blank=True, null=True)
    estado = models.IntegerField(choices=ESTADOS_DEVOLUCION_MATERIALES, default=1)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='DevolucionMuestra_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='DevolucionMuestra_updated_by', editable=False)

    objects = DevolucionMuestraManager()

    class Meta:

        verbose_name = 'Devolución Muestras'
        verbose_name_plural = 'Devolución Muestras'
        ordering = ['numero_devolucion',]

    @property
    def fecha(self):
        return self.fecha_devolucion

    def __str__(self):
        return "%s - %s" % (numeroXn(self.numero_devolucion, 6), self.proveedor)

class DevolucionMuestraDetalle(models.Model):
    item = models.IntegerField(blank=True, null=True)
    content_type = models.ForeignKey(ContentType, blank=True, null=True, on_delete=models.CASCADE) #Material
    id_registro = models.IntegerField(blank=True, null=True)
    cantidad_devolucion = models.DecimalField('Cantidad Devolución', max_digits=22, decimal_places=10, default=Decimal('0.00'))
    almacen = models.ForeignKey(Almacen, on_delete=models.CASCADE)
    observacion = models.TextField(blank=True, null=True)
    devolucion_muestra = models.ForeignKey(DevolucionMuestra, blank=True, null=True, on_delete=models.CASCADE, related_name='DevolucionMuestraDetalle_devolucion_muestra')

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='DevolucionMuestraDetalle_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='DevolucionMuestraDetalle_updated_by', editable=False)

    class Meta:

        verbose_name = 'Devolución Muestras Detalle'
        verbose_name_plural = 'Devolución Muestras Detalle'
        ordering = ['item',]

    @property
    def producto(self):
        return self.content_type.get_object_for_this_type(id=self.id_registro)

    @property
    def cantidad(self):
        return self.cantidad_devolucion

    @property
    def unidad(self):
        return self.producto.unidad_base

    def __str__(self):
        return "%s - %s" % (self.item, self.producto)


class ValidarSerieDevolucionMuestraDetalle(models.Model):
    devolucion_muestra_detalle = models.ForeignKey(DevolucionMuestraDetalle, on_delete=models.PROTECT, related_name='ValidarSerieDevolucionMuestraDetalle_devolucion_muestra_detalle')
    serie = models.ForeignKey(Serie, on_delete=models.CASCADE, blank=True, null=True)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='ValidarSerieDevolucionMuestraDetalle_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='ValidarSerieDevolucionMuestraDetalle_updated_by', editable=False)

    class Meta:
        verbose_name = 'Validar Series Devolución Muestra Detalle'
        verbose_name_plural = 'Validar Series Devolución Muestra Detalle'
        ordering = [
            'created_at',
            ]

    def __str__(self):
        return "%s - %s" % (self.devolucion_muestra_detalle, str(self.serie))