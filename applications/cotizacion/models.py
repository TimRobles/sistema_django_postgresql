from functools import total_ordering
import keyword
from django.db import models
from django.contrib.contenttypes.models import ContentType
from applications.sociedad.models import Sociedad
from applications.datos_globales.models import Moneda, TipoCambio
from applications.clientes.models import Cliente, ClienteInterlocutor, InterlocutorCliente
from applications.variables import ESTADOS, ESTADOS_COTIZACION_VENTA, TIPO_IGV_CHOICES, TIPO_VENTA

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
    sociedad = models.ForeignKey(Sociedad, on_delete=models.PROTECT, blank=True, null=True)
    numero_cotizacion = models.CharField('Número de Cotización', max_length=50, blank=True, null=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='CotizacionVenta_cliente', blank=True, null=True)
    cliente_interlocutor = models.ForeignKey(InterlocutorCliente, on_delete=models.PROTECT, related_name='CotizacionVenta_cliente_interlocutor', blank=True, null=True)
    fecha_cotizacion = models.DateField('Fecha Cotización', auto_now=False, auto_now_add=False, blank=True, null=True)
    fecha_validez = models.DateField('Fecha Validez', auto_now=False, auto_now_add=False, blank=True, null=True)
    tipo_cambio = models.ForeignKey(TipoCambio, on_delete=models.PROTECT, related_name='CotizacionVenta_tipo_cambio', blank=True, null=True)
    observaciones_adicionales = models.TextField(blank=True, null=True)
    condiciones_pago = models.TextField(blank=True, null=True)
    tipo_venta = models.IntegerField('Tipo de Venta', choices=TIPO_VENTA, default=1)
    descuento_global = models.DecimalField('Descuento global', max_digits=14, decimal_places=2, default=0)
    total = models.DecimalField('Total', max_digits=14, decimal_places=2, default=0)
    estado = models.IntegerField(choices=ESTADOS_COTIZACION_VENTA, default=1)
    motivo_anulacion = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='CotizacionVenta_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='CotizacionVenta_updated_by', editable=False)

    class Meta:
        verbose_name = 'Cotizacion Venta'
        verbose_name_plural = 'Cotizaciones Venta'

    @property
    def internacional_nacional(self):
        return 2

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

    def __str__(self):
        return str(self.id)


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

    def __str__(self):
        return str(self.condicion)


class ReservaVenta(models.Model):
    cotizacion_venta = models.ForeignKey(CotizacionVenta, on_delete=models.CASCADE)
    sociedad = models.ForeignKey(Sociedad, on_delete=models.PROTECT)
    numero_cotizacion = models.CharField('Núero de cotización', max_length=50)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='ReservaVenta_cliente')
    cliente_interlocutor = models.ForeignKey(InterlocutorCliente, on_delete=models.PROTECT, related_name='ReservaVenta_cliente_interlocutor')
    fecha_cotizacion = models.DateField('Fecha Cotización', auto_now=False, auto_now_add=False)
    fecha_confirmacion = models.DateField('Fecha Confirmación', auto_now=False, auto_now_add=False)
    tipo_cambio = models.ForeignKey(TipoCambio, on_delete=models.PROTECT, related_name='ReservaVenta_tipo_cambio')
    observaciones_adicionales = models.TextField()
    condiciones_pago = models.TextField()
    tipo_venta = models.IntegerField('Tipo de Venta', choices=TIPO_VENTA, default=1)
    descuento_global = models.DecimalField('Descuento global', max_digits=14, decimal_places=2)
    total = models.DecimalField('Total', max_digits=14, decimal_places=2)
    estado = models.IntegerField(choices=ESTADOS)
    motivo_anualacion = models.TextField()

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='ReservaVenta_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='ReservaVenta_updated_by', editable=False)

    class Meta:
        verbose_name = 'Reserva Venta'
        verbose_name_plural = 'Reservas Venta'

    def __str__(self):
        return str(self.id)


class ReservaVentaDetalle(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    id_registro = models.IntegerField()
    item = models.IntegerField()
    cantidad = models.DecimalField('Cantidad', max_digits=22, decimal_places=10)
    precio_unitario_sin_igv = models.DecimalField('Precio unitario sin IGV',max_digits=22, decimal_places=10)
    precio_unitario_con_igv = models.DecimalField('Precio unitario con IGV',max_digits=22, decimal_places=10)
    precio_final_con_igv = models.DecimalField('Precio final con IGV',max_digits=22, decimal_places=10)
    descuento = models.DecimalField('Descuento',max_digits=14, decimal_places=2)
    sub_total = models.DecimalField('Sub Total',max_digits=14, decimal_places=2)
    igv = models.DecimalField('IGV',max_digits=14, decimal_places=2)
    tipo_igv = models.IntegerField('Tipo IGV',choices=TIPO_IGV_CHOICES,)
    reserva_venta = models.ForeignKey(ReservaVenta, on_delete=models.CASCADE)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='ReservaVentaDetalle_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='ReservaVentaDetalle_updated_by', editable=False)

    class Meta:
        verbose_name = 'Reserva Venta Detalle'
        verbose_name_plural = 'Reservas Venta Detalle'

    def __str__(self):
        return str(self.id)


class ConfirmacionVenta(models.Model):
    cotizacion_venta = models.ForeignKey(CotizacionVenta, on_delete=models.CASCADE)
    reserva_venta = models.ForeignKey(ReservaVenta, on_delete=models.PROTECT, null=True) 
    sociedad = models.ForeignKey(Sociedad, on_delete=models.PROTECT)
    numero_cotizacion = models.CharField('Número de Cotización', max_length=50)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='ConfirmacionVenta_cliente')
    fecha_cotizacion = models.DateField('Fecha Cotización', auto_now=False, auto_now_add=False)
    fecha_validez = models.DateField('Fecha Validez', auto_now=False, auto_now_add=False)
    tipo_cambio = models.ForeignKey(TipoCambio, on_delete=models.PROTECT, related_name='ConfirmacionVenta_tipo_cambio')
    observaciones_adicionales = models.TextField()
    condiciones_pago = models.TextField()
    tipo_venta = models.IntegerField('Tipo de Venta', choices=TIPO_VENTA, default=1)
    descuento_global = models.DecimalField('Descuento global', max_digits=14, decimal_places=2)
    total = models.DecimalField('Total', max_digits=14, decimal_places=2)
    estado = models.IntegerField(choices=ESTADOS_COTIZACION_VENTA)
    motivo_anualacion = models.TextField()

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='ConfirmacionVenta_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='ConfirmacionVenta_updated_by', editable=False)

    class Meta:
        verbose_name = 'Confirmación Venta'
        verbose_name_plural = 'Confirmación Ventas'

    def __str__(self):
        return str(self.id)


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

    def __str__(self):
        return "%s - %s - %s" % (self.cotizacion_venta_detalle, self.sociedad, self.cantidad)
