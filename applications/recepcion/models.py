from pyexpat import model
from django.db import models
from django.conf import settings
from applications.variables import TIPO_DOCUMENTO_CHOICES
from applications.sociedad.models import Sociedad
from applications.sede.models import Sede


class Visita(models.Model):
    nombre = models.CharField('Nombre Completo', max_length=50)
    tipo_documento = models.CharField('Tipo de Documento', max_length=1, choices=TIPO_DOCUMENTO_CHOICES)    
    numero_documento = models.CharField('Número de Documento', max_length=15)
    sede = models.ForeignKey(Sede, on_delete=models.PROTECT)
    usuario_atendio = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='Usuario_Atendio')
    motivo_visita = models.CharField('Motivo de Visita', max_length=50)
    hora_ingreso = models.TimeField('Hora de Ingreso',  auto_now=False, auto_now_add=True)
    hora_salida = models.TimeField('Hora de Salida', auto_now=False, auto_now_add=False, blank=True, null=True)
    empresa_cliente = models.CharField('Empresa Cliente', max_length=50, blank=True, null=True)
    fecha_registro = models.DateField('Fecha de Registro', auto_now=False, auto_now_add=True, blank=True, null=True, editable=False)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Visita_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Visita_updated_by', editable=False)

    class Meta:

        verbose_name = 'Visita'
        verbose_name_plural = 'Visitas'
        ordering = [
            '-fecha_registro',
            '-hora_salida',
            '-hora_ingreso',
            'nombre'
            ]

    def save(self):
        self.nombre = self.nombre.upper()
        return super().save()

    def __str__(self):
        return self.nombre


class Asistencia(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Usuarios', on_delete=models.PROTECT, related_name='Asistencia_usuario')
    sociedad = models.ForeignKey(Sociedad, on_delete=models.PROTECT) 
    hora_ingreso = models.TimeField('Hora de Ingreso',  auto_now=False, auto_now_add=True)
    hora_salida = models.TimeField('Hora de Salida', auto_now=False, auto_now_add=False, blank=True, null=True)
    fecha_registro = models.DateField('Fecha de Registro', auto_now=False, auto_now_add=True, blank=True, null=True, editable=False)
    sede =  models.ForeignKey(Sede, on_delete=models.PROTECT) 

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Asistencia_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Asistencia_updated_by', editable=False)

    class Meta:      
        verbose_name = 'Asistencia'
        verbose_name_plural = 'Asistencias'
        ordering = [
            '-fecha_registro',
            '-hora_salida',
            '-hora_ingreso',
            'usuario',
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    'usuario',
                    'fecha_registro',
                ], name='Asistencia_usuario_fecha_registro'
            )
        ]

    def __str__(self):
        return str(self.usuario)+" - "+ str(self.fecha_registro)+" - "+ str(self.hora_ingreso)+" - "+ str(self.sede)


class ResponsableAsistencia(models.Model):
    usuario_responsable = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Usuario Responsable', on_delete=models.PROTECT, related_name='ResponsableAsistencia_usuario_responsable')
    usuario_a_registrar = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name='Usuarios a Registrar',related_name='ResponsableAsistencia_usuario_a_registrar')
    permiso_cambio_ip = models.BooleanField()

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='ResponsableAsistencia_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='ResponsableAsistencia_updated_by', editable=False)

    class Meta:
        verbose_name = 'Responsable Asistencia'
        verbose_name_plural = 'Responsable Asistencias'

    def __str__(self):
        return str(self.usuario_responsable)


class IpPublica(models.Model):
    ip = models.CharField('IP', max_length=15)
    sede = models.ForeignKey(Sede, on_delete=models.PROTECT) 

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='IpPublica_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='IpPublica_updated_by', editable=False)


    class Meta:
        verbose_name = 'Ip Publica'
        verbose_name_plural = 'Ip Publicas'


    def __str__(self):
        return str(self.ip)


class GeoLocalizacion(models.Model):
    longitud = models.DecimalField('Longitud', max_digits=22, decimal_places=16)
    latitud = models.DecimalField('Latitud', max_digits=22, decimal_places=16)
    sede = models.ForeignKey(Sede, on_delete=models.PROTECT)
    distancia = models.IntegerField()

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='GeoLocalizacion_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='GeoLocalizacion_updated_by', editable=False)


    class Meta:
        verbose_name = 'Geo Localización'
        verbose_name_plural = 'Geo Localizaciones'


    def __str__(self):
        return str(self.longitud) + ', ' + str(self.latitud)


