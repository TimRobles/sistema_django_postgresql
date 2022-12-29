from datetime import date, timedelta
from decimal import Decimal
from email.policy import default
from functools import total_ordering
from reportlab.lib import colors
from django.db import models
from django.contrib.contenttypes.models import ContentType
from applications.funciones import calculos_linea, igv, numeroXn, obtener_totales
import applications
from applications import material
from applications.rutas import ORDEN_COMPRA_CONFIRMACION
from applications.sociedad.models import Sociedad
from applications.datos_globales.models import Moneda, TipoCambio
from applications.clientes.models import Cliente, ClienteInterlocutor, InterlocutorCliente
from applications.variables import ESTADOS, ESTADOS_CONFIRMACION, ESTADOS_COTIZACION_VENTA, SUNAT_TRANSACTION, TIPO_IGV_CHOICES, TIPO_VENTA
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete

from django.conf import settings


class PrecioListaMaterial(models.Model):
    content_type_producto = models.ForeignKey(ContentType, on_delete=models.PROTECT, related_name='PrecioListaMaterial_content_type_producto')
    id_registro_producto = models.IntegerField()    
    content_type_documento = models.ForeignKey(ContentType, on_delete=models.PROTECT, related_name='PrecioListaMaterial_content_type_documento', blank=True, null=True)
    id_registro_documento = models.IntegerField(blank=True, null=True)
    precio_compra = models.DecimalField('Precio de compra', max_digits=22, decimal_places=10,default=Decimal('0.00'))
    precio_lista = models.DecimalField('Precio de lista', max_digits=22, decimal_places=10,default=Decimal('0.00'))
    precio_sin_igv = models.DecimalField('Precio sin igv', max_digits=22, decimal_places=10,default=Decimal('0.00'))
    moneda = models.ForeignKey(Moneda, on_delete=models.PROTECT)
    logistico = models.DecimalField('Logistico', max_digits=22, decimal_places=10,default=Decimal('0.00'))
    margen_venta = models.DecimalField('Margen de venta', max_digits=22, decimal_places=10,default=Decimal('0.00'))
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
    numero_cotizacion = models.IntegerField('Número de Cotización', blank=True, null=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='CotizacionVenta_cliente', blank=True, null=True)
    cliente_interlocutor = models.ForeignKey(InterlocutorCliente, on_delete=models.PROTECT, related_name='CotizacionVenta_cliente_interlocutor', blank=True, null=True)
    fecha_cotizacion = models.DateField('Fecha Cotización', auto_now=False, auto_now_add=False, blank=True, null=True)
    fecha_validez = models.DateField('Fecha Validez', auto_now=False, auto_now_add=False, blank=True, null=True)
    moneda = models.ForeignKey(Moneda, on_delete=models.PROTECT, default=1)
    total = models.DecimalField('Total', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    estado = models.IntegerField(choices=ESTADOS_COTIZACION_VENTA, default=1)
    motivo_anulacion = models.TextField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    vendedor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True)

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
    def sociedades(self):
        sociedades = []
        for detalle in self.CotizacionVentaDetalle_cotizacion_venta.all():
            for cotizacion_sociedad in detalle.CotizacionSociedad_cotizacion_venta_detalle.all():
                if cotizacion_sociedad.cantidad > 0:
                    nombre_sociedad = cotizacion_sociedad.sociedad
                    observaciones = material.funciones.observacion(self, nombre_sociedad)
                    sociedad = {
                            'nombre_sociedad':nombre_sociedad,
                            'observaciones':observaciones,
                        }
                    if not sociedad in sociedades:
                        sociedades.append(sociedad)
        return sociedades

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

    @property
    def documento(self):
        return "%s" % (self.numero_cotizacion)

    @property
    def monto_solicitado(self):
        if self.SolicitudCredito_cotizacion_venta:
            return self.SolicitudCredito_cotizacion_venta.SolicitudCreditoCuota_solicitud_credito.all().aggregate(models.Sum('monto'))['monto__sum']
        return Decimal('0.00')

    def __str__(self):
        return "%s - %s" % (numeroXn(self.numero_cotizacion, 6), self.cliente)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.fecha_validez:
            if self.estado == 2:
                if self.fecha_validez < date.today():
                    self.estado = 8
                    self.save()
        

class CotizacionVentaDetalle(models.Model):
    item = models.IntegerField(blank=True, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    id_registro = models.IntegerField()
    cantidad = models.DecimalField('Cantidad', max_digits=22, decimal_places=10, default=Decimal('0.00'))
    precio_unitario_sin_igv = models.DecimalField('Precio unitario sin IGV',max_digits=22, decimal_places=10, default=Decimal('0.00'))
    precio_unitario_con_igv = models.DecimalField('Precio unitario con IGV',max_digits=22, decimal_places=10, default=Decimal('0.00'))
    precio_final_con_igv = models.DecimalField('Precio final con IGV',max_digits=22, decimal_places=10, default=Decimal('0.00'))
    descuento = models.DecimalField('Descuento',max_digits=14, decimal_places=2, default=Decimal('0.00'))
    sub_total = models.DecimalField('Sub Total',max_digits=14, decimal_places=2, default=Decimal('0.00'))
    igv = models.DecimalField('IGV',max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total = models.DecimalField('Total', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    tipo_igv = models.IntegerField('Tipo IGV',choices=TIPO_IGV_CHOICES, default=1)
    tiempo_entrega = models.IntegerField(default=0)
    cotizacion_venta = models.ForeignKey(CotizacionVenta, on_delete=models.CASCADE, related_name='CotizacionVentaDetalle_cotizacion_venta')

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='CotizacionVentaDetalle_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='CotizacionVentaDetalle_updated_by', editable=False)

    class Meta:
        verbose_name = 'Cotizacion Venta Detalle'
        verbose_name_plural = 'Cotizaciones Venta Detalle'
        ordering = [
            'cotizacion_venta',
            'item',
            ]


    def __str__(self):
        return str(self.id)

def cotizacion_venta_detalle_post_save(*args, **kwargs):
    obj = kwargs['instance']
    respuesta = obtener_totales(obj.cotizacion_venta)
    obj.cotizacion_venta.total_descuento = respuesta['total_descuento']
    obj.cotizacion_venta.total_anticipo = respuesta['total_anticipo']
    obj.cotizacion_venta.total_gravada = respuesta['total_gravada']
    obj.cotizacion_venta.total_inafecta = respuesta['total_inafecta']
    obj.cotizacion_venta.total_exonerada = respuesta['total_exonerada']
    obj.cotizacion_venta.total_igv = respuesta['total_igv']
    obj.cotizacion_venta.total_gratuita = respuesta['total_gratuita']
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
    cotizacion_venta = models.ForeignKey(CotizacionVenta, on_delete=models.CASCADE, related_name='ConfirmacionVenta_cotizacion_venta')
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='ConfirmacionVenta_cliente', blank=True, null=True)
    cliente_interlocutor = models.ForeignKey(InterlocutorCliente, on_delete=models.PROTECT, related_name='ConfirmacionVenta_cliente_interlocutor', blank=True, null=True)
    sociedad = models.ForeignKey(Sociedad, on_delete=models.PROTECT)
    tipo_cambio = models.ForeignKey(TipoCambio, on_delete=models.PROTECT, related_name='ConfirmacionVenta_tipo_cambio')
    moneda = models.ForeignKey(Moneda, on_delete=models.PROTECT, default=1)
    observacion = models.TextField(blank=True, null=True)
    condiciones_pago = models.CharField('Condiciones de Pago', max_length=50, blank=True, null=True, help_text='Factura a 30 días')
    tipo_venta = models.IntegerField('Tipo de Venta', choices=TIPO_VENTA, default=1)
    descuento_global = models.DecimalField('Descuento Global', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total_descuento = models.DecimalField('Total Descuento', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total_anticipo = models.DecimalField('Total Anticipo', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total_gravada = models.DecimalField('Total Gravada', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total_inafecta = models.DecimalField('Total Inafecta', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total_exonerada = models.DecimalField('Total Exonerada', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total_igv = models.DecimalField('Total IGV', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total_gratuita = models.DecimalField('Total Gratuita', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    otros_cargos = models.DecimalField('Otros cargos', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total = models.DecimalField('Total', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    estado = models.IntegerField(choices=ESTADOS_CONFIRMACION, default=1)
    sunat_transaction = models.IntegerField(choices=SUNAT_TRANSACTION, default=1)
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

    @property
    def monto_solicitado(self):
        return self.cotizacion_venta.monto_solicitado

    def __str__(self):
        return "%s%s" % (self.sociedad.abreviatura, self.cotizacion_venta)


class ConfirmacionVentaDetalle(models.Model):
    item = models.IntegerField(blank=True, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    id_registro = models.IntegerField()
    cantidad_confirmada = models.DecimalField('Cantidad confirmada', max_digits=22, decimal_places=10)
    precio_unitario_sin_igv = models.DecimalField('Precio unitario sin IGV',max_digits=22, decimal_places=10, default=Decimal('0.00'))
    precio_unitario_con_igv = models.DecimalField('Precio unitario con IGV',max_digits=22, decimal_places=10, default=Decimal('0.00'))
    precio_final_con_igv = models.DecimalField('Precio final con IGV',max_digits=22, decimal_places=10, default=Decimal('0.00'))
    descuento = models.DecimalField('Descuento',max_digits=14, decimal_places=2, default=Decimal('0.00'))
    sub_total = models.DecimalField('Sub Total',max_digits=14, decimal_places=2, default=Decimal('0.00'))
    igv = models.DecimalField('IGV',max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total = models.DecimalField('Total', max_digits=14, decimal_places=2, default=Decimal('0.00'))
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
    def producto(self):
        return self.content_type.get_object_for_this_type(id=self.id_registro)

    @property
    def cantidad(self):
        return self.cantidad_confirmada

    def __str__(self):
        return "%s - %s" % (self.item, self.producto)

def confirmacion_venta_detalle_post_save(*args, **kwargs):
    obj = kwargs['instance']
    respuesta = obtener_totales(obj.confirmacion_venta)
    obj.confirmacion_venta.total_descuento = respuesta['total_descuento']
    obj.confirmacion_venta.total_anticipo = respuesta['total_anticipo']
    obj.confirmacion_venta.total_gravada = respuesta['total_gravada']
    obj.confirmacion_venta.total_inafecta = respuesta['total_inafecta']
    obj.confirmacion_venta.total_exonerada = respuesta['total_exonerada']
    obj.confirmacion_venta.total_igv = respuesta['total_igv']
    obj.confirmacion_venta.total_gratuita = respuesta['total_gratuita']
    obj.confirmacion_venta.otros_cargos = respuesta['total_otros_cargos']
    obj.confirmacion_venta.total = respuesta['total']
    obj.confirmacion_venta.save()

post_save.connect(confirmacion_venta_detalle_post_save, sender=ConfirmacionVentaDetalle)


class ConfirmacionVentaCuota(models.Model):
    confirmacion_venta = models.ForeignKey(ConfirmacionVenta, on_delete=models.CASCADE, related_name='ConfirmacionVentaCuota_confirmacion_venta')
    monto = models.DecimalField(max_digits=14, decimal_places=2)
    dias_pago = models.IntegerField('Días de pago', blank=True, null=True)
    fecha_pago = models.DateField('Fecha de pago', auto_now=False, auto_now_add=False, blank=True, null=True)
    dias_calculo = models.IntegerField('Días de calculo', blank=True, null=True)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='ConfirmacionVentaCuota_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='ConfirmacionVentaCuota_updated_by', editable=False)

    class Meta:
        verbose_name = 'Confirmación Venta Cuota'
        verbose_name_plural = 'Confirmación Venta Cuotas'
        ordering = [
            'confirmacion_venta',
            'dias_calculo',
            ]

    @property
    def fecha(self):
        return date.today()

    @property
    def fecha_mostrar(self):
        if self.fecha_pago:
            return self.fecha_pago
        return date.today() + timedelta(self.dias_calculo)

    @property
    def dias_mostrar(self):
        return (self.fecha_mostrar - date.today()).days

    def save(self, **kwargs):
        if self.dias_pago:
            self.dias_calculo = self.dias_pago
        else:
            if self.fecha_pago:
                self.dias_calculo = (self.fecha_pago - self.fecha).days
            else:
                self.dias_calculo = 0
        
        return super().save(**kwargs)

    def __str__(self):
        return "%s - %s - %s - %s" % (self.confirmacion_venta, self.monto, self.dias_pago, self.fecha_pago)


class CotizacionSociedad(models.Model):
    cotizacion_venta_detalle = models.ForeignKey(CotizacionVentaDetalle, on_delete=models.CASCADE, related_name='CotizacionSociedad_cotizacion_venta_detalle')
    sociedad = models.ForeignKey(Sociedad, on_delete=models.PROTECT)
    cantidad = models.DecimalField('Cantidad', max_digits=22, decimal_places=10, default=Decimal('0.00'))

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
    
    @property
    def stock(self):
        return applications.material.funciones.stock(self.cotizacion_venta_detalle.content_type, self.cotizacion_venta_detalle.id_registro, self.sociedad.id)

    @property
    def color(self):
        if self.stock < self.cantidad:
            return "#" + colors.red.hexval()[2:]
        else:
            return "#" + colors.black.hexval()[2:]

    def __str__(self):
        return "%s - %s - %s" % (self.cotizacion_venta_detalle, self.sociedad, self.cantidad)

def cotizacion_sociedad_post_save(*args, **kwargs):
    obj = kwargs['instance']
    suma = Decimal('0.00')
    for detalle in obj.cotizacion_venta_detalle.CotizacionSociedad_cotizacion_venta_detalle.all():
        suma += detalle.cantidad
    obj.cotizacion_venta_detalle.cantidad = suma
    precio_unitario_con_igv = obj.cotizacion_venta_detalle.precio_unitario_con_igv
    precio_final_con_igv = obj.cotizacion_venta_detalle.precio_final_con_igv
    respuesta = calculos_linea(obj.cotizacion_venta_detalle.cantidad, precio_unitario_con_igv, precio_final_con_igv, igv(), obj.cotizacion_venta_detalle.tipo_igv)
    obj.cotizacion_venta_detalle.precio_unitario_sin_igv = respuesta['precio_unitario_sin_igv']
    obj.cotizacion_venta_detalle.precio_unitario_con_igv = precio_unitario_con_igv
    obj.cotizacion_venta_detalle.precio_final_con_igv = precio_final_con_igv
    obj.cotizacion_venta_detalle.sub_total = respuesta['subtotal']
    obj.cotizacion_venta_detalle.descuento = respuesta['descuento']
    obj.cotizacion_venta_detalle.igv = respuesta['igv']
    obj.cotizacion_venta_detalle.total = respuesta['total']
    obj.cotizacion_venta_detalle.save()

post_save.connect(cotizacion_sociedad_post_save, sender=CotizacionSociedad)


class CotizacionDescuentoGlobal(models.Model):
    cotizacion_venta = models.ForeignKey(CotizacionVenta, on_delete=models.CASCADE, related_name='CotizacionDescuentoGlobal_cotizacion_venta')
    sociedad = models.ForeignKey(Sociedad, on_delete=models.PROTECT)
    descuento_global = models.DecimalField('Descuento Global', max_digits=14, decimal_places=2, default=Decimal('0.00'))

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
    otros_cargos = models.DecimalField('Otros cargos', max_digits=14, decimal_places=2, default=Decimal('0.00'))

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


class ConfirmacionOrdenCompra(models.Model):
    numero_orden = models.CharField('Número de Orden', max_length=100)
    fecha_orden = models.DateField('Fecha Orden', auto_now=False, auto_now_add=False)
    documento = models.FileField('Documento', upload_to=ORDEN_COMPRA_CONFIRMACION, max_length=100, blank=True, null=True)
    confirmacion_venta = models.OneToOneField(ConfirmacionVenta, on_delete=models.PROTECT, related_name='ConfirmacionOrdenCompra_confirmacion_venta')

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='ConfirmacionOrdenCompra_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='ConfirmacionOrdenCompra_updated_by', editable=False)

    class Meta:
        verbose_name = 'Confirmacion Orden Compra'
        verbose_name_plural = 'Confirmaciones Orden Compra'

    def __str__(self):
        return str(self.numero_orden)