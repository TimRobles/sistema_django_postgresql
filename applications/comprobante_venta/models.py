from decimal import Decimal
from django.db import models
from django.contrib.contenttypes.models import ContentType
from applications import cobranza
from applications.comprobante_venta.managers import BoletaVentaManager, FacturaVentaManager
from applications.datos_globales.models import Moneda, SeriesComprobante, TipoCambio, Unidad
from applications.sociedad.models import Sociedad
from applications.clientes.models import Cliente, InterlocutorCliente
from applications.variables import ESTADOS_DOCUMENTO, TIPO_COMPROBANTE, TIPO_DOCUMENTO_SUNAT, TIPO_IGV_CHOICES, TIPO_ISC_CHOICES, TIPO_PERCEPCION, TIPO_RETENCION, TIPO_VENTA
from django.conf import settings
from applications.funciones import numeroXn, obtener_totales
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete

from applications.cotizacion.models import ConfirmacionVenta
import applications


class FacturaVenta(models.Model):
    tipo_comprobante = models.IntegerField('Tipo de Comprobante', choices=TIPO_COMPROBANTE, default=1)
    sociedad = models.ForeignKey(Sociedad, on_delete=models.PROTECT)
    serie_comprobante = models.ForeignKey(SeriesComprobante, on_delete=models.PROTECT, blank=True, null=True)
    numero_factura = models.IntegerField('Nro. Factura', blank=True, null=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='FacturaVenta_cliente', blank=True, null=True)
    cliente_interlocutor = models.ForeignKey(InterlocutorCliente, on_delete=models.PROTECT, related_name='FacturaVenta_interlocutor', blank=True, null=True)
    fecha_emision = models.DateField('Fecha Emisión', auto_now=False, auto_now_add=False, blank=True, null=True)
    fecha_vencimiento = models.DateField('Fecha Vencimiento', auto_now=False, auto_now_add=False, blank=True, null=True)
    moneda = models.ForeignKey(Moneda, on_delete=models.PROTECT, default=1)
    tipo_cambio = models.ForeignKey(TipoCambio, on_delete=models.PROTECT, related_name='FacturaVenta_tipo_cambio')
    tipo_venta = models.IntegerField('Tipo de Venta', choices=TIPO_VENTA, default=1)
    condiciones_pago = models.CharField('Condiciones de Pago', max_length=250, blank=True, null=True, help_text='Factura a 30 días')
    descuento_global = models.DecimalField('Descuento Global', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total_descuento = models.DecimalField('Total Descuento', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total_anticipo = models.DecimalField('Total Anticipo', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total_gravada = models.DecimalField('Total Gravada', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total_inafecta = models.DecimalField('Total Inafecta', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total_exonerada = models.DecimalField('Total Exonerada', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total_igv = models.DecimalField('Total IGV', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total_gratuita = models.DecimalField('Total Gratuita', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total_otros_cargos = models.DecimalField('Total Otros Cargos', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total = models.DecimalField('Total', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    percepcion_tipo = models.IntegerField(choices=TIPO_PERCEPCION, blank=True, null=True)
    percepcion_base_imponible = models.DecimalField('Percepcion Base Imponible', max_digits=14, decimal_places=2, default=Decimal('0.00'), blank=True, null=True)
    total_percepcion = models.DecimalField('Total Percepcion', max_digits=14, decimal_places=2, default=Decimal('0.00'), blank=True, null=True)
    total_incluido_percepcion = models.DecimalField('Total Incluido Percepcion', max_digits=14, decimal_places=2, default=Decimal('0.00'), blank=True, null=True)
    total_impuestos_bolsas = models.DecimalField('Total Impuestos Bolsas', max_digits=14, decimal_places=2, default=Decimal('0.00'), blank=True, null=True)
    detraccion = models.BooleanField(default=False)
    retencion_tipo = models.IntegerField(choices=TIPO_RETENCION, blank=True, null=True)
    retencion_base_imponible = models.DecimalField('Retencion Base Imponible', max_digits=14, decimal_places=2, default=Decimal('0.00'), blank=True, null=True)
    total_retencion = models.DecimalField('Total Retencion', max_digits=14, decimal_places=2, default=Decimal('0.00'), blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True, max_length=1000)
    estado = models.IntegerField(choices = ESTADOS_DOCUMENTO, default=1)
    numero_orden = models.CharField('Número de Orden', max_length=100, blank=True, null=True)
    motivo_anulacion = models.CharField('Motivo de Anulación', max_length=100, blank=True, null=True)
    confirmacion = models.ForeignKey(ConfirmacionVenta, on_delete=models.PROTECT, related_name='FacturaVenta_confirmacion', blank=True, null=True)
    nubefact = models.URLField(max_length=400, blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='FacturaVenta_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='FacturaVenta_updated_by', editable=False)

    objects = FacturaVentaManager()

    class Meta:
        verbose_name = 'Factura Venta'
        verbose_name_plural = 'Facturas Venta'
        ordering = [
                '-created_at',
                ]

    @property
    def internacional_nacional(self):
        return 2

    @property
    def fecha(self):
        return self.fecha_emision

    @property
    def documento(self):
        return "%s-%s" % (self.serie_comprobante.serie, numeroXn(self.numero_factura, 6))

    @property
    def detalles(self):
        return self.FacturaVentaDetalle_factura_venta.all()

    @property
    def guias(self):
        return [] # self.confirmacion.NotaSalida.NotaDespacho.Guias

    @property
    def cuotas(self):
        try:
            return cobranza.models.Deuda.objects.get(content_type=ContentType.objects.get_for_model(self), id_registro=self.id).Cuota_deuda.all()
        except:
            return []

    @property
    def descripcion(self):
        return "%s %s-%s" % (self.get_tipo_comprobante_display(), self.serie_comprobante.serie, numeroXn(self.numero_factura, 6))

    def __str__(self):
        if self.numero_factura:
            return "%s %s-%s %s %s %s %s" % (self.get_tipo_comprobante_display(), self.serie_comprobante.serie, self.numero_factura, self.sociedad.abreviatura, self.cliente, self.moneda.simbolo, self.total)
        else:
            return "%s %s %s %s %s %s" % (self.get_tipo_comprobante_display(), self.serie_comprobante.serie, self.sociedad.abreviatura, self.cliente, self.moneda.simbolo, self.total)

def factura_venta_post_save(*args, **kwargs):
    print('factura_venta_post_save')
    obj = kwargs['instance']
    applications.crm.models.actualizar_estado_cliente_crm(obj.cliente.id)

def factura_venta_pre_save(*args, **kwargs):
    print('factura_venta_pre_save')

post_save.connect(factura_venta_post_save, sender=FacturaVenta)
pre_save.connect(factura_venta_pre_save, sender=FacturaVenta)

class FacturaVentaDetalle(models.Model):
    item = models.IntegerField()
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT, blank=True, null=True)
    id_registro = models.IntegerField(blank=True, null=True)
    unidad = models.ForeignKey(Unidad, on_delete=models.CASCADE, blank=True, null=True)
    codigo_interno = models.CharField('Código Interno', max_length=250, blank=True, null=True)
    descripcion_documento = models.CharField('Descripción', max_length=250)
    cantidad = models.DecimalField('Cantidad', max_digits=22, decimal_places=10)
    precio_unitario_sin_igv = models.DecimalField('Precio unitario sin IGV',max_digits=22, decimal_places=10, default=Decimal('0.00'))
    precio_unitario_con_igv = models.DecimalField('Precio unitario con IGV',max_digits=22, decimal_places=10, default=Decimal('0.00'))
    precio_final_con_igv = models.DecimalField('Precio final con IGV',max_digits=22, decimal_places=10, default=Decimal('0.00'))
    descuento = models.DecimalField('Descuento',max_digits=22, decimal_places=10, default=Decimal('0.00'))
    sub_total = models.DecimalField('Sub Total',max_digits=14, decimal_places=2, default=Decimal('0.00'))
    tipo_igv = models.IntegerField('Tipo IGV',choices=TIPO_IGV_CHOICES, default=1)
    igv = models.DecimalField('IGV', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total = models.DecimalField('Total', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    anticipo_regularizacion = models.BooleanField(default=False)
    anticipo_documento_serie = models.ForeignKey(SeriesComprobante, on_delete=models.PROTECT, blank=True, null=True)
    anticipo_documento_numero = models.IntegerField(blank=True, null=True)
    codigo_producto_sunat = models.CharField(max_length=8, blank=True)
    tipo_de_isc = models.IntegerField(choices=TIPO_ISC_CHOICES, blank=True, null=True)
    isc = models.DecimalField('ISC', max_digits=14, decimal_places=2, blank=True, null=True)
    factura_venta = models.ForeignKey(FacturaVenta, on_delete=models.CASCADE, related_name='FacturaVentaDetalle_factura_venta')
    
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='FacturaVentaDetalle_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='FacturaVentaDetalle_updated_by', editable=False)

    class Meta:
        verbose_name = 'Factura Venta Detalle'
        verbose_name_plural = 'Facturas Venta Detalle'
        ordering = [
            'factura_venta',
            'item',
            ]

    @property
    def moneda(self):
        return self.factura_venta.moneda
    
    @property
    def documento(self):
        return f'FACTURA {self.factura_venta.documento}'
    
    @property
    def fecha(self):
        return self.factura_venta.fecha_emision

    @property
    def cliente(self):
        return self.factura_venta.cliente

    @property
    def producto(self):
        return self.content_type.get_object_for_this_type(id = self.id_registro)

    def __str__(self):
        return str(self.id)


def factura_venta_detalle_post_save(*args, **kwargs):
    obj = kwargs['instance']
    respuesta = obtener_totales(obj.factura_venta)
    obj.factura_venta.total_descuento = respuesta['total_descuento']
    obj.factura_venta.total_anticipo = respuesta['total_anticipo']
    obj.factura_venta.total_gravada = respuesta['total_gravada']
    obj.factura_venta.total_inafecta = respuesta['total_inafecta']
    obj.factura_venta.total_exonerada = respuesta['total_exonerada']
    obj.factura_venta.total_igv = respuesta['total_igv']
    obj.factura_venta.total_gratuita = respuesta['total_gratuita']
    obj.factura_venta.otros_cargos = respuesta['total_otros_cargos']
    obj.factura_venta.total = respuesta['total']
    obj.factura_venta.save()

post_save.connect(factura_venta_detalle_post_save, sender=FacturaVentaDetalle)


class BoletaVenta(models.Model):
    tipo_comprobante = models.IntegerField('Tipo de Comprobante', choices=TIPO_COMPROBANTE, default=2)
    sociedad = models.ForeignKey(Sociedad, on_delete=models.PROTECT)
    serie_comprobante = models.ForeignKey(SeriesComprobante, on_delete=models.PROTECT, blank=True, null=True)
    numero_boleta = models.IntegerField('Nro. Boleta', blank=True, null=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='BoletaVenta_cliente', blank=True, null=True)
    cliente_interlocutor = models.ForeignKey(InterlocutorCliente, on_delete=models.PROTECT, related_name='BoletaVenta_interlocutor', blank=True, null=True)
    fecha_emision = models.DateField('Fecha Emisión', auto_now=False, auto_now_add=False, blank=True, null=True)
    fecha_vencimiento = models.DateField('Fecha Vencimiento', auto_now=False, auto_now_add=False, blank=True, null=True)
    moneda = models.ForeignKey(Moneda, on_delete=models.PROTECT, default=1)
    tipo_cambio = models.ForeignKey(TipoCambio, on_delete=models.PROTECT, related_name='BoletaVenta_tipo_cambio')
    tipo_venta = models.IntegerField('Tipo de Venta', choices=TIPO_VENTA, default=1)
    condiciones_pago = models.CharField('Condiciones de Pago', max_length=250, blank=True, null=True, help_text='Factura a 30 días')
    descuento_global = models.DecimalField('Descuento Global', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total_descuento = models.DecimalField('Total Descuento', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total_anticipo = models.DecimalField('Total Anticipo', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total_gravada = models.DecimalField('Total Gravada', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total_inafecta = models.DecimalField('Total Inafecta', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total_exonerada = models.DecimalField('Total Exonerada', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total_igv = models.DecimalField('Total IGV', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total_gratuita = models.DecimalField('Total Gratuita', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total_otros_cargos = models.DecimalField('Total Otros Cargos', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total = models.DecimalField('Total', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    percepcion_tipo = models.IntegerField(choices=TIPO_PERCEPCION, blank=True, null=True)
    percepcion_base_imponible = models.DecimalField('Percepcion Base Imponible', max_digits=14, decimal_places=2, default=Decimal('0.00'), blank=True, null=True)
    total_percepcion = models.DecimalField('Total Percepcion', max_digits=14, decimal_places=2, default=Decimal('0.00'), blank=True, null=True)
    total_incluido_percepcion = models.DecimalField('Total Incluido Percepcion', max_digits=14, decimal_places=2, default=Decimal('0.00'), blank=True, null=True)
    retencion_tipo = models.IntegerField(choices=TIPO_RETENCION, blank=True, null=True)
    retencion_base_imponible = models.DecimalField('Retencion Base Imponible', max_digits=14, decimal_places=2, default=Decimal('0.00'), blank=True, null=True)
    total_retencion = models.DecimalField('Total Retencion', max_digits=14, decimal_places=2, default=Decimal('0.00'), blank=True, null=True)
    total_impuestos_bolsas = models.DecimalField('Total Impuestos Bolsas', max_digits=14, decimal_places=2, default=Decimal('0.00'), blank=True, null=True)
    detraccion = models.BooleanField(default=False)
    observaciones = models.TextField(blank=True, null=True, max_length=1000)
    estado = models.IntegerField(choices = ESTADOS_DOCUMENTO, default=1)
    motivo_anulacion = models.CharField('Motivo de Anulación', max_length=100, blank=True, null=True)
    confirmacion = models.ForeignKey(ConfirmacionVenta, on_delete=models.PROTECT, related_name='BoletaVenta_confirmacion', blank=True, null=True)
    nubefact = models.URLField(max_length=400, blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='BoletaVenta_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='BoletaVenta_updated_by', editable=False)

    objects = BoletaVentaManager()

    class Meta:
        verbose_name = 'Boleta Venta'
        verbose_name_plural = 'Boletas Venta'
        ordering = [
                '-created_at',
                ]

    @property
    def internacional_nacional(self):
        return 2

    @property
    def fecha(self):
        return self.fecha_emision

    @property
    def documento(self):
        return "%s-%s" % (self.serie_comprobante.serie, numeroXn(self.numero_boleta, 6))

    @property
    def detalles(self):
        return self.BoletaVentaDetalle_boleta_venta.all()

    @property
    def guias(self):
        return [] # self.confirmacion.NotaSalida.NotaDespacho.Guias
    
    @property
    def cuotas(self):
        try:
            return cobranza.models.Deuda.objects.get(content_type=ContentType.objects.get_for_model(self), id_registro=self.id).Cuota_deuda.all()
        except:
            return []

    @property
    def descripcion(self):
        return "%s %s-%s" % (self.get_tipo_comprobante_display(), self.serie_comprobante.serie, numeroXn(self.numero_boleta, 6))

    def __str__(self):
        if self.numero_boleta:
            return "%s %s-%s %s %s %s" % (self.get_tipo_comprobante_display(), self.serie_comprobante.serie, self.numero_boleta, self.cliente, self.moneda.simbolo, self.total)
        else:
            return "%s %s %s %s %s" % (self.get_tipo_comprobante_display(), self.serie_comprobante.serie, self.cliente, self.moneda.simbolo, self.total)

class BoletaVentaDetalle(models.Model):
    item = models.IntegerField()
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT, blank=True, null=True)
    id_registro = models.IntegerField(blank=True, null=True)
    unidad = models.ForeignKey(Unidad, on_delete=models.CASCADE, blank=True, null=True)
    codigo_interno = models.CharField('Código Interno', max_length=250, blank=True, null=True)
    descripcion_documento = models.CharField('Descripción', max_length=250)
    cantidad = models.DecimalField('Cantidad', max_digits=22, decimal_places=10)
    precio_unitario_sin_igv = models.DecimalField('Precio unitario sin IGV',max_digits=22, decimal_places=10, default=Decimal('0.00'))
    precio_unitario_con_igv = models.DecimalField('Precio unitario con IGV',max_digits=22, decimal_places=10, default=Decimal('0.00'))
    precio_final_con_igv = models.DecimalField('Precio final con IGV',max_digits=22, decimal_places=10, default=Decimal('0.00'))
    descuento = models.DecimalField('Descuento',max_digits=22, decimal_places=10, default=Decimal('0.00'))
    sub_total = models.DecimalField('Sub Total',max_digits=14, decimal_places=2, default=Decimal('0.00'))
    tipo_igv = models.IntegerField('Tipo IGV',choices=TIPO_IGV_CHOICES, default=1)
    igv = models.DecimalField('IGV', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total = models.DecimalField('Total', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    anticipo_regularizacion = models.BooleanField(default=False)
    anticipo_documento_serie = models.ForeignKey(SeriesComprobante, on_delete=models.PROTECT, blank=True, null=True)
    anticipo_documento_numero = models.IntegerField(blank=True, null=True)
    codigo_producto_sunat = models.CharField(max_length=8, blank=True)
    tipo_de_isc = models.IntegerField(choices=TIPO_ISC_CHOICES, blank=True, null=True)
    isc = models.DecimalField('ISC', max_digits=14, decimal_places=2, blank=True, null=True)
    descuento_sin_igv = models.DecimalField('Descuento sin IGV',max_digits=22, decimal_places=10, default=Decimal('0.00'))
    descuento_con_igv = models.DecimalField('Descuento con IGV',max_digits=22, decimal_places=10, default=Decimal('0.00'))
    boleta_venta = models.ForeignKey(BoletaVenta, on_delete=models.CASCADE, related_name='BoletaVentaDetalle_boleta_venta')
    
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='BoletaVentaDetalle_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='BoletaVentaDetalle_updated_by', editable=False)
 
    class Meta:
        verbose_name = 'Boleta Venta Detalle'
        verbose_name_plural = 'Boletas Venta Detalle'
        ordering = [
            'boleta_venta',
            'item',
            ]

    @property
    def moneda(self):
        return self.boleta_venta.moneda

    @property
    def documento(self):
        return f'BOLETA {self.boleta_venta.documento}'
    
    @property
    def fecha(self):
        return self.boleta_venta.fecha_emision

    @property
    def cliente(self):
        return self.boleta_venta.cliente

    @property
    def producto(self):
        return self.content_type.get_object_for_this_type(id = self.id_registro)

    def __str__(self):
        return str(self.id)

def boleta_venta_detalle_post_save(*args, **kwargs):
    obj = kwargs['instance']
    respuesta = obtener_totales(obj.boleta_venta)
    obj.boleta_venta.total_descuento = respuesta['total_descuento']
    obj.boleta_venta.total_anticipo = respuesta['total_anticipo']
    obj.boleta_venta.total_gravada = respuesta['total_gravada']
    obj.boleta_venta.total_inafecta = respuesta['total_inafecta']
    obj.boleta_venta.total_exonerada = respuesta['total_exonerada']
    obj.boleta_venta.total_igv = respuesta['total_igv']
    obj.boleta_venta.total_gratuita = respuesta['total_gratuita']
    obj.boleta_venta.otros_cargos = respuesta['total_otros_cargos']
    obj.boleta_venta.total = respuesta['total']
    obj.boleta_venta.save()

post_save.connect(boleta_venta_detalle_post_save, sender=BoletaVentaDetalle)
