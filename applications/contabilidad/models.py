from django.conf import settings
from django.db import models
from datetime import datetime
from decimal import Decimal

from django.contrib.contenttypes.models import ContentType
from django.core.validators import MaxValueValidator, MinValueValidator
import applications

from applications.datos_globales.models import Moneda, Area, Cargo, Sociedad, Banco
from applications.home.templatetags.funciones_propias import nombre_usuario
from applications.variables import ESTADOS_RECIBO, TIPOS_COMISION, ESTADOS, TIPO_PAGO_BOLETA, TIPO_PAGO_RECIBO, MESES

from applications.rutas import CONTABILIDAD_FOTO_CHEQUE
from applications.caja_chica import funciones
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete

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
        ordering = [
            '-fecha_vigencia',
            'fondo_pensiones',
        ]

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
        ordering = [
            'estado',
            '-fecha_inicio',
            ]

    def __str__(self):
        return f"{self.usuario.username} - {self.sociedad.abreviatura}"
        

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
    compra_vacaciones = models.DecimalField('Compra de Vacaciones', max_digits=7, decimal_places=2, default=Decimal('0.00'), blank=True, null=True)
    gratificacion = models.DecimalField('Gratificación', max_digits=7, decimal_places=2, default=Decimal('0.00'), blank=True, null=True)
    ley29351 = models.DecimalField('Ley29351', max_digits=7, decimal_places=2, default=Decimal('0.00'), blank=True, null=True)
    bonif_1mayo = models.DecimalField('Bonificación 1 Mayo', max_digits=7, decimal_places=2, default=Decimal('0.00'), blank=True, null=True)
    essalud = models.DecimalField('Essalud', max_digits=7, decimal_places=2, default=Decimal('0.00'), blank=True, null=True)
    aporte_obligatorio = models.DecimalField('Aporte Obligatorio', max_digits=7, decimal_places=2, default=Decimal('0.00'), blank=True, null=True)
    comision = models.DecimalField('Comisión', max_digits=7, decimal_places=2, default=Decimal('0.00'), blank=True, null=True)
    prima_seguro = models.DecimalField('Prima Seguro', max_digits=7, decimal_places=2, default=Decimal('0.00'), blank=True, null=True)
    impuesto_quinta = models.DecimalField('Impuesto de Quinta', max_digits=7, decimal_places=2, default=Decimal('0.00'), blank=True, null=True)
    neto_recibido = models.DecimalField('Neto Recibido', max_digits=7, decimal_places=2, default=Decimal('0.00'), blank=True, null=True)
    cts = models.DecimalField('CTS', max_digits=7, decimal_places=2, default=Decimal('0.00'), blank=True, null=True)
    dias_trabajados = models.DecimalField('Días Trabajados', max_digits=2, decimal_places=0, default=Decimal('30'), blank=True, null=True)
    estado = models.IntegerField(choices=ESTADOS, default=1, blank=True, null=True)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='BoletaPago_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='BoletaPago_updated_by', editable=False)
    
    class Meta:
        verbose_name = 'Boleta de Pago'
        verbose_name_plural = 'Boletas de Pago'
        ordering = [
            '-year',
            '-month',
            'tipo',
            'datos_planilla',
            ]

    @property
    def periodo(self):
        return f"{self.get_month_display()} - {self.year}"

    @property
    def total_haber(self):
        return self.haber_mensual + self.lic_con_goce_haber + self.dominical + self.asig_familiar + self.movilidad + self.vacaciones + self.gratificacion + self.ley29351 + self.cts + self.bonif_1mayo

    @property
    def total_descuento_empleador(self):
        return self.essalud

    @property
    def total_descuento_trabajador(self):
        return self.aporte_obligatorio + self.comision + self.prima_seguro + self.impuesto_quinta

    @property
    def moneda(self):
        return self.datos_planilla.moneda

    def __str__(self):
        return "%s - %s  - %s - %s" % (self.get_month_display(), self.year, self.get_tipo_display(), self.datos_planilla) 

class ReciboBoletaPago(models.Model):
    boleta_pago = models.ForeignKey(BoletaPago, null=True,  on_delete=models.PROTECT)
    fecha_pagar = models.DateField('Fecha Pagar', auto_now=False, auto_now_add=False)
    tipo_pago = models.IntegerField(choices=TIPO_PAGO_RECIBO, blank=True, null=True)
    monto = models.DecimalField('Monto', max_digits=7, decimal_places=2, default=0)
    redondeo = models.DecimalField('Redondeo', max_digits=3, decimal_places=2, default=0, blank=True, null=True)
    monto_pagado = models.DecimalField('Monto Pagado', max_digits=7, decimal_places=2, default=0)
    voucher = models.FileField('Voucher', upload_to=None, max_length=100, blank=True, null=True)
    fecha_pago = models.DateField('Fecha de Pago', auto_now=False, auto_now_add=False, blank=True, null=True)
    content_type = models.ForeignKey(ContentType, blank=True, null=True, on_delete=models.PROTECT) #Cheque / Telecrédito / Caja Chica
    id_registro = models.IntegerField(blank=True, null=True)   
    estado = models.IntegerField(choices=ESTADOS_RECIBO, default=1, blank=True, null=True)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='ReciboBoletaPago_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='ReciboBoletaPago_updated_by', editable=False)
    
    class Meta:
        verbose_name = 'Recibo Boleta Pago'
        verbose_name_plural = 'Recibos Boleta Pago'
        ordering = [
            '-fecha_pagar',
            'boleta_pago',
            ]
    
    @property
    def moneda(self):
        return self.boleta_pago.moneda

    @property
    def cheque(self):
        if self.content_type == ContentType.objects.get_for_model(Cheque):
            return self.content_type.get_object_for_this_type(id=self.id_registro)
        return False

    @property
    def caja(self):
        if self.content_type == ContentType.objects.get_for_model(applications.caja_chica.models.CajaChica):
            return self.content_type.get_object_for_this_type(id=self.id_registro)
        return False

    @property
    def telecredito(self):
        if self.content_type == ContentType.objects.get_for_model(Telecredito):
            return self.content_type.get_object_for_this_type(id=self.id_registro)
        return False

    def __str__(self):
        return "%s - %s  - %s - %s" % (self.boleta_pago.get_month_display(), self.boleta_pago.year, self.get_tipo_pago_display(), self.boleta_pago.datos_planilla ) 


post_save.connect(funciones.cheque_monto_usado_post_save, sender=ReciboBoletaPago)


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
    tipo_servicio = models.ForeignKey(TipoServicio, on_delete=models.CASCADE, blank=True, null=True)
    medio_pago = models.ManyToManyField(MedioPago)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Institucion_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Institucion_updated_by', editable=False)

    class Meta:
        verbose_name = 'Institucion'
        verbose_name_plural = 'Instituciones'
        ordering = [
            'nombre',
        ]

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
        ordering = [
            'institucion',
            'tipo_servicio',
            'alias',
            'sociedad',
        ]

    def __str__(self):
        if self.sociedad:
            return f"{self.institucion} - {self.tipo_servicio} - {self.alias} - {self.sociedad.abreviatura}"
        return f"{self.institucion} - {self.tipo_servicio} - {self.alias}"

class ReciboServicio(models.Model):
    servicio = models.ForeignKey(Servicio, blank=True, null=True, on_delete=models.PROTECT)
    foto = models.FileField('Documento Recibo', blank=True, null=True)
    fecha_emision = models.DateField('Fecha de Emision', auto_now=False, auto_now_add=False, blank=True, null=True)
    fecha_vencimiento = models.DateField('Fecha de Vencimiento', auto_now=False, auto_now_add=False, blank=True, null=True)
    monto = models.DecimalField('Monto', max_digits=7, decimal_places=2, blank=True, null=True)
    moneda = models.ForeignKey(Moneda, on_delete=models.PROTECT, blank=True, null=True)
    mora = models.DecimalField('Mora', max_digits=3, decimal_places=2, default=0)
    redondeo = models.DecimalField('Redondeo', max_digits=3, decimal_places=2, default=0)
    monto_pagado = models.DecimalField('Monto Pagado', max_digits=7, decimal_places=2, default=0)
    voucher = models.FileField('Voucher',blank=True, null=True)
    fecha_pago = models.DateField('Fecha de Pago', null=True)
    content_type = models.ForeignKey(ContentType, blank=True, null=True, on_delete=models.PROTECT) #Cheque / Caja Chica
    id_registro = models.IntegerField(blank=True, null=True)   
    estado = models.IntegerField(choices=ESTADOS_RECIBO, default=1)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='ReciboServicio_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='ReciboServicio_updated_by', editable=False)

    class Meta:
        verbose_name = 'Recibo de Servicio'
        verbose_name_plural = 'Recibos de Servicios'
        ordering = [
            '-fecha_emision',
            'servicio',
        ]

    @property
    def cheque(self):
        if self.content_type == ContentType.objects.get_for_model(Cheque):
            return self.content_type.get_object_for_this_type(id=self.id_registro)
        return False

    @property
    def caja(self):
        if self.content_type == ContentType.objects.get_for_model(applications.caja_chica.models.CajaChica):
            return self.content_type.get_object_for_this_type(id=self.id_registro)
        return False

    def __str__(self):
        return str(self.servicio)

post_save.connect(funciones.cheque_monto_usado_post_save, sender=ReciboServicio)


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
        (1, 'PENDIENTE'),
        (2, 'SOLICITADO'),
        (3, 'COBRADO'),
        (4, 'FINALIZADO'),
        )
    
    concepto = models.CharField('Concepto', max_length=50, default='Nuevo Cheque')
    moneda = models.ForeignKey(Moneda, on_delete=models.PROTECT, blank=True, null=True)
    monto_cheque = models.DecimalField('Monto del cheque', max_digits=7, decimal_places=2, default=0)
    monto_usado = models.DecimalField('Monto Usado', max_digits=7, decimal_places=2, default=0)
    comision = models.DecimalField('Comisión', max_digits=7, decimal_places=2, default=0)
    redondeo = models.DecimalField('Redondeo', max_digits=7, decimal_places=2, default=0)
    vuelto = models.DecimalField('Vuelto', max_digits=7, decimal_places=2, default=0)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='Cheque_usuario', blank=True, null=True)
    estado = models.IntegerField('Estado', choices=ESTADO_CHEQUE, default=1)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Cheque_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Cheque_updated_by', editable=False)

    class Meta:
        verbose_name = 'Cheque'
        verbose_name_plural = 'Cheques'
        ordering = [
            'estado',
            'created_at',
            'concepto',
            ]

    @property
    def content_type(self):
        return ContentType.objects.get_for_model(self)
    
    @property
    def vuelto_extra(self):
        if self.ChequeVueltoExtra_cheque.all():
            return self.ChequeVueltoExtra_cheque.all().aggregate(models.Sum('vuelto_extra'))['vuelto_extra__sum']
        return Decimal('0.00')
    
    @property
    def recibido(self):
        if self.ChequeFisico_cheque.all():
            return self.ChequeFisico_cheque.all().aggregate(models.Sum('monto_recibido'))['monto_recibido__sum']
        return Decimal('0.00')

    def __str__(self):
        if self.moneda:
            return self.concepto + ' ' + self.usuario.username + ' ' + self.get_estado_display() + ' ' + self.moneda.nombre
        else:
            return self.concepto + ' ' + self.usuario.username + ' ' + self.get_estado_display()
        

class ChequeFisico(models.Model):
    ESTADO_CHEQUE_FISICO = (
        (1, 'PENDIENTE'),
        (2, 'COBRADO'),
        )
    
    banco = models.ForeignKey(Banco, on_delete=models.PROTECT, blank=True, null=True)
    numero = models.CharField('Número de cheque', max_length=50, blank=True, null=True)
    responsable = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT)
    moneda = models.ForeignKey(Moneda, on_delete=models.RESTRICT)
    monto = models.DecimalField('Monto del cheque', max_digits=7, decimal_places=2, default=0)
    comision = models.DecimalField('Comision', max_digits=4, decimal_places=4, default=0) #Eliminar
    monto_recibido = models.DecimalField('Monto Recibido', max_digits=7, decimal_places=2, default=0)
    fecha_emision = models.DateField('Fecha de emisión del cheque', auto_now=False, auto_now_add=False, blank=True, null=True)
    fecha_cobro = models.DateField('Fecha de cobro del cheque', auto_now=False, auto_now_add=False, blank=True, null=True)
    foto = models.ImageField('Foto del cheque', upload_to=CONTABILIDAD_FOTO_CHEQUE, height_field=None, width_field=None, max_length=None, blank=True, null=True)
    sociedad = models.ForeignKey(Sociedad, on_delete=models.PROTECT)
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
        return f"{self.banco} - {self.numero} - {self.moneda.simbolo} {self.monto}"


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
        return str(self.cheque) + " " + self.moneda.simbolo + " " + str(self.vuelto_extra)


post_save.connect(funciones.cheque_monto_usado_post_save, sender=ChequeVueltoExtra)


class TamañoEmpresa(models.Model):
    TIPO_EMPRESA = (
        (1, 'MICRO EMPRESA'),
        (2, 'PEQUEÑA EMPRESA'),
        (3, 'MEDIANA EMPRESA'),
        (4, 'GRAN EMPRESA'),
    )
    
    tipo_empresa = models.IntegerField(choices=TIPO_EMPRESA)
    sociedad = models.ForeignKey(Sociedad, on_delete=models.CASCADE, related_name='TamañoEmpresa_sociedad')
    fecha_inicio = models.DateField('Fecha de inicio', auto_now=False, auto_now_add=False)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='TamañoEmpresa_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='TamañoEmpresa_updated_by', editable=False)

    class Meta:
        verbose_name = 'Tamaño de Empresa'
        verbose_name_plural = 'Tamaño de Empresas'

    def __str__(self):
        return f"{self.fecha_inicio} - {self.get_tipo_empresa_display()}"
