from datetime import timedelta
from django.db import models
from applications.clientes.models import Cliente, InterlocutorCliente
from applications.cotizacion.models import CotizacionVenta
from applications.datos_globales.models import Moneda
from applications.variables import ESTADO_SOLICITUD, ESTADOS
from django.conf import settings

from django.db.models.signals import pre_save, post_save, pre_delete, post_delete


class LineaCredito(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='LineaCredito_cliente', blank=True, null=True)
    monto = models.DecimalField('Monto', max_digits=7, decimal_places=2)
    moneda = models.ForeignKey(Moneda, on_delete=models.PROTECT)
    condiciones_pago = models.CharField('Condiciones de pago', max_length=250)
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
    total_cotizado = models.DecimalField('Total Cotizado', max_digits=14, decimal_places=2, default=0)
    total_credito = models.DecimalField('Total Crédito', max_digits=14, decimal_places=2, default=0)
    condiciones_pago = models.CharField('Condiciones de pago', max_length=250, blank=True, null=True)
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

    def save(self):
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
        
        return super().save()

    def __str__(self):
        return "%s - %s - %s - %s" % (self.solicitud_credito, self.monto, self.dias_pago, self.fecha_pago)


