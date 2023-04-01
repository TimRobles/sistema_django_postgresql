from django.conf import settings
from django.db import models
from datetime import datetime
from decimal import Decimal

from django.contrib.contenttypes.models import ContentType
from django.core.validators import MaxValueValidator, MinValueValidator


from applications.datos_globales.models import Moneda, Area, Cargo, Sociedad, Banco
from applications.variables import TIPOS_COMISION, ESTADOS, TIPO_PAGO_BOLETA, TIPO_PAGO_RECIBO, MESES

from applications.rutas import CONTABILIDAD_FOTO_CHEQUE

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

        return str(self.nombre)

class ComisionFondoPensiones(models.Model):
    fondo_pensiones = models.ForeignKey(FondoPensiones, on_delete=models.PROTECT, related_name='ComisionFondoPensiones_fondo_pensiones')
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
    fecha_inicio = models.DateField('Fecha Inicio', auto_now=False, auto_now_add=False, blank=True, null=True)
    fecha_baja = models.DateField('Fecha Baja', auto_now=False, auto_now_add=False, blank=True, null=True)
    sueldo_bruto = models.DecimalField('Sueldo Bruto', max_digits=7, decimal_places=2, blank=True, null=True)
    moneda = models.ForeignKey(Moneda, on_delete=models.PROTECT,  blank=True, null=True)
    movilidad = models.DecimalField('Movilidad', max_digits=7, decimal_places=2, default=Decimal('0.00'),  blank=True, null=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Usuario', on_delete=models.PROTECT, related_name='DatosPlanilla_usuario')
    planilla = models.BooleanField()
    suspension_cuarta = models.BooleanField('Suspención de 4ta categoria', default=False)
    fondo_pensiones = models.ForeignKey(FondoPensiones, on_delete=models.PROTECT, blank=True, null=True)  
    tipo_comision = models.IntegerField(choices=TIPOS_COMISION, blank=True, null=True)
    asignacion_familiar = models.BooleanField()
    area = models.ForeignKey(Area, on_delete=models.PROTECT, blank=True, null=True)
    cargo = models.ForeignKey(Cargo, on_delete=models.PROTECT, blank=True, null=True)
    sociedad = models.ForeignKey(Sociedad,on_delete=models.PROTECT,  blank=True, null=True)
    estado = models.IntegerField(choices=ESTADOS, default=1)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='DatosPlanilla_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='DatosPlanilla_updated_by', editable=False)

    class Meta:
        verbose_name = 'Datos Planilla'
        verbose_name_plural = 'Datos Planillas'

    def __str__(self):
        return str(self.usuario)

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
    year = models.IntegerField('Año', validators=[MinValueValidator(2015),MaxValueValidator(datetime.now().year)], default=datetime.now().year ,blank=True, null=True)
    month = models.IntegerField('Mes',choices=MESES, blank=True, null=True)
    tipo = models.IntegerField(choices=TIPO_PAGO_BOLETA, blank=True, null=True)
    haber_mensual = models.DecimalField('Haber Mensual', max_digits=7, decimal_places=2, blank=True, null=True)
    lic_con_goce_haber = models.DecimalField('Licencia con goce de haber', max_digits=7, decimal_places=2, default=Decimal('0.00'), blank=True, null=True)
    dominical = models.DecimalField('Dominical', max_digits=7, decimal_places=2, default=Decimal('0.00'), blank=True, null=True)
    movilidad = models.DecimalField('Movilidad', max_digits=7, decimal_places=2, default=Decimal('0.00'), blank=True, null=True)
    asig_familiar = models.DecimalField('Asignación Familiar', max_digits=7, decimal_places=2, default=Decimal('0.00'), blank=True, null=True)
    vacaciones = models.DecimalField('Vacaciones', max_digits=7, decimal_places=2, default=Decimal('0.00'), blank=True, null=True)
    gratificacion = models.DecimalField('Gratificación', max_digits=7, decimal_places=2, default=Decimal('0.00'), blank=True, null=True)
    ley29351 = models.DecimalField('Ley29351', max_digits=7, decimal_places=2, default=Decimal('0.00'), blank=True, null=True)
    bonif_1mayo = models.DecimalField('Bonificación 1 Mayo', max_digits=7, decimal_places=2, default=Decimal('0.00'), blank=True, null=True)
    essalud = models.DecimalField('Essalud', max_digits=7, decimal_places=2, default=Decimal('0.00'), blank=True, null=True)
    aporte_obligatorio = models.DecimalField('Aporte Obligatorio', max_digits=7, decimal_places=2, default=Decimal('0.00'), blank=True, null=True)
    comision_porcentaje = models.DecimalField('Comisión Porcentaje', max_digits=7, decimal_places=2, default=Decimal('0.00'), blank=True, null=True)
    prima_seguro = models.DecimalField('Prima Seguro', max_digits=7, decimal_places=2, default=Decimal('0.00'), blank=True, null=True)
    impuesto_quinta = models.DecimalField('Impuesto de Quinta', max_digits=7, decimal_places=2, default=Decimal('0.00'), blank=True, null=True)
    neto_recibido = models.DecimalField('Neto Recibido', max_digits=7, decimal_places=2, default=Decimal('0.00'), blank=True, null=True)
    estado = models.IntegerField(choices=ESTADOS, default=1, blank=True, null=True)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='BoletaPago_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='BoletaPago_updated_by', editable=False)
    
    class Meta:
        verbose_name = 'Boleta de Pago'
        verbose_name_plural = 'Boletas de Pago'
        ordering = ['-id',]


    def __str__(self):
        return "%s - %s  - %s - %s" % (self.get_month_display(), self.year, self.get_tipo_display(), self.datos_planilla ) 

class ReciboBoletaPago(models.Model):
    boleta_pago = models.ForeignKey(BoletaPago, null=True,  on_delete=models.PROTECT)
    fecha_pagar = models.DateField('Fecha Pagar', auto_now=False, auto_now_add=False)
    tipo_pago = models.IntegerField(choices=TIPO_PAGO_RECIBO, blank=True, null=True)
    monto = models.DecimalField('Monto', max_digits=7, decimal_places=2, blank=True, null=True)
    redondeo = models.DecimalField('Redondeo', max_digits=3, decimal_places=2, default=0, blank=True, null=True)
    monto_pagado = models.DecimalField('Monto Pagado', max_digits=7, decimal_places=2, default=0, blank=True, null=True)
    voucher = models.FileField('Voucher', upload_to=None, max_length=100, blank=True, null=True)
    fecha_pago = models.DateField('Fecha de Pago', auto_now=False, auto_now_add=False, blank=True, null=True)
    content_type = models.ForeignKey(ContentType, blank=True, null=True, on_delete=models.PROTECT) #Cheque / Telecrédito / Caja Chica
    id_registro = models.IntegerField(blank=True, null=True)   
    estado = models.IntegerField(choices=ESTADOS, default=1, blank=True, null=True)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='ReciboBoletaPago_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='ReciboBoletaPago_updated_by', editable=False)
    
    class Meta:
        verbose_name = 'Recibo Boleta Pago'
        verbose_name_plural = 'Recibos Boleta Pago'
        ordering = ['-id',]

    def __str__(self):
        return "%s - %s  - %s - %s" % (self.boleta_pago.get_month_display(), self.boleta_pago.year, self.get_tipo_pago_display(), self.boleta_pago.datos_planilla ) 



class TipoServicio(models.Model):
    nombre = models.CharField('Servicio', max_length=50)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='TipoServicio_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='TipoServicio_updated_by', editable=False)

    class Meta:
        verbose_name = 'Tipo Servicio'
        verbose_name_plural = 'Tipos de Servicios'

    def __str__(self):
        return str(self.nombre)

class MedioPago(models.Model):
    nombre = models.CharField('Medio de Pago', max_length=50)
    
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='MedioPago_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='MedioPago_updated_by', editable=False)

    class Meta:
        verbose_name = 'Medio de Pago'
        verbose_name_plural = 'Medios de Pago'

    def __str__(self):
        return str(self.nombre)


class Institucion(models.Model):
    nombre = models.CharField('Institución', max_length=50)
    url = models.URLField('URL', max_length=200, null=True, blank=True)
    tipo_servicio = models.ForeignKey(TipoServicio, on_delete=models.CASCADE)
    medio_pago = models.ManyToManyField(MedioPago)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Institucion_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Institucion_updated_by', editable=False)

    class Meta:
        verbose_name = 'Institucion'
        verbose_name_plural = 'Instituciones'

    def __str__(self):
        return str(self.nombre)


class Servicio(models.Model):
    institucion = models.ForeignKey(Institucion, null=True, blank=True, on_delete=models.PROTECT)
    tipo_servicio = models.ForeignKey(TipoServicio, null=True,blank=True, on_delete=models.PROTECT)
    numero_referencia = models.CharField('Número de referencia', max_length=50,blank=True, null=True)
    titular_servicio = models.CharField('Titular del servicio', max_length=50,blank=True, null=True)
    direccion = models.CharField('Dirección', max_length=255,null=True,blank=True)
    alias = models.CharField('Alias', max_length=50,blank=True, null=True)
    estado = models.IntegerField(choices=ESTADOS,default=1)
    sociedad = models.ForeignKey(Sociedad, null=True,blank=True, on_delete=models.PROTECT)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Servicio_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Servicio_updated_by', editable=False)


    class Meta:
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'

    def __str__(self):
        return str(self.institucion)

class ReciboServicio(models.Model):
    servicio = models.ForeignKey(Servicio, blank=True, null=True, on_delete=models.PROTECT)
    foto = models.FileField('Foto', blank=True, null=True)
    fecha_emision = models.DateField('Fecha de Emision', auto_now=False, auto_now_add=False, blank=True, null=True)
    fecha_vencimiento = models.DateField('Fecha de Vencimiento', auto_now=False, auto_now_add=False, blank=True, null=True)
    monto = models.DecimalField('Monto', max_digits=7, decimal_places=2, blank=True, null=True)
    moneda = models.ForeignKey(Moneda, on_delete=models.PROTECT, blank=True, null=True)
    mora = models.DecimalField('Mora', max_digits=3, decimal_places=2, default=0)
    redondeo = models.DecimalField('Redondeo', max_digits=3, decimal_places=2, default=0)
    monto_pagado = models.DecimalField('Monto Pagado', max_digits=7, decimal_places=2, default=0)
    voucher = models.FileField('Voucher',blank=True, null=True)
    fecha_pago = models.DateField('Fecha de Pago', null=True)
    content_type = models.ForeignKey(ContentType, blank=True, null=True, on_delete=models.PROTECT)
    id_registro = models.IntegerField(blank=True, null=True)   
    estado = models.IntegerField(choices=ESTADOS, default=1)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='ReciboServicio_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='ReciboServicio_updated_by', editable=False)

    class Meta:
        verbose_name = 'Recibo de Servicio'
        verbose_name_plural = 'Recibos de Servicios'

    def __str__(self):
        return str(self.servicio)


class Telecredito(models.Model):
    concepto = models.CharField('Concepto', max_length=50)
    moneda = models.ForeignKey(Moneda, on_delete=models.PROTECT,  blank=True, null=True)
    banco = models.ForeignKey(Banco, on_delete=models.PROTECT,  blank=True, null=True)
    numero = models.CharField('Numero', max_length=50, blank=True, null=True)
    monto = models.DecimalField('Monto', max_digits=7, decimal_places=2, default=0)
    fecha_emision = models.DateField('Fecha de Emisión', auto_now=False, auto_now_add=False)
    fecha_cobro = models.DateField('Fecha de Cobro', auto_now=False, auto_now_add=False, blank=True, null=True)
    foto = models.FileField('Foto', null=True)
    monto_usado = models.DecimalField('Monto Usado', max_digits=7, decimal_places=2, default=0)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Usuario', on_delete=models.PROTECT, related_name='Telecredito_usuario')
    sociedad = models.ForeignKey(Sociedad, null=True,blank=True, on_delete=models.PROTECT)
    estado = models.IntegerField(choices=ESTADOS,default=1)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Telecredito_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Telecredito_updated_by', editable=False)

    class Meta:
        verbose_name = 'Telecredito'
        verbose_name_plural = 'Telecreditos'

    @property
    def content_type(self):
        return ContentType.objects.get_for_model(self)

    def __str__(self):
        return str(id)


class Cheque(models.Model):
    ESTADO_CHEQUE = (
        (1, 'ABIERTO'),
        (2, 'SOLICITADO'),
        (3, 'POR CERRAR'),
        (4, 'CERRADO'),
        )
    
    concepto = models.CharField('Concepto', max_length=50, default='Nuevo Cheque')
    moneda = models.ForeignKey(Moneda, on_delete=models.PROTECT, blank=True, null=True)
    monto_cheque = models.DecimalField('Monto del cheque', max_digits=7, decimal_places=2, default=0)
    monto_usado = models.DecimalField('Monto Usado', max_digits=7, decimal_places=2, default=0)
    redondeo = models.DecimalField('Redondeo', max_digits=7, decimal_places=2, default=0)
    vuelto = models.DecimalField('Vuelto', max_digits=7, decimal_places=2, default=0)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='Cheque_usuario', blank=True, null=True)
    sociedad = models.ForeignKey(Sociedad, on_delete=models.PROTECT)
    estado = models.IntegerField('Estado', choices=ESTADO_CHEQUE, default=1)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Cheque_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Cheque_updated_by', editable=False)

    class Meta:
        verbose_name = 'Cheque'
        verbose_name_plural = 'Cheques'
        ordering = ['estado', 'concepto',]

    def __str__(self):
        if self.moneda:
            return self.concepto + ' ' + self.usuario.username + ' ' + self.sociedad.razon_social + ' ' + self.get_estado_display() + ' ' + self.moneda.nombre
        else:
            return self.concepto + ' ' + self.usuario.username + ' ' + self.sociedad.razon_social + ' ' + self.get_estado_display()
        

class ChequeFisico(models.Model):
    ESTADO_CHEQUE_FISICO = (
        (1, 'ABIERTO'),
        (2, 'SOLICITADO'),
        (3, 'POR CERRAR'),
        (4, 'CERRADO'),
        )
    
    banco = models.ForeignKey(Banco, on_delete=models.PROTECT, blank=True, null=True)
    numero = models.CharField('Número de cheque', max_length=50, blank=True, null=True)
    responsable = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT)
    monto = models.DecimalField('Monto del cheque', max_digits=7, decimal_places=2, default=0)
    fecha_emision = models.DateField('Fecha de emisión del cheque', auto_now=False, auto_now_add=False, blank=True, null=True)
    fecha_cobro = models.DateField('Fecha de cobro del cheque', auto_now=False, auto_now_add=False, blank=True, null=True)
    foto = models.ImageField('Foto del cheque', upload_to=CONTABILIDAD_FOTO_CHEQUE, height_field=None, width_field=None, max_length=None, blank=True, null=True)
    estado = models.IntegerField('Estado', choices=ESTADO_CHEQUE_FISICO, default=1)
    cheque = models.ForeignKey(Cheque, on_delete=models.CASCADE, related_name='ChequeFisico_cheque', blank=True, null=True)
    
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='ChequeFisico_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='ChequeFisico_updated_by', editable=False)

    class Meta:
        verbose_name = 'Cheque Fisico'
        verbose_name_plural = 'Cheques Fisicos'

    def __str__(self):
        return str(self.cheque)


class ChequeVueltoExtra(models.Model):
    vuelto_original = models.DecimalField('Vuelto en Efectivo', max_digits=7, decimal_places=2)
    vuelto_extra = models.DecimalField('Vuelto en Moneda del Cheque', max_digits=7, decimal_places=2)
    moneda = models.ForeignKey(Moneda, on_delete=models.PROTECT)
    tipo_cambio = models.DecimalField('Tipo de Cambio', max_digits=6, decimal_places=4)
    cheque = models.ForeignKey(Cheque, on_delete=models.CASCADE, related_name='ChequeVueltoExtra_cheque', blank=True, null=True)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='ChequeVueltoExtra_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='ChequeVueltoExtra_updated_by', editable=False)

    class Meta:
        verbose_name = 'Cheque Vuelto Extra'
        verbose_name_plural = 'Cheque Vueltos Extras'

    def __str__(self):
        if self.cheque:
            return str(self.cheque) + " " + self.moneda.simbolo + " " + str(self.vuelto_extra)
        else:
            return self.moneda.simbolo + " " + str(self.vuelto_extra)