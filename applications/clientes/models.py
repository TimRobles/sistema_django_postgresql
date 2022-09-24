from decimal import Decimal
from django.db import models
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField
from applications import datos_globales
from applications.variables import CONDICION_SUNAT, DICCIONARIO_TIPO_DOCUMENTO_SUNAT, ESTADOS, ESTADO_SUNAT, TIPO_DOCUMENTO_SUNAT, TIPO_DOCUMENTO_CHOICES, TIPO_REPRESENTANTE_LEGAL_SUNAT

from django.db.models.signals import pre_save, post_save

class Cliente(models.Model):

    tipo_documento = models.CharField('Tipo de Documento', max_length=1, choices=TIPO_DOCUMENTO_SUNAT)
    numero_documento = models.CharField('Número de Documento', max_length=15, blank=True, null=True)
    razon_social = models.CharField('Razón Social', max_length=100)
    nombre_comercial = models.CharField('Nombre Comercial', max_length=50, blank=True, null=True)
    direccion_fiscal = models.CharField('Dirección Fiscal', max_length=100)
    ubigeo = models.CharField('Ubigeo', max_length=6)
    distrito = models.ForeignKey('datos_globales.Distrito', on_delete=models.CASCADE, blank=True, null=True)
    estado_sunat = models.IntegerField('Estado SUNAT', choices=ESTADO_SUNAT)
    condicion_sunat = models.IntegerField('Condición SUNAT', choices=CONDICION_SUNAT, default=1)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='Cliente_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='Cliente_updated_by', editable=False)
    
    class Meta:

        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['estado_sunat', 'razon_social']

    def save(self, *args, **kwargs):
        if self.ubigeo:
            try:
                self.distrito = datos_globales.models.Distrito.objects.get(codigo = self.ubigeo)
            except:
                self.distrito = None
        self.razon_social = self.razon_social.upper()
        self.nombre_comercial = self.nombre_comercial.upper()
        self.direccion_fiscal = self.direccion_fiscal.upper()
        super().save(*args, **kwargs)

    def documento(self):
        return DICCIONARIO_TIPO_DOCUMENTO_SUNAT[self.tipo_documento]

    @property
    def linea_credito_condiciones_pago(self):
        try:
            return self.LineaCredito_cliente.get(estado=1).condiciones_pago
        except:
            return ''

    @property
    def linea_credito_monto(self):
        try:
            return self.LineaCredito_cliente.get(estado=1).monto
        except:
            return Decimal('0.00')

    @property
    def linea_credito_moneda_simbolo(self):
        try:
            return self.LineaCredito_cliente.get(estado=1).moneda.simbolo
        except:
            return ''

    @property
    def deuda_monto(self):
        try:
            total = Decimal('0.00')
            deudas = self.Deuda_cliente.all()
            for deuda in deudas:
                if deuda.moneda.principal:
                    total += deuda.monto
                else:
                    total += deuda.monto / deuda.tipo_cambio
                total -= deuda.pagos

            return total
        except:
            return Decimal('0.00')

    @property
    def nota_credito_monto(self):
        try:
            return Decimal('0.00')
        except:
            return Decimal('0.00')

    @property
    def nota_credito_monto(self):
        try:
            return Decimal('0.00')
        except:
            return Decimal('0.00')

    @property
    def disponible_monto(self):
        try:
            return self.linea_credito_monto - self.deuda_monto + self.nota_credito_monto
        except:
            return Decimal('0.00')

    def __str__(self):
        return self.razon_social


class TipoInterlocutorCliente(models.Model):
    '''Solo por Admin'''

    nombre = models.CharField('Nombre', max_length=60, unique=True)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='TipoInterlocutorCliente_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='TipoInterlocutorCliente_updated_by', editable=False)

    class Meta:
        verbose_name = 'Tipo de Interlocutor Cliente'
        verbose_name_plural = 'Tipos de Interlocutor Cliente'
        ordering = ['nombre',]

    def __str__(self):
        return self.nombre


class InterlocutorCliente(models.Model):

    nombre_completo = models.CharField('Nombre Completo', max_length=120)
    tipo_documento = models.CharField('Tipo de Documento', max_length=1, choices=TIPO_DOCUMENTO_CHOICES)
    numero_documento = models.CharField('Número de Documento', max_length=15, unique=True, blank=True, null=True)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='InterlocutorCliente_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='InterlocutorCliente_updated_by', editable=False)
    
    class Meta:

        verbose_name = 'Interlocutor Cliente'
        verbose_name_plural = 'Interlocutores Cliente'
        ordering = ['-nombre_completo',]

    def __str__(self):
        return str(self.nombre_completo)

class ClienteInterlocutor(models.Model):

    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='ClienteInterlocutor_cliente')
    interlocutor = models.ForeignKey(InterlocutorCliente, on_delete=models.PROTECT, related_name='ClienteInterlocutor_interlocutor')
    tipo_interlocutor = models.ForeignKey(TipoInterlocutorCliente, on_delete=models.PROTECT)
    estado = models.IntegerField('Estado', choices=ESTADOS,default=1)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='ClienteInterlocutor_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='ClienteInterlocutor_updated_by', editable=False)
    
    class Meta:

        verbose_name = 'Cliente Interlocutor'
        verbose_name_plural = 'Cliente Interlocutores'
        ordering = ['estado', '-interlocutor',]

    def __str__(self):
        return "%s - %s" % (self.cliente, self.interlocutor)


class CorreoCliente(models.Model):

    correo = models.EmailField('Correo')
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    fecha_baja = models.DateField('Fecha de Baja', auto_now=False, auto_now_add=False, blank=True, null=True)
    estado = models.IntegerField('Estado', choices=ESTADOS,default=1)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='CorreoCliente_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='CorreoCliente_updated_by', editable=False)
    
    class Meta:

        verbose_name = 'Correo Cliente'
        verbose_name_plural = 'Correos Cliente'
        ordering = ['estado', '-fecha_baja', 'correo']

    def __str__(self):
        return str(self.correo) + ' - ' + str(self.cliente)


class RepresentanteLegalCliente(models.Model):

    interlocutor = models.ForeignKey(InterlocutorCliente, on_delete=models.PROTECT)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    tipo_representante_legal = models.CharField('Tipo de Representante Legal', max_length=4, choices=TIPO_REPRESENTANTE_LEGAL_SUNAT)
    fecha_inicio = models.DateField('Fecha de Inicio', auto_now=False, auto_now_add=False, blank=True, null=True)
    fecha_baja = models.DateField('Fecha de Baja', auto_now=False, auto_now_add=False, blank=True, null=True)
    estado = models.IntegerField('Estado', choices=ESTADOS,default=1)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='RepresentanteLegalCliente_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='RepresentanteLegalCliente_updated_by', editable=False)

    class Meta:

        verbose_name = 'Representante Legal Cliente'
        verbose_name_plural = 'Representantes Legales Cliente'
        ordering = ['estado', '-fecha_baja', '-interlocutor',]

    def __str__(self):
        return str(self.interlocutor) + ' - ' + str(self.cliente)


class TelefonoInterlocutorCliente(models.Model):

    numero = PhoneNumberField('Teléfono')
    interlocutor = models.ForeignKey(InterlocutorCliente, on_delete=models.PROTECT)
    fecha_baja = models.DateField('Fecha de Baja', auto_now=False, auto_now_add=False, blank=True, null=True)
    estado = models.IntegerField('Estado', choices=ESTADOS,default=1)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='TelefonoInterlocutorCliente_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='TelefonoInterlocutorCliente_updated_by', editable=False)
    
    class Meta:

        verbose_name = 'Telefono Interlocutor Cliente'
        verbose_name_plural = 'Telefonos Interlocutores Cliente'
        ordering = ['estado', '-fecha_baja',]

    def __str__(self):
        return str(self.numero) + ' - ' + str(self.interlocutor)


class CorreoInterlocutorCliente(models.Model):

    correo = models.EmailField('Correo')
    interlocutor = models.ForeignKey(InterlocutorCliente, on_delete=models.PROTECT)
    fecha_baja = models.DateField('Fecha de Baja', auto_now=False, auto_now_add=False, blank=True, null=True)
    estado = models.IntegerField('Estado', choices=ESTADOS,default=1)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='CorreoInterlocutorCliente_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='CorreoInterlocutorCliente_updated_by', editable=False)
    
    class Meta:

        verbose_name = 'Correo Interlocutor Cliente'
        verbose_name_plural = 'Correos Interlocutores Cliente'
        ordering = ['estado', '-fecha_baja',]

    def __str__(self):
        return str(self.correo) + ' - ' + str(self.interlocutor)


# def interlocutor_cliente_pre_save(*args, **kwargs):
#     print('pre save')
#     print(kwargs)
#     obj = kwargs['instance']
#     print(obj.nombre_completo)
#     obj.nombre_completo = obj.nombre_completo.upper()
#     print(obj.nombre_completo)

# def interlocutor_cliente_post_save(*args, **kwargs):
#     print('post save')
#     print(kwargs)

# pre_save.connect(interlocutor_cliente_pre_save, sender=InterlocutorCliente)
# post_save.connect(interlocutor_cliente_post_save, sender=InterlocutorCliente)