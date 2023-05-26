from django.db import models
from django.conf import settings
from applications.variables import ESTADOS_CLIENTE_CRM, MEDIO
from applications.clientes.models import Cliente, CorreoInterlocutorCliente, InterlocutorCliente, TelefonoInterlocutorCliente


class ClienteCRM(models.Model):

    cliente_crm = models.OneToOneField(Cliente, on_delete=models.CASCADE)
    medio = models.IntegerField('Medio', choices=MEDIO)
    estado = models.IntegerField('Estado', choices=ESTADOS_CLIENTE_CRM, default=1)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='ClienteCRM_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='ClienteCRM_updated_by', editable=False)

    class Meta:
        verbose_name = 'Cliente CRM'
        verbose_name_plural = 'Clientes CRM'

    def __str__(self):
        return self.cliente_crm.razon_social


class ClienteCRMDetalle(models.Model):

    interlocutor = models.ForeignKey(InterlocutorCliente, on_delete=models.PROTECT)
    correo = models.ForeignKey(CorreoInterlocutorCliente, on_delete=models.PROTECT)
    telefono = models.ForeignKey(TelefonoInterlocutorCliente, on_delete=models.PROTECT)
    cliente_crm =  models.ForeignKey(ClienteCRM, on_delete=models.CASCADE)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='ClienteCRMDetalle_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='ClienteCRMDetalle_updated_by', editable=False)

    class Meta:
        verbose_name = 'Cliente CRM Detalle '
        verbose_name_plural = 'Clientes CRM Detalle '

    def __str__(self):
        return self.interlocutor
