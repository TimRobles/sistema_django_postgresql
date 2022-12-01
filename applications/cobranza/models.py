from datetime import date, timedelta
from decimal import Decimal
from django.db import models
from django.db.models import Sum
from reportlab.lib import colors
from applications.clientes.models import Cliente, InterlocutorCliente
from applications.cobranza.funciones import convertir_moneda
from applications.cotizacion.models import CotizacionVenta
from applications.datos_globales.models import CuentaBancariaSociedad, Moneda
from applications.sociedad.models import Sociedad
from applications.variables import ESTADO_SOLICITUD, ESTADOS
from django.conf import settings
from django.contrib.contenttypes.models import ContentType

from django.db.models.signals import pre_save, post_save, pre_delete, post_delete


class LineaCredito(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='LineaCredito_cliente', blank=True, null=True)
    monto = models.DecimalField('Monto', max_digits=7, decimal_places=2)
    moneda = models.ForeignKey(Moneda, on_delete=models.PROTECT)
    condiciones_pago = models.CharField('Condiciones de pago', max_length=250, help_text='Factura a 30 días')
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


class SolicitudCredito(models.Model):
    cotizacion_venta = models.OneToOneField(CotizacionVenta, on_delete=models.CASCADE, related_name='SolicitudCredito_cotizacion_venta')
    total_cotizado = models.DecimalField('Total Cotizado', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total_credito = models.DecimalField('Total Crédito', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    condiciones_pago = models.CharField('Condiciones de pago', max_length=250, blank=True, null=True, help_text='Factura a 30 días')
    interlocutor_solicita = models.ForeignKey(InterlocutorCliente, on_delete=models.PROTECT, blank=True, null=True)
    estado = models.IntegerField(choices=ESTADO_SOLICITUD, default=1)
    aprobado_por = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Aprobado por', on_delete=models.RESTRICT, blank=True, null=True)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='SolicitudCredito_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='SolicitudCredito_updated_by', editable=False)

    class Meta:
        verbose_name = 'Solicitud de Credito'
        verbose_name_plural = 'Solicitudes de Credito'

    @property
    def total_cuotas(self):
        total = Decimal('0.00')
        if hasattr(self, 'SolicitudCreditoCuota_solicitud_credito'):
            for cuota in self.SolicitudCreditoCuota_solicitud_credito.all():
                total += cuota.monto
        return total

    def __str__(self):
        return "%s - %s - %s" % (self.cotizacion_venta.cliente.razon_social, self.total_credito, self.get_estado_display())


class SolicitudCreditoCuota(models.Model):
    solicitud_credito = models.ForeignKey(SolicitudCredito, on_delete=models.CASCADE, related_name='SolicitudCreditoCuota_solicitud_credito')
    monto = models.DecimalField(max_digits=14, decimal_places=2)
    dias_pago = models.IntegerField('Días de pago', blank=True, null=True)
    fecha_pago = models.DateField('Fecha de pago', auto_now=False, auto_now_add=False, blank=True, null=True)
    dias_calculo = models.IntegerField('Días de calculo', blank=True, null=True)
    fecha_calculo = models.DateField('Fecha de calculo', auto_now=False, auto_now_add=False, blank=True, null=True)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='SolicitudCreditoCuota_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='SolicitudCreditoCuota_updated_by', editable=False)

    class Meta:
        verbose_name = 'Solicitud de Credito Cuota'
        verbose_name_plural = 'Solicitud de Credito Cuotas'
        ordering = [
            'solicitud_credito',
            'fecha_calculo',
            ]

    @property
    def fecha(self):
        try:
            return self.solicitud_credito.cotizacion_venta.ConfirmacionVenta_cotizacion_venta.latest('created_at').created_at
        except:
            return self.solicitud_credito.cotizacion_venta.fecha_cotizacion

    def save(self, **kwargs):
        if self.fecha_pago:
            self.fecha_calculo = self.fecha_pago
        else:
            self.fecha_calculo = self.fecha + timedelta(days=self.dias_pago)

        if self.dias_pago:
            self.dias_calculo = self.dias_pago
        else:
            if self.fecha_pago:
                self.dias_calculo = (self.fecha_pago - self.fecha).days
            else:
                self.dias_calculo = 0
        
        return super().save(**kwargs)

    def __str__(self):
        return "%s - %s - %s - %s" % (self.solicitud_credito, self.monto, self.dias_pago, self.fecha_pago)


# class Nota(models.Model):
#     nota_credito = models.ForeignKey(NotaCredito, on_delete=models.CASCADE)
#     monto = models.DecimalField(max_digits=14, decimal_places=2)
#     moneda = models.ForeignKey(Moneda, on_delete=models.PROTECT)
#     fecha = models.DateField(auto_now=False, auto_now_add=False)
#     tipo_cambio = models.DecimalField('Tipo de Cambio', max_digits=5, decimal_places=3)
#     sociedad = models.ForeignKey(Sociedad, on_delete=models.PROTECT)
#     cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)

#     created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
#     created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Nota_created_by', editable=False)
#     updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
#     updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Nota_updated_by', editable=False)

#     class Meta:
#         verbose_name = 'Nota'
#         verbose_name_plural = 'Notas'

#     def __str__(self):
#         return "%s" % (self.monto)


class Ingreso(models.Model):
    monto = models.DecimalField(max_digits=14, decimal_places=2)
    cuenta_bancaria = models.ForeignKey(CuentaBancariaSociedad, on_delete=models.PROTECT)
    fecha = models.DateField(auto_now=False, auto_now_add=False)
    numero_operacion = models.CharField('Número de operación', max_length=100)
    cuenta_origen = models.CharField('Cuenta de Origen', max_length=100, blank=True, null=True)
    comentario = models.CharField('Comentario', max_length=100, blank=True, null=True)
    comision = models.DecimalField('Comisión', max_digits=5, decimal_places=2)
    tipo_cambio = models.DecimalField('Tipo de Cambio', max_digits=5, decimal_places=3)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Ingreso_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Ingreso_updated_by', editable=False)

    class Meta:
        verbose_name = 'Ingreso'
        verbose_name_plural = 'Ingresos'

    @property
    def tipo(self):
        return 'Ingreso'

    @property
    def moneda(self):
        return self.cuenta_bancaria.moneda

    @property
    def pagos(self):
        return Pago.objects.filter(
            content_type = ContentType.objects.get_for_model(self),
            id_registro = self.id,
            )
    
    @property
    def usado(self):
        if self.pagos.aggregate(Sum('monto'))['monto__sum']:
            return self.pagos.aggregate(Sum('monto'))['monto__sum']
        else:
            return Decimal('0.00')

    @property
    def saldo(self):
        return self.monto - self.usado

    def __str__(self):
        return "Ingreso %s %s %s %s (%s %s)" % (self.cuenta_bancaria.sociedad.alias, self.cuenta_bancaria.banco.nombre_comercial, self.cuenta_bancaria.moneda.simbolo, self.monto, self.cuenta_bancaria.moneda.simbolo, self.saldo)


class Egreso(models.Model):
    monto = models.DecimalField(max_digits=14, decimal_places=2)
    cuenta_bancaria = models.ForeignKey(CuentaBancariaSociedad, on_delete=models.PROTECT)
    fecha = models.DateField(auto_now=False, auto_now_add=False)
    numero_operacion = models.CharField('Número de operación', max_length=100)
    cuenta_destino = models.CharField('Cuenta de Origen', max_length=100, blank=True, null=True)
    comentario = models.CharField('Comentario', max_length=100, blank=True, null=True)
    comision = models.DecimalField('Comisión', max_digits=5, decimal_places=2)
    tipo_cambio = models.DecimalField('Tipo de Cambio', max_digits=5, decimal_places=3)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Egreso_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Egreso_updated_by', editable=False)

    class Meta:
        verbose_name = 'Egreso'
        verbose_name_plural = 'Egresos'

    @property
    def moneda(self):
        return self.cuenta_bancaria.moneda

    def __str__(self):
        return "%s" % (self.monto)


DIAS_SEGUIMIENTO = 5
class Deuda(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT, blank=True, null=True)
    id_registro = models.IntegerField(blank=True, null=True)
    monto = models.DecimalField('Monto', max_digits=14, decimal_places=2)
    moneda = models.ForeignKey(Moneda, on_delete=models.PROTECT)
    tipo_cambio = models.DecimalField('Tipo de Cambio', max_digits=5, decimal_places=3)
    fecha_deuda = models.DateField('Fecha de deuda', auto_now=False, auto_now_add=False)
    fecha_vencimiento = models.DateField('Fecha de vencimiento', auto_now=False, auto_now_add=False)
    sociedad = models.ForeignKey(Sociedad, on_delete=models.PROTECT)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='Deuda_cliente')

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Deuda_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Deuda_updated_by', editable=False)

    class Meta:
        verbose_name = 'Deuda'
        verbose_name_plural = 'Deudas'

    @property
    def pagos(self):
        try:
            pagos = self.Pago_deuda.all()
            total = Decimal('0.00')
            for pago in pagos:
                ingreso_nota = pago.content_type.get_object_for_this_type(id = pago.id_registro)
                total += (pago.monto * convertir_moneda(pago.tipo_cambio, ingreso_nota.moneda, self.moneda)).quantize(Decimal('0.00'))
            return total + self.redondeos
        except Exception as e:
            print(e)
            return Decimal('0.00') + self.redondeos

    @property
    def redondeos(self):
        try:
            redondeos = self.Redondeo_deuda.all()
            total = Decimal('0.00')
            for redondeo in redondeos:
                total += redondeo.monto
            return total
        except Exception as e:
            print(e)
            return Decimal('0.00')

    @property
    def saldo(self):
        return self.monto - self.pagos

    @property
    def color(self):
        if self.saldo == Decimal('0.00'):
            return "#" + colors.black.hexval()[2:]
        elif self.fecha_vencimiento > (date.today() + timedelta(DIAS_SEGUIMIENTO)):
            return "#" + colors.green.hexval()[2:]
        elif self.fecha_vencimiento < date.today():
            return "#" + colors.red.hexval()[2:]
        else:
            return "#" + colors.orange.hexval()[2:]

    @property
    def estado(self):
        if self.saldo == Decimal('0.00'):
            return 'CANCELADO'
        elif self.fecha_vencimiento > (date.today() + timedelta(DIAS_SEGUIMIENTO)):
            return 'PENDIENTE'
        elif self.fecha_vencimiento < date.today():
            return 'VENCIDO'
        else:
            return '%s DÍAS PARA VENCER' % ((self.fecha_vencimiento - date.today()).days)

    @property
    def documento(self):
        if self.content_type:
            documento_venta = self.content_type.get_object_for_this_type(id = self.id_registro)
            return '%s %s - %s' % (documento_venta.get_tipo_comprobante_display(), documento_venta.documento, documento_venta.cliente)
        return ""

    def __str__(self):
        return "%s %s %s (%s %s)" % (self.documento, self.moneda.simbolo, self.monto, self.moneda.simbolo, self.saldo)


class Cuota(models.Model):
    deuda = models.ForeignKey(Deuda, on_delete=models.CASCADE, related_name='Cuota_deuda')
    fecha = models.DateField(auto_now=False, auto_now_add=False)
    monto = models.DecimalField(max_digits=14, decimal_places=2)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Cuota_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Cuota_updated_by', editable=False)

    class Meta:
        verbose_name = 'Cuota'
        verbose_name_plural = 'Cuotas'
        ordering = [
            'deuda',
            'fecha',
            ]

    @property
    def saldo(self):
        saldo = self.deuda.Cuota_deuda.filter(fecha__lte=self.fecha).aggregate(Sum('monto'))['monto__sum'] - self.deuda.pagos
        if saldo > self.monto:
            return self.monto
        elif saldo <= Decimal('0.00'):
            return Decimal('0.00')
        else:
            return saldo
        # return self.deuda.Cuota_deuda.filter(fecha__lte=self.fecha).aggregate(Sum('monto'))['monto__sum'] - self.deuda.pagos

    @property
    def color(self):
        if self.saldo <= Decimal('0.00'):
            return "#" + colors.black.hexval()[2:]
        elif self.fecha > (date.today() + timedelta(DIAS_SEGUIMIENTO)):
            return "#" + colors.green.hexval()[2:]
        elif self.fecha < date.today():
            return "#" + colors.red.hexval()[2:]
        else:
            return "#" + colors.orange.hexval()[2:]

    @property
    def estado(self):
        if self.saldo <= Decimal('0.00'):
            return 'CANCELADO'
        elif self.fecha > (date.today() + timedelta(DIAS_SEGUIMIENTO)):
            return 'PENDIENTE'
        elif self.fecha < date.today():
            return 'VENCIDO'
        else:
            return '%s DÍAS PARA VENCER' % ((self.fecha - date.today()).days)

    def __str__(self):
        return "%s - %s" % (self.fecha, self.monto)


class Redondeo(models.Model):
    deuda = models.ForeignKey(Deuda, on_delete=models.CASCADE, related_name='Redondeo_deuda')
    fecha = models.DateField(auto_now=False, auto_now_add=False)
    monto = models.DecimalField(max_digits=14, decimal_places=2)
    moneda = models.ForeignKey(Moneda, on_delete=models.PROTECT)
    tipo_cambio = models.DecimalField('Tipo de cambio', max_digits=5, decimal_places=3)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Redondeo_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Redondeo_updated_by', editable=False)

    class Meta:
        verbose_name = 'Redondeo'
        verbose_name_plural = 'Redondeos'

    def __str__(self):
        return "%s - %s" % (self.fecha, self.monto)


class Pago(models.Model):
    deuda = models.ForeignKey(Deuda, on_delete=models.CASCADE, related_name='Pago_deuda')
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT, blank=True, null=True)
    id_registro = models.IntegerField(blank=True, null=True)
    monto = models.DecimalField('Monto', max_digits=14, decimal_places=2, blank=True, null=True)
    tipo_cambio = models.DecimalField('Tipo de cambio', max_digits=5, decimal_places=3, blank=True, null=True)
    
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Pago_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Pago_updated_by', editable=False)

    class Meta:
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'

    @property
    def ingreso_nota(self):
        return self.content_type.get_object_for_this_type(id = self.id_registro)

    @property
    def monto_final(self):
        if self.deuda.moneda == self.ingreso_nota.moneda:
            return self.monto
        else:
            return (self.monto * convertir_moneda(self.tipo_cambio, self.ingreso_nota.moneda, self.deuda.moneda)).quantize(Decimal('0.00'))    

    def __str__(self):
        return "%s" % (self.monto)


class Retiro(models.Model):
    egreso = models.ForeignKey(Egreso, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT, blank=True, null=True)
    id_registro = models.IntegerField(blank=True, null=True)
    monto = models.DecimalField('Monto', max_digits=14, decimal_places=2, blank=True, null=True)
    tipo_cambio = models.DecimalField('Tipo de cambio', max_digits=5, decimal_places=3, blank=True, null=True)
    
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Retiro_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Retiro_updated_by', editable=False)

    class Meta:
        verbose_name = 'Retiro'
        verbose_name_plural = 'Retiros'

    def __str__(self):
        return "%s" % (self.monto)