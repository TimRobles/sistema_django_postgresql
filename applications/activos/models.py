from django.db import models
from django.conf import settings
from applications.datos_globales.models import ProductoSunat, Unidad, Moneda
from applications.usuario.models import DatosUsuario
from django.contrib.contenttypes.models import ContentType
from applications.variables import ESTADOS, INCOTERMS, INTERNACIONAL_NACIONAL, TIPO_COMPROBANTE, TIPO_IGV_CHOICES
from applications.sede.models import Sede
from applications.sociedad.models import Sociedad
from applications.orden_compra.models import OrdenCompra, OrdenCompraDetalle
from django.db.models.signals import pre_save, post_save, post_delete

from applications.funciones import obtener_totales
from applications.importaciones import registro_guardar, registro_guardar_user


class FamiliaActivo(models.Model):
    nombre = models.CharField('Nombre', max_length=50)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='FamiliaActivo_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='FamiliaActivo_updated_by', editable=False)

    class Meta:
        verbose_name = 'Familia Activo'
        verbose_name_plural = 'Familias Activo'
        ordering = ['nombre',]

    def __str__(self):
        return self.nombre


class SubFamiliaActivo(models.Model):
    nombre = models.CharField('Nombre', max_length=50)
    familia = models.ForeignKey(FamiliaActivo, on_delete=models.PROTECT)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='SubFamiliaActivo_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='SubFamiliaActivo_updated_by', editable=False)

    class Meta:
        verbose_name = 'SubFamilia Activo'
        verbose_name_plural = 'SubFamilias Activo'
        ordering = ['nombre',]

    def __str__(self):
        return self.nombre


class ModeloActivo(models.Model):
    nombre = models.CharField('Nombre', max_length=50)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='ModeloActivo_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='ModeloActivo_updated_by', editable=False)

    class Meta:
        verbose_name = 'Modelo Activo'
        verbose_name_plural = 'Modelos Activo'
        ordering = ['nombre',]

    def __str__(self):
        return self.nombre


class MarcaActivo(models.Model):
    nombre = models.CharField('Nombre', max_length=50)
    modelos = models.ManyToManyField(ModeloActivo)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='MarcaActivo_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='MarcaActivo_updated_by', editable=False)

    class Meta:
        verbose_name = 'Marca Activo'
        verbose_name_plural = 'Marcas Activo'
        ordering = ['nombre',]

    def __str__(self):
        return self.nombre


class ActivoBase(models.Model):
    descripcion_venta = models.CharField('Descripción de Venta', max_length=150, null=True, blank=True)
    descripcion_corta = models.CharField('Descripción Corta', max_length=150)
    unidad = models.ForeignKey(Unidad, on_delete=models.CASCADE, blank=True, null=True)
    peso = models.DecimalField('Peso', max_digits=6, decimal_places=2, blank=True, null=True)
    sub_familia = models.ForeignKey(SubFamiliaActivo, on_delete=models.CASCADE, blank=True, null=True)
    depreciacion = models.DecimalField('Depreciación', max_digits=6, decimal_places=3)
    vida_util = models.IntegerField('Vida Útil (meses)', blank=True, null=True)
    producto_sunat = models.ForeignKey(ProductoSunat, on_delete=models.CASCADE, blank=True, null=True)
    estado = models.IntegerField('Estado Activo', choices=ESTADOS, default=1)
    traduccion = models.CharField('Traducción', max_length=255, blank=True, null=True)
    partida = models.CharField('Partida', max_length=30, blank=True, null=True)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='ActivoBase_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='ActivoBase_updated_by', editable=False)


    class Meta:
        verbose_name = 'Activo Base'
        verbose_name_plural = 'Activos Base'
        ordering = [
            'descripcion_corta',
            ]

    def content_type(self):
        return ContentType.objects.get_for_model(self).id

    def __str__(self):
        return self.descripcion_corta.upper()


class AsignacionActivo(models.Model):
    ESTADOS_ASIGNACION = [
        (1, 'ALTA'),
        (2, 'ENTREGADO'),
        (3, 'CONCLUIDO SIN ENTREGAR'),
        (4, 'ANULADO'),
        ]
    titulo = models.CharField('Título', max_length=50)
    colaborador = models.ForeignKey(DatosUsuario, on_delete=models.PROTECT)
    fecha_asignacion = models.DateField('Fecha Asignación', auto_now=False, auto_now_add=False)
    observacion = models.TextField(null=True, blank=True)
    fecha_entrega = models.DateField('Fecha Entrega', auto_now=False, auto_now_add=False, null=True, blank=True)
    estado = models.IntegerField('Estado Asignación', choices=ESTADOS_ASIGNACION, default=1)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='AsignacionActivo_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='AsignacionActivo_updated_by', editable=False)

    class Meta:
        verbose_name = 'Asignación de Activo'
        verbose_name_plural = 'Asignación de Activos'
        ordering = [
            '-fecha_asignacion',
            ]

    def __str__(self):
        return self.titulo


class AsignacionDetalleActivo(models.Model):
    activo = models.ForeignKey('Activo', on_delete=models.PROTECT, related_name='AsignacionDetalleActivo_activo')
    asignacion = models.ForeignKey(AsignacionActivo, on_delete=models.PROTECT, related_name='AsignacionDetalleActivo_asignacion')
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='AsignacionActivoDetalle_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='AsignacionActivoDetalle_updated_by', editable=False)

    class Meta:
        verbose_name = 'Asignación Detalle del Activo'
        verbose_name_plural = 'Asignación Detalle de Activos'

    def __str__(self):
        return str(self.activo.descripcion)

class Activo(models.Model):
    ESTADOS_ACTIVO = [
        (1, 'ALTA'),
        (2, 'EN PROCESO ASIGNACIÓN'),
        (3, 'ASIGNADO'),
        (4, 'EN PROCESO DEVOLUCIÓN'),
        ]
    numero_serie = models.CharField('Número de Serie', max_length=25)
    descripcion = models.CharField('Descripción', max_length=150, blank=True, null=True)
    content_type = models.ForeignKey(ContentType, blank=True, null=True, on_delete=models.PROTECT)
    id_registro = models.IntegerField(blank=True, null=True)
    activo_base = models.ForeignKey(ActivoBase, verbose_name='Activo Base', on_delete=models.CASCADE, blank=True, null=True)
    marca = models.ForeignKey(MarcaActivo, on_delete=models.CASCADE, blank=True, null=True)
    modelo = models.ForeignKey(ModeloActivo, on_delete=models.CASCADE, blank=True, null=True)
    fecha_compra = models.DateField('Fecha de Compra', auto_now=False, auto_now_add=False, blank=True, null=True)
    tiempo_garantia = models.IntegerField('Tiempo de Garantía (meses)', blank=True, null=True)
    color = models.CharField('Color', max_length=25, blank=True, null=True)
    informacion_adicional = models.TextField('Información Adicional', blank=True, null=True)
    declarable = models.BooleanField('Declarable', default=False)
    estado = models.IntegerField('Estado Activo', choices=ESTADOS_ACTIVO, default=1)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='Activo_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='Activo_updated_by', editable=False)
    
    class Meta:

        verbose_name = 'Activo'
        verbose_name_plural = 'Activos'
        ordering = ['numero_serie',]

    @property
    def colaborador(self):
        return self.AsignacionDetalleActivo_activo.all()

    @property
    def empresa(self):
        if self.ActivoSociedad_activo.all():
            return self.ActivoSociedad_activo.all()[0].sociedad.razon_social
        else:
            return ""

    def __str__(self):
        return str(self.descripcion)


from django.db.models.signals import post_save

def actualizar_estado_activo_asignacion(*args, **kwargs):
    obj = kwargs['instance']
    activo = Activo.objects.get(id=obj.activo.id)
    activo.estado = 2
    activo.save()

post_save.connect(actualizar_estado_activo_asignacion, sender=AsignacionDetalleActivo)


class ArchivoAsignacionActivo(models.Model):
    archivo = models.FileField('Archivo', blank=True, null=True)
    asignacion = models.ForeignKey(AsignacionActivo, on_delete=models.PROTECT)
    comentario = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='ArchivoAsignacionActivo_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='ArchivoAsignacionActivo_updated_by', editable=False)

    class Meta:
        verbose_name = 'Archivo Asignación de Activos'
        verbose_name_plural = 'Archivos Asignación de Activos'

    def __str__(self):
        return str(self.asignacion)


class DevolucionActivo(models.Model):
    ESTADOS_Devolucion = [
        (1, 'ALTA'),
        (2, 'RECEPCIONADO'),
        (3, 'ANULADO'),
        ]
    titulo = models.CharField('Título', max_length=50)
    colaborador = models.ForeignKey(DatosUsuario, on_delete=models.PROTECT)
    fecha_devolucion = models.DateField('Fecha Devolución', auto_now=False, auto_now_add=False)
    observacion = models.TextField(null=True, blank=True)
    estado = models.IntegerField('Estado Devolución', choices=ESTADOS_Devolucion, default=1)
    archivo = models.FileField('Archivo', blank=True, null=True)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='DevolucionActivo_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='DevolucionActivo_updated_by', editable=False)

    class Meta:
        verbose_name = 'Devolución de Activo'
        verbose_name_plural = 'Devolución de Activos'
        ordering = [
            '-fecha_devolucion',
            ]

    def __str__(self):
        return self.titulo


class DevolucionDetalleActivo(models.Model):
    asignacion = models.ForeignKey(AsignacionActivo, on_delete=models.PROTECT, related_name='DevolucionDetalleActivo_asignacion')
    activo = models.ForeignKey('Activo', on_delete=models.PROTECT, related_name='DevolucionDetalleActivo_activo')
    devolucion = models.ForeignKey(DevolucionActivo, on_delete=models.PROTECT, related_name='DevolucionDetalleActivo_devolucion')
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='DevolucionActivoDetalle_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='DevolucionActivoDetalle_updated_by', editable=False)

    class Meta:
        verbose_name = 'Devolución Detalle del Activo'
        verbose_name_plural = 'Devolución Detalle de Activos'

    def __str__(self):
        return str(self.activo.descripcion)


def actualizar_estado_activo_devolucion(*args, **kwargs):
    obj = kwargs['instance']
    activo = Activo.objects.get(id=obj.activo.id)
    activo.estado = 4
    activo.save()

post_save.connect(actualizar_estado_activo_devolucion, sender=DevolucionDetalleActivo)


class ArchivoDevolucionActivo(models.Model):
    archivo = models.FileField('Archivo', blank=True, null=True)
    devolucion = models.ForeignKey(DevolucionActivo, on_delete=models.PROTECT)
    comentario = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='ArchivodevolucionActivo_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='ArchivodevolucionActivo_updated_by', editable=False)

    class Meta:
        verbose_name = 'Archivo Devolución de Activos'
        verbose_name_plural = 'Archivos Devolución de Activos'

    def __str__(self):
        return str(self.devolucion)


class EstadoActivo(models.Model):
    nro_estado = models.IntegerField('Estado del Activo')
    descripcion = models.CharField('Descripción del estado', max_length=50)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='EstadoActivo_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='EstadoActivo_updated_by', editable=False)

    class Meta:
        verbose_name = 'Estado Activo'
        verbose_name_plural = 'Estado Activos'

    def __str__(self):
        return str(self.descripcion)


class HistorialEstadoActivo(models.Model):
    activo = models.ForeignKey(Activo, on_delete=models.PROTECT)
    content_type = models.ForeignKey(ContentType, blank=True, null=True, on_delete=models.PROTECT)
    id_registro = models.IntegerField(blank=True, null=True)
    estado = models.ForeignKey(EstadoActivo, on_delete=models.PROTECT)
    estado_anterior = models.ForeignKey('self', on_delete=models.PROTECT, blank=True, null=True)
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='HistorialEstadoActivo_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='HistorialEstadoActivo_updated_by', editable=False)

    class Meta:
        verbose_name = 'Historial Estado Activo'
        verbose_name_plural = 'Historial Estado Activos'

    def __str__(self):
        return str(self.estado)



class ActivoSociedad(models.Model):

    sociedad = models.ForeignKey(Sociedad, on_delete=models.CASCADE, blank=True, null=True)
    activo = models.ForeignKey(Activo, on_delete=models.CASCADE, blank=True, null=True, related_name='ActivoSociedad_activo')

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='ActivoSociedad_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='ActivoSociedad_updated_by', editable=False)
    
    class Meta:

        verbose_name = 'Activo Sociedad'
        verbose_name_plural = 'Activos Sociedad'
        ordering = ['activo',]

    def __str__(self):
        return str(self.activo)


class ActivoUbicacion(models.Model):

    sede = models.ForeignKey(Sede, on_delete=models.CASCADE, blank=True, null=True)
    piso = models.IntegerField( blank=True, null=True)
    activo = models.ForeignKey(Activo, on_delete=models.CASCADE, blank=True, null=True)
    comentario = models.TextField( blank=True, null=True)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='ActivoUbicacion_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='ActivoUbicacion_updated_by', editable=False)
    
    class Meta:

        verbose_name = 'Activo Ubicacion'
        verbose_name_plural = 'Activos Ubicacion'
        ordering = ['activo',]

    def __str__(self):
        return self.activo


class ComprobanteCompraActivo(models.Model):

    numero_comprobante = models.CharField('Número de Comprobante', max_length=50, blank=True, null=True)
    internacional_nacional = models.IntegerField('Tipo de Compra', choices=INTERNACIONAL_NACIONAL)
    incoterms = models.IntegerField('INCOTERMS', choices=INCOTERMS, blank=True, null=True)
    tipo_comprobante = models.IntegerField('Tipo de Comprobante', choices=TIPO_COMPROBANTE)
    orden_compra = models.ForeignKey(OrdenCompra, verbose_name='Orden de Compra', null=True, blank=True, on_delete=models.CASCADE)
    sociedad = models.ForeignKey(Sociedad, on_delete=models.CASCADE, blank=True, null=True)
    fecha_comprobante = models.DateField('Fecha de Comprobante', auto_now=False, auto_now_add=False, blank=True, null=True)
    moneda = models.ForeignKey(Moneda, null=True,  on_delete=models.PROTECT)
    descuento_global = models.DecimalField('Descuento Global', max_digits=14, decimal_places=2, default=0)
    total_descuento = models.DecimalField('Total Descuento', max_digits=14, decimal_places=2, default=0)
    total_anticipo = models.DecimalField('Total Anticipo', max_digits=14, decimal_places=2, default=0)
    total_gravada = models.DecimalField('Total Gravada', max_digits=14, decimal_places=2, default=0)
    total_inafecta = models.DecimalField('Total Inafecta', max_digits=14, decimal_places=2, default=0)
    total_exonerada = models.DecimalField('Total Exonerada', max_digits=14, decimal_places=2, default=0)
    total_igv = models.DecimalField('Total IGV', max_digits=14, decimal_places=2, default=0)
    total_gratuita = models.DecimalField('Total Gratuita', max_digits=14, decimal_places=2, default=0)
    total_otros_cargos = models.DecimalField('Total Otros Cargos', max_digits=14, decimal_places=2, default=0)
    total_icbper = models.DecimalField('Total ICBPER', max_digits=14, decimal_places=2, default=0)
    total = models.DecimalField('Total', max_digits=14, decimal_places=2, default=0)
    archivo = models.FileField('Archivo', blank=True, null=True)
    condiciones = models.TextField('Condiciones', null=True, blank=True)
    logistico = models.DecimalField('Logístico', max_digits=3, decimal_places=2, null=True, blank=True)
    estado = models.IntegerField('Estado', choices=ESTADOS, default=1)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='ComprobanteCompraActivo_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='ComprobanteCompraActivo_updated_by', editable=False)

    class Meta:
        verbose_name = 'Comprobante Compra Activo'
        verbose_name_plural = 'Comprobantes Compra Activo'
        ordering = [
            '-fecha_comprobante',
        ]

    def __str__(self):
        return self.numero_comprobante


class ComprobanteCompraActivoDetalle(models.Model):

    item = models.IntegerField(blank=True, null=True)
    descripcion_comprobante = models.TextField('Descripción Comprobante', null=True, blank=True)
    orden_compra_detalle = models.ForeignKey(OrdenCompraDetalle, verbose_name='Orden de Compra Detalle', null=True, blank=True, on_delete=models.CASCADE)
    activo = models.ForeignKey(Activo, on_delete=models.CASCADE, blank=True, null=True)
    cantidad = models.DecimalField('Cantidad', max_digits=22, decimal_places=10, default=0)
    precio_unitario_sin_igv = models.DecimalField('Precio Unitario sin IGV', max_digits=22, decimal_places=10, default=0)
    precio_unitario_con_igv = models.DecimalField('Precio Unitario con IGV', max_digits=22, decimal_places=10, default=0)
    precio_final_con_igv = models.DecimalField('Precio Final con IGV', max_digits=22, decimal_places=10, default=0)
    descuento = models.DecimalField('Descuento', max_digits=14, decimal_places=2, default=0)
    sub_total = models.DecimalField('Sub Total', max_digits=14, decimal_places=2, default=0)
    igv = models.DecimalField('IGV', max_digits=14, decimal_places=2, default=0)
    total = models.DecimalField('Total', max_digits=14, decimal_places=2, default=0)
    tipo_igv = models.IntegerField('Tipo de IGV', choices=TIPO_IGV_CHOICES, null=True)
    comprobante_compra_activo = models.ForeignKey(ComprobanteCompraActivo, verbose_name='Comprobante de Compra', on_delete=models.CASCADE, related_name='ComprobanteCompraActivoDetalle_comprobante_compra_activo')

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='ComprobanteCompraActivoDetalle_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='ComprobanteCompraActivoDetalle_updated_by', editable=False)

    class Meta:
        verbose_name = 'Comprobante Compra Activo Detalle'
        verbose_name_plural = 'Comprobantes Compra Activo Detalle'
        ordering = [
            'item',
            ]

    def __str__(self):
        return str(self.comprobante_compra_activo)

def ComprobanteCompraActivoDetalle_post_save(*args, **kwargs):
    obj = kwargs['instance']
    totales = obtener_totales(ComprobanteCompraActivo.objects.get(id=obj.comprobante_compra_activo.id))
    for key, value in totales.items():
        setattr( obj.comprobante_compra_activo, key, value)
    registro_guardar_user(obj.comprobante_compra_activo, obj.updated_by)
    obj.comprobante_compra_activo.save()

post_save.connect(ComprobanteCompraActivoDetalle_post_save, sender=ComprobanteCompraActivoDetalle)

def ComprobanteCompraActivoDetalle_post_delete(sender, instance, *args, **kwargs):
    obj = instance
    totales = obtener_totales(ComprobanteCompraActivo.objects.get(id=obj.comprobante_compra_activo.id))
    for key, value in totales.items():
        setattr( obj.comprobante_compra_activo, key, value)
    registro_guardar_user(obj.comprobante_compra_activo, obj.updated_by)
    obj.comprobante_compra_activo.save()

post_delete.connect(ComprobanteCompraActivoDetalle_post_delete, sender=ComprobanteCompraActivoDetalle)


class ArchivoComprobanteCompraActivo(models.Model):

    archivo = models.FileField('Archivo', blank=True, null=True)
    comprobante_compra_activo = models.ForeignKey(ComprobanteCompraActivo, verbose_name='Comprobante de Compra', on_delete=models.CASCADE)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='ArchivoComprobanteCompraActivo_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='ArchivoComprobanteCompraActivo_updated_by', editable=False)

    class Meta:
        verbose_name = 'Archivo Comprobante Compra Activo'
        verbose_name_plural = 'Archivos Comprobante Compra Activo'

    def __str__(self):
        return str(self.comprobante_compra_activo)


class InventarioActivo(models.Model):

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, related_name='InventarioActivo_Usuario')
    fecha_inventario = models.DateField('Fecha de Inventario', auto_now=False, auto_now_add=False, blank=True, null=True)
    observacion = models.TextField('Observación', blank=True, null=True)
    documento = models.FileField('Doc. Inventario', blank=True, null=True)
    estado = models.IntegerField('Estado', choices=ESTADOS, default=1)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='InventarioActivo_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='InventarioActivo_updated_by', editable=False)
    
    class Meta:
        verbose_name = 'Inventario Activo'
        verbose_name_plural = 'Inventarios Activo'

    def __str__(self):
        return str(self.usuario)


class InventarioActivoDetalle(models.Model):

    activo = models.ForeignKey(Activo, on_delete=models.CASCADE, blank=True, null=True)
    inventario_activo = models.ForeignKey(InventarioActivo, verbose_name='Inventario Activo', on_delete=models.PROTECT)
    observacion = models.TextField('Observación', blank=True, null=True)
    estado = models.IntegerField('Estado', choices=ESTADOS, default=1)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='InventarioActivoDetalle_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='InventarioActivoDetalle_updated_by', editable=False)
    
    class Meta:
        verbose_name = 'Inventario Activo Detalle'
        verbose_name_plural = 'Inventarios Activo Detalle'

    def __str__(self):
        return self.activo