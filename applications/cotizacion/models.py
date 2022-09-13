from email.policy import default
from functools import total_ordering
import keyword
from django.db import models
from django.contrib.contenttypes.models import ContentType
from applications.funciones import obtener_totales
from applications.sociedad.models import Sociedad
from applications.datos_globales.models import Moneda, TipoCambio
from applications.clientes.models import Cliente, ClienteInterlocutor, InterlocutorCliente
from applications.variables import ESTADOS, ESTADOS_CONFIRMACION, ESTADOS_COTIZACION_VENTA, TIPO_IGV_CHOICES, TIPO_VENTA
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete

from django.conf import settings


class PrecioListaMaterial(models.Model):
    content_type_producto = models.ForeignKey(ContentType, on_delete=models.PROTECT, related_name='PrecioListaMaterial_content_type_producto')
    id_registro_producto = models.IntegerField()    
    content_type_documento = models.ForeignKey(ContentType, on_delete=models.PROTECT, related_name='PrecioListaMaterial_content_type_documento', blank=True, null=True)
    id_registro_documento = models.IntegerField(blank=True, null=True)
    precio_compra = models.DecimalField('Precio de compra', max_digits=22, decimal_places=10,default=0)
    precio_lista = models.DecimalField('Precio de lista', max_digits=22, decimal_places=10,default=0)
    precio_sin_igv = models.DecimalField('Precio sin igv', max_digits=22, decimal_places=10,default=0)
    moneda = models.ForeignKey(Moneda, on_delete=models.PROTECT)
    logistico = models.DecimalField('Logistico', max_digits=22, decimal_places=10,default=0)
    margen_venta = models.DecimalField('Margen de venta', max_digits=22, decimal_places=10,default=0)
    estado = models.IntegerField('Estado', choices=ESTADOS, default=1)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='PrecioListaMaterial_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='PrecioListaMaterial_updated_by', editable=False)

    class Meta:
        verbose_name = 'Precio Lista Materiales'
        verbose_name_plural = 'Precio Lista Materiales'
        ordering = ['-created_at']

    def __str__(self):
        return str(self.id)


class CotizacionVenta(models.Model):
    numero_cotizacion = models.CharField('Número de Cotización', max_length=6, blank=True, null=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='CotizacionVenta_cliente', blank=True, null=True)
    cliente_interlocutor = models.ForeignKey(InterlocutorCliente, on_delete=models.PROTECT, related_name='CotizacionVenta_cliente_interlocutor', blank=True, null=True)
    fecha_cotizacion = models.DateField('Fecha Cotización', auto_now=False, auto_now_add=False, blank=True, null=True)
    fecha_validez = models.DateField('Fecha Validez', auto_now=False, auto_now_add=False, blank=True, null=True)
    moneda = models.ForeignKey(Moneda, on_delete=models.PROTECT, default=1)
    total = models.DecimalField('Total', max_digits=14, decimal_places=2, default=0)
    estado = models.IntegerField(choices=ESTADOS_COTIZACION_VENTA, default=1)
    motivo_anulacion = models.TextField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='CotizacionVenta_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='CotizacionVenta_updated_by', editable=False)

    class Meta:
        verbose_name = 'Cotizacion Venta'
        verbose_name_plural = 'Cotizaciones Venta'
        ordering = [
            '-fecha_cotizacion',
            '-numero_cotizacion',
        ]

    @property
    def internacional_nacional(self):
        return 2
    
    @property
    def fecha(self):
        return self.fecha_cotizacion

    @property
    def descuento_global(self):
        return self.CotizacionDescuentoGlobal_cotizacion_venta.all().aggregate(models.Sum('descuento_global'))['descuento_global__sum']

    @property
    def otros_cargos(self):
        return self.CotizacionOtrosCargos_cotizacion_venta.all().aggregate(models.Sum('otros_cargos'))['otros_cargos__sum']

    def __str__(self):
        return str(self.id)


class CotizacionVentaDetalle(models.Model):
    item = models.IntegerField(blank=True, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    id_registro = models.IntegerField()
    cantidad = models.DecimalField('Cantidad', max_digits=22, decimal_places=10, default=0)
    precio_unitario_sin_igv = models.DecimalField('Precio unitario sin IGV',max_digits=22, decimal_places=10, default=0)
    precio_unitario_con_igv = models.DecimalField('Precio unitario con IGV',max_digits=22, decimal_places=10, default=0)
    precio_final_con_igv = models.DecimalField('Precio final con IGV',max_digits=22, decimal_places=10, default=0)
    descuento = models.DecimalField('Descuento',max_digits=14, decimal_places=2, default=0)
    sub_total = models.DecimalField('Sub Total',max_digits=14, decimal_places=2, default=0)
    igv = models.DecimalField('IGV',max_digits=14, decimal_places=2, default=0)
    total = models.DecimalField('Total', max_digits=14, decimal_places=2, default=0)
    tipo_igv = models.IntegerField('Tipo IGV',choices=TIPO_IGV_CHOICES, default=1)
    cotizacion_venta = models.ForeignKey(CotizacionVenta, on_delete=models.CASCADE, related_name='CotizacionVentaDetalle_cotizacion_venta')

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='CotizacionVentaDetalle_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='CotizacionVentaDetalle_updated_by', editable=False)

    class Meta:
        verbose_name = 'Cotizacion Venta Detalle'
        verbose_name_plural = 'Cotizaciones Venta Detalle'
        ordering = ['item',]


    def __str__(self):
        return str(self.id)

def cotizacion_venta_detalle_post_save(*args, **kwargs):
    obj = kwargs['instance']
    respuesta = obtener_totales(obj.cotizacion_venta)
    obj.cotizacion_venta.total = respuesta['total']
    obj.cotizacion_venta.save()

def cotizacion_venta_material_detalle_post_delete(sender, instance, *args, **kwargs):
    materiales = CotizacionVentaDetalle.objects.filter(cotizacion_venta=instance.cotizacion_venta)
    contador = 1
    for material in materiales:
        material.item = contador
        material.save()
        contador += 1

post_save.connect(cotizacion_venta_detalle_post_save, sender=CotizacionVentaDetalle)
post_delete.connect(cotizacion_venta_material_detalle_post_delete, sender=CotizacionVentaDetalle)


class CotizacionOrdenCompra(models.Model):
    numero_orden = models.TextField()
    fecha_orden = models.DateField('Fecha Orden', auto_now=False, auto_now_add=False)
    documento = models.FileField('Documento', upload_to=None, max_length=100)
    cotizacion_venta = models.ForeignKey(CotizacionVenta, on_delete=models.PROTECT)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='CotizacionOrdenCompra_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='CotizacionOrdenCompra_updated_by', editable=False)

    class Meta:
        verbose_name = 'Cotizacion Orden Compra'
        verbose_name_plural = 'Cotizaciones Orden Compra'

    def __str__(self):
        return str(self.numero_orden)


class CotizacionTerminosCondiciones(models.Model):
    condicion = models.TextField()
    condicion_visible = models.BooleanField()
    orden = models.IntegerField()

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='CotizacionTerminosCondiciones_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='CotizacionTerminosCondiciones_updated_by', editable=False)

    class Meta:
        verbose_name = 'Cotizacion Terminos Condiciones'
        verbose_name_plural = 'Cotizaciones Terminos Condiciones'
        ordering = [
            'orden',
            ]


    def __str__(self):
        return str(self.condicion)


class ConfirmacionVenta(models.Model):
    cotizacion_venta = models.ForeignKey(CotizacionVenta, on_delete=models.CASCADE)
    sociedad = models.ForeignKey(Sociedad, on_delete=models.PROTECT)
    tipo_cambio = models.ForeignKey(TipoCambio, on_delete=models.PROTECT, related_name='ConfirmacionVenta_tipo_cambio')
    observacion = models.TextField(blank=True, null=True)
    condiciones_pago = models.CharField('Condiciones de Pago', max_length=50, blank=True, null=True)
    tipo_venta = models.IntegerField('Tipo de Venta', choices=TIPO_VENTA, default=1)
    descuento_global = models.DecimalField('Descuento Global', max_digits=14, decimal_places=2, default=0)
    otros_cargos = models.DecimalField('Otros cargos', max_digits=14, decimal_places=2, default=0)
    total = models.DecimalField('Total', max_digits=14, decimal_places=2, default=0)
    estado = models.IntegerField(choices=ESTADOS_CONFIRMACION, default=1)
    motivo_anulacion = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='ConfirmacionVenta_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='ConfirmacionVenta_updated_by', editable=False)

    class Meta:
        verbose_name = 'Confirmación Venta'
        verbose_name_plural = 'Confirmación Ventas'
        ordering = [
            '-created_at',
            ]

    @property
    def internacional_nacional(self):
        return 2

    @property
    def fecha_confirmacion(self):
        return self.created_at

    def __str__(self):
        return str(self.id)


class ConfirmacionVentaDetalle(models.Model):
    item = models.IntegerField(blank=True, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    id_registro = models.IntegerField()
    cantidad_confirmada = models.DecimalField('Cantidad confirmada', max_digits=22, decimal_places=10)
    precio_unitario_sin_igv = models.DecimalField('Precio unitario sin IGV',max_digits=22, decimal_places=10, default=0)
    precio_unitario_con_igv = models.DecimalField('Precio unitario con IGV',max_digits=22, decimal_places=10, default=0)
    precio_final_con_igv = models.DecimalField('Precio final con IGV',max_digits=22, decimal_places=10, default=0)
    descuento = models.DecimalField('Descuento',max_digits=14, decimal_places=2, default=0)
    sub_total = models.DecimalField('Sub Total',max_digits=14, decimal_places=2, default=0)
    igv = models.DecimalField('IGV',max_digits=14, decimal_places=2, default=0)
    total = models.DecimalField('Total', max_digits=14, decimal_places=2, default=0)
    tipo_igv = models.IntegerField('Tipo IGV',choices=TIPO_IGV_CHOICES, default=1)
    confirmacion_venta = models.ForeignKey(ConfirmacionVenta, on_delete=models.CASCADE, related_name='ConfirmacionVentaDetalle_confirmacion_venta')

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='ConfirmacionVentaDetalle_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='ConfirmacionVentaDetalle_updated_by', editable=False)

    class Meta:
        verbose_name = 'Confirmación Venta Detalle'
        verbose_name_plural = 'Confirmación Ventas Detalle'
        ordering = [
            'confirmacion_venta',
            'item',
            ]

    @property
    def cantidad(self):
        return self.cantidad_confirmada

    def __str__(self):
        return str(self.id)

def confirmacion_venta_detalle_post_save(*args, **kwargs):
    obj = kwargs['instance']
    respuesta = obtener_totales(obj.confirmacion_venta)
    obj.confirmacion_venta.total = respuesta['total']
    obj.confirmacion_venta.save()

post_save.connect(confirmacion_venta_detalle_post_save, sender=ConfirmacionVentaDetalle)


class CotizacionSociedad(models.Model):
    cotizacion_venta_detalle = models.ForeignKey(CotizacionVentaDetalle, on_delete=models.CASCADE, related_name='CotizacionSociedad_cotizacion_venta_detalle')
    sociedad = models.ForeignKey(Sociedad, on_delete=models.PROTECT)
    cantidad = models.DecimalField('Cantidad', max_digits=22, decimal_places=10, default=0)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='CotizacionSociedad_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='CotizacionSociedad_updated_by', editable=False)

    class Meta:
        verbose_name = 'Cotizacion Sociedad'
        verbose_name_plural = 'Cotizacion Sociedades'
        ordering = [
            'sociedad',
        ]

    def __str__(self):
        return "%s - %s - %s" % (self.cotizacion_venta_detalle, self.sociedad, self.cantidad)


class CotizacionDescuentoGlobal(models.Model):
    cotizacion_venta = models.ForeignKey(CotizacionVenta, on_delete=models.CASCADE, related_name='CotizacionDescuentoGlobal_cotizacion_venta')
    sociedad = models.ForeignKey(Sociedad, on_delete=models.PROTECT)
    descuento_global = models.DecimalField('Descuento Global', max_digits=14, decimal_places=2, default=0)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='CotizacionDescuentoGlobal_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='CotizacionDescuentoGlobal_updated_by', editable=False)

    class Meta:
        verbose_name = 'Cotizacion Descuento Global'
        verbose_name_plural = 'Cotizacion Descuento Globales'
        ordering = [
            'sociedad',
        ]

    def __str__(self):
        return "%s - %s - %s" % (self.cotizacion_venta, self.sociedad, self.descuento_global)


class CotizacionOtrosCargos(models.Model):
    cotizacion_venta = models.ForeignKey(CotizacionVenta, on_delete=models.CASCADE, related_name='CotizacionOtrosCargos_cotizacion_venta')
    sociedad = models.ForeignKey(Sociedad, on_delete=models.PROTECT)
    otros_cargos = models.DecimalField('Otros cargos', max_digits=14, decimal_places=2, default=0)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='CotizacionOtrosCargos_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='CotizacionOtrosCargos_updated_by', editable=False)

    class Meta:
        verbose_name = 'Cotizacion Otros Cargos'
        verbose_name_plural = 'Cotizacion Otros Cargos'
        ordering = [
            'sociedad',
        ]

    def __str__(self):
        return "%s - %s - %s" % (self.cotizacion_venta, self.sociedad, self.otros_cargos)


class CotizacionObservacion(models.Model):
    cotizacion_venta = models.ForeignKey(CotizacionVenta, on_delete=models.CASCADE, related_name='CotizacionObservacion_cotizacion_venta')
    sociedad = models.ForeignKey(Sociedad, on_delete=models.PROTECT)
    observacion = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='CotizacionObservacion_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='CotizacionObservacion_updated_by', editable=False)

    class Meta:
        verbose_name = 'Cotizacion Observación'
        verbose_name_plural = 'Cotizacion Observaciones'
        ordering = [
            'sociedad',
        ]

    def __str__(self):
        return "%s - %s - %s" % (self.cotizacion_venta, self.sociedad, self.observacion)


