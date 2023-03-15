from decimal import Decimal
from secrets import choice
from django.conf import settings
from django.db import models
from django.contrib.contenttypes.models import ContentType
from applications.clientes.models import Cliente
from applications.funciones import numeroXn
from applications.logistica.managers import SerieManager
from applications.sociedad.models import Sociedad
from applications.material.models import Material, SubFamilia
from applications.sede.models import Sede
from applications.almacenes.models import Almacen
from applications.nota_ingreso.models import NotaIngreso, NotaIngresoDetalle
from applications.movimiento_almacen.models import MovimientosAlmacen, TipoStock
from applications.variables import ESTADOS_NOTA_CALIDAD_STOCK, SERIE_CONSULTA

from django.db.models.signals import pre_delete, post_delete

class FallaMaterial(models.Model):
    sub_familia = models.ForeignKey(SubFamilia, on_delete=models.CASCADE, related_name='FallaMaterial_sub_familia')
    titulo = models.CharField('Titulo', max_length=50)
    comentario = models.TextField()
    visible = models.BooleanField()
  
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='FallaMaterial_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='FallaMaterial_updated_by', editable=False)

    class Meta:
        verbose_name = 'Falla Material'
        verbose_name_plural = 'Fallas Materiales'

    def __str__(self):
        return str(self.titulo)


class SolucionMaterial(models.Model):
    falla_material = models.ForeignKey(FallaMaterial, on_delete=models.CASCADE, related_name='SolucionMaterial_falla_material')
    titulo = models.CharField('Titulo', max_length=50)
    comentario = models.TextField()
    visible = models.BooleanField()

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='SolucionMaterial_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='SolucionMaterial_updated_by', editable=False)

    class Meta:
        verbose_name = 'Solución Material'
        verbose_name_plural = 'Soluciones Materiales'

    def __str__(self):
        return str(self.titulo)


class EstadoSerie(models.Model):
    numero_estado = models.IntegerField()
    descripcion = models.CharField('Descripción', max_length=50)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='EstadoSerie_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='EstadoSerie_updated_by', editable=False)

    class Meta:
        verbose_name = 'Estado Serie'
        verbose_name_plural = 'Estados Serie'

    def __str__(self):
        return str(self.descripcion)

class Serie(models.Model):
    serie_base = models.CharField('Nro. Serie', max_length=200)
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT, blank=True, null=True) #Material
    id_registro = models.IntegerField(blank=True, null=True)
    sociedad = models.ForeignKey(Sociedad, on_delete=models.CASCADE)
    nota_control_calidad_stock_detalle = models.ForeignKey('NotaControlCalidadStockDetalle', on_delete=models.CASCADE, blank=True, null=True)
    serie_movimiento_almacen = models.ManyToManyField(MovimientosAlmacen, blank=True, related_name='Serie_serie_movimiento_almacen')

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Serie_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Serie_updated_by', editable=False)

    objects = SerieManager()

    class Meta:
        verbose_name = 'Serie'
        verbose_name_plural = 'Series'
        ordering = [
            '-created_at',
        ]

    @property
    def producto(self):
        return self.content_type.get_object_for_this_type(id=self.id_registro)

    @property
    def falla(self):
        if self.HistorialEstadoSerie_serie.all():
            return self.HistorialEstadoSerie_serie.all()[0].falla_material
        else:
            return ""

    @property
    def observacion(self):
        if self.HistorialEstadoSerie_serie.all():
            return self.HistorialEstadoSerie_serie.all()[0].observacion
        else:
            return ""

    @property
    def estado(self):
        if self.HistorialEstadoSerie_serie.all():
            return self.HistorialEstadoSerie_serie.latest('created_at').estado_serie.descripcion
        else:
            return ""

    @property
    def numero_estado(self):
        if self.HistorialEstadoSerie_serie.all():
            return self.HistorialEstadoSerie_serie.latest('created_at').estado_serie.numero_estado
        else:
            return ""

    @property
    def ultimo_movimiento(self):
        if self.serie_movimiento_almacen.all():
            return self.serie_movimiento_almacen.latest('created_at')
        else:
            return ""

    @property
    def almacen(self):
        if self.serie_movimiento_almacen.all():
            return self.serie_movimiento_almacen.latest('id').almacen
        else:
            return ""

    @property
    def cliente(self):
        if self.serie_movimiento_almacen.all():
            ultimo_movimiento = self.serie_movimiento_almacen.latest('id')
            if ultimo_movimiento.tipo_stock.descripcion == 'DESPACHADO':
                return self.serie_movimiento_almacen.latest('id').documento_proceso.cliente
        return ""

    @property
    def documento(self):
        if self.serie_movimiento_almacen.all():
            ultimo_movimiento = self.serie_movimiento_almacen.latest('id')
            if ultimo_movimiento.tipo_stock.descripcion == 'DESPACHADO':
                return self.serie_movimiento_almacen.latest('id').documento_proceso
        return ""

    def __str__(self):
        return str(self.serie_base)


class SerieCalidad(models.Model):
    ESTADOS_SERIE_CALIDAD = (
        (1, 'DISPONIBLE'),
        (2, 'DUPLICADO'),
    )
    serie = models.CharField('Nro. Serie', max_length=200)
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT,blank=True, null=True) #Material
    id_registro = models.IntegerField(blank=True, null=True)
    observacion = models.TextField('Observación', blank=True, null=True)
    falla_material = models.ForeignKey(FallaMaterial, on_delete=models.CASCADE, blank=True, null=True)
    nota_control_calidad_stock_detalle = models.ForeignKey('NotaControlCalidadStockDetalle', on_delete=models.CASCADE, related_name='SerieCalidad_nota_control_calidad_stock_detalle')
    estado = models.IntegerField(choices=ESTADOS_SERIE_CALIDAD, default=1)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='SerieCalidad_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='SerieCalidad_updated_by', editable=False)
    class Meta:
        verbose_name = 'Serie Calidad'
        verbose_name_plural = 'Series Calidad'
        ordering = [
            '-created_at',
            ]

    def __str__(self):
        return "%s - %s" % (self.serie, self.nota_control_calidad_detalle)


class HistorialEstadoSerie(models.Model):
    serie = models.ForeignKey(Serie, on_delete=models.CASCADE, related_name='HistorialEstadoSerie_serie')
    estado_serie = models.ForeignKey(EstadoSerie, on_delete=models.CASCADE)
    falla_material = models.ForeignKey(FallaMaterial, on_delete=models.CASCADE, blank=True, null=True)
    solucion = models.ForeignKey(SolucionMaterial, on_delete=models.CASCADE, blank=True, null=True)
    observacion = models.TextField('Observación', blank=True, null=True)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='HistorialEstadoSerie_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='HistorialEstadoSerie_updated_by', editable=False)

    class Meta:
        verbose_name = 'Historial Estado Serie'
        verbose_name_plural = 'Historial Estado Series'
        ordering = [
            'created_at',
            ]

    def __str__(self):
        return str(self.serie)

class NotaControlCalidadStock(models.Model):
    nro_nota_calidad = models.CharField('Nro. Nota Calidad', max_length=50, blank=True, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT,blank=True, null=True) #NotaIngreso / Transformacion SIN QA
    id_registro = models.IntegerField(blank=True, null=True)
    motivo_anulacion = models.TextField('Motivo de Anulación', blank=True, null=True)
    comentario = models.TextField(blank=True, null=True)
    estado = models.IntegerField(choices=ESTADOS_NOTA_CALIDAD_STOCK, default=1)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='NotaControlCalidadStock_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='NotaControlCalidadStock_updated_by', editable=False)

    class Meta:
        verbose_name = 'Nota Control Calidad Stock'
        verbose_name_plural = 'Notas Control Calidad Stock'
        ordering = ['-nro_nota_calidad',]

    @property
    def fecha(self):
        return self.nota_ingreso.fecha

    @property
    def sociedad(self):
        return self.nota_ingreso.sociedad

    @property
    def proveedor(self):
        return self.nota_ingreso.recepcion_compra.proveedor

    @property
    def nota_ingreso(self):
        try:
            return self.content_type.get_object_for_this_type(id = self.id_registro)
        except:
            return ""

    @property
    def documentos(self):
        documentos = []
        documentos.append(self.nota_ingreso.recepcion_compra.__str__())
        return documentos

    def __str__(self):
        return str(self.id)

class NotaControlCalidadStockDetalle(models.Model):
    ESTADOS_INSPECCION = [
    (1, 'BUENO'),
    (2, 'DAÑADO'),
    ]
    item = models.IntegerField(blank=True, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT,blank=True, null=True) #NotaIngresoDetalle / SalidaTransformacionProducto
    id_registro = models.IntegerField(blank=True, null=True)
    cantidad_calidad = models.DecimalField('Cantidad', max_digits=22, decimal_places=10, default=Decimal('0.00'))
    inspeccion = models.IntegerField('Estado Inspección',choices=ESTADOS_INSPECCION, default=1)
    nota_control_calidad_stock = models.ForeignKey(NotaControlCalidadStock, on_delete=models.CASCADE, related_name='NotaControlCalidadStockDetalle_nota_control_calidad_stock')

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='NotaControlCalidadStockDetalle_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='NotaControlCalidadStockDetalle_updated_by', editable=False)

    class Meta:
        verbose_name = 'Nota Control Calidad Stock Detalle'
        verbose_name_plural = 'Notas Control Calidad Stock Detalle'
        ordering = ['item',]

    @property
    def material(self):
        return self.nota_ingreso_detalle.comprobante_compra_detalle.producto
        
    @property
    def control_serie(self):
        return self.material.control_serie      

    @property
    def series_calidad(self):
        return Decimal(len(self.SerieCalidad_nota_control_calidad_stock_detalle.all())).quantize(Decimal('0.01'))

    def __str__(self):
        return str(self.id)


class SerieConsulta(models.Model):
    serie_base = models.CharField('Nro. Serie', max_length=200)
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT, blank=True, null=True) #Documento
    id_registro = models.IntegerField(blank=True, null=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, blank=True, null=True)
    material = models.ForeignKey(Material, on_delete=models.CASCADE, blank=True, null=True)
    sociedad = models.ForeignKey(Sociedad, on_delete=models.CASCADE)
    estado = models.IntegerField(choices=SERIE_CONSULTA)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='SerieConsulta_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='SerieConsulta_updated_by', editable=False)

    class Meta:
        verbose_name = 'Serie Consulta'
        verbose_name_plural = 'Series Consultas'
        ordering = [
            '-created_at'
        ]

    def __str__(self):
        return str(self.serie_base)


class SolicitudConsumoInterno(models.Model):
    ESTADOS_SOLICITUD_CONSUMO = (
        (1, 'BORRADOR'),
        (2, 'EN PROCESO'),
        (3, 'ANULADO'),
        (4, 'POR APROBACIÓN'),
        (5, 'RECHAZADO'),
        (6, 'APROBADO'),
    )
    numero_solicitud = models.IntegerField('Número de Solicitud', blank=True, null=True)
    sociedad = models.ForeignKey(Sociedad, on_delete=models.RESTRICT, blank=True, null=True)
    fecha_solicitud = models.DateField('Fecha Solicitud', auto_now=False, auto_now_add=False, blank=True, null=True)
    fecha_consumo = models.DateField('Fecha Consumo', auto_now=False, auto_now_add=False, blank=True, null=True)
    observacion = models.TextField('Comentario', blank=True, null=True)
    estado = models.IntegerField(choices=ESTADOS_SOLICITUD_CONSUMO, default=1)
    motivo_anulacion = models.TextField(blank=True, null=True)
    solicitante = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='SolicitudConsumoInterno_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='SolicitudConsumoInterno_updated_by', editable=False)

    class Meta:
        verbose_name = 'Solicitud Consumo Interno'
        verbose_name_plural = 'Solicitudes Consumo Interno'
        ordering = [
            '-fecha_solicitud',
            '-numero_solicitud',
        ]

    def __str__(self):
        return "%s - %s - %s" % (self.fecha_solicitud.strftime('%d/%m/%Y'), numeroXn(self.numero_solicitud, 6), self.solicitante)
        


class SolicitudConsumoInternoDetalle(models.Model):
    item = models.IntegerField(blank=True, null=True)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    cantidad = models.DecimalField('Cantidad Consumo', max_digits=22, decimal_places=10, default=Decimal('0.00'))
    sede = models.ForeignKey(Sede, on_delete=models.CASCADE, blank=True, null=True)
    almacen = models.ForeignKey(Almacen, on_delete=models.CASCADE, blank=True, null=True)
    solicitud_consumo = models.ForeignKey(SolicitudConsumoInterno, on_delete=models.CASCADE, related_name='SolicitudConsumoInternoDetalle_solicitud_consumo')

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='SolicitudConsumoInternoDetalle_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='SolicitudConsumoInternoDetalle_updated_by', editable=False)
    
    class Meta:
        verbose_name = 'Solicitud Consumo Interno Detalle'
        verbose_name_plural = 'Solicitudes Consumo Interno Detalles'
        ordering = [
            'solicitud_consumo',
            'item',
            ]

    @property
    def series_validar(self):
        return Decimal(len(self.ValidarSerieSolicitudConsumoInternoDetalle_solicitud_consumo_detalle.all())).quantize(Decimal('0.01'))

    def __str__(self):
        return str(self.solicitud_consumo) + ' | ' + str(self.item)


class ValidarSerieSolicitudConsumoInternoDetalle(models.Model):
    solicitud_consumo_detalle = models.ForeignKey(SolicitudConsumoInternoDetalle, on_delete=models.PROTECT, related_name='ValidarSerieSolicitudConsumoInternoDetalle_solicitud_consumo_detalle')
    serie = models.ForeignKey(Serie, on_delete=models.CASCADE, blank=True, null=True)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='ValidarSerieSolicitudConsumoInternoDetalle_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='ValidarSerieSolicitudConsumoInternoDetalle_updated_by', editable=False)

    class Meta:
        verbose_name = 'Validar Series Solicitud de Consumo Detalle'
        verbose_name_plural = 'Validar Series Solicitudes de Consumo Detalle'
        ordering = [
            'created_at',
            ]

    def __str__(self):
        return "%s - %s" % (self.solicitud_consumo_detalle , str(self.serie))
        

class AprobacionConsumoInterno(models.Model):
    ESTADOS_APROBACION_CONSUMO = (
        (1, 'BORRADOR'),
        (2, 'APROBADO'),
        (3, 'RECHAZADO'),
        (4, 'ANULADO'),
    )
    numero_aprobacion = models.IntegerField('Número de aprobacion', blank=True, null=True)
    solicitud_consumo = models.OneToOneField(SolicitudConsumoInterno, on_delete=models.CASCADE)
    responsable = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True)
    fecha_aprobacion = models.DateField('Fecha aprobacion', auto_now=False, auto_now_add=False, blank=True, null=True)
    observacion = models.TextField('Comentario', blank=True, null=True)
    estado = models.IntegerField(choices=ESTADOS_APROBACION_CONSUMO, default=1)
    motivo_anulacion = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='AprobacionConsumoInterno_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='AprobacionConsumoInterno_updated_by', editable=False)

    class Meta:
        verbose_name = 'Aprobacion de Consumo Interno'
        verbose_name_plural = 'Aprobaciones de Consumo Interno'
        ordering = [
            '-fecha_aprobacion',
            '-numero_aprobacion'
            ]

    @property
    def fecha(self):
        return self.fecha_aprobacion

    @property
    def content_type(self):
        return ContentType.objects.get_for_model(self)

    def __str__(self):
        return "%s - %s - %s" % (self.fecha_aprobacion.strftime('%d/%m/%Y'), numeroXn(self.numero_aprobacion, 6), self.responsable)
        


class AprobacionConsumoInternoDetalle(models.Model):
    item = models.IntegerField(blank=True, null=True)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    cantidad = models.DecimalField('Cantidad Consumo', max_digits=22, decimal_places=10, default=Decimal('0.00'))
    sede = models.ForeignKey(Sede, on_delete=models.CASCADE, blank=True, null=True)
    almacen = models.ForeignKey(Almacen, on_delete=models.CASCADE, blank=True, null=True)
    aprobacion_consumo = models.ForeignKey(AprobacionConsumoInterno, on_delete=models.CASCADE, blank=True, null=True, related_name='AprobacionConsumoInternoDetalle_aprobacion_consumo')

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='AprobacionConsumoInternoDetalle_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='AprobacionConsumoInternoDetalle_updated_by', editable=False)
    
    class Meta:
        verbose_name = 'Aprobacion Consumo Interno Detalle'
        verbose_name_plural = 'Aprobaciones Consumo Interno Detalles'
        ordering = [
            'aprobacion_consumo',
            'item',
            ]

    @property
    def sociedad(self):
        return self.aprobacion_consumo.solicitud_consumo.sociedad

    def __str__(self):
        return str(self.aprobacion_consumo) + ' | ' + str(self.item)


class ReparacionMaterial(models.Model):
    ESTADOS_REPARACION_MATERIAL = (
        (1, 'BORRADOR'),
        (2, 'EN PROCESO'),
        (3, 'CONCLUIDO'),
        (4, 'ANULADO'),
    )
    numero_reparacion = models.IntegerField('Número de Reparación', blank=True, null=True)
    sociedad = models.ForeignKey(Sociedad, on_delete=models.RESTRICT, blank=True, null=True)
    fecha_reparacion_inicio = models.DateField('Fecha inicio de reparación', auto_now=False, auto_now_add=False, blank=True, null=True)
    fecha_reparacion_fin = models.DateField('Fecha fin de reparacion', auto_now=False, auto_now_add=False, blank=True, null=True)
    observacion = models.TextField('Comentario', blank=True, null=True)
    tiempo_estimado = models.IntegerField('Tiempo estimado', default=0, blank=True, null=True)
    estado = models.IntegerField(choices=ESTADOS_REPARACION_MATERIAL, default=1)
    motivo_anulacion = models.TextField(blank=True, null=True)
    responsable = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='ReparacionMaterial_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='ReparacionMaterial_updated_by', editable=False)

    class Meta:
        verbose_name = 'Reparación de Material'
        verbose_name_plural = 'Reparaciónes de Materiales'
        ordering = [
            '-fecha_reparacion_inicio',
            '-numero_reparacion',
        ]

    @property
    def fecha(self):
        return self.fecha_reparacion_fin

    @property
    def content_type(self):
        return ContentType.objects.get_for_model(self)

    def __str__(self):
        return "%s - %s - %s" % (self.fecha_reparacion_inicio.strftime('%d/%m/%Y'), numeroXn(self.numero_reparacion, 6), self.responsable)


class ReparacionMaterialDetalle(models.Model):
    item = models.IntegerField(blank=True, null=True)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    cantidad = models.DecimalField('Cantidad a reparar', max_digits=22, decimal_places=10, default=Decimal('0.00'))
    sede = models.ForeignKey(Sede, on_delete=models.CASCADE, blank=True, null=True)
    almacen = models.ForeignKey(Almacen, on_delete=models.CASCADE, blank=True, null=True)
    reparacion = models.ForeignKey(ReparacionMaterial, on_delete=models.CASCADE, related_name='ReparacionMaterialDetalle_reparacion')

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='ReparacionMaterialDetalle_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='ReparacionMaterialDetalle_updated_by', editable=False)
    
    class Meta:
        verbose_name = 'Reparación de Material Detalle'
        verbose_name_plural = 'Reparaciónes de Materiales Detalles'
        ordering = [
            'reparacion',
            'item',
            ]
    
    @property
    def series_validar(self):
        return Decimal(len(self.ValidarSerieReparacionMaterialDetalle_reparacion_detalle.all())).quantize(Decimal('0.01'))

    def __str__(self):
        return str(self.reparacion) + ' | ' + str(self.item)


class ValidarSerieReparacionMaterialDetalle(models.Model):
    reparacion_detalle = models.ForeignKey(ReparacionMaterialDetalle, on_delete=models.PROTECT, related_name='ValidarSerieReparacionMaterialDetalle_reparacion_detalle')
    serie = models.ForeignKey(Serie, on_delete=models.CASCADE, blank=True, null=True)
    solucion_material = models.ForeignKey(SolucionMaterial, on_delete=models.CASCADE, blank=True, null=True)
    observacion = models.TextField('Observación', blank=True, null=True)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='ValidarSerieReparacionMaterialDetalle_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='ValidarSerieReparacionMaterialDetalle_updated_by', editable=False)

    class Meta:
        verbose_name = 'Validar Series Reparación de Material Detalle'
        verbose_name_plural = 'Validar Series Reparaciones de Materiales Detalles'
        ordering = [
            'created_at',
            ]

    def __str__(self):
        return "%s - %s" % (self.reparacion_detalle , str(self.serie))


class TransformacionProductos(models.Model):
    ESTADOS_TRANSFORMACION_PRODUCTOS = [
        (1, 'EN PROCESO'),
        (2, 'CONCLUIDO'),
        ]
    numero_transformacion = models.IntegerField('Número de Transformación', blank=True, null=True)
    sociedad = models.ForeignKey(Sociedad, on_delete=models.CASCADE,blank=True, null=True)
    fecha_transformacion = models.DateField('Fecha de Transformación', auto_now=False, auto_now_add=True, blank=True, null=True)
    tipo_stock = models.ForeignKey(TipoStock, on_delete=models.CASCADE)
    responsable = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='TransformacionProductos_responsable', verbose_name='Responsable')
    observacion = models.TextField(blank=True, null=True)
    estado = models.IntegerField('Estado', choices=ESTADOS_TRANSFORMACION_PRODUCTOS, default=1)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='TransformacionProductos_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='TransformacionProductos_updated_by', editable=False)
    
    class Meta:
        verbose_name = 'Transformación de Productos'
        verbose_name_plural = 'Transformaciones de Productos'
        ordering = [
            '-numero_transformacion',
        ]

    @property
    def fecha(self):
        return self.fecha_transformacion

    @property
    def detalles(self):
        return self.SalidaTransformacionProductos_transformacion_productos.all()
        
    @property
    def content_type(self):
        return ContentType.objects.get_for_model(self)

    def __str__(self):
        return "%s - %s - %s" % (self.fecha_transformacion.strftime('%d/%m/%Y'), numeroXn(self.id, 6), self.responsable)


class EntradaTransformacionProductos(models.Model):

    item = models.IntegerField(blank=True, null=True)
    material = models.ForeignKey(Material, on_delete=models.CASCADE,blank=True, null=True)
    sede = models.ForeignKey(Sede, on_delete=models.CASCADE, blank=True, null=True)
    almacen = models.ForeignKey(Almacen, on_delete=models.CASCADE, blank=True, null=True)
    cantidad = models.DecimalField('Cantidad', max_digits=22, decimal_places=10, default=Decimal('0.00'))
    transformacion_productos = models.ForeignKey(TransformacionProductos, on_delete=models.CASCADE, related_name='EntradaTransformacionProductos_transformacion_productos')

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='EntradaTransformacionProductos_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='EntradaTransformacionProductos_updated_by', editable=False)
    
    class Meta:
        verbose_name = 'Entrada Transformación de Productos'
        verbose_name_plural = 'Entrada Transformaciones de Productos'
        ordering = ['item',]

    @property
    def series_validar(self):
        return Decimal(len(self.ValidarSerieEntradaTransformacionProductos_entrada_transformacion_productos.all())).quantize(Decimal('0.01'))
    
    def __str__(self):
        return str(self.material)


class SalidaTransformacionProductos(models.Model):

    item = models.IntegerField(blank=True, null=True)
    material = models.ForeignKey(Material, on_delete=models.CASCADE,blank=True, null=True)
    sede = models.ForeignKey(Sede, on_delete=models.CASCADE, blank=True, null=True)
    almacen = models.ForeignKey(Almacen, on_delete=models.CASCADE, blank=True, null=True)
    cantidad = models.DecimalField('Cantidad', max_digits=22, decimal_places=10, default=Decimal('0.00'))
    transformacion_productos = models.ForeignKey(TransformacionProductos, on_delete=models.CASCADE, related_name='SalidaTransformacionProductos_transformacion_productos')

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='SalidaTransformacionProductos_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='SalidaTransformacionProductos_updated_by', editable=False)
    
    class Meta:
        verbose_name = 'Salida Transformación de Productos'
        verbose_name_plural = 'Salida Transformaciones de Productos'
        ordering = ['item',]

    @property
    def series_validar(self):
        return Decimal(len(self.ValidarSerieSalidaTransformacionProductos_salida_transformacion_productos.all())).quantize(Decimal('0.01'))
    
    def __str__(self):
        return str(self.material)
    

class ValidarSerieEntradaTransformacionProductos(models.Model):
    entrada_transformacion_productos = models.ForeignKey(EntradaTransformacionProductos, on_delete=models.PROTECT, related_name='ValidarSerieEntradaTransformacionProductos_entrada_transformacion_productos')
    serie = models.ForeignKey(Serie, on_delete=models.CASCADE, blank=True, null=True)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='ValidarSerieEntradaTransformacionProductos_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='ValidarSerieEntradaTransformacionProductos_updated_by', editable=False)

    class Meta:
        verbose_name = 'Validar Series Entrada Transformacion Productos'
        verbose_name_plural = 'Validar Series Entradas Transformacion Productos'
        ordering = [
            'created_at',
            ]

    def __str__(self):
        return "%s - %s" % (self.entrada_transformacion_productos , str(self.serie))
    

class ValidarSerieSalidaTransformacionProductos(models.Model):
    salida_transformacion_productos = models.ForeignKey(SalidaTransformacionProductos, on_delete=models.PROTECT, related_name='ValidarSerieSalidaTransformacionProductos_salida_transformacion_productos')
    serie = models.ForeignKey(Serie, on_delete=models.CASCADE, blank=True, null=True)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='ValidarSerieSalidaTransformacionProductos_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name='ValidarSerieSalidaTransformacionProductos_updated_by', editable=False)

    class Meta:
        verbose_name = 'Validar Series Salida Transformacion Productos'
        verbose_name_plural = 'Validar Series Salidas Transformacion Productos'
        ordering = [
            'created_at',
            ]

    def __str__(self):
        return "%s - %s" % (self.salida_transformacion_productos , str(self.serie))


def eliminar_serie_post_delete(instance, *args, **kwargs):
    try:
        serie_eliminar = instance.serie
        serie_eliminar.delete()
    except Exception as ex:
        print(ex)


post_delete.connect(eliminar_serie_post_delete, sender=ValidarSerieSalidaTransformacionProductos)
