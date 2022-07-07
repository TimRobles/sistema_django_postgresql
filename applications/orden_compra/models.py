from django.db import models
from applications.sociedad.models import Sociedad
from applications.datos_globales.models import Moneda
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from applications.variables import ESTADOS_ORDEN_COMPRA, INTERNACIONAL_NACIONAL

class OrdenCompra(models.Model):
    internacional_nacional = models.IntegerField('INTERNACIONAL-NACIONAL',choices=INTERNACIONAL_NACIONAL, default=1)
    incoterms = models.IntegerField('INCOTERMS', choices=INTERNACIONAL_NACIONAL, blank=True, null=True)
    numero_orden_compra = models.CharField('Número de Orden Compra', max_length=50, blank=True, null=True)
    oferta_proveedor = models.IntegerField()
    orden_compra_anterior = models.ForeignKey('self', on_delete=models.PROTECT,null=True, blank=True)
    sociedad_id = models.ForeignKey(Sociedad, on_delete=models.PROTECT, related_name='SociedadOrdenCompra',null=True, blank=True)
    fecha_orden = models.DateField('Fecha de Orden', auto_now=False, auto_now_add=False)
    moneda = models.ForeignKey(Moneda, on_delete=models.CASCADE)
    descuento_global = models.DecimalField('Descuento global', max_digits=14, decimal_places=2, default=0)
    total_descuento = models.DecimalField('Total descuento', max_digits=14, decimal_places=2, default=0)
    total_anticipo = models.DecimalField('Total anticipo', max_digits=14, decimal_places=2, default=0)
    total_gravada = models.DecimalField('Total anticipo', max_digits=14, decimal_places=2, default=0)
    total_inafacta = models.DecimalField('Total anticipo', max_digits=14, decimal_places=2, default=0)
    total_exonerada = models.DecimalField('Total descuento', max_digits=14, decimal_places=2, default=0)
    total_igv = models.DecimalField('Total descuento', max_digits=14, decimal_places=2, default=0)
    total_gratuita = models.DecimalField('Total descuento', max_digits=14, decimal_places=2, default=0)
    total_otros_cargos = models.DecimalField('Total descuento', max_digits=14, decimal_places=2, default=0)
    total_isc = models.DecimalField('Total descuento', max_digits=14, decimal_places=2, default=0)
    total = models.DecimalField('Total', max_digits=14, decimal_places=2, default=0)
    slug = models.SlugField(null=True, blank=True)
    archivo = models.FileField('Archivo',upload_to = 'file/orden_compra/', max_length=100, blank=True, null=True)
    condiciones = models.TextField()
    motivo_anulacion = models.TextField()
    motivo_anulacion = models.TextField()
    estado = models.IntegerField('Estado', choices=ESTADOS_ORDEN_COMPRA,default=1)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='OrdenCompra_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='OrdenCompra_updated_by', editable=False)

    class Meta:
        verbose_name = 'OrdenCompra'
        verbose_name_plural = 'OrdenCompras'

    def __str__(self):
        return str(id)


class OrdenCompraDetalle(models.Model):
    item = models.IntegerField(null=True, blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    id_registro = models.IntegerField()
    cantidad = models.DecimalField('Cantidad', max_digits=22, decimal_places=10)
    precio_unitario_sin_igv = models.DecimalField('Precio unitario sin igv', max_digits=22, decimal_places=10,default=0)
    precio_unitario_con_igv = models.DecimalField('Precio unitario con igv', max_digits=22, decimal_places=10,default=0)
    precio_final_con_igv = models.DecimalField('Precio final con igv', max_digits=22, decimal_places=10,default=0)
    descuento = models.DecimalField('Descuento', max_digits=14, decimal_places=2,default=0)
    sub_total = models.DecimalField('Sub Total', max_digits=14, decimal_places=2,default=0)
    igv = models.DecimalField('IGV', max_digits=14, decimal_places=2,default=0)
    total = models.DecimalField('Total', max_digits=14, decimal_places=2,default=0)
    tipo_igv = models.IntegerField()
    orden_compra = models.ForeignKey(OrdenCompra, on_delete=models.CASCADE)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='OrdenCompraDetalle_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='OrdenCompraDetalle_updated_by', editable=False)
   
    class Meta:
        verbose_name = 'OrdenCompraDetalle'
        verbose_name_plural = 'OrdenesCompraDetalle'

    def __str__(self):
        return str(id)
