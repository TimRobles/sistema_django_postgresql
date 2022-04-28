from applications.variables import ESTADOS
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from applications.sociedad.models import Sociedad
from django.db import models


class Moneda(models.Model):
    '''Solo por Admin'''

    nombre = models.CharField('Nombre', max_length=50, unique=True)
    abreviatura = models.CharField('Abreviatura', max_length=5, unique=True)
    simbolo = models.CharField('Símbolo', max_length=5)
    estado = models.IntegerField('Estado', choices=ESTADOS,default=1)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='Moneda_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='Moneda_updated_by', editable=False)

    class Meta:
        verbose_name = 'Moneda'
        verbose_name_plural = 'Monedas'
        ordering = ['nombre',]

    def save(self):
        self.nombre = self.nombre.upper()
        self.abreviatura = self.abreviatura.upper()
        return super().save()

    def __str__(self):
        return str(self.nombre)


class Magnitud(models.Model):
    '''Solo por Admin'''

    nombre = models.CharField('Nombre', max_length=50, unique=True)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='Magnitud_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='Magnitud_updated_by', editable=False)

    class Meta:
        verbose_name = 'Magnitud'
        verbose_name_plural = 'Magnitudes'

    def save(self):
        self.nombre = self.nombre.upper()
        return super().save()

    def __str__(self):
        return self.nombre


class Unidad(models.Model):
    '''Solo por Admin'''

    magnitud = models.ForeignKey(Magnitud, on_delete=models.PROTECT)
    nombre = models.CharField('Nombre', max_length=50, unique=True)
    simbolo = models.CharField('Símbolo', max_length=5)
    unidad_sunat = models.CharField('Unidad Sunat', max_length=5)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='Unidad_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='Unidad_updated_by', editable=False)

    class Meta:
        verbose_name = 'Unidad'
        verbose_name_plural = 'Unidades'

    def __str__(self):
        return self.nombre


class Area(models.Model):
    '''Solo por Admin'''

    nombre = models.CharField('Nombre', max_length=50, unique=True)
    estado = models.IntegerField('Estado', choices=ESTADOS, default=1)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='Area_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='Area_updated_by', editable=False)

    class Meta:
        verbose_name = 'Area'
        verbose_name_plural = 'Areas'
        ordering = ['nombre',]

    def __str__(self):
        return self.nombre


class Cargo(models.Model):
    '''Solo por Admin'''

    area = models.ForeignKey(Area, on_delete=models.PROTECT)
    nombre = models.CharField('Nombre', max_length=50, unique=True)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='Cargo_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='Cargo_updated_by', editable=False)

    class Meta:
        verbose_name = 'Cargo'
        verbose_name_plural = 'Cargos'
        ordering = ['nombre',]

    def __str__(self):
        return self.nombre


class TipoInterlocutor(models.Model):
    '''Solo por Admin'''

    nombre = models.CharField('Nombre', max_length=50, unique=True)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='TipoInterlocutor_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='TipoInterlocutor_updated_by', editable=False)

    class Meta:
        verbose_name = 'Tipo de Interlocutor'
        verbose_name_plural = 'Tipos de Interlocutor'
        ordering = ['nombre',]

    def __str__(self):
        return self.nombre

class Departamento(models.Model):
    '''Solo por Admin'''

    codigo = models.CharField('Código', max_length=2, unique=True)
    nombre = models.CharField('Nombre', max_length=50, unique=True)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='Departamento_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='Departamento_updated_by', editable=False)

    class Meta:
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'
        ordering = ['nombre',]

    def __str__(self):
        return self.nombre


class Provincia(models.Model):
    '''Solo por Admin'''

    codigo = models.CharField('Código', max_length=2)
    nombre = models.CharField('Nombre', max_length=50)
    departamento = models.ForeignKey(Departamento, on_delete=models.PROTECT)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='Provincia_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='Provincia_updated_by', editable=False)

    class Meta:
        verbose_name = 'Provincia'
        verbose_name_plural = 'Provincias'
        ordering = ['nombre',]

    def __str__(self):
        return self.nombre


class Distrito(models.Model):
    '''Solo por Admin'''

    codigo = models.CharField('Código', max_length=2)
    nombre = models.CharField('Nombre', max_length=50)
    provincia = models.ForeignKey(Provincia, on_delete=models.PROTECT)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='Distrito_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='Distrito_updated_by', editable=False)

    class Meta:
        verbose_name = 'Distrito'
        verbose_name_plural = 'Distritos'
        ordering = ['nombre',]

    def __str__(self):
        return self.nombre


class Banco(models.Model):
    '''Solo por Admin'''

    razon_social = models.CharField('Razón Social', max_length=50, unique=True)
    nombre_comercial = models.CharField('Nombre Comercial', max_length=50, unique=True)
    estado = models.IntegerField('Estado', choices=ESTADOS, default=1)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='Banco_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='Banco_updated_by', editable=False)

    class Meta:
        verbose_name = 'Banco'
        verbose_name_plural = 'Bancos'

    def __str__(self):
        return self.razon_social


class DocumentoProceso(models.Model):
    nombre = models.CharField('Nombre', max_length=50, unique=True)
    descripcion = models.CharField('Descripción', max_length=250, blank=True, null=True)
    modelo = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='DocumentoProceso_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='DocumentoProceso_updated_by', editable=False)

    class Meta:
        verbose_name = 'Documento de Proceso'
        verbose_name_plural = 'Documentos de Proceso'

    def __str__(self):
        return self.nombre

class DocumentoFisico(models.Model):
    nombre = models.CharField('Nombre', max_length=50, unique=True)
    descripcion = models.CharField('Descripción', max_length=250, blank=True, null=True)
    modelo = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='DocumentoFisico_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='DocumentoFisico_updated_by', editable=False)

    class Meta:
        verbose_name = 'Documento Físico'
        verbose_name_plural = 'Documentos Físicos'

    def __str__(self):
        return self.nombre


class RangoDocumentoProceso(models.Model):
    modelo = models.ForeignKey(DocumentoProceso, on_delete=models.CASCADE)
    serie = models.CharField('Serie', max_length=10)
    rango_inicial = models.CharField('Rango Inicial', max_length=15)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='RangoDocumentoProceso_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='RangoDocumentoProceso_updated_by', editable=False)

    class Meta:
        verbose_name = 'Rango de Documento de Proceso'
        verbose_name_plural = 'Rangos de Documentos de Proceso'

    def __str__(self):
        return str(self.modelo)


class RangoDocumentoFisico(models.Model):
    modelo = models.ForeignKey(DocumentoFisico, on_delete=models.CASCADE)
    serie = models.CharField('Serie', max_length=10)
    rango_inicial = models.CharField('Rango Inicial', max_length=15)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='RangoDocumentoFisico_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='RangoDocumentoFisico_updated_by', editable=False)

    class Meta:
        verbose_name = 'Rango de Documento Físico'
        verbose_name_plural = 'Rangos de Documentos Físicos'

    def __str__(self):
        return str(self.modelo)


class CuentaBancariaSociedad(models.Model):
    sociedad = models.ForeignKey(Sociedad, on_delete=models.CASCADE)
    banco = models.ForeignKey(Banco, on_delete=models.CASCADE)
    moneda = models.ForeignKey(Moneda, on_delete=models.CASCADE)
    numero_cuenta = models.CharField('Número de Cuenta', max_length=20, unique=True)
    numero_cuenta_interbancaria = models.CharField('Número de Cuenta Interbancaria', max_length=20, unique=True)
    estado = models.IntegerField('Estado', choices=ESTADOS,default=1)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='CuentaBancariaSociedad_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='CuentaBancariaSociedad_updated_by', editable=False)

    class Meta:

        verbose_name = 'Cuenta Bancaria Sociedad'
        verbose_name_plural = 'Cuentas Bancarias Sociedad'

    def __str__(self):
        return str(self.sociedad) + ' ' + str(self.numero_cuenta)


class CuentaBancariaPersonal(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='User')
    banco = models.ForeignKey(Banco, on_delete=models.CASCADE)
    moneda = models.ForeignKey(Moneda, on_delete=models.CASCADE)
    numero_cuenta = models.CharField('Número de Cuenta', max_length=20, unique=True)
    numero_cuenta_interbancaria = models.CharField('Número de Cuenta Interbancaria', max_length=20, unique=True)
    estado = models.IntegerField('Estado', choices=ESTADOS,default=1)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='CuentaBancariaPersonal_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='CuentaBancariaPersonal_updated_by', editable=False)

    class Meta:

        verbose_name = 'Cuenta Bancaria Personal'
        verbose_name_plural = 'Cuentas Bancarias Personal'

    def __str__(self):
        return str(self.usuario) + ' ' + str(self.numero_cuenta)


class SegmentoSunat(models.Model):
    codigo = models.CharField('Código', max_length=10, unique=True)
    descripcion = models.CharField('Descripción', max_length=50, unique=True)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='SegmentoSunat_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='SegmentoSunat_updated_by', editable=False)

    class Meta:

        verbose_name = 'Segmento Sunat'
        verbose_name_plural = 'Segmentos Sunat'

    def __str__(self):
        return self.descripcion


class FamiliaSunat(models.Model):
    codigo = models.CharField('Código', max_length=10)
    descripcion = models.CharField('Descripción', max_length=50)
    segmento = models.ForeignKey(SegmentoSunat, on_delete=models.CASCADE)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='FamiliaSunat_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='FamiliaSunat_updated_by', editable=False)

    class Meta:

        verbose_name = 'Familia Sunat'
        verbose_name_plural = 'Familias Sunat'

    def __str__(self):
        return self.descripcion


class ClaseSunat(models.Model):
    codigo = models.CharField('Código', max_length=10)
    descripcion = models.CharField('Descripción', max_length=50)
    familia = models.ForeignKey(FamiliaSunat, on_delete=models.CASCADE)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='ClaseSunat_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='ClaseSunat_updated_by', editable=False)

    class Meta:

        verbose_name = 'Clase Sunat'
        verbose_name_plural = 'Clases Sunat'

    def __str__(self):
        return self.descripcion


class ProductoSunat(models.Model):
    codigo = models.CharField('Código', max_length=10)
    descripcion = models.CharField('Descripción', max_length=50)
    clase = models.ForeignKey(ClaseSunat, on_delete=models.CASCADE)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='ProductoSunat_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='ProductoSunat_updated_by', editable=False)

    class Meta:

        verbose_name = 'Producto Sunat'
        verbose_name_plural = 'Productos Sunat'

    def __str__(self):
        return self.descripcion
