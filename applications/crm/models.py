from django.db import models
from django.conf import settings
from applications.variables import ESTADOS_CLIENTE_CRM, MEDIO, ESTADOS_EVENTO_CRM
from applications.clientes.models import Cliente, CorreoInterlocutorCliente, InterlocutorCliente, TelefonoInterlocutorCliente
from applications.sorteo.models import Sorteo
from applications.datos_globales.models import Pais

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


class EventoCRM(models.Model):
    
    fecha_inicio = models.DateField('Fecha Inicio', blank=True, null=True)
    fecha_cierre = models.DateField('Fecha Cierre', blank=True, null=True)
    titulo = models.CharField('Titulo Evento', max_length=50)
    descripcion = models.TextField('Descripción', blank=True, null=True)
    # total_merchandising = models.DecimalField('Total Merchandising', max_digits=22, decimal_places=10)
    sorteo = models.ForeignKey(Sorteo, on_delete=models.PROTECT, related_name='Sorteo',blank=True, null=True)
    presupuesto_asignado = models.DecimalField('Presupuesto asignado', max_digits=6, decimal_places=3, blank=True, null=True)
    presupuesto_utilizado = models.DecimalField('Presupuesto utilizado', max_digits=6, decimal_places=3, blank=True, null=True)
    pais = models.ForeignKey(Pais, on_delete=models.PROTECT, related_name='Sorteo',blank=True, null=True)
    estado = models.IntegerField('Estado', choices=ESTADOS_EVENTO_CRM, default=1)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='EventoCRM_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='EventoCRM_updated_by', editable=False)

    class Meta:
        verbose_name = 'Evento CRM'
        verbose_name_plural = 'Eventos CRM'

    def __str__(self):
        return str(self.titulo)
