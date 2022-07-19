from django.db import models
from django.conf import settings

from applications.requerimiento_de_materiales.models import RequerimientoMaterialProveedor
from applications.datos_globales.models import Moneda
from applications.material.models import ProveedorMaterial
from applications.variables import INCOTERMS, INTERNACIONAL_NACIONAL, TIPO_IGV_CHOICES

from applications.oferta_proveedor.managers import OfertaProveedorDetalleManager

class OfertaProveedor(models.Model):
    ESTADOS_OFERTA_PROVEEDOR = (
        (1, 'PENDIENTE'),
        (2, 'FINALIZADO'),
    )

    fecha = models.DateField('Fecha', auto_now=False, auto_now_add=True, blank=True, null=True, editable=False)
    internacional_nacional = models.IntegerField('Internacional-Nacional', choices=INTERNACIONAL_NACIONAL, default=1)
    incoterms = models.IntegerField('INCOTERMS', choices=INCOTERMS, blank=True, null=True)
    numero_oferta = models.CharField('Número de Oferta', max_length=50, blank=True, null=True)
    requerimiento_material = models.OneToOneField(RequerimientoMaterialProveedor, on_delete=models.CASCADE)
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
    slug = models.SlugField(null=True, blank=True, editable=False)
    condiciones = models.TextField('Condiciones', null=True, blank=True)
    estado = models.IntegerField('Estado', choices=ESTADOS_OFERTA_PROVEEDOR, default=1)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='OfertaProveedor_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='OfertaProveedor_updated_by', editable=False)

    class Meta:
        verbose_name = 'Oferta Proveedor'
        verbose_name_plural = 'Ofertas Proveedor'
        ordering = [
            '-fecha',
        ]

    def __str__(self):
        return str(self.requerimiento_material)

class OfertaProveedorDetalle(models.Model):

    item = models.IntegerField(null=True, blank=True)
    proveedor_material = models.ForeignKey(ProveedorMaterial, on_delete=models.PROTECT)
    cantidad = models.DecimalField('Cantidad', max_digits=22, decimal_places=10, default=0)
    precio_unitario_sin_igv = models.DecimalField('Precio Unitario sin IGV', max_digits=22, decimal_places=10, default=0)
    precio_unitario_con_igv = models.DecimalField('Precio Unitario con IGV', max_digits=22, decimal_places=10, default=0)
    precio_final_con_igv = models.DecimalField('Precio Final con IGV', max_digits=22, decimal_places=10, default=0)
    descuento = models.DecimalField('Descuento', max_digits=14, decimal_places=2, default=0)
    sub_total = models.DecimalField('Sub Total', max_digits=14, decimal_places=2, default=0)
    igv = models.DecimalField('IGV', max_digits=14, decimal_places=2, default=0)
    total = models.DecimalField('Total', max_digits=14, decimal_places=2, default=0)
    tipo_igv = models.IntegerField('Tipo de IGV', choices=TIPO_IGV_CHOICES, null=True)
    oferta_proveedor = models.ForeignKey(OfertaProveedor, on_delete=models.CASCADE, related_name='OfertaProveedorDetalle_oferta_proveedor')

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='OfertaProveedorDetalle_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='OfertaProveedorDetalle_updated_by', editable=False)

    objects = OfertaProveedorDetalleManager()
    class Meta:
        verbose_name = 'Oferta Proveedor Detalle'
        verbose_name_plural = 'Ofertas Proveedor Detalle'
        ordering = ['item',]

    def __str__(self):
        return str(self.oferta_proveedor)

class ArchivoOfertaProveedor(models.Model):

    archivo = models.FileField('Archivo', null=True, blank=True)
    oferta_proveedor = models.ForeignKey(OfertaProveedor, on_delete=models.PROTECT)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='ArchivoOfertaProveedor_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='ArchivoOfertaProveedor_updated_by', editable=False)

    class Meta:
        verbose_name = 'Archivo Oferta Proveedor'
        verbose_name_plural = 'Archivos Oferta Proveedor'

    def __str__(self):
        return str(self.oferta_proveedor)