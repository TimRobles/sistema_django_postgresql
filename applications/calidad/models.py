from decimal import Decimal
from django.conf import settings
from django.db import models
from django.contrib.contenttypes.models import ContentType
from applications.clientes.models import Cliente
from applications.sociedad.models import Sociedad
from applications.material.models import Material, SubFamilia
from applications.nota_ingreso.models import NotaIngreso, NotaIngresoDetalle
from applications.movimiento_almacen.models import MovimientosAlmacen
from applications.variables import SERIE_CONSULTA

class FallaMaterial(models.Model):
    sub_familia = models.ForeignKey(SubFamilia, on_delete=models.CASCADE)
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
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT,blank=True, null=True) #Material
    id_registro = models.IntegerField(blank=True, null=True)
    sociedad = models.ForeignKey(Sociedad, on_delete=models.CASCADE)
    nota_control_calidad_stock_detalle = models.ForeignKey('NotaControlCalidadStockDetalle', on_delete=models.CASCADE)
    serie_movimiento_almacen = models.ManyToManyField(MovimientosAlmacen)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Serie_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='Serie_updated_by', editable=False)

    class Meta:
        verbose_name = 'Serie'
        verbose_name_plural = 'Series'

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

    def __str__(self):
        return str(self.serie_base)

class HistorialEstadoSerie(models.Model):
    serie = models.ForeignKey(Serie, on_delete=models.CASCADE, related_name='HistorialEstadoSerie_serie')
    estado_serie = models.ForeignKey(EstadoSerie, on_delete=models.CASCADE)
    falla_material = models.ForeignKey(FallaMaterial, on_delete=models.CASCADE,blank=True, null=True)
    observacion = models.TextField('Observación', blank=True, null=True)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='HistorialEstadoSerie_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='HistorialEstadoSerie_updated_by', editable=False)

    class Meta:
        verbose_name = 'Historial Estado Serie'
        verbose_name_plural = 'Historial Estado Series'
        ordering = ['-created_at',]

    def __str__(self):
        return str(self.serie)

class NotaControlCalidadStock(models.Model):
    ESTADOS_NOTA_CALIDAD_STOCK = [
    (1, 'EN PROCESO'),
    (2, 'POR REGISTRAR SERIES'),
    (3, 'CONCLUIDA'),
    (4, 'ANULADA'),
    ]
    nro_nota_calidad = models.CharField('Nro. Nota Calidad', max_length=50, blank=True, null=True)
    nota_ingreso = models.ForeignKey(NotaIngreso, on_delete=models.CASCADE)
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
        ordering = ['nro_nota_calidad',]

    def __str__(self):
        return str(self.id)

class NotaControlCalidadStockDetalle(models.Model):
    ESTADOS_INSPECCION = [
    (1, 'BUENO'),
    (2, 'DAÑADO'),
    ]
    item = models.IntegerField(blank=True, null=True)
    nota_ingreso_detalle = models.ForeignKey(NotaIngresoDetalle, on_delete=models.CASCADE, related_name='NotaControlCalidadStockDetalle_nota_ingreso_detalle')
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
        raiz_material = self.nota_ingreso_detalle.comprobante_compra_detalle.orden_compra_detalle
        material = raiz_material.content_type.get_object_for_this_type(id = raiz_material.id_registro)        
        if raiz_material:
            return material
        else:
            return ""

    @property
    def control_serie(self):
        raiz_material = self.nota_ingreso_detalle.comprobante_compra_detalle.orden_compra_detalle
        material = raiz_material.content_type.get_object_for_this_type(id = raiz_material.id_registro)        
        control_serie = material.control_serie      
        if material:
            return control_serie
        else:
            return ""

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

    def __str__(self):
        return str(self.serie_base)