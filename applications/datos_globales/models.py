from email.policy import default
from applications.datos_globales.managers import NubefactAccesoManager, SeriesComprobanteManager, TipoCambioManager
from applications.rutas import NUBEFACT_ACCESO_ENVIO, NUBEFACT_ACCESO_RESPUESTA
from applications.variables import ESTADOS
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from applications.sociedad.models import Sociedad
from django.db import models

from applications.funciones import validar_numero


class Moneda(models.Model):
    '''Solo por Admin'''

    nombre = models.CharField('Nombre', max_length=50, unique=True)
    abreviatura = models.CharField('Abreviatura', max_length=5, unique=True)
    simbolo = models.CharField('Símbolo', max_length=5)
    estado = models.IntegerField('Estado', choices=ESTADOS,default=1)
    principal = models.BooleanField(default=False)
    secundario = models.BooleanField(default=False)
    moneda_pais = models.BooleanField('Moneda del país', default=False)
    nubefact = models.IntegerField()

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

    nombre = models.CharField('Nombre', max_length=50, unique=True)
    simbolo = models.CharField('Símbolo', max_length=5)
    unidad_sunat = models.CharField('Unidad Sunat', max_length=5)
    magnitud = models.ForeignKey(Magnitud, on_delete=models.PROTECT)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='Unidad_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='Unidad_updated_by', editable=False)

    class Meta:
        verbose_name = 'Unidad'
        verbose_name_plural = 'Unidades'

    def save(self):
        self.nombre = self.nombre.upper()
        self.simbolo = self.simbolo.upper()
        self.unidad_sunat = self.unidad_sunat.upper()
        return super().save()

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

    def save(self):
        self.nombre = self.nombre.capitalize()
        return super().save()

    def __str__(self):
        return self.nombre


class Cargo(models.Model):
    '''Solo por Admin'''

    nombre = models.CharField('Nombre', max_length=50, unique=True)
    area = models.ForeignKey(Area, on_delete=models.PROTECT)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='Cargo_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='Cargo_updated_by', editable=False)

    class Meta:
        verbose_name = 'Cargo'
        verbose_name_plural = 'Cargos'
        ordering = ['nombre',]

    def save(self):
        self.nombre = self.nombre.capitalize()
        return super().save()

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

    def save(self):
        self.nombre = self.nombre.capitalize()
        return super().save()

    def __str__(self):
        return self.nombre


class Pais(models.Model):
    '''Solo por Admin'''

    nombre = models.CharField('Nombre', max_length=50, unique=True)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='Pais_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='Pais_updated_by', editable=False)

    class Meta:
        verbose_name = 'Pais'
        verbose_name_plural = 'Paises'
        ordering = ['nombre',]

    def save(self):
        self.nombre = self.nombre.upper()
        return super().save()

    def __str__(self):
        return self.nombre


class Departamento(models.Model):
    '''Solo por Admin'''

    codigo = models.CharField('Código', max_length=2, unique=True, primary_key=True)
    nombre = models.CharField('Nombre', max_length=50, unique=True)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='Departamento_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='Departamento_updated_by', editable=False)

    class Meta:
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'
        ordering = ['nombre',]

    def save(self):
        self.nombre = self.nombre.upper()
        return super().save()

    def __str__(self):
        return self.codigo + ' - ' + self.nombre


class Provincia(models.Model):
    '''Solo por Admin'''

    codigo = models.CharField('Código', max_length=4, primary_key=True)
    nombre = models.CharField('Nombre', max_length=50)
    departamento = models.ForeignKey(Departamento, on_delete=models.PROTECT)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='Provincia_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='Provincia_updated_by', editable=False)

    class Meta:
        verbose_name = 'Provincia'
        verbose_name_plural = 'Provincias'
        ordering = ['departamento__nombre', 'nombre',]

    def save(self):
        self.nombre = self.nombre.upper()
        return super().save()

    def __str__(self):
        return self.codigo + ' - ' + self.nombre


class Distrito(models.Model):
    '''Solo por Admin'''

    codigo = models.CharField('Código', max_length=6, primary_key=True)
    nombre = models.CharField('Nombre', max_length=50)
    provincia = models.ForeignKey(Provincia, on_delete=models.PROTECT)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='Distrito_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='Distrito_updated_by', editable=False)

    class Meta:
        verbose_name = 'Distrito'
        verbose_name_plural = 'Distritos'
        ordering = ['provincia__nombre', 'nombre',]

    def save(self):
        self.nombre = self.nombre.upper()
        return super().save()

    def __str__(self):
        return self.codigo + ' - ' + self.nombre


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

    def save(self):
        self.nombre = self.nombre.capitalize()
        self.descripcion = self.descripcion.capitalize()
        return super().save()

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

    def save(self):
        self.nombre = self.nombre.capitalize()
        self.descripcion = self.descripcion.capitalize()
        return super().save()

    def __str__(self):
        return self.nombre


class RangoDocumentoProceso(models.Model):
    serie = models.CharField('Serie', max_length=10)
    rango_inicial = models.CharField('Rango Inicial', max_length=15)
    modelo = models.ForeignKey(DocumentoProceso, on_delete=models.CASCADE)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='RangoDocumentoProceso_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='RangoDocumentoProceso_updated_by', editable=False)

    class Meta:
        verbose_name = 'Rango de Documento de Proceso'
        verbose_name_plural = 'Rangos de Documentos de Proceso'
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'modelo',
                    'serie',
                    ], name='RangoDocumentoProceso_modelo_serie',
                ), 
            ]

    def __str__(self):
        return str(self.modelo)


class RangoDocumentoFisico(models.Model):
    serie = models.CharField('Serie', max_length=10)
    rango_inicial = models.CharField('Rango Inicial', max_length=15)
    modelo = models.ForeignKey(DocumentoFisico, on_delete=models.CASCADE)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='RangoDocumentoFisico_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='RangoDocumentoFisico_updated_by', editable=False)

    class Meta:
        verbose_name = 'Rango de Documento Físico'
        verbose_name_plural = 'Rangos de Documentos Físicos'
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'modelo',
                    'serie',
                    ], name='RangoDocumentoFisico_modelo_serie',
                ), 
            ]

    def __str__(self):
        return str(self.modelo)


class CuentaBancariaSociedad(models.Model):
    numero_cuenta = models.CharField('Número de Cuenta', max_length=20, unique=True, validators=[validar_numero])
    numero_cuenta_interbancaria = models.CharField('Número de Cuenta Interbancaria', max_length=20, unique=True, validators=[validar_numero])
    banco = models.ForeignKey(Banco, on_delete=models.CASCADE)
    moneda = models.ForeignKey(Moneda, on_delete=models.CASCADE)
    sociedad = models.ForeignKey(Sociedad, on_delete=models.CASCADE)
    estado = models.IntegerField('Estado', choices=ESTADOS,default=1)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='CuentaBancariaSociedad_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='CuentaBancariaSociedad_updated_by', editable=False)

    class Meta:

        verbose_name = 'Cuenta Bancaria Sociedad'
        verbose_name_plural = 'Cuentas Bancarias Sociedad'
        ordering = [
            'sociedad',
            'banco',
            'moneda',
            ]

    def __str__(self):
        return "%s %s : %s | %s - %s" % (self.banco.nombre_comercial, self.moneda, self.numero_cuenta, self.numero_cuenta_interbancaria, self.sociedad)


class CuentaBancariaPersonal(models.Model):
    numero_cuenta = models.CharField('Número de Cuenta', max_length=20, unique=True, validators=[validar_numero])
    numero_cuenta_interbancaria = models.CharField('Número de Cuenta Interbancaria', max_length=20, unique=True, validators=[validar_numero])
    banco = models.ForeignKey(Banco, on_delete=models.CASCADE)
    moneda = models.ForeignKey(Moneda, on_delete=models.CASCADE)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='User')
    estado = models.IntegerField('Estado', choices=ESTADOS,default=1)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='CuentaBancariaPersonal_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='CuentaBancariaPersonal_updated_by', editable=False)

    class Meta:

        verbose_name = 'Cuenta Bancaria Personal'
        verbose_name_plural = 'Cuentas Bancarias Personal'

    def __str__(self):
        return str(self.banco.nombre_comercial) + ' : ' + str(self.numero_cuenta) + ' | ' + str(self.numero_cuenta_interbancaria) + ' - ' +  str(self.usuario) 


class SegmentoSunat(models.Model):
    codigo = models.CharField('Código', max_length=2, primary_key=True)
    descripcion = models.CharField('Descripción', max_length=255, unique=True)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='SegmentoSunat_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='SegmentoSunat_updated_by', editable=False)

    class Meta:

        verbose_name = 'Segmento Sunat'
        verbose_name_plural = 'Segmentos Sunat'
        ordering = ['codigo',]

    def save(self):
        self.descripcion = self.descripcion.upper()
        return super().save()

    def __str__(self):
        return self.codigo + ' - ' + self.descripcion


class FamiliaSunat(models.Model):
    codigo = models.CharField('Código', max_length=4, primary_key=True)
    descripcion = models.CharField('Descripción', max_length=255)
    segmento = models.ForeignKey(SegmentoSunat, on_delete=models.CASCADE)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='FamiliaSunat_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='FamiliaSunat_updated_by', editable=False)

    class Meta:

        verbose_name = 'Familia Sunat'
        verbose_name_plural = 'Familias Sunat'
        ordering = ['codigo',]

    def save(self):
        self.descripcion = self.descripcion.upper()
        return super().save()

    def __str__(self):
        return self.codigo + ' - ' + self.descripcion


class ClaseSunat(models.Model):
    codigo = models.CharField('Código', max_length=6, primary_key=True)
    descripcion = models.CharField('Descripción', max_length=255)
    familia = models.ForeignKey(FamiliaSunat, on_delete=models.CASCADE)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='ClaseSunat_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='ClaseSunat_updated_by', editable=False)

    class Meta:

        verbose_name = 'Clase Sunat'
        verbose_name_plural = 'Clases Sunat'
        ordering = ['codigo',]

    def save(self):
        self.descripcion = self.descripcion.upper()
        return super().save()

    def __str__(self):
        return self.codigo + ' - ' + self.descripcion


class ProductoSunat(models.Model):
    codigo = models.CharField('Código', max_length=8, primary_key=True)
    descripcion = models.CharField('Descripción', max_length=255)
    clase = models.ForeignKey(ClaseSunat, on_delete=models.CASCADE)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='ProductoSunat_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='ProductoSunat_updated_by', editable=False)

    class Meta:

        verbose_name = 'Producto Sunat'
        verbose_name_plural = 'Productos Sunat'
        ordering = ['codigo',]

    def save(self):
        self.descripcion = self.descripcion.upper()
        return super().save()

    def __str__(self):
        return self.codigo + ' - ' + self.descripcion


class TipoCambio(models.Model):
    fecha = models.DateField('Fecha', auto_now=False, auto_now_add=False)
    tipo_cambio_venta = models.DecimalField('Tipo de Cambio Venta', max_digits=4, decimal_places=3)
    tipo_cambio_compra = models.DecimalField('Tipo de Cambio Compra', max_digits=4, decimal_places=3, default= 0)
    moneda_origen = models.ForeignKey(Moneda, on_delete=models.CASCADE, related_name='TipoCambio_moneda_origen')
    moneda_destino = models.ForeignKey(Moneda, on_delete=models.CASCADE, related_name='TipoCambio_moneda_destino')
    
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='TipoCambio_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='TipoCambio_updated_by', editable=False)

    objects = TipoCambioManager()

    class Meta:
        verbose_name = 'Tipo de Cambio'
        verbose_name_plural = 'Tipos de Cambio'
        ordering = [
            '-fecha',
            '-updated_at',
        ]
    
    @property
    def venta(self):
        return self.tipo_cambio_venta
    
    @property
    def compra(self):
        if self.tipo_cambio_compra:
            return self.tipo_cambio_compra
        else:
            return self.tipo_cambio_venta

    def __str__(self):     
        return str(self.fecha)


class TipoCambioSunat(models.Model):
    fecha = models.DateField('Fecha', auto_now=False, auto_now_add=False)
    tipo_cambio_venta = models.DecimalField('Tipo de Cambio Venta', max_digits=4, decimal_places=3)
    tipo_cambio_compra = models.DecimalField('Tipo de Cambio Compra', max_digits=4, decimal_places=3)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='TipoCambioSunat_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='TipoCambioSunat_updated_by', editable=False)

    class Meta:
        verbose_name = 'Tipo de Cambio Sunat'
        verbose_name_plural = 'Tipos de Cambio Sunat'
        ordering = [
            '-fecha',
            '-updated_at',
        ]

    def __str__(self):     
        return str(self.fecha)


class RemuneracionMinimaVital(models.Model):
    fecha_inicio = models.DateField('Fecha de Inicio', auto_now=False, auto_now_add=False)
    monto = models.DecimalField('Monto', max_digits=7, decimal_places=2)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='RemuneracionMinimaVital_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='RemuneracionMinimaVital_updated_by', editable=False)

    class Meta:
        verbose_name = 'Remuneración Mínima Vital'
        verbose_name_plural = 'Remuneración Mínima Vital'
        ordering = [
            '-fecha_inicio',
        ]

    def __str__(self):     
        return self.monto


class UnidadImpositivaTributaria(models.Model):
    fecha_inicio = models.DateField('Fecha de Inicio', auto_now=False, auto_now_add=False)
    monto = models.DecimalField('Monto', max_digits=7, decimal_places=2)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='UnidadImpositivaTributaria_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='UnidadImpositivaTributaria_updated_by', editable=False)

    class Meta:
        verbose_name = 'Unidad Impositiva Tributaria'
        verbose_name_plural = 'Unidad Impositiva Tributaria'
        ordering = [
            '-fecha_inicio',
        ]

    def __str__(self):     
        return self.monto


class ImpuestoGeneralVentas(models.Model):
    fecha_inicio = models.DateField('Fecha de Inicio', auto_now=False, auto_now_add=False)
    monto = models.DecimalField('Monto', max_digits=4, decimal_places=2)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='ImpuestoGeneralVentas_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='ImpuestoGeneralVentas_updated_by', editable=False)

    class Meta:
        verbose_name = 'Impuesto General a las Ventas'
        verbose_name_plural = 'Impuesto General a las Ventas'
        ordering = [
            '-fecha_inicio',
        ]

    def __str__(self):     
        return str(self.monto)


class ImpuestoPromocionMunicipal(models.Model):
    fecha_inicio = models.DateField('Fecha de Inicio', auto_now=False, auto_now_add=False)
    monto = models.DecimalField('Monto', max_digits=4, decimal_places=2)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='ImpuestoPromocionMunicipal_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='ImpuestoPromocionMunicipal_updated_by', editable=False)

    class Meta:
        verbose_name = 'Impuesto de Promoción Municipal'
        verbose_name_plural = 'Impuesto de Promoción Municipal'
        ordering = [
            '-fecha_inicio',
        ]

    def __str__(self):     
        return str(self.monto)


class SeriesComprobante(models.Model):
    tipo_comprobante = models.ForeignKey(ContentType, blank=True, null=True, on_delete=models.PROTECT)
    serie = models.CharField('Serie', max_length=4)
    defecto = models.BooleanField(default=False)
    contingencia = models.BooleanField(default=False)
    
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='SeriesComprobante_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='SeriesComprobante_updated_by', editable=False)

    objects = SeriesComprobanteManager()
    
    class Meta:
        verbose_name = 'Series Comprobante'
        verbose_name_plural = 'Series Comprobantes'

    def __str__(self):
        return self.serie


class NubefactAcceso(models.Model):
    descripcion = models.CharField(max_length=100)
    ruta = models.URLField(max_length=200)
    token = models.CharField(max_length=200)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='NubefactAcceso_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='NubefactAcceso_updated_by', editable=False)

    objects = NubefactAccesoManager()

    class Meta:
        verbose_name = 'Nubefact Acceso'
        verbose_name_plural = 'Nubefact Accesos'

    def __str__(self):
        return self.descripcion


class NubefactSerieAcceso(models.Model):
    sociedad = models.ForeignKey(Sociedad, on_delete=models.PROTECT)
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    serie_comprobante = models.ForeignKey(SeriesComprobante, on_delete=models.PROTECT, related_name='NubefactSerieAcceso_serie_comprobante')
    acceso = models.ForeignKey(NubefactAcceso, on_delete=models.CASCADE)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='NubefactSerieAcceso_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='NubefactSerieAcceso_updated_by', editable=False)

    objects = NubefactAccesoManager()

    class Meta:
        verbose_name = 'Nubefact Serie Acceso'
        verbose_name_plural = 'Nubefact Serie Accesos'

    def __str__(self):
        return "%s - %s" % (self.acceso, self.id)


class NubefactRespuesta(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    id_registro = models.IntegerField()
    aceptado = models.BooleanField(default=False)
    error = models.BooleanField(default=False)
    envio = models.JSONField() #Usar json.loads() para leer el diccionario
    respuesta = models.JSONField(blank=True, null=True) #Usar json.loads() para leer el diccionario

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='NubefactRespuesta_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='NubefactRespuesta_updated_by', editable=False)

    class Meta:
        verbose_name = 'Nubefact Respuesta'
        verbose_name_plural = 'Nubefact Respuestas'
        ordering = [
            'updated_at',
            ]

    def __str__(self):
        return "%s" % self.aceptado