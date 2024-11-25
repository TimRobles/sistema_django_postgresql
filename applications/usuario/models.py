from email.policy import default
from django.db import models
from django.conf import settings
from datetime import date, timedelta
from phonenumber_field.modelfields import PhoneNumberField

from applications.variables import TIPO_DOCUMENTO_CHOICES, ESTADO_VACACIONES, ESTADO_VACACIONES_DETALLE
from datetime import datetime
from dateutil.relativedelta import relativedelta


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
        ordering = ['estado','usuario__username']
        constraints = [
            models.UniqueConstraint(
                fields=['usuario',], condition=models.Q(estado=1), name = 'usuario de alta',
                ),
            ]
    
    def __str__(self):
        return str(self.usuario) 


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

    @property
    def vacaciones(self):
        return Vacaciones.objects.filter(usuario=self).first()

    @property
    def vacaciones_detalle(self):
        return VacacionesDetalle.objects.filter(vacaciones=self.vacaciones)
    
    @property
    def fecha_cumpleaños(self):
        fecha_cumpleaños = date(day=self.fecha_nacimiento.day, month=self.fecha_nacimiento.month, year=date.today().year)
        if fecha_cumpleaños < date.today():
            fecha_cumpleaños = date(day=self.fecha_nacimiento.day, month=self.fecha_nacimiento.month, year=date.today().year + 1)
        return fecha_cumpleaños
    
    @property
    def cuenta_regresiva(self):
        return (self.fecha_cumpleaños - date.today()).days

    @property
    def get_edad(self):
        return relativedelta(datetime.now(), self.fecha_nacimiento + timedelta(1)).years + 1    

    def __str__(self):
        return str(self.usuario)+ " - " + str(self.numero_documento)



class Vacaciones(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='Vacaciones_usuario')
    dias_vacaciones = models.PositiveIntegerField()
    estado = models.IntegerField('Estado', choices=ESTADO_VACACIONES, default=1)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Vacaciones_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Vacaciones_updated_by', editable=False)

    class Meta:

        verbose_name = 'Vacacion'
        verbose_name_plural = 'Vacaciones'
        ordering = [
            'estado',
            '-created_at', 
            ]

    def __str__(self):
        return f"{self.usuario} - {self.dias_vacaciones}"

    @property
    def total_duracion(self):
        """Calcula la suma de los días usados."""
        total_duracion = sum(detalle.duracion for detalle in self.VacacionesDetalle_vacaciones.all())
        return total_duracion

    @property
    def dias_restantes(self):
        """Calcula los días restantes de vacaciones."""
        total_duracion = sum(detalle.duracion for detalle in self.VacacionesDetalle_vacaciones.all())
        return self.dias_vacaciones - total_duracion
    

class VacacionesDetalle(models.Model):
    vacaciones = models.ForeignKey(Vacaciones, on_delete=models.CASCADE, related_name='VacacionesDetalle_vacaciones')
    fecha_inicio = models.DateField('Fecha de Inicio', auto_now=False, auto_now_add=False)
    fecha_fin = models.DateField('Fecha de Fin', auto_now=False, auto_now_add=False)
    motivo = models.TextField(blank=True, null=True)
    estado = models.IntegerField('Estado', choices=ESTADO_VACACIONES_DETALLE, blank=True, null=True)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='VacacionesDetalle_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='VacacionesDetalle_updated_by', editable=False)


    def __str__(self):
        return f"{self.vacaciones.usuario} - {self.fecha_inicio} a {self.fecha_fin}"
    
    @property
    def duracion(self):
        """Calcula la duración de las vacaciones en días al memento de accionar el form"""
        if self.fecha_inicio and self.fecha_fin:
            return (self.fecha_fin - self.fecha_inicio).days + 1  # +1 para incluir el día de inicio
        return 0
    
    @property
    def usuario(self):
        """Devuelve el usuario asociado a las vacaciones."""
        return self.vacaciones.usuario