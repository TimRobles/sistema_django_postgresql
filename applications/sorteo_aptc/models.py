# Create your models here.
from pyexpat import model
from django.db import models
from django.conf import settings

from applications.clientes.models import Cliente, InterlocutorCliente, TipoInterlocutorCliente
from applications.variables import TIPO_DOCUMENTO_CHOICES



class UsuarioAPTC(models.Model):
    fecha = models.DateField('Fecha', auto_now=False, auto_now_add=True)
    nombre = models.CharField("nombre", max_length=100)
    tipo_documento = models.CharField('Tipo de Documento', max_length=1, choices=TIPO_DOCUMENTO_CHOICES)
    numero_documento = models.CharField('Número de Documento', max_length=15, null=True, blank=True)
    telefono = models.CharField("telefono", max_length=100)
    correo = models.EmailField("correo", max_length=254, blank=True, null=True)
    empresa = models.CharField("empresa", max_length=100, blank=True, null=True)
    ticket = models.CharField("numero_ticket", max_length=4)
    premio = models.CharField('Premio', max_length=50, blank=True, null=True)
    elegido = models.BooleanField(default=False)
    bloqueo = models.BooleanField(default=False)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='UsuarioAPTC_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='UsuarioAPTC_updated_by', editable=False)

    class Meta:
        verbose_name = 'UsuarioAPTC'
        verbose_name_plural = 'UsuarioAPTCs'
        ordering = [
            '-fecha',
            'premio',
            'ticket'
            ]

    def __str__(self):
        return str(self.ticket)




