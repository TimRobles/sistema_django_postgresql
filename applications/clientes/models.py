from django.db import models
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField
from applications import datos_globales
from applications.variables import ESTADOS, ESTADO_SUNAT, TIPO_DOCUMENTO_SUNAT, TIPO_DOCUMENTO_CHOICES, TIPO_REPRESENTANTE_LEGAL_SUNAT


class Cliente(models.Model):

    tipo_documento = models.CharField('Tipo de Documento', max_length=1, choices=TIPO_DOCUMENTO_SUNAT)
    numero_documento = models.CharField('Número de Documento', max_length=15, unique=True)
    razon_social = models.CharField('Razón Social', max_length=100)
    nombre_comercial = models.CharField('Nombre Comercial', max_length=50, blank=True, null=True)
    direccion_fiscal = models.CharField('Dirección Fiscal', max_length=100)
    ubigeo = models.CharField('Ubigeo', max_length=6)
    distrito = models.ForeignKey('datos_globales.Distrito', on_delete=models.CASCADE, blank=True, null=True)
    estado_sunat = models.IntegerField('Estado SUNAT', choices=ESTADO_SUNAT)
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
            self.distrito = datos_globales.models.Distrito.objects.get(codigo = self.ubigeo)
        super().save(*args, **kwargs)

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
    tipo_interlocutor = models.ForeignKey(TipoInterlocutorCliente, on_delete=models.PROTECT)
    tipo_documento = models.CharField('Tipo de Documento', max_length=1, choices=TIPO_DOCUMENTO_CHOICES)
    numero_documento = models.CharField('Número de Documento', max_length=15, unique=True)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='InterlocutorCliente_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='InterlocutorCliente_updated_by', editable=False)
    
    class Meta:

        verbose_name = 'Interlocutor Cliente'
        verbose_name_plural = 'Interlocutores Cliente'

    def __str__(self):
        return str(self.nombre_completo)

class ClienteInterlocutor(models.Model):

    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    interlocutor = models.ForeignKey(InterlocutorCliente, on_delete=models.PROTECT)
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
        return str(self.cliente) + ' - ' + str(self.interlocutor)


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


class RepresentanteLegalCliente(models.Model):

    interlocutor = models.ForeignKey(InterlocutorCliente, on_delete=models.PROTECT)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    tipo_representante_legal = models.IntegerField('Tipo de Representante Legal', choices=TIPO_REPRESENTANTE_LEGAL_SUNAT)
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
        ordering = ['estado', '-fecha_baja',]

    def __str__(self):
        return str(self.interlocutor) + ' - ' + str(self.cliente)