from django.db import models
from applications.variables import ESTADOS
from django.contrib.contenttypes.models import ContentType
from applications.datos_globales.models import Moneda
from django.conf import settings

class PrecioListaMaterial(models.Model):
    content_type_producto = models.ForeignKey(ContentType, on_delete=models.PROTECT, related_name='PrecioListaMaterial_content_type_producto')
    id_registro_producto = models.IntegerField()    
    content_type_documento = models.ForeignKey(ContentType, on_delete=models.PROTECT, related_name='PrecioListaMaterial_content_type_documento')
    id_registro_documento = models.IntegerField()
    precio_compra = models.DecimalField('Precio de compra', max_digits=22, decimal_places=10,default=0)
    precio_lista = models.DecimalField('Precio de lista', max_digits=22, decimal_places=10,default=0)
    precio_sin_igv = models.DecimalField('Precio sin igv', max_digits=22, decimal_places=10,default=0)
    moneda = models.ForeignKey(Moneda, on_delete=models.PROTECT)
    logistico = models.DecimalField('Logistico', max_digits=22, decimal_places=10,default=0)
    margen_venta = models.DecimalField('Margen de venta', max_digits=22, decimal_places=10,default=0)
    estado = models.IntegerField('Estado', choices=ESTADOS, default=1)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='PrecioListaMaterial_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='PrecioListaMaterial_updated_by', editable=False)

    class Meta:
        verbose_name = 'PrecioListaMateriales'
        verbose_name_plural = 'PrecioListaMateriales'

    def __str__(self):
        return "%s" % (str(self.content_type_producto.get_object_for_this_type(id = self.id_registro_producto)))

