from django.db import models
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField
from applications.variables import ESTADOS
from applications.datos_globales.models import Pais

class Proveedor(models.Model):

    nombre = models.CharField('Nombre', max_length=50)
    pais = models.ForeignKey(Pais, on_delete=models.PROTECT)
    direccion = models.CharField('Dirección', max_length=255)
    estado = models.IntegerField('Estado', choices=ESTADOS,default=1)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='Proveedor_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='Proveedor_updated_by', editable=False)
    
    class Meta:

        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        ordering = ['estado', 'nombre',]

    def save(self):
        self.nombre = self.nombre.upper()
        self.direccion = self.direccion.upper()
        return super().save()

    def __str__(self):
        return self.nombre

class InterlocutorProveedor(models.Model):

    nombres = models.CharField('Nombres', max_length=60)
    apellidos = models.CharField('Apellidos', max_length=60)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='InterlocutorProveedor_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='InterlocutorProveedor_updated_by', editable=False)
    
    class Meta:

        verbose_name = 'Interlocutor Proveedor'
        verbose_name_plural = 'Interlocutores Proveedor'

    def __str__(self):
        return str(self.nombres) + ' ' + str(self.apellidos) 

class ProveedorInterlocutor(models.Model):

    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT)
    interlocutor = models.ForeignKey(InterlocutorProveedor, on_delete=models.PROTECT)
    estado = models.IntegerField('Estado', choices=ESTADOS,default=1)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='ProveedorInterlocutor_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='ProveedorInterlocutor_updated_by', editable=False)
    
    class Meta:

        verbose_name = 'Proveedor Interlocutor'
        verbose_name_plural = 'Proveedor Interlocutores'
        ordering = ['estado', '-interlocutor',]

    def __str__(self):
        return str(self.proveedor) + ' - ' + str(self.interlocutor)

class TelefonoInterlocutorProveedor(models.Model):

    numero = PhoneNumberField('Teléfono')
    interlocutor = models.ForeignKey(InterlocutorProveedor, on_delete=models.PROTECT)
    fecha_baja = models.DateField('Fecha de Baja', auto_now=False, auto_now_add=False, blank=True, null=True)
    estado = models.IntegerField('Estado', choices=ESTADOS,default=1)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='TelefonoInterlocutorProveedor_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='TelefonoInterlocutorProveedor_updated_by', editable=False)
    
    class Meta:

        verbose_name = 'Telefono Interlocutor Proveedor'
        verbose_name_plural = 'Telefonos Interlocutores Proveedor'
        ordering = ['estado', '-fecha_baja',]

    def __str__(self):
        return str(self.numero) + ' - ' + str(self.interlocutor)

class CorreoInterlocutorProveedor(models.Model):

    correo = models.EmailField('Correo')
    interlocutor = models.ForeignKey(InterlocutorProveedor, on_delete=models.PROTECT)
    fecha_baja = models.DateField('Fecha de Baja', auto_now=False, auto_now_add=False, blank=True, null=True)
    estado = models.IntegerField('Estado', choices=ESTADOS,default=1)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='CorreoInterlocutorProveedor_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='CorreoInterlocutorProveedor_updated_by', editable=False)
    
    class Meta:

        verbose_name = 'Correo Interlocutor Proveedor'
        verbose_name_plural = 'Correos Interlocutores Proveedor'
        ordering = ['estado', '-fecha_baja',]

    def __str__(self):
        return str(self.correo) + ' - ' + str(self.interlocutor)