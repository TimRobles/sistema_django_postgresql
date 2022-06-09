from django.conf import settings
from django.db import models
from applications.proveedores.models import Proveedor, InterlocutorProveedor,ProveedorInterlocutor
from django.contrib.contenttypes.models import ContentType


class RequerimientoMaterial(models.Model):
    ESTADOS_REQUERIMIENTO = (
        (1, 'BORRADOR'),
        (2, 'PENDIENTE'),
        (3, 'ENVIADO'),
    )

    fecha = models.DateField('Fecha', auto_now=False, auto_now_add=True, blank=True, null=True, editable=False)
    titulo = models.CharField('Titulo', max_length=150,null=True, blank=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT, related_name='Proveedor',null=True, blank=True)
    interlocutor_proveedor = models.ForeignKey(InterlocutorProveedor, on_delete=models.PROTECT, related_name='InterlocutorProveedor',null=True, blank=True)
    requerimiento_material_anterior = models.ForeignKey('self', on_delete=models.CASCADE,null=True, blank=True)
    version = models.IntegerField(default=0)
    slug = models.SlugField(null=True, blank=True)
    estado = models.IntegerField('Estado', choices=ESTADOS_REQUERIMIENTO, default=1)

    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='RequerimientoMaterial_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='RequerimientoMaterial_updated_by', editable=False)

    class Meta:
        verbose_name = 'Requerimiento de Material'
        verbose_name_plural = 'Requerimiento de Materiales'
        ordering = [
            '-fecha',
        ]
    def __str__(self):
        return str(self.titulo)

class RequerimientoMaterialDetalle(models.Model):
    item = models.IntegerField(null=True, blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    id_registro = models.IntegerField()
    cantidad = models.DecimalField('Cantidad', max_digits=22, decimal_places=10, null=True, blank=True)
    requerimiento_material = models.ForeignKey(RequerimientoMaterial, on_delete=models.CASCADE, related_name='RequerimientoMaterialDetalle_requerimiento_material')
 
    created_at = models.DateTimeField('Fecha de Creación', auto_now=False, auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='RequerimientoMaterialDetalle_created_by', editable=False)
    updated_at = models.DateTimeField('Fecha de Modificación', auto_now=True, auto_now_add=False, blank=True, null=True, editable=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, blank=True, null=True, related_name='RequerimientoMaterialDetalle_updated_by', editable=False)
  
    class Meta:
        verbose_name = 'Requerimiento de Material Detalle'
        verbose_name_plural = 'Requerimiento de Materiales Detalle'
        ordering = [
            'item',
        ]

    def __str__(self):
        return str(self.cantidad)
