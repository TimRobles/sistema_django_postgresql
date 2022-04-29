from email.policy import default
from django.db import models
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField

from applications.variables import TIPO_DOCUMENTO_CHOICES


# Create your models here.

class HistoricoUser(models.Model):
    Estados = (
        (1, 'Alta'),
        (2, 'Baja'),
        (3, 'Historico'),
    )

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Id de Usuario', on_delete=models.PROTECT, related_name='HistoricoUser_usuario')
    fecha_alta = models.DateField('Fecha de Alta', auto_now=False, auto_now_add=False)
    fecha_baja = models.DateField('Fecha de Baja', auto_now=False, auto_now_add=False, blank=True, null=True)
    estado = models.IntegerField('Estado', choices=Estados, default=1)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='HistoricoUser_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='HistoricoUser_updated_by', editable=False)


    class Meta:
        verbose_name = 'Histórico Usuario'
        verbose_name_plural = 'Histórico Usuarios'
        ordering = ['estado']
        constraints = [
            models.UniqueConstraint(
                fields=['usuario',], condition=models.Q(estado=1), name = 'usuario de alta',
                ),
            ]

    def __str__(self):
        return str(self.fecha_alta)


class DatosUsuario(models.Model):
    Estados = (
        (1, 'Alta'),
        (2, 'Baja'),
    )
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, unique=True, related_name='DatosUsuario_usuario')
    tipo_documento = models.CharField('Tipo de Documento', max_length=1, choices=TIPO_DOCUMENTO_CHOICES)    
    numero_documento = models.CharField('Número de Documento', max_length=15)
    fecha_nacimiento = models.DateField('Fecha de Nacimiento', auto_now=False, auto_now_add=False)
    foto = models.ImageField('Foto de Perfil', upload_to='img/usuario/datos_usuario/', default='img/usuario/datos_usuario/default-avatar.png', height_field=None, width_field=None, max_length=None)
    direccion = models.CharField('Dirección', max_length=254)
    recuperar_password = models.CharField('Recuperar password', max_length=10, blank=True, null=True)
    telefono_personal = PhoneNumberField('Teléfono Personal')

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='DatosUsuario_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='DatosUsuario_updated_by', editable=False)

    class Meta:
        verbose_name = 'Datos del Usuario'
        verbose_name_plural = 'Datos de los Usuarios'

    def __str__(self):
        return str(self.numero_documento)
