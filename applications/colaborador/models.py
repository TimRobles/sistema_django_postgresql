from distutils.command.upload import upload
from django.db import models
from django.conf import settings
from applications.sociedad.models import Sociedad
from applications.datos_globales.models import Cargo


class DatosContratoPlanilla(models.Model):
    Estados = (
        (1, 'Alta'),
        (2, 'Baja'),
    )

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Usuarios', on_delete=models.PROTECT, related_name='DatosColaboradorPlanilla_usuario')
    sociedad = models.ForeignKey(Sociedad, on_delete=models.PROTECT) 
    fecha_alta = models.DateField('Fecha de Alta', auto_now=False, auto_now_add=False)
    fecha_baja = models.DateField('Fecha de Baja', auto_now=False, auto_now_add=False, blank=True, null=True)
    sueldo_bruto = models.DecimalField('Sueldo Bruto', max_digits=7, decimal_places=2)
    movilidad = models.DecimalField('Movilidad', max_digits=7, decimal_places=2, blank=True, null=True)
    asignacion_familiar = models.BooleanField('Asignación familiar', default=False)
    archivo_contrato = models.FileField('Archivo Contrato',upload_to = 'file/colaboradores/archivo_contrato/', max_length=100, blank=True, null=True)
    cargo = models.ForeignKey(Cargo, on_delete=models.PROTECT)  
    estado_alta_baja = models.IntegerField('Estado', choices=Estados, default=1)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='DatosContratoPlanilla_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='DatosContratoPlanilla_updated_by', editable=False)

    class Meta:
        verbose_name = 'Datos de Contrato de Planilla'
        verbose_name_plural = 'Datos de Contratos de Planilla'

    def __str__(self):
        
        return str(self.fecha_alta)
        


class DatosContratoHonorarios(models.Model):
    Estados = (
        (1, 'Alta'),
        (2, 'Baja'),
    )

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Usuarios', on_delete=models.PROTECT, related_name='DatosColaboradorHonorariosusuario')
    sociedad = models.ForeignKey(Sociedad, on_delete=models.PROTECT) 
    fecha_alta = models.DateField('Fecha de Alta', auto_now=False, auto_now_add=False)
    fecha_baja = models.DateField('Fecha de Baja', auto_now=False, auto_now_add=False, blank=True, null=True)
    sueldo = models.DecimalField('Sueldo', max_digits=7, decimal_places=2)
    suspension_cuarta = models.BooleanField('Suspención de Cuarta Categoria', default=False)
    archivo_suspension_cuarta = models.FileField('Archivo Suspensión Cuarta Categoría',upload_to = 'file/colaboradores/archivo_suspension/', max_length=100, blank=True, null=True)
    archivo_contrato = models.FileField('Archivo Contrato',upload_to = 'file/colaboradores/archivo_contrato/', max_length=100, blank=True, null=True)
    cargo = models.ForeignKey(Cargo, on_delete=models.PROTECT)  
    estado_alta_baja = models.IntegerField('Estado', choices=Estados, default=1)
 
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='DatosContratoHonorarios_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='DatosContratoHonorarios_updated_by', editable=False)

    class Meta:
        verbose_name = 'Datos de Contrato de Honorarios'
        verbose_name_plural = 'Datos de Contratos de Honorarios'

    def __str__(self):
        
        return str(self.fecha_alta)