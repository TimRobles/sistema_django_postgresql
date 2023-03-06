from django.conf import settings
from django.db import models
from datetime import datetime
from decimal import Decimal

from django.contrib.contenttypes.models import ContentType
from django.core.validators import MaxValueValidator, MinValueValidator


from applications.datos_globales.models import Moneda, Area, Cargo, Sociedad
from applications.variables import TIPOS_COMISION, ESTADOS

class FondoPensiones(models.Model):
    nombre = models.CharField('Nombre Fondo de Pensiones', max_length=50)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='FondoPensiones_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='FondoPensiones_updated_by', editable=False)

    class Meta:
        verbose_name = 'Fondo de Pension'
        verbose_name_plural = 'Fondo de Pensiones'

    def __str__(self):

        return str(self.id)



class ComisionFondoPensiones(models.Model):
    fondo_pensiones = models.ForeignKey(FondoPensiones, on_delete=models.PROTECT)  
    fecha_vigencia = models.DateField('Fecha Vigencia', auto_now=False, auto_now_add=False)
    aporte_obligatorio = models.DecimalField('Aporte Obligatorio', max_digits=2, decimal_places=2)
    comision_flujo = models.DecimalField('Comision Flujo', max_digits=4, decimal_places=4)
    comision_flujo_mixta = models.DecimalField('Comision Flujo Mixta', max_digits=4, decimal_places=4)
    prima_seguro = models.DecimalField('Prima Seguro', max_digits=4, decimal_places=4)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='ComisionFondoPensiones_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='ComisionFondoPensiones_updated_by', editable=False)

    class Meta:
        verbose_name = 'Comision Fondo Pension'
        verbose_name_plural = 'Comision Fondos Pensiones'

    def __str__(self):
        return str(self.id)



class DatosPlanilla(models.Model):
    fecha_inicio = models.DateField('Fecha Inicio', auto_now=False, auto_now_add=False)
    fecha_baja = models.DateField('Fecha Baja', auto_now=False, auto_now_add=False)
    sueldo_bruto = models.DecimalField('Sueldo Bruto', max_digits=7, decimal_places=2)
    moneda = models.ForeignKey(Moneda, null=True,  on_delete=models.PROTECT)
    movilidad = models.DecimalField('Movilidad', max_digits=7, decimal_places=2, default=Decimal('0.00'))
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Usuarios', on_delete=models.PROTECT, related_name='DatosPlanilla_suspension_cuarta')
    planilla = models.BooleanField()
    suspension_cuarta = models.BooleanField('Suspención de 4ta categoria', default=False)
    fondo_pensiones = models.ForeignKey(FondoPensiones, on_delete=models.PROTECT)  
    tipo_comision = models.IntegerField(choices=TIPOS_COMISION, default=1)
    asignacion_familiar = models.BooleanField()
    area = models.ForeignKey(Area, null=True,  on_delete=models.PROTECT)
    cargo = models.ForeignKey(Cargo, null=True,  on_delete=models.PROTECT)
    sociedad = models.ForeignKey(Sociedad, null=True,  on_delete=models.PROTECT)
    estado = models.IntegerField(choices=ESTADOS, default=1)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='DatosPlanilla_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='DatosPlanilla_updated_by', editable=False)

    class Meta:
        verbose_name = 'Datos Planilla'
        verbose_name_plural = 'Datos Planillas'

    def __str__(self):
        return str(self.id)



class EsSalud(models.Model):
    fecha_inicio = models.DateField('Fecha Inicio', auto_now=False, auto_now_add=False)
    porcentaje = models.DecimalField('Porcentaje', max_digits=4, decimal_places=4)
    ley30334 = models.BooleanField()

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='EsSalud_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='EsSalud_updated_by', editable=False)

    class Meta:
        verbose_name = 'EsSalud'
        verbose_name_plural = 'Es Salud'

    def __str__(self):
        return str(self.id)


class BoletaPago(models.Model):
    datos_planilla = models.ForeignKey(DatosPlanilla, null=True,  on_delete=models.PROTECT)
    year = models.IntegerField(default=datetime.date.today().year, validators=[MinValueValidator(2015), MaxValueValidator(datetime.date.today().year)])
    month = models.IntegerField()
    tipo = models.IntegerField()
    haber_mensual = models.DecimalField('Haber Mensual', max_digits=7, decimal_places=2)
    lic_con_goce_haber = models.DecimalField('Licencia con goce de haber', max_digits=7, decimal_places=2, default=Decimal('0.00'))
    dominical = models.DecimalField('Dominical', max_digits=7, decimal_places=2, default=Decimal('0.00'))
    movilidad = models.DecimalField('Movilidad', max_digits=7, decimal_places=2, default=Decimal('0.00'))
    asig_familiar = models.DecimalField('Asignación Familiar', max_digits=7, decimal_places=2, default=Decimal('0.00'))
    vacaciones = models.DecimalField('Vacaciones', max_digits=7, decimal_places=2, default=Decimal('0.00'))
    gratificacion = models.DecimalField('Gratificación', max_digits=7, decimal_places=2, default=Decimal('0.00'))
    ley29351 = models.DecimalField('Ley29351', max_digits=7, decimal_places=2, default=Decimal('0.00'))
    bonif_1mayo = models.DecimalField('Bonificación 1 Mayo', max_digits=7, decimal_places=2, default=Decimal('0.00'))
    essalud = models.DecimalField('Essalud', max_digits=7, decimal_places=2, default=Decimal('0.00'))
    aporte_obligatorio = models.DecimalField('Aporte Obligatorio', max_digits=7, decimal_places=2, default=Decimal('0.00'))
    comision_porcentaje = models.DecimalField('Comisión Porcentaje', max_digits=7, decimal_places=2, default=Decimal('0.00'))
    prima_seguro = models.DecimalField('Prima Seguro', max_digits=7, decimal_places=2, default=Decimal('0.00'))
    impuesto_quinta = models.DecimalField('Impuesto de Quinta', max_digits=7, decimal_places=2, default=Decimal('0.00'))
    neto_recibido = models.DecimalField('Neto Recibido', max_digits=7, decimal_places=2, default=Decimal('0.00'))
    estado = models.IntegerField(choices=ESTADOS, default=1)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='BoletaPago_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='BoletaPago_updated_by', editable=False)
    
    class Meta:
        verbose_name = 'Boleta de Pago'
        verbose_name_plural = 'Boletas de Pago'

    def __str__(self):
        return str(self.id)



class ReciboBoletaPago(models.Model):
    boleta_pago = models.ForeignKey(BoletaPago, null=True,  on_delete=models.PROTECT)
    fecha_pagar = models.DateField('Fecha Pagar', auto_now=False, auto_now_add=False)
    tipo_pago = models.IntegerField()
    monto = models.DecimalField('Monto', max_digits=7, decimal_places=2)
    redondeo = models.DecimalField('Redondeo', max_digits=3, decimal_places=2, default=0)
    monto_pagado = models.DecimalField('Monto Pagado', max_digits=7, decimal_places=2, default=0)
    voucher = models.FileField('Voucher', upload_to=None, max_length=100)
    fecha_pago = models.DateField('Fecha de Pago', auto_now=False, auto_now_add=False)
    content_type = models.ForeignKey(ContentType, blank=True, null=True, on_delete=models.PROTECT)
    id_registro = models.IntegerField(blank=True, null=True)   
    estado = models.IntegerField(choices=ESTADOS, default=1)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='ReciboBoletaPago_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='ReciboBoletaPago_updated_by', editable=False)
    

    class Meta:

        verbose_name = 'Recibo Boleta Pago'
        verbose_name_plural = 'Recibos Boleta Pago'

    def __str__(self):
        return str(self.id)

