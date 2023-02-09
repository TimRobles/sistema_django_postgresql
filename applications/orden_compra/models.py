from decimal import Decimal
from django.db import models
from applications.sociedad.models import Sociedad
from applications.oferta_proveedor.models import OfertaProveedor,OfertaProveedorDetalle
from applications.datos_globales.models import Moneda
from applications.proveedores.models import Proveedor, InterlocutorProveedor
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from applications.variables import ESTADOS_ORDEN_COMPRA, INCOTERMS, INTERNACIONAL_NACIONAL, TIPO_IGV_CHOICES
from .managers import OrdenCompraDetalleManager

class OrdenCompra(models.Model):
    internacional_nacional = models.IntegerField('INTERNACIONAL-NACIONAL',choices=INTERNACIONAL_NACIONAL, default=1)
    incoterms = models.IntegerField('INCOTERMS', choices=INCOTERMS, blank=True, null=True)
    numero_orden_compra = models.CharField('Número de Orden Compra', max_length=50, blank=True, null=True)
    oferta_proveedor = models.OneToOneField(OfertaProveedor, on_delete=models.PROTECT, blank=True, null=True, related_name='OrdenCompra_oferta_proveedor')
    orden_compra_anterior = models.OneToOneField('self', on_delete=models.PROTECT,blank=True, null=True, related_name='OrdenCompra_orden_compra_anterior')
    sociedad = models.ForeignKey(Sociedad, on_delete=models.PROTECT, related_name='SociedadOrdenCompra', blank=True, null=True)
    fecha_orden = models.DateField('Fecha de Orden', auto_now=False, auto_now_add=False)
    moneda = models.ForeignKey(Moneda, on_delete=models.PROTECT)
    descuento_global = models.DecimalField('Descuento global', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total_descuento = models.DecimalField('Total descuento', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total_anticipo = models.DecimalField('Total anticipo', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total_gravada = models.DecimalField('Total gravada', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total_inafacta = models.DecimalField('Total inafacta', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total_exonerada = models.DecimalField('Total exonerada', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total_igv = models.DecimalField('Total igv', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total_gratuita = models.DecimalField('Total gratuita', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total_otros_cargos = models.DecimalField('Total otros cargos', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total_isc = models.DecimalField('Total isc', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    total = models.DecimalField('Total', max_digits=14, decimal_places=2, default=Decimal('0.00'))
    slug = models.SlugField(blank=True, null=True)
    archivo = models.FileField('Archivo',upload_to = 'file/orden_compra/', max_length=100, blank=True, null=True)
    condiciones = models.TextField(blank=True, null=True)
    motivo_anulacion = models.TextField(blank=True, null=True)
    proveedor_temporal = models.ForeignKey(Proveedor, verbose_name='Proveedor', on_delete=models.CASCADE, blank=True, null=True)
    interlocutor_temporal = models.ForeignKey(InterlocutorProveedor, on_delete=models.CASCADE, blank=True, null=True)
    estado = models.IntegerField('Estado', choices=ESTADOS_ORDEN_COMPRA,default=1)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='OrdenCompra_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='OrdenCompra_updated_by', editable=False)

    class Meta:
        verbose_name = 'Orden Compra'
        verbose_name_plural = 'Ordenes Compra'
        ordering = [
            '-numero_orden_compra',
            '-created_at',
            ]
            
    @property
    def proveedor(self):
        if self.proveedor_temporal:
            return self.proveedor_temporal
        try:
            return self.oferta_proveedor.requerimiento_material.proveedor
        except:
            try:
                return self.OrdenCompra_orden_compra_anterior.proveedor
            except:
                return None

    @property
    def interlocutor(self):
        if self.interlocutor_temporal:
            return self.interlocutor_temporal
        try:
            return self.oferta_proveedor.requerimiento_material.interlocutor_proveedor
        except:
            try:
                return self.OrdenCompra_orden_compra_anterior.interlocutor
            except:
                return None

    def __str__(self):
        return "%s %s" % (self.id, self.numero_orden_compra)


class OrdenCompraDetalle(models.Model):
    item = models.IntegerField(blank=True, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT) #Material
    id_registro = models.IntegerField()
    cantidad = models.DecimalField('Cantidad', max_digits=22, decimal_places=10, blank=True, null=True)
    precio_unitario_sin_igv = models.DecimalField('Precio unitario sin igv', max_digits=22, decimal_places=10,default=Decimal('0.00'))
    precio_unitario_con_igv = models.DecimalField('Precio unitario con igv', max_digits=22, decimal_places=10,default=Decimal('0.00'))
    precio_final_con_igv = models.DecimalField('Precio final con igv', max_digits=22, decimal_places=10,default=Decimal('0.00'))
    descuento = models.DecimalField('Descuento', max_digits=14, decimal_places=2,default=Decimal('0.00'))
    sub_total = models.DecimalField('Sub Total', max_digits=14, decimal_places=2,default=Decimal('0.00'))
    igv = models.DecimalField('IGV', max_digits=14, decimal_places=2,default=Decimal('0.00'))
    total = models.DecimalField('Total', max_digits=14, decimal_places=2,default=Decimal('0.00'))
    tipo_igv = models.IntegerField('Tipo de IGV', choices=TIPO_IGV_CHOICES, null=True)
    orden_compra = models.ForeignKey(OrdenCompra, on_delete=models.CASCADE,related_name='OrdenCompraDetalle_orden_compra')

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='OrdenCompraDetalle_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='OrdenCompraDetalle_updated_by', editable=False)

    objects = OrdenCompraDetalleManager()
   
    class Meta:
        verbose_name = 'Orden Compra Detalle'
        verbose_name_plural = 'Ordenes Compra Detalle'
        ordering = [
            'orden_compra',
            'item',
            ]
    
    @property
    def producto(self):
        return self.content_type.get_object_for_this_type(id = self.id_registro)

    def __str__(self):
        return "%s" % (str(self.content_type.get_object_for_this_type(id = self.id_registro)))
